# 20 - Glossary

## Introduction

Every term from this module, in one place, defined the way I actually
think about it — with the platform/infra analogy attached where one
helped it stick. Alphabetical, so it's fast to scan as a reference
rather than read top to bottom.

------------------------------------------------------------------------

**Attention** — The mechanism letting each token weigh the relevance of
every other token when building its representation. Computed fresh per
request, like dynamic weighted routing instead of a static table. See
[07-Attention-Mechanism.md](07-Attention-Mechanism.md).

**Autoregressive** — Generating output one token at a time, where each
new token is fed back in as input for producing the next one. See
[03-How-LLMs-Work.md](03-How-LLMs-Work.md).

**BPE (Byte-Pair Encoding)** — The subword tokenization algorithm that
builds a vocabulary from frequent character/word chunks, so any input —
even unseen words — can always be tokenized. See
[04-Tokens-and-Tokenization.md](04-Tokens-and-Tokenization.md).

**Context Window** — The hard token ceiling (input + output combined)
for a single request. Functions like a strict memory limit — exceed it
and the call fails or gets truncated. See
[09-Context-Window.md](09-Context-Window.md).

**Decoder-only** — The Transformer variant used by nearly every chat
model (GPT, Claude, Llama, Mistral) — generates text by attending only
to previous tokens. See
[06-Transformer-Architecture.md](06-Transformer-Architecture.md).

**Embedding** — A dense numeric vector representing the meaning of a
piece of text, positioned so semantically similar text lands close by
in vector space — a different kind of search index, keyed by meaning
instead of exact terms. See
[05-Embeddings-Basics.md](05-Embeddings-Basics.md).

**Fine-tuning** — Further training a pretrained model on a curated
dataset to change its weights and specialize its behavior. Like baking
config into a Docker image at build time. See
[14-Fine-Tuning-vs-RAG.md](14-Fine-Tuning-vs-RAG.md).

**GGUF** — A common file format for quantized, locally-servable model
weights (used by Ollama/llama.cpp).

**Hallucination** — A confidently generated, plausible-sounding, but
factually wrong response — the LLM equivalent of an HTTP 200 with the
wrong body: no error signal, has to be caught by grounding or
verification. See [11-Hallucinations.md](11-Hallucinations.md).

**Inference** — Running a trained model to produce output for a given
input; the "run time" half of the training/inference split, stateless
per call. See
[08-Training-vs-Inference.md](08-Training-vs-Inference.md).

**KV-cache (Key/Value cache)** — Reusing previously computed
attention Key/Value vectors instead of recomputing them for every new
token, essential for reasonable multi-turn chat latency. See
[07-Attention-Mechanism.md](07-Attention-Mechanism.md).

**Multi-head attention** — Running several attention computations in
parallel, each able to specialize on a different kind of relationship
between tokens — like several independent health-check probes examining
the same request from different angles. See
[07-Attention-Mechanism.md](07-Attention-Mechanism.md).

**Parameter** — A single learned weight inside the model. Total
parameter count is the primary driver of the hardware (memory) needed
to run a model. See [12-Model-Parameters.md](12-Model-Parameters.md).

**Pretraining** — The first, most compute-expensive training stage,
where a model learns next-token prediction over a massive text corpus.
See [08-Training-vs-Inference.md](08-Training-vs-Inference.md).

**Prompt Injection** — Untrusted content in a prompt containing
instructions designed to override the system prompt — the LLM
equivalent of SQL injection. See
[17-LLM-Limitations.md](17-LLM-Limitations.md).

**Quantization** — Reducing the numeric precision used to store each
parameter (e.g. fp16 → int4) to shrink memory footprint and speed up
inference, at some cost to accuracy — lossy compression for weights.
See [13-Quantization.md](13-Quantization.md).

**RAG (Retrieval-Augmented Generation)** — Retrieving relevant
documents at request time and injecting them into the prompt, instead
of relying on the model's trained-in memory — like mounting a config
map at runtime instead of baking data into an image. See
[14-Fine-Tuning-vs-RAG.md](14-Fine-Tuning-vs-RAG.md).

**RLHF (Reinforcement Learning from Human Feedback)** — A training
stage where human rankings of model outputs are used to tune the model
toward helpful, instruction-following behavior — the step that turned
GPT-3 into InstructGPT. See
[02-History-of-LLMs.md](02-History-of-LLMs.md).

**Sampling** — Probabilistically selecting the next token from the
model's output distribution, as opposed to always picking the top token
(greedy decoding). Controlled by temperature and top-p. See
[10-Temperature-TopP-and-Sampling.md](10-Temperature-TopP-and-Sampling.md).

**Temperature** — A parameter controlling how "flat" (random) or
"peaked" (deterministic) the token sampling distribution is — a jitter
dial, low for scripts/pipelines, higher for creative/exploratory use.
See
[10-Temperature-TopP-and-Sampling.md](10-Temperature-TopP-and-Sampling.md).

**Token** — The unit of text an LLM actually processes — sometimes a
whole word, often a subword chunk. The real unit of cost, rate limits,
and context-window usage. See
[04-Tokens-and-Tokenization.md](04-Tokens-and-Tokenization.md).

**Top-p (Nucleus Sampling)** — Restricting token sampling to the
smallest set of tokens whose cumulative probability crosses a threshold
`p` — a percentile-based cutoff, like alerting on p90/p99 instead of a
fixed value. See
[10-Temperature-TopP-and-Sampling.md](10-Temperature-TopP-and-Sampling.md).

**Transformer** — The neural network architecture (introduced 2017)
built around self-attention, replacing RNNs' sequential bottleneck with
parallelizable computation — the architectural foundation of every
modern LLM. See
[06-Transformer-Architecture.md](06-Transformer-Architecture.md).

------------------------------------------------------------------------

## Module Complete

That closes out all 20 chapters of **01-LLM-Fundamentals**. Next up per
the [README](../README.md) roadmap:

➡️ `02-Prompt-Engineering`
