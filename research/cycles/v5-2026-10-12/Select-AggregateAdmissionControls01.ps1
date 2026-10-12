# Prepare one finite, synthetic control selection. Never launches the controls.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'aggregate-admission-controls-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $local $name),(Join-Path $local ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer) { throw 'FILE_REQUIRED' }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$sources = [ordered]@{
    'software/v5/admission/__init__.py'='41985fbdd6cfd55b26852adfc784100713528430c8688fdff1fb3cdc5acafb54'
    'software/v5/admission/bindings.py'='233ff29992d524eb1d92d7f1beb9261479e76737acd591c923a30cd32588d1ee'
    'software/v5/admission/verifier.py'='9f77bd17abbf87d8f777c52c047d41cfbfd1b29078f29a173006ccad99839571'
    'software/v5/modules/__init__.py'='1c69237f05e6b86129605789da098235453d00b2f0139502cdbe9206d5891946'
    'software/v5/modules/codec.py'='e01b7478640d72ad5e0634443c87d99a9bf91bc65d2fc2297355b92a27649f58'
    'software/v5/aggregate_claims/__init__.py'='c9440183d92c887c4f6bac36f4bd51b7cf935ddf0f3f155aac8b8f1d48ad6540'
    'software/v5/aggregate_claims/bindings.py'='a6777395353f0421111cc2a2a0b06208dfbe4d60549899a70a42cda0bda9e543'
    'software/v5/aggregate_claims/admission_binding.py'='2746704a28c180df0f549864a7c96b138110f0f6ff57e0de4aae66f198e059f3'
    'software/v5/aggregate_claims/aggregate_admission.py'='a6a7e8041674de60fff198ed8522b1c28e0662bbf1f8acce8fe3eee60ab03561'
    'software/v5/aggregate_claims/aggregate_admission_controls.py'='dc6ba079cb9c2bb60b001ea9a25ea9da7eeea83970d7b68123fa0f34d742fa6a'
    'tools/Run-V5-Check.py'='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
}
foreach ($relative in $sources.Keys) {
    if ((Pin (Join-Path $projectRoot $relative)).sha256 -cne $sources[$relative]) { throw ('REVIEWED_SOURCE_CHANGED:'+ $relative) }
}
$priorPath = Join-Path $local 'delta-claim-controls-01-selection.json'
$priorPin = Pin $priorPath
if ($priorPin.sha256 -cne 'd3a85d4401d4a100a00a475299341ac436ceddbf04aaf184ce71e0b2f764a6fb') { throw 'ADOPTED_RUNTIME_SELECTION' }
$prior = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
$pythonRoot = Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\receiver\runtime\python'
$prefix = $pythonRoot+'\'
$pins = [ordered]@{}
foreach ($property in $prior.runtime_pins.psobject.Properties) {
    if (-not $property.Name.StartsWith($prefix,[StringComparison]::OrdinalIgnoreCase)) { continue }
    $actual = Pin $property.Name
    if ($actual.sha256 -cne $property.Value) { throw ('PRIOR_RUNTIME_CHANGED:'+ $property.Name) }
    $pins[$actual.path] = $actual.sha256
}
if ($pins.Count -ne 18) { throw 'EXACT_PYTHON_RUNTIME_CLOSURE' }
$manifest = Pin (Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\RELEASE-MANIFEST.json')
if ($manifest.sha256 -cne 'a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed') { throw 'FROZEN_SUPERVISOR_MANIFEST' }
foreach ($row in @($manifest,$priorPin)) { $pins[$row.path] = $row.sha256 }
$python = Join-Path $pythonRoot 'python.exe'
if (-not $pins.Contains($python) -or $prior.argv[0] -cne $python) { throw 'PINNED_PYTHON' }
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$pins
    argv=@($python,'-I','-S','-B','{snapshot}\software\v5\aggregate_claims\aggregate_admission_controls.py')
    limits=[ordered]@{cpu_seconds=30;wall_seconds=60;memory_mib=512;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=(Pin $selectionPath);sources=$sources.Count;runtime_pins=$pins.Count;synthetic_groups=17;native_calls=0;real_receipt_verifications=0;executed=$false} | ConvertTo-Json -Depth 5
