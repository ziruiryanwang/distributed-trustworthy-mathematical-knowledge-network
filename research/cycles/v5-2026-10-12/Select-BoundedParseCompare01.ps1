param([Parameter(Mandatory=$true)][string]$BuildResultSha256)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
if ($BuildResultSha256 -cnotmatch '^[0-9a-f]{64}$') { throw 'EXACT_BUILD_RESULT_HASH_REQUIRED' }
$source = Join-Path $projectRoot 'software/v5/bounded_parse/compare.py'
$sourceHash = '240f8cce7d5fdedddb6bdfa7b7dd0375921a6d1fa2566319b808ad1068bc32d6'
if ((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant() -cne $sourceHash -or (Get-Item -LiteralPath $source).Length -ne 15017) { throw 'REVIEWED_COMPARISON_SOURCE' }
$local = Join-Path $projectRoot 'experiments/v5-local-checks'
$build = Join-Path $local 'bounded-parse-native-build-02'
$resultPath = Join-Path $build 'RESULT.json'
if ((Get-FileHash -LiteralPath $resultPath -Algorithm SHA256).Hash.ToLowerInvariant() -cne $BuildResultSha256) { throw 'ADOPTED_BUILD_RESULT' }
$built = Get-Content -LiteralPath $resultPath -Raw | ConvertFrom-Json
if ($built.schema -cne 'DMKN_V5_BOUNDED_PARSE_REMAINING_BUILD_RESULT_V1' -or $built.status -cne 'PASS_BOUNDED_PARSE_TWO_REMAINING_LINKS_ONLY' -or (Test-Path -LiteralPath (Join-Path $build 'FINALIZATION-FAILED.json'))) { throw 'SUCCESSFUL_FINAL_BUILD_REQUIRED' }
$name = 'bounded-parse-native-compare-01'
$selectionPath = Join-Path $local ($name + '-selection.json')
foreach ($path in @($selectionPath,(Join-Path $local $name),(Join-Path $local ($name + '-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:' + $path) }
}
$selection = [ordered]@{
    schema='DMKN_V5_BOUNDED_PARSE_COMPARISON_V1'
    name=$name
    authorizes_ten_controls_and_two_native_calls=$true
    source=[ordered]@{bytes=15017;sha256=$sourceHash}
    build_result=[ordered]@{path=$resultPath;bytes=(Get-Item -LiteralPath $resultPath).Length;sha256=$BuildResultSha256}
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 12) + "`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=$selectionPath;bytes=$raw.Length;sha256=(Get-FileHash -LiteralPath $selectionPath -Algorithm SHA256).Hash.ToLowerInvariant();test_groups=10;native_calls=2;executed=$false} | ConvertTo-Json
