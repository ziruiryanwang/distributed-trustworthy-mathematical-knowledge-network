# Root-only preparation: explicit current adoption of retained intermediates.
# No compiler, Cargo, guest, image assembler or prover is invoked here.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$BuildSourceSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$RecipesSourceSha256
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'bounded-parse-direct-build-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $local $name),(Join-Path $local ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) { throw 'ORDINARY_FILE_REQUIRED' }
    [ordered]@{bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$adapters = [ordered]@{}
$expected = [ordered]@{
    'software/v5/bounded_parse_guest/build_projects.py'=$BuildSourceSha256
    'software/v5/bounded_parse_guest/recipes.py'=$RecipesSourceSha256
}
foreach ($relative in $expected.Keys) {
    $row = Pin (Join-Path $projectRoot $relative)
    if ($row.sha256 -cne $expected[$relative]) { throw ('SOURCE_CHANGED:'+ $relative) }
    $adapters[$relative] = $row
}
$old = Join-Path $local 'aggregate-guest-compile-01'
$stdout = Join-Path $old 'commands\build-aggregate-guest\stdout.txt'
if ((Pin $stdout).sha256 -cne '8e54baefabfa6abc5461af0b6a9b126960203df9bf4e45ae9a9feccd4ad0328b') { throw 'RETAINED_CARGO_ARTIFACT_RECORDS' }
$libraryRoot = Join-Path $old 'target\riscv32im-risc0-zkvm-elf\release\deps'
$macroRoot = Join-Path $old 'target\release\deps'
$retained = [ordered]@{}
$libraryCount = 0; $macroCount = 0; $scriptCount = 0; $finished = 0
[long]$libraryBytes = 0; [long]$totalBytes = 0
foreach ($line in [IO.File]::ReadLines($stdout)) {
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    $row = $line | ConvertFrom-Json
    if ($row.reason -ceq 'build-finished') {
        if ($row.success -ne $true) { throw 'COMPILER_DID_NOT_FINISH' }
        $finished++; continue
    }
    if ($row.reason -ceq 'build-script-executed') {
        if ($row.linked_libs.Count -ne 0 -or $row.linked_paths.Count -ne 0) { throw 'UNRESOLVED_NATIVE_LINK_INPUT' }
        $scriptCount++; continue
    }
    if ($row.reason -cne 'compiler-artifact') { continue }
    $kind = $row.target.kind -join ','
    $paths = @()
    $isLibrary = $false
    if (($kind -ceq 'lib' -or $kind -ceq 'rlib') -and $row.filenames.Count -eq 2) {
        $candidate = @($row.filenames | Where-Object { [IO.Path]::GetDirectoryName($_) -ceq $libraryRoot })
        if ($candidate.Count -ne 2) { continue }
        if ($row.target.name -cin @('dmkn_module_relation','dmkn_aggregate_relation')) { continue }
        if (@($candidate | Where-Object { [IO.Path]::GetExtension($_) -ceq '.rlib' }).Count -ne 1 -or
            @($candidate | Where-Object { [IO.Path]::GetExtension($_) -ceq '.rmeta' }).Count -ne 1 -or
            [IO.Path]::GetFileNameWithoutExtension($candidate[0]) -cne [IO.Path]::GetFileNameWithoutExtension($candidate[1])) { throw 'MATCHED_LIBRARY_PAIR' }
        $paths = $candidate; $isLibrary = $true; $libraryCount++
    } elseif ($kind -ceq 'proc-macro') {
        $paths = @($row.filenames | Where-Object { [IO.Path]::GetExtension($_) -ceq '.dll' })
        if ($paths.Count -ne 1 -or [IO.Path]::GetDirectoryName($paths[0]) -cne $macroRoot) { throw 'EXACT_MACRO_DLL' }
        $macroCount++
    }
    foreach ($path in $paths) {
        if ($retained.Contains($path)) { throw 'DUPLICATE_ARTIFACT' }
        $pin = Pin $path
        $retained[$path] = $pin; $totalBytes += $pin.bytes
        if ($isLibrary) { $libraryBytes += $pin.bytes }
    }
}
if ($libraryCount -ne 108 -or $macroCount -ne 22 -or $retained.Count -ne 238 -or
    $scriptCount -ne 41 -or $finished -ne 1 -or $libraryBytes -ne 281325788 -or $totalBytes -ne 320499420) { throw 'EXACT_RETAINED_CLOSURE' }
$selected = [ordered]@{
    schema='DMKN_V5_BOUNDED_PARSE_DIRECT_PROJECT_BUILD_V1';name=$name
    adapters=$adapters;retained_artifacts=$retained
    authorizes_three_compiles_and_retained_artifact_adoption=$true
    limits=[ordered]@{
        worker_cpu_seconds=240;worker_wall_seconds=300;memory_mib=4096;active_processes=6
        ordinary_controller_cpu_seconds=40;controller_cpu_seconds=60;total_wall_seconds=420
        fresh_output_bytes=536870912;fresh_output_entries=4096;command_log_bytes=8388608
    }
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected|ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=$selectionPath;pin=(Pin $selectionPath);adapters=$adapters.Count;adopted_artifact_files=$retained.Count;adopted_artifact_bytes=$totalBytes;compiler_calls=3;cargo_calls=0;guest_calls=0;proof_calls=0;executed=$false} | ConvertTo-Json -Depth 5
