# 01 - What is Prompt Engineering?

## Introduction

I used to treat prompts like search queries — type something reasonable,
see what comes back, tweak if it's wrong. That works for a one-off
question. It falls apart the moment a prompt is embedded in a script, a
CI job, or a tool other people depend on. Prompt engineering is what
that casual habit turns into once a prompt becomes **part of a system**
instead of a one-time question: an input contract with a
non-deterministic function, and it deserves the same care I'd give to
designing an API request body.

## Learning Objectives

After this chapter I should be able to:

-   Define prompt engineering and explain why it's a real discipline,
    not just "asking nicely."
-   Explain why the same underlying model can produce wildly different
    quality depending on the prompt alone.
-   Identify when a prompt has graduated from "throwaway question" to
    "needs engineering."

------------------------------------------------------------------------

# From Question to Interface

``` text
Casual use:        "Summarize this."
Engineered prompt:  Role + Task + Constraints + Format + Examples
```

A prompt is the only input an LLM receives (chapter 03 of module 01
covered how everything — system instructions, history, retrieved
context — gets flattened into one text payload before the model ever
sees it). Every ounce of behavior you want — tone, format, boundaries,
what to do when the model doesn't know something — has to be encoded in
that text, because there is no other channel.

**Platform analogy:** this is the same shift as moving from "curl a URL
and see what happens" to "write an OpenAPI spec." Nobody designs a
production API by trial and error in a browser tab forever — at some
point you formalize the contract: required fields, expected format,
error behavior. Prompt engineering is that same formalization applied
to natural-language input.

## Why the Same Model Gives Wildly Different Results

Two engineers can call the identical model and get very different
quality, because the model has no way to infer unstated intent — it can
only respond to what's actually on the page.

``` text
Vague:      "Fix this config."
Engineered: "You are a Kubernetes config reviewer. Given this YAML,
             list ONLY syntax errors and schema violations. Do not
             suggest style changes. Output as a numbered list."
```

The model didn't get smarter between those two prompts — the second one
just removed the ambiguity the first one left for the model to guess
at. Most "the model is bad at this" complaints I've run into turn out
to be under-specified prompts, the same way most "the API is broken"
tickets turn out to be a malformed request.

## When a Prompt Needs Engineering

Not every prompt needs this treatment — a one-off question in a chat UI
is fine to leave loose. The signal that a prompt needs real engineering
is the same signal that tells me a script needs to become a proper
tool: **is this going to run more than once, unattended, or feed
something else?**

  Signal                                    Needs engineering?
  ------------------------------------------ --------------------
  One-off question, human reads the answer   No
  Runs in a script or pipeline                Yes
  Output feeds another system                 Yes
  Multiple people/teams will reuse it          Yes
  Behavior must be consistent over time        Yes

## Hands-on: Feel the Gap Yourself

``` bash
ollama run llama3.1:8b "Fix this config: replicas: '3'"
```

versus

``` bash
ollama run llama3.1:8b "You are a Kubernetes config reviewer. Given \
this YAML snippet, list only syntax or schema errors as a numbered \
list, nothing else: replicas: '3'"
```

Same model, same underlying weights, same hardware — compare how much
more usable the second response is. That gap, entirely produced by
prompt structure alone, is the whole reason this module exists.

## Common Misconceptions

❌ Prompt engineering is a temporary skill that better models will make
unnecessary.
(Every model generation has shipped with *more* prompting surface area
— system prompts, tool schemas, structured output modes — not less.
The skill compounds, it doesn't expire.)

❌ A longer prompt is always a better prompt.
(Length isn't the goal — removing ambiguity is. A short, precise prompt
beats a long, vague one every time, and costs fewer tokens per chapter
04 of module 01.)

✔ A good prompt is a specification: role, task, constraints, and
format, stated explicitly instead of implied.

## Interview Questions

1.  What is prompt engineering, and why does it matter even as models
    improve?
2.  Why can the same model produce very different quality output for
    two different prompts asking "the same thing"?
3.  What signal tells you a prompt needs to be engineered rather than
    left as a casual question?

## Summary

Prompt engineering treats the prompt as an interface contract, not a
casual question — because a model can only act on what's explicitly on
the page. The discipline matters most exactly where I spend my time:
prompts embedded in scripts, pipelines, and tools that need to behave
consistently without a human in the loop to catch a bad answer.

## Next Chapter

➡️ `02-Anatomy-of-a-Prompt.md`
