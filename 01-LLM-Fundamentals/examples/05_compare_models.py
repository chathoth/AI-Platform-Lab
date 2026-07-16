"""
Example: 05_compare_models.py

Same prompt, two different model sizes - compare answer quality,
latency, and rough resource footprint. Ties back to
docs/12-Model-Parameters.md and docs/15-Open-vs-Closed-Models.md.

Run:
    ollama pull llama3.2:1b
    ollama pull llama3.1:8b
    python 05_compare_models.py
"""

import time

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# A small model vs. a mid-size model - swap these for whatever you
# have pulled locally (e.g. add "llama3.1:70b" if your hardware can
# take it, per docs/12-Model-Parameters.md).
models = ["llama3.2:1b", "llama3.1:8b"]

prompt = "Explain what a container orchestrator does, in two sentences, for someone new to DevOps."


def ask(model: str) -> tuple[str, float]:
    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    latency = time.time() - start
    return response.choices[0].message.content.strip(), latency


if __name__ == "__main__":
    print(f"Prompt: {prompt}\n")

    for model in models:
        answer, latency = ask(model)
        print(f"--- {model} ---")
        print(f"Answer:  {answer}")
        print(f"Latency: {latency:.2f}s")
        print()

    print("A bigger model isn't automatically 'better' for a simple task")
    print("like this one - check whether the smaller, faster, cheaper")
    print("model already gets the job done before defaulting to the")
    print("largest model available (see docs/12-Model-Parameters.md).")
