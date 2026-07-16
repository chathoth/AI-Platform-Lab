"""
Example: 03_stopping_conditions.py

Add a hard step limit, a token budget, and repetition detection to
an agent loop. Ties back to
docs/09-Stopping-Conditions-and-Loop-Limits.md.

Run:
    ollama pull llama3.1:8b
    pip install openai tiktoken
    python 03_stopping_conditions.py
"""

import json

import tiktoken

from agent_tools import MODEL, TOOL_SCHEMAS, TOOLS, client

enc = tiktoken.encoding_for_model("gpt-4")


def total_tokens(messages: list) -> int:
    # messages is a mix of plain dicts (what we append) and raw
    # ChatCompletionMessage objects (what the API returns for an
    # assistant turn with tool calls) - .get() only works on the dicts.
    total = 0
    for m in messages:
        content = m.get("content", "") if isinstance(m, dict) else (m.content or "")
        total += len(enc.encode(str(content)))
    return total


def is_repeating(tool_call_history: list[str], window: int = 4) -> bool:
    if len(tool_call_history) < window:
        return False
    recent = tool_call_history[-window:]
    return len(set(recent)) <= 2


def run_agent_bounded(goal: str, max_steps: int = 5, max_tokens_budget: int = 8000) -> str:
    messages = [
        {"role": "system", "content": "You are an ops agent. Call ONE tool at a time."},
        {"role": "user", "content": goal},
    ]
    tool_call_history = []

    for step in range(max_steps):
        if total_tokens(messages) > max_tokens_budget:
            return f"stopped: token budget ({max_tokens_budget}) exceeded"

        response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOL_SCHEMAS, temperature=0)
        msg = response.choices[0].message

        if msg.tool_calls:
            messages.append(msg)
            call = msg.tool_calls[0]
            tool_call_history.append(call.function.name)

            if is_repeating(tool_call_history):
                return "stopped: agent appears to be stuck repeating the same actions"

            args = json.loads(call.function.arguments)
            result = TOOLS[call.function.name](**args)
            print(f"  [step {step + 1}] {call.function.name}({args}) -> {result}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
        else:
            return msg.content

    return "stopped: max steps reached without a final answer"


if __name__ == "__main__":
    print("--- a goal no tool can actually solve ---")
    print("(the model may decline directly, or loop until max_steps - either way, this call returns)")
    result = run_agent_bounded("Investigate why the sky is blue and fix it.", max_steps=3)
    print(f"Result: {result}")

    print("\n--- a normal goal, should finish well within the limit ---")
    result = run_agent_bounded("Check disk usage on db-primary-01.", max_steps=5)
    print(f"Result: {result}")
