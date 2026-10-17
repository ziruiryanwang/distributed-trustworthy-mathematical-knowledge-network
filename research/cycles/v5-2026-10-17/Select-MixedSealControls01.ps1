# Prepare one pure conversion gate. This selector performs no Python/native call.
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$name='mixed-seal-preparation-controls-01'
$selectionPath=Join-Path $checks ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw 'NOT_FRESH' }
}
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
$previous=Join-Path $checks 'small-producer-controls-01-selection.json'
if ((Digest $previous) -cne '672a484b26f45f808966fc0967371bf7422743555ec82bf7353525bcbd094466') { throw 'RETAINED_SELECTION_CHANGED' }
$old=Get-Content -LiteralPath $previous -Raw | ConvertFrom-Json
$runtime=[ordered]@{}
foreach ($property in $old.runtime_pins.psobject.Properties) {
    if ((Digest $property.Name) -cne $property.Value) { throw 'RUNTIME_CHANGED' }
    $runtime[$property.Name]=$property.Value
}
$sources=[ordered]@{}
foreach ($relative in @('tools/Run-V5-Check.py',
    'software/v5/modules/__init__.py','software/v5/modules/codec.py',
    'software/v5/admission/__init__.py','software/v5/admission/bindings.py','software/v5/admission/verifier.py',
    'software/v5/production/__init__.py','software/v5/production/producer.py',
    'software/v5/delta/__init__.py','software/v5/delta/packet.py','software/v5/delta/receiver.py',
    'software/v5/delta_claims/__init__.py','software/v5/delta_claims/claims.py','software/v5/delta_claims/receiver.py',
    'software/v5/mixed_claims/__init__.py','software/v5/mixed_claims/packet.py',
    'software/v5/aggregate_claims/__init__.py','software/v5/aggregate_claims/bindings.py',
    'software/v5/aggregate_claims/input.py','software/v5/aggregate_claims/prepare_mixed.py',
    'software/v5/aggregate_claims/test_prepare_mixed.py')) {
    $sources[$relative]=Digest (Join-Path $projectRoot $relative)
}
$inputs=[ordered]@{
    'selected-frontier-layout-01/evidence/wire.bin'='898660ddeea92cefccbf793e35b1ee49ef4867c9daec24b5344f37a1ed375500'
    'selected-frontier-layout-01/evidence/header.bin'='49dd845edaec83f5b0cba5af38653f768e51ed95a4bb6ea7824c10bdd1c3169e'
    'module-base-production-01/finish-0/receipt.bin'='850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47'
}
foreach ($relative in $inputs.Keys) {
    $path=[IO.Path]::GetFullPath((Join-Path $checks $relative))
    if ((Digest $path) -cne $inputs[$relative]) { throw 'HELD_INPUT_CHANGED' }
    $runtime[$path]=$inputs[$relative]
}
$selection=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($old.argv[0],'-I','-S','-B','{snapshot}\software\v5\aggregate_claims\test_prepare_mixed.py')
    limits=[ordered]@{cpu_seconds=30;wall_seconds=90;memory_mib=512;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selection|ConvertTo-Json -Depth 12)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_BOUND' }
$stream=[IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{path=$selectionPath;sha256=(Digest $selectionPath);sources=$sources.Count;runtime_pins=$runtime.Count;executed=$false}|ConvertTo-Json
