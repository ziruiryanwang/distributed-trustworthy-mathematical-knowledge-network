# Prepare the demonstrated five-replacement/seven-addition union; never build here.
param([Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$CompositionReviewSha256)
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
Require-Digest (Join-Path $cycle 'CONSOLIDATED-REVIEW.md') $CompositionReviewSha256
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
    'v5/mixed_claims/imports_atomic.py' = 'software/v5/continuing_context/mixed_claims/imports_atomic.py'
    'v5/mixed_claims/receiver.py' = 'software/v5/incremental_native/mixed_claims/receiver.py'
    'v5/client/workspace_atomic.py' = 'software/v5/continuing_context/client/workspace_atomic.py'
    'v5/discovery/discovery_store.py' = 'software/v5/selective_placement/discovery/discovery_store.py'
    'v5/placement/__init__.py' = 'software/v5/selective_placement/placement/__init__.py'
    'v5/placement/codec.py' = 'software/v5/selective_placement/placement/codec.py'
    'v5/placement/ledger.py' = 'software/v5/selective_placement/placement/ledger.py'
    'v5/placement/controller.py' = 'software/v5/selective_placement/placement/controller.py'
    'v5/placement/network.py' = 'software/v5/placement_network/placement/network.py'
    'v5/placement/advertisement.py' = 'software/v5/retained_advertisement/placement/advertisement.py'
    'v5/client/serve_placement.py' = 'software/v5/retained_advertisement/client/serve_placement.py'
}
$reviewed = [ordered]@{
    'v5/admission/pin_phase.py' = 'ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881'
    'v5/mixed_claims/imports_atomic.py' = '45b082863525fb08c1e8925e998113b55deff4b92482c8cf9b63cea2093725ad'
    'v5/mixed_claims/receiver.py' = '5436569971c272b129fbaec480d51d57a1ec521d43fd4d4ad14133b786691d5b'
    'v5/client/workspace_atomic.py' = '32e3b95ea2e6d3f8dc35d63000728e9e075a16de3e13fb1a0b718bce45e11773'
    'v5/discovery/discovery_store.py' = '1c8543d4903754174b80d107ee923116ddb402d41a3b5af3f1d255abdfc6a328'
    'v5/placement/__init__.py' = '8fe08470d7fd15e96d1305f0e49a8b359cb53ce0c542bf7473b68d869159112e'
    'v5/placement/codec.py' = '6f32569d4807f96130350b85233161603f6860f082c75f81a8bfacf4f0a58999'
    'v5/placement/ledger.py' = 'd955990c347ed466617c752893dded8b8494dd266a050b045352c77c48f21a91'
    'v5/placement/controller.py' = 'ef1c9b59072127379e955bafeea001a22d6e3d10c9c46dca1304f85ab09e2b49'
    'v5/placement/network.py' = '1ec5c452ec129ae033f0577ebac6223e2cf3192d4724a3d31fe2e5c27a06cd4b'
    'v5/placement/advertisement.py' = '5aa23ee76115355ad319ae4acfd4ab418e010166e53b6ed02c82eb25d34d4510'
    'v5/client/serve_placement.py' = '7e735337d595894e25fd07a8dcc9ad8cd3ba9f1c042ba930684b7798232cb7fa'
}
$expectedExisting = @('v5/admission/pin_phase.py','v5/mixed_claims/imports_atomic.py','v5/mixed_claims/receiver.py','v5/client/workspace_atomic.py','v5/discovery/discovery_store.py')
foreach ($key in $sources.Keys) {
    $row = $sources[$key]
    Require-Digest $row.path $row.sha256
    if ((Get-Item -LiteralPath $row.path).Length -ne $row.bytes) { throw ('BASIS_SDK_SIZE: '+$key) }
}
foreach ($logical in $replacements.Keys) {
    if ($sources.Contains($logical) -ne ($logical -cin $expectedExisting)) { throw ('SOURCE_ADDITION_REPLACEMENT_CONFLICT: '+$logical) }
    $path = Join-Path $projectRoot $replacements[$logical]
    Require-Digest $path $reviewed.$logical
    $sources[$logical] = [ordered]@{path=$path;bytes=(Get-Item -LiteralPath $path).Length;sha256=$reviewed.$logical}
}
if ($sources.Count -ne 121) { throw 'SDK_DELTA_CENSUS' }
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
$name = 'distribution-consolidated-build-01'
$inputPath = Join-Path $checks 'distribution-consolidated-01-input.json'
$selectionPath = Join-Path $checks ($name+'-selection.json')
$parent = Join-Path $projectRoot 'product-local/v5-distribution-consolidated-01'
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
    selection_sha256=(Digest $selectionPath);sdk_sources=$sources.Count;replaced=5;added=7;
    installation_parent=$parent;parent_created=$true;build_executed=$false} | ConvertTo-Json
