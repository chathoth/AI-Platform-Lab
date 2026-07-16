# 12 - Model Parameters

## Introduction

"Parameters" is the number everyone quotes (7B, 70B, 405B) but it took
me a while to connect it to something I could size infrastructure
against. I now think of parameter count the way I think of a service's
memory footprint or instance size — it's the number that most directly
predicts how much hardware I need and how fast the thing will respond.

## Learning Objectives

After this chapter I should be able to:

-   Explain what a "parameter" is in a neural network.
-   Explain why parameter count correlates with capability *and* cost.
-   Estimate the memory needed to run a given model size.
-   Choose an appropriately sized model for a given deployment
    constraint.

------------------------------------------------------------------------

# What Is a Parameter?

A parameter is a single learned number (a weight) inside the model — one
entry in one of the matrices used in the embedding layer, attention
heads, and feed-forward networks described in
[06-Transformer-Architecture.md](06-Transformer-Architecture.md). A
"7B model" has 7 billion of these numbers, all learned during training,
all involved (to varying degrees) in every single forward pass.

``` text
"70B model" = 70,000,000,000 individual learned weights
              spread across embedding tables, attention matrices,
              and feed-forward layers, repeated across every stacked layer
```

More parameters generally means more capacity to capture nuanced
patterns — but it's not free capacity. Every one of those numbers has to
be loaded into memory and multiplied against your input on every
forward pass.

## Platform Analogy: Parameter Count ≈ Instance Sizing

This is the most directly *actionable* number in this whole module for
someone doing capacity planning:

  Model size   Rough memory needed (fp16)   Comparable to
  ------------ ----------------------------- --------------------------------
  7B           ~14 GB VRAM                   A single decent consumer GPU
  13B          ~26 GB VRAM                   A workstation GPU (24-48GB)
  70B          ~140 GB VRAM                  Multi-GPU node
  405B         ~810 GB VRAM                  A full GPU cluster

Rule of thumb: **~2 bytes of memory per parameter at fp16 precision**
(2 × parameter count = GB needed, roughly). That single formula is what
lets me answer "can I run this on the box I have" before I even try —
same reflex as checking a container's memory request against node
capacity before scheduling it. Quantization (chapter 13) is the lever
for shrinking that number further.

## Parameters vs Capability: Diminishing Returns, Not a Straight Line

Bigger isn't strictly better in a way that ignores everything else:

-   **Training data quality** matters as much as size — a well-trained
    7B model can outperform a poorly-trained 30B model on real tasks.
-   **Task fit** matters — a small model fine-tuned narrowly for one
    job (e.g., classifying log severity) can beat a giant general-purpose
    model on that specific job, at a fraction of the cost/latency.
-   **Latency budget** — if a use case needs a sub-second response, a
    405B model may simply be operationally disqualified regardless of
    how much better its answers are.

**Platform analogy:** this is the exact same reasoning as picking an
instance type. You don't default to the biggest available machine for
every workload — you right-size against the actual job, because bigger
means slower cold starts, higher cost, and more resource contention,
not automatically "better."

## Hands-on: Compare Sizes on Your Own Hardware

``` bash
ollama pull llama3.1:8b
ollama pull llama3.1:70b   # skip if you don't have the RAM/VRAM for this

# compare load time and response latency
time ollama run llama3.1:8b "Explain what a Kubernetes StatefulSet is, briefly"
time ollama run llama3.1:70b "Explain what a Kubernetes StatefulSet is, briefly"

# compare actual disk/memory footprint
ollama list
```

Notice the size difference in `ollama list` output tracks roughly with
the memory rule of thumb above. If the 70B model struggles to even load
on your machine, that's the parameter-count-to-hardware relationship
showing up directly — the same wall you'd hit trying to schedule a pod
that requests more memory than any node in the cluster has.

## Common Misconceptions

❌ More parameters always means a better model for my use case.
(It means more *capacity*, not automatically better fit — a
well-trained smaller model can win on a narrow task, and will always
win on cost and latency.)

❌ Parameter count is the only thing that determines quality.
(Training data quality, fine-tuning, and RLHF quality routinely matter
as much or more — see chapter 08.)

✔ Parameter count is the single best predictor of the *hardware* you
need to self-host a model — that's the number to check first before
committing to a self-hosting plan.

## Interview Questions

1.  What is a parameter, concretely, inside a neural network?
2.  Roughly how much memory does a 70B parameter model need to run at
    fp16 precision?
3.  Why isn't a bigger model automatically the right choice for a given
    use case?
4.  What other factors, besides parameter count, determine model
    quality?

## Summary

A parameter is one learned weight in the model, and the total count is
the single best predictor of the hardware needed to run it — roughly 2
bytes of memory per parameter at fp16. Bigger models have more capacity,
but capability also depends heavily on training data quality and task
fit, so "biggest available" is rarely the right default, the same way
it isn't for instance sizing.

## Next Chapter

➡️ `13-Quantization.md`
