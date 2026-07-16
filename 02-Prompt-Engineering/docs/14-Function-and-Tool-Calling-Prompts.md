# 14 - Function and Tool-Calling Prompts

## Introduction

Module 01 chapter 17 flagged tool calling as the fix for weak model
arithmetic — instead of computing an answer itself, the model calls a
real function. This chapter covers how that actually gets wired up
through prompting: describing available tools to the model, and
handling the structured "I want to call this function" response it
sends back. This is the mechanism underneath every AI agent (module
07) — worth understanding well before that module, not just when you
get there.

## Learning Objectives

After this chapter I should be able to:

-   Explain how tool/function calling works at the prompt level.
-   Define a tool schema the model can reliably choose to call.
-   Handle the request → tool call → tool result → final answer loop.

------------------------------------------------------------------------

# The Loop, End to End

``` mermaid
flowchart LR
A[User: is disk usage on db-01 critical?] --> B[Model sees tool schemas]
B --> C{Model decides: call get_disk_usage tool}
C --> D[Your code executes the real function]
D --> E[Tool result sent back to model]
E --> F[Model gives final answer using real data]
```

The model never runs code itself — it outputs a structured request
("call this function with these arguments"), your application code
actually executes it, and the result is fed back in as a new message.
This is context injection (chapter 08) with an extra step: instead of
you deciding what data to inject ahead of time, the model decides what
data it needs and asks for it.

## Defining a Tool

``` python
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
```

**Platform analogy:** this schema is an OpenAPI operation definition —
name, description, and a typed parameter schema. The model uses the
`description` fields the same way a developer reads API docs to decide
which endpoint to call and what to pass it — vague descriptions produce
wrong tool choices, the same way vague API docs produce integration
bugs.

## Handling the Response

``` python
def get_disk_usage(hostname: str) -> dict:
    # a real implementation would call your monitoring system
    return {"hostname": hostname, "disk_percent": 92}

response = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "Is disk usage on db-primary-01 critical?"}],
    tools=tools,
)

message = response.choices[0].message

if message.tool_calls:
    for call in message.tool_calls:
        import json
        args = json.loads(call.function.arguments)
        result = get_disk_usage(**args)  # actually execute it - never eval() model output

        # feed the real result back so the model can answer using it
        follow_up = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": "Is disk usage on db-primary-01 critical?"},
                message,
                {"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)},
            ],
        )
        print(follow_up.choices[0].message.content)
```

## The One Rule That Actually Matters Here

The model choosing to call a function is just a **suggestion** — your
code decides whether to actually execute it. Never blindly execute
whatever the model requests, especially for anything with side effects
(deleting a resource, sending a message, running a shell command).
This is the same principle as module 01 chapter 18's "never
`os.system(llm_response)`" rule, applied to structured tool calls
instead of raw text — validate the requested action and its arguments
before running it for real.

``` python
ALLOWED_TOOLS = {"get_disk_usage", "get_pod_status"}  # read-only, safe by design

if call.function.name not in ALLOWED_TOOLS:
    raise ValueError(f"Model requested an unrecognized/unapproved tool: {call.function.name}")
```

## Hands-on: Give the Model a Real Tool

Wire up the `get_disk_usage` example above against a local Ollama model
that supports tool calling (`llama3.1:8b` does). Ask "is db-primary-01
close to running out of disk?" and confirm the model actually issues a
`get_disk_usage` tool call rather than guessing a number — then try
asking something the tool can't answer ("what's the weather today?")
and confirm it does *not* force an irrelevant tool call.

## Common Misconceptions

❌ Tool calling means the model executes code.
(The model only requests a call with arguments — your application code
decides whether and how to actually run it.)

❌ If a tool is defined, the model will always use it correctly.
(A vague `description` field produces wrong tool selection or malformed
arguments just as reliably as vague prose instructions do — write tool
descriptions with the same care as chapter 09's instruction clarity.)

✔ Every tool call request from a model should be validated against an
allowlist and its arguments checked before execution — treat it exactly
like any other untrusted structured input.

## Interview Questions

1.  Walk through the full loop from user question to a tool-informed
    final answer.
2.  Why doesn't the model actually execute the function it "calls"?
3.  What's the risk of executing a tool call without validating it
    first, and how would you mitigate it?
4.  Why does a tool's `description` field matter as much as a prompt
    instruction's wording?

## Summary

Tool calling lets a model request that your code run a real function
and hand back the result, closing the gap between "plausible-sounding
answer" and "answer grounded in real data" — the same context-injection
idea from chapter 08, initiated by the model instead of you. The model's
request is a suggestion, not an execution — validating it against an
allowlist before running it is what keeps this safe, and it's the
mechanism every AI agent (module 07) is built on.

## Next Chapter

➡️ `15-Prompt-Injection-and-Security.md`
