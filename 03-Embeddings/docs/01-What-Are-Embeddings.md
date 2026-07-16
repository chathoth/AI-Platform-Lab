# 01 - What Are Embeddings (Recap and Depth)

## Introduction

Module 01 chapter 05 introduced embeddings as vectors positioned by
meaning, and compared them to a different kind of search index. This
chapter is where that idea gets load-bearing — everything else in this
module builds directly on it, so I want the mental model to be solid
before adding chunking, storage, clustering, and evaluation on top.

## Learning Objectives

After this chapter I should be able to:

-   Explain, precisely, what a number inside an embedding vector
    represents.
-   Explain why embeddings enable comparison that raw text can't.
-   Distinguish an embedding model from a chat/completion model.

------------------------------------------------------------------------

# A Vector Is a Position, Not a Label

``` text
"Kubernetes"              → [0.12, -0.45, 0.88, ..., 0.03]   (768 numbers)
"container orchestration" → [0.14, -0.42, 0.85, ..., 0.05]   (nearby!)
"banana"                   → [0.91,  0.02, -0.77, ..., 0.66]  (far away)
```

No single number in that vector "means" anything on its own — there's no
dimension labeled "is-about-kubernetes." What matters is the vector's
**position relative to every other vector** produced by the same model.
Closeness in that space is what encodes similarity of meaning, learned
entirely from patterns of what text tends to appear near what other
text during training.

**Platform analogy:** this is closer to a hash than a label, but a
*meaningful* hash — two inputs that mean similar things land at similar
coordinates, the way two servers in the same rack get similar IP
ranges. No one coordinate tells you the rack; the neighborhood does.

## Why This Enables Comparison That Text Can't

Raw text can only be compared by exact or fuzzy string match — `grep`,
`LIKE '%disk%'`, edit distance. None of those understand that
`"CrashLoopBackOff"` and `"pod keeps restarting"` are describing the
same situation with zero shared substrings. An embedding model was
trained on enough real-world text that it learned these two phrases
tend to occur in similar contexts, and places their vectors close
together as a result — comparison becomes **math on coordinates**
instead of pattern matching on characters.

## Embedding Models Are Not Chat Models

This is the distinction most worth nailing down before going further:

  Chat / completion model (`llama3.1:8b`)   Embedding model (`nomic-embed-text`)
  ------------------------------------------ ---------------------------------------
  Input: text → Output: more text             Input: text → Output: a fixed-length vector
  Generates, one token at a time (module 01 ch. 03) | Encodes the whole input in one pass, no generation loop
  Used for: answering, summarizing, chatting    Used for: search, comparison, clustering
  Bigger, slower, more expensive generally       Smaller, faster, cheaper generally

Trying to use a chat model for "give me a vector for this text" or an
embedding model for "answer this question" both miss the point of what
each was actually trained to do — they're different tools for different
jobs, the same way a hashing function and a text generator solve
unrelated problems even though both take text as input.

## Hands-on: Generate Your First Embedding, Locally

``` bash
ollama pull nomic-embed-text
```

``` python
import requests

response = requests.post("http://localhost:11434/api/embeddings", json={
    "model": "nomic-embed-text",
    "prompt": "The pod is stuck in CrashLoopBackOff",
})

vector = response.json()["embedding"]
print(f"Vector length: {len(vector)}")
print(f"First 5 numbers: {vector[:5]}")
```

Run it twice with the exact same input and confirm the vector is
identical both times (embedding, unlike chat generation, has no
temperature/sampling — same input always gives the same output). Then
run it against `"banana bread recipe"` and just eyeball how different
the numbers look — that's the same intuition chapter 05 builds on with
actual similarity math.

## Common Misconceptions

❌ An embedding is a compressed version of the text you can decode back.
(It's a one-way projection into a coordinate space — there's no
built-in way to reconstruct the original text from the vector alone.)

❌ Any model can produce embeddings if you just ask it to.
(Chat models are trained for generation; embedding models are trained
specifically so that distance in vector space reflects semantic
similarity — a chat model asked to "output a vector" won't have that
property.)

✔ The only thing that matters about an embedding vector is its position
*relative to other vectors from the same model* — never compare vectors
produced by two different embedding models, they don't share a
coordinate system.

## Interview Questions

1.  What does a single number inside an embedding vector represent?
2.  Why can't two embeddings from different models be meaningfully
    compared to each other?
3.  What's the fundamental difference in what a chat model and an
    embedding model each output?
4.  Why does the same text always produce the same embedding, with no
    variation between calls?

## Summary

An embedding is a position in a learned coordinate space where distance
reflects semantic similarity — not a label, not a compressed copy of
the text, and not something a chat model produces. Embedding models are
purpose-built, smaller, and deterministic, in contrast to the
generative, sampling-based chat models covered in module 01 and 02.

## Next Chapter

➡️ `02-How-Embedding-Models-Are-Trained.md`
