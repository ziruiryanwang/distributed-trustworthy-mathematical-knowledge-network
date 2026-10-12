# One remaining compile; reuse the immutable, successful graph command output.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$proposal = Join-Path $projectRoot 'software\v5\aggregate_guest\COMPILE-PROPOSAL.json'
if ((Get-FileHash -LiteralPath $proposal -Algorithm SHA256).Hash.ToLowerInvariant() -cne '3590807f5759c81f651588dd88b84f4216abfc8d973264d61920f2ba02963a4b') { throw 'EXACT_PROPOSAL' }
$selected = Get-Content -LiteralPath $proposal -Raw | ConvertFrom-Json
if ($selected.authorizes_compile_and_owned_telemetry_cleanup -ne $false -or $selected.name -cne 'aggregate-guest-compile-01') { throw 'INERT_COMPILE_ONLY_PROPOSAL' }
$source = Join-Path $projectRoot 'software\v5\aggregate_guest\compile_only.py'
if ((Get-Item -LiteralPath $source).Length -ne $selected.source.bytes -or (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant() -cne $selected.source.sha256) { throw 'EXACT_REVIEWED_SOURCE' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$path = Join-Path $local ($selected.name+'-selection.json')
foreach ($candidate in @($path,(Join-Path $local $selected.name),(Join-Path $local ($selected.name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $candidate) { throw ('NOT_FRESH:'+ $candidate) }
}
$selected.authorizes_compile_and_owned_telemetry_cleanup = $true
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=$path;bytes=$raw.Length;sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant();compile_calls=1;new_graph_calls=0;executed=$false} | ConvertTo-Json
