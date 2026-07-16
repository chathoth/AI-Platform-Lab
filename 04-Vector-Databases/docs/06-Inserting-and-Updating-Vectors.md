# 06 - Inserting and Updating Vectors

## Introduction

With a real, persistent, locally-embedded collection wired up (chapter
05), this chapter covers the actual write path — `add`, `upsert`, and
`update` — and a genuinely surprising behavior worth verifying for
yourself rather than assuming: what `add()` actually does on an ID
collision is quieter, and more dangerous, than you'd expect.

## Learning Objectives

After this chapter I should be able to:

-   Insert documents with `add()` and know exactly what happens on ID
    collision — verified, not assumed.
-   Use `upsert()` for safe, idempotent re-ingestion.
-   Explain the difference between `update()` and `upsert()`.

------------------------------------------------------------------------

# `add()`: Insert, and Only Insert

``` python
collection.add(
    ids=["doc-1", "doc-2"],
    documents=["Restart the pod by deleting it.", "Disk usage above 90% is HIGH severity."],
    metadatas=[{"source": "runbook-01.md"}, {"source": "runbook-02.md"}],
)
```

Here's the part worth testing yourself instead of trusting a tutorial
(this one included): calling `add()` again with an ID that already
exists does **not** raise an error in current ChromaDB — it silently
**ignores the new call and keeps the original record**. Verified
directly:

``` python
collection.add(ids=["x1"], documents=["original version"])
collection.add(ids=["x1"], documents=["trying to add again"])  # no error raised

print(collection.get(ids=["x1"])["documents"])
# -> ['original version']  - the second add() had NO effect at all
```

This is a genuinely dangerous default: a re-run ingestion script that
uses `add()` won't crash and won't warn you — it'll just silently fail
to apply any updates, and you won't find out until someone notices
stale content days later. A loud error would actually be the *safer*
failure mode here; this is quieter and worse.

**Exact behavior can vary by vector database and version** — this is
exactly why "verify, don't assume" (module 01's running theme) applies
to infrastructure behavior, not just to model output.

## `upsert()`: Insert or Update, Safely and Verifiably

``` python
collection.upsert(
    ids=["doc-1"],  # same ID as before
    documents=["Restart the pod by deleting it - updated with the new kubectl syntax."],
    metadatas=[{"source": "runbook-01.md", "version": 2}],
)
```

`upsert()` inserts if the ID is new, or **actually replaces** the
existing record if the ID already exists — and this one *is* verifiable
directly: fetch the record after upserting and confirm the content
changed. Combined with the stable `chunk_id` pattern from module 05
chapter 06 (a content-derived hash), `upsert()` is what makes
re-running an ingestion pipeline safe and idempotent, the same
`kubectl apply` analogy module 05 chapter 06 already established.

**Platform analogy:** `add()`'s silent-ignore-on-collision behavior is
worse than `kubectl create`'s loud failure on an existing resource —
at least `kubectl create` tells you something didn't happen. `upsert()`
is `kubectl apply` — it converges to the desired state regardless of
whether the resource existed before, and it actually applies your
change. For any real ingestion pipeline that might run more than once
against the same source data, `upsert()` is almost always the right
default — not just for convenience, but because `add()`'s failure mode
on a re-run is silent.

## `update()`: Modify Fields Without Touching Others

``` python
collection.update(
    ids=["doc-1"],
    metadatas=[{"reviewed": True}],  # only this field changes
)
```

`update()` requires the ID to already exist and only touches the
fields you pass — useful for something like flagging a document as
reviewed without re-embedding or re-supplying its full text. Unlike
`add()`, `update()`'s failure mode on a missing ID is worth checking in
your specific database version too, rather than assumed.

## Batching Inserts

Same lesson as module 03 chapter 06: pass lists, not a loop of
single-item calls.

``` python
# slow - one round trip per document
for doc in documents:
    collection.add(ids=[doc["id"]], documents=[doc["text"]])

# fast - one call for the whole batch
collection.add(
    ids=[doc["id"] for doc in documents],
    documents=[doc["text"] for doc in documents],
)
```

## Hands-on: Verify This Behavior Yourself, Don't Trust This Page

``` python
collection.add(ids=["x1"], documents=["original version"])
collection.add(ids=["x1"], documents=["trying to add again"])
print("after duplicate add():", collection.get(ids=["x1"])["documents"])
# confirm for yourself: did it change, error, or silently do nothing?

collection.upsert(ids=["x1"], documents=["updated via upsert"])
print("after upsert():", collection.get(ids=["x1"])["documents"])
# confirm: did THIS one actually change the stored content?
```

Run this exact snippet in your own environment before trusting either
this page's description or your own assumption — vector database
client behavior on edge cases like this is exactly the kind of detail
that changes between library versions without much fanfare.

## Common Misconceptions

❌ `add()` raises an error when the ID already exists.
(In current ChromaDB, it silently does nothing — no error, no
update. This is genuinely worth verifying in your own installed
version rather than assuming either behavior.)

❌ A silent no-op is a "safer" failure mode than a loud error.
(It's the opposite — a loud error stops you immediately; a silent
no-op lets a broken re-run ingestion pipeline look successful while
quietly failing to apply any changes.)

✔ For any ingestion pipeline you expect to run more than once — which
is nearly all of them — `upsert()` with stable, content-derived IDs
(module 05 chapter 06) is the safe default, precisely because `add()`'s
collision behavior is silent and easy to miss.

## Interview Questions

1.  What actually happens when you call `add()` with an ID that
    already exists in current ChromaDB, and why is that more dangerous
    than an error?
2.  Why is `upsert()` generally the safer default for a real ingestion
    pipeline?
3.  How does `update()` differ from `upsert()`?
4.  Why should you verify a database client's collision behavior
    directly rather than trust documentation (including this chapter)?

## Summary

`add()` on a duplicate ID silently does nothing in current ChromaDB —
no error, no update — which is a more dangerous failure mode than an
exception would be, because a broken re-run pipeline can look
successful while quietly failing to apply changes. `upsert()` actually
replaces the existing record, verifiably, and combined with stable,
content-derived IDs is what makes an ingestion pipeline genuinely safe
to re-run. Verify behavior like this directly in your own environment
rather than trusting any single source, this chapter included.

## Next Chapter

➡️ `07-Querying-and-Similarity-Search.md`
