# Stage reviewed changed-boundary controls only; does not execute any source.
param([Parameter(Mandatory=$true)][string]$ReviewedSourcesJson)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Require-Digest([string]$path, [string]$expected) {
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or (Digest $path) -cne $expected) {
        throw ('REVIEWED_INPUT_CHANGED: '+$path)
    }
}
$checks = Join-Path $projectRoot 'experiments/v5-local-checks'
$basisPath = Join-Path $checks 'base-projection-controls-02-selection.json'
Require-Digest $basisPath '92cad921f57e1f5ca6e93e0954198619ba8f75ed8ad0288dd2dd4e4b32d2a542'
$basis = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_LOCAL_CHECK_V1' -or $basis.name -cne 'base-projection-controls-02') { throw 'BASIS_SCHEMA' }
$sources = [ordered]@{}
foreach ($property in $basis.sources.psobject.Properties) {
    Require-Digest (Join-Path $projectRoot $property.Name) $property.Value
    $sources[$property.Name] = $property.Value
}
if ($sources.Count -ne 154) { throw 'BASIS_SOURCE_COUNT' }
$mapPath = Join-Path $checks 'distribution-projection-01-input.json'
$mapSha = 'ad2c15a27a51f749104ac09f9cafee210a108fb0bf46bafad8b2a9542f86d38f'
Require-Digest $mapPath $mapSha
$map = Get-Content -LiteralPath $mapPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($map.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or @($map.sdk_sources.psobject.Properties).Count -ne 113) { throw 'SDK_BASIS' }
foreach ($property in $map.sdk_sources.psobject.Properties) {
    $row = $property.Value
    $path = [IO.Path]::GetFullPath($row.path)
    if (-not $path.StartsWith($projectRoot+'\software\v5\', [StringComparison]::Ordinal)) { throw 'SDK_SOURCE_SCOPE' }
    Require-Digest $path $row.sha256
    if ((Get-Item -LiteralPath $path).Length -ne $row.bytes) { throw 'SDK_SOURCE_SIZE' }
    $relative = $path.Substring($projectRoot.Length+1).Replace('\','/')
    if ($sources.Contains($relative) -and $sources[$relative] -cne $row.sha256) { throw 'SDK_SOURCE_CONFLICT' }
    $sources[$relative] = $row.sha256
}
$required = @(
    'portable/location/protocol.py', 'portable/location/protocol.mjs',
    'portable/location/intent.mjs', 'portable/location/maintained_roles.mjs',
    'portable/location/ipc_wire.mjs', 'portable/location/node_entry_services.mjs',
    'portable/location/controller_services.py',
    'client/body_custody.py', 'client/workspace_evidence.py', 'client/semantic_reader.py',
    'client/serve_advertised.py', 'transport/acquisition_resilience.py',
    'distribution.py', 'tests/controls01.py', 'tests/controls01.mjs')
if ($ReviewedSourcesJson.Length -gt 16384) { throw 'REVIEWED_MAP_BOUND' }
$reviewed = $ReviewedSourcesJson | ConvertFrom-Json
$keys = @($reviewed.psobject.Properties.Name)
if ($keys.Count -ne $required.Count -or @(Compare-Object $keys $required -CaseSensitive).Count -ne 0) {
    throw 'EXACT_REVIEWED_SOURCE_SET'
}
foreach ($key in $required) {
    $relative = 'software/v5/body_location/'+$key
    if ($sources.Contains($relative)) { throw 'FRESH_SUCCESSOR_REQUIRED' }
    Require-Digest (Join-Path $projectRoot $relative) $reviewed.$key
    $sources[$relative] = $reviewed.$key
}
$runtime = [ordered]@{}
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    Require-Digest $property.Name $property.Value
    $runtime[$property.Name] = $property.Value
}
$runtime[$mapPath] = $mapSha
$node = Join-Path $projectRoot 'product-local/v4-library-commons-02/commons-v4/runtime/node/node.exe'
$nodeSha = 'b3094d0b49f9ad602262a9921551737bb97637c05dd357a06ae98188d7290aa3'
Require-Digest $node $nodeSha
$runtime[$node] = $nodeSha
$name = 'exact-custody-controls-01'
$selectionPath = Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath (Join-Path $checks $name))) { throw 'FRESH_SELECTION_REQUIRED' }
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1'; name=$name; sources=$sources; runtime_pins=$runtime
    argv=@($basis.argv[0], '-I', '-S', '-B', '{snapshot}\software\v5\body_location\tests\controls01.py', '--output', '{output}')
    limits=[ordered]@{cpu_seconds=45;wall_seconds=90;memory_mib=384;active_processes=3;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 16)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_JSON_BOUND' }
$stream = [IO.File]::Open($selectionPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
[ordered]@{path=$selectionPath;sha256=(Digest $selectionPath);sources=$sources.Count;
    runtime_pins=$runtime.Count;executed=$false} | ConvertTo-Json
