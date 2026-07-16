"""
Example: 06_cluster_incidents.py

Group a batch of incident titles into clusters with no labels given,
using k-means over their local embeddings. Ties back to
docs/12-Clustering-With-Embeddings.md.

Run:
    ollama pull nomic-embed-text
    pip install scikit-learn numpy
    python 06_cluster_incidents.py
"""

import numpy as np
import requests
from sklearn.cluster import KMeans

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL = "nomic-embed-text"


def embed(text: str) -> list[float]:
    r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": text})
    return r.json()["embedding"]


titles = [
    "checkout service returning 500s",
    "payment API throwing 500 errors",
    "disk full on db-primary-02",
    "database disk usage critical",
    "login page slow to load",
    "auth service high latency",
]

if __name__ == "__main__":
    vectors = np.array([embed(t) for t in titles])

    k = 3
    kmeans = KMeans(n_clusters=k, n_init="auto", random_state=42).fit(vectors)

    clusters: dict[int, list[str]] = {}
    for title, cluster_id in zip(titles, kmeans.labels_):
        clusters.setdefault(int(cluster_id), []).append(title)

    for cluster_id, cluster_titles in sorted(clusters.items()):
        print(f"Cluster {cluster_id}:")
        for t in cluster_titles:
            print(f"  - {t}")
        print()

    print(f"No labels were given - k-means (k={k}) found these groupings")
    print("purely from vector proximity in the embedding space.")
