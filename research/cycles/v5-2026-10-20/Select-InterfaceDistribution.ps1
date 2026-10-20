# Exact source-map consolidation and finite build plan; does not execute build.
param([Parameter(Mandatory=$true)][string]$ReviewedBuilderSha)
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
function New-Json([string]$path, $value) {
    $raw = [Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 64)+"`n")
    if ($raw.Length -gt 8*1024*1024) { throw 'JSON_BOUND' }
    $stream = [IO.File]::Open($path, [IO.FileMode]::CreateNew,
        [IO.FileAccess]::Write, [IO.FileShare]::None)
    try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
    finally { $stream.Dispose() }
}
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$inputBasisPath = Join-Path $checks 'distribution-connected-01-input.json'
Require-Digest $inputBasisPath '557269158f76933177eae962cb97c2862a8512709dbee9842051649552573309'
$inputBasis = Get-Content -LiteralPath $inputBasisPath -Raw | ConvertFrom-Json
if ($inputBasis.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or
    $inputBasis.base_role -cne 'mathematical-client-location-v1') { throw 'INPUT_BASIS' }
$actualPath = Join-Path $checks 'interface-view-actual-01-inputs\plan.json'
Require-Digest $actualPath '99492605f7b1c868f4661f614db7f764a81fd0c4a4a391d882855ad6adf1aa96'
$actual = Get-Content -LiteralPath $actualPath -Raw | ConvertFrom-Json
$reviewPath = Join-Path $checks 'interface-view-actual-01-inputs\SELECTION.json'
Require-Digest $reviewPath '9270bc7bb23a7b651592a741e58e051e0325a33f396b771cbec4c360ac85b8be'
$review = Get-Content -LiteralPath $reviewPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($property in $inputBasis.sdk_sources.psobject.Properties) {
    $sources[$property.Name] = $property.Value
}
if ($sources.Count -ne 106) { throw 'BASIS_SDK_CENSUS' }
$overlays = [ordered]@{
    'v5/mixed_claims/imports_atomic.py'='imports_atomic.py'
    'v5/mixed_claims/interface_projection.py'='projection.py'
    'v5/mixed_claims/authoring_atomic.py'='authoring_atomic.py'
    'v5/client/workspace_evidence.py'='workspace_evidence.py'
    'v5/client/workspace_staged.py'='workspace_staged.py'
    'v5/client/semantic_reader.py'='semantic_reader.py'
    'v5/transport/semantic_staging.py'='semantic_staging.py'
    'v5/transport/declaration_resilience.py'='../transport/declaration_resilience.py'
}
foreach ($key in $overlays.Keys) {
    $relative = 'software/v5/interface_views/'+$overlays[$key]
    $expected = $review.reviewed_sources.$relative
    if ($key -ceq 'v5/transport/declaration_resilience.py') {
        $relative = 'software/v5/transport/declaration_resilience.py'
        $expected = 'd8ee2dafc3237726501a1180ebb6b1be641ea9e5d8092c8ee841e1095da3e06c'
    }
    $path = Join-Path $projectRoot $relative
    Require-Digest $path $expected
    $sources[$key] = [ordered]@{path=$path; bytes=(Get-Item -LiteralPath $path).Length; sha256=$expected}
}
if ($sources.Count -ne 108) { throw 'NEW_SDK_CENSUS' }
# Every selected SDK byte must be the same as the actually exercised SDK map.
$actualSdk = @($actual.sources.psobject.Properties | Where-Object { $_.Name -cmatch '^(v5|portable)/' })
if ($actualSdk.Count -ne $sources.Count) { throw 'ACTUAL_SDK_CENSUS' }
foreach ($property in $actualSdk) {
    $row = $sources[$property.Name]
    if ($null -eq $row -or $row.bytes -ne $property.Value.bytes -or
        $row.sha256 -cne $property.Value.sha256) { throw ('ACTUAL_SDK_DIFFERENCE: '+$property.Name) }
}
$sourceKey = 'software/v5/distribution_interfaces/distribution.py'
$builder = Join-Path $projectRoot $sourceKey
Require-Digest $builder $ReviewedBuilderSha
$inputBasis.sdk_sources = $sources
$inputBasis.distribution_source = [ordered]@{path=$builder; bytes=(Get-Item -LiteralPath $builder).Length; sha256=$ReviewedBuilderSha}
$basisPath = Join-Path $checks 'distribution-connected-build-01-selection.json'
Require-Digest $basisPath '9484fda5bc1b6a2648d4d06b73be443ca361adee8f3d73210655efc07cffdab1'
$basis = Get-Content -LiteralPath $basisPath -Raw | ConvertFrom-Json
$runtime = [ordered]@{}
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    Require-Digest $property.Name $property.Value
    $runtime[$property.Name] = $property.Value
}
$buildSources = [ordered]@{'tools/Run-V5-Check.py'='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'}
$buildSources[$sourceKey] = $ReviewedBuilderSha
foreach ($key in $buildSources.Keys) { Require-Digest (Join-Path $projectRoot $key) $buildSources[$key] }
$name = 'distribution-interface-build-01'
$inputPath = Join-Path $checks 'distribution-interface-01-input.json'
$selectionPath = Join-Path $checks ($name+'-selection.json')
$parent = Join-Path $projectRoot 'product-local\v5-distribution-interface-01'
foreach ($path in @($inputPath, $selectionPath, $parent, (Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED: '+$path) }
}
New-Json $inputPath $inputBasis
$inputSha = Digest $inputPath
$runtime[$inputPath] = $inputSha
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1'; name=$name; sources=$buildSources; runtime_pins=$runtime
    argv=@($basis.argv[0], '-I', '-S', '-B',
        '{snapshot}\software\v5\distribution_interfaces\distribution.py',
        'build', $inputPath, $inputSha, (Join-Path $parent 'Mathematical Commons v5'))
    limits=[ordered]@{cpu_seconds=120; wall_seconds=300; memory_mib=128; active_processes=2; stdout_bytes=1048576; stderr_bytes=1048576}
}
New-Json $selectionPath $selected
# Builder requires an existing parent, but creates the installation itself.
# This exact fixed fresh parent was checked above; never alter an old release.
[void][IO.Directory]::CreateDirectory($parent)
[ordered]@{input=$inputPath; input_sha256=$inputSha; selection=$selectionPath;
    selection_sha256=(Digest $selectionPath); sdk_sources=$sources.Count;
    installation_parent=$parent; parent_created=$true; build_executed=$false} | ConvertTo-Json
