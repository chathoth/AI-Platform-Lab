"""
Example: 07_find_duplicates.py

Find near-duplicate tickets that share no exact words, using
similarity above a tuned threshold. Ties back to
docs/13-Deduplication-With-Embeddings.md.

Run:
    ollama pull nomic-embed-text
    python 07_find_duplicates.py
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


def find_near_duplicates(texts: list[str], threshold: float = 0.85) -> list[tuple]:
    vectors = [embed(t) for t in texts]
    duplicates = []
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            score = cosine_similarity(vectors[i], vectors[j])
            if score >= threshold:
                duplicates.append((texts[i], texts[j], score))
    return duplicates


if __name__ == "__main__":
    tickets = [
        "Disk usage critical on db-primary-02",
        "db-primary-02 is almost out of disk space",
        "Checkout service returning 500 errors",
        "Login page is loading slowly for some users",
        "payment service throwing intermittent 500s",
    ]

    print("Candidates found (NOT auto-merged - flagged for review):\n")
    for a, b, score in find_near_duplicates(tickets, threshold=0.80):
        print(f"[{score:.3f}] possible duplicate:")
        print(f"  A: {a}")
        print(f"  B: {b}\n")

    print("Try lowering the threshold in find_near_duplicates() and")
    print("watch when unrelated-but-topically-similar tickets (like the")
    print("checkout/payment pair) start getting flagged too - that's")
    print("the precision/recall trade-off from the chapter, made real.")
