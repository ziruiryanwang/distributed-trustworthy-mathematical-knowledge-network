# Select three project compiles using adopted native sources; never run them here.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$BuildSourceSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$RecipesSourceSha256
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'restricted-support-guest-build-01'
$selectionPath = Join-Path $checks ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $checks $name),(Join-Path $checks ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_SELECTION_REQUIRED:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) { throw 'ORDINARY_FILE_REQUIRED' }
    [ordered]@{bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
function Record([string]$path,[string]$digest) {
    if ((Pin $path).sha256 -cne $digest) { throw ('ADOPTED_RECORD_CHANGED:'+ $path) }
    Get-Content -LiteralPath $path -Raw -Encoding UTF8 | ConvertFrom-Json
}
$adapters = [ordered]@{}
$expected = [ordered]@{
    'software/v5/restricted_support_guest/build.py'=$BuildSourceSha256
    'software/v5/restricted_support_guest/recipes.py'=$RecipesSourceSha256
}
foreach ($relative in $expected.Keys) {
    $row = Pin (Join-Path $projectRoot $relative)
    if ($row.sha256 -cne $expected[$relative]) { throw ('REVIEWED_ADAPTER_CHANGED:'+ $relative) }
    $adapters[$relative]=$row
}
$native = Record (Join-Path $checks 'restricted-support-build-01-selection.json') 'a6bbb29061cc301a85e258a5c9f84c6c0bd8be644ff84b389d23b6575b47e0f5'
$guest = Record (Join-Path $checks 'restricted-guest-build-03\selection.json') 'd110cb21351b2f07461986d971533a895011ab0da695e07c6b62175e7de85bf3'
$production = [ordered]@{}
$paths = @('software/v5/restricted_support/lib.rs','software/v5/restricted_support/syntax.rs','software/v5/restricted_support/typing.rs',
    'software/v5/restricted_composition/relation.rs','software/v5/restricted_composition/foundation02.rs',
    'software/v5/restricted_composition/aggregate_lib.rs','software/v5/restricted_composition/aggregate_relation.rs',
    'software/v5/restricted_composition/census.rs','software/v5/restricted_composition/wire.rs',
    'software/v5/aggregate_claims/header.rs','software/v5/aggregate_claims/membership.rs','software/v5/aggregate/main.rs')
foreach ($relative in $paths) {
    $row = Pin (Join-Path $projectRoot $relative)
    $prior = $native.sources.$relative
    if ($null -eq $prior) { $prior = $guest.production_sources.$relative }
    if ($null -eq $prior -or $row.bytes -ne $prior.bytes -or $row.sha256 -cne $prior.sha256) { throw ('ADOPTED_PRODUCTION_CHANGED:'+ $relative) }
    $production[$relative]=$row
}
if ($production.Count -ne 12) { throw 'EXACT_TWELVE_SOURCE_CLOSURE' }
$adoption = [ordered]@{}
$records = [ordered]@{
    build=@('restricted-support-build-01\RESULT.json','e26e29de72363e5c0873b9e0c307d3efaaeca4cc5e02144821446b1a06225392')
    controls_outer=@('restricted-support-controls-01\RESULT.json','b1ebc2538329c08fe67509f5d50ea0ead4ac8a174973506f493d160840a27da0')
    controls_inner=@('restricted-support-controls-01\command\stdout.txt','b9ac046a12a5131d67343596dbee9c48ad0c418fda51c2c20146af1610e6f081')
}
foreach ($role in $records.Keys) {
    $path = Join-Path $checks $records[$role][0]
    $null = Record $path $records[$role][1]
    $row = Pin $path
    $adoption[$role]=[ordered]@{path=$path;bytes=$row.bytes;sha256=$row.sha256}
}
# The reviewed builder validates successful closure, exact30/12 and source/binary
# links. The selector admits only the already independently adopted exact bytes.
$selected=[ordered]@{
    schema='DMKN_V5_RC_SUPPORT_GUEST_THREE_CRATE_BUILD_V1';name=$name
    adapters=$adapters;production_sources=$production;native_adoption=$adoption
    authorizes_three_compiles_and_retained_artifact_adoption=$true
    limits=[ordered]@{
        worker_cpu_seconds=240;worker_wall_seconds=300;memory_mib=4096;active_processes=6
        ordinary_controller_cpu_seconds=40;controller_cpu_seconds=60;total_wall_seconds=420
        fresh_output_bytes=268435456;fresh_output_entries=2048;command_log_bytes=8388608
    }
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 12)+"`n")
if ($raw.Length -gt 65536) { throw 'SELECTION_BYTE_LIMIT' }
$stream=[IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=$selectionPath;pin=(Pin $selectionPath);production_sources=$production.Count;compiler_calls=3;executed=$false} | ConvertTo-Json -Depth 5
