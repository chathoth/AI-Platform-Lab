# 09 - Storing Embeddings

## Introduction

Every example so far generated embeddings and immediately used them in
the same script — nothing was actually saved. This chapter covers the
step in between: where embeddings actually live between the moment
they're generated and the moment they're searched, and why "just keep
them in memory" works for a surprisingly long time before it doesn't.
This is the direct on-ramp to module 04 (Vector Databases).

## Learning Objectives

After this chapter I should be able to:

-   Store embeddings alongside their source text and metadata.
-   Persist embeddings to disk so they survive a restart.
-   Know the point at which a simple file-based approach stops being
    enough.

------------------------------------------------------------------------

# The Simplest Possible Store: A List in Memory

``` python
index = []  # list of {"text": ..., "vector": ..., "metadata": {...}}

def add(text: str, metadata: dict = None):
    index.append({"text": text, "vector": embed(text), "metadata": metadata or {}})

add("To debug CrashLoopBackOff, check kubectl logs --previous.", {"source": "runbook-01.md"})
add("To roll back a deployment, use kubectl rollout undo.", {"source": "runbook-02.md"})
```

This is a completely legitimate approach for a few hundred documents —
don't reach for a database before you need one, the same instinct as
not reaching for Kubernetes to run one script.

## Persisting to Disk

In-memory data disappears on restart, and re-embedding everything every
time the script runs wastes time and compute. Save the vectors, not
just the raw text:

``` python
import json

def save_index(index: list, path: str):
    with open(path, "w") as f:
        json.dump(index, f)

def load_index(path: str) -> list:
    with open(path) as f:
        return json.load(f)

save_index(index, "runbook_index.json")
# next run, restore instead of re-embedding everything
index = load_index("runbook_index.json")
```

**Platform analogy:** this is exactly a build cache. Re-embedding
every document on every run is like rebuilding a Docker image from
scratch every time instead of caching layers — correct, but wasteful.
Persisting the index is the cache; you only re-embed documents that are
new or changed (see the versioning discussion in chapter 11).

## What Metadata to Store Alongside Each Vector

The vector alone isn't useful without knowing what it came from and
where to point a user or a downstream system:

``` python
{
    "text": "To debug CrashLoopBackOff, check kubectl logs --previous.",
    "vector": [0.12, -0.45, ...],
    "metadata": {
        "source": "runbook-01.md",
        "section": "Pod Troubleshooting",
        "last_updated": "2026-06-01",
    },
}
```

Metadata is what turns a search result into something actionable — "the
answer is in this vector" is useless without "...and here's the file
and section it came from."

## When a Python List Stops Being Enough

  Symptom                                     What it means
  --------------------------------------------- -------------------------------------
  Search takes noticeably long (seconds+)         Linear scan through every vector is now the bottleneck
  Index no longer fits comfortably in memory        Thousands to tens of thousands of documents, depending on dimension count (chapter 04's storage math)
  Need to filter by metadata AND search by similarity in one query | A plain list requires you to hand-roll that logic
  Multiple processes/services need to query the same index concurrently | A file-based JSON store has no safe concurrent access story

None of these are wrong to hit — they're just the signal that it's time
for module 04's vector databases, which solve exactly these problems
(indexed similarity search, metadata filtering, concurrent access)
instead of a hand-rolled list and a linear scan.

## Hands-on: Build and Persist a Tiny Index

``` python
import requests, json

def embed(text):
    r = requests.post("http://localhost:11434/api/embeddings", json={"model": "nomic-embed-text", "prompt": text})
    return r.json()["embedding"]

runbooks = {
    "runbook-01.md": "To debug CrashLoopBackOff, check kubectl logs --previous.",
    "runbook-02.md": "To roll back a deployment, use kubectl rollout undo.",
}

index = [{"text": text, "vector": embed(text), "metadata": {"source": source}}
          for source, text in runbooks.items()]

with open("runbook_index.json", "w") as f:
    json.dump(index, f)

print(f"Saved {len(index)} entries to runbook_index.json")

# simulate a restart - load without re-embedding
with open("runbook_index.json") as f:
    restored = json.load(f)
print(f"Restored {len(restored)} entries, no re-embedding needed")
```

## Common Misconceptions

❌ You need a vector database from day one for any embedding project.
(A list plus a JSON file is a perfectly good starting point for
hundreds of documents — reach for a database when you hit one of the
scaling symptoms above, not preemptively.)

❌ Storing just the vector is enough.
(Without the source text and metadata attached, a vector is a set of
numbers with no way to turn a search hit into something a user or
system can act on.)

✔ Persisting an embedding index is a caching decision — avoid
re-embedding unchanged content on every run, the same way you'd cache
any other expensive, repeatable computation.

## Interview Questions

1.  Why is a Python list a legitimate embedding store for a small
    document set?
2.  What should be stored alongside each vector, and why?
3.  Name two signals that indicate it's time to move from a
    file-based store to a real vector database.
4.  Why is persisting embeddings to disk conceptually similar to a
    build cache?

## Summary

A simple in-memory list, persisted to a JSON file, is a completely
legitimate way to store embeddings for small-to-medium document sets —
storing the source text and metadata alongside each vector, not just
the vector alone. The move to a real vector database (module 04) is
driven by concrete scaling symptoms — slow linear search, memory
pressure, need for metadata filtering, or concurrent access — not by
default.

## Next Chapter

➡️ `10-Building-Semantic-Search-From-Scratch.md`
