# 07 - Model Formats and Quantization

## Introduction

Module 01 chapter 13 covered quantization conceptually. This chapter
is the Ollama-specific, verified version: what format Ollama actually
stores models in, and how to read the quantization level directly off
a real, already-pulled model.

## Learning Objectives

After this chapter I should be able to:

-   Explain what GGUF is and why Ollama uses it.
-   Read a model's actual quantization level with `ollama show`.
-   Choose a quantization tag deliberately when pulling a model.

------------------------------------------------------------------------

# GGUF: The Format Underneath Every Pulled Model

Every model Ollama runs is stored as a **GGUF** file — the format
`llama.cpp` (chapter 01) uses, purpose-built for efficient local
inference, bundling weights, metadata, and tokenizer info into one
file per model.

## Verified: Reading a Real Model's Quantization

``` bash
ollama show llama3.1:8b
```

Verified real output:

``` text
  Model
    architecture        llama     
    parameters          8.0B      
    context length      131072    
    embedding length    4096      
    quantization        Q4_K_M    
```

`quantization: Q4_K_M` confirms this exact model is running at
roughly 4 bits per parameter, using the "K-quant, medium" method —
module 01 chapter 13's `q4_K_M` notation, now read directly off a real,
already-pulled model instead of inferred from a naming convention.

## Choosing a Quantization Level When Pulling

``` bash
ollama pull llama3.1:8b            # default tag - usually a Q4 quantization
ollama pull llama3.1:8b-instruct-fp16   # full precision, if available for that model
ollama pull llama3.1:8b-instruct-q8_0    # int8-ish, a middle ground
```

Not every model has every quantization level published — check the
model's page on Ollama's library (chapter 08) for what's actually
available before assuming a specific tag exists.

## The Trade-off, Verified in Practice

Module 01 chapter 13 already covered the theory (lower precision =
smaller footprint, some accuracy cost). Here's how to check it
directly on your own machine:

``` bash
ollama list
```

Compare the `SIZE` column across quantization variants of the same
model if you have more than one pulled — the size difference directly
reflects the bits-per-parameter difference chapter 13 predicted, on
your own real disk usage instead of a theoretical estimate.

## Hands-on: Check Every Locally Pulled Model's Quantization

``` bash
for model in $(ollama list | tail -n +2 | awk '{print $1}'); do
  echo "--- $model ---"
  ollama show "$model" | grep -A1 quantization
done
```

Run this against your own pulled models and confirm every one has a
real, readable quantization level — this is the ground truth module
01 chapter 13's theory maps onto.

## Common Misconceptions

❌ All models pulled from Ollama's library are full precision by
default.
(The default tag for most models is a quantized variant, typically
Q4 — full precision (`fp16`) usually needs to be pulled explicitly, if
published for that model at all.)

❌ GGUF is Ollama-specific.
(It's `llama.cpp`'s format, used by several local inference tools —
Ollama is one consumer of it, not its creator.)

✔ `ollama show <model>` is the definitive way to check a model's real
quantization level — don't infer it from the tag name alone if the
tag doesn't explicitly state it.

## Interview Questions

1.  What is GGUF, and why does Ollama use it?
2.  How would you check a specific pulled model's actual quantization
    level?
3.  What does `Q4_K_M` mean, in terms of module 01 chapter 13's
    quantization discussion?
4.  Why might two models with the same name but different tags have
    very different `SIZE` values in `ollama list`?

## Summary

Ollama stores every model as a GGUF file, and `ollama show` reveals
the real, verified quantization level (`Q4_K_M` for this module's
`llama3.1:8b`, at time of writing) — the concrete, checkable version
of module 01 chapter 13's quantization theory. Choosing a quantization
tag when pulling is a deliberate trade-off between disk/memory
footprint and precision, worth checking directly rather than assumed.

## Next Chapter

➡️ `08-Managing-the-Model-Library.md`
