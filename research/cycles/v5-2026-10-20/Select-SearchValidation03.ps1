# Complete the inherited fixture closure by exact union with its passing plan.
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$prior=Join-Path $checks 'search-validation-controls-02-selection.json'
$fixturePlan=Join-Path $checks 'search-resilience-controls-01-selection.json'
if ((Digest $prior) -cne '8faa071f596d9afadf08bbd70b07a6611fc11cf2f4224e2fa41a2077977e0246') { throw 'PRIOR_CHANGED' }
if ((Digest $fixturePlan) -cne '6615ff9b994a2deca02556936b7a272b74beecb8796829642945eafa970f30af') { throw 'FIXTURE_PLAN_CHANGED' }
$old=Get-Content -LiteralPath $prior -Raw | ConvertFrom-Json
$fixtures=Get-Content -LiteralPath $fixturePlan -Raw | ConvertFrom-Json
$sources=[ordered]@{}
foreach ($plan in @($old,$fixtures)) {
    foreach ($property in $plan.sources.psobject.Properties) {
        if ((Digest (Join-Path $projectRoot $property.Name)) -cne $property.Value) { throw 'SOURCE_CHANGED' }
        if ($sources.Contains($property.Name) -and $sources[$property.Name] -cne $property.Value) { throw 'CONFLICTING_SOURCE' }
        $sources[$property.Name]=$property.Value
    }
}
if ($sources.Count -ne 85 -or -not $sources.Contains('software/v5/discovery/test_candidate_query.py')) { throw 'EXACT_FIXTURE_CLOSURE' }
$runtime=[ordered]@{}
foreach ($property in $old.runtime_pins.psobject.Properties) {
    if ((Digest $property.Name) -cne $property.Value) { throw 'RUNTIME_CHANGED' }
    $runtime[$property.Name]=$property.Value
}
$name='search-validation-controls-03'
$path=Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $path) -or (Test-Path -LiteralPath (Join-Path $checks $name))) { throw 'NOT_FRESH' }
$selected=[ordered]@{schema=$old.schema;name=$name;sources=$sources;runtime_pins=$runtime;argv=@($old.argv);limits=$old.limits}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selected|ConvertTo-Json -Depth 12)+"`n")
$stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{path=$path;sha256=(Digest $path);sources=$sources.Count;executed=$false}|ConvertTo-Json
