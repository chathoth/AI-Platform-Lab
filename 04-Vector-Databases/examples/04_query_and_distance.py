"""
Example: 04_query_and_distance.py

Query a collection and inspect every part of the result, including
querying by an existing document's own vector ("more like this").
Ties back to docs/07-Querying-and-Similarity-Search.md.

Run:
    ollama pull nomic-embed-text
    python 04_query_and_distance.py
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
    client = chromadb.PersistentClient(path="./chroma_query_demo")
    collection = client.get_or_create_collection(
        "query_demo", embedding_function=OllamaEmbeddingFunction(), metadata={"hnsw:space": "cosine"}
    )
    collection.upsert(
        ids=["r1", "r2", "r3"],
        documents=[
            "To debug CrashLoopBackOff, check kubectl describe pod and logs --previous.",
            "When disk usage hits 90% on a primary DB, it's HIGH severity.",
            "To roll back a deployment, use kubectl rollout undo.",
        ],
    )

    print("--- query by text ---")
    by_text = collection.query(query_texts=["pod keeps restarting"], n_results=2)
    for doc, dist, doc_id in zip(by_text["documents"][0], by_text["distances"][0], by_text["ids"][0]):
        print(f"  id={doc_id} distance={dist:.4f}: {doc}")

    print("\n--- query by an existing document's own vector ('more like this') ---")
    r1 = collection.get(ids=["r1"], include=["embeddings"])
    by_vector = collection.query(query_embeddings=r1["embeddings"], n_results=3)
    for doc, dist, doc_id in zip(by_vector["documents"][0], by_vector["distances"][0], by_vector["ids"][0]):
        print(f"  id={doc_id} distance={dist:.4f}: {doc}")

    print("\nr1 should rank first against its own vector, with distance near 0.")
