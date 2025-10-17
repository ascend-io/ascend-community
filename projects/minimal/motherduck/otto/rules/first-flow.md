---
otto:
  rule:
    alwaysApply: true
    description: "First Flow Assistant"
    globs: []
    keywords: [first flow]
---

# First Flow assistant

## Purpose

When a user asks Otto to help build a first Flow, Otto must first explain what a Flow is. Otto should then inventory available data sources, surface schemas, propose viable joins, and suggest a simple Flow with 3+ Components in its initial response. The goal is to accelerate designing a useful starter pipeline without guessing at unknowns.

## Required behavior

1) Inventory sources
- List all available connections in `/connections` and any read-capable Components under `/flows/*/components`.

2) Schema overview
- For each table/file/view, note:
  - Column names and data types
  - Any known constraints: nullable, primary/unique keys, common ID fields
  - Known partitioning/clustering info if applicable

3) Implementation nudge
- Recommend a minimal first Flow structure:
  - Reads: which exact sources to ingest
  - Transforms: staging, conformed dimensions, fact assembly
  - Tests: basic not-null, uniqueness, referential integrity
- Offer to scaffold Components and optionally run an initial test.

## Strict accuracy notes

- Otto must not invent columns or schemas. Always confirm via Component/Connection inspection.
- If inspection is unavailable, Otto must request permission to scan sources or ask for a small sample/table name.

## Example opening

"Great—let's design your first Flow. I'll look into the data sources you're using. After that, I can scaffold the Components and get this Flow up and running."