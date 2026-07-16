# 02 - Anatomy of a Prompt

## Introduction

Before comparing prompting techniques, I need the vocabulary for what a
prompt is actually made of. This maps directly onto the "prompt
assembly" stage from module 01's
[16-Prompt-Lifecycle.md](../../01-LLM-Fundamentals/docs/16-Prompt-Lifecycle.md)
— this chapter is the zoomed-in view of exactly what gets assembled.

## Learning Objectives

After this chapter I should be able to:

-   Name the three message roles (system, user, assistant) and what
    each is for.
-   Explain why the system prompt is the closest thing to a config
    file a model has.
-   Break any prompt into its component parts: role, task, context,
    constraints, format.

------------------------------------------------------------------------

# The Three Roles

Every chat-style API call is a list of role-tagged messages, not one
blob of text:

``` python
messages = [
    {"role": "system", "content": "You are a terse Kubernetes troubleshooting assistant."},
    {"role": "user", "content": "Pod is in CrashLoopBackOff, what do I check first?"},
    {"role": "assistant", "content": "Check `kubectl logs <pod> --previous` first."},
    {"role": "user", "content": "It shows OOMKilled."},
]
```

  Role         Purpose
  ------------ ---------------------------------------------------------
  `system`     Sets behavior/persona/rules for the whole conversation
  `user`       The actual request, turn by turn
  `assistant`  The model's prior replies (fed back in for multi-turn context)

**Platform analogy:** the system prompt is the closest thing an LLM
call has to a **config file** — it's set once (often by the
application, not the end user) and shapes every response for the
session. `user`/`assistant` messages are the request/response log —
the actual traffic flowing through that configuration.

## The Five Parts of a Well-Formed Prompt

Regardless of which role it lives in, a well-engineered prompt usually
has five identifiable parts:

``` text
1. ROLE        Who is the model supposed to be / what's its expertise?
2. TASK        What, specifically, do you want done?
3. CONTEXT     What information does it need to do that (data, docs)?
4. CONSTRAINTS What are the boundaries (length, tone, what NOT to do)?
5. FORMAT      What shape should the output take?
```

``` text
[ROLE]        You are a senior SRE reviewing an incident report.
[TASK]        Identify the root cause.
[CONTEXT]     <paste the incident log here>
[CONSTRAINTS] Only use information in the log. Do not speculate.
[FORMAT]      Respond in one sentence.
```

Missing any of these isn't automatically wrong — a casual chat doesn't
need explicit FORMAT — but every time I've had a prompt misbehave in a
pipeline, it's because one of these five was left implicit and the
model filled the gap with its own assumption.

## Where the System Prompt Actually Belongs

A rule I follow: **anything true for every request in this feature goes
in the system prompt; anything specific to this one call goes in the
user message.**

``` python
# anti-pattern - re-stating the role every single call
user_msg = "You are a DevOps assistant. Explain what a readiness probe is."

# better - role lives once, in the system prompt
system_msg = "You are a DevOps assistant specializing in Kubernetes."
user_msg = "Explain what a readiness probe is."
```

This isn't just tidier — it's the same reason environment config lives
in one file instead of being copy-pasted into every script that needs
it: one place to update behavior, and it's harder for the "identity"
part of the prompt to drift or get overridden by user input (a small
head start on the prompt-injection problem in chapter 15).

## Hands-on: Decompose a Real Prompt

``` python
prompt = """You are a Terraform reviewer. Given the plan output below,
list only resources being DESTROYED, as a bulleted list. If none are
being destroyed, say "No destructive changes." Plan output:
<paste plan here>"""
```

Before running this, label each sentence with ROLE / TASK / CONTEXT /
CONSTRAINTS / FORMAT. Then take a prompt you've written yourself
recently (or a system prompt from `08_chat_completion.py` in module 01)
and do the same. Any part you can't label is either redundant or a gap
the model is being left to guess at.

## Common Misconceptions

❌ The system prompt is optional / just a nice-to-have.
(It's the most reliable lever you have for consistent behavior across
many calls — treat it as required for anything beyond a single throwaway
question.)

❌ Users can't influence or override a system prompt.
(They often can, especially with weaker models or careless design —
this is exactly the seam prompt injection exploits, covered in chapter
15.)

✔ Role, Task, Context, Constraints, Format isn't a rigid template to
fill in every time — it's a checklist for finding what's been left
implicit in a prompt that isn't behaving.

## Interview Questions

1.  What are the three message roles in a chat-style LLM API, and what
    is each one for?
2.  Why should stable identity/behavior instructions live in the system
    prompt rather than being repeated in every user message?
3.  Name the five parts of a well-formed prompt and give an example of
    each.

## Summary

A prompt is a structured object, not a blob of text — role-tagged
messages, each with a job, and within any given message, five
identifiable parts (role, task, context, constraints, format). Most
"the model didn't do what I wanted" bugs trace back to one of those
five being left implicit.

## Next Chapter

➡️ `03-Zero-Shot-vs-Few-Shot.md`
