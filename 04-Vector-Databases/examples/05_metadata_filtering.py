"""
Example: 05_metadata_filtering.py

Combine a metadata filter with a similarity search in one query, so a
department's documents never leak into another department's results.
Ties back to docs/08-Metadata-Filtering.md.

Run:
    ollama pull nomic-embed-text
    python 05_metadata_filtering.py
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
    client = chromadb.PersistentClient(path="./chroma_filter_demo")
    collection = client.get_or_create_collection(
        "filter_demo", embedding_function=OllamaEmbeddingFunction(), metadata={"hnsw:space": "cosine"}
    )
    collection.upsert(
        ids=["p1", "p2", "p3"],
        documents=[
            "Vacation carry-over must be requested by November 1.",
            "Sick leave carry-over must be requested by December 15.",
            "Vacation carry-over must be requested by November 1.",
        ],
        metadatas=[
            {"department": "hr", "document_type": "vacation_policy"},
            {"department": "hr", "document_type": "sick_leave_policy"},
            {"department": "legal", "document_type": "vacation_policy"},
        ],
    )

    print("--- unfiltered search ---")
    unfiltered = collection.query(query_texts=["when is the carry-over deadline"], n_results=5)
    print([m["document_type"] for m in unfiltered["metadatas"][0]])

    print("\n--- filtered to vacation_policy only ---")
    filtered = collection.query(
        query_texts=["when is the carry-over deadline"],
        n_results=5,
        where={"document_type": "vacation_policy"},
    )
    print([m["document_type"] for m in filtered["metadatas"][0]])
    print("\nThe filtered results should never include 'sick_leave_policy'.")
