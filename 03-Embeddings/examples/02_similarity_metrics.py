"""
Example: 02_similarity_metrics.py

Compare cosine similarity, dot product, and Euclidean distance on the
same pair of related and unrelated texts. Ties back to
docs/05-Similarity-Metrics.md.

Run:
    ollama pull nomic-embed-text
    pip install requests numpy
    python 02_similarity_metrics.py
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


def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))


def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


if __name__ == "__main__":
    related_a = embed("The pod is stuck in CrashLoopBackOff")
    related_b = embed("Container keeps restarting and failing health checks")
    unrelated = embed("Best pizza toppings for a party")

    for label, a, b in [
        ("related pair", related_a, related_b),
        ("unrelated pair", related_a, unrelated),
    ]:
        print(f"--- {label} ---")
        print(f"  cosine similarity:  {cosine_similarity(a, b):.4f}  (higher = more similar)")
        print(f"  dot product:        {dot_product(a, b):.4f}")
        print(f"  euclidean distance: {euclidean_distance(a, b):.4f}  (lower = more similar)")
        print()

    print("Cosine similarity is usually the easiest to interpret at a")
    print("glance: closer to 1 means more related, regardless of how")
    print("long either piece of text is.")
