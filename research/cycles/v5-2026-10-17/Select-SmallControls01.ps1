# Prepare changed-boundary Python controls only; no project import/test/native call.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$selectionPath = Join-Path $checks 'small-producer-controls-01-selection.json'
$run = Join-Path $checks 'small-producer-controls-01'
foreach ($path in @($selectionPath,$run,(Join-Path $checks 'small-producer-controls-01-attempt.json'))) {
    if (Test-Path -LiteralPath $path) { throw 'NOT_FRESH' }
}
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
$priorPath = Join-Path $checks 'aggregate-resource-controls-01-selection.json'
if ((Digest $priorPath) -cne '9a814b486eed15452732293ec7e76a8c2bc1d43ef0a7712972076a8a7f31ef9e') { throw 'RETAINED_SELECTION_CHANGED' }
$selection = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($relative in @('tools/Run-V5-Check.py','software/v5/production/__init__.py','software/v5/production/producer.py')) {
    $held = $selection.sources.$relative
    $actual = Digest (Join-Path $projectRoot $relative)
    if ($actual -cne $held) { throw ('RETAINED_SOURCE_CHANGED:'+ $relative) }
    $sources[$relative] = $actual
}
foreach ($relative in @('software/v5/aggregate_small/producer.py','software/v5/aggregate_small/__init__.py','software/v5/aggregate_small/test_small.py')) {
    $sources[$relative] = Digest (Join-Path $projectRoot $relative)
}
$selection.name = 'small-producer-controls-01'
$selection.sources = $sources
$selection.argv[4] = '{snapshot}\software\v5\aggregate_small\test_small.py'
if (@($selection.runtime_pins.PSObject.Properties).Count -ne 18) { throw 'EXACT_RUNTIME_PIN_COUNT' }
# Same bounded20CPU/60wall/512MiB/two-process enclosing owner; not a proof Job.
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length);$stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=$selectionPath;sha256=(Digest $selectionPath);sources=$sources;executed=$false} | ConvertTo-Json -Depth 5
