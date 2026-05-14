#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate-byte.py
================
Validator for Bytes sub-topic files (v1.0 spec).

Checks:
  - File starts at byte 0 with `---` (no BOM).
  - YAML frontmatter has all required fields.
  - `keywords[]` has at least 5 entries.
  - `keywords[]` matches order of `# Keyword Name` headings.
  - Each keyword block has all 14 sections in order.
  - Word count per keyword is within difficulty target.
  - Section 8 (Mental Model) has all four required parts.
  - Section 12 (Learning Ladder) Prereq/Next titles resolve
    to real keywords in the bytes corpus.
  - No em dashes anywhere.
  - No line exceeds 70 chars inside fenced code blocks.
  - No ASCII diagram exceeds 59 chars wide.
  - Every diagram block has both ASCII and Mermaid versions.

Usage:
  python bytes/_config/validate-byte.py path/to/file.md
  python bytes/_config/validate-byte.py bytes/java/
  python bytes/_config/validate-byte.py --all

Exit code: 0 = pass, 1 = errors found.
"""

import os
import re
import sys
from pathlib import Path

BASE = Path(r"C:\ASK\Workspace\northstar\sk-bytes")
BYTES_BASE = BASE / "bytes"

REQUIRED_FM_FIELDS = [
    "title", "topic", "subtopic", "difficulty_range",
    "status", "version",
]

# Section header literals in exact order
SECTION_HEADERS = [
    ("3.3", "### 🔥 The Problem in One Paragraph"),
    ("3.4", "### 📘 Textbook Definition"),
    ("3.5", "### 🔩 First Principles"),
    ("3.6", "### 📶 Gradual Depth"),
    ("3.7", "### ⚙️ How It Works"),
    ("3.8", "### 🧠 Mental Model"),
    ("3.9", "### 🚨 Production Reality"),
    ("3.10", "### ⚡ Decision Snap"),
    ("3.11", "### ⚠️ Top Traps"),
    ("3.12", "### 🪜 Learning Ladder"),
    ("3.13", "### 💡 The Surprising Truth"),
    ("3.14", "### 📇 Revision Card"),
]

WORD_TARGETS = {
    "easy":   (600, 900),
    "medium": (900, 1200),
    "hard":   (1200, 1500),
    "mixed":  (600, 1500),
}

DIFFICULTY_LEVELS = {
    "easy": 2, "medium": 3, "hard": 4, "mixed": 2,
}


class ValidationError(Exception):
    pass


def read_file_text(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValidationError(
            f"{path.name}: file has UTF-8 BOM (must be UTF-8 no BOM)"
        )
    if not raw.startswith(b"---"):
        raise ValidationError(
            f"{path.name}: file must start at byte 0 with '---'"
        )
    return raw.decode("utf-8", errors="replace")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (fields dict, body)."""
    end = text.find("\n---", 3)
    if end == -1:
        raise ValidationError("frontmatter not closed with '---'")
    fm_text = text[3:end]
    body = text[end + 4:].lstrip("\n")
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
    fields["_keywords"] = keywords
    return fields, body


def split_keyword_blocks(body: str) -> list[tuple[str, str]]:
    """
    Split body on the double-rule separator into keyword blocks.
    Return list of (keyword_title, block_text) tuples.
    The double rule pattern is:  \\n---\\n\\n---\\n
    """
    # Normalize line endings
    body = body.replace("\r\n", "\n")
    parts = re.split(r"\n---\n\s*\n---\n", body)
    blocks = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        m = re.search(r"^# (.+)$", part, re.MULTILINE)
        if not m:
            # Block with no H1 (e.g. pure TOC block) - skip
            continue
        title = m.group(1).strip()
        blocks.append((title, part))
    return blocks


def validate_frontmatter(fields: dict, errors: list) -> None:
    for f in REQUIRED_FM_FIELDS:
        if f not in fields:
            errors.append(f"missing frontmatter field: {f}")
    kws = fields.get("_keywords", [])
    if len(kws) < 5:
        errors.append(
            f"keywords[] has {len(kws)} entries (need >=5)"
        )
    diff = fields.get("difficulty_range", "")
    if diff not in WORD_TARGETS:
        errors.append(
            f"difficulty_range '{diff}' not in "
            f"{list(WORD_TARGETS.keys())}"
        )
    status = fields.get("status", "")
    if status not in ("draft", "in-progress", "complete"):
        errors.append(
            f"status '{status}' not in draft|in-progress|complete"
        )
    version = fields.get("version", "")
    if version not in ("0", "1"):
        errors.append(f"version '{version}' must be 0 or 1")


def validate_keyword_order(
    fields: dict, blocks: list[tuple[str, str]], errors: list
) -> None:
    declared = fields.get("_keywords", [])
    found = [b[0] for b in blocks]
    if declared != found:
        errors.append(
            "keywords[] order does not match '# Keyword Name' headings\n"
            f"    declared: {declared}\n"
            f"    found:    {found}"
        )


def validate_sections(
    title: str, block: str, errors: list
) -> None:
    # Section 3.1 = the `# Keyword Name` itself (already matched).
    # Section 3.2 = TL;DR line
    if not re.search(r"^\*\*TL;DR\*\* - ", block, re.MULTILINE):
        errors.append(f"[{title}] missing TL;DR line")
    else:
        m = re.search(r"^\*\*TL;DR\*\* - (.+)$", block, re.MULTILINE)
        if m:
            tldr = m.group(1).strip()
            wc = len(tldr.split())
            if wc > 25:
                errors.append(
                    f"[{title}] TL;DR has {wc} words (max 25)"
                )

    # Sections 3.3 .. 3.14 (12 ### headers) in order
    last_pos = 0
    for code, header in SECTION_HEADERS:
        pos = block.find(header, last_pos)
        if pos == -1:
            errors.append(f"[{title}] missing section {code}: {header}")
        else:
            last_pos = pos


def validate_mental_model(title: str, block: str, errors: list) -> None:
    mm_start = block.find("### 🧠 Mental Model")
    if mm_start == -1:
        return
    next_section = block.find("\n### ", mm_start + 5)
    mm = block[mm_start:next_section if next_section != -1 else len(block)]

    if not re.search(r"^> ", mm, re.MULTILINE):
        errors.append(
            f"[{title}] Mental Model missing blockquote analogy"
        )
    if mm.count(" -> ") < 3:
        errors.append(
            f"[{title}] Mental Model needs >=3 '-> ' mapping bullets"
        )
    if "**Where this analogy breaks down:**" not in mm:
        errors.append(
            f"[{title}] Mental Model missing 'Where this analogy "
            f"breaks down:' label"
        )
    if "**BAD use of this model:**" not in mm:
        errors.append(
            f"[{title}] Mental Model missing 'BAD use of this model:'"
        )
    if "**GOOD use of this model:**" not in mm:
        errors.append(
            f"[{title}] Mental Model missing 'GOOD use of this model:'"
        )


def validate_word_count(
    title: str, block: str, difficulty: str, errors: list
) -> None:
    # Strip code fences and tables for a fair word count
    text = re.sub(r"```.*?```", "", block, flags=re.DOTALL)
    text = re.sub(r"\|.*?\|", "", text)
    text = re.sub(r"[#*`>\-\|]", " ", text)
    words = text.split()
    wc = len(words)
    lo, hi = WORD_TARGETS.get(difficulty, (600, 1500))
    # Allow 10% slop
    if wc < int(lo * 0.9):
        errors.append(
            f"[{title}] word count {wc} < target {lo}-{hi} ({difficulty})"
        )
    elif wc > int(hi * 1.1):
        errors.append(
            f"[{title}] word count {wc} > target {lo}-{hi} ({difficulty})"
        )


def validate_em_dashes(text: str, errors: list) -> None:
    for i, line in enumerate(text.splitlines(), 1):
        if "\u2014" in line or "\u2013" in line:
            errors.append(f"em/en dash on line {i}: {line.strip()[:60]}")


def validate_code_lines(text: str, errors: list) -> None:
    in_code = False
    is_ascii = False
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.rstrip()
        if stripped.startswith("```"):
            if not in_code:
                in_code = True
                fence = stripped[3:].strip().lower()
                is_ascii = fence == "" or fence == "text"
            else:
                in_code = False
                is_ascii = False
            continue
        if in_code:
            limit = 59 if is_ascii else 70
            if len(line) > limit:
                kind = "ASCII diagram" if is_ascii else "code"
                errors.append(
                    f"line {i}: {kind} exceeds {limit} chars "
                    f"({len(line)} chars)"
                )


def validate_diagrams(title: str, block: str, errors: list) -> None:
    hiw_start = block.find("### ⚙️ How It Works")
    if hiw_start == -1:
        return
    next_section = block.find("\n### ", hiw_start + 5)
    hiw = block[hiw_start:next_section if next_section != -1 else len(block)]

    # Count fenced blocks: ASCII (no lang or 'text') and Mermaid
    fences = re.findall(r"```([a-zA-Z0-9_+-]*)", hiw)
    # Each fenced block opens once and closes once. We see opens only.
    opens = [f for idx, f in enumerate(fences) if idx % 2 == 0]
    has_ascii = any(f == "" or f.lower() == "text" for f in opens)
    has_mermaid = any(f.lower() == "mermaid" for f in opens)
    if not has_ascii:
        errors.append(
            f"[{title}] How It Works missing ASCII diagram block"
        )
    if not has_mermaid:
        errors.append(
            f"[{title}] How It Works missing Mermaid block"
        )


def collect_all_keywords() -> set:
    """Walk all .md files under bytes/ and collect every '# Keyword' title."""
    titles = set()
    for md in BYTES_BASE.rglob("*.md"):
        if md.name == "index.md":
            continue
        if "_config" in md.parts:
            continue
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for m in re.finditer(r"^# (.+)$", text, re.MULTILINE):
            titles.add(m.group(1).strip())
    return titles


def validate_learning_ladder(
    title: str, block: str, corpus: set, errors: list
) -> None:
    ll_start = block.find("### 🪜 Learning Ladder")
    if ll_start == -1:
        return
    next_section = block.find("\n### ", ll_start + 5)
    ll = block[ll_start:next_section if next_section != -1 else len(block)]

    # Lines under Prerequisites / Next steps look like:
    #   - Keyword Title - reason
    refs = re.findall(r"^- ([^\-\n]+?)\s+-\s+", ll, re.MULTILINE)
    for ref in refs:
        ref = ref.strip()
        if ref.startswith("[FILL"):
            continue  # stub
        if ref not in corpus:
            errors.append(
                f"[{title}] Learning Ladder references unknown "
                f"keyword: '{ref}'"
            )


def validate_file(path: Path, corpus: set) -> list:
    errors = []
    try:
        text = read_file_text(path)
    except ValidationError as e:
        return [str(e)]

    validate_em_dashes(text, errors)
    validate_code_lines(text, errors)

    try:
        fields, body = parse_frontmatter(text)
    except ValidationError as e:
        errors.append(str(e))
        return errors

    validate_frontmatter(fields, errors)
    blocks = split_keyword_blocks(body)

    difficulty = fields.get("difficulty_range", "mixed")
    status = fields.get("status", "draft")

    # Draft stubs may have frontmatter only (no keyword bodies yet).
    # Skip body-level checks until status is in-progress or complete.
    if status == "draft" and not blocks:
        return errors

    validate_keyword_order(fields, blocks, errors)

    for kw_title, block in blocks:
        validate_sections(kw_title, block, errors)
        validate_mental_model(kw_title, block, errors)
        validate_diagrams(kw_title, block, errors)
        # Skip word-count + ladder checks for stub / in-progress files
        if status == "complete":
            validate_word_count(kw_title, block, difficulty, errors)
            validate_learning_ladder(kw_title, block, corpus, errors)

    return errors


def validate_path(target: Path) -> int:
    corpus = collect_all_keywords()

    if target.is_file():
        files = [target]
    elif target.is_dir():
        files = sorted([
            f for f in target.rglob("*.md")
            if f.name != "index.md" and "_config" not in f.parts
        ])
    else:
        print(f"ERROR: path not found: {target}")
        return 1

    total_errors = 0
    print(f"\nValidating {len(files)} file(s)...\n")

    for f in files:
        errs = validate_file(f, corpus)
        rel = f.relative_to(BASE) if BASE in f.parents else f
        if errs:
            print(f"FAIL  {rel}")
            for e in errs:
                print(f"   - {e}")
            total_errors += len(errs)
        else:
            print(f"PASS  {rel}")

    print(f"\n{'='*60}")
    if total_errors == 0:
        print(f"ALL PASS - {len(files)} file(s) validated")
        return 0
    else:
        print(f"FAILED - {total_errors} error(s) across {len(files)} file(s)")
        return 1


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python validate-byte.py <file.md | folder | --all>")
        sys.exit(1)

    arg = sys.argv[1]
    if arg == "--all":
        target = BYTES_BASE
    else:
        p = Path(arg)
        target = p if p.is_absolute() else (BASE / arg)

    sys.exit(validate_path(target))


if __name__ == "__main__":
    main()
