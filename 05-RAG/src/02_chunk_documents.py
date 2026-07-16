"""
Step 2: Split loaded pages into overlapping chunks.

Input:
    artifacts/loaded_documents.json

Output:
    artifacts/chunks.json

Learning objective:
    Understand chunk size, overlap, metadata preservation, and chunk IDs.
"""

from __future__ import annotations

from utils import chunk_documents, load_documents_json, save_documents, settings


def main() -> None:
    input_path = settings.artifacts_dir / "loaded_documents.json"
    output_path = settings.artifacts_dir / "chunks.json"

    documents = load_documents_json(input_path)
    chunks = chunk_documents(documents)
    save_documents(chunks, output_path)

    print("Step 2 complete")
    print(f"Input page documents: {len(documents)}")
    print(f"Output chunks: {len(chunks)}")
    print(f"Chunk size: {settings.chunk_size}")
    print(f"Chunk overlap: {settings.chunk_overlap}")
    print(f"Saved output: {output_path}")

    print("\nFirst three chunks:")
    for chunk in chunks[:3]:
        print("-" * 80)
        print(
            f"source={chunk.metadata.get('source')} "
            f"page={chunk.metadata.get('page')} "
            f"characters={chunk.metadata.get('character_count')}"
        )
        print(chunk.page_content[:500].strip())


if __name__ == "__main__":
    main()
