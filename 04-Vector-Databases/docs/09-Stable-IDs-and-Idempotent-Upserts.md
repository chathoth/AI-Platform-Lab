# 09 - Stable IDs and Idempotent Upserts

## Introduction

Module 05 chapter 06 introduced content-derived chunk IDs to make a
real RAG pipeline's re-indexing safe. This chapter generalizes that
pattern for any vector database use case — it's one of the highest-
leverage design decisions in this whole module, and one of the easiest
to get wrong by skipping it.

## Learning Objectives

After this chapter I should be able to:

-   Explain what makes an ID "stable" and why that property matters.
-   Design a content-derived ID scheme for a real document set.
-   Explain the failure mode that stable IDs specifically prevent.

------------------------------------------------------------------------

# The Failure Mode This Prevents

``` python
import uuid

# fragile - a new random ID every single run
collection.add(ids=[str(uuid.uuid4())], documents=["Restart the pod by deleting it."])
```

Run an ingestion script twice with random IDs, and the same content
gets indexed twice under two different IDs — the collection now has
duplicate, unremovable-by-content entries, silently inflating storage
and, worse, letting the same fact win multiple slots in a `n_results`
list at query time.

## Stable IDs, Generalized From Module 05

``` python
import hashlib

def stable_id(source: str, chunk_index: int, text: str) -> str:
    raw = f"{source}|{chunk_index}|{text.strip()}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
```

The exact fields to hash depend on your data — module 05 chapter 06
used `source + page + chunk text`; a different document set might use
`source + chunk_index + text`, or `url + section_heading`. The
principle is constant: **derive the ID from content that uniquely and
stably identifies the record**, not from a random generator or a
row-insertion order that could shift between runs.

## Combined With `upsert()`, This Is What Makes Re-Running Safe

``` python
def index_documents(collection, documents: list[dict]):
    ids = [stable_id(d["source"], d["chunk_index"], d["text"]) for d in documents]
    collection.upsert(
        ids=ids,
        documents=[d["text"] for d in documents],
        metadatas=[{"source": d["source"], "chunk_index": d["chunk_index"]} for d in documents],
    )
```

Run this function once, or a hundred times, against the same input
documents, and the collection converges to the same state every time —
chapter 06's `upsert()` chapter and this chapter's stable IDs are two
halves of the same idempotency guarantee, neither sufficient alone
(`upsert()` with a random ID still duplicates; a stable ID with `add()`
silently fails to apply the update on the second run, per chapter 06's
verified behavior — no error, but also no effect).

## Hands-on: Prove Idempotency Directly

``` python
documents = [{"source": "runbook.md", "chunk_index": 0, "text": "Restart the pod by deleting it."}]

index_documents(collection, documents)
print(f"After 1st run: {collection.count()}")

index_documents(collection, documents)  # run it again, unchanged input
print(f"After 2nd run (should be identical): {collection.count()}")

# now change the content slightly and re-run
documents[0]["text"] = "Restart the pod by deleting it - updated syntax."
index_documents(collection, documents)
print(f"After content change: {collection.count()}")  # still the same count - it's an UPDATE, not a new record
```

Wait — that last case is worth sitting with: if the ID is derived from
`text`, changing the text changes the ID, which means it becomes a
*new* record rather than updating the old one. This is a real design
choice: hash on content that should trigger a new ID when it changes
(most fields), but *not* on content that should update in place. Most
real designs hash on a stable identity (like `source + chunk_index`)
rather than the text itself, precisely so edits update the existing
record instead of leaving an orphaned old version behind.

## Common Misconceptions

❌ Random IDs (like UUIDs) are fine as long as you don't re-run the
script.
("As long as you don't re-run it" is exactly the assumption that
breaks in practice — deploys get retried, pipelines get re-triggered,
someone runs the script manually to fix one document. Design for
re-runs from the start.)

❌ Hashing the content itself is always the right ID strategy.
(It works for detecting duplicates, but means an edited document gets
a new ID instead of updating in place — decide deliberately whether
you want edits to create new records or update existing ones.)

✔ Stable IDs and `upsert()` are two halves of the same guarantee —
idempotent re-indexing needs both, not just one.

## Interview Questions

1.  What failure mode do stable, content-derived IDs prevent?
2.  Why is a random UUID a poor choice for a document's vector
    database ID in a pipeline that might re-run?
3.  What's the trade-off between hashing on the text itself versus
    hashing on a stable identity field like `source + chunk_index`?
4.  Why do you need both stable IDs and `upsert()` together for true
    idempotency?

## Summary

A stable, content-derived ID — generalized from module 05's chunk-ID
pattern — combined with `upsert()` (chapter 06) is what makes an
ingestion pipeline safe to run more than once. Decide deliberately
whether an edited document should get a new ID (hash includes the
text) or update in place (hash excludes the text) — both are valid
designs, but only one of them is usually what you actually want.

## Next Chapter

➡️ `10-Persistence-and-Backup.md`
