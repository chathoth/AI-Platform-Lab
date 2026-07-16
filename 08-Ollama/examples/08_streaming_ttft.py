"""
Example: 08_streaming_ttft.py

Consume a raw streamed response and measure time-to-first-token
separately from total generation time. Ties back to
docs/13-Streaming-Responses.md.

Run:
    ollama pull llama3.1:8b
    python 08_streaming_ttft.py
"""

import json
import time

import requests

BASE_URL = "http://localhost:11434"
MODEL = "llama3.1:8b"


def stream_and_measure(prompt: str) -> tuple[str, float, float]:
    start = time.time()
    first_token_time = None
    full_text = ""

    response = requests.post(
        f"{BASE_URL}/api/generate",
        json={"model": MODEL, "prompt": prompt, "stream": True},
        stream=True,
    )

    for line in response.iter_lines():
        if not line:
            continue
        chunk = json.loads(line)
        if first_token_time is None and chunk.get("response"):
            first_token_time = time.time()
        full_text += chunk.get("response", "")
        if chunk.get("done"):
            break

    total_time = time.time() - start
    ttft = (first_token_time - start) if first_token_time else total_time
    return full_text, ttft, total_time


if __name__ == "__main__":
    text, ttft, total = stream_and_measure("List 5 benefits of Infrastructure as Code.")

    print(f"Time to first token: {ttft:.2f}s")
    print(f"Total generation time: {total:.2f}s")
    print(f"Response length: {len(text)} characters")
    print()
    print("TTFT is what a user perceives as 'is this responding at all' -")
    print("total time is what your infra cost actually depends on. They're")
    print("different numbers for a reason.")
