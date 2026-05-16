---
mode: agent
description: "Build or refresh learning-path.md for a topic by topologically sorting keywords via Learning Ladder (S11/S15) prereq graph."
---

# Build learning ladder

Generate the ordered curriculum for a topic folder.

## Steps

1. Resolve topic folder (e.g. `learn/java/`).
2. Read every sub-topic `.md` file (exclude `index.md` and
   `learning-path.md`).
3. For each file, split into keyword blocks on the double-rule
   separator (`---` / `---`).
4. For each keyword block, parse:
   - title from the `# Keyword Name` H1,
   - detected tier (presence of distinctive section markers),
   - level from optional `levels:` map in frontmatter, else
     infer from tier (L0/L1 for SIMPLE, etc.),
   - Prereq / Next titles from `### 🪜 Learning Ladder`
     (INTERMEDIATE S11 / COMPLEX S15). SIMPLE keywords are
     ordered by topic index appearance.
5. Build a directed graph: edge from each Prereq keyword to the
   current keyword.
6. Topologically sort. Tie-break by tier order
   (SIMPLE before INTERMEDIATE before COMPLEX), then by file
   order.
7. Detect cycles. If found, report and abort.
8. Write `learn/<topic>/learning-path.md` with:
   - Frontmatter (`title`, `parent`, `nav_order: 1`).
   - 2-3 line intro.
   - Ordered list: `1. [Title](file.md#anchor) - <tier>`.
   - Optional: grouped by tier band (SIMPLE / INTERMEDIATE /
     COMPLEX) with sub-headings.
9. Report: total keywords, longest chain depth, tier mix,
   orphans (no prereq listed by anyone), and cycles (must be 0).

## Output

```
learning-path.md updated: 42 keywords across 7 files,
  tiers SIMPLE 11 / INTERMEDIATE 22 / COMPLEX 9,
  depth 5, 0 orphans, 0 cycles
```
