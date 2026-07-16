# 20 - Glossary

## Introduction

Every term from this module, alphabetical, defined the way I actually
think about it, with the analogy that made it stick attached.

------------------------------------------------------------------------

**ANN (Approximate Nearest Neighbor)** — Search that trades a small,
tunable chance of missing the exact best match for search that stays
fast as a collection scales. See
[02-Indexing-Algorithms-and-ANN-Search.md](02-Indexing-Algorithms-and-ANN-Search.md).

**Collection** — A named, isolated set of vectors with its own index
and ID space — the vector-database equivalent of a namespace or
schema. See
[04-Collections-and-Namespaces.md](04-Collections-and-Namespaces.md).

**Distance** — The inverse framing of similarity (lower = closer);
Chroma and many vector databases report this by default. See
[07-Querying-and-Similarity-Search.md](07-Querying-and-Similarity-Search.md).

**HNSW (Hierarchical Navigable Small World)** — The layered-graph ANN
algorithm behind most local/open-source vector indexes, including
Chroma's default. See
[02-Indexing-Algorithms-and-ANN-Search.md](02-Indexing-Algorithms-and-ANN-Search.md).

**Hybrid Search** — Combining exact-term or keyword matching with
vector similarity in one query, covering semantic search's weakness on
exact identifiers. See
[14-Hybrid-Search-in-a-Vector-Database.md](14-Hybrid-Search-in-a-Vector-Database.md).

**Metadata Filtering** — Narrowing a similarity search by structured
criteria (department, date, tenant) applied during the search itself.
See [08-Metadata-Filtering.md](08-Metadata-Filtering.md).

**Multi-Tenancy** — Keeping multiple tenants' data isolated in a shared
system, either structurally (separate collections) or via a
consistently-enforced metadata filter. See
[12-Multi-Tenancy-and-Access-Control.md](12-Multi-Tenancy-and-Access-Control.md).

**`pgvector`** — A vector-search extension for PostgreSQL, letting an
existing relational database also perform ANN search without standing
up a separate system. See
[16-Vector-Database-vs-Traditional-Database.md](16-Vector-Database-vs-Traditional-Database.md).

**Reranking** — A second, more expensive and accurate scoring pass
applied to a small candidate set an initial vector search already
narrowed down. See [15-Reranking.md](15-Reranking.md).

**Sharding** — Splitting a large collection's data across multiple
machines to scale write/storage capacity. See
[13-Scaling-Vector-Search.md](13-Scaling-Vector-Search.md).

**Soft Delete** — Flagging a record inactive via metadata instead of
removing it, trading a small query-time filtering cost for
reversibility and an audit trail. See
[11-Document-Lifecycle-Update-and-Delete.md](11-Document-Lifecycle-Update-and-Delete.md).

**Stable ID** — A content-derived, deterministic identifier that makes
re-indexing idempotent instead of duplicative. See
[09-Stable-IDs-and-Idempotent-Upserts.md](09-Stable-IDs-and-Idempotent-Upserts.md).

**`upsert()`** — An insert-or-replace operation with no error on ID
collision, the `kubectl apply` of vector database writes. See
[06-Inserting-and-Updating-Vectors.md](06-Inserting-and-Updating-Vectors.md).

**Vector Database** — A datastore specialized for fast nearest-
neighbor search over embeddings, built around an ANN index. See
[01-What-Is-a-Vector-Database.md](01-What-Is-a-Vector-Database.md).

------------------------------------------------------------------------

## Module Complete

That closes out all 20 chapters of **04-Vector-Databases**. Next up per
the [root README](../../README.md) roadmap:

➡️ `05-RAG` (already complete — see [../../05-RAG/](../../05-RAG/))
