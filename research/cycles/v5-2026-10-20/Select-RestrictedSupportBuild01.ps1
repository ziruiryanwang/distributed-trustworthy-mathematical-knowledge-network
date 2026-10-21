# Select one two-crate support-summary native build; no compiler or test runs.
param([Parameter(Mandatory=$true)][string]$ExpectedBuildSha)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) {
    (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
$builder = Join-Path $projectRoot 'software\v5\restricted_support\build.py'
if ($ExpectedBuildSha -cnotmatch '^[0-9a-f]{64}$' -or
    (Digest $builder) -cne $ExpectedBuildSha) { throw 'REVIEWED_BUILDER_CHANGED' }
$sources = [ordered]@{}
foreach ($relative in @(
    'software/v5/restricted_support/lib.rs',
    'software/v5/restricted_support/syntax.rs',
    'software/v5/restricted_support/typing.rs',
    'software/v5/restricted_support/controls.rs',
    'software/v5/restricted_support/controls_root.rs',
    'software/v5/restricted_support/build.py',
    'software/v5/restricted_composition/relation.rs',
    'software/v5/restricted_composition/foundation02.rs'
)) {
    if ($sources.Contains($relative)) { throw 'DUPLICATE_SOURCE' }
    $path = Join-Path $projectRoot $relative
    $sources[$relative] = [ordered]@{
        bytes = (Get-Item -LiteralPath $path).Length
        sha256 = Digest $path
    }
}
if ($sources.Count -ne 8) { throw 'EXACT_SOURCE_CENSUS' }
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'restricted-support-build-01'
$selectionPath = Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $selectionPath) -or
    (Test-Path -LiteralPath (Join-Path $checks $name)) -or
    (Test-Path -LiteralPath (Join-Path $checks ($name+'-attempt.json')))) {
    throw 'FRESH_BUILD_SELECTION_REQUIRED'
}
$selection = [ordered]@{
    schema = 'DMKN_V5_RC_SUPPORT_BUILD_V1'
    name = $name
    authorizes_compile_only = $true
    sources = $sources
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(
    ($selection | ConvertTo-Json -Depth 12)+"`n")
if ($raw.Length -gt 65536) { throw 'SELECTION_SIZE' }
$stream = [IO.File]::Open($selectionPath, [IO.FileMode]::CreateNew,
    [IO.FileAccess]::Write, [IO.FileShare]::None)
try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
finally { $stream.Dispose() }
[ordered]@{
    path = $selectionPath
    sha256 = Digest $selectionPath
    source_count = $sources.Count
    compiler_executed = $false
} | ConvertTo-Json
