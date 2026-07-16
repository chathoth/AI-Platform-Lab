# 06 - Modelfiles: Customizing a Model

## Introduction

Module 02 chapter 05 built system prompts by passing them in every API
call. A Modelfile bakes that same customization into the model itself
— pull once, get the persona/behavior every time, no system message
needed in your application code. Verified directly: built a real
custom model from a Modelfile and confirmed its behavior actually
differs from the base model.

## Learning Objectives

After this chapter I should be able to:

-   Write a Modelfile that sets a system prompt and parameters.
-   Build a custom model with `ollama create`.
-   Explain when baking behavior into a model is worth it over
    passing a system prompt per call.

------------------------------------------------------------------------

# A Complete, Verified Modelfile

``` text
FROM llama3.1:8b
PARAMETER temperature 0
SYSTEM """You are a terse DevOps assistant. Answer in one sentence, no exceptions."""
```

``` bash
ollama create terse-devops -f Modelfile
```

Verified output: `ollama create` builds a new model layer on top of
`llama3.1:8b`'s existing weights (no re-training, no new weights at
all — just a new configuration layer), and it shows up immediately in
`ollama list`.

## Verified: The Custom Model's Behavior Actually Changes

``` bash
ollama run terse-devops "What is a Kubernetes readiness probe?"
```

Verified real output:

``` text
A Kubernetes readiness probe is a liveness check that determines if a
container is ready to receive traffic and handle requests.
```

One sentence, terse, exactly matching the `SYSTEM` instruction — with
no system prompt passed in the `ollama run` call itself. Compare this
to calling plain `llama3.1:8b` with the same question and no system
prompt (module 02 chapter 05's "weak vs. strong system prompt"
comparison) — the difference is the Modelfile, baked in once.

## The Modelfile Directives Worth Knowing

``` text
FROM <model>              - the base model this one builds on (required)
SYSTEM """..."""            - the default system prompt (module 02 chapter 05)
PARAMETER temperature 0      - a default sampling parameter (module 02 chapter 10)
PARAMETER num_ctx 8192         - default context window size (chapter 10)
TEMPLATE """..."""               - advanced: customize the raw prompt template itself
```

Most customization needs are covered by `FROM`, `SYSTEM`, and a few
`PARAMETER` lines — `TEMPLATE` is a deeper customization most projects
won't need, since it controls the literal formatting the base model
expects, not just its behavior.

## When a Modelfile Is Worth It Over a Per-Call System Prompt

  Situation                                   Modelfile worth it?
  ------------------------------------------------ ------------------------------
  One application, prompt already in code             No - a per-call system prompt is simpler
  Same persona reused across multiple apps/scripts       Yes - pull once, consistent everywhere
  Want a default temperature/context without repeating it | Yes - saves repeating the same parameters everywhere
  Sharing a customized model with a team                    Yes - `ollama create` + share the Modelfile, everyone gets the same behavior

**Platform analogy:** this is the difference between passing
environment variables to a container at `docker run` time versus
baking defaults into the image itself — both work, but baking it in
means every consumer gets the same behavior without having to remember
to pass the same configuration every time.

## Hands-on: Build and Compare, Then Clean Up

``` bash
cat > Modelfile << 'EOF'
FROM llama3.1:8b
PARAMETER temperature 0
SYSTEM """You are a terse DevOps assistant. Answer in one sentence, no exceptions."""
EOF

ollama create terse-devops -f Modelfile
ollama run terse-devops "What is a Kubernetes readiness probe?"

# compare against the base model with no system prompt
ollama run llama3.1:8b "What is a Kubernetes readiness probe?"

# clean up when done experimenting
ollama rm terse-devops
```

## Common Misconceptions

❌ A Modelfile trains a new model.
(It creates a new configuration layer — system prompt, parameters,
template — on top of existing weights. No training happens; this is
module 01 chapter 14's RAG-vs-fine-tuning distinction in miniature:
this is closer to a config overlay than to fine-tuning.)

❌ `ollama create` re-downloads the base model's weights.
(It reuses the already-pulled base model's layers — verified in the
build output ("using existing layer...") — only the new configuration
layer is actually created.)

✔ A Modelfile is the Ollama-native way to do what module 02 chapter 05
recommends doing in a system prompt — the difference is *where* that
configuration lives: baked into the model versus passed in every API
call.

## Interview Questions

1.  What does `ollama create -f Modelfile` actually do to the base
    model's weights?
2.  Name three Modelfile directives and what each configures.
3.  When is a Modelfile worth building instead of just passing a
    system prompt per call?
4.  Why is building a custom model from a Modelfile different from
    fine-tuning?

## Summary

A Modelfile bakes a system prompt and default parameters into a new,
named model — verified directly, producing measurably different
behavior (terser answers) from the base model, with no re-training
involved, just a configuration layer on top of existing weights. Worth
building when the same customization needs to be reused consistently
across multiple applications or shared with a team, rather than
repeated in every API call.

## Next Chapter

➡️ `07-Model-Formats-and-Quantization.md`
