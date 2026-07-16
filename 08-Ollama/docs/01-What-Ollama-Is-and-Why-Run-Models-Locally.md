# 01 - What Ollama Is and Why Run Models Locally

## Introduction

Every module so far has been calling Ollama without a proper
introduction. Time to fix that: Ollama is a local model runtime — it
downloads, manages, and serves LLMs on your own machine, exposing a
simple API in front of them so your code never has to deal with the
underlying model format directly.

## Learning Objectives

After this chapter I should be able to:

-   Explain what Ollama actually does, in one sentence.
-   Explain why `base_url="http://localhost:11434/v1"` has worked
    throughout this repository.
-   Name the concrete reasons to run a model locally instead of
    calling a hosted API.

------------------------------------------------------------------------

# What Ollama Actually Does

``` text
Without Ollama:  download model weights yourself, figure out the
                   right inference engine, manage GPU/CPU placement,
                   write your own serving layer, build an API around it

With Ollama:      ollama pull llama3.1:8b
                   ollama serve   (usually running automatically)
                   -> a local HTTP server, ready to call
```

Ollama wraps `llama.cpp` (a C++ inference engine) with model
management (downloading, versioning, storage) and a clean HTTP API on
top — the same role a container runtime plays for images: you don't
manually manage layers and namespaces, you `docker run` and it handles
the rest.

## Why `localhost:11434` Has Worked This Whole Repository

Every example since module 01 pointed an OpenAI-compatible client at
`http://localhost:11434/v1` — that's Ollama's server, running locally,
speaking a format compatible enough with OpenAI's API that existing
client libraries work unmodified (chapter 05 covers exactly what that
compatibility layer does and doesn't cover). No API key was ever
needed because nothing left your machine.

## Why Run Locally At All

This directly extends module 01 chapter 15 and module 03 chapter 03's
residency arguments, now focused on the runtime itself:

  Reason                        Why it matters
  --------------------------------- --------------------------------------
  Cost                                 Free after download — no per-token billing
  Data residency                        Nothing leaves your machine — the actual reason every example in this repo defaults to it
  Offline capability                     Works with no internet connection once a model is pulled
  Learning and experimentation             Break things, try things, without worrying about a bill
  Latency for local tooling                  No network round trip to a remote API

None of this makes local the universally right choice for production —
module 01 chapter 15 already covered that trade-off honestly. Ollama is
the tool that makes the local side of that decision genuinely practical
instead of a research project.

## Hands-on: Confirm Ollama Is Running and Reachable

``` bash
ollama --version
curl -s http://localhost:11434/api/tags
```

The `curl` command should return real JSON listing whatever models
you've pulled — this is the exact request every OpenAI-compatible
client in this repository has been making under the hood, just
without a client library wrapping it. Chapter 04 goes deep on this
native API.

## Common Misconceptions

❌ Ollama is a model.
(It's a runtime that serves models — `llama3.1:8b`, `nomic-embed-text`,
and every other model name pulled with `ollama pull` are what actually
run underneath it.)

❌ The OpenAI-compatible endpoint means Ollama *is* OpenAI's API.
(It's a compatibility layer over Ollama's own native API — close
enough that existing client code works, but not identical, per
chapter 05.)

✔ Ollama's real job is model lifecycle management (download, store,
load, unload) plus a serving API — the same category of tool as a
container runtime, applied to model weights instead of container
images.

## Interview Questions

1.  What does Ollama actually do, in one sentence?
2.  Why has `base_url="http://localhost:11434/v1"` worked throughout
    this repository without an API key?
3.  Name three concrete reasons to run a model locally.
4.  What's the analogy between Ollama and a container runtime?

## Summary

Ollama is a local model runtime — it downloads, manages, and serves
LLMs through a simple API, wrapping `llama.cpp` the way a container
runtime wraps the low-level mechanics of running a container. Every
`localhost:11434` call throughout this repository has been hitting
this exact server, which is why running local, for the reasons module
01 and 03 already established, has been genuinely practical rather
than theoretical.

## Next Chapter

➡️ `02-Installing-and-Running-Ollama.md`
