$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$proposal = Join-Path $projectRoot 'software\v5\modules\native\proof_validation\integration\COMPARE-PROPOSAL.json'
if ((Get-FileHash -LiteralPath $proposal -Algorithm SHA256).Hash.ToLowerInvariant() -cne '564a464c60d8df4b7f7753d6383104eac40e63aeeaa3fef2590d3a4264df8050') { throw 'REVIEWED_PROPOSAL_PIN' }
$selected = Get-Content -LiteralPath $proposal -Raw | ConvertFrom-Json
if ($selected.authorizes_two_native_calls -ne $false -or $selected.name -cne 'proof-validation-native-compare-01') { throw 'INERT_PROPOSAL' }
$controller = Join-Path $projectRoot 'software\v5\modules\native\proof_validation\integration\compare.py'
if ((Get-Item -LiteralPath $controller).Length -ne $selected.source.bytes -or (Get-FileHash -LiteralPath $controller -Algorithm SHA256).Hash.ToLowerInvariant() -cne $selected.source.sha256) { throw 'COMPARISON_SOURCE_PIN' }
if ((Get-Item -LiteralPath $selected.build_result.path).Length -ne $selected.build_result.bytes -or (Get-FileHash -LiteralPath $selected.build_result.path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $selected.build_result.sha256) { throw 'BUILD_RESULT_PIN' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$path = Join-Path $local ($selected.name+'-selection.json')
foreach ($candidate in @($path,(Join-Path $local $selected.name),(Join-Path $local ($selected.name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $candidate) { throw ('NOT_FRESH:'+ $candidate) }
}
$selected.authorizes_two_native_calls = $true
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 10)+"`n")
$stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=$path;bytes=$raw.Length;sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant();native_calls=2;executed=$false} | ConvertTo-Json
