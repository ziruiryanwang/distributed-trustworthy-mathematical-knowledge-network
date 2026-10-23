param(
    [Parameter(Mandatory=$true)][string] $Name,
    [Parameter(Mandatory=$true)][string] $CommandBuild
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -ne $projectRoot) { throw 'Canonical workdir required' }
if ($Name -notmatch '^ordinary-[a-z0-9-]+$' -or $CommandBuild -notmatch '^ordinary-[a-z0-9-]+$') { throw 'Selected operation names required' }
function Hash-File([string] $Path) { (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
$oldPath = Join-Path $projectRoot ('experiments\v5-local-checks\' + $CommandBuild + '\selection.json')
$old = Get-Content -LiteralPath $oldPath -Raw | ConvertFrom-Json
$resultPath = Join-Path $projectRoot ('experiments\v5-local-checks\' + $CommandBuild + '\RESULT.json')
$result = Get-Content -LiteralPath $resultPath -Raw | ConvertFrom-Json
if ($result.result.status -ne 'COMMAND_EXITED_ZERO_AND_CLOSED' -or $result.selection_sha256 -ne (Hash-File $oldPath)) { throw 'Successful selected command build required' }
$pins = [ordered]@{}
foreach ($property in $old.runtime_pins.PSObject.Properties) { $pins[$property.Name] = $property.Value }
$build = Join-Path $projectRoot ('experiments\v5-local-checks\' + $CommandBuild + '\lean-build')
foreach ($file in Get-ChildItem -LiteralPath $build -File) { $pins[$file.FullName] = Hash-File $file.FullName }
$pins[$oldPath] = Hash-File $oldPath
$pins[$resultPath] = Hash-File $resultPath
$prepared = Join-Path $projectRoot 'experiments\v5-local-checks\ordinary-owner-consumer-02\PREPARE-RESULT.json'
if ((Hash-File $prepared) -ne '09477faa163f9e2a6071d479552367650a41ac13218f70d66f8159740cb04d23') { throw 'Actual adopted request manifest changed' }
$pins[$prepared] = Hash-File $prepared
$inventory = Join-Path $projectRoot 'software\assets\foundation\seed-inventory-json.json'
if ((Hash-File $inventory) -ne 'c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0') { throw 'Fixed inventory changed' }
$pins[$inventory] = Hash-File $inventory
$sources = [ordered]@{}
foreach ($relative in @('tools/Run-V5-Check.py','software/v5/ordinary_lean/run_owner_consumer.py','software/v5/ordinary_lean/examples/ReadFootprintConsumer.lean')) {
    $sources[$relative] = Hash-File (Join-Path $projectRoot $relative)
}
$previous = $build + ';' + $old.argv[6]
$selection = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1'; name=$Name; sources=$sources; runtime_pins=$pins
    argv=@('D:\Python314\python.exe','-I','-S','-B','{snapshot}\software\v5\ordinary_lean\run_owner_consumer.py','{output}',$previous)
    limits=[ordered]@{cpu_seconds=120;wall_seconds=150;memory_mib=1536;active_processes=3;stdout_bytes=1048576;stderr_bytes=1048576}
}
if ($pins.Count -gt 256) { throw 'Runtime pin count bound' }
$selectionPath = Join-Path $projectRoot ('experiments\v5-local-checks\' + $Name + '.selection.json')
$outputPath = Join-Path $projectRoot ('experiments\v5-local-checks\' + $Name)
if ((Test-Path -LiteralPath $selectionPath) -or (Test-Path -LiteralPath $outputPath)) { throw 'Fresh paths required' }
$bytes = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 15) + "`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($bytes,0,$bytes.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=$selectionPath;sha256=(Hash-File $selectionPath);execution='NOT_STARTED'} | ConvertTo-Json
