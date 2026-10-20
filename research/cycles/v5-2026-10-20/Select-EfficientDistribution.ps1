# Fresh successor only: reused runtime and immutable input map, no cap increase.
param(
    [Parameter(Mandatory=$true)][string]$ExpectedSourceSha,
    [switch]$Install
)
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Save-NewJson([string]$path,$value) {
    $raw=[Text.UTF8Encoding]::new($false).GetBytes(($value|ConvertTo-Json -Depth 32)+"`n")
    if ($raw.Length -gt 1048576) { throw 'JSON_BOUND' }
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
}
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$basisPath=Join-Path $checks 'distribution-controls-01-selection.json'
if ((Digest $basisPath) -cne 'b8828e68483c57cbad17b29c88ef80e45afbe471c57312bc227d41385a6b492a') { throw 'RUNTIME_BASIS_CHANGED' }
$basis=Get-Content -LiteralPath $basisPath -Raw | ConvertFrom-Json
$productKey='software/v5/distribution_efficient/distribution.py'
$product=Join-Path $projectRoot $productKey
if ($ExpectedSourceSha -cnotmatch '^[0-9a-f]{64}$' -or (Digest $product) -cne $ExpectedSourceSha) { throw 'REVIEWED_SOURCE_REQUIRED' }
$sources=[ordered]@{
    'tools/Run-V5-Check.py'='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
}
$sources[$productKey]=$ExpectedSourceSha
if (-not $Install) {
    $testKey='software/v5/distribution_efficient/test_paths.py'
    $sources[$testKey]=Digest (Join-Path $projectRoot $testKey)
}
foreach ($key in $sources.Keys) {
    if ((Digest (Join-Path $projectRoot $key)) -cne $sources[$key]) { throw 'SOURCE_CHANGED' }
}
$runtime=[ordered]@{}
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    if ((Digest $property.Name) -cne $property.Value) { throw 'RUNTIME_CHANGED' }
    $runtime[$property.Name]=$property.Value
}
$name='distribution-efficient-controls-01'
$argv=@($basis.argv[0],'-I','-S','-B','{snapshot}\software\v5\distribution_efficient\test_paths.py','--output','{output}')
$limits=[ordered]@{cpu_seconds=20;wall_seconds=60;memory_mib=128;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
$inputPath=$null
if ($Install) {
    $name='distribution-build-02'
    $oldInput=Join-Path $checks 'distribution-01-input.json'
    if ((Digest $oldInput) -cne 'cf32059db4f9c6001efe3266ca34127f85b4ee4cd93a4e737c3183e3e2f9e64a') { throw 'IMMUTABLE_INPUT_BASIS_CHANGED' }
    $inputValue=Get-Content -LiteralPath $oldInput -Raw | ConvertFrom-Json
    $inputValue.distribution_source=[ordered]@{path=$product;bytes=(Get-Item -LiteralPath $product).Length;sha256=$ExpectedSourceSha}
    $inputPath=Join-Path $checks 'distribution-02-input.json'
    $destination=Join-Path $projectRoot 'product-local\v5-distribution-02\Mathematical Commons v5'
    if ((Test-Path -LiteralPath $inputPath) -or (Test-Path -LiteralPath $destination)) { throw 'FRESH_SUCCESSOR_REQUIRED' }
    Save-NewJson $inputPath $inputValue
    $argv=@($basis.argv[0],'-I','-S','-B','{snapshot}\software\v5\distribution_efficient\distribution.py','build',$inputPath,(Digest $inputPath),$destination)
    $limits=[ordered]@{cpu_seconds=60;wall_seconds=180;memory_mib=128;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$selectionPath=Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath (Join-Path $checks $name))) { throw 'FRESH_SELECTION_REQUIRED' }
Save-NewJson $selectionPath ([ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime;argv=$argv;limits=$limits
})
[ordered]@{path=$selectionPath;sha256=(Digest $selectionPath);input=$inputPath;sources=$sources.Count;executed=$false}|ConvertTo-Json
