---
mode: agent
description: "OPTIONAL preview: emit 14-section [FILL:] stubs for an existing sub-topic file. Content generation does NOT require this step."
---

# Preview byte structure (optional)

> **Scaffolding is no longer required for content generation.**
> The `/bytes` agent reads `keywords:` from each file's YAML
> frontmatter and generates content directly. Use this prompt
> only when you want to preview the 14-section structure as
> `[FILL:]` stubs before manual editing.
>
> For real content, invoke `@bytes-generate-entries` or the
> `/bytes` agent instead.

## Inputs (collect from user)

- `topic`: Topic name (e.g. `Java`).
- `subtopic`: Subtopic name (e.g. `Collections`).

The target file must already exist with valid YAML frontmatter
and a `keywords:` array of at least 5 entries. Generate those via
`@bytes-generate-keywords` first (which applies
`bytes/_config/BYTES_KEYWORD_GENERATOR.md` v1.0 - non-negotiable).

## Steps

1. Confirm the target file exists at
   `bytes/{topic-folder}/{Topic} - {Subtopic}.md` and has valid
   YAML frontmatter with a `keywords:` array of >=5 entries.
2. Optionally run:
   ```pwsh
   python bytes/_config/bytes_scaffold.py --file "{topic-folder}/{Topic} - {Subtopic}.md"
   ```
   This rewrites the body of the file with the 14-section
   `[FILL:]` template for each keyword, preserving the
   frontmatter.
3. Confirm the new file path and keyword count to the user.
4. Do NOT fill content. Stop after structure preview.

## Output

Single status line: `previewed <path> with N keywords`, plus
next-step suggestion to invoke `@bytes-generate-entries` or the
`/bytes` agent to generate content (which can also operate
directly on the frontmatter-only stub without the preview step).
