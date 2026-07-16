"""
Example: 07_context_window_memory.py

Measure the real memory cost of a larger num_ctx, for the exact same
short prompt. Ties back to docs/10-Context-Length-and-Memory.md.

Run:
    ollama pull llama3.1:8b
    python 07_context_window_memory.py
"""

import requests

BASE_URL = "http://localhost:11434"
MODEL = "llama3.1:8b"


def load_with_context(num_ctx: int) -> dict:
    requests.post(f"{BASE_URL}/api/generate", json={"model": MODEL, "keep_alive": 0})  # unload first, if loaded
    requests.post(
        f"{BASE_URL}/api/generate",
        json={"model": MODEL, "prompt": "hi", "options": {"num_ctx": num_ctx}, "stream": False},
    )
    models = requests.get(f"{BASE_URL}/api/ps").json()["models"]
    return next(m for m in models if m["name"] == MODEL)


if __name__ == "__main__":
    for num_ctx in [4096, 32768]:
        info = load_with_context(num_ctx)
        size_gb = info["size"] / 1_000_000_000
        print(f"num_ctx={num_ctx:>6}: reported size = {size_gb:.2f} GB, active context = {info['context_length']}")

    print()
    print("A larger num_ctx should show up as a measurably larger reported")
    print("size, even though every request here used the identical short")
    print("prompt 'hi' - the memory cost is for the RESERVED window, not")
    print("the actual content sent.")
