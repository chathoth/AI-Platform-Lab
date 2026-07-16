# 02 - History of LLMs

## Introduction

As a Platform/DevOps engineer, I'm used to thinking in terms of
**evolution of infrastructure** — bare metal → VMs → containers →
Kubernetes → serverless. Each shift changed how we build, deploy, and
scale systems.

LLMs went through a very similar kind of evolution, except the thing
being scaled was **language understanding** instead of compute. Looking
at this history through a "platform" lens actually makes it click faster
than reading it as pure ML theory — every jump in model architecture
also caused a jump in how these things get deployed, served, and
operated, which is the part I actually care about day to day.

## Learning Objectives

After this chapter I should be able to:

-   Explain the major eras that led to today's LLMs.
-   Connect each era to a real architectural/deployment shift.
-   Explain why the Transformer (2017) was the turning point.
-   Explain what changed operationally between GPT-2, GPT-3, and
    ChatGPT-era models.
-   Relate this history to decisions I make when serving models today
    (self-hosted vs API, model registry, rollback, versioning).

------------------------------------------------------------------------

# The Timeline, the Way I'd Explain It to My Team

``` text
Rule-based systems (1950s-1980s)
        ↓
Statistical NLP / n-grams (1980s-2000s)
        ↓
Neural nets: RNN / LSTM (1997-2013)
        ↓
Word embeddings: Word2Vec, GloVe (2013)
        ↓
Transformer architecture (2017) ← the real inflection point
        ↓
GPT-1, BERT (2018)
        ↓
GPT-2 (2019) - "too dangerous to release" (at the time)
        ↓
GPT-3 (2020) - 175B params, few-shot learning
        ↓
InstructGPT / RLHF (2022) - models learn to follow instructions
        ↓
ChatGPT (Nov 2022) - the moment this became a product, not a paper
        ↓
GPT-4, Claude 2/3, Llama 2/3, Mixtral (2023-2024) - the multi-vendor era
        ↓
Claude 4/Opus family, reasoning models, agents, MCP (2024-2026)
```

## 1. Rule-Based Era (1950s-1980s)

Early NLP was hand-written rules: `if input contains "hello" → reply
"hi"`. ELIZA (1966) is the classic example — basically a giant
`switch/case` statement pretending to be a therapist.

**Platform analogy:** this is like managing infrastructure with shell
scripts and manual runbooks. It works for a narrow set of known cases
and breaks the moment reality doesn't match the rule.

## 2. Statistical NLP (1980s-2000s)

Instead of hand-written rules, models started learning **probabilities**
from text — n-gram models predicting "the next word" based on word
frequency counts. IBM's statistical translation work in the 90s is a
good example.

**Platform analogy:** this is like moving from manual scripts to config
management (Ansible/Puppet) — still deterministic and rule-driven, but
now data-informed instead of hand-authored.

## 3. Neural Networks: RNN / LSTM (1997-2013)

RNNs and later LSTMs (1997) let models keep a "memory" of earlier words
in a sequence, which mattered for translation and speech. The core
limitation: they process text **one token at a time, sequentially**, so
long sequences were slow to train and prone to losing earlier context.

**Platform analogy:** RNNs are like processing a request queue strictly
serially — correct, but you can't parallelize across the sequence.
That single constraint is exactly what the Transformer fixed.

## 4. Word Embeddings (2013)

Word2Vec and GloVe represented words as dense vectors so that
`king - man + woman ≈ queen`. This is the direct ancestor of the
embeddings covered in [05-Embeddings-Basics.md](05-Embeddings-Basics.md).

**Platform analogy:** this is the "give every entity a stable ID"
moment — like moving from free-text log messages to structured,
queryable telemetry. Once words are vectors, you can do math and search
on meaning instead of exact string match.

## 5. The Transformer (2017) — the real turning point

Google's paper *"Attention Is All You Need"* (2017) removed the
sequential bottleneck of RNNs. Instead of processing tokens one at a
time, the **attention mechanism** lets the model look at *all* tokens in
a sequence at once and weigh how relevant each one is to every other
one.

This is covered in depth in
[06-Transformer-Architecture.md](06-Transformer-Architecture.md) and
[07-Attention-Mechanism.md](07-Attention-Mechanism.md), but the
operational consequence is what matters here:

**Platform analogy:** this is the same jump as going from a single
long-running process to a **parallelizable, horizontally scalable
workload**. RNNs = one worker processing a queue in order. Transformers
= a batch job that fans out across GPUs. That parallelizability is the
entire reason training could scale to billions of parameters — it's an
infra unlock as much as an ML one.

## 6. GPT-1, BERT (2018) → GPT-2 (2019) → GPT-3 (2020)

-   **GPT-1 (2018):** proved a Transformer trained on next-token
    prediction, then fine-tuned, beat task-specific models.
-   **BERT (2018):** same architecture family, trained to understand
    context bidirectionally — great for search/classification, not for
    generation.
-   **GPT-2 (2019):** 1.5B params. OpenAI initially withheld full
    release citing misuse risk — the first time "model release" became
    a governance/ops decision, not just a research one.
-   **GPT-3 (2020):** 175B params. Showed **few-shot learning** — give
    it 2-3 examples in the prompt and it generalizes, no fine-tuning
    required. This is the moment "prompting" became a real interface.

**Platform analogy:** this stretch is like watching a service go from
"a script I run locally" to "a system that needs its own capacity
planning, rollout strategy, and access controls." Model size stopped
being an implementation detail and became an infra cost line item.

## 7. RLHF and InstructGPT (2022)

Raw GPT-3 was a next-token predictor — good at completion, bad at
following instructions. **InstructGPT** (2022) added Reinforcement
Learning from Human Feedback (RLHF): humans ranked model outputs, and
that ranking trained the model to prefer helpful, instruction-following
responses.

**Platform analogy:** this is the model equivalent of adding a
feedback/observability loop to a system — SRE-style "measure real
behavior, feed it back into the system" instead of shipping and hoping.

## 8. ChatGPT (November 2022) — the product moment

ChatGPT wasn't a new architecture — it was InstructGPT wrapped in a chat
UI. But it's the point where LLMs went from "research artifact" to
"100M+ users in weeks." Every platform team (including the kind of work
I do) suddenly had to answer: *do we call an API, self-host an open
model, or both?*

## 9. The Multi-Vendor Era (2023-2024)

GPT-4, Claude 2 → 3, Llama 2 → 3, Mistral/Mixtral, Gemini. This is when
the ecosystem stopped being "OpenAI or nothing" and became a real
market: closed APIs vs open weights, covered in
[15-Open-vs-Closed-Models.md](15-Open-vs-Closed-Models.md).

**Platform analogy:** this is exactly the "multi-cloud" moment for LLMs.
Same questions I already ask about AWS vs GCP now apply to model
providers: vendor lock-in, cost per request, latency, data residency,
rate limits, and whether I need an abstraction layer (a model gateway)
in front of them.

## 10. Reasoning Models, Agents, and MCP (2024-2026)

The most recent shift isn't just bigger models — it's models that plan,
call tools, and act as agents (extended "thinking" before answering,
function/tool calling, and standards like MCP for connecting models to
external systems). This is where the "AI-Platform-Lab" roadmap is
heading — Prompt Engineering → RAG → Agents.

**Platform analogy:** this is the shift from "a service that answers a
question" to "a service that can call *other* services on your behalf" —
which means it now needs the same guardrails I'd put on any autonomous
system: permissions, audit logs, rate limits, and a blast-radius plan.

------------------------------------------------------------------------

# History Mapped to Deployment Reality

  Era                    Year(s)      What changed                 How I'd have to operate it
  ----------------------- ----------- ----------------------------- -----------------------------------------
  Rule-based              1950s-80s   Hand-written logic            Shell script / runbook
  Statistical NLP         1980s-2000s Probabilities from data       Config-managed, deterministic
  RNN / LSTM              1997-2013   Sequential memory             Single-threaded worker, hard to scale
  Embeddings               2013       Words as vectors              First "semantic search" style workload
  Transformer              2017       Parallel attention            GPU-parallel batch training
  GPT-2                    2019       1.5B params                   Runs on a beefy single GPU (or CPU, slowly)
  GPT-3                    2020       175B params, few-shot         Needs a cluster; API-only for most teams
  InstructGPT / RLHF       2022       Instruction-following         Feedback loop added to training pipeline
  ChatGPT                  2022       Consumer product               Real SLAs, real traffic, real cost curves
  Multi-vendor era         2023-24    Open + closed model choice    Need a gateway/abstraction layer
  Agents / MCP             2024-26    Tool-calling, reasoning       Needs permissions, audit, blast-radius limits

------------------------------------------------------------------------

# Hands-on: Feel the Evolution Yourself

The fastest way I found to actually internalize this timeline is to run
an old-generation and a new-generation model side by side locally with
Ollama and compare them like I would compare two service versions.

``` bash
# pull a small, GPT-2-era-equivalent open model
ollama pull gpt2

# pull a modern instruction-tuned model
ollama pull llama3.1:8b

# compare disk footprint - same exercise as comparing container image sizes
du -sh ~/.ollama/models/*

# ask both the same instruction-following prompt
ollama run gpt2 "Write a haiku about Kubernetes."
ollama run llama3.1:8b "Write a haiku about Kubernetes."
```

What to notice, as a platform engineer:

-   `gpt2` will likely ignore the instruction and just continue the
    text pattern — no RLHF, no instruction tuning.
-   `llama3.1:8b` follows the instruction cleanly — the RLHF step from
    2022 is the direct reason for that difference.
-   Compare memory/CPU usage for both — this is the same resource
    curve I'd expect if I were sizing a node pool for either workload.

## Common Misconceptions

❌ ChatGPT was a brand-new architecture in 2022.
(It was InstructGPT + a chat UI — the underlying model class already
existed.)

❌ Bigger model = later date, always in a straight line.
(BERT and GPT-1 shipped the same year with different training
objectives — the timeline branches, it isn't strictly linear.)

❌ Open-source models are "behind" closed ones.
(By 2024 the gap on many practical tasks had narrowed enough that the
real decision is cost/latency/data-control, not raw capability — see
[15-Open-vs-Closed-Models.md](15-Open-vs-Closed-Models.md).)

✔ The single biggest inflection point is the 2017 Transformer paper —
everything since then is scaling and refining that one architectural
idea, not replacing it.

## Interview Questions

1.  What limitation of RNNs/LSTMs did the Transformer solve, and why
    did that matter for training at scale?
2.  What is RLHF, and what problem did it solve that GPT-3 alone
    didn't?
3.  Why was ChatGPT (2022) a bigger deal operationally than GPT-3
    (2020), even though it wasn't a new architecture?
4.  From an infra/ops point of view, what changed between the "one
    API provider" era and the "multi-vendor" era of 2023-2024?
5.  What new operational risks come with agentic/tool-calling models
    compared to plain text-completion models?

## Summary

The history of LLMs isn't just an ML research timeline — for me, it
reads as an infrastructure scaling story: from deterministic rule
engines, to statistical models, to sequential neural nets, to the
Transformer's parallelizable attention mechanism, to instruction-tuned
products, to today's multi-vendor, agentic, tool-calling systems. Every
architectural jump also forced a new operational pattern, and that
pattern is usually the part that ends up on my plate.

## Next Chapter

➡️ `03-How-LLMs-Work.md`
