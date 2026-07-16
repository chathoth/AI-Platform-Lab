"""
Example: 09_multi_agent_supervisor.py

A minimal supervisor pattern: one call routes a request to one of two
narrower worker agents, each with its own small tool set. Ties back
to docs/11-Multi-Agent-Systems.md and docs/12-Orchestration-Patterns.md.

Run:
    ollama pull llama3.1:8b
    python 09_multi_agent_supervisor.py
"""

import json

from agent_tools import MODEL, TOOLS, client

DIAGNOSIS_TOOLS = ["get_disk_usage", "list_large_files"]
REMEDIATION_TOOLS = ["restart_service"]

DIAGNOSIS_SCHEMAS = [
    {"type": "function", "function": {"name": "get_disk_usage", "description": "Get current disk usage percentage for a host.",
        "parameters": {"type": "object", "properties": {"hostname": {"type": "string"}}, "required": ["hostname"]}}},
    {"type": "function", "function": {"name": "list_large_files", "description": "List the largest files or directories on a host.",
        "parameters": {"type": "object", "properties": {"hostname": {"type": "string"}}, "required": ["hostname"]}}},
]
REMEDIATION_SCHEMAS = [
    {"type": "function", "function": {"name": "restart_service", "description": "Restart a named service.",
        "parameters": {"type": "object", "properties": {"service_name": {"type": "string"}}, "required": ["service_name"]}}},
]


def run_worker(goal: str, schemas: list[dict], max_steps: int = 3) -> str:
    messages = [{"role": "user", "content": goal}]
    for _ in range(max_steps):
        response = client.chat.completions.create(model=MODEL, messages=messages, tools=schemas, temperature=0)
        msg = response.choices[0].message
        if msg.tool_calls:
            messages.append(msg)
            call = msg.tool_calls[0]
            args = json.loads(call.function.arguments)
            result = TOOLS[call.function.name](**args)
            print(f"    [worker] {call.function.name}({args}) -> {result}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
        else:
            return msg.content
    return "worker: max steps reached"


def diagnosis_agent(goal: str) -> str:
    return run_worker(goal, DIAGNOSIS_SCHEMAS)


def remediation_agent(goal: str) -> str:
    return run_worker(goal, REMEDIATION_SCHEMAS)


ROUTING_PROMPT = """Classify the request as DIAGNOSIS (checking status, investigating,
read-only) or REMEDIATION (taking a corrective action, changing state).

Request: "Check disk usage on web-node-01"
Answer: DIAGNOSIS

Request: "Restart the payment service"
Answer: REMEDIATION

Request: "List the largest files on db-primary-01"
Answer: DIAGNOSIS

Request: "{goal}"
Answer:"""


def supervisor(goal: str) -> str:
    # A plain "DIAGNOSIS or REMEDIATION?" prompt with no examples
    # misclassified "Restart the cleanup-service" as DIAGNOSIS in
    # testing - a few-shot prompt (module 02 chapter 03) fixed it.
    routing = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": ROUTING_PROMPT.format(goal=goal)}],
        temperature=0,
    ).choices[0].message.content.strip().upper()

    print(f"  [supervisor] routed to: {routing}")
    if "REMEDIATION" in routing:
        return remediation_agent(goal)
    return diagnosis_agent(goal)


if __name__ == "__main__":
    print("--- request 1: a diagnosis-shaped task ---")
    print(supervisor("Check disk usage on db-primary-01."))

    print("\n--- request 2: a remediation-shaped task ---")
    print(supervisor("Restart the cleanup-service on db-primary-01."))
