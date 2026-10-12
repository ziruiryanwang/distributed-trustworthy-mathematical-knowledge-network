# Exact source snapshot for seven changed-boundary tests, not a test launch.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'mixed-network-controls-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $local $name))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer) { throw 'FILE_REQUIRED' }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$priors = [ordered]@{
    'delta-network-controls-01-selection.json'='84b83dfdef0dd8d11851bbc89c4be7888af838a2b7c0ea4204f1678f9aecfaf9'
    'mixed-receiver-controls-01-selection.json'='8b0557bca9af01b5db8b23cc5d1a7214cc95eaf849fb84ac343faa49fc5078b4'
}
$sources = [ordered]@{}
$pins = [ordered]@{}
$pythonRoot = Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\receiver\runtime\python'
foreach ($file in $priors.Keys) {
    $path = Join-Path $local $file
    if ((Pin $path).sha256 -cne $priors[$file]) { throw 'PRIOR_SELECTION_PIN' }
    $prior = Get-Content -LiteralPath $path -Raw | ConvertFrom-Json
    foreach ($property in $prior.sources.psobject.Properties) {
        if ($property.Name -in @('software/v5/delta/test_network.py','software/v5/delta/test_packet.py')) { continue }
        if ($sources.Contains($property.Name) -and $sources[$property.Name] -cne $property.Value) { throw 'SOURCE_CONFLICT' }
        if ((Pin (Join-Path $projectRoot $property.Name)).sha256 -cne $property.Value) { throw ('SOURCE_CHANGED:'+ $property.Name) }
        $sources[$property.Name] = $property.Value
    }
    foreach ($property in $prior.runtime_pins.psobject.Properties) {
        if (-not $property.Name.StartsWith($pythonRoot+'\',[StringComparison]::OrdinalIgnoreCase)) { continue }
        if ($pins.Contains($property.Name) -and $pins[$property.Name] -cne $property.Value) { throw 'RUNTIME_CONFLICT' }
        if ((Pin $property.Name).sha256 -cne $property.Value) { throw 'RUNTIME_CHANGED' }
        $pins[$property.Name] = $property.Value
    }
}
if ($pins.Count -ne 18) { throw 'PYTHON_CLOSURE' }
$fresh = [ordered]@{
    '__init__.py'='468040d5c42f09623939122339c5d8ff080c416503dac098d5e4801f75e77bec'
    'custody.py'='ee84564808978ff7ad7bb201f638371940a5f6bbcc5524ccc23517210973864f'
    'transport.py'='fa92fccc3dfec7dcb00c6b5e0d4cc21b5c6c06997026edda93e1efd6cdf836a3'
    'test_network.py'='f59310331c8be7f6a4e4e53d3f22129ef733c72d1d6d9fb6381d14cd95ff9d19'
}
foreach ($file in $fresh.Keys) {
    $relative = 'software/v5/mixed_network/'+$file
    if ((Pin (Join-Path $projectRoot $relative)).sha256 -cne $fresh[$file]) { throw ('FRESH_SOURCE_CHANGED:'+ $relative) }
    $sources[$relative] = $fresh[$file]
}
foreach ($file in $priors.Keys) {
    $row = Pin (Join-Path $local $file); $pins[$row.path] = $row.sha256
}
$row = Pin (Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\RELEASE-MANIFEST.json')
if ($row.sha256 -cne 'a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed') { throw 'SUPERVISOR_MANIFEST' }
$pins[$row.path] = $row.sha256
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$pins
    argv=@((Join-Path $pythonRoot 'python.exe'),'-I','-S','-B','{snapshot}\software\v5\mixed_network\test_network.py','--output','{output}\evidence')
    limits=[ordered]@{cpu_seconds=30;wall_seconds=60;memory_mib=512;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected|ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=(Pin $selectionPath);sources=$sources.Count;runtime_pins=$pins.Count;synthetic_groups=7;actual_receipt_native_guest_calls=0;executed=$false} | ConvertTo-Json -Depth 5
