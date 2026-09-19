[CmdletBinding()]
param(
    [string]$CodexHome
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($CodexHome)) {
    if (-not [string]::IsNullOrWhiteSpace($env:CODEX_HOME)) {
        $CodexHome = $env:CODEX_HOME
    } else {
        $CodexHome = Join-Path $env:USERPROFILE '.codex'
    }
}

$CodexHome = [System.IO.Path]::GetFullPath($CodexHome)
$SourceRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$InstructionSource = Join-Path $SourceRoot 'defaults\AGENTS.md'
$AgentsTarget = Join-Path $CodexHome 'AGENTS.md'
$ConfigTarget = Join-Path $CodexHome 'config.toml'
$Timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$StartMarker = '<!-- codex-efficiency-setup:start -->'
$EndMarker = '<!-- codex-efficiency-setup:end -->'

New-Item -ItemType Directory -Path $CodexHome -Force | Out-Null

function Backup-IfPresent {
    param([string]$Path)
    if (Test-Path -LiteralPath $Path) {
        Copy-Item -LiteralPath $Path -Destination "$Path.bak-$Timestamp"
    }
}

Backup-IfPresent -Path $AgentsTarget
Backup-IfPresent -Path $ConfigTarget

$InstructionText = (Get-Content -Raw -LiteralPath $InstructionSource).Trim()
$ManagedBlock = "$StartMarker`r`n$InstructionText`r`n$EndMarker"

if (Test-Path -LiteralPath $AgentsTarget) {
    $ExistingAgents = Get-Content -Raw -LiteralPath $AgentsTarget
} else {
    $ExistingAgents = ''
}

$ManagedPattern = '(?s)' + [regex]::Escape($StartMarker) + '.*?' + [regex]::Escape($EndMarker)
if ($ExistingAgents -match [regex]::Escape($StartMarker)) {
    $UpdatedAgents = [regex]::Replace($ExistingAgents, $ManagedPattern, $ManagedBlock)
} elseif ([string]::IsNullOrWhiteSpace($ExistingAgents)) {
    $UpdatedAgents = $ManagedBlock + "`r`n"
} else {
    $UpdatedAgents = $ExistingAgents.TrimEnd() + "`r`n`r`n" + $ManagedBlock + "`r`n"
}
[System.IO.File]::WriteAllText($AgentsTarget, $UpdatedAgents, [System.Text.UTF8Encoding]::new($false))

if (Test-Path -LiteralPath $ConfigTarget) {
    $ConfigLines = [System.Collections.Generic.List[string]]::new()
    Get-Content -LiteralPath $ConfigTarget | ForEach-Object { [void]$ConfigLines.Add($_) }
} else {
    $ConfigLines = [System.Collections.Generic.List[string]]::new()
}

$Desired = [ordered]@{
    model = '"gpt-6-astra"'
    model_reasoning_effort = '"low"'
    service_tier = '"default"'
}

$FirstSection = $ConfigLines.Count
for ($Index = 0; $Index -lt $ConfigLines.Count; $Index++) {
    if ($ConfigLines[$Index] -match '^\s*\[') {
        $FirstSection = $Index
        break
    }
}

$Missing = [System.Collections.Generic.List[string]]::new()
foreach ($Entry in $Desired.GetEnumerator()) {
    $Found = $false
    for ($Index = 0; $Index -lt $FirstSection; $Index++) {
        if ($ConfigLines[$Index] -match ('^\s*' + [regex]::Escape($Entry.Key) + '\s*=')) {
            $ConfigLines[$Index] = "$($Entry.Key) = $($Entry.Value)"
            $Found = $true
            break
        }
    }
    if (-not $Found) {
        [void]$Missing.Add("$($Entry.Key) = $($Entry.Value)")
    }
}

for ($Index = $Missing.Count - 1; $Index -ge 0; $Index--) {
    $ConfigLines.Insert(0, $Missing[$Index])
}

[System.IO.File]::WriteAllLines($ConfigTarget, $ConfigLines, [System.Text.UTF8Encoding]::new($false))

Write-Host "Installed Codex efficiency defaults in $CodexHome"
Write-Host 'Start a new Codex task for the global instructions to take effect.'
