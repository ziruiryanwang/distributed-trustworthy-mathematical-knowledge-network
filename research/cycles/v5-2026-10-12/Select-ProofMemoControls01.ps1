# Prepare one changed-boundary serde-only build/test; does not execute it.
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'proof-memo-controls-01'
$selectionPath = Join-Path $local ($name+'-selection.json')
$configPath = Join-Path $local ($name+'-configuration.json')
foreach ($path in @($selectionPath,$configPath,(Join-Path $local $name))) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer) { throw 'FILE_REQUIRED' }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
function SaveNew([string]$path,$value) {
    $raw = [Text.UTF8Encoding]::new($false).GetBytes(($value|ConvertTo-Json -Depth 15)+"`n")
    $stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
}
$sources = [ordered]@{}
foreach ($relative in @('tools/Run-V5-Check.py') + @('module_correspondence.rs','correspondence_controls.rs','control_root.rs','control.py' | ForEach-Object {'software/v5/modules/native/proof_memo/'+$_})) {
    $sources[$relative] = (Pin (Join-Path $projectRoot $relative)).sha256
}
if ($sources['tools/Run-V5-Check.py'] -cne '44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651') { throw 'SUPERVISOR_CHANGED' }
$pins = [ordered]@{}
$recipePath = Join-Path $projectRoot 'software\v5\delta\NATIVE-BUILD02-PROPOSAL.json'
if ((Pin $recipePath).sha256 -cne 'b0d037459b950c3cbabd1c2554aebf1fe9611820598d370eb40f4d69e700885d') { throw 'RETAINED_RECIPE' }
$recipe = Get-Content -LiteralPath $recipePath -Raw | ConvertFrom-Json
foreach ($property in $recipe.runtime_pins_rechecked.psobject.Properties) {
    if ((Pin $property.Name).sha256 -cne $property.Value) { throw ('RUNTIME_CHANGED:'+ $property.Name) }
    $pins[$property.Name] = $property.Value
}
if ($pins.Count -ne 174) { throw 'RETAINED_RUNTIME_CLOSURE' }
$priorPath = Join-Path $local 'bounded-parse-pc-attribution-01-selection.json'
if ((Pin $priorPath).sha256 -cne '8d4ece90a22f79702778e88edc85da14f7204c04c5cb4aa72577349d6b9c0968') { throw 'ADOPTED_PYTHON_SELECTION' }
$prior = Get-Content -LiteralPath $priorPath -Raw | ConvertFrom-Json
$pythonRoot = Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\receiver\runtime\python'
foreach ($property in $prior.runtime_pins.psobject.Properties) {
    if (-not $property.Name.StartsWith($pythonRoot+'\',[StringComparison]::OrdinalIgnoreCase)) { continue }
    if ((Pin $property.Name).sha256 -cne $property.Value) { throw 'PYTHON_RUNTIME_CHANGED' }
    $pins[$property.Name] = $property.Value
}
$records = [ordered]@{
    'proof-validation-controls-01/compile-and-test-commands.json'='6c4c3767f45a4a7f44410ade8880d76bbba24bf6ecbddfbe3ea8f4a1aec28244'
    'proof-validation-controls-01/environment-profile.json'='34525808d26848e9582ad5ada38ff66fae2205f79ae0421a33f72fbd67af4e18'
    'bounded-parse-aggregate-snapshot-01/evidence/diagnostic.json'='dca409e07e44f7647c2b248167cadcba6f5ad0827af83a3aa3173e0aee0bda72'
}
foreach ($relative in $records.Keys) {
    $row = Pin (Join-Path $local $relative)
    if ($row.sha256 -cne $records[$relative]) { throw 'RETAINED_RECORD_CHANGED' }
    $pins[$row.path] = $row.sha256
}
$profile = Get-Content -LiteralPath (Join-Path $local 'proof-validation-controls-01/environment-profile.json') -Raw | ConvertFrom-Json
foreach ($record in $profile.host_binaries) {
    $row = Pin $record.path
    if ($row.bytes -ne $record.bytes -or $row.sha256 -cne $record.sha256) { throw 'HOST_TOOL_CHANGED' }
    $pins[$row.path] = $row.sha256
}
$diagnostic = Get-Content -LiteralPath (Join-Path $local 'bounded-parse-aggregate-snapshot-01/evidence/diagnostic.json') -Raw | ConvertFrom-Json
$wire = Pin (Join-Path $local 'bounded-parse-aggregate-snapshot-01/evidence/wire.bin')
if ($wire.bytes -ne $diagnostic.wire_bytes -or $wire.sha256 -cne $diagnostic.wire_sha256) { throw 'EXACT_RETAINED_WIRE' }
$pins[$wire.path] = $wire.sha256
$testSource = Get-Content -LiteralPath (Join-Path $projectRoot 'software/v5/modules/native/proof_memo/correspondence_controls.rs') -Raw
$tests = @([regex]::Matches($testSource,'(?m)#\[test\]\s*fn\s+([a-z0-9_]+)\s*\(') | ForEach-Object {$_.Groups[1].Value})
if ($tests.Count -lt 1 -or $tests.Count -gt 32 -or @($tests | Sort-Object -Unique).Count -ne $tests.Count) { throw 'TEST_LIST' }
$config = [ordered]@{schema='DMKN_PROOF_MEMO_CONTROLS_V1';tests=$tests;wire=$wire.path}
SaveNew $configPath $config
$configPin = Pin $configPath
foreach ($path in @($configPath,$recipePath,$priorPath,(Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4\RELEASE-MANIFEST.json'))) {
    $row = Pin $path; $pins[$row.path] = $row.sha256
}
if ($pins.Count -gt 256) { throw 'OUTER_PIN_BOUND' }
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$pins
    argv=@((Join-Path $pythonRoot 'python.exe'),'-I','-S','-B','{snapshot}\software\v5\modules\native\proof_memo\control.py',$configPath,$configPin.sha256)
    limits=[ordered]@{cpu_seconds=60;wall_seconds=120;memory_mib=1024;active_processes=6;stdout_bytes=1048576;stderr_bytes=1048576}
}
SaveNew $selectionPath $selected
[ordered]@{selection=(Pin $selectionPath);configuration=$configPin;sources=$sources.Count;runtime_pins=$pins.Count;tests=$tests;guest_calls=0;proof_calls=0;executed=$false} | ConvertTo-Json -Depth 5
