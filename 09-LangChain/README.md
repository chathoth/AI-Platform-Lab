# 09 - LangChain

> The same things modules 02 and 07 built by hand, wrapped in a
> framework — kept short on purpose, because you already know what's
> underneath.

## Overview

Everything LangChain does here is something this repository already
built manually: prompt templates (module 02), tool calling (module 02
chapter 14), the reason-act-observe agent loop (module 07). LangChain
just gives that a standard set of building blocks and less code to
write. Because the underlying concepts are already covered in depth,
this module stays intentionally brief — a fast, practical tour, not
another 20-chapter deep dive.

Every example runs against local Ollama (`llama3.1:8b`), verified
directly while writing this module.

## Chapters

  Chapter   Topic
  --------- ---------------------------------------
  01        What LangChain Is (and When You Don't Need It)
  02        Chains: Prompt → Model → Output, Composed
  03        Tools and Agents in LangChain
  04        Best Practices and Interview Questions

## Prerequisites

-   [02-Prompt-Engineering](../02-Prompt-Engineering/) and
    [07-AI-Agents](../07-AI-Agents/) — this module assumes you already
    understand what a chain and an agent loop actually do.

## Setup

```bash
ollama pull llama3.1:8b
pip install langchain langchain-ollama
```

## Next Module

➡️ `10-Projects`
