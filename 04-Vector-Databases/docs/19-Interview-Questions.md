# 19 - Interview Questions

## Introduction

Every interview question from this module, grouped by chapter, with
the answer framed the way I'd actually say it. Review material — read
the chapters first.

------------------------------------------------------------------------

## Chapter 01 - What Is a Vector Database

**Q: What does a vector database's index do that a linear scan
doesn't?**
It avoids comparing a query against every stored vector — using a
pre-built structure to jump almost directly to the likely nearest
neighbors, staying fast as the collection grows, unlike a full scan.

## Chapter 02 - Indexing Algorithms and ANN Search

**Q: What does "approximate" mean in ANN search, and why is it usually
an acceptable trade-off?**
A small, tunable chance of missing the exact best match, in exchange
for search that stays fast at scale — acceptable because result #1 and
#2 are both usually "good enough" for ranking purposes.

## Chapter 03 - The Vector Database Landscape

**Q: Why does this module use ChromaDB specifically?**
It's embedded, local, and requires no signup — meaning every example
runs with no API key and no data leaving the machine, and it's the
same database module 05's real RAG pipeline uses.

## Chapter 04 - Collections and Namespaces

**Q: When would you split data across collections instead of using
metadata filtering?**
When the data types are fundamentally different, rarely queried
together, or need different embedding models — metadata filtering fits
better for subsets of the same kind of data.

## Chapter 05 - Running ChromaDB Locally

**Q: What's the practical difference between `Client()` and
`PersistentClient()`?**
`Client()` is in-memory only and loses data when the process exits;
`PersistentClient()` writes to disk and survives a restart.

## Chapter 06 - Inserting and Updating Vectors

**Q: Why is `upsert()` generally the safer default over `add()`?**
Verified directly: `add()` on a duplicate ID silently does nothing in
current ChromaDB — no error, no update — which is more dangerous than
an exception, since a broken re-run pipeline can look successful while
quietly failing to apply changes. `upsert()` actually replaces the
record, which is what any ingestion pipeline that might
re-run needs.

## Chapter 07 - Querying and Similarity Search

**Q: Why does Chroma report distance instead of similarity?**
Distance is the inverse framing (lower = closer); it's a convention
worth confirming explicitly, since comparing across different metrics
or misreading the direction silently inverts your ranking.

## Chapter 08 - Metadata Filtering

**Q: Why is filtering during the search better than filtering results
afterward?**
A document that fails the filter never occupies one of your
`n_results` slots — filtering after the fact risks getting fewer
useful results than requested.

## Chapter 09 - Stable IDs and Idempotent Upserts

**Q: Why is a random UUID a poor choice for a document's vector
database ID?**
Re-running the ingestion script produces a new ID each time, creating
duplicate entries instead of updating the existing record.

## Chapter 10 - Persistence and Backup

**Q: What's the difference between persistence and backup?**
Persistence protects against a process restart; backup protects
against disk failure, accidental deletion, or a bad migration — two
separate concerns needing two separate plans.

## Chapter 11 - Document Lifecycle: Update and Delete

**Q: Why prefer soft delete over hard delete for content with real
consequences?**
Soft delete (deactivation via metadata) is reversible and leaves an
audit trail, at the cost of every query needing an `active: True`
filter — usually a good trade for anything where deleting the wrong
thing matters.

## Chapter 12 - Multi-Tenancy and Access Control

**Q: Why is a shared-collection metadata filter for tenant isolation
fragile if not centralized?**
Its safety depends on every single query correctly including the
filter — one missed filter in one code path is a real cross-tenant
data leak, not a cosmetic bug.

## Chapter 13 - Scaling Vector Search

**Q: Which typically becomes a bottleneck first as a vector database
scales — query latency or memory?**
Memory — the ANN index is specifically designed to keep query latency
close to flat as the collection grows; memory footprint is the more
common early wall for an embedded local database.

## Chapter 14 - Hybrid Search in a Vector Database

**Q: What's the difference between `where` and `where_document`
filtering in Chroma?**
`where` filters on structured metadata fields; `where_document` filters
on the document text itself — useful together for combining exact-term
matching with semantic ranking.

## Chapter 15 - Reranking

**Q: Why is reranking only applied to a small candidate set, never the
whole collection?**
It uses a slower, more expensive scorer (like an LLM call per
candidate) — running it against an entire large collection would be
far too slow and costly; it's meant to refine an already-narrowed set.

## Chapter 16 - Vector Database vs. Traditional Database

**Q: What's the concrete deciding question for choosing a dedicated
vector database versus an extension like `pgvector`?**
Whether you need to join vector search results with relational data in
the same transaction, and whether vector search is a primary,
large-scale workload with real tuning needs.

## Chapter 17 - Monitoring and Observability

**Q: Why is query latency alone an incomplete health signal for a
vector database?**
A vector database can be fast and still wrong — due to a metric
mismatch, stale index, or filter bug — so a correctness signal like
scheduled recall@k needs to sit alongside latency and uptime metrics.

## Chapter 18 - Best Practices

**Q: Why do stable IDs and `upsert()` both need to be present together
for safe re-indexing?**
Neither is sufficient alone — `upsert()` with a random ID still
duplicates records, and a stable ID with `add()` silently fails to
apply the update on a second run (verified: no error, just no effect).

------------------------------------------------------------------------

## Rapid-Fire Round

1.  Vector database — a datastore specialized for nearest-neighbor
    search, built around an ANN index.
2.  ANN search — approximate, trading a small accuracy gap for
    speed at scale.
3.  Collection — an isolated, named vector index, like a namespace.
4.  `add()` vs. `upsert()` — silently ignores collision vs. actually
    converges safely.
5.  Distance vs. similarity — inverse conventions, confirm which one
    you're reading.
6.  Metadata filtering — applied during search, not after.
7.  Stable IDs — content-derived, required for idempotent re-indexing.
8.  Soft delete — reversible, filtered out at query time.
9.  Multi-tenancy — structural (separate collections) or enforced in
    code (centralized filter) — never ad hoc.
10. Scaling — memory usually the first wall, not query latency.
11. Reranking — a second, expensive pass over an already-narrowed
    set.
12. Monitoring — latency and uptime plus a correctness signal
    (recall@k).

## Next Chapter

➡️ `20-Glossary.md`
