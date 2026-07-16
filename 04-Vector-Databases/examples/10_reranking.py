"""
Example: 10_reranking.py

Take the fast, approximate top-N from vector search and re-score just
that small set with an LLM for better precision. Ties back to
docs/15-Reranking.md.

Run:
    ollama pull nomic-embed-text
    ollama pull llama3.1:8b
    python 10_reranking.py
"""

import chromadb
import requests
from chromadb import Documents, EmbeddingFunction, Embeddings
from openai import OpenAI


class OllamaEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model: str = "nomic-embed-text", url: str = "http://localhost:11434/api/embeddings"):
        self.model = model
        self.url = url

    def __call__(self, input: Documents) -> Embeddings:
        return [
            requests.post(self.url, json={"model": self.model, "prompt": text}).json()["embedding"]
            for text in input
        ]


client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


def llm_rerank(query: str, candidates: list[str], model: str = "llama3.1:8b") -> list[tuple[str, float]]:
    scored = []
    for doc in candidates:
        prompt = (
            f"Question: {query}\nPassage: {doc}\n\n"
            "On a scale of 0-10, how directly does this passage answer "
            "the question? Respond with only the number."
        )
        r = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}], temperature=0)
        try:
            score = float(r.choices[0].message.content.strip())
        except ValueError:
            score = 0.0
        scored.append((doc, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


if __name__ == "__main__":
    chroma_client = chromadb.PersistentClient(path="./chroma_rerank_demo")
    collection = chroma_client.get_or_create_collection(
        "rerank_demo", embedding_function=OllamaEmbeddingFunction(), metadata={"hnsw:space": "cosine"}
    )
    collection.upsert(
        ids=["d1", "d2", "d3"],
        documents=[
            "Vacation policies vary by employment type across the organization.",
            "Requests to carry over vacation must be submitted no later than November 1.",
            "The HR department handles all leave-related paperwork and approvals.",
        ],
    )

    query = "carry-over deadline"
    initial = collection.query(query_texts=[query], n_results=3)
    print("initial vector-search order:")
    for doc in initial["documents"][0]:
        print(f"  - {doc}")

    reranked = llm_rerank(query, initial["documents"][0])
    print("\nreranked order:")
    for doc, score in reranked:
        print(f"  [{score:4.1f}] {doc}")

    print("\nThe passage that actually states a deadline (mentions 'November 1')")
    print("should rank at or near the top after reranking.")
