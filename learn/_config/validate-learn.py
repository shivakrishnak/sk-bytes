#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate-learn.py
=================
Validator for sk-learn sub-topic files (v1.0 spec, tri-template).

Checks (per keyword block, after auto-detecting its tier):
  - File starts at byte 0 with `---` (no BOM).
  - YAML frontmatter has all required fields.
  - `keywords[]` has at least 5 entries.
  - `keywords[]` matches order of `# Keyword Name` headings.
  - `## Keywords` TOC with anchor links before first keyword.
  - Each keyword block has its tier's section list in order:
        SIMPLE       -> 9  sections   (L0, L1)
        INTERMEDIATE -> 13 sections   (L2, L3)
        COMPLEX      -> 16 sections   (L4, L5, L6, META)
  - Word count per keyword is within its tier target:
        SIMPLE       400 - 700
        INTERMEDIATE 900 - 1,300
        COMPLEX      1,400 - 2,000
  - INTERMEDIATE Mental Model has all four required parts.
  - INTERMEDIATE + COMPLEX Learning Ladder Prereq/Next titles
    resolve to real keywords in the corpus.
  - INTERMEDIATE + COMPLEX have a Wrong-vs-Right pair (BAD/GOOD).
  - COMPLEX First Principles has >= 3 invariants.
  - COMPLEX has >= 2 named Failure Modes with Diagnostic + Fix.
  - No em dashes anywhere.
  - No line exceeds 70 chars inside fenced code blocks.
  - No ASCII diagram exceeds 59 chars wide.
  - Every mandatory diagram has both ASCII and Mermaid blocks.

Usage:
  python learn/_config/validate-learn.py path/to/file.md
  python learn/_config/validate-learn.py learn/java/
  python learn/_config/validate-learn.py --all

Exit code: 0 = pass, 1 = errors found.
"""

import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
LEARN_BASE = BASE / "learn"

REQUIRED_FM_FIELDS = [
    "title", "topic", "subtopic", "difficulty_range",
    "status", "version",
]

# Jekyll / just-the-docs frontmatter fields required for
# GitHub Pages navigation to work correctly.
JEKYLL_REQUIRED_CONTENT = [
    "layout", "parent", "grand_parent", "nav_order", "permalink",
]
JEKYLL_REQUIRED_INDEX = [
    "layout", "parent", "has_children", "nav_order", "permalink",
]

# ------------------------------------------------------------------
# Tier section schemas (exact ordered list of `### ` headers).
# ------------------------------------------------------------------

SIMPLE_HEADERS = [
    ("S3",  "### 🟢 What it is"),
    ("S4",  "### 🎯 Why it exists"),
    ("S5",  "### 🧠 Mental Model"),
    ("S6",  "### ⚙️ How it works"),
    ("S7",  "### ✏️ Minimal Example"),
    ("S8",  "### ⚡ When to use / Not to use"),
    ("S9",  "### ⚠️ One Gotcha"),
    ("S10", "### 📇 Revision Card"),
]

INTERMEDIATE_HEADERS = [
    ("S3",  "### 🔥 The Problem in One Paragraph"),
    ("S4",  "### 📘 Textbook Definition"),
    ("S5",  "### 🧠 Mental Model"),
    ("S6",  "### ⚙️ How It Works"),
    ("S7",  "### 🛠️ Worked Example"),
    ("S8",  "### ⚖️ Trade-offs"),
    ("S9",  "### ⚡ Decision Snap"),
    ("S10", "### ⚠️ Top Traps"),
    ("S11", "### 🪜 Learning Ladder"),
    ("S12", "### 💡 The Surprising Truth"),
    ("S13", "### 📇 Revision Card"),
]

COMPLEX_HEADERS = [
    ("S3",  "### 🔥 Problem Statement"),
    ("S4",  "### 📜 Historical Context"),
    ("S5",  "### 🔩 First Principles"),
    ("S6",  "### 🧠 Mental Model"),
    ("S7",  "### 🧩 Components"),
    ("S8",  "### 📶 Gradual Depth"),
    ("S9",  "### ⚙️ How It Works"),
    ("S10", "### 🚨 Failure Modes"),
    ("S11", "### 🔬 Production Reality"),
    ("S12", "### ⚖️ Trade-offs & Alternatives"),
    ("S13", "### ⚡ Decision Snap"),
    ("S14", "### ⚠️ Top Traps"),
    ("S15", "### 🪜 Learning Ladder"),
]
# Section 16 is a closing triplet detected separately:
#   "**The Surprising Truth:**" + "**Further Reading:**" +
#   "**Revision Card:**"

WORD_TARGETS = {
    "SIMPLE":       (400, 700),
    "INTERMEDIATE": (900, 1300),
    "COMPLEX":      (1400, 2000),
}

# Distinctive markers used to auto-detect a keyword's tier.
TIER_MARKERS = {
    "COMPLEX":      ["### 🔩 First Principles",
                     "### 🚨 Failure Modes",
                     "### 🧩 Components"],
    "INTERMEDIATE": ["### 🔥 The Problem in One Paragraph",
                     "### 📘 Textbook Definition",
                     "### 🛠️ Worked Example"],
    "SIMPLE":       ["### 🟢 What it is",
                     "### 🎯 Why it exists",
                     "### ✏️ Minimal Example"],
}


class ValidationError(Exception):
    pass


# ------------------------------------------------------------------
# Anchor generation (kramdown GFM-style)
# ------------------------------------------------------------------

def heading_to_anchor(heading: str) -> str:
    """Generate the kramdown GFM auto-ID for a heading."""
    s = re.sub(r'^[^a-zA-Z]+', '', heading)
    s = re.sub(r'[^a-zA-Z0-9 -]', '', s)
    s = s.replace(' ', '-')
    return s.lower()


# ------------------------------------------------------------------
# File and frontmatter parsing
# ------------------------------------------------------------------

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
    end = text.find("\n---", 3)
    if end == -1:
        raise ValidationError("frontmatter not closed with '---'")
    fm_text = text[3:end]
    body = text[end + 4:].lstrip("\n")
    fields: dict = {}
    keywords: list = []
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
            in_keywords = False
        m = re.match(r"^(\w[\w_]*):\s*(.*)$", line)
        if m and not in_keywords:
            fields[m.group(1)] = m.group(2).strip().strip('"\'')
    fields["_keywords"] = keywords
    return fields, body


def split_keyword_blocks(body: str) -> list[tuple[str, str]]:
    """Split body on double-rule separator."""
    body = body.replace("\r\n", "\n")
    parts = re.split(r"\n---\n\s*\n---\n", body)
    blocks = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        m = re.search(r"^# (.+)$", part, re.MULTILINE)
        if not m:
            continue
        title = m.group(1).strip()
        blocks.append((title, part))
    return blocks


# ------------------------------------------------------------------
# Tier detection
# ------------------------------------------------------------------

def detect_tier(block: str) -> str:
    """Score each tier by how many of its distinctive headers
    appear. Return the highest-scoring tier."""
    scores = {}
    for tier, markers in TIER_MARKERS.items():
        scores[tier] = sum(1 for m in markers if m in block)
    # Prefer COMPLEX > INTERMEDIATE > SIMPLE on ties.
    for tier in ("COMPLEX", "INTERMEDIATE", "SIMPLE"):
        if scores[tier] == max(scores.values()) and scores[tier] > 0:
            return tier
    # If no markers match at all, fall back to SIMPLE so the
    # 'missing section' errors point the writer somewhere useful.
    return "SIMPLE"


def tier_headers(tier: str):
    return {
        "SIMPLE":       SIMPLE_HEADERS,
        "INTERMEDIATE": INTERMEDIATE_HEADERS,
        "COMPLEX":      COMPLEX_HEADERS,
    }[tier]


# ------------------------------------------------------------------
# Frontmatter validation
# ------------------------------------------------------------------

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
    if diff not in ("easy", "medium", "hard", "mixed"):
        errors.append(
            f"difficulty_range '{diff}' not in "
            f"easy|medium|hard|mixed"
        )
    status = fields.get("status", "")
    if status not in ("draft", "in-progress", "complete"):
        errors.append(
            f"status '{status}' not in draft|in-progress|complete"
        )
    version = fields.get("version", "")
    if version not in ("0", "1"):
        errors.append(f"version '{version}' must be 0 or 1")


def validate_jekyll_frontmatter(
    fields: dict, path: Path, errors: list
) -> None:
    """Validate just-the-docs frontmatter fields needed for
    GitHub Pages navigation (3-level hierarchy).

    Hierarchy:
      learn/index.md          -> title: Learn, has_children: true
      learn/<topic>/index.md  -> parent: Learn, has_children: true
      learn/<topic>/<file>.md -> parent: <topic>, grand_parent: Learn
    """
    for f in JEKYLL_REQUIRED_CONTENT:
        if f not in fields:
            errors.append(
                f"missing Jekyll frontmatter field: {f} "
                f"(required for GitHub Pages)"
            )
    gp = fields.get("grand_parent", "")
    if gp and gp != "Learn":
        errors.append(
            f"grand_parent is '{gp}' but must be 'Learn'"
        )
    if not gp:
        errors.append(
            "grand_parent must be 'Learn' for just-the-docs "
            "3-level navigation"
        )
    layout = fields.get("layout", "")
    if layout and layout != "default":
        errors.append(
            f"layout is '{layout}' but must be 'default'"
        )
    parent = fields.get("parent", "")
    topic = fields.get("topic", "")
    if parent and topic and parent != topic:
        errors.append(
            f"parent '{parent}' does not match topic '{topic}'"
        )
    permalink = fields.get("permalink", "")
    if permalink and not permalink.startswith("/learn/"):
        errors.append(
            f"permalink '{permalink}' must start with '/learn/'"
        )
    nav_order = fields.get("nav_order", "")
    if nav_order:
        try:
            int(nav_order)
        except ValueError:
            errors.append(
                f"nav_order '{nav_order}' must be an integer"
            )


def validate_keyword_order(
    fields: dict, blocks: list, errors: list
) -> None:
    declared = fields.get("_keywords", [])
    found = [b[0] for b in blocks]
    if declared != found:
        errors.append(
            "keywords[] order does not match '# Keyword Name'\n"
            f"    declared: {declared}\n"
            f"    found:    {found}"
        )


# ------------------------------------------------------------------
# Per-keyword content checks
# ------------------------------------------------------------------

def validate_tldr(title: str, tier: str, block: str, errors: list):
    m = re.search(r"^\*\*TL;DR\*\* - (.+)$", block, re.MULTILINE)
    if not m:
        errors.append(f"[{title}] missing TL;DR line")
        return
    wc = len(m.group(1).strip().split())
    cap = {"SIMPLE": 20, "INTERMEDIATE": 25, "COMPLEX": 30}[tier]
    if wc > cap:
        errors.append(
            f"[{title}] TL;DR has {wc} words "
            f"(max {cap} for {tier})"
        )


def validate_sections(
    title: str, tier: str, block: str, errors: list
) -> None:
    last_pos = 0
    for code, header in tier_headers(tier):
        pos = block.find(header, last_pos)
        if pos == -1:
            errors.append(
                f"[{title}] [{tier}] missing section {code}: "
                f"{header}"
            )
        else:
            last_pos = pos
    if tier == "COMPLEX":
        # S16 - closing triplet labels (order-independent)
        for label in ("**The Surprising Truth:**",
                      "**Further Reading:**",
                      "**Revision Card:**"):
            if label not in block:
                errors.append(
                    f"[{title}] [COMPLEX] missing S16 label: {label}"
                )


def validate_mental_model_intermediate(
    title: str, block: str, errors: list
) -> None:
    mm_start = block.find("### 🧠 Mental Model")
    if mm_start == -1:
        return
    nxt = block.find("\n### ", mm_start + 5)
    mm = block[mm_start:nxt if nxt != -1 else len(block)]
    if not re.search(r"^> ", mm, re.MULTILINE):
        errors.append(
            f"[{title}] Mental Model missing blockquote analogy"
        )
    if mm.count(" -> ") < 3:
        errors.append(
            f"[{title}] Mental Model needs >=3 '-> ' bullets"
        )
    if "**Where this analogy breaks down:**" not in mm:
        errors.append(
            f"[{title}] Mental Model missing "
            f"'Where this analogy breaks down:' label"
        )


def validate_word_count(
    title: str, tier: str, block: str, errors: list
) -> None:
    text = re.sub(r"```.*?```", "", block, flags=re.DOTALL)
    text = re.sub(r"\|.*?\|", "", text)
    text = re.sub(r"[#*`>\-\|]", " ", text)
    wc = len(text.split())
    lo, hi = WORD_TARGETS[tier]
    if wc < int(lo * 0.9):
        errors.append(
            f"[{title}] [{tier}] word count {wc} < "
            f"target {lo}-{hi}"
        )
    elif wc > int(hi * 1.1):
        errors.append(
            f"[{title}] [{tier}] word count {wc} > "
            f"target {lo}-{hi}"
        )


def validate_em_dashes(text: str, errors: list) -> None:
    for i, line in enumerate(text.splitlines(), 1):
        if "\u2014" in line or "\u2013" in line:
            errors.append(
                f"em/en dash on line {i}: {line.strip()[:60]}"
            )


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


def validate_diagrams(
    title: str, tier: str, block: str, errors: list
) -> None:
    """Check ASCII+Mermaid pair in mandatory sections per tier:
       SIMPLE       - optional (no check).
       INTERMEDIATE - S6 How It Works.
       COMPLEX      - S9 How It Works and S7 Components.
    """
    if tier == "SIMPLE":
        return
    targets = ["### ⚙️ How It Works"]
    if tier == "COMPLEX":
        targets.append("### 🧩 Components")
    for header in targets:
        start = block.find(header)
        if start == -1:
            continue
        nxt = block.find("\n### ", start + 5)
        seg = block[start:nxt if nxt != -1 else len(block)]
        fences = re.findall(r"```([a-zA-Z0-9_+-]*)", seg)
        opens = [f for idx, f in enumerate(fences) if idx % 2 == 0]
        has_ascii = any(f == "" or f.lower() == "text"
                        for f in opens)
        has_mermaid = any(f.lower() == "mermaid" for f in opens)
        short = header.split(" ", 1)[-1]
        if not has_ascii:
            errors.append(
                f"[{title}] [{tier}] {short} missing ASCII block"
            )
        if not has_mermaid:
            errors.append(
                f"[{title}] [{tier}] {short} missing Mermaid block"
            )


def validate_code_examples(
    title: str, tier: str, block: str, errors: list
) -> None:
    """Code Example Taxonomy checks:
       Every tier requires at least one Wrong-vs-Right pair
       (BAD + GOOD pattern). INTERMEDIATE/COMPLEX additionally
       require a 'production' or 'failure' example signal.
    """
    has_bad = bool(re.search(r"^\*\*BAD[:\*]", block, re.MULTILINE))
    has_good = bool(re.search(r"^\*\*GOOD[:\*]", block, re.MULTILINE))
    if not (has_bad and has_good):
        errors.append(
            f"[{title}] [{tier}] missing Wrong-vs-Right "
            f"(BAD/GOOD) code example pair"
        )
    if tier in ("INTERMEDIATE", "COMPLEX"):
        # Look for a Production or Failure signal keyword
        has_prod = re.search(
            r"(?i)\bproduction\b|\bfailure\b|\bincident\b|\bdiagnos",
            block
        )
        if not has_prod:
            errors.append(
                f"[{title}] [{tier}] no production/failure example "
                f"signal found"
            )


def validate_first_principles_complex(
    title: str, block: str, errors: list
) -> None:
    start = block.find("### 🔩 First Principles")
    if start == -1:
        return
    nxt = block.find("\n### ", start + 5)
    seg = block[start:nxt if nxt != -1 else len(block)]
    if "**CORE INVARIANTS:**" not in seg:
        errors.append(
            f"[{title}] [COMPLEX] First Principles missing "
            f"'CORE INVARIANTS:' block"
        )
        return
    inv_block = seg.split("**CORE INVARIANTS:**", 1)[1]
    inv_block = inv_block.split("**DERIVED DESIGN:**", 1)[0]
    invariants = re.findall(r"^\s*\d+\.\s+\S", inv_block, re.MULTILINE)
    if len(invariants) < 3:
        errors.append(
            f"[{title}] [COMPLEX] First Principles has "
            f"{len(invariants)} invariants (need >=3)"
        )


def validate_failure_modes_complex(
    title: str, block: str, errors: list
) -> None:
    start = block.find("### 🚨 Failure Modes")
    if start == -1:
        return
    nxt = block.find("\n### ", start + 5)
    seg = block[start:nxt if nxt != -1 else len(block)]
    names = re.findall(r"^\*\*Failure \d+", seg, re.MULTILINE)
    if len(names) < 2:
        errors.append(
            f"[{title}] [COMPLEX] Failure Modes has "
            f"{len(names)} named failures (need >=2)"
        )
    if "**Diagnostic:**" not in seg:
        errors.append(
            f"[{title}] [COMPLEX] Failure Modes missing "
            f"'Diagnostic:' label"
        )
    if "**Fix:**" not in seg:
        errors.append(
            f"[{title}] [COMPLEX] Failure Modes missing "
            f"'Fix:' label"
        )


def collect_all_keywords() -> set:
    titles = set()
    for md in LEARN_BASE.rglob("*.md"):
        if md.name == "index.md":
            continue
        if "_config" in md.parts:
            continue
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for m in re.finditer(r"^# (.+)$", text, re.MULTILINE):
            full = m.group(1).strip()
            titles.add(full)
            # Also add title without code prefix (e.g. HIB-084).
            short = re.sub(r'^[A-Z]+-\d+\s+', '', full)
            if short != full:
                titles.add(short)
    return titles


def validate_learning_ladder(
    title: str, tier: str, block: str, corpus: set, errors: list
) -> None:
    if tier == "SIMPLE":
        return  # Learning Ladder is optional in SIMPLE.
    ll_start = block.find("### 🪜 Learning Ladder")
    if ll_start == -1:
        return
    nxt = block.find("\n### ", ll_start + 5)
    end = nxt if nxt != -1 else len(block)
    # S16 closing triplet starts at **The Surprising Truth:**
    st = block.find("**The Surprising Truth:**", ll_start)
    if st != -1 and st < end:
        end = st
    ll = block[ll_start:end]
    # Join continuation lines (indented, non-bold-label) into
    # their parent list items so multi-line references work.
    ll = re.sub(r'\n  +(?!\*\*)', ' ', ll)
    refs = re.findall(r"^- (.+)[ \t]+-[ \t]+", ll, re.MULTILINE)
    for ref in refs:
        ref = ref.strip()
        if ref.startswith("[FILL"):
            continue
        # Skip lines that are bold labels (e.g. **THIS:** or
        # **Prerequisites:**) - not keyword references.
        if ref.startswith("**"):
            continue
        # Strip trailing level suffixes like (L3), (L4), (L5).
        ref = re.sub(r'\s*\(L\d\)\s*$', '', ref)
        # Skip meta-references like "All L3 keywords ..."
        # or "topic architecture keywords (L5+)".
        if re.match(r'^All\b', ref, re.IGNORECASE):
            continue
        if re.search(r'keywords\s*\(L\d', ref):
            continue
        if ref in corpus:
            continue
        # Accept prefix match: 'Entity Graphs' matches
        # 'Entity Graphs (@EntityGraph, @NamedEntityGraph)'.
        if any(c.startswith(ref) for c in corpus):
            continue
        # Strip parenthetical suffixes for base-name matching.
        base = re.sub(r'\s*\(.*$', '', ref).strip()
        if len(base.split()) >= 2 and any(base in c for c in corpus):
            continue
        # Accept ID-prefixed references where the ID matches
        # a corpus keyword (title may be paraphrased).
        id_m = re.match(r'^([A-Z]+-\d+)\s', ref)
        if id_m:
            pfx = id_m.group(1) + " "
            if any(c.startswith(pfx) for c in corpus):
                continue
        errors.append(
            f"[{title}] Learning Ladder references "
            f"unknown keyword: '{ref}'"
        )


def validate_toc(
    fields: dict, body: str, errors: list
) -> None:
    """Check that a ## Keywords TOC exists between frontmatter
    and the first keyword, listing every keyword with a valid
    anchor link."""
    kws = fields.get("_keywords", [])
    if not kws:
        return

    # The TOC must appear before the first H1 keyword heading.
    first_h1 = re.search(r'^# ', body, re.MULTILINE)
    if first_h1 is None:
        return  # No keyword content yet.
    preamble = body[:first_h1.start()]

    if "## Keywords" not in preamble:
        errors.append(
            "missing '## Keywords' TOC before first keyword"
        )
        return

    # Extract TOC link entries: [text](#anchor)
    toc_links = re.findall(
        r'\[([^\]]+)\]\(#([^)]+)\)', preamble
    )
    if len(toc_links) != len(kws):
        errors.append(
            f"TOC has {len(toc_links)} entries but "
            f"keywords[] has {len(kws)}"
        )
        return

    for i, (kw, (link_text, anchor)) in enumerate(
        zip(kws, toc_links), 1
    ):
        if link_text != kw:
            errors.append(
                f"TOC entry {i}: text '{link_text}' "
                f"does not match keyword '{kw}'"
            )
        expected_anchor = heading_to_anchor(kw)
        if anchor != expected_anchor:
            errors.append(
                f"TOC entry {i}: anchor '#{anchor}' "
                f"expected '#{expected_anchor}'"
            )


# ------------------------------------------------------------------
# Index file validation (topic index.md)
# ------------------------------------------------------------------

def validate_index_file(path: Path) -> list:
    """Validate a topic index.md for just-the-docs requirements."""
    errors: list = []
    try:
        text = read_file_text(path)
    except ValidationError as e:
        return [str(e)]

    try:
        fields, _ = parse_frontmatter(text)
    except ValidationError as e:
        errors.append(str(e))
        return errors

    # Determine if this is learn/index.md (root) or topic index.
    is_root = path.parent.name == "learn"

    title = fields.get("title", "")
    if not title:
        errors.append("missing frontmatter field: title")

    layout = fields.get("layout", "")
    if layout != "default":
        errors.append(
            f"layout is '{layout}' but must be 'default'"
        )

    if "has_children" not in fields:
        errors.append(
            "missing frontmatter field: has_children "
            "(required for just-the-docs navigation)"
        )

    if "nav_order" not in fields:
        errors.append("missing frontmatter field: nav_order")

    if "permalink" not in fields:
        errors.append("missing frontmatter field: permalink")

    if is_root:
        # learn/index.md must NOT have parent.
        if "parent" in fields and fields["parent"]:
            errors.append(
                "learn/index.md must not have a parent "
                "(it is the top-level page)"
            )
    else:
        # Topic index must have parent: "Learn".
        parent = fields.get("parent", "")
        if not parent:
            errors.append(
                "missing frontmatter field: parent "
                "(must be 'Learn' for topic index)"
            )
        elif parent != "Learn":
            errors.append(
                f"parent is '{parent}' but must be 'Learn' "
                f"for topic index"
            )

    return errors


# ------------------------------------------------------------------
# Driver
# ------------------------------------------------------------------

def validate_file(path: Path, corpus: set) -> list:
    errors: list = []
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
    validate_jekyll_frontmatter(fields, path, errors)
    blocks = split_keyword_blocks(body)
    status = fields.get("status", "draft")

    if status == "draft" and not blocks:
        return errors

    validate_toc(fields, body, errors)
    validate_keyword_order(fields, blocks, errors)

    for kw_title, block in blocks:
        tier = detect_tier(block)
        validate_tldr(kw_title, tier, block, errors)
        validate_sections(kw_title, tier, block, errors)
        if tier == "INTERMEDIATE":
            validate_mental_model_intermediate(kw_title, block, errors)
        if tier == "COMPLEX":
            validate_first_principles_complex(kw_title, block, errors)
            validate_failure_modes_complex(kw_title, block, errors)
        validate_diagrams(kw_title, tier, block, errors)
        validate_code_examples(kw_title, tier, block, errors)
        if status == "complete":
            validate_word_count(kw_title, tier, block, errors)
            validate_learning_ladder(kw_title, tier, block,
                                     corpus, errors)

    return errors


def validate_path(target: Path) -> int:
    corpus = collect_all_keywords()
    if target.is_file():
        if target.name == "index.md":
            files = []
            index_files = [target]
        else:
            files = [target]
            index_files = []
    elif target.is_dir():
        files = sorted([
            f for f in target.rglob("*.md")
            if f.name != "index.md" and "_config" not in f.parts
        ])
        index_files = sorted([
            f for f in target.rglob("index.md")
            if "_config" not in f.parts
        ])
    else:
        print(f"ERROR: path not found: {target}")
        return 1

    total_errors = 0
    all_files = index_files + files
    print(f"\nValidating {len(all_files)} file(s)...\n")

    for f in index_files:
        errs = validate_index_file(f)
        try:
            rel = f.relative_to(BASE)
        except ValueError:
            rel = f
        if errs:
            print(f"FAIL  {rel}")
            for e in errs:
                print(f"   - {e}")
            total_errors += len(errs)
        else:
            print(f"PASS  {rel}")

    for f in files:
        errs = validate_file(f, corpus)
        try:
            rel = f.relative_to(BASE)
        except ValueError:
            rel = f
        if errs:
            print(f"FAIL  {rel}")
            for e in errs:
                print(f"   - {e}")
            total_errors += len(errs)
        else:
            print(f"PASS  {rel}")

    print(f"\n{'='*60}")
    if total_errors == 0:
        print(f"ALL PASS - {len(all_files)} file(s) validated")
        return 0
    print(
        f"FAILED - {total_errors} error(s) across "
        f"{len(all_files)} file(s)"
    )
    print(
        "Hint: each keyword's tier is auto-detected. See "
        "learn/_config/LEARN_PROMPT.md Section 3 for the "
        "9/13/16-section template definitions."
    )
    return 1


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage:")
        print(
            "  python learn/_config/validate-learn.py "
            "<file.md | folder | --all>"
        )
        sys.exit(1)
    arg = sys.argv[1]
    if arg == "--all":
        target = LEARN_BASE
    else:
        p = Path(arg)
        target = p if p.is_absolute() else (BASE / arg)
    sys.exit(validate_path(target))


if __name__ == "__main__":
    main()
