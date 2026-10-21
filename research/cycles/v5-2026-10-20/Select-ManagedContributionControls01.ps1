# Preparation only. Root separately adopts reviews and selects one finite run.
param([Parameter(Mandatory=$true)][string]$ReviewedSourcesJson)
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$name='managed-contribution-controls-01'
$selectionPath=Join-Path $checks ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $checks ($name+'-input.json')),(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_CREDENTIAL_CONTROLS_REQUIRED:'+ $path) }
}
function Pin([string]$path,[string]$expected) {
    if ($expected -cnotmatch '^[0-9a-f]{64}$') { throw 'EXPECTED_SHA256' }
    $item=Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) { throw 'ORDINARY_FILE_REQUIRED' }
    $sha=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($sha -cne $expected) { throw ('REVIEWED_PIN_CHANGED:'+ $path) }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=$sha}
}
function AddPin($row) {
    $actual=Pin $row.path $row.sha256
    if ($actual.bytes -ne $row.bytes -or $runtime.Contains($actual.path)) { throw 'RUNTIME_EXTENT_OR_DUPLICATE' }
    $runtime[$actual.path]=$actual.sha256
}
function SaveNew([string]$path,$value) {
    $raw=[Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 32)+"`n")
    if ($raw.Length -gt 1048576) { throw 'SELECTION_SIZE' }
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
}
$install=Join-Path $projectRoot 'product-local\v5-distribution-managed-owner-01\Mathematical Commons v5'
$releasePin=Pin (Join-Path $install 'V5-RELEASE.json') '8fcf2c971029c8ad0787ec8da0891be178a95b80999f8bccc262e077009701a2'
$buildPin=Pin (Join-Path $checks 'distribution-managed-owner-01-input.json') '4a9bfd78afd328d629ee6ad967f7f9378034db86cdee86bef751c5c50e6778a1'
# Adopted lifecycle selection supplies only its eighteen exact Python rows.
# Node/service/other prior fixture inputs are deliberately not selected here.
$basisPin=Pin (Join-Path $checks 'managed-operator-lifecycle-01-selection.json') 'aac5291b234e237e19f75e934fbb8ecf39971027743b85c206035f2f837b4007'
$release=Get-Content -LiteralPath $releasePin.path -Raw -Encoding UTF8 | ConvertFrom-Json
$build=Get-Content -LiteralPath $buildPin.path -Raw -Encoding UTF8 | ConvertFrom-Json
$basis=Get-Content -LiteralPath $basisPin.path -Raw -Encoding UTF8 | ConvertFrom-Json
if ($release.schema -cne 'DMKN_V5_DIRECTORY_RELEASE_V3' -or $release.base_role -cne 'mathematical-client-location-v1' -or
    $release.build_input_sha256 -cne $buildPin.sha256 -or $build.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or
    @($release.sdk_sources.psobject.Properties).Count -ne 126 -or @($build.sdk_sources.psobject.Properties).Count -ne 126) { throw 'ADOPTED_126_SDK_MAP' }
$runtime=[ordered]@{}
foreach ($property in $release.sdk_sources.psobject.Properties) {
    $logical=$property.Name; $relative=$property.Value
    if ($relative -cne ('sdk/'+$logical) -or $relative.Contains('..') -or $relative.Contains('\')) { throw 'INSTALLED_LOGICAL_PATH' }
    $row=$release.files.$relative; $selected=$build.sdk_sources.$logical
    if ($null -eq $row -or $null -eq $selected -or $row.bytes -ne $selected.bytes -or $row.sha256 -cne $selected.sha256) { throw 'BUILD_INSTALL_SOURCE_BINDING' }
    AddPin ([ordered]@{path=(Join-Path $install $relative);bytes=$row.bytes;sha256=$row.sha256})
}
if ($runtime.Count -ne 126) { throw 'EXACT_INSTALLED_SDK' }
$pythonRoot=Join-Path $install 'base\receiver\runtime\python'
$python=Join-Path $pythonRoot 'python.exe'
$pythonCount=0
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    if ($property.Name.StartsWith($pythonRoot+'\',[StringComparison]::Ordinal)) {
        $suffix=$property.Name.Substring($pythonRoot.Length+1)
        $relative='base/receiver/runtime/python/'+$suffix.Replace('\','/')
        $row=$release.files.$relative
        if ($null -eq $row -or $row.sha256 -cne $property.Value) { throw 'ADOPTED_PYTHON_BINDING' }
        AddPin ([ordered]@{path=$property.Name;bytes=$row.bytes;sha256=$row.sha256})
        $pythonCount++
    }
}
if ($pythonCount -ne 18 -or $runtime.Count -ne 144 -or -not $runtime.Contains($python)) { throw 'EXACT_INSTALLED_PYTHON' }
foreach ($row in @($releasePin,$buildPin,$basisPin)) { AddPin $row }
if ($runtime.Count -ne 147) { throw 'EXACT_RUNTIME_COUNT' }
$required=@('credential_controls.py','client/private_credentials.py')
if ($ReviewedSourcesJson.Length -gt 16384) { throw 'REVIEWED_MAP_BOUND' }
$reviewed=$ReviewedSourcesJson | ConvertFrom-Json
$keys=@($reviewed.psobject.Properties.Name)
if ($keys.Count -ne 2 -or @(Compare-Object $keys $required -CaseSensitive).Count -ne 0) { throw 'EXACT_REVIEWED_SOURCES' }
$sources=[ordered]@{'tools/Run-V5-Check.py'='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'}
$null=Pin (Join-Path $projectRoot 'tools/Run-V5-Check.py') $sources['tools/Run-V5-Check.py']
foreach ($key in $required) {
    $relative='software/v5/managed_contribution/'+$key
    $row=Pin (Join-Path $projectRoot $relative) $reviewed.$key
    $sources[$relative]=$row.sha256
    if ($key -ceq 'client/private_credentials.py' -and ($row.bytes -ne 12374 -or
        $row.sha256 -cne '7116e2d9161cbb828203bc7eff1e7dd90c1cab7d6e860a6e16801ffb6ecb37f0')) { throw 'CONTROL_EMBEDDED_HELPER_PIN' }
}
if ($sources.Count -ne 3) { throw 'EXACT_SOURCE_COUNT' }
$selected=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($python,'-I','-S','-B','{snapshot}\software\v5\managed_contribution\credential_controls.py',
        '--output','{output}','--release-sha',$releasePin.sha256)
    limits=[ordered]@{cpu_seconds=30;wall_seconds=60;memory_mib=256;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
SaveNew $selectionPath $selected
[ordered]@{path=$selectionPath;sha256=(Get-FileHash -LiteralPath $selectionPath -Algorithm SHA256).Hash.ToLowerInvariant();
    source_count=$sources.Count;runtime_pins=$runtime.Count;executed=$false} | ConvertTo-Json
