# Prepare one typed-owner adoption/control check. No host, compile or proof.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'typed-production-controls-01'
$run = Join-Path $checks $name
$profilePath = Join-Path $checks ($name+'-profile.json')
$requestPath = Join-Path $checks ($name+'-request.json')
$selectionPath = Join-Path $checks ($name+'-selection.json')
$planned = Join-Path $checks 'typed-general36-production-quote-01'
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
    if ($runtime.Contains($pin.path)) {
        if ($runtime[$pin.path] -cne $pin.sha256) { throw 'PIN_CONFLICT' }
    } else { $runtime[$pin.path]=$pin.sha256 }
    $pin
}
function Record([string]$path,[string]$expected='') { AddRuntime (Pin $path $expected) }
function ReadRecord($pin) { Get-Content -LiteralPath $pin.path -Raw -Encoding UTF8 | ConvertFrom-Json }
function ExactPin($pin) {
    $actual=Record $pin.path $pin.sha256
    if ($actual.bytes -ne $pin.bytes) { throw 'PIN_BYTES' }
    $actual
}
function SaveNew([string]$path,$value) {
    $raw = [Text.UTF8Encoding]::new($false).GetBytes(($value|ConvertTo-Json -Depth 40)+"`n")
    if ($raw.Length -gt 1048576) { throw 'CONTROL_DOCUMENT_LIMIT' }
    $stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
    Pin $path
}
function BuildRecords([string]$stem,[string]$selectionHash,[string]$commandFile,[string]$expectedStatus) {
    $build=Join-Path $checks $stem
    $records=[ordered]@{
        result=(Record (Join-Path $build 'RESULT.json'))
        attempt=(Record (Join-Path $checks ($stem+'-attempt.json')))
        selection=(Record (Join-Path $checks ($stem+'-selection.json')) $selectionHash)
        source_map=(Record (Join-Path $build 'source-map.json'))
        command=(Record (Join-Path $build $commandFile))
    }
    $result=ReadRecord $records.result
    $attempt=ReadRecord $records.attempt
    if ($result.status -cne $expectedStatus -or $attempt.status -cne $expectedStatus -or
        $attempt.result_sha256 -cne $records.result.sha256 -or
        $result.selection_sha256 -cne $records.selection.sha256 -or
        $result.job.active_processes -ne 0 -or $result.job.terminated_processes -ne 0 -or
        (Test-Path -LiteralPath (Join-Path $build 'FINALIZATION-FAILED.json'))) { throw 'BUILD_NOT_ADOPTABLE' }
    # Product adopters validate retained maps, commands, source bytes and lineage.
    # Do not rescan the historical compiler/toolchain as a current runtime.
    $null=ExactPin $result.executable
    $records
}
$templatePin=Record (Join-Path $checks 'module-base-production-01/profile.json') '71af83f7c4822d8d2a322e93dda5f08a59311614d434ab887cc5c33c318d84d0'
$template=ReadRecord $templatePin
foreach ($pin in @($template.supervisor_manifest,$template.python,$template.python_dll)+@($template.runtime_pins)) { $null=ExactPin $pin }
$manifest=ReadRecord $template.supervisor_manifest
$install=Split-Path -Parent $template.supervisor_manifest.path
foreach ($relative in @('operator/commons.py','receiver/helpers/domains.py','receiver/helpers/run_stage.py')) {
    $pin=Record (Join-Path $install $relative) $manifest.files.$relative.sha256
    if ($pin.bytes -ne $manifest.files.$relative.bytes) { throw 'SUPERVISOR_SIZE' }
}
$modules=@(
    'aggregate_lifecycle','aggregate_lifecycle.producer','aggregate_lifecycle.snapshot',
    'aggregate_small','aggregate_small.producer','production','production.producer',
    'aggregate_claims','aggregate_claims.bindings','aggregate_claims.input','aggregate_claims.prepare_mixed',
    'mixed_claims','mixed_claims.packet','delta','delta.packet','delta.receiver',
    'delta_claims','delta_claims.claims','delta_claims.receiver',
    'admission','admission.bindings','admission.verifier','modules','modules.codec',
    'typed_production','typed_production.producer','typed_production.snapshot_adoption',
    'typed_production.host_adoption','typed_production.image_adoption')
$sources=[ordered]@{}
$sourcePins=@{}
$corePins=@()
$entryPins=@()
foreach ($module in @($modules)+@('aggregate_small.operator','typed_production.operator','typed_production.test_adoption')) {
    $rel=$module.Replace('.','/')
    if ($module.Contains('.')) { $rel+='.py' } else { $rel+='/__init__.py' }
    $relative='software/v5/'+$rel
    $pin=Pin (Join-Path $projectRoot $relative)
    $sources[$relative]=$pin.sha256
    $staged=[ordered]@{path=[IO.Path]::GetFullPath((Join-Path (Join-Path $run 'sources') $relative));bytes=$pin.bytes;sha256=$pin.sha256}
    $sourcePins[$relative]=$staged
    if ($module -in $modules) { $corePins+=,$staged }
    if ($module -ne 'typed_production.test_adoption') { $entryPins+=,$staged }
}
$sources['tools/Run-V5-Check.py']=(Pin (Join-Path $projectRoot 'tools/Run-V5-Check.py')).sha256
if ($sources.Count -ne 33 -or $corePins.Count -ne 29 -or $entryPins.Count -ne 31) { throw 'EXACT_SOURCE_COUNTS' }
# The prospective production wrapper is read-only control input, not executed.
$null=Record (Join-Path $projectRoot 'tools/Run-V5-TypedProduction.py')
$stage=BuildRecords 'prover-allocation-build-01' '7a548b3f74c0c5bbe8bc2ba68e408a3dfdf22addefb9410b1a25f5d8be5d13ff' 'compile-commands.json' 'PASS_PROVER_ALLOCATION_FIVE_STEP_COMPILE_ONLY'
$snapshotBuild=BuildRecords 'small-aggregate-snapshot-host-build-01' 'e4493418256735529f7fc19ed606ea459bf35b613b57680d2e0a31a7b858e4bd' 'compile-command.json' 'PASS_SMALL_AGGREGATE_SNAPSHOT_HOST_ONE_LINK_ONLY'
$imageRows=@(
    @('result','typed-guest-image-assembly-01/assembly/RESULT.json','4c26d075d850ff38a0922dbbdfad00303d16b49dee41f71a859f3777166e530c'),
    @('outer','typed-guest-image-assembly-01/RESULT.json','174878e768ed578e0a4f239de8423591ebf4ea34f09213e52c84aff46362b33b'),
    @('selection','typed-guest-image-assembly-01/selection.json','d911dbfd934b5e43c2743403076afd47794185a593f225582f1bfb73ab025362'),
    @('guest_build','typed-guest-build-01/RESULT.json','b1b4f7a82aabddc5dd3349a4f82ba79e846517a6db94c3a3d911702c7d6576a4'),
    @('guest_selection','typed-guest-build-01/selection.json','bab4fd3e335683be859a1f38843b415eff13a2dcb9c215c931ae1d6f463911e3'),
    @('guest_source_map','typed-guest-build-01/SOURCE-MAP.json','a05c6e910664260b05c4c875ea0df6545a4dd969b608f22a3b9585e590885356'),
    @('artifact','typed-guest-build-01/ARTIFACT.json','f1d732f34287a63096f816fcc62f0724a470f6dc3dc725ae6b816787e08800ff'),
    @('guest_attempt','typed-guest-build-01-attempt.json','b807f0c299f40fa509a63099d2e75b4a92bf941062c60376bcf378a9657dc6e7'),
    @('guest_recipes','typed-guest-build-01/RECIPES.json','fa11546f7fe58c752f58830429760c3958566ca36b6da7051fe2142306fa0ac5'),
    @('assembly_command','typed-guest-image-assembly-01/assembly/COMMAND.json','9aa845df63ab85be75b4d54d2f3be94ee23d2dcd9580c825f662f9e3e60d2145'))
$imageAdoption=[ordered]@{}
foreach($row in $imageRows) { $imageAdoption[$row[0]]=Record (Join-Path $checks $row[1]) $row[2] }
$imageResult=ReadRecord $imageAdoption.result
$image=ExactPin $imageResult.image
$layout=Join-Path $checks 'restricted-support-matched-execution-01'
$evidenceRows=@(
    @('result','pair/RESULT.json','07e8840f423f322dda398deb7c83bd9b1eb975935f7547be26ec0c2708144451'),
    @('outer','RESULT.json','a05b2a58bbb3d88eeffa43858e4ad02749b35e904c37e0b4ee5081d460ee6209'),
    @('selection','selection.json','83c64d369149cdc1e2fc840925b215a54ee094ea778810b29e96fb1b543b9235'),
    @('configuration','../restricted-support-matched-execution-01-configuration.json','6afff33289b12bc8d11cd172c50cdc823d1612ee0eac8602d2617ef233687bf4'),
    @('derivation','pair/derivation.json','3156948f6cf3925363b55136f48708c52674b9dc82e8e4d0fe5df84050dd9986'),
    @('arm','pair/general/arm-result.json','a7324dc88040b14bd2797c6ac2b1ce955d52fb7e4affefcea4852b52f40d247b'),
    @('command','pair/general/command/command.json','c969a78647b360130224f4f449c8b8e56d145b971ec1bd5e53416f8adabdcc4a'),
    @('job','pair/general/host-job.json','15317a585ec3343123ab6e087daf7661eac4748903d471d806a16d6b806dc99f'),
    @('diagnostic','pair/general/diagnostic.json','cba882b3f5ec8d60db90794f610500f442fbfce05bda892cbc63cade181041ae'),
    @('stdout','pair/general/command/stdout.txt','a9277c23b92389d89d3381600af057cdc1b66b1b2ea27a4a6f7fc17471cd6211'))
$evidence=[ordered]@{}
foreach($row in $evidenceRows) { $evidence[$row[0]]=Record ([IO.Path]::GetFullPath((Join-Path $layout $row[1]))) $row[2] }
$actual=ReadRecord $evidence.stdout
$configuration=ReadRecord $evidence.configuration
$session=[ordered]@{
    image=$image
    wire=(Record (Join-Path $layout 'pair/general/wire.bin') '478a2b4966fe0fcd3d76901a319a07c3fc1d5f9365b8f772e2d6c9f45915624c')
    expected=(Record (Join-Path $layout 'pair/general/header.bin') '2df5af1a7ded10f5693fb9bff07a7849a67e2a22eaaca39475bf85f96546cd15')
    capsule=(Record (Join-Path $layout 'pair/general/aggregate.snapshot') 'adaee31aec796ca62c884a747e8617d06a49b702de5d3793496470d26fb36872')
    parents=@((ExactPin $configuration.receipt))
    session_binding=$actual.session_binding;capsule_binding=$actual.capsule_binding
    cycles=67108864;po2=18;segments=36;assumptions=1;snapshot_evidence=$evidence
}
$template.host=(ReadRecord $stage.result).executable
$template.image_id=$imageResult.image_id
$template.source_pins=@($sourcePins['software/v5/production/producer.py'],$sourcePins['software/v5/production/__init__.py'])
$template.runtime_pins=@($template.runtime_pins)+@($entryPins)
if ($template.runtime_pins.Count -gt 128) { throw 'PRODUCER_SUPPORT_RUNTIME_BOUND' }
$baseProfile=[ordered]@{
    schema='DMKN_V5_SMALL_AGGREGATE_PRODUCER_PROFILE_V1';support_profile=$template
    stage_memory_ceiling_mib=4096
    source_pins=@($sourcePins['software/v5/aggregate_small/producer.py'],$sourcePins['software/v5/aggregate_small/__init__.py'])
    relation_image='9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e'
    host_build=$stage;image_adoption=$imageAdoption
}
$profile=[ordered]@{schema='DMKN_TYPED_AGGREGATE_LIFECYCLE_PROFILE_V1';base_profile=$baseProfile;source_pins=$corePins;snapshot_host_build=$snapshotBuild}
$stages=[ordered]@{}
$caps=@{segment=1200;lift=250;join=250;resolve=600;finish=300}
$walls=@{segment=240;lift=150;join=150;resolve=600;finish=120}
foreach ($kind in @('segment','lift','join','resolve','finish')) {
    $stages[$kind]=[ordered]@{cpu_seconds=$caps[$kind];wall_seconds=$walls[$kind];memory_mib=4096;active_processes=2;stdout_bytes=65536;stderr_bytes=65536;output_bytes=524288}
}
$budget=[ordered]@{worker_cpu_seconds=70000;controller_cpu_seconds=1200;wall_seconds=28800;output_bytes=536870912;output_entries=2048;stages=$stages}
$basePin=Record (Join-Path $checks 'module-base-production-01/RESULT.json') '1ccfa4835ce7cf8ef62386bd2fc82a548d7e9b82db948a879ab9809f36027749'
$base=ReadRecord $basePin
$carry=[ordered]@{
    worker_cpu_seconds=($base.worker_cpu_charge_this_attempt+$base.prior_allowance_worker_charge+$base.carried_external_costs.worker_cpu_seconds)
    controller_cpu_seconds=($base.controller_cpu_seconds+$base.prior_allowance_controller_cpu+$base.carried_external_costs.controller_cpu_seconds)
    wall_seconds=($base.wall_seconds+$base.prior_allowance_wall+$base.carried_external_costs.wall_seconds)
    scope='Planning-only known subtotal: retained base I including carried prefix; corrected stage and snapshot-host builds; typed guest build and assembly; failed support/general matched execution including both arms. Other historical builds, failed trials, controls, service and research costs remain excluded, not zero. Active wall sum is not elapsed time or a growth-benefit claim. No proof funding.'
}
foreach($pin in @($stage.result,$snapshotBuild.result,$imageAdoption.guest_build)) {
    $value=ReadRecord $pin
    $carry.worker_cpu_seconds+=$value.job.cpu_seconds
    $carry.controller_cpu_seconds+=$value.controller_cpu_seconds
    $carry.wall_seconds+=$value.wall_seconds
}
foreach($pin in @($imageAdoption.outer,$evidence.outer)) {
    $value=ReadRecord $pin
    $carry.worker_cpu_seconds+=$value.result.final_job.cpu_seconds
    $carry.controller_cpu_seconds+=$value.wrapper_cpu_seconds
    $carry.wall_seconds+=$value.wall_seconds
}
$hashMaker=[Security.Cryptography.SHA256]::Create()
try { $allowance=([BitConverter]::ToString($hashMaker.ComputeHash([Text.Encoding]::ASCII.GetBytes('DMKN_TYPED_GENERAL36_CAPABILITY_01')))).Replace('-','').ToLowerInvariant() } finally { $hashMaker.Dispose() }
$request=[ordered]@{
    schema='DMKN_V5_SMALL_AGGREGATE_PRODUCER_REQUEST_V1';allowance_id=$allowance
    session=$session;checkpoints=@();output_directory=$planned;stage_limit=1
    budget=$budget;prior_attempts=@();carried_external_costs=$carry
}
$profilePin=AddRuntime (SaveNew $profilePath $profile)
$requestPin=AddRuntime (SaveNew $requestPath $request)
if ($runtime.Count -gt 256) { throw 'OUTER_RUNTIME_BOUND' }
$selection=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($template.python.path,'-I','-S','-B','{snapshot}\software\v5\typed_production\test_adoption.py',
        '--profile',$profilePath,'--profile-sha256',$profilePin.sha256,
        '--request',$requestPath,'--request-sha256',$requestPin.sha256,'--output','{output}\controls')
    limits=[ordered]@{cpu_seconds=90;wall_seconds=180;memory_mib=768;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$selected=SaveNew $selectionPath $selection
[ordered]@{selection=$selected;profile=$profilePin;request=$requestPin;sources=$sources.Count;runtime_pins=$runtime.Count;producer_runtime_pins=$template.runtime_pins.Count;executed=$false;proof_funded=$false}|ConvertTo-Json -Depth 4
