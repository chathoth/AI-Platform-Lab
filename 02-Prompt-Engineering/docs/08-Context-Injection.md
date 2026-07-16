# 08 - Context Injection

## Introduction

Chapter 07 left a `{% if runbook %}` block in the template with no
explanation of where `runbook` actually comes from. This chapter
answers that: context injection is the practice of pulling real,
current data into a prompt at request time — the same idea as RAG from
module 01 chapter 14, but viewed from the prompting side rather than the
retrieval side.

## Learning Objectives

After this chapter I should be able to:

-   Explain what context injection is and why it reduces hallucination.
-   Inject structured data (not just prose) into a prompt cleanly.
-   Keep injected context clearly delimited from instructions.

------------------------------------------------------------------------

# Why Inject Context At All

A model's trained-in knowledge is frozen at a cutoff date and knows
nothing about your specific systems (module 01 chapter 11). Context
injection fixes this the same way a config-management tool fixes
"the server doesn't know its own hostname" — by handing it the actual,
current data instead of expecting it to already know.

``` text
Without injection:
  "What's our policy on database primary disk usage alerts?"
  → model guesses at a generic best practice

With injection:
  "Given this policy document: '...disk >90% on a primary DB is
   HIGH severity per SRE-042...' What's our policy on database
   primary disk usage alerts?"
  → model answers from the actual document
```

## Injecting Structured Data, Not Just Prose

Raw JSON/YAML dropped into a prompt works, but formatting it
legibly measurably helps the model use it correctly:

``` python
import json

metrics = {"cpu_percent": 45, "memory_percent": 78, "disk_percent": 92}

# works, but harder for the model to parse visually
prompt_v1 = f"Given these metrics: {json.dumps(metrics)}, what's the top concern?"

# clearer - one fact per line
formatted = "\n".join(f"- {k}: {v}%" for k, v in metrics.items())
prompt_v2 = f"Given these metrics:\n{formatted}\nWhat's the top concern?"
```

This mirrors a debugging instinct I already have: a wall of raw JSON in
a terminal is technically readable, but a formatted table gets scanned
correctly far more often — same signal, easier to act on correctly.

## Delimit Injected Context Clearly

Mixing instructions and injected data in the same unstructured blob is
both an accuracy risk (the model can't tell what's a fact vs. what's an
instruction) and a security risk (this is the seam prompt injection
uses, covered fully in chapter 15). Always mark the boundary explicitly:

``` text
Answer the user's question using ONLY the information between the
<context> tags. If the answer isn't in the context, say "I don't have
that information."

<context>
{{ retrieved_document }}
</context>

Question: {{ user_question }}
```

**Platform analogy:** this is exactly the difference between
interpolating a user-supplied string directly into a SQL query versus
using a parameterized query. The `<context>` tags (or a similar clear
delimiter) are your parameterization — they tell the model "this part
is data, not instructions," the same way a bound parameter tells a
database driver "this part is a value, not SQL syntax."

## Hands-on: Grounded vs. Ungrounded

``` python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

policy_doc = "Per SRE-042: disk usage above 90% on any PRIMARY database node is HIGH severity and pages on-call immediately. Replica nodes at the same threshold are MEDIUM severity."

question = "Is 92% disk usage on a replica database node HIGH or MEDIUM severity?"

ungrounded = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": question}], temperature=0)
print("Ungrounded:", ungrounded.choices[0].message.content[:200])

grounded_prompt = f"""Answer using ONLY the information in <context>.

<context>
{policy_doc}
</context>

Question: {question}"""
grounded = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": grounded_prompt}], temperature=0)
print("Grounded:", grounded.choices[0].message.content[:200])
```

The ungrounded version is guessing at a generic convention. The
grounded version can only be right by actually reading the injected
policy — that's the whole value of context injection in one comparison.

## Common Misconceptions

❌ Context injection and RAG are different techniques.
(RAG is *how* you find the right context to inject — the retrieval
step. Context injection is what happens once you have it. They're two
halves of the same pipeline, covered from the retrieval side in module
01 chapter 14 and module 05.)

❌ Dumping raw data into the prompt is good enough.
(Formatting it legibly and delimiting it clearly from instructions
measurably improves both accuracy and safety — see chapter 15.)

✔ Clearly delimiting injected context from instructions is the prompt-
level equivalent of parameterized queries — it's what keeps "data" from
being interpreted as "commands."

## Interview Questions

1.  What problem does context injection solve that the model's trained
    knowledge can't?
2.  Why does formatting matter when injecting structured data like
    metrics into a prompt?
3.  Why is clearly delimiting context from instructions both an
    accuracy and a security practice?
4.  How is delimiting context similar to parameterized SQL queries?

## Summary

Context injection hands the model real, current, request-specific
data instead of relying on frozen training knowledge — directly
reducing hallucination the same way RAG does. Format injected data
legibly and delimit it clearly from instructions, the same discipline
as parameterizing untrusted input instead of concatenating it directly
into a command.

## Next Chapter

➡️ `09-Instruction-Clarity-and-Constraints.md`
