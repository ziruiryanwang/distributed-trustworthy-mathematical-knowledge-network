# File-only selection of ONE installed public V snapshot. No process invocation.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ReleaseSha256,
    [Parameter(Mandatory=$true)][string]$BuildOutcomePath,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$BuildOutcomeSha256,
    [Parameter(Mandatory=$true)][string]$RenewalOutcomePath,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$RenewalOutcomeSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$RenewalRequestSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$RenewalOuterSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$RenewalResultSha256,
    [Parameter(Mandatory=$true)][string]$ProfileOutcomePath,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ProfileOutcomeSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ProfileSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ProfileResultSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$PacketSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$JournalSha256
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$install=Join-Path $projectRoot 'product-local\v5-distribution-installed-producer-01\Mathematical Commons v5'
$work=Join-Path $projectRoot 'product-local\v5-distribution-installed-producer-01\v-continuation01'
$inputs=Join-Path $work 'inputs'
$profileRoot=Join-Path $work 'profile'
$run=Join-Path $work 'snapshot-01'
$capsule=Join-Path $work 'capsule-01'
$renewalBase=Join-Path $projectRoot 'product-local\v5-distribution-candidate-preflight-01'
$renewalRun=Join-Path $renewalBase 'typed-renewal02-operations\installed-typed-renewal-02'
$originals=[ordered]@{}
$operative=[ordered]@{}
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
function Digest([byte[]]$raw) {
    $algorithm=[Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($algorithm.ComputeHash($raw))).Replace('-','').ToLowerInvariant() }
    finally { $algorithm.Dispose() }
}
function Pin([string]$path,[string]$expected,[long]$maximum=134217728) {
    [void](Ordinary $path)
    $size=(Get-Item -LiteralPath $path).Length
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or $size -le 0 -or $size -gt $maximum -or
        (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $expected -or
        (Get-Item -LiteralPath $path).Length -ne $size) { throw ('EXACT_PIN_REQUIRED:'+ $path) }
    return [ordered]@{path=$path;bytes=$size;sha256=$expected}
}
function SamePin($left,$right) {
    return ($left.path -ceq $right.path -and $left.bytes -eq $right.bytes -and $left.sha256 -ceq $right.sha256)
}
function Remember($row) {
    $actual=Pin $row.path $row.sha256
    if (-not (SamePin $actual $row) -or ($originals.Contains($row.path) -and -not (SamePin $originals[$row.path] $row))) { throw 'ORIGINAL_PIN_CONFLICT' }
    $originals[$row.path]=$actual
    return $actual
}
function ReadPin($row,[long]$maximum=1048576) {
    if ($row.bytes -gt $maximum) { throw 'DOCUMENT_BOUND' }
    [void](Remember $row)
    return Get-Content -LiteralPath $row.path -Raw -Encoding UTF8 | ConvertFrom-Json
}
function Installed([string]$relative) {
    if ($relative.Contains('\') -or $relative.StartsWith('/') -or
        @($relative.Split('/') | Where-Object { $_ -in @('','..','.') -or $_.Contains(':') }).Count) { throw 'RELEASE_RELATIVE_PATH' }
    $row=$manifest.files.$relative
    $pin=Pin (Join-Path $install $relative.Replace('/','\')) $row.sha256
    if ($pin.bytes -ne $row.bytes) { throw 'RELEASE_FILE_LENGTH' }
    [void](Remember $pin)
    return $pin
}
function AddOperative($row) {
    if (-not $row.path.StartsWith($install+'\',[StringComparison]::Ordinal)) { throw 'OPERATIVE_RELEASE_ESCAPE' }
    $relative=$row.path.Substring($install.Length+1).Replace('\','/')
    if ($relative -ceq 'V5-RELEASE.json') { $selected=$manifestPin } else { $selected=Installed $relative }
    if (-not (SamePin $row $selected) -or ($operative.Contains($row.path) -and -not (SamePin $operative[$row.path] $row))) { throw 'OPERATIVE_ROLE_CONFLICT' }
    $operative[$row.path]=$selected
}
function NewJson([string]$path,$value) {
    [void](Ordinary $path $false $true)
    $raw=[Text.UTF8Encoding]::new($false).GetBytes((ConvertTo-Json -InputObject $value -Depth 40 -Compress)+"`n")
    if ($raw.Length -eq 0 -or $raw.Length -gt 1048576) { throw 'GENERATED_JSON_BOUND' }
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($raw,0,$raw.Length);$stream.Flush($true) } finally { $stream.Dispose() }
    $row=Pin $path (Digest $raw) 1048576
    if ($row.bytes -ne $raw.Length) { throw 'SAVED_INTENDED_BYTES' }
    return $row
}
foreach($directory in @($install,$work,$inputs,$profileRoot,$renewalRun)) { [void](Ordinary $directory $true) }
foreach($directory in @($run,$capsule)) { [void](Ordinary $directory $true $true) }
foreach($marker in @('PROFILE-PREPARATION-PENDING.json','PROFILE-PREPARATION-FAILED.json',
    'SNAPSHOT-PREPARATION-PENDING.json','SNAPSHOT-PREPARATION-FAILED.json','SNAPSHOT-PREPARED.json')) {
    if (Test-Path -LiteralPath (Join-Path $work $marker)) { throw 'PREPARATION_OVERRIDE_OR_ALREADY_USED' }
}
foreach($marker in @('PROFILE-PENDING.json','PROFILE-FAILED.json')) {
    if (Test-Path -LiteralPath (Join-Path $profileRoot $marker)) { throw 'PROFILE_INCOMPLETE' }
}
foreach($marker in @('FINALIZATION-FAILED.json','BOOT-FAILED.json')) {
    if (Test-Path -LiteralPath (Join-Path $renewalRun $marker)) { throw 'RENEWAL_COMPLETION_OVERRIDDEN' }
}
foreach($name in @('snapshot.json','snapshot-selection.json')) { [void](Ordinary (Join-Path $inputs $name) $false $true) }
# Audits are exact root-selected evidence; their prose is not executable authority.
$buildOutcome=Remember (Pin $BuildOutcomePath $BuildOutcomeSha256 1048576)
$renewalOutcome=Remember (Pin $RenewalOutcomePath $RenewalOutcomeSha256 1048576)
$profileOutcome=Remember (Pin $ProfileOutcomePath $ProfileOutcomeSha256 1048576)
$manifestPin=Pin (Join-Path $install 'V5-RELEASE.json') $ReleaseSha256 8388608
$manifest=ReadPin $manifestPin 8388608
if ($manifest.schema -cne 'DMKN_V5_DIRECTORY_RELEASE_V4' -or
    @($manifest.sdk_sources.psobject.Properties).Count -ne 144 -or @($manifest.preparation.source_pins).Count -ne 109) { throw 'FULL_INSTALLED_PRODUCER_ROLE' }
$descriptorPin=Installed 'production/ARTIFACTS.json'
$descriptor=ReadPin $descriptorPin
$templatePin=Installed 'production/PROFILE-TEMPLATE.json'
[void](ReadPin $templatePin)
$profilePin=Pin (Join-Path $profileRoot 'profile.json') $ProfileSha256 1048576
$profile=ReadPin $profilePin
$profileResultPin=Pin (Join-Path $profileRoot 'RESULT.json') $ProfileResultSha256 1048576
$profileResult=ReadPin $profileResultPin
$release=[ordered]@{root=$install;manifest=$manifestPin;descriptor=$descriptorPin}
foreach($candidate in @($profile.release,$profileResult.release)) {
    if ($candidate.root -cne $install -or -not (SamePin $candidate.manifest $manifestPin) -or
        -not (SamePin $candidate.descriptor $descriptorPin)) { throw 'PROFILE_RELEASE_BINDING' }
}
$domain=[Text.Encoding]::ASCII.GetBytes("DMKN-INSTALLED-RELEASE-AGGREGATE-LIFECYCLE-PROFILE-V1`0")
$profileId=Digest ([byte[]]($domain+[IO.File]::ReadAllBytes($profilePin.path)))
if ($profile.schema -cne 'DMKN_INSTALLED_RELEASE_AGGREGATE_LIFECYCLE_PROFILE_V1' -or
    $profileResult.schema -cne 'DMKN_RELEASE_PRODUCER_PROFILE_RESULT_V1' -or $profileResult.status -cne 'PROFILE_CREATED' -or
    -not (SamePin $profileResult.profile $profilePin) -or -not (SamePin $profileResult.template $templatePin) -or
    $profileResult.profile_id -cne $profileId -or $profileResult.constructor_calls -ne 0 -or $profileResult.host_calls -ne 0 -or
    @(Get-ChildItem -LiteralPath $profileRoot -Force).Count -ne 2) { throw 'ACTUAL_PUBLIC_PROFILE_REQUIRED' }
[void](Remember $profileResult.request)
$requestPin=Pin (Join-Path $renewalBase 'typed-renewal02-inputs\installed-typed-renewal-02-request.json') $RenewalRequestSha256 1048576
$request=ReadPin $requestPin
$outerPin=Pin (Join-Path $renewalRun 'RESULT.json') $RenewalOuterSha256 1048576
$outer=ReadPin $outerPin
$renewalPin=Pin (Join-Path $renewalRun 'work\typed-renewal-result.json') $RenewalResultSha256 1048576
$renewal=ReadPin $renewalPin
if ($request.schema -cne 'DMKN_V5_INSTALLED_REQUEST_V1' -or $request.name -cne 'installed-typed-renewal-02' -or
    (Join-Path $request.workspace_root $request.name) -cne $renewalRun -or
    $outer.schema -cne 'DMKN_V5_CLIENT_LAUNCH_RESULT_V1' -or $outer.status -cne 'COMMAND_EXITED_ZERO_AND_CLOSED' -or
    $outer.result.status -cne 'COMMAND_EXITED_ZERO_AND_CLOSED' -or $null -ne $outer.final_error -or
    $renewal.schema -cne 'DMKN_TYPED_RENEWAL_RESULT_V1' -or $renewal.status -cne 'COMPLETED' -or
    $renewal.local_U_and_V_admitted -ne $true -or $renewal.client_closed -ne $true -or
    $renewal.workspace_closed -ne $true -or $renewal.domain_withdrawn -ne $true -or
    $null -ne $renewal.error -or @($renewal.cleanup_errors).Count -ne 0 -or
    $renewal.cryptographic_production_calls -ne 0 -or $renewal.snapshot_calls -ne 0) { throw 'ACTUAL_CLEAN_RENEWAL02_REQUIRED' }
$renewalPlanPin=Pin (Join-Path $renewalRun 'plan.json') $outer.plan_sha256 1048576
$renewalPlan=ReadPin $renewalPlanPin
if ($renewalPlan.name -cne $request.name) { throw 'RENEWAL_PLAN_NAME' }
$envelope=$request.parameters.workspace_config.packet_envelope
$envelopeFields=@('packet_bytes','receipt_bytes','witness_bytes','claims','frontiers','deltas','edges','openings','bodies','rows','nodes','depth','rank')
if (@($envelope.psobject.Properties).Count -ne 13) { throw 'EXACT_ENVELOPE_FIELDS' }
foreach($key in $envelopeFields) {
    if ($envelope.$key -ne $renewalPlan.parameters.workspace_config.packet_envelope.$key -or
        $envelope.$key -isnot [ValueType] -or [decimal]::Truncate([decimal]$envelope.$key) -ne [decimal]$envelope.$key -or
        $envelope.$key -le 0) { throw 'AUDITED_ENVELOPE_BINDING' }
}
$packet=Remember (Pin $renewal.packet.path $PacketSha256 $envelope.packet_bytes)
$journal=Remember (Pin $renewal.journal.path $JournalSha256 184)
if (-not (SamePin $packet $renewal.packet) -or -not (SamePin $journal $renewal.journal) -or
    $packet.path -cne (Join-Path $renewalRun 'work\V.packet.json') -or
    $journal.path -cne (Join-Path $renewalRun 'work\V.journal') -or $journal.bytes -ne 184) { throw 'ACTUAL_ADMITTED_V_BINDING' }
[void](Remember $renewal.source)
$target=([BitConverter]::ToString([IO.File]::ReadAllBytes($journal.path))).Replace('-','').ToLowerInvariant()
if ($target.Length -ne 368) { throw 'EXACT_JOURNAL_HEX' }
# Reproduce only the existing adoption's finite operative pin union. No constructor.
AddOperative $manifestPin; AddOperative $descriptorPin
foreach($role in $descriptor.roles.psobject.Properties) { AddOperative (Installed $role.Value.path) }
if (@($profile.source_pins).Count -ne 31 -or @($descriptor.sources.psobject.Properties).Count -ne 31) { throw 'CORE31_REQUIRED' }
foreach($row in $profile.source_pins) { AddOperative $row }
foreach($source in $descriptor.sources.psobject.Properties) {
    $pin=Installed $source.Value.path
    if (-not $operative.Contains($pin.path) -or -not (SamePin $operative[$pin.path] $pin)) { throw 'DESCRIPTOR_CORE_BINDING' }
}
$support=$profile.base_profile.support_profile
if (@($support.runtime_pins).Count -ne 49 -or @($support.source_pins).Count -ne 2 -or
    @($profile.base_profile.source_pins).Count -ne 2 -or $support.image_id -cne $descriptor.aggregate_image) { throw 'INSTALLED_SUPPORT_CLOSURE' }
foreach($row in @($support.supervisor_manifest,$support.host,$support.python,$support.python_dll)+
    @($support.source_pins)+@($support.runtime_pins)+@($profile.base_profile.source_pins)) { AddOperative $row }
$supervisor=ReadPin $support.supervisor_manifest 8388608
foreach($relative in @('operator/commons.py','receiver/helpers/domains.py','receiver/helpers/run_stage.py')) {
    $pin=Installed ('base/'+$relative); $row=$supervisor.files.$relative
    if ($pin.bytes -ne $row.bytes -or $pin.sha256 -cne $row.sha256) { throw 'SUPERVISOR_HELPER_BINDING' }
    AddOperative $pin
}
if ($operative.Count -ne 60) { throw 'EXACT_OPERATIVE60_REQUIRED' }
$distributionPin=Installed 'distribution.py'
$entry=Installed 'sdk/v5/release_production/operator.py'
if (-not $operative.Contains($entry.path)) { throw 'ENTRY_ALREADY_IN_OPERATIVE60' }
$nativeLimits=[ordered]@{worker_cpu_seconds=180;controller_cpu_seconds=60;wall_seconds=240;memory_mib=3072
    active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576;output_bytes=218103808;output_entries=288}
$outerLimits=[ordered]@{cpu_seconds=360;wall_seconds=360;memory_mib=4096;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
$pending=Join-Path $work 'SNAPSHOT-PREPARATION-PENDING.json'
try {
    $pendingPin=NewJson $pending ([ordered]@{schema='DMKN_INSTALLED_V_SNAPSHOT_PREPARATION_PENDING_V1';status='PENDING'})
    $configuration=NewJson (Join-Path $inputs 'snapshot.json') ([ordered]@{
        schema='DMKN_AGGREGATE_LIFECYCLE_SNAPSHOT_REQUEST_V1';profile_id=$profileId;profile_document=$profilePin
        packet=$packet;target_journal=$target;envelope=$envelope;cycles=67108864;po2=18;diagnostic_mode='stats'
        limits=$nativeLimits;output_directory=$capsule})
    $runtime=[ordered]@{};[long]$runtimeBytes=0
    foreach($row in @($operative.Values)+@($profilePin,$configuration,$packet)) {
        if ($runtime.Contains($row.path)) { throw 'UNEXPECTED_RUNTIME_DUPLICATE' }
        $runtime[$row.path]=$row.sha256;$runtimeBytes+=$row.bytes
    }
    if ($runtime.Count -ne 63 -or $runtimeBytes -gt 536870912) { throw 'RUNTIME63_BOUND' }
    $selection=NewJson (Join-Path $inputs 'snapshot-selection.json') ([ordered]@{
        schema='DMKN_RELEASE_PRODUCER_LAUNCH_V1';name='snapshot-01';action='snapshot';release=$release
        profile=$profilePin;input=$configuration;entry=$entry;run_directory=$run;runtime_pins=$runtime;limits=$outerLimits
        output_limits=[ordered]@{bytes=536870912;entries=4096};prior_launches=@();input_launch=$null})
    foreach($row in $originals.Values) { $actual=Pin $row.path $row.sha256; if(-not (SamePin $actual $row)) { throw 'ORIGINAL_CHANGED' } }
    foreach($directory in @($run,$capsule)) { [void](Ordinary $directory $true $true) }
    $argv=@($support.python.path,'-I','-S','-B',$distributionPin.path,'producer',$ReleaseSha256,$selection.path,$selection.sha256)
    $prepared=NewJson (Join-Path $work 'SNAPSHOT-PREPARED.json') ([ordered]@{
        schema='DMKN_INSTALLED_V_SNAPSHOT_PREPARATION_V1';status='PREPARED_NOT_EXECUTED';release=$release
        build_outcome=$buildOutcome;renewal_outcome=$renewalOutcome;renewal_outer=$outerPin;renewal_result=$renewalPin
        renewal_request=$requestPin;profile_outcome=$profileOutcome;profile_result=$profileResultPin;profile=$profilePin;profile_id=$profileId
        packet=$packet;journal=$journal;configuration=$configuration;selection=$selection;originals=$originals
        operative_pins=60;runtime_pins=63;runtime_bytes=$runtimeBytes;runtime_invoked=$false;proof_calls=0;argv=$argv
        completion_rule='Valid_only_without_SNAPSHOT-PREPARATION-PENDING.json_or_SNAPSHOT-PREPARATION-FAILED.json'})
    foreach($row in @($configuration,$selection,$prepared,$pendingPin)) { $actual=Pin $row.path $row.sha256; if(-not (SamePin $actual $row)) { throw 'GENERATED_BYTES_CHANGED' } }
    [ordered]@{prepared=$prepared;selection=$selection;runtime_invoked=$false;proof_calls=0;argv=$argv}|ConvertTo-Json -Depth 6
    Remove-Item -LiteralPath $pending -ErrorAction Stop
} catch {
    try { [void](NewJson (Join-Path $work 'SNAPSHOT-PREPARATION-FAILED.json') ([ordered]@{
        schema='DMKN_INSTALLED_V_SNAPSHOT_PREPARATION_FAILURE_V1';status='FAILED';error=$_.Exception.Message;runtime_invoked=$false})) }
    catch { throw 'SNAPSHOT_PREPARATION_FAILURE_MARKER_UNCONFIRMED_PENDING_RETAINS_FAILURE' }
    throw
}
