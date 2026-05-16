# learn/\_config

Generation tooling and master spec for the `/learn` system
(sk-learn v1.0, tri-template).

## Files

| File                         | Purpose                                                                                   |
| ---------------------------- | ----------------------------------------------------------------------------------------- |
| `LEARN_PROMPT.md`            | Master content spec v1.0 (SIMPLE/INTERMEDIATE/COMPLEX templates + Code Example Taxonomy). |
| `LEARN_KEYWORD_GENERATOR.md` | Master keyword generator v1.0 (7 levels + META, 25 rules, 20 quality checks).             |
| `topic-registry.md`          | Topic-to-folder map + sub-topic file plan.                                                |
| `learn_scaffold.py`          | Optional preview emitter (tri-template stubs).                                            |
| `validate-learn.py`          | Structural + content validator (auto-tier detection).                                     |
| `generate-keywords.ps1`      | Topic / subtopic keyword scaffolder (PowerShell 7+).                                      |
| `generate-content.ps1`       | Batch content-fill driver (PowerShell 7+).                                                |

## Quick commands

```pwsh
# Create a new topic folder + index
pwsh -File learn/_config/generate-keywords.ps1 -Topic Java

# Add a subtopic file (>=5 keywords)
pwsh -File learn/_config/generate-keywords.ps1 -Topic React `
  -Subtopic "Hooks" `
  -Keywords "useState,useEffect,useContext,useReducer,useMemo"

# Optional - preview tier-aware [FILL:] stubs
python learn/_config/learn_scaffold.py java
# Force a tier for all keywords in one file:
python learn/_config/learn_scaffold.py --file "java/Java - Foundations.md" --tier SIMPLE

# Validate one file
python learn/_config/validate-learn.py "learn/java/Java - Collections.md"

# Validate a folder
python learn/_config/validate-learn.py learn/java/

# Batch fill
pwsh -File learn/_config/generate-content.ps1 -Folder learn/java
```

## Tier routing

The scaffolder and validator both route each keyword to its
template tier deterministically:

```
L0, L1            -> SIMPLE        (9 sections, 400-700 wd)
L2, L3            -> INTERMEDIATE  (13 sections, 900-1,300 wd)
L4, L5, L6, META  -> COMPLEX       (16 sections, 1,400-2,000 wd)
```

The validator auto-detects each keyword's tier from its section
markers and applies the matching schema.

## Encoding rules

Always use `pwsh` (PowerShell 7+). Never `powershell.exe`.
Python writes files with UTF-8 no BOM. PowerShell uses
`[System.Text.UTF8Encoding]::new($false)` for the same.
