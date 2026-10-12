# One offline reading of the saved failed prefix; no execution/proving retry.
param([Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$HelperSha256)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'aggregate-pc-attribution-01'
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
    'software/v5/aggregate_host/attribute.py'=$HelperSha256
}
foreach ($relative in $sources.Keys) {
    if ((Pin (Join-Path $projectRoot $relative)).sha256 -cne $sources[$relative]) { throw ('SOURCE_CHANGED:'+ $relative) }
}
$pins = [ordered]@{}
$priorPath = Join-Path $local 'aggregate-snapshot-01-selection.json'
if ((Pin $priorPath).sha256 -cne '224ec1f99cb8e9dc59e290eddf526be2bbc7cad7aa13a7146110e31972f08e79') { throw 'ADOPTED_SCREEN_SELECTION' }
$prior = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
$pythonRoot = Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\receiver\runtime\python'
foreach ($property in $prior.runtime_pins.psobject.Properties) {
    if (-not $property.Name.StartsWith($pythonRoot+'\',[StringComparison]::OrdinalIgnoreCase)) { continue }
    if ((Pin $property.Name).sha256 -cne $property.Value) { throw 'PYTHON_RUNTIME_CHANGED' }
    $pins[$property.Name] = $property.Value
}
if ($pins.Count -ne 18) { throw 'PYTHON_CLOSURE' }
$records = [ordered]@{
    diagnostic='aggregate-snapshot-01/evidence/diagnostic.json'
    execution_result='aggregate-snapshot-01/evidence/RESULT.json'
    execution_command='aggregate-snapshot-01/evidence/COMMAND.json'
    assembly_result='aggregate-image-assembly-01/assembly/RESULT.json'
    assembly_command='aggregate-image-assembly-01/assembly/COMMAND.json'
}
$config = [ordered]@{schema='DMKN_PC_ATTRIBUTION_SELECTION_V1'}
foreach ($key in $records.Keys) { $config[$key] = Pin (Join-Path $local $records[$key]); $pins[$config[$key].path] = $config[$key].sha256 }
if ($config.diagnostic.sha256 -cne 'ebd87c76cea9c321d1f64f5aee9ac5f1dc0c4aef0659c1937f0af84e4b259388' -or
    $config.execution_result.sha256 -cne 'a873a4b81d36397191ee8e550d6152eb77951f6204bd80406af73994f37820c5' -or
    $config.assembly_result.sha256 -cne '097775f5318420936b3cce6f16485467ae9fccd68d58947ec76facd210907420') { throw 'ADOPTED_EXACT_RECORDS' }
$assembly = Get-Content -LiteralPath $config.assembly_result.path -Raw | ConvertFrom-Json
$command = Get-Content -LiteralPath $config.assembly_command.path -Raw | ConvertFrom-Json
$validation = Get-Content -LiteralPath $command.artifact_validation.path -Raw | ConvertFrom-Json
foreach ($row in @($command.artifact_validation,$command.guest_build_result,$command.preserved_resource_failure,$validation.artifact.user_elf,$validation.artifact.link_map,$assembly.image)) {
    $actual = Pin $row.path
    if ($actual.sha256 -cne $row.sha256 -or $actual.bytes -ne $row.bytes) { throw 'RETAINED_LINEAGE_CHANGED' }
    $pins[$actual.path] = $actual.sha256
}
$config.output = Join-Path $local ($name+'\attribution')
SaveNew $configPath $config
$configPin = Pin $configPath
foreach ($path in @($configPath,$priorPath,(Join-Path $local 'aggregate-snapshot-01\evidence\wire.bin'),(Join-Path $local 'aggregate-snapshot-01\evidence\header.bin'),(Join-Path $local 'aggregate-snapshot-01\RESULT.json'),(Join-Path $local 'aggregate-image-assembly-01\RESULT.json'),(Join-Path $local 'aggregate-artifact-validation-01\RESULT.json'),(Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\RELEASE-MANIFEST.json'))) {
    $row = Pin $path; $pins[$row.path] = $row.sha256
}
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$pins
    argv=@((Join-Path $pythonRoot 'python.exe'),'-I','-S','-B','{snapshot}\software\v5\aggregate_host\attribute.py',$configPath,$configPin.sha256)
    limits=[ordered]@{cpu_seconds=30;wall_seconds=60;memory_mib=512;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
SaveNew $selectionPath $selected
[ordered]@{selection=(Pin $selectionPath);configuration=$configPin;sources=$sources.Count;runtime_pins=$pins.Count;guest_calls=0;proof_calls=0;executed=$false} | ConvertTo-Json -Depth 5
