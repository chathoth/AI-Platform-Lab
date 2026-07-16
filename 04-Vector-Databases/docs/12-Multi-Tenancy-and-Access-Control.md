# 12 - Multi-Tenancy and Access Control

## Introduction

Chapter 04 raised collections-vs-metadata as a design choice and
promised to revisit it at scale. This is that chapter: how to keep
multiple tenants', teams', or customers' data safely separated in a
shared vector database — a real security question, not just an
organizational one.

## Learning Objectives

After this chapter I should be able to:

-   Compare per-tenant collections against a shared collection with
    tenant metadata.
-   Explain why access-control filtering must be enforced in
    application code, not assumed from the database alone.
-   Choose the right isolation strategy for a given tenant count and
    scale.

------------------------------------------------------------------------

# Two Isolation Strategies

**Per-tenant collections** — one collection per tenant:

``` python
def get_tenant_collection(client, tenant_id: str):
    return client.get_or_create_collection(
        name=f"tenant_{tenant_id}",
        embedding_function=OllamaEmbeddingFunction(),
    )
```

Strong isolation — a bug in query logic literally cannot leak data
across tenants, because the tenants' data lives in structurally
separate indexes. Cost: collection sprawl at high tenant counts, and
no easy way to search across tenants if you ever legitimately need to.

**Shared collection with a `tenant_id` filter** — one collection,
every query filtered:

``` python
results = collection.query(
    query_texts=[question],
    n_results=5,
    where={"tenant_id": tenant_id},
)
```

Simpler to operate at high tenant counts, and cross-tenant analytics
(if ever legitimately needed) stay possible. Cost: isolation now
depends entirely on **every single query** correctly including the
filter — a missed filter is a real data leak, not a cosmetic bug.

## Why This Can't Be "The Database's Job" Alone

**Platform analogy:** this is the exact same trust boundary as
row-level security in a shared multi-tenant SQL database — the
database *can* enforce it if configured correctly (Postgres RLS, for
example), but a hand-rolled `where={"tenant_id": ...}` filter added
per-query is only as strong as the discipline of every engineer who
ever writes a query against that collection. One missed filter in one
code path is a cross-tenant data leak.

``` python
# the entire security boundary in a shared-collection design
# lives in code like this - and MUST be centralized, not
# reimplemented at every call site
def tenant_scoped_query(collection, tenant_id: str, query_text: str, n_results: int = 5):
    return collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where={"tenant_id": tenant_id},  # never optional, never omittable
    )
```

Centralizing this into one function that every caller must go through
— never letting application code call `collection.query()` directly —
is what turns "every engineer has to remember the filter" into
"the filter is structurally impossible to forget."

## Choosing Between the Two

  Factor                         Favors per-tenant collections   Favors shared + filter
  --------------------------------- -------------------------------- ------------------------------
  Tenant count                        Low (tens)                        High (thousands+)
  Isolation requirement                 Very strict (regulatory, etc.)     Strict but centrally enforceable
  Need cross-tenant analytics             No                                  Sometimes
  Operational simplicity at scale           Gets unwieldy past a point           Stays manageable

## Hands-on: Simulate Both Approaches

``` python
# shared collection approach
shared = client.get_or_create_collection("shared_demo", embedding_function=OllamaEmbeddingFunction())
shared.add(
    ids=["t1-doc1", "t2-doc1"],
    documents=["Tenant A's internal runbook content.", "Tenant B's internal runbook content."],
    metadatas=[{"tenant_id": "tenant-a"}, {"tenant_id": "tenant-b"}],
)

# a correctly-scoped query for tenant A should never see tenant B's data
result = tenant_scoped_query(shared, "tenant-a", "runbook content")
print(result["metadatas"])  # every result should show tenant_id: tenant-a
```

## Common Misconceptions

❌ A metadata filter is just as secure as separate collections, as
long as you remember to add it.
("As long as you remember" is the exact weakness — centralize the
filter into one code path so it's structurally required, not a
convention every caller has to independently honor.)

❌ Multi-tenancy is only a concern for large SaaS products.
(Any system serving more than one team, department, or customer from
shared infrastructure has this exact problem, whether or not "tenant"
is the word used internally.)

✔ Per-tenant collections make isolation a structural property of the
database; shared-collection filtering makes isolation a property of
your application code — choose based on how much you trust that code
to never have a gap, at your actual tenant count.

## Interview Questions

1.  What's the isolation trade-off between per-tenant collections and
    a shared collection with a metadata filter?
2.  Why is a metadata-filter-based isolation strategy fragile if not
    centralized?
3.  How is this similar to row-level security in a shared SQL
    database?
4.  At what point would you switch from a shared collection to
    per-tenant collections?

## Summary

Multi-tenant isolation in a vector database is either structural
(separate collections per tenant) or enforced in application code
(shared collection, mandatory metadata filter on every query) — and
the second approach is only as safe as centralizing that filter into
one code path everyone must use, since a single missed filter is a
real cross-tenant data leak, not a minor bug.

## Next Chapter

➡️ `13-Scaling-Vector-Search.md`
