# 18 - Best Practices

## Introduction

The consolidated checklist for this module, same spirit as every other
module's — each item traces back to a specific chapter, several to
chapter 08's directly verified finding rather than a theoretical
concern.

## Learning Objectives

After this chapter I should be able to:

-   Apply a concrete checklist before deploying any agent.
-   Explain the reasoning behind each item, tied to its source
    chapter.

------------------------------------------------------------------------

# The Checklist

## 1. Default to the Simplest Shape That Solves the Problem

Chapter 03. Fixed workflow or chain before agent; single agent before
multi-agent (chapter 11). Reach for more flexibility only when the
task genuinely requires it.

## 2. Force One Tool Call at a Time

Chapter 08, verified directly. Batching tool calls in one turn skips
the observe step and caused a real, reproducible incorrect action in
this module's own testing.

## 3. Write Tool Descriptions That Distinguish Similar Tools

Chapter 06. An agent chooses among tools every turn — ambiguity
compounds across turns, not just within one call.

## 4. Set a Hard Step Limit on Every Agent, Always

Chapter 09. This is the non-negotiable minimum before running any
agent loop unattended — it's what guarantees termination in the worst
case.

## 5. Add a Token/Cost Budget on Top of the Step Limit

Chapter 09/17. A step limit alone doesn't bound cost, since message
history grows every turn.

## 6. Never Rely on a Prompt Instruction as the Only Safety Check

Chapter 13. Put an allowlist and a confirmation gate for destructive
actions in code the model cannot talk its way around — the same
lesson module 02 chapter 15 and module 06 chapter 13 already
established from different angles.

## 7. Trace Every Step, Not Just the Final Answer

Chapter 14. Chapter 08's bug was only findable through a full,
turn-by-turn trace — the final answer alone looked fine.

## 8. Score Actual Actions in Evaluation, Not Just the Final Answer's
Tone

Chapter 15. Chapter 08's incorrect run produced a perfectly reasonable-
sounding summary — evaluation has to check what was actually done.

## 9. Seed Eval Sets With the Edge Cases That Exposed Real Bugs

Chapter 15. Chapter 08's `web-node-01` case is the highest-value test
case this module's own eval set contains, because it's proven to catch
a real regression.

## 10. Treat Every Tool Result as Untrusted Data

Chapter 16 (failure mode 6). The same discipline module 02 chapter 15
and module 06 chapter 14 already applied to retrieved documents and
MCP tool results.

## Anti-Patterns to Avoid

-   **Letting a model batch multiple tool calls per turn by default**
    — chapter 08, the single most concrete finding in this module.
-   **An agent with no step limit, ever** — chapter 09.
-   **Judging an agent's correctness from its final answer alone** —
    chapters 15, 16.
-   **A confirmation gate that isn't actually in the execution path**
    — chapter 13.
-   **Building a multi-agent system before confirming a single agent
    genuinely can't handle the task** — chapter 11.

## Hands-on: Turn This Into a Repo Checklist

Same pattern as every other module: create an `agent-checklist.md`
with these 10 items as literal checkboxes, and walk through it before
pointing any agent at something with real consequences.

## Common Misconceptions

❌ These practices are theoretical caution, not concrete requirements.
(Several items on this list trace directly to chapter 08's verified,
reproducible failure — this isn't hypothetical risk management.)

❌ Following this checklist guarantees a correct agent.
(It avoids the well-understood, verified failure modes in this module
— it doesn't replace testing against your own specific tools and
tasks, per chapter 15.)

✔ Item 2 (one tool call at a time) is this module's single highest-
leverage practice, because it's the one directly proven to prevent a
real, reproduced incorrect action.

## Interview Questions

1.  Which item on this checklist is backed by a directly verified
    finding, and what was that finding?
2.  Why does a step limit alone not fully bound an agent's cost?
3.  Why should eval sets specifically include the edge case that
    exposed a real bug?
4.  Why can't a prompt instruction alone serve as an agent's only
    safety check?

## Summary

Every practice in this checklist maps to a specific chapter, and
several map to chapter 08's directly verified, reproducible finding: a
correctly built agent loop still took an unjustified action when it
was allowed to batch tool calls without observing results in between.
Forcing one tool call at a time, hard limits, code-level guardrails,
full tracing, and action-based evaluation are what turn "an agent that
worked in a demo" into one safe to actually run.

## Next Chapter

➡️ `19-Interview-Questions.md`
