from src.utils import load_documents, chunk_documents
from pathlib import Path

def test_chunk_documents():
    docs = load_documents(Path("sample-data"))
    chunks = chunk_documents(docs)
    assert len(chunks) > len(docs)
    assert chunks[0].metadata["page"] == 1
    assert len(chunks[0].page_content) > 0
