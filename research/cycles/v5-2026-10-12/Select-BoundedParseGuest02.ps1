# Exact root selection for the reviewed resolver-cache successor. No launch.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$BuildSourceSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$CacheSourceSha256
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'bounded-parse-guest-build-02'
$selectionPath = Join-Path $local ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $local $name),(Join-Path $local ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer) { throw 'FILE_REQUIRED' }
    [ordered]@{bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$priorPath = Join-Path $local 'bounded-parse-guest-build-01/selection.json'
if ((Pin $priorPath).sha256 -cne 'be47024a42da96b5d33dcbea8e9ffcc4f2d81be50cc30a1f58ff0b2d4da0e41d') { throw 'EXACT_PREDECESSOR_SELECTION' }
$prior = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
if ($prior.schema -cne 'DMKN_V5_BOUNDED_PARSE_GUEST_BUILD_V1' -or $prior.name -cne 'bounded-parse-guest-build-01') { throw 'PRIOR_PROFILE' }
$sources = [ordered]@{}
foreach ($property in $prior.sources.psobject.Properties) {
    if ($property.Name -ceq 'software/v5/bounded_parse_guest/build.py') { continue }
    $actual = Pin (Join-Path $projectRoot $property.Name)
    if ($actual.bytes -ne $property.Value.bytes -or $actual.sha256 -cne $property.Value.sha256) { throw ('UNCHANGED_SOURCE:'+ $property.Name) }
    $sources[$property.Name] = $actual
}
if ($sources.Count -ne 36) { throw 'EXACT_36_UNCHANGED_SOURCES' }
$fresh = [ordered]@{
    'software/v5/bounded_parse_guest/build_resolver.py'=$BuildSourceSha256
    'software/v5/bounded_parse_guest/cache_resolver.py'=$CacheSourceSha256
}
foreach ($relative in $fresh.Keys) {
    $actual = Pin (Join-Path $projectRoot $relative)
    if ($actual.sha256 -cne $fresh[$relative]) { throw ('FRESH_SOURCE_CHANGED:'+ $relative) }
    $sources[$relative] = $actual
}
if ($sources.Count -ne 38) { throw 'EXACT_38_SOURCES' }
$comparison = Pin $prior.native_comparison.path
if ($comparison.bytes -ne 8960 -or $comparison.sha256 -cne 'ddd411125b809fda24be93280329f6d7b7bd3d4b32ac5cbd71beab46e4948a20') { throw 'ADOPTED_NATIVE_RESULT' }
$selected = [ordered]@{
    schema='DMKN_V5_BOUNDED_PARSE_RESOLVER_GUEST_BUILD_V1';name=$name;sources=$sources
    authorizes_guest_build_and_owned_telemetry_cleanup=$true
    native_comparison=$prior.native_comparison
    limits=$prior.limits
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected|ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=$selectionPath;pin=(Pin $selectionPath);sources=$sources.Count;cargo_calls=2;guest_calls=0;proof_calls=0;executed=$false} | ConvertTo-Json -Depth 5
