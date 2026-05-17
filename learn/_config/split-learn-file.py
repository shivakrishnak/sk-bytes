#!/usr/bin/env python3
"""Split a learn file with many COMPLEX keywords into N smaller files.

Usage:
    python split-learn-file.py <file> <N> [--suffix s1,s2,s3]

Example:
    python split-learn-file.py "learn/hibernate/Hibernate - Architecture and META.md" 2
    python split-learn-file.py "learn/sql/SQL - Architecture and META.md" 3 --suffix "Foundations,Internals,Strategy"
"""
import re
import sys
import math
from pathlib import Path


def slugify(text: str) -> str:
    """Convert text to kramdown GFM anchor."""
    s = text.lower()
    s = re.sub(r'[^a-z0-9 \-]', '', s)
    s = re.sub(r' +', '-', s.strip())
    return s


def parse_file(path: Path):
    """Parse a learn file into frontmatter, toc, and keyword blocks."""
    text = path.read_text(encoding='utf-8')

    # Extract frontmatter
    fm_match = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
    if not fm_match:
        raise ValueError("No YAML frontmatter found")
    fm_raw = fm_match.group(1)
    after_fm = text[fm_match.end():]

    # Parse keywords from frontmatter
    kw_list = []
    in_kw = False
    fm_lines = fm_raw.split('\n')
    for line in fm_lines:
        if re.match(r'^keywords:', line):
            in_kw = True
            continue
        if in_kw:
            m = re.match(r'^\s+-\s+(.+)', line)
            if m:
                kw_list.append(m.group(1).strip())
            else:
                in_kw = False

    # Parse other frontmatter fields
    fm_fields = {}
    for line in fm_lines:
        m = re.match(r'^(\w[\w_]*):\s+(.+)', line)
        if m and m.group(1) != 'keywords':
            val = m.group(2).strip().strip('"\'')
            fm_fields[m.group(1)] = val

    # Find TOC section and keyword blocks
    # TOC ends at the first H1 keyword heading.
    # Keywords after that are separated by double-rule:
    # \n---\n\n---\n
    first_h1 = re.search(r'^# ', after_fm, re.MULTILINE)
    if first_h1:
        toc_section = after_fm[:first_h1.start()].rstrip()
        kw_body = after_fm[first_h1.start():]
    else:
        toc_section = after_fm
        kw_body = ""

    # Split keyword body on double-rule separator
    kw_blocks = re.split(
        r'\n---\s*\n\s*\n---\s*\n', kw_body
    ) if kw_body else []

    # Remove empty blocks
    kw_blocks = [b for b in kw_blocks if b.strip()]

    # Extract keyword title from each block
    block_titles = []
    for block in kw_blocks:
        m = re.search(r'^#\s+(.+)$', block.strip(), re.MULTILINE)
        if m:
            block_titles.append(m.group(1).strip())
        else:
            block_titles.append("UNKNOWN")

    return {
        'fm_raw': fm_raw,
        'fm_fields': fm_fields,
        'fm_lines': fm_lines,
        'keywords': kw_list,
        'toc_section': toc_section,
        'kw_blocks': kw_blocks,
        'block_titles': block_titles,
        'full_text': text,
    }


def build_frontmatter(fields, keywords):
    """Build YAML frontmatter string."""
    lines = ['---']
    title = fields.get('title', '')
    if ': ' in title:
        lines.append(f'title: "{title}"')
    else:
        lines.append(f'title: "{title}"')
    for key in ['topic', 'subtopic']:
        if key in fields:
            lines.append(f'{key}: {fields[key]}')
    lines.append('keywords:')
    for kw in keywords:
        lines.append(f'  - {kw}')
    for key in ['difficulty_range', 'status', 'version',
                'layout', 'parent', 'grand_parent',
                'nav_order', 'permalink']:
        if key in fields:
            val = fields[key]
            if key == 'parent':
                lines.append(f'parent: "{val}"')
            elif key == 'grand_parent':
                lines.append(f'grand_parent: "{val}"')
            else:
                lines.append(f'{key}: {val}')
    lines.append('---')
    return '\n'.join(lines)


def build_toc(keywords):
    """Build ## Keywords TOC section."""
    lines = ['\n## Keywords\n']
    for i, kw in enumerate(keywords, 1):
        anchor = slugify(kw)
        lines.append(f'{i}. [{kw}](#{anchor})')
    lines.append('')
    return '\n'.join(lines)


def split_file(path: Path, n: int, suffixes=None):
    """Split a file into n smaller files."""
    data = parse_file(path)

    kw_blocks = data['kw_blocks']
    block_titles = data['block_titles']
    keywords = data['keywords']
    fm = data['fm_fields']

    total = len(kw_blocks)
    if total == 0:
        print(f"ERROR: No keyword blocks found in {path}")
        return

    print(f"File: {path.name}")
    print(f"  Keywords in YAML: {len(keywords)}")
    print(f"  Keyword blocks found: {total}")
    print(f"  Block titles: {block_titles[:3]}...")
    print(f"  Splitting into {n} files")

    # Calculate group sizes (distribute evenly)
    base_size = total // n
    remainder = total % n
    groups = []
    idx = 0
    for i in range(n):
        size = base_size + (1 if i < remainder else 0)
        groups.append(list(range(idx, idx + size)))
        idx += size

    # Generate suffix names
    if suffixes and len(suffixes) == n:
        suffix_list = suffixes
    else:
        suffix_list = [f"Part {i+1}" for i in range(n)]

    # Get base info
    topic = fm.get('topic', '')
    orig_subtopic = fm.get('subtopic', '')
    parent_name = fm.get('parent', topic)
    grand_parent = fm.get('grand_parent', 'Learn')
    difficulty = fm.get('difficulty_range', 'hard')
    status = fm.get('status', 'complete')
    version = fm.get('version', '1')
    layout = fm.get('layout', 'default')
    orig_nav = int(fm.get('nav_order', '1'))

    # Parse original permalink pattern
    orig_permalink = fm.get('permalink', '')

    stem = path.stem  # e.g. "Hibernate - Architecture and META"
    # Extract the topic prefix and subtopic
    # e.g. "Hibernate - Architecture and META" -> prefix="Hibernate", sub="Architecture and META"
    dash_idx = stem.find(' - ')
    if dash_idx > 0:
        file_prefix = stem[:dash_idx]
        file_sub = stem[dash_idx + 3:]
    else:
        file_prefix = stem
        file_sub = ""

    created_files = []

    for gi, group_indices in enumerate(groups):
        suffix = suffix_list[gi]

        # New subtopic name
        new_subtopic = f"{file_sub} {suffix}".strip()
        new_title = f"{topic} - {new_subtopic}"
        new_filename = f"{file_prefix} - {new_subtopic}.md"
        new_path = path.parent / new_filename

        # Keywords for this group
        group_kws = []
        group_blocks = []
        for idx in group_indices:
            if idx < len(block_titles):
                group_kws.append(block_titles[idx])
            if idx < len(kw_blocks):
                group_blocks.append(kw_blocks[idx])

        # Build new nav_order (spread after original)
        new_nav = orig_nav + gi

        # Build permalink
        sub_slug = slugify(new_subtopic)
        topic_slug = slugify(topic)
        new_permalink = f"/learn/{topic_slug}/{sub_slug}/"

        # Build frontmatter
        new_fm_fields = {
            'title': new_title,
            'topic': topic,
            'subtopic': new_subtopic,
            'difficulty_range': difficulty,
            'status': status,
            'version': version,
            'layout': layout,
            'parent': parent_name,
            'grand_parent': grand_parent,
            'nav_order': str(new_nav),
            'permalink': new_permalink,
        }

        fm_str = build_frontmatter(new_fm_fields, group_kws)
        toc_str = build_toc(group_kws)

        # Assemble file content
        content_parts = []
        for bi, block in enumerate(group_blocks):
            # Ensure block starts cleanly
            block = block.strip()
            content_parts.append(block)

        # Join with double-rule separator
        separator = "\n\n---\n\n---\n\n"
        body = separator.join(content_parts)

        full_content = fm_str + toc_str + "\n---\n\n---\n\n" + body + "\n"

        new_path.write_text(full_content, encoding='utf-8')
        created_files.append((new_path, len(group_kws)))
        print(f"  Created: {new_filename} ({len(group_kws)} kw)")

    # Report
    print(f"\n  Original: {path.name} ({total} kw)")
    print(f"  Split into {len(created_files)} files")
    for fp, count in created_files:
        print(f"    {fp.name}: {count} keywords")

    return created_files


def main():
    if len(sys.argv) < 3:
        print("Usage: python split-learn-file.py <file> <N>"
              " [--suffix s1,s2,...]")
        sys.exit(1)

    path = Path(sys.argv[1])
    n = int(sys.argv[2])

    suffixes = None
    if '--suffix' in sys.argv:
        si = sys.argv.index('--suffix')
        if si + 1 < len(sys.argv):
            suffixes = sys.argv[si + 1].split(',')

    if not path.exists():
        print(f"ERROR: File not found: {path}")
        sys.exit(1)

    split_file(path, n, suffixes)


if __name__ == '__main__':
    main()
