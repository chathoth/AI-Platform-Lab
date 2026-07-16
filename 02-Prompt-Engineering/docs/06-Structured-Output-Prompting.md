# 06 - Structured Output Prompting

## Introduction

Module 01 chapter 16 said the fully assembled prompt is the highest-
value thing to log, and chapter 18 said to validate structured output
like any other untrusted API response. This chapter is the "how do I
actually get JSON out reliably" piece those chapters assumed. Once a
model's output feeds another system instead of a human, free text stops
being acceptable — I need something I can `json.loads()` without
crossing my fingers.

## Learning Objectives

After this chapter I should be able to:

-   Get reliable JSON output from a prompt, without markdown fences or
    commentary wrapped around it.
-   Use a provider's native structured-output/JSON mode when available.
-   Validate structured output against a schema before trusting it.

------------------------------------------------------------------------

# The Naive Approach (and Why It's Not Enough)

``` text
"Parse this alert into JSON: 'Disk usage at 92% on db-primary-02'"
```

A model asked this way will often comply — but "often" isn't good
enough for a pipeline. Common failure modes: wrapping the JSON in
markdown code fences (` ```json ... ``` `), adding a sentence before or
after it ("Here's the JSON:"), or producing almost-valid JSON (trailing
commas, single quotes). Every one of these breaks a naive `json.loads()`
call.

## Three Layers of Reliability

**1. Be explicit in the prompt:**

``` text
Respond with ONLY a JSON object. No markdown, no code fences, no
explanation before or after. If you cannot determine a field, use null.

{"host": string, "metric": string, "value": number, "unit": string}
```

Showing the exact shape you want (even as pseudo-schema like above) is
far more reliable than describing it in prose.

**2. Use the provider's structured output mode, when available:**

``` python
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    response_format={"type": "json_object"},  # OpenAI-style JSON mode
)
```

This constrains the model's *sampling* itself to only produce valid
JSON — a much stronger guarantee than a prompt instruction alone,
because it's enforced at the decoding level (tying back to module 01
chapter 10's sampling mechanics), not just requested in text.

**3. Validate before trusting, every time:**

``` python
import json
from jsonschema import validate, ValidationError

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

try:
    parsed = json.loads(raw_output)
    validate(instance=parsed, schema=schema)
except (json.JSONDecodeError, ValidationError) as e:
    raise ValueError(f"Model output failed validation: {e}")
```

**Platform analogy:** this is exactly a three-stage input validation
pipeline — client-side hint (the prompt), a stricter server-side
constraint (JSON mode), and schema validation before the payload
touches business logic (jsonschema). Skipping any one layer is the
same risk as trusting client-side form validation alone.

## Hands-on: Break It, Then Fix It

``` python
from openai import OpenAI
import json

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

alert = "Disk usage at 92% on db-primary-02"

# naive - likely to fail json.loads() at least some of the time
naive_prompt = f'Parse this alert into JSON: "{alert}"'
r1 = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": naive_prompt}])
print("naive output:", repr(r1.choices[0].message.content[:100]))

# explicit + JSON mode
strict_prompt = f'''Extract fields from this alert as JSON with keys
"host", "metric", "value" (number), "unit". Alert: "{alert}"'''
r2 = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": strict_prompt}],
    response_format={"type": "json_object"},
    temperature=0,
)
parsed = json.loads(r2.choices[0].message.content)
print("strict output:", parsed)
```

Run the naive version a few times and see how often it needs cleanup
before parsing — that failure rate is exactly what the stricter version
is designed to eliminate.

## Common Misconceptions

❌ "Respond only in JSON" in the prompt is sufficient on its own.
(It reduces failures but doesn't eliminate them — pair it with the
provider's structured-output mode and schema validation for anything
that matters.)

❌ If `json.loads()` succeeds, the data is safe to use.
(Valid JSON with the wrong shape — missing fields, wrong types — will
still break downstream code. Validate against a schema, not just parse
successfully.)

✔ Structured output reliability comes from three layers working
together: explicit prompt instructions, provider-level JSON mode, and
schema validation — not any single one of them.

## Interview Questions

1.  Name three ways a naive "respond in JSON" prompt can still produce
    unparseable output.
2.  What does a provider's JSON mode enforce that a prompt instruction
    alone can't?
3.  Why is schema validation still necessary even after `json.loads()`
    succeeds?
4.  How is this three-layer approach similar to standard API input
    validation?

## Summary

Reliable structured output takes three layers: an explicit, example-
shaped prompt instruction; the provider's native JSON/structured-output
mode enforced at the sampling level; and schema validation before the
data is trusted downstream. Treat model output exactly like any other
untrusted API payload — because that's what it is.

## Next Chapter

➡️ `07-Prompt-Templates-and-Variables.md`
