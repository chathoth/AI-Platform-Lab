# 08 - Ollama

> The tool behind every "local model" example in this whole
> repository, finally covered on its own terms.

## Overview

Every module from 01 through 07 called Ollama without stopping to
explain it — `base_url="http://localhost:11434/v1"` just worked. This
module is where that gets a proper explanation: what Ollama actually
is, how it manages models on disk, its REST API (the thing the OpenAI-
compatible endpoint is a thin wrapper around), Modelfiles for
customizing a model's behavior, and the operational questions a
platform engineer actually asks — how much memory does this need, how
do I run it as a real service, what happens if I expose it beyond
localhost.

Every command and API call in this module was run for real against a
locally installed Ollama instance while writing it — including
building and running a custom model from a Modelfile, and reading the
REST API's actual JSON responses directly, not from memory.

## Learning Objectives

After completing this module you will be able to:

-   Explain what Ollama does and how it differs from calling a hosted
    API.
-   Use the CLI confidently: pull, run, list, show, ps, rm.
-   Call Ollama's native REST API directly, not just through a client
    library.
-   Write a Modelfile to customize a model's system prompt and
    parameters.
-   Reason about memory, GPU usage, and context length for a given
    model.
-   Run Ollama as a real service and know what changes when you expose
    it beyond your own machine.

## Prerequisites

-   None strictly required — this module explains Ollama from first
    principles. Chapters reference module 01 (quantization,
    parameters) and module 02 (temperature/sampling) where relevant,
    since Ollama is the delivery mechanism those chapters already
    assumed.

## Repository Structure

``` text
docs/
examples/
notebooks/
```

## Chapters

  Chapter   Topic
  --------- ---------------------------------------
  01        What Ollama Is and Why Run Models Locally
  02        Installing and Running Ollama
  03        The Ollama CLI
  04        The Native REST API
  05        The OpenAI-Compatible Endpoint
  06        Modelfiles: Customizing a Model
  07        Model Formats and Quantization
  08        Managing the Model Library
  09        GPU vs. CPU: How Ollama Chooses
  10        Context Length and Memory
  11        Concurrency and Multiple Models
  12        Embeddings via Ollama
  13        Streaming Responses
  14        Running Ollama as a Service
  15        Security: Exposing Ollama Beyond Localhost
  16        Performance Tuning
  17        Ollama vs. Other Local Runtimes
  18        Best Practices
  19        Interview Questions
  20        Glossary

## Learning Roadmap

``` text
Model Context Protocol
        ↓
AI Agents
        ↓
Ollama and LangChain          ← you are here
        ↓
Projects
```

## Hands-on Labs

-   Pull, run, and inspect a model entirely from the CLI.
-   Call the native REST API directly with `curl`, no client library.
-   Build a custom model from a Modelfile and confirm its behavior
    differs from the base model.
-   Estimate memory requirements for a model before pulling it.
-   Run two models concurrently and observe how Ollama manages them.
-   Set up Ollama as a system service that survives a reboot.

## Technologies

-   Ollama
-   `curl` (for direct REST API calls)
-   Python (`requests`, `openai`)
-   Jupyter

## Expected Outcome

You will be able to operate Ollama the way you'd operate any other
local service — comfortable with its CLI, its API, its resource
footprint, and its service lifecycle — instead of treating it as a
black box that happens to make `base_url="http://localhost:11434"`
work.

## Next Module

➡️ `09-LangChain`
