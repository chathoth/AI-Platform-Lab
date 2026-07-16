"""
Example: 03_compare_temperature.py

Same prompt, three temperatures - watch determinism turn into
variation. Ties back to docs/10-Temperature-TopP-and-Sampling.md.

Run:
    ollama pull llama3.1:8b
    python 03_compare_temperature.py
"""

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

prompt = "Write a one-line git commit message for fixing a null pointer bug in the login service."

# 0.0 = deterministic (good for scripts/pipelines)
# 0.7 = balanced (good for a chat assistant)
# 1.3 = high randomness (good for brainstorming, bad for automation)
temperatures = [0.0, 0.7, 1.3]


def ask(temperature: float) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    for temperature in temperatures:
        print(f"--- temperature={temperature} ---")
        # Run it twice at the same temperature to show whether it's
        # actually deterministic or just "mostly stable".
        for run in range(2):
            print(f"  run {run + 1}: {ask(temperature)}")
        print()

    print("At temperature=0.0 the two runs should be identical (or very")
    print("close). By temperature=1.3 they'll usually differ. Pick low")
    print("temperature for anything a script depends on parsing.")
