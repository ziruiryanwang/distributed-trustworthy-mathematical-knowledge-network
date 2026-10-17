# Root preparation only: four compiles, no Cargo/dependency rebuild or proof.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$BuildSourceSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$RecipesSourceSha256
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'proof-memo-guest-build-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $local $name),(Join-Path $local ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) { throw 'ORDINARY_FILE_REQUIRED' }
    [ordered]@{bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$adapters = [ordered]@{}
$expected = [ordered]@{
    'software/v5/proof_memo_guest/build.py'=$BuildSourceSha256
    'software/v5/proof_memo_guest/recipes.py'=$RecipesSourceSha256
}
foreach ($relative in $expected.Keys) {
    $row = Pin (Join-Path $projectRoot $relative)
    if ($row.sha256 -cne $expected[$relative]) { throw ('SOURCE_CHANGED:'+ $relative) }
    $adapters[$relative] = $row
}
$priorDir = Join-Path $local 'bounded-parse-direct-build-01'
$priorSelectionPath = Join-Path $priorDir 'selection.json'
$priorMapPath = Join-Path $priorDir 'SOURCE-MAP.json'
if ((Pin $priorSelectionPath).sha256 -cne '3f92ea98aa873580929a446635e426717f6d0efe1a1b1a91e272e21ab7eb9bc6' -or
    (Pin $priorMapPath).sha256 -cne '35387a79067d4868e02076c71c9128b1695fe0371524493f87e28de51fa19c3e') { throw 'PRIOR_PINS' }
$priorSelection = Get-Content -LiteralPath $priorSelectionPath -Raw | ConvertFrom-Json
$priorMap = Get-Content -LiteralPath $priorMapPath -Raw | ConvertFrom-Json
$retained = [ordered]@{}
[long]$totalBytes = 0
$removed = 0
foreach ($property in $priorSelection.retained_artifacts.psobject.Properties) {
    if ([IO.Path]::GetFileName($property.Name) -cmatch '^libnanoda_lib-.*\.(rlib|rmeta)$') { $removed++; continue }
    $actual = Pin $property.Name
    if ($actual.bytes -ne $property.Value.bytes -or $actual.sha256 -cne $property.Value.sha256) { throw 'RETAINED_ARTIFACT_CHANGED' }
    $retained[$property.Name] = $actual
    $totalBytes += $actual.bytes
}
if ($removed -ne 2 -or $retained.Count -ne 236 -or $totalBytes -ne 311693039) { throw 'EXACT_RETAINED_VIEW' }
$production = [ordered]@{}
$snapshot = Join-Path $local 'bounded-parse-guest-build-02\project'
if ($priorMap.source_snapshot -cne $snapshot) { throw 'SOURCE_ORIGIN' }
foreach ($property in $priorMap.project.psobject.Properties) {
    if (-not $property.Name.EndsWith('.rs',[StringComparison]::Ordinal) -or $property.Name.StartsWith('software/v5/modules/native/proof_validation/',[StringComparison]::Ordinal)) { continue }
    $actual = Pin (Join-Path $snapshot $property.Name)
    if ($actual.bytes -ne $property.Value.bytes -or $actual.sha256 -cne $property.Value.sha256) { throw 'RETAINED_SOURCE_CHANGED' }
    $production[$property.Name] = $actual
}
if ($production.Count -ne 30) { throw 'EXACT_UNCHANGED_SOURCES' }
$memo = [ordered]@{
    'software/v5/modules/native/proof_memo/lib.rs'='51a83c7820bcbd0750fac54e6f95b8e5992911ce023d139c4cbb28afcf9416eb'
    'software/v5/modules/native/proof_memo/module_correspondence.rs'='7877ee22c7e1d4350858e67c8cebbedf057dee1820cd9f61940e37cf51f6508e'
}
foreach ($relative in $memo.Keys) {
    $actual = Pin (Join-Path $projectRoot $relative)
    if ($actual.sha256 -cne $memo[$relative]) { throw 'MEMO_SOURCE_CHANGED' }
    $production[$relative] = $actual
}
$selected = [ordered]@{
    schema='DMKN_V5_PROOF_MEMO_FOUR_CRATE_BUILD_V1';name=$name
    adapters=$adapters;production_sources=$production;retained_artifacts=$retained
    authorizes_four_compiles_and_retained_artifact_adoption=$true
    limits=[ordered]@{
        worker_cpu_seconds=240;worker_wall_seconds=300;memory_mib=4096;active_processes=6
        ordinary_controller_cpu_seconds=40;controller_cpu_seconds=60;total_wall_seconds=420
        fresh_output_bytes=536870912;fresh_output_entries=4096;command_log_bytes=8388608
    }
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected|ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=$selectionPath;pin=(Pin $selectionPath);adapters=$adapters.Count;production_sources=$production.Count;adopted_artifact_files=$retained.Count;adopted_artifact_bytes=$totalBytes;compiler_calls=4;executed=$false} | ConvertTo-Json -Depth 5
