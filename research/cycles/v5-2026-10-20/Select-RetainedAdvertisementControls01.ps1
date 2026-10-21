# Prepare nine retained-advertisement controls; never execute them here.
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
$mapPath = Join-Path $checks 'distribution-terminal-i-01-input.json'
$mapSha = 'd3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0'
Require-Digest $mapPath $mapSha
$map = Get-Content -LiteralPath $mapPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($map.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or @($map.sdk_sources.psobject.Properties).Count -ne 114) { throw 'SDK_BASIS' }
$sources = [ordered]@{}
$runner = 'tools/Run-V5-Check.py'
$runnerSha = '44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
Require-Digest (Join-Path $projectRoot $runner) $runnerSha
$sources[$runner] = $runnerSha
foreach ($property in $map.sdk_sources.psobject.Properties) {
    $entry = $property.Value
    $path = [IO.Path]::GetFullPath($entry.path)
    if (-not $path.StartsWith($projectRoot+'\software\v5\',[StringComparison]::Ordinal)) { throw 'SDK_SOURCE_SCOPE' }
    Require-Digest $path $entry.sha256
    if ((Get-Item -LiteralPath $path).Length -ne $entry.bytes) { throw 'SDK_SOURCE_SIZE' }
    $relative = $path.Substring($projectRoot.Length+1).Replace('\','/')
    if ($sources.Contains($relative)) { throw 'DUPLICATE_PHYSICAL_SOURCE' }
    $sources[$relative] = $entry.sha256
}
# Preserve original physical closure while replacing four logical modules.
$qualified = [ordered]@{
    'software/v5/standalone_validation/admission/pin_phase.py'='ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881'
    'software/v5/standalone_validation/mixed_claims/imports_atomic.py'='8a8313376d736f25a45b6089f491373bc7e0206aa77b539dbff077fc4eb92595'
    'software/v5/incremental_native/mixed_claims/receiver.py'='5436569971c272b129fbaec480d51d57a1ec521d43fd4d4ad14133b786691d5b'
    'software/v5/selective_placement/discovery/discovery_store.py'='1c8543d4903754174b80d107ee923116ddb402d41a3b5af3f1d255abdfc6a328'
}
foreach ($relative in $qualified.Keys) {
    if ($sources.Contains($relative)) { throw 'QUALIFIED_SOURCE_COLLISION' }
    Require-Digest (Join-Path $projectRoot $relative) $qualified[$relative]
    $sources[$relative] = $qualified[$relative]
}
# Existing core/wire source only; do not import or repeat predecessor tests.
$frozen = [ordered]@{
    'software/v5/selective_placement/placement/__init__.py'='8fe08470d7fd15e96d1305f0e49a8b359cb53ce0c542bf7473b68d869159112e'
    'software/v5/selective_placement/placement/codec.py'='6f32569d4807f96130350b85233161603f6860f082c75f81a8bfacf4f0a58999'
    'software/v5/selective_placement/placement/ledger.py'='d955990c347ed466617c752893dded8b8494dd266a050b045352c77c48f21a91'
    'software/v5/selective_placement/placement/controller.py'='ef1c9b59072127379e955bafeea001a22d6e3d10c9c46dca1304f85ab09e2b49'
    'software/v5/placement_network/placement/network.py'='1ec5c452ec129ae033f0577ebac6223e2cf3192d4724a3d31fe2e5c27a06cd4b'
}
foreach ($relative in $frozen.Keys) {
    if ($sources.Contains($relative)) { throw 'FROZEN_SOURCE_COLLISION' }
    Require-Digest (Join-Path $projectRoot $relative) $frozen[$relative]
    $sources[$relative] = $frozen[$relative]
}
$required = @('placement/advertisement.py','client/serve_placement.py','controls.py')
if ($ReviewedSourcesJson.Length -gt 16384) { throw 'REVIEWED_MAP_BOUND' }
$reviewed = $ReviewedSourcesJson | ConvertFrom-Json
$keys = @($reviewed.psobject.Properties.Name)
if ($keys.Count -ne 3 -or @(Compare-Object $keys $required -CaseSensitive).Count -ne 0) { throw 'EXACT_REVIEWED_SOURCE_SET' }
foreach ($key in $required) {
    $relative = 'software/v5/retained_advertisement/'+$key
    if ($sources.Contains($relative)) { throw 'FRESH_SOURCE_REQUIRED' }
    Require-Digest (Join-Path $projectRoot $relative) $reviewed.$key
    $sources[$relative] = $reviewed.$key
}
# 114 predecessor files + four replacements + seven additions + runner + controls.
if ($sources.Count -ne 127) { throw 'EXACT_SOURCE_COUNT' }
$basisPath = Join-Path $checks 'terminal-i-controls-01-selection.json'
Require-Digest $basisPath 'b43f3eb450219760ae80a91e29b316743b9a517b34c99d688129c067877037ec'
$basis = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
$python = $basis.argv[0]
$pythonRoot = [IO.Path]::GetDirectoryName($python)
$runtime = [ordered]@{}
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    if ($property.Name.StartsWith($pythonRoot+'\',[StringComparison]::Ordinal)) {
        Require-Digest $property.Name $property.Value
        $runtime[$property.Name] = $property.Value
    }
}
if ($runtime.Count -ne 18 -or -not $runtime.Contains($python)) { throw 'PYTHON_RUNTIME_CLOSURE' }
$runtime[$mapPath] = $mapSha
$name = 'retained-advertisement-controls-01'
$selectionPath = Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath (Join-Path $checks $name))) { throw 'FRESH_SELECTION_REQUIRED' }
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($python,'-I','-S','-B','{snapshot}\software\v5\retained_advertisement\controls.py','--output','{output}')
    limits=[ordered]@{cpu_seconds=60;wall_seconds=120;memory_mib=384;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 16)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_JSON_BOUND' }
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
[ordered]@{path=$selectionPath;sha256=(Digest $selectionPath);sources=$sources.Count;runtime_pins=$runtime.Count;logical_sdk_sources=121;executed=$false} | ConvertTo-Json
