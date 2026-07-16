# 13 - Glossary

## Introduction

Every term from this module, alphabetical, defined against this
module's real pipeline and document where possible.

------------------------------------------------------------------------

**Chunk** — A retrieval-sized piece of a document, produced by
splitting page-level Documents (chapter 04). This module's default is
700 characters with 120 characters of overlap.

**`chunk_id`** — A stable, content-derived identifier (SHA-256 of
source + page + chunk text) that makes re-indexing idempotent instead
of duplicative. See [06-Vector-Database.md](06-Vector-Database.md).

**Distance Score** — The number Chroma returns for how close a stored
vector is to a query vector — lower means closer, meaningful only
relative to other results from the same search. See
[07-Retrieval.md](07-Retrieval.md).

**Document (LangChain)** — The object a loader produces from source
content: `page_content` plus a `metadata` dict. This module's loader
produces one `Document` per PDF page. See
[03-Document-Loading.md](03-Document-Loading.md).

**Embedding Model** — The model that converts text into a vector; this
module uses `nomic-embed-text` via Ollama, always through
`get_embedding_model()`. See [05-Embeddings.md](05-Embeddings.md).

**Grounded Answer** — An answer supported by retrieved evidence, as
opposed to a hallucinated one. See
[01-What-is-RAG.md](01-What-is-RAG.md) and
[08-Prompting.md](08-Prompting.md).

**Grounding Rules** — The explicit system-prompt instructions
constraining the model to answer only from supplied context. See
[08-Prompting.md](08-Prompting.md).

**Indexing Phase** — The one-time (or on-change) pipeline stage:
load → chunk → embed → store. See
[02-RAG-Architecture.md](02-RAG-Architecture.md).

**Metadata** — Source, page, chunk index, and other fields carried
alongside each chunk/vector, making a search result citable and
actionable. See [02-RAG-Architecture.md](02-RAG-Architecture.md).

**Query Phase** — The per-question pipeline stage: embed the question →
search → build prompt → generate → answer. See
[02-RAG-Architecture.md](02-RAG-Architecture.md).

**RAG (Retrieval-Augmented Generation)** — A pattern combining a
retriever and a generative model so answers can be grounded in real,
current, private documents. See
[01-What-is-RAG.md](01-What-is-RAG.md).

**`RAGPipeline`** — The reusable class in `src/utils.py` wrapping
retrieval, prompt building, and generation into one `.ask(question)`
call — used by both `07_rag_pipeline.py` and the test suite's
`rag_pipeline` fixture.

**Retrieval** — Finding the chunks most relevant to a question by
comparing embeddings, not keywords. See
[07-Retrieval.md](07-Retrieval.md).

**`TOP_K`** — The number of chunks retrieval returns per question; this
module defaults to 4. See [07-Retrieval.md](07-Retrieval.md).

**Vector Database** — A store that persists chunk text, its embedding
vector, and its metadata together as one retrievable record. This
module uses ChromaDB. See
[06-Vector-Database.md](06-Vector-Database.md).

------------------------------------------------------------------------

## Module Complete

That closes out all 13 chapters of **05-RAG**. Next up per the
[root README](../../README.md) roadmap:

➡️ `06-MCP`
