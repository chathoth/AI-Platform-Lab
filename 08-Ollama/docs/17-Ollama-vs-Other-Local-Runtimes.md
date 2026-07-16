# 17 - Ollama vs. Other Local Runtimes

## Introduction

Module 04 chapter 03 walked through the vector database landscape
honestly instead of assuming one universal answer. This chapter does
the same for local model runtimes — Ollama is what this entire
repository uses, deliberately, but it's worth knowing what else exists
and why.

## Learning Objectives

After this chapter I should be able to:

-   Name the major local model runtime options besides Ollama.
-   Explain what each is better at.
-   Justify Ollama as this repository's choice, honestly.

------------------------------------------------------------------------

# The Landscape

  Tool           What it is                                Best for
  ------------------ ------------------------------------------ --------------------------------
  Ollama                A friendly wrapper around `llama.cpp`      Ease of use, quick setup, good defaults - this repository's choice
  `llama.cpp`             The underlying inference engine itself     Maximum control, custom builds, embedding into other software
  LM Studio                A GUI application wrapping `llama.cpp`       Non-technical users, visual model browsing/chat
  vLLM                       A high-throughput serving engine               Production-scale serving, especially multi-request throughput
  text-generation-webui        A feature-rich web UI for local models          Experimentation with many models/settings in one UI

## Why This Repository Uses Ollama Specifically

**Simple, consistent API** — the same `localhost:11434` pattern (and
its OpenAI-compatible layer, chapter 05) worked identically across
every module from 01 through 07, with zero per-module setup changes.

**Good defaults** — automatic GPU detection (chapter 09), sensible
quantization defaults (chapter 07), and model management (chapter 08)
that "just works" without hand-tuning `llama.cpp` build flags.

**CLI and API both genuinely usable** — `ollama run` for quick
interactive testing, the REST API (chapter 04) for real applications —
covering both this repository's hands-on exercises and its example
scripts without needing a second tool.

## What You'd Reach for Instead, and Why

``` text
Need maximum control over the inference engine itself, custom builds,
or embedding inference directly into another application's binary?
        → llama.cpp directly

Want a GUI for non-technical exploration, no terminal required?
        → LM Studio

Need to serve many concurrent users at production scale, optimized
specifically for throughput?
        → vLLM (though this typically targets GPU server deployments,
          not the local laptop setups this repository focuses on)

Want to experiment with many different models and settings through
one browser-based interface?
        → text-generation-webui
```

**Platform analogy:** this is the same landscape shape as module 04
chapter 03's vector database comparison — a friendly, well-defaulted
option (Ollama, like Chroma) for learning and small-to-medium use,
versus more specialized tools that trade ease-of-use for control or
scale at the high end.

## Hands-on: Confirm What You'd Actually Miss Without Ollama

Take one of this repository's example scripts (any module 01-07
example calling `localhost:11434`) and consider: what would need to
change to point it at raw `llama.cpp`'s server mode instead? The
`base_url` would change, but the OpenAI-compatible request/response
shape (chapter 05) is close enough across several of these tools that
the *application code* often barely needs to change — worth
recognizing, since it means the choice of runtime is more reversible
than it might first appear.

## Common Misconceptions

❌ Ollama is the only way to run models locally.
(It's the friendliest, most consistent option for this repository's
purposes — `llama.cpp` directly, LM Studio, vLLM, and others all serve
different points on the same ease-of-use-versus-control spectrum.)

❌ Choosing Ollama locks you into it permanently.
(Because several of these tools expose an OpenAI-compatible API
surface, switching runtimes often means changing a `base_url`, not
rewriting application code — the choice is more reversible than it
looks.)

✔ Ollama's value in this repository specifically was consistency and
low setup cost across many different modules and examples — the same
reasoning that would apply to choosing any well-defaulted tool for a
learning-focused, broad-coverage project.

## Interview Questions

1.  Name three local model runtime options besides Ollama and what
    each is best suited for.
2.  Why does this repository use Ollama specifically?
3.  When would `llama.cpp` directly be a better choice than Ollama?
4.  Why is switching between OpenAI-compatible local runtimes often
    less disruptive than it initially seems?

## Summary

Ollama sits at the friendly, well-defaulted end of the local model
runtime spectrum — the same role Chroma plays among vector databases
(module 04 chapter 03) — chosen for this repository specifically for
its consistent API and low setup cost across many modules.
`llama.cpp` directly, LM Studio, vLLM, and text-generation-webui each
trade that ease of use for more control, a GUI, production-scale
throughput, or broader experimentation respectively.

## Next Chapter

➡️ `18-Best-Practices.md`
