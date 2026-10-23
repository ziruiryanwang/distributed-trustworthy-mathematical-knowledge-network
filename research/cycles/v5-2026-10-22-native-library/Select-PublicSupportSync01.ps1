$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -ne $projectRoot) { throw 'Canonical workdir required' }
$oldPath = Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-public-support-build-01.selection.json'
if ((Get-FileHash -LiteralPath $oldPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne '18753758cd0c85a34457e65bd83c067462a90525517202e28c1743ab9382946e') { throw 'Original selection changed' }
$selection = Get-Content -LiteralPath $oldPath -Raw | ConvertFrom-Json
$selection.name = 'ordinary-public-expr-sync-01'
$selection.sources.'software/v5/ordinary_lean/run_public_support_build.py' = 'aadce94e778c0ac858da922389e743595fc447a6328b06d032a64dbc65682e0c'
$selection.argv = @($selection.argv) + @('--first-sync')
$selectionPath = Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-public-expr-sync-01.selection.json'
$outputPath = Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-public-expr-sync-01'
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath $outputPath)) { throw 'Fresh paths required' }
$bytes = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 15) + "`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($bytes,0,$bytes.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=$selectionPath;sha256=(Get-FileHash -LiteralPath $selectionPath -Algorithm SHA256).Hash.ToLowerInvariant();execution='NOT_STARTED'} | ConvertTo-Json
