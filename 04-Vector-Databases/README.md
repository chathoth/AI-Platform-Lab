# 04 - Vector Databases

> Where embeddings actually live once "a Python list" stops being
> enough.

## Overview

Module 03 chapter 10 built a working semantic search engine out of
nothing but a Python list and cosine similarity, and was explicit that
it's a **linear scan** — correct at any scale, fast only up to a few
thousand documents. This module picks up exactly where that left off:
what a real vector database adds (an indexed, approximate-nearest-
neighbor search instead of checking every vector), and the operational
concerns — metadata filtering, persistence, updates, multi-tenancy,
scaling — that come with running one for real.

Everything runs against **ChromaDB**, a real, persistent, fully local
vector database with no external service to sign up for, paired with
the same local `nomic-embed-text` embedding model used throughout
module 03. Module 05 (RAG) already uses this exact stack — this module
is where you build the deeper understanding of what's actually
happening underneath those `Chroma(...)` calls.

## Learning Objectives

After completing this module you will be able to:

-   Explain what an approximate-nearest-neighbor index does differently
    from a linear scan.
-   Compare the major vector database options and choose one
    deliberately.
-   Run ChromaDB locally: create collections, insert, query, filter,
    update, and delete.
-   Combine metadata filtering with similarity search in one query.
-   Design for stable IDs, persistence, and safe re-indexing.
-   Reason about scaling, multi-tenancy, and monitoring a vector
    database in production.

## Prerequisites

-   [03-Embeddings](../03-Embeddings/) — specifically chapters 09
    (Storing Embeddings) and 10 (Building Semantic Search From
    Scratch). This module assumes you understand *why* embeddings need
    an index at scale; here we build that index for real.

## Repository Structure

``` text
docs/
examples/
notebooks/
```

## Chapters

  Chapter   Topic
  --------- ---------------------------------------
  01        What Is a Vector Database
  02        Indexing Algorithms and ANN Search
  03        The Vector Database Landscape
  04        Collections and Namespaces
  05        Running ChromaDB Locally
  06        Inserting and Updating Vectors
  07        Querying and Similarity Search
  08        Metadata Filtering
  09        Stable IDs and Idempotent Upserts
  10        Persistence and Backup
  11        Document Lifecycle: Update and Delete
  12        Multi-Tenancy and Access Control
  13        Scaling Vector Search
  14        Hybrid Search in a Vector Database
  15        Reranking
  16        Vector Database vs. Traditional Database
  17        Monitoring and Observability
  18        Best Practices
  19        Interview Questions
  20        Glossary

## Learning Roadmap

``` text
Prompt Engineering
        ↓
Embeddings
        ↓
Vector Databases            ← you are here
        ↓
RAG
        ↓
AI Agents
```

## Hands-on Labs

-   Build a persistent Chroma collection from real text and query it.
-   Combine a metadata filter with a similarity search in one call.
-   Design and verify a stable ID scheme for idempotent re-indexing.
-   Update and delete individual records without rebuilding the whole
    collection.
-   Simulate multi-tenant isolation using metadata and separate
    collections.
-   Measure query latency as a collection grows.

## Technologies

-   Python
-   ChromaDB (persistent, fully local)
-   Ollama (`nomic-embed-text`)
-   Jupyter

## Expected Outcome

You will be able to run and operate a real local vector database with
the same confidence you'd bring to any other datastore — knowing what
its index is actually doing, how to query it correctly, and how to
keep it consistent over time — before moving on to RAG, where this
module's collection becomes the retrieval layer behind a full
question-answering pipeline.

## Next Module

➡️ `05-RAG`
