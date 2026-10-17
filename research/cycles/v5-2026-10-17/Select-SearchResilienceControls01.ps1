# Select only the eight new controls; one loopback sequence, no native/proof.
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$name='search-resilience-controls-01'
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
$sources['tools/Run-V5-Check.py']=Digest (Join-Path $projectRoot 'tools/Run-V5-Check.py')
foreach ($relative in @(
    'admission/__init__.py','admission/bindings.py','admission/verifier.py',
    'aggregate_claims/__init__.py','aggregate_claims/admission_binding.py',
    'aggregate_claims/aggregate_admission.py','aggregate_claims/bindings.py',
    'authoring/__init__.py','authoring/context.py','authoring/imports.py','authoring/source.py',
    'client/__init__.py','client/workspace_atomic.py','client/workspace_evidence.py',
    'client/workspace_mixed.py','client/workspace_resilient.py',
    'custody/module_store.py','custody/receipt_store.py',
    'delta/__init__.py','delta/custody.py','delta/packet.py','delta/receiver.py',
    'delta/reprepare.py','delta/transport.py',
    'delta_claims/__init__.py','delta_claims/claims.py','delta_claims/receiver.py',
    'discovery/authenticated_index.py','discovery/candidate_query.py',
    'discovery/discovery_query.py','discovery/discovery_store.py','discovery/formal_features.py',
    'discovery/module_export_adapter.py','discovery/search_session.py',
    'discovery/summary_wire.py','discovery/test_candidate_query.py',
    'evidence_network/__init__.py','evidence_network/custody.py',
    'evidence_network/packet.py','evidence_network/transport.py',
    'frontier_network/__init__.py','frontier_network/custody.py','frontier_network/transport.py',
    'location/__init__.py','location/available_descriptor.py','location/controller.py',
    'location/controller_services.py','location/observed_route.py','location/protocol.py',
    'location/workflow.py',
    'mixed_claims/__init__.py','mixed_claims/authoring_atomic.py','mixed_claims/imports_atomic.py',
    'mixed_claims/packet.py','mixed_claims/receiver.py',
    'mixed_network/__init__.py','mixed_network/custody.py','mixed_network/transport.py',
    'modules/__init__.py','modules/codec.py','modules/model.py','modules/native_rows.py',
    'modules/receipt/__init__.py','modules/receipt/witness.py','modules/source_rows.py',
    'preparation/__init__.py','preparation/owner.py',
    'production/__init__.py','production/producer.py',
    'transport/clients.py','transport/http_provider.py','transport/http_provider_receipts.py',
    'transport/located_receipts.py','transport/receipt_client.py',
    'transport/search_resilience.py','transport/test_search_resilience.py')) {
    $key='software/v5/'+$relative
    $sources[$key]=Digest (Join-Path $projectRoot $key)
}
if ($sources.Count -ne 77) { throw 'EXACT_SOURCE_COUNT' }
$required=@{
    'tools/Run-V5-Check.py'='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
    'software/v5/transport/search_resilience.py'='e3cf6a06ab59ac28e04411de62ae225a719c6d7d21a7ec17ae3004e735a707b1'
    'software/v5/client/workspace_resilient.py'='7c4d72143c4963b25d147496611f56858a6df361aafdc71773b3c6a1d15ab7e6'
    'software/v5/transport/test_search_resilience.py'='21a540bd9a80fa83214ac25d184195141f8a52f146a424622cad31bf30619f52'
}
foreach ($key in $required.Keys) {
    if ($sources[$key] -cne $required[$key]) { throw ('REVIEWED_SOURCE_CHANGED:'+ $key) }
}
$selection=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($old.argv[0],'-I','-S','-B','{snapshot}\software\v5\transport\test_search_resilience.py','--output','{output}\controls')
    limits=[ordered]@{cpu_seconds=30;wall_seconds=90;memory_mib=512;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selection|ConvertTo-Json -Depth 12)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_BOUND' }
$stream=[IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{path=$selectionPath;sha256=(Digest $selectionPath);sources=$sources.Count;runtime_pins=$runtime.Count;executed=$false}|ConvertTo-Json
