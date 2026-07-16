def test_rag_pipeline(rag_pipeline):
    answer = rag_pipeline.ask(
        "Do employees continue to accrue vacation during maternity leave?"
    )
    assert "maternity" in answer.lower()
