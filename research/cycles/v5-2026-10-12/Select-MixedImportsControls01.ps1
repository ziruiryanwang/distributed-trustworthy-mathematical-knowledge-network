# SOURCE-ONLY selector proposal. Root alone may execute it and launch the check.
# It creates a fresh selection, never imports Python or starts a test/worker.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'mixed-imports-controls-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $local $name),(Join-Path $local ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer) { throw 'FILE_REQUIRED' }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$mixedPath = Join-Path $local 'mixed-receiver-controls-01-selection.json'
$contextPath = Join-Path $local 'delta-network-actual-02-selection.json'
$mixedPin = Pin $mixedPath
$contextPin = Pin $contextPath
if ($mixedPin.sha256 -cne '8b0557bca9af01b5db8b23cc5d1a7214cc95eaf849fb84ac343faa49fc5078b4') { throw 'PRIOR_MIXED_SELECTION_CHANGED' }
if ($contextPin.sha256 -cne '0435e839636101824929c31ec1119074f9543b27806120be1012af0b5699e512') { throw 'PRIOR_CONTEXT_SELECTION_CHANGED' }
$mixed = Get-Content -LiteralPath $mixedPath -Raw | ConvertFrom-Json
$context = Get-Content -LiteralPath $contextPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
$mixedFiles = @(
    'mixed_claims/__init__.py','mixed_claims/packet.py','mixed_claims/receiver.py','mixed_claims/test_receiver.py',
    'aggregate_claims/__init__.py','aggregate_claims/bindings.py','aggregate_claims/admission_binding.py',
    'aggregate_claims/aggregate_admission.py','aggregate_claims/aggregate_admission_controls.py',
    'admission/__init__.py','admission/verifier.py','admission/bindings.py',
    'modules/__init__.py','modules/codec.py','delta/__init__.py','delta/packet.py','delta/receiver.py',
    'delta_claims/__init__.py','delta_claims/receiver.py','delta_claims/claims.py',
    'production/__init__.py','production/producer.py')
foreach ($relative in @($mixedFiles | ForEach-Object {'software/v5/'+$_})+@('tools/Run-V5-Check.py')) {
    $expected = $mixed.sources.psobject.Properties[$relative]
    if ($null -eq $expected) { throw ('MISSING_PRIOR_MIXED_SOURCE:'+ $relative) }
    if ((Pin (Join-Path $projectRoot $relative)).sha256 -cne $expected.Value) { throw ('UNCHANGED_MIXED_SOURCE_PIN:'+ $relative) }
    $sources[$relative] = $expected.Value
}
if ($sources.Count -ne 23) { throw 'EXACT_PRIOR_MIXED_CLOSURE' }

# Context/imports eagerly load these modules, including the inert HTTP/SQLite
# definitions. Namespace packages transport/custody/discovery have no __init__.
# The old network test, its fixtures and its command are NOT selected or rerun.
$contextFiles = @(
    'authoring/__init__.py','authoring/context.py','authoring/source.py','authoring/imports.py',
    'preparation/__init__.py','preparation/owner.py',
    'modules/model.py','modules/native_rows.py','modules/source_rows.py',
    'modules/receipt/__init__.py','modules/receipt/witness.py','delta/reprepare.py',
    'transport/receipt_client.py','transport/clients.py','transport/http_provider.py','transport/http_provider_receipts.py',
    'custody/module_store.py','custody/receipt_store.py',
    'discovery/formal_features.py','discovery/authenticated_index.py','discovery/summary_wire.py','discovery/discovery_store.py')
foreach ($file in $contextFiles) {
    $relative = 'software/v5/'+$file
    if ($sources.Contains($relative)) { throw ('UNEXPECTED_CONTEXT_OVERLAP:'+ $relative) }
    $expected = $context.sources.psobject.Properties[$relative]
    if ($null -eq $expected) { throw ('MISSING_PRIOR_CONTEXT_SOURCE:'+ $relative) }
    if ((Pin (Join-Path $projectRoot $relative)).sha256 -cne $expected.Value) { throw ('UNCHANGED_CONTEXT_SOURCE_PIN:'+ $relative) }
    $sources[$relative] = $expected.Value
}
if ($sources.Count -ne 45) { throw 'EXACT_CONTEXT_CLOSURE' }
$fresh = [ordered]@{
    'imports.py'='50b09b084b7cb54db2b1196e3570f1b15066e85e9ce55002b8d27bb4460cb1df'
    'authoring.py'='8b09cb1b8f0466a5049ed53f7b28098b6022234e3681786b2f4a9f542cd83e1b'
    'test_imports.py'='93ff0a2cd9065bb8ba97fefb9fe9b4e33a0362c28b35156402fa76627e23064a'
}
foreach ($file in $fresh.Keys) {
    $relative = 'software/v5/mixed_claims/'+$file
    if ((Pin (Join-Path $projectRoot $relative)).sha256 -cne $fresh[$file]) { throw ('REVIEWED_SOURCE_CHANGED:'+ $relative) }
    $sources[$relative] = $fresh[$file]
}
if ($sources.Count -ne 48) { throw 'EXACT_EAGER_SOURCE_CLOSURE' }

# Reuse all eighteen retained Python/native-stdlib pins. They already include
# _ssl/libssl/libcrypto and _sqlite3/sqlite3; no network or database is opened.
# This explicit set is not a hermetic OS/stdlib closure or hostile-code sandbox.
$pythonRoot = Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\receiver\runtime\python'
$pins = [ordered]@{}
foreach ($property in $mixed.runtime_pins.psobject.Properties) {
    if (-not $property.Name.StartsWith($pythonRoot+'\',[StringComparison]::OrdinalIgnoreCase)) { continue }
    $actual = Pin $property.Name
    if ($actual.sha256 -cne $property.Value) { throw ('PYTHON_RUNTIME_CHANGED:'+ $property.Name) }
    $pins[$actual.path] = $actual.sha256
}
if ($pins.Count -ne 18) { throw 'EXACT_PYTHON_RUNTIME_CLOSURE' }
foreach ($relative in @('DLLs\_ssl.pyd','DLLs\libssl-3.dll','DLLs\libcrypto-3.dll','DLLs\_sqlite3.pyd','DLLs\sqlite3.dll')) {
    if (-not $pins.Contains((Join-Path $pythonRoot $relative))) { throw 'SSL_SQLITE_RUNTIME_CLOSURE' }
}
$manifestPin = Pin (Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\RELEASE-MANIFEST.json')
if ($manifestPin.sha256 -cne 'a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed') { throw 'FROZEN_SUPERVISOR_MANIFEST_CHANGED' }
foreach ($row in @($mixedPin,$contextPin,$manifestPin)) { $pins[$row.path] = $row.sha256 }
if ($pins.Count -ne 21) { throw 'EXACT_RUNTIME_PROVENANCE_CLOSURE' }
$python = Join-Path $pythonRoot 'python.exe'
if ($mixed.argv[0] -cne $python -or -not $pins.Contains($python)) { throw 'EXACT_PINNED_PYTHON' }
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$pins
    argv=@($python,'-I','-S','-B','{snapshot}\software\v5\mixed_claims\test_imports.py')
    limits=[ordered]@{cpu_seconds=30;wall_seconds=60;memory_mib=512;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected|ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=(Pin $selectionPath);sources=$sources.Count;runtime_pins=$pins.Count
    synthetic_groups=10;actual_receipt_verifications=0;actual_native_calls=0;actual_lean_calls=0
    network_calls=0;executed=$false;authority='SELECTION_ONLY_NOT_TEST_RESULT'} | ConvertTo-Json -Depth 5
