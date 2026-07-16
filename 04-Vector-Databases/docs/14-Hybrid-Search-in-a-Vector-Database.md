# 14 - Hybrid Search in a Vector Database

## Introduction

Module 03 chapter 15 built hybrid search by hand — blending a manual
cosine-similarity score with a manual keyword-overlap score. This
chapter is the same idea, implemented against a real database that has
its own query and filtering machinery to lean on instead of reimplementing
everything from scratch.

## Learning Objectives

After this chapter I should be able to:

-   Combine a metadata-based keyword condition with vector similarity
    in one Chroma query.
-   Explain why some databases offer native hybrid search and others
    don't.
-   Blend two ranked result sets when native support isn't available.

------------------------------------------------------------------------

# Chroma's Approach: Filter Toward Exact Terms, Search for Meaning

Chroma doesn't have a single "hybrid score" built in the way some
dedicated search engines do, but the same effect is achievable by
combining `where_document` (a text-contains condition) with the vector
query:

``` python
results = collection.query(
    query_texts=["what causes error E4021"],
    n_results=5,
    where_document={"$contains": "E4021"},  # exact-term filter
)
```

This guarantees every result actually contains the literal string
`"E4021"`, while still ranking by semantic similarity within that
filtered set — directly solving module 03 chapter 15's "semantic
search misses exact error codes" problem, now handled by the database
instead of hand-rolled keyword-overlap scoring.

## When You Need True Blended Scoring

`where_document` is an exact filter (include/exclude), not a weighted
score — for cases genuinely needing module 03 chapter 15's tunable
`semantic_weight` blend, you still combine two separate result sets
yourself:

``` python
def hybrid_search(collection, query: str, top_k: int = 5, semantic_weight: float = 0.6):
    semantic_results = collection.query(query_texts=[query], n_results=top_k * 2)

    query_words = set(query.lower().split())
    blended = []
    for doc, dist, meta in zip(semantic_results["documents"][0], semantic_results["distances"][0], semantic_results["metadatas"][0]):
        semantic_score = 1 - dist  # convert distance back to similarity (chapter 07)
        keyword_score = len(query_words & set(doc.lower().split())) / max(len(query_words), 1)
        combined = semantic_weight * semantic_score + (1 - semantic_weight) * keyword_score
        blended.append({"document": doc, "metadata": meta, "score": combined})

    blended.sort(key=lambda x: x["score"], reverse=True)
    return blended[:top_k]
```

This is module 03 chapter 15's function, adapted to pull its candidate
set from a real indexed query instead of a full in-memory list —
faster at scale, same blending logic.

## Why Native Hybrid Support Varies

Some vector databases (Weaviate, Qdrant, and Elasticsearch/OpenSearch's
vector fields) offer built-in hybrid search with a tunable blend
parameter, because they were designed with both keyword and vector
indexes from the start. Others, like Chroma, are vector-search-first
and expect exact-term filtering or manual blending for the rest — worth
checking explicitly when picking a database (chapter 03) if hybrid
search quality is a primary requirement, not an afterthought.

## Hands-on: Rescue an Exact-Term Query

``` python
collection.add(
    ids=["d1", "d2"],
    documents=[
        "Common causes of database connection issues include pool exhaustion.",
        "Error E4021 occurs when the connection pool hits its configured max size.",
    ],
)

pure_semantic = collection.query(query_texts=["what causes error E4021"], n_results=2)
print("pure semantic order:", pure_semantic["documents"])

filtered = collection.query(
    query_texts=["what causes error E4021"],
    n_results=2,
    where_document={"$contains": "E4021"},
)
print("filtered to exact term:", filtered["documents"])  # should only include d2
```

## Common Misconceptions

❌ Every vector database supports hybrid search out of the box.
(It varies significantly — check explicitly rather than assuming, per
chapter 03's landscape comparison.)

❌ `where_document` filtering and metadata `where` filtering (chapter
08) are the same thing.
(`where` filters on structured metadata fields; `where_document`
filters on the document text itself — different mechanisms, both
useful together.)

✔ Combining an exact-term filter with vector search is often enough to
solve the specific "missed an error code" problem, without needing a
database with native weighted hybrid scoring.

## Interview Questions

1.  How does `where_document` differ from `where` in a Chroma query?
2.  Why doesn't every vector database offer native hybrid search?
3.  How would you implement a tunable semantic/keyword blend against a
    database without native hybrid support?
4.  What specific problem does combining an exact-term filter with
    vector search solve?

## Summary

Hybrid search in a real vector database can mean two different things:
an exact-term filter (`where_document`) combined with vector ranking —
often enough to fix the "missed an exact error code" problem — or a
true weighted blend of semantic and keyword scores, which still
requires combining two result sets yourself unless the database offers
native support. Module 03 chapter 15's blending function adapts
directly, now pulling from an indexed query instead of a full scan.

## Next Chapter

➡️ `15-Reranking.md`
