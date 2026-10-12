# Root preparation only after independent successful guest-build adoption.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$GuestResultSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$AssemblerSourceSha256
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'bounded-parse-image-assembly-01'
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
    'software/v5/bounded_parse_guest/assemble.py'=$AssemblerSourceSha256
}
foreach ($relative in $sources.Keys) {
    if ((Pin (Join-Path $projectRoot $relative)).sha256 -cne $sources[$relative]) { throw ('SOURCE_CHANGED:'+ $relative) }
}
$pins = [ordered]@{}
$runtimePrior = Join-Path $local 'aggregate-admission-controls-01-selection.json'
if ((Pin $runtimePrior).sha256 -cne '4e57759d8aa1f359b996d837bcc00312759e9e9c8a55f99d8fc9bbefe3cf1a95') { throw 'PRIOR_RUNTIME' }
$prior = Get-Content -LiteralPath $runtimePrior -Raw | ConvertFrom-Json
$pythonRoot = Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\receiver\runtime\python'
foreach ($property in $prior.runtime_pins.psobject.Properties) {
    if (-not $property.Name.StartsWith($pythonRoot+'\',[StringComparison]::OrdinalIgnoreCase)) { continue }
    if ((Pin $property.Name).sha256 -cne $property.Value) { throw 'PYTHON_RUNTIME_CHANGED' }
    $pins[$property.Name] = $property.Value
}
if ($pins.Count -ne 18) { throw 'PYTHON_CLOSURE' }
$assemblyPrior = Join-Path $local 'module-image-assembly-04-selection.json'
if ((Pin $assemblyPrior).sha256 -cne 'f69121ae9bcc0910069bfee36d166dbd3dafe7f3cb3b6c43963bc04a89858378') { throw 'ASSEMBLY_PRIOR' }
$previous = Get-Content -LiteralPath $assemblyPrior -Raw | ConvertFrom-Json
foreach ($property in $previous.runtime_pins.psobject.Properties) {
    if (-not ($property.Name.Contains('\driver-build-04\') -or $property.Name.EndsWith('\v1compat.elf'))) { continue }
    if ((Pin $property.Name).sha256 -cne $property.Value) { throw 'DRIVER_KERNEL_CHANGED' }
    $pins[$property.Name] = $property.Value
}
if ($pins.Count -ne 21) { throw 'DRIVER_KERNEL_CLOSURE' }
$buildDir = Join-Path $local 'bounded-parse-direct-build-01'
$buildPath = Join-Path $buildDir 'RESULT.json'
if ((Pin $buildPath).sha256 -cne $GuestResultSha256) { throw 'ADOPTED_GUEST_RESULT' }
$built = Get-Content -LiteralPath $buildPath -Raw | ConvertFrom-Json
if ($built.schema -cne 'DMKN_V5_BOUNDED_PARSE_DIRECT_PROJECT_BUILD_RESULT_V1' -or
    $built.status -cne 'PASS_BOUNDED_PARSE_THREE_PROJECT_COMPILES_ONLY' -or
    $built.compiler_calls -ne 3 -or $built.cargo_calls -ne 0 -or $built.dependency_compiles -ne 0 -or
    $built.commands.Count -ne 3 -or $built.job.active_processes -ne 0 -or $built.job.terminated_processes -ne 0 -or
    (Test-Path -LiteralPath (Join-Path $buildDir 'FINALIZATION-FAILED.json'))) { throw 'SUCCESSFUL_CLOSED_BUILD_REQUIRED' }
if (($built.commands.label -join ',') -cne 'module,aggregate,guest') { throw 'EXACT_THREE_PROJECT_COMMANDS' }
foreach ($command in $built.commands) {
    if ($command.status -cne 'COMMAND_COMPLETED' -or $command.exit_code -ne 0 -or $command.cleanup_errors.Count -ne 0 -or $command.job_after.active_processes -ne 0) { throw 'EXACT_CLOSED_COMMANDS' }
}
foreach ($row in @($built.artifact.user_elf,$built.artifact.link_map)) {
    $actual = Pin $row.path
    if ($actual.bytes -ne $row.bytes -or $actual.sha256 -cne $row.sha256) { throw 'BUILD_ARTIFACT_CHANGED' }
}
foreach ($path in @($buildPath,(Join-Path $buildDir 'ARTIFACT.json'),(Join-Path $buildDir 'GRAPH-COMPARISON.json'),(Join-Path $buildDir 'INPUT-MAP.json'),(Join-Path $buildDir 'SOURCE-MAP.json'),(Join-Path $buildDir 'RECIPES.json'),(Join-Path $buildDir 'selection.json'),(Join-Path $local 'bounded-parse-direct-build-01-attempt.json'),$built.artifact.user_elf.path,$built.artifact.link_map.path,$runtimePrior,$assemblyPrior,(Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\RELEASE-MANIFEST.json'))) {
    $row = Pin $path; $pins[$row.path] = $row.sha256
}
$retainedDir = Join-Path $local 'bounded-parse-guest-build-02'
$recordPins = [ordered]@{
    'RESULT.json'='792ed5825ae3110dc3ddc1a85b49636b63469f5e4cb1d662e70d8ddf27d6b4b6'
    'FINALIZATION-FAILED.json'='36c6f5c6b7084dbb08d461c008ea8b39e71e80bf95cc90860e455936b637cf55'
    'selection.json'='a537fdbc9bf27b9a0832bb14a72aa07aad4d96abe9cc6bb433473a58935c16e2'
    'SOURCE-MAP.json'='1ca936d624d91d7d395ac89f7535e1564473ee62e05a6f357e754b6d2c93281b'
    'UNIT-GRAPH.json'='142224e56a81b3d73960a0aa5c5f80360658ccf0f1bff06883152cbfe92511fe'
    'GRAPH-COMPARISON.json'='36b0bd9bc55a15adca6f8e878bda3b2529d015fe841075aa3f2d30e771780bc5'
}
foreach ($relative in $recordPins.Keys) {
    $row = Pin (Join-Path $retainedDir $relative)
    if ($row.sha256 -cne $recordPins[$relative]) { throw ('RETAINED_RECORD_CHANGED:'+ $relative) }
    $pins[$row.path] = $row.sha256
}
$retainedMap = Get-Content -LiteralPath (Join-Path $retainedDir 'SOURCE-MAP.json') -Raw | ConvertFrom-Json
if (@($retainedMap.project.psobject.Properties).Count -ne 39) { throw 'RETAINED_SOURCE_COUNT' }
foreach ($property in $retainedMap.project.psobject.Properties) {
    $row = Pin (Join-Path (Join-Path $retainedDir 'project') $property.Name)
    if ($row.bytes -ne $property.Value.bytes -or $row.sha256 -cne $property.Value.sha256) { throw ('RETAINED_SOURCE_CHANGED:'+ $property.Name) }
    $pins[$row.path] = $row.sha256
}
$buildSelection = Get-Content -LiteralPath (Join-Path $buildDir 'selection.json') -Raw | ConvertFrom-Json
if (@($buildSelection.adapters.psobject.Properties).Count -ne 2) { throw 'DIRECT_ADAPTER_COUNT' }
foreach ($property in $buildSelection.adapters.psobject.Properties) {
    $row = Pin (Join-Path $projectRoot $property.Name)
    if ($row.bytes -ne $property.Value.bytes -or $row.sha256 -cne $property.Value.sha256) { throw ('USED_ADAPTER_CHANGED:'+ $property.Name) }
    $pins[$row.path] = $row.sha256
}
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$pins
    argv=@((Join-Path $pythonRoot 'python.exe'),'-I','-S','-B','{snapshot}\software\v5\bounded_parse_guest\assemble.py','--guest-result',$buildPath,'--guest-result-sha256',$GuestResultSha256,'--output','{output}\assembly')
    limits=[ordered]@{cpu_seconds=120;wall_seconds=120;memory_mib=1024;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected|ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=(Pin $selectionPath);sources=$sources.Count;runtime_pins=$pins.Count;assembler_calls=1;guest_calls=0;proof_calls=0;executed=$false} | ConvertTo-Json -Depth 5
