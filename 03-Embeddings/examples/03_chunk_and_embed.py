"""
Example: 03_chunk_and_embed.py

Split a runbook into chunks with and without overlap, then embed each
chunk and show how overlap keeps boundary content intact. Ties back
to docs/07-Chunking-Before-Embedding.md.

Run:
    ollama pull nomic-embed-text
    python 03_chunk_and_embed.py
"""

import requests

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL = "nomic-embed-text"

runbook = """To debug CrashLoopBackOff:
1. Run kubectl describe pod to see recent events.
2. Check kubectl logs --previous for the crash reason.
3. Common causes: OOMKilled, a failed liveness probe, or a bad image.
4. If memory-related, correlate with the metrics dashboard before
   raising limits blindly - it may be a real leak."""


def chunk_fixed(text: str, chunk_size: int = 120, overlap: int = 0) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def embed(text: str) -> list[float]:
    r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": text})
    return r.json()["embedding"]


if __name__ == "__main__":
    no_overlap = chunk_fixed(runbook, chunk_size=120, overlap=0)
    with_overlap = chunk_fixed(runbook, chunk_size=120, overlap=25)

    for label, chunks in [("no overlap", no_overlap), ("with overlap", with_overlap)]:
        print(f"--- {label} ({len(chunks)} chunks) ---")
        for i, c in enumerate(chunks):
            print(f"  chunk {i}: {c!r}")
        print()

    print("Look for a chunk boundary in 'no overlap' that cuts a")
    print("numbered step or sentence in half - then check whether")
    print("'with overlap' keeps that same content intact in at least")
    print("one chunk.")
    print()

    # Embed each chunk from the overlapping version - this is what
    # would actually get stored in a real search index (chapter 09).
    print("Embedding each chunk from the overlapping version...")
    for i, c in enumerate(with_overlap):
        vector = embed(c)
        print(f"  chunk {i}: {len(vector)}-dim vector")
