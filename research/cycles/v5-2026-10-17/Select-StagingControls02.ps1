# Fresh successor to the unused01 plan: metadata-only preview, same nine tests.
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$name='structural-staging-controls-02'
$selectionPath=Join-Path $checks ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw 'NOT_FRESH' }
}
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
$prior=Join-Path $checks 'structural-staging-controls-01-selection.json'
if ((Digest $prior) -cne '48d5d4740f37dddf9b786736d027b4acaae1105bf4d7476bc90bada4dc409ab4') { throw 'PRIOR_PLAN_CHANGED' }
if (Test-Path -LiteralPath (Join-Path $checks 'structural-staging-controls-01')) { throw 'SUPERSEDED_PLAN_MUST_BE_UNEXECUTED' }
$old=Get-Content -LiteralPath $prior -Raw | ConvertFrom-Json
$revised=@{
    'software/v5/client/workspace_staged.py'='bdd539d5f3fbc48d18215e25811178c5991e8475068156353e3cce7c1a97cf1a'
    'software/v5/client/test_workspace_staged.py'='81b2fd8e2df54a49f3f2b5a8bb30908c073263dd1df4fc6b11077a4e85009382'
}
$sources=[ordered]@{}
foreach ($property in $old.sources.psobject.Properties) {
    $key=$property.Name
    $expected=if ($revised.ContainsKey($key)) { $revised[$key] } else { $property.Value }
    if ((Digest (Join-Path $projectRoot $key)) -cne $expected) { throw ('SOURCE_CHANGED:'+ $key) }
    $sources[$key]=$expected
}
if ($sources.Count -ne 80) { throw 'EXACT_SOURCE_COUNT' }
foreach ($key in $revised.Keys) { if ($sources[$key] -cne $revised[$key]) { throw 'MISSING_REVISED_SOURCE' } }
$runtime=[ordered]@{}
foreach ($property in $old.runtime_pins.psobject.Properties) {
    if ((Digest $property.Name) -cne $property.Value) { throw 'RUNTIME_OR_DATA_CHANGED' }
    $runtime[$property.Name]=$property.Value
}
if ($runtime.Count -ne 19) { throw 'EXACT_RUNTIME_DATA_COUNT' }
$selection=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($old.argv)
    limits=[ordered]@{cpu_seconds=30;wall_seconds=90;memory_mib=512;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selection|ConvertTo-Json -Depth 12)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_BOUND' }
$stream=[IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{path=$selectionPath;sha256=(Digest $selectionPath);sources=$sources.Count;runtime_and_data_pins=$runtime.Count;executed=$false}|ConvertTo-Json
