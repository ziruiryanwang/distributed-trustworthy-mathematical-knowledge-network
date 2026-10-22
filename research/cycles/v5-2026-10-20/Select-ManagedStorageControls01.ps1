# Prepare one finite controls selection. No product/test process is started.
param(
    [Parameter(Mandatory=$true)][ValidateSet('python','node')][string]$Kind,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$TestSha256
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function CheckPin([string]$path,[string]$sha) {
    $item=Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) -or
        (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $sha) { throw ('PIN_CHANGED:'+ $path) }
}
$checks=Join-Path $projectRoot 'experiments/v5-local-checks'
$name='managed-storage-'+$Kind+'-controls-01'
$selectionPath=Join-Path $checks ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw 'FRESH_CONTROLS_REQUIRED' }
}
$basisPath=Join-Path $checks 'distribution-managed-observed-build-01-selection.json'
CheckPin $basisPath 'c3257f270ca3b45bfa5a5c7f88798112dac49d9aaea378913ec1df9f98e3b3f6'
$basis=Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
$excluded=Join-Path $checks 'distribution-managed-observed-01-input.json'
$runtime=[ordered]@{}
foreach ($row in $basis.runtime_pins.psobject.Properties) {
    if ($row.Name -ceq $excluded) { continue }
    CheckPin $row.Name $row.Value
    $runtime[$row.Name]=$row.Value
}
if ($runtime.Count -ne 28 -or -not $runtime.Contains($basis.argv[0])) { throw 'EXACT_BASE_RUNTIME' }
$sources=[ordered]@{'tools/Run-V5-Check.py'='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'}
if ($Kind -ceq 'python') {
    $test='software/v5/managed_storage/python_controls.py'
    $sources[$test]=$TestSha256
    $dependencies=[ordered]@{
        'software/v5/instantiation_discovery/discovery/formal_features.py'='8822c8186ba120da9c8b72abe6d0c905eeaced5af46ef19600e463904a6d1b0c'
        'software/v5/managed_storage/placement/storage_profile.py'='3b535a337c1731ead3b9930c7cbe1f7c340a17152bd8b57e32981552ec061c90'
        'software/v5/managed_storage/placement/storage_paths.py'='e1bcba2730e432b4dfc428d9c56ebb2e5b7bc0f4d8a9bfa0751b8818557eb9da'
        'software/v5/managed_storage/placement/lifecycle.py'='0fa3dcc4285aa4afc87dfda5741e5c68334f8c0398138c3f218351e705a1f427'
        'software/v5/managed_storage/client/workspace_evidence.py'='d94e38257444da3bda04e4d9b298d422280a573becc27eaa063fdbc01f9c02a2'
        'software/v5/managed_storage/custody/module_store.py'='580515e461c95b424bc59011b8bf87e4776039f7d6cb87c27599f295c602dcbb'
        'software/v5/managed_storage/evidence_network/custody.py'='4264841e55ebc21899d8967ef9ac439d0682da5ea4a0d1c2097eddc930f1300e'
        'software/v5/managed_storage/discovery/discovery_store.py'='7f3c884b3ef3455e51563d233a2ca4a19087bc8097186e6b43e949abededa2c5'
        'software/v5/managed_storage/placement/ledger.py'='59f87b9334c44a8a9f8feb236084f419081d2484582917aded55eaac15f8351d'
        'software/v5/managed_storage/placement/advertisement.py'='13b0ef1ae400990f237e5e1957a77008d7f2ac51fb96758560152cfda3ecdf28'
    }
    foreach ($key in $dependencies.Keys) {$sources[$key]=$dependencies[$key]}
    $argv=@($basis.argv[0],'-I','-S','-B',('{snapshot}\'+$test.Replace('/','\')),'--output','{output}')
    if ($sources.Count -ne 12) { throw 'PYTHON_SOURCE_CENSUS' }
} else {
    $test='software/v5/managed_storage/node_controls.mjs'
    $sources[$test]=$TestSha256
    $sources['software/v5/managed_storage/portable/location/intent.mjs']='6c30e8793f737f0512e3e7e9d785d1311cafa35116784f4f8b3dda5c1a75fa29'
    $sources['software/v5/managed_storage/portable/location/maintained_roles.mjs']='d69d0b123e52f5cfbf4c2eef2e2d2dfecf9b9b11c9ddfabc4c5e37499e1a12e0'
    # Identical adjacent fixture only; never an addition to the product SDK map.
    $sources['software/v5/managed_storage/portable/location/protocol.mjs']='88c2bc34e5ebefc412b564bef06e0d4210e0c44e3102be1d6adacfc6334af986'
    $base=Join-Path $projectRoot 'product-local/v5-distribution-managed-observed-01/Mathematical Commons v5/base'
    $node=Join-Path $base 'runtime/node/node.exe'
    $extra=[ordered]@{}
    $extra[$node]='b3094d0b49f9ad602262a9921551737bb97637c05dd357a06ae98188d7290aa3'
    $extra[(Join-Path $base 'RELEASE-MANIFEST.json')]='a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed'
    $extra[(Join-Path $base 'overlay/quota_store.mjs')]='7c6cbeea0c685ec81f8d263cf84c6b8b9dd2c1f09e9f2f0f063196abc929eca4'
    foreach ($key in $extra.Keys) {CheckPin $key $extra[$key];$runtime[$key]=$extra[$key]}
    $argv=@($node,('{snapshot}\'+$test.Replace('/','\')),'--output','{output}')
    if ($sources.Count -ne 5 -or $runtime.Count -ne 31) { throw 'NODE_SOURCE_RUNTIME_CENSUS' }
}
foreach ($key in $sources.Keys) {CheckPin (Join-Path $projectRoot $key) $sources[$key]}
$selection=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime;argv=$argv
    limits=[ordered]@{cpu_seconds=10;wall_seconds=45;memory_mib=128;active_processes=1;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 48)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_SIZE' }
$stream=[IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=$selectionPath;selection_sha256=(Get-FileHash -LiteralPath $selectionPath -Algorithm SHA256).Hash.ToLowerInvariant();
    sources=$sources.Count;runtime_pins=$runtime.Count;executed=$false} | ConvertTo-Json
