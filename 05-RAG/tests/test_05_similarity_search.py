def test_similarity_search(vector_store):
    results = vector_store.similarity_search(
        "When must a carry-over request be submitted?", k=2
    )
    assert results
    assert any(doc.metadata.get("page")==2 for doc in results)
