# Select one file-only optional-role installation; no build or runtime invocation.
param()
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) {
    (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Require-Digest([string]$path, [string]$expected) {
    if ((Digest $path) -cne $expected) { throw ('REVIEWED_INPUT_CHANGED: '+$path) }
}
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$inputPath = Join-Path $checks 'distribution-connected-01-input.json'
$inputSha = '557269158f76933177eae962cb97c2862a8512709dbee9842051649552573309'
Require-Digest $inputPath $inputSha
$inputValue = Get-Content -LiteralPath $inputPath -Raw | ConvertFrom-Json
$sourceKey = 'software/v5/distribution_connected/distribution.py'
$sourceSha = '8e34df2a98fc3bf017f3d57ea2f92211bbcf156ee801479cbfaf9261f76763a6'
if ($inputValue.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or
    $inputValue.base_role -cne 'mathematical-client-location-v1' -or
    $inputValue.distribution_source.path -cne (Join-Path $projectRoot $sourceKey) -or
    $inputValue.distribution_source.sha256 -cne $sourceSha) {
    throw 'EXACT_CONNECTED_INPUT'
}
$basisPath = Join-Path $checks 'connected-distribution-controls-01-selection.json'
Require-Digest $basisPath '544cf07e5dffb4b3f98b560ecf692ad785f0f8b07ec454f724385949c57b85da'
$basis = Get-Content -LiteralPath $basisPath -Raw | ConvertFrom-Json
$sources = [ordered]@{
    'tools/Run-V5-Check.py' = '44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
}
$sources[$sourceKey] = $sourceSha
foreach ($key in $sources.Keys) {
    Require-Digest (Join-Path $projectRoot $key) $sources[$key]
}
$runtime = [ordered]@{}
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    Require-Digest $property.Name $property.Value
    $runtime[$property.Name] = $property.Value
}
$runtime[$inputPath] = $inputSha
$parent = Join-Path $projectRoot 'product-local\v5-distribution-connected-01'
$destination = Join-Path $parent 'Mathematical Commons v5'
$name = 'distribution-connected-build-01'
$selectionPath = Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $parent) -or (Test-Path -LiteralPath $selectionPath) -or
    (Test-Path -LiteralPath (Join-Path $checks $name))) { throw 'FRESH_BUILD_REQUIRED' }
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1'; name=$name; sources=$sources; runtime_pins=$runtime
    argv=@($basis.argv[0], '-I', '-S', '-B',
        '{snapshot}\software\v5\distribution_connected\distribution.py',
        'build', $inputPath, $inputSha, $destination)
    limits=[ordered]@{
        cpu_seconds=120; wall_seconds=300; memory_mib=128; active_processes=2
        stdout_bytes=1048576; stderr_bytes=1048576
    }
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 16)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_JSON_BOUND' }
$stream = [IO.File]::Open($selectionPath, [IO.FileMode]::CreateNew,
    [IO.FileAccess]::Write, [IO.FileShare]::None)
try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
[ordered]@{path=$selectionPath; sha256=(Digest $selectionPath)
    sources=$sources.Count; runtime_pins=$runtime.Count
    installation_parent=$parent; parent_created=$false; executed=$false} | ConvertTo-Json
