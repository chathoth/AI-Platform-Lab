# 19 - Interview Questions

## Introduction

Every interview question from this module, grouped by chapter, with
the answer framed the way I'd actually say it. Review material — read
the chapters first.

------------------------------------------------------------------------

## Chapter 01 - What Ollama Is

**Q: What does Ollama actually do?**
It's a local model runtime — downloads, manages, and serves LLMs
through a simple API, wrapping `llama.cpp`'s inference engine the way
a container runtime wraps the low-level mechanics of running a
container.

## Chapter 02 - Installing and Running

**Q: What's the fastest way to confirm Ollama is running?**
`curl http://localhost:11434/api/tags` — real JSON back means it's up
and reachable.

## Chapter 03 - The CLI

**Q: What's the difference between `ollama list` and `ollama ps`?**
`list` shows what's on disk (every model ever pulled); `ps` shows
what's currently loaded in memory, verified directly by loading a
model and watching it appear in `ps` and disappear after `stop`.

## Chapter 04 - The Native REST API

**Q: What does the `load_duration` field in a response tell you?**
How much of total response time was spent loading the model versus
actually generating — useful for distinguishing a cold-load problem
from a genuine generation-speed problem.

## Chapter 05 - The OpenAI-Compatible Endpoint

**Q: Why does `api_key="ollama"` work with no real key?**
The OpenAI SDK requires a non-empty string to construct a client;
Ollama's server never actually checks its value — fine on localhost,
a real risk once exposed (chapter 15).

## Chapter 06 - Modelfiles

**Q: What does `ollama create -f Modelfile` actually do to the base
model's weights?**
Nothing — it builds a new configuration layer (system prompt,
parameters) on top of existing weights, verified directly by the build
output reusing existing layers with no re-training involved.

## Chapter 07 - Model Formats and Quantization

**Q: How would you check a specific model's real quantization level?**
`ollama show <model>` — verified directly, showing `Q4_K_M` for this
module's `llama3.1:8b`.

## Chapter 08 - Managing the Model Library

**Q: What happens when you re-pull an already-pulled tag?**
Ollama checks for upstream changes first — if nothing changed, it
completes almost instantly instead of re-downloading everything, the
same idempotent behavior as re-pulling an unchanged Docker image tag.

## Chapter 09 - GPU vs. CPU

**Q: What's the fastest way to diagnose unexpectedly slow generation?**
`ollama ps`'s `PROCESSOR` column — a CPU fallback (verified as a real,
observable state) is often the single biggest speed factor.

## Chapter 10 - Context Length and Memory

**Q: Why does a larger context window cost memory even for a short
prompt?**
It reserves KV-cache memory sized to the configured window, not the
actual prompt length — verified directly: `num_ctx=32768` measurably
increased reported memory usage from 5.3GB to 9.1GB for the same short
prompt.

## Chapter 11 - Concurrency and Multiple Models

**Q: What happens when loading a new model would exceed available
memory?**
Ollama evicts the least-recently-used model automatically — the same
LRU behavior as any resource-constrained cache.

## Chapter 12 - Embeddings via Ollama

**Q: How do you confirm a model is actually suited for embeddings?**
`ollama show` — an embedding model's Capabilities section won't list
`completion`, distinguishing it from a chat model.

## Chapter 13 - Streaming Responses

**Q: Does streaming make generation faster overall?**
No — it changes when the first output becomes visible, not total
generation time, verified by comparing streamed and non-streamed
total timing for the same prompt.

## Chapter 14 - Running as a Service

**Q: How would you confirm a service setup actually survives a
restart?**
Restart the service, then run the same `curl` check from chapter 02
again — "installed" doesn't guarantee "configured to start
automatically."

## Chapter 15 - Security

**Q: Why is `OLLAMA_HOST=0.0.0.0` a security decision, not a
convenience toggle?**
Ollama has no built-in authentication — network exposure without a
real access-control layer (a reverse proxy, firewall rules) lets
anyone reachable run inference, pull or delete models, and consume
your compute.

## Chapter 16 - Performance Tuning

**Q: What two things should you check before touching a performance
setting?**
`ollama ps` (GPU/CPU placement) and the response's timing fields
(load vs. generation duration) — diagnose the actual bottleneck before
guessing at a fix.

## Chapter 17 - Ollama vs. Other Local Runtimes

**Q: Why does this repository use Ollama specifically?**
Consistency and low setup cost across many different modules — the
same reasoning module 04 chapter 03 applied to choosing ChromaDB among
vector database options.

## Chapter 18 - Best Practices

**Q: Name one practice in this checklist backed by a directly
verified finding.**
Right-sizing `num_ctx` — verified that a larger context window
measurably increases memory usage even for a short prompt, not just
theoretically.

------------------------------------------------------------------------

## Rapid-Fire Round

1.  Ollama — a local model runtime wrapping `llama.cpp`.
2.  `ollama list` vs. `ollama ps` — disk inventory vs. memory-resident.
3.  `ollama show` — ground truth for a model's real capabilities.
4.  Modelfile — a configuration layer, not a re-training.
5.  Quantization — checkable directly, not just inferred from a tag
    name.
6.  GPU vs. CPU — checkable via `ollama ps`, the biggest speed factor.
7.  `num_ctx` — real memory cost, verified directly.
8.  `keep_alive` — trades reload cost against held memory.
9.  Security — no auth by default, dangerous once network-exposed.
10. Performance tuning — measure first, then tune the specific
    bottleneck.

## Next Chapter

➡️ `20-Glossary.md`
