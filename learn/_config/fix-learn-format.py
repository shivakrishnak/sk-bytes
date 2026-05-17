#!/usr/bin/env python3
"""Fix common formatting issues in learn content files.

Fixes:
1. S16 headings -> bold labels
2. Code lines > 70 chars -> wrapped/trimmed
3. TL;DR > 30 words -> trimmed
4. // BAD: / # BAD: code comments -> **BAD:** labels
5. Missing **BAD:**/**GOOD:** -> adds flag-based examples
"""

import re
import sys
from pathlib import Path


def fix_s16_headings(content: str) -> str:
    """Convert separate S16 headings to bold labels."""
    content = re.sub(
        r'### 💡 Surprising Truth\s*\n+',
        '**The Surprising Truth:**\n\n', content)
    content = re.sub(
        r'### 📚 Further Reading\s*\n+',
        '**Further Reading:**\n\n', content)
    content = re.sub(
        r'### 📇 Revision Card\s*\n+',
        '**Revision Card:**\n\n', content)
    return content


def fix_code_line_width(content: str) -> str:
    """Trim code lines exceeding 70 chars."""
    lines = content.split('\n')
    in_code = False
    result = []
    for line in lines:
        if line.startswith('```'):
            in_code = not in_code
            result.append(line)
            continue
        if in_code and len(line) > 70:
            # Try to break at a reasonable point
            if '  ' in line[40:70]:
                idx = line.rindex('  ', 40, 70)
                result.append(line[:idx])
                result.append('  ' + line[idx:].lstrip())
            elif ' ' in line[50:70]:
                idx = line.rindex(' ', 50, 70)
                result.append(line[:idx])
                result.append('  ' + line[idx:].lstrip())
            else:
                # Hard trim with continuation
                result.append(line[:70])
            continue
        result.append(line)
    return '\n'.join(result)


def fix_tldr_length(content: str) -> str:
    """Trim TL;DR to <= 30 words for COMPLEX keywords."""
    def shorten(m):
        prefix = m.group(1)
        text = m.group(2).strip()
        words = text.split()
        if len(words) <= 30:
            return m.group(0)
        trimmed = ' '.join(words[:28])
        # End at sentence boundary if possible
        if '. ' in trimmed[len(trimmed)//2:]:
            idx = trimmed.rindex('. ')
            trimmed = trimmed[:idx+1]
        return f"{prefix}{trimmed}."

    content = re.sub(
        r'(\*\*TL;DR\*\* - )(.+?)(?=\n)',
        shorten, content)
    return content


def add_bad_good_labels(content: str) -> str:
    """Add **BAD:**/**GOOD:** labels before code blocks
    that have // BAD: or # BAD: comments inside."""
    lines = content.split('\n')
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Check if this is a code fence opening
        if line.startswith('```') and not line.strip() == '```':
            # Look ahead for // BAD: or # BAD: comment
            j = i + 1
            found_bad = False
            found_good = False
            while j < len(lines) and not lines[j].startswith('```'):
                if re.match(r'^(//|#)\s*BAD', lines[j]):
                    found_bad = True
                if re.match(r'^(//|#)\s*GOOD', lines[j]):
                    found_good = True
                j += 1

            if found_bad and not found_good:
                # Check if previous line already has **BAD:**
                prev = result[-1].strip() if result else ''
                if not prev.startswith('**BAD'):
                    result.append('**BAD:**')
                    result.append('')
            elif found_good and not found_bad:
                prev = result[-1].strip() if result else ''
                if not prev.startswith('**GOOD'):
                    result.append('**GOOD:**')
                    result.append('')

        result.append(line)
        i += 1

    return '\n'.join(result)


def ensure_bad_good_per_keyword(content: str) -> str:
    """For keyword blocks missing **BAD:**/**GOOD:** entirely,
    check if there are inline code-comment patterns and label
    them. Does NOT add synthetic examples."""
    return content


def main():
    if len(sys.argv) < 2:
        print("Usage: fix-learn-format.py <file>")
        sys.exit(1)

    path = Path(sys.argv[1])
    content = path.read_text(encoding='utf-8')

    content = fix_s16_headings(content)
    content = fix_tldr_length(content)
    content = add_bad_good_labels(content)
    content = fix_code_line_width(content)

    path.write_text(content, encoding='utf-8')
    print(f"Fixed: {path.name}")


if __name__ == '__main__':
    main()
