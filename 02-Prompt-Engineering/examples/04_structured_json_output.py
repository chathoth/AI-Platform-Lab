"""
Example: 04_structured_json_output.py

Force reliable JSON output using explicit prompt instructions + the
provider's JSON mode, then validate it against a schema before
trusting it. Ties back to docs/06-Structured-Output-Prompting.md.

Run:
    ollama pull llama3.1:8b
    pip install openai jsonschema
    python 04_structured_json_output.py
"""

import json

from jsonschema import ValidationError, validate
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

alert = "Disk usage at 92% on db-primary-02"

schema = {
    "type": "object",
    "properties": {
        "host": {"type": "string"},
        "metric": {"type": "string"},
        "value": {"type": "number"},
        "unit": {"type": "string"},
    },
    "required": ["host", "metric", "value"],
}

prompt = f'''Extract fields from this alert as a JSON object with keys
"host", "metric", "value" (a number, not a string), and "unit".
Alert: "{alert}"'''


def extract_structured(prompt: str) -> dict:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},  # constrains sampling to valid JSON
        temperature=0,
    )
    raw = response.choices[0].message.content

    try:
        parsed = json.loads(raw)
        validate(instance=parsed, schema=schema)
    except (json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"Model output failed validation: {e}\nRaw output: {raw}")

    return parsed


if __name__ == "__main__":
    result = extract_structured(prompt)
    print("Parsed and schema-validated:")
    print(json.dumps(result, indent=2))
