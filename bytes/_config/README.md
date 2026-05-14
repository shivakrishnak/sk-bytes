# bytes/\_config

Generation tooling and master spec for the `/bytes` system.

## Files

| File                         | Purpose                                               |
| ---------------------------- | ----------------------------------------------------- |
| `BYTES_PROMPT.md`            | Master content spec v1.0 (14-section template).       |
| `BYTES_KEYWORD_GENERATOR.md` | Master keyword generator spec v1.0 (7 levels + META). |
| `topic-registry.md`          | Topic-to-folder map + sub-topic file plan.            |
| `bytes_scaffold.py`          | Optional preview emitter (14-section stubs).          |
| `validate-byte.py`           | Structural + content validator.                       |
| `generate-keywords.ps1`      | Topic / subtopic keyword scaffolder (PowerShell 7+).  |
| `generate-content.ps1`       | Batch content-fill driver (PowerShell 7+).            |

## Quick commands

```pwsh
# Create a new topic folder + index
pwsh -File bytes/_config/generate-keywords.ps1 -Topic Java

# Add a subtopic file (>=5 keywords)
pwsh -File bytes/_config/generate-keywords.ps1 -Topic React `
  -Subtopic "Hooks" `
  -Keywords "useState,useEffect,useContext,useReducer,useMemo"

# Optional - preview 14-section structure with [FILL:] stubs
python bytes/_config/bytes_scaffold.py java

# Validate one file
python bytes/_config/validate-byte.py "bytes/java/Java - Collections.md"

# Validate a folder
python bytes/_config/validate-byte.py bytes/java/

# Batch fill
pwsh -File bytes/_config/generate-content.ps1 -Folder bytes/java
```

## Encoding rules

Always use `pwsh` (PowerShell 7+). Never `powershell.exe`. Python
writes files with UTF-8 no BOM. PowerShell uses
`[System.Text.UTF8Encoding]::new($false)` for the same.
