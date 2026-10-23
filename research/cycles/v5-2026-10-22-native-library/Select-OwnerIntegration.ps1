param(
    [Parameter(Mandatory=$true)][string] $Name,
    [Parameter(Mandatory=$true)][string[]] $Modules,
    [Parameter(Mandatory=$true)][string[]] $Previous
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -ne $projectRoot) { throw 'Canonical workdir required' }
if ($Name -notmatch '^ordinary-[a-z0-9-]+$' -or $Modules.Count -lt 1 -or $Modules.Count -gt 8) { throw 'Bounded build name/modules required' }
function Hash-File([string] $Path) { (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
$oldPath = Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-public-remaining-01.selection.json'
if ((Hash-File $oldPath) -ne '24aa7daa0ccdb293638f180a7ff6334f8881801fd21fea2589bd8c71fa4634c0') { throw 'Original selection changed' }
$old = Get-Content -LiteralPath $oldPath -Raw | ConvertFrom-Json
$pins = [ordered]@{}
foreach ($property in $old.runtime_pins.PSObject.Properties) {
    if ($property.Name -match '(python|\\bin\\)') { $pins[$property.Name] = $property.Value }
}
$previousPaths = @()
foreach ($item in $Previous) {
    if ($item -notmatch '^ordinary-[a-z0-9-]+$') { throw 'Selected local predecessor required' }
    $base = Join-Path $projectRoot ('experiments\v5-local-checks\' + $item)
    $build = Join-Path $base 'lean-build'
    if (-not (Test-Path -LiteralPath $build -PathType Container)) { throw 'Missing retained build' }
    $previousPaths += $build
    foreach ($file in Get-ChildItem -LiteralPath $build -File) { $pins[$file.FullName] = Hash-File $file.FullName }
    foreach ($leaf in @('selection.json','RESULT.json')) {
        $path = Join-Path $base $leaf
        $pins[$path] = Hash-File $path
    }
}
$sources = [ordered]@{}
foreach ($relative in @('tools/Run-V5-Check.py','software/v5/ordinary_lean/run_selected_compile.py')) {
    $sources[$relative] = Hash-File (Join-Path $projectRoot $relative)
}
foreach ($module in $Modules) {
    if ($module -notmatch '^[A-Za-z][A-Za-z0-9_]*$') { throw 'Plain module required' }
    $relative = 'software/v5/ordinary_lean/' + $module + '.lean'
    $sources[$relative] = Hash-File (Join-Path $projectRoot $relative)
}
$selection = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1'; name=$Name; sources=$sources; runtime_pins=$pins
    argv=@('D:\Python314\python.exe','-I','-S','-B','{snapshot}\software\v5\ordinary_lean\run_selected_compile.py','{output}',($previousPaths -join ';')) + $Modules
    limits=[ordered]@{cpu_seconds=(30 * $Modules.Count);wall_seconds=(45 * $Modules.Count + 15);memory_mib=1536;active_processes=3;stdout_bytes=1048576;stderr_bytes=1048576}
}
$selectionPath = Join-Path $projectRoot ('experiments\v5-local-checks\' + $Name + '.selection.json')
$outputPath = Join-Path $projectRoot ('experiments\v5-local-checks\' + $Name)
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath $outputPath)) { throw 'Fresh paths required' }
$bytes = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 15) + "`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($bytes,0,$bytes.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=$selectionPath;sha256=(Hash-File $selectionPath);execution='NOT_STARTED'} | ConvertTo-Json
