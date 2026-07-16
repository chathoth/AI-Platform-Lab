"""
Example: 01_create_collection.py

Create a persistent Chroma collection backed by a local Ollama
embedding model, add documents, and query it. Ties back to
docs/01-What-Is-a-Vector-Database.md and
docs/05-Running-ChromaDB-Locally.md.

Run:
    ollama pull nomic-embed-text
    pip install chromadb requests
    python 01_create_collection.py
"""

import requests
from chromadb import Documents, EmbeddingFunction, Embeddings
import chromadb


class OllamaEmbeddingFunction(EmbeddingFunction):
    """Wires Chroma up to a local Ollama embedding model explicitly,
    instead of relying on Chroma's built-in default (docs ch. 05)."""

    def __init__(self, model: str = "nomic-embed-text", url: str = "http://localhost:11434/api/embeddings"):
        self.model = model
        self.url = url

    def __call__(self, input: Documents) -> Embeddings:
        return [
            requests.post(self.url, json={"model": self.model, "prompt": text}).json()["embedding"]
            for text in input
        ]


if __name__ == "__main__":
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(
        name="runbooks",
        embedding_function=OllamaEmbeddingFunction(),
        metadata={"hnsw:space": "cosine"},  # explicit metric, per docs ch. 04
    )

    collection.add(
        ids=["r1", "r2", "r3"],
        documents=[
            "To debug CrashLoopBackOff, check kubectl describe pod and logs --previous.",
            "When disk usage hits 90% on a primary DB, it's HIGH severity per SRE-042.",
            "To roll back a failed deployment, run kubectl rollout undo deployment/<name>.",
        ],
        metadatas=[
            {"source": "runbook-01.md"},
            {"source": "runbook-02.md"},
            {"source": "runbook-03.md"},
        ],
    )

    print(f"Collection count: {collection.count()}")

    results = collection.query(
        query_texts=["one of our pods keeps restarting, what do I check?"],
        n_results=2,
    )
    for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        print(f"[distance={dist:.4f}] {meta['source']}: {doc}")
