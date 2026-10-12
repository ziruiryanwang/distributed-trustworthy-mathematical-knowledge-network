$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'aggregate-claims-controls-01'
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
$priorSelection=Get-Content (Join-Path $local 'aggregate-native-controls-02-selection.json') -Raw|ConvertFrom-Json
$priorConfig=Get-Content (Join-Path $local 'aggregate-native-controls-02-config.json') -Raw|ConvertFrom-Json
$build=Get-Content (Join-Path $local 'aggregate-claims-build-02\RESULT.json') -Raw|ConvertFrom-Json
if($build.status -cne 'PASS_CLAIMS_V2_THREE_THIN_COMPILES_ONLY'){throw 'REQUIRES_CLAIMS_BUILD_PASS'}
if(Test-Path -LiteralPath (Join-Path $local 'aggregate-claims-build-02\FINALIZATION-FAILED.json')){throw 'BUILD_FINALIZATION_FAILED'}
$sources=[ordered]@{}
foreach($property in $priorSelection.sources.psobject.Properties) {
    if((Pin (Join-Path $projectRoot $property.Name)).sha256 -cne $property.Value){throw 'PRIOR_SOURCE_CHANGED'}
    if($property.Name -notlike 'software/v5/aggregate/*'){$sources[$property.Name]=$property.Value}
}
foreach($file in @('__init__.py','bindings.py','input.py','admission_binding.py','binding_controls.py','native_controls.py')) {
    $relative='software/v5/aggregate_claims/'+$file
    $sources[$relative]=(Pin (Join-Path $projectRoot $relative)).sha256
}
$rows=@()
foreach($relative in $sources.Keys){
    $row=Pin (Join-Path $projectRoot $relative);$row.path=Join-Path (Join-Path $output 'sources') $relative;$rows+=$row
}
foreach($row in $priorConfig.runtime_pins){
    if($row.path -like '*\aggregate-native-controls-02\sources\*' -or $row.path -like '*\aggregate-native-build-02\*'){continue}
    $actual=Pin $row.path
    if($actual.bytes -ne $row.bytes -or $actual.sha256 -cne $row.sha256){throw 'PRIOR_RUNTIME_CHANGED'}
    $rows+=$actual
}
$native=Pin (Join-Path $local 'aggregate-claims-build-02\native_aggregate.exe')
$tests=Pin (Join-Path $local 'aggregate-claims-build-02\aggregate_tests.exe')
foreach($row in @($native,$tests)) {
    $key=[IO.Path]::GetFileName($row.path)
    $built=$build.outputs.psobject.Properties[$key].Value
    if($built.bytes -ne $row.bytes -or $built.sha256 -cne $row.sha256){throw 'ACTUAL_BUILD_OUTPUT_PIN'}
    $rows+=$row
}
$config=[ordered]@{schema='DMKN_V5_AGGREGATE_CLAIMS_CONTROLS_V1';packet=$priorConfig.packet
    native=$native;tests=$tests;runtime_pins=$rows;output_directory=(Join-Path $output 'evidence')}
SaveNew $configPath $config
$pins=[ordered]@{}
foreach($row in $rows){if($row.path -notlike ($output+'\sources\*')){$pins[$row.path]=$row.sha256}}
$reference=Pin (Join-Path $local 'aggregate-native-controls-02\evidence\cross-language-vectors.json')
if($reference.sha256 -cne '877f8d8b92d9b54c28ac7ab18949c22e302880d8a0dcec9781620a0a71347364'){throw 'RETAINED_REFERENCE_CHANGED'}
foreach($row in @((Pin $configPath),$config.packet,$reference)){$pins[$row.path]=$row.sha256}
$selection=[ordered]@{schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$pins
    argv=@($priorSelection.argv[0],'-I','-S','-B','{snapshot}\software\v5\aggregate_claims\native_controls.py',$configPath,(Pin $configPath).sha256)
    limits=$priorSelection.limits}
SaveNew $selectionPath $selection
@{config=(Pin $configPath);selection=(Pin $selectionPath);sources=$sources.Count;executed=$false}|ConvertTo-Json -Depth 5
