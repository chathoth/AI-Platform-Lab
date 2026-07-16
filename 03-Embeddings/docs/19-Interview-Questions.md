# 19 - Interview Questions

## Introduction

Every interview question from this module, grouped by chapter, with the
answer framed the way I'd actually say it. Review material — read the
chapters first.

------------------------------------------------------------------------

## Chapter 01 - What Are Embeddings

**Q: What does a single number inside an embedding vector represent?**
Nothing on its own — only the vector's position *relative to other
vectors from the same model* carries meaning. It's a coordinate, not a
labeled feature.

## Chapter 02 - How Embedding Models Are Trained

**Q: Why can an embedding model struggle with internal company jargon?**
Contrastive training learns patterns from the corpus it was trained
on — general web text mostly. Internal shorthand it never saw enough
times produces a less meaningful vector; expanding jargon to plain
language before embedding is a cheap mitigation.

## Chapter 03 - The Embedding Model Landscape

**Q: Why does data residency matter more for embeddings than for
typical chat completions?**
Embedding calls are, by design, almost always your actual internal
content sent in bulk to build a search index — not an occasional
question. A local model keeps that content on your own network.

## Chapter 04 - Vector Space and Dimensionality

**Q: How do you estimate storage cost for a set of embeddings?**
`document count × dimensions × 4 bytes` — the same simple math as
estimating a database table's disk footprint from row count and row
size.

## Chapter 05 - Similarity Metrics

**Q: Why is cosine similarity the standard default for text search?**
It ignores vector magnitude and measures direction only — magnitude
often correlates with things like text length that you don't actually
want to measure, while direction is where meaning lives.

## Chapter 06 - Generating Embeddings Locally with Ollama

**Q: Why does batching embedding calls matter?**
Each call has fixed per-request overhead; batching amortizes that cost
across many documents, the same reason bulk database writes beat
one-row-at-a-time inserts.

## Chapter 07 - Chunking Before Embedding

**Q: Why not just embed a whole document?**
A single embedding is a blurry average of everything in the input —
chunking preserves granularity so a search for one specific fact isn't
diluted by everything else in a long document.

## Chapter 08 - Embedding Different Content Types

**Q: Why does embedding a raw log line with its timestamp hurt search
quality?**
High-cardinality, unique-per-event fields like timestamps add noise
without contributing meaning, dragging down similarity between
otherwise-identical events.

## Chapter 09 - Storing Embeddings

**Q: When should you move from a Python list to a real vector
database?**
When you hit a concrete scaling symptom — slow linear search, memory
pressure, need for metadata filtering, or concurrent access — not
preemptively.

## Chapter 10 - Building Semantic Search From Scratch

**Q: What does a vector database's index actually optimize, compared
to a hand-rolled linear scan?**
Speed at scale via approximate nearest-neighbor search — the underlying
similarity math is identical; only the strategy for finding the best
matches without checking every vector changes.

## Chapter 11 - Embedding Drift and Model Versioning

**Q: Why is swapping an embedding model dangerous without a full
migration?**
Old and new vectors live in incompatible coordinate spaces — mixing
them degrades search quality silently, with no error to signal it.

## Chapter 12 - Clustering With Embeddings

**Q: How does clustering differ from search, given they use the same
vectors?**
Search compares one query vector against many; clustering compares
every vector against every other vector to find natural groupings, with
no query and no labels required.

## Chapter 13 - Deduplication With Embeddings

**Q: Why shouldn't near-duplicate matches be auto-merged?**
The similarity threshold is a tuned trade-off, not a certainty — the
cost of an incorrect merge is usually higher than a few seconds of
human review.

## Chapter 14 - Classification With Embeddings

**Q: When does embedding-based classification beat an LLM prompt?**
High-volume, simple categorization — it's cheaper and faster per
classification, at the cost of not being able to reason through
genuinely ambiguous cases.

## Chapter 15 - Hybrid Search

**Q: Why does semantic search need to be paired with keyword search?**
Embeddings encode general meaning, not exact identifiers — an error
code or hostname can be conceptually unremarkable but critically
specific, which is exactly what keyword matching catches reliably.

## Chapter 16 - Evaluating Embedding Quality

**Q: What does recall@k measure?**
Whether the correct document appeared in the top k search results,
averaged across a labeled eval set — a measurable way to compare
chunking or model changes instead of eyeballing results.

## Chapter 17 - Cost and Performance at Scale

**Q: Why should re-embedding be based on content hashing?**
Re-embedding an entire document set on every small change wastes real
compute — hashing lets you skip anything that hasn't actually changed,
the same idea as incremental builds.

## Chapter 18 - Best Practices

**Q: Why does this checklist matter more for embeddings than it might
seem?**
Nearly every failure mode here is silent — mismatched models, unfiltered
noise, bad auto-merges — none of them crash, they just quietly degrade
quality until someone notices much later.

------------------------------------------------------------------------

## Rapid-Fire Round

1.  Embedding — a position in a learned coordinate space, not a label.
2.  Contrastive training — pulls related pairs together, pushes
    unrelated pairs apart.
3.  Cosine similarity — measures direction, ignores magnitude.
4.  Chunking — required, respects meaning boundaries, uses overlap.
5.  Storage cost — count × dimensions × 4 bytes.
6.  Model versioning — tag every vector, migrate fully, never mix.
7.  Clustering — finds groups with no query and no labels.
8.  Deduplication — flag for review, never auto-merge.
9.  Classification — cheap nearest-neighbor alternative to an LLM
    prompt, weaker on ambiguity.
10. Hybrid search — semantic + keyword, complementary not competing.
11. Recall@k — did the right answer show up in the top results.
12. Re-embedding — hash-based, incremental, not wholesale.

## Next Chapter

➡️ `20-Glossary.md`
