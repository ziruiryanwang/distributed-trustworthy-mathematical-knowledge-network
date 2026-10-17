# Generate one exact new snapshot-host link selection; no compiler invocation.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'geometry17-snapshot-host-build-01'
$selectionPath = Join-Path $checks ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $checks $name),(Join-Path $checks ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'ORDINARY_FILE_REQUIRED' }
    [ordered]@{bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$priorPath = Join-Path $checks 'prover-allocation-build-01-selection.json'
if ((Pin $priorPath).sha256 -cne '7a548b3f74c0c5bbe8bc2ba68e408a3dfdf22addefb9410b1a25f5d8be5d13ff') { throw 'RETAINED_SELECTION_CHANGED' }
$prior = [IO.File]::ReadAllText($priorPath) | ConvertFrom-Json
if (@($prior.runtime_pins.psobject.Properties).Count -ne 1071) { throw 'RETAINED_RUNTIME_COUNT' }
$expected = [ordered]@{
    'software/v5/aggregate_geometry/build_snapshot.py' = 'd9ae9e237b7c191ece8d7862b116b56f372863e7dea68579eef8426dc043eaf6'
    'software/v5/aggregate_geometry/aggregate_host.rs' = '7f3fefab48c30ec414a54620391f4be1ca8e27de19a6f61c7091614d148cf5c3'
    'software/v5/aggregate/receipt.rs' = '41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254'
}
$sources = [ordered]@{}
foreach ($relative in $expected.Keys) {
    $sources[$relative] = Pin (Join-Path $projectRoot $relative)
    if ($sources[$relative].sha256 -cne $expected[$relative]) { throw ('SOURCE_REVIEW_PIN:'+ $relative) }
}
$selection = [ordered]@{
    schema='DMKN_V5_GEOMETRY17_SNAPSHOT_HOST_BUILD_V1'; name=$name; authorizes_compile_only=$true
    sources=$sources; runtime_pins=$prior.runtime_pins
    limits=[ordered]@{worker_cpu_seconds=240;worker_wall_seconds=300;memory_mib=2048;active_processes=6
        ordinary_controller_cpu_seconds=40;controller_cpu_seconds=60;total_wall_seconds=420
        fresh_output_bytes=536870912;fresh_output_entries=8192;command_log_bytes=1048576}
}
$bytes = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 12)+"`n")
if ($bytes.Length -gt 1048576) { throw 'SELECTION_BOUND' }
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($bytes,0,$bytes.Length);$stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=$selectionPath;pin=(Pin $selectionPath);sources=$sources;executed=$false} | ConvertTo-Json -Depth 5
