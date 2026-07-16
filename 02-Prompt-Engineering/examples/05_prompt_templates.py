"""
Example: 05_prompt_templates.py

Build one reusable prompt template with Jinja2 and render it for
different roles/scopes without touching the template itself. Ties
back to docs/07-Prompt-Templates-and-Variables.md.

Run:
    pip install jinja2 openai
    python 05_prompt_templates.py
"""

from jinja2 import Template
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

# {% if %} lets the template render differently depending on whether
# context (e.g. a retrieved runbook excerpt) is actually available -
# the seam where RAG retrieval would plug in.
TEMPLATE = Template("""You are a {{ role }}. Scope: {{ scope }}.
{% if runbook %}
Relevant runbook excerpt:
{{ runbook }}
{% endif %}
Classify the severity of this alert as LOW, MEDIUM, or HIGH:
"{{ alert_text }}" """)

alert_text = "Disk usage at 92% on db-primary-02"


def render_and_ask(**variables) -> str:
    prompt = TEMPLATE.render(**variables)
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return r.choices[0].message.content.strip()


if __name__ == "__main__":
    # Same template, three different variable sets - no template edits.
    print("SRE, no extra context:")
    print(" ", render_and_ask(role="SRE", scope="infrastructure reliability", alert_text=alert_text, runbook=None))

    print("\nSecurity reviewer, no extra context:")
    print(" ", render_and_ask(role="security reviewer", scope="security and compliance risk", alert_text=alert_text, runbook=None))

    print("\nSRE, with a runbook excerpt injected:")
    print(" ", render_and_ask(
        role="SRE",
        scope="infrastructure reliability",
        alert_text=alert_text,
        runbook="Per SRE-042: disk >90% on a PRIMARY database is HIGH severity.",
    ))
