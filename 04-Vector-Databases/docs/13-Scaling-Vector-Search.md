# 13 - Scaling Vector Search

## Introduction

Every example so far ran comfortably on a laptop. This chapter is
about what actually changes as a collection grows from thousands to
millions of vectors — where the real bottlenecks show up, and which
levers actually move the needle versus which ones are premature
optimization.

## Learning Objectives

After this chapter I should be able to:

-   Identify the three resources that scale with collection size:
    memory, index build time, and query latency.
-   Explain sharding and replication at a conceptual level.
-   Reason about when embedded/local stops being the right choice
    (tying back to chapter 03).

------------------------------------------------------------------------

# What Actually Grows

``` text
Memory       - the HNSW graph (chapter 02) typically needs to fit in
               RAM for good performance; more vectors = more memory
Index build   - inserting into an HNSW graph gets somewhat slower as
                the graph grows, though it stays sub-linear
Query latency  - grows very slowly with collection size, thanks to the
                ANN index (chapter 02) - this is the whole point of
                having one
```

The reassuring news: query latency is specifically what an ANN index
is designed to keep flat-ish as data grows. **Memory** is usually the
first real wall a local, embedded database like Chroma hits — the
index needs to live in RAM for good performance, and a laptop or a
single server only has so much of it.

## Rough Memory Math

Same instinct as module 03 chapter 04's storage estimate, extended to
include index overhead:

``` text
raw vector storage  ≈ count × dimensions × 4 bytes  (module 03 ch. 04)
HNSW index overhead  ≈ roughly 1.5-2x the raw vector storage,
                        depending on the M parameter (chapter 02)

Rough total for 1M documents, 768-dim embeddings:
  raw:   1,000,000 × 768 × 4 bytes ≈ 3.1 GB
  index: ≈ 4.5-6 GB total, including HNSW overhead
```

This is the point where "run it on a laptop" (this module's whole
premise) starts genuinely straining, and where chapter 03's landscape
comparison becomes a live decision instead of an abstract one.

## Sharding and Replication, Conceptually

**Sharding** splits one large collection across multiple machines, each
holding a subset of the vectors — a query fans out to all shards and
merges results. **Replication** copies the same data across multiple
machines for read throughput and fault tolerance.

**Platform analogy:** this is horizontal database scaling, full stop —
the same sharding-for-write-capacity, replication-for-read-throughput
pattern used for any large datastore. Self-hosted vector databases like
Milvus and Qdrant (chapter 03) build this in; an embedded local
database like Chroma fundamentally doesn't, because it's designed to
run in a single process.

## When to Actually Move Off Embedded/Local

  Symptom                                       Likely next step
  ------------------------------------------------ ------------------------------------
  Index no longer fits comfortably in available RAM  Self-hosted server or managed option (chapter 03)
  Need to scale reads across multiple app instances    Client-server database instead of embedded
  Need write throughput beyond one machine               Sharded self-hosted or managed option
  Uptime/failover requirements beyond "restart the process" | Managed option, likely

This is the same "measure, don't assume" discipline as module 03
chapter 10's linear-scan-to-vector-database transition — don't
pre-optimize for a scale you're not at, but recognize the concrete
symptoms when you get there.

## Hands-on: Watch Memory Grow, Roughly

``` python
import chromadb
import os

client = chromadb.PersistentClient(path="./chroma_scale_demo")
collection = client.get_or_create_collection("scale_test", embedding_function=OllamaEmbeddingFunction())

for batch in range(3):
    docs = [f"Sample document number {batch * 100 + i} about infrastructure topics" for i in range(100)]
    collection.add(ids=[f"doc-{batch}-{i}" for i in range(100)], documents=docs)
    dir_size = sum(f.stat().st_size for f in __import__("pathlib").Path("./chroma_scale_demo").rglob("*") if f.is_file())
    print(f"After {collection.count()} documents: {dir_size / 1_000_000:.2f} MB on disk")
```

Watch on-disk size grow roughly linearly with document count — this is
the same relationship the memory math above describes, made directly
observable.

## Common Misconceptions

❌ Query latency is the main thing that suffers as a vector database
grows.
(The ANN index is specifically designed to keep query latency close to
flat — memory footprint and index build time are the more common early
bottlenecks.)

❌ You should design for sharding and replication from day one.
(This module's whole premise — a local, embedded database — is the
right starting point for learning and small-to-medium scale. Design
for the scale you're actually at, per module 01 chapter 18's general
best-practices advice about right-sizing infrastructure.)

✔ Memory is usually the first real constraint an embedded local vector
database hits, not query speed — plan capacity around that, not around
a latency worry the ANN index already handles.

## Interview Questions

1.  Which resource typically becomes a bottleneck first as an embedded
    vector database's collection grows — memory or query latency?
2.  Roughly how does HNSW's memory overhead compare to raw vector
    storage?
3.  What's the conceptual difference between sharding and replication?
4.  Name two concrete symptoms that indicate it's time to move off an
    embedded local vector database.

## Summary

As a vector database's collection grows, query latency stays
relatively flat thanks to its ANN index (chapter 02) — memory and index
build time are the more likely early bottlenecks. Sharding and
replication are the standard horizontal-scaling answers once a single
machine's capacity is genuinely exceeded, which is also the point where
chapter 03's landscape comparison (self-hosted or managed) becomes a
live decision rather than a hypothetical one.

## Next Chapter

➡️ `14-Hybrid-Search-in-a-Vector-Database.md`
