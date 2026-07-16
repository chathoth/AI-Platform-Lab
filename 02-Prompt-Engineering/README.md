# 02 - Prompt Engineering

> Turning "asking an LLM nicely" into a repeatable, testable engineering
> practice.

## Overview

Module 01 covered how LLMs work under the hood. This module covers the
one interface I actually touch every day: the prompt. A prompt isn't a
casual question — it's the input contract to a non-deterministic
function, and like any other input contract, sloppy prompts produce
brittle systems.

This module treats prompting the way I'd treat API design or writing a
config schema: same discipline, same instinct for validation, same
expectation that "it worked once in the playground" isn't the bar for
production.

## Learning Objectives

After completing this module you will be able to:

-   Structure a prompt with clear roles (system/user/assistant).
-   Choose between zero-shot, few-shot, and chain-of-thought prompting
    for a given task.
-   Get reliable structured (JSON) output instead of free text.
-   Build reusable prompt templates instead of copy-pasted strings.
-   Design multi-turn conversations and multi-step prompt chains.
-   Recognize and defend against prompt injection.
-   Evaluate and version prompts like any other piece of production
    code.

## Prerequisites

-   [01-LLM-Fundamentals](../01-LLM-Fundamentals/) — specifically
    chapters on tokens, temperature/sampling, context window, and
    hallucinations. This module assumes you know *why* a prompt
    behaves the way it does; here we focus on *how to write one well*.

## Repository Structure

``` text
docs/
examples/
notebooks/
```

## Chapters

  Chapter   Topic
  --------- ---------------------------------------
  01        What is Prompt Engineering
  02        Anatomy of a Prompt
  03        Zero-Shot vs Few-Shot Prompting
  04        Chain-of-Thought Prompting
  05        Role and System Prompts
  06        Structured Output Prompting
  07        Prompt Templates and Variables
  08        Context Injection
  09        Instruction Clarity and Constraints
  10        Negative Prompting and Common Pitfalls
  11        Multi-Turn Conversation Design
  12        Prompt Chaining
  13        Self-Consistency and Verification
  14        Function and Tool-Calling Prompts
  15        Prompt Injection and Security
  16        Evaluating Prompt Quality
  17        Prompt Versioning and Change Management
  18        Best Practices
  19        Interview Questions
  20        Glossary

## Learning Roadmap

``` text
LLM Fundamentals
        ↓
Prompt Engineering          ← you are here
        ↓
Embeddings
        ↓
Vector Databases
        ↓
RAG
        ↓
AI Agents
```

## Hands-on Labs

-   Rewrite a vague prompt into a structured one with explicit
    constraints.
-   Compare zero-shot vs few-shot accuracy on a classification task.
-   Force reliable JSON output and validate it against a schema.
-   Build a reusable prompt template with variable substitution.
-   Chain three prompts together to break down a complex task.
-   Attempt (and then defend against) a prompt injection.
-   Write a small eval set and score two prompt variants against it.

## Technologies

-   Python
-   OpenAI SDK (pointed at Ollama by default — no API key required)
-   `jsonschema` for output validation
-   Jupyter

## Expected Outcome

You will be able to design prompts the way you design any other
interface — deliberately, defensively, and with a way to test whether
a change made things better or worse — before moving on to Embeddings
and Vector Databases, where prompt design and retrieved context start
working together.

## Next Module

➡️ `03-Embeddings`
