# Prepare one bounded native comparison; does not invoke Python/native checks.
param(
    [Parameter(Mandatory=$true)][string]$ExpectedBuildResultSha,
    [Parameter(Mandatory=$true)][string]$ExpectedBinarySha,
    [Parameter(Mandatory=$true)][string]$ExpectedAdapterSha,
    [Parameter(Mandatory=$true)][ValidateRange(1,64)][int]$ExpectedTests
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
$build = Join-Path $checks 'restricted-composition-build-02'
$resultPath = Join-Path $build 'RESULT.json'
Require-Digest $resultPath $ExpectedBuildResultSha
$result = Get-Content -Encoding UTF8 -LiteralPath $resultPath -Raw | ConvertFrom-Json
if ($result.status -cne 'PASS_RC_THREE_COMPILES_ONLY' -or
    (Test-Path -LiteralPath (Join-Path $build 'FINALIZATION-FAILED.json'))) {
    throw 'SUCCESSFUL_EXACT_BUILD_REQUIRED'
}
$binary = Join-Path $build 'restricted_controls.exe'
Require-Digest $binary $ExpectedBinarySha
if ($result.outputs.'restricted_controls.exe'.sha256 -cne $ExpectedBinarySha -or
    $result.outputs.'restricted_controls.exe'.bytes -ne (Get-Item -LiteralPath $binary).Length) {
    throw 'CONTROL_BINARY_BUILD_BINDING'
}
$attemptPath = Join-Path $checks 'restricted-composition-build-02-attempt.json'
$attempt = Get-Content -Encoding UTF8 -LiteralPath $attemptPath -Raw | ConvertFrom-Json
if ($attempt.status -cne $result.status -or $attempt.result_sha256 -cne $ExpectedBuildResultSha) {
    throw 'BUILD_FINALIZATION_BINDING'
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
$runtime[$attemptPath] = Digest $attemptPath
$fixtures = [ordered]@{
    'experiments/v5-local-checks/module-base-snapshot-03/evidence/base.expected-journal' = '22fe722c57894cb192a6700954fb045a708431a1470e274440c7d60a5767b682'
    'experiments/v5-local-checks/receipt-prepare-01/prepared/base/bundle.json' = '09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926'
    'product-local/v5-distribution-terminal-i-01/Mathematical Commons v5/assets/foundation/foundation.json' = '736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c'
}
foreach ($relative in $fixtures.Keys) {
    $path = Join-Path $projectRoot $relative
    Require-Digest $path $fixtures[$relative]
    $runtime[$path] = $fixtures[$relative]
}
$sources = [ordered]@{
    'tools/Run-V5-Check.py' = '44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
    'software/v5/restricted_composition/run_controls.py' = $ExpectedAdapterSha
}
$buildSelectionPath = Join-Path $checks 'restricted-composition-build-02-selection.json'
Require-Digest $buildSelectionPath $result.selection_sha256
$buildSelection = Get-Content -Encoding UTF8 -LiteralPath $buildSelectionPath -Raw | ConvertFrom-Json
if ($buildSelection.schema -cne 'DMKN_V5_RC_NATIVE_BUILD_V1' -or
    $buildSelection.name -cne 'restricted-composition-build-02') { throw 'EXACT_BUILD_SELECTION' }
$runtime[$buildSelectionPath] = $result.selection_sha256
$fixtureRelative = 'software/v5/restricted_composition/fixtures.py'
$sources[$fixtureRelative] = $buildSelection.sources.$fixtureRelative.sha256
foreach ($relative in @('software/v5/modules/__init__.py','software/v5/modules/codec.py',
    'software/v5/modules/model.py','software/v5/modules/native_rows.py',
    'software/v5/modules/receipt/__init__.py','software/v5/modules/receipt/witness.py')) {
    $sources[$relative] = Digest (Join-Path $projectRoot $relative)
}
foreach ($relative in $sources.Keys) {
    Require-Digest (Join-Path $projectRoot $relative) $sources[$relative]
}
$python = $basis.argv[0]
if (-not $runtime.Contains($python) -or $sources.Count -ne 9) { throw 'EXACT_RUNTIME_SOURCE_CENSUS' }
$name = 'restricted-composition-controls-01'
$path = Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $path) -or (Test-Path -LiteralPath (Join-Path $checks $name))) {
    throw 'FRESH_CONTROLS_REQUIRED'
}
$selection = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1'; name=$name; sources=$sources; runtime_pins=$runtime
    argv=@($python,'-I','-S','-B',
        '{snapshot}\software\v5\restricted_composition\run_controls.py',
        '--binary',$binary,'--binary-sha',$ExpectedBinarySha,
        '--output','{output}\evidence','--expected-tests',[string]$ExpectedTests)
    limits=[ordered]@{
        cpu_seconds=45; wall_seconds=90; memory_mib=512; active_processes=3
        stdout_bytes=1048576; stderr_bytes=1048576
    }
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 16)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_SIZE' }
$stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
[ordered]@{path=$path;sha256=(Digest $path);runtime_pins=$runtime.Count;source_count=$sources.Count;executed=$false} | ConvertTo-Json
