# Prepare only seven changed-policy controls. No host, native or proof call.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$selectionPath = Join-Path $checks 'aggregate-resource-controls-01-selection.json'
$run = Join-Path $checks 'aggregate-resource-controls-01'
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath $run)) { throw 'NOT_FRESH' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
$priorPath = Join-Path $checks 'aggregate-producer-controls-01-selection.json'
if ((Digest $priorPath) -cne '40a4d0082169575d028dbeeed637fd500e8053a735e98433078331c02bf713f9') { throw 'PRIOR_SELECTION_CHANGED' }
$selection = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($relative in @('tools/Run-V5-Check.py','software/v5/production/__init__.py','software/v5/production/producer.py')) {
    $held = $selection.sources.$relative
    $actual = Digest (Join-Path $projectRoot $relative)
    if ($actual -cne $held) { throw ('RETAINED_SOURCE_CHANGED:'+ $relative) }
    $sources[$relative] = $actual
}
$producer = 'software/v5/aggregate_resources/producer.py'
if ((Digest (Join-Path $projectRoot $producer)) -cne '1d191bdc2079760ce89a57a08924254f01487d24726e10b386c7eca1ef9eec09') { throw 'REVIEWED_PRODUCER_CHANGED' }
if ((Digest (Join-Path $projectRoot 'software/v5/aggregate_resources/test_resources.py')) -cne 'f86ac914fab8851077313a7089391b8ed5c37b7e31a8cb78b6842235056cc111') { throw 'REVIEWED_CONTROLS_CHANGED' }
foreach ($relative in @($producer,'software/v5/aggregate_resources/__init__.py','software/v5/aggregate_resources/test_resources.py')) {
    $sources[$relative] = Digest (Join-Path $projectRoot $relative)
}
$selection.name = 'aggregate-resource-controls-01'
$selection.sources = $sources
$selection.argv[4] = '{snapshot}\software\v5\aggregate_resources\test_resources.py'
# The old test's assembly-data regression is unchanged and is not rerun.
foreach ($relative in @('experiments/v5-local-checks/proof-memo-image-assembly-01/RESULT.json','experiments/v5-local-checks/proof-memo-image-assembly-01/selection.json')) {
    $selection.runtime_pins.PSObject.Properties.Remove((Join-Path $projectRoot $relative))
}
if (@($selection.runtime_pins.PSObject.Properties).Count -ne 18) { throw 'EXACT_RUNTIME_PIN_COUNT' }
# Retain20CPU/60wall/512MiB/two-process; this does not allocate a large proof Job.
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length);$stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=$selectionPath;sha256=(Digest $selectionPath);sources=$sources.Count;executed=$false} | ConvertTo-Json
