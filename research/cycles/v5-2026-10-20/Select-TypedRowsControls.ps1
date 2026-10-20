# Prepare one exact control invocation; never execute it from this selector.
param(
    [Parameter(Mandatory=$true)][string]$ExpectedBuildResultSha,
    [Parameter(Mandatory=$true)][string]$ExpectedBinarySha,
    [Parameter(Mandatory=$true)][string]$ExpectedAdapterSha
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
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$build = Join-Path $checks 'typed-rows-build-02'
$resultPath = Join-Path $build 'RESULT.json'
Require-Digest $resultPath $ExpectedBuildResultSha
$result = Get-Content -Encoding UTF8 -LiteralPath $resultPath -Raw | ConvertFrom-Json
if ($result.status -cne 'PASS_TYPED_ROWS_FOUR_COMPILES_ONLY' -or
    $result.selection_sha256 -cne '0eaf0bd562b1d501412e415394d4ce33acb2c20c44df028bca64bbdfa24846a3' -or
    (Test-Path -LiteralPath (Join-Path $build 'FINALIZATION-FAILED.json'))) {
    throw 'SUCCESSFUL_EXACT_BUILD_REQUIRED'
}
$binary = Join-Path $build 'typed_rows_tests.exe'
Require-Digest $binary $ExpectedBinarySha
if ($result.outputs.'typed_rows_tests.exe'.sha256 -cne $ExpectedBinarySha -or
    $result.outputs.'typed_rows_tests.exe'.bytes -ne (Get-Item -LiteralPath $binary).Length) {
    throw 'TEST_BINARY_BUILD_BINDING'
}
$basisPath = Join-Path $checks 'advertised-service-controls-01-selection.json'
Require-Digest $basisPath 'e450cbe5590f28e5b857d50eb3c48fa71488f1b1742070e59f7f62946010c3fc'
$basis = Get-Content -Encoding UTF8 -LiteralPath $basisPath -Raw | ConvertFrom-Json
$runtime = [ordered]@{}
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    Require-Digest $property.Name $property.Value
    $runtime[$property.Name] = $property.Value
}
$runtime[$resultPath] = $ExpectedBuildResultSha
$runtime[$binary] = $ExpectedBinarySha
$fixtures = [ordered]@{
    'delta-reprepare-01/evidence/delta-packet.json' = '54c7dac7f83a9a06c2b23b17a77be20364c1b90e4cd3b1db58b69c62fda2dcf1'
    'aggregate-claims-controls-02/evidence/actual-two-delta.bin' = '7e21d092206b08a9a71231045b8152df4179ee6575cdc5e3afc704ef03c0be58'
    'aggregate-claims-controls-02/evidence/actual-two-delta/stdout.txt' = '01d7c9cc45a16f520980e80672f90c0a97a69e31e344f748910df5abb24ffd0b'
}
foreach ($relative in $fixtures.Keys) {
    $path = Join-Path $checks $relative
    Require-Digest $path $fixtures[$relative]
    $runtime[$path] = $fixtures[$relative]
}
$sources = [ordered]@{
    'tools/Run-V5-Check.py' = '44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
    'software/v5/typed_rows/run_controls.py' = $ExpectedAdapterSha
}
foreach ($relative in $sources.Keys) {
    Require-Digest (Join-Path $projectRoot $relative) $sources[$relative]
}
$python = $basis.argv[0]
if (-not $runtime.Contains($python)) { throw 'PINNED_OUTER_PYTHON' }
$name = 'typed-rows-controls-01'
$path = Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $path) -or (Test-Path -LiteralPath (Join-Path $checks $name))) {
    throw 'FRESH_CONTROLS_REQUIRED'
}
$selection = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1'; name=$name; sources=$sources; runtime_pins=$runtime
    argv=@($python,'-I','-S','-B',
        '{snapshot}\software\v5\typed_rows\run_controls.py',
        '--binary',$binary,'--binary-sha',$ExpectedBinarySha,
        '--output','{output}\evidence','--expected-tests','8')
    limits=[ordered]@{
        cpu_seconds=40; wall_seconds=90; memory_mib=512; active_processes=3
        stdout_bytes=1048576; stderr_bytes=1048576
    }
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 16)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_SIZE' }
$stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
[ordered]@{path=$path;sha256=(Digest $path);runtime_pins=$runtime.Count;executed=$false} | ConvertTo-Json
