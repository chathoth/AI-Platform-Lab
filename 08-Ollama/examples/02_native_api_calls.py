"""
Example: 02_native_api_calls.py

Call Ollama's three core native endpoints directly with requests -
no client library. Ties back to docs/04-The-Native-REST-API.md.

Run:
    ollama pull llama3.1:8b
    ollama pull nomic-embed-text
    python 02_native_api_calls.py
"""

import requests

BASE_URL = "http://localhost:11434"


def generate(prompt: str, model: str = "llama3.1:8b") -> dict:
    return requests.post(f"{BASE_URL}/api/generate", json={"model": model, "prompt": prompt, "stream": False}).json()


def chat(messages: list[dict], model: str = "llama3.1:8b") -> dict:
    return requests.post(f"{BASE_URL}/api/chat", json={"model": model, "messages": messages, "stream": False}).json()


def embed(text: str, model: str = "nomic-embed-text") -> dict:
    return requests.post(f"{BASE_URL}/api/embeddings", json={"model": model, "prompt": text}).json()


if __name__ == "__main__":
    print("--- /api/generate ---")
    result = generate("Say OK")
    print(f"response: {result['response']!r}")
    print(f"done_reason: {result['done_reason']}")

    print("\n--- /api/chat ---")
    result = chat([{"role": "user", "content": "Say OK"}])
    print(f"message: {result['message']}")
    print(f"load_duration: {result['load_duration'] / 1e9:.3f}s")
    print(f"eval_duration:  {result['eval_duration'] / 1e9:.3f}s ({result['eval_count']} tokens)")

    print("\n--- /api/embeddings ---")
    result = embed("test")
    print(f"embedding length: {len(result['embedding'])}")
