# 16 - Common Failure Modes

## Introduction

A consolidated list of how agents actually fail — one of them (chapter
08's) verified directly in this module, the rest following the same
pattern of "this is a predictable consequence of how the loop works,"
not a random or rare occurrence.

## Learning Objectives

After this chapter I should be able to:

-   Recognize each failure mode by name and by symptom.
-   Connect each one to the chapter that covers its fix.
-   Explain why these are predictable, not freak occurrences.

------------------------------------------------------------------------

# The Failure List

## 1. Acting Before Observing (Verified, Chapter 08)

Batching multiple tool calls into one turn skips the observe step for
later calls, letting an action get taken before its precondition was
actually checked. **Fix:** one tool call at a time (chapter 08).

## 2. Runaway Loops

No stopping condition means a stuck or overly cautious agent can loop
indefinitely, burning time and money. **Fix:** hard step limits, token
budgets, repetition detection (chapter 09).

## 3. Tool Misselection

Given several similarly-named or vaguely-described tools, the model
picks the wrong one — the agent-loop version of module 02 chapter 14's
tool-selection risk, compounded by happening on every turn instead of
once. **Fix:** precise, distinguishing tool descriptions (chapter 06).

## 4. Confidently Wrong Final Answers

Chapter 15 already showed this directly: a wrong action can still
produce a perfectly reasonable-sounding summary. This is module 01
chapter 11's hallucination lesson, applied to an agent's self-report
of what it did instead of to a single factual claim. **Fix:** score
actual actions, not just the final answer text (chapter 15).

## 5. Context Overflow

An agent's message list (chapter 04) grows every turn — a long-running
agent can eventually exceed the context window (module 01 chapter 09),
causing truncated history and degraded reasoning. **Fix:** the same
retention strategies (summarization, trimming) module 02 chapter 11
covered for ordinary conversations.

## 6. Prompt Injection Through Tool Results

A tool's return value (say, log content fetched from a real system)
can contain text designed to look like a new instruction — module 02
chapter 15's injection risk, now arriving through the "observe" step
instead of a retrieved document. **Fix:** treat every tool result as
untrusted data, the same discipline module 02 chapter 15 and module 06
chapter 14 already established.

## 7. Escalating Privilege Through Chained Actions

No single action looks dangerous on its own, but a sequence of them
adds up to something that should have required approval — check disk
usage (fine), list files (fine), delete files (should have paused).
**Fix:** guardrails scoped to the cumulative sequence, not just each
individual action (chapter 13).

## Why These Are Predictable, Not Random

Every failure above traces to a specific, understandable mechanism —
skipping an observe step, no stopping condition, ambiguous
instructions, unchecked context growth, untrusted input, or
unreviewed cumulative risk. None of them require the model to be
"broken" — they're consequences of how the loop, the tools, and the
context work, which is exactly why they're predictable and preventable
rather than freak occurrences to shrug off.

## Hands-on: Match Each Failure to Its Verified or Demonstrated Fix

For each of the seven failure modes above, name the specific chapter
and mechanism that addresses it — this list is deliberately built so
every failure mode maps to something concrete already covered, not a
vague "be careful" warning.

## Common Misconceptions

❌ Agent failures are unpredictable model quirks.
(Every failure mode here has an identifiable mechanism — this module
verified one of them directly (chapter 08) rather than just describing
it abstractly.)

❌ A more capable model eliminates these failure modes.
(A stronger model reduces how *often* some of these happen — it
doesn't eliminate the underlying mechanisms, which is why the
structural and code-level fixes in chapters 08, 09, and 13 matter
regardless of model choice.)

✔ Every failure mode in this list has a concrete, already-covered fix
— treat this chapter as a checklist to run through when designing a
new agent, not just a list of things to worry about abstractly.

## Interview Questions

1.  Name three of the seven failure modes in this chapter and their
    fixes.
2.  Why is "acting before observing" a predictable consequence of
    batching tool calls, not a random glitch?
3.  How can a sequence of individually-safe actions still be
    dangerous?
4.  Why doesn't using a stronger model eliminate the need for
    structural fixes like stopping conditions and guardrails?

## Summary

Every common agent failure mode — acting before observing, runaway
loops, tool misselection, confidently wrong summaries, context
overflow, injection through tool results, and escalating cumulative
risk — has an identifiable mechanism and a concrete fix already covered
in this module, several verified directly rather than just described.
Treat this list as a design checklist, not a warning to worry about
vaguely.

## Next Chapter

➡️ `17-Cost-and-Latency-of-Agentic-Systems.md`
