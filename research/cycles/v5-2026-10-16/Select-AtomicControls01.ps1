# One fresh changed-boundary control plan; this script never launches tests.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$priorPath = Join-Path $local 'client-actual-03-plan.json'
$planPath = Join-Path $local 'atomic-import-controls-01-plan.json'
$run = Join-Path $projectRoot 'product-local\v5-client-owner-runs\atomic-import-controls-01'
if ((Test-Path -LiteralPath $planPath) -or (Test-Path -LiteralPath $run)) { throw 'NOT_FRESH' }
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer) { throw 'FILE_REQUIRED' }
    [ordered]@{bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
if ((Pin $priorPath).sha256 -cne '75d36efe15ad634c8e98c49938a647e602d4c3a789dbaef5fab6fe1da9b49b66') { throw 'PRIOR_PLAN_CHANGED' }
$plan = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($property in $plan.sources.psobject.Properties) {
    $name = $property.Name
    $parts = $name.Split('/',2)
    $sourceRoot = $plan.source_roots.($parts[0])
    if (-not $sourceRoot) { throw 'SOURCE_ROOT_REQUIRED' }
    $row = Pin (Join-Path $sourceRoot $parts[1])
    if ($row.bytes -ne $property.Value.bytes -or $row.sha256 -cne $property.Value.sha256) { throw ('RETAINED_SOURCE_CHANGED:'+ $name) }
    if ($name.StartsWith('owner/')) { continue }
    $sources[$name] = $row
}
foreach ($rel in @('mixed_claims/imports_atomic.py','mixed_claims/authoring_atomic.py',
    'client/workspace_atomic.py','mixed_claims/test_atomic.py','mixed_claims/test_imports.py',
    'mixed_claims/test_receiver.py','aggregate_claims/aggregate_admission_controls.py')) {
    $sources['v5/'+$rel] = Pin (Join-Path $projectRoot ('software/v5/'+$rel))
}
$sources['owner/atomic_control_owner.py'] = Pin (Join-Path $projectRoot 'software/v5/client/atomic_control_owner.py')
$plan.name = 'atomic-import-controls-01'
$plan.owner_entry = 'atomic_control_owner.py'
$plan.sources = $sources
$plan.parameters = [ordered]@{}
$plan.limits = [ordered]@{cpu_seconds=30;wall_seconds=90;memory_mib=512;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
$plan.output_limits = [ordered]@{bytes=134217728;entries=4096}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($plan|ConvertTo-Json -Depth 16)+"`n")
$stream = [IO.File]::Open($planPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{plan_path=$planPath;plan=(Pin $planPath);sources=$sources.Count;run=$run;tests=13;cold_closure_gate=1;executed=$false} | ConvertTo-Json -Depth 4
