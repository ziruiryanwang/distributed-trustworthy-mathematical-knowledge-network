# Fresh02 after preserved01 harness projection/census failure; no product rebuild.
# Select one installed restart/discovery boundary; no network runs here.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ReleaseSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$BuildInputSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$SmokeSourceSha256
)
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$name='consolidated-restart-smoke-02'
$inputPath=Join-Path $checks ($name+'-input.json')
$selectionPath=Join-Path $checks ($name+'-selection.json')
foreach ($path in @($inputPath,$selectionPath,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_SMOKE_REQUIRED:'+ $path) }
}
function Pin([string]$path) {
    $item=Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) { throw 'ORDINARY_FILE_REQUIRED' }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
function Exact([string]$path,[string]$digest) {
    $row=Pin $path
    if ($row.sha256 -cne $digest) { throw ('ADOPTED_PIN_CHANGED:'+ $path) }
    $row
}
function SaveNew([string]$path,$value) {
    $raw=[Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 32)+"`n")
    if ($raw.Length -gt 1048576) { throw 'INPUT_SIZE' }
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
}
$install=Join-Path $projectRoot 'product-local\v5-distribution-consolidated-01\Mathematical Commons v5'
$releasePin=Exact (Join-Path $install 'V5-RELEASE.json') $ReleaseSha256
$release=Get-Content -LiteralPath $releasePin.path -Raw -Encoding UTF8 | ConvertFrom-Json
$buildPin=Exact (Join-Path $checks 'distribution-consolidated-01-input.json') $BuildInputSha256
$build=Get-Content -LiteralPath $buildPin.path -Raw -Encoding UTF8 | ConvertFrom-Json
if ($release.schema -cne 'DMKN_V5_DIRECTORY_RELEASE_V3' -or $release.base_role -cne 'mathematical-client-location-v1' -or
    $release.build_input_sha256 -cne $BuildInputSha256 -or @($release.sdk_sources.psobject.Properties).Count -ne 121 -or
    @($build.sdk_sources.psobject.Properties).Count -ne 121) { throw 'ADOPTED_CONSOLIDATED_MAP' }
$basisPin=Exact (Join-Path $checks 'placement-network-integration-02-input.json') '6e14ba3b8abbce616a8115b7ce3a229242869a3b8861c427c52e3221a2f47f58'
$basis=Get-Content -LiteralPath $basisPin.path -Raw -Encoding UTF8 | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_PLACEMENT_NETWORK_INTEGRATION_INPUT_V1') { throw 'FIXTURE_BASIS' }
$sources=[ordered]@{
    'tools/Run-V5-Check.py'='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
    'software/v5/consolidated_candidate/restart_smoke02.py'=$SmokeSourceSha256
    'software/v5/examples/mirror_method/method_query.py'='0ddbc8dac7e60180f3f9aad3216873158d8b2722a9d31c48112e20262298c642'
    'software/v5/examples/terminal_i/congruence_query.py'='07a323edd3b10f94f6fc7f9790191b1145666b547b4575c70c4a7261b3d8fadd'
}
foreach ($relative in $sources.Keys) { $null=Exact (Join-Path $projectRoot $relative) $sources[$relative] }
$runtime=[ordered]@{}
function AddPin($row) {
    $actual=Exact $row.path $row.sha256
    if ($actual.bytes -ne $row.bytes) { throw 'PIN_EXTENT' }
    if ($runtime.Contains($row.path) -and $runtime[$row.path] -cne $row.sha256) { throw 'PIN_CONFLICT' }
    $runtime[$row.path]=$row.sha256
}
foreach ($property in $release.sdk_sources.psobject.Properties) {
    $relative=$property.Value
    if ($relative -cne ('sdk/'+$property.Name) -or $relative.Contains('..')) { throw 'INSTALLED_LOGICAL_PATH' }
    $row=$release.files.$relative
    $selected=$build.sdk_sources.($property.Name)
    if ($null -eq $selected -or $row.bytes -ne $selected.bytes -or $row.sha256 -cne $selected.sha256) { throw 'BUILD_INSTALL_SOURCE_BINDING' }
    AddPin ([ordered]@{path=(Join-Path $install $relative);bytes=$row.bytes;sha256=$row.sha256})
}
if ($runtime.Count -ne 121) { throw 'EXACT_INSTALLED_SDK' }
foreach ($relative in @('distribution.py','base/RELEASE-MANIFEST.json')) {
    $row=$release.files.$relative
    AddPin ([ordered]@{path=(Join-Path $install $relative);bytes=$row.bytes;sha256=$row.sha256})
}
$oldPython=Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\receiver\runtime\python'
$pythonRoot=Join-Path $install 'base\receiver\runtime\python'
if (@($basis.python_runtime).Count -ne 18) { throw 'EXACT_PYTHON_BASIS' }
foreach ($row in $basis.python_runtime) {
    if (-not $row.path.StartsWith($oldPython+'\',[StringComparison]::Ordinal)) { throw 'PYTHON_BASIS_SCOPE' }
    $suffix=$row.path.Substring($oldPython.Length+1)
    $relative='base/receiver/runtime/python/'+$suffix.Replace('\','/')
    $installed=$release.files.$relative
    if ($installed.bytes -ne $row.bytes -or $installed.sha256 -cne $row.sha256) { throw 'UNCHANGED_INSTALLED_PYTHON' }
    AddPin ([ordered]@{path=(Join-Path $pythonRoot $suffix);bytes=$row.bytes;sha256=$row.sha256})
}
foreach ($row in @($releasePin,$buildPin,$basisPin,$basis.receipt,$basis.journal,$basis.bundle)) { AddPin $row }
# Select once, after all preparation work. Do not refresh horizons after failure.
$now=[DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$inputValue=[ordered]@{
    schema='DMKN_CONSOLIDATED_RESTART_SMOKE_INPUT_V1';installation=$install
    release=$releasePin;build_input=$buildPin
    receipt=$basis.receipt;journal=$basis.journal;bundle=$basis.bundle;workspace_config=$basis.workspace_config
    generation_horizons=[ordered]@{admission_close_ms=($now+180000);retention_not_after_ms=($now+240000);
        write_until_ms=($now+150000);retention_until_ms=($now+220000);retention_end_ms=($now+210000)}
}
SaveNew $inputPath $inputValue
$inputPin=Pin $inputPath;AddPin $inputPin
$selected=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@((Join-Path $pythonRoot 'python.exe'),'-I','-S','-B','{snapshot}\software\v5\consolidated_candidate\restart_smoke02.py',
        '--input',$inputPath,'--input-sha',$inputPin.sha256,'--output','{output}')
    limits=[ordered]@{cpu_seconds=150;wall_seconds=300;memory_mib=512;active_processes=6;stdout_bytes=1048576;stderr_bytes=1048576}
}
if ($runtime.Count -gt 256) { throw 'FINITE_RUNTIME_CLOSURE' }
SaveNew $selectionPath $selected
[ordered]@{selection=(Pin $selectionPath);input=$inputPin;source_count=$sources.Count;runtime_pins=$runtime.Count;
    native_calls=0;proof_calls=0;executed=$false} | ConvertTo-Json -Depth 6

