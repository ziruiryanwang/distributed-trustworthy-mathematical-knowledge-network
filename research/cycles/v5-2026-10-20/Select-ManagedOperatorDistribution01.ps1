# Prepare the exact existing121 plus five reviewed managed-owner additions.
# This creates a fresh finite build selection only; it never executes a build.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$OwnerSourceSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$CompositionReviewSha256
)
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Require-Digest([string]$path,[string]$expected) {
    $item=Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) -or
        $expected -cnotmatch '^[0-9a-f]{64}$' -or (Digest $path) -cne $expected) { throw ('REVIEWED_INPUT_CHANGED:'+ $path) }
}
function New-Json([string]$path,$value) {
    $raw=[Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 64)+"`n")
    if ($raw.Length -gt 8*1024*1024) { throw 'JSON_BOUND' }
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
}
$checks=Join-Path $projectRoot 'experiments/v5-local-checks'
$cycle=Join-Path $projectRoot 'research/cycles/v5-2026-10-20'
Require-Digest (Join-Path $cycle 'MANAGED-OPERATOR-REVIEW.md') $CompositionReviewSha256
$basisPath=Join-Path $checks 'distribution-consolidated-01-input.json'
Require-Digest $basisPath '8ba3707236c1a6e01ab7f87886814f801034b2fe9144ad9603585adcc73feb33'
$basis=Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or $basis.base_role -cne 'mathematical-client-location-v1') { throw 'INPUT_BASIS' }
$sources=[ordered]@{}
foreach ($property in $basis.sdk_sources.psobject.Properties) { $sources[$property.Name]=$property.Value }
if ($sources.Count -ne 121) { throw 'BASIS_SDK_CENSUS' }
foreach ($key in $sources.Keys) {
    $row=$sources[$key]; Require-Digest $row.path $row.sha256
    if ((Get-Item -LiteralPath $row.path).Length -ne $row.bytes) { throw ('BASIS_SDK_SIZE:'+ $key) }
}
$additions=[ordered]@{
    'v5/placement/lifecycle.py'='software/v5/supervised_generations/placement/lifecycle.py'
    'v5/placement/sessions.py'='software/v5/supervised_generations/placement/sessions.py'
    'v5/placement/reclaim.py'='software/v5/bounded_reclamation/placement/reclaim.py'
    'v5/client/serve_generations.py'='software/v5/bounded_generations/client/serve_generations.py'
    'v5/client/managed_owner.py'='software/v5/managed_operator/client/managed_owner.py'
}
$reviewed=[ordered]@{
    'v5/placement/lifecycle.py'='bec62143313e1abd400550bae45a6334be2ddffb94d77a14ba9b5853b565042f'
    'v5/placement/sessions.py'='b4cfab61c990464756e87a7344e2a029a5374602283a4255d4d5aa854090b7f7'
    'v5/placement/reclaim.py'='19713fc4baec821a5c77a0071182c63401b292cbe79a7ed7c04b7deba50e1894'
    'v5/client/serve_generations.py'='404365849dd0e41860ba8ccda01a5b064d028241a2d8b0063d76936fcd306687'
    'v5/client/managed_owner.py'=$OwnerSourceSha256
}
foreach ($logical in $additions.Keys) {
    if ($sources.Contains($logical)) { throw ('EXPECTED_ONLY_ADDITION:'+ $logical) }
    $path=Join-Path $projectRoot $additions[$logical]
    Require-Digest $path $reviewed[$logical]
    $sources[$logical]=[ordered]@{path=$path;bytes=(Get-Item -LiteralPath $path).Length;sha256=$reviewed[$logical]}
}
if ($sources.Count -ne 126 -or @($sources.Keys | Where-Object {$_.StartsWith('v5/',[StringComparison]::Ordinal)}).Count -ne 105) { throw 'EXACT_SDK_AND_PREPARATION_CENSUS' }
$sourceKey='software/v5/body_location/distribution.py'
$builder=Join-Path $projectRoot $sourceKey
$builderSha='eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813'
if ($basis.distribution_source.path -cne $builder -or $basis.distribution_source.sha256 -cne $builderSha) { throw 'BUILDER_BASIS' }
Require-Digest $builder $builderSha
$basis.sdk_sources=$sources
$buildBasisPath=Join-Path $checks 'distribution-body-custody-build-01-selection.json'
Require-Digest $buildBasisPath 'ec52d60965bcdf885455a4aeb20e9c27fedd87fb0fc73b363c3522aca9b6e0ab'
$buildBasis=Get-Content -LiteralPath $buildBasisPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($buildBasis.schema -cne 'DMKN_V5_LOCAL_CHECK_V1' -or $buildBasis.name -cne 'distribution-body-custody-build-01') { throw 'BUILD_BASIS' }
$runtime=[ordered]@{}
foreach ($property in $buildBasis.runtime_pins.psobject.Properties) {
    Require-Digest $property.Name $property.Value
    $runtime[$property.Name]=$property.Value
}
$runnerKey='tools/Run-V5-Check.py'
$runnerSha='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
Require-Digest (Join-Path $projectRoot $runnerKey) $runnerSha
$buildSources=[ordered]@{}
$buildSources[$runnerKey]=$runnerSha; $buildSources[$sourceKey]=$builderSha
if (-not $runtime.Contains($buildBasis.argv[0])) { throw 'BUILD_RUNTIME_BASIS' }
$name='distribution-managed-owner-build-01'
$inputPath=Join-Path $checks 'distribution-managed-owner-01-input.json'
$selectionPath=Join-Path $checks ($name+'-selection.json')
$parent=Join-Path $projectRoot 'product-local/v5-distribution-managed-owner-01'
foreach ($path in @($inputPath,$selectionPath,$parent,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED:'+ $path) }
}
New-Json $inputPath $basis
$inputSha=Digest $inputPath; $runtime[$inputPath]=$inputSha
$selected=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$buildSources;runtime_pins=$runtime
    argv=@($buildBasis.argv[0],'-I','-S','-B','{snapshot}\software\v5\body_location\distribution.py',
           'build',$inputPath,$inputSha,(Join-Path $parent 'Mathematical Commons v5'))
    # Same finite file-only build envelope as adopted consolidated121.
    limits=[ordered]@{cpu_seconds=120;wall_seconds=600;memory_mib=128;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
New-Json $selectionPath $selected
[void][IO.Directory]::CreateDirectory($parent)
[ordered]@{input=$inputPath;input_sha256=$inputSha;selection=$selectionPath;
    selection_sha256=(Digest $selectionPath);sdk_sources=$sources.Count;preparation_sources=105;replaced=0;added=5;
    installation_parent=$parent;parent_created=$true;build_executed=$false} | ConvertTo-Json
