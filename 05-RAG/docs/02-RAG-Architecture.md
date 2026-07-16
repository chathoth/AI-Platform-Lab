# 02 - RAG Architecture

## Introduction

Chapter 01 named the eight components. This chapter is the wiring
diagram — how those components connect into two distinct phases, and
exactly how data flows through this module's actual `src/` scripts,
file by file. I think of this the way I'd think of a CI/CD pipeline
diagram: build phase (indexing) vs. runtime phase (querying), each with
its own inputs, outputs, and failure modes.

## Learning Objectives

After this chapter I should be able to:

-   Distinguish the indexing phase from the query phase.
-   Trace this module's actual data flow from PDF to answer.
-   Explain why metadata is as important as the vectors themselves.

------------------------------------------------------------------------

# Two Phases: Indexing and Querying

A RAG solution separates **indexing** (done once, or whenever source
documents change) from **querying** (done on every user question) —
the same build-vs-run split module 01 chapter 08 drew between training
and inference.

## Indexing Phase

``` text
Source documents
      ↓
Document loader
      ↓
Text normalization
      ↓
Chunking
      ↓
Embedding generation
      ↓
Vector storage
```

**Source documents** — PDFs, Word docs, Confluence pages, GitHub repos,
object storage, databases — anything with knowledge worth retrieving.

**Document loading** extracts text and metadata:

``` json
{
  "source": "leave-policy.pdf",
  "page": 1,
  "department": "Human Resources",
  "effective_date": "2026-01-01"
}
```

**Text normalization** cleans up extraction artifacts: repeated
headers/footers, broken line wraps, inconsistent whitespace, flattened
tables — the RAG-pipeline equivalent of module 03 chapter 08's
"strip noise before embedding" lesson, applied at the document level
instead of the log-line level.

**Chunking** splits long documents into retrieval-sized units — covered
in depth in chapter 04.

**Embedding generation** converts each chunk into a vector:

``` text
"Employees receive 20 days of annual leave"
                 ↓
[0.021, -0.144, 0.883, ...]
```

**Vector storage** persists the chunk text, its vector, its metadata,
and a stable unique ID together — covered in chapter 06.

## Query Phase

``` text
User question
      ↓
Question embedding
      ↓
Vector similarity search
      ↓
Top matching chunks
      ↓
Prompt construction
      ↓
Language model
      ↓
Answer and sources
```

The question must be embedded with the **same embedding model** used
during indexing (module 03 chapter 01's rule: never compare vectors
from different models). The vector database compares the question's
vector against every stored vector, returns the closest matches, those
get formatted into a prompt alongside system instructions, and the
language model generates the final answer.

## This Module's Actual Data Flow

``` text
sample-data/*.pdf
      ↓
01_load_documents.py
      ↓
artifacts/loaded_documents.json
      ↓
02_chunk_documents.py
      ↓
artifacts/chunks.json
      ↓
03_generate_embeddings.py
      ↓
artifacts/embeddings.json
      ↓
04_store_vectors.py
      ↓
chroma_db/
      ↓
05_similarity_search.py
      ↓
retrieved chunks
      ↓
06_build_prompt.py
      ↓
artifacts/prompt.txt
      ↓
07_rag_pipeline.py
      ↓
final answer
```

Every arrow in that diagram is a real file you can open and inspect —
this isn't a conceptual diagram, it's the literal path data takes
through this repository, which is what makes chapter 10 (Debugging)
possible: you can inspect the JSON artifact at every single stage
boundary.

## Metadata Architecture

Metadata is as important as the embeddings themselves — a vector alone
can't be turned into a citable, actionable answer (the same point
module 03 chapter 09 made about storing embeddings generically).

  Field              Purpose
  ------------------- ----------------------------------
  `source`             Display the source file
  `page`                Show page-level citations
  `chunk_id`             Identify a chunk uniquely (chapter 06)
  `document_type`        Filter policies, contracts, FAQs
  `department`            Restrict search to a business area
  `effective_date`         Prefer current documents
  `access_group`            Enforce authorization

**Platform analogy:** this is exactly the difference between an
unlabeled backup and one tagged with environment, timestamp, and owner
— technically the same data, but only one of them is actually useful
when you need to act on it under pressure.

## Production Additions

A production RAG architecture typically adds: OCR, document versioning,
metadata extraction, hybrid search (module 03 chapter 15), reranking,
authorization filters, caching, query rewriting, guardrails,
observability, evaluation pipelines, and feedback collection. This
module builds the core pipeline first — these are the natural next
additions once the fundamentals are solid.

## Hands-on: Watch the Files Appear

``` bash
python src/01_load_documents.py   # creates artifacts/loaded_documents.json
python src/02_chunk_documents.py  # creates artifacts/chunks.json
python src/03_generate_embeddings.py  # creates artifacts/embeddings.json
python src/04_store_vectors.py --reset  # creates chroma_db/

ls -la artifacts/ chroma_db/
```

Open each JSON file as it's created and confirm it matches the diagram
above — this is the fastest way to build real intuition for where data
actually lives at each stage.

## Common Misconceptions

❌ Indexing and querying are the same operation, just at different
times.
(They're structurally different: indexing runs once (or on document
change) and is compute-heavy; querying runs on every question and needs
to be fast — the same build-vs-run split as training vs. inference.)

❌ Metadata is a nice-to-have on top of the "real" data (the vector).
(Without metadata, a search hit is just numbers with no way to cite,
filter, or act on it — metadata is what turns a match into an answer.)

✔ Every arrow in this module's data-flow diagram corresponds to a real,
inspectable file — use that literally when debugging (chapter 10).

## Interview Questions

1.  What's the difference between the indexing phase and the query
    phase?
2.  Why must the same embedding model be used for both indexing and
    querying?
3.  Name three metadata fields useful in a production RAG system and
    what each enables.
4.  Walk through this module's actual data flow from PDF to answer.

## Summary

RAG architecture splits into an indexing phase (documents → chunks →
vectors → storage, run once or on change) and a query phase (question →
retrieval → prompt → answer, run every request) — the same shape as a
build pipeline versus a running service. Metadata carried alongside
each vector is what makes a retrieved match citable and actionable, not
just numerically similar.

## Next Chapter

➡️ `03-Document-Loading.md`
