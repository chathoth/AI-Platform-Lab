"""
Example: 01_generate_embedding.py

Generate your first embedding locally and inspect its shape. Ties
back to docs/01-What-Are-Embeddings.md and
docs/04-Vector-Space-and-Dimensionality.md.

Run:
    ollama pull nomic-embed-text
    pip install requests
    python 01_generate_embedding.py
"""

import requests

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL = "nomic-embed-text"


def embed(text: str) -> list[float]:
    response = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": text})
    response.raise_for_status()
    return response.json()["embedding"]


if __name__ == "__main__":
    text = "The pod is stuck in CrashLoopBackOff"
    vector = embed(text)

    print(f"Text: {text!r}")
    print(f"Vector length (dimensions): {len(vector)}")
    print(f"First 5 numbers: {vector[:5]}")
    print(f"Estimated bytes per vector: {len(vector) * 4}")

    # Determinism check - same input, same model, should give an
    # identical vector every time (no sampling/temperature involved).
    vector2 = embed(text)
    identical = vector == vector2
    print(f"\nSame input embedded twice - identical? {identical}")
