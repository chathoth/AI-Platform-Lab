# 01 - What Is a Vector Database

## Introduction

Module 03 chapter 10 was explicit that its from-scratch search engine
was a linear scan — correct at any scale, slow past a few thousand
documents. This chapter picks up exactly there: what a vector database
actually adds on top of "a list plus cosine similarity," and why that
addition matters the moment real document volume shows up.

## Learning Objectives

After this chapter I should be able to:

-   Define a vector database and what makes it different from a
    regular database.
-   Explain, at a high level, what problem it solves that a Python
    list doesn't.
-   Identify the four things a vector database stores per record.

------------------------------------------------------------------------

# What's Actually New Here

A vector database is a datastore purpose-built to do one thing fast:
given a query vector, find the stored vectors closest to it, without
comparing against every single one. Everything else — persistence,
metadata, collections, an insert/update/delete API — is table stakes
that any real database needs; the **index** is the part that's actually
new relative to what module 03 chapter 10 built by hand.

``` text
Module 03's SimpleSearchIndex:
  search(query) -> compare query vector against EVERY stored vector
                 -> sort -> return top-k
                 (correct, gets slower as the collection grows)

A real vector database:
  search(query) -> use a pre-built index to jump almost directly to
                    the likely nearest vectors
                 -> return top-k
                 (approximate, but stays fast as the collection grows)
```

**Platform analogy:** this is a full table scan versus a B-tree index
lookup — the exact same "correct but slow" vs. "fast but needs
maintenance" trade-off that governs database indexing decisions
everywhere else. A vector database is what happens when you take that
same indexing discipline and apply it to nearest-neighbor search
instead of exact-match lookup.

## What Gets Stored Per Record

Same four things module 03 chapter 09 said to store, now inside a real
database instead of a hand-rolled list:

``` text
ID          - a unique, stable identifier (chapter 09)
Vector      - the embedding itself
Document    - the original text (so a hit is actually readable)
Metadata    - source, page, timestamp, and anything you'll filter on (chapter 08)
```

## Why Not Just Use a Regular Database?

A regular relational or document database can technically store a
vector as a blob or array column — but it has no efficient way to
answer "find the 5 rows whose vector is closest to this one" without a
full scan, because its indexes (B-trees, hash indexes) are built for
exact-match and range queries, not for distance in high-dimensional
space. A vector database's index (chapter 02) is specifically built for
that different query shape.

## Hands-on: Install and Confirm It Works Locally

``` bash
pip install chromadb
```

``` python
import chromadb

client = chromadb.PersistentClient(path="./chroma_demo")
collection = client.get_or_create_collection(name="test")

collection.add(
    ids=["1", "2", "3"],
    documents=["The pod is stuck in CrashLoopBackOff", "Disk usage is critical", "Best pizza toppings"],
)

results = collection.query(query_texts=["container keeps restarting"], n_results=2)
print(results["documents"])
```

Notice you didn't have to generate embeddings yourself — Chroma has a
default embedding function built in for exactly this kind of quick
test. Later chapters swap that default for the local `nomic-embed-text`
model used throughout module 03, for consistency and quality.

## Common Misconceptions

❌ A vector database is a completely different category of technology
from a regular database.
(It's a database specialized for one query shape — nearest-neighbor
search — the same way a time-series database is a regular database
specialized for time-ordered data.)

❌ You need a vector database the moment you're doing any embedding-
based search.
(Module 03 chapter 10 already covered this — a linear scan over a
modest document set is often fast enough. This module is for when it
isn't.)

✔ The core addition a vector database makes over a hand-rolled list is
the **index** — everything else (storage, metadata, an API) is
necessary infrastructure around that one core capability.

## Interview Questions

1.  What does a vector database do differently from a linear scan over
    a list of vectors?
2.  Why can't a regular relational database efficiently answer a
    nearest-neighbor query using its normal indexes?
3.  What four things does a vector database typically store per
    record?
4.  What's the platform-engineering analogy for the linear-scan-vs-
    indexed trade-off?

## Summary

A vector database is a datastore specialized for fast nearest-neighbor
search over embeddings, built around an index that avoids comparing a
query against every stored vector — the same full-scan-vs-indexed-
lookup trade-off that governs indexing decisions in any other database.
Everything else it does (storage, metadata, CRUD) is necessary
scaffolding around that one specialized capability.

## Next Chapter

➡️ `02-Indexing-Algorithms-and-ANN-Search.md`
