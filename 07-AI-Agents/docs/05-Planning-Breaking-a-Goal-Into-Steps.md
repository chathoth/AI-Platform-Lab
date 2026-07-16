# 05 - Planning: Breaking a Goal Into Steps

## Introduction

The agent loop (chapter 02) lets the model decide one step at a time.
Planning is a variation: asking the model to sketch the *whole* likely
sequence of steps up front, before taking any action — closer to how a
person might jot down a rough plan before starting, while still
staying ready to adjust it.

## Learning Objectives

After this chapter I should be able to:

-   Explain the difference between step-by-step reasoning and
    up-front planning.
-   Write a planning prompt that produces a usable step list.
-   Explain why a plan should be treated as a draft, not a contract.

------------------------------------------------------------------------

# Two Ways to Approach a Goal

``` text
Pure loop (chapter 02): decide ONE step, act, observe, decide the
                          NEXT step - no upfront plan at all

Plan-then-act:            first, ask the model to sketch the likely
                           steps. THEN start the loop, using the plan
                           as a guide - but still observing and
                           adjusting at each step
```

Planning doesn't replace the loop — it's an extra reasoning step
*before* the loop starts, giving the model (and you) a preview of the
likely path, while chapter 02's reason-act-observe cycle still runs
underneath.

## Why Bother Planning at All?

This connects directly to module 02 chapter 04's chain-of-thought
lesson: asking a model to lay out its reasoning before jumping to an
answer improves multi-step accuracy. Planning is that same idea,
applied to *actions* instead of a single answer — asking "what are the
likely steps?" before diving in tends to produce a more coherent
sequence than deciding purely one step at a time with no forward view.

``` text
Prompt: "Before taking any action, list the likely steps to
investigate why checkout-service is returning errors. Then begin."

Model's plan:
  1. Check recent error logs for checkout-service
  2. Check if there was a recent deploy
  3. Check downstream dependencies (payment service, database)
  4. Based on what's found, narrow down the likely cause
```

## A Plan Is a Draft, Not a Contract

This is the part worth internalizing: **the plan is allowed to be
wrong**, and the loop's observe step (chapter 02) is what corrects it.
If step 1 reveals the actual cause immediately, a good agent skips
straight to a conclusion instead of mechanically working through steps
2-4 anyway.

``` text
Plan said: check logs, check deploys, check dependencies, conclude.

What actually happened:
  Step 1 (check logs) -> found a clear database timeout error
  -> the plan's remaining steps are no longer needed
  -> a well-designed agent should skip ahead to a conclusion here,
     not mechanically execute steps 2-4 out of obligation to the plan
```

**Platform analogy:** a plan is a runbook you sketch before starting an
incident response — a reasonable starting guess at the steps, not a
rigid script. A good on-call engineer deviates from the runbook the
moment the evidence points somewhere the runbook didn't anticipate;
they don't follow it blindly once it's clearly wrong.

## Hands-on: Get a Plan, Then Watch It Adapt

``` python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

response = client.chat.completions.create(
    model="llama3.1:8b",
    messages=[{"role": "user", "content": "Before taking any action, list the likely steps to investigate why a service is returning 500 errors. Just the plan, no action yet."}],
    temperature=0.3,
)
print(response.choices[0].message.content)
```

Compare the plan to chapter 07's actual working agent, once you build
it — check whether the real run follows the plan exactly, or adapts
once it finds something the plan didn't anticipate. Either is fine;
what matters is which one actually happened, and why.

## Common Misconceptions

❌ A plan should always be followed exactly once made.
(Treating a plan as a rigid contract defeats the purpose of the loop's
observe step — a plan is a starting guess, and the loop should be free
to deviate when evidence says otherwise.)

❌ Planning replaces the reason-act-observe loop.
(It's an extra step *before* the loop starts, not a substitute for it
— the loop still runs underneath, informed by the plan but not bound
to it.)

✔ Planning is chain-of-thought (module 02 chapter 04) applied to a
sequence of actions instead of a single answer — useful for the same
reason: it gives the model a coherent structure to reason within,
without eliminating the ability to adapt.

## Interview Questions

1.  What's the difference between planning and the pure reason-act-
    observe loop?
2.  Why does planning connect to module 02 chapter 04's chain-of-
    thought lesson?
3.  Why should a plan be treated as a draft rather than a fixed
    sequence?
4.  Give an example of when a good agent should deviate from its own
    plan.

## Summary

Planning asks the model to sketch the likely steps before acting,
giving the agent loop a coherent starting structure — the same value
chain-of-thought brings to a single answer, applied to a sequence of
actions. A plan should stay a draft: the loop's observe step is what
lets the agent correct course the moment reality diverges from what
was expected, and a good agent does exactly that rather than following
a wrong plan out of obligation.

## Next Chapter

➡️ `06-Giving-an-Agent-Tools.md`
