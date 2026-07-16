# 11 - Embedding Drift and Model Versioning

## Introduction

Chapter 01 said it plainly: never compare vectors from two different
embedding models. This chapter is about the operational consequence of
that rule — what happens when you upgrade the embedding model behind an
existing index, and why "just swap the model" is one of the more subtle
ways to silently break a production search feature.

## Learning Objectives

After this chapter I should be able to:

-   Explain why swapping an embedding model invalidates an existing
    index.
-   Design a re-embedding/migration plan for a model upgrade.
-   Track which model version produced which stored vector.

------------------------------------------------------------------------

# Why You Can't Just Swap the Model

Every embedding model has its own coordinate system, shaped by its own
training. A vector from `nomic-embed-text` and a vector from a newer
model aren't just "a little different" — they live in entirely
unrelated spaces, and comparing them (even though the math would happily
compute a number) produces a meaningless result.

``` text
Old index (embedded with model A):  [vectors in space A]
New queries (embedded with model B): [vectors in space B]

Comparing across A and B: numerically possible, semantically meaningless
```

If you upgrade your embedding model but don't re-embed the existing
documents, every search silently degrades — not with an error, just
with worse and worse results, until someone notices relevance has quietly
gotten bad and has no idea why.

**Platform analogy:** this is a schema migration that only updates new
rows, not the whole table — old rows are now silently in a different,
incompatible format from what your application code expects, and
nothing tells you until a query on old data returns nonsense. An
embedding model change is exactly that kind of change: it needs a full
migration, not an incremental cutover.

## A Minimal Migration Plan

``` text
1. Deploy the new model alongside the old one (don't remove the old one yet)
2. Re-embed the ENTIRE document set with the new model
3. Store vectors with a model_version tag - never mix versions in one index
4. Validate search quality on the new index before cutting over
5. Only then, switch queries to use the new index
6. Keep the old index available briefly, in case of rollback
```

``` python
entry = {
    "text": "...",
    "vector": [...],
    "metadata": {
        "source": "runbook-01.md",
        "embedding_model": "nomic-embed-text",  # critical - never omit this
        "embedded_at": "2026-07-15",
    },
}
```

Tagging every stored vector with the model that produced it is the
single cheapest insurance against this failure mode — it turns "did we
already migrate this?" from a guess into a query.

## Detecting Drift Before It's a Production Problem

``` python
def validate_index_consistency(index: list, expected_model: str) -> list:
    mismatched = [e for e in index if e["metadata"].get("embedding_model") != expected_model]
    if mismatched:
        raise ValueError(f"{len(mismatched)} entries embedded with a different model than expected!")
    return index
```

A check like this, run before an index is used in production, catches
exactly the "half-migrated" state that would otherwise degrade search
quality silently — the same instinct as a schema-version check that
refuses to run application code against an unmigrated database.

## Hands-on: Simulate the Failure, Then Fix It

``` python
import requests, numpy as np

def embed(text, model):
    r = requests.post("http://localhost:11434/api/embeddings", json={"model": model, "prompt": text})
    return np.array(r.json()["embedding"])

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# same text, same model twice - should be near-identical (allowing tiny float variance)
v1 = embed("disk usage is critical", "nomic-embed-text")
v2 = embed("disk usage is critical", "nomic-embed-text")
print("same model, same text:", cosine(v1, v2))
```

If you have a second embedding model pulled locally, embed the same
text with both and compare vector *lengths* (`len(v1)` vs `len(v2)`) —
different dimension counts alone prove they can't even be compared
mathematically, let alone meaningfully.

## Common Misconceptions

❌ Upgrading to a "better" embedding model is a safe, low-risk change.
(Without a full re-embedding migration, it silently corrupts search
quality across the entire existing index — one of the more dangerous
"quiet" changes in this whole stack.)

❌ You'll notice immediately if an embedding model swap goes wrong.
(There's no error, no crash — just gradually worse search relevance,
which is exactly the kind of regression that goes unnoticed without an
explicit consistency check.)

✔ Tag every stored vector with the model (and ideally version) that
produced it — the cheapest possible insurance against silent drift.

## Interview Questions

1.  Why can't vectors from two different embedding models be compared,
    even though the similarity math still runs without error?
2.  What does re-embedding a document set actually involve, and why
    can't it be skipped during a model upgrade?
3.  Why is an embedding model swap comparable to a partial schema
    migration?
4.  What's the cheapest safeguard against accidentally mixing vectors
    from two different model versions in one index?

## Summary

Swapping an embedding model without a full re-embedding migration
silently corrupts search quality, because vectors from different
models live in incompatible coordinate spaces with no error to signal
the mismatch. Tag every stored vector with its source model, and treat
a model upgrade as a full migration — re-embed everything, validate,
then cut over — not an incremental swap.

## Next Chapter

➡️ `12-Clustering-With-Embeddings.md`
