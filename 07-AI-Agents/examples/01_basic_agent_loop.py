"""
Example: 01_basic_agent_loop.py

A complete, minimal reason-act-observe agent loop - allows the model
to request multiple tool calls in one turn. Ties back to
docs/07-Building-a-Minimal-Agent-From-Scratch.md.

This version has a known, verified reliability issue - see
02_one_tool_at_a_time_fix.py and docs/08 for the real fix.

Run:
    ollama pull llama3.1:8b
    pip install openai
    python 01_basic_agent_loop.py
"""

import json

from agent_tools import MODEL, TOOL_SCHEMAS, TOOLS, client


def run_agent(goal: str, max_steps: int = 5) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are an ops agent. Use tools step by step to accomplish "
                "the goal. When done, reply with a final answer and no tool call."
            ),
        },
        {"role": "user", "content": goal},
    ]
    for step in range(max_steps):
        response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOL_SCHEMAS, temperature=0)
        msg = response.choices[0].message

        if msg.tool_calls:
            messages.append(msg)
            for call in msg.tool_calls:
                args = json.loads(call.function.arguments)
                print(f"  [step {step + 1}] tool call: {call.function.name}({args})")
                result = TOOLS[call.function.name](**args)
                print(f"  [step {step + 1}] tool result: {result}")
                messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
        else:
            return msg.content
    return "max steps reached without a final answer"


if __name__ == "__main__":
    print("Goal: check disk usage on db-primary-01 (92%), restart if above 90%\n")
    answer = run_agent(
        "Check disk usage on db-primary-01, and if it's above 90%, restart the cleanup-service."
    )
    print(f"\nFinal answer: {answer}")
