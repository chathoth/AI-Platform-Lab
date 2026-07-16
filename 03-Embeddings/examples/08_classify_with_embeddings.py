"""
Example: 08_classify_with_embeddings.py

Classify alert severity by nearest-neighbor comparison against a
handful of labeled examples - no LLM call needed at inference time.
Ties back to docs/14-Classification-With-Embeddings.md.

Run:
    ollama pull nomic-embed-text
    python 08_classify_with_embeddings.py
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


labeled_examples = [
    ("CPU at 45% on web-node-01", "LOW"),
    ("Disk at 98% on db-primary-01, 5 minutes to full", "HIGH"),
    ("Memory at 78% on cache-node-03", "MEDIUM"),
    ("Disk at 90% on a replica node, 30 minutes to full", "MEDIUM"),
]


def build_labeled_vectors():
    return [(embed(text), label) for text, label in labeled_examples]


def classify(text: str, labeled_vectors: list) -> tuple[str, float]:
    query_vector = embed(text)
    best_label, best_score = None, -1.0
    for vector, label in labeled_vectors:
        score = cosine_similarity(query_vector, vector)
        if score > best_score:
            best_label, best_score = label, score
    return best_label, best_score


if __name__ == "__main__":
    print("Embedding labeled examples once...")
    labeled_vectors = build_labeled_vectors()

    test_alerts = [
        "Disk at 95%, 10 minutes to full on the primary",
        "CPU at 40% on a background worker node",
        "Memory at 82% on a replica cache node",
    ]

    for alert in test_alerts:
        label, confidence = classify(alert, labeled_vectors)
        print(f"[{label:>6} conf={confidence:.3f}] {alert}")

    print()
    print("No LLM call happened at classification time - each test")
    print("alert only needed ONE embedding call, then a comparison")
    print("against the 4 pre-embedded labeled examples.")
