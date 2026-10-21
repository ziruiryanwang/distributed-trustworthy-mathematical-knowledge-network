# Prepare exactly four new project compiles; do not execute them here.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$BuildSourceSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$RecipesSourceSha256
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'typed-guest-build-01'
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
    if ($digest -cnotmatch '^[0-9a-f]{64}$' -or (Pin $path).sha256 -cne $digest) { throw ('ADOPTED_RECORD_CHANGED:'+ $path) }
    Get-Content -LiteralPath $path -Raw -Encoding UTF8 | ConvertFrom-Json
}
$adapters = [ordered]@{}
$expected = [ordered]@{
    'software/v5/typed_guest/build.py'=$BuildSourceSha256
    'software/v5/typed_guest/recipes.py'=$RecipesSourceSha256
}
foreach ($relative in $expected.Keys) {
    $row = Pin (Join-Path $projectRoot $relative)
    if ($row.sha256 -cne $expected[$relative]) { throw ('REVIEWED_SOURCE_CHANGED:'+ $relative) }
    $adapters[$relative] = $row
}
$typedHome = Join-Path $checks 'typed-rows-build-02'
$typed = Record (Join-Path $typedHome 'selection.json') 'b4da69c0b7b925415931f11adb31c690d2f0ae18f57edddc4b74fcbd44d57cb4'
$typedResult = Record (Join-Path $typedHome 'RESULT.json') 'add627e4fe4bdc102c79eeea745233d95cbfd56f48f58b118fe276adb6c00794'
if ($typed.schema -cne 'DMKN_V5_TYPED_ROWS_BUILD_V1' -or $typed.authorizes_compile_only -ne $true -or
    @($typed.sources.psobject.Properties).Count -ne 39 -or
    $typedResult.status -cne 'PASS_TYPED_ROWS_FOUR_COMPILES_ONLY' -or
    $typedResult.job.active_processes -ne 0 -or $typedResult.job.terminated_processes -ne 0 -or
    (Test-Path -LiteralPath (Join-Path $typedHome 'FINALIZATION-FAILED.json'))) { throw 'ADOPTED_TYPED_BUILD_REQUIRED' }
$controlsHome = Join-Path $checks 'typed-rows-controls-01'
$controlOuter = Record (Join-Path $controlsHome 'RESULT.json') 'bbdceb54b828f79c017481da542d4a2834763932b3c07da4fab544c34dd41b72'
$controlInner = Record (Join-Path $controlsHome 'evidence\result.json') 'daeb9f2f242ef1a027d54c1b16a330b1a4e0e63e6dce0d797eeb88bc8084c71e'
if ($controlOuter.result.status -cne 'COMMAND_EXITED_ZERO_AND_CLOSED' -or
    $controlOuter.result.child_exit_code -ne 0 -or $controlOuter.result.final_job.active_processes -ne 0 -or
    $controlOuter.result.cleanup_errors.Count -ne 0) { throw 'ADOPTED_TYPED_CONTROLS_REQUIRED' }
# The independently adopted exact inner bytes bind the eight-test result.
# No test is imported or rerun by preparation.
$memo = Record (Join-Path $checks 'proof-memo-guest-build-01\selection.json') '16730dce90438a8ee83215af842babfc0def7ef1ef89a6a8bf901c8e05b855b9'
if ($memo.schema -cne 'DMKN_V5_PROOF_MEMO_FOUR_CRATE_BUILD_V1' -or
    @($memo.production_sources.psobject.Properties).Count -ne 32 -or
    @($memo.retained_artifacts.psobject.Properties).Count -ne 236) { throw 'ADOPTED_GUEST_BASIS_REQUIRED' }
$production = [ordered]@{}
$excluded = @('software/v5/typed_rows/build.py','software/v5/typed_rows/controls.rs','software/v5/typed_rows/controls_root.rs')
$excludedCount = 0
foreach ($property in $typed.sources.psobject.Properties) {
    if ($excluded -ccontains $property.Name) { $excludedCount++; continue }
    if (-not $property.Name.StartsWith('software/v5/',[StringComparison]::Ordinal) -or
        -not $property.Name.EndsWith('.rs',[StringComparison]::Ordinal) -or
        $property.Name.Contains('..')) { throw 'PRODUCTION_SOURCE_SCOPE' }
    $actual = Pin (Join-Path $projectRoot $property.Name)
    if ($actual.bytes -ne $property.Value.bytes -or $actual.sha256 -cne $property.Value.sha256) {
        throw ('TYPED_PRODUCTION_CHANGED:'+ $property.Name)
    }
    $production[$property.Name] = $actual
}
if ($excludedCount -ne 3 -or $production.Count -ne 36) { throw 'EXACT_TYPED_PRODUCTION_CLOSURE' }
$entry = 'software/v5/aggregate/main.rs'
$entryPin = Pin (Join-Path $projectRoot $entry)
$expectedEntry = $memo.production_sources.$entry
if ($null -eq $expectedEntry -or $entryPin.bytes -ne $expectedEntry.bytes -or
    $entryPin.sha256 -cne $expectedEntry.sha256) { throw 'UNCHANGED_GENUINE_GUEST_ENTRY' }
$production[$entry] = $entryPin
$retained = [ordered]@{}
[long]$retainedBytes = 0
foreach ($property in $memo.retained_artifacts.psobject.Properties) {
    $actual = Pin $property.Name
    if ($actual.bytes -ne $property.Value.bytes -or $actual.sha256 -cne $property.Value.sha256) {
        throw ('RETAINED_ARTIFACT_CHANGED:'+ $property.Name)
    }
    $retained[$property.Name] = $actual
    $retainedBytes += $actual.bytes
}
if ($production.Count -ne 37 -or $retained.Count -ne 236 -or $retainedBytes -ne 311693039) {
    throw 'EXACT_PRODUCTION_AND_LIBRARY_VIEW'
}
$selected = [ordered]@{
    schema='DMKN_V5_TYPED_GUEST_FOUR_CRATE_BUILD_V1';name=$name
    adapters=$adapters;production_sources=$production;retained_artifacts=$retained
    authorizes_four_compiles_and_retained_artifact_adoption=$true
    limits=[ordered]@{
        worker_cpu_seconds=240;worker_wall_seconds=300;memory_mib=4096;active_processes=6
        ordinary_controller_cpu_seconds=40;controller_cpu_seconds=60;total_wall_seconds=420
        fresh_output_bytes=536870912;fresh_output_entries=4096;command_log_bytes=8388608
    }
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 12)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_BYTE_LIMIT' }
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
[ordered]@{selection=$selectionPath;pin=(Pin $selectionPath);production_sources=$production.Count;
    retained_artifact_files=$retained.Count;retained_artifact_bytes=$retainedBytes;compiler_calls=4;executed=$false} | ConvertTo-Json -Depth 5
