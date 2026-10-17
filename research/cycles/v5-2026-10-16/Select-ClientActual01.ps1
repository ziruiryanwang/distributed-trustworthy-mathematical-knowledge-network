# One exact ordinary-owner plan; no client, verifier, Node, Lean or proof execution.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$planPath = Join-Path $local 'client-actual-01-plan.json'
$allocationRoot = Join-Path $projectRoot 'product-local\v5-client-owner-runs'
$run = Join-Path $allocationRoot 'client-actual-01'
if ((Test-Path -LiteralPath $planPath) -or (Test-Path -LiteralPath $run)) { throw 'NOT_FRESH' }
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer) { throw 'FILE_REQUIRED' }
    [ordered]@{bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
function Asset([string]$relative,[long]$bytes,[string]$digest) {
    $path = Join-Path $projectRoot $relative
    $row = Pin $path
    if ($row.bytes -ne $bytes -or $row.sha256 -cne $digest) { throw ('ASSET_CHANGED:'+ $relative) }
    [ordered]@{path=$path;bytes=$row.bytes;sha256=$row.sha256}
}
$priorPath = Join-Path $local 'client-controls-01-plan.json'
if ((Pin $priorPath).sha256 -cne '3bf47c5469f4ef66ab28d2023500559437d9ae34202f194acdc01c3e2e934869') { throw 'PRIOR_PLAN_CHANGED' }
$prior = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($property in $prior.sources.psobject.Properties) {
    $name = $property.Name
    if ($name.StartsWith('owner/') -or $name -in @('v5/client/test_paths.py','v5/client/test_workspace.py')) { continue }
    $parts = $name.Split('/',2)
    $sourceRoot = $prior.source_roots.($parts[0])
    if (-not $sourceRoot) { throw 'SOURCE_ROOT_REQUIRED' }
    $row = Pin (Join-Path $sourceRoot $parts[1])
    if ($row.bytes -ne $property.Value.bytes -or $row.sha256 -cne $property.Value.sha256) { throw ('RETAINED_SOURCE_CHANGED:'+ $name) }
    $sources[$name] = $row
}
# The source worker is a separately executed child, so its pin is explicit even
# though parent imports never discover it. The profile template fixes its bytes.
$profilePath = Join-Path $local 'delta-author-01-profile.json'
$profileRow = Pin $profilePath
if ($profileRow.sha256 -cne 'f03b591c6e9e40346028c35b663d4d2c5daaf9a58ec6eb890810f96c6c984a4b') { throw 'PROFILE_TEMPLATE_CHANGED' }
$profile = Get-Content -LiteralPath $profilePath -Raw | ConvertFrom-Json
$worker = Pin (Join-Path $projectRoot 'software/v5/authoring/worker.py')
if ($worker.bytes -ne $profile.worker.bytes -or $worker.sha256 -cne $profile.worker.sha256) { throw 'WORKER_BASELINE_CHANGED' }
$sources['v5/authoring/worker.py'] = $worker
$sources['v5/client/actual_assets.py'] = Pin (Join-Path $projectRoot 'software/v5/client/actual_assets.py')
$sources['owner/actual_owner.py'] = Pin (Join-Path $projectRoot 'software/v5/client/actual_owner.py')
$assets = [ordered]@{
    receipt=(Asset 'experiments/v5-local-checks/module-base-production-01/finish-0/receipt.bin' 223594 '850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47')
    bundle=(Asset 'experiments/v5-local-checks/receipt-prepare-01/prepared/base/bundle.json' 53769 '09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926')
    foundation=(Asset 'experiments/v5-local-checks/receipt-prepare-01/prepared/foundation.json' 23313 '736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c')
    host=(Asset 'experiments/v5-local-checks/module-host-build-03/module_host.exe' 66652160 '74a58215351a641d9efbbffbc389b5faea350c46f5c1e1a48bf76cf77b99d6c9')
    native=(Asset 'experiments/v5-local-checks/delta-native-build-02/native_delta.exe' 1713152 '37a0af1b08e7176fb0d387b3e8439266d7c2c0befe5b08bc3cdd4c90c62d3e40')
    image=(Asset 'experiments/v5-local-checks/module-image-assembly-04/assembly/module_image.bin' 1681428 'd76f623bb1de5c840fd2ef9c1ac35fc6aba2de74cda0f62c11c161f6973da31f')
    frontend=(Asset 'experiments/v5-local-checks/author-lean-link-01/link/AuthorLean.exe' 593408 '1f73b8b0ea20395a43202a3c155e6fd929a5ae0cef2a74a4c70d2625b9e3f69d')
    profile=[ordered]@{path=$profilePath;bytes=$profileRow.bytes;sha256=$profileRow.sha256}
}
$ports = [ordered]@{router=46171;provider=46172;reader=46173;http=46174}
$occupied = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object {$_.LocalPort -in $ports.Values})
if ($occupied.Count) { throw 'SELECTED_PORT_ALREADY_LISTENING' }
$plan = [ordered]@{
    schema='DMKN_V5_CLIENT_LAUNCH_V1';name='client-actual-01'
    installation_root=$prior.installation_root;workspace_root=$allocationRoot
    source_roots=$prior.source_roots;sources=$sources;owner_entry='actual_owner.py'
    parameters=[ordered]@{schema='DMKN_V5_CLIENT_ACTUAL_OWNER_V1';assets=$assets;ports=$ports}
    limits=[ordered]@{cpu_seconds=600;wall_seconds=900;memory_mib=2048;active_processes=8;stdout_bytes=1048576;stderr_bytes=1048576}
    output_limits=[ordered]@{bytes=536870912;entries=16384}
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($plan|ConvertTo-Json -Depth 16)+"`n")
$stream = [IO.File]::Open($planPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{plan_path=$planPath;plan=(Pin $planPath);sources=$sources.Count;run=$run;executed=$false} | ConvertTo-Json -Depth 4
