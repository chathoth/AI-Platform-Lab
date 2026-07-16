"""
Example: 06_tracing.py

A full, step-by-step trace of an agent run - tool calls, results, and
latency per step. Run against chapter 08's exact failing scenario to
show how a trace makes the bug findable at all. Ties back to
docs/14-Observability-Tracing-an-Agents-Steps.md.

Run:
    ollama pull llama3.1:8b
    python 06_tracing.py
"""

import json
import time

from agent_tools import MODEL, TOOL_SCHEMAS, TOOLS, client


def run_agent_traced(goal: str, max_steps: int = 5) -> tuple[str, list[dict]]:
    trace = []
    messages = [
        {"role": "system", "content": "You are an ops agent. Use tools step by step."},
        {"role": "user", "content": goal},
    ]
    for step in range(max_steps):
        start = time.time()
        response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOL_SCHEMAS, temperature=0)
        msg = response.choices[0].message
        latency = time.time() - start

        if msg.tool_calls:
            messages.append(msg)
            for call in msg.tool_calls:
                args = json.loads(call.function.arguments)
                result = TOOLS[call.function.name](**args)
                messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
                trace.append({
                    "step": step, "type": "tool_call", "tool": call.function.name,
                    "args": args, "result": result, "latency_s": round(latency, 2),
                })
        else:
            trace.append({"step": step, "type": "final_answer", "content": msg.content, "latency_s": round(latency, 2)})
            return msg.content, trace
    trace.append({"step": max_steps, "type": "max_steps_reached"})
    return "max steps reached", trace


if __name__ == "__main__":
    # This is the original (unfixed) loop, on purpose - allowing
    # multiple tool calls per turn, so the trace can reveal exactly
    # where the bug happens.
    goal = "Check disk usage on web-node-01, and if it is above 90%, restart the cleanup-service."
    answer, trace = run_agent_traced(goal)

    print(f"Goal: {goal}\n")
    print("Full trace:")
    print(json.dumps(trace, indent=2))
    print(f"\nFinal answer: {answer}")

    restart_entries = [t for t in trace if t.get("tool") == "restart_service"]
    if restart_entries:
        print("\nLook at the trace: restart_service was called in the SAME step")
        print("as get_disk_usage - meaning it happened before the 41% result was")
        print("actually available to reason about. That's the whole bug, visible")
        print("directly in the trace, not just inferred from the final answer.")
