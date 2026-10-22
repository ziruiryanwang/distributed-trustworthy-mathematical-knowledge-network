# Prepare one finite changed-boundary run; no constructor or child dispatch here.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$PreparationSha,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ControlsSha
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function CheckPin($pin) {
    $item=Get-Item -LiteralPath $pin.path
    if($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -or
        $item.Length -ne $pin.bytes -or
        (Get-FileHash -LiteralPath $pin.path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $pin.sha256) {
        throw ('REVIEWED_PIN_CHANGED:'+ $pin.path)
    }
}
function SelectedSource([string]$relative,[string]$expected) {
    $path=Join-Path $projectRoot $relative
    CheckPin ([ordered]@{path=$path;bytes=(Get-Item -LiteralPath $path).Length;sha256=$expected})
    $sources[$relative]=$expected
}
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$name='release-producer-controls-01'
$selectionPath=Join-Path $checks ($name+'-selection.json')
foreach($path in @($selectionPath,(Join-Path $checks $name))) {
    if(Test-Path -LiteralPath $path) { throw 'FRESH_CONTROL_SELECTION_REQUIRED' }
}
$preparedPath=Join-Path $checks 'release-producer-component-01\PREPARATION.json'
$failedPath=Join-Path $checks 'release-producer-component-01\PREPARATION-FAILED.json'
if(Test-Path -LiteralPath $failedPath) { throw 'PREPARATION_FAILURE_OVERRIDES_SAVED_SUCCESS' }
CheckPin ([ordered]@{path=$preparedPath;bytes=(Get-Item -LiteralPath $preparedPath).Length;sha256=$PreparationSha})
$prepared=Get-Content -LiteralPath $preparedPath -Raw -Encoding UTF8 | ConvertFrom-Json
if($prepared.schema -cne 'DMKN_RELEASE_PRODUCER_COMPONENT_PREPARATION_V1' -or
    $prepared.status -cne 'FILES_STAGED_AND_HASH_VERIFIED_ONLY' -or
    $prepared.constructor_calls -ne 0 -or $prepared.proof_calls -ne 0 -or
    $prepared.full_distribution_validation -ne $false) { throw 'EXACT_COMPONENT_PREPARATION_SCOPE' }
$installation=Join-Path $checks 'release-producer-component-01\installation'
if($prepared.installation_root -cne $installation -or
    $prepared.profile.path -cne (Join-Path $checks 'release-producer-component-01\profile.json')) {
    throw 'EXACT_COMPONENT_LOCATIONS'
}
$runtime=[ordered]@{}
foreach($pin in @($prepared.installation_pins)+@($prepared.profile)) {
    CheckPin $pin
    if($runtime.Contains($pin.path) -and $runtime[$pin.path] -cne $pin.sha256) { throw 'CONFLICTING_RUNTIME_PIN' }
    $runtime[$pin.path]=$pin.sha256
}
if(@($prepared.installation_pins).Count -gt 64 -or @($prepared.installation_pins).Count -lt 27 -or
    $runtime.Count -ne @($prepared.installation_pins).Count+1 -or
    -not $runtime.Contains($prepared.python.path) -or
    $prepared.python.path -cne (Join-Path $installation 'base\receiver\runtime\python\python.exe')) {
    throw 'EXACT_BOUNDED_COMPONENT_RUNTIME'
}
$runtime[$preparedPath]=$PreparationSha
if($runtime.Count -gt 256) { throw 'OUTER_RUNTIME_BOUND' }
$sources=[ordered]@{}
$entry='software/v5/release_production/operator.py'
$controls='software/v5/release_production/controls.py'
$fixtures='software/v5/typed_production/lifecycle_controls.py'
$fixtureSha='21c26ced6138791d978dfddd28d49b5b5599fc2c2ee9abeda7d3a690f05fc1da'
SelectedSource 'tools/Run-V5-Check.py' '44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
SelectedSource $entry $prepared.entry.sha256
SelectedSource $controls $ControlsSha
SelectedSource $fixtures $fixtureSha
CheckPin $prepared.entry
if($prepared.entry.path -cne (Join-Path $installation 'sdk\v5\release_production\operator.py') -or
    $sources.Count -ne 4) { throw 'EXACT_SOURCE_AND_ENTRY_BINDING' }
$selection=[ordered]@{schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($prepared.python.path,'-I','-S','-B',('{snapshot}\'+$controls.Replace('/','\')),
        '--entry',('{snapshot}\'+$entry.Replace('/','\')),'--entry-sha256',$prepared.entry.sha256,
        '--entry-fixtures',('{snapshot}\'+$fixtures.Replace('/','\')),'--entry-fixtures-sha256',$fixtureSha,
        '--profile',$prepared.profile.path,'--profile-sha256',$prepared.profile.sha256,'--output','{output}')
    limits=[ordered]@{cpu_seconds=45;wall_seconds=120;memory_mib=384;active_processes=1;stdout_bytes=1048576;stderr_bytes=1048576}}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selection|ConvertTo-Json -Depth 48)+"`n")
if($raw.Length -gt 1048576) { throw 'SELECTION_SIZE' }
if(Test-Path -LiteralPath $failedPath) { throw 'PREPARATION_FAILURE_OVERRIDES_SAVED_SUCCESS' }
$stream=[IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length);$stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=$selectionPath;selection_sha256=(Get-FileHash -LiteralPath $selectionPath -Algorithm SHA256).Hash.ToLowerInvariant();sources=$sources.Count;runtime_pins=$runtime.Count;executed=$false}|ConvertTo-Json
