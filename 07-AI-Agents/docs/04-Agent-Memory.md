# 04 - Agent Memory

## Introduction

An agent's loop (chapter 02) needs to remember what happened in
earlier turns to make good decisions in later ones. This chapter
covers what "memory" actually means for an agent — and it turns out to
be two genuinely different things wearing the same name.

## Learning Objectives

After this chapter I should be able to:

-   Distinguish short-term (within-run) memory from long-term
    (across-run) memory.
-   Explain how short-term memory connects to module 01's statelessness
    lesson.
-   Explain when long-term memory is worth the added complexity.

------------------------------------------------------------------------

# Two Different Kinds of Memory

``` text
Short-term memory:  everything that happened THIS run - the growing
                      list of reasoning steps, tool calls, and results
                      within one execution of the loop (chapter 02)

Long-term memory:     information that persists ACROSS separate runs -
                      "last time we investigated this service, the
                      cause was X" - remembered days or weeks later
```

## Short-Term Memory Is Just the Message List

This directly reuses module 01 chapter 08's statelessness lesson: the
model itself remembers nothing between calls. An agent's "memory"
within one run is simply the growing list of messages (reasoning,
tool calls, tool results) that gets resent on every turn of the loop —
exactly the mechanism module 02 chapter 11 covered for ordinary
multi-turn conversations, applied to an agent's internal loop instead
of a user-facing chat.

``` python
messages = [{"role": "system", "content": "..."}, {"role": "user", "content": goal}]
# every turn of the loop appends to this list - that list IS the
# agent's short-term memory, nothing more mysterious than that
```

Module 02 chapter 11's warning applies directly here too: this list
grows every turn, and grows expensive the same way a long conversation
does — chapter 09's stopping conditions are partly about controlling
this cost.

## Long-Term Memory Is a Separate Storage Problem

Long-term memory means something gets written down after a run ends,
and read back in on a *different* run later. This is genuinely a
retrieval problem, not a new agent-specific concept — it's module 03
and 05's embeddings and RAG, applied to an agent's own history instead
of external documents.

``` text
After a run: store a summary of what happened (embed it, per module
              03) - "investigated high latency on checkout-service,
              root cause was a slow database query, fixed by adding
              an index"

Next run, similar problem: retrieve that summary via semantic search
              (module 03 chapter 10) and inject it as context (module
              02 chapter 08) before the agent starts reasoning
```

**Platform analogy:** short-term memory is a request's trace context —
relevant for the duration of that one request, then discarded.
Long-term memory is a knowledge base — built up over time, queried
later by a completely different request. Different lifetimes, different
storage mechanisms, and conflating them is a common design mistake.

## When Long-Term Memory Is Worth It

  Situation                                  Worth the complexity?
  ---------------------------------------------- --------------------------------
  One-off task, unlikely to repeat                  No - short-term memory is enough
  Recurring investigation type (e.g. incident triage) | Yes - past runs are genuinely useful context
  Task needs to remember user-specific preferences      Yes - but scope carefully (chapter 13's guardrails apply)

Long-term memory adds real infrastructure (an embedding pipeline, a
vector store, module 03 and 04's whole stack) — don't reach for it
until short-term memory genuinely isn't enough for the task at hand.

## Hands-on: Trace Short-Term Memory Growing

``` python
messages = [{"role": "system", "content": "You are an ops agent."}]
messages.append({"role": "user", "content": "Check disk usage on db-primary-01."})
print(f"turn 1: {len(messages)} messages")

# simulate the loop appending a tool call and its result
messages.append({"role": "assistant", "content": "calling get_disk_usage"})
messages.append({"role": "tool", "content": '{"disk_percent": 92}'})
print(f"turn 2: {len(messages)} messages")
```

Run this pattern through a few more turns and watch the list grow —
this is the entirety of what "short-term memory" means in code, no
more abstract than a growing list.

## Common Misconceptions

❌ Agent memory requires a special memory system or database.
(Short-term memory is just the growing message list — no special
infrastructure needed. Long-term memory does need storage, but it's
the same embeddings/vector-database stack from modules 03-04, not a
new concept.)

❌ Long-term memory is always worth adding.
(It's real infrastructure with real cost — worth it specifically when
past runs contain genuinely reusable information for future runs, not
by default.)

✔ Short-term memory is "what happened this run" (a list); long-term
memory is "what's worth remembering for next time" (a retrieval
problem) — different lifetimes, different mechanisms.

## Interview Questions

1.  What's the difference between short-term and long-term agent
    memory?
2.  Why is short-term memory not a new concept beyond what module 01
    and 02 already covered?
3.  What infrastructure does long-term memory actually require?
4.  When is long-term memory worth the added complexity?

## Summary

Short-term memory is just the growing list of messages within one
agent run — the same statelessness-plus-resent-history mechanism from
modules 01 and 02, nothing more. Long-term memory is a genuinely
separate retrieval problem, reusing modules 03 and 04's embeddings and
vector-database stack to let information persist across runs — worth
adding specifically when past runs contain reusable context, not as a
default.

## Next Chapter

➡️ `05-Planning-Breaking-a-Goal-Into-Steps.md`
