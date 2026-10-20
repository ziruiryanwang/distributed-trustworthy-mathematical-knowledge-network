# Prepare only one real location-to-HTTP composition; no process launch.
param([Parameter(Mandatory=$true)][string]$ExpectedAdapterSha)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) {
    (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Require-Digest([string]$path, [string]$expected) {
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or (Digest $path) -cne $expected) {
        throw ('REVIEWED_INPUT_CHANGED: ' + $path)
    }
}
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$basisPath = Join-Path $checks 'advertised-service-controls-01-selection.json'
Require-Digest $basisPath 'e450cbe5590f28e5b857d50eb3c48fa71488f1b1742070e59f7f62946010c3fc'
$basis = Get-Content -LiteralPath $basisPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($property in $basis.sources.psobject.Properties) {
    Require-Digest (Join-Path $projectRoot $property.Name) $property.Value
    $sources[$property.Name] = $property.Value
}
$relative = 'software/v5/client/advertised_service_check.py'
if ($sources.Contains($relative)) { throw 'ADAPTER_SOURCE_COLLISION' }
Require-Digest (Join-Path $projectRoot $relative) $ExpectedAdapterSha
$sources[$relative] = $ExpectedAdapterSha
$runtime = [ordered]@{}
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    Require-Digest $property.Name $property.Value
    $runtime[$property.Name] = $property.Value
}
$baseRoot = Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4'
$manifestPath = Join-Path $baseRoot 'RELEASE-MANIFEST.json'
Require-Digest $manifestPath 'a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed'
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
$nodePath = Join-Path $baseRoot 'runtime\node\node.exe'
$nodeSha = $manifest.files.'runtime/node/node.exe'.sha256
Require-Digest $nodePath $nodeSha
$runtime[$nodePath] = $nodeSha
$runtime[$manifestPath] = 'a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed'
# Exact overlay census and all role hashes remain the adopted controller's
# pre/post obligation; there is no unverified alternative runtime.
$name = 'advertised-service-actual-01'
$selectionPath = Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath (Join-Path $checks $name))) {
    throw 'FRESH_SELECTION_REQUIRED'
}
$selected = [ordered]@{
    schema = 'DMKN_V5_LOCAL_CHECK_V1'
    name = $name
    sources = $sources
    runtime_pins = $runtime
    argv = @($basis.argv[0], '-I', '-S', '-B',
        '{snapshot}\software\v5\client\advertised_service_check.py', '--output', '{output}\actual')
    limits = [ordered]@{
        cpu_seconds=45; wall_seconds=120; memory_mib=512; active_processes=4
        stdout_bytes=1048576; stderr_bytes=1048576
    }
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 16)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_JSON_BOUND' }
$stream = [IO.File]::Open($selectionPath, [IO.FileMode]::CreateNew,
    [IO.FileAccess]::Write, [IO.FileShare]::None)
try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
[ordered]@{
    path=$selectionPath; sha256=(Digest $selectionPath)
    sources=$sources.Count; runtime_pins=$runtime.Count; executed=$false
} | ConvertTo-Json
