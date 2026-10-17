# Prepare only the five new I-only profile controls; no execution here.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'frontier-profile-controls-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath (Join-Path $local $name))) { throw 'NOT_FRESH' }
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer) { throw 'FILE_REQUIRED' }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$priorPath = Join-Path $local 'mixed-network-controls-01-selection.json'
$priorPin = Pin $priorPath
if ($priorPin.sha256 -cne '3273d116a942916cb3f57b5ad4441f37cbba0edb0950034483f61e11c30bf331') { throw 'PRIOR_SELECTION' }
$prior = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($property in $prior.sources.psobject.Properties) {
    if ($property.Name -in @('software/v5/mixed_network/test_network.py','software/v5/mixed_claims/test_receiver.py','software/v5/aggregate_claims/aggregate_admission_controls.py')) { continue }
    if ((Pin (Join-Path $projectRoot $property.Name)).sha256 -cne $property.Value) { throw ('RETAINED_SOURCE_CHANGED:'+ $property.Name) }
    $sources[$property.Name] = $property.Value
}
foreach ($namePart in @('__init__.py','custody.py','transport.py','test_profile.py')) {
    $relative = 'software/v5/frontier_network/'+$namePart
    $sources[$relative] = (Pin (Join-Path $projectRoot $relative)).sha256
}
$pins = [ordered]@{}
foreach ($property in $prior.runtime_pins.psobject.Properties) {
    if ((Pin $property.Name).sha256 -cne $property.Value) { throw ('RUNTIME_CHANGED:'+ $property.Name) }
    $pins[$property.Name] = $property.Value
}
$pins[$priorPath] = $priorPin.sha256
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1'; name='frontier-profile-controls-01'; sources=$sources; runtime_pins=$pins
    argv=@($prior.argv[0],'-I','-S','-B','{snapshot}\software\v5\frontier_network\test_profile.py','--output','{output}\evidence')
    limits=[ordered]@{cpu_seconds=30;wall_seconds=60;memory_mib=512;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected|ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=(Pin $selectionPath);sources=$sources.Count;runtime_pins=$pins.Count;tests=5;native_calls=0;proof_calls=0;executed=$false} | ConvertTo-Json -Depth 4
