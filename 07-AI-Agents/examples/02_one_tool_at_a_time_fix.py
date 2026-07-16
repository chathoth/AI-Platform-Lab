"""
Example: 02_one_tool_at_a_time_fix.py

Reproduces the verified failure from docs/08-One-Tool-at-a-Time-A-Verified-Reliability-Lesson.md:
given a condition that ISN'T met (disk usage well under 90%), the
basic agent (01_basic_agent_loop.py) can still call restart_service
because it batches both tool calls into one turn, before observing
the disk usage result. This script runs both the broken and fixed
versions against BOTH cases - the one where a restart is needed and
the one where it isn't - so the fix's correctness is checked in both
directions, not just the one that first exposed the bug.

Run:
    ollama pull llama3.1:8b
    python 02_one_tool_at_a_time_fix.py
"""

import json

from agent_tools import MODEL, TOOL_SCHEMAS, TOOLS, client

GOAL_SHOULD_RESTART = "Check disk usage on db-primary-01, and if it is above 90%, restart the cleanup-service."
GOAL_SHOULD_NOT_RESTART = "Check disk usage on web-node-01, and if it is above 90%, restart the cleanup-service."
# db-primary-01 is at 92% (restart IS justified), web-node-01 is at 41% (restart is NOT justified).


def run_agent_broken(goal: str, max_steps: int = 5) -> tuple[str, list[str]]:
    """Allows the model to batch multiple tool calls into one turn -
    this is the version that produced the verified incorrect restart."""
    messages = [
        {"role": "system", "content": "You are an ops agent. Use tools step by step to accomplish the goal."},
        {"role": "user", "content": goal},
    ]
    tools_called = []
    for _ in range(max_steps):
        response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOL_SCHEMAS, temperature=0)
        msg = response.choices[0].message
        if msg.tool_calls:
            messages.append(msg)
            for call in msg.tool_calls:
                args = json.loads(call.function.arguments)
                tools_called.append(call.function.name)
                result = TOOLS[call.function.name](**args)
                messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
        else:
            return msg.content, tools_called
    return "max steps reached", tools_called


def run_agent_fixed(goal: str, max_steps: int = 6) -> tuple[str, list[str]]:
    """Executes only ONE tool call per turn, even if the model requested
    more - forces a real observe step before every action. Also includes
    a single bounded "nudge": if the model stops without a tool call,
    it gets one chance to confirm the goal is actually complete, rather
    than a half-finished task being silently accepted as done. Without
    this nudge, testing showed the model sometimes stopped after only
    checking disk usage, without following through on a needed restart -
    a different, milder failure than this chapter's main one, but worth
    guarding against too."""
    messages = [
        {"role": "system", "content": "You are an ops agent. Call ONE tool at a time and wait for its result before deciding the next step."},
        {"role": "user", "content": goal},
    ]
    tools_called = []
    nudged = False
    for _ in range(max_steps):
        response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOL_SCHEMAS, temperature=0)
        msg = response.choices[0].message
        if msg.tool_calls:
            messages.append(msg)
            call = msg.tool_calls[0]  # <- the core fix: only the first call, ever
            args = json.loads(call.function.arguments)
            tools_called.append(call.function.name)
            result = TOOLS[call.function.name](**args)
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
        else:
            if not nudged:
                messages.append({"role": "assistant", "content": msg.content})
                messages.append({"role": "user", "content": "If the goal requires another tool call to be fully complete, make that call now. Otherwise, confirm it is complete."})
                nudged = True
                continue
            return msg.content, tools_called
    return "max steps reached", tools_called


def check(label: str, tools_called: list[str], should_restart: bool):
    restarted = "restart_service" in tools_called
    status = "OK" if restarted == should_restart else "WRONG"
    print(f"  [{status}] {label}: tools_called={tools_called}")


if __name__ == "__main__":
    print("--- broken (batches tool calls) ---")
    _, tools_called = run_agent_broken(GOAL_SHOULD_RESTART)
    check("should restart (92%)", tools_called, should_restart=True)
    _, tools_called = run_agent_broken(GOAL_SHOULD_NOT_RESTART)
    check("should NOT restart (41%)", tools_called, should_restart=False)

    print("\n--- fixed (one tool call per turn, plus a bounded completion check) ---")
    _, tools_called = run_agent_fixed(GOAL_SHOULD_RESTART)
    check("should restart (92%)", tools_called, should_restart=True)
    _, tools_called = run_agent_fixed(GOAL_SHOULD_NOT_RESTART)
    check("should NOT restart (41%)", tools_called, should_restart=False)

    print()
    print("The broken version should show [WRONG] on the 41% case - it")
    print("restarts anyway, because it never actually waited to observe")
    print("the disk usage result before also requesting the restart.")
