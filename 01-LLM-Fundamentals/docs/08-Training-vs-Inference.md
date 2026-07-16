# 08 - Training vs Inference

## Introduction

This is a distinction I already understand instinctively from CI/CD:
**build time vs run time**. Training is the (expensive, one-time-ish)
build. Inference is the (cheap-per-call, repeated) run. Almost every
confusing "why is this so expensive / why can't I just retrain it
myself" question resolves once you separate which phase you're actually
talking about.

## Learning Objectives

After this chapter I should be able to:

-   Distinguish training from inference in terms of compute, cost, and
    frequency.
-   Explain pretraining, fine-tuning, and RLHF as distinct training
    stages.
-   Explain why inference cost and latency matter operationally, and
    training cost usually doesn't (for me, as a consumer of models).
-   Map this distinction to a CI/CD build-vs-deploy mental model.

------------------------------------------------------------------------

# Training vs Inference, Side by Side

  Aspect          Training                          Inference
  --------------- ---------------------------------- --------------------------------
  What happens    Model learns weights from data     Model uses learned weights
  Frequency       Once (or periodically, per version) Every single request
  Cost            Millions of $, weeks on GPU clusters Cents-to-dollars per million tokens
  Who does it     Model providers (mostly)           Anyone with API access or weights
  Output          A set of model weights (a file)    Generated text
  CI/CD analogy   The build pipeline                 The running service handling traffic

``` mermaid
flowchart LR
subgraph Training [Training - happens rarely]
A[Raw text corpus] --> B[Pretraining]
B --> C[Fine-tuning / RLHF]
C --> D[Model weights - the artifact]
end
subgraph Inference [Inference - happens every request]
D --> E[Load weights]
E --> F[Your prompt]
F --> G[Forward pass]
G --> H[Response]
end
```

## The Training Stages

1.  **Pretraining** — the model reads a massive, mostly-unlabeled text
    corpus and learns to predict the next token. This is where the
    bulk of the compute cost lives (this is the GPT-3-scale expense
    from chapter 02).
2.  **Fine-tuning** — the pretrained model is further trained on a
    smaller, curated dataset to specialize behavior (e.g., following
    instructions, coding well, a specific domain). Detailed in
    [14-Fine-Tuning-vs-RAG.md](14-Fine-Tuning-vs-RAG.md).
3.  **RLHF (Reinforcement Learning from Human Feedback)** — humans rank
    outputs, and that ranking further tunes the model to prefer
    helpful, safe, well-formatted responses (this is the step that
    turned GPT-3 into InstructGPT in chapter 02).

**Platform analogy:** pretraining is compiling from source. Fine-tuning
is applying a config overlay/patch on top of a known-good base image.
RLHF is closer to a policy/admission-control layer trained on real
approval/rejection decisions. Each stage produces a new "build" — a new
set of weights — that then gets deployed.

## Inference: What I Actually Operate

As a platform engineer, I almost never touch training directly — I
consume the *artifact* (the weights) and I'm responsible for the
**inference** side: serving it, scaling it, monitoring it. That's the
"run the container" half of the CI/CD analogy, and it's where my actual
job lives:

-   **Latency** — time-to-first-token and tokens/sec (chapter 03).
-   **Throughput** — concurrent requests a GPU/node can serve.
-   **Cost per request** — driven by token count (chapter 04) and model
    size (chapter 12).
-   **Scaling** — batching multiple requests together on the same GPU to
    improve utilization, same idea as connection pooling or request
    coalescing.

## Hands-on: Watch Inference Resource Usage Live

``` bash
# start serving a model
ollama run llama3.1:8b &

# watch GPU/CPU + memory while you send it a request - this IS the "run time" cost
# on macOS:
top -pid $(pgrep ollama)
# on Linux with a GPU:
watch -n 1 nvidia-smi
```

Send a few prompts of different lengths while watching this. Notice
resource usage spikes per-request, then drops — that's inference. There
is no "training" happening here at all; the weights are already fixed.
This is the exact distinction people muddle when they ask "does the
model learn from my conversation" — by default, no, inference doesn't
modify the weights at all; it's a pure read+compute operation, more like
a stateless function call than a database write.

## Common Misconceptions

❌ The model "learns" from every conversation I have with it.
(Standard inference is stateless with respect to weights — nothing
about your chat changes the underlying model, unless a provider
explicitly opts you into a separate training/feedback pipeline.)

❌ Training and inference cost roughly the same per use.
(Training is a massive one-time-ish cost amortized across millions of
users; inference is a small, repeated per-request cost — like comparing
the cost of building a Docker image once vs. running a container a
million times.)

✔ When someone says "call the model," they always mean inference. When
someone says "train/fine-tune the model," that's an entirely separate,
far more expensive, far less frequent operation.

## Interview Questions

1.  What's the difference between training and inference, in terms of
    frequency and cost?
2.  Name the three main training stages and what each one produces.
3.  Does a model "remember" a previous conversation by default? Why or
    why not?
4.  Which phase — training or inference — is a platform/DevOps engineer
    most likely to actually operate, and why?

## Summary

Training builds the model (rare, expensive, produces a weights
artifact); inference runs it (frequent, cheap-per-call, produces
responses) — the same shape as a CI/CD build vs. a running deployment.
Nearly all of my day-to-day work with LLMs lives entirely on the
inference side.

## Next Chapter

➡️ `09-Context-Window.md`
