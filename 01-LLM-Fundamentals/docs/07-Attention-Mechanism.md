# 07 - Attention Mechanism

## Introduction

Attention is the specific mechanism inside the Transformer block
(chapter 06) that made the whole architecture work. I think of it as a
**dynamic routing/dependency graph** computed fresh for every single
request — closer to a service mesh recomputing routes per-request based
on live signal than to any static config.

## Learning Objectives

After this chapter I should be able to:

-   Explain self-attention in plain terms (Query, Key, Value).
-   Explain why attention scores are a form of "relevance weighting."
-   Explain multi-head attention and why multiple heads help.
-   Explain why attention cost scales quadratically with sequence
    length, and why that matters operationally.

------------------------------------------------------------------------

# Self-Attention: Query, Key, Value

For every token, the model computes three vectors:

-   **Query (Q):** "what am I looking for?"
-   **Key (K):** "what do I represent?" (one per token)
-   **Value (V):** "what information do I actually carry?" (one per
    token)

The attention score between two tokens is the similarity between one
token's Query and another token's Key (the same dot-product/cosine idea
from chapter 05). Those scores are normalized (softmax) into weights
that sum to 1, and the token's new representation becomes a weighted sum
of every token's Value, using those weights.

``` text
"The server crashed because the disk was full"
                             ↑
When processing "disk", attention gives high weight to
"crashed" and "full" - and low weight to "The", "was"
```

**Platform analogy:** this is a dependency resolution step computed
fresh, per request. Think of it like a service mesh doing weighted
routing based on real-time signals instead of a static routing table —
every token dynamically decides which other tokens matter to it *for
this specific input*, rather than following a fixed rule.

## Multi-Head Attention: Running It in Parallel, Multiple Ways

A single attention computation only captures one "kind" of relationship.
Multi-head attention runs several attention computations **in
parallel**, each with its own learned Q/K/V projections, so different
heads can specialize — one head might track grammatical subject/verb
relationships, another might track long-range topic continuity.

**Platform analogy:** this is exactly like running several independent
readiness/liveness probes in parallel instead of one monolithic health
check — each probe looks at the same request from a different angle,
and you combine the signals for a fuller picture.

## Why Attention Is Expensive: O(n²)

Every token attends to every other token, so cost grows **quadratically**
with sequence length: double the input length, and attention compute
roughly quadruples.

  Sequence length   Relative attention cost
  ----------------- --------------------------
  1,000 tokens       1x
  2,000 tokens        ~4x
  4,000 tokens        ~16x
  32,000 tokens       ~1024x

**Why this is on my radar operationally:** this is *the* reason long
context windows are expensive and slow, why providers rate-limit tokens
per minute so aggressively, and why techniques like KV-caching (reusing
previously computed Key/Value vectors instead of recomputing them every
token) are essential for making chat-style, multi-turn conversations
serve at reasonable latency. It's the same category of problem as an
unindexed `O(n²)` join blowing up as a table grows — except here "the
table" is your prompt.

## Hands-on: Feel the Cost Curve

``` bash
# time a short prompt vs a long prompt against the same model
time ollama run llama3.1:8b "Summarize: $(head -c 500 /var/log/system.log)"
time ollama run llama3.1:8b "Summarize: $(head -c 8000 /var/log/system.log)"
```

Compare wall-clock time. The second call isn't just doing "more work
linearly" — the growth is closer to quadratic in the attention step,
even though total end-to-end latency is dominated by other linear
factors too at these sizes. On genuinely long contexts (50K+ tokens)
this curve is very visible in both latency and cost.

## Common Misconceptions

❌ Attention means the model "pays attention" the way a human does.
(It's a learned weighting function over token representations — a math
operation, not cognition.)

❌ More attention heads always means a smarter model.
(Head count is a capacity/architecture choice tuned during design, not
a dial you can freely turn up on a deployed model.)

✔ Attention cost scaling with sequence length (roughly quadratic) is
the direct cause of why long-context requests cost more and run slower
— not "the model thinking longer."

## Interview Questions

1.  What do Query, Key, and Value represent in self-attention?
2.  Why does multi-head attention exist instead of a single attention
    computation?
3.  Why does attention cost scale roughly quadratically with sequence
    length, and what operational problems does that cause?
4.  What is KV-caching, and why does it matter for multi-turn chat
    latency?

## Summary

Self-attention computes, per request, a relevance-weighted view of every
token against every other token — the mechanism that let Transformers
replace RNNs' sequential bottleneck. That same power is what makes long
context expensive: attention cost grows roughly quadratically with
sequence length, which is the root cause behind context-window pricing,
token-per-minute limits, and why KV-caching exists at all.

## Next Chapter

➡️ `08-Training-vs-Inference.md`
