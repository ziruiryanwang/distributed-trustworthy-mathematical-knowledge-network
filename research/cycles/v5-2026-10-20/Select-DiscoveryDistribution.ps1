# Prepare the unchanged coherent builder with the adopted numeral/pattern sources.
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
Require-Digest (Join-Path $cycle 'NAT-LITERAL-OUTCOME.md') '7582a3010927c9848c14ec26cfd4eeaa94ae99f6556166426276d4eb64095d14'
Require-Digest (Join-Path $cycle 'TYPE-PATTERN-OUTCOME.md') '9963383eb940b17916067482d83fbfab5797b0cc5751c5abcbd37dd995d5c047'
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$basisPath = Join-Path $checks 'distribution-coherent-01-input.json'
Require-Digest $basisPath '1903bb44b6176dae5d43142f11cd90ddde6d494d51d5b5c1c377f3ebf5182528'
$basis = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or
    $basis.base_role -cne 'mathematical-client-location-v1') { throw 'INPUT_BASIS' }
$sources = [ordered]@{}
foreach ($property in $basis.sdk_sources.psobject.Properties) {
    $sources[$property.Name] = $property.Value
}
if ($sources.Count -ne 109) { throw 'BASIS_SDK_CENSUS' }
$replacements = @(
    @('v5/modules/source_rows.py','nat_literals/source_rows.py','b9525df05f265a78dfe89b205e5531eeba5d7128185a9f065aca9df2f2d93e85'),
    @('v5/discovery/formal_features.py','type_pattern/discovery/formal_features.py','ae78289a5a49d6eec5b36dc929799e8cbd4beafa3c28b93bef4e10d0d09762ad'),
    @('v5/discovery/authenticated_index.py','type_pattern/discovery/authenticated_index.py','de29c02489dbac486b745662caf0ec2cd8d923a394aaf2728f9625c4fed3f05e'),
    @('v5/discovery/discovery_store.py','type_pattern/discovery/discovery_store.py','2e7cae37ddec4dc6ec146acc7cfa89fff24e60f58dca08af900d0c3c626ed88c'),
    @('v5/discovery/module_export_adapter.py','type_pattern/discovery/module_export_adapter.py','336ae03bccbb5c700c36ab45f91235a23e27d15543f3eeddbb24d28c47f0f6ce'),
    @('v5/client/workspace_evidence.py','type_pattern/client/workspace_evidence.py','051e130f12f5e6a640026a0ea34f7005192c15f3be2f5c3f667a4085687f95b9')
)
foreach ($replacement in $replacements) {
    $key, $relative, $expected = $replacement
    if (-not $sources.Contains($key)) { throw ('REPLACEMENT_KEY_MISSING: '+$key) }
    $path = Join-Path $projectRoot ('software/v5/'+$relative)
    Require-Digest $path $expected
    $sources[$key] = [ordered]@{path=$path; bytes=(Get-Item -LiteralPath $path).Length; sha256=$expected}
}
$helperKey = 'v5/discovery/type_pattern.py'
if ($sources.Contains($helperKey)) { throw 'NEW_HELPER_ALREADY_PRESENT' }
$helper = Join-Path $projectRoot 'software/v5/type_pattern/discovery/type_pattern.py'
$helperSha = 'b75277b55cdb25a22fbdc517bdc0bdf1173ced7c22c895fdc313a86f23857582'
Require-Digest $helper $helperSha
$sources[$helperKey] = [ordered]@{path=$helper; bytes=(Get-Item -LiteralPath $helper).Length; sha256=$helperSha}
if ($sources.Count -ne 110 -or $replacements.Count -ne 6) { throw 'SDK_DELTA_CENSUS' }
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
$buildBasisPath = Join-Path $checks 'distribution-coherent-build-01-selection.json'
Require-Digest $buildBasisPath '3954472c55b5bfdac93a029d96cce80e06c71ee0db9e0625bfb80af0e43a238f'
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
$name = 'distribution-discovery-build-01'
$inputPath = Join-Path $checks 'distribution-discovery-01-input.json'
$selectionPath = Join-Path $checks ($name+'-selection.json')
$parent = Join-Path $projectRoot 'product-local\v5-distribution-discovery-01'
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
