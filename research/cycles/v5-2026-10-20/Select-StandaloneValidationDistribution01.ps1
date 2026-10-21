# Prepare a three-replacement standalone-validation distribution; never execute a build here.
param(
    [Parameter(Mandatory=$true)][string]$ControlsOutcomeSha256,
    [Parameter(Mandatory=$true)][string]$ReviewedProductHashesJson
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Require-Digest([string]$path, [string]$expected) {
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or (Digest $path) -cne $expected) {
        throw ('REVIEWED_INPUT_CHANGED: '+$path)
    }
}
function New-Json([string]$path, $value) {
    $raw = [Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 64)+"`n")
    if ($raw.Length -gt 8*1024*1024) { throw 'JSON_BOUND' }
    $stream = [IO.File]::Open($path, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
    finally { $stream.Dispose() }
}
$checks = Join-Path $projectRoot 'experiments/v5-local-checks'
$cycle = Join-Path $projectRoot 'research/cycles/v5-2026-10-20'
Require-Digest (Join-Path $cycle 'STANDALONE-VALIDATION-OUTCOME.md') $ControlsOutcomeSha256
$basisPath = Join-Path $checks 'distribution-terminal-i-01-input.json'
Require-Digest $basisPath 'd3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0'
$basis = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or
    $basis.base_role -cne 'mathematical-client-location-v1') { throw 'INPUT_BASIS' }
$sources = [ordered]@{}
foreach ($property in $basis.sdk_sources.psobject.Properties) { $sources[$property.Name] = $property.Value }
if ($sources.Count -ne 114) { throw 'BASIS_SDK_CENSUS' }
$replacements = [ordered]@{
    'v5/admission/pin_phase.py' = 'software/v5/standalone_validation/admission/pin_phase.py'
    'v5/mixed_claims/receiver.py' = 'software/v5/standalone_validation/mixed_claims/receiver.py'
    'v5/mixed_claims/imports_atomic.py' = 'software/v5/standalone_validation/mixed_claims/imports_atomic.py'
}
if ($ReviewedProductHashesJson.Length -gt 16384) { throw 'REVIEWED_MAP_BOUND' }
$reviewed = $ReviewedProductHashesJson | ConvertFrom-Json
$keys = @($reviewed.psobject.Properties.Name)
if ($keys.Count -ne 3 -or @(Compare-Object $keys @($replacements.Keys) -CaseSensitive).Count -ne 0) {
    throw 'EXACT_REVIEWED_SOURCE_SET'
}
foreach ($key in $sources.Keys) {
    $row = $sources[$key]
    Require-Digest $row.path $row.sha256
    if ((Get-Item -LiteralPath $row.path).Length -ne $row.bytes) { throw ('BASIS_SDK_SIZE: '+$key) }
}
foreach ($logical in $replacements.Keys) {
    if (-not $sources.Contains($logical)) { throw ('MISSING_BASIS_SOURCE: '+$logical) }
    $path = Join-Path $projectRoot $replacements[$logical]
    Require-Digest $path $reviewed.$logical
    $sources[$logical] = [ordered]@{path=$path;bytes=(Get-Item -LiteralPath $path).Length;sha256=$reviewed.$logical}
}
if ($sources.Count -ne 114) { throw 'SDK_DELTA_CENSUS' }
$sourceKey = 'software/v5/body_location/distribution.py'
$builder = Join-Path $projectRoot $sourceKey
$builderSha = 'eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813'
if ($basis.distribution_source.path -cne $builder -or $basis.distribution_source.sha256 -cne $builderSha) { throw 'BUILDER_BASIS' }
Require-Digest $builder $builderSha
$basis.sdk_sources = $sources
$buildBasisPath = Join-Path $checks 'distribution-body-custody-build-01-selection.json'
Require-Digest $buildBasisPath 'ec52d60965bcdf885455a4aeb20e9c27fedd87fb0fc73b363c3522aca9b6e0ab'
$buildBasis = Get-Content -LiteralPath $buildBasisPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($buildBasis.schema -cne 'DMKN_V5_LOCAL_CHECK_V1' -or $buildBasis.name -cne 'distribution-body-custody-build-01') { throw 'BUILD_BASIS' }
$runtime = [ordered]@{}
foreach ($property in $buildBasis.runtime_pins.psobject.Properties) {
    Require-Digest $property.Name $property.Value
    $runtime[$property.Name] = $property.Value
}
$runnerKey = 'tools/Run-V5-Check.py'
$runnerSha = '44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
Require-Digest (Join-Path $projectRoot $runnerKey) $runnerSha
$buildSources = [ordered]@{}
$buildSources[$runnerKey] = $runnerSha
$buildSources[$sourceKey] = $builderSha
if (-not $runtime.Contains($buildBasis.argv[0])) { throw 'BUILD_RUNTIME_BASIS' }
$name = 'distribution-standalone-validation-build-01'
$inputPath = Join-Path $checks 'distribution-standalone-validation-01-input.json'
$selectionPath = Join-Path $checks ($name+'-selection.json')
$parent = Join-Path $projectRoot 'product-local/v5-distribution-standalone-validation-01'
foreach ($path in @($inputPath, $selectionPath, $parent, (Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED: '+$path) }
}
New-Json $inputPath $basis
$inputSha = Digest $inputPath
$runtime[$inputPath] = $inputSha
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$buildSources;runtime_pins=$runtime
    argv=@($buildBasis.argv[0], '-I', '-S', '-B', '{snapshot}\software\v5\body_location\distribution.py',
           'build', $inputPath, $inputSha, (Join-Path $parent 'Mathematical Commons v5'))
    # Prior identical-size packaging used294.94s wall; allow copy/I/O variance.
    # This is not a change to any mathematical client's controller/workload cap.
    limits=[ordered]@{cpu_seconds=120;wall_seconds=600;memory_mib=128;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
New-Json $selectionPath $selected
[void][IO.Directory]::CreateDirectory($parent)
[ordered]@{input=$inputPath;input_sha256=$inputSha;selection=$selectionPath;
    selection_sha256=(Digest $selectionPath);sdk_sources=$sources.Count;replaced=3;added=0;
    installation_parent=$parent;parent_created=$true;build_executed=$false} | ConvertTo-Json
