---
mode: agent
description: "Fill one or more multi-keyword byte files end-to-end per v1.0 spec. Hits every depth and progression signal for every keyword."
---

# Generate byte content

Fill a multi-keyword byte file (or a batch) with v1.0-compliant
content. Each file has >=5 keywords; each keyword has its own 14
sections.

## Inputs

- `target`: path to one file OR a topic folder (batch mode).
- Optional: `tone` (default = "concise, technical, no-fluff").

## Workflow per file

1. Read the file. Parse file-level frontmatter (`keywords[]`,
   `difficulty_range`).
2. Read `bytes/_config/BYTES_PROMPT.md` master spec.
3. Split the file into keyword blocks on the double-rule separator.
4. Confirm each keyword's difficulty -> word target -> levels count
   -> invariants count.
5. For each keyword block, fill sections 2..14 in order. Section 1
   (`# Keyword Name`) is fixed.
6. For each section, enforce its specific rules from the spec.
7. Quality gates after writing each keyword:
   - Word count in range for that keyword's difficulty.
   - First Principles has the required invariant count.
   - Gradual Depth has the required level count.
   - Production Reality has named diagnostic + named fix.
   - Learning Ladder names a Prereq and a Next keyword.
   - TL;DR <= 25 words.
   - All diagrams: ASCII + Mermaid pair.
   - No em dashes. Code <=70 chars/line.
8. Verify keyword separator is preserved between blocks:
   blank-line / `---` / blank-line / `---` / blank-line.
9. Run validator: `python bytes/_config/validate-byte.py <path>`.
10. Fix every validator error before reporting done.

## Hard rules

- Never invent CVEs, JEPs, RFCs, benchmarks. Hedge if unsure.
- BAD pattern before GOOD pattern.
- Set file `status: complete` and `version: 1` only after every
  keyword in the file passes the validator.

## Output

Per file: one line `filled <path> (<N> keywords, <total_wd> words, validator OK)`.
End batch with summary count.
