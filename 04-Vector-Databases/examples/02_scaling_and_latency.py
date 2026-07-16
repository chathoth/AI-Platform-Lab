"""
Example: 02_scaling_and_latency.py

Watch query latency and on-disk size as a collection grows. Ties back
to docs/02-Indexing-Algorithms-and-ANN-Search.md and
docs/13-Scaling-Vector-Search.md.

Run:
    ollama pull nomic-embed-text
    python 02_scaling_and_latency.py
"""

import pathlib
import time

import chromadb
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


def dir_size_mb(path: str) -> float:
    total = sum(f.stat().st_size for f in pathlib.Path(path).rglob("*") if f.is_file())
    return total / 1_000_000


if __name__ == "__main__":
    db_path = "./chroma_scale_demo"
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection(
        "scale_test", embedding_function=OllamaEmbeddingFunction(), metadata={"hnsw:space": "cosine"}
    )

    for batch in range(4):
        docs = [f"Sample incident report {batch * 50 + i} about infrastructure degradation" for i in range(50)]
        collection.add(ids=[f"doc-{batch}-{i}" for i in range(50)], documents=docs)

        start = time.perf_counter()
        collection.query(query_texts=["why is the service degraded"], n_results=5)
        latency_ms = (time.perf_counter() - start) * 1000

        print(
            f"count={collection.count():>4}  "
            f"query_latency={latency_ms:6.1f}ms  "
            f"disk_size={dir_size_mb(db_path):6.2f}MB"
        )

    print()
    print("Notice query latency stays roughly flat while disk size grows")
    print("roughly linearly - that's the ANN index (docs ch. 02) doing its job.")
