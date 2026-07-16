"""
Example: 01_zero_shot_vs_few_shot.py

Classify the same alerts two ways - with no examples (zero-shot) and
with a handful of labeled examples (few-shot) - and compare how each
handles a genuinely ambiguous case. Ties back to
docs/03-Zero-Shot-vs-Few-Shot.md.

Run:
    ollama pull llama3.1:8b
    pip install openai
    python 01_zero_shot_vs_few_shot.py
"""

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

# The tricky one: severity depends on whether it's a primary or replica -
# a team-specific convention the model can't know without examples.
alert = "Disk usage at 92% on db-replica-02, 20 minutes to full"

zero_shot_prompt = f'Classify the severity of this alert as LOW, MEDIUM, or HIGH:\n"{alert}"\nSeverity:'

few_shot_prompt = f'''Classify the severity of the alert as LOW, MEDIUM, or HIGH.

Alert: "CPU usage at 45% on web-node-01"
Severity: LOW

Alert: "Disk usage at 98% on db-primary-01, 5 minutes to full"
Severity: HIGH

Alert: "Disk usage at 90% on db-replica-01, 30 minutes to full"
Severity: MEDIUM

Alert: "{alert}"
Severity:'''


def classify(prompt: str) -> str:
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return r.choices[0].message.content.strip()


if __name__ == "__main__":
    print(f"Alert: {alert}\n")
    print(f"Zero-shot: {classify(zero_shot_prompt)}")
    print(f"Few-shot:  {classify(few_shot_prompt)}")
    print()
    print("The few-shot examples encode a convention (primary=HIGH,")
    print("replica=MEDIUM) that isn't stated anywhere in the prompt text -")
    print("zero-shot has no way to know it, few-shot infers it from the")
    print("pattern.")
