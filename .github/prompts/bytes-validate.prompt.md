---
mode: agent
description: "Validate one or more bytes against the v1.0 spec and report failures."
---

# Validate byte

Run the structural and content validator.

## Steps

1. Resolve target: single file or folder (recursive).
2. For each `.md` byte:
   ```pwsh
   python bytes/_config/validate-byte.py <path>
   ```
3. Collect errors. Categorize:
   - Frontmatter: missing field, wrong type, unquoted title with colon.
   - Structure: missing/reordered/duplicate section.
   - Content: word count out of range, missing depth signals, missing
     progression signals, no diagnostic command in section 9, no
     prereq/next IDs in section 12.
   - Formatting: em dash present, line >70 chars, ASCII diagram
     without Mermaid pair, missing `---` divider before `###`.
4. Report a table: file | error type | line | detail.
5. Do NOT auto-fix. Report only; user decides.

## Output

Markdown table of failures. End with totals: `N files passed, M files
failed, K total errors`.
