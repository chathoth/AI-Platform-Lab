# 03 - How LLMs Work

## Introduction

I already know how a request flows through a system I operate: it hits
a load balancer, gets routed, passes through some middleware, gets
processed, and a response comes back. An LLM request has a very similar
**pipeline shape** — the difference is what happens inside the
"processing" box. This chapter walks that pipeline end to end, the way
I'd document a request flow for a service I'm on call for.

## Learning Objectives

After this chapter I should be able to:

-   Describe the full request → response pipeline for an LLM call.
-   Explain what happens at each stage: tokenize → embed → transform →
    predict → decode.
-   Map each stage to something concrete I can observe (latency,
    tokens, logs).
-   Explain why generation is a **loop**, not a single call.

------------------------------------------------------------------------

# The Request Pipeline

``` mermaid
flowchart LR
A[Prompt] --> B[Tokenizer]
B --> C[Embedding Layer]
C --> D[Transformer Stack - N layers]
D --> E[Next-token Probabilities]
E --> F[Sampling]
F --> G[Append token to sequence]
G -->|repeat until stop token or max_tokens| B
G --> H[Detokenize -> Response]
```

Reading this the way I'd read a service diagram:

1.  **Tokenizer** — a stateless preprocessing step. Same job as a
    request validator/normalizer sitting in front of your API. Covered
    in [04-Tokens-and-Tokenization.md](04-Tokens-and-Tokenization.md).
2.  **Embedding layer** — converts each token ID into a vector. This is
    a lookup table, effectively an in-memory cache keyed by token ID.
3.  **Transformer stack** — the actual "compute." Dozens of identical
    layers stacked on top of each other, each one refining the
    representation using self-attention. Covered in
    [06-Transformer-Architecture.md](06-Transformer-Architecture.md) and
    [07-Attention-Mechanism.md](07-Attention-Mechanism.md).
4.  **Next-token probabilities** — the model doesn't output "the
    answer," it outputs a probability distribution over the entire
    vocabulary for what token comes next.
5.  **Sampling** — a token is picked from that distribution (greedy,
    or randomized via temperature/top-p — see
    [10-Temperature-TopP-and-Sampling.md](10-Temperature-TopP-and-Sampling.md)).
6.  **Loop** — the new token gets appended to the sequence and the
    *entire* forward pass repeats to produce the next one. This is the
    single most important operational fact about LLMs: **one API call
    that "writes a paragraph" is actually hundreds of forward passes
    under the hood.**

## Platform Analogy: This Is a Streaming Job, Not a Request/Response Call

When I first called an LLM API I expected request-in, response-out,
like a REST call. What actually happens is closer to a **long-running
streaming job**:

-   Time-to-first-token (TTFT) ≈ the time to run the prompt through the
    model once.
-   Every subsequent token costs another forward pass.
-   Total latency ≈ `TTFT + (tokens_generated × per-token latency)`.

That's why in production I care about **tokens/sec throughput** the
same way I'd care about requests/sec on a normal service — it directly
drives autoscaling and cost decisions.

## Hands-on: Watch the Loop Yourself

``` bash
# stream tokens as they're generated - watch the loop happen in real time
curl -N http://localhost:11434/api/generate -d '{
  "model": "llama3.1:8b",
  "prompt": "List 5 benefits of Kubernetes",
  "stream": true
}'
```

Each JSON line you see streamed back is **one iteration of the loop**
above — one token (or a few), not the whole answer at once. Time how
long the first line takes vs. the total response time — that gap is
your TTFT vs. total generation time, the same split you'd track for any
streaming API.

## Common Misconceptions

❌ The model "writes" the whole response at once, then sends it.

❌ A slow response means the model is "thinking harder" about your
question.
(It just means more tokens are being generated — length drives latency
far more than difficulty does.)

✔ Generation is next-token prediction, repeated in a loop, until a stop
condition (stop token, max tokens, or a stop sequence you configured)
is hit.

## Interview Questions

1.  Walk through the full pipeline from prompt to response.
2.  Why is LLM inference described as "autoregressive"?
3.  What's the difference between time-to-first-token and total
    generation time, and why does it matter for a production system?
4.  Why does response length affect latency more than "question
    difficulty"?

## Summary

An LLM call isn't one computation — it's a loop of forward passes, each
one predicting a single next token, streamed back until a stop
condition fires. Thinking of it as a streaming pipeline instead of a
request/response call is what made latency and cost behavior finally
make sense to me operationally.

## Next Chapter

➡️ `04-Tokens-and-Tokenization.md`
