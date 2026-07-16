"""
agent.py

The Runbook Ops Assistant: RAG over data/runbooks/ (module 05) feeding
a guarded agent loop (module 07) that can actually act on what it
retrieves, instead of just answering questions about it.

Two things from module 07 are reused deliberately, not reinvented:
  1. The one-tool-at-a-time fix (chapter 08) - the model executes only
     ONE tool call per turn, so it always observes a result before
     deciding the next action.
  2. Guardrails enforced in code (chapter 13) - an allowlist (which
     role may call which tool) and a confirmation gate for destructive
     tools, checked in execute_tool() itself, not left to the model's
     own judgment about whether an action is safe.

Run:
    ollama pull nomic-embed-text
    ollama pull llama3.1:8b
    pip install chromadb requests openai
    python src/index_runbooks.py     # once, to build the runbook collection
    python src/agent.py
"""

import json

import chromadb

from index_runbooks import DB_PATH, OllamaEmbeddingFunction
from tools import DESTRUCTIVE_TOOLS, MODEL, TOOL_SCHEMAS, TOOLS, client


def retrieve_runbook(query: str) -> tuple[str, str]:
    """RAG step: find the single most relevant runbook for this
    request. Returns (source_filename, runbook_text)."""
    db = chromadb.PersistentClient(path=str(DB_PATH))
    collection = db.get_collection(name="runbooks", embedding_function=OllamaEmbeddingFunction())
    results = collection.query(query_texts=[query], n_results=1)
    return results["metadatas"][0][0]["source"], results["documents"][0][0]


def execute_tool(name: str, args: dict, caller_role: str, auto_confirm: bool | None) -> dict:
    """The guardrail layer from module 07 chapter 13, applied here.
    auto_confirm lets demo runs be non-interactive; a real system
    would always prompt a human for destructive actions."""
    if name in DESTRUCTIVE_TOOLS:
        if caller_role != "operator":
            return {"error": True, "message": f"{name} requires the 'operator' role. Caller was {caller_role!r}."}
        if auto_confirm is None:
            confirmed = input(f"Agent wants to call {name}({args}). Allow? [y/N] ").lower() == "y"
        else:
            confirmed = auto_confirm
        if not confirmed:
            return {"error": True, "message": "Action declined by human reviewer."}
    return TOOLS[name](**args)


def run_ops_assistant(
    request: str,
    caller_role: str = "operator",
    auto_confirm: bool | None = None,
    max_steps: int = 10,
) -> tuple[str, list[str]]:
    source, runbook_text = retrieve_runbook(request)
    print(f"[retrieved runbook: {source}]\n")

    messages = [
        {
            "role": "system",
            "content": (
                "You are an ops assistant. Use the runbook below to decide what to "
                "do. Call ONE tool at a time and wait for its result before deciding "
                "the next step. Follow the runbook's safety notes exactly - do not "
                "call a destructive tool unless its stated condition is confirmed by "
                "an actual tool result in this conversation.\n\n"
                f"--- RUNBOOK: {source} ---\n{runbook_text}"
            ),
        },
        {"role": "user", "content": request},
    ]

    # A single one-shot nudge (module 07 chapter 08) was enough for a
    # 1-2 step goal. Verified against this runbook's multi-step
    # sequence (check usage -> list files -> clean up -> re-check),
    # llama3.1:8b reliably STOPPED and narrated the next action as
    # text ("Let's call cleanup_old_logs...") instead of issuing a
    # real tool call. Worse: a generic nudge ("make a real tool call
    # now") often made it treat its OWN narration as if the action had
    # already happened, and it skipped straight to the next runbook
    # step instead of actually calling the tool it had just described.
    # This matters more here than in module 07: if that narrated,
    # never-executed destructive action were ever treated as "done" by
    # surrounding code, it would bypass execute_tool()'s guardrail
    # entirely, since the guardrail only runs on real tool calls.
    #
    # Fix verified to work reliably: when the model stops without a
    # tool call, check whether its text named one of our known tools,
    # and nudge for THAT specific tool by name, rather than a generic
    # "continue" nudge. Bounded to MAX_NUDGES per step so a genuinely
    # confused model still surfaces to the caller instead of looping.
    MAX_NUDGES = 2

    def build_nudge(narrated_text: str) -> str:
        mentioned = [t for t in TOOLS if t in (narrated_text or "")]
        if mentioned:
            return (
                f"You said you would call {mentioned[-1]}. Make that exact tool "
                "call now - do not just describe it in text."
            )
        return "Make your next action a real tool call, not text. If the runbook is complete, reply DONE."

    tools_called = []
    nudges_used = 0
    last_call = None  # (name, args) of the previous call, to catch exact repeats
    response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOL_SCHEMAS, temperature=0)
    msg = response.choices[0].message
    for _ in range(max_steps):
        if msg.tool_calls:
            messages.append(msg)
            call = msg.tool_calls[0]  # one tool call per turn - module 07 chapter 08's fix
            args = json.loads(call.function.arguments)
            tools_called.append(call.function.name)
            result = execute_tool(call.function.name, args, caller_role, auto_confirm)
            print(f"  -> {call.function.name}({args}) = {result}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})

            # Verified: after a step succeeds, the model sometimes calls
            # the exact same tool with the exact same args again instead
            # of recognizing the runbook is done - a redundant re-check
            # loop. And a guardrail decline alone isn't enough either:
            # the model will happily retry the exact same DENIED call
            # rather than accept "no". Both are the same underlying
            # problem (repeating a call that already produced its
            # answer), so both are caught by the same check: stop on the
            # second identical call instead of letting it repeat.
            this_call = (call.function.name, json.dumps(args, sort_keys=True))
            if this_call == last_call:
                if result.get("error"):
                    return f"STOPPED: {call.function.name} was denied twice - not retrying further. Escalate to a human operator.", tools_called
                return "Runbook actions complete (repeated an identical call, stopping instead of looping).", tools_called
            last_call = this_call
            nudges_used = 0  # a real action happened - reset the nudge budget for the next step
        else:
            if msg.content and msg.content.strip().upper() == "DONE":
                return msg.content, tools_called
            if nudges_used >= MAX_NUDGES:
                return f"NEEDS HUMAN REVIEW (stalled without confirming completion): {msg.content}", tools_called
            messages.append({"role": "assistant", "content": msg.content})
            messages.append({"role": "user", "content": build_nudge(msg.content)})
            nudges_used += 1
        response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOL_SCHEMAS, temperature=0)
        msg = response.choices[0].message
    return f"NEEDS HUMAN REVIEW (max steps reached): {msg.content}", tools_called


if __name__ == "__main__":
    request = "Disk usage alert fired for db-replica-03. What should I do?"

    print("=== Scenario 1: operator role, action approved ===\n")
    final, tools_called = run_ops_assistant(request, caller_role="operator", auto_confirm=True)
    print(f"\nFinal response: {final}")
    print(f"Tools called: {tools_called}\n")

    print("=== Scenario 2: operator role, action declined by human reviewer ===\n")
    final, tools_called = run_ops_assistant(request, caller_role="operator", auto_confirm=False)
    print(f"\nFinal response: {final}")
    print(f"Tools called: {tools_called}\n")

    print("=== Scenario 3: readonly role - allowlist blocks it before confirmation is even asked ===\n")
    final, tools_called = run_ops_assistant(request, caller_role="readonly", auto_confirm=True)
    print(f"\nFinal response: {final}")
    print(f"Tools called: {tools_called}")
