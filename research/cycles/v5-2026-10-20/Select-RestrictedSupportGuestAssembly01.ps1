# Root preparation: one assembly, only after independent actual build adoption.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$GuestResultSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$AssemblerSourceSha256
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'restricted-support-guest-image-assembly-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $local $name),(Join-Path $local ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) { throw 'ORDINARY_FILE_REQUIRED' }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$sources = [ordered]@{
    'tools/Run-V5-Check.py'='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
    'software/v5/bounded_parse_guest/assemble.py'='220f54cf19fb9bebfd61674df332113a9e0f98bbd003bcecb5a268738048ca01'
    'software/v5/restricted_support_guest/assemble.py'=$AssemblerSourceSha256
}
foreach ($relative in $sources.Keys) {
    if ((Pin (Join-Path $projectRoot $relative)).sha256 -cne $sources[$relative]) { throw ('SOURCE_CHANGED:'+ $relative) }
}
$pins = [ordered]@{}
$priorPath = Join-Path $local 'bounded-parse-image-assembly-01-selection.json'
if ((Pin $priorPath).sha256 -cne 'f78b388b6b6278ffbae2aa73ab50f5eadfe5f1527a744e2f4cc8799670abcb35') { throw 'ADOPTED_ASSEMBLY_SELECTION' }
$prior = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
$pythonRoot = Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\receiver\runtime\python'
foreach ($property in $prior.runtime_pins.psobject.Properties) {
    if (-not ($property.Name.StartsWith($pythonRoot+'\',[StringComparison]::OrdinalIgnoreCase) -or
        $property.Name.Contains('\driver-build-04\') -or $property.Name.EndsWith('\v1compat.elf'))) { continue }
    if ((Pin $property.Name).sha256 -cne $property.Value) { throw 'RETAINED_RUNTIME_CHANGED' }
    $pins[$property.Name] = $property.Value
}
if ($pins.Count -ne 21) { throw 'EXACT_PYTHON_DRIVER_KERNEL' }
$buildDir = Join-Path $local 'restricted-support-guest-build-01'
$buildPath = Join-Path $buildDir 'RESULT.json'
if ((Pin $buildPath).sha256 -cne $GuestResultSha256) { throw 'ADOPTED_BUILD_RESULT' }
$built = Get-Content -LiteralPath $buildPath -Raw | ConvertFrom-Json
if ($built.schema -cne 'DMKN_V5_RC_SUPPORT_GUEST_THREE_CRATE_BUILD_RESULT_V1' -or
    $built.status -cne 'PASS_RC_SUPPORT_GUEST_THREE_CRATE_COMPILES_ONLY' -or
    $built.compiler_calls -ne 3 -or $built.checker_compiles -ne 0 -or $built.module_compiles -ne 0 -or $built.cargo_calls -ne 0 -or
    $built.job.active_processes -ne 0 -or $built.job.terminated_processes -ne 0 -or
    ($built.commands.label -join ',') -cne 'rc-core,aggregate,guest' -or
    (Test-Path -LiteralPath (Join-Path $buildDir 'FINALIZATION-FAILED.json'))) { throw 'SUCCESSFUL_CLOSED_BUILD_REQUIRED' }
foreach ($command in $built.commands) {
    if ($command.status -cne 'COMMAND_COMPLETED' -or $command.exit_code -ne 0 -or
        $command.cleanup_errors.Count -ne 0 -or $command.job_after.active_processes -ne 0 -or
        $command.job_after.terminated_processes -ne 0) { throw 'CLOSED_COMMAND_REQUIRED' }
    $row = Pin (Join-Path $buildDir ('commands\'+$command.label+'\command.json'))
    $pins[$row.path] = $row.sha256
    foreach ($log in $command.logs) {
        $row = Pin $log.path
        if ($row.bytes -ne $log.bytes -or $row.sha256 -cne $log.sha256) { throw 'BUILD_LOG_CHANGED' }
        $pins[$row.path] = $row.sha256
    }
}
$selection = Get-Content -LiteralPath (Join-Path $buildDir 'selection.json') -Raw | ConvertFrom-Json
if ((Pin (Join-Path $buildDir 'selection.json')).sha256 -cne $built.selection_sha256 -or
    @($selection.production_sources.psobject.Properties).Count -ne 12 -or
    @($selection.adapters.psobject.Properties).Count -ne 2 -or
    @($built.outputs.psobject.Properties).Count -ne 5) { throw 'EXACT_BUILD_MAPS' }
foreach ($property in $selection.production_sources.psobject.Properties) {
    $row = Pin (Join-Path (Join-Path $buildDir 'project') $property.Name)
    if ($row.bytes -ne $property.Value.bytes -or $row.sha256 -cne $property.Value.sha256) { throw 'SNAPSHOT_CHANGED' }
    $pins[$row.path] = $row.sha256
}
foreach ($property in $selection.adapters.psobject.Properties) {
    $row = Pin (Join-Path $projectRoot $property.Name)
    if ($row.bytes -ne $property.Value.bytes -or $row.sha256 -cne $property.Value.sha256) { throw 'USED_ADAPTER_CHANGED' }
    $pins[$row.path] = $row.sha256
}
foreach ($property in $built.outputs.psobject.Properties) {
    $row = Pin $property.Value.path
    if ($row.bytes -ne $property.Value.bytes -or $row.sha256 -cne $property.Value.sha256) { throw 'BUILD_OUTPUT_CHANGED' }
    $pins[$row.path] = $row.sha256
}
$inputMap = Get-Content -LiteralPath (Join-Path $buildDir 'INPUT-MAP.json') -Raw | ConvertFrom-Json
if (@($inputMap.copied_module_artifacts.psobject.Properties).Count -ne 2) { throw 'EXACT_COPIED_MODULE_PAIR' }
foreach ($property in $inputMap.copied_module_artifacts.psobject.Properties) {
    if ($property.Name -cnotin @('libdmkn_module_relation.rlib','libdmkn_module_relation.rmeta')) { throw 'EXACT_MODULE_NAME' }
    $row = Pin (Join-Path (Join-Path $buildDir 'retained\modules') $property.Name)
    if ($row.bytes -ne $property.Value.bytes -or $row.sha256 -cne $property.Value.sha256) { throw 'COPIED_MODULE_CHANGED' }
    $pins[$row.path] = $row.sha256
}
$mapPin = Pin $built.artifact.link_map.path
if ($mapPin.bytes -ne $built.artifact.link_map.bytes -or $mapPin.sha256 -cne $built.artifact.link_map.sha256) { throw 'LINK_MAP_CHANGED' }
$pins[$mapPin.path] = $mapPin.sha256
foreach ($relative in @('RESULT.json','ARTIFACT.json','INPUT-MAP.json','SOURCE-MAP.json','RECIPES.json','selection.json')) {
    $row = Pin (Join-Path $buildDir $relative); $pins[$row.path] = $row.sha256
}
foreach ($path in @((Join-Path $local 'restricted-support-guest-build-01-attempt.json'),$priorPath,
    (Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\RELEASE-MANIFEST.json'))) {
    $row = Pin $path; $pins[$row.path] = $row.sha256
}
if (@($selection.native_adoption.psobject.Properties).Count -ne 3) { throw 'EXACT_NATIVE_ADOPTION_COUNT' }
foreach ($property in $selection.native_adoption.psobject.Properties) {
    $row = Pin $property.Value.path
    if ($row.bytes -ne $property.Value.bytes -or $row.sha256 -cne $property.Value.sha256) {
        throw 'ADOPTED_NATIVE_RECORD_CHANGED'
    }
    $pins[$row.path] = $row.sha256
}
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$pins
    argv=@((Join-Path $pythonRoot 'python.exe'),'-I','-S','-B','{snapshot}\software\v5\restricted_support_guest\assemble.py','--guest-result',$buildPath,'--guest-result-sha256',$GuestResultSha256,'--output','{output}\assembly')
    limits=[ordered]@{cpu_seconds=120;wall_seconds=120;memory_mib=1024;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected|ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=(Pin $selectionPath);sources=$sources.Count;runtime_pins=$pins.Count;assembler_calls=1;guest_calls=0;proof_calls=0;executed=$false} | ConvertTo-Json -Depth 5
