# File-only preparation of one non-native adapter-control run; no dispatch.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$InitSha,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$SourceSha,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$OwnerSha,
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
$name='typed-renewal-controls-01'
$selectionPath=Join-Path $checks ($name+'-selection.json')
foreach($path in @($selectionPath,(Join-Path $checks $name))) {
    if(Test-Path -LiteralPath $path) { throw 'FRESH_CONTROLS_REQUIRED' }
}
$mapPath=Join-Path $checks 'distribution-candidate-preflight-01-input.json'
$mapSha='25e7c849e41f394498e21a60cc7800ecffb67b0cee1b3911d7164977ce4f2364'
CheckPin $mapPath $mapSha
$map=Get-Content -LiteralPath $mapPath -Raw -Encoding UTF8 | ConvertFrom-Json
if($map.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or @($map.sdk_sources.psobject.Properties).Count -ne 130) { throw 'EXACT_CURRENT_130' }
$runner='tools/Run-V5-Check.py'
$sources=[ordered]@{}
$sources[$runner]='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
CheckPin (Join-Path $projectRoot $runner) $sources[$runner]
foreach($property in $map.sdk_sources.psobject.Properties) {
    $row=$property.Value
    $path=[IO.Path]::GetFullPath($row.path)
    if(-not $path.StartsWith($projectRoot+'\software\v5\',[StringComparison]::Ordinal)) { throw 'SDK_SOURCE_SCOPE' }
    CheckPin $path $row.sha256
    if((Get-Item -LiteralPath $path).Length -ne $row.bytes) { throw 'SDK_SOURCE_SIZE' }
    $relative=$path.Substring($projectRoot.Length+1).Replace('\','/')
    if($sources.Contains($relative)) { throw 'DUPLICATE_PHYSICAL_SOURCE' }
    $sources[$relative]=$row.sha256
}
$additions=[ordered]@{
    'software/v5/typed_renewal/__init__.py'=$InitSha
    'software/v5/typed_renewal/source.py'=$SourceSha
    'software/v5/typed_renewal/owner.py'=$OwnerSha
    'software/v5/typed_renewal/controls.py'=$ControlsSha
}
foreach($entry in $additions.GetEnumerator()) {
    CheckPin (Join-Path $projectRoot $entry.Key) $entry.Value
    if($sources.Contains($entry.Key)) { throw 'NEW_SOURCE_MUST_BE_DISJOINT' }
    $sources[$entry.Key]=$entry.Value
}
if($sources.Count -ne 135) { throw 'EXACT_SOURCE_CENSUS' }
$basisPath=Join-Path $checks 'candidate-preflight-controls-01-selection.json'
# Existing immutable control selection supplies the same pinned Python/Job baseline.
$basisSha='12d765027be1114a22b79fe806eb9dcb60d2182bc15b80eb2ba089b5285e23b1'
CheckPin $basisPath $basisSha
$basis=Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
$runtime=[ordered]@{}
foreach($row in $basis.runtime_pins.psobject.Properties) {
    CheckPin $row.Name $row.Value
    $runtime[$row.Name]=$row.Value
}
if($runtime.Count -ne 30 -or -not $runtime.Contains($basis.argv[0])) { throw 'EXACT_RUNTIME_BASIS' }
$runtime[$mapPath]=$mapSha
$fixturePath=Join-Path $checks 'restricted-composition-controls-01\evidence\fixture.json'
$fixtureSha='019219ca4548dafbdaa814c209a4ec087229091750db3f3cf48fcc155269f40a'
CheckPin $fixturePath $fixtureSha
if((Get-Item -LiteralPath $fixturePath).Length -ne 84727) { throw 'EXACT_CONTROL_FIXTURE' }
$runtime[$fixturePath]=$fixtureSha
if($runtime.Count -ne 32) { throw 'EXACT_RUNTIME_CENSUS' }
$selection=[ordered]@{schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($basis.argv[0],'-I','-S','-B','{snapshot}\software\v5\typed_renewal\controls.py','--output','{output}')
    limits=[ordered]@{cpu_seconds=30;wall_seconds=90;memory_mib=256;active_processes=1;stdout_bytes=1048576;stderr_bytes=1048576}}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selection|ConvertTo-Json -Depth 48)+"`n")
if($raw.Length -gt 1048576) { throw 'SELECTION_SIZE' }
$stream=[IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length);$stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=$selectionPath;selection_sha256=(Get-FileHash -LiteralPath $selectionPath -Algorithm SHA256).Hash.ToLowerInvariant();sources=$sources.Count;runtime_pins=$runtime.Count;executed=$false}|ConvertTo-Json
