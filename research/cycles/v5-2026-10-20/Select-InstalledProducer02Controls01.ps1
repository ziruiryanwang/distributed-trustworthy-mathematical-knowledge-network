# Prepare only: two repaired-boundary groups, no product owner or native calls.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$DistributionSha,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ControlsSha,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$SourceReviewSha
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$name='installed-producer02-controls-01'
$selectionPath=Join-Path $checks ($name+'-selection.json')
$output=Join-Path $checks $name
function Ordinary([string]$path,[bool]$fresh=$false) {
    $full=[IO.Path]::GetFullPath($path)
    if ($full -cne $path -or -not $path.StartsWith($projectRoot+'\',[StringComparison]::Ordinal)) { throw 'CANONICAL_PATH' }
    $cursor=$full
    while ($cursor -and $cursor.Length -ge $projectRoot.Length) {
        if ((Test-Path -LiteralPath $cursor) -and
            (((Get-Item -LiteralPath $cursor).Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) { throw 'NO_REPARSE_PATH' }
        $cursor=[IO.Path]::GetDirectoryName($cursor)
    }
    if ($fresh) {
        if (Test-Path -LiteralPath $path) { throw 'FRESH_SELECTION_OR_OUTPUT_REQUIRED' }
    } elseif (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw 'ORDINARY_FILE_REQUIRED' }
}
function Pin([string]$path,[string]$expected,[long]$maximum=134217728) {
    Ordinary $path
    $item=Get-Item -LiteralPath $path
    if ($item.Length -le 0 -or $item.Length -gt $maximum -or
        (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $expected) { throw ('EXACT_SELECTED_PIN:'+ $path) }
    return [ordered]@{path=$path;bytes=$item.Length;sha256=$expected}
}
Ordinary $selectionPath $true
Ordinary $output $true
$sources=[ordered]@{}
$selectedPins=@()
function Source([string]$relative,[string]$sha) {
    $path=Join-Path $projectRoot $relative.Replace('/','\')
    $row=Pin $path $sha 2097152
    $sources[$relative]=$sha
    return $row
}
$entry='software/v5/installed_production02/release_production/operator.py'
$distribution='software/v5/installed_production02/body_location/distribution.py'
$controls='software/v5/installed_production02/controls.py'
$selectedPins+=Source 'tools/Run-V5-Check.py' '44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
$selectedPins+=Source $entry $EntrySha
$selectedPins+=Source $distribution $DistributionSha
$selectedPins+=Source $controls $ControlsSha
[long]$selectedSourceBytes=0
foreach ($row in $selectedPins) { $selectedSourceBytes += [long]$row.bytes }
if ($sources.Count -ne 4 -or $selectedSourceBytes -gt 16777216) { throw 'EXACT_SOURCE_BOUND' }
$review=Pin (Join-Path $projectRoot 'research\cycles\v5-2026-10-20\INSTALLED-PRODUCER02-REVIEW.md') $SourceReviewSha 1048576
$base=Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4'
$basePin=Pin (Join-Path $base 'RELEASE-MANIFEST.json') 'a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed' 8388608
$manifest=Get-Content -LiteralPath $basePin.path -Raw -Encoding UTF8 | ConvertFrom-Json
$runtime=[ordered]@{}
$runtime[$basePin.path]=$basePin.sha256
$runtime[$review.path]=$review.sha256
$pythonNames=@('python.exe','python314.dll','python3.dll','vcruntime140.dll','vcruntime140_1.dll',
    'DLLs/_asyncio.pyd','DLLs/_overlapped.pyd','DLLs/_socket.pyd','DLLs/select.pyd',
    'DLLs/_ssl.pyd','DLLs/libssl-3.dll','DLLs/libcrypto-3.dll','DLLs/_hashlib.pyd',
    'DLLs/_sqlite3.pyd','DLLs/sqlite3.dll','DLLs/_queue.pyd','DLLs/_ctypes.pyd','DLLs/libffi-8.dll')
$relativeRuntime=@('operator/commons.py','receiver/helpers/domains.py','receiver/helpers/run_stage.py')+
    @($pythonNames | ForEach-Object { 'receiver/runtime/python/'+$_ })
foreach ($relative in $relativeRuntime) {
    $expected=$manifest.files.$relative
    $row=Pin (Join-Path $base $relative.Replace('/','\')) $expected.sha256
    if ($row.bytes -ne $expected.bytes -or $runtime.Contains($row.path)) { throw 'RUNTIME_EXACT_ROW' }
    $runtime[$row.path]=$row.sha256
}
$auxiliary=[ordered]@{
    'product-local/v5-distribution-installed-producer-01/Mathematical Commons v5/base/RELEASE-MANIFEST.json'='a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed'
    'software/v5/installed_production/release_production/operator.py'='f404f0ba4d5177654fd02e999b00c0d8d104f1a4b85295414dff2720ddf6021a'
    'software/v5/installed_production/body_location/distribution.py'='afbea96badbead846aecc2d3014c19d38375cd2605c225ab0799ebde0ce48774'
}
foreach($relative in $auxiliary.Keys) {
    $row=Pin (Join-Path $projectRoot $relative.Replace('/','\')) $auxiliary[$relative] 8388608
    if ($runtime.Contains($row.path)) { throw 'AUXILIARY_DUPLICATE' }
    $runtime[$row.path]=$row.sha256
}
if ($runtime.Count -ne 26) { throw 'EXACT_RUNTIME_CLOSURE' }
$python=Join-Path $base 'receiver\runtime\python\python.exe'
function Copied([string]$relative) { return '{snapshot}\'+$relative.Replace('/','\') }
$selection=[ordered]@{schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($python,'-I','-S','-B',(Copied $controls),
        '--operator',(Copied $entry),'--operator-sha256',$EntrySha,
        '--distribution',(Copied $distribution),'--distribution-sha256',$DistributionSha,'--output','{output}')
    limits=[ordered]@{cpu_seconds=30;wall_seconds=90;memory_mib=256;active_processes=1;stdout_bytes=1048576;stderr_bytes=1048576}}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selection|ConvertTo-Json -Depth 16)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_SIZE' }
foreach ($row in $selectedPins) { $null=Pin $row.path $row.sha256 2097152 }
$null=Pin $review.path $review.sha256 1048576
$stream=[IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=$selectionPath;selection_sha256=(Get-FileHash -LiteralPath $selectionPath -Algorithm SHA256).Hash.ToLowerInvariant()
    sources=$sources.Count;runtime_pins=$runtime.Count;executed=$false}|ConvertTo-Json

)][string]$EntrySha,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$DistributionSha,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ControlsSha,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$SourceReviewSha
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$name='installed-producer-controls-01'
$selectionPath=Join-Path $checks ($name+'-selection.json')
$output=Join-Path $checks $name
function Ordinary([string]$path,[bool]$fresh=$false) {
    $full=[IO.Path]::GetFullPath($path)
    if ($full -cne $path -or -not $path.StartsWith($projectRoot+'\',[StringComparison]::Ordinal)) { throw 'CANONICAL_PATH' }
    $cursor=$full
    while ($cursor -and $cursor.Length -ge $projectRoot.Length) {
        if ((Test-Path -LiteralPath $cursor) -and
            (((Get-Item -LiteralPath $cursor).Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) { throw 'NO_REPARSE_PATH' }
        $cursor=[IO.Path]::GetDirectoryName($cursor)
    }
    if ($fresh) {
        if (Test-Path -LiteralPath $path) { throw 'FRESH_SELECTION_OR_OUTPUT_REQUIRED' }
    } elseif (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw 'ORDINARY_FILE_REQUIRED' }
}
function Pin([string]$path,[string]$expected,[long]$maximum=134217728) {
    Ordinary $path
    $item=Get-Item -LiteralPath $path
    if ($item.Length -le 0 -or $item.Length -gt $maximum -or
        (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $expected) { throw ('EXACT_SELECTED_PIN:'+ $path) }
    return [ordered]@{path=$path;bytes=$item.Length;sha256=$expected}
}
Ordinary $selectionPath $true
Ordinary $output $true
$sources=[ordered]@{}
$selectedPins=@()
function Source([string]$relative,[string]$sha) {
    $path=Join-Path $projectRoot $relative.Replace('/','\')
    $row=Pin $path $sha 2097152
    $sources[$relative]=$sha
    return $row
}
$contract='software/v5/installed_production/release_production/launch_contract.py'
$launcher='software/v5/installed_production/release_production/launch.py'
$distribution='software/v5/installed_production/body_location/distribution.py'
$controls='software/v5/installed_production/controls.py'
$selectedPins+=Source 'tools/Run-V5-Check.py' '44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
$selectedPins+=Source $contract $ContractSha
$selectedPins+=Source $launcher $LauncherSha
$selectedPins+=Source $distribution $DistributionSha
$selectedPins+=Source $controls $ControlsSha
[long]$selectedSourceBytes=0
foreach ($row in $selectedPins) { $selectedSourceBytes += [long]$row.bytes }
if ($sources.Count -ne 5 -or $selectedSourceBytes -gt 16777216) { throw 'EXACT_SOURCE_BOUND' }
$review=Pin (Join-Path $projectRoot 'research\cycles\v5-2026-10-20\INSTALLED-PRODUCER-SOURCE-REVIEW.md') $SourceReviewSha 1048576
$base=Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4'
$basePin=Pin (Join-Path $base 'RELEASE-MANIFEST.json') 'a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed' 8388608
$manifest=Get-Content -LiteralPath $basePin.path -Raw -Encoding UTF8 | ConvertFrom-Json
$runtime=[ordered]@{}
$runtime[$basePin.path]=$basePin.sha256
$runtime[$review.path]=$review.sha256
$pythonNames=@('python.exe','python314.dll','python3.dll','vcruntime140.dll','vcruntime140_1.dll',
    'DLLs/_asyncio.pyd','DLLs/_overlapped.pyd','DLLs/_socket.pyd','DLLs/select.pyd',
    'DLLs/_ssl.pyd','DLLs/libssl-3.dll','DLLs/libcrypto-3.dll','DLLs/_hashlib.pyd',
    'DLLs/_sqlite3.pyd','DLLs/sqlite3.dll','DLLs/_queue.pyd','DLLs/_ctypes.pyd','DLLs/libffi-8.dll')
$relativeRuntime=@('operator/commons.py','receiver/helpers/domains.py','receiver/helpers/run_stage.py')+
    @($pythonNames | ForEach-Object { 'receiver/runtime/python/'+$_ })
foreach ($relative in $relativeRuntime) {
    $expected=$manifest.files.$relative
    $row=Pin (Join-Path $base $relative.Replace('/','\')) $expected.sha256
    if ($row.bytes -ne $expected.bytes -or $runtime.Contains($row.path)) { throw 'RUNTIME_EXACT_ROW' }
    $runtime[$row.path]=$row.sha256
}
if ($runtime.Count -ne 23) { throw 'EXACT_RUNTIME_CLOSURE' }
$python=Join-Path $base 'receiver\runtime\python\python.exe'
function Copied([string]$relative) { return '{snapshot}\'+$relative.Replace('/','\') }
$selection=[ordered]@{schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($python,'-I','-S','-B',(Copied $controls),
        '--contract',(Copied $contract),'--contract-sha256',$ContractSha,
        '--launcher',(Copied $launcher),'--launcher-sha256',$LauncherSha,
        '--distribution',(Copied $distribution),'--distribution-sha256',$DistributionSha,'--output','{output}')
    limits=[ordered]@{cpu_seconds=30;wall_seconds=90;memory_mib=256;active_processes=1;stdout_bytes=1048576;stderr_bytes=1048576}}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selection|ConvertTo-Json -Depth 16)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_SIZE' }
foreach ($row in $selectedPins) { $null=Pin $row.path $row.sha256 2097152 }
$null=Pin $review.path $review.sha256 1048576
$stream=[IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=$selectionPath;selection_sha256=(Get-FileHash -LiteralPath $selectionPath -Algorithm SHA256).Hash.ToLowerInvariant()
    sources=$sources.Count;runtime_pins=$runtime.Count;executed=$false}|ConvertTo-Json
