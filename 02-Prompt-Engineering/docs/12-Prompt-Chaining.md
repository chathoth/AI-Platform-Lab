# 12 - Prompt Chaining

## Introduction

Chapter 10's pitfall list flagged "one prompt trying to do five
unrelated things" as a reliability problem. Prompt chaining is the fix:
break a complex task into a sequence of smaller, single-purpose calls,
each one's output feeding the next — the same instinct as breaking a
giant deploy script into discrete, individually-testable pipeline
stages instead of one 500-line shell script.

## Learning Objectives

After this chapter I should be able to:

-   Explain why decomposing a task into multiple prompts improves
    reliability.
-   Design a simple prompt chain with intermediate validation.
-   Weigh the latency/cost trade-off of chaining against a single
    larger prompt.

------------------------------------------------------------------------

# One Giant Prompt vs. a Chain

``` text
One giant prompt:
  "Read this incident log, identify the root cause, write a customer-
   facing status update, AND suggest three follow-up action items,
   formatted as JSON."
```

Asking for four different things in different formats, in one call,
means any one of them can come out wrong or malformed with no visibility
into *which* step failed. Compare that to a chain:

``` mermaid
flowchart LR
A[Incident log] --> B[Prompt 1: extract root cause]
B --> C[Prompt 2: draft customer-facing update - from root cause]
C --> D[Prompt 3: suggest action items - from root cause]
D --> E[Combine + validate each piece]
```

Each step has one job, a checkable output, and can be retried or fixed
independently without re-running the whole pipeline.

**Platform analogy:** this is a CI/CD pipeline with discrete stages
(build → test → package → deploy) instead of one script that does
everything and fails opaquely somewhere in the middle. When stage 2
fails, you know it's stage 2 — you don't have to guess which of four
things went wrong inside a single monolithic step.

## A Minimal Chain, in Code

``` python
def extract_root_cause(client, model, log_text):
    r = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": f"In one sentence, what is the root cause in this log?\n{log_text}"}],
        temperature=0,
    )
    return r.choices[0].message.content.strip()

def draft_status_update(client, model, root_cause):
    r = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": f"Write a 2-sentence customer-facing status update for this root cause, no technical jargon: {root_cause}"}],
        temperature=0.3,
    )
    return r.choices[0].message.content.strip()

def suggest_action_items(client, model, root_cause):
    r = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": f"Suggest 3 short follow-up action items for this root cause, as a numbered list: {root_cause}"}],
        temperature=0.3,
    )
    return r.choices[0].message.content.strip()

# each step's output can be logged, validated, and retried independently
root_cause = extract_root_cause(client, MODEL, log_text)
assert root_cause, "root cause extraction failed - stop before wasting downstream calls"

status_update = draft_status_update(client, MODEL, root_cause)
action_items = suggest_action_items(client, MODEL, root_cause)
```

## The Trade-off: More Calls, More Latency, More Reliability

  Approach          Latency/cost              Reliability
  ------------------ -------------------------- --------------------------------
  One giant prompt    1 call, lowest latency      Any one sub-task failing corrupts the whole output
  Chained prompts      N calls, N× the round trips Each step independently checkable and retryable

This is a direct latency-vs-reliability trade-off, the same one behind
choosing synchronous vs. asynchronous processing stages in a pipeline.
Chain when a step's failure needs to be caught before it propagates
(e.g., don't draft a customer-facing message from a wrong root cause);
don't chain when the task is genuinely simple enough for one prompt to
handle reliably — chaining a trivial task just adds latency for no
reliability gain.

## Hands-on: Chain It, Then Break a Link on Purpose

Take the incident log from module 01's `09_summarization.py` example
and build the three-step chain above. Then deliberately feed
`extract_root_cause` a log with no clear cause (e.g. just a timestamp)
and watch how the failure stays contained to step 1 — `assert
root_cause` should stop the chain before a nonsense root cause pollutes
the customer-facing update.

## Common Misconceptions

❌ Chaining is always better than one well-crafted prompt.
(For simple, single-purpose tasks, one prompt is faster and cheaper —
chaining earns its keep specifically when a task has multiple
independent sub-goals or needs intermediate validation.)

❌ A chain is the same thing as a multi-turn conversation.
(A chain is a sequence of independent, often stateless calls each doing
one job — a conversation (chapter 11) is one ongoing context growing
turn by turn. They can be combined, but they solve different problems.)

✔ Each link in a chain should be independently testable — if you can't
write a unit test for one step's input/output, it's probably still
doing too much.

## Interview Questions

1.  Why does breaking a complex prompt into a chain improve
    reliability?
2.  What's the cost of chaining, compared to one larger prompt?
3.  When would you choose one prompt over a chain?
4.  How is prompt chaining similar to a staged CI/CD pipeline?

## Summary

Prompt chaining decomposes a complex task into a sequence of smaller,
single-purpose calls, each independently checkable and retryable — the
same reliability gain as staged CI/CD pipelines over one monolithic
script. It costs more latency and calls than a single prompt, so reserve
it for tasks with multiple independent sub-goals, not simple single-
purpose requests.

## Next Chapter

➡️ `13-Self-Consistency-and-Verification.md`
