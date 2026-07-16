# 10 - Persistence and Backup

## Introduction

Chapter 05 proved data survives a process restart. This chapter is
about the next question a platform engineer asks immediately after
that: what actually is on disk, and what's the recovery plan if it gets
corrupted or deleted? A vector database is still a database — it needs
the same backup discipline as any other stateful system, even when
it's "just" holding derived data.

## Learning Objectives

After this chapter I should be able to:

-   Locate and understand what a persistent Chroma directory actually
    contains.
-   Explain the difference between backing up the vector database and
    being able to regenerate it.
-   Choose a backup strategy appropriate for the data's actual value.

------------------------------------------------------------------------

# What's Actually on Disk

``` bash
ls -la chroma_db/
```

A persistent Chroma directory contains the HNSW index files, a SQLite
metadata store, and the raw vector data — everything needed to
reconstruct the collection exactly as it was, without needing to
re-embed anything.

## Two Different Recovery Strategies

**Strategy 1: Back up the database files directly** — copy
`chroma_db/` (or the equivalent for your vector database) to durable
storage on a schedule, the same as backing up any other stateful
service's data directory.

**Strategy 2: Regenerate from source** — if the original documents
(chapter 09's ingestion source) are themselves durably stored, and
re-embedding is acceptably fast/cheap, you may not need to back up the
vector database at all — just re-run the ingestion pipeline against
the source documents.

  Factor                          Favors direct backup           Favors regenerate-from-source
  --------------------------------- --------------------------------- --------------------------------
  Re-embedding cost/time                High (large corpus, slow model)   Low (small corpus, fast local model)
  Source documents durably stored         Not necessarily                     Yes, reliably
  Recovery time requirement                 Must be fast                        Can tolerate a rebuild window

**Platform analogy:** this is the exact same choice as backing up a
database's data files versus relying on being able to replay events
from a durable message log — both are valid disaster-recovery
strategies, and the right one depends on how expensive "replay" is and
how durable the source of truth already is.

## This Module's Own Case

Every example in this module can be regenerated from the source text
in the example itself (or, in module 05's case, from the PDF in
`sample-data/`) using a fast, free, local embedding model — so
"regenerate from source" is the obviously right strategy here, and
`chroma_db/` is correctly gitignored (module 05 chapter 06)
rather than backed up as precious data. A production system embedding
millions of documents through a slower or paid API would likely weigh
this very differently.

## Hands-on: Practice an Actual Recovery

``` bash
# simulate data loss
rm -rf ./chroma_persist_test

# recover by re-running the ingestion, from source, from scratch
python -c "
import chromadb
client = chromadb.PersistentClient(path='./chroma_persist_test')
collection = client.get_or_create_collection('test', embedding_function=OllamaEmbeddingFunction())
collection.add(ids=['1'], documents=['This should still be here after a restart'])
print(f'Recovered count: {collection.count()}')
"
```

Actually running this — not just reading about it — is the point:
disaster recovery plans that have never been executed are unverified
assumptions, not real plans.

## Common Misconceptions

❌ A vector database's data is always safe to skip backing up because
"it's derived data."
(True only when regenerating it is actually fast, cheap, and the
source documents are themselves durably stored — verify that
assumption rather than assuming it by default.)

❌ Persistence to disk is the same thing as being backed up.
(Persistence protects against a process restart; it does nothing
against disk failure, accidental deletion, or a bad migration —
backup is a separate concern with its own plan.)

✔ Whichever recovery strategy you choose, actually test it — restore
from a backup, or run the regenerate-from-source pipeline end to end —
before you need it for real.

## Interview Questions

1.  What does a persistent Chroma directory actually contain on disk?
2.  What two recovery strategies exist for a vector database, and what
    factors decide between them?
3.  Why is `chroma_db/` correctly gitignored in this repository rather
    than committed?
4.  Why is an untested recovery plan not really a recovery plan?

## Summary

A persistent vector database directory contains everything needed to
reconstruct a collection exactly, and needs the same backup discipline
as any other stateful system — either direct backup of the data files,
or a verified regenerate-from-source pipeline, chosen based on
re-embedding cost and how durable the source documents already are.
This module's local, free embedding model makes "regenerate from
source" the obvious choice — a larger, paid-API pipeline might not have
that luxury.

## Next Chapter

➡️ `11-Document-Lifecycle-Update-and-Delete.md`
