# Prepare exact changed-boundary controls; no product import or test execution.
param([Parameter(Mandatory=$true)][string]$ReviewedSourceHashesJson)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) {
    (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Require-Digest([string]$path, [string]$expected) {
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or (Digest $path) -cne $expected) {
        throw ('REVIEWED_INPUT_CHANGED: ' + $path)
    }
}
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$basisPath = Join-Path $checks 'declaration-continuation-controls-01-selection.json'
Require-Digest $basisPath 'eee5ea43dc626df9754a9e695a24b51334e45ccf5066ab67b65b8540e22f1cda'
$basis = Get-Content -LiteralPath $basisPath -Raw | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_LOCAL_CHECK_V1' -or
    $basis.name -cne 'declaration-continuation-controls-01') { throw 'BASIS_SCHEMA' }
$sources = [ordered]@{}
foreach ($property in $basis.sources.psobject.Properties) {
    Require-Digest (Join-Path $projectRoot $property.Name) $property.Value
    $sources[$property.Name] = $property.Value
}
if ($ReviewedSourceHashesJson.Length -gt 32768) { throw 'REVIEWED_MAP_BOUND' }
$additional = $ReviewedSourceHashesJson | ConvertFrom-Json
foreach ($property in $additional.psobject.Properties) {
    if ($property.Name -cnotmatch '^software/v5/[A-Za-z0-9_/-]+\.py$' -or
        $property.Name.Contains('..')) { throw 'SOURCE_SCOPE' }
    $path = [IO.Path]::GetFullPath((Join-Path $projectRoot $property.Name))
    if (-not $path.StartsWith($projectRoot+'\software\v5\', [StringComparison]::Ordinal)) {
        throw 'CANONICAL_SOURCE_SCOPE'
    }
    Require-Digest $path $property.Value
    if ($sources.Contains($property.Name) -and $sources[$property.Name] -cne $property.Value) {
        throw 'PREDECESSOR_REWRITE_REFUSED'
    }
    $sources[$property.Name] = $property.Value
}
if ($sources.Count -gt 256 -or
    -not $sources.Contains('software/v5/interface_views/test_interface.py')) {
    throw 'SOURCE_CENSUS_OR_TEST_MISSING'
}
$runtime = [ordered]@{}
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    Require-Digest $property.Name $property.Value
    $runtime[$property.Name] = $property.Value
}
$name = 'interface-view-controls-01'
$selectionPath = Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $selectionPath) -or
    (Test-Path -LiteralPath (Join-Path $checks $name))) { throw 'FRESH_SELECTION_REQUIRED' }
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1'; name=$name; sources=$sources; runtime_pins=$runtime
    argv=@($basis.argv[0], '-I', '-S', '-B',
        '{snapshot}\software\v5\interface_views\test_interface.py', '--output', '{output}')
    limits=[ordered]@{
        cpu_seconds=30; wall_seconds=60; memory_mib=256; active_processes=2
        stdout_bytes=1048576; stderr_bytes=1048576
    }
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 16)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_JSON_BOUND' }
$stream = [IO.File]::Open($selectionPath, [IO.FileMode]::CreateNew,
    [IO.FileAccess]::Write, [IO.FileShare]::None)
try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
[ordered]@{
    path=$selectionPath; sha256=(Digest $selectionPath)
    sources=$sources.Count; runtime_pins=$runtime.Count; executed=$false
} | ConvertTo-Json
