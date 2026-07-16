"""
Example: 06_context_injection.py

Compare an ungrounded answer against one grounded in injected,
clearly-delimited context. Ties back to
docs/08-Context-Injection.md.

Run:
    ollama pull llama3.1:8b
    python 06_context_injection.py
"""

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

# The kind of fact a model can't know from training - it's an internal,
# team-specific policy document.
policy_doc = (
    "Per SRE-042: disk usage above 90% on any PRIMARY database node is "
    "HIGH severity and pages on-call immediately. Replica nodes at the "
    "same threshold are MEDIUM severity."
)

question = "Is 92% disk usage on a replica database node HIGH or MEDIUM severity?"

ungrounded_prompt = question

# <context> tags mark the boundary between data and instructions -
# the prompt-level equivalent of a parameterized query.
grounded_prompt = f"""Answer using ONLY the information between the
<context> tags. If the answer isn't in the context, say so.

<context>
{policy_doc}
</context>

Question: {question}"""


def ask(prompt: str) -> str:
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return r.choices[0].message.content.strip()


if __name__ == "__main__":
    print("--- ungrounded (no policy doc) ---")
    print(ask(ungrounded_prompt))
    print()
    print("--- grounded (policy doc injected) ---")
    print(ask(grounded_prompt))
    print()
    print("The ungrounded answer is guessing at a generic convention.")
    print("The grounded answer can only be right by actually reading")
    print("the injected policy text - that's the whole value of")
    print("context injection.")
