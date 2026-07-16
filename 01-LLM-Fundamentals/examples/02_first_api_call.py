"""
Example: 02_first_api_call.py

The simplest possible LLM call - send a prompt, get a response, time it.
Ties back to docs/01-What-is-an-LLM.md and docs/03-How-LLMs-Work.md.

Runs against a LOCAL Ollama model by default, so there's no API key
and no cost to experiment with. See the "Switch to a hosted API"
comment at the bottom to point this at OpenAI/Claude instead.

Run:
    ollama pull llama3.1:8b
    pip install openai
    python 02_first_api_call.py
"""

import time

from openai import OpenAI

# Ollama exposes an OpenAI-compatible endpoint, so the same `openai`
# SDK works locally - just point base_url at it. api_key is required
# by the SDK but Ollama ignores its value.
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

prompt = "In one sentence, explain what a Kubernetes Deployment is."

if __name__ == "__main__":
    start = time.time()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )

    latency = time.time() - start
    answer = response.choices[0].message.content

    print(f"Prompt:   {prompt}")
    print(f"Answer:   {answer}")
    print(f"Latency:  {latency:.2f}s")
    print(f"Tokens:   {response.usage.prompt_tokens} in / "
          f"{response.usage.completion_tokens} out")

# --- Switch to a hosted API (OpenAI) ---
# client = OpenAI()  # reads OPENAI_API_KEY from your environment
# MODEL = "gpt-4o-mini"
