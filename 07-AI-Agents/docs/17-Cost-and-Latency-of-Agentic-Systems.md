# 17 - Cost and Latency of Agentic Systems

## Introduction

A single LLM call has one, roughly predictable cost. An agent run has
an unknown number of calls, decided by the model itself — this chapter
is the capacity-planning conversation module 01 chapter 12 and module
04 chapter 17 already had for models and vector databases, now applied
to something with genuinely variable cost per run.

## Learning Objectives

After this chapter I should be able to:

-   Explain why an agent's cost is fundamentally less predictable than
    a single call's.
-   Estimate a rough cost range for an agent task.
-   Apply concrete levers to control cost without breaking
    correctness.

------------------------------------------------------------------------

# Why Agent Cost Is Different

``` text
Single LLM call:  1 request, roughly predictable tokens in/out
                    (module 01 chapter 04's cost math applies directly)

Agent run:          N requests, where N depends on how many turns the
                    LOOP takes - and the model itself decides N,
                    within chapter 09's bounds
```

Every turn re-sends the growing message list (chapter 04), so cost
doesn't just multiply by turn count — it grows faster, the same
"conversation gets progressively more expensive to continue" lesson
module 02 chapter 11 already established, now happening automatically
across an agent's own internal turns instead of a user-facing chat.

## A Rough Cost Estimate

``` python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4")

def estimate_agent_cost(trace: list[dict], price_per_million_tokens: float = 3.00) -> float:
    # rough: re-derive approximate token count per turn from the trace
    total_tokens = 0
    running_context = 0
    for entry in trace:
        turn_tokens = len(enc.encode(str(entry)))
        running_context += turn_tokens
        total_tokens += running_context  # each turn re-sends everything before it
    return (total_tokens / 1_000_000) * price_per_million_tokens
```

This is a rough estimate, not a precise bill — but it makes the point
directly: a 5-turn agent run costs meaningfully more than 5× a single
call, because each turn resends everything accumulated so far.

## Levers That Actually Control Cost

  Lever                          Effect
  ---------------------------------- --------------------------------------
  Lower `max_steps` (chapter 09)         Hard cap on the worst case
  Smaller/cheaper model for simple steps  Module 01 chapter 12's right-sizing, applied per agent or per step
  Trim conversation history (module 02 ch. 11) | Keeps the resend cost from growing unbounded
  Fewer, more capable tools per turn        Reduces the chance of extra, unnecessary turns
  Right-size context injected (module 02 ch. 08) | Don't hand the agent more background than the task needs

## Latency Compounds the Same Way

Every turn is a full round trip (module 01 chapter 03's generation
loop), so a 5-turn agent isn't just "5× slower" than a single call —
tool execution time (a real API call, a real database query) adds on
top of each turn's generation time. A user waiting on an agent's answer
is waiting on the sum of every turn's latency, not just one call's.

**Platform analogy:** this is the same reasoning behind setting a
timeout and a retry budget on any external call chain — the total
latency of a request that fans out to several dependent calls is the
sum of those calls, not the latency of any single one, and it needs to
be budgeted for explicitly rather than assumed away.

## Hands-on: Measure a Real Run's Cost and Time

``` python
import time

start = time.time()
answer, trace = run_agent_traced("Check disk usage on db-primary-01, and if it's above 90%, restart the cleanup-service.")
elapsed = time.time() - start

print(f"Turns taken: {len([t for t in trace if t['type'] == 'tool_call'])}")
print(f"Total wall time: {elapsed:.2f}s")
print(f"Estimated cost: ${estimate_agent_cost(trace):.6f}")
```

Compare this against a single, non-agentic tool call for the same
question — the multiplier is the real, measurable cost of the agent's
flexibility, not just a theoretical concern.

## Common Misconceptions

❌ An agent costs roughly the same as one LLM call, since it's "one
task."
(It costs roughly the sum of every turn's tokens, growing faster than
linear because each turn resends the accumulated history — same
mechanism as module 02 chapter 11's conversation-cost warning.)

❌ Cost control means sacrificing correctness.
(Right-sizing models per step, trimming unnecessary context, and
capping `max_steps` at a sensible ceiling all reduce cost without
touching the actual reasoning quality for a well-scoped task.)

✔ Estimate an agent task's cost range *before* deploying it broadly —
the same capacity-planning discipline module 01 and module 04 already
applied to models and vector databases, now applied to a
variable-length loop.

## Interview Questions

1.  Why does an agent's cost grow faster than linearly with turn
    count?
2.  Name three concrete levers for controlling an agent's cost.
3.  Why does latency compound across an agent's turns rather than
    just adding tool execution time once?
4.  How is agent latency budgeting similar to timeout/retry budgeting
    for a chain of dependent service calls?

## Summary

An agent's cost and latency are the sum across every turn, growing
faster than linear because each turn resends the accumulated history —
a fundamentally less predictable cost profile than a single LLM call.
Concrete levers (step limits, right-sized models per step, trimmed
context) keep this bounded, and estimating a rough cost range before
deploying an agent broadly is the same capacity-planning discipline
already applied to models and vector databases elsewhere in this
repository.

## Next Chapter

➡️ `18-Best-Practices.md`
