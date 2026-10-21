# Root selection for one retained RC snapshot-host link, not host execution.
param([Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$BuilderSha256)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'restricted-snapshot-host-build-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $local $name),(Join-Path $local ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_SELECTION_REQUIRED:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) { throw 'ORDINARY_FILE_REQUIRED' }
    [ordered]@{bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$oldMapPath = Join-Path $local 'small-aggregate-snapshot-host-build-01\INPUT-MAP.json'
if ((Pin $oldMapPath).sha256 -cne '91f26a1052f22410925bf6d94328295d266c09236ce948c24cddd2aa546c809f') { throw 'EXACT_RETAINED_INPUT_MAP' }
$oldMap = Get-Content -LiteralPath $oldMapPath -Raw | ConvertFrom-Json
$pins = [ordered]@{}
foreach ($property in $oldMap.runtime_pins.psobject.Properties) { $pins[$property.Name] = $property.Value }
if ($pins.Count -ne 1071) { throw 'EXACT_1071_PRIOR_PINS' }
$oldLibrary = Join-Path $local 'proof-validation-integration-build-01\libdmkn_aggregate_relation.rlib'
if (-not $pins.Contains($oldLibrary)) { throw 'EXACT_OLD_LIBRARY' }
$pins.Remove($oldLibrary)
$libraries = [ordered]@{
    'libdmkn_rc_relation.rlib'='1bdfd6a0943b6a09248ae99aefd793b63384a957bf8d98c0cd8d8b430fd04a0b'
    'libdmkn_aggregate_relation.rlib'='be8bdcb4c815e5c610145e5fea28a6d6601fe8dd9ae8cd04f3bf35c5b9dbcbba'
}
foreach ($entry in $libraries.GetEnumerator()) {
    $path = Join-Path (Join-Path $local 'restricted-composition-build-02') $entry.Key
    if ($pins.Contains($path) -or (Pin $path).sha256 -cne $entry.Value) { throw 'ADOPTED_NEW_LIBRARY' }
    $pins[$path] = $entry.Value
}
if ($pins.Count -ne 1072) { throw 'EXACT_1072_SUCCESSOR_PINS' }
$expected = [ordered]@{
    'software/v5/restricted_guest/build_snapshot_host.py'=$BuilderSha256
    'software/v5/aggregate_small/aggregate_host.rs'='6644d9a03f25a59089fd735b0e2f2229ec8940dedbe2502568dfd8c6a36d9c25'
    'software/v5/aggregate/receipt.rs'='41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254'
}
$sources = [ordered]@{}
foreach ($relative in $expected.Keys) {
    $row = Pin (Join-Path $projectRoot $relative)
    if ($row.sha256 -cne $expected[$relative]) { throw ('REVIEWED_SOURCE_CHANGED:'+ $relative) }
    $sources[$relative] = $row
}
$selected = [ordered]@{
    schema='DMKN_V5_RC_SNAPSHOT_HOST_BUILD_V1';name=$name;authorizes_compile_only=$true
    sources=$sources;runtime_pins=$pins
    limits=[ordered]@{
        worker_cpu_seconds=240;worker_wall_seconds=300;memory_mib=3072;active_processes=6
        ordinary_controller_cpu_seconds=40;controller_cpu_seconds=60;total_wall_seconds=420
        fresh_output_bytes=536870912;fresh_output_entries=8192;command_log_bytes=1048576
    }
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 12)+"`n")
if ($raw.Length -gt 2097152) { throw 'SELECTION_BYTE_LIMIT' }
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=$selectionPath;pin=(Pin $selectionPath);sources=$sources.Count;runtime_pins=$pins.Count;compiler_calls=1;executed=$false} | ConvertTo-Json -Depth 5
