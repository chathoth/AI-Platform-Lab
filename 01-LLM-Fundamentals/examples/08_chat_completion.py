"""
Example: 08_chat_completion.py

A minimal multi-turn chatbot loop - a tiny "DevOps assistant" that
remembers the conversation. Ties back to docs/08-Training-vs-Inference.md
(the model itself has no memory - the application resends history
every turn) and docs/16-Prompt-Lifecycle.md.

Run:
    ollama pull llama3.1:8b
    python 08_chat_completion.py

Type 'quit' to exit.
"""

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

SYSTEM_PROMPT = (
    "You are a concise DevOps assistant. Answer questions about "
    "Kubernetes, CI/CD, and cloud infrastructure clearly and briefly. "
    "If you're not sure about something, say so instead of guessing."
)

if __name__ == "__main__":
    # This list IS the "memory" - nothing is remembered by the model
    # itself between calls. Every turn, we resend the whole thing.
    history = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("DevOps assistant ready. Type 'quit' to exit.\n")

    while True:
        user_input = input("you> ").strip()
        if user_input.lower() in ("quit", "exit"):
            break
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model=MODEL,
            messages=history,
            temperature=0.5,
        )
        reply = response.choices[0].message.content

        print(f"bot> {reply}\n")
        history.append({"role": "assistant", "content": reply})

        # Every turn costs more tokens than the last, because the
        # WHOLE history gets resent (see docs/09-Context-Window.md).
        print(f"[history so far: {len(history)} messages]\n")
