# 11 - Concurrency and Multiple Models

## Introduction

This repository has pulled four different models (chapter 08) — a real
setup, worth understanding: what happens when more than one model is
loaded at once, and what happens when multiple requests hit Ollama at
the same time.

## Learning Objectives

After this chapter I should be able to:

-   Explain what happens in memory when a second model is loaded.
-   Explain how Ollama handles concurrent requests.
-   Reason about whether your machine can handle a given multi-model
    setup.

------------------------------------------------------------------------

# Multiple Models Can Be Loaded Simultaneously

``` bash
ollama run llama3.1:8b "hi"
ollama run nomic-embed-text "hi"   # via /api/embeddings normally, simplified here
ollama ps
```

Both can show up in `ollama ps` at once, each with its own memory
footprint — Ollama doesn't require unloading one model before loading
another, up to whatever your machine's memory (GPU and/or system RAM)
can actually hold.

``` text
NAME                       SIZE      PROCESSOR
llama3.1:8b                5.3 GB    100% GPU
nomic-embed-text:latest    ~0.3 GB   100% GPU
```

This is exactly why this repository could run module 03's embedding
examples and module 07's agent examples using different models without
manually unloading anything between them — Ollama managed that
automatically.

## What Happens When Memory Runs Out

If loading a new model would exceed available memory, Ollama evicts
the least-recently-used model to make room — the same eviction policy
any resource-constrained cache uses. This is transparent (you don't
have to manage it manually) but worth knowing about, since it means a
model you expect to still be "warm" might have been evicted by a
different model's recent use.

**Platform analogy:** this is an LRU cache, applied to loaded models
instead of application data — the same trade-off: automatic and
convenient, but occasionally surprising when something you expected to
be fast (because it was recently used) has actually been evicted.

## Concurrent Requests to the Same Model

Ollama can handle multiple simultaneous requests to the same loaded
model, queuing or parallelizing depending on configuration and
available resources (`OLLAMA_NUM_PARALLEL`, an environment variable
covered further in chapter 16). This matters directly for module 07's
agent examples — if an application makes several tool-calling requests
in quick succession, Ollama is the layer handling whether those run
concurrently or queue.

## Hands-on: Load Two Models and Watch Memory

``` bash
ollama run llama3.1:8b "hi"
ollama run llama3.2:3b "hi"
ollama ps
```

Confirm both show up simultaneously, each with its own `SIZE`. Then
check total memory: does your machine comfortably hold both, or is one
already showing signs of being CPU-bound (chapter 09) because GPU
memory ran out?

## Common Misconceptions

❌ Only one model can be loaded into memory at a time.
(Multiple models can coexist, limited only by available memory —
verified directly by loading two different models simultaneously and
confirming both appear in `ollama ps`.)

❌ Loading a new model when memory is full causes an error.
(Ollama evicts the least-recently-used model automatically, the same
transparent eviction behavior as any LRU-based resource cache — no
error, just a model you might have expected to still be warm getting
unloaded.)

✔ `ollama ps`, checked periodically, is the way to see exactly what's
resident in memory right now — useful for understanding why a call to
a model you used five minutes ago might suddenly be slow (it got
evicted and needs a fresh load).

## Interview Questions

1.  Can more than one model be loaded into memory simultaneously?
2.  What happens when loading a new model would exceed available
    memory?
3.  How is Ollama's model eviction policy similar to an LRU cache?
4.  Why might a model that was fast five minutes ago suddenly be slow
    again?

## Summary

Ollama can hold multiple models in memory simultaneously, limited by
available resources, and automatically evicts the least-recently-used
model when memory runs out — the same LRU behavior as any resource-
constrained cache, verified directly by loading two models at once and
watching `ollama ps`. This transparent management is what let this
repository switch between chat and embedding models across modules
without any manual unloading.

## Next Chapter

➡️ `12-Embeddings-via-Ollama.md`
