---
mode: agent
description: "Generate keyword entries for a byte topic or subtopic using BYTES_KEYWORD_GENERATOR v1.0"
tools:
  - run_in_terminal
  - read_file
  - replace_string_in_file
  - create_file
  - list_dir
  - file_search
  - grep_search
---

# Bytes Keyword Generator - Topic / Subtopic Processor

Generate keyword entries for a byte topic, then sync the topic
`index.md` and create stub sub-topic files (each with 5+ keywords).

**Target:** `${input:target:Topic name (e.g. Java, Angular, Kubernetes) or "topic/subtopic" pair}`

If the target does not resolve to a topic folder under `bytes/`, stop
and return an error showing the valid formats.

---

## MASTER SPEC (NON-NEGOTIABLE)

The full keyword generation specification is in
`bytes/_config/BYTES_KEYWORD_GENERATOR.md` (Category Keyword
Generator - Master Prompt v1.0). **Apply it exactly. It is the
single source of truth for topics, subtopics, levels, coverage,
rules, and tags. Do not improvise keyword lists.**

Keep the workflow linear and scoped: validate the target, scan the
current topic state, generate only missing keywords (per the v1.0
spec), group keywords into sub-topic files (>= 5 keywords each),
sync `index.md`, and create stub files only when needed.

The byte content spec lives in `bytes/_config/BYTES_PROMPT.md` v1.0
and is applied during the SEPARATE content-fill step
(`@bytes-generate-entries` or `/bytes` agent). This prompt is
keyword generation only.

---

## Phase 0 - Resolve Target

Follow exactly one path. Do not combine paths.

**Step 1 - Identify input type:**

- Input is a topic name (e.g. `Java`, `Angular`) -> **Path A: full topic**
- Input is `topic/subtopic` (e.g. `java/Collections`) -> **Path B: single subtopic**
- Input matches neither format -> stop and return an error showing
  valid formats

**Path A - Full topic:** Look up the topic in
`bytes/_config/topic-registry.md`. If present, use its planned
sub-topic file mapping. If absent, generate the full level
distribution from BYTES_KEYWORD_GENERATOR.md and propose a sub-topic
split (each file >= 5 keywords).

**Path B - Single subtopic:** Resolve folder and file name. Confirm
the topic folder exists. Generate keywords for that subtopic only.

**Step 2 - Look up registry fields:**

| Field          | Source                                          |
| -------------- | ----------------------------------------------- |
| TOPIC_NAME     | Display name from `topic-registry.md`           |
| TOPIC_FOLDER   | Lowercase hyphenated folder name                |
| DICT_SOURCES   | Dictionary categories that seed keywords        |
| INDEX_PATH     | bytes/{TOPIC_FOLDER}/index.md                   |
| SUBTOPIC_FILES | Planned sub-topic file split (5+ keywords each) |

---

## Phase 1 - Scan Existing State

### 1a. Read topic `index.md`

```
Read: bytes/{TOPIC_FOLDER}/index.md
```

Extract:

- **EXISTING_FILES**: every sub-topic file row in the table
- **EXISTING_KEYWORDS**: every keyword listed in any sub-topic file
- **YAML_FRONTMATTER**: the complete YAML block (IMMUTABLE)
- **TITLE_HEADING**: the `# Topic Name` line (IMMUTABLE)
- **DESCRIPTION_LINE**: the one-sentence description (IMMUTABLE)

If `index.md` does NOT exist, treat the topic as new and proceed to
Phase 2 with no existing state.

### 1b. Scan actual sub-topic files

```
List: bytes/{TOPIC_FOLDER}/*.md (excluding index.md, learning-path.md)
```

For each sub-topic file:

- Extract `title:`, `topic:`, `subtopic:`, `keywords:` from YAML
- Extract `status:` (draft / in-progress / complete) and `version:`
- Count keywords. If a file has fewer than 5 keywords, FLAG it as a
  file-rule violation (do NOT auto-fix; report and stop).

Build a **FILE_INVENTORY** mapping subtopic -> keyword set.

### 1c. Detect sync issues

Compare EXISTING_FILES (from index.md) vs FILE_INVENTORY:

| Situation                     | Action                            |
| ----------------------------- | --------------------------------- |
| File in index AND on disk     | Already synced - no action        |
| File on disk but NOT in index | ORPHAN - add row to index         |
| File in index but NOT on disk | MISSING - flag, do NOT delete row |
| File with < 5 keywords        | Rule violation - flag and stop    |

Report all sync issues before proceeding.

---

## Phase 2 - Generate Keywords

Using `bytes/_config/BYTES_KEYWORD_GENERATOR.md` v1.0:

1. Generate the L0 -> L1 -> L2 -> L3 -> L4 -> L5 -> L6 -> META
   keyword set for the topic (per Section 1, Levels).
2. Apply all 22 rules from Section 2.
3. Apply all 10 knowledge dimensions from Rule 5.
4. Use the 12 output components from Section 3 (level blocks,
   sub-topic clustering, level milestones, confusion pairs,
   meta-skills, summary, learning path, cross-category deps).
5. Remove any keyword already present in EXISTING_KEYWORDS (no
   duplicates - Rule 8).
6. Tag every keyword: `🎯 ivw`, `⚠️ anti-{severity}`, `🔧 tool`,
   `🔴 inc`, `🔄 mig`, `📋 cpl`, `🧪 test`, `📊 obs`, `⚡ perf`,
   `🧭 dec`, `🏋️ prac`, `🔨 proj`, `🎓 teach`, `🔁 ret`,
   `🚨 triage` as appropriate.

---

## Phase 3 - Group Into Sub-topic Files

**File rule (non-negotiable):** every sub-topic file MUST contain at
least 5 keywords. Never create per-keyword files.

Group the generated keywords into sub-topic files by:

- Existing `topic-registry.md` mapping (if present), OR
- Natural clusters from Section 3.3 of BYTES_KEYWORD_GENERATOR.md.

Each file is named `{Topic} - {Subtopic}.md` with SPACE-HYPHEN-SPACE
separators. Example: `Java - Collections.md`. Never em dash.

Each file's YAML frontmatter (per interview-style spec):

```yaml
---
title: "Topic - Subtopic"
topic: Topic
subtopic: Subtopic
keywords:
  - Keyword One
  - Keyword Two
  - Keyword Three
  - Keyword Four
  - Keyword Five
difficulty_range: easy | medium | hard | mixed
status: draft
version: 0
---
```

Keywords are listed foundational first, advanced last.

---

## Phase 4 - Update `index.md` (Non-Destructive)

Follow Section 3.10 safety rules from BYTES_KEYWORD_GENERATOR.md.
Adapted for bytes:

1. NEVER delete an existing sub-topic file row.
2. NEVER modify an existing row's content.
3. NEVER reorder existing rows.
4. NEVER change the YAML frontmatter (except `keywords_count` and
   `files_count` totals).
5. NEVER change the `title:` (would break child `topic:` references).
6. ALWAYS preserve exact whitespace and formatting.
7. ALWAYS update `keywords_count` and `files_count` to new totals.
8. ALWAYS append new rows AFTER all existing rows.
9. If in doubt about any existing content: DO NOT MODIFY IT.

---

## Phase 5 - Create Stub Files

For every NEW sub-topic file, create a stub at
`bytes/{TOPIC_FOLDER}/{Topic} - {Subtopic}.md` with:

- Full frontmatter (status: draft, version: 0).
- A note line directing the next step to `@bytes-fill-content`.

Do NOT generate the 14-section byte content here. That is the
content-fill step's job.

---

## Phase 6 - Validate

After all writes, run:

```pwsh
pwsh -File bytes/_config/generate-keywords.ps1 -Topic {TopicName} -DryRun
```

Confirm:

- [ ] Every sub-topic file has >= 5 keywords.
- [ ] No file name uses em dash.
- [ ] No keyword duplicated across files.
- [ ] `index.md` `keywords_count` matches sum of file keyword counts.
- [ ] `index.md` `files_count` matches actual file count.
- [ ] All 22 rules from BYTES_KEYWORD_GENERATOR.md Section 2 hold.
- [ ] All 17 quality checks from Section 4 pass.

Stop on any violation. Report and do NOT auto-fix.

---

## Output

End with a short status block:

```
TOPIC:          {TopicName}
FILES CREATED:  N
FILES UPDATED:  M
KEYWORDS ADDED: K
RULE VIOLATIONS: 0
NEXT STEP:      @bytes-fill-content {TopicName}
```
