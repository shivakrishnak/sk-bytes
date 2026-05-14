# GitHub Copilot - sk-bytes Workspace Instructions

This workspace is **sk-bytes**: a learning ladder of byte-sized study
units. ONE atomic keyword per file, 600-1,500 words, depth-first and
progression-first.

## How instructions load

| Context                  | Loads                                        |
| ------------------------ | -------------------------------------------- |
| Any interaction          | This file (lean overview + shared rules)     |
| Editing `bytes/**` files | `.github/instructions/bytes.instructions.md` |
| Using `/bytes` agent     | Agent instructions + reads spec on demand    |
| Using `@bytes-*` prompts | Prompt-specific instructions                 |

## Quick reference

| Item                | Location                                            |
| ------------------- | --------------------------------------------------- |
| Content spec (v1.0) | `bytes/_config/BYTES_PROMPT.md`                     |
| Keyword spec (v1.0) | `bytes/_config/BYTES_KEYWORD_GENERATOR.md`          |
| Topic registry      | `bytes/_config/topic-registry.md`                   |
| Topic scaffolder    | `bytes/_config/generate-keywords.ps1`               |
| Preview emitter     | `bytes/_config/bytes_scaffold.py` (optional)        |
| Validator           | `bytes/_config/validate-byte.py`                    |
| Auto-instructions   | `.github/instructions/bytes.instructions.md`        |
| Agent               | `.github/agents/bytes.agent.md`                     |
| Keyword-gen prompt  | `.github/prompts/bytes-generate-keywords.prompt.md` |

**Spec Versions**: content `SPEC_VERSION` = 1 (v1.0); keyword
generator = v1.0.
**NON-NEGOTIABLE:** Topic / subtopic / keyword generation MUST use
`bytes/_config/BYTES_KEYWORD_GENERATOR.md` v1.0 as the single source
of truth. No ad-hoc keyword lists.

## Shared rules

### Encoding safety

- Always `pwsh` (PowerShell 7+), never `powershell.exe`.
- UTF-8 without BOM: `[System.Text.UTF8Encoding]::new($false)`.
- Python path: `$env:USERPROFILE\.local\bin\python3.14.exe`.

### Formatting (non-negotiable)

- No em dashes anywhere. Regular hyphens only.
- Code lines max 70 chars.
- Diagrams: DUAL format - ASCII first (max 59 chars wide), then
  equivalent Mermaid block immediately below.
- Supported Mermaid types: `flowchart`, `sequenceDiagram`,
  `stateDiagram-v2`, `classDiagram`, `erDiagram`, `mindmap`.
- BAD pattern before GOOD pattern in all code examples.
- File MUST start at byte 0 with `---` (no BOM, no whitespace).
- Double-quote any YAML title containing `: ` (colon + space).

### Anti-hallucination

- Never invent benchmarks, latency numbers, scale claims, CVE
  details, or "production stories".
- Hedge when uncertain: "implementation-dependent", "typically",
  "varies by version".
- Cite primary sources (RFCs, JEPs, official docs) where possible.

### Git workflow

```pwsh
git add bytes/ .github/
git commit -m "feat: <description>"
# Do NOT git push without explicit user approval
```

## Default behaviour

- When asked to work on byte content: read
  `bytes/_config/BYTES_PROMPT.md` for the full spec.
- When asked to generate or validate bytes: invoke the
  matching `@bytes-*` prompt or `/bytes` agent.
- When editing `bytes/**`, the bytes instructions auto-load with the
  14-section template and validation rules.
- Always validate before committing: `python bytes/_config/validate-byte.py`.
