# Select one fresh native-only changed-boundary check; no test executes here.
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
$build = Join-Path $checks 'restricted-support-build-01'
$resultPath = Join-Path $build 'RESULT.json'
Require-Digest $resultPath $ExpectedBuildResultSha
$result = Get-Content -Encoding UTF8 -LiteralPath $resultPath -Raw | ConvertFrom-Json
if ($result.schema -cne 'DMKN_V5_RC_SUPPORT_BUILD_RESULT_V1' -or
    $result.status -cne 'PASS_RC_SUPPORT_TWO_COMPILES_ONLY' -or
    $result.compiler_calls -ne 2 -or
    (Test-Path -LiteralPath (Join-Path $build 'FINALIZATION-FAILED.json'))) {
    throw 'SUCCESSFUL_TWO_COMPILE_BUILD_REQUIRED'
}
$binary = Join-Path $build 'restricted_support_controls.exe'
Require-Digest $binary $ExpectedBinarySha
if ($result.outputs.'restricted_support_controls.exe'.sha256 -cne $ExpectedBinarySha -or
    $result.outputs.'restricted_support_controls.exe'.bytes -ne (Get-Item -LiteralPath $binary).Length) {
    throw 'BINARY_BUILD_BINDING'
}
$attemptPath = Join-Path $checks 'restricted-support-build-01-attempt.json'
$attempt = Get-Content -Encoding UTF8 -LiteralPath $attemptPath -Raw | ConvertFrom-Json
if ($attempt.status -cne $result.status -or $attempt.result_sha256 -cne $ExpectedBuildResultSha) {
    throw 'BUILD_FINALIZATION_BINDING'
}
$buildSelectionPath = Join-Path $checks 'restricted-support-build-01-selection.json'
Require-Digest $buildSelectionPath $result.selection_sha256
$buildSelection = Get-Content -Encoding UTF8 -LiteralPath $buildSelectionPath -Raw | ConvertFrom-Json
$sourceMapPath = Join-Path $build 'source-map.json'
$sourceMap = Get-Content -Encoding UTF8 -LiteralPath $sourceMapPath -Raw | ConvertFrom-Json
if ($buildSelection.schema -cne 'DMKN_V5_RC_SUPPORT_BUILD_V1' -or
    $buildSelection.name -cne 'restricted-support-build-01' -or
    @($buildSelection.sources.psobject.Properties).Count -ne 8 -or
    @($sourceMap.psobject.Properties).Count -ne 8) { throw 'EXACT_BUILD_SOURCE_MAP' }
$sources = [ordered]@{
    'tools/Run-V5-Check.py' = '44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
    'software/v5/restricted_support/run_controls.py' = $ExpectedAdapterSha
}
foreach ($property in $buildSelection.sources.psobject.Properties) {
    $pin = $property.Value
    $mapped = $sourceMap.($property.Name)
    if ($null -eq $mapped -or $mapped.sha256 -cne $pin.sha256 -or
        $mapped.bytes -ne $pin.bytes) { throw 'EXACT_SOURCE_MAP_BINDING' }
    $path = Join-Path $projectRoot $property.Name
    Require-Digest $path $pin.sha256
    if ((Get-Item -LiteralPath $path).Length -ne $pin.bytes -or
        $sources.Contains($property.Name)) { throw 'SOURCE_LENGTH_OR_DUPLICATE' }
    $sources[$property.Name] = $pin.sha256
}
foreach ($relative in $sources.Keys) {
    Require-Digest (Join-Path $projectRoot $relative) $sources[$relative]
}
$basisPath = Join-Path $checks 'advertised-service-controls-01-selection.json'
Require-Digest $basisPath 'e450cbe5590f28e5b857d50eb3c48fa71488f1b1742070e59f7f62946010c3fc'
$basis = Get-Content -Encoding UTF8 -LiteralPath $basisPath -Raw | ConvertFrom-Json
$runtime = [ordered]@{}
$pythonRoot = Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\receiver\runtime\python\'
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    if ($property.Name.StartsWith($pythonRoot, [StringComparison]::Ordinal)) {
        Require-Digest $property.Name $property.Value
        $runtime[$property.Name] = $property.Value
    }
}
$runtime[$resultPath] = $ExpectedBuildResultSha
$runtime[$binary] = $ExpectedBinarySha
$runtime[$attemptPath] = Digest $attemptPath
$runtime[$buildSelectionPath] = $result.selection_sha256
$runtime[$sourceMapPath] = Digest $sourceMapPath
$fixture = Join-Path $checks 'restricted-composition-controls-01\evidence\fixture.json'
$fixtureSha = '019219ca4548dafbdaa814c209a4ec087229091750db3f3cf48fcc155269f40a'
Require-Digest $fixture $fixtureSha
if ((Get-Item -LiteralPath $fixture).Length -ne 84727) { throw 'EXACT_RETAINED_FIXTURE' }
$runtime[$fixture] = $fixtureSha
$python = $basis.argv[0]
if (-not $runtime.Contains($python) -or $sources.Count -ne 10) { throw 'RUNTIME_SOURCE_CENSUS' }
$name = 'restricted-support-controls-01'
$path = Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $path) -or (Test-Path -LiteralPath (Join-Path $checks $name))) {
    throw 'FRESH_CONTROLS_REQUIRED'
}
$selection = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1'; name=$name; sources=$sources; runtime_pins=$runtime
    argv=@($python,'-I','-S','-B','{snapshot}\software\v5\restricted_support\run_controls.py')
    limits=[ordered]@{
        cpu_seconds=30; wall_seconds=60; memory_mib=512; active_processes=3
        stdout_bytes=1048576; stderr_bytes=1048576
    }
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 16)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_SIZE' }
$stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
[ordered]@{path=$path;sha256=(Digest $path);runtime_pins=$runtime.Count;source_count=$sources.Count;executed=$false} | ConvertTo-Json
