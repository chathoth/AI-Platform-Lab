"""
Example: 02_chain_of_thought.py

Compare a direct answer against a chain-of-thought answer on a small
multi-step reasoning problem. Ties back to docs/04-Chain-of-Thought.md.

Run:
    ollama pull llama3.1:8b
    python 02_chain_of_thought.py
"""

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

# Correct answer, worked by hand: 5 batches * 60s wait + 1 * 30s
# readiness delay = 330s. A good test case because it's easy for a
# model to skip a step and land on a plausible-but-wrong number.
problem = (
    "A rolling deploy replaces 10 pods, 2 at a time, waiting 60 seconds "
    "between batches, with a 30 second readiness probe delay before "
    "the first batch is considered healthy. How many seconds, at "
    "minimum, before all 10 pods are updated?"
)

direct_prompt = f"{problem} Answer with just the number of seconds."

cot_prompt = (
    f"{problem} Think through this step by step - how many batches, "
    "how long each wait is, and the initial readiness delay - then "
    "give the final answer on the last line as 'Answer: N seconds'."
)


def ask(prompt: str) -> str:
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return r.choices[0].message.content.strip()


if __name__ == "__main__":
    print("--- direct answer ---")
    print(ask(direct_prompt))
    print()
    print("--- chain-of-thought ---")
    print(ask(cot_prompt))
    print()
    print("Worked by hand: 5 batches x 60s + 30s readiness delay = 330s.")
    print("Check which answer above actually landed on 330.")
