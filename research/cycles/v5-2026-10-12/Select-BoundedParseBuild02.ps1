$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$priorMapPath = Join-Path $projectRoot 'experiments/v5-local-checks/bounded-parse-native-build-01/source-map.json'
if ((Get-FileHash -LiteralPath $priorMapPath -Algorithm SHA256).Hash.ToLowerInvariant() -cne '2d2e9bcc29c19d84fe8530434eee5f35e937194f3f8e4ab50821092378695c42') { throw 'RETAINED_MAP_PIN' }
$priorMap = Get-Content -LiteralPath $priorMapPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($property in $priorMap.psobject.Properties) {
    $relative = $property.Name
    $pin = $property.Value
    $path = Join-Path $projectRoot $relative
    if ((Get-Item -LiteralPath $path).Length -ne $pin.bytes -or (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $pin.sha256) { throw ('UNCHANGED_SOURCE_PIN:' + $relative) }
    $sources[$relative] = $pin
}
if ($sources.Count -ne 19) { throw 'EXACT_19_USED_SOURCES' }
$fresh = [ordered]@{
    'build_remaining.py' = 'ea6f285cd56f5ff8e59b36640a55a006e2a46549499b9e639c308434c5eadd7c'
    'controls_root.rs' = 'dfcb4657c70c072fccfb5df98e63f58f9aab685d296ccf6986f44749269dacc6'
}
foreach ($name in $fresh.Keys) {
    $relative = 'software/v5/bounded_parse/' + $name
    $path = Join-Path $projectRoot $relative
    if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $fresh[$name]) { throw ('REVIEWED_SOURCE_PIN:' + $relative) }
    $sources[$relative] = [ordered]@{ bytes = (Get-Item -LiteralPath $path).Length; sha256 = $fresh[$name] }
}
$name = 'bounded-parse-native-build-02'
$local = Join-Path $projectRoot 'experiments/v5-local-checks'
$selectionPath = Join-Path $local ($name + '-selection.json')
foreach ($path in @($selectionPath,(Join-Path $local $name),(Join-Path $local ($name + '-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:' + $path) }
}
$selection = [ordered]@{schema='DMKN_V5_BOUNDED_PARSE_REMAINING_BUILD_V1';name=$name;authorizes_compile_only=$true;sources=$sources}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 12) + "`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=$selectionPath;bytes=$raw.Length;sha256=(Get-FileHash -LiteralPath $selectionPath -Algorithm SHA256).Hash.ToLowerInvariant();sources=$sources.Count;remaining_link_calls=2;executed=$false} | ConvertTo-Json
