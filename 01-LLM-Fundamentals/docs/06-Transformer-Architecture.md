# 06 - Transformer Architecture

## Introduction

Chapter 02 called the 2017 Transformer the real inflection point in LLM
history. This chapter opens up what's actually inside that box. I find
it easiest to read a Transformer the way I'd read a microservice
architecture diagram: a fixed set of components, wired together in a
repeatable pattern, stacked N times like replicas behind a load
balancer.

## Learning Objectives

After this chapter I should be able to:

-   Name the core components of a Transformer block.
-   Explain what "stacking layers" means and why it improves quality.
-   Explain the difference between encoder-only, decoder-only, and
    encoder-decoder architectures.
-   Identify which architecture family GPT, BERT, and T5 belong to.

------------------------------------------------------------------------

# Anatomy of a Transformer Block

``` mermaid
flowchart TB
A[Input Embeddings + Positional Encoding] --> B[Multi-Head Self-Attention]
B --> C[Add and Norm]
C --> D[Feed-Forward Network]
D --> E[Add and Norm]
E --> F[Output -> next layer]
```

This single block is **stacked N times** (32 layers for a 7-8B model,
80+ for the largest models) — output of layer 1 becomes input of layer
2, and so on. Each layer refines the representation a bit further.

**Platform analogy:** this is identical in shape to a middleware chain
or a Kubernetes admission-webhook chain — a fixed-shape unit
(attention → normalize → feed-forward → normalize) repeated in a
pipeline, where each stage passes a transformed version of the request
to the next. More layers = more chances to refine understanding, at the
cost of more compute per request — exactly the latency/quality trade-off
I already navigate when deciding how many processing stages to put in a
pipeline.

## The Components, Briefly

-   **Positional encoding** — since attention looks at all tokens at
    once (chapter 07), the model has no built-in sense of *order*.
    Positional encoding injects "this token is at position 5" into the
    embedding so word order still matters (`"dog bites man"` ≠
    `"man bites dog"`).
-   **Multi-head self-attention** — the mechanism that lets each token
    look at every other token and decide what's relevant. Full
    treatment in [07-Attention-Mechanism.md](07-Attention-Mechanism.md).
-   **Add & Norm (residual connection + layer normalization)** — adds
    the block's input back to its output before normalizing.
    Operationally this is a stability mechanism — it's what keeps
    gradients from exploding/vanishing across dozens of stacked layers,
    the training-time equivalent of a circuit breaker.
-   **Feed-forward network** — a small per-token neural net applied
    identically to every position, adding non-linear transformation
    capacity.

## Three Architecture Families

  Family            Uses            Examples
  ----------------- ---------------- ------------------------------
  Encoder-only       Understanding    BERT — classification, search
  Decoder-only       Generation       GPT, Claude, Llama, Mistral
  Encoder-decoder    Transform text   T5, original translation models

Almost everything you interact with day to day — ChatGPT, Claude, the
model behind your coding assistant — is **decoder-only**: it reads the
prompt and generates output one token at a time, attending only to
previous tokens (causal attention). That architectural choice is *why*
generation is inherently sequential/streaming, tying directly back to
the pipeline described in
[03-How-LLMs-Work.md](03-How-LLMs-Work.md).

## Hands-on: See the Layer Count for Yourself

``` bash
ollama show llama3.1:8b --modelfile
```

or, if you inspect the model config directly (e.g. from a Hugging Face
`config.json`):

``` bash
curl -s https://huggingface.co/meta-llama/Meta-Llama-3.1-8B/resolve/main/config.json | \
  python3 -c "import json,sys; c=json.load(sys.stdin); print('layers:', c['num_hidden_layers'], '| attention heads:', c['num_attention_heads'])"
```

Compare `num_hidden_layers` across an 8B and a 70B variant of the same
model family — larger models are mostly just **more of the same block,
stacked deeper and wider**, not a different architecture. That's a
useful mental model when someone asks "why does the bigger model cost
so much more to serve" — it's literally more sequential compute per
token, same block repeated more times.

## Common Misconceptions

❌ Bigger models use a fundamentally different architecture.
(Usually it's the same Transformer block, just more layers, wider
layers, and more attention heads — depth/width, not a new design.)

❌ The Transformer processes the whole sequence and it's magically
"aware" of everything.
(Decoder-only models can only attend to *previous* tokens during
generation — that's what "causal" attention means.)

✔ Every popular chat model you use (GPT, Claude, Llama, Mistral,
Gemini) is decoder-only — same architectural family, different training
data, training recipe, and scale.

## Interview Questions

1.  Name the four main components of a Transformer block, in order.
2.  Why is positional encoding necessary if attention already looks at
    every token?
3.  What's the practical difference between encoder-only and
    decoder-only architectures?
4.  Why do larger models generally cost more to serve per token, given
    they use "the same" architecture as smaller ones?

## Summary

A Transformer is a repeatable block — attention, normalize, feed-forward,
normalize — stacked many times, the same way a middleware chain is a
repeatable unit stacked into a pipeline. Nearly every model I'll deploy
or call is decoder-only, generating one token at a time by attending
only to what came before.

## Next Chapter

➡️ `07-Attention-Mechanism.md`
