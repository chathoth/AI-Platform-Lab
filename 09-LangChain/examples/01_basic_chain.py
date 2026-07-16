"""
Example: 01_basic_chain.py

A prompt | model | output-parser chain against local Ollama. Ties
back to docs/02-Chains-Prompt-Model-Output.md.

Run:
    ollama pull llama3.1:8b
    pip install langchain langchain-ollama
    python 01_basic_chain.py
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.1:8b", base_url="http://localhost:11434", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a terse DevOps assistant. One sentence only."),
    ("user", "{question}"),
])

chain = prompt | llm | StrOutputParser()

if __name__ == "__main__":
    result = chain.invoke({"question": "What is a Kubernetes readiness probe?"})
    print(result)
