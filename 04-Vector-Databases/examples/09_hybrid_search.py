"""
Example: 09_hybrid_search.py

Combine an exact-term document filter with vector search so a
specific error code isn't missed just because it's not conceptually
distinctive. Ties back to
docs/14-Hybrid-Search-in-a-Vector-Database.md.

Run:
    ollama pull nomic-embed-text
    python 09_hybrid_search.py
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
    client = chromadb.PersistentClient(path="./chroma_hybrid_demo")
    collection = client.get_or_create_collection(
        "hybrid_demo", embedding_function=OllamaEmbeddingFunction(), metadata={"hnsw:space": "cosine"}
    )
    collection.upsert(
        ids=["d1", "d2"],
        documents=[
            "Common causes of database connection issues include pool exhaustion and timeouts.",
            "Error E4021 occurs when the connection pool hits its configured max size.",
        ],
    )

    print("--- pure semantic search ---")
    pure_semantic = collection.query(query_texts=["what causes error E4021"], n_results=2)
    print(pure_semantic["documents"][0])

    print("\n--- filtered to documents that literally contain 'E4021' ---")
    filtered = collection.query(
        query_texts=["what causes error E4021"],
        n_results=2,
        where_document={"$contains": "E4021"},
    )
    print(filtered["documents"][0])
    print("\nThe filtered version should only ever include d2 - the one")
    print("document that actually mentions the exact error code.")
