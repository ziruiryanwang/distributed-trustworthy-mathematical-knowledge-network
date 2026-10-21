# Fresh image-bound execution of the unchanged FIRST target, not proof production.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ImageResultSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ImageOuterSha256
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'typed-frontier-execution-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
$configPath = Join-Path $local ($name+'-configuration.json')
foreach ($path in @($selectionPath,$configPath,(Join-Path $local $name))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_EXECUTION_REQUIRED:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) { throw 'ORDINARY_FILE_REQUIRED' }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
function Record([string]$path,[string]$digest) {
    if ($digest -cnotmatch '^[0-9a-f]{64}$' -or (Pin $path).sha256 -cne $digest) { throw ('ADOPTED_RECORD_CHANGED:'+ $path) }
    Get-Content -LiteralPath $path -Raw -Encoding UTF8 | ConvertFrom-Json
}
function SaveNew([string]$path,$value) {
    $raw = [Text.UTF8Encoding]::new($false).GetBytes(($value|ConvertTo-Json -Depth 15)+"`n")
    if ($raw.Length -gt 1048576) { throw 'SELECTION_BYTE_LIMIT' }
    $stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
}
$priorPath = Join-Path $local 'selected-frontier-layout-01-selection.json'
$priorConfig = Join-Path $local 'selected-frontier-layout-01-configuration.json'
$selected = Record $priorPath '05888ba9f7fffb600c6b117f39bdfcb8e0b58b870ed311147a557ccd80dfcb45'
$config = Record $priorConfig '02cccc1cda2ac7a6a4971f5e077e04b26fcfa4dc384ff01cf84bfa4c3d5b6431'
if ($selected.name -cne 'selected-frontier-layout-01' -or
    $config.schema -cne 'DMKN_SMALL_AGGREGATE_COST_SCREEN_V1' -or
    $selected.limits.cpu_seconds -ne 180 -or $selected.limits.wall_seconds -ne 240 -or
    $selected.limits.memory_mib -ne 3072 -or $selected.limits.active_processes -ne 3) { throw 'EXACT_RETAINED_TARGET_ENVELOPE' }
$imageDir = Join-Path $local 'typed-guest-image-assembly-01'
$imageResultPath = Join-Path $imageDir 'assembly\RESULT.json'
$imageOuterPath = Join-Path $imageDir 'RESULT.json'
$assembly = Record $imageResultPath $ImageResultSha256
$outer = Record $imageOuterPath $ImageOuterSha256
if ($assembly.schema -cne 'DMKN_V5_TYPED_GUEST_IMAGE_ASSEMBLY_RESULT_V1' -or
    $assembly.status -cne 'PASS_NEW_AGGREGATE_IMAGE_ASSEMBLY_ONLY' -or
    $assembly.assembler_calls -ne 1 -or $assembly.guest_executions -ne 0 -or
    $assembly.proof_calls -ne 0 -or $assembly.mathematical_admission -ne $false -or
    $assembly.image_id -cnotmatch '^[0-9a-f]{64}$' -or $assembly.image_id -ceq $config.aggregate_image -or
    $outer.schema -cne 'DMKN_V5_LOCAL_CHECK_RESULT_V1' -or
    $outer.result.status -cne 'COMMAND_EXITED_ZERO_AND_CLOSED' -or
    $outer.result.child_exit_code -ne 0 -or $outer.result.final_job.active_processes -ne 0 -or
    $outer.result.final_job.terminated_processes -ne 0 -or $outer.result.cleanup_errors.Count -ne 0) { throw 'ADOPTED_NEW_ASSEMBLY_AND_CLEAN_OWNER' }
$imagePath = Join-Path $imageDir 'assembly\aggregate_image.bin'
if ($assembly.image.path -cne $imagePath) { throw 'EXACT_NEW_IMAGE_PATH' }
$imagePin = Pin $imagePath
if ($imagePin.bytes -ne $assembly.image.bytes -or $imagePin.bytes -gt 67108864 -or
    $imagePin.sha256 -cne $assembly.image.sha256) { throw 'EXACT_NEW_IMAGE_BYTES' }
$sources = [ordered]@{}
foreach ($property in $selected.sources.psobject.Properties) {
    if ((Pin (Join-Path $projectRoot $property.Name)).sha256 -cne $property.Value) { throw 'RETAINED_SOURCE_CHANGED' }
    $sources[$property.Name]=$property.Value
}
# No adapter change: existing exact-FIRST derivation and pinned generic host
# already take an explicit adopted image. They derive fresh header/wire/capsule.
$drop = @($priorConfig,
    (Join-Path $local 'proof-memo-image-assembly-01\assembly\RESULT.json'),
    (Join-Path $local 'proof-memo-image-assembly-01\assembly\aggregate_image.bin'),
    (Join-Path $local 'proof-memo-image-assembly-01\RESULT.json'))
$pins = [ordered]@{}
$dropped = 0
foreach ($property in $selected.runtime_pins.psobject.Properties) {
    if ($drop -ccontains $property.Name) { $dropped++; continue }
    if ((Pin $property.Name).sha256 -cne $property.Value) { throw 'RETAINED_RUNTIME_CHANGED' }
    $pins[$property.Name]=$property.Value
}
if ($dropped -ne 4 -or $pins.Count -ne 32 -or $sources.Count -ne 10) { throw 'EXACT_UNCHANGED_SOURCE_HOST_PARENT' }
foreach ($path in @($imageResultPath,$imageOuterPath,$imagePath,$priorPath,$priorConfig)) {
    $row=Pin $path; $pins[$row.path]=$row.sha256
}
# Preserve exact old FIRST/header for independent matched-target audit, not
# as inputs to the changed image or as transferred proof authority.
$comparison = [ordered]@{
    'selected-frontier-layout-01\evidence\wire.bin'='898660ddeea92cefccbf793e35b1ee49ef4867c9daec24b5344f37a1ed375500'
    'selected-frontier-layout-01\evidence\header.bin'='49dd845edaec83f5b0cba5af38653f768e51ed95a4bb6ea7824c10bdd1c3169e'
}
foreach ($relative in $comparison.Keys) {
    $row = Pin (Join-Path $local $relative)
    if ($row.sha256 -cne $comparison[$relative]) { throw 'UNCHANGED_MATHEMATICAL_TARGET' }
    $pins[$row.path]=$row.sha256
}
$config.image_result=$imageResultPath
$config.image_result_sha256=$ImageResultSha256
$config.aggregate_image=$assembly.image_id
$config.output=Join-Path $local ($name+'\evidence')
SaveNew $configPath $config
$configPin=Pin $configPath
$pins[$configPath]=$configPin.sha256
$selected.name=$name
$selected.sources=$sources
$selected.runtime_pins=$pins
$selected.argv[5]=$configPath
$selected.argv[6]=$configPin.sha256
if ($pins.Count -ne 40 -or $selected.argv[4] -cne '{snapshot}\software\v5\aggregate_small\frontier_snapshot.py') { throw 'EXACT_TYPED_EXECUTION_CLOSURE' }
SaveNew $selectionPath $selected
[ordered]@{selection=(Pin $selectionPath);configuration=$configPin;sources=$sources.Count;
    runtime_pins=$pins.Count;prospective_proof_screen_segments=128;proof_authorized=$false;executed=$false} | ConvertTo-Json -Depth 5
