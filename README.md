# sk-bytes

A learning ladder of byte-sized study units. Multi-keyword files
organized by topic, with each keyword filled to 600-1,500 words and
optimized for **Knowledge Depth** and **Learning Progression**.

## What is a "byte"?

A byte is a dense study unit for a single concept. It is shorter than a
full dictionary entry but deeper than a flashcard. Every byte hits two
non-negotiable depth signals (First Principles invariants + one fully
developed Production failure mode) and two non-negotiable progression
signals (Gradual Depth Levels + explicit Learning Ladder).

## File model

- Files are grouped by **topic** in a flat folder (e.g. `bytes/java/`).
- Each file is named `Topic - Subtopic.md` (SPACE-HYPHEN-SPACE, no em dash).
- Each file contains **at least 5 keywords**. Never per-keyword files.
- Each keyword inside the file is its own 14-section byte.

## Sister systems (not included here)

- **/dictionary** (24 sections, 1.5-12k wd): mastery reference manual.
- **/interview** (19 sections, Q&A): interview drill.
- **/bytes** (14 sections, 600-1.5k wd per keyword): study sequence.

## Repo layout

```
sk-bytes/
  _config.yml                          Jekyll just-the-docs
  Gemfile
  index.md                             Site root
  bytes/
    index.md                           Bytes nav root
    _config/
      BYTES_PROMPT.md                  Master content spec v1.0
      BYTES_KEYWORD_GENERATOR.md       Keyword generator spec v1.0
      README.md                        Generation guide
      topic-registry.md                Topic-to-folder map
      bytes_scaffold.py                Optional preview emitter
      validate-byte.py                 Section + frontmatter validator
      generate-keywords.ps1            Topic / subtopic keyword scaffolder
      generate-content.ps1             Batch fill driver
    {topic}/                           Flat topic folders
      index.md                         Topic nav root
      Topic - Subtopic.md              Multi-keyword file (>=5 kw)
  .github/
    copilot-instructions.md            Root contract
    agents/bytes.agent.md              Custom Copilot agent
    instructions/bytes.instructions.md Auto-attach for bytes/**
    prompts/                           Prompt files
    workflows/pages.yml                GitHub Pages deploy
```

## Quick start

1. Install Jekyll: `bundle install`
2. Local preview: `bundle exec jekyll serve`
3. To author a byte: invoke the `/bytes` agent in Copilot Chat, or
   use `@bytes-generate-entries` / `@bytes-generate-keywords`. The
   agent reads keywords from each file's YAML frontmatter and
   generates content directly.
4. Validate before commit: `python bytes/_config/validate-byte.py path/to/byte.md`

## Conventions (shared with sister systems)

- UTF-8 without BOM. File starts at byte 0 with `---`.
- No em dashes. Regular hyphens only.
- Code lines max 70 chars. ASCII diagrams max 59 chars wide.
- Every diagram uses DUAL format: ASCII first, then equivalent
  Mermaid block.
- BAD pattern before GOOD pattern in code examples.
- Always `pwsh` (PowerShell 7+), never `powershell.exe`.

## License

TBD by author.
