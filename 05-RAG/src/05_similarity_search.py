"""
Step 5: Retrieve chunks similar to a user question.

Input:
    chroma_db/

Output:
    ranked results printed to the terminal

Learning objective:
    Understand question embeddings, top-K retrieval, metadata, and scores.
"""

from __future__ import annotations

import argparse

from utils import get_vector_store, settings


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--question",
        required=True,
        help="Natural-language question to search for.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=settings.top_k,
        help="Number of chunks to retrieve.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    vector_store = get_vector_store()

    if vector_store._collection.count() == 0:
        raise RuntimeError(
            "The vector database is empty. Run 04_store_vectors.py first."
        )

    results = vector_store.similarity_search_with_score(
        args.question,
        k=args.top_k,
    )

    print("Step 5: similarity search")
    print(f"Question: {args.question}")
    print(f"Top K: {args.top_k}")
    print(
        "\nChroma returns a distance score. Lower distance generally means "
        "a closer match for this collection."
    )

    for rank, (document, score) in enumerate(results, start=1):
        print("\n" + "=" * 90)
        print(f"Rank: {rank}")
        print(f"Distance: {score:.6f}")
        print(
            f"Source: {document.metadata.get('source')} | "
            f"Page: {document.metadata.get('page')} | "
            f"Chunk: {document.metadata.get('chunk_index')}"
        )
        print("-" * 90)
        print(document.page_content.strip())


if __name__ == "__main__":
    main()
