[CmdletBinding()]
param([string]$CodexHome)
$ErrorActionPreference = 'Stop'
$syncArgs = @((Join-Path $PSScriptRoot 'sync.py'), '--source', $PSScriptRoot, '--apply', '--adopt')
if ($CodexHome) { $syncArgs += @('--codex-home', $CodexHome) }
& python @syncArgs
if ($LASTEXITCODE -ne 0) { throw 'Installation failed. Python 3.11+ and a supported Codex CLI are required.' }
Write-Host 'Installed local defaults. Start a new task to load instructions. No schedule was created.'
