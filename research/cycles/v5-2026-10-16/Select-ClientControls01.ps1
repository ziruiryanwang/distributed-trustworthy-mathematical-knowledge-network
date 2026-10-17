# Prepare one owner plan for the public launcher; no client or test execution.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$planPath = Join-Path $local 'client-controls-01-plan.json'
$allocationRoot = Join-Path $projectRoot 'product-local\v5-client-owner-runs'
$run = Join-Path $allocationRoot 'client-controls-01'
if ((Test-Path -LiteralPath $planPath) -or (Test-Path -LiteralPath $run)) { throw 'NOT_FRESH' }
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer) { throw 'FILE_REQUIRED' }
    [ordered]@{bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$sources = [ordered]@{}
$priors = [ordered]@{
    'frontier-profile-controls-01-selection.json'='89558ab639a2f1af95fe05744e7671b3f2c5c73546988e5f217ce3d56579955f'
    'mixed-imports-controls-01-selection.json'='9a45d66fd63615e9bfccd86ec927d385e7474f51dba367cca7760383faeff397'
}
foreach ($oldName in $priors.Keys) {
    $oldPath = Join-Path $local $oldName
    if ((Pin $oldPath).sha256 -cne $priors[$oldName]) { throw 'PRIOR_SELECTION_CHANGED' }
    $old = Get-Content -LiteralPath $oldPath -Raw | ConvertFrom-Json
    foreach ($property in $old.sources.psobject.Properties) {
        $rel = $property.Name
        if (-not $rel.StartsWith('software/v5/')) { continue }
        if ($rel.StartsWith('software/v5/location/') -or $rel -match '/test_[^/]+\.py$' -or
            $rel -eq 'software/v5/aggregate_claims/aggregate_admission_controls.py') { continue }
        $row = Pin (Join-Path $projectRoot $rel)
        if ($row.sha256 -cne $property.Value) { throw ('RETAINED_SOURCE_CHANGED:'+ $rel) }
        $target = 'v5/'+$rel.Substring('software/v5/'.Length)
        if ($sources.Contains($target) -and $sources[$target].sha256 -cne $row.sha256) { throw 'SOURCE_CONFLICT' }
        $sources[$target] = $row
    }
}
$baselinePath = Join-Path $projectRoot 'research/cycles/v5-2026-10-16/LOCATION-PORTABILITY-BASELINE.json'
$baseline = Get-Content -LiteralPath $baselinePath -Raw | ConvertFrom-Json
foreach ($entry in $baseline.files) {
    $row = Pin (Join-Path $baseline.destination_root $entry.target)
    if (-not $entry.allowed_successor_edit -and ($row.bytes -ne $entry.bytes -or $row.sha256 -cne $entry.sha256)) { throw 'UNCHANGED_PORTABLE_SOURCE' }
    $sources['portable/'+$entry.target] = $row
}
foreach ($file in @('__init__.py','workspace.py','launch.py','boot.py','test_paths.py','test_workspace.py')) {
    $sources['v5/client/'+$file] = Pin (Join-Path $projectRoot ('software/v5/client/'+$file))
}
$sources['owner/control_owner.py'] = Pin (Join-Path $projectRoot 'software/v5/client/control_owner.py')
$plan = [ordered]@{
    schema='DMKN_V5_CLIENT_LAUNCH_V1'; name='client-controls-01'
    installation_root=(Join-Path $projectRoot 'product-local/v4-library-commons-02/commons-v4')
    workspace_root=$allocationRoot
    source_roots=[ordered]@{
        v5=(Join-Path $projectRoot 'software/v5')
        portable=(Join-Path $projectRoot 'software/v5/portable_runtime')
        owner=(Join-Path $projectRoot 'software/v5/client')
    }
    sources=$sources; owner_entry='control_owner.py'; parameters=[ordered]@{}
    limits=[ordered]@{cpu_seconds=30;wall_seconds=90;memory_mib=512;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
    output_limits=[ordered]@{bytes=134217728;entries=4096}
}
if (-not (Test-Path -LiteralPath $allocationRoot)) { New-Item -ItemType Directory -Path $allocationRoot | Out-Null }
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($plan|ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($planPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{plan_path=$planPath;plan=(Pin $planPath);sources=$sources.Count;run=$run;tests=14;executed=$false} | ConvertTo-Json -Depth 4
