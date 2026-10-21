# Pure projection controls only; no product service, credential or database.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$TestSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$OwnerSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$FeaturesSha256
)
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks=Join-Path $projectRoot 'experiments/v5-local-checks'
$name='managed-observed-controls-01'
$selectionPath=Join-Path $checks ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw 'FRESH_CONTROLS_REQUIRED' }
}
function CheckPin([string]$path,[string]$expected) {
    $item=Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) -or
        (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $expected) { throw 'REVIEWED_PIN_CHANGED' }
}
$basisPath=Join-Path $checks 'distribution-managed-contribution-build-01-selection.json'
CheckPin $basisPath 'ad982f4d49107a6bc6ed4e6268adad9e9e88f963930106ba06eda57faedd5959'
$basis=Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
$excluded=Join-Path $checks 'distribution-managed-contribution-01-input.json'
$runtime=[ordered]@{}
foreach ($row in $basis.runtime_pins.psobject.Properties) {
    if ($row.Name -ceq $excluded) { continue }
    CheckPin $row.Name $row.Value
    $runtime[$row.Name]=$row.Value
}
if ($runtime.Count -ne 28 -or -not $runtime.Contains($basis.argv[0])) { throw 'EXACT_PRESERVED_RUNTIME' }
$sources=[ordered]@{
    'tools/Run-V5-Check.py'='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
    'software/v5/managed_observed/observation_controls.py'=$TestSha256
    'software/v5/managed_observed/client/managed_owner.py'=$OwnerSha256
    'software/v5/instantiation_discovery/discovery/formal_features.py'=$FeaturesSha256
}
foreach($relative in $sources.Keys) { CheckPin (Join-Path $projectRoot $relative) $sources[$relative] }
$selection=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($basis.argv[0],'-I','-S','-B','{snapshot}\software\v5\managed_observed\observation_controls.py','--output','{output}')
    limits=[ordered]@{cpu_seconds=10;wall_seconds=30;memory_mib=128;active_processes=1;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 40)+"`n")
if($raw.Length -gt 1048576) { throw 'SELECTION_SIZE' }
$stream=[IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=$selectionPath;selection_sha256=(Get-FileHash -LiteralPath $selectionPath -Algorithm SHA256).Hash.ToLowerInvariant();
    source_count=$sources.Count;runtime_pins=$runtime.Count;executed=$false} | ConvertTo-Json
