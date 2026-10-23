$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -ne $projectRoot) { throw 'Canonical workdir required' }
$origin = Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-native-admission-01'
$selectionHash = 'ab2f655448242587880129e62cca4bc5dc74638c1e8699e30b4a9f67e26fce5f'
$recoveryRelative = 'software/v5/ordinary_lean/run_native_admission_recovery.py'
$recoveryHash = 'e063c39127a5448784660cc946fb837ba68df2f173da9fa1745d6fb83e54e449'
function Hash-File([string] $Path) {
    (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
if ((Hash-File (Join-Path $origin 'selection.json')) -ne $selectionHash) { throw 'Origin selection changed' }
if ((Hash-File (Join-Path $projectRoot $recoveryRelative)) -ne $recoveryHash) { throw 'Reviewed recovery changed' }
$original = Get-Content -LiteralPath (Join-Path $origin 'selection.json') -Raw | ConvertFrom-Json
$operations = @(
    '271479fcbce08ebc01dc64502a83b82e578d7897548e3bc7e2a1304eff582a51',
    '5f300d0fa7e48fa4efc8bf9e359bd5f552e0c8572b95142afbca7b45fa913221',
    '7160c6db37d6548f76f6fa319131ca50c8428147f85f278697a9613eddf1abcb')
$calls = @('000-basis', '001-extension', '002-extension')
$names = [System.Collections.Generic.List[string]]::new()
@('selection.json','RESULT.json','command/stdout.txt','command/stderr.txt',
  'native-admission/PLAN.json','native-admission/PROFILE.json',
  'native-admission/catalog/ADOPTION.json','native-admission/catalog/catalog.sqlite',
  'native-admission/catalog/owner.lock') | ForEach-Object { $names.Add($_) }
for ($index = 0; $index -lt 2852; $index++) { $names.Add(('native-admission/evidence/{0:D5}.json' -f $index)) }
for ($index = 0; $index -lt 3; $index++) {
    $prefix = 'native-admission/calls/' + $calls[$index] + '/'
    $names.Add($prefix + 'SUPERVISION.json')
    $names.Add($prefix + 'supervision/stderr.txt')
    if ($index -lt 2) {
        $names.Add($prefix + 'worker-report.json')
        $names.Add('native-admission/catalog/operations/' + $operations[$index] + '/chunk.olean')
    }
    if ($index -gt 0) { $names.Add($prefix + 'plan.json'); $names.Add($prefix + 'units.json') }
}
$files = [ordered]@{}
$total = 0L
foreach ($relative in ($names | Sort-Object)) {
    $path = Join-Path $origin $relative
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or $item.Length -gt 64MB -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Invalid fixed input' }
    $files[$relative] = [ordered]@{ bytes = $item.Length; sha256 = (Hash-File $path) }
    $total += $item.Length
}
if ($total -gt 128MB) { throw 'Origin total bound' }
$manifest = [ordered]@{
    schema = 'DMKN_ORDINARY_ADMISSION_RECOVERY_V1'; origin = $origin
    original_selection_sha256 = $selectionHash
    profile_id = 'fd23ae289706e5a3277a3c4304de83d65498755dd014b234810e79539f5c8219'
    basis_id = 'cb8f9c2db2b5b53984be1ce8b5f540024264a1e2db41fc7226c594ee1f022299'
    accepted_root = 'e0053044c9c3974bc4912e2083ff5f2340e5fd9e2326594e62de9c7b0421d201'
    store_id = '12185a972a6302a0a70899e968f4c249d1994afd252ecbb74c91e59961b81eb5'
    known_spent_cpu_ticks64 = 7483
    disposition = 'ADOPTED_FIXED_ORIGIN_AFTER_KERNEL_SNAPSHOT_REVIEW'; files = $files
}
$inputDirectory = Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-native-recovery-01-inputs'
$selectionPath = Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-native-recovery-01.selection.json'
$outputDirectory = Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-native-recovery-01'
foreach ($path in @($inputDirectory, $selectionPath, $outputDirectory)) {
    if (Test-Path -LiteralPath $path) { throw ('Fresh path required: ' + $path) }
}
New-Item -ItemType Directory -Path $inputDirectory | Out-Null
function Write-NewJson([string] $Path, $Value) {
    $bytes = [Text.UTF8Encoding]::new($false).GetBytes(($Value | ConvertTo-Json -Depth 20) + "`n")
    $stream = [IO.File]::Open($Path, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    try { $stream.Write($bytes, 0, $bytes.Length); $stream.Flush($true) } finally { $stream.Dispose() }
}
$manifestPath = Join-Path $inputDirectory 'RECOVERY-MANIFEST.json'
Write-NewJson $manifestPath $manifest
$pins = [ordered]@{}
foreach ($property in $original.runtime_pins.PSObject.Properties) { $pins[$property.Name] = $property.Value }
$pins[(Join-Path $origin 'selection.json')] = $selectionHash
$pins[$manifestPath] = Hash-File $manifestPath
$sources = [ordered]@{
    'tools/Run-V5-Check.py' = (Hash-File (Join-Path $projectRoot 'tools/Run-V5-Check.py'))
}
$sources[$recoveryRelative] = $recoveryHash
$selection = [ordered]@{
    schema = 'DMKN_V5_LOCAL_CHECK_V1'; name = 'ordinary-native-recovery-01'
    sources = $sources; runtime_pins = $pins
    argv = @('D:\Python314\python.exe', '-I', '-S', '-B',
      '{snapshot}\software\v5\ordinary_lean\run_native_admission_recovery.py', '{output}', $manifestPath)
    limits = [ordered]@{ cpu_seconds = 360; wall_seconds = 420; memory_mib = 1536
      active_processes = 4; stdout_bytes = 1048576; stderr_bytes = 1048576 }
}
Write-NewJson $selectionPath $selection
[ordered]@{ selection = $selectionPath; sha256 = (Hash-File $selectionPath)
    manifest_sha256 = (Hash-File $manifestPath); original_files = $files.Count
    original_bytes = $total; execution = 'NOT_STARTED' } | ConvertTo-Json
