# 17 - Prompt Versioning and Change Management

## Introduction

Chapter 07 moved prompts into their own files; chapter 16 gave us a way
to score changes. This chapter closes the loop: treating a prompt file
exactly like any other piece of production code that needs a change
history, a rollback path, and a review process before a change ships.
Module 01 chapter 18 already flagged "pin your model version" as a best
practice — this is the same instinct applied to the prompt itself.

## Learning Objectives

After this chapter I should be able to:

-   Explain why prompts need the same version discipline as code.
-   Track prompt versions alongside the eval scores that justified each
    change.
-   Roll back a prompt change safely when it regresses in production.

------------------------------------------------------------------------

# Prompts Drift the Same Way Code Drifts

A prompt template file, once it's shared across a team, accumulates
small edits over time — someone tweaks the wording to fix one case,
someone else adds a constraint for another. Without version control and
an eval score attached to each change, there's no way to answer "did
this edit from three weeks ago actually help, or did we just get used
to it?"

``` text
prompts/classify_severity/
├── v1.j2   accuracy: 72% (eval_set_v1)
├── v2.j2   accuracy: 89% (eval_set_v1)  <- added disk-threshold context
├── v3.j2   accuracy: 84% (eval_set_v1)  <- regression! reverted to v2 in prod
└── CHANGELOG.md
```

**Platform analogy:** this is exactly semantic versioning plus a
changelog for a config file — each version tagged with what changed and
why, and critically, **what the eval score was before shipping it**,
the same way you wouldn't merge a code change without CI passing.

## A Minimal Versioning Workflow

``` text
1. Propose a prompt change (a diff, same as code)
2. Run it against the eval set (chapter 16)
3. Compare score to the current production version
4. If it's a clear improvement (and no format/latency regression),
   ship it as a new version
5. Keep the previous version available for instant rollback
6. Log which version produced which output, in production
```

``` python
PROMPT_VERSION = "v2"  # bump deliberately, never edit v2.j2 in place

def load_prompt(name: str, version: str) -> str:
    with open(f"prompts/{name}/{version}.j2") as f:
        return f.read()

# log the version alongside every call - this is what makes a
# production regression traceable to a specific prompt change
response = call_llm(load_prompt("classify_severity", PROMPT_VERSION))
log.info("llm_call", prompt_name="classify_severity", prompt_version=PROMPT_VERSION, ...)
```

Never edit a shipped prompt version file in place — the same reason you
don't edit a tagged release's source in place. If `v2.j2` produced a
specific output in production last week, you need to be able to look at
`v2.j2` today and see exactly what generated it.

## Rollback Has to Be Instant

Because prompt changes are text, not a deploy pipeline, rolling back
should be trivial — flip `PROMPT_VERSION` back to the previous value,
no rebuild required. If a new prompt version is causing bad output in
production, the fix should be as fast as changing a feature flag, not
as slow as a full redeploy.

## Hands-on: Version and Compare

Take the `v1`/`v2` severity-classification prompts from chapter 16,
save them as `prompts/classify_severity/v1.j2` and `v2.j2`, and write a
tiny `CHANGELOG.md` entry for `v2` explaining what changed and citing
the eval score from chapter 16. Then simulate a rollback: point
`PROMPT_VERSION` back at `v1` and confirm the app still runs correctly
against the older file.

## Common Misconceptions

❌ Prompts are just strings, so they don't need the same rigor as code.
(A prompt change can break production behavior just as thoroughly as a
code change — the discipline gap is exactly what causes "the bot
started acting weird and nobody knows which prompt edit did it.")

❌ It's fine to edit a live prompt file directly when a fix is urgent.
(That's editing a tagged release in place — it destroys the ability to
know what produced past output, and makes rollback impossible.)

✔ Every prompt change should carry an eval score (chapter 16) the way
every code change should carry a passing test run — "we changed it" and
"we changed it and confirmed it's better" are very different claims.

## Interview Questions

1.  Why do prompts need version control the same way code does?
2.  What should accompany a new prompt version before it ships to
    production?
3.  Why is editing a shipped prompt version in place a problem?
4.  How does logging the prompt version per call help debug a
    production regression?

## Summary

Prompts need the same change discipline as code: versioned files, an
eval score attached to each change, logging which version produced
which output, and an instant rollback path. Skipping this is how a team
ends up with a prompt nobody remembers the history of and no way to
know whether the last change actually helped.

## Next Chapter

➡️ `18-Best-Practices.md`
