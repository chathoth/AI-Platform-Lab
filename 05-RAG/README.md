# Retrieval-Augmented Generation (RAG)

A practical explanation of Retrieval-Augmented Generation for Platform Engineers, DevOps Engineers, SREs, and AI developers.

---

## What is RAG?

Large Language Models, or LLMs, such as ChatGPT, Claude, Gemini, and Llama are trained on very large datasets.

They can answer many general questions, write code, summarize text, and explain technical concepts. However, they have an important limitation:

> An LLM does not automatically know your organization’s private, internal, or recently updated information.

For example, an LLM normally cannot access:

- Internal runbooks
- Confluence pages
- Git repositories
- Infrastructure documentation
- Incident reports
- Standard operating procedures
- Jenkins pipelines
- Terraform modules
- Internal architecture documents
- Recently updated operational instructions

Imagine asking a general-purpose LLM:

> What is the restart procedure for our Jenkins production server?

The model does not know your internal Jenkins environment, server names, dependencies, validation steps, or support procedures.

Without access to the correct documentation, it may:

- Provide a generic answer
- Make assumptions
- Produce incorrect steps
- Hallucinate information

This is where **Retrieval-Augmented Generation**, commonly called **RAG**, becomes useful.

RAG allows an application to search your own documents, retrieve the most relevant information, and provide that information to the LLM before it generates an answer.

Instead of depending only on what the model learned during training, the model also receives relevant information from your own knowledge base.

---

## Simple Definition

RAG can be understood as:

```text
Search + AI

```

The basic process is:

- Search the organization’s documents.
- Retrieve the most relevant content.
- Add that content to the LLM prompt.
- Ask the LLM to generate an answer using the retrieved information.

The LLM is not expected to remember all company information.

It is given the required information at the time the question is asked.

---

## Traditional LLM Workflow
```
User Question
      │
      ▼
Large Language Model
      │
      ▼
Generated Answer
```
In this model, the LLM answers only from:

- Its training data
- The user’s prompt
- The context already available in the conversation

The model does not automatically search your internal systems.

---

## RAG Workflow

```
      User Question
            │
            ▼
Convert Question into Embedding
            │
            ▼
    Search Vector Store
            │
            ▼
Retrieve Relevant Documents
            │
            ▼
Question + Retrieved Context
            │
            ▼
      Large Language Model
            │
            ▼
      Grounded Answer

```

The important difference is that the LLM is no longer answering blindly.

It receives relevant information before generating the final response.


---


## Why Do We Need RAG?
Consider an enterprise platform that contains:


- 20,000 Confluence pages
- 8,000 PDF documents
- 15 Git repositories
- 400 operational runbooks
- Terraform documentation
- Jenkins pipelines
- AEM documentation
- Architecture diagrams
- Incident reports
- Troubleshooting guides

A public LLM was not trained specifically on this private content.

Even when the model understands technologies such as Jenkins, AWS, AEM, Elasticsearch, or Terraform, it does not understand the exact way your organization has implemented them.

## Without RAG

```

      User Question
            │
            ▼
  LLM uses general knowledge
            │
            ▼
Generic or possibly incorrect answer

```
## With RAG

```
      User Question
            │
            ▼
  Search internal knowledge
            │
            ▼
  Retrieve relevant documents
            │
            ▼
 Provide documents to the LLM
            │
            ▼
Generate an answer based on the documents

```

RAG helps connect the general reasoning capability of an LLM with the private and current knowledge of an organization.

---

## Real-World Example: AEM Platform Support

Imagine that you are managing an enterprise Adobe Experience Manager platform.

Your internal documentation contains:

- AEM Author restart procedures
- AEM Publish restart procedures
- Dispatcher configuration
- Apache HTTP Server configuration
- Load balancer health-check details
- Elasticsearch troubleshooting instructions
- Jenkins deployment pipelines
- AWS infrastructure documentation
- Terraform modules
- Production SOPs
- Previous incident reports

An engineer asks:

>Why is AEM Publish QA returning HTTP 503?

## Without RAG

A general LLM may respond:

> Restart the application and check whether the service is running.

This answer is too generic.

It does not identify:

1. Which service should be checked
2. Which logs are relevant
3. Whether the issue is in AEM, Dispatcher, Apache, or the load balancer
4. Whether a similar incident happened previously
5. What validation is required before restarting the platform


## With RAG

The RAG application searches the internal knowledge base using concepts such as:

```
HTTP 503
AEM Publish
QA
Dispatcher
health check
Apache
backend connectivity
```
The retrieval system may find:

- Incident INC-2345
- Dispatcher health-check runbook
- Apache virtual-host configuration
- AEM Publish connectivity guide
- Known issue KB-145

These documents are added to the LLM prompt.

The generated answer may then be:

> According to incident INC-2345, HTTP 503 in the QA Publish environment previously occurred when the Dispatcher health check failed because /bin/healthcheck returned HTTP 500. First verify the Apache error log and confirm connectivity from Dispatcher to the Publish instance. Restart Dispatcher only if the backend is healthy. Restart AEM Publish only after validating that the issue is coming from the application layer.

This answer is more useful because it is based on the organization’s own documentation.

The model is not simply recalling information from its training data. It is using retrieved context.

---
## How RAG Works Internally

A RAG system normally has two major workflows:

1. Indexing workflow
2. Question-answering workflow

---
### Part 1: Indexing Workflow

The indexing workflow prepares documents so they can be searched efficiently.
```
Documents
    │
    ▼
Load Content
    │
    ▼
Clean and Split Text
    │
    ▼
Create Embeddings
    │
    ▼
Store in Vector Database

```
---
#### Step 1: Collect Documents

Documents may come from different sources, including:

- PDF
- Microsoft Word
- Markdown
- HTML
- Confluence
- SharePoint
- Git repositories
- Jira
- Email
- S3
- Internal APIs
- Databases

The component that reads these documents is commonly called a document loader.

---
#### Step 2: Extract and Clean the Content

The system extracts text from the source documents.

During this stage, it may also:

- Remove repeated headers and footers
- Remove unnecessary HTML
- Normalize spacing
- Preserve headings
- Extract page numbers
- Capture URLs
- Capture document titles
- Capture access-control metadata
- Remove duplicate content

Clean input improves retrieval quality.

---

#### Step 3: Split Documents into Chunks

Large documents are normally too long to store or retrieve as one unit.

For example, a 200-page PDF may be divided into smaller sections:

```
Chunk 1: Platform overview

Chunk 2: Restart procedure

Chunk 3: Health-check validation

Chunk 4: Rollback procedure

Chunk 5: Escalation process
```
A chunk may contain:

- A paragraph
- A section
- Several related paragraphs
- A fixed number of tokens
- A heading and its related content

There is no single chunk size that works for every use case.

The correct chunk size depends on:

- Document type
- Embedding model
- Type of questions
- Required level of detail
- Context-window size
- Retrieval strategy

Chunks often include some overlap so that important information is not lost between two sections.

---

#### Step 4: Create Embeddings

Each chunk is converted into an embedding.

An embedding is a numerical representation of the meaning of the text.

For example:

`Restart Jenkins production server`

may be converted into a vector similar to:

``[0.234, 0.881, 0.122, 0.654, ...]``

The individual numbers are not normally interpreted manually.

What matters is that text with similar meaning should have embeddings that are close to each other in vector space.

For example, the following phrases are semantically related:
```
Restart Jenkins

Restart the CI server

Bounce the build server

Recover the Jenkins controller
```

Although the wording is different, the meaning is similar.

---

#### Step 5: Store Data in a Vector Database

The embeddings are stored in a vector database or vector index.

Common options include:

- ChromaDB
- FAISS
- Pinecone
- Milvus
- Weaviate
- Elasticsearch
- OpenSearch
- PostgreSQL with pgvector

A vector database normally stores more than only the vector.

Example:

```
{
  "text": "Restart the Jenkins service only after confirming that no deployment is running.",
  "embedding": [0.234, 0.881, 0.122],
  "source": "jenkins-production-runbook.pdf",
  "page": 12,
  "section": "Restart Procedure",
  "environment": "production",
  "document_type": "runbook",
  "url": "https://example.internal/runbooks/jenkins",
  "last_updated": "2026-06-10"
}
```

The additional information is called metadata.

Metadata can be used for:

- Filtering
- Source citations
- Access control
- Environment selection
- Country selection
- Document freshness
- Document-type filtering

---

### Part 2: Question-Answering Workflow

When a user asks a question, the RAG system performs retrieval and generation.

```
User Question
      │
      ▼
Create Question Embedding
      │
      ▼
Search Vector Database
      │
      ▼
Retrieve Top Matching Chunks
      │
      ▼
Build Prompt
      │
      ▼
Generate Answer

```
---

#### Step 6: Receive the User Question

Example:

`How do I safely restart Jenkins production?`

The question is converted into an embedding using the same or a compatible embedding model.

---
#### Step 7: Perform Similarity Search

The question embedding is compared with the document embeddings stored in the vector database.

The system retrieves the chunks that are closest in meaning.

This is called:

- Vector search
- Semantic search
- Similarity search

For example, the user may ask:

`How do I restart the CI server?`

The document may contain:

`Jenkins production restart procedure`

A traditional keyword search may fail when the exact words are different.

A semantic search system can recognize that:

`CI server`

and:

`Jenkins`

may refer to related concepts.

---

#### Step 8: Retrieve the Best Matches

The system normally retrieves a small number of relevant chunks.

For example:

```
Top result 1:
Jenkins production restart procedure

Top result 2:
Deployment validation checklist

Top result 3:
Jenkins rollback procedure

Top result 4:
Production escalation matrix

```
Retrieving too few chunks may miss important information.

Retrieving too many chunks may introduce noise and increase token usage.

The retrieval configuration must be tested and tuned.

---

#### Step 9: Build the Prompt

The application combines:

- System instructions
- Retrieved document chunks
- Metadata
- User question
- Output requirements

Example:

```
You are an infrastructure support assistant.

Answer the question using only the provided documentation.

If the documentation does not contain enough information, say that the
answer cannot be confirmed.

Include the source document names in the answer.

Context:

Document 1:
Restart the Jenkins service only after confirming that no production
deployment is active.

Document 2:
After restarting Jenkins, validate the login page, executor status,
connected agents, and scheduled jobs.

Question:
How do I safely restart Jenkins production?

```

This process is sometimes called context injection or prompt augmentation.

---

#### Step 10: Generate the Answer

The LLM receives both the question and the retrieved context.

It can then generate an answer such as:

>Before restarting Jenkins production, confirm that no deployment or scheduled maintenance job is active. Restart the Jenkins service using the approved operational procedure. After the restart, validate the login page, executor status, connected agents, scheduled jobs, and build queue.

>Sources: Jenkins Production Runbook, Deployment Validation Checklist

The answer is grounded in the retrieved documentation.

---

# Complete RAG Architecture

INDEXING WORKFLOW
```
     PDF / Word / Wiki / Git / Confluence / Jira / S3
                            │
                            ▼
                      Document Loader
                            │
                            ▼
                    Content Extraction
                            │
                            ▼
                   Cleaning and Chunking
                            │
                            ▼
                     Embedding Model
                            │
                            ▼
                     Vector Database

```

QUESTION-ANSWERING WORKFLOW
```
                       User Question
                            │
                            ▼
                     Embedding Model
                            │
                            ▼
                      Vector Search
                            │
                            ▼
                 Retrieve Relevant Chunks
                            │
                            ▼
                    Optional Re-Ranking
                            │
                            ▼
                     Prompt Construction
                            │
                            ▼
                    Large Language Model
                            │
                            ▼
                 Grounded Answer + Sources
```

## Why Embeddings Matter

Traditional keyword search mainly looks for matching words.

Example query:

>Restart Jenkins

A keyword-based search works well when the document contains the same words.

However, users may use different wording:

```
Restart the CI server

Bounce the Jenkins controller

Recover the build platform

Restart the automation server
```

Embedding-based search compares meaning rather than only exact words.

This is why embeddings are important for RAG.

However, semantic search is not always enough.

For many enterprise systems, the best results come from hybrid search, which combines:

- Keyword search
- Vector search
- Metadata filtering

Keyword search is useful for exact values such as:

- Incident numbers
- Hostnames
- Error codes
- HTTP status codes
- Configuration properties
- Application names

Vector search is useful for meaning and intent.

----

## Benefits of RAG

### Uses Current Information

Documents can be updated and re-indexed without retraining the LLM.

### Works with Private Knowledge

RAG can retrieve information from internal runbooks, documentation, tickets, and repositories.

### Reduces Hallucination

The model is given relevant source material instead of being asked to answer only from memory.

RAG reduces hallucination risk, but it does not completely eliminate it.

### Supports Source References

The application can show:

- Document name
- Page number
- Section
- URL
- Last-updated date

### No Model Retraining Required

The underlying LLM does not need to be retrained whenever documentation changes.

### Supports Large Knowledge Bases

RAG can be used with thousands or millions of document chunks.

### Can Run Locally

RAG can be implemented using local components such as:

- Ollama
- Open-source embedding models
- ChromaDB
- FAISS
- Elasticsearch
- OpenSearch

### Can Apply Access Controls

Metadata can be used to ensure that users retrieve only the documents they are authorized to access.

----

## Limitations and Challenges

RAG is powerful, but it is not automatically accurate.

The quality of the final answer depends on the complete pipeline.

### Poor Document Quality

Incorrect, incomplete, duplicated, or outdated documents can produce incorrect answers.

### Poor Chunking

If content is split incorrectly, the retrieved chunk may not contain enough context.

### Weak Retrieval

The correct answer may exist in the knowledge base but may not be retrieved.

### Irrelevant Context

The vector database may return similar but unrelated chunks.

### Hallucination Is Still Possible

Even with retrieved context, the model may misinterpret or add unsupported information.

### Access-Control Risk

A RAG application must not retrieve restricted documents for unauthorized users.

### Prompt-Injection Risk

Documents themselves may contain malicious or misleading instructions.

Retrieved content should be treated as untrusted data, not as system instructions.

### Cost and Latency

Retrieval, re-ranking, prompt construction, and LLM generation all add processing time and cost.

### Freshness

Documents must be re-indexed when they are updated, deleted, or replaced.

### Evaluation Is Required

A RAG system should be tested using real questions and expected answers.

Important evaluation areas include:

- Retrieval accuracy
- Answer correctness
- Faithfulness to sources
- Citation accuracy
- Response time
- Access-control enforcement

---

## Common RAG Technology Stack

| Layer | Purpose | Popular Technologies |
|--------|---------|----------------------|
| **Large Language Model (LLM)** | Generates the final response using the retrieved context | GPT-4/5, Claude, Gemini, Llama 3, Mistral |
| **Embedding Model** | Converts text into vector embeddings for semantic search | OpenAI Embeddings, BGE, E5, Instructor, Nomic Embed |
| **Vector Database** | Stores embeddings and performs similarity search | ChromaDB, FAISS, Pinecone, Milvus, Weaviate, Qdrant |
| **Traditional Search** | Keyword and hybrid search over documents | Elasticsearch, OpenSearch, Solr |
| **RAG Framework** | Orchestrates retrieval, prompts, and LLM interactions | LangChain, LlamaIndex, Haystack |
| **Local Model Runtime** | Runs open-source models locally | Ollama, vLLM, LM Studio |
| **Document Sources** | Enterprise knowledge repositories | PDF, Confluence, GitHub, SharePoint, Jira, S3, Databases |
| **Application Layer** | User interface and API layer | Python, FastAPI, Flask, Streamlit, Gradio |
| **Evaluation** | Measures retrieval and answer quality | RAGAS, DeepEval, custom test datasets, human evaluation |
| **Observability** | Tracks performance, prompts, latency, and costs | LangSmith, Langfuse, Phoenix, OpenTelemetry, application logs |

----

### RAG Is More Than a Vector Database

A common misunderstanding is that RAG means only:

```
Upload documents
      +
Store embeddings
      +
Ask an LLM

```

A production-quality RAG system also requires:

- Document ingestion
- Data cleaning
- Chunking strategy
- Metadata design
- Access control
- Search configuration
- Hybrid retrieval
- Re-ranking
- Prompt design
- Citation handling
- Evaluation
- Monitoring
- Data refresh
- Error handling
- Security controls

The vector database is only one component of the complete solution.

--- 

## RAG vs Fine-Tuning

RAG and fine-tuning solve different problems.

| Feature | Retrieval-Augmented Generation (RAG) | Fine-Tuning |
|---------|---------------------------------------|-------------|
| **Primary Purpose** | Retrieves external knowledge before generating a response | Modifies the model's behavior through additional training |
| **Knowledge Source** | External documents, databases, and knowledge bases | Information learned during fine-tuning |
| **Best For** | Current, dynamic, and private organizational knowledge | Domain expertise, response style, formatting, and specialized tasks |
| **Knowledge Updates** | Simply update the documents or database | Requires retraining or additional fine-tuning |
| **Real-Time Information** | ✅ Yes | ❌ No (limited to training data) |
| **Private/Internal Data** | ✅ Easily supported | ⚠️ Requires including the data during training |
| **Citations & References** | ✅ Can provide document sources and citations | ❌ Typically cannot cite original sources automatically |
| **Infrastructure** | Requires a retrieval pipeline and vector database | Requires training infrastructure and model hosting |
| **Cost** | Lower cost for frequent knowledge updates | Higher cost due to training and maintenance |
| **Hallucination Reduction** | Significantly reduced when relevant context is retrieved | May still hallucinate if knowledge wasn't learned during training |
| **Typical Use Cases** | Enterprise search, internal documentation, knowledge assistants, customer support | Chatbot personality, code generation style, document formatting, domain-specific behavior |


For many enterprise knowledge-assistant use cases, RAG is usually the first approach to evaluate.

RAG and fine-tuning can also be used together.

---

## When Should RAG Be Used?

RAG is a good fit when the answer depends on:

- Internal company documentation
- Frequently changing information
- Product documentation
- Operational runbooks
- Incident history
- Policies and procedures
- Legal or compliance documents
- Technical manuals
- Source-code documentation
- Customer-support knowledge
- Infrastructure standards

RAG may not be required when:

- The task uses only general knowledge
- The information already fits directly in the prompt
- The task is mainly text transformation
- The model does not need external information

---

## Key Takeaway

RAG connects an LLM with an external knowledge source.

```
The process is:

Retrieve
    ↓
Add Context
    ↓
Generate

```

The LLM provides language understanding and answer generation.

The retrieval system provides relevant, private, and up-to-date information.

Together, they can create an AI assistant that answers questions using the organization’s own knowledge instead of relying only on the model’s training data.