# Prepare focused synthetic controls only; this selector runs no Python/host.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$selectionPath = Join-Path $checks 'aggregate-producer-controls-01-selection.json'
$run = Join-Path $checks 'aggregate-producer-controls-01'
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath $run)) { throw 'NOT_FRESH' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
$priorPath = Join-Path $checks 'producer-controls-01-selection.json'
if ((Digest $priorPath) -cne 'e3f2bbfeff4f3be607068da5499b3f3c251e41d15b36b325464e328451c8828c') { throw 'PRIOR_SELECTION_CHANGED' }
$selection = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($relative in @('tools/Run-V5-Check.py','software/v5/production/__init__.py','software/v5/production/producer.py')) {
    $held = $selection.sources.$relative
    $actual = Digest (Join-Path $projectRoot $relative)
    if ($actual -cne $held) { throw ('RETAINED_SOURCE_CHANGED:'+ $relative) }
    $sources[$relative] = $actual
}
$producer = 'software/v5/aggregate_production/producer.py'
if ((Digest (Join-Path $projectRoot $producer)) -cne '796eb24619370a30192db6d0f63b914516919e7cae90aee32a1750736331b86b') { throw 'REVIEWED_PRODUCER_CHANGED' }
foreach ($relative in @($producer,'software/v5/aggregate_production/__init__.py','software/v5/aggregate_production/test_producer.py')) {
    $sources[$relative] = Digest (Join-Path $projectRoot $relative)
}
$selection.name = 'aggregate-producer-controls-01'
$selection.sources = $sources
$selection.argv[4] = '{snapshot}\software\v5\aggregate_production\test_producer.py'
$data = [ordered]@{
    'experiments/v5-local-checks/proof-memo-image-assembly-01/RESULT.json'='50de313fbc8f20b3f48d971f3183bf66f1079cafe18af460538b414d715a2f4e'
    'experiments/v5-local-checks/proof-memo-image-assembly-01/selection.json'='60b1955f8b7f70b9238693ffb9c31018dc19a2089d6aec13b3238d2810f33600'
}
foreach ($entry in $data.GetEnumerator()) {
    $path = Join-Path $projectRoot $entry.Key
    if ((Digest $path) -cne $entry.Value) { throw ('RETAINED_REGRESSION_INPUT_CHANGED:'+ $entry.Key) }
    $selection.runtime_pins | Add-Member -NotePropertyName $path -NotePropertyValue $entry.Value
}
# Reuse unchanged20CPU/60wall/512MiB/two-process and explicit installed Python.
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length);$stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=$selectionPath;sha256=(Digest $selectionPath);sources=$sources.Count;executed=$false} | ConvertTo-Json
