# Prepare one useful five-node prefix from adopted controls; does not launch it.
# Proof funding requires root's separate written decision after outcome adoption.
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$name='typed-general36-prefix-owner-01'
$output=Join-Path $checks 'typed-general36-prefix-01'
$selectionPath=Join-Path $checks ($name+'-selection.json')
$requestPath=Join-Path $checks 'typed-general36-prefix-01-request.json'
foreach($path in @((Join-Path $checks $name),$output,$selectionPath,$requestPath)) {
    if(Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path,[string]$expected='') {
    $item=Get-Item -LiteralPath $path
    if($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -or $item.Length -le 0 -or $item.Length -gt 536870912) { throw 'ORDINARY_BOUNDED_FILE' }
    $hash=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    if($expected -ne '' -and $hash -cne $expected) { throw ('PIN_CHANGED:'+ $path) }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=$hash}
}
function ReadPin($pin) { Get-Content -LiteralPath $pin.path -Raw -Encoding UTF8 | ConvertFrom-Json }
function SaveNew([string]$path,$value) {
    $bytes=[Text.UTF8Encoding]::new($false).GetBytes(($value|ConvertTo-Json -Depth 40)+"`n")
    if($bytes.Length -gt 1048576) { throw 'DOCUMENT_BOUND' }
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($bytes,0,$bytes.Length);$stream.Flush($true) } finally { $stream.Dispose() }
    Pin $path
}
$oldPin=Pin (Join-Path $checks 'typed-production-controls-01-selection.json') 'f30248a9588ae8e09c4c7d0d8cff8735387d1d6e1e56582b6d88c4c09f258c28'
$old=ReadPin $oldPin
$profilePin=Pin (Join-Path $checks 'typed-production-controls-01-profile.json') '1242b0a8430e68032bbedbddcb3c6539fbdc95a2a5cf567936545c5f891246cc'
$oldRequestPin=Pin (Join-Path $checks 'typed-production-controls-01-request.json') 'c420af6e541fbe2744d4d913ed5331b88fb5203b56a719b52f19c9858ccd2f2f'
$profile=ReadPin $profilePin
$request=ReadPin $oldRequestPin
$controlsRoot=Join-Path $checks 'typed-production-controls-01'
$outerPin=Pin (Join-Path $controlsRoot 'RESULT.json') 'e703f8cdd61ac341a8ecd16320cc4c6356cf0dace4b79661c8d1a712dda4096f'
$controlsPin=Pin (Join-Path $controlsRoot 'controls/RESULT.json') '49ad5eb513373fcfb222a2aa55ed542bec0170214f0717c2d00ca4f5ef990041'
$outer=ReadPin $outerPin
$controls=ReadPin $controlsPin
if($outer.selection_sha256 -cne $oldPin.sha256 -or
    $outer.result.status -cne 'COMMAND_EXITED_ZERO_AND_CLOSED' -or $outer.result.child_exit_code -ne 0 -or
    $outer.result.direct_child_reaped -ne $true -or $outer.result.job_closed -ne $true -or
    $outer.result.final_job.active_processes -ne 0 -or $outer.result.final_job.terminated_processes -ne 0 -or
    @($outer.result.cleanup_errors).Count -ne 0 -or
    $controls.schema -cne 'DMKN_TYPED_ADOPTION_CONTROLS_V1' -or $controls.status -cne 'PASS' -or
    $controls.tests_run -ne 10 -or $controls.failures -ne 0 -or $controls.errors -ne 0 -or
    @($controls.process_dispatch_attempts).Count -ne 0 -or $controls.native_calls -ne 0 -or
    $controls.proof_calls -ne 0 -or $controls.mathematical_admission -ne $false -or
    $controls.profile_sha256 -cne $profilePin.sha256 -or $controls.request_sha256 -cne $oldRequestPin.sha256 -or
    $controls.real_quote.full_path_envelope.full_path_fits_requested_envelopes -ne $true -or
    $controls.real_quote.full_path_envelope.missing_host_calls -ne 109 -or
    $controls.real_quote.full_path_envelope.selected_worker_cpu_envelope -ne 61850 -or
    $controls.real_quote.full_path_envelope.selected_worker_wall_envelope -ne 20010 -or
    (Test-Path -LiteralPath (Join-Path $controlsRoot 'FINALIZATION-FAILED.json'))) { throw 'ADOPTABLE_CONTROLS_REQUIRED' }
$runtime=[ordered]@{}
foreach($property in $old.runtime_pins.psobject.Properties) { $runtime[$property.Name]=$property.Value }
foreach($pin in @($oldPin,$profilePin,$oldRequestPin,$outerPin,$controlsPin)) { $runtime[$pin.path]=$pin.sha256 }
$sources=[ordered]@{}
$stableRoot=Join-Path $controlsRoot 'sources'
foreach($property in $old.sources.psobject.Properties) {
    if($property.Name -ceq 'tools/Run-V5-Check.py' -or $property.Name -ceq 'software/v5/typed_production/test_adoption.py') { continue }
    $original=Pin (Join-Path $projectRoot $property.Name) $property.Value
    $stable=Pin (Join-Path $stableRoot $property.Name) $property.Value
    if($original.bytes -ne $stable.bytes) { throw 'STABLE_SOURCE_BYTES' }
    $sources[$property.Name]=$property.Value
    $runtime[$stable.path]=$stable.sha256
}
if($sources.Count -ne 31) { throw 'EXACT_TYPED_ENTRY_CLOSURE' }
$wrapper=Pin (Join-Path $projectRoot 'tools/Run-V5-TypedProduction.py') '1bf3fda942213abcab1572fb8b4a35dc4744ce331cf913a16cb54ddf945e92a9'
$sources['tools/Run-V5-TypedProduction.py']=$wrapper.sha256
$operator=Join-Path $stableRoot 'software/v5/typed_production/operator.py'
# Only dispatch/output and the disclosed new historical subtotal change.
# Profile/session/allowance/complete budget remain exactly the planned values.
$request.output_directory=$output
$request.stage_limit=5
$request.carried_external_costs.worker_cpu_seconds+=$outer.result.final_job.cpu_seconds
$request.carried_external_costs.controller_cpu_seconds+=$outer.wrapper_cpu_seconds
$request.carried_external_costs.wall_seconds+=$outer.wall_seconds
$request.carried_external_costs.scope='Known partial historical subtotal from the fixed typed-general36 planning request plus its one completed no-host controls operation (inclusive child Job plus separate wrapper once). Other historical build, failure, research, service and control costs remain excluded, not zero. Active-wall sum is not elapsed time or growth benefit; this is not new allowance consumption.'
$requestPin=SaveNew $requestPath $request
$runtime[$requestPin.path]=$requestPin.sha256
if($runtime.Count -gt 256) { throw 'RUNTIME_COUNT' }
$selection=[ordered]@{
    schema='DMKN_V5_TYPED_PRODUCTION_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($profile.base_profile.support_profile.python.path,'-I','-S','-B',$operator,'run',
        '--profile',$profilePin.path,'--profile-sha256',$profilePin.sha256,
        '--request',$requestPin.path,'--request-sha256',$requestPin.sha256,
        '--owner-report','{output}\operator-result.json')
    limits=[ordered]@{cpu_seconds=3270;wall_seconds=1020;memory_mib=4352;active_processes=4;stdout_bytes=1048576;stderr_bytes=1048576}
}
$selected=SaveNew $selectionPath $selection
[ordered]@{selection=$selected;request=$requestPin;profile=$profilePin;sources=$sources.Count;runtime_pins=$runtime.Count;planned_stages=5;worker_cpu_cap=3150;stage_wall_cap=930;executed=$false;proof_funded_by_this_script=$false}|ConvertTo-Json -Depth 4
