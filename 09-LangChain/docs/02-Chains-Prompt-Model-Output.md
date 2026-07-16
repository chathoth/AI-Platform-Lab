# 02 - Chains: Prompt → Model → Output, Composed

A "chain" is LangChain's version of module 02's prompt assembly and
call — a `ChatPromptTemplate` (module 02 chapter 07's templating,
standardized), piped into a model, piped into an output parser, using
the `|` operator (LCEL — LangChain Expression Language).

``` python
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="llama3.1:8b", base_url="http://localhost:11434", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a terse DevOps assistant. One sentence only."),
    ("user", "{question}"),
])

chain = prompt | llm | StrOutputParser()

result = chain.invoke({"question": "What is a Kubernetes readiness probe?"})
print(result)
```

Verified output: *"A Kubernetes readiness probe is a liveness check
that determines if a container is ready to receive traffic, not just
running."*

That's module 02's system-prompt-plus-template pattern (chapters 02,
07), the model call, and reading `.content` off the response — all in
three composed pieces instead of hand-assembled message lists. Nothing
new conceptually, just less code per call, and reusable across
however many chains an application needs.

## Retrieval Chains (Module 05, Revisited)

LangChain also standardizes RAG's retrieve-then-generate pattern
(module 05) as a composable chain — same idea (embed the question,
search a vector store, inject the result as context), expressed with
LangChain's retriever and chain abstractions instead of the manual
loop module 05's `RAGPipeline` class built directly.

## Next Chapter

➡️ `03-Tools-and-Agents-in-LangChain.md`
