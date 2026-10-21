# Prepare one same-target general/RC execution, not a proof or acceptance.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$PairSourceSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$RestrictedAssemblySha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$RestrictedAssemblyOuterSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$RestrictedGuestResultSha256
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'restricted-matched-execution-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
$configurationPath = Join-Path $local ($name+'-configuration.json')
foreach ($path in @($selectionPath,$configurationPath,(Join-Path $local $name))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_PAIR_REQUIRED:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) { throw 'ORDINARY_FILE_REQUIRED' }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
function ExactPin([string]$path,[string]$digest) {
    $row = Pin $path
    if ($row.sha256 -cne $digest) { throw ('ADOPTED_PIN_CHANGED:'+ $path) }
    $row
}
function ReadRecord([string]$path,[string]$digest) {
    $null = ExactPin $path $digest
    Get-Content -LiteralPath $path -Raw -Encoding UTF8 | ConvertFrom-Json
}
function SaveNew([string]$path,$value) {
    $raw = [Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 18)+"`n")
    if ($raw.Length -gt 1048576) { throw 'SELECTION_BYTE_LIMIT' }
    $stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($raw,0,$raw.Length);$stream.Flush($true) } finally { $stream.Dispose() }
}
$controlSelectionPath = Join-Path $local 'restricted-composition-controls-01-selection.json'
$controlSelection = ReadRecord $controlSelectionPath '7dd9e6b651f91ddf6638bceffc78593e7696d2df95c234075b15a68136f26291'
$generalSelectionPath = Join-Path $local 'typed-frontier-execution-01-selection.json'
$generalSelection = ReadRecord $generalSelectionPath 'a1ba369a538638ce7fb08abcbe1d65c1353f2af0b9138acb27463b42c209e9e0'
$sources = [ordered]@{}
foreach ($property in $controlSelection.sources.psobject.Properties) { $sources[$property.Name] = $property.Value }
foreach ($relative in @('software/v5/admission/__init__.py','software/v5/admission/bindings.py',
    'software/v5/aggregate_claims/__init__.py','software/v5/aggregate_claims/bindings.py','software/v5/aggregate_claims/input.py')) {
    if ($null -eq $generalSelection.sources.$relative) { throw 'RETAINED_PREPARER_SOURCE' }
    $sources[$relative] = $generalSelection.sources.$relative
}
$sources['software/v5/restricted_composition/prepare_execution.py']='fd184d7be0ca6eaa139a4b79764ac435c9e2036fea9116d591701d85a192e71d'
$sources['software/v5/restricted_composition/matched_pair.py']=$PairSourceSha256
if ($sources.Count -ne 16) { throw 'EXACT_16_PYTHON_SOURCES' }
foreach ($relative in $sources.Keys) { $null = ExactPin (Join-Path $projectRoot $relative) $sources[$relative] }
$config = [ordered]@{
    schema='DMKN_RC_MATCHED_EXECUTION_INPUT_V1'
    fixture=(ExactPin (Join-Path $local 'restricted-composition-controls-01\evidence\fixture.json') '019219ca4548dafbdaa814c209a4ec087229091750db3f3cf48fcc155269f40a')
    controls=[ordered]@{
        result=(ExactPin (Join-Path $local 'restricted-composition-controls-01\evidence\result.json') '1e7d6130444fd133e2f88b95e057e7338df8beaa0a42b14e9f471dd0b7b9fca2')
        outer=(ExactPin (Join-Path $local 'restricted-composition-controls-01\RESULT.json') '74646cc153e87c186586e97e699c19225c3a729a31377e1248a7ceb4585013a3')
        selection=(Pin $controlSelectionPath)
    }
    receipt=(ExactPin (Join-Path $local 'module-base-production-01\finish-0\receipt.bin') '850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47')
}
$pins = [ordered]@{}
$pythonRoot = Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\receiver\runtime\python'
foreach ($property in $controlSelection.runtime_pins.psobject.Properties) {
    if ($property.Name.StartsWith($pythonRoot+'\',[StringComparison]::OrdinalIgnoreCase)) {
        $null = ExactPin $property.Name $property.Value
        $pins[$property.Name]=$property.Value
    }
}
if ($pins.Count -ne 18) { throw 'EXACT_RETAINED_PYTHON_PINS' }
foreach ($path in @($controlSelectionPath,$generalSelectionPath)) { $row=Pin $path;$pins[$row.path]=$row.sha256 }
$base = Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4'
$manifestPath = Join-Path $base 'RELEASE-MANIFEST.json'
$manifest = ReadRecord $manifestPath 'a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed'
$pins[$manifestPath]='a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed'
foreach ($relative in @('operator/commons.py','receiver/helpers/domains.py','receiver/helpers/run_stage.py')) {
    $row = ExactPin (Join-Path $base $relative) $manifest.files.$relative.sha256
    if ($row.bytes -ne $manifest.files.$relative.bytes) { throw 'SUPERVISOR_EXTENT' }
    $pins[$row.path]=$row.sha256
}
foreach ($role in @('general','restricted')) {
    $hostName = if ($role -ceq 'general') { 'small-aggregate-snapshot-host-build-01' } else { 'restricted-snapshot-host-build-01' }
    $imageName = if ($role -ceq 'general') { 'typed-guest-image-assembly-01' } else { 'restricted-guest-image-assembly-01' }
    $guestName = if ($role -ceq 'general') { 'typed-guest-build-01' } else { 'restricted-guest-build-03' }
    $hostDigest = if ($role -ceq 'general') { '7ad07e35602092833d9f40e7f0775f0b4eceb451e52853875bd5baeaf63f78b1' } else { 'ecbfeb97fe6d290b687945a1b8975c85d976274bdaa29943563453b36074a404' }
    $imageDigest = if ($role -ceq 'general') { '4c26d075d850ff38a0922dbbdfad00303d16b49dee41f71a859f3777166e530c' } else { $RestrictedAssemblySha256 }
    $outerDigest = if ($role -ceq 'general') { '174878e768ed578e0a4f239de8423591ebf4ea34f09213e52c84aff46362b33b' } else { $RestrictedAssemblyOuterSha256 }
    $guestDigest = if ($role -ceq 'general') { 'b1b4f7a82aabddc5dd3349a4f82ba79e846517a6db94c3a3d911702c7d6576a4' } else { $RestrictedGuestResultSha256 }
    $hostDir=Join-Path $local $hostName
    $imageDir=Join-Path $local $imageName
    $guestDir=Join-Path $local $guestName
    $hostRecords=[ordered]@{
        result=(ExactPin (Join-Path $hostDir 'RESULT.json') $hostDigest)
        attempt=(Pin (Join-Path $local ($hostName+'-attempt.json')))
        selection=(Pin (Join-Path $local ($hostName+'-selection.json')))
        source_map=(Pin (Join-Path $hostDir 'source-map.json'))
        command=(Pin (Join-Path $hostDir 'compile-command.json'))
    }
    $imageRecords=[ordered]@{
        result=(ExactPin (Join-Path $imageDir 'assembly\RESULT.json') $imageDigest)
        outer=(ExactPin (Join-Path $imageDir 'RESULT.json') $outerDigest)
        guest_result=(ExactPin (Join-Path $guestDir 'RESULT.json') $guestDigest)
        guest_attempt=(Pin (Join-Path $local ($guestName+'-attempt.json')))
    }
    $config[$role]=[ordered]@{host_build=$hostRecords;assembly=$imageRecords}
    foreach ($records in @($hostRecords,$imageRecords)) {
        foreach ($row in $records.Values) { $pins[$row.path]=$row.sha256 }
    }
    $hostResult=ReadRecord $hostRecords.result.path $hostDigest
    $imageResult=ReadRecord $imageRecords.result.path $imageDigest
    foreach ($artifact in @($hostResult.executable,$imageResult.image)) {
        $row=ExactPin $artifact.path $artifact.sha256
        if ($row.bytes -ne $artifact.bytes) { throw 'ACTUAL_ARTIFACT_EXTENT' }
        $pins[$row.path]=$row.sha256
    }
}
foreach ($row in @($config.fixture,$config.receipt,$config.controls.result,$config.controls.outer)) { $pins[$row.path]=$row.sha256 }
SaveNew $configurationPath $config
$configurationPin=Pin $configurationPath
$pins[$configurationPath]=$configurationPin.sha256
$selected=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$pins
    argv=@((Join-Path $pythonRoot 'python.exe'),'-I','-S','-B','{snapshot}\software\v5\restricted_composition\matched_pair.py',
        '--input',$configurationPath,'--input-sha',$configurationPin.sha256,'--output','{output}\pair')
    limits=[ordered]@{cpu_seconds=420;wall_seconds=600;memory_mib=4096;active_processes=3;stdout_bytes=1048576;stderr_bytes=1048576}
}
if ($pins.Count -gt 256) { throw 'FINITE_PIN_CLOSURE' }
SaveNew $selectionPath $selected
[ordered]@{selection=(Pin $selectionPath);configuration=$configurationPin;sources=$sources.Count;runtime_pins=$pins.Count;
    guest_execution_count=2;proof_authorized=$false;executed=$false} | ConvertTo-Json -Depth 6
