# 20 - Glossary

## Introduction

Every term from this module, alphabetical, defined the way I actually
think about it, with the analogy that made it stick attached.

------------------------------------------------------------------------

**GGUF** — The file format `llama.cpp` (and Ollama) uses to store a
model's weights, metadata, and tokenizer in one file. See
[07-Model-Formats-and-Quantization.md](07-Model-Formats-and-Quantization.md).

**`keep_alive`** — A request or Modelfile parameter controlling how
long a model stays loaded in memory after use before being unloaded.
See [16-Performance-Tuning.md](16-Performance-Tuning.md).

**`llama.cpp`** — The underlying C++ inference engine Ollama wraps; a
local runtime option in its own right. See
[17-Ollama-vs-Other-Local-Runtimes.md](17-Ollama-vs-Other-Local-Runtimes.md).

**Modelfile** — A text file defining a custom model as a configuration
layer (system prompt, parameters) on top of an existing base model's
weights. See
[06-Modelfiles-Customizing-a-Model.md](06-Modelfiles-Customizing-a-Model.md).

**`num_ctx`** — The parameter controlling a model's active context
window size, with a direct, verified memory cost. See
[10-Context-Length-and-Memory.md](10-Context-Length-and-Memory.md).

**Ollama** — A local model runtime that downloads, manages, and serves
LLMs through a simple HTTP API. See
[01-What-Ollama-Is-and-Why-Run-Models-Locally.md](01-What-Ollama-Is-and-Why-Run-Models-Locally.md).

**`OLLAMA_HOST`** — The environment variable controlling what address
Ollama's server binds to — `127.0.0.1` (localhost-only, safe default)
versus `0.0.0.0` (network-reachable, needs real authentication in
front of it). See
[15-Security-Exposing-Ollama-Beyond-Localhost.md](15-Security-Exposing-Ollama-Beyond-Localhost.md).

**`OLLAMA_NUM_PARALLEL`** — An environment variable controlling how
many requests Ollama handles concurrently. See
[11-Concurrency-and-Multiple-Models.md](11-Concurrency-and-Multiple-Models.md).

**`ollama ps`** — The CLI command showing models currently loaded in
memory, their processor placement, and active context size. See
[03-The-Ollama-CLI.md](03-The-Ollama-CLI.md).

**`ollama show`** — The CLI command revealing a model's real
specifications: architecture, parameters, context length,
quantization, and capabilities. See
[03-The-Ollama-CLI.md](03-The-Ollama-CLI.md).

**OpenAI-Compatible Endpoint (`/v1`)** — Ollama's compatibility layer
accepting and returning OpenAI-shaped requests, letting existing
OpenAI SDK code work against a local model unmodified. See
[05-The-OpenAI-Compatible-Endpoint.md](05-The-OpenAI-Compatible-Endpoint.md).

**Quantization Level** — How many bits per parameter a model is
stored at (e.g. `Q4_K_M`), readable directly via `ollama show`. See
[07-Model-Formats-and-Quantization.md](07-Model-Formats-and-Quantization.md).

**Streaming** — Receiving generated tokens incrementally as they're
produced, rather than waiting for the complete response — improves
perceived latency, not total generation time. See
[13-Streaming-Responses.md](13-Streaming-Responses.md).

------------------------------------------------------------------------

## Module Complete

That closes out all 20 chapters of **08-Ollama**. Next up per the
[root README](../../README.md) roadmap:

➡️ `09-LangChain`
