# Prepare one completed po18 layout plan after actual new snapshot-host build.
# No native, Python, guest or proof invocation occurs in this selector.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'small-aggregate-layout-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
$configPath = Join-Path $local ($name+'-configuration.json')
foreach ($path in @($selectionPath,$configPath,(Join-Path $local $name))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'ORDINARY_FILE_REQUIRED' }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
function SaveNew([string]$path,$value) {
    $raw = [Text.UTF8Encoding]::new($false).GetBytes(($value|ConvertTo-Json -Depth 15)+"`n")
    $stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
}
$priorPath = Join-Path $local 'frontier-capability-execution-01-selection.json'
$priorConfig = Join-Path $local 'frontier-capability-execution-01-configuration.json'
if ((Pin $priorPath).sha256 -cne '85555faa0313c26919800a8974c81f55e3add29f7d8892cd095314b0b94c02ef') { throw 'RETAINED_PLAN_CHANGED' }
if ((Pin $priorConfig).sha256 -cne 'd4d9751b155bc4b04e9d110ca23bfe31a8adc34e267d86fd00003da6c64004bd') { throw 'RETAINED_CONFIG_CHANGED' }
$selected = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
$config = Get-Content -LiteralPath $priorConfig -Raw | ConvertFrom-Json
$build = Join-Path $local 'small-aggregate-snapshot-host-build-01'
$hostBuild = [ordered]@{
    result=(Pin (Join-Path $build 'RESULT.json'))
    attempt=(Pin (Join-Path $local 'small-aggregate-snapshot-host-build-01-attempt.json'))
    selection=(Pin (Join-Path $local 'small-aggregate-snapshot-host-build-01-selection.json'))
    source_map=(Pin (Join-Path $build 'source-map.json'))
    command=(Pin (Join-Path $build 'compile-command.json'))
}
if ($hostBuild.selection.sha256 -cne 'e4493418256735529f7fc19ed606ea459bf35b613b57680d2e0a31a7b858e4bd') { throw 'NEW_BUILD_SELECTION_CHANGED' }
$result = Get-Content -LiteralPath $hostBuild.result.path -Raw | ConvertFrom-Json
$attempt = Get-Content -LiteralPath $hostBuild.attempt.path -Raw | ConvertFrom-Json
if ($result.status -cne 'PASS_SMALL_AGGREGATE_SNAPSHOT_HOST_ONE_LINK_ONLY' -or
    $result.job.active_processes -ne 0 -or $result.job.terminated_processes -ne 0 -or
    $attempt.result_sha256 -cne $hostBuild.result.sha256 -or $attempt.status -cne $result.status -or
    (Test-Path -LiteralPath (Join-Path $build 'FINALIZATION-FAILED.json'))) { throw 'UNCLEAN_NEW_BUILD' }
$sources = [ordered]@{}
foreach ($property in $selected.sources.psobject.Properties) {
    if ((Pin (Join-Path $projectRoot $property.Name)).sha256 -cne $property.Value) { throw 'RETAINED_SOURCE_CHANGED' }
    if ($property.Name -ceq 'software/v5/aggregate_host/capability_snapshot.py') { continue }
    $sources[$property.Name]=$property.Value
}
$adapter='software/v5/aggregate_small/capability_snapshot.py'
$sources[$adapter]=(Pin (Join-Path $projectRoot $adapter)).sha256
$pins = [ordered]@{}
$drop = @($priorConfig,(Join-Path $local 'aggregate-host-build-01\RESULT.json'),(Join-Path $local 'aggregate-host-build-01\aggregate_host.exe'))
foreach ($property in $selected.runtime_pins.psobject.Properties) {
    if ($drop -ccontains $property.Name) { continue }
    if ((Pin $property.Name).sha256 -cne $property.Value) { throw 'RETAINED_RUNTIME_CHANGED' }
    $pins[$property.Name]=$property.Value
}
foreach ($pin in $hostBuild.Values) { $pins[$pin.path]=$pin.sha256 }
$map=Get-Content -LiteralPath $hostBuild.source_map.path -Raw | ConvertFrom-Json
foreach ($property in $map.psobject.Properties) {
    $path=Join-Path (Join-Path $build 'source') $property.Name
    $actual=Pin $path
    if ($actual.bytes -ne $property.Value.bytes -or $actual.sha256 -cne $property.Value.sha256) { throw 'NEW_BUILD_SNAPSHOT_CHANGED' }
    $pins[$actual.path]=$actual.sha256
}
$hostPin=Pin $result.executable.path
if ($hostPin.bytes -gt 8388608 -or $hostPin.bytes -ne $result.executable.bytes -or $hostPin.sha256 -cne $result.executable.sha256) { throw 'NEW_BUILD_EXECUTABLE_CHANGED' }
$pins[$hostPin.path]=$hostPin.sha256
$config.schema='DMKN_SMALL_AGGREGATE_COST_SCREEN_V1'
$config.output=Join-Path $local ($name+'\evidence')
$config | Add-Member -NotePropertyName host_build -NotePropertyValue $hostBuild
SaveNew $configPath $config
$configPin=Pin $configPath
$pins[$configPath]=$configPin.sha256
$selected.name=$name
$selected.sources=$sources
$selected.runtime_pins=$pins
$selected.argv[4]='{snapshot}\software\v5\aggregate_small\capability_snapshot.py'
$selected.argv[5]=$configPath
$selected.argv[6]=$configPin.sha256
# Preserve finite180CPU/240wall/3072MiB/three-process outer owner.
if ($sources.Count -ne 8 -or $pins.Count -ne 36) { throw 'EXACT_LAYOUT_CLOSURE' }
SaveNew $selectionPath $selected
[ordered]@{selection=(Pin $selectionPath);configuration=$configPin;sources=$sources.Count;runtime_pins=$pins.Count;executed=$false} | ConvertTo-Json -Depth 5
