---
mode: agent
description: "Build or refresh the learning-path.md for a topic by topologically sorting keywords via section 12 (Learning Ladder) prereq graph."
---

# Build learning ladder

Generate the ordered curriculum for a topic folder.

## Steps

1. Resolve topic folder (e.g. `bytes/java/`).
2. Read every sub-topic file in the folder (excluding `index.md` and
   `learning-path.md`).
3. For each file, split into keyword blocks on the double-rule
   separator (`---` / `---`).
4. For each keyword block, parse:
   - keyword title from `# Keyword Name` heading,
   - difficulty from `Difficulty:` line or file `difficulty_range`,
   - prereq / next titles from section 12 (Learning Ladder).
5. Build a directed graph: edge from each `Prereq` keyword to the
   current keyword.
6. Topologically sort. Tie-break by difficulty asc, then file order.
7. Detect cycles. If found, report and abort.
8. Write `learning-path.md` with:
   - Frontmatter (`title`, `parent`, `nav_order: 1`).
   - Intro paragraph (2-3 lines).
   - Ordered list: `1. [Keyword Title](file.md#anchor) - <difficulty>`
   - Optional: grouped by difficulty band.
9. Report total keywords, depth (longest chain), any orphans.

## Output

```
learning-path.md updated: 42 keywords across 7 files, depth 5, 0 orphans, 0 cycles
```
