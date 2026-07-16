# 11 - Schema Design for MCP Tools

## Introduction

Chapter 05 showed the schema gets auto-derived from your function
signature — which means schema quality is now entirely a function of
how well you write Python type hints and docstrings. This chapter is
module 02 chapter 09's instruction-clarity discipline, applied
specifically to that translation.

## Learning Objectives

After this chapter I should be able to:

-   Write type-annotated tool functions that produce precise schemas.
-   Use Pydantic models for structured, validated tool arguments.
-   Recognize schema ambiguity that will cause wrong tool calls.

------------------------------------------------------------------------

# Vague Types Produce Vague Schemas

``` python
# vague - the model has to guess what "data" should look like
@mcp.tool()
def update_incident(data: dict) -> dict:
    """Updates an incident."""
    ...

# precise - the schema tells the model exactly what's expected
@mcp.tool()
def update_incident(incident_id: str, status: str, notes: str = "") -> dict:
    """Update an incident's status. status must be one of: open,
    investigating, resolved, closed."""
    ...
```

This is module 02 chapter 09's "vague instructions produce
inconsistent output" lesson, restated for schemas: a `dict` parameter
gives the model no structural guidance at all about what keys are
expected, while explicit, named parameters produce a schema that
constrains the model toward a correct call.

## Using Pydantic for Real Validation

``` python
from pydantic import BaseModel, Field

class IncidentUpdate(BaseModel):
    incident_id: str = Field(description="The incident ID, e.g. INC-2345")
    status: str = Field(description="One of: open, investigating, resolved, closed")
    notes: str = Field(default="", description="Optional notes about this update")

@mcp.tool()
def update_incident(update: IncidentUpdate) -> dict:
    """Update an incident's status and notes."""
    return {"incident_id": update.incident_id, "status": update.status, "updated": True}
```

Pydantic's `Field(description=...)` flows directly into the generated
schema's per-field descriptions — giving the model guidance at the
field level, not just the function level, the same granularity module
02 chapter 09's constraint table recommends for prompt instructions
generally.

## Constrain What You Can, at the Type Level

``` python
from typing import Literal

@mcp.tool()
def classify_severity(alert_text: str) -> Literal["LOW", "MEDIUM", "HIGH"]:
    """Classify an alert's severity."""
    ...

@mcp.tool()
def set_status(incident_id: str, status: Literal["open", "investigating", "resolved", "closed"]) -> dict:
    """Update an incident's status."""
    ...
```

`Literal` types generate an `enum` constraint in the resulting JSON
schema — the model isn't just told which values are valid in prose
(easy to ignore), the schema itself constrains what a well-behaved
client will even attempt to send.

## Where Ambiguity Actually Causes Failures

``` text
Ambiguous:  def restart(name: str) -> dict
            - restart WHAT? A pod? A service? A whole node?

Precise:    def restart_kubernetes_pod(pod_name: str, namespace: str) -> dict
            - unambiguous about both what's being restarted and where
```

A model choosing between several similarly-named, vaguely-described
tools is exactly module 02 chapter 14's tool-selection risk — vague
tool names and descriptions produce wrong tool selection just as
reliably as vague prose produces wrong prompt behavior.

## Hands-on: Rewrite a Vague Tool

Take this intentionally poor tool definition and rewrite it using
everything from this chapter — precise types, a `Literal` where
applicable, and a Pydantic model if more than two or three parameters
are involved:

``` python
@mcp.tool()
def do_thing(x: str, y: str, z: dict) -> dict:
    """Does a thing."""
    ...
```

Then run it through chapter 09's client and inspect the generated
schema — confirm the rewritten version produces a schema you'd
actually trust a model to use correctly without additional prompting.

## Common Misconceptions

❌ Schema quality is fixed once type hints are added — nothing more
to do.
(Type hints define structure; docstrings and `Field(description=...)`
still carry the semantic guidance a model needs — both matter, per
module 02 chapter 14's original lesson.)

❌ A `dict` parameter is fine as long as the docstring explains its
shape.
(Prose describing a dict's expected keys is far weaker guidance than
an actual typed schema — use a Pydantic model or explicit named
parameters whenever the shape is known ahead of time.)

✔ `Literal` types are the schema-level equivalent of module 02 chapter
09's "explicit constraint" advice — they don't just suggest valid
values, they structurally constrain what a well-behaved client sends.

## Interview Questions

1.  Why does a `dict` parameter produce a weaker schema than named,
    typed parameters?
2.  How does `Field(description=...)` on a Pydantic model improve a
    tool's generated schema?
3.  What does a `Literal` type add to a tool's schema, beyond what a
    docstring alone provides?
4.  Why is vague tool naming a tool-selection risk, not just a
    readability issue?

## Summary

Because MCP derives a tool's schema from its Python signature, schema
quality is entirely a function of how precisely that signature and its
docstrings are written — the same instruction-clarity discipline from
module 02 chapter 09, now applied to type hints, Pydantic models, and
`Literal` constraints instead of prose.

## Next Chapter

➡️ `12-Error-Handling-in-MCP-Tools.md`
