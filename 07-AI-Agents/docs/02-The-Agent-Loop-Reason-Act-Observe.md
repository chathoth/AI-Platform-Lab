# 02 - The Agent Loop: Reason, Act, Observe

## Introduction

Chapter 01 named the loop. This chapter is the loop itself, in enough
detail to actually build it in chapter 07. This exact pattern has a
name in the research literature — **ReAct** (Reason + Act) — but the
name matters less than understanding what each of the three steps is
actually doing.

## Learning Objectives

After this chapter I should be able to:

-   Explain what happens in each of the three loop stages.
-   Explain why "observe" is the step that makes an agent different
    from a single tool call.
-   Trace a multi-step example through the loop by hand.

------------------------------------------------------------------------

# The Three Stages

``` text
REASON   - given the goal and everything that's happened so far,
            decide what to do next (call a tool? give a final answer?)

ACT       - actually do that thing (call the tool, run the query)

OBSERVE    - look at what came back, and add it to what the model
             knows before reasoning again
```

``` mermaid
flowchart LR
A[Goal] --> B[Reason: what next?]
B --> C{Tool call or final answer?}
C -->|tool call| D[Act: run it]
D --> E[Observe: read the result]
E --> B
C -->|final answer| F[Done]
```

## Why "Observe" Is the Important Part

A single tool call (module 02 chapter 14) does Reason and Act once,
then stops — the result goes straight back to the user. An agent's
loop feeds the result back into the **next reasoning step**, so later
decisions can depend on earlier outcomes.

``` text
Single tool call:
  question -> reason -> act -> here's the result (done)

Agent loop:
  goal -> reason -> act -> OBSERVE -> reason again (using that result)
       -> act -> OBSERVE -> reason again -> ... -> final answer
```

**Platform analogy:** this is the difference between running one
health check and a full monitoring-and-remediation loop. One health
check tells you the current state. A remediation loop checks the
state, takes an action if needed, checks the state *again* to confirm
the action worked, and only stops once the target state is actually
reached — not just after one action was taken.

## Walking Through an Example by Hand

``` text
Goal: "Check disk usage on db-primary-01 and clean up if it's critical."

Turn 1
  REASON:  I need to check disk usage first.
  ACT:     call get_disk_usage("db-primary-01")
  OBSERVE: result = 92% - that's above the 90% threshold

Turn 2
  REASON:  92% is critical. I should find what's using the space.
  ACT:     call list_large_files("db-primary-01")
  OBSERVE: result = mostly old logs in /var/log

Turn 3
  REASON:  Old logs are safe to clean. Do it.
  ACT:     call cleanup_logs("db-primary-01")
  OBSERVE: result = freed 30GB

Turn 4
  REASON:  Let me confirm it actually worked.
  ACT:     call get_disk_usage("db-primary-01") again
  OBSERVE: result = 61% - problem solved

Turn 5
  REASON:  Goal met. No more actions needed.
  -> final answer: "Disk usage was at 92%, cleaned up old logs,
     now at 61%."
```

Five turns, each one building on the last. This is what chapter 07
builds in real code, using this exact scenario.

## Hands-on: Predict the Next Step

Before chapter 07's code, try this on paper: given the observation
"disk usage is 45%" instead of 92% in Turn 1 above, what should Turn 2
look like? (Answer: there shouldn't be a Turn 2 doing cleanup — the
threshold wasn't crossed, so the very next reasoning step should go
straight to a final answer.) Chapter 08 verifies, with a real model,
that this "don't act unless the condition is actually met" step is
exactly where smaller models can get it wrong — worth predicting the
correct behavior yourself first.

## Common Misconceptions

❌ More loop turns always means a better answer.
(More turns mean more chances to gather information, but also more
cost and more chances for the model to go off track — chapter 09
covers stopping conditions specifically because more isn't
automatically better.)

❌ The "observe" step is just logging.
(It's what the next reasoning step is actually built on — skip it, and
you're back to a single tool call with no ability to react to what
happened.)

✔ Every agent, no matter how sophisticated, is built from this same
three-stage loop repeated — the sophistication comes from what happens
inside "reason" (chapters 05, 10, 11), not from a different loop shape.

## Interview Questions

1.  Name the three stages of the agent loop and what happens in each.
2.  Why does the "observe" step matter more than it might seem?
3.  What's the difference between a single tool call and the full
    loop, in terms of these three stages?
4.  Walk through a two-turn example of the loop, in your own words.

## Summary

The agent loop is reason (decide what's next), act (do it), observe
(read the result and feed it into the next reasoning step) — repeated
until the goal is met. The "observe" step is what turns a one-shot tool
call into something that can react to what actually happened, which is
the entire mechanism every agent in this module is built from.

## Next Chapter

➡️ `03-Agents-vs-Chains-vs-Fixed-Workflows.md`
