# 07 - Prompt Templates and Variables

## Introduction

Once I have a prompt that works, the next problem is reusing it without
copy-pasting and hand-editing a string every time. This is the exact
moment prompting stops being "writing text" and starts being "writing
code that generates text" — the same shift as replacing a one-off shell
script with a parameterized Ansible playbook.

## Learning Objectives

After this chapter I should be able to:

-   Turn a working prompt into a reusable template with variables.
-   Separate prompt structure from the data injected into it.
-   Organize templates as version-controlled files, not inline strings.

------------------------------------------------------------------------

# From Hardcoded String to Template

``` python
# anti-pattern - a new hand-written string for every alert
prompt = "Classify the severity of: Disk usage at 92% on db-primary-02"

# template - structure is fixed, data is injected
TEMPLATE = "Classify the severity of: {alert_text}"
prompt = TEMPLATE.format(alert_text="Disk usage at 92% on db-primary-02")
```

Trivial with one variable — but real prompts usually need several,
plus formatting logic (rendering a list, conditionally including a
section). That's exactly what a real templating engine is for.

## Using Jinja2 for Real Templates

``` python
from jinja2 import Template

TEMPLATE = Template("""You are a {{ role }} reviewing an alert.

Alert: {{ alert_text }}
{% if runbook %}
Relevant runbook excerpt:
{{ runbook }}
{% endif %}

Classify severity as LOW, MEDIUM, or HIGH. Respond with only the word.""")

prompt = TEMPLATE.render(
    role="site reliability engineer",
    alert_text="Disk usage at 92% on db-primary-02",
    runbook="Disk >90% on a primary DB is HIGH severity per SRE-042.",
)
```

The `{% if runbook %}` block only renders when context is actually
available — this is the seam where chapter 08 (context injection) and
RAG retrieval (module 05) plug in: the template stays the same whether
or not a runbook was found, only the data changes.

**Platform analogy:** this is Jinja2 templating a Kubernetes manifest —
`values.yaml` provides the variables, the template provides the
structure, and the same template produces different rendered output
for dev vs. prod. A prompt template plays exactly the same role: fixed
structure, swappable data, one place to fix a bug instead of N
scattered copies.

## Organizing Templates as Files, Not Inline Strings

``` text
prompts/
├── classify_severity.j2
├── summarize_incident.j2
└── review_terraform_plan.j2
```

``` python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("prompts/"))
template = env.get_template("classify_severity.j2")
prompt = template.render(alert_text=alert_text)
```

Once prompts live in their own files, they get everything code gets:
diffable changes in version control, a clear owner, and the ability to
update behavior without redeploying application code — the same reason
config and application logic live in separate files instead of being
interleaved.

## Hands-on: Templatize a Prompt You Already Wrote

Take the "strong" system prompt from chapter 05 and the alert-
classification prompt from chapter 03, and combine them into one
Jinja2 template with `role`, `scope`, and `alert_text` as variables.
Render it for three different roles (SRE, security reviewer, on-call
generalist) without touching the template itself — only the variables
change.

``` python
from jinja2 import Template

TEMPLATE = Template("""You are a {{ role }}. Scope: {{ scope }}.
Classify the severity of this alert as LOW, MEDIUM, or HIGH:
"{{ alert_text }}" """)

for role, scope in [
    ("SRE", "infrastructure reliability"),
    ("security reviewer", "security and compliance risk"),
]:
    print(TEMPLATE.render(role=role, scope=scope, alert_text="Disk usage at 92% on db-primary-02"))
    print()
```

## Common Misconceptions

❌ Python f-strings are good enough for any prompt template.
(They work for simple substitution, but have no conditionals, loops, or
escaping — Jinja2 (or similar) earns its keep once a template has
optional sections or repeated structure, like a rendered few-shot
example list.)

❌ Templating is over-engineering for "just a prompt."
(The moment a prompt is reused with different inputs more than once,
hardcoded strings become exactly the kind of copy-paste drift that
makes a fix in one place not apply everywhere else.)

✔ Separating prompt *structure* (the template) from prompt *data* (the
variables) is what makes a prompt maintainable, testable, and safe to
change without touching application code.

## Interview Questions

1.  Why is a hardcoded prompt string harder to maintain than a
    template?
2.  What does a templating engine like Jinja2 offer beyond simple
    string formatting?
3.  Why should prompt templates live in their own files rather than
    inline in application code?
4.  Where would retrieved context (from a RAG pipeline) plug into a
    prompt template?

## Summary

A prompt template separates fixed structure from variable data, the
same way a Kubernetes manifest separates template from `values.yaml`.
Moving from hardcoded strings to file-based, version-controlled
templates is what makes prompts maintainable at the point where they
start being reused across different inputs and contexts.

## Next Chapter

➡️ `08-Context-Injection.md`
