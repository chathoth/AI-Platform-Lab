"""
Example: 05_model_specs.py

Read every locally pulled model's real specs - architecture, context
length, quantization, capabilities - straight from the API. Ties back
to docs/03-The-Ollama-CLI.md and docs/07-Model-Formats-and-Quantization.md.

Run:
    python 05_model_specs.py
"""

import requests

BASE_URL = "http://localhost:11434"


def list_models() -> list[str]:
    return [m["name"] for m in requests.get(f"{BASE_URL}/api/tags").json()["models"]]


def show_model(name: str) -> dict:
    return requests.post(f"{BASE_URL}/api/show", json={"model": name}).json()


if __name__ == "__main__":
    for name in list_models():
        info = show_model(name)
        details = info.get("details", {})
        model_info = info.get("model_info", {})

        print(f"--- {name} ---")
        print(f"  family:        {details.get('family', '?')}")
        print(f"  parameters:    {details.get('parameter_size', '?')}")
        print(f"  quantization:  {details.get('quantization_level', '?')}")
        print(f"  capabilities:  {info.get('capabilities', [])}")
        print()
