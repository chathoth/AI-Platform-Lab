# Examples

Ten self-contained scripts, each mapped to a technique from
[../docs/](../docs/). Every script runs **entirely against a local
Ollama embedding model** — no API key, no cost, nothing leaves your
machine. That's deliberate: anyone can pull the same model and run
every example exactly as written.

## Setup

```bash
ollama pull nomic-embed-text
pip install requests numpy scikit-learn
```

## Scripts

| Script                              | Concept                              | Docs chapter |
| ------------------------------------- | --------------------------------------- | ------------ |
| `01_generate_embedding.py`            | Your first local embedding, inspected     | 01, 04       |
| `02_similarity_metrics.py`            | Cosine, dot product, Euclidean compared    | 05           |
| `03_chunk_and_embed.py`               | Chunking with and without overlap           | 07           |
| `04_clean_before_embedding.py`        | Stripping noise from logs before embedding  | 08           |
| `05_semantic_search.py`               | Full search engine, persisted to disk         | 09, 10       |
| `06_cluster_incidents.py`             | Grouping text with no labels (k-means)          | 12           |
| `07_find_duplicates.py`               | Near-duplicate detection, flagged for review     | 13           |
| `08_classify_with_embeddings.py`      | Nearest-neighbor classification, no LLM call       | 14           |
| `09_hybrid_search.py`                 | Semantic + keyword blended ranking                   | 15           |
| `10_evaluate_search.py`               | Scoring search quality with recall@k                    | 16           |

Run any of them directly:

```bash
python 01_generate_embedding.py
```

Make sure `ollama serve` is running first (it usually starts
automatically after installing Ollama).
