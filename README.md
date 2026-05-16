# sk-learn

A learning ladder of bite-sized study units. Multi-keyword files
organized by topic; each keyword routed to one of three templates
(SIMPLE / INTERMEDIATE / COMPLEX) based on its level, depth-first
and progression-first.

## What is a "learn"?

A learn is a dense study unit for a single atomic concept. It is
shorter than a full dictionary entry but deeper than a flashcard.
Three templates cover different complexity tiers:

| Tier         | Levels        | Sections | Words       | Use for                       |
| ------------ | ------------- | -------- | ----------- | ----------------------------- |
| SIMPLE       | L0, L1        | 9        | 400-700     | Orientation + vocabulary      |
| INTERMEDIATE | L2, L3        | 13       | 900-1,300   | Working trade-offs, decisions |
| COMPLEX      | L4,L5,L6,META | 16       | 1,400-2,000 | Failure modes, architecture   |

Every learn hits the depth and progression signals appropriate to
its tier: SIMPLE makes the concept stick; INTERMEDIATE adds
trade-offs and a learning ladder; COMPLEX adds first-principles
invariants, named failure modes with diagnostic commands, and
primary-source citations.

## File model

- Files grouped by **topic** in a flat folder (e.g. `learn/java/`).
- Each file: `Topic - Subtopic.md` (SPACE-HYPHEN-SPACE).
- Each file contains **at least 5 keywords**. Never per-keyword
  files.
- Each keyword inside a file is rendered with its tier-matching
  template, auto-routed from its level.

## Sister systems (not included here)

- **/dictionary** (24 sections, 1.5-12k wd): mastery reference.
- **/interview** (19 sections, Q&A): interview drill.
- **/learn** (tri-template, 400-2,000 wd per keyword): study
  sequence.

## Repo layout

```
sk-learn/
  _config.yml                          Jekyll just-the-docs
  Gemfile
  index.md                             Site root
  learn/
    index.md                           Learn nav root
    _config/
      LEARN_PROMPT.md                  Master content spec v1.0
      LEARN_KEYWORD_GENERATOR.md       Keyword generator spec v1.0
      README.md                        Generation guide
      topic-registry.md                Topic-to-folder map
      learn_scaffold.py                Optional preview emitter
      validate-learn.py                Tri-template validator
      generate-keywords.ps1            Topic / subtopic keyword scaffolder
      generate-content.ps1             Batch fill driver
    {topic}/                           Flat topic folders
      index.md                         Topic nav root
      Topic - Subtopic.md              Multi-keyword file (>=5 kw)
  .github/
    copilot-instructions.md            Root contract
    agents/learn.agent.md              /learn agent
    instructions/learn.instructions.md Auto-attach for learn/**
    prompts/                           @learn-* prompt files
    workflows/pages.yml                GitHub Pages deploy
```

## Quick start

1. Install Jekyll: `bundle install`
2. Local preview: `bundle exec jekyll serve`
3. To author content: invoke the `/learn` agent in Copilot Chat,
   or use `@learn-generate-entries` / `@learn-generate-keywords`.
   The agent reads `keywords:` from each file's YAML frontmatter
   and writes content tier-by-tier.
4. Validate before commit:
   `python learn/_config/validate-learn.py path/to/file.md`

## Conventions (shared with sister systems)

- UTF-8 without BOM. File starts at byte 0 with `---`.
- No em dashes. Regular hyphens only.
- Code lines max 70 chars. ASCII diagrams max 59 chars wide.
- Every mandatory diagram uses DUAL format: ASCII first, then
  equivalent Mermaid block.
- BAD pattern before GOOD pattern in code examples.
- Always `pwsh` (PowerShell 7+), never `powershell.exe`.

## License

TBD by author.
