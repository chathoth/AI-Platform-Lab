"""
Example: 06_gpu_cpu_check.py

Check which processor a loaded model is actually running on, via the
API (the same data ollama ps shows). Ties back to
docs/09-GPU-vs-CPU-How-Ollama-Chooses.md.

Run:
    ollama pull llama3.1:8b
    python 06_gpu_cpu_check.py
"""

import requests

BASE_URL = "http://localhost:11434"


def loaded_models() -> list[dict]:
    return requests.get(f"{BASE_URL}/api/ps").json().get("models", [])


if __name__ == "__main__":
    # Make sure at least one model is actually loaded before checking.
    requests.post(f"{BASE_URL}/api/generate", json={"model": "llama3.1:8b", "prompt": "hi", "stream": False})

    models = loaded_models()
    if not models:
        print("No models currently loaded.")
    for model in models:
        size_vram = model.get("size_vram", 0)
        size_total = model.get("size", 1)
        gpu_percent = round((size_vram / size_total) * 100) if size_total else 0
        print(f"{model['name']}: {gpu_percent}% GPU, expires {model.get('expires_at', '?')}")

        if gpu_percent < 100:
            print("  -> not fully on GPU - generation will be slower than a full-GPU load (docs ch. 09)")
