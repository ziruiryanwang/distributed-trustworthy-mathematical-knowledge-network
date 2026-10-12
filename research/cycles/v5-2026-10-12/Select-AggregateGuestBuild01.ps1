# Exact selection preparation only, not a Cargo/build/guest/proof invocation.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$proposal = Join-Path $projectRoot 'software\v5\aggregate_guest\BUILD-PROPOSAL.json'
if ((Get-FileHash -LiteralPath $proposal -Algorithm SHA256).Hash.ToLowerInvariant() -cne 'e10b3a5d5f32718583e41986d7b46dd6bb514867f31f5c3fc9cfbe0bf3978729') { throw 'PROPOSAL_PIN' }
$selected = Get-Content -LiteralPath $proposal -Raw | ConvertFrom-Json
if ($selected.authorizes_guest_build_and_owned_telemetry_cleanup -ne $false -or $selected.name -cne 'aggregate-guest-build-01') { throw 'INERT_PROPOSAL' }
$count = 0
foreach ($row in $selected.sources.psobject.Properties) {
    $path = Join-Path $projectRoot $row.Name
    if ((Get-Item -LiteralPath $path).Length -ne $row.Value.bytes -or (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $row.Value.sha256) { throw ('SOURCE_PIN:'+ $row.Name) }
    $count++
}
if ($count -ne 38) { throw 'EXACT_38_SOURCE_CLOSURE' }
$comparison = $selected.native_comparison
if ((Get-Item -LiteralPath $comparison.path).Length -ne $comparison.bytes -or (Get-FileHash -LiteralPath $comparison.path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $comparison.sha256) { throw 'NATIVE_COMPARISON_PIN' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$path = Join-Path $local ($selected.name+'-selection.json')
foreach ($candidate in @($path,(Join-Path $local $selected.name),(Join-Path $local ($selected.name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $candidate) { throw ('NOT_FRESH:'+ $candidate) }
}
$selected.authorizes_guest_build_and_owned_telemetry_cleanup = $true
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=$path;bytes=$raw.Length;sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant();sources=$count;executed=$false} | ConvertTo-Json
