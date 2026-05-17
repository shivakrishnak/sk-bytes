---
mode: agent
description: "Fill one or more multi-keyword learn files end-to-end per LEARN_PROMPT.md v1.0. Auto-routes each keyword to its tier template (SIMPLE / INTERMEDIATE / COMPLEX)."
---

# Generate learn content

Fill a multi-keyword learn file (or a batch) with v1.0-compliant
content. Each file has >=5 keywords; each keyword gets the
template that matches its level.

## Inputs

- `target`: path to one file OR a topic folder (batch mode).
- Optional: `tone` (default = "concise, technical, no-fluff").

## Tier routing

Per keyword, read its level from `levels:` in YAML frontmatter
(or infer from `difficulty_range`) and apply the matching
template:

```
L0, L1            -> SIMPLE        9 sections, 400-700 words
L2, L3            -> INTERMEDIATE  13 sections, 900-1,300 words
L4, L5, L6, META  -> COMPLEX       16 sections, 1,400-2,000 words
```

## Pre-fill check (non-negotiable)

Before filling any file, count its COMPLEX-tier keywords
(L4, L5, L6, META). If count >= 10, do NOT fill. Instead:

1. Split the file into smaller files of 5-7 COMPLEX each.
2. Update frontmatter and TOC for each split file.
3. Update the topic index.md.
4. Then fill each smaller file separately.
   COMPLEX content is 1,400-2,000 words per keyword; 10+
   COMPLEX in one file produces 14,000-20,000+ words - too
   large to read, process, and maintain.

## Workflow per file

1. Read the file. Parse YAML frontmatter (`keywords[]`,
   `levels` map if present, `difficulty_range`).
2. Read [learn/\_config/LEARN_PROMPT.md](../../learn/_config/LEARN_PROMPT.md)
   v1.0 (master spec).
3. Split the body into keyword blocks on the double-rule
   separator. If empty, write fresh blocks.
4. For each keyword: determine tier, then write the
   tier-matching section list in order.
5. Apply per-section rules from LEARN_PROMPT.md Section 3
   (3.A / 3.B / 3.C). Apply Section 3a Code Example Taxonomy.
6. Quality gates after writing each keyword:
   **Structural (validator-enforced):**
   - Word count within tier target.
   - TL;DR within tier word cap (20/25/30).
   - Wrong-vs-Right BAD->GOOD pair present.
   - INTERMEDIATE/COMPLEX: production/failure example present.
   - INTERMEDIATE S6 and COMPLEX S7+S9: ASCII + Mermaid pair.
   - COMPLEX S5: >=3 CORE INVARIANTS.
   - COMPLEX S10: >=2 named Failure Modes with Diagnostic+Fix.
   - INTERMEDIATE S11 / COMPLEX S15: Prereq + Next titles
     resolve to real corpus keywords.
   - No em dashes. Code <=70 chars/line. ASCII <=59 chars.
     **Content quality (all 8 must pass per keyword):**
   - Search Again: engineer would NOT need to search elsewhere.
   - Feynman: smart beginner CAN follow without confusion.
   - Senior Engineer: learns something non-obvious.
   - Staff Engineer: would respect this explanation.
   - Production: could diagnose a real issue from this.
   - Retention: memorable analogy, mental model, memory hook.
   - Decision: clear when to use, avoid, prefer alternative.
   - Scale: addresses 10x/100x/1000x behavior changes.
     **Ten pillars per keyword (depth scales with tier):**
     INTUITION, MECHANISM, TRADE-OFF, FAILURE, DIAGNOSIS,
     SCALE, DECISION, MEMORY, TRANSFER, REALITY.
     **Forbidden:** generic textbook-only definitions, syntax
     demos, toy examples, "it depends" without framework,
     fabricated stories, surface explanations, formulaic
     sentence patterns repeated across keywords.
7. Preserve double-rule separator between blocks:
   blank-line / `---` / blank-line / `---` / blank-line.
8. Run validator:
   `python learn/_config/validate-learn.py <path>`.
9. Fix every validator error before reporting done.
10. Set `status: complete` and `version: 1` only after the
    validator passes for every keyword in the file.

## Hard rules

- Never invent CVEs, JEPs, RFCs, benchmarks, latency numbers,
  thread-pool sizes, or production stories. Hedge if unsure.
- BAD pattern before GOOD pattern in every Wrong-vs-Right.
- COMPLEX Further Reading uses real primary sources only.
- No emojis in prose; only inside the templates' section
  headers.

## Output

Per file: one line
`filled <path> (<N> keywords, <tier mix>, <total_wd> wd, validator OK)`.
End a batch with a summary table grouped by tier.
