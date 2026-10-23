$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -ne $projectRoot) { throw 'Canonical workdir required' }
function Hash-File([string] $Path) { (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
$originalPath = Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-native-admission-01\selection.json'
if ((Hash-File $originalPath) -ne 'ab2f655448242587880129e62cca4bc5dc74638c1e8699e30b4a9f67e26fce5f') { throw 'Original pins changed' }
$original = Get-Content -LiteralPath $originalPath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
foreach ($relative in @('tools/Run-V5-Check.py','software/v5/ordinary_lean/run_selected_compile.py','software/v5/ordinary_lean/OwnerRebind.lean')) {
    $sources[$relative] = Hash-File (Join-Path $projectRoot $relative)
}
if ($sources['software/v5/ordinary_lean/OwnerRebind.lean'] -ne 'a7fbb85189fbee3d816c822d56bb8642e48e24f8952776ec9439fea12b6f6e01') { throw 'Reviewed helper changed' }
$pins = [ordered]@{}
foreach ($property in $original.runtime_pins.PSObject.Properties) {
    if ($property.Name -match '(python|\\bin\\|OriginalExpr|OriginalDecl|CheckedExtension|BootstrapSupport)') {
        $pins[$property.Name] = $property.Value
    }
}
$previous = (Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-library-controls-05\lean-build') + ';' +
    (Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-workflow-build-01\lean-build')
$selection = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1'; name='ordinary-owner-rebind-build-01'
    sources=$sources; runtime_pins=$pins
    argv=@('D:\Python314\python.exe','-I','-S','-B','{snapshot}\software\v5\ordinary_lean\run_selected_compile.py','{output}',$previous,'OwnerRebind')
    limits=[ordered]@{cpu_seconds=60;wall_seconds=90;memory_mib=1536;active_processes=3;stdout_bytes=1048576;stderr_bytes=1048576}
}
$selectionPath = Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-owner-rebind-build-01.selection.json'
$outputPath = Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-owner-rebind-build-01'
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath $outputPath)) { throw 'Fresh paths required' }
$bytes = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 15) + "`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($bytes,0,$bytes.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=$selectionPath;sha256=(Hash-File $selectionPath);execution='NOT_STARTED'} | ConvertTo-Json
