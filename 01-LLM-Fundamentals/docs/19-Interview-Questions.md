# 19 - Interview Questions

## Introduction

A consolidated set of every interview question from this module,
grouped by chapter, plus the answer framed the way I'd actually say it
out loud — through the platform/DevOps analogies that made each concept
stick for me. Meant as review before a system-design or AI-platform-
flavored interview, not as first-pass learning material.

------------------------------------------------------------------------

## Chapter 01 - What is an LLM

**Q: What is an LLM, in one sentence?**
A Transformer-based neural network trained to predict the next token in
a sequence, at a scale (billions of parameters, massive training data)
that gives it broad language and reasoning ability.

**Q: How is an LLM different from traditional software?**
Traditional software runs fixed, explicitly written logic
(deterministic). An LLM is probability-based — it learned patterns from
data and generates the statistically likely continuation, which can
vary between calls.

## Chapter 02 - History of LLMs

**Q: What was the single biggest inflection point in LLM history?**
The 2017 Transformer paper ("Attention Is All You Need") — it replaced
RNNs' sequential processing with parallelizable self-attention, which
is what made training at massive scale feasible.

**Q: What changed operationally with ChatGPT's 2022 launch, if the
underlying model wasn't new?**
It went from "API only, dev-facing" to "consumer product with real
SLAs, real traffic, real cost curves" — a governance/ops shift, not an
architecture shift.

## Chapter 03 - How LLMs Work

**Q: Why is LLM generation described as autoregressive?**
Because each output token is produced by one full forward pass, then
fed back in as input for the next token — a loop, not a single
computation.

## Chapter 04 - Tokens and Tokenization

**Q: Why isn't a token the same as a word?**
Subword tokenization (BPE) splits text into frequency-based chunks —
common words are single tokens, rare/technical words split into
multiple pieces. This lets a fixed vocabulary handle any input, at the
cost of unpredictable token counts for niche text.

## Chapter 05 - Embeddings Basics

**Q: How can two pieces of text be "similar" with zero shared words?**
Embeddings encode meaning as position in a high-dimensional vector
space, learned from co-occurrence patterns in training data — semantic
closeness, not lexical overlap.

## Chapter 06 - Transformer Architecture

**Q: What's the practical difference between encoder-only and
decoder-only models?**
Encoder-only (BERT) is for understanding/classification tasks.
Decoder-only (GPT, Claude, Llama — nearly every model used for chat) is
for generation, attending only to previous tokens (causal attention).

## Chapter 07 - Attention Mechanism

**Q: Why does attention cost scale roughly quadratically with sequence
length, and why does that matter?**
Every token attends to every other token, so cost grows with the square
of sequence length. It's the direct cause of why long-context requests
are slower and more expensive, and why KV-caching exists.

## Chapter 08 - Training vs Inference

**Q: Does a model "remember" a conversation by default?**
No — inference is stateless with respect to the model's weights.
Anything resembling memory is the application layer re-sending history
on every call.

## Chapter 09 - Context Window

**Q: What counts toward the context window?**
Input tokens plus output tokens combined, not just the prompt — and for
multi-turn chat, that includes the full re-sent conversation history
each turn.

## Chapter 10 - Temperature, Top-P, Sampling

**Q: When would you use temperature=0 vs. temperature=0.9?**
0 for anything programmatic/structured that needs consistent, testable
output. Higher for human-facing, creative, or brainstorming use cases
where variety is the goal.

## Chapter 11 - Hallucinations

**Q: Why is hallucination more dangerous than a typical error response?**
There's no error code or failed status — a hallucinated answer looks
exactly like a correct one, confidently stated. It has to be caught by
grounding (RAG) or verification, not by checking for a failure signal.

## Chapter 12 - Model Parameters

**Q: Roughly how much memory does a 70B model need at fp16?**
About 2 bytes per parameter, so ~140GB — the direct driver of hardware
sizing for self-hosting.

## Chapter 13 - Quantization

**Q: What does quantization trade off?**
Lower numeric precision per parameter for lower memory footprint and
faster compute, at some cost to accuracy — most noticeable on precise
math/logic tasks, usually negligible for conversational tasks.

## Chapter 14 - Fine-Tuning vs RAG

**Q: When would you choose fine-tuning over RAG?**
When you're teaching a stable behavior, tone, or output format — not
injecting facts. For frequently changing or citable knowledge, RAG is
almost always the right tool.

## Chapter 15 - Open vs Closed Models

**Q: When does self-hosting an open-weight model make financial sense
over a closed API?**
When token volume is high and steady enough that fixed GPU infra cost
beats pay-per-token pricing — the same reserved-vs-on-demand math used
for regular cloud infra.

## Chapter 16 - Prompt Lifecycle

**Q: What's the single most valuable debug log in an LLM pipeline?**
The fully assembled prompt right before it's sent to the model — system
prompt + history + RAG context + user input — since most "why did it
say that" bugs live in that assembly step.

## Chapter 17 - LLM Limitations

**Q: What is prompt injection, and what's it analogous to?**
Untrusted content in the prompt containing instructions designed to
override the system prompt — the LLM-era equivalent of SQL injection,
fixed the same way: treat external content strictly as data, never as
commands.

## Chapter 18 - Best Practices

**Q: Why should model versions be pinned?**
Providers update models continuously — an unpinned model reference can
mean behavior silently shifts under you, the same risk as floating on a
`latest` Docker tag instead of a fixed version.

------------------------------------------------------------------------

## Rapid-Fire Round

1.  Token vs. word — different, subword-based.
2.  Embedding vs. token — token is discrete ID, embedding is a dense
    meaning vector.
3.  Training vs. inference — build vs. run.
4.  Context window — combined input+output token ceiling per request.
5.  Temperature — randomness dial on token sampling.
6.  Quantization — precision-for-memory trade-off.
7.  RAG — retrieval at request time, no weight changes.
8.  Fine-tuning — weight changes via further training.
9.  Hallucination — confident, plausible, wrong — no error signal.
10. Prompt injection — untrusted data overriding instructions.

## Next Chapter

➡️ `20-Glossary.md`
