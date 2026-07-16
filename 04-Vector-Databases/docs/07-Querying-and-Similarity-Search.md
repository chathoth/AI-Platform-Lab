# 07 - Querying and Similarity Search

## Introduction

Module 03 chapter 10 built `search()` by hand. This chapter is the same
operation through a real database's API — `query()` — plus the details
that actually matter in practice: what comes back, how distance is
reported, and how to query by an existing vector instead of new text.

## Learning Objectives

After this chapter I should be able to:

-   Run a similarity query and correctly read every part of the
    result.
-   Query using an existing embedding instead of new text.
-   Explain why Chroma returns distance, not similarity, by default.

------------------------------------------------------------------------

# A Basic Query

``` python
results = collection.query(
    query_texts=["one of our pods keeps restarting, what do I check?"],
    n_results=3,
)

print(results["documents"])   # the matched text
print(results["distances"])   # how far each match is from the query
print(results["metadatas"])   # source, page, etc. for each match
print(results["ids"])         # the stable ID for each match
```

`query_texts` gets embedded internally using the collection's
configured embedding function (chapter 05) — the exact same model used
when the documents were added, automatically.

## Distance, Not Similarity

Chroma reports **distance** — lower means closer/more similar, the
inverse framing from cosine *similarity* (module 03 chapter 05, where
higher meant more similar). This trips people up the first time:

``` text
cosine similarity: 1.0 = identical, 0.0 = unrelated, -1.0 = opposite
cosine distance:    0.0 = identical, 1.0 = unrelated, 2.0 = opposite
                    (distance = 1 - similarity, for cosine space)
```

Always check which convention a specific database and configured
metric use — module 03 chapter 05's warning about not comparing scores
across different metrics applies doubly here, since even the *direction*
of "better" can flip between similarity and distance.

## Querying With Multiple Texts at Once

``` python
results = collection.query(
    query_texts=["pod restarting", "disk almost full"],
    n_results=2,
)
# results["documents"][0] -> top 2 matches for "pod restarting"
# results["documents"][1] -> top 2 matches for "disk almost full"
```

Batching queries (same lesson as batching inserts, chapter 06) is more
efficient than looping over single queries when you have several
questions to answer at once.

## Querying by Vector Directly

Sometimes you already have an embedding — from a previous computation,
or because you're comparing two stored documents to each other rather
than a fresh piece of text:

``` python
existing_doc = collection.get(ids=["doc-1"], include=["embeddings"])
similar = collection.query(
    query_embeddings=existing_doc["embeddings"],
    n_results=5,
)
```

This is the mechanism behind "find documents similar to this one" —
module 03 chapter 13's deduplication and chapter 12's clustering both
build on exactly this capability, now backed by an indexed database
instead of a manual loop.

## Hands-on: Compare a Text Query and a Vector Query

``` python
collection.add(
    ids=["r1", "r2", "r3"],
    documents=[
        "To debug CrashLoopBackOff, check kubectl describe pod and logs --previous.",
        "When disk usage hits 90% on a primary DB, it's HIGH severity.",
        "To roll back a deployment, use kubectl rollout undo.",
    ],
)

# query by text
by_text = collection.query(query_texts=["pod keeps restarting"], n_results=1)
print("by text:", by_text["documents"])

# query by an existing document's own vector - "more like this one"
r1 = collection.get(ids=["r1"], include=["embeddings"])
by_vector = collection.query(query_embeddings=r1["embeddings"], n_results=2)
print("more like r1:", by_vector["documents"])  # r1 itself should rank first (distance ~0)
```

## Common Misconceptions

❌ A lower distance score always means an absolutely "good" match.
(Same warning as module 03 chapter 05 — it's only meaningful relative
to other results from the same query and collection, not as an
absolute quality threshold.)

❌ You can only query with fresh text.
(`query_embeddings` lets you query with any vector you already have —
including a stored document's own embedding, for "find similar" use
cases.)

✔ Always confirm which convention (distance vs. similarity) a specific
database and metric report — getting the direction backwards silently
inverts your ranking.

## Interview Questions

1.  What four things does a typical Chroma query result contain?
2.  Why does Chroma report distance instead of similarity, and how do
    the two relate for cosine?
3.  When would you query with `query_embeddings` instead of
    `query_texts`?
4.  Why is batching multiple queries into one call more efficient than
    looping?

## Summary

Querying a vector database returns matched documents, their distances,
metadata, and IDs — with distance conventionally inverted from
similarity (lower is better), which is worth confirming explicitly for
any metric you use. Querying by an existing vector, not just fresh
text, is the mechanism behind "find documents similar to this one,"
building on module 03's clustering and deduplication chapters with real
indexed search behind it.

## Next Chapter

➡️ `08-Metadata-Filtering.md`
