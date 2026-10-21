# Select the fresh registry controls only; no test/product import or execution here.
param([Parameter(Mandatory=$true)][string]$ReviewedSourcesJson)
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$name='bounded-generations-controls-01'
$selectionPath=Join-Path $checks ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_CONTROLS_REQUIRED:'+ $path) }
}
function Pin([string]$path,[string]$expected) {
    if ($expected -cnotmatch '^[0-9a-f]{64}$') { throw 'EXPECTED_SHA256' }
    $item=Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) { throw 'ORDINARY_FILE_REQUIRED' }
    $sha=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($sha -cne $expected) { throw ('REVIEWED_PIN_CHANGED:'+ $path) }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=$sha}
}
$install=Join-Path $projectRoot 'product-local\v5-distribution-consolidated-01\Mathematical Commons v5'
$releasePin=Pin (Join-Path $install 'V5-RELEASE.json') '1fd0ae63faa84cc1f3ef82f17d2056657f8d6a3e5dea3686ace433987bd1e5be'
$buildPin=Pin (Join-Path $checks 'distribution-consolidated-01-input.json') '8ba3707236c1a6e01ab7f87886814f801034b2fe9144ad9603585adcc73feb33'
$basisPin=Pin (Join-Path $checks 'consolidated-restart-smoke-02-selection.json') '04522d4b3fe8679c4d9a6af12c390b521f1ebe9135db6a2fdfe504776828d3ce'
$release=Get-Content -LiteralPath $releasePin.path -Raw -Encoding UTF8 | ConvertFrom-Json
$build=Get-Content -LiteralPath $buildPin.path -Raw -Encoding UTF8 | ConvertFrom-Json
$basis=Get-Content -LiteralPath $basisPin.path -Raw -Encoding UTF8 | ConvertFrom-Json
if ($release.schema -cne 'DMKN_V5_DIRECTORY_RELEASE_V3' -or $release.build_input_sha256 -cne $buildPin.sha256 -or
    @($release.sdk_sources.psobject.Properties).Count -ne 121 -or @($build.sdk_sources.psobject.Properties).Count -ne 121) { throw 'ADOPTED_SDK_MAP' }
$runtime=[ordered]@{}
foreach ($property in $release.sdk_sources.psobject.Properties) {
    $relative=$property.Value
    if ($relative -cne ('sdk/'+$property.Name) -or $relative.Contains('..')) { throw 'INSTALLED_LOGICAL_PATH' }
    $row=$release.files.$relative
    $selected=$build.sdk_sources.($property.Name)
    if ($null -eq $selected -or $row.bytes -ne $selected.bytes -or $row.sha256 -cne $selected.sha256) { throw 'BUILD_INSTALL_BINDING' }
    $actual=Pin (Join-Path $install $relative) $row.sha256
    if ($actual.bytes -ne $row.bytes -or $runtime.Contains($actual.path)) { throw 'SDK_EXTENT_OR_DUPLICATE' }
    $runtime[$actual.path]=$actual.sha256
}
if ($runtime.Count -ne 121) { throw 'EXACT_INSTALLED_SDK' }
$pythonRoot=Join-Path $install 'base\receiver\runtime\python'
$python=Join-Path $pythonRoot 'python.exe'
$pythonCount=0
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    if ($property.Name.StartsWith($pythonRoot+'\',[StringComparison]::Ordinal)) {
        $actual=Pin $property.Name $property.Value
        $runtime[$actual.path]=$actual.sha256
        $pythonCount++
    }
}
if ($pythonCount -ne 18 -or -not $runtime.Contains($python)) { throw 'EXACT_INSTALLED_PYTHON' }
foreach ($row in @($releasePin,$buildPin,$basisPin)) { $runtime[$row.path]=$row.sha256 }
if ($runtime.Count -ne 142) { throw 'EXACT_RUNTIME_PIN_COUNT' }
$required=@('placement/lifecycle.py','client/serve_generations.py','tests.py')
if ($ReviewedSourcesJson.Length -gt 16384) { throw 'REVIEWED_MAP_BOUND' }
$reviewed=$ReviewedSourcesJson | ConvertFrom-Json
$keys=@($reviewed.psobject.Properties.Name)
if ($keys.Count -ne 3 -or @(Compare-Object $keys $required -CaseSensitive).Count -ne 0) { throw 'EXACT_REVIEWED_SOURCES' }
$sources=[ordered]@{'tools/Run-V5-Check.py'='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'}
$null=Pin (Join-Path $projectRoot 'tools/Run-V5-Check.py') $sources['tools/Run-V5-Check.py']
foreach ($key in $required) {
    $relative='software/v5/bounded_generations/'+$key
    $null=Pin (Join-Path $projectRoot $relative) $reviewed.$key
    $sources[$relative]=$reviewed.$key
}
$selected=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($python,'-I','-S','-B','{snapshot}\software\v5\bounded_generations\tests.py',
        '--output','{output}','--release-sha',$releasePin.sha256)
    limits=[ordered]@{cpu_seconds=60;wall_seconds=120;memory_mib=384;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 16)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_JSON_BOUND' }
$stream=[IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{path=$selectionPath;sha256=(Get-FileHash -LiteralPath $selectionPath -Algorithm SHA256).Hash.ToLowerInvariant();
    source_count=$sources.Count;runtime_pins=$runtime.Count;executed=$false} | ConvertTo-Json
