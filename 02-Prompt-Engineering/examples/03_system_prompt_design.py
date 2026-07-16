"""
Example: 03_system_prompt_design.py

A weak, generic system prompt vs. a system prompt that states
identity, scope, tone, defaults, and refusal rules explicitly. Ties
back to docs/05-Role-and-System-Prompts.md.

Run:
    ollama pull llama3.1:8b
    python 03_system_prompt_design.py
"""

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

weak_system = "You are a helpful assistant."

# Identity, scope, tone, defaults, and a refusal rule - the six-part
# checklist from the chapter, minus "format" (not needed here).
strong_system = """You are a DevOps runbook assistant.
Scope: Kubernetes, CI/CD pipelines, and cloud infrastructure only. If
asked about anything else, say "That's outside my scope" and stop.
Tone: concise - under 3 sentences unless asked for more detail.
Never suggest a destructive command (delete, drop, force-push) without
explicitly labeling it "DESTRUCTIVE" first."""

questions = [
    "How do I get rid of all stuck pods in the cluster?",
    "What's a good recipe for chocolate chip cookies?",
]


def ask(system: str, question: str) -> str:
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": question}],
        temperature=0.3,
    )
    return r.choices[0].message.content.strip()


if __name__ == "__main__":
    for question in questions:
        print(f"Q: {question}")
        print(f"  weak system:   {ask(weak_system, question)}")
        print(f"  strong system: {ask(strong_system, question)}")
        print()

    print("Check: does the strong system prompt flag the destructive")
    print("mass-delete command, and correctly refuse the off-scope")
    print("cookie question? That's the scope + refusal rules paying off.")
