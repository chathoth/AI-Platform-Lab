"""
Step 4: Store chunks in ChromaDB.

Input:
    artifacts/chunks.json

Output:
    chroma_db/

Learning objective:
    Understand persistent vector storage and stable document IDs.
"""

from __future__ import annotations

import argparse
import shutil

from utils import get_vector_store, load_documents_json, settings


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete the existing Chroma database before indexing.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.reset and settings.chroma_dir.exists():
        shutil.rmtree(settings.chroma_dir)
        settings.chroma_dir.mkdir(parents=True, exist_ok=True)
        print("Existing vector database deleted.")

    chunks = load_documents_json(settings.artifacts_dir / "chunks.json")
    vector_store = get_vector_store()

    ids = [str(chunk.metadata["chunk_id"]) for chunk in chunks]

    # Stable IDs make repeated indexing deterministic. Existing IDs are updated
    # rather than creating uncontrolled duplicates.
    vector_store.add_documents(
        documents=chunks,
        ids=ids,
    )

    count = vector_store._collection.count()

    print("\nStep 4 complete")
    print(f"Chunks submitted: {len(chunks)}")
    print(f"Collection: {settings.collection_name}")
    print(f"Total vectors in collection: {count}")
    print(f"Persistent database: {settings.chroma_dir}")


if __name__ == "__main__":
    main()
