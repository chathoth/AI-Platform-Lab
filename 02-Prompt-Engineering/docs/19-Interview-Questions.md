# 19 - Interview Questions

## Introduction

Every interview question from this module, grouped by chapter, with
the answer framed the way I'd actually say it out loud. Review material,
not first-pass learning — read the chapters first.

------------------------------------------------------------------------

## Chapter 01 - What is Prompt Engineering

**Q: Why does prompt engineering matter even as models keep improving?**
Every model generation has added more prompting surface area (system
prompts, tool schemas, structured output modes), not less. The
underlying skill — removing ambiguity from an instruction — compounds
rather than becoming obsolete.

## Chapter 02 - Anatomy of a Prompt

**Q: What are the three message roles, and what's each for?**
`system` sets behavior for the whole session (closest thing to a config
file). `user` is the actual request. `assistant` is the model's prior
replies, resent to preserve multi-turn context.

## Chapter 03 - Zero-Shot vs Few-Shot

**Q: When does few-shot prompting help most?**
When calibrating to a team-specific or otherwise non-obvious pattern —
it teaches the *pattern*, not just the topic. For generic, well-
understood tasks it mostly just adds token cost.

## Chapter 04 - Chain-of-Thought

**Q: Why does asking a model to "think step by step" improve accuracy?**
It gives the model's own next-token predictions intermediate steps to
condition on, narrowing the space of plausible continuations at each
step — at the cost of more output tokens and latency, so reserve it for
genuinely multi-step problems.

## Chapter 05 - Role and System Prompts

**Q: Why isn't a system prompt a security boundary?**
With enough adversarial input, a model can be talked out of its system
prompt (prompt injection, chapter 15). Anything with real consequences
needs enforcement outside the model, not just an instruction inside it.

## Chapter 06 - Structured Output Prompting

**Q: What three layers make structured output reliable?**
An explicit, example-shaped prompt instruction; the provider's native
JSON/structured-output mode (enforced at sampling); and schema
validation before the data is trusted downstream.

## Chapter 07 - Prompt Templates and Variables

**Q: Why move from hardcoded prompt strings to templates?**
Templates separate fixed structure from variable data — one place to
fix a bug or add a conditional section instead of scattered, drifting
copies, the same value a Kubernetes manifest gets from `values.yaml`.

## Chapter 08 - Context Injection

**Q: Why does clearly delimiting injected context matter for both
accuracy and security?**
Undelimited data blurs into instructions — the model can't tell fact
from command, and it's the exact seam prompt injection exploits.
Explicit delimiters (like `<context>` tags) are the prompt-level
equivalent of parameterized queries.

## Chapter 09 - Instruction Clarity and Constraints

**Q: Why does "keep it short" produce inconsistent output?**
It leaves a judgment call to the model without stating your actual bar
— every unstated judgment call is a place output can drift between
calls, independent of sampling randomness.

## Chapter 10 - Negative Prompting and Pitfalls

**Q: Why is "do Y" more reliable than "don't do X"?**
A pure negative tells the model what to avoid but not what to produce
instead, leaving a gap it can fill with an equally undesired
alternative. Reserve negatives for hard, checkable exclusions.

## Chapter 11 - Multi-Turn Conversation Design

**Q: Why does turn 10 of a conversation cost more than turn 1?**
Every turn resends the entire history (module 01, statelessness) — cost
grows with conversation length regardless of how short the newest
question is, unless a retention policy trims or summarizes it.

## Chapter 12 - Prompt Chaining

**Q: Why does decomposing a task into a chain improve reliability?**
Each link has one job and a checkable output — a failure is contained
to a specific step instead of corrupting one large, multi-goal
response, the same value staged CI/CD pipelines have over one script.

## Chapter 13 - Self-Consistency and Verification

**Q: What kind of error do these techniques fail to catch?**
Systematic, confidently-wrong beliefs baked into training — they catch
inconsistent, low-confidence sampling errors well, not consistent bias.
That still needs grounding (RAG) or human review.

## Chapter 14 - Function and Tool-Calling Prompts

**Q: Why doesn't the model actually execute the function it "calls"?**
It only emits a structured request with arguments — your application
code decides whether and how to run it, which is exactly the point
where a validation/allowlist check belongs.

## Chapter 15 - Prompt Injection and Security

**Q: What's the deepest defense against a successful injection?**
Least-privilege tool access — even a fully successful injection can
only do damage within what the model is capable of doing. Delimiting
and validation reduce the odds of success; least privilege limits the
blast radius when one gets through anyway.

## Chapter 16 - Evaluating Prompt Quality

**Q: Why isn't "it looks better to me" sufficient validation for a
prompt change?**
A fix for the one example you're staring at can silently break cases
you weren't checking — an eval set with known edge cases catches
exactly what a spot check would miss.

## Chapter 17 - Prompt Versioning

**Q: Why shouldn't you edit a shipped prompt file in place?**
It destroys the ability to know what generated past production output
and makes instant rollback impossible — the same reason you don't edit
a tagged release's source directly.

## Chapter 18 - Best Practices

**Q: Why does every practice in this module trace back to a specific
chapter instead of being a standalone rule?**
Understanding the underlying failure mode (ambiguity, injection,
unmanaged drift) is what lets you judge edge cases the checklist
doesn't explicitly cover — memorizing rules without the "why" doesn't
generalize.

------------------------------------------------------------------------

## Rapid-Fire Round

1.  System prompt — reusable, application-owned config for behavior.
2.  Few-shot — calibrates to a pattern, not just a topic.
3.  Chain-of-thought — trades tokens/latency for multi-step accuracy.
4.  Structured output — needs prompt + JSON mode + schema validation,
    all three.
5.  Context injection — must be delimited from instructions.
6.  Negative prompting — weaker than positive, except hard exclusions.
7.  Conversation history — needs an explicit retention policy.
8.  Prompt chaining — decomposition for independently-checkable steps.
9.  Self-consistency — catches noise, not systematic bias.
10. Tool calling — a suggestion, always validated before execution.
11. Prompt injection — same root cause as SQL injection.
12. Eval sets — turn prompt changes into testable claims.
13. Prompt versioning — same discipline as code, never edit in place.

## Next Chapter

➡️ `20-Glossary.md`
