"""
Example: 08_tool_calling.py

Give the model a real tool (a function it can request, not execute)
and complete the request -> tool call -> tool result -> final answer
loop. Ties back to docs/14-Function-and-Tool-Calling-Prompts.md.

Run:
    ollama pull llama3.1:8b   # supports tool calling
    python 08_tool_calling.py
"""

import json

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

# A read-only, allowlisted tool - safe by design even if a model
# somewhere in the pipeline is fed untrusted content (see chapter 15).
ALLOWED_TOOLS = {"get_disk_usage"}

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_disk_usage",
            "description": "Get current disk usage percentage for a given host.",
            "parameters": {
                "type": "object",
                "properties": {
                    "hostname": {"type": "string", "description": "The hostname to check, e.g. db-primary-01"},
                },
                "required": ["hostname"],
            },
        },
    }
]


def get_disk_usage(hostname: str) -> dict:
    # Stand-in for a real monitoring API call.
    fake_data = {"db-primary-01": 92, "web-node-01": 41}
    return {"hostname": hostname, "disk_percent": fake_data.get(hostname, 50)}


def ask_with_tools(question: str) -> str:
    messages = [{"role": "user", "content": question}]

    response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
    message = response.choices[0].message

    if not message.tool_calls:
        return message.content  # model answered directly, no tool needed

    messages.append(message)
    for call in message.tool_calls:
        if call.function.name not in ALLOWED_TOOLS:
            raise ValueError(f"Model requested an unapproved tool: {call.function.name}")

        args = json.loads(call.function.arguments)
        result = get_disk_usage(**args)  # actually execute it ourselves - never eval() model output
        print(f"  [tool call] get_disk_usage({args}) -> {result}")

        messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})

    follow_up = client.chat.completions.create(model=MODEL, messages=messages)
    return follow_up.choices[0].message.content


if __name__ == "__main__":
    print(ask_with_tools("Is disk usage on db-primary-01 critical?"))
    print()
    # A question the tool can't help with - the model should NOT force
    # an irrelevant tool call here.
    print(ask_with_tools("What is a Kubernetes readiness probe?"))
