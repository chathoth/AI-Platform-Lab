# 01 - What Is Retrieval-Augmented Generation?

## Introduction

Module 01 chapter 14 (Fine-Tuning vs RAG) introduced the concept from a
distance: "mount a config map at runtime instead of baking data into
the image." This module is where that idea becomes a real, working
pipeline — built and verified against one real document
(`sample-data/Vacation Time Policy.pdf`) so every concept has a
concrete, checkable answer instead of a hypothetical one.

## Learning Objectives

After this chapter I should be able to:

-   Define RAG and explain the retrieval + generation pattern.
-   Explain why RAG exists instead of just relying on the model's
    trained knowledge.
-   Name the core components of a RAG pipeline.
-   Explain the difference between a grounded and a hallucinated
    answer.

------------------------------------------------------------------------

# Retrieval + Generation, Combined

RAG combines two systems that solve different problems:

1.  a **retriever** that finds information relevant to a question, and
2.  a **generative model** that turns that information into a
    readable answer.

``` text
Question
   ↓
Retrieve relevant document passages
   ↓
Add passages to the prompt
   ↓
Generate an answer from the supplied context
```

## Why RAG Exists

A model's knowledge is frozen at training time (module 01 chapter 11).
It doesn't know your private documents, your internal policies, or
anything published after its cutoff — and it has no built-in way to
say "I was never shown that." RAG fixes this at query time, without
retraining anything.

**Platform analogy:** this is exactly the config-map-vs-baked-image
trade-off from module 01 chapter 14, now with a real, running example:
the model's weights never change (nothing is "baked in"), but the
`Vacation Time Policy.pdf` content gets mounted into the prompt fresh
on every question — update the PDF, and the very next query sees the
change, no redeploy of the model required.

## A Concrete Example, From This Module

``` text
Employee asks: "How many annual leave days do I receive?"
```

The model doesn't know your company's specific policy. A RAG system
searches the actual handbook and retrieves the relevant passage:

``` text
"Full-time employees receive 20 working days of annual leave each year."
```

The model receives both pieces:

``` text
Context:
Full-time employees receive 20 working days of annual leave each year.

Question:
How many annual leave days do I receive?
```

And can now answer correctly, grounded in a real source — not a guess.

## RAG vs. a Plain LLM Call

``` text
Plain call:  User question → LLM → answer (from trained knowledge only)
RAG call:    User question → retrieval → context → LLM → grounded answer
```

## RAG vs. Fine-Tuning

  RAG                                   Fine-tuning
  -------------------------------------- --------------------------------------
  Supplies knowledge at query time        Changes model behavior through training
  Documents can be updated independently   Model may need to be trained again
  Suitable for private, current knowledge   Suitable for style or task specialization
  Can expose supporting sources              Does not automatically provide sources
  Usually faster to update                    Training requires preparation and compute

They aren't mutually exclusive — module 01 chapter 14 covers combining
both (fine-tune for consistent style, RAG for fresh facts).

## Core Components

A basic RAG system contains eight stages, each with its own numbered
script in this module's `src/` directory:

1.  **Document loader** — reads PDF, TXT, HTML, or other formats
    (`01_load_documents.py`).
2.  **Chunker** — splits long content into retrieval-sized passages
    (`02_chunk_documents.py`).
3.  **Embedding model** — converts text into vectors
    (`03_generate_embeddings.py`).
4.  **Vector database** — stores vectors and metadata
    (`04_store_vectors.py`).
5.  **Retriever** — finds chunks relevant to the question
    (`05_similarity_search.py`).
6.  **Prompt builder** — combines instructions, context, and question
    (`06_build_prompt.py`).
7.  **Language model** — generates the final response
    (`07_rag_pipeline.py`).
8.  **Evaluator** — measures retrieval and answer quality
    (`08_evaluate_rag.py`).

## Grounding and Hallucination

A **grounded** answer is supported by retrieved evidence. A
**hallucinated** answer contains unsupported information (module 01
chapter 11). A strong prompt tells the model explicitly:

``` text
Use only the supplied context.
If the answer is not present, say that the documents do not contain
enough information.
```

This reduces hallucination — it doesn't eliminate it, which is exactly
why chapter 09 (Evaluation) exists as a required stage, not an optional
one.

## Hands-on: Run It, Don't Just Read About It

Every chapter in this module references a real command against a real
document. Start here:

``` bash
cd 05-RAG
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ollama pull llama3.2:3b
ollama pull nomic-embed-text

python src/01_load_documents.py
```

You should see `Total page documents: 6` — the policy PDF has six
pages, and each becomes one loaded document. This is the first, most
basic checkpoint the whole rest of the module builds on.

## Limitations, Honestly

RAG does not guarantee correctness. A RAG system can still fail
because:

-   the document was never loaded,
-   chunk boundaries destroyed the context (chapter 04),
-   the embedding didn't represent the query well (chapter 05),
-   the right chunk wasn't retrieved (chapter 07),
-   too much irrelevant context diluted the good context,
-   the prompt was weak (chapter 08),
-   or the model ignored or misread the context anyway.

## Common Misconceptions

❌ RAG makes a model's answers always correct.
(It grounds answers in real evidence, which reduces but does not
eliminate wrong answers — every stage in the pipeline can still fail,
per the list above.)

❌ RAG and fine-tuning solve the same problem.
(They solve different problems — module 01 chapter 14 covers this in
depth. RAG is for fresh, citable facts; fine-tuning is for consistent
behavior/style.)

✔ The quality of a RAG answer is the product of every stage, not just
the model: `document quality × chunk quality × embedding quality ×
retrieval quality × prompt quality × model quality` — one weak link
degrades the whole chain.

## Interview Questions

1.  What are the two systems RAG combines, and what does each do?
2.  Why does RAG exist instead of just relying on the model's trained
    knowledge?
3.  Name the eight stages of a RAG pipeline.
4.  What's the difference between a grounded and a hallucinated
    answer?

## Summary

RAG combines a retriever and a generative model so that answers can be
grounded in real, current, private documents instead of relying solely
on frozen training knowledge. It's a pipeline, not a single model call
— every stage from document loading through evaluation contributes to
(or can degrade) the final answer's quality, which is exactly why this
module walks through each stage individually against one real document.

## Next Chapter

➡️ `02-RAG-Architecture.md`
