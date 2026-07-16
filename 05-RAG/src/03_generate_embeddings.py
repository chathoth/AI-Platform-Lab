"""
Step 3: Generate embeddings for document chunks.

Input:
    artifacts/chunks.json

Output:
    artifacts/embeddings.json

Learning objective:
    See how text is converted into numeric vectors.

Note:
    This script stores vectors in JSON only for learning and inspection.
    In production, vectors are normally written directly to a vector database.
"""

from __future__ import annotations

import json
from math import sqrt

from utils import generate_embeddings, load_documents_json, settings


def vector_norm(vector: list[float]) -> float:
    return sqrt(sum(value * value for value in vector))


def main() -> None:
    chunks_path = settings.artifacts_dir / "chunks.json"
    output_path = settings.artifacts_dir / "embeddings.json"

    chunks = load_documents_json(chunks_path)
    texts = [chunk.page_content for chunk in chunks]

    print(f"Generating embeddings for {len(texts)} chunks...")
    print(f"Embedding model: {settings.embedding_model}")

    vectors = generate_embeddings(texts)

    payload = []
    for chunk, vector in zip(chunks, vectors):
        payload.append(
            {
                "chunk_id": chunk.metadata["chunk_id"],
                "source": chunk.metadata.get("source"),
                "page": chunk.metadata.get("page"),
                "dimensions": len(vector),
                "vector_norm": vector_norm(vector),
                "embedding": vector,
            }
        )

    output_path.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )

    print("\nStep 3 complete")
    print(f"Vectors generated: {len(vectors)}")
    print(f"Embedding dimensions: {len(vectors[0]) if vectors else 0}")
    print(f"Saved output: {output_path}")

    if vectors:
        print("\nFirst 10 values of the first embedding:")
        print(vectors[0][:10])


if __name__ == "__main__":
    main()
