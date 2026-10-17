# Prepare actual selected-frontier documents and one CLI preflight. No host/proof.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'selected-frontier-preflight-01'
$run = Join-Path $checks $name
$profilePath = Join-Path $checks ($name+'-profile.json')
$requestPath = Join-Path $checks ($name+'-request.json')
$selectionPath = Join-Path $checks ($name+'-selection.json')
$planned = Join-Path $checks 'selected-frontier-production-quote-01'
foreach ($path in @($run,$profilePath,$requestPath,$selectionPath,$planned)) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
$runtime = [ordered]@{}
function Pin([string]$path,[string]$expected='') {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -or $item.Length -le 0 -or $item.Length -gt 536870912) { throw 'ORDINARY_BOUNDED_FILE' }
    $hash = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($expected -ne '' -and $hash -cne $expected) { throw ('PIN_CHANGED:'+ $path) }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=$hash}
}
function AddRuntime($pin) {
    $actual = Pin $pin.path $pin.sha256
    if ($actual.bytes -ne $pin.bytes) { throw 'PIN_BYTES' }
    if ($runtime.Contains($pin.path) -and $runtime[$pin.path] -cne $pin.sha256) { throw 'PIN_CONFLICT' }
    $runtime[$pin.path]=$pin.sha256
    $pin
}
function Record([string]$path,[string]$expected='') { AddRuntime (Pin $path $expected) }
function ReadRecord($pin) { Get-Content -LiteralPath $pin.path -Raw -Encoding UTF8 | ConvertFrom-Json }
function SaveNew([string]$path,$value) {
    $raw = [Text.UTF8Encoding]::new($false).GetBytes(($value|ConvertTo-Json -Depth 35)+"`n")
    if ($raw.Length -gt 1048576) { throw 'CONTROL_DOCUMENT_LIMIT' }
    $stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
    Pin $path
}
function BuildRecords([string]$role,[string]$selectionHash) {
    $stem='small-aggregate-'+$role+'-host-build-01'
    $build=Join-Path $checks $stem
    $records=[ordered]@{
        result=(Record (Join-Path $build 'RESULT.json'))
        attempt=(Record (Join-Path $checks ($stem+'-attempt.json')))
        selection=(Record (Join-Path $checks ($stem+'-selection.json')) $selectionHash)
        source_map=(Record (Join-Path $build 'source-map.json'))
        command=(Record (Join-Path $build 'compile-command.json'))
    }
    $result=ReadRecord $records.result
    $attempt=ReadRecord $records.attempt
    if ($result.status -cne ('PASS_SMALL_AGGREGATE_'+$role.ToUpperInvariant()+'_HOST_ONE_LINK_ONLY') -or
        $attempt.result_sha256 -cne $records.result.sha256 -or $attempt.status -cne $result.status -or
        $result.job.active_processes -ne 0 -or $result.job.terminated_processes -ne 0 -or
        (Test-Path -LiteralPath (Join-Path $build 'FINALIZATION-FAILED.json'))) { throw 'BUILD_NOT_ADOPTABLE' }
    $map=ReadRecord $records.source_map
    foreach ($property in $map.psobject.Properties) {
        $held=Record (Join-Path (Join-Path $build 'source') $property.Name) $property.Value.sha256
        if ($held.bytes -ne $property.Value.bytes) { throw 'BUILD_SOURCE_BYTES' }
    }
    $null=AddRuntime $result.executable
    $records
}
$templatePin=Record (Join-Path $checks 'module-base-production-01/profile.json') '71af83f7c4822d8d2a322e93dda5f08a59311614d434ab887cc5c33c318d84d0'
$template=ReadRecord $templatePin
foreach ($pin in @($template.supervisor_manifest,$template.python,$template.python_dll)+@($template.runtime_pins)) { $null=AddRuntime $pin }
$manifest=ReadRecord $template.supervisor_manifest
$install=Split-Path -Parent $template.supervisor_manifest.path
foreach ($relative in @('operator/commons.py','receiver/helpers/domains.py','receiver/helpers/run_stage.py')) {
    $pin=Record (Join-Path $install $relative) $manifest.files.$relative.sha256
    if ($pin.bytes -ne $manifest.files.$relative.bytes) { throw 'SUPERVISOR_SIZE' }
}
$sources=[ordered]@{}
$sourcePins=@{}
foreach ($relative in @('tools/Run-V5-Check.py','software/v5/production/__init__.py','software/v5/production/producer.py','software/v5/aggregate_small/__init__.py','software/v5/aggregate_small/producer.py','software/v5/aggregate_small/operator.py')) {
    $pin=Pin (Join-Path $projectRoot $relative)
    $sources[$relative]=$pin.sha256
    $sourcePins[$relative]=[ordered]@{path=[IO.Path]::GetFullPath((Join-Path (Join-Path $run 'sources') $relative));bytes=$pin.bytes;sha256=$pin.sha256}
}
$stage=BuildRecords 'stage' '049129dacf8b43ea3e4a1796a26098dfb207ddbc80d5c1b49cbfde94fc71fa38'
$snapshotBuild=BuildRecords 'snapshot' 'e4493418256735529f7fc19ed606ea459bf35b613b57680d2e0a31a7b858e4bd'
$imagePaths=[ordered]@{
    result='proof-memo-image-assembly-01/assembly/RESULT.json'
    outer='proof-memo-image-assembly-01/RESULT.json'
    selection='proof-memo-image-assembly-01/selection.json'
    guest_build='proof-memo-guest-build-01/RESULT.json'
    guest_selection='proof-memo-guest-build-01/selection.json'
    guest_source_map='proof-memo-guest-build-01/SOURCE-MAP.json'
    artifact='proof-memo-guest-build-01/ARTIFACT.json'
}
# Identity is fixed by the previously selected real-adoption plan, not by mtime.
$oldPlanPin=Pin (Join-Path $checks 'real-producer-preflight-02-selection.json') '0e6cbd6e160ad1a0753b9b013ad73c2387b6d00fa234f04d7d187a89c0986b3a'
$oldPlan=ReadRecord $oldPlanPin
$imageAdoption=[ordered]@{}
foreach ($key in $imagePaths.Keys) {
    $path=Join-Path $checks $imagePaths[$key]
    $expected=$oldPlan.runtime_pins.$path
    if (-not $expected) { throw 'RETAINED_IMAGE_PIN_MISSING' }
    $imageAdoption[$key]=Record $path $expected
}
$imageResult=ReadRecord $imageAdoption.result
$image=AddRuntime $imageResult.image
$layout=Join-Path $checks 'selected-frontier-layout-01'
$screen=[ordered]@{
    result=(Record (Join-Path $layout 'evidence/RESULT.json'))
    outer=(Record (Join-Path $layout 'RESULT.json'))
    selection=(Record (Join-Path $layout 'selection.json') '05888ba9f7fffb600c6b117f39bdfcb8e0b58b870ed311147a557ccd80dfcb45')
    configuration=(Record (Join-Path $layout 'evidence/configuration.json') '02cccc1cda2ac7a6a4971f5e077e04b26fcfa4dc384ff01cf84bfa4c3d5b6431')
    command=(Record (Join-Path $layout 'evidence/COMMAND.json'))
}
$screenResult=ReadRecord $screen.result
$outer=ReadRecord $screen.outer
if ($screenResult.status -cne 'PASS_ONE_AGGREGATE_EXECUTION_CAPSULE_ONLY' -or
    $outer.result.status -cne 'COMMAND_EXITED_ZERO_AND_CLOSED' -or
    $outer.result.final_job.active_processes -ne 0 -or $outer.result.final_job.terminated_processes -ne 0 -or
    $outer.selection_sha256 -cne $screen.selection.sha256 -or
    $screenResult.actual_result.segments -ne 167 -or $screenResult.actual_result.assumptions -ne 1 -or
    (Test-Path -LiteralPath (Join-Path $layout 'FINALIZATION-FAILED.json'))) { throw 'COMPLETE_FRONTIER_REQUIRED' }
foreach ($key in $snapshotBuild.Keys) {
    if ($screenResult.host_build.$key.sha256 -cne $snapshotBuild[$key].sha256) { throw 'SNAPSHOT_BUILD_MISMATCH' }
}
$parent=Record (Join-Path $checks 'module-base-production-01/finish-0/receipt.bin') '850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47'
$session=[ordered]@{
    image=$image
    wire=(Record (Join-Path $layout 'evidence/wire.bin'))
    expected=(Record (Join-Path $layout 'evidence/header.bin'))
    capsule=(AddRuntime $screenResult.capsule)
    parents=@($parent)
    session_binding=$screenResult.actual_result.session_binding
    capsule_binding=$screenResult.actual_result.capsule_binding
    cycles=$screenResult.cycles;po2=$screenResult.segment_po2
    segments=$screenResult.actual_result.segments;assumptions=$screenResult.actual_result.assumptions
    snapshot_evidence=$screen
}
$template.host=(ReadRecord $stage.result).executable
$template.image_id=$imageResult.image_id
$template.source_pins=@($sourcePins['software/v5/production/producer.py'],$sourcePins['software/v5/production/__init__.py'])
$profile=[ordered]@{
    schema='DMKN_V5_SMALL_AGGREGATE_PRODUCER_PROFILE_V1';support_profile=$template
    stage_memory_ceiling_mib=4096
    source_pins=@($sourcePins['software/v5/aggregate_small/producer.py'],$sourcePins['software/v5/aggregate_small/__init__.py'])
    relation_image='9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e'
    host_build=$stage;image_adoption=$imageAdoption
}
$stages=[ordered]@{}
$caps=@{segment=1200;lift=250;join=250;resolve=600;finish=300}
$walls=@{segment=240;lift=150;join=150;resolve=600;finish=120}
foreach ($kind in @('segment','lift','join','resolve','finish')) {
    $stages[$kind]=[ordered]@{cpu_seconds=$caps[$kind];wall_seconds=$walls[$kind];memory_mib=4096;active_processes=2;stdout_bytes=65536;stderr_bytes=65536;output_bytes=524288}
}
$budget=[ordered]@{worker_cpu_seconds=500000;controller_cpu_seconds=7200;wall_seconds=172800;output_bytes=2415919104;output_entries=8192;stages=$stages}
$basePin=Record (Join-Path $checks 'module-base-production-01/RESULT.json') '1ccfa4835ce7cf8ef62386bd2fc82a548d7e9b82db948a879ab9809f36027749'
$base=ReadRecord $basePin
$carry=[ordered]@{
    worker_cpu_seconds=($base.worker_cpu_charge_this_attempt+$base.prior_allowance_worker_charge+$base.carried_external_costs.worker_cpu_seconds)
    controller_cpu_seconds=($base.controller_cpu_seconds+$base.prior_allowance_controller_cpu+$base.carried_external_costs.controller_cpu_seconds)
    wall_seconds=($base.wall_seconds+$base.prior_allowance_wall+$base.carried_external_costs.wall_seconds)
    scope='Planning-only known subtotal: retained base I including carried prefix, both small host links, both failed po18 layouts and selected FIRST layout. No funding. Other preserved development/build/search/service costs remain excluded, not zero; active wall sums are not calendar time or benefit.'
}
foreach ($records in @($stage,$snapshotBuild)) {
    $value=ReadRecord $records.result
    $carry.worker_cpu_seconds+=$value.job.cpu_seconds
    $carry.controller_cpu_seconds+=$value.controller_cpu_seconds
    $carry.wall_seconds+=$value.wall_seconds
}
foreach ($stem in @('small-aggregate-layout-01','small-aggregate-layout-02','selected-frontier-layout-01')) {
    $pin=Record (Join-Path (Join-Path $checks $stem) 'RESULT.json')
    $value=ReadRecord $pin
    $carry.worker_cpu_seconds+=$value.result.final_job.cpu_seconds
    $carry.controller_cpu_seconds+=$value.wrapper_cpu_seconds
    $carry.wall_seconds+=$value.wall_seconds
}
$request=[ordered]@{
    schema='DMKN_V5_SMALL_AGGREGATE_PRODUCER_REQUEST_V1'
    allowance_id='c1930fbf721a7f373aa0a339d895fc9a9287f9f0a11ee88f70c7f1f5d80e0160'
    session=$session;checkpoints=@();output_directory=$planned;stage_limit=502
    budget=$budget;prior_attempts=@();carried_external_costs=$carry
}
$profilePin=AddRuntime (SaveNew $profilePath $profile)
$requestPin=AddRuntime (SaveNew $requestPath $request)
$selection=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($template.python.path,'-I','-S','-B','{snapshot}\software\v5\aggregate_small\operator.py','preflight','--profile',$profilePath,'--profile-sha256',$profilePin.sha256,'--request',$requestPath,'--request-sha256',$requestPin.sha256,'--owner-report','{output}\operator-result.json')
    limits=[ordered]@{cpu_seconds=30;wall_seconds=90;memory_mib=512;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$selected=SaveNew $selectionPath $selection
[ordered]@{selection=$selected;profile=$profilePin;request=$requestPin;sources=$sources.Count;runtime_pins=$runtime.Count;executed=$false;proof_funded=$false}|ConvertTo-Json -Depth 4
