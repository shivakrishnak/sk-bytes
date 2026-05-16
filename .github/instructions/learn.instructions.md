---
description: Auto-attached rules for any work under learn/** - tri-template content, formatting, validation, git workflow.
applyTo: "learn/**"
---

# sk-learn Authoring Rules (auto-loaded under learn/\*\*)

These rules apply to **every file you create or edit in `learn/`**.
Master spec: [learn/\_config/LEARN_PROMPT.md](../../learn/_config/LEARN_PROMPT.md) v1.0.
Keyword spec: [learn/\_config/LEARN_KEYWORD_GENERATOR.md](../../learn/_config/LEARN_KEYWORD_GENERATOR.md) v1.0.

## 1. Three templates, one tier per keyword

Every keyword is routed to ONE of three templates based on its
level (set by the keyword generator). Never mix sections across
tiers within a single keyword.

| Tier         | Levels        | Sections | Words       | Diagrams     |
| ------------ | ------------- | -------- | ----------- | ------------ |
| SIMPLE       | L0, L1        | 9        | 400-700     | optional     |
| INTERMEDIATE | L2, L3        | 13       | 900-1,300   | S6 mandatory |
| COMPLEX      | L4,L5,L6,META | 16       | 1,400-2,000 | S7 + S9      |

### SIMPLE - 9 sections (L0, L1)

1. `# Keyword Name`
2. `**TL;DR** - ...` (<=20 words)
3. `### 🟢 What it is`
4. `### 🎯 Why it exists`
5. `### 🧠 Mental Model`
6. `### ⚙️ How it works`
7. `### ✏️ Minimal Example` (Wrong-vs-Right)
8. `### ⚡ When to use / Not to use`
9. `### ⚠️ One Gotcha`
10. `### 📇 Revision Card`

### INTERMEDIATE - 13 sections (L2, L3)

1. `# Keyword Name`
2. `**TL;DR** - ...` (<=25 words)
3. `### 🔥 The Problem in One Paragraph`
4. `### 📘 Textbook Definition`
5. `### 🧠 Mental Model`
6. `### ⚙️ How It Works` (ASCII + Mermaid mandatory)
7. `### 🛠️ Worked Example` (Wrong-vs-Right + Production)
8. `### ⚖️ Trade-offs`
9. `### ⚡ Decision Snap`
10. `### ⚠️ Top Traps` (3 rows)
11. `### 🪜 Learning Ladder`
12. `### 💡 The Surprising Truth`
13. `### 📇 Revision Card`

### COMPLEX - 16 sections (L4, L5, L6, META)

1. `# Keyword Name`
2. `**TL;DR** - ...` (<=30 words)
3. `### 🔥 Problem Statement`
4. `### 📜 Historical Context`
5. `### 🔩 First Principles` (>=3 CORE INVARIANTS)
6. `### 🧠 Mental Model`
7. `### 🧩 Components` (architecture diagram pair)
8. `### 📶 Gradual Depth` (4 layers)
9. `### ⚙️ How It Works` (ASCII + Mermaid mandatory)
10. `### 🚨 Failure Modes` (>=2 named + Diagnostic + Fix)
11. `### 🔬 Production Reality`
12. `### ⚖️ Trade-offs & Alternatives` (table vs >=2 systems)
13. `### ⚡ Decision Snap`
14. `### ⚠️ Top Traps` (5 rows)
15. `### 🪜 Learning Ladder`
16. Closing triplet: `**The Surprising Truth:**` + `**Further Reading:**` + `**Revision Card:**`

## 2. Code Example Taxonomy (LEARN_PROMPT.md Section 3a)

Every code example MUST answer at least one of: how is it used,
how does it fail, why this design, what breaks at scale, how do
experts debug, what is the trade-off, what mistake do beginners
make, how does production differ from tutorial.

| Tier         | Examples | Mandatory categories                    |
| ------------ | -------- | --------------------------------------- |
| SIMPLE       | 1-2      | Recognition + Wrong-vs-Right            |
| INTERMEDIATE | 2-4      | Wrong-vs-Right + Production + Failure   |
| COMPLEX      | 4-7      | Wrong-vs-Right + Production + Failure + |
|              |          | Scale + Debugging                       |

No syntax demos. No hello-world. Delete any snippet that fails
the eight-questions test.

## 3. YAML frontmatter (file level)

```yaml
---
title: "Topic - Subtopic"
topic: Topic
subtopic: Subtopic
keywords:
  - Keyword One
  - Keyword Two
  - Keyword Three
  - Keyword Four
  - Keyword Five
difficulty_range: easy | medium | hard | mixed
status: draft | in-progress | complete
version: 1
layout: default
parent: "Topic"
grand_parent: "Learn"
nav_order: N
permalink: /learn/topic-folder/subtopic-slug/
---
```

Rules:

- File starts at byte 0 with `---`. UTF-8 no BOM.
- Double-quote any title containing `: ` (colon-space).
- `keywords:` array has **>=5 entries** and matches the order of
  the `# Keyword Name` H1 headings inside the file.
- Keywords are separated by the double-rule divider:
  blank line, `---`, blank line, `---`, blank line.
- A `## Keywords` TOC block MUST appear between the closing
  `---` of frontmatter and the first `# Keyword` heading.
  Each entry is a numbered markdown link:
  `1. [Keyword Name](#anchor)` where the anchor follows
  kramdown GFM rules (lowercase, remove non-alphanum except
  spaces and hyphens, spaces to hyphens). The validator
  enforces entry count, text match, and anchor correctness.

## 4. Formatting (non-negotiable)

- No em dashes. Regular hyphens only.
- Code lines: max 70 chars.
- ASCII diagrams: max 59 chars wide.
- Mandatory diagrams use DUAL format: ASCII first, Mermaid
  second. Supported Mermaid types: `flowchart`,
  `sequenceDiagram`, `stateDiagram-v2`, `classDiagram`,
  `erDiagram`, `mindmap`.
- BAD pattern before GOOD pattern in every Wrong-vs-Right
  example.
- Bold keyword on first mention in Textbook Definition / What
  it is.

## 5. Anti-hallucination

- Never invent CVEs, JEPs, RFCs, benchmarks, latency figures,
  thread-pool sizes, scaling thresholds, or "production stories".
- Hedge: "implementation-dependent", "typically", "varies by
  version", "illustrative pattern".
- Cite primary sources in COMPLEX Further Reading (paper, RFC,
  JEP, official spec).

## 6. Validation (before commit)

```pwsh
python learn/_config/validate-learn.py path/to/file.md
```

The validator auto-detects each keyword's tier from its section
markers and applies the matching 9 / 13 / 16-section schema.
Fix every error before changing `status:` to `complete`.

## 7. Scaffolding (optional)

Content generation does NOT require pre-scaffolding. The `/learn`
agent reads `keywords:` from frontmatter and writes content
directly. Use the scaffold only for preview/manual editing:

```pwsh
python learn/_config/learn_scaffold.py --file "java/Java - X.md"
# Optional tier override (else inferred from level/difficulty):
python learn/_config/learn_scaffold.py --file "..." --tier COMPLEX
```

## 8. Git workflow (non-negotiable)

Every fix, addition, or edit MUST be committed immediately
after validation passes. Do not batch unrelated changes.

**Commit after every fix.** One logical change = one commit.

```pwsh
git add learn/ .github/
git commit -m "<type>: <scope> - <description>"
# Do NOT git push without explicit user approval.
```

**Commit types:**

| Type     | When                                       |
| -------- | ------------------------------------------ |
| feat     | New keyword, topic, or subtopic content    |
| fix      | Correct content, formatting, or validation |
| refactor | Restructure without changing meaning       |
| chore    | Config, scaffold, tooling, CI changes      |
| docs     | Spec, instructions, README updates         |

**Scope:** topic/subtopic slug (e.g., `java/language-core`).

**Examples:**

```pwsh
git commit -m "feat: java/language-core - add 5 keywords"
git commit -m "fix: java/exceptions-io - repair broken table"
git commit -m "chore: config - remove compress_html endings"
git commit -m "docs: instructions - add commit-after-fix rule"
```

**Sequence:** edit -> validate -> fix errors -> commit.
Never leave validated fixes uncommitted.

## 9. Shell

- Always `pwsh` (PowerShell 7+). Never `powershell.exe`.
- UTF-8 no BOM via `[System.Text.UTF8Encoding]::new($false)`.
- Python: `$env:USERPROFILE\.local\bin\python3.14.exe` if present,
  otherwise `python`.

## 10. Quality standard (non-negotiable)

Every keyword's content must pass all eight tests before the
keyword is considered done. Structural correctness (sections,
word count, diagrams) is necessary but not sufficient.

| #   | Test            | FAIL if answer is                                 |
| --- | --------------- | ------------------------------------------------- |
| 1   | Search Again    | a serious engineer would still search elsewhere   |
| 2   | Feynman         | a smart beginner could not follow                 |
| 3   | Senior Engineer | a senior engineer learns nothing new              |
| 4   | Staff Engineer  | a staff/principal engineer would not respect this |
| 5   | Production      | no one could diagnose a real issue from this      |
| 6   | Retention       | the reader will forget within a month             |
| 7   | Decision        | the reader cannot decide when to use or avoid     |
| 8   | Scale           | 10x / 100x / 1000x behavior is not addressed      |

**Ten pillars (depth scales with tier):** INTUITION, MECHANISM,
TRADE-OFF, FAILURE, DIAGNOSIS, SCALE, DECISION, MEMORY,
TRANSFER, REALITY.

**Forbidden patterns:** generic textbook-only definitions,
API-doc disguised as explanation, syntax-only / hello-world
examples, toy code without production relevance, "it depends"
without decision framework, fabricated benchmarks or stories,
surface-level explanations that skip WHY, "best practice"
without reasoning, formulaic repetition across keywords,
walls of prose without structure.
