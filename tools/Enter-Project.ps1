# This guard changes only this PowerShell session, never desktop app metadata.
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$projectCanonical = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
$projectLegacy = 'E:\Distributed Verifiable Mathematical Knowledge Network'
$projectRoot = Get-Item -LiteralPath $projectCanonical -Force
if (-not $projectRoot.PSIsContainer -or
    ($projectRoot.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
    throw 'Canonical project root must be the actual directory, not a link.'
}
$projectExpectedScript = Join-Path $projectCanonical 'tools\Enter-Project.ps1'
if (-not [string]::Equals($PSCommandPath, $projectExpectedScript,
        [StringComparison]::OrdinalIgnoreCase)) {
    throw "Run the guard by its canonical absolute path: $projectExpectedScript"
}
foreach ($projectMarker in @('AGENTS.md', 'GOAL.md', 'research\NOW.md')) {
    if (-not (Test-Path -LiteralPath (Join-Path $projectCanonical $projectMarker) -PathType Leaf)) {
        throw "Missing canonical project marker: $projectMarker"
    }
}
$projectLegacyItem = Get-Item -LiteralPath $projectLegacy -Force -ErrorAction SilentlyContinue
$projectLegacyState = 'absent'
if ($null -ne $projectLegacyItem) {
    $projectTargets = @($projectLegacyItem.Target)
    if ($projectLegacyItem.LinkType -eq 'Junction' -and
        ($projectLegacyItem.Attributes -band [IO.FileAttributes]::ReparsePoint) -and
        $projectTargets.Count -eq 1 -and
        [string]::Equals([string]$projectTargets[0], $projectCanonical,
            [StringComparison]::OrdinalIgnoreCase)) {
        $projectLegacyState = 'junction-to-canonical'
    } elseif ($projectLegacyItem.PSIsContainer -and
        -not ($projectLegacyItem.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        $projectLegacyChildren = @(Get-ChildItem -LiteralPath $projectLegacy -Force)
        $projectMarkerTemplate = Join-Path $projectCanonical 'tools\retired-workspace-AGENTS.md'
        if ($projectLegacyChildren.Count -ne 1 -or
            $projectLegacyChildren[0].Name -ne 'AGENTS.md' -or
            $projectLegacyChildren[0].PSIsContainer -or
            ($projectLegacyChildren[0].Attributes -band [IO.FileAttributes]::ReparsePoint) -or
            (Get-FileHash -LiteralPath $projectLegacyChildren[0].FullName -Algorithm SHA256).Hash -ne
            (Get-FileHash -LiteralPath $projectMarkerTemplate -Algorithm SHA256).Hash) {
            throw 'Workspace split detected: legacy directory must contain only the exact retirement marker. Preserve unexpected files before working.'
        }
        $projectLegacyState = 'retired-placeholder-awaiting-app-cwd-correction'
    } else {
        throw 'Workspace split detected: unexpected legacy path type or junction target.'
    }
}
Set-Location -LiteralPath $projectCanonical
[pscustomobject]@{
    Status = 'PASS'
    CanonicalRoot = $projectCanonical
    WorkingDirectory = (Get-Location).ProviderPath
    LegacyPath = $projectLegacy
    LegacyState = $projectLegacyState
}
