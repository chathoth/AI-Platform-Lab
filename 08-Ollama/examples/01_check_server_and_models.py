"""
Example: 01_check_server_and_models.py

Confirm Ollama is running and reachable, then list every locally
pulled model with its real specs. Ties back to
docs/02-Installing-and-Running-Ollama.md and
docs/03-The-Ollama-CLI.md.

Run:
    python 01_check_server_and_models.py
"""

import sys

import requests


def check_server(base_url: str = "http://localhost:11434") -> bool:
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False


def list_models(base_url: str = "http://localhost:11434") -> list[dict]:
    return requests.get(f"{base_url}/api/tags").json()["models"]


if __name__ == "__main__":
    if not check_server():
        print("Ollama is not reachable at localhost:11434.")
        print("Start it with 'ollama serve' (Linux) or open the Ollama app.")
        sys.exit(1)

    print("Ollama is running and reachable.\n")

    models = list_models()
    print(f"{len(models)} model(s) pulled locally:\n")
    for model in models:
        details = model["details"]
        size_gb = model["size"] / 1_000_000_000
        print(f"  {model['name']:<30} {size_gb:>6.2f} GB   quantization={details.get('quantization_level', '?')}")
