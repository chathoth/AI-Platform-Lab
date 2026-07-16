# 18 - Best Practices

## Introduction

This chapter is my consolidated checklist — the operational rules I'd
actually want written down before putting any LLM-backed feature in
front of real users. Every item here traces back to a limitation or
mechanism covered in an earlier chapter; this is just the "so what do I
actually do about it" version.

## Learning Objectives

After this chapter I should be able to:

-   Apply a concrete checklist when designing an LLM-backed system.
-   Explain the reasoning behind each best practice, tied back to the
    underlying mechanism.
-   Recognize anti-patterns that look convenient but cause production
    problems.

------------------------------------------------------------------------

# The Checklist

## 1. Treat Every LLM Response as Untrusted Input

Same as chapter 11 and 17 — validate structure, sanity-check facts that
matter, never directly execute a generated command without review or a
dry-run step.

``` python
# anti-pattern
os.system(llm_response)  # never do this

# better
proposed_cmd = llm_response
if is_safe_and_expected(proposed_cmd):
    run(proposed_cmd)
else:
    flag_for_human_review(proposed_cmd)
```

## 2. Pin Model Versions Like You'd Pin Dependencies

Providers update models continuously. Calling `"gpt-4"` without a
version can mean your behavior silently shifts under you.

``` python
# anti-pattern - unpinned, can shift under you
model = "gpt-4"

# better - pinned, same discipline as pinning a package version
model = "gpt-4-0613"
```

Same reasoning as pinning a Docker base image tag instead of floating on
`latest` — reproducibility matters more than always having the newest
version by default.

## 3. Set Low Temperature for Anything Programmatic

Covered in chapter 10 — if the output feeds into a script, a schema, or
downstream automation, keep temperature near 0. Save higher temperature
for human-facing, exploratory interactions only.

## 4. Pre-flight Token Counts, Don't Just Handle the Failure

Covered in chapter 16 — check token count against the context window
*before* sending, the same way you'd validate payload size before a
call instead of relying purely on catching a 413 after the fact.

## 5. Ground Factual Answers With RAG, Don't Rely on Trained Memory

Covered in chapters 11 and 14 — for anything time-sensitive or
company-specific, retrieve real source documents into the prompt rather
than trusting what the model "remembers" from training.

## 6. Log the Fully Assembled Prompt, Not Just the User's Message

Covered in chapter 16 — most debugging starts with "what was actually
sent to the model," which includes system prompt, RAG context, and
history, not just what the user typed.

## 7. Set Real Timeouts and Retries, With Backoff

LLM calls are a network dependency like any other external API — they
can hang, rate-limit, or fail. Apply the same resilience patterns:

``` python
import time

def call_with_retry(fn, max_retries=3, base_delay=1):
    for attempt in range(max_retries):
        try:
            return fn()
        except RateLimitError:
            time.sleep(base_delay * (2 ** attempt))  # exponential backoff
    raise Exception("Max retries exceeded")
```

## 8. Monitor Cost and Token Usage Like Any Other Spend Metric

Covered in chapter 04 — token usage should be on a dashboard with
alerting thresholds, the same as cloud spend or egress bandwidth. A
runaway prompt-injection loop or an unbounded conversation history can
turn into a real cost incident fast.

## 9. Right-Size the Model to the Task

Covered in chapters 12/13/15 — don't default to the biggest/most
expensive model for every call. Route cheap, high-volume, low-stakes
tasks (classification, simple extraction) to smaller/cheaper models,
and reserve frontier models for tasks that actually need that
reasoning depth. This is load-balancing/tiering applied to model choice.

## 10. Have a Fallback for When the Model/Provider Is Down

Closed APIs (chapter 15) are a third-party dependency with their own
uptime SLA, outside your control. Design a degraded-mode path
(cached response, a smaller local fallback model, or a clear "AI
assistant unavailable" state) instead of letting an outage upstream
become an outage for your users.

## Anti-Patterns to Avoid

-   **Concatenating unbounded conversation history** into every call
    without a trimming/summarization strategy — context and cost grow
    unchecked (chapter 09).
-   **Trusting the model's stated confidence** as a proxy for
    correctness (chapter 11) — tone and accuracy are uncorrelated.
-   **Skipping output schema validation** on anything meant to be
    parsed as structured data — treat it exactly like any other
    untrusted API response.
-   **Using max context window "just in case"** on every call — driving
    up cost and latency for headroom that's rarely used (chapter 09).

## Hands-on: Turn This Into a Repo Checklist

Create `checklist.md` in your own project and copy in the ten items
above as literal checkboxes. Before shipping any LLM-backed feature,
walk through it the same way you'd walk through a pre-deploy checklist
— it takes five minutes and catches the mistakes this whole module was
built around.

## Common Misconceptions

❌ Best practices for LLMs are a completely new discipline.
(Nearly every item above is a direct port of an existing distributed-
systems/API-design practice — validate untrusted input, pin versions,
retry with backoff, monitor spend, right-size resources.)

❌ Following these practices is optional for a "simple" internal tool.
(Internal tools are exactly where unbounded cost, prompt injection from
internal documents, and silent version drift tend to go unnoticed the
longest — the stakes being lower doesn't make the failure modes go
away.)

✔ Every practice on this list maps to a limitation from chapter 17 —
if you understand *why* a limitation exists, the corresponding best
practice stops being a rule to memorize and becomes the obvious fix.

## Interview Questions

1.  Why should model versions be pinned rather than left floating on
    the latest tag?
2.  What's the risk of not validating structured output from an LLM
    before using it downstream?
3.  Why does an LLM API call need the same retry/backoff treatment as
    any other external network dependency?
4.  How would you decide which tasks in a system should use a smaller/
    cheaper model vs. a frontier model?

## Summary

Nearly every LLM best practice is a familiar distributed-systems
practice applied to a new kind of dependency: validate untrusted output,
pin versions, retry with backoff, log the real request payload, monitor
spend, and right-size the resource (model) to the job. None of this
requires new instincts — it requires applying the instincts already
built from operating other systems, mapped onto where LLMs specifically
tend to fail.

## Next Chapter

➡️ `19-Interview-Questions.md`
