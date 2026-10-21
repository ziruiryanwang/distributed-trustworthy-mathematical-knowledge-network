# Stage one finite changed-boundary control request; never executes it.
param([Parameter(Mandatory=$true)][string]$ReviewedSourceHashesJson)
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
$checks = Join-Path $projectRoot 'experiments/v5-local-checks'
$basisPath = Join-Path $checks 'instantiation-discovery-controls-01-selection.json'
Require-Digest $basisPath '421469bd6569e89359e8de6118c85f09698f0e603f6cfb2b908258f7bb031257'
$basis = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_LOCAL_CHECK_V1' -or $basis.name -cne 'instantiation-discovery-controls-01') {
    throw 'BASIS_SCHEMA'
}
$sources = [ordered]@{}
foreach ($property in $basis.sources.psobject.Properties) {
    Require-Digest (Join-Path $projectRoot $property.Name) $property.Value
    $sources[$property.Name] = $property.Value
}
if ($sources.Count -ne 147) { throw 'BASIS_SOURCE_COUNT' }
# Read-only predecessor fixture helpers, not their suite. The fixture context
# also hashes its original service source; both must exist in the snapshot.
$support = [ordered]@{
    'software/v5/client/test_serve_workspace.py' = '5b51a5a8d78fe98927e27de98f09b6e0b004fb2a137b3be3cb9d1a4feba31361'
    'software/v5/client/serve_workspace.py' = '89723f2e8a03abcaa709560f6d991ffc5d2bb349ef6cb662aadad7589a73936c'
}
foreach ($key in $support.Keys) {
    if ($sources.Contains($key) -and $sources[$key] -cne $support[$key]) { throw 'SUPPORT_PIN_CONFLICT' }
    Require-Digest (Join-Path $projectRoot $key) $support[$key]
    $sources[$key] = $support[$key]
}
$required = @(
    'software/v5/base_projection/client/base_projection.py',
    'software/v5/base_projection/client/serve_workspace.py',
    'software/v5/base_projection/client/serve_advertised.py',
    'software/v5/base_projection/distribution.py',
    'software/v5/base_projection/controls.py'
)
if ($ReviewedSourceHashesJson.Length -gt 8192) { throw 'REVIEWED_MAP_BOUND' }
$additional = $ReviewedSourceHashesJson | ConvertFrom-Json
$keys = @($additional.psobject.Properties.Name)
if ($keys.Count -ne $required.Count -or @(Compare-Object $keys $required -CaseSensitive).Count -ne 0) {
    throw 'EXACT_REVIEWED_SOURCE_SET'
}
foreach ($property in $additional.psobject.Properties) {
    Require-Digest (Join-Path $projectRoot $property.Name) $property.Value
    if ($sources.Contains($property.Name)) { throw 'FRESH_SUCCESSOR_REQUIRED' }
    $sources[$property.Name] = $property.Value
}
$runtime = [ordered]@{}
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    Require-Digest $property.Name $property.Value
    $runtime[$property.Name] = $property.Value
}
$name = 'base-projection-controls-01'
$selectionPath = Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath (Join-Path $checks $name))) {
    throw 'FRESH_SELECTION_REQUIRED'
}
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1'; name=$name; sources=$sources; runtime_pins=$runtime
    argv=@($basis.argv[0], '-I', '-S', '-B',
        '{snapshot}\software\v5\base_projection\controls.py', '--output', '{output}')
    limits=[ordered]@{cpu_seconds=45; wall_seconds=75; memory_mib=384; active_processes=2;
        stdout_bytes=1048576; stderr_bytes=1048576}
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 16)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_JSON_BOUND' }
$stream = [IO.File]::Open($selectionPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
[ordered]@{path=$selectionPath; sha256=(Digest $selectionPath);
    sources=$sources.Count; runtime_pins=$runtime.Count; executed=$false} | ConvertTo-Json
