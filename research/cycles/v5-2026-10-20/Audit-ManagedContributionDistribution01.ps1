$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
# Read-only saved-evidence audit. No product imports, calls, builds or file writes.
$ProjectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
$RunRoot = Join-Path $ProjectRoot 'experiments\v5-local-checks\distribution-managed-contribution-build-01'
$InstallRoot = Join-Path $ProjectRoot 'product-local\v5-distribution-managed-contribution-01\Mathematical Commons v5'
$NewInputPath = Join-Path $ProjectRoot 'experiments\v5-local-checks\distribution-managed-contribution-01-input.json'
$OldInputPath = Join-Path $ProjectRoot 'experiments\v5-local-checks\distribution-managed-owner-01-input.json'
$SelectionPath = Join-Path $ProjectRoot 'experiments\v5-local-checks\distribution-managed-contribution-build-01-selection.json'
$SelectionSha = 'ad982f4d49107a6bc6ed4e6268adad9e9e88f963930106ba06eda57faedd5959'
$InputSha = '33bd99d7c3a1db865a6abcb92c96b5df2d0923a793535135e133aebc54aacc0c'
$ReleaseSha = '2cb30fae38d4054a2662f7652ac7ad4d5eef5b1e5f7ba8549b8fd288a90792f1'

function Need([bool]$Condition, [string]$Code) {
    if (-not $Condition) { throw $Code }
}
function Read-Json([string]$Path) {
    Get-Content -Raw -Encoding UTF8 -LiteralPath $Path | ConvertFrom-Json
}
function Digest([string]$Path) {
    (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
}
function Canon($Value) { ConvertTo-Json -InputObject $Value -Depth 100 -Compress }
function File-Pin([string]$Path) {
    [ordered]@{path=$Path; bytes=(Get-Item -LiteralPath $Path).Length; sha256=(Digest $Path)}
}
function Check-Row([string]$Path, $Row, [string]$Code) {
    Need ((Get-Item -LiteralPath $Path).Length -eq $Row.bytes) ($Code + '_LENGTH')
    Need ((Digest $Path) -ceq $Row.sha256) ($Code + '_HASH')
}

Need ((Get-Location).Path -ceq $ProjectRoot) 'CANONICAL_WORKDIR'
Need ((Digest $SelectionPath) -ceq $SelectionSha) 'SELECTION_HASH'
Need ((Digest (Join-Path $RunRoot 'selection.json')) -ceq $SelectionSha) 'RETAINED_SELECTION_HASH'
Need ((Digest $NewInputPath) -ceq $InputSha) 'INPUT_HASH'
Need ((Digest $OldInputPath) -ceq '4a9bfd78afd328d629ee6ad967f7f9378034db86cdee86bef751c5c50e6778a1') 'OLD_INPUT_HASH'
$Selection = Read-Json $SelectionPath
$Report = Read-Json (Join-Path $RunRoot 'RESULT.json')
$Command = Read-Json (Join-Path $RunRoot 'command\command.json')
$Build = Read-Json (Join-Path $RunRoot 'command\stdout.txt')
$InputNew = Read-Json $NewInputPath
$InputOld = Read-Json $OldInputPath
$ManifestPath = Join-Path $InstallRoot 'V5-RELEASE.json'
Need ((Digest $ManifestPath) -ceq $ReleaseSha) 'RELEASE_HASH'
$Manifest = Read-Json $ManifestPath

Need ($Report.selection_sha256 -ceq $SelectionSha) 'REPORT_SELECTION'
Need ($Report.result.status -ceq 'COMMAND_EXITED_ZERO_AND_CLOSED') 'TERMINAL_STATUS'
Need ($Report.result.child_exit_code -eq 0 -and $Report.result.direct_child_reaped -and $Report.result.job_closed) 'CLEAN_EXIT'
Need ($Report.result.final_job.active_processes -eq 0 -and $Report.result.final_job.terminated_processes -eq 0) 'FINAL_PROCESSES'
Need (-not $Report.result.termination_requested -and @($Report.result.cleanup_errors).Count -eq 0) 'NO_FORCED_CLEANUP'
Need ($Command.cwd -ceq $ProjectRoot -and $Report.result.cwd -ceq $ProjectRoot) 'COMMAND_CWD'
$ExpectedArgv = @($Selection.argv | ForEach-Object { $_.Replace('{snapshot}', (Join-Path $RunRoot 'sources')) })
Need ((Canon $ExpectedArgv) -ceq (Canon $Command.argv)) 'SELECTED_ARGV'
Need ((Canon $Command.argv) -ceq (Canon $Report.result.argv)) 'REPORTED_ARGV'
foreach ($Property in $Selection.limits.psobject.Properties) {
    Need ($Command.limits.($Property.Name) -eq $Property.Value) ('COMMAND_LIMIT_' + $Property.Name)
    Need ($Report.result.limits.($Property.Name) -eq $Property.Value) ('REPORT_LIMIT_' + $Property.Name)
}
Need ($Report.result.final_job.cpu_seconds -le $Selection.limits.cpu_seconds) 'CPU_LIMIT'
Need ($Report.wall_seconds -le $Selection.limits.wall_seconds) 'WALL_LIMIT'
Need ($Report.result.final_job.peak_job_private_commit_bytes -le $Selection.limits.memory_mib * 1MB) 'MEMORY_LIMIT'
foreach ($Stream in @('stdout','stderr')) {
    $Size = (Get-Item -LiteralPath (Join-Path $RunRoot ('command\' + $Stream + '.txt'))).Length
    Need ($Size -eq $Report.result.observed_logs.($Stream + '_bytes')) ('LOG_SIZE_' + $Stream)
    Need ($Size -le $Selection.limits.($Stream + '_bytes')) ('LOG_LIMIT_' + $Stream)
}
Need ((Get-Item -LiteralPath (Join-Path $RunRoot 'command\stderr.txt')).Length -eq 0) 'EMPTY_STDERR'

Need (@($Selection.sources.psobject.Properties).Count -eq 2) 'SOURCE_SNAPSHOT_COUNT'
foreach ($Property in $Selection.sources.psobject.Properties) {
    Need ((Digest (Join-Path (Join-Path $RunRoot 'sources') $Property.Name)) -ceq $Property.Value) ('SNAPSHOT_' + $Property.Name)
    Need ((Digest (Join-Path $ProjectRoot $Property.Name)) -ceq $Property.Value) ('SOURCE_' + $Property.Name)
}
Need (@($Selection.runtime_pins.psobject.Properties).Count -eq 29) 'RUNTIME_PIN_COUNT'
foreach ($Property in $Selection.runtime_pins.psobject.Properties) {
    Need ((Digest $Property.Name) -ceq $Property.Value) ('RUNTIME_' + $Property.Name)
}

Need (@($InputOld.sdk_sources.psobject.Properties).Count -eq 126) 'OLD_SDK_COUNT'
Need (@($InputNew.sdk_sources.psobject.Properties).Count -eq 127) 'NEW_SDK_COUNT'
Need ((Canon @($InputNew.psobject.Properties.Name | Sort-Object)) -ceq (Canon @($InputOld.psobject.Properties.Name | Sort-Object))) 'INPUT_TOP_LEVEL_KEYS'
foreach ($Property in $InputOld.psobject.Properties) {
    if ($Property.Name -ne 'sdk_sources') {
        Need ((Canon $Property.Value) -ceq (Canon $InputNew.($Property.Name))) ('UNCHANGED_INPUT_' + $Property.Name)
    }
}
$Unchanged = 0
$Changed = @()
$Added = @()
foreach ($Property in $InputOld.sdk_sources.psobject.Properties) {
    Need ($null -ne $InputNew.sdk_sources.psobject.Properties[$Property.Name]) ('NO_REMOVED_SOURCE_' + $Property.Name)
    if ((Canon $Property.Value) -ceq (Canon $InputNew.sdk_sources.($Property.Name))) { $Unchanged++ }
    else { $Changed += $Property.Name }
}
foreach ($Property in $InputNew.sdk_sources.psobject.Properties) {
    if ($null -eq $InputOld.sdk_sources.psobject.Properties[$Property.Name]) { $Added += $Property.Name }
}
Need ($Unchanged -eq 125 -and $Changed.Count -eq 1 -and $Changed[0] -ceq 'v5/client/managed_owner.py') 'EXACT_REPLACEMENT'
Need ($Added.Count -eq 1 -and $Added[0] -ceq 'v5/client/private_credentials.py') 'EXACT_ADDITION'
Need (@($Manifest.sdk_sources.psobject.Properties).Count -eq 127) 'MANIFEST_SDK_COUNT'
foreach ($Property in $InputNew.sdk_sources.psobject.Properties) {
    $Name = $Property.Name
    $Relative = 'sdk/' + $Name
    Need ($Manifest.sdk_sources.$Name -ceq $Relative) ('SDK_MAP_' + $Name)
    $Row = $Manifest.files.$Relative
    Need ($Row.bytes -eq $Property.Value.bytes -and $Row.sha256 -ceq $Property.Value.sha256) ('SDK_PIN_' + $Name)
}
$PreparationNames = @()
Need ($Manifest.preparation.source_pins.Count -eq 106) 'PREPARATION_SOURCE_COUNT'
foreach ($Row in $Manifest.preparation.source_pins) {
    $Name = $Row.path
    Need ($Name.StartsWith('sdk/v5/') -and $Name.EndsWith('.py')) 'PREPARATION_SCOPE'
    Need ($Row.bytes -eq $Manifest.files.$Name.bytes -and $Row.sha256 -ceq $Manifest.files.$Name.sha256) ('PREPARATION_PIN_' + $Name)
    $PreparationNames += $Name
}
$ExpectedPreparation = @($Manifest.sdk_sources.psobject.Properties | Where-Object { $_.Name.StartsWith('v5/') -and $_.Name.EndsWith('.py') } | ForEach-Object { $_.Value } | Sort-Object)
Need ((Canon @($PreparationNames | Sort-Object)) -ceq (Canon $ExpectedPreparation)) 'EXACT_PREPARATION_MAP'
foreach ($Name in @('v5/client/managed_owner.py','v5/client/private_credentials.py')) {
    Check-Row $InputNew.sdk_sources.$Name.path $InputNew.sdk_sources.$Name ('CHANGED_SOURCE_' + $Name)
    Check-Row (Join-Path $InstallRoot ('sdk/' + $Name)) $InputNew.sdk_sources.$Name ('CHANGED_INSTALLED_' + $Name)
}
$BuilderSha = 'eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813'
Need ((Digest (Join-Path $InstallRoot 'distribution.py')) -ceq $BuilderSha) 'UNCHANGED_INSTALLED_BUILDER'
Need ($Manifest.build_input_sha256 -ceq $InputSha) 'MANIFEST_INPUT'
Need ($Manifest.base_manifest_sha256 -ceq 'a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed') 'MANIFEST_BASE'
Need ($Build.status -ceq 'DIRECTORY_CREATED_AND_EXACTLY_VERIFIED' -and $Build.mathematical_acceptance -eq $false) 'BUILD_STATUS_SCOPE'
Need ($Build.root -ceq $InstallRoot -and $Build.manifest_sha256 -ceq $ReleaseSha) 'BUILD_OUTPUT'
$FileCount = @($Manifest.files.psobject.Properties).Count
$FileBytes = ($Manifest.files.psobject.Properties | ForEach-Object { [long]$_.Value.bytes } | Measure-Object -Sum).Sum
Need ($Build.files -eq $FileCount -and $Build.bytes -eq $FileBytes) 'BUILD_MANIFEST_TOTALS'
$Evidence = @('RESULT.json','selection.json','command/command.json','command/stdout.txt','command/stderr.txt') | ForEach-Object { File-Pin (Join-Path $RunRoot $_) }
[ordered]@{
    audit='PASS_READ_ONLY_SAVED_BUILD_EVIDENCE'; release=(File-Pin $ManifestPath);
    evidence=$Evidence; source_snapshots=2; runtime_pins=29; input_unchanged_rows=$Unchanged;
    input_replaced=$Changed; input_added=$Added; manifest_sdk_sources=127;
    preparation_sources=106; payload_files=$FileCount; payload_bytes=$FileBytes;
    independently_hashed_installed_payloads=@('distribution.py','sdk/v5/client/managed_owner.py','sdk/v5/client/private_credentials.py');
    full_payload_sweep_repeated=$false; build_job_cpu=$Report.result.final_job.cpu_seconds;
    build_wrapper_cpu=$Report.wrapper_cpu_seconds;
    build_known_cpu=$Report.result.final_job.cpu_seconds+$Report.wrapper_cpu_seconds;
    build_wall=$Report.wall_seconds; peak_job_private_commit=$Report.result.final_job.peak_job_private_commit_bytes
} | ConvertTo-Json -Depth 8
