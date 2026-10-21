# Prepare one fresh native compile selection. Does not start a compiler or test.
param([Parameter(Mandatory=$true)][string]$ExpectedBuildSha)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) {
    (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
$builder = Join-Path $projectRoot 'software\v5\restricted_composition\build.py'
if ($ExpectedBuildSha -cnotmatch '^[0-9a-f]{64}$' -or
    (Digest $builder) -cne $ExpectedBuildSha) { throw 'REVIEWED_BUILDER_CHANGED' }
$paths = [Collections.Generic.List[string]]::new()
foreach ($name in @('lib.rs','syntax.rs','foundation.rs','typing.rs','relation.rs',
    'census.rs','wire.rs','aggregate_relation.rs','aggregate_lib.rs','controls.rs',
    'controls_root.rs','build.py','fixtures.py')) {
    $paths.Add('software/v5/restricted_composition/'+$name)
}
foreach ($name in @('header.rs','membership.rs')) {
    $paths.Add('software/v5/aggregate_claims/'+$name)
}
$sources = [ordered]@{}
foreach ($relative in $paths) {
    if ($sources.Contains($relative)) { throw 'DUPLICATE_SOURCE' }
    $path = Join-Path $projectRoot $relative
    $sources[$relative] = [ordered]@{
        bytes = (Get-Item -LiteralPath $path).Length; sha256 = (Digest $path)
    }
}
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'restricted-composition-build-01'
$selectionPath = Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $selectionPath) -or
    (Test-Path -LiteralPath (Join-Path $checks $name)) -or
    (Test-Path -LiteralPath (Join-Path $checks ($name+'-attempt.json')))) {
    throw 'FRESH_BUILD_SELECTION_REQUIRED'
}
$selection = [ordered]@{
    schema = 'DMKN_V5_RC_NATIVE_BUILD_V1'; name = $name
    authorizes_compile_only = $true; sources = $sources
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(
    ($selection | ConvertTo-Json -Depth 12)+"`n")
if ($raw.Length -gt 65536) { throw 'SELECTION_SIZE' }
$stream = [IO.File]::Open($selectionPath, [IO.FileMode]::CreateNew,
    [IO.FileAccess]::Write, [IO.FileShare]::None)
try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
[ordered]@{
    path=$selectionPath; sha256=(Digest $selectionPath)
    source_count=$sources.Count; compiler_executed=$false
} | ConvertTo-Json
