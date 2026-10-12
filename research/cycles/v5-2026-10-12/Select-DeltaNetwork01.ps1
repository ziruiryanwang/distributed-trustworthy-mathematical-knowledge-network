$ErrorActionPreference = 'Stop'
$root = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $root) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $root 'experiments\v5-local-checks'
$name = 'delta-network-actual-01'
$output = Join-Path $local $name
$configPath = Join-Path $local ($name + '-config.json')
$selectionPath = Join-Path $local ($name + '-selection.json')
foreach ($path in @($output,$configPath,$selectionPath)) { if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+$path) } }
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    return [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
function SaveNew([string]$path,$value) {
    $raw = [Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 60) + "`n")
    $stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) } finally { $stream.Dispose() }
}
$previous = Get-Content -LiteralPath (Join-Path $local 'delta-reprepare-01-config.json') -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($prior in @('delta-reprepare-01\selection.json','delta-network-controls-01\selection.json')) {
    $held = Get-Content -LiteralPath (Join-Path $local $prior) -Raw | ConvertFrom-Json
    foreach ($property in $held.sources.psobject.Properties) {
        $row = Pin (Join-Path $root $property.Name)
        if ($row.sha256 -cne $property.Value) { throw ('PRIOR_SOURCE_CHANGED:'+$property.Name) }
        $sources[$property.Name] = $property.Value
    }
}
foreach ($relative in @('software/v5/delta/network_actual.py','software/v5/location/available_descriptor.py')) {
    $sources[$relative] = (Pin (Join-Path $root $relative)).sha256
}
$runtimeRows = @()
foreach ($relative in $sources.Keys) {
    if ($relative.EndsWith('.py')) {
        $row = Pin (Join-Path $root $relative)
        $row.path = Join-Path (Join-Path $output 'sources') $relative
        $runtimeRows += $row
    }
}
foreach ($row in $previous.runtime_pins) {
    if ($row.path -notlike '*\sources\software\v5\*') {
        $actual = Pin $row.path
        if ($actual.sha256 -cne $row.sha256 -or $actual.bytes -ne $row.bytes) { throw 'PRIOR_RUNTIME_CHANGED' }
        $runtimeRows += $actual
    }
}
$node = Join-Path $local 'delta-network-node-01\software\v5\location'
$nodeRecord = Get-Content -LiteralPath (Join-Path $local 'delta-network-node-01\SNAPSHOT.json') -Raw | ConvertFrom-Json
$sourcePins = [ordered]@{}; $rolePins = [ordered]@{}
$roleNames = @('maintained_roles.mjs','role_composition.mjs','node_entry_roles.mjs','services_composition.mjs','node_entry_services.mjs')
foreach ($row in $nodeRecord.files) {
    $actual = Pin $row.path
    if ($actual.bytes -ne $row.bytes -or $actual.sha256 -cne $row.sha256) { throw 'NODE_SNAPSHOT_CHANGED' }
    if ($row.name -in $roleNames) { $rolePins[$row.name]=$row.sha256 } else { $sourcePins[$row.name]=$row.sha256 }
}
$api = Get-Content -LiteralPath (Join-Path $root 'software\v5\delta\network_actual_api.md') -Raw -Encoding UTF8
$match = [regex]::Match($api, '(?s)```json\s*(\{.*?\})\s*```')
if (-not $match.Success) { throw 'LIMITS_PROPOSAL' }
$limits = $match.Groups[1].Value | ConvertFrom-Json
$ports = [ordered]@{bootstrap=43171;origin_location=43172;replica_location=43173;reader1=43174;reader2=43175;origin_http=43176;replica_http=43177}
$listeners = @()
try {
    foreach ($port in $ports.Values) {
        $listener = [Net.Sockets.TcpListener]::new([Net.IPAddress]::Loopback,$port)
        $listener.Server.ExclusiveAddressUse = $true
        $listener.Start(); $listeners += $listener
    }
} finally { foreach ($listener in $listeners) { $listener.Stop() } }
$config = [ordered]@{
    schema='DMKN_V5_ACTUAL_DELTA_NETWORK_V1'
    packet=(Pin (Join-Path $local 'delta-reprepare-01\evidence\delta-packet.json'))
    lineage=@((Pin $previous.request.path),(Pin $previous.export.path),(Pin (Join-Path $local 'delta-reprepare-01\evidence\RESULT.json')),(Pin (Join-Path $local 'delta-reprepare-01\RESULT.json')))
    preparation_profile=$previous.preparation_profile
    foundation=$previous.foundation
    native_executable=$previous.native_executable
    runtime_pins=$runtimeRows
    location=[ordered]@{source_directory=$node;source_pins=$sourcePins;role_pins=$rolePins;entry_source=(Pin (Join-Path $root 'software\v5\location\node_entry_services_available.mjs'))}
    ports=$ports
    output_directory=(Join-Path $output 'evidence')
    limits=$limits
}
SaveNew $configPath $config
$outerPins = [ordered]@{}
foreach ($row in $runtimeRows) { if ($row.path -notlike ($output+'\sources\*')) { $outerPins[$row.path]=$row.sha256 } }
foreach ($row in @((Pin $configPath),$config.packet,$config.preparation_profile,$config.foundation,$config.location.entry_source)+$config.lineage) {
    $actual=Pin $row.path
    if ($actual.sha256 -cne $row.sha256 -or $actual.bytes -ne $row.bytes) { throw 'FINAL_INPUT_CHANGED' }
    $outerPins[$row.path]=$row.sha256
}
foreach ($row in $nodeRecord.files) { $outerPins[$row.path]=$row.sha256 }
$python = Join-Path $root 'product-local\v4-library-commons-02\commons-v4\receiver\runtime\python\python.exe'
$selection = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$outerPins
    argv=@($python,'-I','-S','-B','{snapshot}\software\v5\delta\network_actual.py','--config',$configPath,'--config-sha256',(Pin $configPath).sha256)
    limits=[ordered]@{cpu_seconds=300;wall_seconds=600;memory_mib=4096;active_processes=8;stdout_bytes=1048576;stderr_bytes=1048576}
}
SaveNew $selectionPath $selection
@{config=(Pin $configPath);selection=(Pin $selectionPath);source_count=$sources.Count;runtime_count=$outerPins.Count;ports=$ports;executed=$false} | ConvertTo-Json -Depth 5
