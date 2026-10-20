# Prepare the new composed-service controls only. No product import or test.
param(
    [Parameter(Mandatory=$true)][string]$ExpectedServiceSha,
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
$basisPath = Join-Path $checks 'ordinary-serving-controls-03-selection.json'
Require-Digest $basisPath '64b269af83ea802f8437f69225b9e22000ad906e4f3a10691e5020fe64d6ae64'
$basis = Get-Content -LiteralPath $basisPath -Raw | ConvertFrom-Json
$locationPath = Join-Path $checks 'client-retained-reuse-01-plan.json'
Require-Digest $locationPath 'ad119b77bd672583521e0449ce0454deae163b09d13a444ddd5161f959720d25'
$location = Get-Content -LiteralPath $locationPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($property in $basis.sources.psobject.Properties) {
    Require-Digest (Join-Path $projectRoot $property.Name) $property.Value
    # Preserve fixture dependencies, not execution of predecessor tests.
    $sources[$property.Name] = $property.Value
}
$portableCount = 0
foreach ($property in $location.sources.psobject.Properties) {
    if ($property.Name.StartsWith('portable/location/')) {
        $relative = 'software/v5/portable_runtime/' + $property.Name.Substring('portable/'.Length)
        if ($sources.Contains($relative)) { throw 'PORTABLE_SOURCE_COLLISION' }
        Require-Digest (Join-Path $projectRoot $relative) $property.Value.sha256
        $sources[$relative] = $property.Value.sha256
        $portableCount++
    }
}
if ($portableCount -ne 21) { throw 'PORTABLE_SOURCE_MAP' }
$additional = [ordered]@{
    'software/v5/client/serve_advertised.py' = $ExpectedServiceSha
    'software/v5/client/test_serve_advertised.py' = $ExpectedTestSha
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
$name = 'advertised-service-controls-01'
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
        '{snapshot}\software\v5\client\test_serve_advertised.py', '--output', '{output}')
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
