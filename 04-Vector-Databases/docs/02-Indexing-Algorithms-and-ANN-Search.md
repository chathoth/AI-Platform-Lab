# 02 - Indexing Algorithms and ANN Search

## Introduction

Chapter 01 said a vector database's index avoids comparing a query
against every stored vector. This chapter opens that up: what
"approximate" actually means, why it's a deliberate trade-off and not
a limitation to work around, and the specific algorithm (HNSW) most
local and open-source vector databases, including Chroma, use under
the hood.

## Learning Objectives

After this chapter I should be able to:

-   Explain what "approximate nearest neighbor" (ANN) means and why
    it's an acceptable trade-off.
-   Describe HNSW at a conceptual level.
-   Explain the accuracy/speed trade-off exposed by index tuning
    parameters.

------------------------------------------------------------------------

# Exact vs. Approximate Nearest Neighbor

**Exact** nearest neighbor (what module 03 chapter 10's linear scan
does) guarantees the true closest matches, at the cost of checking
every vector. **Approximate** nearest neighbor (ANN) trades a small,
usually negligible chance of missing the single best match for a
massive speedup — typically returning results that are extremely close
to, but not mathematically guaranteed to be, the exact top-k.

``` text
Exact search over 10M vectors:  compare against all 10M -> slow
ANN search over 10M vectors:    navigate a pre-built index structure,
                                  checking a tiny fraction of vectors -> fast
                                  (with a small chance of missing the
                                   single best match, if it happens to
                                   sit awkwardly in the index)
```

**Platform analogy:** this is caching with a small, controlled chance
of a stale read — not "wrong," but not perfectly authoritative either.
For search ranking, where result #1 and result #2 are both usually
"good enough," that trade-off is almost always worth taking. It would
not be an acceptable trade-off for, say, a financial balance lookup —
which is exactly why vector databases aren't used for those.

## HNSW, Conceptually

**Hierarchical Navigable Small World** (HNSW) is the algorithm behind
most local/open-source vector indexes, including Chroma's default.
Picture it as a multi-layer graph:

``` text
Layer 2 (sparse):    A -------- E
                      |           \
Layer 1 (medium):    A -- C ---- E -- G
                      |    |      |    |
Layer 0 (dense, all): A-B-C-D-E-F-G-H-I-J
```

A search starts at the sparse top layer, quickly narrows to the right
neighborhood, then descends into denser layers for precision — similar
to how a skip list or a multi-level cache narrows a search space
quickly before doing fine-grained work. This is *why* ANN search stays
fast even as a collection grows into the millions: it's not brute-force
distance computation, it's graph navigation.

## The Trade-off You Can Tune

Most ANN indexes (HNSW included) expose parameters trading index build
time and memory for search accuracy and speed:

  Parameter (HNSW)   Higher value means
  ------------------- ---------------------------------------------
  `ef_construction`     Slower index build, higher quality graph
  `M` (connections)      More memory per node, better recall
  `ef_search`             Slower queries, closer to exact results

The right values depend on your accuracy requirements and collection
size — the same "tune it, don't guess it" discipline as tuning cache
size or connection pool limits, and something to measure (chapter 17)
rather than set once and forget.

## Hands-on: See the Trade-off, Not Just Read About It

``` python
import chromadb
import time

client = chromadb.PersistentClient(path="./chroma_ann_demo")
collection = client.get_or_create_collection(
    name="ann_demo",
    metadata={"hnsw:space": "cosine"},  # explicit distance metric (chapter 07)
)

# add a modest batch of documents to make timing observable
docs = [f"Incident report number {i}: service degraded due to high memory usage" for i in range(500)]
collection.add(ids=[str(i) for i in range(500)], documents=docs)

start = time.time()
results = collection.query(query_texts=["why is memory usage high"], n_results=5)
print(f"Query took {time.time() - start:.4f}s over {collection.count()} documents")
```

At this scale you likely won't feel the difference between exact and
approximate search — that's the point module 03 chapter 10 already
made: the real payoff of an ANN index shows up at much larger scale
than a laptop demo can easily simulate.

## Common Misconceptions

❌ "Approximate" means the results are often wrong.
(In practice, ANN recall is typically 95-99%+ against true nearest
neighbors for reasonable settings — "approximate" describes a small,
tunable, usually negligible gap, not an unreliable result.)

❌ A vector database always uses HNSW.
(HNSW is the most common choice for local/open-source options, but
other algorithms exist — IVF, product quantization, and others — each
with different trade-offs, particularly around memory usage at very
large scale.)

✔ ANN parameters are a real, tunable trade-off between speed, memory,
and accuracy — worth measuring against your own data and query
patterns rather than trusting default values blindly at scale.

## Interview Questions

1.  What does "approximate" mean in approximate nearest neighbor
    search, and why is that trade-off usually acceptable for search
    ranking?
2.  Describe HNSW's layered graph structure at a conceptual level.
3.  Name two HNSW parameters and what increasing each one trades off.
4.  Why wouldn't ANN search be appropriate for something like an exact
    financial balance lookup?

## Summary

Vector databases use approximate nearest neighbor search — most
commonly via HNSW's layered graph structure — trading a small, tunable
chance of missing the exact best match for search that stays fast even
as a collection grows into the millions. This is a deliberate, sensible
trade-off for ranking search results, not a limitation to work around.

## Next Chapter

➡️ `03-The-Vector-Database-Landscape.md`
