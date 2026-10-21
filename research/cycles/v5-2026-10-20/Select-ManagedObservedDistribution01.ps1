# Source-map preparation only; no builder, service or credential execution.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$OwnerSourceSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$CompositionReviewSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$CloseServiceSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$CloseReviewSha256
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
Require-Digest (Join-Path $cycle 'MANAGED-OBSERVED-OWNER-REVIEW.md') $CompositionReviewSha256
Require-Digest (Join-Path $cycle 'MANAGED-CLOSE-DRAIN-REVIEW.md') $CloseReviewSha256
$basisPath=Join-Path $checks 'distribution-managed-contribution-01-input.json'
Require-Digest $basisPath '33bd99d7c3a1db865a6abcb92c96b5df2d0923a793535135e133aebc54aacc0c'
$basis=Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or $basis.base_role -cne 'mathematical-client-location-v1') { throw 'INPUT_BASIS' }
$sources=[ordered]@{}
foreach ($property in $basis.sdk_sources.psobject.Properties) { $sources[$property.Name]=$property.Value }
if ($sources.Count -ne 127 -or
    $sources['v5/client/managed_owner.py'].sha256 -cne '75c0e8a93c26594d459e716cf55dc6c982b1df079eeaed7834a1347fe4a40d09' -or
    $sources['v5/client/serve_placement.py'].sha256 -cne '7e735337d595894e25fd07a8dcc9ad8cd3ba9f1c042ba930684b7798232cb7fa' -or
    $sources['v5/client/private_credentials.py'].sha256 -cne '7116e2d9161cbb828203bc7eff1e7dd90c1cab7d6e860a6e16801ffb6ecb37f0') { throw 'BASIS_EXACT_127' }
foreach ($key in $sources.Keys) {
    $row=$sources[$key]; Require-Digest $row.path $row.sha256
    if ((Get-Item -LiteralPath $row.path).Length -ne $row.bytes) { throw ('BASIS_SDK_SIZE:'+ $key) }
}
$changes=[ordered]@{
    'v5/client/managed_owner.py'=@('software/v5/managed_observed/client/managed_owner.py',$OwnerSourceSha256)
    'v5/client/serve_placement.py'=@('software/v5/managed_close_drain/client/serve_placement.py',$CloseServiceSha256)
}
foreach ($logical in $changes.Keys) {
    $path=Join-Path $projectRoot $changes[$logical][0]
    Require-Digest $path $changes[$logical][1]
    $sources[$logical]=[ordered]@{path=$path;bytes=(Get-Item -LiteralPath $path).Length;sha256=$changes[$logical][1]}
}
if ($sources.Count -ne 127 -or @($sources.Keys | Where-Object {$_.StartsWith('v5/',[StringComparison]::Ordinal)}).Count -ne 106) { throw 'EXACT_SDK_AND_PREPARATION_CENSUS' }
$sourceKey='software/v5/body_location/distribution.py'
$builder=Join-Path $projectRoot $sourceKey
$builderSha='eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813'
if ($basis.distribution_source.path -cne $builder -or $basis.distribution_source.sha256 -cne $builderSha) { throw 'BUILDER_BASIS' }
Require-Digest $builder $builderSha
$basis.sdk_sources=$sources
$buildBasisPath=Join-Path $checks 'distribution-managed-contribution-build-01-selection.json'
Require-Digest $buildBasisPath 'ad982f4d49107a6bc6ed4e6268adad9e9e88f963930106ba06eda57faedd5959'
$buildBasis=Get-Content -LiteralPath $buildBasisPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($buildBasis.schema -cne 'DMKN_V5_LOCAL_CHECK_V1' -or $buildBasis.name -cne 'distribution-managed-contribution-build-01') { throw 'BUILD_BASIS' }
$runtime=[ordered]@{}
foreach ($property in $buildBasis.runtime_pins.psobject.Properties) {
    if ($property.Name -ceq $basisPath) { continue }
    Require-Digest $property.Name $property.Value
    $runtime[$property.Name]=$property.Value
}
$runnerKey='tools/Run-V5-Check.py'
$runnerSha='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
Require-Digest (Join-Path $projectRoot $runnerKey) $runnerSha
$buildSources=[ordered]@{}
$buildSources[$runnerKey]=$runnerSha; $buildSources[$sourceKey]=$builderSha
if (-not $runtime.Contains($buildBasis.argv[0])) { throw 'BUILD_RUNTIME_BASIS' }
$name='distribution-managed-observed-build-01'
$inputPath=Join-Path $checks 'distribution-managed-observed-01-input.json'
$selectionPath=Join-Path $checks ($name+'-selection.json')
$parent=Join-Path $projectRoot 'product-local/v5-distribution-managed-observed-01'
foreach ($path in @($inputPath,$selectionPath,$parent,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED:'+ $path) }
}
New-Json $inputPath $basis
$inputSha=Digest $inputPath; $runtime[$inputPath]=$inputSha
$selected=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$buildSources;runtime_pins=$runtime
    argv=@($buildBasis.argv[0],'-I','-S','-B','{snapshot}\software\v5\body_location\distribution.py',
           'build',$inputPath,$inputSha,(Join-Path $parent 'Mathematical Commons v5'))
    limits=[ordered]@{cpu_seconds=120;wall_seconds=600;memory_mib=128;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
New-Json $selectionPath $selected
[void][IO.Directory]::CreateDirectory($parent)
[ordered]@{input=$inputPath;input_sha256=$inputSha;selection=$selectionPath;
    selection_sha256=(Digest $selectionPath);sdk_sources=$sources.Count;preparation_sources=106;replaced=2;added=0;
    installation_parent=$parent;parent_created=$true;build_executed=$false} | ConvertTo-Json
