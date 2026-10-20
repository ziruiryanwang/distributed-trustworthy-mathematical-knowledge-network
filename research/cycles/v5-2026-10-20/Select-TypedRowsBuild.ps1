# Prepare a fresh exact source manifest. This script never starts a compiler.
param([Parameter(Mandatory=$true)][string]$ExpectedBuildSha)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) {
    (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
$builder = Join-Path $projectRoot 'software\v5\typed_rows\build.py'
if ($ExpectedBuildSha -cnotmatch '^[0-9a-f]{64}$' -or
    (Digest $builder) -cne $ExpectedBuildSha) { throw 'REVIEWED_BUILDER_CHANGED' }
$paths = [Collections.Generic.List[string]]::new()
foreach ($name in @('rows.rs','decode.rs','checker_lib.rs','module_correspondence.rs',
    'parser.rs','foundation_static.rs','module_relation.rs','module_lib.rs',
    'census.rs','aggregate_relation.rs','aggregate_lib.rs','controls.rs',
    'controls_root.rs','build.py')) {
    $paths.Add('software/v5/typed_rows/'+$name)
}
foreach ($name in @('input','foundation_data','commitments','journal','policy')) {
    $paths.Add('software/v5/modules/receipt/src/'+$name+'.rs')
}
foreach ($name in @('header','membership','wire')) {
    $paths.Add('software/v5/aggregate_claims/'+$name+'.rs')
}
foreach ($name in @('canonical','module_relation','census')) {
    $paths.Add('software/v5/bounded_parse/'+$name+'.rs')
}
$paths.Add('software/v5/modules/native/proof_memo/module_correspondence.rs')
foreach ($name in @('debug_printer','demand','env','expr','inductive','level',
    'module','name','pretty_printer','quot','tc','unique_hasher','util')) {
    $paths.Add('software/v5/modules/native/checker/src/'+$name+'.rs')
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
$name = 'typed-rows-build-01'
$selectionPath = Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $selectionPath) -or
    (Test-Path -LiteralPath (Join-Path $checks $name)) -or
    (Test-Path -LiteralPath (Join-Path $checks ($name+'-attempt.json')))) {
    throw 'FRESH_BUILD_SELECTION_REQUIRED'
}
$selection = [ordered]@{
    schema = 'DMKN_V5_TYPED_ROWS_BUILD_V1'; name = $name
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
