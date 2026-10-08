# One-shot incident repair. Refuses any unexpected topology or changed bytes.
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$repairCanonical = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
$repairLegacy = 'E:\Distributed Verifiable Mathematical Knowledge Network'
$repairAudit = Join-Path $repairCanonical 'research\audits\workspace-repair-2026-09-23'
if ($PSScriptRoot -ne $repairAudit) { throw 'Use the canonical repair script.' }
$repairManifest = Get-Content -LiteralPath (Join-Path $repairAudit 'BEFORE.json') -Raw | ConvertFrom-Json
$repairRecovered = Join-Path $repairAudit 'recovered'
$repairSource = Join-Path $repairLegacy 'experiments'
$repairDestination = Join-Path $repairRecovered 'experiments'
foreach ($repairPath in @($repairCanonical, $repairLegacy, $repairSource, $repairAudit)) {
    $repairItem = Get-Item -LiteralPath $repairPath -Force
    if (-not $repairItem.PSIsContainer -or
        ($repairItem.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        throw "Refusing non-directory or link: $repairPath"
    }
}
if ((Resolve-Path -LiteralPath $repairSource).ProviderPath -ne
    'E:\Distributed Verifiable Mathematical Knowledge Network\experiments') {
    throw 'Unexpected resolved source.'
}
if ([IO.Path]::GetFullPath($repairDestination) -ne
    'E:\Distributed Trustworthy Mathematical Knowledge Network\research\audits\workspace-repair-2026-09-23\recovered\experiments') {
    throw 'Unexpected destination outside exact recovery allocation.'
}
if (Test-Path -LiteralPath $repairRecovered) { throw 'Recovery allocation already exists.' }
$repairAll = @(Get-ChildItem -LiteralPath $repairLegacy -Recurse -Force)
if (@($repairAll | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) {
    throw 'Unexpected link under source.'
}
$repairActualFiles = @($repairAll | Where-Object { -not $_.PSIsContainer })
$repairActualDirs = @($repairAll | Where-Object { $_.PSIsContainer } | ForEach-Object {
    $_.FullName.Substring($repairLegacy.Length + 1).Replace('\', '/')
})
if ($repairActualFiles.Count -ne $repairManifest.files.Count -or
    @(Compare-Object $repairActualDirs $repairManifest.unexpected_directories).Count) {
    throw 'Unexpected source inventory.'
}
foreach ($repairEntry in $repairManifest.files) {
    $repairFile = Get-Item -LiteralPath (Join-Path $repairLegacy $repairEntry.relative_path)
    if ($repairFile.Length -ne $repairEntry.bytes -or
        (Get-FileHash -LiteralPath $repairFile.FullName -Algorithm SHA256).Hash -ne $repairEntry.sha256) {
        throw "Source changed: $($repairEntry.relative_path)"
    }
    if ((Get-FileHash -LiteralPath (Join-Path $repairCanonical $repairEntry.relative_path) -Algorithm SHA256).Hash -ne $repairEntry.canonical_peer_sha256) {
        throw "Canonical peer changed: $($repairEntry.relative_path)"
    }
}
New-Item -ItemType Directory -Path $repairRecovered | Out-Null
# Move only the explicitly verified child tree; never move/delete the project.
Move-Item -LiteralPath $repairSource -Destination $repairDestination
foreach ($repairEntry in $repairManifest.files) {
    $repairFile = Get-Item -LiteralPath (Join-Path $repairRecovered $repairEntry.relative_path)
    if ($repairFile.Length -ne $repairEntry.bytes -or
        (Get-FileHash -LiteralPath $repairFile.FullName -Algorithm SHA256).Hash -ne $repairEntry.sha256) {
        throw "Recovery verification failed: $($repairEntry.relative_path)"
    }
}
if (@(Get-ChildItem -LiteralPath $repairLegacy -Force).Count -ne 0) {
    throw 'Legacy directory is not empty; leave it intact for inspection.'
}
# Non-recursive removal of the now-empty, explicitly named accidental shell.
Remove-Item -LiteralPath $repairLegacy -Force
New-Item -ItemType Junction -Path $repairLegacy -Target $repairCanonical | Out-Null
& (Join-Path $repairCanonical 'tools\Enter-Project.ps1')
[pscustomobject]@{
    Status = 'PASS'
    PreservedFiles = $repairManifest.files.Count
    PreservedBytes = $repairManifest.unexpected_total_file_bytes
    RecoveryDirectory = $repairRecovered
    CompletedUtc = [DateTime]::UtcNow.ToString('o')
}
