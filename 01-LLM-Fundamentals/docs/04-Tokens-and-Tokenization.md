# 04 - Tokens and Tokenization

## Introduction

Every cost dashboard, rate limit, and context-window error I'll ever
debug on an LLM platform traces back to one unit: the **token**. If I
had to pick the single most operationally important concept in this
whole module, it's this one — tokens are the "request unit" of LLMs the
same way vCPU-seconds or API calls-per-minute are the billing/limit unit
for the infra I'm used to.

## Learning Objectives

After this chapter I should be able to:

-   Explain what a token is and why it isn't "a word."
-   Explain subword tokenization (BPE) and why it exists.
-   Count tokens for a given input using `tiktoken`.
-   Explain how tokenization drives cost, rate limits, and context
    window usage.

------------------------------------------------------------------------

# What Is a Token?

A token is a chunk of text — sometimes a whole word, sometimes part of
a word, sometimes a single character or punctuation mark. Models don't
read words; they read **token IDs**, integers mapped to entries in a
fixed vocabulary (typically 50K-200K entries depending on the model).

``` text
"Kubernetes deploys containers"
        ↓ tokenizer
["Kub", "ernetes", " deploys", " containers"]
        ↓ vocabulary lookup
[42891, 7801, 21340, 17023]
```

Notice `"Kubernetes"` split into two tokens — it's not common enough in
general training text to earn its own single token, unlike `"the"` or
`"and"`. Domain-specific/technical vocabulary (Kubernetes, kubectl,
Terraform, Prometheus) often costs *more* tokens than plain English
words for exactly this reason — worth knowing before you assume "short
prompt = cheap prompt."

## Why Subwords, Not Whole Words? (Byte-Pair Encoding)

A whole-word vocabulary would need millions of entries to cover every
language, typo, and made-up product name, and would still fail on
anything unseen. **Byte-Pair Encoding (BPE)** solves this by building
the vocabulary from the most frequent character/subword pairs in the
training corpus — common words become single tokens, rare/unseen words
get broken into smaller known pieces, and literally *any* string can
still be tokenized (worst case, one token per byte).

**Platform analogy:** this is the same trade-off as choosing a cache key
strategy — a whole-word vocabulary is like caching only exact URLs
(great hit rate for common paths, total miss on anything new). BPE is
like caching path *segments* — you always get partial hits, so nothing
is ever a total cache miss, at the cost of doing a bit more lookup work
per request.

## Tokens Drive Cost, Limits, and Context — Directly

This is the part that matters when I'm the one sizing a deployment or
setting a budget alert:

-   **Cost:** API pricing is per-1K/1M input and output tokens — same
    shape as egress-GB pricing on cloud providers.
-   **Rate limits:** most providers cap **tokens per minute (TPM)** in
    addition to requests per minute (RPM) — I've been throttled on TPM
    while nowhere near the RPM limit.
-   **Context window:** the model has a hard cap on total tokens
    (prompt + response combined) — see
    [09-Context-Window.md](09-Context-Window.md). Blow past it and the
    call fails or gets silently truncated, same failure mode as a
    payload-size limit on a load balancer.

## Hands-on: Count Tokens Like You'd Size a Payload

``` python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4")

text = "kubectl apply -f deployment.yaml --namespace production"
tokens = enc.encode(text)

print(f"Token count: {len(tokens)}")
print(f"Tokens: {[enc.decode([t]) for t in tokens]}")
```

Try this with a chunk of your own `values.yaml`, a Terraform block, or a
raw log line — compare the token count to the word count. Structured
config (YAML/JSON with lots of punctuation, indentation, and repeated
symbols) almost always tokenizes worse (more tokens per character) than
plain prose. That's directly useful the day you're deciding whether to
paste a whole log file into a prompt or pre-filter it first.

``` bash
# rough token estimate from the CLI without writing a script
ollama run llama3.1:8b --verbose "test" 2>&1 | grep -i "eval count"
```

## Common Misconceptions

❌ 1 token ≈ 1 word.
(Rule of thumb is closer to 1 token ≈ 4 characters / ~0.75 words in
English — and it's worse for code, YAML, and non-English text.)

❌ Shorter-looking prompts are always cheaper.
(A short prompt full of technical identifiers/YAML can tokenize to more
tokens than a longer plain-English sentence.)

✔ Tokenization is deterministic and model-specific — the same string
can tokenize differently across GPT, Claude, and Llama tokenizers,
which is why token counts aren't directly comparable across providers.

## Interview Questions

1.  What is a token, and why isn't it the same as a word?
2.  What problem does Byte-Pair Encoding solve that a whole-word
    vocabulary doesn't?
3.  Name three operational limits that are measured in tokens, not
    requests.
4.  Why might a YAML/JSON payload use more tokens than an equivalent
    plain-English sentence?

## Summary

Tokens are the real unit of cost, throughput, and capacity in any LLM
system — the same role vCPU-seconds or request units play in
traditional infra billing. Subword tokenization (BPE) is what lets a
fixed vocabulary handle unlimited text without ever fully failing, at
the cost of technical/domain vocabulary often costing more tokens than
expected.

## Next Chapter

➡️ `05-Embeddings-Basics.md`
