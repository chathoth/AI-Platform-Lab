"""
Example: 10_evaluate_search.py

Score a search index against a labeled eval set using recall@k,
instead of judging quality by eye. Ties back to
docs/16-Evaluating-Embedding-Quality.md.

Run:
    ollama pull nomic-embed-text
    python 10_evaluate_search.py
"""

import numpy as np
import requests

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL = "nomic-embed-text"


def embed(text: str) -> np.ndarray:
    r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": text})
    return np.array(r.json()["embedding"])


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class SimpleSearchIndex:
    def __init__(self):
        self.entries: list[dict] = []

    def add(self, text: str, metadata: dict):
        self.entries.append({"text": text, "vector": embed(text), "metadata": metadata})

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        query_vector = embed(query)
        scored = [
            {**e, "score": cosine_similarity(query_vector, np.array(e["vector"]))}
            for e in self.entries
        ]
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]


def recall_at_k(index: SimpleSearchIndex, eval_set: list[dict], k: int = 3) -> tuple[float, list]:
    hits = 0
    misses = []
    for case in eval_set:
        results = index.search(case["query"], top_k=k)
        sources = [r["metadata"]["source"] for r in results]
        if case["expected_source"] in sources:
            hits += 1
        else:
            misses.append(case["query"])
    return hits / len(eval_set), misses


if __name__ == "__main__":
    index = SimpleSearchIndex()
    index.add("To debug CrashLoopBackOff, check kubectl describe pod and logs --previous.", {"source": "runbook-crashloop.md"})
    index.add("When disk usage hits 90% on a primary DB, it's HIGH severity per SRE-042.", {"source": "runbook-disk.md"})
    index.add("To roll back a failed deployment, run kubectl rollout undo deployment/<name>.", {"source": "runbook-rollback.md"})

    # Deliberately phrased differently than the source text - the
    # tricky cases a real eval set should include.
    eval_set = [
        {"query": "how do I restart a stuck pod?", "expected_source": "runbook-crashloop.md"},
        {"query": "what happens when disk is full on the primary db?", "expected_source": "runbook-disk.md"},
        {"query": "how do I undo a bad deployment?", "expected_source": "runbook-rollback.md"},
    ]

    for k in [1, 2, 3]:
        score, misses = recall_at_k(index, eval_set, k=k)
        print(f"recall@{k}: {score:.0%}" + (f"  (missed: {misses})" if misses else ""))
