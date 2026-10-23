$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -ne $projectRoot) { throw 'Canonical workdir required' }
function Hash-File([string] $Path) { (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
$oldPath = Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-owner-rebind-build-01.selection.json'
if ((Hash-File $oldPath) -ne '0dab9fa5190010dcb747c7d255fdd181ea0d064f7b158e66a1c034db71c7c9c1') { throw 'Predecessor selection changed' }
$old = Get-Content -LiteralPath $oldPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($relative in @('tools/Run-V5-Check.py','software/v5/ordinary_lean/run_public_support_build.py',
  'software/v5/ordinary_lean/OwnerRebind.lean','software/v5/ordinary_lean/OriginalExpr.lean',
  'software/v5/ordinary_lean/OriginalDecl.lean','software/v5/ordinary_lean/CheckedExtension.lean',
  'software/v5/ordinary_lean/BootstrapSupport.lean')) { $sources[$relative] = Hash-File (Join-Path $projectRoot $relative) }
$selection = [ordered]@{schema='DMKN_V5_LOCAL_CHECK_V1';name='ordinary-public-support-build-01';sources=$sources
  runtime_pins=$old.runtime_pins
  argv=@('D:\Python314\python.exe','-I','-S','-B','{snapshot}\software\v5\ordinary_lean\run_public_support_build.py','{output}')
  limits=[ordered]@{cpu_seconds=90;wall_seconds=120;memory_mib=1536;active_processes=3;stdout_bytes=1048576;stderr_bytes=1048576}}
$selectionPath = Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-public-support-build-01.selection.json'
$outputPath = Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-public-support-build-01'
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath $outputPath)) { throw 'Fresh paths required' }
$bytes = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 15) + "`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($bytes,0,$bytes.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=$selectionPath;sha256=(Hash-File $selectionPath);execution='NOT_STARTED'} | ConvertTo-Json
