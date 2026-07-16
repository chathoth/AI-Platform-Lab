import sys
from pathlib import Path

import pytest

# The numbered scripts in src/ are written to run standalone (each does
# `from utils import ...`, not `from src.utils import ...`) since they're
# meant to be run one at a time, e.g. `python 01_load_documents.py`.
# test_06_build_prompt.py loads one of those scripts directly via
# importlib, so `utils` needs to be importable by that bare name too -
# not just as the `src.utils` package the rest of the tests use.
SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

@pytest.fixture(scope="session")
def settings():
    from src.utils import settings
    return settings

@pytest.fixture(scope="session")
def vector_store(settings):
    """
    Build a real Chroma collection from sample-data once per test
    session. Chunk IDs are stable (see stable_chunk_id), so re-running
    the suite re-indexes the same chunks instead of duplicating them.
    """
    from src.utils import chunk_documents, get_vector_store, load_documents

    documents = load_documents(settings.sample_data_dir)
    chunks = chunk_documents(documents)

    store = get_vector_store()
    ids = [str(chunk.metadata["chunk_id"]) for chunk in chunks]
    store.add_documents(documents=chunks, ids=ids)
    return store

@pytest.fixture(scope="session")
def rag_pipeline(vector_store, settings):
    from src.utils import RAGPipeline

    return RAGPipeline(vector_store=vector_store, top_k=settings.top_k)
