from src.utils import generate_embeddings

def test_generate_embeddings():
    embeddings = generate_embeddings(["Example chunk"])
    assert len(embeddings) == 1
    assert len(embeddings[0]) > 300
