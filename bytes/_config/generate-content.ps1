<#
.SYNOPSIS
  Batch driver for byte content workflows.

.DESCRIPTION
  Runs scaffold and validate operations over a folder. UTF-8 no BOM
  is preserved by Python tools. Requires pwsh 7+.

.EXAMPLE
  pwsh -File bytes/_config/generate-content.ps1 -Folder bytes/java

.EXAMPLE
  pwsh -File bytes/_config/generate-content.ps1 -Validate -Path bytes/java/
#>
[CmdletBinding()]
param(
  [string]$Folder,
  [string]$Path,
  [switch]$Validate
)

$ErrorActionPreference = "Stop"

if ($PSVersionTable.PSVersion.Major -lt 7) {
  Write-Error "Requires PowerShell 7+ (pwsh)."
  exit 2
}

$python = if ($env:USERPROFILE) {
  Join-Path $env:USERPROFILE ".local\bin\python3.14.exe"
} else { "python3" }

if (-not (Test-Path $python)) {
  Write-Warning "Falling back to 'python' on PATH."
  $python = "python"
}

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$scaffold = Join-Path $PSScriptRoot "bytes_scaffold.py"
$validator = Join-Path $PSScriptRoot "validate-byte.py"

if ($Validate) {
  $target = if ($Path) { $Path } elseif ($Folder) { $Folder }
            else { "bytes" }
  & $python $validator $target
  exit $LASTEXITCODE
}

if (-not $Folder) {
  Write-Error "Provide -Folder for batch operations or -Validate."
  exit 2
}

Write-Host "Listing skeletons in $Folder..."
$items = Get-ChildItem -Path $Folder -Filter "*.md" -File |
  Where-Object { $_.Name -notin @("index.md", "learning-path.md") }

foreach ($i in $items) {
  Write-Host "Found: $($i.Name)"
}

Write-Host ""
Write-Host "Running validator..."
& $python $validator $Folder
exit $LASTEXITCODE
