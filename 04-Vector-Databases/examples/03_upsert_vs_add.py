"""
Example: 03_upsert_vs_add.py

Show what add() actually does on a duplicate ID (verified: it's a
SILENT no-op in current ChromaDB, not an error - a more dangerous
failure mode than a loud exception), and compare it against upsert(),
which actually replaces the record. Ties back to
docs/06-Inserting-and-Updating-Vectors.md.

Run:
    ollama pull nomic-embed-text
    python 03_upsert_vs_add.py
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
    client = chromadb.PersistentClient(path="./chroma_upsert_demo")
    collection = client.get_or_create_collection(
        "upsert_demo", embedding_function=OllamaEmbeddingFunction(), metadata={"hnsw:space": "cosine"}
    )
    # start clean so this script is safe to re-run
    existing = collection.get(ids=["x1"])
    if existing["ids"]:
        collection.delete(ids=["x1"])

    collection.add(ids=["x1"], documents=["original version of the text"])
    print("Added x1 successfully.")

    # This does NOT raise in current ChromaDB - it's a silent no-op.
    # That's worth seeing directly: no exception, but also no change.
    collection.add(ids=["x1"], documents=["trying to add the same ID again"])
    after_duplicate_add = collection.get(ids=["x1"])["documents"]
    print(f"After a duplicate add() (no error raised): {after_duplicate_add}")
    print("  -> notice it's still the ORIGINAL text - add() silently did nothing.")

    collection.upsert(ids=["x1"], documents=["updated via upsert - actually changes the record"])
    after_upsert = collection.get(ids=["x1"])["documents"]
    print(f"\nAfter upsert(): {after_upsert}")
    print("  -> this one actually changed the stored content.")

    print(f"\nCollection count (should still be 1 throughout): {collection.count()}")
    print()
    print("Lesson: add()'s silent-ignore behavior on a duplicate ID is more")
    print("dangerous than an error would be - a re-run ingestion script using")
    print("add() can look successful while quietly failing to apply updates.")
