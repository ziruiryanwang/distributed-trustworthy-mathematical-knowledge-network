# Prepare the changed continuation controls only; no test execution.
param(
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
$basisPath = Join-Path $checks 'acquisition-resilience-controls-01-selection.json'
Require-Digest $basisPath '5eff81de1ed686cf3db2d6d901073f7f7070c3497762d22aef998736c4ddc4e4'
$basis = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($property in $basis.sources.psobject.Properties) {
    Require-Digest (Join-Path $projectRoot $property.Name) $property.Value
    # Existing fixture/support modules may be imported, not their prior suites.
    $sources[$property.Name] = $property.Value
}
$additional = [ordered]@{
    'software/v5/examples/contribution.py' = $ExpectedHelperSha
    'software/v5/examples/test_contribution.py' = $ExpectedTestSha
}
foreach ($property in $additional.GetEnumerator()) {
    if ($sources.Contains($property.Key)) { throw 'NEW_SOURCE_COLLISION' }
    Require-Digest (Join-Path $projectRoot $property.Key) $property.Value
    $sources[$property.Key] = $property.Value
}
if ($sources['tools/Run-V5-Check.py'] -cne '44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651') {
    throw 'RUNNER_IDENTITY'
}
$runtime = [ordered]@{}
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    Require-Digest $property.Name $property.Value
    $runtime[$property.Name] = $property.Value
}
$name = 'context-contribution-controls-01'
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
        '{snapshot}\software\v5\examples\test_contribution.py', '--output', '{output}')
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
