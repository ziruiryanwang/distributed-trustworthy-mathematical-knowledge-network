# Only the three unreached controls, with a corrected synthetic definition record.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$priorPath = Join-Path $local 'atomic-import-controls-01-plan.json'
$planPath = Join-Path $local 'atomic-import-controls-02-plan.json'
$run = Join-Path $projectRoot 'product-local\v5-client-owner-runs\atomic-import-controls-02'
if ((Test-Path -LiteralPath $planPath) -or (Test-Path -LiteralPath $run)) { throw 'NOT_FRESH' }
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer) { throw 'FILE_REQUIRED' }
    [ordered]@{bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
if ((Pin $priorPath).sha256 -cne '2548e019bb45c24f09a03fe609cd8328c22b1be4ae2862c0575658d603225cb3') { throw 'PRIOR_PLAN_CHANGED' }
$plan = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($property in $plan.sources.psobject.Properties) {
    $name = $property.Name
    $parts = $name.Split('/',2)
    $row = Pin (Join-Path $plan.source_roots.($parts[0]) $parts[1])
    if ($row.bytes -ne $property.Value.bytes -or $row.sha256 -cne $property.Value.sha256) { throw ('RETAINED_SOURCE_CHANGED:'+ $name) }
    if ($name.StartsWith('owner/') -or $name -eq 'v5/mixed_claims/test_atomic.py') { continue }
    $sources[$name] = $row
}
$sources['v5/mixed_claims/test_atomic02.py'] = Pin (Join-Path $projectRoot 'software/v5/mixed_claims/test_atomic02.py')
$sources['owner/atomic_control_owner02.py'] = Pin (Join-Path $projectRoot 'software/v5/client/atomic_control_owner02.py')
$plan.name = 'atomic-import-controls-02'
$plan.owner_entry = 'atomic_control_owner02.py'
$plan.sources = $sources
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($plan|ConvertTo-Json -Depth 16)+"`n")
$stream = [IO.File]::Open($planPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{plan_path=$planPath;plan=(Pin $planPath);sources=$sources.Count;run=$run;tests=3;executed=$false} | ConvertTo-Json -Depth 4
