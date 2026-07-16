# 04 - Chunking the Vacation Policy

## Introduction

Module 03 chapter 07 covered chunking in the abstract. This chapter
applies it to one real, messy case: the Carry-Over section that
chapter 03 flagged as spanning pages 1 and 2 of the actual policy PDF.
If chunking handles that correctly, it'll handle most real documents
correctly — it's a genuinely good stress test, not a toy example.

## Learning Objectives

After this chapter I should be able to:

-   Explain why neither whole pages nor tiny fragments make good chunks.
-   Explain this module's starting chunk size/overlap and why overlap
    matters specifically for the Carry-Over section.
-   Run the chunking step and verify a specific fact survives intact.

------------------------------------------------------------------------

# Why Not Embed One Page at a Time?

A page can contain several unrelated topics. In this policy, a single
page includes accrual rules, carry-over rules, management
responsibilities, and leave-of-absence rules all together — embedding
the whole page (module 03 chapter 07's "blurry average" problem) would
dilute a search for any one of those specific topics.

## Why Not Use Tiny Chunks Either?

A tiny chunk might contain just:

``` text
no later than November 1
```

...without the surrounding sentence that says *what* is due by
November 1. The retriever could technically find the date while losing
the fact that it's the carry-over request deadline — a match with no
usable meaning attached.

## This Module's Starting Configuration

``` env
CHUNK_SIZE=700
CHUNK_OVERLAP=120
```

## Why Overlap Matters, Concretely

The Carry-Over section crosses from page 1 to page 2 in the real
document. Overlap (module 03 chapter 07) helps preserve context if a
chunk boundary happens to fall near:

-   the five-day carry-over rule,
-   the minimum-vacation-usage rule,
-   the November 1 submission deadline.

**Platform analogy:** this is the same reason a log-tailing pipeline
uses overlapping read windows instead of hard-cut boundaries — a single
important event (an error, a rule) shouldn't be able to fall exactly on
a boundary and get split across two reads with neither one making full
sense on its own.

## Hands-on: Verify a Specific Fact Survives Chunking

``` bash
python src/02_chunk_documents.py
```

This calls `chunk_documents()` from `src/utils.py`. Open
`artifacts/chunks.json` and search for the string `November 1`. Confirm
the chunk containing it *also* contains enough surrounding text to
identify the rule as specifically a **carry-over request deadline** —
not just a bare date with no context.

``` python
from pathlib import Path
from src.utils import load_documents, chunk_documents

docs = load_documents(Path("sample-data"))
chunks = chunk_documents(docs)
assert len(chunks) > len(docs)  # chunking should produce more, smaller units

november_chunks = [c for c in chunks if "November 1" in c.page_content]
print(november_chunks[0].page_content)
```

## Experiment: Feel the Trade-off Yourself

Change the configuration and re-run steps 2 through 5 (chunking through
retrieval) to compare results:

``` env
CHUNK_SIZE=250
CHUNK_OVERLAP=0
```

Then try the opposite extreme:

``` env
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

Small chunks with no overlap should start losing context around
sentence boundaries (check whether the November 1 fact stays intact).
Large chunks preserve more context per chunk but start re-introducing
the "blurry average" dilution problem from module 03 chapter 07 — this
is the precision-vs-context trade-off made directly observable against
one real document.

## Common Misconceptions

❌ There's one universally correct chunk size.
(It depends on the document's structure and how granular your
questions are — this module's `CHUNK_SIZE=700` is a starting point
tuned for this specific policy document, not a rule for every document.)

❌ Overlap is just wasted, duplicated storage.
(It's small, deliberate redundancy that prevents a fact from being
split exactly at a chunk boundary — the storage cost is minor compared
to the retrieval-quality cost of losing a fact entirely.)

✔ The best way to validate a chunking configuration isn't eyeballing
chunk sizes — it's checking whether a *specific, known fact* (like the
November 1 deadline) survives intact and identifiable in at least one
chunk.

## Interview Questions

1.  Why does embedding whole pages reduce retrieval precision for this
    document?
2.  Why can a tiny, unoverlapped chunk technically "contain" an answer
    while still being useless?
3.  Why does the Carry-Over section specifically make a good test case
    for chunk overlap?
4.  How would you validate that a chunking configuration is working,
    beyond just checking chunk count?

## Summary

Chunking exists to balance precision (small enough to retrieve
specifically) against context (large enough to preserve meaning) — and
this module's real document, with a Carry-Over section spanning two
pages, is a concrete test of whether that balance is actually working.
Verify chunking by checking that a specific known fact survives intact
in a retrievable chunk, not by eyeballing configuration numbers.

## Next Chapter

➡️ `05-Embeddings.md`
