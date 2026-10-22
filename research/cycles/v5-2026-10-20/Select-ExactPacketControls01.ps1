# Prepare the changed-boundary controls only; never run them here.
param(
    [Parameter(Mandatory=$true)][string]$ReviewedSourcesJson,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$TestSha256
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function CheckPin([string]$path,[string]$expected) {
    $item=Get-Item -LiteralPath $path
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or $item.PSIsContainer -or
        (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) -or
        (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $expected) {
        throw ('REVIEWED_PIN_CHANGED:'+ $path)
    }
}
$checks=Join-Path $projectRoot 'experiments/v5-local-checks'
$name='exact-packet-controls-01'
$selectionPath=Join-Path $checks ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw 'FRESH_CONTROLS_REQUIRED' }
}
$mapPath=Join-Path $checks 'distribution-managed-storage-01-input.json'
$mapSha='a629df82718f6a9d0560cacbfdc459739c15a56a1f2a46dd87929a1db51c22a4'
CheckPin $mapPath $mapSha
$map=Get-Content -LiteralPath $mapPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($map.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or
    @($map.sdk_sources.psobject.Properties).Count -ne 129) { throw 'EXACT_BASE_129' }
$runner='tools/Run-V5-Check.py'
$sources=[ordered]@{}
$sources[$runner]='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
CheckPin (Join-Path $projectRoot $runner) $sources[$runner]
foreach ($property in $map.sdk_sources.psobject.Properties) {
    $row=$property.Value
    $path=[IO.Path]::GetFullPath($row.path)
    if (-not $path.StartsWith($projectRoot+'\software\v5\',[StringComparison]::Ordinal)) { throw 'SDK_SOURCE_SCOPE' }
    CheckPin $path $row.sha256
    if ((Get-Item -LiteralPath $path).Length -ne $row.bytes) { throw 'SDK_SOURCE_SIZE' }
    $relative=$path.Substring($projectRoot.Length+1).Replace('\','/')
    if ($sources.Contains($relative)) { throw 'DUPLICATE_PHYSICAL_SOURCE' }
    $sources[$relative]=$row.sha256
}
$required=@('evidence_network/transport.py','placement/controller.py','client/workspace_evidence.py',
            'client/workspace_staged.py','client/semantic_reader.py','client/managed_owner.py')
if ($ReviewedSourcesJson.Length -gt 16384) { throw 'REVIEWED_MAP_BOUND' }
$reviewed=$ReviewedSourcesJson | ConvertFrom-Json
$keys=@($reviewed.psobject.Properties.Name)
if ($keys.Count -ne 6 -or @(Compare-Object $keys $required -CaseSensitive).Count -ne 0) { throw 'EXACT_REVIEWED_SET' }
foreach ($key in $required) {
    if (-not ($map.sdk_sources.psobject.Properties.Name -ccontains ('v5/'+$key))) { throw 'REPLACEMENT_MUST_EXIST' }
    $relative='software/v5/exact_packet/'+$key
    if ($sources.Contains($relative)) { throw 'FRESH_SUCCESSOR_REQUIRED' }
    CheckPin (Join-Path $projectRoot $relative) $reviewed.$key
    $sources[$relative]=$reviewed.$key
}
$test='software/v5/exact_packet/controls.py'
CheckPin (Join-Path $projectRoot $test) $TestSha256
$sources[$test]=$TestSha256
if ($sources.Count -ne 137) { throw 'SOURCE_CENSUS' }
$basisPath=Join-Path $checks 'distribution-managed-storage-build-01-selection.json'
CheckPin $basisPath '4df4b09b82c00e4ad70351eeb385b6d6a900fdaf70565b41c716400ee0246f54'
$basis=Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
$runtime=[ordered]@{}
foreach ($row in $basis.runtime_pins.psobject.Properties) {
    CheckPin $row.Name $row.Value
    $runtime[$row.Name]=$row.Value
}
if ($runtime.Count -ne 29 -or -not $runtime.Contains($basis.argv[0]) -or
    $runtime[$mapPath] -cne $mapSha) { throw 'EXACT_RUNTIME_AND_MAP' }
$selection=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($basis.argv[0],'-I','-S','-B','{snapshot}\software\v5\exact_packet\controls.py','--output','{output}')
    limits=[ordered]@{cpu_seconds=30;wall_seconds=90;memory_mib=256;active_processes=1;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 48)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_SIZE' }
$stream=[IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=$selectionPath;
    selection_sha256=(Get-FileHash -LiteralPath $selectionPath -Algorithm SHA256).Hash.ToLowerInvariant();
    sources=$sources.Count;runtime_pins=$runtime.Count;executed=$false} | ConvertTo-Json
