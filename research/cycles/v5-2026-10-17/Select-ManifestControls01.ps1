# Prepare one ten-case finish-only native manifest gate. No test/host/proof launch.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'selected-frontier-manifest-controls-01'
$run = Join-Path $checks $name
$configPath = Join-Path $checks ($name+'-configuration.json')
$selectionPath = Join-Path $checks ($name+'-selection.json')
foreach ($path in @($run,$configPath,$selectionPath)) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
$outerRuntime = [ordered]@{}
$innerRuntime = [ordered]@{}
function Pin([string]$path,[string]$expected='') {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -or
        $item.Length -le 0 -or $item.Length -gt 134217728 -or
        [IO.Path]::GetFullPath($path) -cne $item.FullName) { throw ('ORDINARY_BOUNDED_FILE:'+ $path) }
    $hash = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($expected -ne '' -and $hash -cne $expected) { throw ('PIN_CHANGED:'+ $path) }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=$hash}
}
function AddOuter($pin) {
    $actual = Pin $pin.path $pin.sha256
    if ($actual.bytes -ne $pin.bytes) { throw 'PIN_BYTES' }
    if ($outerRuntime.Contains($pin.path) -and $outerRuntime[$pin.path] -cne $pin.sha256) { throw 'OUTER_PIN_CONFLICT' }
    $outerRuntime[$pin.path]=$pin.sha256
    $pin
}
function Record([string]$path,[string]$expected='') { AddOuter (Pin $path $expected) }
function AddInner($pin) {
    $null = AddOuter $pin
    if ($innerRuntime.Contains($pin.path) -and $innerRuntime[$pin.path].sha256 -cne $pin.sha256) { throw 'INNER_PIN_CONFLICT' }
    $innerRuntime[$pin.path]=$pin
}
function ReadRecord($pin) { Get-Content -LiteralPath $pin.path -Raw -Encoding UTF8 | ConvertFrom-Json }
function SaveNew([string]$path,$value) {
    $raw = [Text.UTF8Encoding]::new($false).GetBytes(($value|ConvertTo-Json -Depth 25)+"`n")
    if ($raw.Length -gt 1048576) { throw 'CONTROL_DOCUMENT_LIMIT' }
    $stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
    Pin $path
}

$templatePin = Record (Join-Path $checks 'module-base-production-01/profile.json') '71af83f7c4822d8d2a322e93dda5f08a59311614d434ab887cc5c33c318d84d0'
$template = ReadRecord $templatePin
$supervisorManifest = AddOuter $template.supervisor_manifest
if ($supervisorManifest.sha256 -cne 'a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed') { throw 'ADOPTED_SUPERVISOR_MANIFEST' }
foreach ($pin in @($template.python,$template.python_dll)+@($template.runtime_pins)) { AddInner $pin }
$manifest = ReadRecord $supervisorManifest
$install = Split-Path -Parent $supervisorManifest.path
foreach ($relative in @('operator/commons.py','receiver/helpers/domains.py','receiver/helpers/run_stage.py')) {
    $pin = Pin (Join-Path $install $relative) $manifest.files.$relative.sha256
    if ($pin.bytes -ne $manifest.files.$relative.bytes) { throw 'SUPERVISOR_SOURCE_BYTES' }
    AddInner $pin
}

$sources = [ordered]@{}
$expectedSources = [ordered]@{
    'tools/Run-V5-Check.py'='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
    'software/v5/production/__init__.py'='c66f4ce32e6a929bf3d0a178fb9c62e6aaaebe45b441a98e4d2bc10b68d916ae'
    'software/v5/production/producer.py'='5555e944d7473731e3e9095e85c5c57ce89c5f59187f78c5b248b4c1227532f3'
    'software/v5/aggregate_small/manifest_controls.py'='ab897b28fbbdc930e9f775ac8461e07aaf5b6d284da4c329930f6997df5589eb'
}
foreach ($relative in $expectedSources.Keys) {
    $pin = Pin (Join-Path $projectRoot $relative) $expectedSources[$relative]
    $sources[$relative]=$pin.sha256
    if ($relative -cne 'tools/Run-V5-Check.py') {
        # These do not exist until Run-V5-Check makes its immutable snapshot.
        # They belong only in the child's configuration, never outer runtime_pins.
        $future = [IO.Path]::GetFullPath((Join-Path (Join-Path $run 'sources') $relative))
        $innerRuntime[$future]=[ordered]@{path=$future;bytes=$pin.bytes;sha256=$pin.sha256}
    }
}

$stageBuild = Join-Path $checks 'small-aggregate-stage-host-build-01'
$stageResultPin = Record (Join-Path $stageBuild 'RESULT.json') '2c201aa68a50ccc93c90f73ae8aba5d924cef858bbec900f858d738b0135e499'
$stageResult = ReadRecord $stageResultPin
$stageAttemptPin = Record (Join-Path $checks 'small-aggregate-stage-host-build-01-attempt.json')
$stageAttempt = ReadRecord $stageAttemptPin
$null = Record (Join-Path $checks 'small-aggregate-stage-host-build-01-selection.json') '049129dacf8b43ea3e4a1796a26098dfb207ddbc80d5c1b49cbfde94fc71fa38'
$stageMapPin = Record (Join-Path $stageBuild 'source-map.json')
$stageMap = ReadRecord $stageMapPin
$null = Record (Join-Path $stageBuild 'compile-command.json')
if ($stageResult.status -cne 'PASS_SMALL_AGGREGATE_STAGE_HOST_ONE_LINK_ONLY' -or
    $stageAttempt.result_sha256 -cne $stageResultPin.sha256 -or $stageAttempt.status -cne $stageResult.status -or
    $stageResult.job.active_processes -ne 0 -or $stageResult.job.terminated_processes -ne 0 -or
    (Test-Path -LiteralPath (Join-Path $stageBuild 'FINALIZATION-FAILED.json'))) { throw 'ADOPTED_STAGE_BUILD_REQUIRED' }
foreach ($property in $stageMap.psobject.Properties) {
    $pin = Record (Join-Path (Join-Path $stageBuild 'source') $property.Name) $property.Value.sha256
    if ($pin.bytes -ne $property.Value.bytes) { throw 'STAGE_SOURCE_BYTES' }
}
$hostPin = AddOuter $stageResult.executable
if ($hostPin.bytes -ne 68036608 -or $hostPin.sha256 -cne '8f8e444ddd9029906fee60a073a701bdd34c8b095d54f81f2554bfe1e91ad8ee') { throw 'EXACT_STAGE_BINARY' }
AddInner $hostPin

$layout = Join-Path $checks 'selected-frontier-layout-01'
$layoutResultPin = Record (Join-Path $layout 'evidence/RESULT.json') 'da1acf4d2469e92ffde297648702fe4c281406353fb3691a4a7d5ffa3efd484e'
$layoutOuterPin = Record (Join-Path $layout 'RESULT.json') 'f11c567f70d5543fe648f32df2bb254736deada086bcc40e3f6b01c87d493d6f'
$layoutCommandPin = Record (Join-Path $layout 'evidence/COMMAND.json') '98144eda4a410695233d5388f7e3a5e41dd64b22eb4098d41a95e31424690a83'
$null = Record (Join-Path $layout 'selection.json') '05888ba9f7fffb600c6b117f39bdfcb8e0b58b870ed311147a557ccd80dfcb45'
$layoutResult = ReadRecord $layoutResultPin
$layoutOuter = ReadRecord $layoutOuterPin
if ($layoutResult.status -cne 'PASS_ONE_AGGREGATE_EXECUTION_CAPSULE_ONLY' -or
    $layoutOuter.result.status -cne 'COMMAND_EXITED_ZERO_AND_CLOSED' -or
    $layoutOuter.result.child_exit_code -ne 0 -or -not $layoutOuter.result.job_closed -or
    -not $layoutOuter.result.direct_child_reaped -or $layoutOuter.result.termination_requested -or
    @($layoutOuter.result.cleanup_errors).Count -ne 0 -or
    $layoutOuter.result.final_job.active_processes -ne 0 -or $layoutOuter.result.final_job.terminated_processes -ne 0 -or
    $layoutResult.actual_result.segments -ne 167 -or $layoutResult.actual_result.assumptions -ne 1 -or
    $layoutResult.actual_result.session_binding -cne '9c87448ba08ae98273ac6fc1df8a41a22716db8be686ce473eb5fba874a1475d' -or
    $layoutResult.actual_result.capsule_binding -cne 'e56cb33f432a4c5bbdb0624eb2a072db48562e26c77fc20cefd0da8831585a2b' -or
    (Test-Path -LiteralPath (Join-Path $layout 'FINALIZATION-FAILED.json')) -or
    (Test-Path -LiteralPath (Join-Path $layout 'evidence/FINALIZATION-FAILED.json'))) { throw 'COMPLETE_SELECTED_LAYOUT_REQUIRED' }
$imageResultPin = Record (Join-Path $checks 'proof-memo-image-assembly-01/assembly/RESULT.json') '8a2174ad097333a54f3a314d63f0e646607a639aa5755efdd31c2ee1d08d43ea'
$imageResult = ReadRecord $imageResultPin
$imagePin = AddOuter $imageResult.image
$capsulePin = AddOuter $layoutResult.capsule
if ($capsulePin.bytes -ne 32965324 -or $capsulePin.sha256 -cne '6e41621e2595c252328eaf5f34862c6d6f913caecb68117406bcd616a61b44a5') { throw 'COMPLETE_SELECTED_CAPSULE_PIN' }
$inputs = [ordered]@{
    host=$hostPin;image=$imagePin
    wire=(Record (Join-Path $layout 'evidence/wire.bin') '898660ddeea92cefccbf793e35b1ee49ef4867c9daec24b5344f37a1ed375500')
    expected=(Record (Join-Path $layout 'evidence/header.bin') '49dd845edaec83f5b0cba5af38653f768e51ed95a4bb6ea7824c10bdd1c3169e')
    capsule=$capsulePin
    parent=(Record (Join-Path $checks 'module-base-production-01/finish-0/receipt.bin') '850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47')
    layout_result=$layoutResultPin;layout_outer=$layoutOuterPin;layout_command=$layoutCommandPin
}
$configuration = [ordered]@{
    schema='DMKN_SMALL_NATIVE_MANIFEST_CONTROLS_V1';inputs=$inputs
    supervisor_manifest=$supervisorManifest;runtime_pins=@($innerRuntime.Values)
    case_limits=[ordered]@{cpu_seconds=15;wall_seconds=20;memory_mib=1024;active_processes=1;stdout_bytes=65536;stderr_bytes=65536}
    total_limits=[ordered]@{worker_cpu_seconds=150;controller_cpu_seconds=30;wall_seconds=240;output_bytes=16777216;output_entries=128}
    output_directory=(Join-Path $run 'evidence')
}
if ($sources.Count -ne 4 -or $innerRuntime.Count -ne 25) { throw 'EXACT_FOUR_SOURCE_25_RUNTIME_CLOSURE' }
foreach ($path in $outerRuntime.Keys) {
    if ($path.StartsWith(($run+'\'),[StringComparison]::OrdinalIgnoreCase)) { throw 'FUTURE_SNAPSHOT_IN_OUTER_RUNTIME' }
}
$configPin = AddOuter (SaveNew $configPath $configuration)
$selection = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$outerRuntime
    argv=@($template.python.path,'-I','-S','-B','{snapshot}\software\v5\aggregate_small\manifest_controls.py',$configPath,$configPin.sha256)
    limits=[ordered]@{cpu_seconds=210;wall_seconds=300;memory_mib=1536;active_processes=3;stdout_bytes=1048576;stderr_bytes=1048576}
}
$selected = SaveNew $selectionPath $selection
[ordered]@{selection=$selected;configuration=$configPin;sources=$sources.Count;runtime_pins=$outerRuntime.Count;inner_runtime_pins=$innerRuntime.Count;executed=$false;proof_funded=$false}|ConvertTo-Json -Depth 4
