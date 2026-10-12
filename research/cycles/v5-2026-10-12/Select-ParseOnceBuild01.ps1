$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'aggregate-parse-once-build-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $local $name),(Join-Path $local ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+$path) }
}
$sources=[ordered]@{}
function Include([string]$relative) {
    $item=Get-Item -LiteralPath (Join-Path $projectRoot $relative)
    $sources[$relative]=[ordered]@{bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
foreach($file in @('lib.rs','census.rs','relation.rs','parse_once_controls.rs','build_native.py')) {
    Include ('software/v5/aggregate_parse_once/'+$file)
}
foreach($file in @('header.rs','membership.rs','wire.rs','tests.rs','graph_controls.rs','census.rs','native.rs')) {
    Include ('software/v5/aggregate/'+$file)
}
$selection=[ordered]@{schema='DMKN_V5_AGGREGATE_PARSE_ONCE_BUILD_V1';name=$name;authorizes_compile_only=$true;sources=$sources}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selection|ConvertTo-Json -Depth 10)+"`n")
$stream=[IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{path=$selectionPath;bytes=$raw.Length;sha256=(Get-FileHash -LiteralPath $selectionPath -Algorithm SHA256).Hash.ToLowerInvariant();executed=$false}|ConvertTo-Json
