# Selection preparation only. No compiler, host, guest or proof is executed.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'aggregate-host-build-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $local $name),(Join-Path $local ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer) { throw 'FILE_REQUIRED' }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$recipePath = Join-Path $projectRoot 'software\v5\delta\NATIVE-BUILD02-PROPOSAL.json'
$linkPath = Join-Path $local 'module-host-build-03\LINK-INPUTS.json'
$buildPath = Join-Path $local 'proof-validation-integration-build-01\RESULT.json'
$records = [ordered]@{
    $recipePath='b0d037459b950c3cbabd1c2554aebf1fe9611820598d370eb40f4d69e700885d'
    $linkPath='57b9e92616d78e81fc2c99177a127464656ee89a5a189b013b1b2b99b2b9589d'
    $buildPath='55ba9a702360dd10a6b9bea00f481d5066553a1b8debcb10ca43bbcab4de4069'
}
foreach ($path in $records.Keys) { if ((Pin $path).sha256 -cne $records[$path]) { throw 'RETAINED_RECORD_CHANGED' } }
$recipe = Get-Content -LiteralPath $recipePath -Raw | ConvertFrom-Json
$linkMap = Get-Content -LiteralPath $linkPath -Raw | ConvertFrom-Json
$built = Get-Content -LiteralPath $buildPath -Raw | ConvertFrom-Json
if ($built.status -cne 'PASS_PROOF_VALIDATION_FOUR_COMPILES_ONLY') { throw 'INTEGRATED_BUILD_STATUS' }
$runtime = [ordered]@{}
function AddPin([string]$path,[string]$expected) {
    $actual = Pin $path
    if ($actual.sha256 -cne $expected) { throw ('RETAINED_INPUT_CHANGED:'+ $path) }
    if ($runtime.Contains($actual.path) -and $runtime[$actual.path] -cne $expected) { throw 'CONFLICTING_PIN' }
    $runtime[$actual.path] = $expected
}
# Reuse the complete adopted native recipe's compiler, linker, CRT, helper and
# checker dependencies, then add the retained host's dependency search closure.
foreach ($row in $recipe.runtime_pins_rechecked.psobject.Properties) { AddPin $row.Name $row.Value }
$targetRoot = Join-Path $projectRoot 'experiments\general-checker-host-05\build-01\target'
$searchPaths = @($linkMap.dependency_search_paths)+@($linkMap.native_search_paths)
foreach ($row in $linkMap.target_map.psobject.Properties) {
    $path = [IO.Path]::GetFullPath((Join-Path $targetRoot $row.Name))
    $included = $false
    foreach ($directory in $searchPaths) {
        if ($path.StartsWith($directory+'\',[StringComparison]::OrdinalIgnoreCase)) { $included = $true; break }
    }
    if ($included) { AddPin $path $row.Value.sha256 }
}
foreach ($row in $linkMap.external_native.psobject.Properties) {
    foreach ($file in $row.Value.files.psobject.Properties) { AddPin (Join-Path $row.Value.path $file.Name) $file.Value.sha256 }
}
foreach ($row in $linkMap.externs.psobject.Properties) {
    if (-not $runtime.Contains($row.Value.path) -or $runtime[$row.Value.path] -cne $row.Value.sha256) { throw 'DIRECT_HOST_LIBRARY_NOT_IN_CLOSURE' }
}
foreach ($row in $built.outputs.psobject.Properties) { AddPin $row.Value.path $row.Value.sha256 }
foreach ($path in $records.Keys) { AddPin $path $records[$path] }
$sources = [ordered]@{}
$fresh = [ordered]@{
    'software/v5/aggregate_host/build.py'='0c6a98237e63b1245e20af1a95fb91cf42231064345ce8d22d160ad1c99e62a2'
    'software/v5/aggregate_host/aggregate_host.rs'='7548e5b2092f3ece5d9ef93cef6c7ccd7d5e01ad123053f28e836558617857ca'
    'software/v5/aggregate/receipt.rs'='41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254'
}
foreach ($relative in $fresh.Keys) {
    $pin = Pin (Join-Path $projectRoot $relative)
    if ($pin.sha256 -cne $fresh[$relative]) { throw ('SOURCE_CHANGED:'+ $relative) }
    $sources[$relative] = [ordered]@{bytes=$pin.bytes;sha256=$pin.sha256}
}
$selected = [ordered]@{schema='DMKN_V5_AGGREGATE_HOST_BUILD_V1';name=$name;authorizes_compile_only=$true
    sources=$sources;integrated_result=(Pin $buildPath);runtime_pins=$runtime}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 15)+"`n")
if ($raw.Length -gt 2*1024*1024 -or $runtime.Count -gt 8192) { throw 'SELECTION_BOUND' }
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=(Pin $selectionPath);sources=$sources.Count;runtime_pins=$runtime.Count;compiler_calls=1;executed=$false} | ConvertTo-Json -Depth 4
