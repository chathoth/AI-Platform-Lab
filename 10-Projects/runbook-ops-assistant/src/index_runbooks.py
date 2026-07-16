"""
index_runbooks.py

Embeds each runbook in data/runbooks/ into a local, persistent Chroma
collection, using the same OllamaEmbeddingFunction pattern as module
04 and as ../incident-similarity-finder/src/index_incidents.py. This
is the RAG half of this project - the agent (agent.py) retrieves the
most relevant runbook for a request before deciding what to do.

Run:
    ollama pull nomic-embed-text
    pip install chromadb requests
    python src/index_runbooks.py
"""

from pathlib import Path

import chromadb
import requests
from chromadb import Documents, EmbeddingFunction, Embeddings

RUNBOOKS_DIR = Path(__file__).parent.parent / "data" / "runbooks"
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


def index_runbooks() -> chromadb.Collection:
    files = sorted(RUNBOOKS_DIR.glob("*.md"))

    client = chromadb.PersistentClient(path=str(DB_PATH))
    collection = client.get_or_create_collection(
        name="runbooks",
        embedding_function=OllamaEmbeddingFunction(),
        metadata={"hnsw:space": "cosine"},
    )

    collection.add(
        ids=[f.stem for f in files],
        documents=[f.read_text() for f in files],
        metadatas=[{"source": f.name} for f in files],
    )

    return collection


if __name__ == "__main__":
    collection = index_runbooks()
    print(f"Indexed {collection.count()} runbooks into '{DB_PATH}'.")
