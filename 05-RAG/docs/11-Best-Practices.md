# 11 - Best Practices

## Introduction

The consolidated checklist for this module, same spirit as the
best-practices chapter in every other module in this repo — each item
here traces back to something covered earlier, grounded in this
specific pipeline and its real document.

## Learning Objectives

After this chapter I should be able to:

-   Apply a concrete checklist before trusting or shipping a RAG
    pipeline.
-   Explain the reasoning behind each item, tied to its source chapter.

------------------------------------------------------------------------

# The Checklist

## 1. Preserve Source Metadata

Chapter 02/03. Always retain filename and page number end to end — it's
what makes an answer traceable and citable, not just plausible.

## 2. Evaluate Negative Questions, Not Just Positive Ones

Chapter 09. A RAG system must know when the source doesn't contain an
answer — this is arguably the higher-stakes half of the evaluation set.

## 3. Keep Indexing and Querying Separate, Re-Index Deliberately

Chapter 02/06. Re-index only when documents or indexing configuration
actually change — not on every query, and not by habit.

## 4. Rebuild After an Embedding Model Change

Chapter 05/06. Module 03 chapter 11's drift warning, applied directly —
changing the embedding model invalidates the existing index and
requires a full `--reset` and re-index, not an incremental swap.

## 5. Inspect Real Retrieval Results, Not Just Polished Final Answers

Chapter 07/10. A fluent final answer can hide a retrieval miss —
inspect the actual retrieved chunks, not just what the model said about
them.

## 6. Use Representative Questions, Not Just Easy Ones

Chapter 09. This module's own evaluation set covers direct,
paraphrased, cross-section, and unsupported questions — use all four
categories, not just the ones that are easiest to pass.

## 7. Treat Tables and Structured Content Carefully

Chapter 03. Appendix A (page 6 of this policy) is a table, and PDF text
extraction can flatten table structure into something that no longer
reads correctly. For high-accuracy table questions, consider
table-aware extraction, Markdown conversion, structured metadata, or
manual normalization — the module 03 chapter 08 lesson about
content-type-specific handling, applied to tables specifically.

## 8. Never Treat Retrieved Text as Trusted Instructions

Chapter 08. Policy documents (or any retrieved content) are data, not
system instructions — this pipeline's system prompt says so explicitly,
and it's a real defense against prompt injection (module 02 chapter
15), not just a formality.

## 9. Debug in Pipeline Order

Chapter 10. Rule out loading, chunking, embedding, and retrieval before
touching the prompt or the model.

## 10. Keep Utility Functions as the Single Source of Truth

This pipeline's `src/utils.py` now holds `load_documents`,
`chunk_documents`, `generate_embeddings`, and `get_vector_store` as the
one place each operation is implemented — every numbered script and
every test calls through the same functions. Before this was fixed,
the same Chroma-construction logic was duplicated across five different
files; any future change to how the vector store gets built would have
had to be made in five places instead of one, with no guarantee they'd
stay in sync.

## Production Requirements Beyond This Learning Pipeline

A production RAG system needs, in addition to everything above:
authorization filters, document versioning, audit logs, observability,
secure file handling, malware scanning on uploaded documents, retention
and deletion processes, and regression evaluation run on every change —
this module builds the core pipeline correctly first, which is the
prerequisite for all of these being meaningful additions rather than
bolted-on afterthoughts.

## Hands-on: Turn This Into a Repo Checklist

Same pattern as every other module: create a `rag-checklist.md` with
these 10 items as literal checkboxes, and walk through it before
trusting this pipeline's answers for anything beyond learning — or
before adapting it to a real internal document set.

## Common Misconceptions

❌ A RAG pipeline that passes its evaluation set once is done.
(Documents change, embedding models get upgraded, and chunking
configs get tuned — re-run the evaluation set after any of those, not
just once at the start.)

❌ Duplicated helper logic across pipeline scripts is a minor style
issue.
(It's a real correctness risk — the exact bug this module had before
being fixed: tests expected functions that didn't exist anywhere
importable, because the real logic was scattered across five
non-importable, digit-prefixed scripts.)

✔ Every item in this checklist is something this actual pipeline does,
or was just fixed to do — this isn't a generic best-practices list,
it's a description of this codebase's own design decisions.

## Interview Questions

1.  Why does re-indexing need to be deliberate rather than automatic
    on every query?
2.  Why is Appendix A (a table) a special case for this document's
    extraction quality?
3.  Why is retrieved document content treated as untrusted data by the
    system prompt?
4.  What real bug did consolidating duplicated logic into `utils.py`
    fix in this module?

## Summary

Every practice in this checklist is grounded in a specific chapter and,
in several cases, a specific fix made to this actual codebase —
preserving metadata for traceability, evaluating negative questions
as seriously as positive ones, rebuilding deliberately after model or
config changes, debugging in pipeline order, and keeping shared logic
in one place instead of duplicated across scripts.

## Next Chapter

➡️ `12-Interview-Questions.md`
