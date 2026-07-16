"""
Example: 04_clean_before_embedding.py

Compare embedding similarity for the same underlying log event, with
and without timestamp/ID noise stripped out. Ties back to
docs/08-Embedding-Different-Content-Types.md.

Run:
    ollama pull nomic-embed-text
    python 04_clean_before_embedding.py
"""

import re

import numpy as np
import requests

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL = "nomic-embed-text"


def embed(text: str) -> np.ndarray:
    r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": text})
    return np.array(r.json()["embedding"])


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def clean_log_line(line: str) -> str:
    # Strip ISO timestamps and bracketed pod/request IDs - high-
    # cardinality fields that add noise, not meaning.
    line = re.sub(r"\d{4}-\d{2}-\d{2}T[\d:.]+Z", "", line)
    line = re.sub(r"\[[a-zA-Z0-9\-]+\]", "", line)
    return line.strip()


if __name__ == "__main__":
    # Two log lines describing the exact same kind of event, but with
    # different timestamps and pod hashes.
    log1_raw = "2026-07-15T09:12:03.882Z [pod-7d9f4c8b6-x2k9p] ERROR CrashLoopBackOff exit=137"
    log2_raw = "2026-07-15T14:47:19.201Z [pod-a3f8e1c2d-m7q4r] ERROR CrashLoopBackOff exit=137"

    log1_clean = clean_log_line(log1_raw)
    log2_clean = clean_log_line(log2_raw)

    print(f"cleaned log 1: {log1_clean!r}")
    print(f"cleaned log 2: {log2_clean!r}\n")

    raw_similarity = cosine_similarity(embed(log1_raw), embed(log2_raw))
    clean_similarity = cosine_similarity(embed(log1_clean), embed(log2_clean))

    print(f"raw logs similarity:     {raw_similarity:.4f}")
    print(f"cleaned logs similarity: {clean_similarity:.4f}")
    print()
    print("The cleaned version should score closer to a perfect match -")
    print("the timestamp and pod ID noise measurably drags down")
    print("similarity for what is, semantically, the exact same event.")
