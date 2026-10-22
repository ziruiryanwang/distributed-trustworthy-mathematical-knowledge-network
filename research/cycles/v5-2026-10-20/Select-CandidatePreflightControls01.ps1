# File-only preparation. Root separately reviews/selects execution.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$TransportSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$FacadeSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$OwnerSha256,
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
$name='candidate-preflight-controls-01'
$selectionPath=Join-Path $checks ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw 'FRESH_CONTROLS_REQUIRED' }
}
$mapPath=Join-Path $checks 'distribution-exact-packet-01-input.json'
$mapSha='328c21bb585881d654f1a23f1704fbaa277ee865f7adb1250cf6c19b85647561'
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
$overlays=[ordered]@{
    'v5/delta/custody.py'=@('software/v5/offer_enumeration/delta/custody.py','e1e35cecd8f40154a98e40cb1a5a2cca1d8c376966e57ef529c7c878bdd6c634')
    'v5/admission/clean_refusal.py'=@('software/v5/candidate_admission/admission/clean_refusal.py','7c1386cce693185ac7d6e1dda149993c892ac5b2d417242fb7e02b873648e5a7')
    'v5/admission/verifier.py'=@('software/v5/candidate_admission/admission/verifier.py','ec6474cdd0580df89f9c646a41c0d909ec20e83da0a42274e0510a6e01bbbaea')
    'v5/aggregate_claims/aggregate_admission.py'=@('software/v5/candidate_admission/aggregate_claims/aggregate_admission.py','ce2cfc95f08699c679128448d9d9f5131cf54acbefa91225db2689a2b1574f5c')
    'v5/evidence_network/transport.py'=@('software/v5/candidate_preflight/evidence_network/transport.py',$TransportSha256)
    'v5/client/workspace_evidence.py'=@('software/v5/candidate_preflight/client/workspace_evidence.py',$FacadeSha256)
    'v5/client/managed_owner.py'=@('software/v5/candidate_preflight/client/managed_owner.py',$OwnerSha256)
}
foreach ($entry in $overlays.GetEnumerator()) {
    $exists=$map.sdk_sources.psobject.Properties.Name -ccontains $entry.Key
    if ($exists -eq ($entry.Key -ceq 'v5/admission/clean_refusal.py')) { throw 'EXACT_REPLACEMENT_OR_ADDITION' }
    $relative=$entry.Value[0]; $expected=$entry.Value[1]
    CheckPin (Join-Path $projectRoot $relative) $expected
    if ($sources.Contains($relative)) { throw 'FRESH_SUCCESSOR_REQUIRED' }
    $sources[$relative]=$expected
}
$test='software/v5/candidate_preflight/controls.py'
CheckPin (Join-Path $projectRoot $test) $TestSha256
$sources[$test]=$TestSha256
if ($sources.Count -ne 138) { throw 'SOURCE_CENSUS' }
$basisPath=Join-Path $checks 'distribution-exact-packet-build-01-selection.json'
CheckPin $basisPath '539cdda982392f8f128103909b53c9c74b014c5613562b9252e679979c4185ed'
$basis=Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
$runtime=[ordered]@{}
foreach ($row in $basis.runtime_pins.psobject.Properties) {
    CheckPin $row.Name $row.Value
    $runtime[$row.Name]=$row.Value
}
if ($runtime.Count -ne 29 -or -not $runtime.Contains($basis.argv[0]) -or
    $runtime[$mapPath] -cne $mapSha) { throw 'EXACT_RUNTIME_AND_MAP' }
$supervisor=Join-Path $projectRoot 'product-local/v4-library-commons-02/commons-v4/operator/commons.py'
$supervisorSha='6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9'
CheckPin $supervisor $supervisorSha
if ($runtime.Contains($supervisor)) { throw 'UNEXPECTED_SUPERVISOR_DUPLICATE' }
$runtime[$supervisor]=$supervisorSha
$selection=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($basis.argv[0],'-I','-S','-B','{snapshot}\software\v5\candidate_preflight\controls.py','--output','{output}')
    limits=[ordered]@{cpu_seconds=30;wall_seconds=90;memory_mib=256;active_processes=1;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 48)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_SIZE' }
$stream=[IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=$selectionPath;
    selection_sha256=(Get-FileHash -LiteralPath $selectionPath -Algorithm SHA256).Hash.ToLowerInvariant();
    sources=$sources.Count;runtime_pins=$runtime.Count;executed=$false} | ConvertTo-Json
