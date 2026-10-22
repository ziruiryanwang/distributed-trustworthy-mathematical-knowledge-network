# Prepare one small stdlib/inert command-boundary check; never dispatch.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$EntrySha,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ControlsSha
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function CheckPin([string]$path,[string]$expected) {
    $item=Get-Item -LiteralPath $path
    if($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -or
        (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $expected) {
        throw ('REVIEWED_PIN_CHANGED:'+ $path)
    }
}
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$name='typed-lifecycle-entry-controls-01'
$selectionPath=Join-Path $checks ($name+'-selection.json')
foreach($path in @($selectionPath,(Join-Path $checks $name))) {
    if(Test-Path -LiteralPath $path) { throw 'FRESH_CONTROLS_REQUIRED' }
}
$entry='software/v5/typed_production/lifecycle_operator.py'
$controls='software/v5/typed_production/lifecycle_controls.py'
$sources=[ordered]@{
    'tools/Run-V5-Check.py'='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
}
$sources[$entry]=$EntrySha
$sources[$controls]=$ControlsSha
foreach($row in $sources.GetEnumerator()) { CheckPin (Join-Path $projectRoot $row.Key) $row.Value }
if($sources.Count -ne 3) { throw 'EXACT_SOURCE_CENSUS' }
$basisPath=Join-Path $checks 'candidate-preflight-controls-01-selection.json'
CheckPin $basisPath '12d765027be1114a22b79fe806eb9dcb60d2182bc15b80eb2ba089b5285e23b1'
$basis=Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
$runtime=[ordered]@{}
foreach($row in $basis.runtime_pins.psobject.Properties) {
    CheckPin $row.Name $row.Value
    $runtime[$row.Name]=$row.Value
}
if($runtime.Count -ne 30 -or -not $runtime.Contains($basis.argv[0])) { throw 'EXACT_RUNTIME_BASIS' }
$selection=[ordered]@{schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($basis.argv[0],'-I','-S','-B',('{snapshot}\'+$controls.Replace('/','\')),
        '--entry',('{snapshot}\'+$entry.Replace('/','\')),'--entry-sha256',$EntrySha,'--output','{output}')
    limits=[ordered]@{cpu_seconds=30;wall_seconds=90;memory_mib=256;active_processes=1;stdout_bytes=1048576;stderr_bytes=1048576}}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selection|ConvertTo-Json -Depth 48)+"`n")
if($raw.Length -gt 1048576) { throw 'SELECTION_SIZE' }
$stream=[IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length);$stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=$selectionPath;selection_sha256=(Get-FileHash -LiteralPath $selectionPath -Algorithm SHA256).Hash.ToLowerInvariant();sources=$sources.Count;runtime_pins=$runtime.Count;executed=$false}|ConvertTo-Json
