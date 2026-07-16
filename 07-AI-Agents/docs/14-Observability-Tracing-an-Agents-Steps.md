# 14 - Observability: Tracing an Agent's Steps

## Introduction

Chapter 08's failure was only findable because every step of that
agent's run was printed and readable. In a real system, that
visibility has to be deliberate — module 01 chapter 16's "log the
fully assembled prompt" lesson, extended to a whole multi-turn loop
instead of one call.

## Learning Objectives

After this chapter I should be able to:

-   Log every reasoning, action, and observation step in an agent run.
-   Explain why a full trace matters more for agents than for a
    single LLM call.
-   Build a minimal trace you could actually debug from.

------------------------------------------------------------------------

# Why This Matters More for Agents

A single LLM call has one input and one output to inspect. An agent
run has a whole sequence of decisions, any one of which could be where
something went wrong — chapter 08's mistake happened on a specific
turn, and finding it required seeing that turn's tool calls *and* the
result *and* what the model did next. Without a trace, all you'd see is
the final (wrong) answer, with no way to tell which step actually
caused it.

## A Minimal Trace

``` python
import json
import time

def run_agent_traced(goal: str, max_steps: int = 5) -> tuple[str, list[dict]]:
    trace = []
    messages = [
        {"role": "system", "content": "You are an ops agent..."},
        {"role": "user", "content": goal},
    ]
    for step in range(max_steps):
        start = time.time()
        response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOL_SCHEMAS)
        msg = response.choices[0].message
        latency = time.time() - start

        if msg.tool_calls:
            messages.append(msg)
            call = msg.tool_calls[0]
            args = json.loads(call.function.arguments)
            result = TOOLS[call.function.name](**args)
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
            trace.append({"step": step, "type": "tool_call", "tool": call.function.name, "args": args, "result": result, "latency_s": round(latency, 2)})
        else:
            trace.append({"step": step, "type": "final_answer", "content": msg.content, "latency_s": round(latency, 2)})
            return msg.content, trace
    trace.append({"step": max_steps, "type": "max_steps_reached"})
    return "max steps reached", trace
```

Running chapter 08's exact scenario through this produces a trace that
makes the mistake visible immediately — step 0 shows
`restart_service` called with a 41% result already on record, which is
the whole bug, right there in the log.

## What to Log, at Minimum

  Field                Why it matters
  ---------------------- --------------------------------------
  Step number               Order matters for understanding a sequence
  Tool called + arguments    Exactly what the agent decided to do
  Tool result                  What it actually observed
  Latency per step               Cost/performance debugging (chapter 17)
  Final answer or stop reason      Did it finish normally, or hit a limit (chapter 09)?

**Platform analogy:** this is distributed tracing for a multi-service
request — each span (here, each turn) records what happened and how
long it took, so a slow or incorrect request can be diagnosed by
looking at exactly which span misbehaved, instead of only seeing the
overall (wrong or slow) final result.

## Hands-on: Trace Chapter 08's Exact Failure

Run `run_agent_traced()` against the `web-node-01` scenario from
chapter 08, using the original (unfixed) loop that allows multiple
tool calls per turn. Print the trace and confirm you can identify,
from the trace alone, exactly which step contains the unjustified
`restart_service` call — this is the debugging workflow a real
incident review of an agent's bad decision would actually use.

## Common Misconceptions

❌ Printing the final answer is enough to debug an agent.
(The final answer doesn't show which of several steps actually caused
a problem — chapter 08's mistake was only findable by looking at the
full turn-by-turn trace.)

❌ Tracing is only useful after something goes wrong.
(It's equally useful for chapter 17's cost/latency analysis and
chapter 15's evaluation — a trace is the raw data multiple other
chapters build on, not just an incident-response tool.)

✔ A trace should let you answer "what did the agent see, and what did
it decide, at every single step" — anything less makes debugging a
specific wrong decision far harder than it needs to be.

## Interview Questions

1.  Why does an agent need step-by-step tracing more than a single
    LLM call does?
2.  What fields should a minimal agent trace include?
3.  How would a trace have made chapter 08's bug easier to find?
4.  How is agent tracing similar to distributed tracing for a
    multi-service request?

## Summary

An agent's trace should record every step's tool call, arguments,
result, and latency — the same "log the real request, not just the
final output" discipline from module 01 chapter 16, extended across a
whole multi-turn loop. Without it, a bad decision buried in the middle
of a run (like chapter 08's) is nearly impossible to diagnose from the
final answer alone.

## Next Chapter

➡️ `15-Evaluating-Agent-Performance.md`
