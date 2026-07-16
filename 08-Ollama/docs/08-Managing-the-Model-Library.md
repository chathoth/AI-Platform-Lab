# 08 - Managing the Model Library

## Introduction

Every model this repository has used — `llama3.1:8b`, `llama3.2:3b`,
`nomic-embed-text`, `phi3:3.8b` — came from Ollama's public model
library. This chapter covers how that library is organized, how tags
and versions work, and the housekeeping that keeps a growing local
collection under control.

## Learning Objectives

After this chapter I should be able to:

-   Explain how model names and tags map to specific versions.
-   Search and choose a model from the library deliberately.
-   Manage disk usage as a local model collection grows.

------------------------------------------------------------------------

# Reading a Model Name

``` text
llama3.1:8b
  |       |
  name    tag

nomic-embed-text:latest
  |               |
  name            tag ("latest" is the default if omitted)
```

The **name** identifies the model family; the **tag** identifies a
specific variant — usually parameter count (`8b`, `70b`) or
quantization level (chapter 07), sometimes both
(`llama3.1:8b-instruct-q8_0`).

## Browsing the Library

Ollama's library (browsable at ollama.com/library) lists every
publicly available model and its published tags — worth checking
before assuming a specific size or quantization exists for a given
model family. Not every model publishes every combination.

``` bash
ollama pull llama3.1          # pulls the default tag (usually the most common size)
ollama pull llama3.1:70b       # a specific, larger variant
ollama pull llama3.1:8b-instruct-q8_0  # a specific size AND quantization
```

## Verified: What's Actually Pulled on This Machine

``` text
NAME                       ID              SIZE      MODIFIED     
nomic-embed-text:latest    0a109f422b47    274 MB    42 hours ago    
llama3.2:3b                a80c4f17acd5    2.0 GB    42 hours ago    
phi3:3.8b                  4f2222927938    2.2 GB    7 months ago    
llama3.1:8b                46e0c10c039e    4.9 GB    7 months ago    
```

Four different model families, each chosen for a specific role across
this repository: `llama3.1:8b` for general chat and tool-calling
examples, `nomic-embed-text` for every embedding example (module 03
onward), `llama3.2:3b` as a smaller/faster alternative, `phi3:3.8b` as
a third data point for model comparisons (module 01 chapter 12's
model-size discussion).

## Disk Housekeeping

``` bash
du -sh ~/.ollama/models   # total disk used by all pulled models
ollama list                 # per-model breakdown
ollama rm <model>            # remove a model you're no longer using
```

**Platform analogy:** this is the same housekeeping as pruning unused
Docker images — a local model collection grows quietly over time as
you experiment, and periodically checking `du -sh` against `ollama
list` is the same instinct as `docker system df` before disk pressure
becomes a real problem.

## Updating a Model

``` bash
ollama pull llama3.1:8b   # re-running pull on an existing tag checks for and applies updates
```

Model publishers occasionally update a tag's underlying weights (a bug
fix, a retrain) — re-pulling the same tag checks for and applies any
update, the same idempotent-pull behavior as re-pulling a Docker image
tag that's been updated upstream.

## Hands-on: Audit Your Own Local Library

``` bash
ollama list
du -sh ~/.ollama/models
```

For each model listed, ask honestly: is this still being used for
something, or a leftover from an earlier experiment? Remove anything
genuinely unused — the same discipline as periodically cleaning up
unused container images or unattached volumes.

## Common Misconceptions

❌ A model name without a tag always means the smallest available
size.
(The default tag varies by model family — check the library page or
`ollama show` rather than assuming.)

❌ Re-pulling an already-pulled tag wastes time and bandwidth if
nothing changed.
(Ollama checks for changes first — if the tag is unchanged upstream,
the re-pull completes almost instantly rather than re-downloading
everything.)

✔ Periodically running `du -sh ~/.ollama/models` against `ollama list`
is worth doing the same way you'd periodically prune unused container
images — a local model collection grows quietly.

## Interview Questions

1.  What's the difference between a model's name and its tag?
2.  How would you find out what quantization/size variants exist for
    a given model family?
3.  What happens when you re-run `ollama pull` on an already-pulled
    tag?
4.  How is managing a local model library similar to managing local
    Docker images?

## Summary

Model names and tags together identify a specific variant (size,
quantization) of a model family, browsable through Ollama's public
library. Re-pulling an existing tag checks for updates idempotently,
and periodic disk housekeeping (`du -sh`, `ollama rm`) is worth doing
the same way you'd prune unused container images — a local collection
grows quietly as you experiment.

## Next Chapter

➡️ `09-GPU-vs-CPU-How-Ollama-Chooses.md`
