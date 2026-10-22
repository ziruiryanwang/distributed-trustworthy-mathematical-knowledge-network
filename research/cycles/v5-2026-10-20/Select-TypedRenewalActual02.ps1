# Preparation only. Requires a finished, independently reviewed actual U receipt.
# Does not launch the request, create trust state, prove, or change the installation.
param(
    [Parameter(Mandatory=$true)][string]$ReceiptPath,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ReceiptSha256,
    [Parameter(Mandatory=$true)][string]$ProductionResultPath,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ProductionResultSha256,
    [Parameter(Mandatory=$true)][string]$OperatorResultPath,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$OperatorResultSha256,
    [Parameter(Mandatory=$true)][string]$OuterResultPath,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$OuterResultSha256,
    [Parameter(Mandatory=$true)][string]$ProductionSelectionPath,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ProductionSelectionSha256,
    [Parameter(Mandatory=$true)][string]$ProductionOutcomePath,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ProductionOutcomeSha256,
    [Parameter(Mandatory=$true)][string]$ControlsOutcomePath,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ControlsOutcomeSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$SourceReviewSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ActualReviewSha256
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$cycle=Join-Path $projectRoot 'research\cycles\v5-2026-10-20'
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$parent=Join-Path $projectRoot 'product-local\v5-distribution-candidate-preflight-01'
$install=Join-Path $parent 'Mathematical Commons v5'
$data=Join-Path $parent 'typed-renewal02-inputs'
$operations=Join-Path $parent 'typed-renewal02-operations'
$workspace=Join-Path $parent 'typed-renewal02-consumer'
$domain=Join-Path $parent 'typed-renewal02-trust'
$aImage='9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865'
$iImage='9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e'
$releaseSha='bd9f161c43551a578605d5e0c7da34c332cb838c1c70ddb859d2ebd0062b8f03'
$mapSha='25e7c849e41f394498e21a60cc7800ecffb67b0cee1b3911d7164977ce4f2364'
$headerSha='2df5af1a7ded10f5693fb9bff07a7849a67e2a22eaaca39475bf85f96546cd15'
$journalSha='0ba261cd27c816223aa56bc6cbe217e67f48264b8d1c707326095492620a1657'

function Ordinary([string]$path,[bool]$directory=$false,[bool]$fresh=$false) {
    $full=[IO.Path]::GetFullPath($path)
    if ($full -cne $path -or -not $full.StartsWith($projectRoot+'\',[StringComparison]::Ordinal)) { throw 'EXACT_CANONICAL_SCOPE' }
    $cursor=$full
    while ($cursor -and $cursor.Length -ge $projectRoot.Length) {
        if (Test-Path -LiteralPath $cursor) {
            if (((Get-Item -LiteralPath $cursor).Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'NO_REPARSE_PATH' }
        }
        $cursor=[IO.Path]::GetDirectoryName($cursor)
    }
    if ($fresh) {
        if (Test-Path -LiteralPath $full) { throw ('FRESH_OUTPUT_REQUIRED:'+ $full) }
    } elseif ([bool](Get-Item -LiteralPath $full).PSIsContainer -ne $directory) { throw 'ORDINARY_PATH_KIND' }
    return $full
}
function Digest([byte[]]$raw) {
    $algorithm=[Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($algorithm.ComputeHash($raw))).Replace('-','').ToLowerInvariant() }
    finally { $algorithm.Dispose() }
}
function Pin([string]$path,[string]$expected,[long]$maximum=8388608) {
    [void](Ordinary $path)
    $item=Get-Item -LiteralPath $path
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or $item.Length -le 0 -or $item.Length -gt $maximum -or
        (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $expected) { throw ('PIN_CHANGED:'+ $path) }
    return [ordered]@{path=$path;bytes=$item.Length;sha256=$expected}
}
function Read-Pin($row,[long]$maximum=8388608) {
    $actual=Pin $row.path $row.sha256 $maximum
    if ($actual.bytes -ne $row.bytes) { throw 'PIN_SIZE_CHANGED' }
    return Get-Content -LiteralPath $row.path -Raw -Encoding UTF8 | ConvertFrom-Json
}
function Same-Pin($left,$right) {
    return $left.path -ceq $right.path -and $left.bytes -eq $right.bytes -and $left.sha256 -ceq $right.sha256
}
function Json-Bytes($value) { return [Text.UTF8Encoding]::new($false).GetBytes((ConvertTo-Json -InputObject $value -Depth 64 -Compress)+"`n") }
function New-Bytes([string]$path,[byte[]]$raw) {
    [void](Ordinary $path $false $true)
    if ($raw.Length -le 0 -or $raw.Length -gt 8388608) { throw 'STAGED_BOUND' }
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($raw,0,$raw.Length);$stream.Flush($true) } finally { $stream.Dispose() }
    return Pin $path (Digest $raw)
}
function Clean($value) {
    return $value.status -ceq 'COMMAND_EXITED_ZERO_AND_CLOSED' -and $value.child_exit_code -eq 0 -and
        $value.direct_child_reaped -eq $true -and $value.job_closed -eq $true -and
        $value.termination_requested -eq $false -and
        $value.final_job.active_processes -eq 0 -and $value.final_job.terminated_processes -eq 0 -and
        @($value.cleanup_errors).Count -eq 0
}
foreach ($path in @($data,$operations,$workspace,$domain)) { [void](Ordinary $path $true $true) }
$reviews=[ordered]@{
    source=(Pin (Join-Path $cycle 'TYPED-RENEWAL-SOURCE-REVIEW.md') $SourceReviewSha256)
    actual=(Pin (Join-Path $cycle 'TYPED-RENEWAL-ACTUAL-REVIEW.md') $ActualReviewSha256)
    production=(Pin $ProductionOutcomePath $ProductionOutcomeSha256)
    controls=(Pin $ControlsOutcomePath $ControlsOutcomeSha256)
}
# Review pins are root-selected adoption evidence, not machine-parsed verdicts.
$receiptPin=Pin $ReceiptPath $ReceiptSha256
$productionPin=Pin $ProductionResultPath $ProductionResultSha256
$operatorPin=Pin $OperatorResultPath $OperatorResultSha256
$outerPin=Pin $OuterResultPath $OuterResultSha256
$selectionPin=Pin $ProductionSelectionPath $ProductionSelectionSha256
$production=Read-Pin $productionPin
$operator=Read-Pin $operatorPin
$outer=Read-Pin $outerPin
$selection=Read-Pin $selectionPin
foreach ($path in @((Join-Path ([IO.Path]::GetDirectoryName($ProductionResultPath)) 'FINALIZATION-FAILED.json'),
    (Join-Path ([IO.Path]::GetDirectoryName($OuterResultPath)) 'FINALIZATION-FAILED.json'),
    ($OperatorResultPath+'.FINALIZATION-FAILED.json'))) {
    if (Test-Path -LiteralPath $path) { throw 'FINALIZATION_OVERRIDE' }
}
$profilePin=Pin (Join-Path $checks 'typed-production-controls-01-profile.json') '1242b0a8430e68032bbedbddcb3c6539fbdc95a2a5cf567936545c5f891246cc'
$profile=Read-Pin $profilePin
$proofRequest=Read-Pin $operator.request_document 1048576
$proofRequestPin=$operator.request_document
if ($production.schema -cne 'DMKN_V5_SMALL_AGGREGATE_PRODUCER_ATTEMPT_V1' -or
    $production.status -cne 'PASS_FINISHED_RECEIPT_ARTIFACT' -or
    $production.profile_id -cne '166ad63e75a43a427f2b4fcd8642849ba0ab804ac54b08cea39cd422863e779e' -or
    $production.session_id -cne 'b688cf5eb04957cc8ff3398ed2be1ff29b8f2794758160dceff05dc65f8378ec' -or
    $production.allowance_id -cne '703f83c9219832770c806a60949016b8cd6dbd7434820e403df41d048c61d179' -or
    $production.application_receipt_created -ne $true -or $production.final_binding_validated -ne $true -or
    $production.closure_accounting_known -ne $true -or $production.error -ne $null -or
    $production.final_binding_error -ne $null -or -not (Same-Pin $production.receipt $receiptPin) -or
    $production.mathematical_admission -ne $false -or $production.guest_execute_calls -ne 0) { throw 'FINISHED_BOUND_U_RECEIPT_REQUIRED' }
if ($operator.schema -cne 'DMKN_TYPED_AGGREGATE_OPERATOR_RESULT_V1' -or $operator.status -cne 'PASS_ONE_FINITE_ATTEMPT' -or
    $operator.command -cne 'run' -or $operator.production_status -cne $production.status -or
    -not (Same-Pin $operator.production_result $productionPin) -or -not (Same-Pin $operator.profile_document $profilePin) -or
    $operator.owner_report -cne $OperatorResultPath -or $operator.production_output -cne $proofRequest.output_directory -or
    $proofRequest.output_directory -cne [IO.Path]::GetDirectoryName($ProductionResultPath) -or
    $operator.owner_closed -ne $true -or $operator.final_binding_validated -ne $true -or
    $operator.run_calls_attempted -ne 1 -or $operator.error -ne $null -or $operator.close_error -ne $null -or
    $operator.final_binding_error -ne $null -or $operator.mathematical_admission -ne $false) { throw 'CLEAN_BOUND_OPERATOR_REQUIRED' }
if ($outer.schema -cne 'DMKN_V5_TYPED_PRODUCTION_RESULT_V1' -or $outer.selection_sha256 -cne $selectionPin.sha256 -or
    -not (Clean $outer.result) -or @($selection.argv).Count -ne 16 -or @($outer.result.argv).Count -ne 16) { throw 'CLEAN_BOUND_OUTER_REQUIRED' }
$expectedArgv=@($selection.argv)
$expectedArgv[15]=$OperatorResultPath
$expectedFlags=@{1='-I';2='-S';3='-B';5='run';6='--profile';8='--profile-sha256';10='--request';12='--request-sha256';14='--owner-report'}
foreach ($key in $expectedFlags.Keys) { if ($expectedArgv[$key] -cne $expectedFlags[$key]) { throw 'PRODUCTION_ARGV_FLAGS' } }
if ($expectedArgv[7] -cne $profilePin.path -or $expectedArgv[9] -cne $profilePin.sha256 -or
    $expectedArgv[11] -cne $proofRequestPin.path -or $expectedArgv[13] -cne $proofRequestPin.sha256 -or
    $expectedArgv[4] -cne $operator.entry_source.path) { throw 'PRODUCTION_ARGV_DOCUMENTS' }
for ($index=0;$index -lt 16;$index++) { if ($expectedArgv[$index] -cne $outer.result.argv[$index]) { throw 'PRODUCTION_ARGV_BINDING' } }
$session=$proofRequest.session
if ($proofRequest.allowance_id -cne $production.allowance_id -or $session.segments -ne 36 -or $session.assumptions -ne 1 -or
    $session.session_binding -cne '0ef6b41b1085314631b93dc483c8fb95ae5ee9b30949daa2d525d645023d7d90' -or
    $session.capsule_binding -cne 'f8f0fcac4ef9e4726f20fe526836eb465c295b3aa8dd322321d91ecd4fedf332' -or
    $session.expected.bytes -ne 192 -or $session.expected.sha256 -cne $headerSha) { throw 'EXACT_U_SESSION' }
# Check the saved finish-stage link without importing or running the producer.
$finishRows=@($production.stages | Where-Object { [IO.Path]::GetFileName([IO.Path]::GetDirectoryName($_.path)) -ceq 'finish-0' })
if ($finishRows.Count -ne 1) { throw 'SOLE_FINISH_STAGE' }
$finish=Read-Pin $finishRows[0] 1048576
$bound=$finish.bound_stdout
if ($finish.stage -cne 'finish:0' -or $finish.status -cne 'PASS_BOUND_HOST_STAGE' -or -not (Clean $finish.process) -or
    -not (Same-Pin $finish.artifact $receiptPin) -or $bound.schema -cne 'DMKN_SMALL_AGGREGATE_PROOF_STAGE_V1' -or
    $bound.status -cne 'REAL_AGGREGATE_RECEIPT_FINISHED' -or $bound.aggregate_image -cne $aImage -or
    $bound.header_sha256 -cne $headerSha -or $bound.output_sha256 -cne $receiptPin.sha256 -or $bound.output_bytes -ne $receiptPin.bytes -or
    $bound.session_binding -cne $session.session_binding -or $bound.capsule_binding -cne $session.capsule_binding -or
    $bound.application_receipt_created -ne $true -or $bound.mathematical_admission -ne $false) { throw 'EXACT_FINISH_RECEIPT_BINDING' }

$mapPin=Pin (Join-Path $checks 'distribution-candidate-preflight-01-input.json') $mapSha
$releasePin=Pin (Join-Path $install 'V5-RELEASE.json') $releaseSha
$map=Read-Pin $mapPin
$release=Read-Pin $releasePin
if ($map.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or $release.schema -cne 'DMKN_V5_DIRECTORY_RELEASE_V3' -or
    $release.build_input_sha256 -cne $mapSha -or @($map.sdk_sources.psobject.Properties).Count -ne 130 -or
    @($release.sdk_sources.psobject.Properties).Count -ne 130) { throw 'CURRENT130_REQUIRED' }
$totalSources=[long]0
foreach ($property in $map.sdk_sources.psobject.Properties) {
    $logical=$property.Name;$row=$property.Value;$relative=$release.sdk_sources.$logical
    $target=$release.files.$relative
    if ($relative -cne ('sdk/'+$logical) -or $target.bytes -ne $row.bytes -or $target.sha256 -cne $row.sha256) { throw 'UNCHANGED_SDK_MAP' }
    $originalPin=Pin $row.path $row.sha256 2097152
    $installedPin=Pin (Join-Path $install $relative) $row.sha256 2097152
    if ($originalPin.bytes -ne $row.bytes -or $installedPin.bytes -ne $row.bytes) { throw 'UNCHANGED_SDK_SIZE' }
    $totalSources+=$row.bytes
}
$distributionPin=Pin (Join-Path $install 'distribution.py') 'eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813'
$preparationPin=Pin (Join-Path $parent 'candidate-preflight01-operations\installed-candidate-preflight-01-request\preparation.json') '779efefc13f7e90b2edf8e55c58a88cca9f1099be72c80f2e7c35635e2cb4a25' 1048576
$preparation=Read-Pin $preparationPin 1048576
if ($preparation.schema -cne 'DMKN_V5_PREPARATION_PROFILE_V1' -or $preparation.producer.image_id -cne $iImage -or
    $preparation.image.sha256 -cne 'd76f623bb1de5c840fd2ef9c1ac35fc6aba2de74cda0f62c11c161f6973da31f') { throw 'PRESERVE_NATIVE_I_PREPARATION' }
$hostPin=Pin $profile.base_profile.support_profile.host.path '263841ae256af217de2c00452c7f0688a2e9e58e6aa6d95457d5118aef04ff3c' 134217728
if ($hostPin.bytes -ne 68039168 -or $profile.base_profile.support_profile.image_id -cne $aImage) { throw 'TYPED_VERIFICATION_HOST' }
$nativeRow=$release.files.($release.roles.native)
$nativePin=Pin (Join-Path $install $release.roles.native) $nativeRow.sha256
$foundationRow=$release.files.($release.roles.foundation)
$foundationPin=Pin (Join-Path $install $release.roles.foundation) $foundationRow.sha256
if ($nativePin.bytes -ne $nativeRow.bytes -or $foundationPin.bytes -ne 23313 -or
    $foundationPin.sha256 -cne '736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c') { throw 'INSTALLED_NATIVE_FOUNDATION' }
$basisPin=Pin (Join-Path $parent 'candidate-preflight01-inputs\installed-candidate-preflight-01-request.json') '3fff9c9beb0a848e958fb84471571be3d9aabdd5e347f4707ee145ee82e7fad9' 1048576
$basis=Read-Pin $basisPin 1048576
$config=$basis.parameters.workspace_config
if ($config.schema -cne 'DMKN_V5_CLIENT_EVIDENCE_WORKSPACE_V1' -or $config.wire_profile.schema -cne 'DMKN_V5_MODULE_EVIDENCE_WIRE_PROFILE_V2') { throw 'EVIDENCE_WORKSPACE_BASIS' }
$config.wire_profile.aggregate_image=$aImage
# Extraction is selection-time only. Neither whole source document is a client input.
$derivationPin=Pin (Join-Path $checks 'restricted-support-matched-execution-01\pair\derivation.json') '3156948f6cf3925363b55136f48708c52674b9dc82e8e4d0fe5df84050dd9986'
$fixturePin=Pin (Join-Path $checks 'restricted-composition-controls-01\evidence\fixture.json') '019219ca4548dafbdaa814c209a4ec087229091750db3f3cf48fcc155269f40a'
$derivation=Read-Pin $derivationPin
$fixture=Read-Pin $fixturePin
$headerRaw=[byte[]]$derivation.arms.general.header
$journalRaw=[byte[]]$derivation.target_journal
$members=@($derivation.members | Where-Object { (Digest ([byte[]]$_.journal)) -ceq $journalSha })
if ($headerRaw.Length -ne 192 -or (Digest $headerRaw) -cne $headerSha -or $journalRaw.Length -ne 184 -or
    (Digest $journalRaw) -cne $journalSha -or $members.Count -ne 1 -or $members[0].index -ne 1 -or
    @($members[0].siblings).Count -ne 1 -or (Digest ([byte[]]$fixture.second.parents[0].journal)) -cne $journalSha -or
    @($fixture.second.parents[0].openings).Count -ne 1 -or $fixture.second.parents[0].openings[0].index -ne 0) { throw 'EXACT_MINIMAL_U_EXTRACTION' }
$sibling=[byte[]]$members[0].siblings[0]
if ($sibling.Length -ne 32) { throw 'U_MEMBERSHIP_SIBLING_SIZE' }
$membership=[ordered]@{index=1;siblings=@(([BitConverter]::ToString($sibling)).Replace('-','').ToLowerInvariant())}
$rawInputs=[ordered]@{
    'U.receipt'=([IO.File]::ReadAllBytes($receiptPin.path));'U.header'=$headerRaw;'U.journal'=$journalRaw
    'U.membership.json'=(Json-Bytes $membership);'U.opening.json'=(Json-Bytes $fixture.second.parents[0].openings[0])
}
if ((Digest $rawInputs['U.receipt']) -cne $receiptPin.sha256 -or $rawInputs['U.receipt'].Length -ne $receiptPin.bytes) { throw 'RECEIPT_CHANGED_DURING_PREPARATION' }
$sourcePins=[ordered]@{
    'owner.py'=(Pin (Join-Path $projectRoot 'software\v5\typed_renewal\owner02.py') '054499dec130e7b9752bd20b3b1c2a2946aa7bc1986cf617e2d8fd98e211aa43' 1048576)
    'renewal_source.py'=(Pin (Join-Path $projectRoot 'software\v5\typed_renewal\source.py') 'fc5902f778fa37b484a4ab50d0594a1d5a0afe8b91896928bf321cce64dac019' 1048576)
}
$ownerRows=[ordered]@{};$rawSources=[ordered]@{}
foreach ($key in $sourcePins.Keys) {
    $row=$sourcePins[$key];$rawSources[$key]=[IO.File]::ReadAllBytes($row.path)
    if ((Digest $rawSources[$key]) -cne $row.sha256 -or $rawSources[$key].Length -ne $row.bytes) { throw 'OWNER_CHANGED' }
    $ownerRows[$key]=[ordered]@{bytes=$row.bytes;sha256=$row.sha256};$totalSources+=$row.bytes
}
if ($totalSources -gt 67108864) { throw 'SOURCE_BYTES_BOUND' }
$inputPins=[ordered]@{}
foreach ($key in $rawInputs.Keys) { $inputPins[$key]=[ordered]@{path=(Join-Path $data $key);bytes=$rawInputs[$key].Length;sha256=(Digest $rawInputs[$key])} }
$parameters=[ordered]@{
    schema='DMKN_TYPED_RENEWAL_OWNER_V1';action='explicit-temporary-A-only-adoption-and-source-renewal'
    runtime_adoption=[ordered]@{schema='DMKN_V5_CLIENT_RUNTIME_V1';preparation_profile=$preparationPin;native=$nativePin;receipt=$null
        aggregate=[ordered]@{executable=$hostPin;image=$aImage}}
    foundation=$foundationPin;receipt=$inputPins['U.receipt'];header=$inputPins['U.header'];journal=$inputPins['U.journal']
    membership=$inputPins['U.membership.json'];opening=$inputPins['U.opening.json'];workspace_config=$config
    workspace_path=$workspace;domain_path=$domain;domain_id=([Guid]::NewGuid().ToString('N')+[Guid]::NewGuid().ToString('N'))
    operation_limits=[ordered]@{wall_seconds=300;controller_cpu_seconds=90;calls=128;input_bytes=67108864;worker_cpu_seconds=180
        output_bytes=268435456;output_entries=2048
        acquisition=[ordered]@{requests=1;reply_bytes=1048576;verify_attempts=2;verification_input_bytes=16777216;worker_cpu_seconds=120}
        imports=[ordered]@{max_sources=1;max_members=2;max_receipts=1;max_calls=8192;submitted_bytes=33554432;data_bytes=8388608}}
    receipt_limits=[ordered]@{cpu_seconds=30;wall_seconds=60;memory_mib=512}
    author_limits=[ordered]@{cpu_seconds=60;wall_seconds=120;memory_mib=768}
    admission_limits=[ordered]@{native_cpu_seconds=60;receipt_cpu_seconds=30;wall_seconds=120;memory_mib=768}
}
$parameterText=ConvertTo-Json -InputObject $parameters -Depth 64 -Compress
if ($parameterText.Length -gt 49152 -or $parameterText.Contains($fixturePin.path) -or $parameterText.Contains($derivationPin.path) -or
    $parameterText.Contains('850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47')) { throw 'MINIMAL_CONSUMER_PARAMETERS' }
$request=[ordered]@{schema='DMKN_V5_INSTALLED_REQUEST_V1';name='installed-typed-renewal-02';workspace_root=$operations;parameters=$parameters
    limits=[ordered]@{cpu_seconds=360;wall_seconds=480;memory_mib=1024;active_processes=4;stdout_bytes=1048576;stderr_bytes=1048576}
    output_limits=[ordered]@{bytes=536870912;entries=8192};owner=[ordered]@{root=$data;entry='owner.py';sources=$ownerRows};runtime_mode='aggregate'}
$requestRaw=Json-Bytes $request
if ($requestRaw.Length -gt 1048576) { throw 'REQUEST_BOUND' }
# All prerequisite checks precede fresh writes. A partial preparation is preserved,
# never overwritten or launched automatically.
[void][IO.Directory]::CreateDirectory($data)
[void][IO.Directory]::CreateDirectory($operations)
foreach ($key in $rawSources.Keys) { $null=New-Bytes (Join-Path $data $key) $rawSources[$key] }
foreach ($key in $rawInputs.Keys) { $actual=New-Bytes (Join-Path $data $key) $rawInputs[$key];if (-not (Same-Pin $actual $inputPins[$key])) { throw 'STAGED_INPUT_READBACK' } }
$requestPin=New-Bytes (Join-Path $data 'installed-typed-renewal-02-request.json') $requestRaw
$argv=@((Join-Path $install 'base\receiver\runtime\python\python.exe'),'-I','-S','-B',(Join-Path $install 'distribution.py'),
    'launch',$releaseSha,'run',$requestPin.path,$requestPin.sha256)
$prepared=[ordered]@{schema='DMKN_TYPED_RENEWAL_INSTALLED_PREPARATION_V1';request=$requestPin;release=$releasePin;source_map=$mapPin
    reviews=$reviews;production=$productionPin;operator=$operatorPin;outer=$outerPin;production_selection=$selectionPin
    actual_receipt=$receiptPin;fixture_selection_only=$fixturePin;derivation_selection_only=$derivationPin
    native_I_preparation=$preparationPin;aggregate_verifier=$hostPin;aggregate_image=$aImage
    consumer_inputs=$inputPins;owner_sources=$sourcePins;sdk_sources=130;boot_sources=132;selected_source_bytes=$totalSources
    runtime_invoked=$false;cryptographic_production_calls=0;mathematical_acceptance=$false;argv=$argv}
$preparedPin=New-Bytes (Join-Path $data 'PREPARED.json') (Json-Bytes $prepared)
[ordered]@{prepared=$preparedPin;request=$requestPin;runtime_invoked=$false;argv=$argv}|ConvertTo-Json -Depth 6
