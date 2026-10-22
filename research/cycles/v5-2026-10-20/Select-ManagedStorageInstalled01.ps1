# Preparation only. Root separately adopts the actual build and source reviews.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ReleaseSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$BuildInputSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$AdapterSourceSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$AdapterReviewSha256
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks=Join-Path $projectRoot 'experiments/v5-local-checks'
$cycle=Join-Path $projectRoot 'research/cycles/v5-2026-10-20'
$name='managed-storage-installed-01'
$inputPath=Join-Path $checks ($name+'-input.json')
$selectionPath=Join-Path $checks ($name+'-selection.json')
foreach ($path in @($inputPath,$selectionPath,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_STORAGE_CHECK_REQUIRED:'+ $path) }
}
function Pin([string]$path,[string]$expected) {
    $item=Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) { throw 'ORDINARY_FILE_REQUIRED' }
    $sha=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or $sha -cne $expected) { throw ('REVIEWED_PIN_CHANGED:'+ $path) }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=$sha}
}
function SaveNew([string]$path,$value) {
    $raw=[Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 32)+"`n")
    if ($raw.Length -gt 1048576) { throw 'INPUT_SIZE' }
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
}
$null=Pin (Join-Path $cycle 'MANAGED-STORAGE-INSTALLED-SOURCE-REVIEW.md') $AdapterReviewSha256
$install=Join-Path $projectRoot 'product-local/v5-distribution-managed-storage-01/Mathematical Commons v5'
$releasePin=Pin (Join-Path $install 'V5-RELEASE.json') $ReleaseSha256
$buildPin=Pin (Join-Path $checks 'distribution-managed-storage-01-input.json') $BuildInputSha256
$release=Get-Content -LiteralPath $releasePin.path -Raw -Encoding UTF8 | ConvertFrom-Json
$build=Get-Content -LiteralPath $buildPin.path -Raw -Encoding UTF8 | ConvertFrom-Json
if ($release.schema -cne 'DMKN_V5_DIRECTORY_RELEASE_V3' -or $release.base_role -cne 'mathematical-client-location-v1' -or
    $release.build_input_sha256 -cne $BuildInputSha256 -or $build.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or
    @($release.sdk_sources.psobject.Properties).Count -ne 129 -or @($build.sdk_sources.psobject.Properties).Count -ne 129) { throw 'ADOPTED_STORAGE_MAP' }
$basisPin=Pin (Join-Path $checks 'consolidated-restart-smoke-02-selection.json') '04522d4b3fe8679c4d9a6af12c390b521f1ebe9135db6a2fdfe504776828d3ce'
$basis=Get-Content -LiteralPath $basisPin.path -Raw -Encoding UTF8 | ConvertFrom-Json
$templatePin=Pin (Join-Path $checks 'bounded-reclamation-service-01/bounded-reclamation-service-result.json') '21ee791482d385521467673ad67630f7f6626ceb840c7adaf6ea61b7ce263a5b'
$sources=[ordered]@{
    'tools/Run-V5-Check.py'='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
    'software/v5/managed_storage/installed_controls.py'=$AdapterSourceSha256
    'software/v5/managed_operator/installed_lifecycle.py'='b64579269104b866e5ed45aeef121e799bcd8c505532913a5a5faf687c9c310e'
}
foreach ($relative in $sources.Keys) { $null=Pin (Join-Path $projectRoot $relative) $sources[$relative] }
$runtime=[ordered]@{}
function AddPin($row) {
    $actual=Pin $row.path $row.sha256
    if ($actual.bytes -ne $row.bytes) { throw 'PIN_EXTENT' }
    if ($runtime.Contains($actual.path) -and $runtime[$actual.path] -cne $actual.sha256) { throw 'PIN_CONFLICT' }
    $runtime[$actual.path]=$actual.sha256
}
foreach ($property in $release.sdk_sources.psobject.Properties) {
    $logical=$property.Name; $relative=$property.Value
    if ($relative -cne ('sdk/'+$logical) -or $relative.Contains('..') -or $relative.Contains('\')) { throw 'INSTALLED_LOGICAL_PATH' }
    $row=$release.files.$relative; $selected=$build.sdk_sources.$logical
    if ($null -eq $row -or $null -eq $selected -or $row.bytes -ne $selected.bytes -or $row.sha256 -cne $selected.sha256) { throw 'BUILD_INSTALL_SOURCE_BINDING' }
    AddPin ([ordered]@{path=(Join-Path $install $relative);bytes=$row.bytes;sha256=$row.sha256})
}
if ($runtime.Count -ne 129) { throw 'EXACT_INSTALLED_SDK' }
foreach ($relative in @('distribution.py','base/RELEASE-MANIFEST.json','base/operator/commons.py',
        'base/receiver/helpers/domains.py','base/receiver/helpers/run_stage.py','base/runtime/node/node.exe')) {
    $row=$release.files.$relative
    if ($null -eq $row) { throw ('REQUIRED_BASE_FILE:'+ $relative) }
    AddPin ([ordered]@{path=(Join-Path $install $relative);bytes=$row.bytes;sha256=$row.sha256})
}
# Relocate the adopted eighteen Python pins; no repeated large-payload sweep.
$oldPython=Join-Path $projectRoot 'product-local/v5-distribution-consolidated-01/Mathematical Commons v5/base/receiver/runtime/python'
$pythonRoot=Join-Path $install 'base/receiver/runtime/python'
$pythonCount=0
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    if ($property.Name.StartsWith($oldPython+'\',[StringComparison]::Ordinal)) {
        $suffix=$property.Name.Substring($oldPython.Length+1)
        $relative='base/receiver/runtime/python/'+$suffix.Replace('\','/')
        $row=$release.files.$relative
        if ($null -eq $row -or $row.sha256 -cne $property.Value) { throw 'UNCHANGED_INSTALLED_PYTHON' }
        AddPin ([ordered]@{path=(Join-Path $pythonRoot $suffix);bytes=$row.bytes;sha256=$row.sha256})
        $pythonCount++
    }
}
if ($pythonCount -ne 18 -or $runtime.Count -ne 153) { throw 'EXACT_RUNTIME_CLOSURE' }
foreach ($row in @($releasePin,$buildPin,$basisPin,$templatePin)) { AddPin $row }
$inputValue=[ordered]@{
    schema='DMKN_MANAGED_STORAGE_INSTALLED_INPUT_V1'
    installation_root=$install;release_sha256=$ReleaseSha256;template=$templatePin
}
SaveNew $inputPath $inputValue
$inputSha=(Get-FileHash -LiteralPath $inputPath -Algorithm SHA256).Hash.ToLowerInvariant()
$inputPin=Pin $inputPath $inputSha; AddPin $inputPin
if ($runtime.Count -ne 158 -or $sources.Count -ne 3) { throw 'EXACT_FINITE_SELECTION' }
$selected=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@((Join-Path $pythonRoot 'python.exe'),'-I','-S','-B','{snapshot}\software\v5\managed_storage\installed_controls.py',
        '--output','{output}','--input',$inputPath,'--input-sha',$inputSha)
    limits=[ordered]@{cpu_seconds=240;wall_seconds=600;memory_mib=768;active_processes=8;stdout_bytes=1048576;stderr_bytes=1048576}
}
SaveNew $selectionPath $selected
[ordered]@{input=$inputPin;selection_sha256=(Get-FileHash -LiteralPath $selectionPath -Algorithm SHA256).Hash.ToLowerInvariant();
    selection=$selectionPath;source_count=$sources.Count;runtime_pins=$runtime.Count;executed=$false} | ConvertTo-Json -Depth 6
