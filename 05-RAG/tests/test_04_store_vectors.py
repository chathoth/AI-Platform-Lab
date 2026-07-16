from src.utils import get_vector_store

def test_store_vectors():
    store = get_vector_store()
    assert store is not None
