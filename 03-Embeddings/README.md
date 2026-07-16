# 03 - Embeddings

> Turning text into numbers you can search, compare, and cluster —
> entirely on your own machine.

## Overview

Module 01 introduced embeddings as "a different kind of search index —
keyed by meaning instead of exact words." This module goes deep on that
one idea, because it's the foundation everything after it is built on:
Vector Databases (module 04) store embeddings, RAG (module 05)
retrieves by embedding similarity, and AI Agents (module 07) use the
same mechanism to recall relevant memory.

Everything in this module runs against a **local embedding model via
Ollama** — no API key, no cost, no data leaving your machine. That's
deliberate: embeddings are the one place in this whole repo where
running locally is not just cheaper, it's often the *right* choice —
you're usually embedding your own internal documents, and a local model
means that data never has to leave your network.

## Learning Objectives

After completing this module you will be able to:

-   Explain how an embedding model turns text into a vector, and why
    that's different from a chat/completion model.
-   Choose a similarity metric and understand what it actually measures.
-   Chunk and embed real-world content (logs, YAML, runbooks, code).
-   Build a working semantic search engine with nothing but a Python
    list and cosine similarity.
-   Cluster, deduplicate, and classify text using embeddings alone.
-   Evaluate whether an embedding-based search is actually working.
-   Know when embeddings are the wrong tool.

## Prerequisites

-   [01-LLM-Fundamentals](../01-LLM-Fundamentals/) — specifically
    chapter 05 (Embeddings Basics), which this module expands on in
    depth.
-   [02-Prompt-Engineering](../02-Prompt-Engineering/) — helpful but
    not required; this module is mostly about the retrieval side, not
    the generation side.

## Repository Structure

``` text
docs/
examples/
notebooks/
```

## Chapters

  Chapter   Topic
  --------- ---------------------------------------
  01        What Are Embeddings (Recap and Depth)
  02        How Embedding Models Are Trained
  03        The Embedding Model Landscape
  04        Vector Space and Dimensionality
  05        Similarity Metrics
  06        Generating Embeddings Locally with Ollama
  07        Chunking Before Embedding
  08        Embedding Different Content Types
  09        Storing Embeddings
  10        Building Semantic Search From Scratch
  11        Embedding Drift and Model Versioning
  12        Clustering With Embeddings
  13        Deduplication With Embeddings
  14        Classification With Embeddings
  15        Hybrid Search (Keyword + Semantic)
  16        Evaluating Embedding Quality
  17        Cost and Performance at Scale
  18        Best Practices
  19        Interview Questions
  20        Glossary

## Learning Roadmap

``` text
LLM Fundamentals
        ↓
Prompt Engineering
        ↓
Embeddings                  ← you are here
        ↓
Vector Databases
        ↓
RAG
        ↓
AI Agents
```

## Hands-on Labs

-   Generate an embedding locally and inspect its raw shape.
-   Compare cosine similarity across related and unrelated text.
-   Chunk a real document and embed each chunk.
-   Build a semantic search engine over a folder of runbooks, using
    only Python and numpy.
-   Cluster a batch of incident titles into groups without any labels.
-   Find near-duplicate tickets using embedding similarity.
-   Measure recall@k for a small search evaluation set.

## Technologies

-   Python
-   Ollama (`nomic-embed-text` for embeddings, `llama3.1:8b` where a
    chat model is also needed)
-   numpy
-   Jupyter

## Expected Outcome

You will be able to build a working semantic search or classification
system entirely on local infrastructure, and know exactly what
trade-offs you're making — before moving on to Vector Databases, where
these same embeddings get stored and queried at scale instead of held
in a Python list.

## Next Module

➡️ `04-Vector-Databases`
