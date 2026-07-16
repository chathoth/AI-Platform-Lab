"""
Example: 01_token_count.py

Counts tokens for a few real-world strings and compares them.
Ties back to docs/04-Tokens-and-Tokenization.md.

Run:
    pip install tiktoken
    python 01_token_count.py
"""

import tiktoken

# gpt-4's tokenizer is a good general-purpose one to reason with,
# even if you end up calling a different model day to day.
enc = tiktoken.encoding_for_model("gpt-4")

# Plain English vs. the kind of text a platform engineer actually
# pastes into a prompt - commands, YAML, log lines.
samples = {
    "plain_english": "The deployment finished successfully this morning.",
    "kubectl_command": "kubectl apply -f deployment.yaml --namespace production",
    "yaml_snippet": (
        "apiVersion: apps/v1\n"
        "kind: Deployment\n"
        "metadata:\n"
        "  name: web-app\n"
        "spec:\n"
        "  replicas: 3\n"
    ),
    "log_line": "2026-07-15T09:12:03Z ERROR pod/web-app-7d9f CrashLoopBackOff: exit code 137 (OOMKilled)",
}


def count_tokens(text: str) -> int:
    return len(enc.encode(text))


if __name__ == "__main__":
    print(f"{'sample':<18} {'chars':>6} {'tokens':>7} {'tokens/char':>12}")
    print("-" * 48)
    for name, text in samples.items():
        n_chars = len(text)
        n_tokens = count_tokens(text)
        ratio = n_tokens / n_chars
        print(f"{name:<18} {n_chars:>6} {n_tokens:>7} {ratio:>12.2f}")

    print()
    print("Notice: YAML and kubectl commands use MORE tokens per character")
    print("than plain English - punctuation, indentation, and identifiers")
    print("all cost tokens. Keep that in mind before pasting a whole")
    print("manifest or log file into a prompt.")
