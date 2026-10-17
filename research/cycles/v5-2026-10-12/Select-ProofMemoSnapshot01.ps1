# Prepare exact one-screen inputs only after actual image adoption; no launch.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$AssemblyResultSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$AssemblyOuterResultSha256
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'proof-memo-aggregate-snapshot-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
$configPath = Join-Path $local ($name+'-configuration.json')
foreach ($path in @($selectionPath,$configPath,(Join-Path $local $name),(Join-Path $local ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer) { throw 'FILE_REQUIRED' }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
function SaveNew([string]$path,$value) {
    $raw = [Text.UTF8Encoding]::new($false).GetBytes(($value|ConvertTo-Json -Depth 15)+"`n")
    $stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
}
$sources = [ordered]@{
    'tools/Run-V5-Check.py'='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
    'software/v5/aggregate_host/snapshot.py'='d99656a17891983e2ae5ee0afb78fd4695b0ac4746a58aade34977b36fd2f442'
    'software/v5/admission/__init__.py'='41985fbdd6cfd55b26852adfc784100713528430c8688fdff1fb3cdc5acafb54'
    'software/v5/admission/bindings.py'='233ff29992d524eb1d92d7f1beb9261479e76737acd591c923a30cd32588d1ee'
    'software/v5/modules/__init__.py'='1c69237f05e6b86129605789da098235453d00b2f0139502cdbe9206d5891946'
    'software/v5/modules/codec.py'='e01b7478640d72ad5e0634443c87d99a9bf91bc65d2fc2297355b92a27649f58'
    'software/v5/aggregate_claims/__init__.py'='c9440183d92c887c4f6bac36f4bd51b7cf935ddf0f3f155aac8b8f1d48ad6540'
    'software/v5/aggregate_claims/bindings.py'='a6777395353f0421111cc2a2a0b06208dfbe4d60549899a70a42cda0bda9e543'
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
$assemblyPath = Join-Path $local 'proof-memo-image-assembly-01\assembly\RESULT.json'
if ((Pin $assemblyPath).sha256 -cne $AssemblyResultSha256) { throw 'ADOPTED_ASSEMBLY_RESULT' }
$outerPath = Join-Path $local 'proof-memo-image-assembly-01\RESULT.json'
if ((Pin $outerPath).sha256 -cne $AssemblyOuterResultSha256) { throw 'ADOPTED_OUTER_ASSEMBLY_RESULT' }
$outer = Get-Content -LiteralPath $outerPath -Raw | ConvertFrom-Json
if ($outer.result.status -cne 'COMMAND_EXITED_ZERO_AND_CLOSED' -or $outer.result.child_exit_code -ne 0 -or $outer.result.cleanup_errors.Count -ne 0 -or $outer.result.job_closed -ne $true -or $outer.result.direct_child_reaped -ne $true -or $outer.result.final_job.active_processes -ne 0 -or $outer.result.termination_requested -ne $false) { throw 'CLEAN_OUTER_ASSEMBLY_REQUIRED' }
$assembly = Get-Content -LiteralPath $assemblyPath -Raw | ConvertFrom-Json
if ($assembly.status -cne 'PASS_NEW_AGGREGATE_IMAGE_ASSEMBLY_ONLY' -or $assembly.guest_executions -ne 0 -or $assembly.proof_calls -ne 0 -or $assembly.image_id -cnotmatch '^[0-9a-f]{64}$') { throw 'ASSEMBLY_ONLY_PASS_REQUIRED' }
if ((Pin $assembly.image.path).sha256 -cne $assembly.image.sha256) { throw 'ACTUAL_IMAGE_CHANGED' }
$hostPath = Join-Path $local 'aggregate-host-build-01\RESULT.json'
if ((Pin $hostPath).sha256 -cne '4cdb12b5e3aeaebcfef5e0370bd445f24ff6779b196ca69cbab60f9d57002a75') { throw 'ADOPTED_HOST_RESULT' }
$built = Get-Content -LiteralPath $hostPath -Raw | ConvertFrom-Json
if ((Pin $built.executable.path).sha256 -cne 'b1605995c957e06b7c4529d28dfc2a49e496cefae7629b3fdddfc4a1bfb6f6d1') { throw 'ACTUAL_HOST_CHANGED' }
$fixed = [ordered]@{
    'aggregate-claims-controls-02/evidence/actual-two-delta.bin'='7e21d092206b08a9a71231045b8152df4179ee6575cdc5e3afc704ef03c0be58'
    'aggregate-claims-controls-02/evidence/actual-two-delta/stdout.txt'='01d7c9cc45a16f520980e80672f90c0a97a69e31e344f748910df5abb24ffd0b'
    'module-base-production-01/finish-0/receipt.bin'='850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47'
}
foreach ($relative in $fixed.Keys) {
    $row = Pin (Join-Path $local $relative)
    if ($row.sha256 -cne $fixed[$relative]) { throw ('FIXTURE_CHANGED:'+ $relative) }
    $pins[$row.path] = $row.sha256
}
$config = [ordered]@{schema='DMKN_AGGREGATE_COST_SCREEN_V1';image_result=$assemblyPath;image_result_sha256=$AssemblyResultSha256;aggregate_image=$assembly.image_id;output=(Join-Path $local ($name+'\evidence'))}
SaveNew $configPath $config
$configPin = Pin $configPath
foreach ($path in @($assemblyPath,$assembly.image.path,(Join-Path $local 'proof-memo-image-assembly-01\RESULT.json'),$hostPath,$built.executable.path,$configPath,$runtimePrior,(Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\RELEASE-MANIFEST.json'))) {
    $row = Pin $path; $pins[$row.path] = $row.sha256
}
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$pins
    argv=@((Join-Path $pythonRoot 'python.exe'),'-I','-S','-B','{snapshot}\software\v5\aggregate_host\snapshot.py',$configPath,$configPin.sha256)
    limits=[ordered]@{cpu_seconds=180;wall_seconds=240;memory_mib=3072;active_processes=3;stdout_bytes=1048576;stderr_bytes=1048576}
}
SaveNew $selectionPath $selected
[ordered]@{selection=(Pin $selectionPath);configuration=$configPin;sources=$sources.Count;runtime_pins=$pins.Count;guest_calls=1;proof_calls=0;executed=$false} | ConvertTo-Json -Depth 5
