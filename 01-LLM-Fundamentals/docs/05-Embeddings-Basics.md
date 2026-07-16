# 05 - Embeddings Basics

## Introduction

The infra pattern I already know for "find things that are similar" is
an index — a B-tree, a hash index, an inverted index for full-text
search. Embeddings are the LLM-world answer to the same problem, except
the thing being indexed is **meaning**, not exact strings. Once that
clicked, RAG (chapter 14) and vector databases stopped feeling like
magic and started feeling like "a search index, just with a different
kind of key."

## Learning Objectives

After this chapter I should be able to:

-   Explain what an embedding is and what it represents.
-   Explain why embeddings enable semantic (meaning-based) search
    instead of exact-match/keyword search.
-   Generate an embedding via API and compute similarity between two
    pieces of text.
-   Relate embeddings to how I'd design an indexing/search system.

------------------------------------------------------------------------

# What Is an Embedding?

An embedding is a **fixed-length vector of numbers** that represents the
meaning of a piece of text.

``` text
"Kubernetes"     → [0.12, -0.45, 0.88, ..., 0.03]   (1536 numbers)
"container orchestration" → [0.14, -0.42, 0.85, ..., 0.05]  (very close!)
"banana"         → [0.91, 0.02, -0.77, ..., 0.66]   (far away)
```

Texts with similar *meaning* end up as vectors that are close together
in this high-dimensional space, regardless of whether they share any
literal words. `"Kubernetes"` and `"container orchestration"` share zero
words but land close together, because the model learned they're used
in similar contexts.

## Platform Analogy: This Is a Different Kind of Index

  Traditional search index          Embedding-based search
  ---------------------------------- -------------------------------------
  Exact/keyword match (grep, LIKE)  Semantic/meaning match
  Inverted index on tokens          Vector index (e.g. HNSW) on floats
  Query: `"k8s deployment failed"`  Also matches `"pod rollout error"`
  Fast, cheap, no ML needed         Needs an embedding model + vector DB

I think of it like this: my log search stack (grep/Elasticsearch)
answers *"which documents contain these exact terms?"* An embedding
index answers *"which documents mean the same thing as this, even with
completely different wording?"* Both are legitimate indexes — you pick
based on the query pattern, same as choosing between a hash index and a
full-text index today.

## Similarity: Cosine Similarity

To compare two embeddings, you measure the angle between them — **cosine
similarity**, ranging from -1 (opposite) to 1 (identical meaning).

``` python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

A similarity above ~0.8 usually means "closely related" — this
threshold is exactly the kind of tunable knob I'd treat like an alert
threshold: too low and you get noisy/irrelevant matches, too high and
you get zero results.

## Hands-on: Embed and Compare Real Ops Text

``` python
from openai import OpenAI

client = OpenAI()

def embed(text):
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return resp.data[0].embedding

a = embed("The pod is stuck in CrashLoopBackOff")
b = embed("Container keeps restarting and failing health checks")
c = embed("Deploy the new frontend release to staging")

import numpy as np
print("a vs b:", cosine_similarity(np.array(a), np.array(b)))  # high
print("a vs c:", cosine_similarity(np.array(a), np.array(c)))  # low
```

Or fully local with Ollama, no API cost:

``` bash
ollama pull nomic-embed-text

curl http://localhost:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "The pod is stuck in CrashLoopBackOff"
}'
```

**Practical use case that maps to real work:** feed a year of incident
postmortems through an embedding model, store the vectors, and now
`"database connection pool exhausted"` can retrieve a past incident
titled `"prod outage: pgbouncer ran out of connections"` even though no
words match. That's semantic search over your own runbooks/postmortems
— the actual RAG pattern from chapter 14, one step removed.

## Common Misconceptions

❌ Embeddings understand text the way a human does.
(They encode statistical patterns of co-occurrence from training data —
useful, but not comprehension.)

❌ You need a vector database to use embeddings.
(For a few thousand documents, a numpy array and a for-loop is a
perfectly fine "vector index" — the dedicated DB earns its keep at
scale, same as any other infra choice.)

✔ Embedding models are separate from chat/completion models — they're
smaller, cheaper, and their only job is producing vectors, not
generating text.

## Interview Questions

1.  What does an embedding vector represent?
2.  Why can two pieces of text be semantically similar despite sharing
    no words?
3.  How is cosine similarity computed, and what does a score near 1
    mean?
4.  When would you reach for a real vector database instead of an
    in-memory array?

## Summary

Embeddings turn text into vectors positioned by meaning, not spelling —
the same conceptual leap as moving from exact-match indexing to
semantic search. This is the foundation every RAG and semantic-search
system is built on, and it's the piece that makes chapter 14
(Fine-Tuning vs RAG) make sense operationally.

## Next Chapter

➡️ `06-Transformer-Architecture.md`
