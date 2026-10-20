# Run only the unresolved control with a source-justified expansion bound.
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$prior=Join-Path $checks 'ordinary-serving-controls-02-selection.json'
if ((Digest $prior) -cne '5d3a3581e68341d8a98dffc588bc73b5b63672350dc2e59f75c10ed7ff10f25d') { throw 'PRIOR_CHANGED' }
$old=Get-Content -LiteralPath $prior -Raw | ConvertFrom-Json
$sources=[ordered]@{}
foreach ($property in $old.sources.psobject.Properties) {
    if ((Digest (Join-Path $projectRoot $property.Name)) -cne $property.Value) { throw 'SOURCE_CHANGED' }
    $sources[$property.Name]=$property.Value
}
$entry='software/v5/client/test_serve_workspace03.py'
if ($sources.Contains($entry)) { throw 'NEW_SOURCE_COLLISION' }
$sources[$entry]=Digest (Join-Path $projectRoot $entry)
$runtime=[ordered]@{}
foreach ($property in $old.runtime_pins.psobject.Properties) {
    if ((Digest $property.Name) -cne $property.Value) { throw 'RUNTIME_CHANGED' }
    $runtime[$property.Name]=$property.Value
}
$name='ordinary-serving-controls-03'
$path=Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $path) -or (Test-Path -LiteralPath (Join-Path $checks $name))) { throw 'NOT_FRESH' }
$selected=[ordered]@{
    schema=$old.schema;name=$name;sources=$sources;runtime_pins=$runtime;limits=$old.limits
    argv=@($old.argv[0],'-I','-S','-B','{snapshot}\software\v5\client\test_serve_workspace03.py',
           '--output','{output}\controls')
}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selected|ConvertTo-Json -Depth 12)+"`n")
$stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{path=$path;sha256=(Digest $path);sources=$sources.Count;executed=$false}|ConvertTo-Json
