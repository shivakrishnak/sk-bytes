---
mode: agent
description: "OPTIONAL preview: emit tier-aware [FILL:] stubs (SIMPLE / INTERMEDIATE / COMPLEX) for an existing sub-topic file. Content generation does NOT require this step."
---

# Preview learn structure (optional)

> **Scaffolding is no longer required for content generation.**
> The `/learn` agent reads `keywords:` from each file's YAML
> frontmatter and generates content directly. Use this prompt
> only when you want to preview the tier-matching section
> structure as `[FILL:]` stubs before manual editing.
>
> For real content, invoke `@learn-generate-entries` or the
> `/learn` agent instead.

## Inputs

- `topic`: Topic name (e.g. `Java`).
- `subtopic`: Subtopic name (e.g. `Collections`).
- Optional: `--tier SIMPLE|INTERMEDIATE|COMPLEX` to force one
  tier for all keywords (override).

The target file must already exist with valid YAML frontmatter
and a `keywords:` array of at least 5 entries. Generate those
via `@learn-generate-keywords` first (which applies
`learn/_config/LEARN_KEYWORD_GENERATOR.md` v1.0 -
non-negotiable).

## Steps

1. Confirm
   `learn/{topic-folder}/{Topic} - {Subtopic}.md` exists with
   `keywords:` >=5.
2. Optionally run:

   ```pwsh
   python learn/_config/learn_scaffold.py --file "{topic-folder}/{Topic} - {Subtopic}.md"
   # or force a tier for all keywords in this file:
   python learn/_config/learn_scaffold.py --file "..." --tier COMPLEX
   ```

   For each keyword the scaffolder selects the template tier:
   1. CLI `--tier` override, else
   2. per-keyword level from `levels:` map in frontmatter, else
   3. `difficulty_range` (easy=SIMPLE, medium=INTERMEDIATE,
      hard=COMPLEX, mixed=INTERMEDIATE default).

3. The body of the file is rewritten with the tier-matching
   `[FILL:]` template per keyword. Frontmatter is preserved.
4. Confirm the new file path and keyword count.
5. Do NOT fill content. Stop after structure preview.

## Output

`previewed <path> with N keywords (<tier mix>)`, plus a hint to
invoke `@learn-generate-entries` or the `/learn` agent to write
content. The agent can also operate on a frontmatter-only stub
directly, without preview.
