# 20 - Glossary

## Introduction

Every term from this module, alphabetical, defined the way I actually
think about it, with the analogy that made it stick attached.

------------------------------------------------------------------------

**Agent** — A model that repeatedly decides what to do next based on
what it just observed, instead of following a sequence decided in
advance. See
[01-What-Is-an-AI-Agent.md](01-What-Is-an-AI-Agent.md).

**Agent Loop / ReAct** — The reason → act → observe cycle every agent
is built from, repeated until the goal is met or a stopping condition
fires. See
[02-The-Agent-Loop-Reason-Act-Observe.md](02-The-Agent-Loop-Reason-Act-Observe.md).

**Guardrail** — A code-level check (allowlist, confirmation gate) that
enforces safety regardless of what the model decides — not a prompt
instruction, which the model can get wrong. See
[13-Guardrails-and-Human-in-the-Loop.md](13-Guardrails-and-Human-in-the-Loop.md).

**Long-Term Memory** — Information stored after one agent run and
retrieved in a later, separate run — a retrieval problem reusing
modules 03-04's embeddings and vector-database stack. See
[04-Agent-Memory.md](04-Agent-Memory.md).

**Max Steps** — A hard limit on how many loop turns an agent can take,
guaranteeing termination in the worst case. See
[09-Stopping-Conditions-and-Loop-Limits.md](09-Stopping-Conditions-and-Loop-Limits.md).

**One Tool Call Per Turn** — The verified fix (chapter 08) for a real,
reproduced failure: batching multiple tool calls in one turn skips the
observe step, letting an action happen before its condition was
actually checked. See
[08-One-Tool-at-a-Time-A-Verified-Reliability-Lesson.md](08-One-Tool-at-a-Time-A-Verified-Reliability-Lesson.md).

**Orchestration** — Coordinating multiple agents, via a supervisor
(dynamic routing) or a pipeline (fixed sequence of stages). See
[12-Orchestration-Patterns.md](12-Orchestration-Patterns.md).

**Pipeline Pattern** — A multi-agent shape where every request runs
through the same fixed sequence of agent stages. See
[12-Orchestration-Patterns.md](12-Orchestration-Patterns.md).

**Planning** — Asking the model to sketch the likely steps before
acting, giving the loop a starting structure it's still free to
deviate from. See
[05-Planning-Breaking-a-Goal-Into-Steps.md](05-Planning-Breaking-a-Goal-Into-Steps.md).

**Reflection** — A self-review step checking whether a recent action
was actually justified, given the goal and what was observed. See
[10-Reflection-and-Self-Correction.md](10-Reflection-and-Self-Correction.md).

**Short-Term Memory** — The growing list of messages within one agent
run — the mechanism, not a special system. See
[04-Agent-Memory.md](04-Agent-Memory.md).

**Stopping Condition** — Any mechanism (step limit, token budget,
repetition detection) that bounds an agent loop and guarantees it
eventually stops. See
[09-Stopping-Conditions-and-Loop-Limits.md](09-Stopping-Conditions-and-Loop-Limits.md).

**Supervisor Pattern** — A multi-agent shape where one agent
dynamically decides which worker agent handles a given request. See
[12-Orchestration-Patterns.md](12-Orchestration-Patterns.md).

**Trace** — A step-by-step record of an agent's tool calls, arguments,
results, and latency — what made chapter 08's bug findable at all. See
[14-Observability-Tracing-an-Agents-Steps.md](14-Observability-Tracing-an-Agents-Steps.md).

------------------------------------------------------------------------

## Module Complete

That closes out all 20 chapters of **07-AI-Agents**. Next up per the
[root README](../../README.md) roadmap:

➡️ `08-Ollama`
