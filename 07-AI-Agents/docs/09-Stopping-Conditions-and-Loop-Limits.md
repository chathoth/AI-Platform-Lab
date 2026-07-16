# 09 - Stopping Conditions and Loop Limits

## Introduction

Chapter 07's `max_steps` parameter got a one-line mention and deserves
a full chapter — an agent loop with no limit is a genuine operational
risk, not just a theoretical one. This chapter covers the ways a loop
can fail to stop, and the concrete limits that keep it bounded.

## Learning Objectives

After this chapter I should be able to:

-   Explain the ways an agent loop can fail to terminate on its own.
-   Set a hard step limit and a cost/token budget.
-   Detect when an agent is stuck repeating itself.

------------------------------------------------------------------------

# How a Loop Fails to Stop

``` text
1. The model keeps calling tools without ever giving a final answer
   ("just one more check...")
2. The model gets stuck in a cycle - call A, call B, call A, call B,
   with no progress toward the goal
3. A tool call keeps failing (chapter 12 of module 06's error
   handling), and the model keeps retrying it instead of giving up
```

None of these are hypothetical — an LLM has no innate sense of "I've
been at this too long," the same way it has no innate sense of correct
arithmetic (module 01 chapter 17). Something outside the model has to
enforce a limit.

## The Hard Limit: Max Steps

Chapter 07's agent already has this:

``` python
for step in range(max_steps):
    ...
return "max steps reached without a final answer"
```

This is the simplest, most important guardrail — it guarantees the
loop *will* terminate, even in the worst case. Setting `max_steps` too
low risks cutting off a genuinely multi-step task early; too high risks
a runaway loop burning real time and money before hitting the limit.

## A Budget Limit: Tokens or Cost

Step count alone doesn't capture cost — module 01 chapter 04 already
established that longer responses cost more, and an agent's message
list (chapter 04) grows every turn. A token or cost budget catches a
loop that's technically making progress but burning an unreasonable
amount of money doing it.

``` python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4")

def total_tokens(messages: list[dict]) -> int:
    return sum(len(enc.encode(str(m.get("content", "")))) for m in messages)

MAX_TOKENS_BUDGET = 8000

for step in range(max_steps):
    if total_tokens(messages) > MAX_TOKENS_BUDGET:
        return "stopped: token budget exceeded"
    ...
```

## Detecting Repetition

A loop stuck alternating between the same two tool calls will hit
`max_steps` eventually, but detecting the cycle early saves time and
cost:

``` python
def is_repeating(tool_call_history: list[str], window: int = 4) -> bool:
    if len(tool_call_history) < window:
        return False
    recent = tool_call_history[-window:]
    return len(set(recent)) <= 2  # only 1-2 distinct calls across the window
```

``` python
tool_call_history = []
for step in range(max_steps):
    ...
    if msg.tool_calls:
        tool_call_history.append(msg.tool_calls[0].function.name)
        if is_repeating(tool_call_history):
            return "stopped: agent appears to be stuck repeating the same actions"
```

**Platform analogy:** these are the same protections a retry loop
against a flaky network call needs — a max retry count (equivalent to
`max_steps`), a total time/cost budget, and detection for "this keeps
failing the same way, stop retrying and surface the error" instead of
looping forever hoping it resolves itself.

## Hands-on: Force a Loop to Hit Its Limit

``` python
response = run_agent("Investigate why the sky is blue and fix it.", max_steps=3)
print(response)
```

This goal has no real tool that can accomplish it — a good test for
watching `max_steps` actually trigger and produce the "max steps
reached" message, instead of the loop running forever. Confirm the
function returns cleanly instead of hanging.

## Common Misconceptions

❌ A well-designed prompt means an agent will naturally know when to
stop.
(An LLM has no innate sense of "this has gone on too long" — the same
lesson as module 01 chapter 17's arithmetic limitation, applied to
loop control instead of math.)

❌ `max_steps` alone is a sufficient safety net.
(It bounds the number of turns, but not cost (token budget) or wasted
effort (repetition) — all three limits matter for different failure
modes.)

✔ Every agent loop needs at least a hard step limit before it's safe
to run unattended — this is not optional polish, it's the minimum
bound that guarantees termination in the worst case.

## Interview Questions

1.  Name three ways an agent loop can fail to terminate on its own.
2.  Why is a step limit alone not sufficient to bound cost?
3.  How would you detect an agent stuck in a repetitive cycle?
4.  Why is this comparable to retry-limit design for a flaky network
    call?

## Summary

An agent loop has no innate sense of when to stop — a hard step limit,
a token/cost budget, and repetition detection are all separate,
necessary guardrails against different ways a loop can fail to
terminate cleanly. `max_steps` is the minimum required before running
any agent loop unattended; the other two catch failure modes a step
count alone would miss.

## Next Chapter

➡️ `10-Reflection-and-Self-Correction.md`
