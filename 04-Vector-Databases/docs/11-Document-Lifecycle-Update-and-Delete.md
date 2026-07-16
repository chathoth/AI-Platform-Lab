# 11 - Document Lifecycle: Update and Delete

## Introduction

Module 05 chapter 11 flagged that a real vector database needs
explicit lifecycle operations — insert, update, deactivate, delete,
re-index — beyond a blunt full rebuild. Chapters 06 and 09 covered
insert and update. This chapter covers the operations most tutorials
skip entirely: actually removing something, and the softer alternative
of deactivating it instead.

## Learning Objectives

After this chapter I should be able to:

-   Delete records by ID and by metadata filter.
-   Explain when a soft delete (deactivation) is safer than a hard
    delete.
-   Design a re-indexing plan for when a source document changes
    significantly.

------------------------------------------------------------------------

# Deleting by ID

``` python
collection.delete(ids=["doc-1", "doc-2"])
```

Straightforward, and irreversible — the same caution any hard delete
deserves anywhere else in infrastructure.

## Deleting by Metadata Filter

``` python
collection.delete(where={"source": "old-runbook.md"})
```

This is the real-world common case: a document was replaced or
retired, and every chunk that came from it needs to go, without having
to look up each individual chunk ID first. This is exactly why chapter
08's metadata (`source`, in particular) matters beyond just filtering
searches — it's also the handle for cleanup.

## Hard Delete vs. Soft Delete

**Hard delete** removes the record entirely — clean, but unrecoverable
without a backup (chapter 10), and if something downstream still holds
a reference to that ID, the reference now points at nothing.

**Soft delete** (deactivation) flags a record as inactive via metadata
instead of removing it:

``` python
collection.update(
    ids=["doc-1"],
    metadatas=[{"active": False, "deactivated_at": "2026-07-15"}],
)
```

...and every query filters it out explicitly:

``` python
results = collection.query(
    query_texts=["restart procedure"],
    n_results=5,
    where={"active": True},
)
```

**Platform analogy:** this is exactly the choice between actually
deleting a Kubernetes resource versus scaling it to zero and labeling
it retired — the second option costs a little ongoing overhead (every
query needs the `active: True` filter) in exchange for reversibility
and an audit trail. For anything where "we deleted the wrong thing" has
real consequences, soft delete is usually the safer default.

## Re-Indexing When a Document Changes Significantly

If a source document's chunking boundaries would change (a major
rewrite, not just a typo fix), the safest approach is: delete all
chunks for that source, then re-add the newly chunked version —
because the old chunk IDs (module 05 chapter 06's `source + page +
text` hash) won't line up with the new chunk boundaries anyway.

``` python
def reindex_document(collection, source: str, new_chunks: list[dict]):
    collection.delete(where={"source": source})  # clear the old version entirely
    collection.upsert(  # add the new version
        ids=[c["chunk_id"] for c in new_chunks],
        documents=[c["text"] for c in new_chunks],
        metadatas=[{"source": source, **c["metadata"]} for c in new_chunks],
    )
```

## Hands-on: Practice Both Delete Paths

``` python
collection.add(
    ids=["a1", "a2", "b1"],
    documents=["old policy text 1", "old policy text 2", "unrelated policy text"],
    metadatas=[{"source": "old.md"}, {"source": "old.md"}, {"source": "other.md"}],
)

print(f"Before: {collection.count()}")
collection.delete(where={"source": "old.md"})
print(f"After deleting by source: {collection.count()}")  # only b1 should remain
```

## Common Misconceptions

❌ Deleting by ID is the only way to remove records.
(Deleting by metadata filter is the far more common real-world
operation — removing every chunk from a retired document without
tracking each chunk ID individually.)

❌ Hard delete is always the right choice for removing outdated
content.
(Soft delete trades a small ongoing query-filter cost for
reversibility and an audit trail — often the safer default, the same
way scaling a deployment to zero beats deleting it outright when you
might need it back.)

✔ When a document's chunking would meaningfully change, delete-then-
readd by source is safer than trying to reconcile old and new chunk
IDs that no longer correspond to the same boundaries.

## Interview Questions

1.  How do you delete every chunk belonging to one source document,
    without listing each chunk ID?
2.  What's the trade-off between a hard delete and a soft delete?
3.  Why does re-chunking a document usually require a delete-then-
    readd instead of an in-place update?
4.  How is soft delete similar to scaling a Kubernetes deployment to
    zero instead of deleting it?

## Summary

Deletion in a vector database is usually done by metadata filter
(removing every chunk from a retired source), not by individually
tracked IDs — and soft delete (deactivation via metadata, filtered out
at query time) is often the safer default over a hard, irreversible
delete. Significant re-chunking calls for delete-then-readd rather than
trying to reconcile old and new chunk boundaries.

## Next Chapter

➡️ `12-Multi-Tenancy-and-Access-Control.md`
