# 05 - Running ChromaDB Locally

## Introduction

Every prior chapter used Chroma's built-in default embedding function
for quick demos. This chapter wires it up properly — persistent
storage, and the same local `nomic-embed-text` model used throughout
module 03 — so the rest of this module (and its examples) run on a
consistent, production-shaped setup instead of a toy default.

## Learning Objectives

After this chapter I should be able to:

-   Set up a persistent Chroma client backed by a local embedding
    model.
-   Explain the difference between an in-memory and a persistent
    client.
-   Confirm data survives a process restart.

------------------------------------------------------------------------

# In-Memory vs. Persistent

``` python
import chromadb

# in-memory - gone the moment the process exits, useful for quick tests
ephemeral_client = chromadb.Client()

# persistent - writes to disk, survives a restart
persistent_client = chromadb.PersistentClient(path="./chroma_db")
```

Every earlier chapter's examples used `PersistentClient` already —
worth calling out explicitly here because the difference is a common
source of "why did my data disappear" confusion the first time someone
uses `chromadb.Client()` for something they expected to persist.

## Wiring In a Local Embedding Model

Chroma's default embedding function is a fine quick-start, but for
anything real, module 03's rule applies: know exactly which embedding
model is being used, and keep it consistent (module 03 chapter 11). A
custom embedding function makes that explicit instead of implicit:

``` python
import requests
from chromadb import Documents, EmbeddingFunction, Embeddings

class OllamaEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model: str = "nomic-embed-text", url: str = "http://localhost:11434/api/embeddings"):
        self.model = model
        self.url = url

    def __call__(self, input: Documents) -> Embeddings:
        return [
            requests.post(self.url, json={"model": self.model, "prompt": text}).json()["embedding"]
            for text in input
        ]
```

``` python
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="runbooks",
    embedding_function=OllamaEmbeddingFunction(),
    metadata={"hnsw:space": "cosine"},
)
```

Now every `add()` and `query()` call against this collection uses the
exact same local model, explicitly — this is the pattern every example
script in this module builds on.

## Hands-on: Prove Persistence Across Restarts

``` bash
ollama pull nomic-embed-text
```

``` python
# --- run 1 ---
import chromadb
client = chromadb.PersistentClient(path="./chroma_persist_test")
collection = client.get_or_create_collection("test", embedding_function=OllamaEmbeddingFunction())
collection.add(ids=["1"], documents=["This should still be here after a restart"])
print(f"Count after adding: {collection.count()}")
```

``` python
# --- run 2, a completely separate Python process ---
import chromadb
client = chromadb.PersistentClient(path="./chroma_persist_test")
collection = client.get_or_create_collection("test", embedding_function=OllamaEmbeddingFunction())
print(f"Count after restart, no re-adding: {collection.count()}")  # should still be 1
```

Run these as two genuinely separate script invocations (not in the same
Python session) — the count surviving between them is the direct,
observable proof of persistence, the same verification module 03
chapter 09 recommended for a hand-rolled JSON index, now backed by a
real database.

## Common Misconceptions

❌ `chromadb.Client()` and `chromadb.PersistentClient()` behave the
same way.
(`Client()` is in-memory only — anything added is lost when the
process exits. Always use `PersistentClient` (or a client-server setup)
for anything meant to survive.)

❌ Chroma's default embedding function is fine to use in any real
project.
(It works, but using it means not knowing — or controlling — exactly
which model and version is generating your vectors. Wiring in an
explicit embedding function, as this chapter does, keeps that under
your control, matching module 03 chapter 11's versioning discipline.)

✔ Always verify persistence directly (add data, restart the process,
confirm it's still there) rather than assuming a "persistent" client is
behaving as expected — the same "verify, don't assume" instinct
covered in module 01's best practices.

## Interview Questions

1.  What's the practical difference between `chromadb.Client()` and
    `chromadb.PersistentClient()`?
2.  Why wire in an explicit embedding function instead of relying on
    Chroma's default?
3.  How would you verify that a Chroma collection is actually
    persisting data across restarts?
4.  What does `path="./chroma_db"` actually control?

## Summary

`PersistentClient` writes to disk and survives process restarts;
`Client()` is in-memory and doesn't — a distinction worth verifying
directly rather than assuming. Wiring in an explicit local embedding
function (rather than Chroma's default) keeps the exact model in your
control, the same discipline module 03 chapter 11 recommends for
avoiding silent embedding drift.

## Next Chapter

➡️ `06-Inserting-and-Updating-Vectors.md`
