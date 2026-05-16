---
mode: agent
description: "Validate one or more learn files against LEARN_PROMPT.md v1.0 (tri-template) and report failures."
---

# Validate learn

Run the structural and content validator. The validator
auto-detects each keyword's tier and applies the matching
schema.

## Steps

1. Resolve target: single file or folder (recursive).
2. For each `.md` file (excluding `index.md`):

   ```pwsh
   python learn/_config/validate-learn.py <path>
   ```

3. Collect errors. Categorize:
   - **Frontmatter**: missing field, wrong type, unquoted title
     with colon, keywords <5.
   - **Structure**: missing / reordered / duplicate section for
     the detected tier (9 / 13 / 16). Tier-mismatch.
   - **Content**:
     - TL;DR over its tier cap (20 / 25 / 30 words).
     - Word count out of tier range
       (400-700 / 900-1,300 / 1,400-2,000).
     - COMPLEX First Principles with <3 invariants.
     - COMPLEX Failure Modes with <2 named failures or missing
       Diagnostic / Fix labels.
     - Missing Wrong-vs-Right BAD/GOOD pair.
     - INTERMEDIATE / COMPLEX missing production or failure
       example signal.
     - Learning Ladder references unknown corpus keywords.
   - **Formatting**: em dash present, code line >70 chars,
     ASCII >59 chars, missing Mermaid pair on a mandatory
     diagram, missing `---` divider, BOM present.
4. Report a table: file | tier | error type | line | detail.
5. Do NOT auto-fix. Report only; user decides.

## Output

Markdown table of failures. End with totals:
`N files passed, M files failed, K total errors`.
