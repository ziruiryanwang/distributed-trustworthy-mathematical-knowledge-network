# Read-only retained artifact validation; never repeat graph or compilation.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'aggregate-artifact-validation-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $local $name),(Join-Path $local ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer) { throw 'FILE_REQUIRED' }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$sources = [ordered]@{
    'tools/Run-V5-Check.py'='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
    'software/v5/aggregate_guest/validate_artifact.py'='715733a37e150d307a99008970ea26fca84f5234beba17e4147577d58ed0f7c4'
}
foreach ($relative in $sources.Keys) {
    if ((Pin (Join-Path $projectRoot $relative)).sha256 -cne $sources[$relative]) { throw ('SOURCE_CHANGED:'+ $relative) }
}
$runtimePrior = Join-Path $local 'aggregate-admission-controls-01-selection.json'
if ((Pin $runtimePrior).sha256 -cne '4e57759d8aa1f359b996d837bcc00312759e9e9c8a55f99d8fc9bbefe3cf1a95') { throw 'PRIOR_RUNTIME' }
$prior = Get-Content -LiteralPath $runtimePrior -Raw | ConvertFrom-Json
$pythonRoot = Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\receiver\runtime\python'
$pins = [ordered]@{}
foreach ($property in $prior.runtime_pins.psobject.Properties) {
    if (-not $property.Name.StartsWith($pythonRoot+'\',[StringComparison]::OrdinalIgnoreCase)) { continue }
    if ((Pin $property.Name).sha256 -cne $property.Value) { throw 'PYTHON_RUNTIME_CHANGED' }
    $pins[$property.Name] = $property.Value
}
if ($pins.Count -ne 18) { throw 'PYTHON_CLOSURE' }
$resultPath = Join-Path $local 'aggregate-guest-compile-01\RESULT.json'
$mapPath = Join-Path $local 'aggregate-guest-compile-01\SOURCE-MAP.json'
if ((Pin $resultPath).sha256 -cne '81cce68d9b20f22b12d12d5d698084eb8eb101493de71c6e35cd6acb7b44f47a' -or (Pin $mapPath).sha256 -cne '75c710e3ee13f63cb6ef44da8656caa53c300bf649317d2b5669d8b9cde06ce0') { throw 'ADOPTED_FAILED_COMPILE_RECORDS' }
$built = Get-Content -LiteralPath $resultPath -Raw | ConvertFrom-Json
$map = Get-Content -LiteralPath $mapPath -Raw | ConvertFrom-Json
$files = @(
    'aggregate-guest-build-01/RESULT.json','aggregate-guest-build-01/SOURCE-MAP.json',
    'aggregate-guest-build-01/selection.json','aggregate-guest-build-01/commands/offline-aggregate-graph/stdout.txt',
    'aggregate-guest-build-01-attempt.json','aggregate-guest-compile-01/RESULT.json',
    'aggregate-guest-compile-01/FINALIZATION-FAILED.json','aggregate-guest-compile-01/ARTIFACT.json',
    'aggregate-guest-compile-01/SOURCE-MAP.json','aggregate-guest-compile-01/GRAPH-COMPARISON.json',
    'aggregate-guest-compile-01/selection.json','aggregate-guest-compile-01-attempt.json')
foreach ($file in $files) { $row = Pin (Join-Path $local $file); $pins[$row.path] = $row.sha256 }
$count = 0
foreach ($property in $map.project.psobject.Properties) {
    $row = Pin (Join-Path $map.reused_project $property.Name)
    if ($row.sha256 -cne $property.Value.sha256 -or $row.bytes -ne $property.Value.bytes) { throw 'REUSED_PROJECT_CHANGED' }
    $pins[$row.path] = $row.sha256; $count++
}
if ($count -ne 39) { throw 'EXACT_39_REUSED_FILES' }
foreach ($inputPin in @($map.controller,$built.artifact.user_elf,$built.artifact.link_map)+@($built.commands[0].logs)) {
    $row = Pin $inputPin.path
    if ($row.sha256 -cne $inputPin.sha256 -or $row.bytes -ne $inputPin.bytes) { throw 'ARTIFACT_OR_LOG_CHANGED' }
    $pins[$row.path] = $row.sha256
}
if ($pins.Count -ne 74) { throw 'EXACT_56_INPUT_PLUS_18_PYTHON_BINDINGS' }
foreach ($path in @($runtimePrior,(Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\RELEASE-MANIFEST.json'))) {
    $row = Pin $path; $pins[$row.path] = $row.sha256
}
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$pins
    argv=@((Join-Path $pythonRoot 'python.exe'),'-I','-S','-B','{snapshot}\software\v5\aggregate_guest\validate_artifact.py','--output','{output}\validation')
    limits=[ordered]@{cpu_seconds=30;wall_seconds=60;memory_mib=512;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected|ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=(Pin $selectionPath);sources=$sources.Count;runtime_pins=$pins.Count;new_compile_graph_guest_proof_calls=0;executed=$false} | ConvertTo-Json -Depth 5
