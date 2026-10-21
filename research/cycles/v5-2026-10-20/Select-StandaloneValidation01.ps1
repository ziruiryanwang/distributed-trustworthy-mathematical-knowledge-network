# Stage current114 plus three reviewed standalone-validation successors. No execution.
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
    $row = $property.Value
    $path = [IO.Path]::GetFullPath($row.path)
    if (-not $path.StartsWith($projectRoot+'\software\v5\', [StringComparison]::Ordinal)) { throw 'SDK_SOURCE_SCOPE' }
    Require-Digest $path $row.sha256
    if ((Get-Item -LiteralPath $path).Length -ne $row.bytes) { throw 'SDK_SOURCE_SIZE' }
    $relative = $path.Substring($projectRoot.Length+1).Replace('\','/')
    if ($sources.Contains($relative)) { throw 'DUPLICATE_PHYSICAL_SOURCE' }
    $sources[$relative] = $row.sha256
}
$required = @('admission/pin_phase.py','mixed_claims/receiver.py','mixed_claims/imports_atomic.py','controls.py')
if ($ReviewedSourcesJson.Length -gt 16384) { throw 'REVIEWED_MAP_BOUND' }
$reviewed = $ReviewedSourcesJson | ConvertFrom-Json
$keys = @($reviewed.psobject.Properties.Name)
if ($keys.Count -ne $required.Count -or @(Compare-Object $keys $required -CaseSensitive).Count -ne 0) { throw 'EXACT_REVIEWED_SOURCE_SET' }
foreach ($key in $required) {
    $relative = 'software/v5/standalone_validation/'+$key
    if ($sources.Contains($relative)) { throw 'FRESH_SUCCESSOR_REQUIRED' }
    Require-Digest (Join-Path $projectRoot $relative) $reviewed.$key
    $sources[$relative] = $reviewed.$key
}
if ($sources.Count -ne 119) { throw 'EXACT_SOURCE_COUNT' }
# The two AST-only predecessor checks already belong to the114 input map.
if ($sources['software/v5/runtime_efficient/mixed_claims/receiver.py'] -cne 'aa591a1829deff82576ba30af484ab560ee04900200fd79ac93c19a9c2c7bf7f' -or
    $sources['software/v5/interface_views/imports_atomic.py'] -cne 'e38ac52a888f354e8e878984397a5c93c82ac38284b9e6fc89051063537aa459') { throw 'AST_PREDECESSOR_PINS' }
$basisPath = Join-Path $checks 'terminal-i-controls-01-selection.json'
Require-Digest $basisPath 'b43f3eb450219760ae80a91e29b316743b9a517b34c99d688129c067877037ec'
$basis = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
$python = $basis.argv[0]
$pythonRoot = [IO.Path]::GetDirectoryName($python)
$runtime = [ordered]@{}
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    if ($property.Name.StartsWith($pythonRoot+'\', [StringComparison]::Ordinal)) {
        Require-Digest $property.Name $property.Value
        $runtime[$property.Name] = $property.Value
    }
}
if ($runtime.Count -ne 18 -or -not $runtime.Contains($python)) { throw 'PYTHON_RUNTIME_CLOSURE' }
$runtime[$mapPath] = $mapSha
$name = 'standalone-validation-controls-01'
$selectionPath = Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath (Join-Path $checks $name))) { throw 'FRESH_SELECTION_REQUIRED' }
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($python,'-I','-S','-B','{snapshot}\software\v5\standalone_validation\controls.py','--output','{output}')
    limits=[ordered]@{cpu_seconds=45;wall_seconds=90;memory_mib=384;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected | ConvertTo-Json -Depth 16)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_JSON_BOUND' }
$stream = [IO.File]::Open($selectionPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
[ordered]@{path=$selectionPath;sha256=(Digest $selectionPath);sources=$sources.Count;runtime_pins=$runtime.Count;executed=$false} | ConvertTo-Json
