"""
Example: 05_semantic_search.py

A complete semantic search engine from scratch - embed, store,
persist to disk, and search by cosine similarity. Ties back to
docs/09-Storing-Embeddings.md and
docs/10-Building-Semantic-Search-From-Scratch.md.

Run:
    ollama pull nomic-embed-text
    python 05_semantic_search.py
"""

import json
import os

import numpy as np
import requests

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL = "nomic-embed-text"
INDEX_PATH = "runbook_index.json"


def embed(text: str) -> list[float]:
    r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": text})
    return r.json()["embedding"]


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class SimpleSearchIndex:
    def __init__(self):
        self.entries: list[dict] = []

    def add(self, text: str, metadata: dict | None = None):
        self.entries.append({"text": text, "vector": embed(text), "metadata": metadata or {}})

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        query_vector = np.array(embed(query))
        scored = [
            {**e, "score": cosine_similarity(query_vector, np.array(e["vector"]))}
            for e in self.entries
        ]
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    def save(self, path: str):
        with open(path, "w") as f:
            json.dump(self.entries, f)

    def load(self, path: str):
        with open(path) as f:
            self.entries = json.load(f)


if __name__ == "__main__":
    index = SimpleSearchIndex()

    if os.path.exists(INDEX_PATH):
        print(f"Loading existing index from {INDEX_PATH} (skipping re-embedding)...")
        index.load(INDEX_PATH)
    else:
        print("Building a new index...")
        index.add("To debug CrashLoopBackOff, check kubectl describe pod and logs --previous.", {"source": "runbook-01.md"})
        index.add("When disk usage hits 90% on a primary DB, it's HIGH severity per SRE-042.", {"source": "runbook-02.md"})
        index.add("To roll back a failed deployment, run kubectl rollout undo deployment/<name>.", {"source": "runbook-03.md"})
        index.add("Best pizza toppings for a team lunch order.", {"source": "random-doc.md"})
        index.save(INDEX_PATH)
        print(f"Saved index to {INDEX_PATH}")

    query = "one of our pods keeps restarting, what do I check?"
    print(f"\nQuery: {query!r}\n")
    for r in index.search(query, top_k=2):
        print(f"[{r['score']:.3f}] {r['metadata']['source']}: {r['text']}")
