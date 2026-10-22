# Source-only until root adopts the prefix outcome and explicitly selects continuation.
# Prepares one same-allowance remainder request; does not launch or fund it.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$PrefixResultSha,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$OuterResultSha,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$OwnerResultSha,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$AuditSha
)
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$name='typed-general36-remainder-owner-01'
$output=Join-Path $checks 'typed-general36-remainder-01'
$selectionPath=Join-Path $checks ($name+'-selection.json')
$requestPath=Join-Path $checks 'typed-general36-remainder-01-request.json'
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
function Normalize($value) {
    if($null -eq $value) { return $null }
    if($value -is [System.Collections.IDictionary]) {
        $ordered=[ordered]@{}
        foreach($key in @($value.Keys | Sort-Object)) { $ordered[$key]=Normalize $value[$key] }
        return $ordered
    }
    if($value -is [System.Management.Automation.PSCustomObject]) {
        $ordered=[ordered]@{}
        foreach($key in @($value.psobject.Properties.Name | Sort-Object)) { $ordered[$key]=Normalize $value.$key }
        return $ordered
    }
    if($value -is [array]) { return ,@($value | ForEach-Object { Normalize $_ }) }
    return $value
}
function Json($value) { ConvertTo-Json -InputObject (Normalize $value) -Depth 40 -Compress }
function SaveNew([string]$path,$value) {
    $bytes=[Text.UTF8Encoding]::new($false).GetBytes((Json $value)+"`n")
    if($bytes.Length -gt 1048576) { throw 'DOCUMENT_BOUND' }
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($bytes,0,$bytes.Length);$stream.Flush($true) } finally { $stream.Dispose() }
    Pin $path
}
$oldPin=Pin (Join-Path $checks 'typed-general36-prefix-owner-01-selection.json') 'fa40f145a27b379e4c783a242b2178856153bd2d1473d8b06914eae56c85a291'
$requestPin=Pin (Join-Path $checks 'typed-general36-prefix-01-request.json') '7aac14ce23df913409ba5cf4e9c94389e7cd3276c46831cfc799583896238f75'
$profilePin=Pin (Join-Path $checks 'typed-production-controls-01-profile.json') '1242b0a8430e68032bbedbddcb3c6539fbdc95a2a5cf567936545c5f891246cc'
$prefix=Join-Path $checks 'typed-general36-prefix-01'
$prefixOwner=Join-Path $checks 'typed-general36-prefix-owner-01'
$resultPin=Pin (Join-Path $prefix 'RESULT.json') $PrefixResultSha
$outerPin=Pin (Join-Path $prefixOwner 'RESULT.json') $OuterResultSha
$ownerPin=Pin (Join-Path $prefixOwner 'operator-result.json') $OwnerResultSha
$auditPin=Pin (Join-Path $projectRoot 'research\cycles\v5-2026-10-20\TYPED-PRODUCTION-PREFIX-OUTCOME.md') $AuditSha
$old=ReadPin $oldPin
$request=ReadPin $requestPin
$result=ReadPin $resultPin
$outer=ReadPin $outerPin
$owner=ReadPin $ownerPin
foreach($path in @((Join-Path $prefix 'FINALIZATION-FAILED.json'),(Join-Path $prefixOwner 'FINALIZATION-FAILED.json'),(Join-Path $prefixOwner 'operator-result.json.FINALIZATION-FAILED.json'))) {
    if(Test-Path -LiteralPath $path) { throw 'FINALIZATION_OVERRIDE' }
}
if($outer.schema -cne 'DMKN_V5_TYPED_PRODUCTION_RESULT_V1' -or
    $outer.selection_sha256 -cne $oldPin.sha256 -or
    $outer.result.status -cne 'COMMAND_EXITED_ZERO_AND_CLOSED' -or
    $outer.result.child_exit_code -ne 0 -or $outer.result.direct_child_reaped -ne $true -or
    $outer.result.job_closed -ne $true -or $outer.result.final_job.active_processes -ne 0 -or
    $outer.result.final_job.terminated_processes -ne 0 -or @($outer.result.cleanup_errors).Count -ne 0 -or
    $owner.schema -cne 'DMKN_TYPED_AGGREGATE_OPERATOR_RESULT_V1' -or
    $owner.status -cne 'PASS_ONE_FINITE_ATTEMPT' -or $owner.owner_closed -ne $true -or
    $owner.final_binding_validated -ne $true -or $owner.error -ne $null -or
    $owner.close_error -ne $null -or $owner.final_binding_error -ne $null -or
    $owner.profile_document.sha256 -cne $profilePin.sha256 -or
    $owner.request_document.sha256 -cne $requestPin.sha256 -or
    $owner.production_result.sha256 -cne $resultPin.sha256 -or
    $owner.production_result.bytes -ne $resultPin.bytes -or
    $owner.production_result.path -cne $resultPin.path -or
    $owner.production_status -cne 'PASS_SELECTED_PREFIX_ONLY' -or $owner.run_calls_attempted -ne 1 -or
    $owner.host_calls_attempted -ne 5 -or $owner.proof_calls -ne 5 -or
    $owner.mathematical_admission -ne $false) { throw 'CLEAN_EXACT_PREFIX_OWNER_REQUIRED' }
if($result.schema -cne 'DMKN_V5_SMALL_AGGREGATE_PRODUCER_ATTEMPT_V1' -or
    $result.status -cne 'PASS_SELECTED_PREFIX_ONLY' -or
    $result.profile_id -cne '166ad63e75a43a427f2b4fcd8642849ba0ab804ac54b08cea39cd422863e779e' -or
    $result.session_id -cne 'b688cf5eb04957cc8ff3398ed2be1ff29b8f2794758160dceff05dc65f8378ec' -or
    $result.allowance_id -cne $request.allowance_id -or
    $request.allowance_id -cne '703f83c9219832770c806a60949016b8cd6dbd7434820e403df41d048c61d179' -or
    (Json $result.budget) -cne (Json $request.budget) -or
    (Json $result.carried_external_costs) -cne (Json $request.carried_external_costs) -or
    @($result.prior_attempts).Count -ne 0 -or @($request.prior_attempts).Count -ne 0 -or
    @($request.checkpoints).Count -ne 0 -or $request.stage_limit -ne 5 -or
    $result.closure_accounting_known -ne $true -or $result.final_binding_validated -ne $true -or
    $result.application_receipt_created -ne $false -or $result.receipt -ne $null -or
    $result.mathematical_admission -ne $false -or $result.guest_execute_calls -ne 0 -or
    $result.host_calls_attempted -ne 5 -or $result.reported_proof_stage_calls -ne 5 -or
    @($result.stages).Count -ne 5 -or @($result.retained_checkpoints).Count -ne 5 -or
    $result.error -ne $null -or $result.final_binding_error -ne $null) { throw 'EXACT_SAME_ALLOWANCE_PREFIX_REQUIRED' }
# Serialization key ordering is immaterial, but decimal values and scope must stay exact.
# The existing producer validates complete lineage and checkpoint headers before dispatch.
$expectedKeys=@('join:1','lift:0','lift:1','segment:0','segment:1')
if((@($result.retained_checkpoints | ForEach-Object { $_.key } | Sort-Object) -join ',') -cne ($expectedKeys -join ',')) { throw 'EXACT_FIVE_RETAINED_KEYS' }
$runtime=[ordered]@{}
foreach($property in $old.runtime_pins.psobject.Properties) { $runtime[$property.Name]=$property.Value }
foreach($pin in @($oldPin,$requestPin,$profilePin,$resultPin,$outerPin,$ownerPin,$auditPin)) { $runtime[$pin.path]=$pin.sha256 }
foreach($row in $result.retained_checkpoints) {
    $pin=Pin $row.file.path $row.file.sha256
    if($pin.bytes -ne $row.file.bytes -or $pin.bytes -gt 524288) { throw 'CHECKPOINT_PIN_BYTES' }
    $runtime[$pin.path]=$pin.sha256
}
foreach($property in $old.sources.psobject.Properties) { $null=Pin (Join-Path $projectRoot $property.Name) $property.Value }
if(@($old.sources.psobject.Properties).Count -ne 32) { throw 'FROZEN_SOURCE_COUNT' }
# Root's full-path funding policy, not an inherited scheduler guarantee.
if($result.worker_cpu_charge_this_attempt -lt 0 -or $result.worker_cpu_charge_this_attempt + 58700 -gt $request.budget.worker_cpu_seconds -or
    $result.controller_cpu_seconds -lt 0 -or $result.controller_cpu_seconds -ge $request.budget.controller_cpu_seconds -or
    $result.wall_seconds -lt 0 -or $result.wall_seconds + 19800 -gt $request.budget.wall_seconds -or
    $result.output_charge_this_attempt -lt 0 -or $result.output_charge_this_attempt + 317718528 -gt $request.budget.output_bytes -or
    $result.entry_charge_this_attempt -lt 0 -or $result.entry_charge_this_attempt + 940 -gt $request.budget.output_entries) { throw 'COMPLETE_REMAINDER_MUST_FIT' }
$request.prior_attempts=@($resultPin)
$request.checkpoints=@($result.retained_checkpoints)
$request.output_directory=$output
$request.stage_limit=104
# Preserve carry verbatim in value: prefix costs enter prior_attempts, never this subtotal.
$freshRequest=SaveNew $requestPath $request
$runtime[$freshRequest.path]=$freshRequest.sha256
if($runtime.Count -gt 256) { throw 'RUNTIME_COUNT' }
$argv=@($old.argv)
$argv[11]=$freshRequest.path
$argv[13]=$freshRequest.sha256
$selection=[ordered]@{schema=$old.schema;name=$name;sources=$old.sources;runtime_pins=$runtime;argv=$argv
    limits=[ordered]@{cpu_seconds=60000;wall_seconds=19800;memory_mib=4352;active_processes=4;stdout_bytes=1048576;stderr_bytes=1048576}}
$selected=SaveNew $selectionPath $selection
[ordered]@{selection=$selected;request=$freshRequest;profile=$profilePin;prior_attempt=$resultPin;checkpoints=5;planned_calls=104;worker_cpu_cap=58700;stage_wall_cap=19080;executed=$false;proof_funded_by_this_script=$false}|ConvertTo-Json -Depth 4
