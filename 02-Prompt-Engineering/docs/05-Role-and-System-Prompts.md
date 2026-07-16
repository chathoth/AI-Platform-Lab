# 05 - Role and System Prompts

## Introduction

Chapter 02 introduced the system prompt as "the closest thing a model
has to a config file." This chapter goes deep on that one lever,
because in my experience it's the single highest-leverage thing to get
right — a well-written system prompt fixes more bad outputs than any
amount of per-request tweaking.

## Learning Objectives

After this chapter I should be able to:

-   Write a system prompt that reliably constrains tone, scope, and
    behavior.
-   Explain the difference between a "persona" and a "role" in
    prompting.
-   Design a system prompt defensively, anticipating misuse.

------------------------------------------------------------------------

# Persona vs. Role — a Useful Distinction

``` text
Persona:  "You are a friendly, upbeat assistant."       (tone/style)
Role:     "You are a Kubernetes troubleshooting expert." (expertise/scope)
```

Persona shapes *how* it talks. Role shapes *what* it's allowed to talk
about and how deep its assumed expertise runs. A good system prompt
usually sets both, plus explicit boundaries:

``` text
You are a senior SRE assistant embedded in an internal chat tool.

- Answer only questions related to infrastructure, Kubernetes, CI/CD,
  and cloud platforms.
- If asked something outside that scope, say so and suggest who to
  ask instead.
- Be concise: prefer a short direct answer over a long explanation
  unless asked to elaborate.
- Never suggest running a destructive command (delete, drop, force-
  push) without explicitly flagging it as destructive first.
```

**Platform analogy:** this reads like an RBAC policy plus a linter
config for a chatbot. It's not just describing a personality — it's
defining scope (what it should refuse), defaults (concise unless asked
otherwise), and a safety rule (flag destructive actions). Same shape as
writing a policy document for a new team member's on-call permissions.

## System Prompts Are Not a Security Boundary

This is worth stating clearly before chapter 15: a system prompt shapes
*default* behavior, but with enough adversarial user input, a weaker
model can be talked out of it (prompt injection). Treat the system
prompt as **strong guidance**, not as an access-control mechanism — any
action with real consequences (running a command, deleting a resource)
needs enforcement *outside* the model, not just an instruction inside
the prompt.

## Writing an Effective System Prompt: A Checklist

``` text
1. Identity   - who/what is it? (role, not just persona)
2. Scope      - what's in bounds, what's explicitly out of bounds?
3. Tone       - concise vs. thorough, formal vs. casual
4. Defaults   - what should it do when the user is vague?
5. Refusals   - what should it refuse, and how should it say no?
6. Format     - does every response need a particular shape?
```

Not every system prompt needs all six — a quick internal tool might
only need Identity and Format. But for anything user-facing or
production, walking through this checklist catches the gaps that
otherwise surface as "why did it just do that" surprises later.

## Hands-on: Before and After

``` python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.1:8b"

weak_system = "You are a helpful assistant."

strong_system = """You are a DevOps runbook assistant.
Scope: Kubernetes, CI/CD pipelines, and cloud infrastructure only.
If asked about anything else, say "That's outside my scope" and stop.
Always respond in under 3 sentences unless the user asks for more detail.
Never suggest a destructive command (delete, drop, force-push) without
explicitly labeling it "DESTRUCTIVE" first."""

user_question = "How do I get rid of all stuck pods in the cluster?"

for label, system in [("weak", weak_system), ("strong", strong_system)]:
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user_question}],
        temperature=0.3,
    )
    print(f"--- {label} system prompt ---\n{r.choices[0].message.content}\n")
```

Compare: does the "strong" version flag the destructive nature of a
mass-delete command, and stay within scope? That's the checklist above
paying off directly in the output.

## Common Misconceptions

❌ A system prompt guarantees the model will never do X.
(It sets strong defaults, not a hard guarantee — see chapter 15. Real
guardrails for consequential actions belong in code, not just in the
prompt.)

❌ Persona (tone) and role (expertise/scope) are the same thing.
(A friendly persona with no defined scope will just as happily answer
questions it has no business answering — scope has to be stated
explicitly, tone alone doesn't constrain it.)

✔ The system prompt is reusable, application-owned configuration —
design it once, deliberately, using the six-part checklist, rather than
accumulating ad hoc instructions over time.

## Interview Questions

1.  What's the difference between "persona" and "role" in a system
    prompt?
2.  Why shouldn't a system prompt be treated as a security boundary?
3.  Name the six things a thorough system prompt should define.
4.  Why does a well-designed system prompt reduce the need for
    per-request prompt engineering?

## Summary

The system prompt is the highest-leverage, most reusable part of any
prompt — it's application-owned configuration for identity, scope,
tone, defaults, refusals, and format. It shapes default behavior
reliably, but it's guidance, not enforcement — anything with real
consequences still needs a check outside the model.

## Next Chapter

➡️ `06-Structured-Output-Prompting.md`
