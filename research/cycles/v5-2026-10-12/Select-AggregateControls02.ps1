$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'aggregate-native-controls-02'
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
$priorSelection=Get-Content (Join-Path $local 'aggregate-native-controls-01-selection.json') -Raw|ConvertFrom-Json
$priorConfig=Get-Content (Join-Path $local 'aggregate-native-controls-01-config.json') -Raw|ConvertFrom-Json
$sources=[ordered]@{}
foreach($property in $priorSelection.sources.psobject.Properties) {
    if((Pin (Join-Path $projectRoot $property.Name)).sha256 -cne $property.Value){throw 'PRIOR_SOURCE_CHANGED'}
    $sources[$property.Name]=$property.Value
}
# delta.packet imports execute delta/__init__.py first, which eagerly imports
# receiver, which in turn imports admission.verifier. Neither is invoked here.
foreach($relative in @('software/v5/delta/receiver.py','software/v5/admission/verifier.py')) {
    $sources[$relative]=(Pin (Join-Path $projectRoot $relative)).sha256
}
$rows=@()
foreach($relative in $sources.Keys){
    $row=Pin (Join-Path $projectRoot $relative);$row.path=Join-Path (Join-Path $output 'sources') $relative;$rows+=$row
}
foreach($row in $priorConfig.runtime_pins){
    if($row.path -like '*\aggregate-native-controls-01\sources\*'){continue}
    $actual=Pin $row.path
    if($actual.bytes -ne $row.bytes -or $actual.sha256 -cne $row.sha256){throw 'PRIOR_RUNTIME_CHANGED'}
    $rows+=$actual
}
$config=[ordered]@{}
foreach($property in $priorConfig.psobject.Properties){$config[$property.Name]=$property.Value}
$config.runtime_pins=$rows
$config.output_directory=Join-Path $output 'evidence'
SaveNew $configPath $config
$pins=[ordered]@{}
foreach($row in $rows){if($row.path -notlike ($output+'\sources\*')){$pins[$row.path]=$row.sha256}}
foreach($row in @((Pin $configPath),$config.packet)){$pins[$row.path]=$row.sha256}
$selection=[ordered]@{schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$pins
    argv=@($priorSelection.argv[0],'-I','-S','-B','{snapshot}\software\v5\aggregate\native_controls.py',$configPath,(Pin $configPath).sha256)
    limits=$priorSelection.limits}
SaveNew $selectionPath $selection
@{config=(Pin $configPath);selection=(Pin $selectionPath);sources=$sources.Count;executed=$false}|ConvertTo-Json -Depth 5
