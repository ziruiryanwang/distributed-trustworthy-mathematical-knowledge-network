# Prepare one combined fingerprint/base-projection installation; never execute it.
param(
    [Parameter(Mandatory=$true)][string]$ProjectionOutcomeSha256,
    [Parameter(Mandatory=$true)][string]$ReviewedProjectionHashesJson
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
function New-Json([string]$path, $value) {
    $raw = [Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 64)+"`n")
    if ($raw.Length -gt 8*1024*1024) { throw 'JSON_BOUND' }
    $stream = [IO.File]::Open($path, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
    finally { $stream.Dispose() }
}
$cycle = Join-Path $projectRoot 'research/cycles/v5-2026-10-20'
Require-Digest (Join-Path $cycle 'INSTANTIATION-OUTCOME.md') 'dda469c4990a432be4e4ef79995f0849f1073c6e0f89b7f5fa1aa8708da782c8'
Require-Digest (Join-Path $cycle 'PROFILE-PROJECTION-OUTCOME.md') $ProjectionOutcomeSha256
$checks = Join-Path $projectRoot 'experiments/v5-local-checks'
$basisPath = Join-Path $checks 'distribution-adaptive-01-input.json'
Require-Digest $basisPath 'a74eaf51a71b5e0ec49a762fd5c7e6cce4f8fc6b107e97ae6e71fd7ec0cf1e32'
$basis = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or
    $basis.base_role -cne 'mathematical-client-location-v1') { throw 'INPUT_BASIS' }
$sources = [ordered]@{}
foreach ($property in $basis.sdk_sources.psobject.Properties) { $sources[$property.Name] = $property.Value }
if ($sources.Count -ne 111) { throw 'BASIS_SDK_CENSUS' }
$required = @('client/base_projection.py', 'client/serve_workspace.py', 'client/serve_advertised.py', 'distribution.py')
if ($ReviewedProjectionHashesJson.Length -gt 8192) { throw 'REVIEWED_MAP_BOUND' }
$reviewed = $ReviewedProjectionHashesJson | ConvertFrom-Json
$keys = @($reviewed.psobject.Properties.Name)
if ($keys.Count -ne $required.Count -or @(Compare-Object $keys $required -CaseSensitive).Count -ne 0) {
    throw 'EXACT_REVIEWED_SOURCE_SET'
}
foreach ($key in $keys) {
    Require-Digest (Join-Path $projectRoot ('software/v5/base_projection/'+$key)) $reviewed.$key
}
$replacements = @(
    @('v5/client/workspace_evidence.py', 'instantiation_discovery/client/workspace_evidence.py',
      '051e130f12f5e6a640026a0ea34f7005192c15f3be2f5c3f667a4085687f95b9',
      'bae2f9237ca4bce16d4aa68efaebf7a2a9e63bbe10018f4623f415c15ad9e8b8'),
    @('v5/discovery/authenticated_index.py', 'instantiation_discovery/discovery/authenticated_index.py',
      'de29c02489dbac486b745662caf0ec2cd8d923a394aaf2728f9625c4fed3f05e',
      '578e75a0d943b683248a94cf5834421099892fabcd46e6fadd44dc5504d341b6'),
    @('v5/discovery/discovery_store.py', 'instantiation_discovery/discovery/discovery_store.py',
      '2e7cae37ddec4dc6ec146acc7cfa89fff24e60f58dca08af900d0c3c626ed88c',
      '32df0e1d5be03b9bb0ac3c57f3df367857e608e4678c8ede262593ea9f65b884'),
    @('v5/discovery/formal_features.py', 'instantiation_discovery/discovery/formal_features.py',
      'ae78289a5a49d6eec5b36dc929799e8cbd4beafa3c28b93bef4e10d0d09762ad',
      '8822c8186ba120da9c8b72abe6d0c905eeaced5af46ef19600e463904a6d1b0c'),
    @('v5/discovery/module_export_adapter.py', 'instantiation_discovery/discovery/module_export_adapter.py',
      '336ae03bccbb5c700c36ab45f91235a23e27d15543f3eeddbb24d28c47f0f6ce',
      '508fe4449de8ffcdaccf6b06c1ceb133006cfdb91cc7a180e6e0ffd066a371ac'),
    @('v5/client/serve_workspace.py', 'base_projection/client/serve_workspace.py',
      '89723f2e8a03abcaa709560f6d991ffc5d2bb349ef6cb662aadad7589a73936c', $reviewed.'client/serve_workspace.py'),
    @('v5/client/serve_advertised.py', 'base_projection/client/serve_advertised.py',
      '80d6c0746eca23398cfe735af5d8de1076eb3725439414cce68de743c518a7ed', $reviewed.'client/serve_advertised.py')
)
foreach ($row in $replacements) {
    $key, $relative, $old, $sha = $row
    if (-not $sources.Contains($key) -or $sources[$key].sha256 -cne $old) { throw ('REPLACEMENT_BASIS: '+$key) }
    $path = Join-Path $projectRoot ('software/v5/'+$relative)
    Require-Digest $path $sha
    $sources[$key] = [ordered]@{path=$path; bytes=(Get-Item -LiteralPath $path).Length; sha256=$sha}
}
$additions = @(
    @('v5/discovery/conclusion_fingerprint.py', 'instantiation_discovery/discovery/conclusion_fingerprint.py',
      'ac32cf53a4bf91bb012b4ba4f6701103580a51718e8c898156d5fef0b26f1bb3'),
    @('v5/client/base_projection.py', 'base_projection/client/base_projection.py', $reviewed.'client/base_projection.py')
)
foreach ($row in $additions) {
    $key, $relative, $sha = $row
    if ($sources.Contains($key)) { throw ('NEW_HELPER_ALREADY_PRESENT: '+$key) }
    $path = Join-Path $projectRoot ('software/v5/'+$relative)
    Require-Digest $path $sha
    $sources[$key] = [ordered]@{path=$path; bytes=(Get-Item -LiteralPath $path).Length; sha256=$sha}
}
if ($sources.Count -ne 113 -or $replacements.Count -ne 7 -or $additions.Count -ne 2) { throw 'SDK_DELTA_CENSUS' }
foreach ($key in $sources.Keys) {
    $row = $sources[$key]
    Require-Digest $row.path $row.sha256
    if ((Get-Item -LiteralPath $row.path).Length -ne $row.bytes) { throw ('SDK_SIZE: '+$key) }
}
$oldBuilder = Join-Path $projectRoot 'software/v5/distribution_coherent/distribution.py'
if ($basis.distribution_source.path -cne $oldBuilder -or
    $basis.distribution_source.sha256 -cne '6d6f541112f5f25493a67da6a67065535d8a5e8347456004c89435cbfdc14ee6') {
    throw 'BUILDER_BASIS'
}
$sourceKey = 'software/v5/base_projection/distribution.py'
$builder = Join-Path $projectRoot $sourceKey
$builderSha = $reviewed.'distribution.py'
$basis.distribution_source = [ordered]@{path=$builder; bytes=(Get-Item -LiteralPath $builder).Length; sha256=$builderSha}
$basis.sdk_sources = $sources
$buildBasisPath = Join-Path $checks 'distribution-adaptive-build-01-selection.json'
Require-Digest $buildBasisPath '7ec39f9f533582768617e902ab8bcd0875ce734a3bd795f0fa54fd70abbfd4fb'
$buildBasis = Get-Content -LiteralPath $buildBasisPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($buildBasis.schema -cne 'DMKN_V5_LOCAL_CHECK_V1') { throw 'BUILD_BASIS' }
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
$name = 'distribution-projection-build-01'
$inputPath = Join-Path $checks 'distribution-projection-01-input.json'
$selectionPath = Join-Path $checks ($name+'-selection.json')
$parent = Join-Path $projectRoot 'product-local/v5-distribution-projection-01'
foreach ($path in @($inputPath, $selectionPath, $parent, (Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED: '+$path) }
}
New-Json $inputPath $basis
$inputSha = Digest $inputPath
$runtime[$inputPath] = $inputSha
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1'; name=$name; sources=$buildSources; runtime_pins=$runtime
    argv=@($buildBasis.argv[0], '-I', '-S', '-B', '{snapshot}\software\v5\base_projection\distribution.py',
           'build', $inputPath, $inputSha, (Join-Path $parent 'Mathematical Commons v5'))
    limits=$buildBasis.limits
}
New-Json $selectionPath $selected
[void][IO.Directory]::CreateDirectory($parent)
[ordered]@{input=$inputPath; input_sha256=$inputSha; selection=$selectionPath;
    selection_sha256=(Digest $selectionPath); sdk_sources=$sources.Count;
    replaced=7; added=2; installation_parent=$parent; parent_created=$true; build_executed=$false} | ConvertTo-Json
