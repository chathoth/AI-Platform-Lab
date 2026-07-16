# 01 - What is an LLM?

## Introduction

Large Language Models (LLMs) are neural networks trained on enormous
collections of text to predict the next token in a sequence. This simple
objective enables them to answer questions, write code, summarize
documents, translate languages, and assist with reasoning tasks.

## Learning Objectives

After this chapter you should be able to:

-   Define an LLM.
-   Explain why it is called **Large Language Model**.
-   Distinguish AI, Machine Learning, Deep Learning, and LLMs.
-   Describe next-token prediction.

------------------------------------------------------------------------

# From AI to LLMs

``` text
Artificial Intelligence
        ↓
Machine Learning
        ↓
Deep Learning
        ↓
Transformers
        ↓
Large Language Models
```

## What does "Large Language Model" mean?

### Large

Modern models contain billions (sometimes trillions) of parameters
learned during training.

### Language

They are trained primarily on natural language and source code.

### Model

A mathematical function that predicts the next token based on previous
tokens.

------------------------------------------------------------------------

# How an LLM Works (High Level)

``` mermaid
flowchart LR
A[User Prompt] --> B[Tokenizer]
B --> C[Embeddings]
C --> D[Transformer]
D --> E[Next Token Prediction]
E --> F[Response]
```

The model generates **one token at a time**, repeatedly extending the
response until it decides to stop.

## Example

Prompt:

> The capital of France is

Prediction:

> Paris

The model is not querying a database. It predicts the statistically most
likely continuation based on patterns learned during training.

## Traditional Software vs LLM

  Traditional Software   LLM
  ---------------------- ----------------------------------
  Rule based             Probability based
  Fixed logic            Learns patterns
  Deterministic          Can generate different responses
  Explicit programming   Learned from data

## Real-world Use Cases

-   Chatbots
-   Coding assistants
-   Enterprise search
-   Document summarization
-   Translation
-   Knowledge management
-   Customer support

## Simple Python Example

``` python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    input="Explain Kubernetes in simple terms."
)

print(response.output_text)
```

## Common Misconceptions

❌ LLMs search Google before answering.

❌ LLMs always know the latest information.

❌ Bigger models are always better.

✔ LLMs predict tokens from learned patterns.

## Hands-on Exercise

1.  Install Ollama or create an OpenAI API key.
2.  Ask the same question three different ways.
3.  Observe how wording changes the response.

## Interview Questions

1.  What is an LLM?
2.  Why is it called a Large Language Model?
3.  What is next-token prediction?
4.  How is an LLM different from traditional software?
5.  Name three enterprise use cases.

## Summary

An LLM is a Transformer-based neural network trained to predict the next
token. Although the prediction task appears simple, scaling it to
massive datasets and model sizes enables powerful language understanding
and generation capabilities.

## Next Chapter

➡️ `02-History-of-LLMs.md`
