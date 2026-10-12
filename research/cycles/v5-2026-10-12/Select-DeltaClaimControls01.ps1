# SOURCE-ONLY selector proposal. Root alone may execute this selector and launch
# its resulting finite check. This script itself never launches a test/worker.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'delta-claim-controls-01'
$output = Join-Path $local $name
$selectionPath = Join-Path $local ($name+'-selection.json')
foreach ($path in @($output,$selectionPath,(Join-Path $local ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+$path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer) { throw ('FILE_REQUIRED:'+$path) }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
function SaveNew([string]$path,$value) {
    $raw = [Text.UTF8Encoding]::new($false).GetBytes(($value|ConvertTo-Json -Depth 15)+"`n")
    $stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
}

# Reuse the audited native-free packet import closure, not any aggregate native
# executable or real receipt. Pin the prior selections themselves as provenance.
$priorPath = Join-Path $local 'delta-packet-controls-01-selection.json'
$runtimePriorPath = Join-Path $local 'delta-network-controls-01-selection.json'
$priorPin = Pin $priorPath
$runtimePriorPin = Pin $runtimePriorPath
if ($priorPin.sha256 -cne 'c8cc86ce63e63daecc421ce90e7c80362eb50a3e207813faecae1969eb066ae1') { throw 'PRIOR_PACKET_SELECTION_CHANGED' }
if ($runtimePriorPin.sha256 -cne '84b83dfdef0dd8d11851bbc89c4be7888af838a2b7c0ea4204f1678f9aecfaf9') { throw 'PRIOR_PYTHON_RUNTIME_SELECTION_CHANGED' }
$prior = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
$runtimePrior = Get-Content -LiteralPath $runtimePriorPath -Raw | ConvertFrom-Json

$sources = [ordered]@{}
$common = @(
    'software/v5/admission/__init__.py','software/v5/admission/bindings.py',
    'software/v5/admission/verifier.py','software/v5/modules/__init__.py',
    'software/v5/modules/codec.py','software/v5/production/__init__.py',
    'software/v5/production/producer.py','software/v5/delta/__init__.py',
    'software/v5/delta/packet.py','software/v5/delta/receiver.py','tools/Run-V5-Check.py'
)
foreach ($relative in $common) {
    $expected = $prior.sources.psobject.Properties[$relative]
    if ($null -eq $expected) { throw ('MISSING_PRIOR_SOURCE:'+ $relative) }
    $actual = Pin (Join-Path $projectRoot $relative)
    if ($actual.sha256 -cne $expected.Value) { throw ('PRIOR_SOURCE_CHANGED:'+ $relative) }
    $sources[$relative] = $actual.sha256
}
# Snapshot all seven reviewed fresh artifacts. Only the five receiver/import/
# binding/test modules are imported by the controls; authoring.py and API.md are
# exact reviewed context, NOT exercised ordinary-source authoring qualification.
$fresh = [ordered]@{
    '__init__.py'='dc919d97068cea9d267b07368d238e4ce7a5689d20439ac5e6d69f7f76bb4987'
    'receiver.py'='7731f712902b5c5e0869a51c913b335428309760df604768293f7ab58c301bfd'
    'claims.py'='c880964241e5b0f492ab332b2c694896b3b6efdc638e014b25148bd6410e6564'
    'imports.py'='216f3ce48543ff4638c7112aa16d6dc430f7bc9a04f6927a7d036b81ddee137f'
    'authoring.py'='cc62ebd697d8137f021dbf79feb4e39e41639a8c5864c041da40838469bbc290'
    'test_claims.py'='f719bfcaf0e658dac8eeb76b7cce8b365a8da5567563cd37b812af062881860c'
    'API.md'='abf2fc482658aad9005fc248aa3fb95540d2c69620f9d9c6b3f352a7d5dd06b2'
}
foreach ($file in $fresh.Keys) {
    $relative = 'software/v5/delta_claims/'+$file
    $actual = Pin (Join-Path $projectRoot $relative)
    if ($actual.sha256 -cne $fresh[$file]) { throw ('REVIEWED_FRESH_SOURCE_CHANGED:'+ $relative) }
    $sources[$relative] = $actual.sha256
}
if ($sources.Count -ne 18) { throw 'EXACT_EAGER_SOURCE_CLOSURE' }

# unittest.mock imports asyncio and associated native stdlib modules. Reuse the
# previously pinned 18-file Python/DLL set, not the old network test or fixtures.
# These explicit pins are not a hermetic operating-system/stdlib proof.
$pythonRoot = Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\receiver\runtime\python'
$prefix = $pythonRoot+'\'
$pins = [ordered]@{}
foreach ($property in $runtimePrior.runtime_pins.psobject.Properties) {
    if (-not $property.Name.StartsWith($prefix,[StringComparison]::OrdinalIgnoreCase)) { continue }
    $actual = Pin $property.Name
    if ($actual.sha256 -cne $property.Value) { throw ('PRIOR_RUNTIME_CHANGED:'+ $property.Name) }
    $pins[$actual.path] = $actual.sha256
}
if ($pins.Count -ne 18) { throw 'EXACT_PYTHON_RUNTIME_CLOSURE' }
$manifestPath = Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\RELEASE-MANIFEST.json'
$manifestPin = Pin $manifestPath
if ($manifestPin.sha256 -cne 'a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed') { throw 'FROZEN_SUPERVISOR_MANIFEST_CHANGED' }
foreach ($row in @($manifestPin,$priorPin,$runtimePriorPin)) { $pins[$row.path] = $row.sha256 }
$python = Join-Path $pythonRoot 'python.exe'
if ($prior.argv[0] -cne $python -or -not $pins.Contains($python)) { throw 'EXACT_PINNED_PYTHON' }

$selection = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$pins
    argv=@($python,'-I','-S','-B','{snapshot}\software\v5\delta_claims\test_claims.py')
    limits=[ordered]@{cpu_seconds=30;wall_seconds=60;memory_mib=512;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
SaveNew $selectionPath $selection
[ordered]@{selection=(Pin $selectionPath);sources=$sources.Count;runtime_pins=$pins.Count
    expected_synthetic_tests=25;native_calls=0;receipt_verifications=0;authoring_calls=0
    network_calls=0;executed=$false;authority='SELECTION_ONLY_NOT_TEST_RESULT'} | ConvertTo-Json -Depth 5
