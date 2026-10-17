# Select one fresh compiler link. Does not invoke Python, rustc, host or prover.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'aggregate-stage-host-build-01'
$selectionPath = Join-Path $checks ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $checks $name),(Join-Path $checks ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer) { throw 'FILE_REQUIRED' }
    [ordered]@{bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$held = [ordered]@{
    'aggregate-host-build-01-selection.json'='b8c64994f64c66eaa8a90612d5fa0f3ebcad4ce053e86f4f8fe485408cadbb8b'
    'aggregate-host-build-01-attempt.json'='cdc489e3d1dcd73bcb4ab782fd10138ccaaf452725976c2f38ac644348590ee2'
    'aggregate-host-build-01/RESULT.json'='4cdb12b5e3aeaebcfef5e0370bd445f24ff6779b196ca69cbab60f9d57002a75'
    'aggregate-host-build-01/compile-command.json'='acc215837499107a01bfe60544dceeb40ff19ad4d67f93252867bbf30f3de96b'
    'aggregate-host-build-01/environment-profile.json'='34525808d26848e9582ad5ada38ff66fae2205f79ae0421a33f72fbd67af4e18'
}
foreach ($entry in $held.GetEnumerator()) {
    if ((Pin (Join-Path $checks $entry.Key)).sha256 -cne $entry.Value) { throw ('OLD_RECORD_CHANGED:'+ $entry.Key) }
}
if (Test-Path -LiteralPath (Join-Path $checks 'aggregate-host-build-01/FINALIZATION-FAILED.json')) { throw 'OLD_FINALIZATION_FAILED' }
$old = Get-Content -LiteralPath (Join-Path $checks 'aggregate-host-build-01-selection.json') -Raw | ConvertFrom-Json
$argv = @(Get-Content -LiteralPath (Join-Path $checks 'aggregate-host-build-01/compile-command.json') -Raw | ConvertFrom-Json)
$directories = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
$externs = @()
for ($i=0; $i -lt $argv.Count; $i++) {
    if ($argv[$i] -ceq '-L') { [void]$directories.Add($argv[$i+1].Split('=',2)[1]) }
    if ($argv[$i] -ceq '--extern') { $externs += $argv[$i+1].Split('=',2)[1] }
}
if ($directories.Count -ne 14 -or $externs.Count -ne 7 -or @($old.runtime_pins.psobject.Properties).Count -ne 3142) { throw 'OLD_LINK_SHAPE' }
$rust = Join-Path $projectRoot 'experiments\scale-crypto-01\runs\run-01\rust'
$rustBin = Join-Path $rust 'bin'
$rustLib = Join-Path $rust 'lib\rustlib\x86_64-pc-windows-msvc\lib'
$suffixes = @('.rlib','.rmeta','.dll','.lib','.a')
$runtime = [ordered]@{}
$runtimeBytes = 0L
$hostCount = 0
$rustCount = 0
foreach ($property in $old.runtime_pins.psobject.Properties) {
    $path = $property.Name
    $parent = [IO.Path]::GetDirectoryName($path)
    $extension = [IO.Path]::GetExtension($path)
    $hostTool = [IO.Path]::GetPathRoot($path).ToLowerInvariant() -ceq 'c:\'
    $keep = $hostTool -or ($directories.Contains($parent) -and $suffixes -ccontains $extension) -or
        ($path -ceq (Join-Path $rustBin 'rustc.exe')) -or
        ($parent -ceq $rustBin -and $extension -ceq '.dll') -or
        ($parent -ceq $rustLib -and $suffixes -ccontains $extension)
    if ($keep) {
        if ($property.Value -cnotmatch '^[0-9a-f]{64}$') { throw 'RUNTIME_DIGEST' }
        $runtime[$path] = $property.Value
        $item = Get-Item -LiteralPath $path
        if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'ORDINARY_RUNTIME_FILE' }
        $runtimeBytes += $item.Length
        if ($hostTool) { $hostCount++ }
        if ($path.StartsWith($rust+'\',[StringComparison]::Ordinal)) { $rustCount++ }
    }
}
if ($runtime.Count -ne 1071 -or $runtimeBytes -ne 2320491997 -or $hostCount -ne 98 -or $rustCount -ne 25) { throw 'EXACT_RUNTIME_SUBSET' }
foreach ($path in $externs) { if (-not $runtime.Contains($path)) { throw 'UNPINNED_EXTERN' } }
if ($argv[0] -cne (Join-Path $rustBin 'rustc.exe') -or -not $runtime.Contains($argv[0])) { throw 'UNPINNED_RUSTC' }
foreach ($argument in $argv) {
    if ($argument.StartsWith('linker=',[StringComparison]::Ordinal) -and -not $runtime.Contains($argument.Split('=',2)[1])) { throw 'UNPINNED_LINKER' }
}
$expectedSources = [ordered]@{
    'software/v5/aggregate_production/build.py'='a1d2c22427ffa9f8293813ac76359f9cdde6a3f73870c75a209dad2310bc781a'
    'software/v5/aggregate_production/stage_host.rs'='5865e6afb30bd81adb79d6fe04e09ac8bb7238b40956284fa3bcd2d4da4fe102'
    'software/v5/aggregate/receipt.rs'='41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254'
}
$sources = [ordered]@{}
foreach ($entry in $expectedSources.GetEnumerator()) {
    $pin = Pin (Join-Path $projectRoot $entry.Key)
    if ($pin.sha256 -cne $entry.Value) { throw ('SOURCE_CHANGED:'+ $entry.Key) }
    $sources[$entry.Key] = $pin
}
$selection = [ordered]@{
    schema='DMKN_V5_AGGREGATE_STAGE_HOST_BUILD_V1';name=$name;authorizes_compile_only=$true
    sources=$sources;runtime_pins=$runtime
    limits=[ordered]@{worker_cpu_seconds=240;worker_wall_seconds=300;memory_mib=3072;active_processes=6
        ordinary_controller_cpu_seconds=40;controller_cpu_seconds=60;total_wall_seconds=420
        fresh_output_bytes=536870912;fresh_output_entries=8192;command_log_bytes=1048576}
}
$bytes = [Text.UTF8Encoding]::new($false).GetBytes(($selection | ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($bytes,0,$bytes.Length);$stream.Flush($true) } finally { $stream.Dispose() }
[ordered]@{selection=$selectionPath;pin=(Pin $selectionPath);runtime_files=$runtime.Count;runtime_bytes=$runtimeBytes;executed=$false} | ConvertTo-Json -Depth 4
