"""
Example: 07_lifecycle_update_delete.py

Delete every chunk from a retired source in one call, and compare
hard delete against soft delete (deactivation). Ties back to
docs/11-Document-Lifecycle-Update-and-Delete.md.

Run:
    ollama pull nomic-embed-text
    python 07_lifecycle_update_delete.py
"""

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


if __name__ == "__main__":
    client = chromadb.PersistentClient(path="./chroma_lifecycle_demo")
    collection = client.get_or_create_collection(
        "lifecycle_demo", embedding_function=OllamaEmbeddingFunction(), metadata={"hnsw:space": "cosine"}
    )
    collection.upsert(
        ids=["a1", "a2", "b1"],
        documents=["old policy text 1", "old policy text 2", "unrelated current policy text"],
        metadatas=[
            {"source": "old.md", "active": True},
            {"source": "old.md", "active": True},
            {"source": "other.md", "active": True},
        ],
    )
    print(f"Before: {collection.count()}")

    print("\n--- soft delete: deactivate 'old.md' instead of removing it ---")
    collection.update(ids=["a1", "a2"], metadatas=[{"active": False}, {"active": False}])
    active_only = collection.query(
        query_texts=["policy text"], n_results=5, where={"active": True}
    )
    print("active-only search results:", active_only["documents"][0])
    print(f"Collection count unchanged (soft delete keeps records): {collection.count()}")

    print("\n--- hard delete: remove every chunk from 'old.md' by metadata filter ---")
    collection.delete(where={"source": "old.md"})
    print(f"After hard delete by source: {collection.count()}")
    print("Remaining:", collection.get()["documents"])
