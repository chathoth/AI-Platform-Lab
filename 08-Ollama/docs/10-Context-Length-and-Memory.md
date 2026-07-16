# 10 - Context Length and Memory

## Introduction

Chapter 03's `ollama show` output listed `context length: 131072` for
`llama3.1:8b` — module 01 chapter 09's context window, now a real,
checkable number for a specific model, plus the memory cost that comes
with actually using it.

## Learning Objectives

After this chapter I should be able to:

-   Read a model's maximum context length directly.
-   Set a smaller, practical context window with `num_ctx`.
-   Explain why context length and memory usage are directly linked.

------------------------------------------------------------------------

# Verified: A Model's Real Context Length

``` bash
ollama show llama3.1:8b
```

``` text
context length    131072
```

This is the model's architectural maximum — module 01 chapter 09's
context window, for this exact model. `ollama ps` showed a different,
smaller number earlier in this module:

``` text
CONTEXT    4096
```

That's the **active** context window for the currently loaded
instance — Ollama defaults to a smaller working context than the
architectural maximum, because the max context window costs real
memory (below) whether or not you're actually using that much.

## Why Context Length Costs Memory Directly

Module 01 chapter 07's attention mechanism computes relationships
between every pair of tokens in context — the memory needed for that
computation (the KV-cache, module 01 chapter 07) scales with context
length. A larger `num_ctx` means more memory reserved for that cache,
regardless of how much of it a given request actually uses.

``` text
Small context window:   less memory reserved, faster to allocate,
                           but longer conversations get truncated sooner
                           (module 01 chapter 09)
Large context window:     more memory reserved upfront, supports much
                           longer conversations/documents, at a real
                           memory cost even for short requests
```

## Setting a Custom Context Window

``` bash
# via the API, per request
curl -s http://localhost:11434/api/chat -d '{
  "model": "llama3.1:8b",
  "messages": [{"role": "user", "content": "hi"}],
  "options": {"num_ctx": 8192},
  "stream": false
}'
```

``` text
# via a Modelfile (chapter 06), as a persistent default
PARAMETER num_ctx 8192
```

**Platform analogy:** this is the same trade-off as sizing a
connection pool or a buffer — too small and you hit limits sooner than
necessary (module 01 chapter 09's context overflow); too large and
you're reserving resources you usually don't need, for every request,
whether or not it uses them.

## Choosing a Context Window Size Deliberately

  Use case                                 Reasonable `num_ctx`
  --------------------------------------------- --------------------------------
  Short Q&A, no long documents                     2048-4096 (Ollama's typical default)
  RAG with moderately long retrieved chunks (module 05) | 8192-16384
  Long documents, long agent conversations (module 07)    32768+, if the model's architecture supports it and memory allows

Never set `num_ctx` higher than the model's actual maximum (chapter
03's `ollama show` output) — doing so has no effect beyond that
ceiling, since the model architecture itself caps it.

## Hands-on: Compare Memory Behavior at Two Context Sizes

``` bash
ollama run llama3.1:8b "hi"
ollama ps   # note the CONTEXT column and SIZE

ollama stop llama3.1:8b
curl -s http://localhost:11434/api/generate -d '{"model": "llama3.1:8b", "prompt": "hi", "options": {"num_ctx": 32768}, "stream": false}' > /dev/null
ollama ps   # note the CONTEXT column and SIZE again - both should be larger
```

Compare the `SIZE` column between the two runs — a larger `num_ctx`
should show up as measurably more memory reserved, even for the exact
same short prompt.

## Common Misconceptions

❌ A model's context length in `ollama show` is what's actually being
used right now.
(That's the architectural maximum — the active window, shown in
`ollama ps`, is often smaller by default and configurable via
`num_ctx`.)

❌ Setting a huge `num_ctx` is free as long as your machine has enough
RAM.
(It reserves that memory for the KV-cache regardless of whether a
given request needs it — reserving more than necessary is real,
avoidable waste, the same as over-provisioning any other resource.)

✔ `num_ctx` is a real, per-request or per-model-default lever — size
it to the task, the same right-sizing instinct module 01 chapter 12
applied to model/parameter choice.

## Interview Questions

1.  What's the difference between a model's maximum context length
    and its currently active context window?
2.  Why does a larger context window cost more memory, even for a
    short prompt?
3.  How would you set a custom context window for a specific request?
4.  What determines the practical ceiling for `num_ctx`?

## Summary

A model's architectural maximum context length (`ollama show`) and its
currently active context window (`ollama ps`, configurable via
`num_ctx`) are two different numbers — the active window defaults
smaller because reserving context-window memory (the KV-cache) costs
real resources regardless of use. Size `num_ctx` deliberately to the
task, the same right-sizing discipline applied to model choice
elsewhere in this repository.

## Next Chapter

➡️ `11-Concurrency-and-Multiple-Models.md`
