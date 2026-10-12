# One offline attribution of the newly retained failed prefix; no guest rerun.
param([Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$AdapterSourceSha256)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'bounded-parse-pc-attribution-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
$configPath = Join-Path $local ($name+'-configuration.json')
foreach ($path in @($selectionPath,$configPath,(Join-Path $local $name))) {
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
    'software/v5/bounded_parse_guest/attribute.py'=$AdapterSourceSha256
    'software/v5/aggregate_host/attribute.py'='0fc2ca9b35892cf86b3f8fdbf124db8cdb31f6cd20658125e2d6c23967c3a786'
}
foreach ($relative in $sources.Keys) {
    if ((Pin (Join-Path $projectRoot $relative)).sha256 -cne $sources[$relative]) { throw ('SOURCE_CHANGED:'+ $relative) }
}
$pins = [ordered]@{}
$priorPath = Join-Path $local 'bounded-parse-aggregate-snapshot-01-selection.json'
if ((Pin $priorPath).sha256 -cne '115c00c10b33e75e72b4427061a1b933cb3b632e0ed70681611cb6d766100719') { throw 'ADOPTED_SCREEN_SELECTION' }
$prior = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
$pythonRoot = Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\receiver\runtime\python'
foreach ($property in $prior.runtime_pins.psobject.Properties) {
    if (-not $property.Name.StartsWith($pythonRoot+'\',[StringComparison]::OrdinalIgnoreCase)) { continue }
    if ((Pin $property.Name).sha256 -cne $property.Value) { throw 'PYTHON_RUNTIME_CHANGED' }
    $pins[$property.Name] = $property.Value
}
if ($pins.Count -ne 18) { throw 'PYTHON_CLOSURE' }
$records = [ordered]@{
    build_result=@('bounded-parse-direct-build-01/RESULT.json','694d205b63082ecd02536eb70b16ae08a271f06d66d5df95f296a51a607ce22b')
    build_attempt=@('bounded-parse-direct-build-01-attempt.json','692d111e16ace683c0ae6b267ebabacbf12132d509487efc040641ccec53437a')
    artifact=@('bounded-parse-direct-build-01/ARTIFACT.json','d551a90cb1af3ed77c064bb457f34c38aaa9acc0eaf766143393cdb1c09dccb8')
    source_map=@('bounded-parse-direct-build-01/SOURCE-MAP.json','35387a79067d4868e02076c71c9128b1695fe0371524493f87e28de51fa19c3e')
    assembly_result=@('bounded-parse-image-assembly-01/assembly/RESULT.json','696774f9616ffd0f8a058eccf5fbf13f9f6b6e2eb0cfdbb5f7ee6acde75e6b7a')
    assembly_outer=@('bounded-parse-image-assembly-01/RESULT.json','f92ac44d3b2b12c677e3dcbe819dd64703cfd9f1da00d01efd58bb68e49c47ab')
    assembly_command=@('bounded-parse-image-assembly-01/assembly/COMMAND.json','fa544ea6ce87fee63a1b70e3e443461fa7f535e34b524de5979f9bb456840cde')
    screen_result=@('bounded-parse-aggregate-snapshot-01/evidence/RESULT.json','bc7fae70d1a7cde35a3db76a075ff289d8e082dea90b4ec2f726fb05ed99ba05')
    screen_outer=@('bounded-parse-aggregate-snapshot-01/RESULT.json','a4db15321bc9084ba5db4c7f4dbbb702a391909c8cafe7fd7d82f7ecec6237e9')
    screen_command=@('bounded-parse-aggregate-snapshot-01/evidence/COMMAND.json','86330929aa77c80bc641a924a66f2b855947d73368db8217a7f80e6ef69901ce')
    diagnostic=@('bounded-parse-aggregate-snapshot-01/evidence/diagnostic.json','dca409e07e44f7647c2b248167cadcba6f5ad0827af83a3aa3173e0aee0bda72')
    baseline_report=@('aggregate-pc-attribution-01/attribution/RESULT.json','31b29b7a8888fbfa0337fbf3a72b3269d2facbf05513d0e27a23ac4ca91de84b')
}
$config = [ordered]@{schema='DMKN_BOUNDED_PARSE_ATTRIBUTION_SELECTION_V1';records=[ordered]@{};output=(Join-Path $local ($name+'\attribution'))}
foreach ($key in $records.Keys) {
    $row = Pin (Join-Path $local $records[$key][0])
    if ($row.sha256 -cne $records[$key][1]) { throw ('ADOPTED_RECORD_CHANGED:'+ $key) }
    $config.records[$key] = $row; $pins[$row.path] = $row.sha256
}
$artifact = Get-Content -LiteralPath $config.records.artifact.path -Raw | ConvertFrom-Json
$assembly = Get-Content -LiteralPath $config.records.assembly_result.path -Raw | ConvertFrom-Json
$command = Get-Content -LiteralPath $config.records.screen_command.path -Raw | ConvertFrom-Json
foreach ($row in @($artifact.user_elf,$artifact.link_map,$assembly.image)) {
    $actual = Pin $row.path
    if ($actual.bytes -ne $row.bytes -or $actual.sha256 -cne $row.sha256) { throw 'ARTIFACT_CHANGED' }
    $pins[$actual.path] = $actual.sha256
}
SaveNew $configPath $config
$configPin = Pin $configPath
foreach ($path in @($command.argv[4],$command.argv[5],$command.argv[12],$configPath,$priorPath,(Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\RELEASE-MANIFEST.json'))) {
    $row = Pin $path; $pins[$row.path] = $row.sha256
}
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$pins
    argv=@((Join-Path $pythonRoot 'python.exe'),'-I','-S','-B','{snapshot}\software\v5\bounded_parse_guest\attribute.py',$configPath,$configPin.sha256)
    limits=[ordered]@{cpu_seconds=30;wall_seconds=60;memory_mib=512;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
SaveNew $selectionPath $selected
[ordered]@{selection=(Pin $selectionPath);configuration=$configPin;sources=$sources.Count;runtime_pins=$pins.Count;guest_calls=0;proof_calls=0;executed=$false} | ConvertTo-Json -Depth 5
