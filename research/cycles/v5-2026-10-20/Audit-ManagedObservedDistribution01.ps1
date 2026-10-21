$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
# Read-only saved-evidence audit. No product execution, payload sweep or writes.
$ProjectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
$RunRoot = Join-Path $ProjectRoot 'experiments\v5-local-checks\distribution-managed-observed-build-01'
$InstallRoot = Join-Path $ProjectRoot 'product-local\v5-distribution-managed-observed-01\Mathematical Commons v5'
$OldInstall = Join-Path $ProjectRoot 'product-local\v5-distribution-managed-contribution-01\Mathematical Commons v5'
$InputPath = Join-Path $ProjectRoot 'experiments\v5-local-checks\distribution-managed-observed-01-input.json'
$OldInputPath = Join-Path $ProjectRoot 'experiments\v5-local-checks\distribution-managed-contribution-01-input.json'
$SelectionPath = Join-Path $ProjectRoot 'experiments\v5-local-checks\distribution-managed-observed-build-01-selection.json'
$SelectionSha = 'c3257f270ca3b45bfa5a5c7f88798112dac49d9aaea378913ec1df9f98e3b3f6'
$InputSha = 'e0f0dc5d63dee0d088b8edd9e61d9a1d1bebbe31d3dde76b53887d1c901f7201'
$ReleaseSha = '7381fa03ba8d02017b3f96ff589eca468cdba8c2aa9c4b0a4c1ca4ad968dc344'
$ExpectedChanged = @('v5/client/managed_owner.py','v5/client/serve_placement.py')

function Need([bool]$Value, [string]$Code) { if (-not $Value) { throw $Code } }
function ReadJson([string]$Path) { Get-Content -Raw -Encoding UTF8 -LiteralPath $Path | ConvertFrom-Json }
function Digest([string]$Path) { (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant() }
function Canon($Value) { ConvertTo-Json -InputObject $Value -Depth 100 -Compress }
function FilePin([string]$Path) {
    [ordered]@{path=$Path;bytes=(Get-Item -LiteralPath $Path).Length;sha256=(Digest $Path)}
}
function CheckRow([string]$Path, $Row) {
    Need ((Get-Item -LiteralPath $Path).Length -eq $Row.bytes) ('FILE_LENGTH:' + $Path)
    Need ((Digest $Path) -ceq $Row.sha256) ('FILE_HASH:' + $Path)
}

Need ((Get-Location).Path -ceq $ProjectRoot) 'CANONICAL_WORKDIR'
Need ((Digest $InputPath) -ceq $InputSha) 'INPUT_HASH'
Need ((Digest $OldInputPath) -ceq '33bd99d7c3a1db865a6abcb92c96b5df2d0923a793535135e133aebc54aacc0c') 'OLD_INPUT_HASH'
Need ((Digest $SelectionPath) -ceq $SelectionSha) 'SELECTION_HASH'
Need ((Digest (Join-Path $RunRoot 'selection.json')) -ceq $SelectionSha) 'SAVED_SELECTION_HASH'
$Selection = ReadJson $SelectionPath
$Report = ReadJson (Join-Path $RunRoot 'RESULT.json')
$Command = ReadJson (Join-Path $RunRoot 'command\command.json')
$Build = ReadJson (Join-Path $RunRoot 'command\stdout.txt')
$InputNew = ReadJson $InputPath
$InputOld = ReadJson $OldInputPath
$ManifestPath = Join-Path $InstallRoot 'V5-RELEASE.json'
$OldManifestPath = Join-Path $OldInstall 'V5-RELEASE.json'
Need ((Digest $ManifestPath) -ceq $ReleaseSha) 'RELEASE_HASH'
Need ((Digest $OldManifestPath) -ceq '2cb30fae38d4054a2662f7652ac7ad4d5eef5b1e5f7ba8549b8fd288a90792f1') 'OLD_RELEASE_HASH'
$Manifest = ReadJson $ManifestPath
$OldManifest = ReadJson $OldManifestPath

Need ($Report.selection_sha256 -ceq $SelectionSha) 'REPORT_SELECTION'
Need ($Report.result.status -ceq 'COMMAND_EXITED_ZERO_AND_CLOSED') 'TERMINAL_STATUS'
Need ($Report.result.child_exit_code -eq 0 -and $Report.result.direct_child_reaped -and $Report.result.job_closed) 'CLEAN_EXIT'
Need ($Report.result.final_job.active_processes -eq 0 -and $Report.result.final_job.terminated_processes -eq 0) 'FINAL_PROCESSES'
Need (-not $Report.result.termination_requested -and @($Report.result.cleanup_errors).Count -eq 0) 'NO_FORCED_CLEANUP'
Need ($Command.cwd -ceq $ProjectRoot -and $Report.result.cwd -ceq $ProjectRoot) 'COMMAND_CWD'
$ExpectedArgv = @($Selection.argv | ForEach-Object { $_.Replace('{snapshot}', (Join-Path $RunRoot 'sources')) })
Need ((Canon $ExpectedArgv) -ceq (Canon $Command.argv)) 'SELECTED_ARGV'
Need ((Canon $Command.argv) -ceq (Canon $Report.result.argv)) 'REPORTED_ARGV'
$ExpectedLimits = [ordered]@{cpu_seconds=120;wall_seconds=600;memory_mib=128;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
Need (@($Selection.limits.psobject.Properties).Count -eq 6) 'LIMIT_FIELD_COUNT'
foreach ($Name in $ExpectedLimits.Keys) {
    Need ($Selection.limits.$Name -eq $ExpectedLimits[$Name]) ('SELECTED_LIMIT:' + $Name)
    Need ($Command.limits.$Name -eq $ExpectedLimits[$Name]) ('COMMAND_LIMIT:' + $Name)
    Need ($Report.result.limits.$Name -eq $ExpectedLimits[$Name]) ('REPORT_LIMIT:' + $Name)
}
Need ($Report.result.final_job.cpu_seconds -le $Selection.limits.cpu_seconds) 'CPU_BOUND'
Need ($Report.wall_seconds -le $Selection.limits.wall_seconds) 'WALL_BOUND'
Need ($Report.result.final_job.peak_job_private_commit_bytes -le $Selection.limits.memory_mib * 1MB) 'MEMORY_BOUND'
foreach ($Stream in @('stdout','stderr')) {
    $Size = (Get-Item -LiteralPath (Join-Path $RunRoot ('command\' + $Stream + '.txt'))).Length
    Need ($Size -eq $Report.result.observed_logs.($Stream + '_bytes')) ('LOG_SIZE:' + $Stream)
    Need ($Size -le $Selection.limits.($Stream + '_bytes')) ('LOG_BOUND:' + $Stream)
}
Need ((Get-Item -LiteralPath (Join-Path $RunRoot 'command\stderr.txt')).Length -eq 0) 'EMPTY_STDERR'

Need (@($Selection.sources.psobject.Properties).Count -eq 2) 'SOURCE_COUNT'
foreach ($Property in $Selection.sources.psobject.Properties) {
    Need ((Digest (Join-Path (Join-Path $RunRoot 'sources') $Property.Name)) -ceq $Property.Value) ('SNAPSHOT:' + $Property.Name)
    Need ((Digest (Join-Path $ProjectRoot $Property.Name)) -ceq $Property.Value) ('SOURCE:' + $Property.Name)
}
Need (@($Selection.runtime_pins.psobject.Properties).Count -eq 29) 'RUNTIME_COUNT'
foreach ($Property in $Selection.runtime_pins.psobject.Properties) {
    Need ((Digest $Property.Name) -ceq $Property.Value) ('RUNTIME:' + $Property.Name)
}

Need (@($InputOld.sdk_sources.psobject.Properties).Count -eq 127) 'OLD_SDK_COUNT'
Need (@($InputNew.sdk_sources.psobject.Properties).Count -eq 127) 'NEW_SDK_COUNT'
Need ((Canon @($InputNew.psobject.Properties.Name | Sort-Object)) -ceq (Canon @($InputOld.psobject.Properties.Name | Sort-Object))) 'INPUT_KEYS'
foreach ($Property in $InputOld.psobject.Properties) {
    if ($Property.Name -ne 'sdk_sources') {
        Need ((Canon $Property.Value) -ceq (Canon $InputNew.($Property.Name))) ('UNCHANGED_INPUT:' + $Property.Name)
    }
}
$Unchanged = 0
$Changed = @()
foreach ($Property in $InputOld.sdk_sources.psobject.Properties) {
    Need ($null -ne $InputNew.sdk_sources.psobject.Properties[$Property.Name]) ('NO_REMOVED_SOURCE:' + $Property.Name)
    if ((Canon $Property.Value) -ceq (Canon $InputNew.sdk_sources.($Property.Name))) { $Unchanged++ }
    else { $Changed += $Property.Name }
}
Need ($Unchanged -eq 125 -and (Canon @($Changed | Sort-Object)) -ceq (Canon $ExpectedChanged)) 'EXACT_TWO_REPLACEMENTS'
Need (@($Manifest.sdk_sources.psobject.Properties).Count -eq 127) 'MANIFEST_SDK_COUNT'
foreach ($Property in $InputNew.sdk_sources.psobject.Properties) {
    $Name = $Property.Name
    $Relative = 'sdk/' + $Name
    Need ($Manifest.sdk_sources.$Name -ceq $Relative) ('SDK_MAP:' + $Name)
    $Row = $Manifest.files.$Relative
    Need ($Row.bytes -eq $Property.Value.bytes -and $Row.sha256 -ceq $Property.Value.sha256) ('SDK_ROW:' + $Name)
}
$PreparationNames = @()
Need ($Manifest.preparation.source_pins.Count -eq 106) 'PREPARATION_COUNT'
foreach ($Row in $Manifest.preparation.source_pins) {
    $Name = $Row.path
    Need ($Name.StartsWith('sdk/v5/') -and $Name.EndsWith('.py')) 'PREPARATION_SCOPE'
    Need ($Row.bytes -eq $Manifest.files.$Name.bytes -and $Row.sha256 -ceq $Manifest.files.$Name.sha256) ('PREPARATION_PIN:' + $Name)
    $PreparationNames += $Name
}
$ExpectedPreparation = @($Manifest.sdk_sources.psobject.Properties | Where-Object { $_.Name.StartsWith('v5/') -and $_.Name.EndsWith('.py') } | ForEach-Object { $_.Value } | Sort-Object)
Need ((Canon @($PreparationNames | Sort-Object)) -ceq (Canon $ExpectedPreparation)) 'EXACT_PREPARATION_MAP'
foreach ($Name in $ExpectedChanged) {
    CheckRow $InputNew.sdk_sources.$Name.path $InputNew.sdk_sources.$Name
    CheckRow (Join-Path $InstallRoot ('sdk/' + $Name)) $InputNew.sdk_sources.$Name
}
Need ((Digest (Join-Path $InstallRoot 'distribution.py')) -ceq 'eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813') 'INSTALLED_BUILDER'
Need ($Manifest.schema -ceq 'DMKN_V5_DIRECTORY_RELEASE_V3') 'RELEASE_SCHEMA'
Need ($Manifest.build_input_sha256 -ceq $InputSha) 'MANIFEST_INPUT'
Need ($Manifest.base_manifest_sha256 -ceq 'a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed') 'MANIFEST_BASE'
Need ($Build.status -ceq 'DIRECTORY_CREATED_AND_EXACTLY_VERIFIED' -and $Build.mathematical_acceptance -eq $false) 'BUILD_STATUS_SCOPE'
Need ($Build.root -ceq $InstallRoot -and $Build.manifest_sha256 -ceq $ReleaseSha) 'BUILD_OUTPUT'
$FileCount = @($Manifest.files.psobject.Properties).Count
$FileBytes = ($Manifest.files.psobject.Properties | ForEach-Object { [long]$_.Value.bytes } | Measure-Object -Sum).Sum
Need ($Build.files -eq $FileCount -and $Build.bytes -eq $FileBytes) 'MANIFEST_TOTALS'
Need ($FileCount -eq 9872 -and $FileBytes -eq 842694113) 'EXPECTED_PAYLOAD_TOTALS'
Need (@($OldManifest.files.psobject.Properties).Count -eq $FileCount) 'UNCHANGED_FILE_COUNT'
$FileChanged = @()
foreach ($Property in $OldManifest.files.psobject.Properties) {
    Need ($null -ne $Manifest.files.psobject.Properties[$Property.Name]) 'NO_REMOVED_PAYLOAD'
    if ((Canon $Property.Value) -cne (Canon $Manifest.files.($Property.Name))) { $FileChanged += $Property.Name }
}
Need ((Canon @($FileChanged | Sort-Object)) -ceq (Canon @($ExpectedChanged | ForEach-Object {'sdk/' + $_}))) 'EXACT_TWO_PAYLOAD_ROWS'
$Evidence = @('RESULT.json','selection.json','command/command.json','command/stdout.txt','command/stderr.txt') | ForEach-Object { FilePin (Join-Path $RunRoot $_) }
[ordered]@{
    audit='PASS_READ_ONLY_SAVED_BUILD_EVIDENCE'; release=(FilePin $ManifestPath); evidence=$Evidence;
    source_snapshots=2;runtime_pins=29;input_unchanged_rows=$Unchanged;input_replaced=$Changed;
    manifest_sdk_sources=127;preparation_sources=106;payload_files=$FileCount;payload_bytes=$FileBytes;
    changed_payload_rows=$FileChanged;unchanged_payload_rows=$FileCount-$FileChanged.Count;
    independently_hashed_installed_payloads=@('distribution.py','sdk/v5/client/managed_owner.py','sdk/v5/client/serve_placement.py');
    full_payload_sweep_repeated=$false;job_cpu=$Report.result.final_job.cpu_seconds;
    wrapper_cpu=$Report.wrapper_cpu_seconds;known_cpu=$Report.result.final_job.cpu_seconds+$Report.wrapper_cpu_seconds;
    wall=$Report.wall_seconds;peak_job_private_commit=$Report.result.final_job.peak_job_private_commit_bytes
} | ConvertTo-Json -Depth 8
