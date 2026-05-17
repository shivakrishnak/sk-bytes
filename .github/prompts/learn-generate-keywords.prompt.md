---
agent: learn
description: "Generate keyword list (L0..L6 + META) for a new or existing topic using LEARN_KEYWORD_GENERATOR.md v1.0. Emits folder, index.md, and per-subtopic stub files with frontmatter only."
---

# Generate learn keywords

Produce a complete keyword list for a topic following
`learn/_config/LEARN_KEYWORD_GENERATOR.md` v1.0 (non-negotiable),
then scaffold the folder + sub-topic stub files.

## Inputs

- `topic`: Topic name (e.g. `Caching`, `Java`).
- `topic_slug` (optional): folder name (defaults to lowercase
  with hyphens).
- Optional: existing `learn/<topic_slug>/index.md` to extend.

## Workflow

0. **Load the source of truth.** Read
   `learn/_config/LEARN_KEYWORD_GENERATOR.md` v1.0 end to end
   BEFORE emitting any keyword. Echo
   `GENERATED_FROM: LEARN_KEYWORD_GENERATOR.md v1.0` into the
   output header (Section 3.1). If the file is unavailable or
   its version is not v1.0, abort and report. No fallback. No
   ad-hoc lists.
1. Read the keyword spec:
   `learn/_config/LEARN_KEYWORD_GENERATOR.md` v1.0.
2. Generate the full keyword set:
   - Cover ALL levels L0..L6 + META per the table in Section 1.
   - Apply Rules 1-25 from the keyword spec. Key groups:
     **Coverage** (R1-R5): all levels, atomicity, no gaps.
     **Quality** (R6-R15): anti-patterns, practice, decision
     frameworks, retention, interview readiness.
     **Tiers** (R23): every keyword declares SIMPLE /
     INTERMEDIATE / COMPLEX.
     **Unlearn** (R24): at least 2 unlearn keywords per
     category.
   - At least 2 META keywords from unrelated source domains
     (Rule 25). A "source domain" is a distinct technical
     area (e.g., Networking, Databases, OS, Distributed
     Systems). Two META keywords must draw from different
     areas to ensure cross-domain transfer.
3. Group keywords into sub-topic files of **>=5 keywords**
   following the suggested split:
   - `{Topic} - Foundations.md` (L0 + L1)
   - `{Topic} - {Working Area}.md` (L2-L4)
   - `{Topic} - Architecture and Strategy.md` (L5 + L6 + META)
   **COMPLEX file size limit:** If any sub-topic file would
   contain 10+ COMPLEX-tier keywords (L4, L5, L6, META),
   split it into smaller files of 5-7 COMPLEX keywords each
   (max 9 per file). COMPLEX content is 1,400-2,000 words
   per keyword; 10+ becomes too large to process. Use
   descriptive subtopic names for each split.
4. Emit:
   - `learn/<topic_slug>/index.md` with the file table.
   - One sub-topic stub `.md` file per group, frontmatter-only,
     `status: draft`, `version: 0`, plus the keyword list.
5. Append the new topic to
   `learn/_config/topic-registry.md`.
6. Run the 20 quality checks defined in Section 4 of
   `LEARN_KEYWORD_GENERATOR.md` v1.0. Report any failures.

## Stub file frontmatter

```yaml
---
title: "Topic - Subtopic"
topic: Topic
subtopic: Subtopic
keywords:
  - Keyword One
  - Keyword Two
  - ...
levels:           # optional but recommended for mixed files
  Keyword One: L1
  Keyword Two: L2
  ...
difficulty_range: mixed
status: draft
version: 0
layout: default
parent: "Topic"
grand_parent: "Learn"
nav_order: N
permalink: /learn/topic-slug/subtopic-slug/
---
```

Body of the stub:

```
> Stub. Fill via @learn-generate-entries or the /learn agent
> per LEARN_PROMPT.md v1.0.
>
> Each keyword routes to a template tier (see frontmatter
> `levels:` map):
>   L0,L1 -> SIMPLE        (9 sections, 400-700 wd)
>   L2,L3 -> INTERMEDIATE  (13 sections, 900-1.3k wd)
>   L4+   -> COMPLEX       (16 sections, 1.4-2k wd)
```

## Output

Single line per file emitted:
`stub <path> (<N> keywords, <tiers summary>)`
plus index.md and topic-registry update lines.

End with a 20-check summary table (PASS/FAIL per check).

## Hard rules

- Never invent keywords outside the LEARN_KEYWORD_GENERATOR.md
  framework.
- Never skip a level (L0..L6 + META all required).
- Never emit a stub with `<5` keywords.
- File starts at byte 0 with `---`. UTF-8 no BOM. No em dashes.
