"""
Example: 10_eval_prompt_variants.py

Score two prompt variants against a small labeled eval set instead of
judging "which looks better" by eye. Ties back to
docs/16-Evaluating-Prompt-Quality.md.

Run:
    ollama pull llama3.1:8b
    python 10_eval_prompt_variants.py
"""

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

# Deliberately includes the tricky primary-vs-replica case from
# 01_zero_shot_vs_few_shot.py - eval sets should include the edge
# cases that made the prompt hard to write in the first place.
eval_set = [
    {"input": "CPU at 45% on web-node-01", "expected": "LOW"},
    {"input": "Disk at 98% on db-primary-01, 5 minutes to full", "expected": "HIGH"},
    {"input": "Memory at 78% on cache-node-03", "expected": "MEDIUM"},
    {"input": "Disk at 92% on a REPLICA db node", "expected": "MEDIUM"},
    {"input": "5xx error rate at 0.01%", "expected": "LOW"},
]

# v1: no domain knowledge given
v1 = "Classify severity as LOW, MEDIUM, or HIGH: {alert}"

# v2: encodes the primary/replica convention explicitly
v2 = (
    "You are an SRE. Classify severity as LOW, MEDIUM, or HIGH. "
    "Disk >90% on a PRIMARY is HIGH; on a REPLICA is MEDIUM.\n"
    "Alert: {alert}"
)


def evaluate_prompt(prompt_template: str, eval_set: list) -> tuple[float, list]:
    correct = 0
    failures = []
    for case in eval_set:
        prompt = prompt_template.format(alert=case["input"])
        r = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        answer = r.choices[0].message.content.strip().upper()
        if case["expected"] in answer:
            correct += 1
        else:
            failures.append((case["input"], case["expected"], answer))
    return correct / len(eval_set), failures


if __name__ == "__main__":
    for label, template in [("v1", v1), ("v2", v2)]:
        accuracy, failures = evaluate_prompt(template, eval_set)
        print(f"{label}: {accuracy:.0%} accuracy")
        for input_text, expected, got in failures:
            print(f"  MISS: '{input_text}' expected {expected}, got '{got}'")
        print()

    print("v2 should score higher specifically on the replica case -")
    print("that's a measurable, not just a felt, improvement.")
