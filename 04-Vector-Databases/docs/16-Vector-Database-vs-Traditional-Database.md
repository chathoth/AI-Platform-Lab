# 16 - Vector Database vs. Traditional Database

## Introduction

By now this module has covered enough real vector-database mechanics
(indexing, filtering, lifecycle, scaling) to answer a question that
comes up constantly from engineers new to this space: do I need a
*separate* database for this, or can my existing Postgres/Elasticsearch
handle it? This chapter is a direct, honest comparison.

## Learning Objectives

After this chapter I should be able to:

-   Compare a dedicated vector database against a vector extension on
    an existing database.
-   Identify what each approach is genuinely better at.
-   Make (and justify) this decision for a real system you already
    operate.

------------------------------------------------------------------------

# Two Real Options, Not a Vector-Database-vs-Nothing Choice

**Dedicated vector database** (Chroma, Milvus, Qdrant, Pinecone) — built
from the ground up around ANN indexing (chapter 02); vector search is
the primary, most-optimized use case.

**Vector extension on an existing database** (`pgvector` for Postgres,
Elasticsearch/OpenSearch vector fields) — adds ANN indexing to a
database you already run for other things; vector search is one
capability among many.

## What Each Is Genuinely Better At

  Factor                              Dedicated vector DB          Extension on existing DB
  -------------------------------------- ------------------------------ --------------------------------
  Raw vector search performance/scale       Usually better, purpose-built    Usually adequate, not class-leading
  Operational simplicity (new system)          Another system to run/monitor    None — reuses infra you already operate
  Joining vector search with relational data     Requires app-level joins          Native SQL joins, transactions
  Metadata filtering sophistication                Good, purpose-built               Good, and reuses existing indexes/query language
  Team familiarity                                   New tool to learn                    Already know it

**Platform analogy:** this is the same "add a capability to what you
already run" versus "bring in a specialized tool" decision behind
choosing Redis for caching versus adding a cache table to Postgres —
the specialized tool is usually faster at its one job; the extension
avoids operating Yet Another System, and lets you keep transactional
guarantees across your vector and non-vector data in the same query.

## A Concrete Deciding Question

``` text
Do you need to JOIN vector search results with relational data in
the same transaction? (e.g. "find similar support tickets, but only
ones belonging to customers on an active contract")

  Yes, frequently  → pgvector (or similar) - native SQL joins win
  No, rarely         → either works; choose based on scale and team
                        familiarity

Is vector search the PRIMARY workload, at real scale, with vector-
specific tuning needs (chapter 02's HNSW parameters, sharding)?

  Yes  → dedicated vector database - purpose-built tuning surface
  No     → an extension is probably simpler to operate
```

## Where This Module's Choice (Chroma) Fits

Chroma is a dedicated vector database, chosen for this module
specifically because it's embedded and local (chapter 03) — but the
underlying decision framework above applies regardless of which
specific option you pick. A real production system already running
Postgres for its transactional data, needing vector search over a
modest number of embeddings that need to join against relational
records, would reasonably choose `pgvector` over adding Chroma as a
second system to operate.

## Hands-on: Frame the Decision for a System You Know

Take a real (or realistic) system you operate or have operated. Answer
the deciding question above for it: does it need vector-relational
joins, and is vector search a primary, large-scale workload? Write down
which option — dedicated vector database or an extension — the
framework points to, and why. This is the actual exercise platform
engineers do before this decision gets made for real, not a coding
exercise.

## Common Misconceptions

❌ A dedicated vector database is always the "more correct" choice for
any AI project.
(It's the better choice for vector-search-primary workloads at scale —
an extension on an existing database is frequently the more pragmatic
choice when you need relational joins or want to avoid operating a new
system.)

❌ `pgvector` and similar extensions can't scale to real production
workloads.
(They handle a substantial range of real-world scale well — the
crossover point where a dedicated database clearly wins is higher than
many assume, tied to chapter 13's actual scaling symptoms, not to
category alone.)

✔ The deciding factor is rarely "which is more powerful" in the
abstract — it's whether you need relational joins with vector search,
and whether vector search is a primary, large workload or one
capability among several.

## Interview Questions

1.  What's the main advantage of a vector extension on an existing
    database over a dedicated vector database?
2.  What's the main advantage of a dedicated vector database?
3.  What's the concrete deciding question this chapter proposes for
    choosing between them?
4.  Why might a team already running Postgres reasonably choose
    `pgvector` over standing up Chroma or Milvus?

## Summary

Choosing between a dedicated vector database and a vector extension on
an existing database comes down to two concrete questions: do you need
to join vector search with relational data in the same transaction, and
is vector search a primary, large-scale workload with specific tuning
needs? Neither option is universally "more correct" — this module's use
of Chroma is a deliberate choice for its local-first, zero-signup
properties, not a universal recommendation.

## Next Chapter

➡️ `17-Monitoring-and-Observability.md`
