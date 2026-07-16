# 10 - Building Semantic Search From Scratch

## Introduction

This is the payoff chapter for everything so far — embedding (chapters
01-06), chunking (07), content prep (08), and storage (09) all come
together into one working search engine, built with nothing but Python,
a list, and cosine similarity. No vector database, no framework — I
want the mechanics fully visible before module 04 wraps them in
something more scalable.

## Learning Objectives

After this chapter I should be able to:

-   Build a complete semantic search function end to end.
-   Rank and return the top-k most relevant results for a query.
-   Recognize exactly which part of this hand-rolled version a real
    vector database would optimize.

------------------------------------------------------------------------

# The Whole Pipeline, in One Place

``` mermaid
flowchart LR
A[Documents] --> B[Chunk]
B --> C[Embed each chunk]
C --> D[Store: text + vector + metadata]
E[User query] --> F[Embed the query]
F --> G[Compare query vector to every stored vector]
G --> H[Sort by similarity, return top-k]
```

``` python
import requests
import numpy as np

def embed(text: str) -> np.ndarray:
    r = requests.post("http://localhost:11434/api/embeddings", json={"model": "nomic-embed-text", "prompt": text})
    return np.array(r.json()["embedding"])

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

class SimpleSearchIndex:
    def __init__(self):
        self.entries = []  # each: {"text": ..., "vector": ..., "metadata": {...}}

    def add(self, text: str, metadata: dict = None):
        self.entries.append({"text": text, "vector": embed(text), "metadata": metadata or {}})

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        query_vector = embed(query)
        scored = [
            {**entry, "score": cosine_similarity(query_vector, entry["vector"])}
            for entry in self.entries
        ]
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]
```

## Using It

``` python
index = SimpleSearchIndex()
index.add("To debug CrashLoopBackOff, check kubectl describe pod and logs --previous.", {"source": "runbook-01.md"})
index.add("When disk usage hits 90% on a primary DB, it's HIGH severity per SRE-042.", {"source": "runbook-02.md"})
index.add("To roll back a failed deployment, run kubectl rollout undo deployment/<name>.", {"source": "runbook-03.md"})
index.add("Best pizza toppings for a team lunch order.", {"source": "random-doc.md"})

results = index.search("one of our pods keeps restarting, what do I check?", top_k=2)
for r in results:
    print(f"[{r['score']:.3f}] {r['metadata']['source']}: {r['text']}")
```

Notice the query shares almost no exact words with the winning
runbook — no `"restart"` in the source text, no `"CrashLoopBackOff"` in
the query — and the pizza document should score visibly lowest. That's
the entire value proposition of embeddings from module 01 chapter 05,
now fully working end to end in code you wrote yourself.

## What This Is — and What It Isn't

This *is* a real, correct implementation of semantic search. What it
is **not** is fast at scale: `search()` computes a similarity score
against every single stored vector, every single query — a **linear
scan**. For a few hundred to a few thousand documents this is
genuinely fast enough (embedding the query itself is usually the
slower part). Past that, the linear scan becomes the bottleneck.

**Platform analogy:** this is a full table scan versus an indexed
lookup. Correct at any size, fast only at small size. A vector database
(module 04) is the equivalent of adding an index — specifically an
approximate nearest-neighbor index (like HNSW) that finds very-likely-
best matches without checking every single row, the same trade-off a
database index makes: a little accuracy risk in edge cases, in exchange
for massive speed at scale.

## Hands-on: Find the Break-Even Point Yourself

``` python
import time

# generate a larger synthetic set to feel the linear-scan cost grow
docs = [f"Incident report {i}: service degraded due to high memory usage" for i in range(200)]
big_index = SimpleSearchIndex()
for d in docs:
    big_index.add(d)

start = time.time()
big_index.search("why is memory usage high", top_k=5)
print(f"Search over {len(docs)} docs took {time.time() - start:.3f}s")
```

Most of that time is almost certainly the query embedding call itself,
not the comparison loop — at this scale, a linear scan genuinely isn't
the bottleneck yet. That's worth confirming directly rather than
assuming, before "I need a vector database" becomes the reflexive
answer to every search problem.

## Common Misconceptions

❌ Hand-rolled semantic search isn't "real" search.
(It's exactly the same math a vector database runs — the difference is
purely about indexing strategy for speed at scale, not correctness.)

❌ You need a vector database the moment you're doing semantic search
at all.
(A linear scan over a few hundred to low thousands of documents is
often still fast enough — measure before reaching for more
infrastructure.)

✔ Every vector database in module 04 is solving exactly the problem
this chapter's `SimpleSearchIndex` has: making similarity search fast
at scale, without changing what similarity search fundamentally *is*.

## Interview Questions

1.  Walk through the full pipeline from adding a document to returning
    a search result.
2.  Why is this implementation called a "linear scan," and why does
    that matter at scale?
3.  What does a vector database's approximate nearest-neighbor index
    actually optimize, compared to this implementation?
4.  Why might a query and its best-matching document share zero exact
    words?

## Summary

A working semantic search engine is genuinely just: embed documents,
embed the query, compute similarity against every stored vector, sort,
return the top matches. This chapter's from-scratch version is
correct at any scale and fast enough at small-to-medium scale — a
vector database (module 04) adds an approximate-nearest-neighbor index
to make the same fundamental operation fast at large scale, not a
different kind of search.

## Next Chapter

➡️ `11-Embedding-Drift-and-Model-Versioning.md`
