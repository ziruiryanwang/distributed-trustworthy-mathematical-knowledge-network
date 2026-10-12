# Fresh exact build selection only. No Cargo, guest, native test or proof launch.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'bounded-parse-guest-build-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
foreach ($path in @($selectionPath,(Join-Path $local $name),(Join-Path $local ($name+'-attempt.json')))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer) { throw 'FILE_REQUIRED' }
    [ordered]@{bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$oldPath = Join-Path $local 'aggregate-guest-compile-01/SOURCE-MAP.json'
$nativePath = Join-Path $local 'bounded-parse-native-build-02/source-map.json'
if ((Pin $oldPath).sha256 -cne '75c710e3ee13f63cb6ef44da8656caa53c300bf649317d2b5669d8b9cde06ce0' -or (Pin $nativePath).sha256 -cne '5eed690e54ab6a42f8cc3da93c93901aae18c4c5ad441851df072dfd91f81f54') { throw 'PRIOR_MAP_PINS' }
$old = (Get-Content -LiteralPath $oldPath -Raw | ConvertFrom-Json).project
$native = Get-Content -LiteralPath $nativePath -Raw | ConvertFrom-Json
$sources = [ordered]@{}
$reused = @('input','foundation_static','foundation_data','commitments','journal','policy') | ForEach-Object {'software/v5/modules/receipt/src/'+$_+'.rs'}
$reused += @('header','membership','wire') | ForEach-Object {'software/v5/aggregate_claims/'+$_+'.rs'}
$reused += @('debug_printer','demand','env','expr','inductive','level','module','name','parser','pretty_printer','quot','tc','unique_hasher','util') | ForEach-Object {'software/v5/modules/native/checker/src/'+$_+'.rs'}
$reused += @('software/v5/modules/native/proof_validation/lib.rs','software/v5/modules/native/proof_validation/module_correspondence.rs','software/v5/aggregate/main.rs')
if ($reused.Count -ne 26) { throw 'EXACT_REUSED_SOURCE_SET' }
foreach ($relative in $reused) {
    $expected = $old.psobject.Properties[$relative].Value
    if ($null -eq $expected) { throw ('MISSING_PRIOR_SOURCE:'+ $relative) }
    $actual = Pin (Join-Path $projectRoot $relative)
    if ($actual.bytes -ne $expected.bytes -or $actual.sha256 -cne $expected.sha256) { throw ('UNCHANGED_SOURCE:'+ $relative) }
    $sources[$relative] = $actual
}
foreach ($file in @('canonical','module_relation','module_lib','census','aggregate_relation','aggregate_lib')) {
    $relative = 'software/v5/bounded_parse/'+$file+'.rs'
    $expected = $native.psobject.Properties[$relative].Value
    if ($null -eq $expected) { throw 'MISSING_ADOPTED_NATIVE_SOURCE' }
    $actual = Pin (Join-Path $projectRoot $relative)
    if ($actual.bytes -ne $expected.bytes -or $actual.sha256 -cne $expected.sha256) { throw ('NATIVE_SOURCE_CHANGED:'+ $relative) }
    $sources[$relative] = $actual
}
$fresh = [ordered]@{
    'Cargo.toml'='7eaa23cdc5aaf4c8fd1b8e1924a1cb4f702d7af8d04cdd06a33df23dfa5c0ad1'
    'module/Cargo.toml'='0435d18fdfb878290b291e62978643975fe2887c79873f50d6d4fa7332dba15c'
    'checker/Cargo.toml'='56364af430400d805de9be09d842b70e2f3bc3de9a14ff8082b18bcbcc1ff543'
    'graph.py'='090744c1b479474399912c2180e8cca8e1e12afe050689f6c310af4c57136c87'
    'build.py'='514b5f743ee7acef21c02719d98aa2b910e67a4966231527a1d4b83ac450f584'
}
foreach ($file in $fresh.Keys) {
    $relative = 'software/v5/bounded_parse_guest/'+$file
    $actual = Pin (Join-Path $projectRoot $relative)
    if ($actual.sha256 -cne $fresh[$file]) { throw ('FRESH_SOURCE_CHANGED:'+ $relative) }
    $sources[$relative] = $actual
}
if ($sources.Count -ne 37) { throw 'EXACT_37_SOURCES' }
$comparison = Join-Path $local 'bounded-parse-native-compare-01/RESULT.json'
$pin = Pin $comparison
if ($pin.bytes -ne 8960 -or $pin.sha256 -cne 'ddd411125b809fda24be93280329f6d7b7bd3d4b32ac5cbd71beab46e4948a20') { throw 'ADOPTED_NATIVE_RESULT' }
$selected = [ordered]@{
    schema='DMKN_V5_BOUNDED_PARSE_GUEST_BUILD_V1';name=$name;sources=$sources
    authorizes_guest_build_and_owned_telemetry_cleanup=$true
    native_comparison=[ordered]@{path=(Get-Item -LiteralPath $comparison).FullName;bytes=$pin.bytes;sha256=$pin.sha256}
    limits=[ordered]@{worker_cpu_seconds=480;worker_wall_seconds=600;memory_mib=4096;active_processes=8;controller_cpu_seconds=90;ordinary_controller_cpu_seconds=70;total_wall_seconds=780;fresh_output_bytes=3221225472;fresh_output_entries=32768;command_log_bytes=33554432}
}
$raw = [Text.UTF8Encoding]::new($false).GetBytes(($selected|ConvertTo-Json -Depth 12)+"`n")
$stream = [IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{selection=$selectionPath;pin=(Pin $selectionPath);sources=$sources.Count;cargo_calls=2;guest_calls=0;proof_calls=0;executed=$false} | ConvertTo-Json -Depth 5
