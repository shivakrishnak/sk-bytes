# GitHub Copilot - sk-learn Workspace Instructions

This workspace is **sk-learn**: a learning ladder of bite-sized
study units. One atomic keyword per template tier (SIMPLE /
INTERMEDIATE / COMPLEX), depth-first and progression-first.

## How instructions load

| Context                  | Loads                                        |
| ------------------------ | -------------------------------------------- |
| Any interaction          | This file (lean overview + shared rules)     |
| Editing `learn/**` files | `.github/instructions/learn.instructions.md` |
| Using `/learn` agent     | Agent instructions + reads spec on demand    |
| Using `@learn-*` prompts | Prompt-specific instructions                 |

## Quick reference

| Item                | Location                                            |
| ------------------- | --------------------------------------------------- |
| Content spec (v1.0) | `learn/_config/LEARN_PROMPT.md`                     |
| Keyword spec (v1.0) | `learn/_config/LEARN_KEYWORD_GENERATOR.md`          |
| Topic registry      | `learn/_config/topic-registry.md`                   |
| Topic scaffolder    | `learn/_config/generate-keywords.ps1`               |
| Preview emitter     | `learn/_config/learn_scaffold.py` (optional)        |
| Validator           | `learn/_config/validate-learn.py`                   |
| Auto-instructions   | `.github/instructions/learn.instructions.md`        |
| Agent               | `.github/agents/learn.agent.md`                     |
| Keyword-gen prompt  | `.github/prompts/learn-generate-keywords.prompt.md` |

**Spec Versions**: content `SPEC_VERSION` = 1 (v1.0); keyword
generator = v1.0. Three templates auto-selected by keyword level:

| Tier         | Levels        | Sections | Words       |
| ------------ | ------------- | -------- | ----------- |
| SIMPLE       | L0, L1        | 9        | 400-700     |
| INTERMEDIATE | L2, L3        | 13       | 900-1,300   |
| COMPLEX      | L4,L5,L6,META | 16       | 1,400-2,000 |

**NON-NEGOTIABLE:** Any list of concepts, sub-topics, keywords,
roadmap nodes, or learning paths - for any skill, language,
framework, CS topic, free-text blob, or job description - MUST
be generated through `learn/_config/LEARN_KEYWORD_GENERATOR.md`
v1.0. The agent loads that file end to end before emitting any
list. Halt and report if the file is unavailable or its version
is not v1.0. No ad-hoc lists. No shortcuts.

## Shared rules

### Encoding safety

- Always `pwsh` (PowerShell 7+), never `powershell.exe`.
- UTF-8 without BOM: `[System.Text.UTF8Encoding]::new($false)`.
- Python path: `$env:USERPROFILE\.local\bin\python3.14.exe` if
  present, otherwise `python`.

### Formatting (non-negotiable)

- No em dashes (U+2014) anywhere. No en dashes (U+2013) either.
  Regular ASCII hyphens only.
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
git add learn/ .github/
git commit -m "feat: <description>"
# Do NOT git push without explicit user approval
```

## Default behaviour

- When asked to work on learn content: read
  `learn/_config/LEARN_PROMPT.md` for the full spec including
  the three templates (SIMPLE / INTERMEDIATE / COMPLEX).
- When asked to generate or validate content: invoke the
  matching `@learn-*` prompt or the `/learn` agent.
- When editing `learn/**`, the learn instructions auto-load with
  the tri-template structure and validation rules.
- Always validate before committing:
  `python learn/_config/validate-learn.py`.
- Any keyword / sub-topic / roadmap list MUST be generated
  through `learn/_config/LEARN_KEYWORD_GENERATOR.md` v1.0 and
  carry `GENERATED_FROM: LEARN_KEYWORD_GENERATOR.md v1.0` plus
  `ARCHETYPE`, `MODE`, and `PROVENANCE` in its header.

## Quality standard (non-negotiable)

Content quality MUST be world-class / masterclass-level.
Not optional. Not best-effort. Every output must feel like
a senior principal engineer teaching a curious engineer
after surviving real production failures - not an LLM
summarizing Wikipedia.

### Eight quality tests (all must pass)

| #   | Test            | Question                                                   | FAIL if |
| --- | --------------- | ---------------------------------------------------------- | ------- |
| 1   | Search Again    | Would a serious engineer still need to search elsewhere?   | YES     |
| 2   | Feynman         | Could a smart beginner understand without confusion?       | NO      |
| 3   | Senior Engineer | Would a senior engineer learn something useful?            | NO      |
| 4   | Staff Engineer  | Would a staff/principal engineer respect this explanation? | NO      |
| 5   | Production      | Could someone diagnose a real production issue from this?  | NO      |
| 6   | Retention       | Will the reader remember this next month?                  | NO      |
| 7   | Decision        | Could the reader decide when to use or avoid this?         | NO      |
| 8   | Scale           | Does it address what changes at 10x / 100x / 1000x?        | NO      |

### Benchmark caliber

- Explanation quality: Feynman, Josh Bloch, Martin Fowler,
  Rich Hickey, Martin Kleppmann, Brendan Gregg.
- Engineering depth: Google / Netflix / Uber / Cloudflare
  engineering blogs, AWS architecture docs.
- Pedagogical quality: MIT / Stanford-level clarity and rigor.

### Ten mandatory pillars (depth scales with tier)

Every non-trivial explanation covers: INTUITION, MECHANISM,
TRADE-OFF, FAILURE, DIAGNOSIS, SCALE, DECISION, MEMORY,
TRANSFER, REALITY.

### Forbidden patterns

- Generic textbook definitions without insight.
- API documentation disguised as explanation.
- Syntax-only or hello-world code examples.
- Toy examples without production relevance.
- Vague advice ("it depends") without decision framework.
- Fabricated benchmarks, CVEs, or production stories.
- Surface-level explanations that skip WHY.
- "Best practice" claims without reasoning.
- Repetition across sections within a keyword.
- Walls of prose without structure.
- Formulaic sentence patterns repeated across keywords.
