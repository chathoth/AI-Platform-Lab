# 08 - Metadata Filtering

## Introduction

Semantic similarity alone can't express "only search documents from
this department" or "only the current version of this policy" —
that's what metadata filtering is for, combined with similarity search
in the same query. This is the single feature that turns a generic
similarity search into something safe and precise enough for a real
multi-document system.

## Learning Objectives

After this chapter I should be able to:

-   Combine a metadata filter with a similarity search in one query.
-   Use comparison and logical operators in a filter.
-   Explain why filtering matters for both precision and access
    control.

------------------------------------------------------------------------

# Filtering + Similarity, Together

``` python
results = collection.query(
    query_texts=["what's the deadline for this request"],
    n_results=3,
    where={"department": "hr"},  # only search within HR documents
)
```

This isn't two separate steps (search everything, then filter results)
— Chroma applies the filter *during* the search, which is both more
efficient and, importantly, doesn't risk a filtered-out document
occupying one of your `n_results` slots.

## Filter Operators

``` python
# equality (implicit)
where={"department": "hr"}

# comparison operators
where={"effective_date": {"$gte": "2026-01-01"}}

# logical combination
where={
    "$and": [
        {"department": "hr"},
        {"document_type": "policy"},
    ]
}

# "or" logic
where={"$or": [{"department": "hr"}, {"department": "legal"}]}
```

Available operators typically include `$eq`, `$ne`, `$gt`, `$gte`,
`$lt`, `$lte`, `$in`, `$and`, `$or` — check your specific vector
database's documentation, since the exact syntax varies between Chroma,
Pinecone, Weaviate, and others, even though the underlying concept is
universal.

## Why Filtering Matters Beyond Just Precision

**Precision** — module 05's real pipeline uses metadata like
`document_type` and `effective_date` (module 05 chapter 02) so a search
can be scoped to just current, relevant document types instead of
everything ever indexed.

**Access control** — filtering on an `access_group` or `tenant_id`
field is how a shared collection enforces "only search documents this
user is allowed to see" (chapter 12 goes deeper on this specific
pattern) — a real security boundary, not just a convenience.

**Platform analogy:** this is a `WHERE` clause combined with a
full-text search, or a Kubernetes label selector combined with a field
query — narrowing the candidate set by exact criteria *before or
during* the fuzzy part of the search, not as an afterthought applied to
already-returned results.

## Hands-on: Filter and Search Together

``` python
collection.add(
    ids=["p1", "p2", "p3"],
    documents=[
        "Vacation carry-over must be requested by November 1.",
        "Sick leave carry-over must be requested by December 15.",
        "Vacation carry-over must be requested by November 1.",  # duplicate content, different dept for demo
    ],
    metadatas=[
        {"department": "hr", "document_type": "vacation_policy"},
        {"department": "hr", "document_type": "sick_leave_policy"},
        {"department": "legal", "document_type": "vacation_policy"},
    ],
)

# search only vacation policies, ignoring the sick-leave document entirely
results = collection.query(
    query_texts=["when is the carry-over deadline"],
    n_results=5,
    where={"document_type": "vacation_policy"},
)
print(results["documents"])  # should only include p1 and p3, never p2
```

## Common Misconceptions

❌ Filtering happens after the similarity search, on the returned
results.
(It's applied during the search itself — a document that fails the
filter never competes for one of your `n_results` slots in the first
place.)

❌ Metadata filter syntax is identical across every vector database.
(The concept is universal, but exact operator names and structure
differ between Chroma, Pinecone, Weaviate, and others — check the
specific docs.)

✔ For any system with more than one document type, department, or
access level, metadata filtering isn't optional polish — it's what
keeps a similarity search from returning irrelevant or unauthorized
results.

## Interview Questions

1.  Why is applying a filter during the search better than filtering
    the results afterward?
2.  Give an example of combining two conditions with `$and`.
3.  How does metadata filtering support access control in a shared
    collection?
4.  How is a metadata filter conceptually similar to a Kubernetes label
    selector?

## Summary

Metadata filtering narrows a similarity search by exact criteria
(department, date, document type, access group) applied during the
search itself, not after — both improving precision and, combined with
an access-control field, providing a real security boundary in a
shared collection. This is the feature that makes vector search
practical beyond a single, homogeneous document set.

## Next Chapter

➡️ `09-Stable-IDs-and-Idempotent-Upserts.md`
