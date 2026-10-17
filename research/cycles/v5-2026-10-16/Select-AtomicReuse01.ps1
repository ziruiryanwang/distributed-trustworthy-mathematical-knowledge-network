# Fresh retained-seed continuation. No guest, proof, network or test is launched.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$priorPath = Join-Path $local 'client-actual-03-plan.json'
$controlPath = Join-Path $local 'atomic-import-controls-01-plan.json'
$planPath = Join-Path $local 'client-retained-reuse-01-plan.json'
$run = Join-Path $projectRoot 'product-local\v5-client-owner-runs\client-retained-reuse-01'
if ((Test-Path -LiteralPath $planPath) -or (Test-Path -LiteralPath $run)) { throw 'NOT_FRESH' }
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer) { throw 'FILE_REQUIRED' }
    [ordered]@{bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
if ((Pin $priorPath).sha256 -cne '75d36efe15ad634c8e98c49938a647e602d4c3a789dbaef5fab6fe1da9b49b66') { throw 'PRIOR_PLAN_CHANGED' }
if ((Pin $controlPath).sha256 -cne '2548e019bb45c24f09a03fe609cd8328c22b1be4ae2862c0575658d603225cb3') { throw 'CONTROL_PLAN_CHANGED' }
$plan = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
$controls = Get-Content -LiteralPath $controlPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($property in $plan.sources.psobject.Properties) {
    $name = $property.Name
    $parts = $name.Split('/',2)
    $row = Pin (Join-Path $plan.source_roots.($parts[0]) $parts[1])
    if ($row.bytes -ne $property.Value.bytes -or $row.sha256 -cne $property.Value.sha256) { throw ('RETAINED_SOURCE_CHANGED:'+ $name) }
    if ($name -eq 'owner/actual_owner03.py') {
        $sources['v5/client/actual_owner03.py'] = $row
    } else { $sources[$name] = $row }
}
foreach ($rel in @('mixed_claims/imports_atomic.py','mixed_claims/authoring_atomic.py','client/workspace_atomic.py')) {
    $row = Pin (Join-Path $projectRoot ('software/v5/'+$rel))
    $held = $controls.sources.('v5/'+$rel)
    if (-not $held -or $row.bytes -ne $held.bytes -or $row.sha256 -cne $held.sha256) { throw 'USED_ATOMIC_SOURCE_CHANGED' }
    $sources['v5/'+$rel] = $row
}
$sources['v5/client/actual_assets_atomic.py'] = Pin (Join-Path $projectRoot 'software/v5/client/actual_assets_atomic.py')
$sources['owner/actual_resume_owner.py'] = Pin (Join-Path $projectRoot 'software/v5/client/actual_resume_owner.py')
foreach ($property in $plan.parameters.assets.psobject.Properties) {
    $row = Pin $property.Value.path
    if ($row.bytes -ne $property.Value.bytes -or $row.sha256 -cne $property.Value.sha256) { throw ('ASSET_CHANGED:'+ $property.Name) }
}
$seedPath = Join-Path $projectRoot 'product-local/v5-client-owner-runs/client-actual-03/work/origin/operations/4898246455cde36d15d11631b263a7a4fe9bb8d6c18d920504e72f038ca8490b/preparation/author-1/mixed-packet.json'
$seed = Pin $seedPath
if ($seed.bytes -ne 554165 -or $seed.sha256 -cne '92bbe15b0c8cfcba805efe86939009a9c0c53148e1c9fbd708d48fc6e0fe507f') { throw 'RETAINED_SEED_CHANGED' }
$plan.name = 'client-retained-reuse-01'
$plan.owner_entry = 'actual_resume_owner.py'
$plan.sources = $sources
# The unchanged original outer limits contain both unchanged nonrenewable grants.
# No selected ports are opened; historical Assets checks still parse them.
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($plan|ConvertTo-Json -Depth 16)+"`n")
$stream = [IO.File]::Open($planPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{plan_path=$planPath;plan=(Pin $planPath);sources=$sources.Count;run=$run;seed=$seed;executed=$false} | ConvertTo-Json -Depth 4
