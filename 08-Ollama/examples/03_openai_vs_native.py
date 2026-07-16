"""
Example: 03_openai_vs_native.py

Call the same model through both the OpenAI-compatible endpoint and
the native API, confirming they're two shapes over the same
underlying call. Ties back to
docs/05-The-OpenAI-Compatible-Endpoint.md.

Run:
    ollama pull llama3.1:8b
    pip install openai requests
    python 03_openai_vs_native.py
"""

import requests
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


def via_openai_compatible(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama3.1:8b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content


def via_native_api(prompt: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.1:8b",
            "messages": [{"role": "user", "content": prompt}],
            "options": {"temperature": 0},
            "stream": False,
        },
    ).json()
    return response["message"]["content"]


if __name__ == "__main__":
    prompt = "What is a Kubernetes readiness probe? One sentence."

    print("--- via OpenAI-compatible endpoint (/v1) ---")
    print(via_openai_compatible(prompt))

    print("\n--- via native API (/api/chat) ---")
    print(via_native_api(prompt))

    print()
    print("Both hit the same local Ollama server - two request/response")
    print("shapes over the same underlying model call, not two systems.")
