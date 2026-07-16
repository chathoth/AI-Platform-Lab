# 03 - Document Loading

## Introduction

This is where the pipeline actually starts, and it's a good chapter to
slow down on: I've seen more RAG debugging sessions end here than in
any "smarter model" fix — if the loader silently mangles a document,
every later stage inherits a problem it has no way to detect on its
own.

## Learning Objectives

After this chapter I should be able to:

-   Explain why an LLM can't read a PDF directly.
-   Load `Vacation Time Policy.pdf` into LangChain `Document` objects
    and verify the result.
-   Explain why page boundaries aren't the same as topic boundaries.

------------------------------------------------------------------------

# Why a Loader Is Required

An LLM only ever sees text — it has no native understanding of a PDF's
binary format, embedded fonts, or layout. The first job in any RAG
pipeline is extracting plain text and attaching metadata, before any
model is involved at all. This module uses `PyPDFLoader`, which turns
each PDF page into one LangChain `Document`.

``` python
Document(
    page_content="Vacation Time ...",
    metadata={
        "source": "Vacation Time Policy.pdf",
        "page": 1,
        "source_path": ".../Vacation Time Policy.pdf",
    },
)
```

**Platform analogy:** this is a parser at the front of an ingestion
pipeline — the same role a log-shipping agent plays turning raw bytes
into structured events before anything downstream can query them. Get
the parsing wrong here, and every downstream stage (chunking, indexing,
retrieval) is working with corrupted input and has no way to know it.

## Expected Result for This Module's Document

The policy PDF has six pages, so loading it should produce exactly six
page-level `Document` objects — this is a concrete, checkable number,
not an approximation.

## Why Metadata Matters

Metadata (chapter 02) is what lets the system later:

-   display the source filename in an answer's citation,
-   cite specific page numbers,
-   filter by document type or department,
-   debug retrieval by tracing an answer back to its source,
-   manage document versions over time.

## Hands-on: Load It and Verify

``` bash
python src/01_load_documents.py
```

This calls `load_documents()` from `src/utils.py` (the same function
the test suite calls directly in `tests/test_01_load_documents.py`),
prints a preview, and writes the result to
`artifacts/loaded_documents.json`. Open that file and confirm:

-   six page objects exist,
-   page numbers are human-readable (`1` through `6`, not zero-based),
-   page 1 contains the Accrual and Carry-Over sections,
-   page 2 continues the Carry-Over section,
-   page 6 contains Appendix A.

``` python
from pathlib import Path
from src.utils import load_documents

docs = load_documents(Path("sample-data"))
assert len(docs) == 6
assert docs[0].metadata["source"] == "Vacation Time Policy.pdf"
assert docs[0].metadata["page"] == 1
print(docs[0].page_content[:200])
```

## Important Observation: Page Boundaries ≠ Topic Boundaries

PDF page breaks are **layout** boundaries, not **semantic** ones. In
this exact document, the Carry-Over section begins on page 1 and
continues onto page 2 — a real, verifiable example of why a RAG system
can't assume a complete topic always fits inside one page, or one
chunk. This single observation is the entire motivation for chapter 04
(Chunking) using overlap.

## Common Misconceptions

❌ PyPDFLoader (or any PDF loader) reliably preserves layout like tables
and columns.
(Text extraction from PDFs is lossy — tables in particular often
flatten in ways that lose their row/column structure, a problem chapter
11 revisits directly for this document's Appendix A.)

❌ One page always equals one self-contained topic.
(This document's own Carry-Over section proves otherwise — it spans
pages 1 and 2, meaning a page-level (or badly-chunked) retrieval could
easily miss half the relevant content.)

✔ The loading step is the cheapest place in the whole pipeline to catch
a problem — verify the exact page count and spot-check page content
before moving on to chunking, embedding, or anything more expensive.

## Interview Questions

1.  Why can't an LLM read a PDF file directly?
2.  What does `PyPDFLoader` produce for a six-page PDF, and why does
    that number matter as a checkpoint?
3.  Why are PDF page boundaries not reliable proxies for topic
    boundaries?
4.  Name three things metadata attached during loading enables later
    in the pipeline.

## Summary

Document loading extracts plain text and metadata from a source file
before any model gets involved — get this step wrong, and every later
stage inherits a problem with no way to detect it. This module's real
PDF has a concrete, checkable expected result (six pages) and a
concrete example of why page boundaries can't be trusted as topic
boundaries: its own Carry-Over section spans two pages.

## Next Chapter

➡️ `04-Chunking.md`
