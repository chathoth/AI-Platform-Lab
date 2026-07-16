# 05 - Embeddings

## Introduction

Module 03 covered embeddings in full depth, in the abstract. This
chapter is the short, applied version: the exact model this pipeline
uses, the one rule that breaks everything if violated, and how to
inspect the real vectors this module generates from the policy PDF.
If anything here feels unfamiliar, module 03 is the place to go deeper.

## Learning Objectives

After this chapter I should be able to:

-   Explain what embedding a chunk and embedding a question have in
    common.
-   Name the embedding model this pipeline uses and why it matters that
    it stays consistent.
-   Inspect a real generated embedding and know what's worth looking at.

------------------------------------------------------------------------

# Same Space, Different Wording

Document text:

``` text
Requests to carry over vacation must be submitted no later than
November 1.
```

A user's question, worded completely differently:

``` text
What is the deadline for moving unused vacation to next year?
```

Zero words in common — `"carry over"` vs. `"moving"`, `"submitted"` vs.
nothing at all — but both describe the same underlying fact. An
embedding model places both pieces of text near each other in vector
space based on learned meaning, not shared vocabulary (module 03
chapter 01). This is the exact mechanism that makes semantic retrieval
(chapter 07) work at all.

## The Model This Module Uses

``` text
nomic-embed-text
```

...served locally through Ollama. Chosen for the same reasons module 03
chapter 03 recommends it as a default: solid general-purpose quality,
free, and — since this pipeline embeds a real (if fictional) HR
document — nothing leaves the machine.

## The One Rule That Breaks Everything If Violated

**Use the exact same embedding model for document chunks during
indexing and for user questions during retrieval.** This is module 03
chapter 01's "never compare vectors from different models" rule, made
concrete: `src/utils.py`'s `get_embedding_model()` is the single place
this pipeline constructs an `OllamaEmbeddings` instance, and every
script (`03_generate_embeddings.py`, `04_store_vectors.py`,
`05_similarity_search.py`, and beyond) calls through it — so indexing
and querying can never silently drift onto different models.

**Platform analogy:** this is the same discipline as pinning a shared
library version across every service that depends on it — one function
version does the embedding everywhere, so there's no seam where two
parts of the pipeline could quietly disagree about what a vector means.

## Hands-on: Generate and Inspect Real Embeddings

``` bash
python src/03_generate_embeddings.py
```

This calls `generate_embeddings()` from `src/utils.py`. Open
`artifacts/embeddings.json` and look at:

-   **vector dimensions** — how many numbers per chunk (module 03
    chapter 04's dimensionality math),
-   **the first few vector values** — you'll confirm they're not
    human-readable; their value is entirely relational,
-   **vector norm** — a sanity-check number, useful for spotting a
    degenerate (e.g. all-zero) embedding,
-   **source and page metadata** — carried through from chunking
    (chapter 04) so every vector still traces back to its origin.

``` python
from src.utils import generate_embeddings

vectors = generate_embeddings(["Example chunk"])
print(f"count: {len(vectors)}")
print(f"dimensions: {len(vectors[0])}")
```

Raw vector values are not meaningful to read directly — their only
value is *relative distance and direction* to other vectors, which is
exactly what chapter 07 (Retrieval) puts to use.

## Common Misconceptions

❌ You could safely switch to a different embedding model mid-project
without consequence.
(Module 03 chapter 11 covers this directly — it would silently
invalidate the existing `chroma_db/` index. This pipeline's
single-source-of-truth `get_embedding_model()` function is specifically
designed to make that mistake harder to make by accident.)

❌ The raw numbers in an embedding vector are individually meaningful.
(Nothing about a single number in the vector is interpretable on its
own — only relative position to other vectors, per module 03 chapter
01.)

✔ Vector norm and dimension count are useful *sanity checks*
(catching a broken or degenerate embedding call) — they are not a
measure of embedding quality itself.

## Interview Questions

1.  Why can two pieces of text with zero shared words end up with
    similar embeddings?
2.  Why must the same embedding model be used for indexing and
    querying in this pipeline?
3.  Where does this codebase enforce that rule structurally, rather
    than just by convention?
4.  What can a vector's norm tell you, and what can't it tell you?

## Summary

This module embeds both document chunks and user questions with
`nomic-embed-text`, always through the same shared `get_embedding_model()`
function, so indexing and querying can never silently drift onto
different models — the single most important rule from module 03
applied structurally, not just as a guideline to remember.

## Next Chapter

➡️ `06-Vector-Database.md`
