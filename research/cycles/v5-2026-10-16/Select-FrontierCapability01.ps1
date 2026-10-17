# One fresh capability selection, not a repeated efficiency comparison or proof.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'frontier-capability-execution-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
$configPath = Join-Path $local ($name+'-configuration.json')
foreach ($path in @($selectionPath,$configPath,(Join-Path $local $name),(Join-Path $local ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer) { throw 'FILE_REQUIRED' }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
function SaveNew([string]$path,$value) {
    $raw = [Text.UTF8Encoding]::new($false).GetBytes(($value|ConvertTo-Json -Depth 15)+"`n")
    $stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
}
$priorPath = Join-Path $local 'proof-memo-aggregate-snapshot-01-selection.json'
$priorConfigPath = Join-Path $local 'proof-memo-aggregate-snapshot-01-configuration.json'
if ((Pin $priorPath).sha256 -cne '8c630587ea56bb0a4b6ddf7e014294dfbbbb76395f72e2f6d4d1dc7b53bcff04') { throw 'PRIOR_SELECTION_CHANGED' }
if ((Pin $priorConfigPath).sha256 -cne 'e0cf7861d1a1714e64d54416dfdef726152d9eeefde6df9fce39ffda7b96277f') { throw 'PRIOR_CONFIGURATION_CHANGED' }
$selected = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
$config = Get-Content -LiteralPath $priorConfigPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($property in $selected.sources.psobject.Properties) {
    if ((Pin (Join-Path $projectRoot $property.Name)).sha256 -cne $property.Value) { throw ('RETAINED_SOURCE_CHANGED:'+ $property.Name) }
    if ($property.Name -eq 'software/v5/aggregate_host/snapshot.py') { continue }
    $sources[$property.Name] = $property.Value
}
$adapter = 'software/v5/aggregate_host/capability_snapshot.py'
$adapterPin = Pin (Join-Path $projectRoot $adapter)
if ($adapterPin.sha256 -cne '9f914e2c5c5c86d3bd1f4efbdc45a16fadec67f14df082b82a2d506e98d506b5') { throw 'CAPABILITY_ADAPTER_CHANGED' }
$sources[$adapter] = $adapterPin.sha256
$pins = [ordered]@{}
foreach ($property in $selected.runtime_pins.psobject.Properties) {
    if ((Pin $property.Name).sha256 -cne $property.Value) { throw ('RETAINED_RUNTIME_CHANGED:'+ $property.Name) }
    if ($property.Name -ceq $priorConfigPath) { continue }
    $pins[$property.Name] = $property.Value
}
$config.output = Join-Path $local ($name+'\evidence')
SaveNew $configPath $config
$configPin = Pin $configPath
$pins[$configPath] = $configPin.sha256
$selected.name = $name
$selected.sources = $sources
$selected.runtime_pins = $pins
$selected.argv[4] = '{snapshot}\software\v5\aggregate_host\capability_snapshot.py'
$selected.argv[5] = $configPath
$selected.argv[6] = $configPin.sha256
if ($sources.Count -ne 8 -or $pins.Count -ne 29) { throw 'EXACT_CLOSURE_COUNT' }
SaveNew $selectionPath $selected
[ordered]@{selection=(Pin $selectionPath);configuration=$configPin;sources=$sources.Count;runtime_pins=$pins.Count;guest_calls=1;proof_calls=0;executed=$false} | ConvertTo-Json -Depth 5
