#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bytes_scaffold.py
=================
OPTIONAL preview tool. Pre-generates scaffold byte content files
with [FILL:...] stubs.

Content scaffolding is no longer required for content generation:
the /bytes agent reads `keywords:` from each file's YAML frontmatter
and generates content directly. This script exists only to preview
the 14-section structure or to seed files for manual editing.

Each scaffold has:
  - Correct file-level YAML frontmatter
  - All 14 required sections per keyword with [FILL:...] stubs
  - Proper double-rule separators between keywords
  - Keyword TOC at top of file

Usage (optional):
  python bytes/_config/bytes_scaffold.py <topic-folder>
  python bytes/_config/bytes_scaffold.py java
  python bytes/_config/bytes_scaffold.py --file "java/Java - Collections.md"
"""

import os
import re
import sys
from pathlib import Path

BASE = Path(r"C:\ASK\Workspace\northstar\sk-bytes")
BYTES_BASE = BASE / "bytes"


def read_frontmatter(path: Path) -> dict:
    """Extract YAML frontmatter fields from an existing file."""
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm_text = text[3:end]
    fields = {}
    keywords = []
    in_keywords = False
    for line in fm_text.splitlines():
        if re.match(r"^keywords:", line):
            in_keywords = True
            continue
        if in_keywords:
            m = re.match(r"^\s+-\s+(.+)", line)
            if m:
                keywords.append(m.group(1).strip())
                continue
            else:
                in_keywords = False
        m = re.match(r"^(\w[\w_]*):\s*(.*)$", line)
        if m and not in_keywords:
            fields[m.group(1)] = m.group(2).strip().strip('"\'')
    if keywords:
        fields["_keywords"] = keywords
    return fields


def keyword_to_anchor(kw: str) -> str:
    """Convert keyword to markdown anchor."""
    anchor = kw.lower()
    anchor = re.sub(r"[()&/,]", "", anchor)
    anchor = re.sub(r"[^a-z0-9\s-]", "", anchor)
    anchor = re.sub(r"\s+", "-", anchor.strip())
    return re.sub(r"-+", "-", anchor).strip("-")


def build_keyword_scaffold(keyword: str, difficulty: str = "mixed") -> str:
    """Build 14-section scaffold for a single keyword."""
    return f"""# {keyword}

**TL;DR** - [FILL: one sentence, max 25 words. What + why, zero jargon.]

---

### 🔥 The Problem in One Paragraph

[FILL: 80-160 words. One tight paragraph. Concrete scenario showing
the pain. End with: "This is exactly why {keyword} was created."]

---

### 📘 Textbook Definition

[FILL: 2-4 sentences. Formal, precise, technically complete.
Bold **{keyword}** on first mention. No analogies.]

---

### 🔩 First Principles

**CORE INVARIANTS:**
1. [FILL: always true about this concept]
2. [FILL: always true about this concept]
3. [FILL: always true about this concept - hard only]

**DERIVED DESIGN:**
[FILL: how invariants force the design. 2-4 sentences.]

**THE TRADE-OFF:**
**Gain:** [FILL: what you get]
**Cost:** [FILL: what you sacrifice]

---

### 📶 Gradual Depth

**Level 1 - What it is:**
[FILL: plain English, no jargon. 2-3 sentences.]

**Level 2 - How to use it:**
[FILL: basic usage, common patterns. 3-4 sentences.]

**Level 3 - How it works:**
[FILL: internals, data structures, algorithms. 4-5 sentences.]

**Level 4 - Production mastery:**
[FILL: design decisions, edge cases, cross-system reasoning.
5-6 sentences. Hard difficulty only.]

---

### ⚙️ How It Works

[FILL: step-by-step technical walkthrough. Include ASCII diagram
below (max 59 chars wide), then equivalent Mermaid block.]

```
[FILL: ASCII diagram, <=59 chars wide]
```

```mermaid
flowchart TD
    A[FILL: Step 1] --> B[FILL: Step 2]
    B --> C[FILL: Step 3]
```

---

### 🧠 Mental Model

> [FILL: 2-3 sentence real-world analogy in blockquote.
> Concrete everyday object/process.]

- "[FILL: analogy element]" -> [FILL: technical element]
- "[FILL: analogy element]" -> [FILL: technical element]
- "[FILL: analogy element]" -> [FILL: technical element]

**Where this analogy breaks down:** [FILL: 1 sentence]

**BAD use of this model:** [FILL: how a junior misapplies it.]
**GOOD use of this model:** [FILL: how a senior wields it.]

---

### 🚨 Production Reality

**The failure:** [FILL: name + 1-sentence description]
**Symptom:** [FILL: what you actually observe in production]
**Root cause:** [FILL: why it happens - first-principles depth]
**Diagnostic:**
```
[FILL: real command / metric / log query that reveals it]
```
**Fix:** [FILL: BAD approach -> GOOD approach]
**Prevention:** [FILL: how to avoid it next time]

---

### ⚡ Decision Snap

**USE WHEN:**
- [FILL: condition 1]
- [FILL: condition 2]
- [FILL: condition 3]

**AVOID WHEN:**
- [FILL: condition 1]
- [FILL: condition 2]

**PREFER [FILL: alternative] WHEN:**
- [FILL: condition 1]
- [FILL: condition 2]

---

### ⚠️ Top Traps

| # | Misconception | Reality |
|---|---------------|---------|
| 1 | [FILL: wrong belief] | [FILL: actual truth] |
| 2 | [FILL: wrong belief] | [FILL: actual truth] |
| 3 | [FILL: wrong belief] | [FILL: actual truth] |

---

### 🪜 Learning Ladder

**Prerequisites (understand these first):**
- [FILL: Keyword title verbatim] - [FILL: why needed in 1 line]
- [FILL: Keyword title verbatim] - [FILL: why needed in 1 line]

**THIS:** {keyword}

**Next steps (learn these after):**
- [FILL: Keyword title verbatim] - [FILL: what it adds in 1 line]
- [FILL: Keyword title verbatim] - [FILL: what it adds in 1 line]

---

### 💡 The Surprising Truth

[FILL: exactly ONE counterintuitive fact. 2-4 sentences.
Specific, accurate, memorable.]

---

### 📇 Revision Card

1. [FILL: most important insight - one line]
2. [FILL: key trade-off or constraint - one line]
3. [FILL: production gotcha that bites everyone - one line]
"""


def build_file_scaffold(file_path: Path, fm: dict) -> str:
    """Build complete scaffold for a bytes sub-topic file."""
    title = fm.get("title", file_path.stem)
    topic = fm.get("topic", "Unknown")
    subtopic = fm.get("subtopic", "Unknown")
    keywords = fm.get("_keywords", [])
    difficulty = fm.get("difficulty_range", "mixed")
    parent = fm.get("parent", topic)
    grand_parent = fm.get("grand_parent", "Bytes")
    nav_order = fm.get("nav_order", "1")
    permalink = fm.get("permalink", "")
    version = 1

    kw_yaml = "\n".join(f"  - {kw}" for kw in keywords)

    toc = "\n".join(
        f"- [{kw}](#{keyword_to_anchor(kw)})" for kw in keywords
    )

    kw_sections = []
    for i, kw in enumerate(keywords):
        kw_sections.append(build_keyword_scaffold(kw, difficulty))
        if i < len(keywords) - 1:
            # Double-rule separator: blank/---/blank/---/blank
            kw_sections.append("\n---\n\n---\n")

    all_keywords = "\n".join(kw_sections)

    permalink_line = (
        f"permalink: {permalink}\n" if permalink else ""
    )

    return f"""---
title: "{title}"
topic: {topic}
subtopic: {subtopic}
keywords:
{kw_yaml}
difficulty_range: {difficulty}
status: in-progress
version: {version}
layout: default
parent: "{parent}"
grand_parent: "{grand_parent}"
nav_order: {nav_order}
{permalink_line}---

**Keywords covered in this file:**

{toc}

{all_keywords}
"""


def process_file(file_path: Path) -> None:
    """Process a single byte file - read frontmatter, generate scaffold."""
    fm = read_frontmatter(file_path)
    keywords = fm.get("_keywords", [])

    if not keywords:
        print(f"  SKIP: {file_path.name} - no keywords in frontmatter")
        return

    if len(keywords) < 5:
        print(f"  WARN: {file_path.name} - only {len(keywords)} keywords "
              f"(bytes requires >=5)")

    content = build_file_scaffold(file_path, fm)

    # Write UTF-8 no BOM
    file_path.write_text(content, encoding="utf-8", newline="\n")

    fill_count = content.count("[FILL:")
    print(f"  OK: {file_path.name} - {len(keywords)} keywords, "
          f"{fill_count} [FILL:] stubs, {len(content)} bytes")


def process_topic(topic_folder: str) -> None:
    """Process all files in a topic folder."""
    topic_dir = BYTES_BASE / topic_folder
    if not topic_dir.is_dir():
        print(f"ERROR: folder not found: {topic_dir}")
        sys.exit(1)

    md_files = sorted([
        f for f in topic_dir.glob("*.md")
        if f.name != "index.md"
    ])

    if not md_files:
        print(f"ERROR: no .md files found in {topic_dir}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"BYTES SCAFFOLD: {topic_folder}")
    print(f"Files: {len(md_files)}")
    print(f"{'='*60}\n")

    total_keywords = 0

    for f in md_files:
        fm = read_frontmatter(f)
        kw_count = len(fm.get("_keywords", []))
        process_file(f)
        total_keywords += kw_count

    print(f"\n{'='*60}")
    print(f"DONE: {len(md_files)} files, {total_keywords} keywords scaffolded")
    print(f"{'='*60}\n")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python bytes_scaffold.py <topic-folder>")
        print("  python bytes_scaffold.py java")
        print("  python bytes_scaffold.py --file \"java/Java - Collections.md\"")
        sys.exit(1)

    if sys.argv[1] == "--file":
        if len(sys.argv) < 3:
            print("ERROR: --file requires a path argument")
            sys.exit(1)
        file_path = BYTES_BASE / sys.argv[2]
        if not file_path.exists():
            print(f"ERROR: file not found: {file_path}")
            sys.exit(1)
        process_file(file_path)
    else:
        process_topic(sys.argv[1])


if __name__ == "__main__":
    main()
