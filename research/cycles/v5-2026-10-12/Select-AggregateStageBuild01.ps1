# Root-only exact one-link selection, not a compiler or proof invocation.
# Requires separately adopted source review and a completed aggregate screen.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$BuildSourceSha256
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'aggregate-stage-host-build-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $local $name),(Join-Path $local ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) { throw 'ORDINARY_FILE_REQUIRED' }
    [ordered]@{bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$sources = [ordered]@{}
$expected = [ordered]@{
    'software/v5/aggregate_production/build.py'=$BuildSourceSha256
    'software/v5/aggregate_production/stage_host.rs'='5865e6afb30bd81adb79d6fe04e09ac8bb7238b40956284fa3bcd2d4da4fe102'
    'software/v5/aggregate/receipt.rs'='41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254'
}
foreach ($relative in $expected.Keys) {
    $row = Pin (Join-Path $projectRoot $relative)
    if ($row.sha256 -cne $expected[$relative]) { throw ('SOURCE_CHANGED:'+ $relative) }
    $sources[$relative] = $row
}
$priorPath = Join-Path $local 'aggregate-host-build-01-selection.json'
$commandPath = Join-Path $local 'aggregate-host-build-01\compile-command.json'
if ((Pin $priorPath).sha256 -cne 'b8c64994f64c66eaa8a90612d5fa0f3ebcad4ce053e86f4f8fe485408cadbb8b' -or
    (Pin $commandPath).sha256 -cne 'acc215837499107a01bfe60544dceeb40ff19ad4d67f93252867bbf30f3de96b') { throw 'EXACT_RETAINED_RECIPE' }
$prior = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
$command = @(Get-Content -LiteralPath $commandPath -Raw | ConvertFrom-Json)
if (@($prior.runtime_pins.psobject.Properties).Count -ne 3142) { throw 'EXACT_PRIOR_RUNTIME_MAP' }
$directories = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
for ($index = 0; $index -lt $command.Count; $index++) {
    if ($command[$index] -ceq '-L') {
        $parts = $command[$index+1] -split '=',2
        if ($parts.Count -ne 2) { throw 'LINK_SEARCH_SHAPE' }
        [void]$directories.Add($parts[1])
    }
}
if ($directories.Count -ne 14 -or @($command | Where-Object { $_ -ceq '--extern' }).Count -ne 7) { throw 'RETAINED_LINK_INPUTS' }
$rust = Join-Path $projectRoot 'experiments\scale-crypto-01\runs\run-01\rust'
$rustBin = Join-Path $rust 'bin'
$rustLib = Join-Path $rust 'lib\rustlib\x86_64-pc-windows-msvc\lib'
$suffixes = @('.rlib','.rmeta','.dll','.lib','.a')
$pins = [ordered]@{}
[long]$totalBytes = 0; $hostCount = 0; $rustCount = 0
foreach ($property in $prior.runtime_pins.psobject.Properties) {
    $path = $property.Name
    $parent = [IO.Path]::GetDirectoryName($path)
    $suffix = [IO.Path]::GetExtension($path)
    $isHost = [IO.Path]::GetPathRoot($path) -ieq 'C:\'
    $keep = $isHost -or ($directories.Contains($parent) -and $suffix -cin $suffixes) -or
        $path -ceq (Join-Path $rustBin 'rustc.exe') -or ($parent -ceq $rustBin -and $suffix -ceq '.dll') -or
        ($parent -ceq $rustLib -and $suffix -cin $suffixes)
    if (-not $keep) { continue }
    $row = Pin $path
    if ($row.sha256 -cne $property.Value) { throw ('RETAINED_RUNTIME_CHANGED:'+ $path) }
    $pins[$path] = $row.sha256; $totalBytes += $row.bytes
    if ($isHost) { $hostCount++ }
    if ($path.StartsWith($rust+'\',[StringComparison]::OrdinalIgnoreCase)) { $rustCount++ }
}
if ($pins.Count -ne 1071 -or $totalBytes -ne 2320491997 -or $hostCount -ne 98 -or $rustCount -ne 25) { throw 'EXACT_FILTERED_CLOSURE' }
$selected = [ordered]@{
    schema='DMKN_V5_AGGREGATE_STAGE_HOST_BUILD_V1';name=$name;authorizes_compile_only=$true
    sources=$sources;runtime_pins=$pins
    limits=[ordered]@{
        worker_cpu_seconds=240;worker_wall_seconds=300;memory_mib=3072;active_processes=6
        ordinary_controller_cpu_seconds=40;controller_cpu_seconds=60;total_wall_seconds=420
        fresh_output_bytes=536870912;fresh_output_entries=8192;command_log_bytes=1048576
    }
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected|ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=$selectionPath;pin=(Pin $selectionPath);sources=$sources.Count;runtime_pins=$pins.Count;runtime_bytes=$totalBytes;compiler_calls=1;proof_calls=0;executed=$false} | ConvertTo-Json -Depth 5
