"""
Example: 04_build_custom_model.py

Build a custom model from a Modelfile-equivalent config, entirely
through the API (no shelling out to the ollama CLI), confirm its
behavior actually differs from the base model, then clean up. Ties
back to docs/06-Modelfiles-Customizing-a-Model.md.

Run:
    ollama pull llama3.1:8b
    python 04_build_custom_model.py
"""

import requests

BASE_URL = "http://localhost:11434"
CUSTOM_MODEL_NAME = "terse-devops-example"


def create_model():
    response = requests.post(
        f"{BASE_URL}/api/create",
        json={
            "model": CUSTOM_MODEL_NAME,
            "from": "llama3.1:8b",
            "system": "You are a terse DevOps assistant. Answer in one sentence, no exceptions.",
            "parameters": {"temperature": 0},
        },
        stream=True,
    )
    for line in response.iter_lines():
        pass  # drain the stream of build status messages
    return response.status_code == 200


def ask(model: str, question: str) -> str:
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={"model": model, "messages": [{"role": "user", "content": question}], "stream": False},
    ).json()
    return response["message"]["content"]


def delete_model(model: str):
    requests.delete(f"{BASE_URL}/api/delete", json={"model": model})


if __name__ == "__main__":
    question = "What is a Kubernetes readiness probe?"

    print(f"Creating custom model '{CUSTOM_MODEL_NAME}'...")
    create_model()
    print("Done.\n")

    print("--- base model (no custom system prompt) ---")
    print(ask("llama3.1:8b", question))

    print(f"\n--- {CUSTOM_MODEL_NAME} (Modelfile-baked terse system prompt) ---")
    print(ask(CUSTOM_MODEL_NAME, question))

    print(f"\nCleaning up '{CUSTOM_MODEL_NAME}'...")
    delete_model(CUSTOM_MODEL_NAME)
    print("Done.")
