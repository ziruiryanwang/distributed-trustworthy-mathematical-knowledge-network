# Fresh exact plan for qualified imported names; no product/native execution.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$priorPath = Join-Path $local 'client-actual-02-plan.json'
$planPath = Join-Path $local 'client-actual-03-plan.json'
$run = Join-Path $projectRoot 'product-local\v5-client-owner-runs\client-actual-03'
if ((Test-Path -LiteralPath $planPath) -or (Test-Path -LiteralPath $run)) { throw 'NOT_FRESH' }
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer) { throw 'FILE_REQUIRED' }
    [ordered]@{bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
if ((Pin $priorPath).sha256 -cne 'd0b801146563c6302f6bdb5120fb53cc29e6e3f4d37fab8db4ddd4d3da495ab3') { throw 'PRIOR_PLAN_CHANGED' }
$plan = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($property in $plan.sources.psobject.Properties) {
    $name = $property.Name
    $parts = $name.Split('/',2)
    $sourceRoot = $plan.source_roots.($parts[0])
    if (-not $sourceRoot) { throw 'SOURCE_ROOT_REQUIRED' }
    $row = Pin (Join-Path $sourceRoot $parts[1])
    if ($row.bytes -ne $property.Value.bytes -or $row.sha256 -cne $property.Value.sha256) { throw ('RETAINED_SOURCE_CHANGED:'+ $name) }
    if ($name -eq 'owner/actual_owner02.py') { continue }
    $sources[$name] = $row
}
$sources['owner/actual_owner03.py'] = Pin (Join-Path $projectRoot 'software/v5/client/actual_owner03.py')
if ($sources.Count -ne 85) { throw 'SOURCE_COUNT' }
foreach ($property in $plan.parameters.assets.psobject.Properties) {
    $actual = Pin $property.Value.path
    if ($actual.bytes -ne $property.Value.bytes -or $actual.sha256 -cne $property.Value.sha256) { throw ('ASSET_CHANGED:'+ $property.Name) }
}
$ports = @($plan.parameters.ports.psobject.Properties | ForEach-Object { $_.Value })
$occupied = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object {$_.LocalPort -in $ports})
if ($occupied.Count) { throw 'SELECTED_PORT_ALREADY_LISTENING' }
$plan.name = 'client-actual-03'
$plan.owner_entry = 'actual_owner03.py'
$plan.sources = $sources
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($plan|ConvertTo-Json -Depth 16)+"`n")
$stream = [IO.File]::Open($planPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{plan_path=$planPath;plan=(Pin $planPath);sources=$sources.Count;run=$run;executed=$false} | ConvertTo-Json -Depth 4
