"""
Example: 06_stable_ids.py

Prove that content-derived stable IDs plus upsert() make an ingestion
pipeline idempotent - running it twice doesn't duplicate anything.
Ties back to docs/09-Stable-IDs-and-Idempotent-Upserts.md.

Run:
    ollama pull nomic-embed-text
    python 06_stable_ids.py
"""

import hashlib

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


def stable_id(source: str, chunk_index: int) -> str:
    # Hashes on identity (source + position), not on the text itself,
    # so an edit to the text updates the record in place instead of
    # creating an orphaned new one (see docs ch. 09's discussion of
    # this exact trade-off).
    raw = f"{source}|{chunk_index}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def index_documents(collection, documents: list[dict]):
    ids = [stable_id(d["source"], d["chunk_index"]) for d in documents]
    collection.upsert(
        ids=ids,
        documents=[d["text"] for d in documents],
        metadatas=[{"source": d["source"], "chunk_index": d["chunk_index"]} for d in documents],
    )


if __name__ == "__main__":
    client = chromadb.PersistentClient(path="./chroma_stable_id_demo")
    collection = client.get_or_create_collection(
        "stable_id_demo", embedding_function=OllamaEmbeddingFunction(), metadata={"hnsw:space": "cosine"}
    )

    documents = [{"source": "runbook.md", "chunk_index": 0, "text": "Restart the pod by deleting it."}]

    index_documents(collection, documents)
    print(f"After 1st run: {collection.count()}")

    index_documents(collection, documents)  # unchanged input, run again
    print(f"After 2nd run (should be identical): {collection.count()}")

    documents[0]["text"] = "Restart the pod by deleting it - updated syntax."
    index_documents(collection, documents)
    print(f"After content update (still 1 record, updated in place): {collection.count()}")
    print("Current text:", collection.get(ids=[stable_id("runbook.md", 0)])["documents"])
