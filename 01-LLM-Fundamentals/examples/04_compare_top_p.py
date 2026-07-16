"""
Example: 04_compare_top_p.py

Same prompt, three top_p values - a different way to control
randomness than temperature. Ties back to
docs/10-Temperature-TopP-and-Sampling.md.

Run:
    ollama pull llama3.1:8b
    python 04_compare_top_p.py
"""

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

prompt = "Suggest a name for an internal CLI tool that wraps kubectl and adds guardrails."

# top_p keeps only the smallest set of tokens whose combined probability
# crosses this threshold, then samples from that set.
# Low top_p = narrow, safe word choices. High top_p = wider variety.
top_p_values = [0.1, 0.5, 1.0]


def ask(top_p: float) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0,  # keep temperature fixed so top_p is the only variable
        top_p=top_p,
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    for top_p in top_p_values:
        print(f"--- top_p={top_p} ---")
        print(ask(top_p))
        print()

    print("Notice low top_p tends to produce the same 'obvious' answer")
    print("repeatedly, while top_p=1.0 allows lower-probability, more")
    print("unusual word choices into the sampling pool.")
