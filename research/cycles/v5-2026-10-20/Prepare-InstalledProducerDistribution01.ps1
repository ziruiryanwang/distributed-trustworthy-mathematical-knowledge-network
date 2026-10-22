# File-only selection for ONE future full distribution. Does not run the builder.
# Root separately selects this preparer and all reviewed successor digests.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$BuilderSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$LifecycleProducerSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$LifecycleSnapshotSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ProducerSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$AdoptionSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$EntrySha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$LauncherSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ContractSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$SourceReviewSha256
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$prepared=Join-Path $checks 'installed-producer-distribution-01'
$name='distribution-installed-producer-build-01'
$parent=Join-Path $projectRoot 'product-local\v5-distribution-installed-producer-01'
$component=Join-Path $checks 'release-producer-component-01'
$installation=Join-Path $component 'installation'
$overlay='software/v5/installed_production/'
$originals=[ordered]@{}
function Ordinary([string]$path,[bool]$directory=$false,[bool]$fresh=$false) {
    $full=[IO.Path]::GetFullPath($path)
    if ($full -cne $path -or -not $full.StartsWith($projectRoot+'\',[StringComparison]::Ordinal)) { throw 'CANONICAL_PROJECT_PATH' }
    $cursor=$full
    while ($cursor) {
        if (Test-Path -LiteralPath $cursor) {
            $item=Get-Item -LiteralPath $cursor
            if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0 -or
                ($cursor -cne $full -and -not $item.PSIsContainer)) { throw 'ORDINARY_PATH_REQUIRED' }
        }
        $cursor=[IO.Path]::GetDirectoryName($cursor)
    }
    if ($fresh) { if (Test-Path -LiteralPath $full) { throw ('FRESH_OUTPUT_REQUIRED:'+ $full) } }
    elseif ([bool](Get-Item -LiteralPath $full).PSIsContainer -ne $directory) { throw 'PATH_KIND' }
    return $full
}
function Pin([string]$path,[string]$expected,[long]$maximum=134217728) {
    [void](Ordinary $path)
    $size=(Get-Item -LiteralPath $path).Length
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or $size -lt 0 -or $size -gt $maximum -or
        (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $expected -or
        (Get-Item -LiteralPath $path).Length -ne $size) { throw ('PIN_CHANGED:'+ $path) }
    return [ordered]@{path=$path;bytes=$size;sha256=$expected}
}
function Remember($row) {
    $actual=Pin $row.path $row.sha256
    if ($actual.bytes -ne $row.bytes) { throw 'PIN_SIZE' }
    if ($originals.Contains($row.path) -and ($originals[$row.path].sha256 -cne $row.sha256 -or
        $originals[$row.path].bytes -ne $row.bytes)) { throw 'PIN_CONFLICT' }
    $originals[$row.path]=$actual
    return $actual
}
function ReadKnown([string]$path,[string]$expected) {
    $row=Pin $path $expected 8388608; [void](Remember $row)
    return Get-Content -LiteralPath $path -Raw -Encoding UTF8 | ConvertFrom-Json
}
function DigestBytes([byte[]]$raw) {
    $algorithm=[Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($algorithm.ComputeHash($raw))).Replace('-','').ToLowerInvariant() }
    finally { $algorithm.Dispose() }
}
function NewJson([string]$path,$value,[long]$maximum=8388608) {
    [void](Ordinary $path $false $true)
    $raw=[Text.UTF8Encoding]::new($false).GetBytes((ConvertTo-Json -InputObject $value -Depth 64 -Compress)+"`n")
    if ($raw.Length -eq 0 -or $raw.Length -gt $maximum) { throw 'GENERATED_JSON_BOUND' }
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($raw,0,$raw.Length);$stream.Flush($true) } finally { $stream.Dispose() }
    $row=Pin $path (DigestBytes $raw) $maximum
    if ($row.bytes -ne $raw.Length) { throw 'GENERATED_JSON_SIZE_CHANGED' }
    return $row
}
function RelativePin([string]$path,$row) { return [ordered]@{path=$path;bytes=$row.bytes;sha256=$row.sha256} }
foreach($path in @($prepared,$parent,(Join-Path $checks $name))) { [void](Ordinary $path $true $true) }
if (Test-Path -LiteralPath (Join-Path $component 'PREPARATION-FAILED.json')) { throw 'COMPONENT_PREPARATION_FAILED' }
$basisPath=Join-Path $checks 'distribution-candidate-preflight-01-input.json'
$basis=ReadKnown $basisPath '25e7c849e41f394498e21a60cc7800ecffb67b0cee1b3911d7164977ce4f2364'
$buildBasis=ReadKnown (Join-Path $checks 'distribution-candidate-preflight-build-01-selection.json') '1329ea5ee86d223c65ccb949bf0ebf66f3f3646c975ad58055aa8a5545662d14'
$componentManifest=ReadKnown (Join-Path $installation 'V5-RELEASE.json') 'b0e2145aea33171d9fd7d65e2a2913d832753dee1575d05fff320a825f5fc9ac'
$componentDescriptor=ReadKnown (Join-Path $installation 'assets\producer\ARTIFACTS.json') 'fde60e82ebbc5fe65949fcc946bd80d3ff11464f983f356aa20c0f3e1efffe3e'
$oldProfile=ReadKnown (Join-Path $component 'profile.json') 'd08c46b29b136087c72b52ecab201d89e3eed4941819d01953ae9100df9bbe8d'
$reviewPath=Join-Path $projectRoot 'research\cycles\v5-2026-10-20\INSTALLED-PRODUCER-SOURCE-REVIEW.md'
$review=Remember (Pin $reviewPath $SourceReviewSha256 1048576)
$consumerImage='99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60'
$producerImage='9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865'
if ($basis.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or $basis.base_role -cne 'mathematical-client-location-v1' -or
    $basis.aggregate_image -cne $consumerImage -or $componentDescriptor.aggregate_image -cne $producerImage) { throw 'FIXED_INPUT_ROLES' }
$sources=[ordered]@{}
foreach($entry in $basis.sdk_sources.psobject.Properties) { $sources[$entry.Name]=Remember $entry.Value }
if ($sources.Count -ne 130 -or $sources['v5/admission/verifier.py'].sha256 -cne
    'ec6474cdd0580df89f9c646a41c0d909ec20e83da0a42274e0510a6e01bbbaea') { throw 'CURRENT_RECEIVER_REQUIRED' }
$frozen=@('aggregate_lifecycle/__init__.py','aggregate_small/__init__.py','aggregate_small/producer.py',
    'aggregate_small/operator.py','aggregate_claims/input.py','aggregate_claims/prepare_mixed.py','release_production/__init__.py')
foreach($relative in $frozen) {
    $logical='v5/'+$relative; $installed='sdk/'+$logical
    if ($sources.Contains($logical)) { throw 'NO_EXISTING_SOURCE_REPLACEMENT' }
    $row=$componentManifest.files.$installed
    $path=Join-Path $installation ($installed.Replace('/','\'))
    $sources[$logical]=Remember ([ordered]@{path=$path;bytes=$row.bytes;sha256=$row.sha256})
}
$newSources=[ordered]@{
    'aggregate_lifecycle/producer.py'=$LifecycleProducerSha256
    'aggregate_lifecycle/snapshot.py'=$LifecycleSnapshotSha256
    'release_production/producer.py'=$ProducerSha256
    'release_production/adoption.py'=$AdoptionSha256
    'release_production/operator.py'=$EntrySha256
    'release_production/launch.py'=$LauncherSha256
    'release_production/launch_contract.py'=$ContractSha256
}
foreach($relative in $newSources.Keys) {
    $logical='v5/'+$relative
    if ($sources.Contains($logical)) { throw 'NO_EXISTING_SOURCE_REPLACEMENT' }
    $sources[$logical]=Remember (Pin (Join-Path $projectRoot ($overlay+$relative).Replace('/','\')) $newSources[$relative] 1048576)
}
if ($sources.Count -ne 144 -or @($sources.Keys | Where-Object {$_.StartsWith('v5/',[StringComparison]::Ordinal) -and $_.EndsWith('.py',[StringComparison]::Ordinal)}).Count -ne 123) { throw 'EXACT_144_123_MAP' }
$producerOnly=@(($frozen+@($newSources.Keys)) | ForEach-Object {'v5/'+$_})
$consumerNames=@($sources.Keys | Where-Object {$_ -cnotin $producerOnly})
if ($producerOnly.Count -ne 14 -or @($producerOnly | Sort-Object -Unique).Count -ne 14 -or
    $consumerNames.Count -ne 130 -or @($consumerNames | Where-Object {$_.StartsWith('v5/',[StringComparison]::Ordinal) -and $_.EndsWith('.py',[StringComparison]::Ordinal)}).Count -ne 109) { throw 'EXACT_CONSUMER_PROJECTION_130_109' }
foreach($entry in $basis.sdk_sources.psobject.Properties) {
    $row=$sources[$entry.Name]
    if ($row.path -cne $entry.Value.path -or $row.bytes -ne $entry.Value.bytes -or $row.sha256 -cne $entry.Value.sha256) { throw 'CURRENT_130_CHANGED' }
}
$core=@('aggregate_lifecycle','aggregate_lifecycle.producer','aggregate_lifecycle.snapshot','aggregate_small','aggregate_small.producer',
    'production','production.producer','aggregate_claims','aggregate_claims.bindings','aggregate_claims.input','aggregate_claims.prepare_mixed',
    'mixed_claims','mixed_claims.packet','delta','delta.packet','delta.receiver','delta_claims','delta_claims.claims','delta_claims.receiver',
    'admission','admission.bindings','admission.verifier','modules','modules.codec','release_production','release_production.producer',
    'release_production.adoption','admission.pin_phase','admission.trust','admission.clean_refusal','release_production.launch_contract')
$corePins=@(); foreach($module in $core) {
    $relative=$module.Replace('.','/')
    if ($module.Contains('.')) { $relative+='.py' } else { $relative+='/__init__.py' }
    $logical='v5/'+$relative
    if (-not $sources.Contains($logical)) { throw 'CORE_SOURCE_MISSING' }
    $corePins+=RelativePin ('sdk/'+$logical) $sources[$logical]
}
$baseManifest=ReadKnown $basis.base_manifest.path $basis.base_manifest.sha256
$baseRuntime=@()
foreach($row in $oldProfile.base_profile.support_profile.runtime_pins) {
    $prefix=$installation+'\base\receiver\runtime\python\'
    if (-not $row.path.StartsWith($prefix,[StringComparison]::Ordinal)) { continue }
    $relative=$row.path.Substring(($installation+'\base\').Length).Replace('\','/')
    $baseRow=$baseManifest.files.$relative
    if ($row.bytes -ne $baseRow.bytes -or $row.sha256 -cne $baseRow.sha256) { throw 'BASE_RUNTIME_ROLE_CHANGED' }
    [void](Remember ([ordered]@{path=(Join-Path $basis.base_root $relative.Replace('/','\'));bytes=$baseRow.bytes;sha256=$baseRow.sha256}))
    $baseRuntime+=RelativePin ('base/'+$relative) $baseRow
}
if ($baseRuntime.Count -ne 16 -or $corePins.Count -ne 31) { throw 'EXACT_CORE_AND_BASE_RUNTIME' }
$runtimePins=@($baseRuntime)+@($corePins)+@((RelativePin 'sdk/v5/aggregate_small/operator.py' $sources['v5/aggregate_small/operator.py']),
    (RelativePin 'sdk/v5/release_production/operator.py' $sources['v5/release_production/operator.py']))
if ($runtimePins.Count -ne 49 -or @($runtimePins.path | Sort-Object -Unique).Count -ne 49) { throw 'EXACT_SUPPORT_RUNTIME_49' }
$artifacts=[ordered]@{}
foreach($role in @('stage_host','snapshot_host','guest_image')) {
    $row=$componentDescriptor.roles.$role
    $artifacts[$role]=Remember ([ordered]@{path=(Join-Path $installation $row.path.Replace('/','\'));bytes=$row.bytes;sha256=$row.sha256})
}
$support=[ordered]@{
    schema='DMKN_V5_PRODUCER_PROFILE_V1';supervisor_manifest=(RelativePin 'base/RELEASE-MANIFEST.json' $basis.base_manifest)
    host=(RelativePin 'assets/producer/stage_host.exe' $artifacts['stage_host'])
    python=(RelativePin 'base/receiver/runtime/python/python.exe' $baseManifest.files.'receiver/runtime/python/python.exe')
    python_dll=(RelativePin 'base/receiver/runtime/python/python314.dll' $baseManifest.files.'receiver/runtime/python/python314.dll')
    source_pins=@((RelativePin 'sdk/v5/production/__init__.py' $sources['v5/production/__init__.py']),
                 (RelativePin 'sdk/v5/production/producer.py' $sources['v5/production/producer.py']))
    runtime_pins=$runtimePins;image_id=$producerImage;foundation=$componentDescriptor.foundation;policy=$componentDescriptor.policy
}
$template=[ordered]@{schema='DMKN_RELEASE_PRODUCER_PROFILE_TEMPLATE_V1';support_profile=$support;source_pins=$corePins
    base_source_pins=@((RelativePin 'sdk/v5/aggregate_small/__init__.py' $sources['v5/aggregate_small/__init__.py']),
                      (RelativePin 'sdk/v5/aggregate_small/producer.py' $sources['v5/aggregate_small/producer.py']))
    stage_memory_ceiling_mib=$oldProfile.base_profile.stage_memory_ceiling_mib}
if ($template.stage_memory_ceiling_mib -ne 4096) { throw 'RETAINED_STAGE_CEILING' }
$operativePaths=@($runtimePins.path)+@($support.python.path,$support.python_dll.path,$support.supervisor_manifest.path,
    'base/operator/commons.py','base/receiver/helpers/domains.py','base/receiver/helpers/run_stage.py',
    'assets/producer/stage_host.exe','assets/producer/snapshot_host.exe','assets/producer/aggregate_image.bin',
    'production/ARTIFACTS.json','V5-RELEASE.json')
if ($operativePaths.Count -ne 60 -or @($operativePaths | Sort-Object -Unique).Count -ne 60) { throw 'EXACT_OPERATIVE_60' }
$builder=$overlay+'body_location/distribution.py'
$builderPin=Remember (Pin (Join-Path $projectRoot $builder.Replace('/','\')) $BuilderSha256 1048576)
$runner='tools/Run-V5-Check.py'; $runnerSha='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
[void](Remember (Pin (Join-Path $projectRoot $runner.Replace('/','\')) $runnerSha 1048576))
$runtime=[ordered]@{}
$pythonPrefix=$basis.base_root+'\receiver\runtime\python\'
foreach($entry in $buildBasis.runtime_pins.psobject.Properties) {
    if ($entry.Name.StartsWith($pythonPrefix,[StringComparison]::Ordinal)) {
        $row=Remember (Pin $entry.Name $entry.Value); $runtime[$row.path]=$row.sha256
    }
}
if ($runtime.Count -ne 18 -or -not $runtime.Contains($buildBasis.argv[0])) { throw 'EXACT_BUILD_PYTHON_18' }
$runtime[$basis.base_manifest.path]=$basis.base_manifest.sha256
$foundationPin=Remember $basis.assets.foundation; $runtime[$foundationPin.path]=$foundationPin.sha256
$contractPin=$sources['v5/release_production/launch_contract.py']; $runtime[$contractPin.path]=$contractPin.sha256
$distributionInput=[ordered]@{}
foreach($entry in $basis.psobject.Properties) { $distributionInput[$entry.Name]=$entry.Value }
$distributionInput.schema='DMKN_V5_DISTRIBUTION_INPUT_V4'; $distributionInput.sdk_sources=$sources; $distributionInput.distribution_source=$builderPin
if ($runtime.Count -ne 21 -or $distributionInput.aggregate_image -cne $consumerImage) { throw 'BUILD_SELECTION_BASIS' }
[void][IO.Directory]::CreateDirectory($prepared)
$pending=Join-Path $prepared 'PREPARATION-PENDING.json'
try {
    $pendingPin=NewJson $pending ([ordered]@{schema='DMKN_INSTALLED_PRODUCER_DISTRIBUTION_PREPARATION_PENDING_V1';status='PENDING'})
    $templatePin=NewJson (Join-Path $prepared 'producer-template.json') $template 1048576
    $distributionInput['production']=[ordered]@{artifacts=$artifacts;profile_template=$templatePin}
    $inputPin=NewJson (Join-Path $prepared 'input.json') $distributionInput
    $runtime[$templatePin.path]=$templatePin.sha256; $runtime[$inputPin.path]=$inputPin.sha256
    if ($runtime.Count -ne 23) { throw 'EXACT_BUILD_RUNTIME_23' }
    $buildSources=[ordered]@{}; $buildSources[$runner]=$runnerSha; $buildSources[$builder]=$BuilderSha256
    $buildSources[$overlay+'release_production/launch_contract.py']=$ContractSha256
    $selection=[ordered]@{schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$buildSources;runtime_pins=$runtime
        argv=@($buildBasis.argv[0],'-I','-S','-B',('{snapshot}\'+$builder.Replace('/','\')),'build',
               $inputPin.path,$inputPin.sha256,(Join-Path $parent 'Mathematical Commons v5'))
        limits=[ordered]@{cpu_seconds=120;wall_seconds=600;memory_mib=128;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}}
    $selectionPin=NewJson (Join-Path $prepared 'build-selection.json') $selection 1048576
    foreach($row in @($originals.Values)) { [void](Pin $row.path $row.sha256); if ((Get-Item -LiteralPath $row.path).Length -ne $row.bytes) { throw 'FINAL_INPUT_SIZE' } }
    if (Test-Path -LiteralPath (Join-Path $component 'PREPARATION-FAILED.json')) { throw 'COMPONENT_PREPARATION_FAILED' }
    [void][IO.Directory]::CreateDirectory($parent)
    $report=[ordered]@{schema='DMKN_INSTALLED_PRODUCER_DISTRIBUTION_PREPARATION_V1';status='PREPARED_NOT_EXECUTED';review=$review
        input=$inputPin;template=$templatePin;selection=$selectionPin;installation_parent=$parent;originals=$originals
        sdk_sources=144;sdk_python_sources=123;consumer_sources=130;preserved_current_sources=130
        added_frozen_sources=7;added_successor_sources=7;preparation_sources=109
        core_sources=31;support_runtime_pins=49;predicted_operative_pins=60;build_runtime_pins=23;build_source_snapshots=3
        consumer_aggregate_image=$consumerImage;producer_aggregate_image=$producerImage;build_executed=$false
        completion_rule='PREPARATION_valid_only_without_PREPARATION-PENDING.json_or_PREPARATION-FAILED.json'}
    $reportPin=NewJson (Join-Path $prepared 'PREPARATION.json') $report
    foreach($row in @($templatePin,$inputPin,$selectionPin,$reportPin,$pendingPin)) { [void](Pin $row.path $row.sha256 8388608) }
    if (@(Get-ChildItem -LiteralPath $prepared -Force).Count -ne 5 -or @(Get-ChildItem -LiteralPath $parent -Force).Count -ne 0) { throw 'PREPARATION_FINAL_CENSUS' }
    [ordered]@{preparation=$reportPin;selection=$selectionPin;input=$inputPin;build_executed=$false} | ConvertTo-Json -Depth 6
    Remove-Item -LiteralPath $pending -ErrorAction Stop
} catch {
    try { [void](NewJson (Join-Path $prepared 'PREPARATION-FAILED.json') ([ordered]@{schema='DMKN_INSTALLED_PRODUCER_DISTRIBUTION_PREPARATION_FAILURE_V1';status='FAILED';error=$_.Exception.Message;build_executed=$false})) }
    catch { throw 'PREPARATION_FAILURE_MARKER_UNCONFIRMED_PENDING_RETAINS_FAILURE' }
    throw
}
