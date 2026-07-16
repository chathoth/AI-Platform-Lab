# 04 - Collections and Namespaces

## Introduction

Every example so far quietly created a "collection" without explaining
it. This chapter covers what that actually is — the organizational
unit that keeps unrelated vector sets from colliding, the same role a
database schema or a Kubernetes namespace plays for keeping unrelated
resources apart.

## Learning Objectives

After this chapter I should be able to:

-   Explain what a collection is and why it matters.
-   Decide when to split data across multiple collections versus using
    metadata to separate it within one.
-   Set a collection's distance metric explicitly instead of relying
    on a default.

------------------------------------------------------------------------

# What a Collection Is

A collection is a named, isolated set of vectors — its own index, its
own ID space, queried independently of every other collection in the
same database.

``` python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

runbooks = client.get_or_create_collection(name="runbooks")
incidents = client.get_or_create_collection(name="incidents")

# these two collections never see each other's data, even though
# they live in the same PersistentClient / same directory on disk
```

**Platform analogy:** this is a Kubernetes namespace, or a separate
database schema — logical isolation within one running system.
Querying the `runbooks` collection can never accidentally return a
result from `incidents`, the same way a query scoped to one namespace
can't accidentally touch resources in another.

## Collections vs. Metadata: Two Ways to Separate Data

Both approaches keep data apart — the right one depends on how
*independent* the data actually needs to be:

  Use separate collections when                Use metadata filtering (chapter 08) when
  ---------------------------------------------- --------------------------------------------
  Data types are fundamentally different            Data is the same "kind," just different subsets
  You'll query them independently, never together    You sometimes need to query across the subsets
  Different embedding models per data type             Same embedding model throughout
  Strong isolation matters (e.g. per-tenant data)        Isolation is a filter, not a hard boundary

``` text
Separate collections:  "runbooks" vs "incident_reports" - genuinely
                        different content types, queried separately

Metadata filtering:    one "documents" collection, with a
                        "department": "finance" vs "department": "hr"
                        field - same kind of content, sometimes
                        queried together, sometimes filtered apart
```

Chapter 12 (multi-tenancy) revisits this exact decision at a larger
scale — per-tenant collections vs. a shared collection with a
`tenant_id` metadata filter.

## Setting the Distance Metric Explicitly

Chroma defaults to a distance metric, but module 03 chapter 05's advice
— check what your embedding model recommends, and set it explicitly —
applies here too:

``` python
collection = client.get_or_create_collection(
    name="runbooks",
    metadata={"hnsw:space": "cosine"},  # explicit, not left to the default
)
```

Leaving this implicit is the same silent-mismatch risk module 03
chapter 05 warned about — better to state it once, deliberately, than
discover later that a default didn't match your embedding model's
assumptions.

## Hands-on: Prove Isolation Between Collections

``` python
import chromadb

client = chromadb.PersistentClient(path="./chroma_collections_demo")

runbooks = client.get_or_create_collection("runbooks", metadata={"hnsw:space": "cosine"})
incidents = client.get_or_create_collection("incidents", metadata={"hnsw:space": "cosine"})

runbooks.add(ids=["r1"], documents=["To restart a stuck pod, delete it and let the deployment recreate it."])
incidents.add(ids=["i1"], documents=["INC-2345: checkout service returned 500s for 12 minutes."])

# querying "runbooks" for something that only exists in "incidents"
# should return nothing relevant, even though both collections exist
# in the same PersistentClient directory
result = runbooks.query(query_texts=["INC-2345 checkout outage"], n_results=1)
print(result["documents"])
```

## Common Misconceptions

❌ More collections is always better organization.
(Splitting data that's frequently queried *together* across
collections just adds complexity — use metadata filtering within one
collection for that case, per the table above.)

❌ The distance metric is a minor detail that defaults handle fine.
(Different metrics rank results differently — module 03 chapter 05's
lesson applies here directly: set it deliberately, matching what your
embedding model expects.)

✔ Choose collections vs. metadata based on whether the data needs
**hard isolation** (separate collections) or just **filterable
subsets** (metadata) — not on habit.

## Interview Questions

1.  What is a collection, and what does it isolate?
2.  When would you split data across separate collections instead of
    using metadata filtering within one?
3.  Why should the distance metric be set explicitly rather than left
    as a default?
4.  How is a collection similar to a Kubernetes namespace?

## Summary

A collection is a named, isolated vector index — the organizational
unit that keeps unrelated data from colliding, similar to a namespace
or schema. Choose separate collections for genuinely independent data
that's rarely queried together, and metadata filtering for subsets of
the same kind of data — and set the distance metric explicitly rather
than trusting a default.

## Next Chapter

➡️ `05-Running-ChromaDB-Locally.md`
