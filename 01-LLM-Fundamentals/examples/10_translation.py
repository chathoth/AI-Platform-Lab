"""
Example: 10_translation.py

Translate an on-call status update into another language - the kind
of task that matters for a globally distributed on-call rotation.
Ties back to docs/01-What-is-an-LLM.md (real-world use cases).

Run:
    ollama pull llama3.1:8b
    python 10_translation.py
"""

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

status_update = (
    "The database migration is complete and all services have been "
    "restarted. We are monitoring error rates for the next hour before "
    "closing out the maintenance window."
)

target_languages = ["Spanish", "French", "Japanese"]


def translate(text: str, language: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    f"Translate the user's message into {language}. "
                    "Keep technical terms (service names, database, etc.) "
                    "recognizable. Respond with only the translation."
                ),
            },
            {"role": "user", "content": text},
        ],
        temperature=0.0,  # translation should be faithful, not creative
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    print(f"Original (EN): {status_update}\n")
    for language in target_languages:
        print(f"{language}: {translate(status_update, language)}")

    print()
    print("For anything that actually ships to users (status pages,")
    print("customer-facing incident comms), have a native speaker spot-")
    print("check this - the model can sound fluent while getting a")
    print("technical term subtly wrong (docs/11-Hallucinations.md).")
