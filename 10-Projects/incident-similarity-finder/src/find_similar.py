"""
find_similar.py

Given a new, in-progress incident description, find the most similar
past incidents by semantic meaning (not keyword match) and print their
resolutions. This is the core of the "Incident Similarity Finder"
project: pure retrieval, read-only, no agent loop and no destructive
tool calls - it only ever reads from the vector store.

Run:
    python src/index_incidents.py   # once, to build the collection
    python src/find_similar.py "checkout pods keep restarting after a deploy"
"""

import sys
from pathlib import Path

import chromadb

from index_incidents import DB_PATH, OllamaEmbeddingFunction


def find_similar(query: str, n_results: int = 3) -> None:
    client = chromadb.PersistentClient(path=str(DB_PATH))
    collection = client.get_collection(
        name="incidents",
        embedding_function=OllamaEmbeddingFunction(),
    )

    results = collection.query(query_texts=[query], n_results=n_results)

    print(f"Query: {query}\n")
    print(f"Top {n_results} similar past incidents:\n")

    for doc_id, meta, distance in zip(
        results["ids"][0], results["metadatas"][0], results["distances"][0]
    ):
        print(f"[{doc_id}] {meta['title']}  (service: {meta['service']}, distance={distance:.4f})")
        print(f"  Resolution: {meta['resolution']}")
        print()


if __name__ == "__main__":
    if not DB_PATH.exists():
        print("No collection found. Run 'python src/index_incidents.py' first.")
        sys.exit(1)

    query = " ".join(sys.argv[1:]) or "web pods returning 500 errors, no recent deploy"
    find_similar(query)
