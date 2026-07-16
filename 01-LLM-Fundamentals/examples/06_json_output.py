"""
Example: 06_json_output.py

Ask the model for STRUCTURED output (JSON) instead of free text, then
validate it before trusting it - exactly like validating any other
API response. Ties back to docs/16-Prompt-Lifecycle.md and
docs/18-Best-Practices.md ("treat every LLM response as untrusted
input").

Run:
    ollama pull llama3.1:8b
    python 06_json_output.py
"""

import json

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

log_line = (
    "2026-07-15T09:12:03Z ERROR pod/web-app-7d9f CrashLoopBackOff: "
    "exit code 137 (OOMKilled), namespace=production, restarts=6"
)

system_prompt = """You are a log parser. Given one log line, respond with
ONLY a JSON object (no markdown, no explanation) with these exact keys:
"timestamp", "level", "resource", "reason", "namespace".
If a field isn't present in the log, use null."""

# The fields we require before we trust this output downstream.
REQUIRED_KEYS = {"timestamp", "level", "resource", "reason", "namespace"}


def parse_log_line(line: str) -> dict:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": line},
        ],
        temperature=0.0,  # deterministic - this feeds a script, not a human
    )
    raw = response.choices[0].message.content.strip()

    # Never trust raw model output directly - parse it, and be ready
    # for it to fail (chapter 11: hallucinations, chapter 18: validate
    # structured output like any other untrusted API response).
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f"Model did not return valid JSON:\n{raw}")

    missing = REQUIRED_KEYS - parsed.keys()
    if missing:
        raise ValueError(f"Missing required keys {missing} in: {parsed}")

    return parsed


if __name__ == "__main__":
    result = parse_log_line(log_line)
    print("Parsed and validated:")
    print(json.dumps(result, indent=2))
