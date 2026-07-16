# 07 - Building a Minimal Agent From Scratch

## Introduction

Every chapter so far has been building toward this one: a complete,
working agent loop, in plain Python, verified against a real local
model. No framework — just the reason-act-observe loop from chapter 02,
written out directly, so nothing about how it works is hidden.

## Learning Objectives

After this chapter I should be able to:

-   Write a complete agent loop in under 40 lines of Python.
-   Trace exactly what happens on each turn.
-   Run it against a real local model and read its actual behavior.

------------------------------------------------------------------------

# The Complete, Verified Agent

``` python
import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

def get_disk_usage(hostname: str) -> dict:
    known = {"db-primary-01": 92, "web-node-01": 41}
    return {"hostname": hostname, "disk_percent": known.get(hostname, 50)}

def restart_service(service_name: str) -> dict:
    return {"service": service_name, "status": "restarted"}

TOOLS = {"get_disk_usage": get_disk_usage, "restart_service": restart_service}

TOOL_SCHEMAS = [
    {"type": "function", "function": {
        "name": "get_disk_usage",
        "description": "Get current disk usage percentage for a host.",
        "parameters": {"type": "object", "properties": {"hostname": {"type": "string"}}, "required": ["hostname"]},
    }},
    {"type": "function", "function": {
        "name": "restart_service",
        "description": "Restart a named service.",
        "parameters": {"type": "object", "properties": {"service_name": {"type": "string"}}, "required": ["service_name"]},
    }},
]

def run_agent(goal: str, max_steps: int = 5) -> str:
    messages = [
        {"role": "system", "content": "You are an ops agent. Use tools step by step to accomplish the goal. When done, reply with a final answer and no tool call."},
        {"role": "user", "content": goal},
    ]
    for step in range(max_steps):
        response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOL_SCHEMAS)
        msg = response.choices[0].message

        if msg.tool_calls:
            messages.append(msg)
            for call in msg.tool_calls:
                args = json.loads(call.function.arguments)
                result = TOOLS[call.function.name](**args)
                messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
        else:
            return msg.content
    return "max steps reached without a final answer"
```

This is verified, real code — the exact agent used to test the
behavior chapter 08 covers next.

## Reading What Happens, Turn by Turn

``` text
run_agent("Check disk usage on db-primary-01, and if it's above 90%, restart the cleanup-service.")
```

Verified output from a real run:

``` text
turn 1: model calls get_disk_usage("db-primary-01") -> {"disk_percent": 92}
        model ALSO calls restart_service("cleanup-service") -> {"status": "restarted"}
        (both in the same turn - chapter 08 covers exactly why that's worth noticing)
turn 2: model gives a final answer summarizing what it did
```

Every line of this maps directly onto chapter 02's loop: turn 1 is
reason (decide to check disk usage) → act (call it) → observe (read
92%) → reason again (that's high, restart) → act → observe, all within
one turn because the model chose to request two tool calls at once;
turn 2 is the final reason step that produces an answer instead of
another action.

## Why This Is All It Takes

Compare this to module 02 chapter 14's single tool call — the only new
code here is the `for step in range(max_steps)` loop and an `if/else`
checking whether the model wants to call a tool or is ready to answer.
Everything else (the client, the tool schemas, the message list) is
identical to what module 02 already covered. The "agent" part is
entirely in that loop structure.

## Hands-on: Run It Yourself

``` bash
ollama pull llama3.1:8b
pip install openai
```

Run the exact code above with the goal string shown. Then try a
different goal — `"Check disk usage on web-node-01, and if it's above
90%, restart the cleanup-service."` — and watch what happens when the
condition *shouldn't* trigger the restart. Don't skip this: chapter 08
is built entirely around what a real run of this second case revealed.

## Common Misconceptions

❌ Building an agent requires a framework like LangChain from the
start.
(This complete, working example is under 40 lines of plain Python — a
framework, covered in module 09, adds convenience for larger systems,
not the core capability.)

❌ The loop needs to be complicated to work correctly.
(The loop itself — check for tool calls, execute them, append results,
repeat — is genuinely this simple. What's *not* simple, covered next in
chapter 08, is trusting the model to reason correctly inside that
loop.)

✔ This exact code is the reference implementation the rest of this
module builds on — every later chapter (stopping conditions, guardrails,
observability) is an addition to this same core loop, not a
replacement for it.

## Interview Questions

1.  Walk through what `run_agent()` does, turn by turn.
2.  What's the only genuinely new code here, compared to module 02
    chapter 14's single tool call?
3.  Why does the loop check `if msg.tool_calls` instead of always
    treating the response as a final answer?
4.  What happens if the model never stops requesting tool calls within
    `max_steps` turns?

## Summary

A complete, working agent loop is a `for` loop around module 02
chapter 14's tool-calling pattern: check whether the model wants to
call a tool, execute it if so, append the result, and repeat until it
gives a final answer instead. This chapter's code is real and verified
— run it yourself before moving to chapter 08, which is built entirely
around a real finding from running this exact loop.

## Next Chapter

➡️ `08-One-Tool-at-a-Time-A-Verified-Reliability-Lesson.md`
