# Prepare only the new body-refusal controls; no test or product import.
param(
    [Parameter(Mandatory=$true)][string]$ExpectedTransportSha,
    [Parameter(Mandatory=$true)][string]$ExpectedEvidenceSha,
    [Parameter(Mandatory=$true)][string]$ExpectedHelperSha,
    [Parameter(Mandatory=$true)][string]$ExpectedTestSha
)
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
$basisPath = Join-Path $checks 'supplier-controls-01-selection.json'
Require-Digest $basisPath '76e8de0f264c2396b86176d9793ff5d6b0e68a0d15733f6b3bc702004045c262'
$basis = Get-Content -LiteralPath $basisPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($property in $basis.sources.psobject.Properties) {
    Require-Digest (Join-Path $projectRoot $property.Name) $property.Value
    # Retain predecessors for byte identity/fixture imports, not suite execution.
    $sources[$property.Name] = $property.Value
}
$additional = [ordered]@{
    'software/v5/transport/acquisition_resilience.py' = $ExpectedTransportSha
    'software/v5/client/supplier_resilient/workspace_evidence.py' = $ExpectedEvidenceSha
    'software/v5/client/supplier_resilient/semantic_reader.py' = $ExpectedHelperSha
    'software/v5/client/supplier_resilient/test_resilience.py' = $ExpectedTestSha
}
foreach ($property in $additional.GetEnumerator()) {
    if ($sources.Contains($property.Key)) { throw 'NEW_SOURCE_COLLISION' }
    Require-Digest (Join-Path $projectRoot $property.Key) $property.Value
    $sources[$property.Key] = $property.Value
}
$runtime = [ordered]@{}
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    Require-Digest $property.Name $property.Value
    $runtime[$property.Name] = $property.Value
}
$name = 'acquisition-resilience-controls-01'
$selectionPath = Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath (Join-Path $checks $name))) {
    throw 'FRESH_SELECTION_REQUIRED'
}
$selected = [ordered]@{
    schema = 'DMKN_V5_LOCAL_CHECK_V1'
    name = $name
    sources = $sources
    runtime_pins = $runtime
    argv = @($basis.argv[0], '-I', '-S', '-B',
        '{snapshot}\software\v5\client\supplier_resilient\test_resilience.py', '--output', '{output}')
    limits = [ordered]@{
        cpu_seconds=20; wall_seconds=60; memory_mib=128; active_processes=2
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
