# Examples

Ten self-contained scripts, each mapped to a technique from
[../docs/](../docs/). Every script runs against a **local, persistent
ChromaDB collection backed by a local Ollama embedding model** — no
API key, no signup, nothing leaves your machine.

## Setup

```bash
ollama pull nomic-embed-text
ollama pull llama3.1:8b       # only needed by 10_reranking.py
pip install chromadb requests openai
```

## Scripts

| Script                             | Concept                                | Docs chapter |
| ------------------------------------- | ----------------------------------------- | ------------ |
| `01_create_collection.py`             | Persistent collection, add, query           | 01, 05       |
| `02_scaling_and_latency.py`           | Query latency vs. disk size as data grows    | 02, 13       |
| `03_upsert_vs_add.py`                 | `add()` errors on collision, `upsert()` doesn't | 06        |
| `04_query_and_distance.py`            | Reading query results, "more like this"        | 07           |
| `05_metadata_filtering.py`            | Filtering during search, not after              | 08           |
| `06_stable_ids.py`                    | Idempotent re-indexing with content-derived IDs  | 09           |
| `07_lifecycle_update_delete.py`       | Soft delete vs. hard delete by filter             | 11           |
| `08_multi_tenant_isolation.py`        | Centralized tenant-scoped querying                  | 12           |
| `09_hybrid_search.py`                 | Exact-term filter + vector ranking                    | 14           |
| `10_reranking.py`                     | LLM-based reranking of a small candidate set            | 15           |

Run any of them directly:

```bash
python 01_create_collection.py
```

Make sure `ollama serve` is running first. Each script creates its own
`./chroma_*_demo` directory on first run — safe to delete any of them
to reset that script's state.
