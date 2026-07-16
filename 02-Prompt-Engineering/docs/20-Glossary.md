# 20 - Glossary

## Introduction

Every term from this module, alphabetical, defined the way I actually
think about it, with the analogy that made it stick attached.

------------------------------------------------------------------------

**Chain-of-Thought (CoT)** — Prompting a model to produce intermediate
reasoning steps before a final answer, improving accuracy on multi-step
problems at the cost of more tokens/latency. See
[04-Chain-of-Thought.md](04-Chain-of-Thought.md).

**Context Injection** — Handing the model real, current, request-
specific data at prompt time instead of relying on frozen training
knowledge. See [08-Context-Injection.md](08-Context-Injection.md).

**Eval Set** — A fixed, labeled set of test inputs used to score a
prompt objectively — the regression-test suite for a prompt. See
[16-Evaluating-Prompt-Quality.md](16-Evaluating-Prompt-Quality.md).

**Few-Shot Prompting** — Including a handful of labeled examples in the
prompt to calibrate the model to a specific, often non-obvious pattern.
See [03-Zero-Shot-vs-Few-Shot.md](03-Zero-Shot-vs-Few-Shot.md).

**Persona** — The tone/style a system prompt sets ("friendly,"
"terse") — distinct from role, which sets scope and expertise. See
[05-Role-and-System-Prompts.md](05-Role-and-System-Prompts.md).

**Prompt Chain** — A sequence of smaller, single-purpose prompts where
each step's output feeds the next, improving reliability over one
large multi-goal prompt. See
[12-Prompt-Chaining.md](12-Prompt-Chaining.md).

**Prompt Injection** — Untrusted content in a prompt containing text
designed to look like a new instruction and override prior ones — the
SQL-injection analog for LLMs. See
[15-Prompt-Injection-and-Security.md](15-Prompt-Injection-and-Security.md).

**Prompt Template** — A reusable prompt structure with variable
placeholders, separating fixed structure from injected data. See
[07-Prompt-Templates-and-Variables.md](07-Prompt-Templates-and-Variables.md).

**Retention Policy (conversation)** — An explicit rule (sliding window,
summarization, pin-and-trim) for what conversation history to keep as
it grows, to control cost and context-window usage. See
[11-Multi-Turn-Conversation-Design.md](11-Multi-Turn-Conversation-Design.md).

**Role (message)** — The `system`/`user`/`assistant` tag on a message
in a chat-style API call, defining who "said" it and how it should be
weighted. See [02-Anatomy-of-a-Prompt.md](02-Anatomy-of-a-Prompt.md).

**Role (persona)** — The expertise/scope a system prompt assigns the
model ("You are a Kubernetes troubleshooting expert") — distinct from
tone/persona. See
[05-Role-and-System-Prompts.md](05-Role-and-System-Prompts.md).

**Self-Consistency** — Sampling the same prompt multiple times at
nonzero temperature and checking agreement across the answers, as a
signal for ambiguity or uncertainty. See
[13-Self-Consistency-and-Verification.md](13-Self-Consistency-and-Verification.md).

**Structured Output** — Model output constrained to a specific,
parseable format (typically JSON) rather than free text, validated
against a schema before use. See
[06-Structured-Output-Prompting.md](06-Structured-Output-Prompting.md).

**System Prompt** — The message that sets identity, scope, tone,
defaults, and refusal rules for an entire conversation — the closest
thing an LLM call has to a config file. See
[02-Anatomy-of-a-Prompt.md](02-Anatomy-of-a-Prompt.md) and
[05-Role-and-System-Prompts.md](05-Role-and-System-Prompts.md).

**Tool/Function Calling** — A model requesting that application code
execute a defined function with specific arguments, then using the
result to answer — the mechanism underlying AI agents. See
[14-Function-and-Tool-Calling-Prompts.md](14-Function-and-Tool-Calling-Prompts.md).

**Verification Prompting** — A second model call that critiques a
first call's answer for errors, catching some (not all) mistakes the
original generation missed. See
[13-Self-Consistency-and-Verification.md](13-Self-Consistency-and-Verification.md).

**Zero-Shot Prompting** — Asking a model to perform a task with no
examples given, relying entirely on knowledge from training. See
[03-Zero-Shot-vs-Few-Shot.md](03-Zero-Shot-vs-Few-Shot.md).

------------------------------------------------------------------------

## Module Complete

That closes out all 20 chapters of **02-Prompt-Engineering**. Next up
per the [root README](../../README.md) roadmap:

➡️ `03-Embeddings`
