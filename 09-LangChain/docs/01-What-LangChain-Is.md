# 01 - What LangChain Is (and When You Don't Need It)

LangChain is a Python/JS library that standardizes the pieces this
repository has already built by hand: prompt templates (module 02),
calling a model, parsing its output, and wiring in tools (module 02
chapter 14, module 07). It doesn't add new capability — it adds
consistent building blocks and less boilerplate.

``` text
Hand-rolled (module 02/07):   your own message lists, your own loop,
                                your own tool-schema dicts

LangChain:                      the same concepts, as reusable classes
                                 (ChatPromptTemplate, tools, chains)
                                 you compose instead of writing from scratch
```

**Platform analogy:** this is Terraform versus raw cloud API calls —
Terraform doesn't do anything a script calling the API couldn't do, it
just gives you a standard, composable way to express it, with less
repetition across projects.

## When It's Worth the Extra Dependency

``` text
One-off script, a single prompt, no reuse?
        → hand-rolled is simpler (module 02's approach)

Multiple chains/agents across a real application, wanting standard
patterns for memory, retrieval, and tool-calling?
        → LangChain earns its keep
```

Verified directly: `ChatOllama` from `langchain-ollama` connects to
the exact same local Ollama server every other module in this
repository uses — no new infrastructure, just a different client
library on top of it.

``` python
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.1:8b", base_url="http://localhost:11434", temperature=0)
response = llm.invoke("Say OK")
print(response.content)  # verified: "OK"
```

## Next Chapter

➡️ `02-Chains-Prompt-Model-Output.md`
