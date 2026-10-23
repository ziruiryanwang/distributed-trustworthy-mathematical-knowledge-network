param(
    [Parameter(Mandatory=$true)][string] $Name,
    [Parameter(Mandatory=$true)][string] $Consumer
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -ne $projectRoot) { throw 'Canonical workdir required' }
if ($Name -notmatch '^ordinary-[a-z0-9-]+$' -or $Consumer -notmatch '^ordinary-[a-z0-9-]+$') { throw 'Selected local names required' }
function Hash-File([string] $Path) { (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Write-NewJson([string] $Path, $Value) {
    $bytes = [Text.UTF8Encoding]::new($false).GetBytes(($Value | ConvertTo-Json -Depth 18) + "`n")
    $stream = [IO.File]::Open($Path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($bytes,0,$bytes.Length); $stream.Flush($true) } finally { $stream.Dispose() }
}
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$selectionPath = Join-Path $local ($Name + '.selection.json')
$manifestPath = Join-Path $local ($Name + '.parent.json')
foreach ($path in @($selectionPath,$manifestPath,(Join-Path $local $Name))) {
    if (Test-Path -LiteralPath $path) { throw 'Fresh selection, manifest and output paths required' }
}
$origin = Join-Path $local 'ordinary-native-admission-01'
$oldPath = Join-Path $origin 'selection.json'
if ((Hash-File $oldPath) -ne 'ab2f655448242587880129e62cca4bc5dc74638c1e8699e30b4a9f67e26fce5f') { throw 'Frozen native selection changed' }
$old = Get-Content -Raw -LiteralPath $oldPath | ConvertFrom-Json
$pins = [ordered]@{}
foreach ($entry in $old.runtime_pins.PSObject.Properties) {
    if ($entry.Name -notlike '*\ordinary-native-owner-export-01\*' -and $entry.Name -notlike '*\software\assets\foundation\*') {
        $pins[$entry.Name] = $entry.Value
    }
}
$pins[$oldPath] = Hash-File $oldPath
foreach ($entry in $old.sources.PSObject.Properties) {
    $path = Join-Path (Join-Path $origin 'sources') $entry.Name
    if ((Hash-File $path) -ne $entry.Value) { throw 'Original source changed' }
    $pins[$path] = $entry.Value
}
$profilePath = Join-Path $origin 'native-admission\PROFILE.json'
$pins[$profilePath] = Hash-File $profilePath
$consumerPath = Join-Path $local $Consumer
$resultPath = Join-Path $consumerPath 'RESULT.json'
$result = Get-Content -Raw -LiteralPath $resultPath | ConvertFrom-Json
$consumerSelection = Join-Path $consumerPath 'selection.json'
if ($result.result.status -ne 'COMMAND_EXITED_ZERO_AND_CLOSED' -or $result.selection_sha256 -ne (Hash-File $consumerSelection)) { throw 'Successful consumer supervision required' }
$consumerReport = Join-Path $consumerPath 'CONSUMER-RESULT.json'
$report = Get-Content -Raw -LiteralPath $consumerReport | ConvertFrom-Json
$bundle = Join-Path $consumerPath 'consumer-export.json'
if ($report.status -ne 'PASS_OWNER_SOURCE_USE_AND_INERT_SUCCESSOR_EXPORT' -or (Hash-File $bundle) -ne $report.export_sha256 -or (Get-Item -LiteralPath $bundle).Length -ne $report.export_bytes) { throw 'Successful exact consumer export required' }
$prepare = Join-Path $consumerPath 'PREPARE-RESULT.json'
foreach ($path in @($resultPath,$consumerSelection,$consumerReport,$bundle,$prepare)) { $pins[$path] = Hash-File $path }
$store = Join-Path $local 'ordinary-native-recovery-01\native-recovery\catalog'
$directories = @()
$files = [ordered]@{}
$pending = [Collections.Generic.Queue[string]]::new()
$pending.Enqueue($store)
$entries = 0
while ($pending.Count -gt 0) {
    $directory = $pending.Dequeue()
    foreach ($entry in Get-ChildItem -LiteralPath $directory -Force) {
        $entries += 1
        if ($entries -gt 32 -or ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Bounded ordinary catalog tree required' }
        $relative = $entry.FullName.Substring($store.Length + 1).Replace('\','/')
        if ($entry.PSIsContainer) { $directories += $relative; $pending.Enqueue($entry.FullName) }
        else { $files[$relative] = [ordered]@{bytes=$entry.Length;sha256=(Hash-File $entry.FullName)} }
    }
}
if ($directories.Count -ne 6 -or $files.Count -ne 7 -or $files['catalog.sqlite'].sha256 -ne 'bcb94ff9695f4d360205eaf8f81151f1cf70437c0e6c434b48f6993d893980e9') { throw 'Exact adopted catalog census/database required' }
$manifest = [ordered]@{
    schema='DMKN_ORDINARY_SUCCESSOR_PARENT_COPY_V1';store_directory=$store
    profile_id='fd23ae289706e5a3277a3c4304de83d65498755dd014b234810e79539f5c8219'
    basis_id='cb8f9c2db2b5b53984be1ce8b5f540024264a1e2db41fc7226c594ee1f022299'
    context_id='4d70ddd613bbbfe5e9312ea403e64a95a0a2239842a19d90bf0c044847929026'
    store_id='12185a972a6302a0a70899e968f4c249d1994afd252ecbb74c91e59961b81eb5'
    directories=@($directories | Sort-Object);files=$files
}
Write-NewJson $manifestPath $manifest
$pins[$manifestPath] = Hash-File $manifestPath
$sources = [ordered]@{}
foreach ($relative in @('tools/Run-V5-Check.py','software/v5/ordinary_lean/run_successor_admission.py')) {
    $sources[$relative] = Hash-File (Join-Path $projectRoot $relative)
}
$selection = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$Name;sources=$sources;runtime_pins=$pins
    argv=@('D:\Python314\python.exe','-I','-S','-B','{snapshot}\software\v5\ordinary_lean\run_successor_admission.py','{output}',$bundle,$prepare,$manifestPath,'DMKN.ReadFootprint.Consumer.snapshot_predicate_applyBatches')
    limits=[ordered]@{cpu_seconds=120;wall_seconds=180;memory_mib=1536;active_processes=3;stdout_bytes=1048576;stderr_bytes=1048576}
}
if ($pins.Count -gt 256) { throw 'Runtime pin bound' }
Write-NewJson $selectionPath $selection
[ordered]@{selection=$selectionPath;sha256=(Hash-File $selectionPath);parent_manifest=$manifestPath;execution='NOT_STARTED'} | ConvertTo-Json
