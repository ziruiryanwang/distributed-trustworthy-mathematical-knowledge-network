# One changed-boundary serving suite; no old test entry or native process.
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$prior=Join-Path $checks 'ordinary-runtime-controls-01-selection.json'
if ((Digest $prior) -cne '82c763d514d1f5d4cd39674053647be05e9e050640963522b61d829d119120d0') {
    throw 'PRIOR_SELECTION_CHANGED'
}
$old=Get-Content -LiteralPath $prior -Raw | ConvertFrom-Json
$sources=[ordered]@{}
foreach ($property in $old.sources.psobject.Properties) {
    if ((Digest (Join-Path $projectRoot $property.Name)) -cne $property.Value) {
        throw ('PREDECESSOR_SOURCE_CHANGED:'+ $property.Name)
    }
    $sources[$property.Name]=$property.Value
}
foreach ($relative in @('client/serve_workspace.py','client/test_serve_workspace.py')) {
    $key='software/v5/'+$relative
    if ($sources.Contains($key)) { throw 'NEW_SOURCE_COLLISION' }
    $sources[$key]=Digest (Join-Path $projectRoot $key)
}
$runtime=[ordered]@{}
foreach ($property in $old.runtime_pins.psobject.Properties) {
    if ((Digest $property.Name) -cne $property.Value) { throw 'RUNTIME_OR_DATA_CHANGED' }
    $runtime[$property.Name]=$property.Value
}
$name='ordinary-serving-controls-01'
$path=Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $path) -or (Test-Path -LiteralPath (Join-Path $checks $name))) { throw 'NOT_FRESH' }
$selected=[ordered]@{
    schema=$old.schema;name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($old.argv[0],'-I','-S','-B','{snapshot}\software\v5\client\test_serve_workspace.py',
           '--output','{output}\controls')
    limits=[ordered]@{cpu_seconds=30;wall_seconds=90;memory_mib=256;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selected|ConvertTo-Json -Depth 12)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_BOUND' }
$stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{path=$path;sha256=(Digest $path);sources=$sources.Count;runtime_pins=$runtime.Count;executed=$false}|ConvertTo-Json
