# 07 - AI Agents

> Everything from modules 01-06, wired into a loop that can plan,
> act, and check its own work.

## Overview

Every module up to this point built one piece: how models work (01),
how to prompt them well (02), how to search by meaning (03), where to
store that (04), how to ground answers in real documents (05), and how
to standardize tool access (06). An **agent** is what you get when you
put a model in a loop with tools and let it decide, step by step, what
to do next — instead of you deciding the whole sequence up front.

This module is written to be simple first, deep second. Every concept
gets a plain-language explanation before any code, and every piece of
code was actually run against a local Ollama model while writing this
module — including a genuine failure worth seeing directly: a small
local model incorrectly restarted a service despite a condition not
being met, and the fix (forcing one tool call at a time, with real
guardrails in code) is one of this module's central lessons, not just
a caveat.

Everything runs locally: `llama3.1:8b` via Ollama, no hosted API, no
signup.

## Learning Objectives

After completing this module you will be able to:

-   Explain what makes something an "agent" instead of a chatbot or a
    fixed prompt chain.
-   Build a working agent loop (reason → act → observe) from scratch.
-   Give an agent real tools safely, reusing module 06's MCP patterns.
-   Explain why agents fail in specific, predictable ways — verified
    directly, not just described.
-   Add guardrails that don't rely on the model behaving correctly.
-   Evaluate whether an agent is actually working, not just "looks
    busy."

## Prerequisites

-   [02-Prompt-Engineering](../02-Prompt-Engineering/) — chapter 14
    (tool calling) is the mechanism every agent loop is built on.
-   [06-MCP](../06-MCP/) — helpful, not required. This module's tools
    are plain Python functions; MCP is one good way to standardize
    them, covered as an extension, not a prerequisite.

## Repository Structure

``` text
docs/
examples/
notebooks/
```

## Chapters

  Chapter   Topic
  --------- ---------------------------------------
  01        What Is an AI Agent
  02        The Agent Loop: Reason, Act, Observe
  03        Agents vs. Chains vs. Fixed Workflows
  04        Agent Memory
  05        Planning: Breaking a Goal Into Steps
  06        Giving an Agent Tools
  07        Building a Minimal Agent From Scratch
  08        One Tool at a Time: A Verified Reliability Lesson
  09        Stopping Conditions and Loop Limits
  10        Reflection and Self-Correction
  11        Multi-Agent Systems
  12        Orchestration Patterns
  13        Guardrails and Human-in-the-Loop
  14        Observability: Tracing an Agent's Steps
  15        Evaluating Agent Performance
  16        Common Failure Modes
  17        Cost and Latency of Agentic Systems
  18        Best Practices
  19        Interview Questions
  20        Glossary

## Learning Roadmap

``` text
Retrieval-Augmented Generation
        ↓
Model Context Protocol
        ↓
AI Agents                   ← you are here
        ↓
Ollama and LangChain
```

## Hands-on Labs

-   Build a working reason-act-observe loop from scratch, no framework.
-   Reproduce the verified batching failure, then fix it.
-   Add a stopping condition so a stuck agent can't loop forever.
-   Add a code-level guardrail that a prompt instruction alone
    couldn't provide.
-   Trace every step of an agent's run for debugging.
-   Score an agent's success rate against a small task set.

## Technologies

-   Python
-   Ollama (`llama3.1:8b`)
-   Jupyter

## Expected Outcome

You will be able to build a simple, working agent from first
principles — understanding exactly what it's doing at each step and
why it sometimes gets things wrong — before reaching for a framework.
That understanding is what makes module 09 (LangChain) legible instead
of magic.

## Next Module

➡️ `08-Ollama`
