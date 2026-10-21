# Prepare a four-crate guest selection; never execute a compiler here.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$BuildSourceSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$RecipesSourceSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$NativeBuildResultSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ControlsOuterSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ControlsInnerSha256
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'restricted-guest-build-03'
$selectionPath = Join-Path $checks ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $checks $name),(Join-Path $checks ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_SELECTION_REQUIRED:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) {
        throw 'ORDINARY_FILE_REQUIRED'
    }
    [ordered]@{bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
function Record([string]$path,[string]$digest) {
    if ($digest -cnotmatch '^[0-9a-f]{64}$' -or (Pin $path).sha256 -cne $digest) {
        throw ('ADOPTED_RECORD_CHANGED:'+ $path)
    }
    Get-Content -LiteralPath $path -Raw -Encoding UTF8 | ConvertFrom-Json
}
$adapters = [ordered]@{}
$expected = [ordered]@{
    'software/v5/restricted_guest/build03.py'=$BuildSourceSha256
    'software/v5/restricted_guest/recipes03.py'=$RecipesSourceSha256
}
foreach ($relative in $expected.Keys) {
    $row = Pin (Join-Path $projectRoot $relative)
    if ($row.sha256 -cne $expected[$relative]) { throw ('REVIEWED_ADAPTER_CHANGED:'+ $relative) }
    $adapters[$relative] = $row
}
$nativeHome = Join-Path $checks 'restricted-composition-build-02'
$nativePath = Join-Path $nativeHome 'RESULT.json'
$built = Record $nativePath $NativeBuildResultSha256
if ($built.schema -cne 'DMKN_V5_RC_NATIVE_BUILD_RESULT_V1' -or
    $built.status -cne 'PASS_RC_THREE_COMPILES_ONLY' -or
    $built.job.active_processes -ne 0 -or $built.job.terminated_processes -ne 0 -or
    (Test-Path -LiteralPath (Join-Path $nativeHome 'FINALIZATION-FAILED.json'))) {
    throw 'ADOPTED_NATIVE_BUILD_REQUIRED'
}
$nativeAttempt = Get-Content -LiteralPath (Join-Path $checks 'restricted-composition-build-02-attempt.json') -Raw | ConvertFrom-Json
if ($nativeAttempt.status -cne $built.status -or $nativeAttempt.result_sha256 -cne $NativeBuildResultSha256) {
    throw 'NATIVE_ATTEMPT_BINDING'
}
$native = Record (Join-Path $checks 'restricted-composition-build-02-selection.json') $built.selection_sha256
if ($native.schema -cne 'DMKN_V5_RC_NATIVE_BUILD_V1' -or $native.name -cne 'restricted-composition-build-02' -or
    @($native.sources.psobject.Properties).Count -ne 15) { throw 'EXACT_NATIVE_SOURCE_BASIS' }
$controlHome = Join-Path $checks 'restricted-composition-controls-01'
$outerPath = Join-Path $controlHome 'RESULT.json'
$innerPath = Join-Path $controlHome 'evidence\result.json'
$outer = Record $outerPath $ControlsOuterSha256
$inner = Record $innerPath $ControlsInnerSha256
if ($outer.result.status -cne 'COMMAND_EXITED_ZERO_AND_CLOSED' -or
    $outer.result.child_exit_code -ne 0 -or $outer.result.final_job.active_processes -ne 0 -or
    $outer.result.final_job.terminated_processes -ne 0 -or $outer.result.job_closed -ne $true -or
    $outer.result.cleanup_errors.Count -ne 0 -or $inner.schema -cne 'DMKN_RC_CONTROL_RUN_V1' -or
    $inner.status -cne 'PASS' -or $inner.exit_code -ne 0 -or $inner.native.executed_count -ne 40 -or
    $inner.native.errors.Count -ne 0 -or $inner.native.expected_refusals.Count -ne 26 -or
    $inner.native.crypto_produced -ne $false -or $inner.native.global_growth_claim -ne $false -or
    $inner.test_binary_sha256 -cne $built.outputs.'restricted_controls.exe'.sha256) {
    throw 'ADOPTED_EXACT_NATIVE_CONTROLS_REQUIRED'
}
$production = [ordered]@{}
$names = @('lib02.rs','foundation02.rs','syntax.rs','typing.rs','relation.rs',
    'aggregate_lib.rs','aggregate_relation.rs','census.rs','wire.rs')
$relativePaths = @($names | ForEach-Object { 'software/v5/restricted_composition/'+$_ })
$relativePaths += @('software/v5/aggregate_claims/header.rs','software/v5/aggregate_claims/membership.rs')
foreach ($relative in $relativePaths) {
    $row = Pin (Join-Path $projectRoot $relative)
    $prior = $native.sources.$relative
    if ($null -eq $prior -or $row.bytes -ne $prior.bytes -or $row.sha256 -cne $prior.sha256) {
        throw ('EXACT_COMPILED_PRODUCTION_SOURCE:'+ $relative)
    }
    $production[$relative] = $row
}
$entry = 'software/v5/aggregate/main.rs'
$entryPin = Pin (Join-Path $projectRoot $entry)
if ($entryPin.bytes -ne 816 -or $entryPin.sha256 -cne 'd7b9b93843b683215e0556e585bc5ea241c672fe4c2a89cc07afa41afb81acad') {
    throw 'UNCHANGED_VERIFY_EVERY_CLAIM_GUEST_ENTRY'
}
$production[$entry] = $entryPin
$moduleMap = Record (Join-Path $checks 'proof-validation-integration-build-01\source-map.json') 'a5693f19236bb8051e476d9f61d8d2449cbcd023054a1e9c8606607049957f2a'
foreach ($stem in @('lib','canonical','input','foundation_static','foundation_data','commitments','journal','policy','relation')) {
    $relative = 'software/v5/modules/receipt/src/'+$stem+'.rs'
    $row = Pin (Join-Path $projectRoot $relative)
    $prior = $moduleMap.$relative
    if ($null -eq $prior -or $row.bytes -ne $prior.bytes -or $row.sha256 -cne $prior.sha256) { throw ('EXACT_NATIVE_MODULE_SOURCE:'+ $relative) }
    $production[$relative] = $row
}
if ($production.Count -ne 21) { throw 'EXACT_21_SOURCE_CLOSURE' }
$adoption = [ordered]@{}
foreach ($role in @('build','controls_outer','controls_inner')) {
    $path = @{build=$nativePath;controls_outer=$outerPath;controls_inner=$innerPath}[$role]
    $row = Pin $path
    $adoption[$role] = [ordered]@{path=$path;bytes=$row.bytes;sha256=$row.sha256}
}
$selected = [ordered]@{
    schema='DMKN_V5_RC_GUEST_FOUR_CRATE_BUILD_V1';name=$name
    adapters=$adapters;production_sources=$production;native_adoption=$adoption
    authorizes_four_compiles_and_retained_artifact_adoption=$true
    limits=[ordered]@{
        worker_cpu_seconds=240;worker_wall_seconds=300;memory_mib=4096;active_processes=6
        ordinary_controller_cpu_seconds=40;controller_cpu_seconds=60;total_wall_seconds=420
        fresh_output_bytes=268435456;fresh_output_entries=2048;command_log_bytes=8388608
    }
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 12)+"`n")
if ($raw.Length -gt 65536) { throw 'SELECTION_BYTE_LIMIT' }
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
[ordered]@{selection=$selectionPath;pin=(Pin $selectionPath);production_sources=$production.Count;
    existing_dependency_files=236;copied_project_artifacts=2;compiler_calls=4;executed=$false} | ConvertTo-Json -Depth 5
