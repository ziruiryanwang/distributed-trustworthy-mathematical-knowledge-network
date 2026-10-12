# Selection preparation only, after independent retained-artifact adoption.
param([Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ValidationResultSha256)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'aggregate-image-assembly-01'
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
    'software/v5/aggregate_guest/assemble.py'='61587d9a15a093c25b89f3e7d76439011c39831cbca8d19d986cd45db5426750'
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
$buildPath = Join-Path $local 'aggregate-guest-compile-01\RESULT.json'
if ((Pin $buildPath).sha256 -cne '81cce68d9b20f22b12d12d5d698084eb8eb101493de71c6e35cd6acb7b44f47a') { throw 'ACTUAL_RETAINED_COMPILE_PREFIX' }
$built = Get-Content -LiteralPath $buildPath -Raw | ConvertFrom-Json
if ($built.status -cne 'PASS_OPTIMIZED_EXACT_WARRANT_AGGREGATE_GUEST_COMPILE_ONLY' -or $built.commands.Count -ne 1 -or $built.job.active_processes -ne 0) { throw 'CLOSED_COMPILER_PREFIX_REQUIRED' }
$failurePath = Join-Path $local 'aggregate-guest-compile-01\FINALIZATION-FAILED.json'
if ((Pin $failurePath).sha256 -cne 'd0d6d8980c492d43a8927825aa153271543fa18d960305db5bde1e51c323dd54') { throw 'ORIGINAL_RESOURCE_FAILURE_MUST_REMAIN' }
$validationPath = Join-Path $local 'aggregate-artifact-validation-01\validation\RESULT.json'
if ((Pin $validationPath).sha256 -cne $ValidationResultSha256) { throw 'ADOPTED_ARTIFACT_VALIDATION' }
$validation = Get-Content -LiteralPath $validationPath -Raw | ConvertFrom-Json
if ($validation.status -cne 'PASS_REVALIDATED_AGGREGATE_GUEST_ARTIFACT_ONLY' -or $validation.old_failure_preserved -ne $true -or $validation.prior_budget_met -ne $false -or (Test-Path -LiteralPath (Join-Path $local 'aggregate-artifact-validation-01\validation\FINALIZATION-FAILED.json'))) { throw 'DISTINCT_ARTIFACT_ONLY_ADOPTION_REQUIRED' }
if ((Pin $built.artifact.user_elf.path).sha256 -cne $built.artifact.user_elf.sha256) { throw 'ELF_CHANGED' }
foreach ($path in @($buildPath,$failurePath,$validationPath,(Join-Path $local 'aggregate-artifact-validation-01\RESULT.json'),$built.artifact.user_elf.path,(Join-Path $local 'aggregate-guest-compile-01-attempt.json'),(Join-Path $local 'aggregate-guest-build-01\RESULT.json'),(Join-Path $local 'aggregate-guest-build-01\commands\offline-aggregate-graph\stdout.txt'),(Join-Path $local 'aggregate-guest-build-01-attempt.json'),$runtimePrior,$assemblyPrior,(Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\RELEASE-MANIFEST.json'))) {
    $row = Pin $path; $pins[$row.path] = $row.sha256
}
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$pins
    argv=@((Join-Path $pythonRoot 'python.exe'),'-I','-S','-B','{snapshot}\software\v5\aggregate_guest\assemble.py','--artifact-validation',$validationPath,'--artifact-validation-sha256',$ValidationResultSha256,'--output','{output}\assembly')
    limits=[ordered]@{cpu_seconds=120;wall_seconds=120;memory_mib=1024;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected|ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=(Pin $selectionPath);sources=$sources.Count;runtime_pins=$pins.Count;assembler_calls=1;guest_calls=0;proof_calls=0;executed=$false} | ConvertTo-Json -Depth 5
