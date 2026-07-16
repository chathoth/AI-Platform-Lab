# 03 - The Embedding Model Landscape

## Introduction

Module 01 chapter 15 walked through open vs. closed *chat* models. This
chapter is the same decision, applied to embedding models specifically
— and the calculus tilts differently here, because embeddings are
almost always generated from *your own* data, which makes the "does it
need to leave my network" question a lot more concrete than it is for a
general chat assistant.

## Learning Objectives

After this chapter I should be able to:

-   Compare local/open embedding models to hosted/closed ones.
-   Explain why data residency matters more for embeddings than for
    most chat use cases.
-   Choose a reasonable default model for a given constraint.

------------------------------------------------------------------------

# The Two Categories

  Local (open-weight)                       Hosted (closed API)
  ------------------------------------------- ----------------------------------------
  `nomic-embed-text`, `mxbai-embed-large` (via Ollama) | OpenAI `text-embedding-3-small/large`, Cohere, Voyage AI
  Runs entirely on your machine/network          Your text is sent to a third party
  Free after download, uses your own compute      Pay per token, no infra to manage
  Full control over version/updates                Provider controls model updates

This maps directly onto module 01 chapter 15's managed-vs-self-hosted
framing — but weighted differently, because of what's actually being
sent over the wire.

## Why Data Residency Bites Harder Here

A chat prompt is usually a *question* — often generic, sometimes with
some context attached. An embedding call is, by design, almost always
your **actual internal content**: a real incident postmortem, a real
runbook, a real ticket description, run through the model in bulk to
build a search index. If that content includes hostnames, customer
data, or anything sensitive, a hosted embedding API means all of it
leaves your network, at volume, as a matter of routine — not as an
occasional edge case.

**Platform analogy:** this is the same distinction as choosing where to
run a log-aggregation pipeline. Sending ad hoc queries to a SaaS tool
occasionally is a much smaller exposure than piping your entire raw log
stream through a third party continuously. Embedding a whole
documentation set is closer to the second case.

## Practical Comparison

  Factor                Local (Ollama)                    Hosted API
  ----------------------- ---------------------------------- --------------------------------
  Setup effort              `ollama pull`, done                API key, SDK, done
  Cost at scale               Fixed (your hardware)              Scales with token volume
  Data leaves your network    No                                  Yes
  Quality (general text)       Good, competitive                    Often slightly ahead at the top end
  Batch throughput             Limited by your hardware              Limited by rate limits

For this module, and for most internal-document use cases I'd actually
build, local wins by default — not because hosted models are worse, but
because the content being embedded is exactly the kind of internal data
that shouldn't need to leave the network just to become searchable.

## A Reasonable Default

``` bash
ollama pull nomic-embed-text
```

`nomic-embed-text` is a solid, fast, general-purpose default for
English technical text — the model used throughout this module's
examples. For non-English content or highly specialized domains
(legal, medical), check whether a more specialized model exists before
assuming the general default is good enough; the domain-gap problem
from chapter 02 applies here directly.

## Hands-on: Compare Local vs. a Hosted Model's Behavior

If you have access to a hosted embedding API, embed the same 3-4
sentences with both `nomic-embed-text` (local) and a hosted model, and
compare relative similarity rankings (not raw vector values — those
aren't comparable across models per chapter 01) between related and
unrelated pairs. If you don't have hosted API access, that's fine —
every example in this module runs entirely on the local model, which is
the point.

## Common Misconceptions

❌ Hosted embedding APIs are always meaningfully better quality.
(For general technical text, local open models are competitive — the
bigger differentiator is usually data residency and cost, not raw
quality.)

❌ Embedding your own documents locally has no trade-offs.
(You're responsible for your own hardware, batch throughput, and model
updates — a real trade-off against the convenience of a managed API,
just usually the right one for internal document search.)

✔ The residency question is sharper for embeddings than for chat,
because embedding calls are, by their nature, almost always your real
internal content, sent in bulk.

## Interview Questions

1.  Why does data residency matter more for embedding calls than for
    typical chat completions?
2.  Name two trade-offs of running a local embedding model versus a
    hosted API.
3.  What's a reasonable default local embedding model for general
    English technical text?
4.  When might a domain-specific or non-English embedding model be
    worth seeking out over the general default?

## Summary

Choosing between a local and hosted embedding model is the same
managed-vs-self-hosted decision from module 01, but weighted more
heavily toward local — because embedding calls are, by design, almost
always your real internal content sent in bulk. `nomic-embed-text` via
Ollama is a solid, free, private default for the examples in this
module and for most real internal-document search use cases.

## Next Chapter

➡️ `04-Vector-Space-and-Dimensionality.md`
