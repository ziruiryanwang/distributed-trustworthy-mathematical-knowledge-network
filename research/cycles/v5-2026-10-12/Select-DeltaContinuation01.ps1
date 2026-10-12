$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'delta-network-continuation-01'
$output = Join-Path $local $name
$configPath = Join-Path $local ($name+'-config.json')
$selectionPath = Join-Path $local ($name+'-selection.json')
foreach ($path in @($output,$configPath,$selectionPath)) { if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+$path) } }
function Pin([string]$path) {
    $item=Get-Item -LiteralPath $path
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
function SaveNew([string]$path,$value) {
    $raw=[Text.UTF8Encoding]::new($false).GetBytes(($value|ConvertTo-Json -Depth 60)+"`n")
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
}
$priorSelection=Get-Content (Join-Path $local 'delta-network-actual-02-selection.json') -Raw|ConvertFrom-Json
$priorConfig=Get-Content (Join-Path $local 'delta-network-actual-02-config.json') -Raw|ConvertFrom-Json
$sources=[ordered]@{}
foreach($property in $priorSelection.sources.psobject.Properties) {
    if((Pin (Join-Path $projectRoot $property.Name)).sha256 -cne $property.Value){throw 'PRIOR_SOURCE_CHANGED'}
    $sources[$property.Name]=$property.Value
}
foreach($relative in @('software/v5/delta/network_continue.py','software/v5/delta/retained_custody.py')) {
    $sources[$relative]=(Pin (Join-Path $projectRoot $relative)).sha256
}
$rows=@()
foreach($relative in $sources.Keys){
    $row=Pin (Join-Path $projectRoot $relative);$row.path=Join-Path (Join-Path $output 'sources') $relative;$rows+=$row
}
foreach($row in $priorConfig.runtime_pins){
    if($row.path -like '*\delta-network-actual-02\sources\*'){continue}
    $actual=Pin $row.path
    if($actual.bytes -ne $row.bytes -or $actual.sha256 -cne $row.sha256){throw 'PRIOR_RUNTIME_CHANGED'}
    $rows+=$actual
}
$retained=Join-Path $local 'delta-network-actual-02\evidence'
$config=[ordered]@{}
foreach($property in $priorConfig.psobject.Properties){if($property.Name -cne 'packet'){$config[$property.Name]=$property.Value}}
$config.schema='DMKN_V5_DELTA_RETAINED_CONTINUATION_V1'
$config.retained_custody=[ordered]@{
    recipient_result=(Pin (Join-Path $retained 'reader1-result.json'))
    packet_db=(Pin (Join-Path $retained 'reader1-packets\delta-packets.sqlite'))
    module_db=(Pin (Join-Path $retained 'reader1-modules\modules.sqlite'))}
$config.runtime_pins=$rows
$config.lineage=@($priorConfig.lineage)+@((Pin (Join-Path $local 'delta-network-actual-02\RESULT.json')),(Pin (Join-Path $retained 'RESULT.json')))
$config.output_directory=Join-Path $output 'evidence'
# Reuse the exact fourteen-file Node02 snapshot. No new source cut or limits.
SaveNew $configPath $config
$pins=[ordered]@{}
foreach($row in $rows){if($row.path -notlike ($output+'\sources\*')){$pins[$row.path]=$row.sha256}}
$inputRows=@((Pin $configPath),$config.preparation_profile,$config.foundation,$config.location.entry_source,$config.location.ready_source)+$config.lineage+@($config.retained_custody.Values)
foreach($row in $inputRows){
    $actual=Pin $row.path
    if($actual.bytes -ne $row.bytes -or $actual.sha256 -cne $row.sha256){throw 'FINAL_INPUT_CHANGED'}
    $pins[$row.path]=$row.sha256
}
foreach($property in @($config.location.source_pins.psobject.Properties)+@($config.location.role_pins.psobject.Properties)) {
    $row=Pin (Join-Path $config.location.source_directory $property.Name)
    if($row.sha256 -cne $property.Value){throw 'NODE_SNAPSHOT_CHANGED'}
    $pins[$row.path]=$row.sha256
}
$selection=[ordered]@{schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$pins
    argv=@($priorSelection.argv[0],'-I','-S','-B','{snapshot}\software\v5\delta\network_continue.py','--config',$configPath,'--config-sha256',(Pin $configPath).sha256)
    limits=$priorSelection.limits}
SaveNew $selectionPath $selection
@{config=(Pin $configPath);selection=(Pin $selectionPath);sources=$sources.Count;executed=$false}|ConvertTo-Json -Depth 5
