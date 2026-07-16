# 05 - Retrieval-Augmented Generation (RAG)

This module teaches RAG by building and inspecting every stage of the pipeline.

The knowledge source is a real six-page HR document:

```text
sample-data/Vacation Time Policy.pdf
```

Using one consistent document makes it easier to see how information moves from a PDF into a grounded LLM answer.

## What you will learn

By the end of this module, you will understand:

- how PDF pages become LangChain `Document` objects,
- why metadata matters,
- how chunk size and overlap affect retrieval,
- how text becomes an embedding vector,
- what ChromaDB stores,
- how semantic similarity search works,
- how retrieved chunks become LLM context,
- how to construct a grounded prompt,
- how to evaluate answerable and unanswerable questions,
- how to debug a RAG pipeline stage by stage.

Each chapter in `docs/` also includes a Platform Analogy tying the
concept back to infrastructure/DevOps work, a Common Misconceptions
section, Interview Questions, and a Summary — the same structure used
across every module in this repository. Chapters 12 and 13 consolidate
interview questions and terminology across the whole module.

## Architecture

### Indexing phase

```text
Vacation Time Policy.pdf
          |
          v
Load PDF pages
          |
          v
Inspect page text and metadata
          |
          v
Split pages into overlapping chunks
          |
          v
Generate embeddings
          |
          v
Store chunks, vectors, IDs, and metadata in ChromaDB
```

### Query phase

```text
User question
      |
      v
Generate question embedding
      |
      v
Similarity search
      |
      v
Retrieve top-K chunks
      |
      v
Build grounded prompt
      |
      v
Generate answer with Ollama
      |
      v
Display answer and source pages
```

## Folder structure

```text
05-RAG/
├── README.md
├── requirements.txt
├── .env.example
├── docs/
│   ├── 01-What-is-RAG.md
│   ├── 02-RAG-Architecture.md
│   ├── 03-Document-Loading.md
│   ├── 04-Chunking.md
│   ├── 05-Embeddings.md
│   ├── 06-Vector-Database.md
│   ├── 07-Retrieval.md
│   ├── 08-Prompting.md
│   ├── 09-Evaluation.md
│   ├── 10-Debugging.md
│   ├── 11-Best-Practices.md
│   ├── 12-Interview-Questions.md
│   └── 13-Glossary.md
├── sample-data/
│   └── Vacation Time Policy.pdf
├── evaluation/
│   ├── evaluation_dataset.csv
│   └── evaluation_dataset.json
├── src/
│   ├── 01_load_documents.py
│   ├── 02_chunk_documents.py
│   ├── 03_generate_embeddings.py
│   ├── 04_store_vectors.py
│   ├── 05_similarity_search.py
│   ├── 06_build_prompt.py
│   ├── 07_rag_pipeline.py
│   ├── 08_evaluate_rag.py
│   └── utils.py
├── artifacts/
├── chroma_db/
├── notebooks/
│   └── rag_demo.ipynb
└── tests/
```

## Prerequisites

- Python 3.10+
- Ollama
- `llama3.2:3b`
- `nomic-embed-text`

```bash
ollama --version
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

## Setup

```bash
cd AI-Platform-Lab/05-RAG

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

cp .env.example .env
```

## Run the pipeline step by step

### Step 1 - Load the PDF

```bash
python src/01_load_documents.py
```

Inspect:

```text
artifacts/loaded_documents.json
```

Expected result:

```text
Loaded file: Vacation Time Policy.pdf
Loaded pages: 6
```

### Step 2 - Chunk the pages

```bash
python src/02_chunk_documents.py
```

Inspect:

```text
artifacts/chunks.json
```

Pay particular attention to the Carry-Over section, which begins on page 1 and continues on page 2. This is a useful example of why page boundaries and overlap matter.

### Step 3 - Generate embeddings

```bash
python src/03_generate_embeddings.py
```

Inspect:

```text
artifacts/embeddings.json
```

The file is intentionally generated for learning. A production application would normally avoid storing large raw vectors in JSON.

### Step 4 - Store vectors in ChromaDB

```bash
python src/04_store_vectors.py --reset
```

This creates the persistent index under:

```text
chroma_db/
```

### Step 5 - Test semantic retrieval

```bash
python src/05_similarity_search.py \
  --question "When must a carry-over request be submitted?"
```

The best result should point to page 2 and include `November 1`.

Try a paraphrased query:

```bash
python src/05_similarity_search.py \
  --question "What is the deadline for moving unused vacation to next year?"
```

This demonstrates semantic retrieval rather than exact keyword matching.

### Step 6 - Inspect the prompt

```bash
python src/06_build_prompt.py \
  --question "Do employees accrue vacation during maternity leave?"
```

Inspect:

```text
artifacts/prompt.txt
```

### Step 7 - Run the complete RAG query

```bash
python src/07_rag_pipeline.py \
  --question "Do employees accrue vacation during maternity leave?" \
  --show-context
```

Expected answer:

```text
Yes. Employees continue to accrue vacation during maternity and parental leave.
```

### Step 8 - Run the evaluation set

```bash
python src/08_evaluate_rag.py
```

The evaluator checks:

- whether expected pages were retrieved,
- whether answer keywords were present,
- whether negative questions produced the no-answer response.

Results are written to:

```text
artifacts/evaluation_results.json
```

## Recommended learning questions

### Direct questions

```text
What is the maximum vacation entitlement?
When must carry-over requests be submitted?
How many days can normally be carried over?
What is the accrual period?
```

### Paraphrased questions

```text
What is the deadline for moving unused vacation to next year?
Does family leave stop vacation accumulation?
What happens to unused vacation when employment ends?
```

### Multi-condition questions

```text
When may sick leave replace vacation?
Can more than five days be carried over, and who must approve it?
```

### Unanswerable questions

```text
How many sick days are employees entitled to?
What dental benefits are provided?
What is the overtime compensation policy?
```

A grounded system should not invent answers to these questions.

## Debugging order

When the answer is wrong, inspect the pipeline in this order:

```text
1. Was the PDF loaded?
2. Is the expected text present in the page document?
3. Is it preserved in a chunk?
4. Was the chunk embedded and stored?
5. Was the correct chunk retrieved?
6. Was the chunk included in the prompt?
7. Did the LLM follow the prompt?
```

Do not change the LLM first when the actual problem is document loading or retrieval.
