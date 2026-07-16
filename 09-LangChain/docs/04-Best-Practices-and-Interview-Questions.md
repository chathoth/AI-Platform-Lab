# 04 - Best Practices and Interview Questions

## Best Practices

1.  **Don't reach for LangChain by default.** A single script with one
    prompt is simpler hand-rolled (module 02) — LangChain earns its
    keep once an application has several chains/agents that benefit
    from shared, standard patterns.
2.  **The reliability lessons from modules 02, 06, and 07 still
    apply.** A framework doesn't remove the need for guardrails
    (module 07 chapter 13), structured output validation (module 02
    chapter 06), or one-tool-at-a-time discipline (module 07 chapter
    08) — it just removes boilerplate around them.
3.  **Point it at local Ollama the same way every other module does.**
    `ChatOllama(model=..., base_url="http://localhost:11434")` — no
    new infrastructure, no API key, verified directly in this module.
4.  **Understand what's underneath before trusting the abstraction.**
    Every LangChain concept in this module maps to something built by
    hand earlier in this repository — that's what makes debugging a
    LangChain application tractable instead of a black box.

## Interview Questions

1.  What does LangChain actually add on top of calling a model
    directly?
2.  When would you choose hand-rolled code (module 02's approach) over
    LangChain?
3.  Does using LangChain's agent tooling protect against module 07
    chapter 08's verified tool-batching failure?
4.  How does `@tool`'s schema derivation compare to module 06's MCP
    `@mcp.tool()` decorator?

## Summary

LangChain standardizes prompt templates, chains, and tool/agent
patterns already covered by hand in modules 02, 05, and 07 — genuinely
useful for reducing boilerplate across a real application, but not a
substitute for understanding (or applying) the reliability lessons
those modules verified directly. Every example in this module ran
against the same local Ollama instance every other module used, with
no new infrastructure required.

## Next Module

➡️ `10-Projects`
