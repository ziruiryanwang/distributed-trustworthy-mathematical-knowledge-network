# Exact changed-boundary synthetic controls only; this selector never runs them.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'mixed-receiver-controls-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $local $name),(Join-Path $local ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer) { throw 'FILE_REQUIRED' }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$admissionPath = Join-Path $local 'aggregate-admission-controls-01-selection.json'
$deltaPath = Join-Path $local 'delta-claim-controls-01-selection.json'
if ((Pin $admissionPath).sha256 -cne '4e57759d8aa1f359b996d837bcc00312759e9e9c8a55f99d8fc9bbefe3cf1a95' -or (Pin $deltaPath).sha256 -cne 'd3a85d4401d4a100a00a475299341ac436ceddbf04aaf184ce71e0b2f764a6fb') { throw 'FROZEN_PRIOR_SOURCE_SELECTIONS' }
$admission = Get-Content -LiteralPath $admissionPath -Raw | ConvertFrom-Json
$delta = Get-Content -LiteralPath $deltaPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
$common = @(
    'admission/__init__.py','admission/bindings.py','admission/verifier.py',
    'modules/__init__.py','modules/codec.py',
    'aggregate_claims/__init__.py','aggregate_claims/bindings.py','aggregate_claims/admission_binding.py',
    'aggregate_claims/aggregate_admission.py','aggregate_claims/aggregate_admission_controls.py',
    'delta/__init__.py','delta/packet.py','delta/receiver.py',
    'delta_claims/__init__.py','delta_claims/receiver.py','delta_claims/claims.py',
    'production/__init__.py','production/producer.py')
foreach ($relative in @($common | ForEach-Object {'software/v5/'+$_})+@('tools/Run-V5-Check.py')) {
    $a = $admission.sources.psobject.Properties[$relative]
    $d = $delta.sources.psobject.Properties[$relative]
    if ($null -eq $a -and $null -eq $d) { throw ('MISSING_PRIOR_SOURCE:'+ $relative) }
    if ($null -ne $a -and $null -ne $d -and $a.Value -cne $d.Value) { throw 'PRIOR_SOURCE_CONFLICT' }
    $expected = if ($null -ne $a) { $a.Value } else { $d.Value }
    if ((Pin (Join-Path $projectRoot $relative)).sha256 -cne $expected) { throw ('UNCHANGED_SOURCE_PIN:'+ $relative) }
    $sources[$relative] = $expected
}
$fresh = [ordered]@{
    '__init__.py'='2371afae23fa43f733cb959557a9451df64ce4181a4a9ec5ef72ec28d9290abf'
    'packet.py'='8a18e3d35e33210df9b669b3fe8dc3785e13bfb1184bd0bd2fbec683063758b1'
    'receiver.py'='d292a966469402a24282e40377c8ac9c929504e38de7862aa9a6bd1b3ad3fb00'
    'test_receiver.py'='a75ce1e30e9328ddbe6f27d79dff38d47412001af8d816743702489788ee96b3'
}
foreach ($file in $fresh.Keys) {
    $relative = 'software/v5/mixed_claims/'+$file
    if ((Pin (Join-Path $projectRoot $relative)).sha256 -cne $fresh[$file]) { throw ('FRESH_SOURCE_CHANGED:'+ $relative) }
    $sources[$relative] = $fresh[$file]
}
if ($sources.Count -ne 23) { throw 'EXACT_EAGER_SOURCE_CLOSURE' }
$pins = [ordered]@{}
$pythonRoot = Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\receiver\runtime\python'
foreach ($property in $admission.runtime_pins.psobject.Properties) {
    if (-not $property.Name.StartsWith($pythonRoot+'\',[StringComparison]::OrdinalIgnoreCase)) { continue }
    if ((Pin $property.Name).sha256 -cne $property.Value) { throw 'PYTHON_RUNTIME_CHANGED' }
    $pins[$property.Name] = $property.Value
}
if ($pins.Count -ne 18) { throw 'PYTHON_CLOSURE' }
foreach ($path in @($admissionPath,$deltaPath,(Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\RELEASE-MANIFEST.json'))) {
    $row = Pin $path; $pins[$row.path] = $row.sha256
}
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$pins
    argv=@((Join-Path $pythonRoot 'python.exe'),'-I','-S','-B','{snapshot}\software\v5\mixed_claims\test_receiver.py')
    limits=[ordered]@{cpu_seconds=30;wall_seconds=60;memory_mib=512;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected|ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=(Pin $selectionPath);sources=$sources.Count;runtime_pins=$pins.Count;synthetic_groups=12;actual_receipt_native_guest_calls=0;executed=$false} | ConvertTo-Json -Depth 5
