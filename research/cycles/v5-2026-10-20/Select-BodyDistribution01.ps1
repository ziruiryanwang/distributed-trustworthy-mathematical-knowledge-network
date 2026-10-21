# Stage the exact reviewed custody successor; never execute a build here.
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
Require-Digest (Join-Path $cycle 'EXACT-CUSTODY-OUTCOME.md') $ControlsOutcomeSha256
$basisPath = Join-Path $checks 'distribution-projection-01-input.json'
Require-Digest $basisPath 'ad2c15a27a51f749104ac09f9cafee210a108fb0bf46bafad8b2a9542f86d38f'
$basis = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or
    $basis.base_role -cne 'mathematical-client-location-v1') { throw 'INPUT_BASIS' }
$sources = [ordered]@{}
foreach ($property in $basis.sdk_sources.psobject.Properties) { $sources[$property.Name] = $property.Value }
if ($sources.Count -ne 113) { throw 'BASIS_SDK_CENSUS' }
$replaced = @(
    'portable/location/protocol.py', 'portable/location/protocol.mjs',
    'portable/location/intent.mjs', 'portable/location/maintained_roles.mjs',
    'portable/location/ipc_wire.mjs', 'portable/location/node_entry_services.mjs',
    'portable/location/controller_services.py',
    'client/workspace_evidence.py', 'client/semantic_reader.py',
    'client/serve_advertised.py', 'transport/acquisition_resilience.py'
)
$required = @($replaced) + @('client/body_custody.py', 'distribution.py')
if ($ReviewedProductHashesJson.Length -gt 16384) { throw 'REVIEWED_MAP_BOUND' }
$reviewed = $ReviewedProductHashesJson | ConvertFrom-Json
$keys = @($reviewed.psobject.Properties.Name)
if ($keys.Count -ne 13 -or @(Compare-Object $keys $required -CaseSensitive).Count -ne 0) {
    throw 'EXACT_REVIEWED_SOURCE_SET'
}
foreach ($relative in $required) {
    Require-Digest (Join-Path $projectRoot ('software/v5/body_location/'+$relative)) $reviewed.$relative
}
foreach ($relative in @($replaced)+@('client/body_custody.py')) {
    $logical = if ($relative.StartsWith('portable/')) { $relative } else { 'v5/'+$relative }
    if ($relative -ceq 'client/body_custody.py') {
        if ($sources.Contains($logical)) { throw 'NEW_HELPER_ALREADY_PRESENT' }
    } elseif (-not $sources.Contains($logical)) { throw ('MISSING_BASIS_SOURCE: '+$logical) }
    $path = Join-Path $projectRoot ('software/v5/body_location/'+$relative)
    $sources[$logical] = [ordered]@{path=$path;bytes=(Get-Item -LiteralPath $path).Length;sha256=$reviewed.$relative}
}
if ($sources.Count -ne 114 -or $replaced.Count -ne 11) { throw 'SDK_DELTA_CENSUS' }
foreach ($key in $sources.Keys) {
    $row = $sources[$key]
    Require-Digest $row.path $row.sha256
    if ((Get-Item -LiteralPath $row.path).Length -ne $row.bytes) { throw ('SDK_SIZE: '+$key) }
}
$oldBuilder = Join-Path $projectRoot 'software/v5/base_projection/distribution.py'
if ($basis.distribution_source.path -cne $oldBuilder -or
    $basis.distribution_source.sha256 -cne '0db784331ba5ac8966c9b4411385fd2fc734b384a2a5ed3729b74f4bb6bff0e3') {
    throw 'BUILDER_BASIS'
}
$sourceKey = 'software/v5/body_location/distribution.py'
$builder = Join-Path $projectRoot $sourceKey
$builderSha = $reviewed.'distribution.py'
$basis.distribution_source = [ordered]@{path=$builder;bytes=(Get-Item -LiteralPath $builder).Length;sha256=$builderSha}
$basis.sdk_sources = $sources
$buildBasisPath = Join-Path $checks 'distribution-projection-build-01-selection.json'
Require-Digest $buildBasisPath '1e558685080a904464a26789a68283a4af07c823632b712da39e861cd1fa7286'
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
$name = 'distribution-body-custody-build-01'
$inputPath = Join-Path $checks 'distribution-body-custody-01-input.json'
$selectionPath = Join-Path $checks ($name+'-selection.json')
$parent = Join-Path $projectRoot 'product-local/v5-distribution-body-custody-01'
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
    limits=$buildBasis.limits
}
New-Json $selectionPath $selected
[void][IO.Directory]::CreateDirectory($parent)
[ordered]@{input=$inputPath;input_sha256=$inputSha;selection=$selectionPath;
    selection_sha256=(Digest $selectionPath);sdk_sources=$sources.Count;replaced=11;added=1;
    installation_parent=$parent;parent_created=$true;build_executed=$false} | ConvertTo-Json
