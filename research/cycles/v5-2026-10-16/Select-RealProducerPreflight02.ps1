# One genuine record/request preflight only. No compiler, host or proof launch.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$selectionPath = Join-Path $checks 'real-producer-preflight-02-selection.json'
$run = Join-Path $checks 'real-producer-preflight-02'
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath $run)) { throw 'NOT_FRESH' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
$priorPath = Join-Path $checks 'aggregate-resource-controls-01-selection.json'
if ((Digest $priorPath) -cne '9a814b486eed15452732293ec7e76a8c2bc1d43ef0a7712972076a8a7f31ef9e') { throw 'PRIOR_SELECTION_CHANGED' }
$prior = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($relative in @('tools/Run-V5-Check.py','software/v5/production/__init__.py','software/v5/production/producer.py','software/v5/aggregate_resources/__init__.py','software/v5/aggregate_resources/producer.py')) {
    $actual = Digest (Join-Path $projectRoot $relative)
    if ($actual -cne $prior.sources.$relative) { throw ('USED_SOURCE_CHANGED:'+ $relative) }
    $sources[$relative] = $actual
}
$adapterRelative = 'software/v5/aggregate_resources/preflight_actual.py'
$adapterPath = Join-Path $projectRoot $adapterRelative
$adapterHash = Digest $adapterPath
if ($adapterHash -cne '4720822d4174c2808db57972046cd23b16189fd6769981d36811540e9f918f27') { throw 'REVIEWED_ADAPTER_CHANGED' }
$sources[$adapterRelative] = $adapterHash
$adapter = Get-Content -LiteralPath $adapterPath -Raw
$runtime = [ordered]@{}
function Add-Pin([string]$path,[string]$expected,[long]$bytes=0) {
    $resolved = [IO.Path]::GetFullPath($path)
    if ($expected -cnotmatch '^[0-9a-f]{64}$') { throw 'PIN_FORMAT' }
    if ((Digest $resolved) -cne $expected) { throw ('INPUT_CHANGED:'+ $resolved) }
    if ($bytes -gt 0 -and (Get-Item -LiteralPath $resolved).Length -ne $bytes) { throw ('INPUT_SIZE:'+ $resolved) }
    if ($runtime.Contains($resolved) -and $runtime[$resolved] -cne $expected) { throw 'PIN_CONFLICT' }
    $runtime[$resolved] = $expected
}
# Parse only the reviewed literal data tables, without importing/executing Python.
$recordBlock = [regex]::Match($adapter,'(?ms)^RECORDS = \{\r?\n(?<body>.*?)^\}')
$recordRows = [regex]::Matches($recordBlock.Groups['body'].Value,'"(?<path>[^"]+)": "(?<sha>[0-9a-f]{64})"')
if (-not $recordBlock.Success -or $recordRows.Count -ne 19) { throw 'EXACT_RECORD_TABLE' }
foreach ($row in $recordRows) { Add-Pin (Join-Path $checks $row.Groups['path'].Value) $row.Groups['sha'].Value }
$assetBlock = [regex]::Match($adapter,'(?ms)^ASSETS = \{\r?\n(?<body>.*?)^\}')
$assetRows = [regex]::Matches($assetBlock.Groups['body'].Value,'"[^"]+": \("(?<path>[^"]+)", (?<bytes>[0-9]+),\s*"(?<sha>[0-9a-f]{64})"\)')
if (-not $assetBlock.Success -or $assetRows.Count -ne 7) { throw 'EXACT_ASSET_TABLE' }
foreach ($row in $assetRows) { Add-Pin (Join-Path $checks $row.Groups['path'].Value) $row.Groups['sha'].Value ([long]$row.Groups['bytes'].Value) }
$template = Get-Content -LiteralPath (Join-Path $checks 'module-base-production-01/profile.json') -Raw | ConvertFrom-Json
foreach ($pin in @($template.supervisor_manifest,$template.python,$template.python_dll)+@($template.runtime_pins)) { Add-Pin $pin.path $pin.sha256 $pin.bytes }
$manifest = Get-Content -LiteralPath $template.supervisor_manifest.path -Raw | ConvertFrom-Json
$install = Split-Path -Parent $template.supervisor_manifest.path
foreach ($relative in @('operator/commons.py','receiver/helpers/domains.py','receiver/helpers/run_stage.py')) {
    $pin = $manifest.files.$relative
    Add-Pin (Join-Path $install $relative) $pin.sha256 $pin.bytes
}
$buildMap = Get-Content -LiteralPath (Join-Path $checks 'aggregate-stage-host-build-01/source-map.json') -Raw | ConvertFrom-Json
foreach ($property in $buildMap.PSObject.Properties) {
    Add-Pin (Join-Path (Join-Path $checks 'aggregate-stage-host-build-01/source') $property.Name) $property.Value.sha256 $property.Value.bytes
}
if ($runtime.Count -ne 51) { throw ('EXACT_RUNTIME_COUNT:'+ $runtime.Count) }
$selection = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name='real-producer-preflight-02';sources=$sources;runtime_pins=$runtime
    argv=@($template.python.path,'-I','-S','-B','{snapshot}\software\v5\aggregate_resources\preflight_actual.py','--output','{output}\evidence')
    limits=[ordered]@{cpu_seconds=30;wall_seconds=90;memory_mib=512;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
# The two-process outer limit covers the retained embedded Python launcher;
# no inner native/proof call is part of this operation.
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length);$stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=$selectionPath;sha256=(Digest $selectionPath);sources=$sources.Count;runtime_pins=$runtime.Count;executed=$false} | ConvertTo-Json
