# 03 - Agents vs. Chains vs. Fixed Workflows

## Introduction

Module 02 chapter 12 already built something that looks agent-adjacent
— prompt chaining, where one call's output feeds the next. This
chapter draws the line clearly, because picking the wrong one of these
three for a given task is one of the most common design mistakes: an
agent where a fixed workflow would do, or a fixed workflow forced onto
a problem that genuinely needs an agent's flexibility.

## Learning Objectives

After this chapter I should be able to:

-   Tell apart a fixed workflow, a chain, and an agent.
-   Explain why a fixed sequence is more predictable and cheaper than
    an agent.
-   Choose the right one for a given real task.

------------------------------------------------------------------------

# Three Shapes, Compared

``` text
Fixed workflow:  step 1 -> step 2 -> step 3 -> done
                 The SEQUENCE is decided by you, ahead of time.
                 Each step might call an LLM, but the ORDER never changes.

Chain (module 02 ch. 12): same as above, specifically for LLM calls -
                 root cause -> status update -> action items.
                 Still a fixed sequence, just of prompts instead of
                 arbitrary steps.

Agent:            the MODEL decides the sequence, turn by turn, based
                 on what it observes. The steps aren't fixed in advance
                 - they emerge from the loop (chapter 02).
```

## Why This Distinction Actually Matters

**Platform analogy:** a fixed workflow or chain is a deploy pipeline —
build, test, package, deploy, in that exact order, every time,
predictable and easy to debug. An agent is more like an on-call
engineer working an incident — they don't follow a fixed script; they
check something, decide what that tells them, check something else
based on what they found, and keep going until the problem is
resolved. Both are valuable. They're not interchangeable.

  Factor                  Fixed workflow / chain          Agent
  --------------------------- --------------------------------- --------------------------------
  Predictability                High - same steps every run        Lower - steps depend on what happens
  Debuggability                  Easy - trace a known sequence        Harder - the sequence itself varies
  Cost                            Fixed, known ahead of time             Variable - more turns, more cost
  Flexibility                      Low - can't adapt to surprises          High - can react to the unexpected
  Best for                          Well-understood, repeatable tasks       Tasks where the right steps depend on what's found along the way

## The Decision, Made Concretely

``` text
Do you already know the exact sequence of steps that solves this,
every time, regardless of what any step returns?
        → fixed workflow or chain - simpler, cheaper, more predictable

Does the right NEXT step genuinely depend on what a PREVIOUS step
returned, in a way you can't fully predict ahead of time?
        → agent - the flexibility is actually needed here
```

**A worked example:** "summarize this incident log, draft a status
update, and suggest action items" (module 02 chapter 12's example) is
a fixed chain — the three steps happen in that order regardless of what
the log says. "Investigate why this service is returning errors" is
an agent problem — the right next step (check logs? check a
dependency? check recent deploys?) depends entirely on what the first
check turns up.

## Hands-on: Classify Three Real Tasks

For each of these, decide: fixed workflow, chain, or agent — and say
why.

``` text
1. "Every morning, pull yesterday's deploy count and post it to Slack."
2. "Given this error message, find the most likely cause among our
   last 5 incidents, using whichever information turns out to be
   relevant."
3. "Translate this document into three languages."
```

(1 and 3 are fixed workflows — the steps never change based on
results. 2 is an agent problem — "whichever information turns out to
be relevant" is exactly the phrase that signals the steps can't be
fully decided in advance.)

## Common Misconceptions

❌ An agent is just a "smarter" or "more advanced" chain.
(It's a different shape, not a strictly better one — a fixed chain is
more predictable and cheaper for tasks where the steps genuinely don't
need to vary.)

❌ If a task involves multiple LLM calls, it must need an agent.
(Module 02 chapter 12's chaining already covers multi-call tasks whose
sequence is fixed — reach for an agent specifically when the sequence
itself needs to adapt.)

✔ Default to the simplest shape that solves the problem: fixed
workflow first, chain if you need multiple fixed LLM steps, agent only
when the right next step truly can't be known in advance.

## Interview Questions

1.  What's the core difference between a chain and an agent?
2.  Why is a fixed workflow more predictable and cheaper than an
    agent?
3.  Give an example of a task that's a good fit for a fixed workflow,
    and one that genuinely needs an agent.
4.  Why shouldn't "involves multiple LLM calls" be the deciding factor
    for reaching for an agent?

## Summary

A fixed workflow or chain follows a sequence you decided in advance;
an agent lets the model decide the sequence as it goes, based on what
it observes. Default to the simpler, more predictable option — reach
for an agent specifically when the right next step genuinely can't be
known ahead of time, not just because a task involves several steps.

## Next Chapter

➡️ `04-Agent-Memory.md`
