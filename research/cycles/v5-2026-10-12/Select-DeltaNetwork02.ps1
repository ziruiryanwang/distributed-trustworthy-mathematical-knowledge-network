$ErrorActionPreference = 'Stop'
$root = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $root) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $root 'experiments\v5-local-checks'
$name = 'delta-network-actual-02'
$output = Join-Path $local $name
$configPath = Join-Path $local ($name+'-config.json')
$selectionPath = Join-Path $local ($name+'-selection.json')
$nodeRoot = Join-Path $local 'delta-network-node-02'
foreach ($path in @($output,$configPath,$selectionPath,$nodeRoot)) { if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+$path) } }
function Pin([string]$path) {
    $item=Get-Item -LiteralPath $path
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
function SaveNew([string]$path,$value) {
    $raw=[Text.UTF8Encoding]::new($false).GetBytes(($value|ConvertTo-Json -Depth 60)+"`n")
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
}
$priorSelection=Get-Content (Join-Path $local 'delta-network-actual-01-selection.json') -Raw|ConvertFrom-Json
$priorConfig=Get-Content (Join-Path $local 'delta-network-actual-01-config.json') -Raw|ConvertFrom-Json
$sources=[ordered]@{}
foreach($property in $priorSelection.sources.psobject.Properties) {
    if($property.Name -ceq 'software/v5/delta/network_actual.py'){continue}
    if((Pin (Join-Path $root $property.Name)).sha256 -cne $property.Value){throw 'PRIOR_SOURCE_CHANGED'}
    $sources[$property.Name]=$property.Value
}
foreach($relative in @('software/v5/delta/network_actual02.py','software/v5/location/observed_route.py')) {
    $sources[$relative]=(Pin (Join-Path $root $relative)).sha256
}
$node=Join-Path $nodeRoot 'software\v5\location'
New-Item -ItemType Directory -Path $node -Force|Out-Null
$nodeFiles=@();$sourcePins=[ordered]@{};$rolePins=[ordered]@{}
foreach($property in @($priorConfig.location.source_pins.psobject.Properties)+@($priorConfig.location.role_pins.psobject.Properties)) {
    $source=Join-Path $priorConfig.location.source_directory $property.Name
    if((Pin $source).sha256 -cne $property.Value){throw 'PRIOR_NODE_SNAPSHOT_CHANGED'}
    if($property.Name -ceq 'maintained_roles.mjs'){$source=Join-Path $root 'software\v5\location\maintained_roles_ready.mjs'}
    $target=Join-Path $node $property.Name
    Copy-Item -LiteralPath $source -Destination $target
    $row=Pin $target
    if($row.sha256 -cne (Pin $source).sha256){throw 'EXACT_NODE_COPY'}
    $row.name=$property.Name;$row.source=$source;$nodeFiles+=$row
    if($property.Name -in $priorConfig.location.source_pins.psobject.Properties.Name){$sourcePins[$property.Name]=$row.sha256}
    else{$rolePins[$property.Name]=$row.sha256}
}
SaveNew (Join-Path $nodeRoot 'SNAPSHOT.json') ([ordered]@{schema='DMKN_OWNER_EXACT_LOCATION_SNAPSHOT_V1';scope='SOURCE_SNAPSHOT_NOT_EXECUTION_OR_MATHEMATICAL_AUTHORITY';files=$nodeFiles})
$rows=@()
foreach($relative in $sources.Keys){
    $row=Pin (Join-Path $root $relative);$row.path=Join-Path (Join-Path $output 'sources') $relative;$rows+=$row
}
foreach($row in $priorConfig.runtime_pins){
    if($row.path -like '*\delta-network-actual-01\sources\*'){continue}
    $actual=Pin $row.path
    if($actual.bytes -ne $row.bytes -or $actual.sha256 -cne $row.sha256){throw 'PRIOR_RUNTIME_CHANGED'}
    $rows+=$actual
}
$config=[ordered]@{}
foreach($property in $priorConfig.psobject.Properties){$config[$property.Name]=$property.Value}
$config.schema='DMKN_V5_ACTUAL_DELTA_NETWORK_V2'
$config.runtime_pins=$rows
$config.location=[ordered]@{source_directory=$node;source_pins=$sourcePins;role_pins=$rolePins;entry_source=$priorConfig.location.entry_source;ready_source=(Pin (Join-Path $root 'software\v5\location\maintained_roles_ready.mjs'))}
$config.lineage=@($priorConfig.lineage)+@((Pin (Join-Path $local 'delta-network-actual-01\RESULT.json')),(Pin (Join-Path $local 'delta-network-actual-01\evidence\RESULT.json')))
$config.output_directory=Join-Path $output 'evidence'
SaveNew $configPath $config
$pins=[ordered]@{}
foreach($row in $rows){if($row.path -notlike ($output+'\sources\*')){$pins[$row.path]=$row.sha256}}
foreach($row in @((Pin $configPath),$config.packet,$config.preparation_profile,$config.foundation,$config.location.entry_source,$config.location.ready_source)+$config.lineage+$nodeFiles){
    $actual=Pin $row.path
    if($actual.bytes -ne $row.bytes -or $actual.sha256 -cne $row.sha256){throw 'FINAL_INPUT_CHANGED'}
    $pins[$row.path]=$row.sha256
}
$selection=[ordered]@{schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$pins
    argv=@($priorSelection.argv[0],'-I','-S','-B','{snapshot}\software\v5\delta\network_actual02.py','--config',$configPath,'--config-sha256',(Pin $configPath).sha256)
    limits=$priorSelection.limits}
SaveNew $selectionPath $selection
@{config=(Pin $configPath);selection=(Pin $selectionPath);node_files=$nodeFiles.Count;sources=$sources.Count;executed=$false}|ConvertTo-Json -Depth 5
