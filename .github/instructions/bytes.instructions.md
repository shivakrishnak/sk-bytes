---
applyTo: "bytes/**"
description: "Rules for generating and editing byte content - interview-style multi-keyword files, 14-section per-keyword template, depth + progression signals"
---

# Bytes - Auto-Loaded Instructions

> Auto-attaches when editing files under `bytes/`. Full content spec
> at `bytes/_config/BYTES_PROMPT.md` (v1.0). Full keyword generation
> spec at `bytes/_config/BYTES_KEYWORD_GENERATOR.md` (v1.0).
>
> **NON-NEGOTIABLE:** All topic / subtopic / keyword generation MUST
> use `bytes/_config/BYTES_KEYWORD_GENERATOR.md` v1.0 as the single
> source of truth. Do not invent levels, tags, or coverage rules
> outside that spec. Do not bypass it for "quick" keyword lists.

## Workspace structure

```
bytes/
  _config/
    BYTES_PROMPT.md             Master content spec v1.0
    BYTES_KEYWORD_GENERATOR.md  Master keyword spec v1.0
    README.md                   Generation guide
    topic-registry.md           Topic -> folder + sub-topic plan
    bytes_scaffold.py           Optional preview emitter (14-section stubs)
    validate-byte.py            Section + frontmatter validator
    generate-keywords.ps1       Topic / subtopic keyword scaffolder
    generate-content.ps1        Batch fill driver
  index.md                      Nav root
  {topic}/                      Flat topic folder (e.g. java/)
    index.md                    Topic nav root + file table
    Topic - Subtopic.md         Multi-keyword file (>=5 keywords)
```

No tier directories. No `CODE-NNN` filename prefixes.

## Version registry

| Constant            | Value | Meaning                                   |
| ------------------- | ----- | ----------------------------------------- |
| `SPEC_VERSION`      | 1     | Integer for `version:` in completed files |
| `SPEC_LABEL`        | v1.0  | Human label for commits                   |
| `KEYWORD_GEN_LABEL` | v1.0  | Keyword generator spec version            |
| `STUB_VERSION`      | 0     | Placeholder skeleton                      |

## File model

- Each sub-topic file lives directly under its topic folder.
- File name: `Topic - Subtopic.md` with **SPACE-HYPHEN-SPACE**
  separators. Never em dash. Example: `Java - Collections.md`.
- Each file MUST contain **at least 5 keywords**. Never per-keyword
  files. Split a subtopic if natural keyword count drops below 5
  (combine into a sibling subtopic).
- Keyword blocks within a file are separated by:
  blank-line / `---` / blank-line / `---` / blank-line (double rule).

## Keyword Level Coverage (MANDATORY)

Every topic MUST cover ALL knowledge levels from
`bytes/_config/BYTES_KEYWORD_GENERATOR.md`:

| Level | Icon | Name         | Min KW | What It Covers                          |
| ----- | ---- | ------------ | ------ | --------------------------------------- |
| L0    | 🌱   | Orientation  | 3-5    | Why it exists, ecosystem, before it     |
| L1    | ★☆☆  | Foundational | 4-6    | Core vocabulary, building blocks, setup |
| L2    | ★★☆  | Working      | 5-8    | Patterns, daily usage, idioms           |
| L3    | ★★☆+ | Intermediate | 5-10   | Design decisions, trade-offs, internals |
| L4    | ★★★  | Expert       | 5-10   | Production diagnostics, failure modes   |
| L5    | 🔥   | Architect    | 3-5    | Strategy, migration, governance         |
| L6    | 🔬   | Creator      | 2-3    | Theory, specification, research         |
| META  | 🧠   | Meta-Skills  | 2-3    | Transferable thinking patterns          |

**File-level rule: >=5 keywords per file.** A level with more than
5 keywords splits across multiple files.

**Suggested file structure per topic:**

- `{Topic} - Foundations.md` for L0 + L1 keywords (combined >=5).
- Core working files for L2-L4 keywords (>=5 each, split as needed:
  e.g. `{Topic} - Collections.md`, `{Topic} - Concurrency.md`).
- `{Topic} - Architecture and Strategy.md` for L5 + L6 + META
  (combined >=5).

A topic missing any level is INCOMPLETE. Always verify before
generating content.

## Byte structure - 14 sections per keyword (exact order)

| #   | Section                                             | Required?              |
| --- | --------------------------------------------------- | ---------------------- |
| 1   | `# Keyword Name`                                    | Required               |
| 2   | TL;DR (<=25 words)                                  | Required               |
| 3   | The Problem in One Paragraph                        | Required               |
| 4   | Textbook Definition                                 | Required               |
| 5   | First Principles (invariants + derived + trade-off) | **DEPTH SIGNAL**       |
| 6   | Gradual Depth (Levels 1..N by difficulty)           | **PROGRESSION SIGNAL** |
| 7   | How It Works (ASCII + Mermaid flow)                 | Required               |
| 8   | Mental Model (analogy + mapping + breaks-when)      | Required               |
| 9   | Production Reality (ONE failure, deep)              | **DEPTH SIGNAL**       |
| 10  | Decision Snap (use when / avoid when / prefer X)    | Required               |
| 11  | Top Traps (3-5 misconception rows)                  | Required               |
| 12  | Learning Ladder (Prereq -> THIS -> Next)            | **PROGRESSION SIGNAL** |
| 13  | The Surprising Truth (1 fact)                       | Required               |
| 14  | Revision Card (3 lines you must remember)           | Required               |

## Word targets (per keyword)

| Difficulty       | Target      | Levels in section 6 | Invariants in section 5 |
| ---------------- | ----------- | ------------------- | ----------------------- |
| Easy (1 star)    | 600-900     | 2                   | 2                       |
| Medium (2 stars) | 900-1,200   | 3                   | 2-3                     |
| Hard (3 stars)   | 1,200-1,500 | 4                   | 3+                      |

## YAML frontmatter (file-level)

```yaml
---
title: "Topic - Subtopic"
topic: Topic Name
subtopic: Subtopic Name
keywords:
  - Keyword One
  - Keyword Two
  - Keyword Three
  - Keyword Four
  - Keyword Five
difficulty_range: easy | medium | hard | mixed
status: draft | in-progress | complete
version: 0 | 1
layout: default
parent: "Topic Name"
grand_parent: "Bytes"
nav_order: N
permalink: /bytes/topic-folder/subtopic-slug/
---
```

`keywords` MUST list every `# Keyword Name` heading inside the file,
in the same order. Minimum 5 entries.

## File naming

`Topic - Subtopic.md` with SPACE-HYPHEN-SPACE separator. Never em
dash. Title in filename matches `title:` (minus quoting).
Examples:

- `Java - Collections.md`
- `Java - Garbage Collection.md`
- `React - Hooks.md`
- `Kubernetes - Networking.md`

## ID system

There are no per-keyword IDs in bytes. Cross-references to sister
systems (when one exists) use the keyword title verbatim, not an
opaque code.

## Formatting rules (non-negotiable)

- No em dashes anywhere.
- Code lines max 70 chars.
- Every `###` heading preceded by `---` divider with blank lines.
- ASCII diagrams max 59 chars wide.
- Every diagram has DUAL format: ASCII first, then equivalent
  ` ```mermaid ` block immediately below.
- Supported Mermaid: `flowchart`, `sequenceDiagram`,
  `stateDiagram-v2`, `classDiagram`, `erDiagram`, `mindmap`.
- BAD code before GOOD code in section 8 mental model examples and
  anywhere code appears.
- File starts at byte 0 with `---`. UTF-8 no BOM.
- Double-quote any YAML title containing `: ` (colon + space).

## Voice

Precise like Josh Bloch. Clear like Martin Fowler. Intuitive like
Feynman. Production-scarred like a senior systems architect.
Interview-ready like a FAANG bar raiser.

## Validation before commit

```pwsh
python bytes/_config/validate-byte.py path/to/Topic - Subtopic.md
```

Validator checks: file frontmatter complete, `keywords[]` matches
heading list, >=5 keywords, every keyword block has all 14 sections
present and ordered, word count per keyword in range, Prereq/Next
titles in section 12 resolve to known keywords, ASCII+Mermaid
pairing, no em dashes, line length.

## Scaffold Workflow (optional)

Content scaffolding is no longer required for content generation.
The agent reads `keywords:` from each file's YAML frontmatter and
generates content directly. Use scaffold only to preview file
structure:

1. **Scaffold (optional):** `& "$env:USERPROFILE\.local\bin\python3.14.exe" bytes/_config/bytes_scaffold.py <topic>`
2. **Generate content:** Use `@bytes-generate-entries` prompt or
   `/bytes` agent. The agent reads keywords from frontmatter and
   produces the 14 sections per keyword directly.
3. **Validate:** Run `validate-byte.py` before commit.

## Git workflow

```pwsh
git add bytes/ .github/
git commit -m "feat: add {Topic} - {Subtopic} byte file"
# Do NOT git push without explicit user approval
```
