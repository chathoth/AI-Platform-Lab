# 12 - Interview Questions

## Introduction

Every interview question from this module, grouped by chapter, with
the answer framed the way I'd actually say it — grounded in this
module's real pipeline and its one real document, not hypotheticals.
Review material — read the chapters first.

------------------------------------------------------------------------

## Chapter 01 - What Is RAG

**Q: What are the two systems RAG combines?**
A retriever, which finds relevant information, and a generative model,
which turns that information into a readable, grounded answer.

## Chapter 02 - RAG Architecture

**Q: What's the difference between the indexing phase and the query
phase?**
Indexing runs once (or when documents change) and is compute-heavy:
load, chunk, embed, store. Querying runs on every question and needs to
be fast: embed the question, search, build a prompt, generate — the
same build-vs-run split as training vs. inference.

## Chapter 03 - Document Loading

**Q: Why are PDF page boundaries not reliable proxies for topic
boundaries?**
This module's own document proves it — its Carry-Over section spans
pages 1 and 2, so page-level retrieval alone could miss half the
relevant content.

## Chapter 04 - Chunking

**Q: Why does the Carry-Over section make a good test case for chunk
overlap?**
It spans a natural page boundary in the real document, so it directly
tests whether the chosen `CHUNK_SIZE`/`CHUNK_OVERLAP` preserves a real
fact instead of splitting it apart.

## Chapter 05 - Embeddings

**Q: Where does this codebase enforce "same embedding model for
indexing and querying," structurally?**
`get_embedding_model()` in `src/utils.py` is the single place an
`OllamaEmbeddings` instance gets constructed — every script calls
through it, so indexing and querying can't silently drift onto
different models.

## Chapter 06 - Vector Database

**Q: How does `chunk_id` make re-indexing idempotent?**
It's a SHA-256 hash of `source + page + chunk text` — re-indexing the
same content produces the same ID, so Chroma updates the existing
record instead of creating a duplicate.

## Chapter 07 - Retrieval

**Q: Why does a paraphrased query with no shared vocabulary still
retrieve the correct chunk?**
Because retrieval compares embeddings (learned meaning), not keywords —
proven directly in this module by testing paraphrased questions against
the real policy document.

## Chapter 08 - Prompting

**Q: Why does the system prompt tell the model to treat retrieved
document content as untrusted, not as instructions?**
It's a direct defense against prompt injection (module 02 chapter 15)
— without that rule, text embedded in a retrieved document could be
crafted to override the assistant's actual instructions.

## Chapter 09 - Evaluation

**Q: Why does the evaluation dataset deliberately include unanswerable
questions?**
They test the higher-stakes failure mode — a confidently wrong answer
on something the source document doesn't cover — which is more
dangerous than an answer that correctly says "I don't know."

## Chapter 10 - Debugging

**Q: Why should debugging follow pipeline order instead of jumping
straight to the model?**
Because loading, chunking, and retrieval failures are far more common
in practice, and "fixing" a wrong answer by changing the prompt or
model when the real bug is upstream just papers over the actual
problem.

## Chapter 11 - Best Practices

**Q: What real bug did consolidating duplicated logic into
`src/utils.py` fix?**
The test suite expected functions like `load_documents` and
`get_vector_store` to be importable from `src.utils` — before the fix,
that logic was duplicated across five separate, digit-prefixed scripts
that couldn't be imported as modules at all, so every test importing
them failed immediately.

------------------------------------------------------------------------

## Rapid-Fire Round

1.  RAG — retriever + generator, grounding answers in real documents.
2.  Indexing vs. querying — build phase vs. run phase.
3.  Page boundaries — layout, not semantic, boundaries.
4.  Chunk overlap — protects facts that fall near a boundary.
5.  Embedding model consistency — indexing and querying must match,
    enforced structurally, not just by convention.
6.  `chunk_id` — content-derived hash, makes re-indexing idempotent.
7.  Semantic retrieval — matches meaning, not keywords.
8.  Grounding rules — each one defends a specific failure mode.
9.  Negative evaluation — tests the model's ability to say "I don't
    know."
10. Debugging order — rule out pipeline stages before touching the
    model.
11. Shared utility functions — one source of truth, prevents drift and
    import bugs.

## Next Chapter

➡️ `13-Glossary.md`
