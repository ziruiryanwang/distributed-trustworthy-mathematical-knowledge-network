# Prepare a fresh source map/build instruction only. Does not execute the build.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ReviewSha256
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
function CheckPin([string]$path,[string]$expected) {
    $item=Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) -or
        (Digest $path) -cne $expected) { throw ('REVIEWED_PIN_CHANGED:'+ $path) }
}
function NewJson([string]$path,$value) {
    $raw=[Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 64)+"`n")
    if ($raw.Length -gt 8*1024*1024) { throw 'JSON_BOUND' }
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
}
$checks=Join-Path $projectRoot 'experiments/v5-local-checks'
$cycle=Join-Path $projectRoot 'research/cycles/v5-2026-10-20'
CheckPin (Join-Path $cycle 'MANAGED-STORAGE-OWNER-PATHS-REVIEW.md') $ReviewSha256
$basisPath=Join-Path $checks 'distribution-managed-observed-01-input.json'
CheckPin $basisPath 'e0f0dc5d63dee0d088b8edd9e61d9a1d1bebbe31d3dde76b53887d1c901f7201'
$basis=Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or $basis.base_role -cne 'mathematical-client-location-v1') { throw 'INPUT_BASIS' }
$sources=[ordered]@{}
foreach ($row in $basis.sdk_sources.psobject.Properties) { $sources[$row.Name]=$row.Value }
if ($sources.Count -ne 127) { throw 'EXACT_BASIS_127' }
foreach ($name in $sources.Keys) {
    $row=$sources[$name]; CheckPin $row.path $row.sha256
    if ((Get-Item -LiteralPath $row.path).Length -ne $row.bytes) { throw 'BASIS_SOURCE_SIZE' }
}
$changes=[ordered]@{
    'client/managed_owner.py'='6991ac58310b0c3a6456f033bff7bccbb02dd1299c67716d805762e0dea69a0f'
    'client/serve_generations.py'='e12f3899f28cab8a95a9b497a6a7f5148cdc537912bed3d357310e2c0d220a83'
    'client/workspace_evidence.py'='d94e38257444da3bda04e4d9b298d422280a573becc27eaa063fdbc01f9c02a2'
    'custody/module_store.py'='580515e461c95b424bc59011b8bf87e4776039f7d6cb87c27599f295c602dcbb'
    'evidence_network/custody.py'='4264841e55ebc21899d8967ef9ac439d0682da5ea4a0d1c2097eddc930f1300e'
    'discovery/discovery_store.py'='7f3c884b3ef3455e51563d233a2ca4a19087bc8097186e6b43e949abededa2c5'
    'placement/ledger.py'='59f87b9334c44a8a9f8feb236084f419081d2484582917aded55eaac15f8351d'
    'placement/advertisement.py'='13b0ef1ae400990f237e5e1957a77008d7f2ac51fb96758560152cfda3ecdf28'
    'placement/lifecycle.py'='0fa3dcc4285aa4afc87dfda5741e5c68334f8c0398138c3f218351e705a1f427'
    'placement/sessions.py'='6e07010c47b0e95abbb80125e838b759e2a4206bdc3cafa735e31c7015d1a63b'
    'placement/storage_profile.py'='3b535a337c1731ead3b9930c7cbe1f7c340a17152bd8b57e32981552ec061c90'
    'placement/storage_paths.py'='e1bcba2730e432b4dfc428d9c56ebb2e5b7bc0f4d8a9bfa0751b8818557eb9da'
    'portable/location/intent.mjs'='6c30e8793f737f0512e3e7e9d785d1311cafa35116784f4f8b3dda5c1a75fa29'
    'portable/location/maintained_roles.mjs'='d69d0b123e52f5cfbf4c2eef2e2d2dfecf9b9b11c9ddfabc4c5e37499e1a12e0'
}
$added=0;$replaced=0
foreach ($name in $changes.Keys) {
    $logical=if ($name.StartsWith('portable/')) {$name} else {'v5/'+$name}
    $path=Join-Path $projectRoot ('software/v5/managed_storage/'+$name)
    CheckPin $path $changes[$name]
    if ($sources.Contains($logical)) {$replaced++} else {$added++}
    $sources[$logical]=[ordered]@{path=$path;bytes=(Get-Item -LiteralPath $path).Length;sha256=$changes[$name]}
}
if ($sources.Count -ne 129 -or $added -ne 2 -or $replaced -ne 12 -or
    @($sources.Keys | Where-Object {$_.StartsWith('v5/',[StringComparison]::Ordinal)}).Count -ne 108) { throw 'EXACT_STORAGE_MAP' }
$builderKey='software/v5/body_location/distribution.py'
$builderSha='eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813'
if ($basis.distribution_source.path -cne (Join-Path $projectRoot $builderKey) -or
    $basis.distribution_source.sha256 -cne $builderSha) { throw 'BUILDER_BASIS' }
CheckPin (Join-Path $projectRoot $builderKey) $builderSha
$basis.sdk_sources=$sources
$buildBasisPath=Join-Path $checks 'distribution-managed-observed-build-01-selection.json'
CheckPin $buildBasisPath 'c3257f270ca3b45bfa5a5c7f88798112dac49d9aaea378913ec1df9f98e3b3f6'
$buildBasis=Get-Content -LiteralPath $buildBasisPath -Raw -Encoding UTF8 | ConvertFrom-Json
$runtime=[ordered]@{}
foreach ($row in $buildBasis.runtime_pins.psobject.Properties) {
    if ($row.Name -ceq $basisPath) { continue }
    CheckPin $row.Name $row.Value
    $runtime[$row.Name]=$row.Value
}
$runnerKey='tools/Run-V5-Check.py'
$runnerSha='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
CheckPin (Join-Path $projectRoot $runnerKey) $runnerSha
if ($runtime.Count -ne 28 -or -not $runtime.Contains($buildBasis.argv[0])) { throw 'EXACT_RUNTIME_BASIS' }
$name='distribution-managed-storage-build-01'
$inputPath=Join-Path $checks 'distribution-managed-storage-01-input.json'
$selectionPath=Join-Path $checks ($name+'-selection.json')
$parent=Join-Path $projectRoot 'product-local/v5-distribution-managed-storage-01'
foreach ($path in @($inputPath,$selectionPath,$parent,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED:'+ $path) }
}
NewJson $inputPath $basis
$inputSha=Digest $inputPath;$runtime[$inputPath]=$inputSha
$buildSources=[ordered]@{}
$buildSources[$runnerKey]=$runnerSha;$buildSources[$builderKey]=$builderSha
$selection=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$buildSources;runtime_pins=$runtime
    argv=@($buildBasis.argv[0],'-I','-S','-B','{snapshot}\software\v5\body_location\distribution.py',
           'build',$inputPath,$inputSha,(Join-Path $parent 'Mathematical Commons v5'))
    limits=[ordered]@{cpu_seconds=120;wall_seconds=600;memory_mib=128;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
NewJson $selectionPath $selection
[void][IO.Directory]::CreateDirectory($parent)
[ordered]@{input=$inputPath;input_sha256=$inputSha;selection=$selectionPath;
    selection_sha256=(Digest $selectionPath);sdk_sources=129;preparation_sources=108;
    replaced=12;added=2;unchanged=115;installation_parent=$parent;build_executed=$false} | ConvertTo-Json
