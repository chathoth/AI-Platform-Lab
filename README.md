# AI Platform Lab

A practical learning repository for understanding and building modern AI applications.

This repository documents my hands-on learning journey across Large Language Models, prompt engineering, embeddings, vector databases, Retrieval-Augmented Generation, Model Context Protocol, AI agents, local LLMs, and AI application frameworks.

The objective is not only to explain the concepts, but also to demonstrate how they can be applied to real-world platform engineering, DevOps, SRE, automation, and enterprise knowledge-management use cases.

## Repository Objectives

- Explain AI concepts using clear and practical language
- Build working examples instead of theory-only documentation
- Explore both cloud-hosted and locally running language models
- Apply AI to infrastructure and platform-engineering use cases
- Document architecture decisions, limitations, and lessons learned
- Create reusable examples that others can follow

## Learning Roadmap

| Module | Topic | Description | Status |
|---|---|---|---|
| 01 | [LLM Fundamentals](./01-LLM-Fundamentals/) | How Large Language Models work and where they are used | Complete |
| 02 | [Prompt Engineering](./02-Prompt-Engineering/) | Techniques for creating clear, reliable, and structured prompts | Complete |
| 03 | [Embeddings](./03-Embeddings/) | Representing text as vectors for semantic comparison | Complete |
| 04 | [Vector Databases](./04-Vector-Databases/) | Storing and retrieving embeddings efficiently | Complete |
| 05 | [Retrieval-Augmented Generation](./05-RAG/) | Building AI systems that answer from private knowledge | Complete |
| 06 | [Model Context Protocol](./06-MCP/) | Connecting AI models to tools and external data sources | Complete |
| 07 | [AI Agents](./07-AI-Agents/) | Creating systems that reason, use tools, and execute tasks | Complete |
| 08 | [Ollama](./08-Ollama/) | Running open-source language models locally | Complete |
| 09 | [LangChain](./09-LangChain/) | Building LLM workflows using LangChain | Complete |
| 10 | [Projects](./10-Projects/) | End-to-end practical AI projects | Complete |

## Real-World Projects

### [Incident Similarity Finder](./10-Projects/incident-similarity-finder/)

A read-only tool that takes a new incident description and finds the
most similar past incidents by meaning, not keywords, using the
embeddings and vector database patterns from modules 03-05.

### [Runbook Ops Assistant](./10-Projects/runbook-ops-assistant/)

Retrieves the right runbook for an incident (RAG), then runs a guarded
agent loop that can actually act on it - one tool call at a time, with
an allowlist and a human confirmation gate enforced in code, reusing
module 07's verified agent-reliability lessons.

## Technology Stack

The examples in this repository may use:

- Python
- Ollama
- Llama
- OpenAI-compatible APIs
- LangChain
- LlamaIndex
- ChromaDB
- FAISS
- Elasticsearch
- Docker
- Streamlit
- FastAPI

## Repository Principles

### Learn by Building

Every major concept should include a working example wherever practical.

### Explain the Architecture

Projects should document data flow, system components, design decisions, and trade-offs.

### Use Safe Examples

All sample data must be fictional, anonymized, or publicly available. No confidential company information, credentials, internal hostnames, customer data, or proprietary source code should be committed.

### Keep Examples Reproducible

Each project should include installation instructions, dependencies, configuration examples, and expected output.

## Suggested Learning Order

```text

LLM Fundamentals
        ↓
Prompt Engineering
        ↓
    Embeddings
        ↓
Vector Databases
        ↓
       RAG
        ↓
Ollama and LangChain
        ↓
       MCP
        ↓
    AI Agents
        ↓
End-to-End Projects

```