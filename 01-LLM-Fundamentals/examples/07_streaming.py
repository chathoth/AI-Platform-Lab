"""
Example: 07_streaming.py

Stream a response token by token instead of waiting for the whole
thing, and measure time-to-first-token (TTFT) separately from total
generation time. Ties back to docs/03-How-LLMs-Work.md (generation is
a loop, not a single call).

Run:
    ollama pull llama3.1:8b
    python 07_streaming.py
"""

import time

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

prompt = "List 5 benefits of using Infrastructure as Code."

if __name__ == "__main__":
    start = time.time()
    first_token_time = None
    full_response = ""

    stream = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    print("Streaming response:\n")
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            if first_token_time is None:
                first_token_time = time.time()
            print(delta, end="", flush=True)
            full_response += delta

    total_time = time.time() - start
    ttft = first_token_time - start if first_token_time else None

    print("\n")
    print(f"Time to first token: {ttft:.2f}s")
    print(f"Total generation time: {total_time:.2f}s")
    print(f"Response length: {len(full_response)} characters")
    print()
    print("TTFT is what a user actually perceives as 'is this thing")
    print("responding'. Total time is what your infra bill cares about.")
    print("They're different numbers for a reason - see")
    print("docs/03-How-LLMs-Work.md.")
