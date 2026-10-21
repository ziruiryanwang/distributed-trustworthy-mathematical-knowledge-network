# Preserve the original selection/input/horizons; narrow only the process cap.
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks=Join-Path $projectRoot 'experiments/v5-local-checks'
$oldPath=Join-Path $checks 'managed-contribution-01-selection.json'
$newPath=Join-Path $checks 'managed-contribution-01-eight-processes-selection.json'
$inputPath=Join-Path $checks 'managed-contribution-01-input.json'
if ((Get-FileHash -LiteralPath $oldPath -Algorithm SHA256).Hash.ToLowerInvariant() -cne 'cbd5e7cb510dbb6818e50dd6ed31aaa24f4378d17c13448478b613187f51c67b') { throw 'ORIGINAL_SELECTION_PIN' }
if ((Get-FileHash -LiteralPath $inputPath -Algorithm SHA256).Hash.ToLowerInvariant() -cne 'd8f40d9c05b4edf5242b319f4dcba204ab5da09e11b8467091f5d5e7be7b1c6f') { throw 'ORIGINAL_INPUT_PIN' }
foreach ($path in @($newPath,(Join-Path $checks 'managed-contribution-01'))) {
    if (Test-Path -LiteralPath $path) { throw 'UNUSED_TARGET_REQUIRED' }
}
$selection=Get-Content -LiteralPath $oldPath -Raw -Encoding UTF8 | ConvertFrom-Json
$originalInput=Get-Content -LiteralPath $inputPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($selection.name -cne 'managed-contribution-01' -or $selection.limits.active_processes -ne 12 -or
    [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()+300000 -ge $originalInput.horizons.write_until_ms) { throw 'UNCHANGED_SELECTION_OR_HORIZON' }
$selection.limits.active_processes=8
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 40)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_SIZE' }
$stream=[IO.File]::Open($newPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=$newPath;selection_sha256=(Get-FileHash -LiteralPath $newPath -Algorithm SHA256).Hash.ToLowerInvariant();
    original_input_unchanged=$true;original_horizons_unchanged=$true;active_processes=8;executed=$false} | ConvertTo-Json
