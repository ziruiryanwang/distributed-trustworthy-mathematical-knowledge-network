param([Parameter(Mandatory=$true)][ValidateSet('search','runtime')][string]$Suite)
# Select changed-boundary checks only; reuse the existing bounded Job runner.
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$name=if ($Suite -eq 'search') { 'search-validation-controls-01' } else { 'ordinary-runtime-controls-01' }
$selectionPath=Join-Path $checks ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw 'NOT_FRESH' }
}
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
$prior=Join-Path $checks 'structural-staging-controls-02-selection.json'
if ((Digest $prior) -cne '986fcd62f410cf13cf7bc3db4bc815f28445776884a466b6c2f024304921cfb5') {
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
$newFiles=@('client/workspace_validated.py','transport/search_validation.py')
if ($Suite -eq 'search') {
    $newFiles+=@('transport/test_search_validation.py')
    $entry='transport\test_search_validation.py'
} else {
    $newFiles+=@('client/runtime.py','client/test_runtime.py','authoring/worker.py')
    $entry='client\test_runtime.py'
}
foreach ($relative in $newFiles) {
    $key='software/v5/'+$relative
    if ($sources.Contains($key)) { throw 'NEW_SOURCE_COLLISION' }
    $sources[$key]=Digest (Join-Path $projectRoot $key)
}
$runtime=[ordered]@{}
foreach ($property in $old.runtime_pins.psobject.Properties) {
    if ((Digest $property.Name) -cne $property.Value) { throw 'RUNTIME_OR_DATA_CHANGED' }
    $runtime[$property.Name]=$property.Value
}
$selection=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($old.argv[0],'-I','-S','-B',('{snapshot}\software\v5\'+$entry),
           '--output','{output}\controls')
    limits=[ordered]@{cpu_seconds=30;wall_seconds=90;memory_mib=256;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selection|ConvertTo-Json -Depth 12)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_BOUND' }
$stream=[IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{path=$selectionPath;sha256=(Digest $selectionPath);sources=$sources.Count;runtime_pins=$runtime.Count;executed=$false}|ConvertTo-Json
