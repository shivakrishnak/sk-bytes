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
3. Author content via the `/learn` agent or `@learn-*` prompts
   (see below).
4. Validate before commit:
   `python learn/_config/validate-learn.py path/to/file.md`

## Using the `/learn` agent

The agent is a single entry point that routes work to the right
prompt and enforces every spec. Invoke it in Copilot Chat:

```
/learn <request in plain English>
```

Examples:

- `/learn add a new topic for Kafka, levels L0..L4`
- `/learn fill keywords in learn/java/Java - Collections.md`
- `/learn validate everything under learn/java/`
- `/learn turn this JD into a roadmap: <paste JD>`

What the agent does on every turn:

1. Reads [.github/agents/learn.agent.md](.github/agents/learn.agent.md)
   and follows the **source of truth refusal protocol**: before
   emitting any keyword / sub-topic / roadmap list, it loads
   [learn/\_config/LEARN_KEYWORD_GENERATOR.md](learn/_config/LEARN_KEYWORD_GENERATOR.md)
   v1.0 end to end. Wrong version or missing file = HALT.
2. Picks the matching `@learn-*` prompt for your intent.
3. Auto-routes each keyword to its tier template (SIMPLE /
   INTERMEDIATE / COMPLEX) based on level.
4. Stops for your approval before destructive or shared-state
   actions (git push, large rewrites, deletions).

## Using `@learn-*` prompts directly

Use a prompt when you know exactly which step you want. Each
prompt is in `.github/prompts/` and runs in Copilot Chat by
typing `@<name>`:

| Prompt                                                                          | Purpose                                                                                                                                                                                                                              |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`@learn-generate-keywords`](.github/prompts/learn-generate-keywords.prompt.md) | Generate the keyword / roadmap list for a topic, language, framework, CS concept, free-text blob, or job description. Loads `LEARN_KEYWORD_GENERATOR.md` v1.0 and emits `GENERATED_FROM`, `ARCHETYPE`, `MODE`, `PROVENANCE` headers. |
| [`@learn-generate-entries`](.github/prompts/learn-generate-entries.prompt.md)   | Fill content for each keyword in a file, routing per tier template per `LEARN_PROMPT.md` v1.0.                                                                                                                                       |
| [`@learn-scaffold`](.github/prompts/learn-scaffold.prompt.md)                   | Emit optional `[FILL:]` placeholder previews before full generation.                                                                                                                                                                 |
| [`@learn-build-ladder`](.github/prompts/learn-build-ladder.prompt.md)           | Build / refresh a topic's `learning-path.md` ladder from the existing keywords.                                                                                                                                                      |
| [`@learn-validate`](.github/prompts/learn-validate.prompt.md)                   | Run the tri-template validator on one file, a topic, or the whole `learn/` tree and report issues.                                                                                                                                   |

Typical authoring flow for a new topic:

```
@learn-generate-keywords    # produce the keyword list and stub files
@learn-scaffold             # (optional) preview [FILL:] placeholders
@learn-generate-entries     # fill each keyword tier-by-tier
@learn-build-ladder         # emit learning-path.md
@learn-validate             # final check before commit
```

Non-negotiable: any list of concepts, sub-topics, keywords,
roadmap nodes, or learning paths MUST come through
`@learn-generate-keywords` (which loads
`LEARN_KEYWORD_GENERATOR.md` v1.0). No ad-hoc lists, no shortcuts.

## Conventions (shared with sister systems)

- UTF-8 without BOM. File starts at byte 0 with `---`.
- No em dashes (U+2014). No en dashes (U+2013). ASCII hyphens only.
- Code lines max 70 chars. ASCII diagrams max 59 chars wide.
- Every mandatory diagram uses DUAL format: ASCII first, then
  equivalent Mermaid block.
- BAD pattern before GOOD pattern in code examples.
- Always `pwsh` (PowerShell 7+), never `powershell.exe`.

## License

TBD by author.
