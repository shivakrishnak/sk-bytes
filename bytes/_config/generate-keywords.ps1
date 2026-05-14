<#
.SYNOPSIS
    sk-bytes - Keyword Generator & Folder Scaffolding
.DESCRIPTION
    Generates keyword lists for byte topics, groups them into
    sub-topic files, and creates folder/index/stub structure.

    Uses bytes/_config/BYTES_KEYWORD_GENERATOR.md (Category Keyword
    Generator v1.0) as the master specification for all keyword
    generation. The prompt file at
    .github/prompts/bytes-generate-keywords.prompt.md orchestrates
    this process for byte topics.

    Supports four flows:
    1. New topic from scratch (generates keywords via
       bytes/_config/BYTES_KEYWORD_GENERATOR.md v1.0 spec)
    2. New topic from existing dictionary category
    3. Add subtopic to existing topic
    4. Scan existing dictionary category to find new
       sub-topic opportunities

    DESIGN CONSIDERATIONS:
    - For new topics without an index.md, use
      bytes/_config/BYTES_KEYWORD_GENERATOR.md to generate a
      comprehensive keyword list, then apply folder/file rules
      and generate file content per BYTES_PROMPT.md v1.0.
    - For brand-new topics (e.g., Angular), analyse where the
      topic belongs, generate keywords via BYTES_KEYWORD_GENERATOR.md,
      create folders and files, and generate content.
    - For new subtopics where the main topic already exists,
      create the file in the existing topic folder, apply file
      rules (5+ keywords per file), generate keywords via
      BYTES_KEYWORD_GENERATOR.md, and generate content.
    - For existing dictionary categories (e.g., JVM, JCC),
      scan the dictionary index.md, analyse keywords, map to
      byte sub-topic files, and generate content.

    ALWAYS use pwsh (PowerShell 7+):
      pwsh -ExecutionPolicy Bypass -File bytes/_config/generate-keywords.ps1

    REFERENCES:
    - bytes/_config/BYTES_KEYWORD_GENERATOR.md: Master keyword spec
    - .github/prompts/bytes-generate-keywords.prompt.md: Prompt file
    - bytes/_config/BYTES_PROMPT.md: Content generation spec

.PARAMETER Topic
    Topic name (e.g., "Java", "Angular", "Kubernetes")
.PARAMETER FromDictionary
    Dictionary category code(s) to source keywords from
    (e.g., "JLG", "JVM,JLG"). Optional. If sk-bytes is a standalone
    repo with no sister dictionary, omit this flag.
.PARAMETER Subtopic
    Add a new subtopic file to an existing topic
.PARAMETER Keywords
    Comma-separated list of keywords for a new subtopic
.PARAMETER DryRun
    Preview what would be created without writing files
.EXAMPLE
    pwsh -File generate-keywords.ps1 -Topic Java -FromDictionary "JVM,JLG"
.EXAMPLE
    pwsh -File generate-keywords.ps1 -Topic Angular
.EXAMPLE
    pwsh -File generate-keywords.ps1 -Topic React -Subtopic "Hooks" `
      -Keywords "useState,useEffect,useContext,useReducer,useMemo,useCallback,useRef,Custom Hooks"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$Topic,

    [Parameter()]
    [string]$FromDictionary,

    [Parameter()]
    [string]$Subtopic,

    [Parameter()]
    [string]$Keywords,

    [Parameter()]
    [switch]$DryRun
)

# Constants
$ErrorActionPreference = "Stop"
$WorkspaceRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$BytesRoot     = Join-Path $WorkspaceRoot "bytes"
$Utf8NoBom     = [System.Text.UTF8Encoding]::new($false)

if ($PSVersionTable.PSVersion.Major -lt 7) {
    Write-Error "Requires PowerShell 7+ (pwsh)."
    exit 2
}

# Helpers
function Get-TopicFolder {
    param([string]$TopicName)
    return ($TopicName.ToLower() -replace '\s+', '-' -replace '[^a-z0-9\-]', '')
}

function Get-TopicPath {
    param([string]$TopicName)
    return Join-Path $BytesRoot (Get-TopicFolder $TopicName)
}

function Write-Utf8NoBom {
    param([string]$Path, [string]$Content)
    if ($DryRun) {
        Write-Host "DRY RUN - would write: $Path"
        return
    }
    $dir = Split-Path -Parent $Path
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    [System.IO.File]::WriteAllText($Path, $Content, $Utf8NoBom)
    Write-Host "wrote: $Path"
}

function New-TopicIndex {
    param(
        [string]$TopicName,
        [string]$TopicFolder,
        [string]$Description,
        [string]$DictionarySources
    )
    $sources = if ($DictionarySources) { "**Dictionary Sources:** $DictionarySources" } else { "" }
    @"
---
layout: default
title: "$TopicName"
parent: "Bytes"
nav_order: 1
has_children: true
permalink: /bytes/$TopicFolder/
description: Byte-sized study units for $TopicName
keywords_count: 0
files_count: 0
---

# $TopicName

$Description

$sources

| File | Keywords | Description |
| ---- | -------- | ----------- |

"@
}

function New-SubtopicStub {
    param(
        [string]$TopicName,
        [string]$SubtopicName,
        [string[]]$KeywordList,
        [string]$Difficulty = "mixed"
    )
    $kwYaml = ($KeywordList | ForEach-Object { "  - $_" }) -join "`n"
    @"
---
title: "$TopicName - $SubtopicName"
topic: $TopicName
subtopic: $SubtopicName
keywords:
$kwYaml
difficulty_range: $Difficulty
status: draft
version: 0
---

> Stub generated by generate-keywords.ps1.
> Fill via @bytes-generate-entries or /bytes agent per BYTES_PROMPT.md v1.0.
> Minimum 5 keywords per file (this file has $($KeywordList.Count)).
"@
}

# Workflows
Write-Host ""
Write-Host "=== sk-bytes Keyword Generator ==="
Write-Host "Spec: bytes/_config/BYTES_KEYWORD_GENERATOR.md (v1.0)"
Write-Host ""
Write-Host "Topic:          $Topic"
if ($FromDictionary) { Write-Host "From dict:      $FromDictionary" }
if ($Subtopic)       { Write-Host "Subtopic:       $Subtopic" }
if ($Keywords)       { Write-Host "Keywords:       $Keywords" }
if ($DryRun)         { Write-Host "Mode:           DRY RUN" }
Write-Host ""

$topicFolder = Get-TopicFolder $Topic
$topicPath   = Get-TopicPath  $Topic
$indexPath   = Join-Path $topicPath "index.md"

# Flow: add subtopic to existing topic
if ($Subtopic) {
    if (-not $Keywords) {
        Write-Error "When -Subtopic is set, -Keywords must also be provided (>= 5)."
        exit 2
    }
    $kwList = $Keywords -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ }
    if ($kwList.Count -lt 5) {
        Write-Error ("File rule violation: each sub-topic file must contain " +
            "at least 5 keywords. Got $($kwList.Count).")
        exit 1
    }
    if (-not (Test-Path $topicPath)) {
        Write-Error "Topic folder not found: $topicPath. Create the topic first."
        exit 1
    }
    $fileName = "$Topic - $Subtopic.md"
    $filePath = Join-Path $topicPath $fileName
    if (Test-Path $filePath) {
        Write-Error "File already exists: $filePath"
        exit 1
    }
    $content = New-SubtopicStub -TopicName $Topic -SubtopicName $Subtopic `
        -KeywordList $kwList
    Write-Utf8NoBom -Path $filePath -Content $content
    Write-Host ""
    Write-Host "Done. Next: invoke @bytes-generate-keywords to expand keyword"
    Write-Host "       coverage to 7 mastery levels per BYTES_KEYWORD_GENERATOR.md."
    exit 0
}

# Flow: new topic (or topic from dictionary category)
if (-not (Test-Path $topicPath)) {
    Write-Host "Creating topic folder: $topicPath"
    if (-not $DryRun) {
        New-Item -ItemType Directory -Path $topicPath -Force | Out-Null
    }
}

if (-not (Test-Path $indexPath)) {
    $desc = "Byte-sized study units for $Topic."
    $content = New-TopicIndex -TopicName $Topic -TopicFolder $topicFolder `
        -Description $desc -DictionarySources $FromDictionary
    Write-Utf8NoBom -Path $indexPath -Content $content
}

Write-Host ""
Write-Host "Topic scaffold ready."
Write-Host ""
Write-Host "Next step: invoke @bytes-generate-keywords with:"
Write-Host "  target: $Topic"
if ($FromDictionary) {
    Write-Host "  from:   $FromDictionary"
}
Write-Host ""
Write-Host "The prompt will apply BYTES_KEYWORD_GENERATOR.md v1.0:"
Write-Host "  - generate L0..L6 + META keywords"
Write-Host "  - apply all 22 rules from Section 2"
Write-Host "  - run all 17 quality checks from Section 4"
Write-Host "  - group keywords into sub-topic files (>= 5 per file)"
Write-Host "  - update topic index.md non-destructively"
Write-Host ""
exit 0
