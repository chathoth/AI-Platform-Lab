# 18 - Best Practices

## Introduction

The consolidated checklist for this module, in the same spirit as
module 01's chapter 18 — everything here traces back to a specific
chapter, this is just the "what do I actually do" version to walk
through before shipping a prompt-driven feature.

## Learning Objectives

After this chapter I should be able to:

-   Apply a concrete checklist when writing or reviewing a prompt for
    production use.
-   Explain the reasoning behind each item, tied to its source chapter.

------------------------------------------------------------------------

# The Checklist

## 1. State Role, Task, Context, Constraints, and Format Explicitly

Chapter 02. If you can't label a part of your prompt with one of these
five, either it's redundant or it's a gap the model is filling with its
own assumption.

## 2. Put Stable Behavior in the System Prompt

Chapter 05. Identity, scope, tone, and refusal rules belong in the
system prompt — reusable, one place to update, harder to accidentally
override with user input.

## 3. Prefer Positive Instructions Over Pure Negatives

Chapter 10. "Do Y" beats "don't do X" — a positive instruction gives
the model a concrete target instead of an empty space to fill in on its
own, unless it's a hard, checkable exclusion ("never suggest a
destructive command").

## 4. Use Few-Shot Examples for Team-Specific Conventions

Chapter 03. Reserve examples for calibrating non-obvious, internal
patterns — not for generic tasks the model already handles well
zero-shot. 3-5 good examples beat a dozen mediocre ones.

## 5. Reach for Chain-of-Thought Only Where Reasoning Errors Matter

Chapter 04. Root-cause analysis and multi-step calculations benefit
significantly; simple lookups and well-defined classification don't
need the extra tokens and latency.

## 6. Force and Validate Structured Output

Chapter 06. Explicit prompt instruction + provider JSON mode + schema
validation — all three, not just one. Treat model output as untrusted
input, always.

## 7. Templatize Anything Reused More Than Once

Chapter 07. Hardcoded prompt strings drift; a versioned template file
with variables doesn't.

## 8. Delimit Injected/Untrusted Content

Chapters 08 and 15. Wrap retrieved documents, user input, and tool
results in clear delimiters, and instruct the model to treat that
content strictly as data, never as instructions.

## 9. Give Every Long-Lived Conversation a Retention Policy

Chapter 11. Sliding window, summarization, or pin-and-trim — unbounded
history is an unmanaged cost and context-window risk.

## 10. Decompose Multi-Goal Tasks Into a Chain

Chapter 12. If a single prompt is trying to do more than one
independently-checkable thing, split it — each link becomes testable
and independently retryable.

## 11. Use Self-Consistency or Verification Where Noise Is the Risk

Chapter 13. Cheap insurance against inconsistent sampling errors — not
a defense against a systematic, confidently-wrong belief, which still
needs grounding or human review.

## 12. Give Tools Least Privilege, Not Just a Clear Description

Chapter 14/15. A model's tool-call request is a suggestion your code
validates before executing — never expose a destructive tool to a
model that also processes untrusted content in the same context.

## 13. Score Prompt Changes Against an Eval Set

Chapter 16. "I improved the prompt" should be a measurable claim,
including a check against the edge cases that made the prompt tricky in
the first place.

## 14. Version Prompts Like Code

Chapter 17. Versioned files, a changelog, a logged version-per-call,
and an instant rollback path — never edit a shipped prompt file in
place.

## Anti-Patterns to Avoid

-   **Vague adjectives instead of measurable constraints** ("keep it
    short" instead of "under 50 words") — chapter 09.
-   **One prompt trying to do five things at once** — chapter 12.
-   **Concatenating untrusted content directly into instructions with
    no delimiter** — chapter 15.
-   **Editing a live/shipped prompt file in place "just this once"** —
    chapter 17.
-   **Shipping a prompt change based on one manually-checked example**
    — chapter 16.

## Hands-on: Turn This Into a Repo Checklist

Same pattern as module 01: create a `prompt-checklist.md` and copy in
the 14 items above as literal checkboxes. Walk through it before any
prompt goes into a script, pipeline, or tool other people depend on.

## Common Misconceptions

❌ These practices only matter for large, complex prompting systems.
(A single-purpose internal script with a hardcoded, unvalidated prompt
is exactly where format drift and silent regressions go unnoticed
longest — low visibility isn't low risk.)

❌ Following this checklist guarantees a good prompt.
(It catches the common, well-understood failure modes covered in this
module — it doesn't replace testing against real inputs and an eval
set, chapter 16.)

✔ Every item on this list maps to a chapter that explains *why* — once
you understand the underlying failure mode, the practice stops being a
rule to memorize and becomes the obvious fix.

## Interview Questions

1.  Why should stable behavior live in the system prompt rather than be
    repeated per request?
2.  What are the three layers needed for reliable structured output,
    and why isn't one layer enough?
3.  Why does an eval set matter more than "this prompt looks better to
    me"?
4.  What's the deepest defense against a prompt injection succeeding,
    and why does delimiting alone not fully solve it?

## Summary

Every practice in this checklist maps back to a specific failure mode
covered earlier in the module: ambiguity (explicit constraints),
inconsistency (few-shot, self-consistency), unreliable structure
(validation), untrusted content (delimiting, least privilege), and
unmanaged change (versioning, eval sets). Together they're what turns
"a prompt that worked once" into a prompt that's safe to depend on.

## Next Chapter

➡️ `19-Interview-Questions.md`
