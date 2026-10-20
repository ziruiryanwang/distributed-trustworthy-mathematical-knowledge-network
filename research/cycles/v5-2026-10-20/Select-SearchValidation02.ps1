# Correct only the omitted inert-fixture import in the failed pre-test selection.
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$prior=Join-Path $checks 'search-validation-controls-01-selection.json'
if ((Digest $prior) -cne '532600e0e9c6e288c4df10682a133d5a9003d368bcef5d4556ea8888a1a962b6') { throw 'PRIOR_CHANGED' }
$old=Get-Content -LiteralPath $prior -Raw | ConvertFrom-Json
$sources=[ordered]@{}
foreach ($property in $old.sources.psobject.Properties) {
    if ((Digest (Join-Path $projectRoot $property.Name)) -cne $property.Value) { throw 'SOURCE_CHANGED' }
    $sources[$property.Name]=$property.Value
}
$fixture='software/v5/transport/test_search_resilience.py'
$fixtureHash='21a540bd9a80fa83214ac25d184195141f8a52f146a424622cad31bf30619f52'
if ((Digest (Join-Path $projectRoot $fixture)) -cne $fixtureHash) { throw 'FIXTURE_CHANGED' }
$sources[$fixture]=$fixtureHash
$runtime=[ordered]@{}
foreach ($property in $old.runtime_pins.psobject.Properties) {
    if ((Digest $property.Name) -cne $property.Value) { throw 'RUNTIME_CHANGED' }
    $runtime[$property.Name]=$property.Value
}
$name='search-validation-controls-02'
$path=Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $path) -or (Test-Path -LiteralPath (Join-Path $checks $name))) { throw 'NOT_FRESH' }
$selected=[ordered]@{schema=$old.schema;name=$name;sources=$sources;runtime_pins=$runtime;argv=@($old.argv);limits=$old.limits}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selected|ConvertTo-Json -Depth 12)+"`n")
$stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{path=$path;sha256=(Digest $path);sources=$sources.Count;executed=$false}|ConvertTo-Json
