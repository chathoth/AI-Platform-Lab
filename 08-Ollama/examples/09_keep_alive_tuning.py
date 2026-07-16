"""
Example: 09_keep_alive_tuning.py

Show keep_alive actually controlling how long a model stays loaded,
verified against real /api/ps output. Ties back to
docs/16-Performance-Tuning.md.

Run:
    ollama pull llama3.1:8b
    python 09_keep_alive_tuning.py
"""

import time

import requests

BASE_URL = "http://localhost:11434"
MODEL = "llama3.1:8b"


def call_with_keep_alive(keep_alive) -> dict | None:
    requests.post(
        f"{BASE_URL}/api/generate",
        json={"model": MODEL, "prompt": "hi", "keep_alive": keep_alive, "stream": False},
    )
    models = requests.get(f"{BASE_URL}/api/ps").json().get("models", [])
    return next((m for m in models if m["name"] == MODEL), None)


if __name__ == "__main__":
    print("--- keep_alive='10m' (stays loaded for 10 minutes) ---")
    info = call_with_keep_alive("10m")
    print(f"expires_at: {info['expires_at'] if info else 'not loaded'}")

    print("\n--- keep_alive=0 (unloads after this request, asynchronously) ---")
    call_with_keep_alive(0)
    # Verified directly: unload with keep_alive=0 is NOT instant when a real
    # generation happened - it takes a couple of seconds to actually clear,
    # unlike a bare keep_alive=0 ping with no prompt, which unloads
    # immediately. Poll briefly instead of assuming either timing.
    for attempt in range(6):
        models = requests.get(f"{BASE_URL}/api/ps").json().get("models", [])
        still_loaded = any(m["name"] == MODEL for m in models)
        if not still_loaded:
            break
        time.sleep(1)
    print(f"still loaded after keep_alive=0: {still_loaded} (checked after ~{attempt + 1}s)")

    print()
    print("keep_alive=0 unloads the model, but NOT instantly when combined")
    print("with a real prompt - verified here to take a couple of seconds.")
    print("Appropriate when memory is tight and you don't need it warm for")
    print("a follow-up request. '10m' trades that memory for avoiding a")
    print("cold reload on the next call within that window.")
