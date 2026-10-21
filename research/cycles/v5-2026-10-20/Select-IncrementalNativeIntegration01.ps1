# Stage one genuine warm-prefix check, without executing it or copying a distribution.
param([Parameter(Mandatory=$true)][string]$ReviewedIntegrationSha256)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Require-Digest([string]$path, [string]$expected) {
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or (Digest $path) -cne $expected) {
        throw ('REVIEWED_INPUT_CHANGED: '+$path)
    }
}
function Row([string]$path, [string]$expected) {
    Require-Digest $path $expected
    return [ordered]@{path=$path;bytes=(Get-Item -LiteralPath $path).Length;sha256=$expected}
}
function New-Json([string]$path, $value) {
    $raw = [Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 32)+"`n")
    if ($raw.Length -gt 1048576) { throw 'JSON_BOUND' }
    $stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) }
    finally { $stream.Dispose() }
}
$checks = Join-Path $projectRoot 'experiments/v5-local-checks'
$mapPath = Join-Path $checks 'distribution-terminal-i-01-input.json'
$mapRow = Row $mapPath 'd3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0'
$map = Get-Content -LiteralPath $mapPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($map.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or @($map.sdk_sources.psobject.Properties).Count -ne 114) { throw 'SDK_BASIS' }
$sources = [ordered]@{}
$runnerKey = 'tools/Run-V5-Check.py'
$runnerSha = '44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
Require-Digest (Join-Path $projectRoot $runnerKey) $runnerSha
$sources[$runnerKey] = $runnerSha
foreach ($property in $map.sdk_sources.psobject.Properties) {
    $entry = $property.Value
    $path = [IO.Path]::GetFullPath($entry.path)
    if (-not $path.StartsWith($projectRoot+'\software\v5\',[StringComparison]::Ordinal)) { throw 'SDK_SOURCE_SCOPE' }
    Require-Digest $path $entry.sha256
    if ((Get-Item -LiteralPath $path).Length -ne $entry.bytes) { throw 'SDK_SOURCE_SIZE' }
    $relative = $path.Substring($projectRoot.Length+1).Replace('\','/')
    if ($sources.Contains($relative)) { throw 'DUPLICATE_SOURCE' }
    $sources[$relative] = $entry.sha256
}
$successors = [ordered]@{
    'software/v5/standalone_validation/admission/pin_phase.py'='ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881'
    'software/v5/standalone_validation/mixed_claims/imports_atomic.py'='8a8313376d736f25a45b6089f491373bc7e0206aa77b539dbff077fc4eb92595'
    'software/v5/incremental_native/mixed_claims/receiver.py'='5436569971c272b129fbaec480d51d57a1ec521d43fd4d4ad14133b786691d5b'
    'software/v5/incremental_native/integration.py'=$ReviewedIntegrationSha256
}
foreach ($key in $successors.Keys) {
    if ($sources.Contains($key)) { throw 'SUCCESSOR_COLLISION' }
    Require-Digest (Join-Path $projectRoot $key) $successors[$key]
    $sources[$key] = $successors[$key]
}
if ($sources.Count -ne 119) { throw 'EXACT_SOURCE_COUNT' }
$basisPath = Join-Path $checks 'terminal-i-controls-01-selection.json'
Require-Digest $basisPath 'b43f3eb450219760ae80a91e29b316743b9a517b34c99d688129c067877037ec'
$basis = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
$python = $basis.argv[0]
$pythonRoot = [IO.Path]::GetDirectoryName($python)
$runtime = [ordered]@{}
$pythonRows = @()
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    if ($property.Name.StartsWith($pythonRoot+'\',[StringComparison]::Ordinal)) {
        $pythonRows += ,(Row $property.Name $property.Value)
        $runtime[$property.Name] = $property.Value
    }
}
if ($runtime.Count -ne 18 -or -not $runtime.Contains($python)) { throw 'PYTHON_CLOSURE' }
$runtime[$mapPath] = $mapRow.sha256
$installation = Join-Path $projectRoot 'product-local/v5-distribution-terminal-i-01/Mathematical Commons v5'
$assets = [ordered]@{
    'base/RELEASE-MANIFEST.json'='a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed'
    'assets/native/native_delta.exe'='37a0af1b08e7176fb0d387b3e8439266d7c2c0befe5b08bc3cdd4c90c62d3e40'
    'assets/receipt/module_host.exe'='74a58215351a641d9efbbffbc389b5faea350c46f5c1e1a48bf76cf77b99d6c9'
    'base/operator/commons.py'='6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9'
    'base/receiver/helpers/domains.py'='651db5f6bb707159c0d29dd6092174bfcebd1dc17b833fdfdacf7e2a66d8522a'
    'base/receiver/helpers/run_stage.py'='bdd2cbc28258f49ef08b678ba54b437ff541ef4deb0af4aa36795d2baa19b028'
}
$assetRows = [ordered]@{}
foreach ($key in $assets.Keys) {
    $path = Join-Path $installation $key
    $assetRows[$key] = Row $path $assets[$key]
    $runtime[$path] = $assets[$key]
}
$operation = Join-Path $projectRoot 'product-local/v5-distribution-origin-01/mirror-method03-first/operations/47cbc7c244193477517c609adbfd0b72e163dc57958848d4f9e6f8149dd6fe16'
$packets = @(
    (Row (Join-Path $operation 'delta/1/packet.json') 'efc96de9cafea117baad14cfd160f42c2a3ad41bf9cb4e6a2dc18a7dad3ffc1b'),
    (Row (Join-Path $operation 'delta/2/packet.json') '30566df7734d2d0d407cc553b923617453a3162c68a36afafe9a970eb4eb8dfc')
)
foreach ($entry in $packets) { $runtime[$entry.path] = $entry.sha256 }
if ($runtime.Count -ne 27) { throw 'EXACT_PREINPUT_RUNTIME_COUNT' }
$name = 'incremental-native-integration-01'
$inputPath = Join-Path $checks ($name+'-input.json')
$selectionPath = Join-Path $checks ($name+'-selection.json')
foreach ($path in @($inputPath,$selectionPath,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_SELECTION_REQUIRED: '+$path) }
}
$inputValue = [ordered]@{
    schema='DMKN_INCREMENTAL_NATIVE_INTEGRATION_INPUT_V1';map=$mapRow;installation=$installation
    supervisor_manifest=$assetRows['base/RELEASE-MANIFEST.json']
    native=$assetRows['assets/native/native_delta.exe'];receipt=$assetRows['assets/receipt/module_host.exe']
    python_runtime=$pythonRows;packets=$packets
}
New-Json $inputPath $inputValue
$inputSha = Digest $inputPath
$runtime[$inputPath] = $inputSha
$selection = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($python,'-I','-S','-B','{snapshot}\software\v5\incremental_native\integration.py','--output','{output}','--input',$inputPath)
    limits=[ordered]@{cpu_seconds=90;wall_seconds=180;memory_mib=512;active_processes=4;stdout_bytes=1048576;stderr_bytes=1048576}
}
New-Json $selectionPath $selection
[ordered]@{input=$inputPath;input_sha256=$inputSha;selection=$selectionPath;selection_sha256=(Digest $selectionPath);
    sources=$sources.Count;runtime_pins=$runtime.Count;executed=$false} | ConvertTo-Json
