# Prepare one focused structural-staging selection, not a test/proof launch.
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$name='structural-staging-controls-01'
$selectionPath=Join-Path $checks ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw 'NOT_FRESH' }
}
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
$prior=Join-Path $checks 'search-resilience-controls-01-selection.json'
if ((Digest $prior) -cne '6615ff9b994a2deca02556936b7a272b74beecb8796829642945eafa970f30af') { throw 'RETAINED_SELECTION_CHANGED' }
$old=Get-Content -LiteralPath $prior -Raw | ConvertFrom-Json
$sources=[ordered]@{}
foreach ($property in $old.sources.psobject.Properties) {
    $key=$property.Name
    if ((Digest (Join-Path $projectRoot $key)) -cne $property.Value) { throw ('PRIOR_SOURCE_CHANGED:'+ $key) }
    if ($key -in @('software/v5/transport/test_search_resilience.py','software/v5/discovery/test_candidate_query.py')) { continue }
    $sources[$key]=$property.Value
}
foreach ($relative in @('client/test_workspace_mixed.py','client/test_workspace_evidence.py',
                        'client/test_workspace_staged.py','client/workspace_staged.py','transport/semantic_staging.py')) {
    $key='software/v5/'+$relative
    $sources[$key]=Digest (Join-Path $projectRoot $key)
}
if ($sources.Count -ne 80) { throw 'EXACT_SOURCE_COUNT' }
$required=@{
    'tools/Run-V5-Check.py'='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
    'software/v5/client/workspace_staged.py'='b31b34d04a72fe668e2898dab73f7117503ae036422ae9e2b9dae4b698d06dde'
    'software/v5/transport/semantic_staging.py'='1b58f247a4f03c393fe6e52fb22037d56449b183bbb63b2767ab1b344c523be2'
    'software/v5/client/test_workspace_staged.py'='48020bea16bbe7b22294a6b2f5726862282f0036f8bcd6317ea101ff056e0120'
}
foreach ($key in $required.Keys) {
    if ($sources[$key] -cne $required[$key]) { throw ('SELECTED_SOURCE_CHANGED:'+ $key) }
}
$runtime=[ordered]@{}
foreach ($property in $old.runtime_pins.psobject.Properties) {
    if ((Digest $property.Name) -cne $property.Value) { throw 'RUNTIME_CHANGED' }
    $runtime[$property.Name]=$property.Value
}
if ($runtime.Count -ne 18) { throw 'EXACT_PREDECESSOR_RUNTIME_COUNT' }
$foundation=Join-Path $checks 'receipt-prepare-01\prepared\foundation.json'
if ((Get-Item -LiteralPath $foundation).Length -ne 23313 -or
    (Digest $foundation) -cne '736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c') { throw 'FOUNDATION_DATA_PIN' }
$runtime[$foundation]='736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c'
$selection=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($old.argv[0],'-I','-S','-B','{snapshot}\software\v5\client\test_workspace_staged.py',
           '--output','{output}\controls','--foundation',$foundation)
    limits=[ordered]@{cpu_seconds=30;wall_seconds=90;memory_mib=512;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selection|ConvertTo-Json -Depth 12)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_BOUND' }
$stream=[IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{path=$selectionPath;sha256=(Digest $selectionPath);sources=$sources.Count;runtime_and_data_pins=$runtime.Count;executed=$false}|ConvertTo-Json
