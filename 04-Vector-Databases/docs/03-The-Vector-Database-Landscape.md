# 03 - The Vector Database Landscape

## Introduction

Module 01 chapter 15 and module 03 chapter 03 both walked through
open-vs-closed, local-vs-hosted decisions for models. This chapter is
the same category of decision, now for where the vectors themselves
live — and just like those earlier chapters, the right answer depends
on scale, ops appetite, and how sensitive the underlying data is.

## Learning Objectives

After this chapter I should be able to:

-   Name the major categories of vector database and a representative
    option in each.
-   Compare embedded/local options against client-server and managed
    options.
-   Justify this module's choice of ChromaDB for learning and
    small-to-medium production use.

------------------------------------------------------------------------

# Three Categories

  Category                Examples                          Runs where
  ------------------------- ---------------------------------- ----------------------------------
  Embedded / local            ChromaDB, FAISS, sqlite-vec         In-process or a local file, no server to run
  Self-hosted client-server    Milvus, Weaviate, Qdrant             Your own server/cluster, you operate it
  Managed / hosted               Pinecone, Weaviate Cloud, Qdrant Cloud | Vendor's infrastructure, you call an API

There's a fourth option worth naming separately: **vector extensions on
databases you already run** — `pgvector` for Postgres, or Elasticsearch/
OpenSearch's vector fields. If your data already lives in one of these,
adding vector search there avoids standing up a whole new system.

## The Same Trade-offs, Familiar From Earlier Modules

**Platform analogy:** this maps directly onto module 01 chapter 15's
managed-vs-self-hosted framing, and module 03 chapter 03's residency
argument — the vectors here are frequently derived from your own
internal documents, so where they live matters for the same reasons.

  Factor                   Embedded/local          Self-hosted server      Managed/hosted
  -------------------------- ------------------------ ------------------------ --------------------------
  Setup effort                 `pip install`, done       Deploy and operate a service | Sign up, get an API key
  Ops burden                    None                        You own uptime/scaling      Vendor owns uptime/scaling
  Data residency                  Fully local                 Fully in your infra           Leaves your network
  Cost model                        Free (your disk/CPU)         Your infra cost                 Usage-based vendor pricing
  Ceiling                             Single-machine scale          Scales with your cluster       Scales to vendor's limits
  Best fit                             Learning, small-to-medium apps | Larger internal apps, full control | High scale, minimal ops appetite

## Why This Module Uses ChromaDB

Same reasoning module 03 chapter 03 applied to choosing a local
embedding model: an embedded, local, zero-signup database means
**anyone can run every example in this module exactly as written**, no
account, no cost, no data leaving the machine — and Chroma is already
the vector store module 05 (RAG) uses in its real, working pipeline, so
the skills transfer directly.

That doesn't make Chroma the universal right answer — it's a
deliberate choice for *this module's* constraints (learning, local-
first, small-to-medium document volume). A team running retrieval over
tens of millions of vectors with strict uptime SLAs would reasonably
land on Milvus, Qdrant, or a managed option instead.

## A Decision Sketch

``` text
Learning, prototyping, or a small-to-medium internal tool?
        → embedded/local (Chroma, FAISS)

Already running Postgres or Elasticsearch, moderate vector volume?
        → add a vector extension (pgvector, ES/OpenSearch vector fields)

Need full control, larger scale, in-house ops capacity?
        → self-hosted server (Milvus, Weaviate, Qdrant)

High scale, minimal ops appetite, budget for a vendor?
        → managed/hosted (Pinecone, Weaviate Cloud, Qdrant Cloud)
```

## Hands-on: Confirm the Local Option Actually Works Offline

``` bash
# turn off networking mentally for a second - this should still work
python -c "
import chromadb
client = chromadb.PersistentClient(path='./chroma_offline_test')
collection = client.get_or_create_collection('test')
collection.add(ids=['1'], documents=['fully local, no network call needed'])
print(collection.query(query_texts=['local test'], n_results=1))
"
```

No API key, no network call to a vector database vendor — the same
verification module 03's examples give for the embedding model itself.

## Common Misconceptions

❌ There's one "best" vector database and everyone should use it.
(Same lesson as every other build-vs-buy decision in this repo — the
right choice depends on scale, ops capacity, and data sensitivity, not
a universal ranking.)

❌ Embedded/local vector databases can't be used in production.
(Chroma, FAISS, and similar options are genuinely production-viable
for small-to-medium scale — module 05's RAG pipeline runs one for real,
not just as a toy.)

✔ This module's choice of Chroma is deliberate for its constraints
(learning, local-first, no signup) — treat it as a starting point to
reason from, not a universal recommendation.

## Interview Questions

1.  Name the three broad categories of vector database and a
    representative option in each.
2.  Why might a team choose `pgvector` over standing up a dedicated
    vector database?
3.  What specifically makes ChromaDB a good fit for this module's
    goals?
4.  Under what conditions would a self-hosted or managed option be the
    better choice over an embedded local database?

## Summary

Vector databases split into embedded/local, self-hosted client-server,
and managed/hosted categories — the same familiar trade-offs around ops
burden, cost, and data residency that govern every other build-vs-buy
infrastructure decision. This module uses ChromaDB deliberately for its
local-first, zero-signup properties, matching the "anyone can run this"
goal — not because it's universally the best option for every scale.

## Next Chapter

➡️ `04-Collections-and-Namespaces.md`
