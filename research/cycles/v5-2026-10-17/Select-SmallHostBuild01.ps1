# Prepare one exact fresh link plan; no compiler/host/guest/proof invocation.
param([Parameter(Mandatory=$true)][ValidateSet('snapshot','stage')][string]$Kind)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'small-aggregate-'+$Kind+'-host-build-01'
$selectionPath = Join-Path $checks ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $checks $name),(Join-Path $checks ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'ORDINARY_FILE_REQUIRED' }
    [ordered]@{bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$priorPath = Join-Path $checks 'aggregate-stage-host-build-01-selection.json'
if ((Pin $priorPath).sha256 -cne 'fde4496bea48c5682116c5f2bf7e37bf7834fb422a4abef04b43867dee709326') { throw 'RETAINED_SELECTION_CHANGED' }
$prior = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
if (@($prior.runtime_pins.psobject.Properties).Count -ne 1071) { throw 'RETAINED_RUNTIME_COUNT' }
$hostFile = if ($Kind -ceq 'stage') {'stage_host.rs'} else {'aggregate_host.rs'}
$sources = [ordered]@{}
foreach ($relative in @(('software/v5/aggregate_small/build_'+$Kind+'.py'),('software/v5/aggregate_small/'+$hostFile),'software/v5/aggregate/receipt.rs')) {
    $sources[$relative] = Pin (Join-Path $projectRoot $relative)
}
if ($sources['software/v5/aggregate/receipt.rs'].sha256 -cne '41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254') { throw 'RECEIPT_SOURCE_CHANGED' }
$selection = [ordered]@{
    schema=('DMKN_V5_SMALL_AGGREGATE_'+$Kind.ToUpperInvariant()+'_HOST_BUILD_V1')
    name=$name;authorizes_compile_only=$true;sources=$sources;runtime_pins=$prior.runtime_pins
    limits=$prior.limits
}
$bytes = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($bytes,0,$bytes.Length);$stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=$selectionPath;pin=(Pin $selectionPath);sources=$sources;executed=$false} | ConvertTo-Json -Depth 5
