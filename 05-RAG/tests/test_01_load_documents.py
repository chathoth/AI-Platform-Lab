from pathlib import Path
from src.utils import load_documents

def test_load_documents():
    docs = load_documents(Path("sample-data"))
    assert len(docs) == 6
    assert docs[0].metadata["source"] == "Vacation Time Policy.pdf"
    assert docs[0].metadata["page"] == 1
    assert len(docs[0].page_content) > 100
