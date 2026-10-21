# One fresh frontend export plus zero-parent native checking; no proof production.
param(
    [Parameter(Mandatory=$true)][string]$ReviewedSourceSha,
    [Parameter(Mandatory=$true)][string]$ReviewedAdapterSha,
    [Parameter(Mandatory=$true)][string]$ReviewedLeanSha
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) {
    (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Require-Digest([string]$path, [string]$expected) {
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or (Digest $path) -cne $expected) {
        throw ('REVIEWED_INPUT_CHANGED: '+$path)
    }
}
function Read-Json([string]$path) {
    Get-Content -LiteralPath $path -Raw -Encoding UTF8 | ConvertFrom-Json
}
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$basisPath = Join-Path $checks 'delta-author-01-selection.json'
Require-Digest $basisPath '159c8c6f8a5350b3d3d113187fba1126dbc4be761923f03193d162a9455e740b'
$basis = Read-Json $basisPath
$mapPath = Join-Path $checks 'distribution-coherent-01-input.json'
$mapSha = '1903bb44b6176dae5d43142f11cd90ddde6d494d51d5b5c1c377f3ebf5182528'
Require-Digest $mapPath $mapSha
$map = Read-Json $mapPath
$controlSelection = Join-Path $checks 'nat-literal-controls-01-selection.json'
$control = Read-Json $controlSelection
$closed = Read-Json (Join-Path $checks 'nat-literal-controls-01\RESULT.json')
$passed = Read-Json (Join-Path $checks 'nat-literal-controls-01\controls-result.json')
if ($control.sources.'software/v5/nat_literals/source_rows.py' -cne $ReviewedSourceSha -or
    $closed.selection_sha256 -cne (Digest $controlSelection) -or
    $closed.result.status -cne 'COMMAND_EXITED_ZERO_AND_CLOSED' -or
    $passed.status -cne 'PASS' -or $passed.tests -ne 9 -or
    $passed.failures -ne 0 -or $passed.errors -ne 0 -or $passed.skipped -ne 0) {
    throw 'EXACT_IMPORTER_CONTROLS_REQUIRED'
}
$sources = [ordered]@{}
$retained = @('tools/Run-V5-Check.py', 'software/v5/modules/__init__.py',
    'software/v5/modules/codec.py', 'software/v5/modules/model.py',
    'software/v5/modules/native_rows.py', 'software/v5/modules/receipt/__init__.py',
    'software/v5/modules/receipt/witness.py', 'software/v5/authoring/__init__.py',
    'software/v5/authoring/worker.py')
foreach ($relative in $retained) { $sources[$relative] = $basis.sources.$relative }
$sources['software/v5/authoring/test_native_frontend.py'] = '3f13702cea308fff9e0552c9465f1b00361fa3d8fda2824de9193c4cca90f547'
$sources['software/v5/nat_literals/source_rows.py'] = $ReviewedSourceSha
$sources['software/v5/nat_literals/native.py'] = $ReviewedAdapterSha
$sources['software/v5/nat_literals/Arithmetic.lean'] = $ReviewedLeanSha
foreach ($relative in $sources.Keys) {
    Require-Digest (Join-Path $projectRoot $relative) $sources[$relative]
}
$runtime = [ordered]@{}
$pythonRoot = Split-Path -Parent $basis.argv[0]
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    if ($property.Name.StartsWith($pythonRoot+'\', [StringComparison]::OrdinalIgnoreCase)) {
        $runtime[$property.Name] = $property.Value
    }
}
$runtime[$mapPath] = $mapSha
foreach ($name in @('frontend','native','foundation')) {
    $pin = $map.assets.$name
    $runtime[$pin.path] = $pin.sha256
}
foreach ($property in $map.lean_runtime.psobject.Properties) {
    $pin = $property.Value
    $runtime[$pin.path] = $pin.sha256
}
foreach ($path in $runtime.Keys) { Require-Digest $path $runtime[$path] }
$name = 'nat-literal-native-01'
$selectionPath = Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $selectionPath) -or
    (Test-Path -LiteralPath (Join-Path $checks $name))) { throw 'FRESH_SELECTION_REQUIRED' }
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1'; name=$name; sources=$sources; runtime_pins=$runtime
    argv=@($basis.argv[0], '-I', '-S', '-B',
        '{snapshot}\software\v5\nat_literals\native.py', '--output', '{output}',
        '--runtime-map', $mapPath, '--runtime-map-sha256', $mapSha)
    limits=[ordered]@{
        cpu_seconds=60; wall_seconds=120; memory_mib=512; active_processes=4
        stdout_bytes=1048576; stderr_bytes=1048576
    }
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 16)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_JSON_BOUND' }
$stream = [IO.File]::Open($selectionPath, [IO.FileMode]::CreateNew,
    [IO.FileAccess]::Write, [IO.FileShare]::None)
try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
[ordered]@{path=$selectionPath; sha256=(Digest $selectionPath); sources=$sources.Count
    runtime_pins=$runtime.Count; executed=$false; proof_calls=0} | ConvertTo-Json
