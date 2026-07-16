# 17 - Cost and Performance at Scale

## Introduction

Everything in this module has run against a handful of documents on a
local machine. This chapter is the capacity-planning conversation for
when that handful becomes millions — the same exercise module 01
chapter 12 walked through for model parameters, applied to embedding
pipelines specifically: what actually costs time and money as volume
grows, and where the real bottlenecks show up.

## Learning Objectives

After this chapter I should be able to:

-   Identify the three cost centers in an embedding pipeline: initial
    embedding, storage, and query time.
-   Estimate re-embedding cost when content changes.
-   Apply caching to avoid redundant embedding calls.

------------------------------------------------------------------------

# Three Places Cost Shows Up

``` text
1. INITIAL EMBEDDING  - embedding your entire document set, once (or on updates)
2. STORAGE            - holding all those vectors (chapter 04's math)
3. QUERY TIME          - embedding each incoming query, then searching
```

Each has a different cost shape and a different lever to pull:

  Cost center        Local (Ollama)                       Hosted API
  -------------------- -------------------------------------- ------------------------------
  Initial embedding      Your hardware's throughput, no $ cost   Per-token cost, scales with document volume
  Storage                 Disk/RAM on your infra                  Vendor's storage pricing (if using their vector store too)
  Query time                Your hardware's latency                   Per-query cost + network latency to the provider

## Re-Embedding Cost Is the One People Forget

Documents change. Every time a runbook is edited, the old embedding is
stale (chapter 11) and needs to be regenerated — but re-embedding the
*entire* document set on every small change is wasteful. The fix is the
same instinct as an incremental build: only re-embed what actually
changed.

``` python
import hashlib

def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def needs_reembedding(entry: dict, current_text: str) -> bool:
    return entry.get("content_hash") != content_hash(current_text)

# only re-embed documents whose content actually changed
for doc in documents:
    existing = find_existing_entry(doc["source"])
    if existing is None or needs_reembedding(existing, doc["text"]):
        vector = embed(doc["text"])
        store(doc, vector, content_hash=content_hash(doc["text"]))
    # else: skip - nothing changed, no need to spend an embedding call
```

**Platform analogy:** this is exactly incremental compilation, or a
build tool that hashes source files to decide what needs rebuilding.
Re-embedding unchanged content wastes time and money for zero benefit
— hash-and-compare is a small amount of code that pays for itself
immediately at any real document volume.

## Query-Time Latency Has Two Parts

``` text
Total query latency = time to embed the query + time to search the index

Embedding the query: usually tens to low hundreds of milliseconds locally
Searching the index:  linear scan (chapter 10) or indexed lookup (module 04)
```

At small scale, embedding the query dominates total latency — the
search itself is nearly instant. At large scale (the symptoms from
chapter 09), the search step can become the bottleneck instead, which
is exactly the trigger for adopting a vector database's indexed search
in module 04.

## Batch Processing for Large Initial Loads

When embedding a large existing document set for the first time,
batching (chapter 06) and parallelizing across the available hardware
matters far more than at query time, since it's a one-time bulk job:

``` python
from concurrent.futures import ThreadPoolExecutor

def embed_all(texts: list[str], max_workers: int = 4) -> list[list[float]]:
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(embed, texts))
```

Tune `max_workers` against what your local Ollama instance can actually
handle concurrently — pushing too much parallel load at a local model
server can just queue requests rather than speed things up, the same
diminishing-returns curve as over-parallelizing any resource-bound job.

## Hands-on: Measure Your Own Bottleneck

``` python
import time

texts = [f"Sample runbook entry number {i} about deployment issues" for i in range(50)]

start = time.time()
vectors_sequential = [embed(t) for t in texts]
sequential_time = time.time() - start

start = time.time()
vectors_parallel = embed_all(texts, max_workers=4)
parallel_time = time.time() - start

print(f"Sequential: {sequential_time:.2f}s")
print(f"Parallel (4 workers): {parallel_time:.2f}s")
```

Compare the two on your own hardware — the speedup (or lack of one) is
specific to what your local Ollama instance can actually handle
concurrently, which is exactly why "measure on your own setup" beats
assuming a general rule of thumb here.

## Common Misconceptions

❌ Re-embedding the whole document set on every update is simplest and
safest.
(It's simplest, but wastes real time/compute at any meaningful scale —
hash-based change detection is a small amount of code for a large,
compounding savings.)

❌ Parallelizing embedding calls always speeds things up proportionally.
(Past your hardware's actual concurrency limit, more parallel requests
just queue rather than help — measure the real bottleneck instead of
assuming more workers is always better.)

✔ At small scale, query embedding time dominates total search latency;
at large scale, the search/index step becomes the bottleneck — know
which regime you're actually in before optimizing the wrong part.

## Interview Questions

1.  Name the three cost centers in an embedding pipeline.
2.  Why should re-embedding be based on content hashing rather than
    re-running on every document unconditionally?
3.  At small scale, which part of query latency typically dominates —
    embedding the query, or searching the index?
4.  What's the risk of over-parallelizing embedding calls against a
    local model server?

## Summary

Embedding pipelines have three cost centers — initial embedding,
storage, and query time — each with its own bottleneck and lever.
Hash-based change detection avoids wasteful re-embedding of unchanged
content, and knowing whether query latency is currently dominated by
embedding the query or searching the index tells you which part is
actually worth optimizing.

## Next Chapter

➡️ `18-Best-Practices.md`
