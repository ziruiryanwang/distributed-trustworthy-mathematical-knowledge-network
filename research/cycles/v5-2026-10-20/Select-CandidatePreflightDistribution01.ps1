# File-only preparation of one combined candidate; no build is run here.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$TransportSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$FacadeSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$OwnerSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ControlsOutcomeSha256
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
function CheckPin([string]$path,[string]$expected) {
    $item=Get-Item -LiteralPath $path
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or $item.PSIsContainer -or
        (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) -or
        (Digest $path) -cne $expected) { throw ('REVIEWED_PIN_CHANGED:'+ $path) }
}
function NewJson([string]$path,$value) {
    $raw=[Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 64)+"`n")
    if ($raw.Length -gt 8*1024*1024) { throw 'JSON_BOUND' }
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
}
$checks=Join-Path $projectRoot 'experiments/v5-local-checks'
$basisPath=Join-Path $checks 'distribution-exact-packet-01-input.json'
CheckPin $basisPath '328c21bb585881d654f1a23f1704fbaa277ee865f7adb1250cf6c19b85647561'
CheckPin (Join-Path $projectRoot 'research/cycles/v5-2026-10-20/CANDIDATE-PREFLIGHT-CONTROLS-OUTCOME.md') $ControlsOutcomeSha256
$basis=Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or
    $basis.base_role -cne 'mathematical-client-location-v1') { throw 'INPUT_BASIS' }
$sources=[ordered]@{}
foreach ($row in $basis.sdk_sources.psobject.Properties) {
    CheckPin $row.Value.path $row.Value.sha256
    if ((Get-Item -LiteralPath $row.Value.path).Length -ne $row.Value.bytes) { throw 'BASIS_SOURCE_SIZE' }
    $sources[$row.Name]=$row.Value
}
if ($sources.Count -ne 129) { throw 'EXACT_BASIS_129' }
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
    if ($sources.Contains($entry.Key) -eq ($entry.Key -ceq 'v5/admission/clean_refusal.py')) {
        throw 'EXACT_REPLACEMENT_OR_ADDITION'
    }
    $path=Join-Path $projectRoot $entry.Value[0]; $expected=$entry.Value[1]
    CheckPin $path $expected
    $sources[$entry.Key]=[ordered]@{path=$path;bytes=(Get-Item -LiteralPath $path).Length;sha256=$expected}
}
if ($sources.Count -ne 130 -or
    @($sources.Keys | Where-Object {$_.StartsWith('v5/',[StringComparison]::Ordinal)}).Count -ne 109) { throw 'EXACT_MAP' }
$builder='software/v5/body_location/distribution.py'
$builderSha='eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813'
if ($basis.distribution_source.path -cne (Join-Path $projectRoot $builder) -or
    $basis.distribution_source.sha256 -cne $builderSha) { throw 'BUILDER_BASIS' }
CheckPin (Join-Path $projectRoot $builder) $builderSha
$basis.sdk_sources=$sources
$buildBasisPath=Join-Path $checks 'distribution-exact-packet-build-01-selection.json'
CheckPin $buildBasisPath '539cdda982392f8f128103909b53c9c74b014c5613562b9252e679979c4185ed'
$buildBasis=Get-Content -LiteralPath $buildBasisPath -Raw -Encoding UTF8 | ConvertFrom-Json
$runtime=[ordered]@{}
foreach ($row in $buildBasis.runtime_pins.psobject.Properties) {
    if ($row.Name -ceq $basisPath) { continue }
    CheckPin $row.Name $row.Value
    $runtime[$row.Name]=$row.Value
}
$runner='tools/Run-V5-Check.py'
$runnerSha='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
CheckPin (Join-Path $projectRoot $runner) $runnerSha
if ($runtime.Count -ne 28 -or -not $runtime.Contains($buildBasis.argv[0])) { throw 'EXACT_RUNTIME' }
$name='distribution-candidate-preflight-build-01'
$inputPath=Join-Path $checks 'distribution-candidate-preflight-01-input.json'
$selectionPath=Join-Path $checks ($name+'-selection.json')
$parent=Join-Path $projectRoot 'product-local/v5-distribution-candidate-preflight-01'
foreach ($path in @($inputPath,$selectionPath,$parent,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED:'+ $path) }
}
NewJson $inputPath $basis
$inputSha=Digest $inputPath; $runtime[$inputPath]=$inputSha
$buildSources=[ordered]@{}
$buildSources[$runner]=$runnerSha; $buildSources[$builder]=$builderSha
$selection=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$buildSources;runtime_pins=$runtime
    argv=@($buildBasis.argv[0],'-I','-S','-B','{snapshot}\software\v5\body_location\distribution.py',
           'build',$inputPath,$inputSha,(Join-Path $parent 'Mathematical Commons v5'))
    limits=[ordered]@{cpu_seconds=120;wall_seconds=600;memory_mib=128;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
NewJson $selectionPath $selection
[void][IO.Directory]::CreateDirectory($parent)
[ordered]@{input=$inputPath;input_sha256=$inputSha;selection=$selectionPath;
    selection_sha256=(Digest $selectionPath);sdk_sources=130;preparation_sources=109;
    replaced=6;added=1;unchanged=123;installation_parent=$parent;build_executed=$false} | ConvertTo-Json
