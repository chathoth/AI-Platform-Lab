# 09 - GPU vs. CPU: How Ollama Chooses

## Introduction

`ollama ps`'s `PROCESSOR` column, glanced at in chapter 03, deserves a
real explanation — how Ollama decides what runs where, and what that
decision actually costs you in speed.

## Learning Objectives

After this chapter I should be able to:

-   Read `ollama ps`'s processor column and understand what it means.
-   Explain why Ollama prefers GPU when available.
-   Recognize the symptoms of a model running entirely on CPU when it
    shouldn't be.

------------------------------------------------------------------------

# Verified: Reading the Processor Column

``` bash
ollama ps
```

Verified real output:

``` text
NAME           ID              SIZE      PROCESSOR    CONTEXT    UNTIL              
llama3.1:8b    46e0c10c039e    5.3 GB    100% GPU     4096       2 minutes from now
```

`100% GPU` means the entire model is loaded into GPU memory — the
fastest configuration. Other values you might see:

``` text
100% GPU        - fully GPU-accelerated, fastest
100% CPU          - no GPU used at all (or none available), slowest
X% GPU / Y% CPU     - split, because the model didn't fully fit in
                       available GPU memory - part runs on GPU, part
                       on CPU, at a real speed cost
```

## Why Ollama Prefers GPU

Module 01 chapter 12's parameter-count-to-memory math is exactly why
this matters: a model's parameters need to be loaded somewhere fast
enough to do the matrix math generation requires (module 01 chapter
03's forward pass, repeated every token). GPU memory (VRAM) is built
for exactly this kind of parallel computation; CPU can do it too, just
far slower for the same operation.

**Platform analogy:** this is the same reasoning behind choosing a
GPU-backed instance type for a training or inference workload over a
general-purpose CPU instance — the hardware is purpose-built for the
kind of parallel computation the workload actually needs, and the
speed difference is not subtle.

## Why a Model Might Split or Fall Back to CPU

``` text
Model doesn't fit in available VRAM entirely
  -> Ollama splits: part on GPU, part on CPU (slower than full GPU,
     faster than full CPU)

No compatible GPU detected at all
  -> Ollama falls back to CPU entirely (works, but noticeably slower,
     especially for larger models)
```

This connects directly to module 01 chapter 12's memory math — a 70B
model needing ~140GB at fp16 (or less with chapter 07's quantization)
simply won't fit in most consumer GPUs' VRAM, forcing a split or a
CPU fallback regardless of how fast the GPU itself is.

## Recognizing a CPU Fallback From Symptoms Alone

If `ollama ps` isn't checked directly, the symptom is simple: **response
generation feels dramatically slower than expected** for a model size
that should run comfortably. Checking `ollama ps`'s `PROCESSOR` column
is the fast, direct way to confirm whether that's actually what's
happening, rather than guessing.

## Hands-on: Check Your Own Setup

``` bash
ollama run llama3.1:8b "hi"   # load the model
ollama ps                       # check what processor it landed on
```

If your machine shows `100% CPU`, that's either because no compatible
GPU was detected, or because the specific model didn't fit in
available VRAM — worth knowing before assuming a slow response is a
model-choice or prompt problem instead of a hardware placement one.

## Common Misconceptions

❌ Ollama always uses the GPU if one exists in the machine.
(It uses a compatible GPU if detected and if the model fits — an
incompatible GPU, insufficient VRAM, or driver issues can all still
result in a CPU fallback.)

❌ A split GPU/CPU model runs at roughly full GPU speed.
(The CPU-resident portion is still bottlenecked by CPU speed for its
share of the computation — a real, meaningful slowdown compared to
100% GPU, not a rounding error.)

✔ `ollama ps`'s `PROCESSOR` column is the fastest, most direct way to
diagnose whether unexpectedly slow generation is a hardware placement
issue — check it before assuming the problem is elsewhere.

## Interview Questions

1.  What does `100% GPU` versus `100% CPU` mean in `ollama ps`
    output?
2.  Why might a model end up split across GPU and CPU?
3.  What's the fastest way to check whether slow generation is a
    hardware placement problem?
4.  How does module 01 chapter 12's memory math relate to whether a
    model fits fully in GPU memory?

## Summary

Ollama prefers running a model entirely on GPU for speed, falling back
to a GPU/CPU split or full CPU if the model doesn't fit in available
VRAM or no compatible GPU exists — verified directly via `ollama ps`'s
`PROCESSOR` column, which is the fastest way to diagnose unexpectedly
slow generation as a hardware placement issue rather than a prompt or
model-choice problem.

## Next Chapter

➡️ `10-Context-Length-and-Memory.md`
