"""
index_incidents.py

Loads data/incidents.json and embeds each incident into a local,
persistent Chroma collection using a local Ollama embedding model.
This is the same OllamaEmbeddingFunction + PersistentClient pattern
from module 04 (docs/05-Running-ChromaDB-Locally.md), applied here to
a real DevOps use case: making past incidents searchable by meaning,
not just by keyword.

Run:
    ollama pull nomic-embed-text
    pip install chromadb requests
    python src/index_incidents.py
"""

import json
from pathlib import Path

import chromadb
import requests
from chromadb import Documents, EmbeddingFunction, Embeddings

DATA_FILE = Path(__file__).parent.parent / "data" / "incidents.json"
DB_PATH = Path(__file__).parent.parent / "chroma_db"


class OllamaEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model: str = "nomic-embed-text", url: str = "http://localhost:11434/api/embeddings"):
        self.model = model
        self.url = url

    def __call__(self, input: Documents) -> Embeddings:
        return [
            requests.post(self.url, json={"model": self.model, "prompt": text}).json()["embedding"]
            for text in input
        ]


def build_searchable_text(incident: dict) -> str:
    """What actually gets embedded. Combines title, description, and
    root cause so a query about symptoms (title/description) can also
    match incidents by underlying cause (e.g. 'WAL segments')."""
    return f"{incident['title']}. {incident['description']} Root cause: {incident['root_cause']}"


def index_incidents() -> chromadb.Collection:
    incidents = json.loads(DATA_FILE.read_text())

    client = chromadb.PersistentClient(path=str(DB_PATH))
    collection = client.get_or_create_collection(
        name="incidents",
        embedding_function=OllamaEmbeddingFunction(),
        metadata={"hnsw:space": "cosine"},
    )

    collection.add(
        ids=[inc["id"] for inc in incidents],
        documents=[build_searchable_text(inc) for inc in incidents],
        metadatas=[
            {
                "title": inc["title"],
                "service": inc["service"],
                "resolution": inc["resolution"],
                "tags": ",".join(inc["tags"]),
            }
            for inc in incidents
        ],
    )

    return collection


if __name__ == "__main__":
    collection = index_incidents()
    print(f"Indexed {collection.count()} incidents into '{DB_PATH}'.")
