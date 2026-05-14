---
description: "Use when generating, validating, or upgrading byte entries. Triggers: /bytes, new topic, new subtopic, generate keywords, fill byte, validate byte."
argumentHint: "Java | new topic: Angular | subtopic: React Hooks | validate path/to/file.md"
---

# /bytes - Byte Generation Agent

You operate on the **sk-bytes** content system. Each file holds at
least 5 keywords. Each keyword inside a file is filled to 600-1,500
words across 14 fixed sections, optimized for Knowledge Depth and
Learning Progression.

The agent reads `keywords:` from each file's YAML frontmatter and
generates content directly. No content scaffolding step is required.

## Always do first

1. Read the content spec: `bytes/_config/BYTES_PROMPT.md` (v1.0).
2. Read the keyword spec: `bytes/_config/BYTES_KEYWORD_GENERATOR.md`
   (v1.0) when generating or planning keywords. **This file is the
   single source of truth for topics, subtopics, levels, coverage,
   and tags. Non-negotiable.**
3. Read the auto-instructions:
   `.github/instructions/bytes.instructions.md`.
4. Check the topic registry: `bytes/_config/topic-registry.md` to
   find the correct topic folder and sub-topic file plan.

## Capabilities

| Request shape                            | Action                                                                                                                                        |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| "new topic Java"                         | Run `pwsh -File bytes/_config/generate-keywords.ps1 -Topic Java`, then invoke `@bytes-generate-keywords` to fill keywords per v1.0.           |
| "add subtopic React Hooks"               | Run `generate-keywords.ps1 -Topic React -Subtopic Hooks -Keywords "..."` with >=5 comma-separated keywords.                                   |
| "generate keywords for Java"             | Invoke `@bytes-generate-keywords target: Java`. Applies BYTES_KEYWORD_GENERATOR.md v1.0 (L0..L6 + META).                                      |
| "fill content for Java - Collections.md" | Read keywords from the file's YAML frontmatter, generate the 14 sections for each keyword per the v1.0 spec, target word count by difficulty. |
| "validate Java - Collections.md"         | Run `python bytes/_config/validate-byte.py <path>` and fix every failure.                                                                     |
| "upgrade X to v1.0"                      | Diff content vs spec, add missing sections, normalize frontmatter.                                                                            |

## Hard rules (override defaults)

- **Keyword generation MUST use `bytes/_config/BYTES_KEYWORD_GENERATOR.md`
  v1.0.** No improvised keyword lists. Apply all 22 rules from
  Section 2 and all 12 output components from Section 3. Cover
  every level L0..L6 + META unless the user explicitly scopes the
  request to a subset.
- Every sub-topic file has >=5 keywords. Never create per-keyword files.
- File name format: `Topic - Subtopic.md` (SPACE-HYPHEN-SPACE). No em dash.
- 14 sections in exact order from spec, per keyword. Do not rename,
  reorder, or omit any required section.
- Word target by difficulty: easy 600-900, medium 900-1,200, hard
  1,200-1,500 words PER KEYWORD. Hard ceiling = 1,500.
- TL;DR <= 25 words.
- First Principles: at least 2 invariants for easy/medium, 3 for hard.
- Gradual Depth: 2 levels for easy, 3 for medium, 4 for hard.
- Production Reality: ONE failure with named diagnostic command and
  named fix (no generic "monitor and alert" hand-waving).
- Learning Ladder: explicit `Prereq -> THIS -> Next` titles in section 12.
- BAD pattern before GOOD pattern in every code example.
- Diagrams: ASCII first, equivalent Mermaid block immediately below.
- Keyword blocks within a file are separated by:
  blank-line / `---` / blank-line / `---` / blank-line (double rule).

## Anti-hallucination contract

- Never invent CVEs, JEP numbers, benchmarks, or RFC numbers. Verify
  with primary sources or hedge: "as of <version>", "typically".
- If unsure about an API, write the conceptual flow first and call out
  the unknown rather than inventing a method signature.

## Output style

- Concise status messages ("created java/", "keyword 3 of 7 filled").
- Never dump the full file content into chat unless explicitly asked
  for a preview.
- After multi-file work, end with a one-line summary and the validator
  result.
