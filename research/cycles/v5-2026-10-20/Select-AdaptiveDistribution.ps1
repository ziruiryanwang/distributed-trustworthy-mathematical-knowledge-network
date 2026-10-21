# Stage one combined direct/located adaptive-query source map for the existing builder.
# Fresh input/selection only; never executes a build or mutates an old install.
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
$cycle = Join-Path $projectRoot 'research\cycles\v5-2026-10-20'
Require-Digest (Join-Path $cycle 'DISCOVERY-DISTRIBUTION-OUTCOME.md') '8627901370d14c44f1a710491cd65d5d0f3209bcb0fed5ff233ae76a11c21c2a'
Require-Digest (Join-Path $cycle 'ITERATIVE-DISCOVERY-OUTCOME.md') 'af49d968c470aa4a8feb5a74698d64064f99ae4f7f2d4e4eca85cba436bf8b86'
Require-Digest (Join-Path $cycle 'ADAPTIVE-LOCATED-OUTCOME.md') 'd758b5a345bfbc6eefbdfe9ccccf6671cf43e5746ac5698db9389e87af7ec634'
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$basisPath = Join-Path $checks 'distribution-discovery-01-input.json'
Require-Digest $basisPath 'e0e22f412a6d276f172603ad11ff5217ea321b5a038921af2bd7f1b4b028e20b'
$basis = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or
    $basis.base_role -cne 'mathematical-client-location-v1') { throw 'INPUT_BASIS' }
$sources = [ordered]@{}
foreach ($property in $basis.sdk_sources.psobject.Properties) {
    $sources[$property.Name] = $property.Value
}
if ($sources.Count -ne 110) { throw 'BASIS_SDK_CENSUS' }
$replacements = @(
    @('v5/client/direct_contacts.py','iterative_queries/client/direct_contacts.py',
      '88ce2581a7432421e2619c57ad0645f29f66d400f94c5d12db8c74c5f3d78e51',
      'e243a094b9fdce2adef221514923bf6753d04b8cc3ed8ae60e392c0ebd804545'),
    @('v5/client/workspace_validated.py','iterative_queries/client/workspace_validated.py',
      '4f379f478b9226fd19af1b282d1888ee8cd3430dacf6820596506985993c2a0c',
      '901ffd191131a8eb293c4f11ca8a890a5edd800d3d90156dc298ff13ac15a4be'),
    @('v5/client/semantic_reader.py','iterative_queries/client/semantic_reader.py',
      'eb925191365d9f4daf04b86804f484e4096713f7ad9dd4b0919d1ab584bbe641',
      'ec040740ad00b913c3061156d019f40887f926bf7be1ef144b116fa366c47c0b'),
    @('v5/evidence_network/transport.py','iterative_queries/evidence_network/transport.py',
      'f4734bff9bdfd2ac3fc7ae770a9bc3f0d4b6e47a41ab60fd65fa21ab50f7b880',
      '5808c0e253b203cdf38bd2069c593888ea4814d47f756871237c38eb3e0caab7')
)
foreach ($replacement in $replacements) {
    $key, $relative, $previous, $expected = $replacement
    if (-not $sources.Contains($key) -or $sources[$key].sha256 -cne $previous) {
        throw ('REPLACEMENT_BASIS_CHANGED: '+$key)
    }
    $path = Join-Path $projectRoot ('software/v5/'+$relative)
    Require-Digest $path $expected
    $sources[$key] = [ordered]@{path=$path; bytes=(Get-Item -LiteralPath $path).Length; sha256=$expected}
}
$helperKey = 'v5/client/located_queries.py'
if ($sources.Contains($helperKey)) { throw 'NEW_HELPER_ALREADY_PRESENT' }
$helper = Join-Path $projectRoot 'software/v5/located_queries/client/located_queries.py'
$helperSha = '419df8428528203858eff69da43c7e3ed7e5634d06007dc5e30ca2f33df82c4e'
Require-Digest $helper $helperSha
$sources[$helperKey] = [ordered]@{path=$helper; bytes=(Get-Item -LiteralPath $helper).Length; sha256=$helperSha}
if ($sources.Count -ne 111 -or $replacements.Count -ne 4) { throw 'SDK_DELTA_CENSUS' }
# Verify all retained and replacement sources before creating any output.
foreach ($key in $sources.Keys) {
    $row = $sources[$key]
    Require-Digest $row.path $row.sha256
    if ((Get-Item -LiteralPath $row.path).Length -ne $row.bytes) { throw ('SDK_SIZE: '+$key) }
}
$sourceKey = 'software/v5/distribution_coherent/distribution.py'
$builder = Join-Path $projectRoot 'software\v5\distribution_coherent\distribution.py'
$builderSha = '6d6f541112f5f25493a67da6a67065535d8a5e8347456004c89435cbfdc14ee6'
Require-Digest $builder $builderSha
if ($basis.distribution_source.path -cne $builder -or
    $basis.distribution_source.sha256 -cne $builderSha -or
    $basis.distribution_source.bytes -ne (Get-Item -LiteralPath $builder).Length) { throw 'UNCHANGED_BUILDER_REQUIRED' }
$basis.sdk_sources = $sources
$buildBasisPath = Join-Path $checks 'distribution-discovery-build-01-selection.json'
Require-Digest $buildBasisPath 'a50cdd5ebdbeb1c9ff497eda8a992ee119ea4f65a48accacf7f88ef9c0688a68'
$buildBasis = Get-Content -LiteralPath $buildBasisPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($buildBasis.schema -cne 'DMKN_V5_LOCAL_CHECK_V1') { throw 'BUILD_BASIS' }
$runtime = [ordered]@{}
foreach ($property in $buildBasis.runtime_pins.psobject.Properties) {
    Require-Digest $property.Name $property.Value
    $runtime[$property.Name] = $property.Value
}
$buildSources = [ordered]@{}
foreach ($property in $buildBasis.sources.psobject.Properties) {
    Require-Digest (Join-Path $projectRoot $property.Name) $property.Value
    $buildSources[$property.Name] = $property.Value
}
if ($buildSources.Count -ne 2 -or $buildSources[$sourceKey] -cne $builderSha -or
    -not $runtime.Contains($buildBasis.argv[0])) { throw 'BUILD_SOURCE_RUNTIME_BASIS' }
$name = 'distribution-adaptive-build-01'
$inputPath = Join-Path $checks 'distribution-adaptive-01-input.json'
$selectionPath = Join-Path $checks ($name+'-selection.json')
$parent = Join-Path $projectRoot 'product-local\v5-distribution-adaptive-01'
foreach ($path in @($inputPath, $selectionPath, $parent, (Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED: '+$path) }
}
New-Json $inputPath $basis
$inputSha = Digest $inputPath
$runtime[$inputPath] = $inputSha
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1'; name=$name; sources=$buildSources; runtime_pins=$runtime
    argv=@($buildBasis.argv[0], '-I', '-S', '-B',
        '{snapshot}\software\v5\distribution_coherent\distribution.py',
        'build', $inputPath, $inputSha, (Join-Path $parent 'Mathematical Commons v5'))
    limits=$buildBasis.limits
}
New-Json $selectionPath $selected
[void][IO.Directory]::CreateDirectory($parent)
[ordered]@{input=$inputPath; input_sha256=$inputSha; selection=$selectionPath;
    selection_sha256=(Digest $selectionPath); sdk_sources=$sources.Count;
    replaced=$replacements.Count; added=1; installation_parent=$parent;
    parent_created=$true; build_executed=$false} | ConvertTo-Json
