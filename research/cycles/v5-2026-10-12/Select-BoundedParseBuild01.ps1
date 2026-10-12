$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$fresh = [ordered]@{
    'aggregate_lib.rs' = '4476115a65c03d5c81250017d4308b2dc8e3d64b8c2190f428c30ac03ed1098a'
    'aggregate_relation.rs' = '6a2425aa6d26bf10ab6053d92f498d09b6c7bdde598efe118a5bc7bd2ceb0947'
    'build.py' = 'f068cdaa3f3fe24ddceb6ea8aeb0e56080b07bdabb88625b1d3f107aef92d8df'
    'canonical.rs' = 'f8356d9300f5436b3b6fb7a76b7d2d19e0b3dcedae0bfd00e1e10abea54de9c1'
    'census.rs' = '48cad55b54d3cd233d760871308ccfdc54bb50711adb89651f7d2861caa5a1d5'
    'controls.rs' = '9ea0a9b0da364b9c05d1eb0535d1becc7e070b09e887a05bd7b0bb9cc65db00a'
    'module_lib.rs' = '328692d04054f54bcb79ce316b14df6c472590160b39615942a027202d55be76'
    'module_relation.rs' = '0f78c1663673f291c7b612cc3bdef423124cc6cc47fd649b71e5bc13d4cd808a'
}
$retained = @(
    'software/v5/aggregate/native.rs',
    'software/v5/aggregate_claims/header.rs',
    'software/v5/aggregate_claims/membership.rs',
    'software/v5/aggregate_claims/wire.rs',
    'software/v5/aggregate_parse_once/census.rs',
    'software/v5/modules/receipt/src/commitments.rs',
    'software/v5/modules/receipt/src/foundation_data.rs',
    'software/v5/modules/receipt/src/foundation_static.rs',
    'software/v5/modules/receipt/src/input.rs',
    'software/v5/modules/receipt/src/journal.rs',
    'software/v5/modules/receipt/src/policy.rs'
)
$priorMapPath = Join-Path $projectRoot 'experiments/v5-local-checks/proof-validation-integration-build-01/source-map.json'
if ((Get-FileHash -LiteralPath $priorMapPath -Algorithm SHA256).Hash.ToLowerInvariant() -cne 'a5693f19236bb8051e476d9f61d8d2449cbcd023054a1e9c8606607049957f2a') { throw 'RETAINED_MAP_PIN' }
$priorMap = Get-Content -LiteralPath $priorMapPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($relative in $retained) {
    $pin = $priorMap.psobject.Properties[$relative].Value
    $path = Join-Path $projectRoot $relative
    if ($null -eq $pin -or (Get-Item -LiteralPath $path).Length -ne $pin.bytes -or (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $pin.sha256) { throw ('RETAINED_SOURCE_PIN:' + $relative) }
    $sources[$relative] = $pin
}
foreach ($name in $fresh.Keys) {
    $relative = 'software/v5/bounded_parse/' + $name
    $path = Join-Path $projectRoot $relative
    if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $fresh[$name]) { throw ('REVIEWED_SOURCE_PIN:' + $relative) }
    $sources[$relative] = [ordered]@{ bytes = (Get-Item -LiteralPath $path).Length; sha256 = $fresh[$name] }
}
if ($sources.Count -ne 19) { throw 'EXACT_19_SOURCES' }
$name = 'bounded-parse-native-build-01'
$local = Join-Path $projectRoot 'experiments/v5-local-checks'
$selectionPath = Join-Path $local ($name + '-selection.json')
foreach ($path in @($selectionPath,(Join-Path $local $name),(Join-Path $local ($name + '-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:' + $path) }
}
$selection = [ordered]@{schema='DMKN_V5_BOUNDED_PARSE_BUILD_V1';name=$name;authorizes_compile_only=$true;sources=$sources}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 12) + "`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=$selectionPath;bytes=$raw.Length;sha256=(Get-FileHash -LiteralPath $selectionPath -Algorithm SHA256).Hash.ToLowerInvariant();sources=$sources.Count;compiler_calls=4;checker_rebuilds=0;executed=$false} | ConvertTo-Json
