$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -ne $projectRoot) { throw 'Canonical workdir required' }
function Hash-File([string] $Path) { (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
$oldPath = Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-public-expr-sync-01.selection.json'
if ((Hash-File $oldPath) -ne '75a53fd0d2905d6b60c52eeb134bf3e2691829eb99e8e697e41d4db8483d93f2') { throw 'Original selection changed' }
$selection = Get-Content -LiteralPath $oldPath -Raw | ConvertFrom-Json
$selection.name = 'ordinary-public-remaining-01'
$selection.sources.'software/v5/ordinary_lean/run_public_support_build.py' = Hash-File (Join-Path $projectRoot 'software/v5/ordinary_lean/run_public_support_build.py')
$previous = Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-public-expr-sync-01'
$pins = [ordered]@{}
foreach ($property in $selection.runtime_pins.PSObject.Properties) { $pins[$property.Name] = $property.Value }
foreach ($suffix in @('lean-build/OriginalExpr.olean','lean-build/OriginalExpr.olean.private','lean-build/OriginalExpr.olean.server',
  'lean-build/OriginalExpr.ir','lean-build/OriginalExpr.ir.sig','public-source/OriginalExpr.lean','PUBLIC-SOURCE-MAP.json','COMPILE-RESULT.json','RESULT.json')) {
    $path = Join-Path $previous $suffix
    $pins[$path] = Hash-File $path
}
$selection.runtime_pins = $pins
$selection.argv = @($selection.argv[0..5]) + @('--remaining-sync',(Join-Path $previous 'lean-build'))
$selection.limits.cpu_seconds = 120
$selection.limits.wall_seconds = 210
$selectionPath = Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-public-remaining-01.selection.json'
$outputPath = Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-public-remaining-01'
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath $outputPath)) { throw 'Fresh paths required' }
$bytes = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 15) + "`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($bytes,0,$bytes.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=$selectionPath;sha256=(Hash-File $selectionPath);execution='NOT_STARTED'} | ConvertTo-Json
