"""
Example: 09_hybrid_search.py

Blend semantic (embedding) search with keyword overlap so an exact
error code isn't missed just because it's not conceptually
distinctive. Ties back to docs/15-Hybrid-Search.md.

Run:
    ollama pull nomic-embed-text
    python 09_hybrid_search.py
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


def keyword_score(query: str, text: str) -> float:
    query_words = set(query.lower().split())
    text_words = set(text.lower().split())
    if not query_words:
        return 0.0
    return len(query_words & text_words) / len(query_words)


def hybrid_search(query: str, index: list[dict], top_k: int = 3, semantic_weight: float = 0.5) -> list[dict]:
    query_vector = embed(query)
    scored = []
    for entry in index:
        semantic = cosine_similarity(query_vector, np.array(entry["vector"]))
        keyword = keyword_score(query, entry["text"])
        combined = semantic_weight * semantic + (1 - semantic_weight) * keyword
        scored.append({**entry, "score": combined, "semantic": semantic, "keyword": keyword})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    documents = [
        "Common causes of database connection issues include pool exhaustion and network partitions.",
        "Error E4021 occurs when the connection pool hits its configured max size.",
        "To roll back a failed deployment, use kubectl rollout undo.",
    ]
    index = [{"text": d, "vector": embed(d)} for d in documents]

    query = "what causes error E4021"

    print("--- pure semantic search (semantic_weight=1.0) ---")
    for r in hybrid_search(query, index, semantic_weight=1.0):
        print(f"  score={r['score']:.3f}: {r['text'][:70]}")

    print("\n--- hybrid search (semantic_weight=0.5) ---")
    for r in hybrid_search(query, index, semantic_weight=0.5):
        print(f"  combined={r['score']:.3f} semantic={r['semantic']:.3f} keyword={r['keyword']:.3f}: {r['text'][:70]}")

    print()
    print("Check whether the document literally containing 'E4021' ranks")
    print("more reliably at #1 once keyword score is factored in.")
