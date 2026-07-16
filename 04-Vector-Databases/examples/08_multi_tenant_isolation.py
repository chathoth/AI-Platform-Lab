"""
Example: 08_multi_tenant_isolation.py

Simulate a shared collection serving two tenants, with isolation
enforced through one centralized query function - never an ad hoc
filter at each call site. Ties back to
docs/12-Multi-Tenancy-and-Access-Control.md.

Run:
    ollama pull nomic-embed-text
    python 08_multi_tenant_isolation.py
"""

import chromadb
import requests
from chromadb import Documents, EmbeddingFunction, Embeddings


class OllamaEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model: str = "nomic-embed-text", url: str = "http://localhost:11434/api/embeddings"):
        self.model = model
        self.url = url

    def __call__(self, input: Documents) -> Embeddings:
        return [
            requests.post(self.url, json={"model": self.model, "prompt": text}).json()["embedding"]
            for text in input
        ]


def tenant_scoped_query(collection, tenant_id: str, query_text: str, n_results: int = 5):
    # The ENTIRE isolation boundary lives here. Every caller must go
    # through this function - never call collection.query() directly
    # with a hand-rolled filter at the call site (docs ch. 12).
    return collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where={"tenant_id": tenant_id},
    )


if __name__ == "__main__":
    client = chromadb.PersistentClient(path="./chroma_tenant_demo")
    collection = client.get_or_create_collection(
        "shared_demo", embedding_function=OllamaEmbeddingFunction(), metadata={"hnsw:space": "cosine"}
    )
    collection.upsert(
        ids=["t1-doc1", "t2-doc1"],
        documents=[
            "Tenant A's internal deployment runbook and escalation contacts.",
            "Tenant B's internal deployment runbook and escalation contacts.",
        ],
        metadatas=[{"tenant_id": "tenant-a"}, {"tenant_id": "tenant-b"}],
    )

    result_a = tenant_scoped_query(collection, "tenant-a", "deployment runbook")
    print("Tenant A's results:", result_a["documents"][0])
    print("Tenant A's result metadata:", result_a["metadatas"][0])

    result_b = tenant_scoped_query(collection, "tenant-b", "deployment runbook")
    print("\nTenant B's results:", result_b["documents"][0])
    print("Tenant B's result metadata:", result_b["metadatas"][0])

    print("\nEvery result's tenant_id should match the tenant that queried it -")
    print("that's the isolation boundary being enforced correctly.")
