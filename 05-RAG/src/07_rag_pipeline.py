"""
Step 7: Run the complete query-time RAG pipeline.

Query-time flow:
    question
      -> retrieve relevant chunks
      -> build grounded prompt
      -> invoke Ollama chat model
      -> display answer and sources
"""

from __future__ import annotations

import argparse
import time

from utils import RAGPipeline, format_source, settings


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    parser.add_argument("--top-k", type=int, default=settings.top_k)
    parser.add_argument(
        "--show-context",
        action="store_true",
        help="Print the retrieved chunks before generating the answer.",
    )
    return parser.parse_args()


def unique_sources(documents):
    seen = set()
    output = []
    for document in documents:
        source = format_source(document)
        if source not in seen:
            seen.add(source)
            output.append(source)
    return output


def main() -> None:
    args = parse_args()

    if not args.question.strip():
        raise ValueError("Question cannot be empty.")

    pipeline = RAGPipeline(top_k=args.top_k)

    if pipeline.vector_store._collection.count() == 0:
        raise RuntimeError(
            "The vector database is empty. Run steps 1-4 first."
        )

    retrieval_start = time.perf_counter()
    documents = pipeline.retrieve(args.question)
    retrieval_seconds = time.perf_counter() - retrieval_start

    if args.show_context:
        print("\nRetrieved context:")
        for index, document in enumerate(documents, start=1):
            print("\n" + "-" * 90)
            print(f"{index}. {format_source(document)}")
            print(document.page_content.strip())

    prompt = pipeline.build_prompt(args.question, documents)

    generation_start = time.perf_counter()
    response = pipeline.llm.invoke(prompt)
    generation_seconds = time.perf_counter() - generation_start

    print("\nQuestion:")
    print(args.question.strip())

    print("\nAnswer:")
    print(str(response.content).strip())

    print("\nSources:")
    for source in unique_sources(documents):
        print(f"- {source}")

    print("\nTiming:")
    print(f"- Retrieval: {retrieval_seconds:.3f} seconds")
    print(f"- Generation: {generation_seconds:.3f} seconds")


if __name__ == "__main__":
    main()
