# 18 - Best Practices

## Introduction

The consolidated checklist for this module, same spirit as every other
module's — each item traces back to a specific chapter, this is the
"what do I actually do" version to walk through before trusting a
vector database with real data.

## Learning Objectives

After this chapter I should be able to:

-   Apply a concrete checklist when designing or reviewing a vector
    database setup.
-   Explain the reasoning behind each item, tied to its source
    chapter.

------------------------------------------------------------------------

# The Checklist

## 1. Confirm You Actually Need a Vector Database

Chapter 01 / module 03 chapter 10. A linear scan is often fast enough —
measure before adding infrastructure.

## 2. Choose Deliberately, Not by Default

Chapter 03. Embedded/local, self-hosted, managed, or an extension on an
existing database (chapter 16) — the right choice depends on scale,
ops appetite, and data residency, not habit.

## 3. Set the Distance Metric Explicitly

Chapter 04/07. Don't rely on a default matching your embedding model's
assumptions — state it, matching module 03 chapter 05's guidance.

## 4. Use `upsert()` With Stable, Content-Derived IDs

Chapters 06, 09. Together, these are what make an ingestion pipeline
safe to run more than once — neither one alone is sufficient.

## 5. Filter During the Search, Not After

Chapter 08. Metadata filtering applied at query time is both more
efficient and more correct than filtering results after the fact.

## 6. Centralize Access-Control Filters Into One Code Path

Chapter 12. A per-query `where={"tenant_id": ...}` filter is only as
safe as never being forgotten — make it structurally impossible to
skip, not a convention.

## 7. Prefer Soft Delete for Anything With Real Consequences

Chapter 11. Reversibility is usually worth the small ongoing cost of
filtering out deactivated records.

## 8. Know Your Recovery Strategy Before You Need It

Chapter 10. Direct backup or regenerate-from-source — pick deliberately
based on re-embedding cost, and actually test it.

## 9. Don't Add Reranking or Hybrid Search Without Evidence

Chapters 14, 15. Verify with recall@k (module 03 chapter 16) that
initial retrieval is actually the bottleneck before adding either
stage's cost and complexity.

## 10. Monitor Correctness, Not Just Uptime

Chapter 17. A scheduled recall@k check is what catches a vector
database that's fast, responsive, and quietly wrong.

## Anti-Patterns to Avoid

-   **Random IDs in an ingestion pipeline that might re-run** —
    chapter 09.
-   **A metadata filter for tenant isolation that isn't centralized in
    one code path** — chapter 12.
-   **Treating persistence to disk as equivalent to being backed up**
    — chapter 10.
-   **Adding reranking or a dedicated vector database before measuring
    whether the simpler option is actually insufficient** — chapters
    01, 15, 16.
-   **Monitoring only latency and uptime, with no correctness signal**
    — chapter 17.

## Hands-on: Turn This Into a Repo Checklist

Same pattern as every other module: create a
`vector-database-checklist.md` with these 10 items as literal
checkboxes, and walk through it before trusting a vector database
setup with real production data.

## Common Misconceptions

❌ A vector database is simple enough not to need this level of
process.
(It's a real, stateful datastore — the same operational rigor applied
to any other database applies here: backup, access control,
monitoring, capacity planning.)

❌ Following this checklist means you've built a scalable system.
(It means you've avoided the well-understood failure modes covered in
this module — chapter 13's scaling chapter still applies once real
growth arrives.)

✔ Every item here maps to a chapter that explains the underlying
failure mode — understanding *why* is what lets you judge the cases
this checklist doesn't explicitly cover.

## Interview Questions

1.  Why are stable IDs and `upsert()` both necessary for safe
    re-indexing, not just one?
2.  Why should tenant-isolation filtering be centralized into one code
    path?
3.  What's the difference between persistence and backup, and why
    does that distinction matter?
4.  Why is uptime monitoring alone insufficient for a vector database?

## Summary

Every practice in this checklist traces back to a specific chapter's
failure mode: unnecessary infrastructure, silent metric mismatches,
duplicate or orphaned records, access-control gaps, untested recovery
plans, premature complexity, and blind spots in monitoring. Together
they're what turns "a vector database that worked in a demo" into one
safe to operate for real.

## Next Chapter

➡️ `19-Interview-Questions.md`
