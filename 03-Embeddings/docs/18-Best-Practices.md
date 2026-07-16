# 18 - Best Practices

## Introduction

The consolidated checklist for this module, same spirit as module 01
chapter 18 and module 02 chapter 18 — everything here traces back to a
specific chapter, this is the "what do I actually do" version to walk
through before building anything embedding-backed for real.

## Learning Objectives

After this chapter I should be able to:

-   Apply a concrete checklist when building an embedding-based search
    or classification feature.
-   Explain the reasoning behind each item, tied to its source chapter.

------------------------------------------------------------------------

# The Checklist

## 1. Never Compare Vectors From Different Models

Chapter 01/11. Different embedding models produce incompatible
coordinate spaces — mixing them is a silent, hard-to-detect bug, not a
crash.

## 2. Default to a Local Model for Internal Content

Chapter 03. Embedding calls are, by nature, almost always your real
internal data sent in bulk — `nomic-embed-text` via Ollama keeps that
data on your own network, at no per-token cost.

## 3. Choose Cosine Similarity Unless the Model Says Otherwise

Chapter 05. It's the safe general default for text because it ignores
magnitude — check your specific model's documentation before deviating.

## 4. Chunk Before You Embed, With Boundaries That Respect Meaning

Chapter 07. Whole-document embeddings dilute signal; fixed-size cuts
break code and structured data. Use overlap to avoid splitting an idea
exactly at a boundary.

## 5. Clean Noise Out of Logs and Structured Data Before Embedding

Chapter 08. Timestamps, request IDs, and raw YAML punctuation dilute
semantic signal without adding meaning — strip what doesn't contribute
to your notion of "similar."

## 6. Store Metadata, Not Just the Vector

Chapter 09. A vector alone can't be turned into an actionable result —
always store source, section, and timestamp alongside it.

## 7. Persist and Cache — Don't Re-Embed Unchanged Content

Chapter 09/17. Hash content before re-embedding; treat the embedding
step like any other expensive, cacheable computation.

## 8. Know When a Linear Scan Is (and Isn't) Fast Enough

Chapter 10. Measure before assuming you need a vector database — a
Python list is genuinely fine for hundreds to low thousands of
documents.

## 9. Tag Every Vector With the Model That Produced It

Chapter 11. The cheapest insurance against silently mixing incompatible
vectors after a model upgrade — treat a model swap as a full migration,
never an incremental cutover.

## 10. Use Clustering to Discover Structure, Not Just Search to Confirm It

Chapter 12. When you don't already know the categories in your data,
clustering finds them — a genuinely different use case from search, on
the exact same vectors.

## 11. Flag Near-Duplicates for Review, Never Auto-Merge

Chapter 13. A similarity threshold is a tuned trade-off, not a
certainty — treat matches as candidates, the same caution module 01
chapter 18 applies to any LLM-adjacent output.

## 12. Reach for Embedding Classification When Volume Is High and
Categories Are Simple

Chapter 14. Cheaper and faster than an LLM prompt at scale — but weaker
at genuinely ambiguous cases, where a prompt or human judgment still
wins.

## 13. Combine Semantic and Keyword Search for Anything With Exact
Identifiers

Chapter 15. Pure semantic search structurally misses exact error codes,
hostnames, and version numbers — hybrid search covers both.

## 14. Evaluate With Recall@K, Not by Eyeballing Results

Chapter 16. Build an eval set with deliberately hard, differently-
worded queries, and use it to compare chunking and model choices
objectively.

## Anti-Patterns to Avoid

-   **Embedding raw logs/YAML without cleaning** — chapter 08.
-   **Upgrading an embedding model without a full re-embedding
    migration** — chapter 11.
-   **Auto-merging "duplicate" tickets based on similarity score alone**
    — chapter 13.
-   **Reaching for a vector database before measuring whether a linear
    scan is actually too slow** — chapter 10.
-   **Judging search quality by trying a few queries yourself instead
    of a real eval set** — chapter 16.

## Hands-on: Turn This Into a Repo Checklist

Same pattern as the previous two modules: create an
`embeddings-checklist.md` with these 14 items as literal checkboxes,
and walk through it before shipping any embedding-backed search,
classification, or clustering feature.

## Common Misconceptions

❌ Embeddings are simple enough not to need this level of process.
(The failure modes here — silent model-mismatch drift, noisy
unfiltered logs, unreviewed auto-merges — are exactly the kind that
don't crash anything, they just quietly degrade quality until someone
notices much later.)

❌ Following this checklist guarantees good search results.
(It avoids the common, well-understood failure modes from this module —
it doesn't replace testing against real content and real queries via
an eval set, chapter 16.)

✔ Every item here maps to a chapter that explains the underlying
failure mode — understanding *why* is what lets you judge the cases
this checklist doesn't explicitly cover.

## Interview Questions

1.  Why is comparing vectors from two different embedding models a
    silent failure rather than a crash?
2.  What's the risk of skipping content-cleaning before embedding logs
    or structured data?
3.  Why should near-duplicate matches be reviewed rather than
    auto-merged?
4.  When is embedding-based classification the better choice over an
    LLM prompt, and when is it not?

## Summary

Every practice in this module traces back to a specific, usually silent
failure mode: incompatible vector spaces, unfiltered noise, unreviewed
auto-merges, premature infrastructure, and untested search quality.
Together, they're what turns "embeddings that worked in a demo" into a
search or classification feature that's safe to depend on.

## Next Chapter

➡️ `19-Interview-Questions.md`
