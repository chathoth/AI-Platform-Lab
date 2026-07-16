# 06 - Vector Database

## Introduction

Module 03 chapter 09 covered storage in the abstract, and chapter 10
covered when to graduate from a Python list to a real database. This
chapter is that graduation, applied: this module uses **ChromaDB**, a
real, persistent vector database, and this chapter covers exactly what
it stores, why stable IDs matter, and how re-indexing actually works
against the real policy document.

## Learning Objectives

After this chapter I should be able to:

-   Explain what a ChromaDB record contains, conceptually.
-   Explain why stable, content-derived chunk IDs prevent duplicate
    indexing.
-   Reset and rebuild the vector database, and know when that's
    actually necessary.

------------------------------------------------------------------------

# What a Chroma Record Contains

Conceptually, every indexed item in this pipeline's collection carries:

``` text
ID
Chunk text
Embedding vector
Source filename
Page number
Chunk index
```

This maps directly onto module 03 chapter 09's "never store just the
vector" rule — Chroma stores the vector *and* the document text *and*
metadata together, retrievable as a unit.

## Why Stable IDs Matter

Without a stable ID, re-running ingestion on the same document creates
duplicate entries every time — the vector database equivalent of an
`INSERT` with no unique constraint. This project avoids that by hashing
`source + page + chunk text` together into a deterministic `chunk_id`
(see `stable_chunk_id()` in `src/utils.py`):

``` python
def stable_chunk_id(document: Document) -> str:
    source = str(document.metadata.get("source", ""))
    page = str(document.metadata.get("page", ""))
    text = document.page_content.strip()
    raw = f"{source}|{page}|{text}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
```

Because the ID is *derived from content*, re-indexing the exact same
chunk twice produces the exact same ID — Chroma treats it as an update
to an existing record, not a new one. This is the same idempotency
guarantee module 03 chapter 17 recommends via content-hashing before
re-embedding, applied one level further: here it also controls what
gets **stored**, not just what gets re-embedded.

**Platform analogy:** this is `kubectl apply` versus `kubectl create` —
applying the same manifest repeatedly converges to the same state
instead of erroring or duplicating resources, because the resource has
a stable identity. `chunk_id` is that stable identity for a piece of
retrievable text.

## Reset and Rebuild

``` bash
python src/04_store_vectors.py --reset
```

Use `--reset` when:

-   chunking settings changed (chapter 04's `CHUNK_SIZE`/`CHUNK_OVERLAP`),
-   the source PDF changed,
-   the embedding model changed (chapter 05's "one rule that breaks
    everything"),
-   duplicates or stale data are suspected.

Without `--reset`, re-running `04_store_vectors.py` re-applies the same
stable-ID chunks — safe, but it won't remove chunks that no longer
exist if the source document shrank or was edited.

## Hands-on: Watch Idempotency in Action

``` bash
python src/04_store_vectors.py --reset
python -c "from src.utils import get_vector_store; print(get_vector_store()._collection.count())"

# run it again WITHOUT --reset - count should stay identical, not double
python src/04_store_vectors.py
python -c "from src.utils import get_vector_store; print(get_vector_store()._collection.count())"
```

The collection count staying flat across the second run is the direct,
observable proof that stable IDs are doing their job.

## Production Note

A production vector database needs explicit document lifecycle
operations beyond what this learning pipeline covers: insert, update,
deactivate, delete, and re-index — each one a real operation against
`chroma_db/`, not just a full reset. `--reset` is a blunt instrument
appropriate for learning; a production system needs surgical updates.

## Common Misconceptions

❌ Re-running the indexing script always creates duplicate entries.
(Only true without stable IDs — this pipeline's content-derived
`chunk_id` makes re-indexing idempotent by design.)

❌ `--reset` is something you'd need to run routinely.
(It's a full rebuild, appropriate after a structural change — chunking
config, embedding model, or source document. Routine re-indexing of
unchanged content should rely on stable IDs, not a full reset.)

✔ A stable, content-derived ID is what turns "re-run the pipeline" from
a risky operation into a safe, idempotent one — the same guarantee
`kubectl apply` gives you over `kubectl create`.

## Interview Questions

1.  What does a Chroma record contain beyond just the embedding vector?
2.  How is `chunk_id` computed, and why does that make re-indexing
    idempotent?
3.  When should you actually use `--reset`, versus just re-running the
    indexing step?
4.  Why is `chunk_id` conceptually similar to `kubectl apply`'s
    resource identity?

## Summary

ChromaDB stores chunk text, its embedding vector, and its metadata
together as one retrievable record, identified by a content-derived
`chunk_id` that makes re-indexing idempotent instead of duplicative.
`--reset` is for structural changes (chunking, embedding model, source
document); routine re-runs rely on stable IDs to converge safely.

## Next Chapter

➡️ `07-Retrieval.md`
