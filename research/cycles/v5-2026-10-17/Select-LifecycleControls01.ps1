# Select the already-planned ten synthetic lifecycle controls; no native call.
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$name='generic-seal-lifecycle-controls-01'
$selectionPath=Join-Path $checks ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw 'NOT_FRESH' }
}
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
$prior=Join-Path $checks 'small-producer-controls-01-selection.json'
if ((Digest $prior) -cne '672a484b26f45f808966fc0967371bf7422743555ec82bf7353525bcbd094466') { throw 'RETAINED_SELECTION_CHANGED' }
$old=Get-Content -LiteralPath $prior -Raw | ConvertFrom-Json
$runtime=[ordered]@{}
foreach ($property in $old.runtime_pins.psobject.Properties) {
    if ((Digest $property.Name) -cne $property.Value) { throw 'RUNTIME_CHANGED' }
    $runtime[$property.Name]=$property.Value
}
if ($runtime.Count -ne 18) { throw 'EXACT_RUNTIME_COUNT' }
$sources=[ordered]@{}
foreach ($relative in @('tools/Run-V5-Check.py',
    'software/v5/aggregate_lifecycle/__init__.py','software/v5/aggregate_lifecycle/producer.py',
    'software/v5/aggregate_lifecycle/snapshot.py','software/v5/aggregate_lifecycle/test_lifecycle.py',
    'software/v5/aggregate_small/__init__.py','software/v5/aggregate_small/producer.py',
    'software/v5/production/__init__.py','software/v5/production/producer.py',
    'software/v5/aggregate_claims/__init__.py','software/v5/aggregate_claims/bindings.py',
    'software/v5/aggregate_claims/input.py','software/v5/aggregate_claims/prepare_mixed.py',
    'software/v5/mixed_claims/__init__.py','software/v5/mixed_claims/packet.py',
    'software/v5/delta/__init__.py','software/v5/delta/packet.py','software/v5/delta/receiver.py',
    'software/v5/delta_claims/__init__.py','software/v5/delta_claims/claims.py','software/v5/delta_claims/receiver.py',
    'software/v5/admission/__init__.py','software/v5/admission/bindings.py','software/v5/admission/verifier.py',
    'software/v5/modules/__init__.py','software/v5/modules/codec.py')) {
    $sources[$relative]=Digest (Join-Path $projectRoot $relative)
}
if ($sources.Count -ne 26) { throw 'EXACT_SOURCE_COUNT' }
$selection=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($old.argv[0],'-I','-S','-B','{snapshot}\software\v5\aggregate_lifecycle\test_lifecycle.py','--output','{output}\controls')
    limits=[ordered]@{cpu_seconds=30;wall_seconds=90;memory_mib=512;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selection|ConvertTo-Json -Depth 12)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_BOUND' }
$stream=[IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{path=$selectionPath;sha256=(Digest $selectionPath);sources=$sources.Count;runtime_pins=$runtime.Count;executed=$false}|ConvertTo-Json
