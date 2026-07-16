"""
Step 1: Load PDF documents.

Input:
    sample-data/*.pdf

Output:
    artifacts/loaded_documents.json

Learning objective:
    Understand how source files become LangChain Document objects.
"""

from __future__ import annotations

from utils import discover_pdf_files, load_documents, save_documents, settings


def main() -> None:
    pdf_files = discover_pdf_files(settings.sample_data_dir)

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files were found in {settings.sample_data_dir}"
        )

    print("Discovered PDF files:")
    for pdf_file in pdf_files:
        print(f"  - {pdf_file.name}")

    all_documents = load_documents(settings.sample_data_dir)

    output = settings.artifacts_dir / "loaded_documents.json"
    save_documents(all_documents, output)

    print("\nStep 1 complete")
    print(f"Total page documents: {len(all_documents)}")
    print(f"Saved output: {output}")

    print("\nFirst loaded document preview:")
    first = all_documents[0]
    print(f"Metadata: {first.metadata}")
    print(first.page_content[:500].strip())


if __name__ == "__main__":
    main()
