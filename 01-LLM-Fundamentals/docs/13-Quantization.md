# 13 - Quantization

## Introduction

Quantization is the lever that actually made self-hosting LLMs
practical for me. Chapter 12 showed a 70B model needs ~140GB of VRAM at
full precision — way beyond anything I have on hand. Quantization is
how that same model runs on a single consumer GPU, at some cost to
precision. This is directly analogous to image/video compression, or
choosing a smaller instance type by trading some headroom for cost —
a trade-off I make constantly.

## Learning Objectives

After this chapter I should be able to:

-   Explain what quantization is and what it trades off.
-   Read common quantization notation (fp16, int8, Q4_K_M, etc.).
-   Estimate memory savings from quantization.
-   Decide when quantization is an acceptable trade-off for a real
    workload.

------------------------------------------------------------------------

# What Quantization Actually Does

Every parameter (chapter 12) is a number stored at some **precision** —
how many bits are used to represent it. Quantization reduces that
precision, shrinking memory footprint and speeding up compute, at the
cost of some accuracy.

``` text
fp32 (32-bit): 3.14159265358979...   ← full precision, 4 bytes/param
fp16 (16-bit): 3.140625              ← "half precision", 2 bytes/param
int8  (8-bit): 3                     ← 1 byte/param
int4  (4-bit): ~3 (very coarse)      ← 0.5 bytes/param
```

Applied across billions of parameters, dropping from fp16 to int4 roughly
**quarters** the memory footprint:

  Precision   Bytes/param   70B model memory (rough)
  ----------- ------------- ---------------------------
  fp32        4             ~280 GB
  fp16        2             ~140 GB
  int8        1             ~70 GB
  int4        0.5           ~35 GB

That's the difference between "needs a GPU cluster" and "runs on a
single high-end consumer GPU or a beefy laptop."

## Platform Analogy: This Is Lossy Compression for Weights

I think of quantization exactly like choosing a compression codec:

-   **fp32/fp16** ≈ lossless/near-lossless — highest fidelity, biggest
    footprint.
-   **int8** ≈ a solid lossy compression — noticeably smaller, quality
    loss usually small enough not to matter for most tasks.
-   **int4** ≈ aggressive compression — real quality loss becomes
    noticeable on harder reasoning/precise-output tasks, but often still
    "good enough" for many workloads, similar to trading some video
    quality for a much smaller file.

Same principle as picking a compression level for logs before shipping
them off-node, or choosing a smaller/cheaper instance type that's "good
enough" for a given SLA instead of always provisioning for peak
headroom — you're trading a resource (memory/compute) against a quality
metric (accuracy), and the right point on that curve depends entirely on
the workload.

## Reading Quantization Notation (GGUF / Ollama style)

You'll see model names like `llama3.1:8b-instruct-q4_K_M`. Breaking that
down:

-   `q4` — roughly 4 bits per weight.
-   `K` — a specific quantization method (k-quants), generally better
    quality-per-bit than naive rounding.
-   `M` — "medium" variant within that method (S/M/L trade size vs
    quality further).

``` bash
ollama list
# NAME                     SIZE
# llama3.1:8b               4.7 GB   ← this is already a quantized default
# llama3.1:8b-instruct-fp16 16 GB    ← full precision, for comparison
```

Ollama defaults to a quantized (usually Q4) version specifically because
that's the sweet spot for running well on typical consumer/workstation
hardware — worth knowing so you're not surprised the "full" model is
3-4x larger on disk.

## Hands-on: Feel the Trade-off Directly

``` bash
ollama pull llama3.1:8b              # quantized default (~Q4)
ollama pull llama3.1:8b-instruct-fp16 # full precision

du -sh ~/.ollama/models/blobs/*      # compare file sizes directly

# ask both a precise reasoning question and compare answers
ollama run llama3.1:8b "A train leaves at 3pm going 60mph, another leaves at 4pm going 90mph on the same route. When does the second train catch up?"
ollama run llama3.1:8b-instruct-fp16 "A train leaves at 3pm going 60mph, another leaves at 4pm going 90mph on the same route. When does the second train catch up?"
```

For most everyday tasks (summarizing, chatting, simple code) the two
will look nearly identical. On precise multi-step math/logic, the
quantized version is more likely to slip. That gap — small for most
tasks, real for precision-sensitive ones — is exactly the judgment call
to make before choosing a quantization level for a production workload.

## Common Misconceptions

❌ Quantization always noticeably degrades quality.
(For most conversational/summarization tasks, int8 and even int4 are
close to indistinguishable from full precision in practice — the
degradation shows up most on precise math/logic-heavy tasks.)

❌ Quantization is something only model providers do.
(You can quantize a model yourself with tools like `llama.cpp` or
`bitsandbytes` — it's a deployment-time optimization, not a
training-time-only decision.)

✔ The memory savings are close to linear with bit-width — going from
fp16 to int4 roughly quarters memory footprint, which is usually the
deciding factor for whether self-hosting a given model size is even
possible on the hardware you have.

## Interview Questions

1.  What does quantization trade off, and why does it save memory?
2.  Roughly how much memory would a 13B model need at int4 vs fp16?
3.  What does `q4_K_M` mean in a model name like
    `llama3.1:8b-instruct-q4_K_M`?
4.  Under what conditions would you choose fp16 over a quantized model
    for a production workload?

## Summary

Quantization reduces the precision used to store each parameter,
shrinking memory footprint (and often improving speed) at some cost to
accuracy — the same lossy-compression trade-off used everywhere else in
infrastructure. It's what makes running a 7-70B model on commodity
hardware possible at all, and picking the right quantization level is a
workload-specific judgment call, not a universal default.

## Next Chapter

➡️ `14-Fine-Tuning-vs-RAG.md`
