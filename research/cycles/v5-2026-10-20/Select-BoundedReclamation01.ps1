# Preparation only. Each mode has its own fresh allocation and root launch decision.
param(
    [Parameter(Mandatory=$true)][ValidateSet('Controls','Service')][string]$Mode,
    [Parameter(Mandatory=$true)][string]$ReviewedSourcesJson
)
$ErrorActionPreference='Stop'
if ($Mode -cnotin @('Controls','Service')) { throw 'EXACT_MODE_REQUIRED' }
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$name=if ($Mode -ceq 'Controls') {'bounded-reclamation-controls-01'} else {'bounded-reclamation-service-01'}
$selectionPath=Join-Path $checks ($name+'-selection.json')
$inputPath=Join-Path $checks ($name+'-input.json')
foreach ($path in @($selectionPath,$inputPath,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_RECLAMATION_REQUIRED:'+ $path) }
}
function Pin([string]$path,[string]$expected) {
    if ($expected -cnotmatch '^[0-9a-f]{64}$') { throw 'EXPECTED_SHA256' }
    $item=Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) { throw 'ORDINARY_FILE_REQUIRED' }
    $sha=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($sha -cne $expected) { throw ('REVIEWED_PIN_CHANGED:'+ $path) }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=$sha}
}
function SaveNew([string]$path,$value) {
    $raw=[Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 32)+"`n")
    if ($raw.Length -gt 1048576) { throw 'SELECTION_SIZE' }
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
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
    $row=$release.files.$relative; $selected=$build.sdk_sources.($property.Name)
    if ($null -eq $selected -or $row.bytes -ne $selected.bytes -or $row.sha256 -cne $selected.sha256) { throw 'BUILD_INSTALL_BINDING' }
    $actual=Pin (Join-Path $install $relative) $row.sha256
    if ($actual.bytes -ne $row.bytes -or $runtime.Contains($actual.path)) { throw 'SDK_EXTENT_OR_DUPLICATE' }
    $runtime[$actual.path]=$actual.sha256
}
if ($runtime.Count -ne 121) { throw 'EXACT_INSTALLED_SDK' }
$pythonRoot=Join-Path $install 'base\receiver\runtime\python'; $python=Join-Path $pythonRoot 'python.exe'
$pythonCount=0
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    if ($property.Name.StartsWith($pythonRoot+'\',[StringComparison]::Ordinal)) {
        $actual=Pin $property.Name $property.Value; $runtime[$actual.path]=$actual.sha256; $pythonCount++
    }
}
if ($pythonCount -ne 18 -or -not $runtime.Contains($python)) { throw 'EXACT_INSTALLED_PYTHON' }
foreach ($row in @($releasePin,$buildPin,$basisPin)) { $runtime[$row.path]=$row.sha256 }
if ($runtime.Count -ne 142) { throw 'EXACT_COMMON_RUNTIME_COUNT' }
$required=@('placement/lifecycle.py','placement/reclaim.py')
if ($Mode -ceq 'Controls') {$required+=@('tests.py')} else {$required+=@('service_smoke.py','client/serve_generations.py')}
if ($ReviewedSourcesJson.Length -gt 16384) { throw 'REVIEWED_MAP_BOUND' }
$reviewed=$ReviewedSourcesJson | ConvertFrom-Json; $keys=@($reviewed.psobject.Properties.Name)
if ($keys.Count -ne $required.Count -or @(Compare-Object $keys $required -CaseSensitive).Count -ne 0) { throw 'EXACT_REVIEWED_SOURCES' }
$sources=[ordered]@{'tools/Run-V5-Check.py'='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'}
$null=Pin (Join-Path $projectRoot 'tools/Run-V5-Check.py') $sources['tools/Run-V5-Check.py']
$additions=[ordered]@{}
foreach ($key in $required) {
    $relative=if ($key -ceq 'client/serve_generations.py') {'software/v5/bounded_generations/'+$key} else {'software/v5/bounded_reclamation/'+$key}
    $row=Pin (Join-Path $projectRoot $relative) $reviewed.$key; $sources[$relative]=$reviewed.$key
    if ($key -notin @('tests.py','service_smoke.py')) {$additions['v5/'+$key]=[ordered]@{bytes=$row.bytes;sha256=$row.sha256}}
}
if ($Mode -ceq 'Controls') {
    $argv=@($python,'-I','-S','-B','{snapshot}\software\v5\bounded_reclamation\tests.py','--output','{output}','--release-sha',$releasePin.sha256)
    $limits=[ordered]@{cpu_seconds=30;wall_seconds=60;memory_mib=256;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
} else {
    $configPin=Pin (Join-Path $checks 'placement-network-integration-02-input.json') '6e14ba3b8abbce616a8115b7ce3a229242869a3b8861c427c52e3221a2f47f58'
    $runtime[$configPin.path]=$configPin.sha256
    $row=$release.files.'base/RELEASE-MANIFEST.json'
    $basePin=Pin (Join-Path $install 'base/RELEASE-MANIFEST.json') $row.sha256
    if ($basePin.bytes -ne $row.bytes) { throw 'BASE_MANIFEST_EXTENT' }
    $runtime[$basePin.path]=$basePin.sha256
    # The existing AdoptedLocationRuntime performs its exact Node/overlay pre/post validation.
    # No certificate/proof fixtures from the config basis are opened or selected.
    SaveNew $inputPath ([ordered]@{schema='DMKN_BOUNDED_RECLAMATION_SERVICE_INPUT_V1';additions=$additions})
    $inputSha=(Get-FileHash -LiteralPath $inputPath -Algorithm SHA256).Hash.ToLowerInvariant()
    $runtime[$inputPath]=$inputSha
    if ($runtime.Count -ne 145) { throw 'EXACT_SERVICE_RUNTIME_COUNT' }
    $argv=@($python,'-I','-S','-B','{snapshot}\software\v5\bounded_reclamation\service_smoke.py',
        '--output','{output}','--input',$inputPath,'--input-sha',$inputSha)
    $limits=[ordered]@{cpu_seconds=90;wall_seconds=200;memory_mib=512;active_processes=4;stdout_bytes=1048576;stderr_bytes=1048576}
}
SaveNew $selectionPath ([ordered]@{schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime;argv=$argv;limits=$limits})
[ordered]@{path=$selectionPath;sha256=(Get-FileHash -LiteralPath $selectionPath -Algorithm SHA256).Hash.ToLowerInvariant();
    source_count=$sources.Count;runtime_pins=$runtime.Count;executed=$false} | ConvertTo-Json
