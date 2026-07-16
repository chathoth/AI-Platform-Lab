# 02 - How Embedding Models Are Trained

## Introduction

I don't need to train an embedding model to use one effectively, but
knowing roughly how they're trained explains *why* they behave the way
they do — specifically, why they're good at general similarity and can
be surprisingly bad at your specific domain's jargon without help. This
is the same reason it helps to understand roughly how a load balancer's
health check algorithm works even if I never write one myself.

## Learning Objectives

After this chapter I should be able to:

-   Explain contrastive training at a conceptual level.
-   Explain why embedding models trained on general web text can
    struggle with narrow technical/internal vocabulary.
-   Know when fine-tuning or choosing a domain-specific model matters.

------------------------------------------------------------------------

# Contrastive Training, in Plain Terms

Embedding models are mostly trained with **contrastive learning**: the
model is shown pairs of text known to be related (a question and its
correct answer, two sentences from the same paragraph) and pairs known
to be unrelated, and adjusts its output vectors so related pairs land
closer together and unrelated pairs land farther apart.

``` text
Related pair (pull closer):
  "How do I restart a Kubernetes pod?"
  "kubectl delete pod <name> lets the deployment recreate it"

Unrelated pair (push apart):
  "How do I restart a Kubernetes pod?"
  "Best pizza toppings for a party"
```

Millions of these pairs, repeated over training, is what shapes the
vector space so that semantically related text ends up nearby — the
model was never told what "Kubernetes" *means*, it just learned the
statistical shape of what tends to appear near what.

**Platform analogy:** this is like inferring a service dependency graph
purely from traffic patterns — you never read the code, you just notice
service A's requests are always followed by service B's, over and over,
until the *pattern* of co-occurrence reveals the relationship. Embedding
training does the same thing with text instead of network calls.

## Why General Models Can Miss Your Domain

Most popular embedding models are trained heavily on general web text,
Wikipedia, books, and public code — not your company's internal
runbooks, ticket conventions, or product-specific acronyms. This
produces a predictable gap:

``` text
General term:        "database" and "storage" -> embeds well, common on the web
Internal shorthand:  "the P1 board" or your team's specific incident
                      severity codes -> may not cluster meaningfully,
                      because the model never saw that pattern enough
                      times during training to learn it
```

This is the direct embedding-side analog of module 01 chapter 11's
hallucination problem — a knowledge gap the model has no way to signal
on its own. It doesn't throw an error; it just quietly produces a less
useful vector.

## What To Do About the Gap

  Option                                 When it's worth it
  --------------------------------------- ---------------------------------------
  Use a general model as-is                Most cases — the gap is usually small enough not to matter
  Fine-tune an embedding model on your data  High-volume, high-stakes internal search (rare to need this)
  Normalize/expand internal jargon before embedding | Cheap, effective: expand "P1" to "Priority 1 - Severity Critical" in text before embedding

That third option is the one I actually reach for most: a small text
pre-processing step that expands internal shorthand into plain language
before it ever hits the embedding model — cheaper than fine-tuning, and
it directly targets the specific gap instead of trying to retrain
general behavior.

## Hands-on: Feel the Gap

``` python
import requests
import numpy as np

def embed(text):
    r = requests.post("http://localhost:11434/api/embeddings", json={"model": "nomic-embed-text", "prompt": text})
    return np.array(r.json()["embedding"])

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

a = embed("database connection pool exhausted")
b = embed("pgbouncer ran out of connections")
c = embed("the P1 board needs review")
d = embed("Priority 1, Severity Critical incidents needing review")

print("common terms, related concepts: ", cosine(a, b))
print("internal shorthand, expanded:    ", cosine(c, d))
```

The first pair (common infra terms) usually scores meaningfully higher
similarity than you'd expect from raw string overlap. Try substituting
your own team's actual shorthand for the second pair and see how much
the expanded, plain-language version changes the outcome for a real
search query.

## Common Misconceptions

❌ An embedding model "understands" text the way a person does.
(It encodes statistical co-occurrence patterns learned from training
data — extremely useful, but not comprehension, same caveat as module
01 chapter 11 makes about chat models.)

❌ Every embedding model will handle your internal jargon equally well.
(Models trained on different corpora have different blind spots —
worth spot-checking on your own vocabulary before trusting a model for
production search.)

✔ The cheapest fix for a jargon gap is usually expanding shorthand into
plain language before embedding — not fine-tuning a whole new model.

## Interview Questions

1.  What is contrastive training, in your own words?
2.  Why might an embedding model perform worse on internal company
    jargon than on general technical terms?
3.  What's a low-effort mitigation for the jargon gap, before reaching
    for fine-tuning?
4.  How is inferring meaning from co-occurrence similar to inferring a
    service dependency graph from traffic patterns?

## Summary

Embedding models learn to place related text close together and
unrelated text far apart, through contrastive training on huge numbers
of example pairs — which means their quality on any given domain
depends heavily on how well-represented that domain was in training.
Internal jargon is a common blind spot, and expanding shorthand into
plain language before embedding is usually a cheaper fix than
fine-tuning a new model.

## Next Chapter

➡️ `03-The-Embedding-Model-Landscape.md`
