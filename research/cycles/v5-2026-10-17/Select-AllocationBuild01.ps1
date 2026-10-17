# Prepare one exact fresh allocation-refined build plan; no compiler invocation.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'prover-allocation-build-01'
$selectionPath = Join-Path $checks ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $checks $name),(Join-Path $checks ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'ORDINARY_FILE_REQUIRED' }
    [ordered]@{bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$priorPath = Join-Path $checks 'small-aggregate-stage-host-build-01\selection.json'
if ((Pin $priorPath).sha256 -cne '049129dacf8b43ea3e4a1796a26098dfb207ddbc80d5c1b49cbfde94fc71fa38') { throw 'RETAINED_SELECTION_CHANGED' }
$prior = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
if (@($prior.runtime_pins.psobject.Properties).Count -ne 1071) { throw 'RETAINED_RUNTIME_COUNT' }
$sources = [ordered]@{}
foreach ($relative in @('software/v5/prover_memory/build.py','software/v5/prover_memory/SOURCE.json',
                       'software/v5/prover_memory/preflight.patch','software/v5/prover_memory/BUILD-RECIPE.md')) {
    $sources[$relative] = Pin (Join-Path $projectRoot $relative)
}
if ($sources['software/v5/prover_memory/SOURCE.json'].sha256 -cne 'c93a45a6a558718c931c39b121e9bcffa7d464ecaa1d5b0e80185efd6cace710' -or
    $sources['software/v5/prover_memory/preflight.patch'].sha256 -cne 'a53940b67580e215c55c2eae1e33e12f93a410193dde5f6414f533e4517fdc6c') { throw 'REFINEMENT_CHANGED' }
$selection = [ordered]@{
    schema='DMKN_V5_PROVER_ALLOCATION_BUILD_V1';name=$name;authorizes_compile_only=$true
    sources=$sources;runtime_pins=$prior.runtime_pins
    limits=[ordered]@{worker_cpu_seconds=240;worker_wall_seconds=300;memory_mib=2048;active_processes=6
        total_worker_cpu_seconds=1200;ordinary_controller_cpu_seconds=120;controller_cpu_seconds=180
        total_wall_seconds=1800;fresh_output_bytes=1073741824;fresh_output_entries=8192;command_log_bytes=1048576}
}
$bytes = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 12)+"`n")
if ($bytes.Length -gt 1048576) { throw 'SELECTION_BOUND' }
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($bytes,0,$bytes.Length);$stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=$selectionPath;pin=(Pin $selectionPath);sources=$sources;executed=$false} | ConvertTo-Json -Depth 5
