# 10 - Reflection and Self-Correction

## Introduction

Module 02 chapter 13 built self-consistency and verification prompting
for single answers — a second pass checking the first. Reflection is
that same idea, applied inside an agent's loop: pausing to check its
own recent actions before continuing, catching a mistake like chapter
08's incorrect restart *during* the run instead of only after the fact.

## Learning Objectives

After this chapter I should be able to:

-   Explain what reflection adds to the basic agent loop.
-   Add a reflection step that checks a recent action against the
    original goal.
-   Explain reflection's real limits, honestly.

------------------------------------------------------------------------

# What Reflection Adds

``` text
Basic loop (chapter 02):   reason -> act -> observe -> reason -> ...

With reflection:            reason -> act -> observe -> REFLECT (did
                             that action make sense, given the goal?)
                             -> reason -> ...
```

Reflection is an extra reasoning step, specifically framed as
self-review rather than forward planning — "look back at what I just
did" instead of "decide what's next."

## A Reflection Prompt, Applied to Chapter 08's Exact Failure

``` python
def reflect(goal: str, recent_action: str, recent_result: dict) -> str:
    prompt = f"""Goal: {goal}
Action just taken: {recent_action}
Result: {recent_result}

Was this action actually justified by the goal's conditions, based on
the result? Answer YES or NO, with a one-sentence reason."""
    response = client.chat.completions.create(
        model=MODEL, messages=[{"role": "user", "content": prompt}], temperature=0
    )
    return response.choices[0].message.content
```

Applied to chapter 08's exact failure — restarting `cleanup-service`
when disk usage was 41%, well under the 90% threshold:

``` text
reflect(
    goal="Check disk usage on web-node-01, and if it is above 90%, restart the cleanup-service.",
    recent_action="restart_service('cleanup-service')",
    recent_result={"disk_percent": 41},
)
-> "NO, because the disk usage is below 90%, so there was no need to
    restart the cleanup-service."
```

A reflection step, inserted right after that action, could have caught
the mistake **during** the run — flagging it for a retry, a rollback,
or a human escalation (chapter 13) — instead of only being visible
afterward in a transcript review.

## Reflection's Real Limits

This is worth being honest about, in the same spirit as module 02
chapter 13's caution about self-consistency: reflection catches
**inconsistent** mistakes — a model that reasoned correctly most of the
time but slipped once. It does **not** reliably catch a **systematic**
misunderstanding, because the same flawed reasoning that caused the
mistake can also produce a flawed reflection that says "yes, that was
fine."

  What reflection catches well            What it doesn't reliably catch
  ------------------------------------------ ------------------------------------
  A one-off slip in an otherwise sound loop    A consistently wrong understanding of the goal
  An action that clearly contradicts the stated goal | A subtly wrong interpretation of an ambiguous goal

## Reflection Is a Second Layer, Not a Replacement

Chapter 08's structural fix (one tool call at a time) reduces how often
the mistake happens in the first place. Reflection is a second,
independent check *on top of* that fix — not instead of it. Layering
both is stronger than relying on either alone, the same "defense in
depth" idea module 02 chapter 15 applied to prompt injection defenses.

## Hands-on: Add Reflection to Chapter 07's Agent

Insert a call to `reflect()` after every tool call in chapter 07's loop,
and print its output. Run it against chapter 08's exact `web-node-01`
scenario using the *original*, unfixed agent (allowing multiple tool
calls per turn) — check whether reflection alone catches the mistake
even without chapter 08's structural fix, and compare that to running
it with both the fix and reflection together.

## Common Misconceptions

❌ Adding reflection eliminates the need for chapter 08's structural
fix.
(Reflection is a probabilistic check, using the same kind of reasoning
that caused the original mistake — it's a second layer of defense, not
a substitute for forcing one tool call at a time.)

❌ Reflection guarantees a mistake gets caught.
(It catches inconsistent errors reasonably well and systematic
misunderstandings poorly — the same honest limitation module 02
chapter 13 already established for self-consistency checks generally.)

✔ Reflection is most valuable layered on top of structural fixes
(chapter 08) and code-level guardrails (chapter 13) — not as a
standalone safety mechanism.

## Interview Questions

1.  What does reflection add to the basic reason-act-observe loop?
2.  Applied to chapter 08's failure, what would a reflection step have
    flagged?
3.  Why doesn't reflection reliably catch a systematic
    misunderstanding of the goal?
4.  Why should reflection be layered on top of chapter 08's structural
    fix, not used instead of it?

## Summary

Reflection adds a self-review step after an action, checking whether
it was actually justified by the goal and what was observed — catching
some mistakes, like chapter 08's incorrect restart, during the run
instead of only in hindsight. It reliably catches inconsistent slips
better than systematic misunderstandings, which is why it belongs
alongside chapter 08's structural fix and chapter 13's guardrails, not
as a replacement for either.

## Next Chapter

➡️ `11-Multi-Agent-Systems.md`
