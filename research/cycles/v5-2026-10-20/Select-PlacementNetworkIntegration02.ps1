# Prepare one exact fresh integration; does not execute it.
param([Parameter(Mandatory=$true)][string]$ReviewedNetworkJson,
      [Parameter(Mandatory=$true)][string]$ReviewedIntegrationSha)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Exact([string]$path,[string]$digest) {
    if ($digest -cnotmatch '^[0-9a-f]{64}$' -or (Digest $path) -cne $digest) { throw ('SOURCE_PIN:'+ $path) }
}
function File-Row([string]$path) {
    $path = [IO.Path]::GetFullPath($path)
    [ordered]@{path=$path;bytes=(Get-Item -LiteralPath $path).Length;sha256=(Digest $path)}
}
function Save-New([string]$path,$value) {
    $raw = [Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 30)+"`n")
    if ($raw.Length -gt 1048576) { throw 'INPUT_BYTE_BOUND' }
    $stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) } finally { $stream.Dispose() }
}
$checks = Join-Path $projectRoot 'experiments/v5-local-checks'
$name = 'placement-network-integration-02'
$inputPath = Join-Path $checks ($name+'-input.json')
$selectionPath = Join-Path $checks ($name+'-selection.json')
foreach ($path in @($inputPath,$selectionPath,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw 'FRESH_SELECTION_REQUIRED' }
}
$mapPath = Join-Path $checks 'distribution-terminal-i-01-input.json'
Exact $mapPath 'd3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0'
$map = Get-Content -LiteralPath $mapPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ((Get-Item -LiteralPath $mapPath).Length -ne 2805479 -or @($map.sdk_sources.psobject.Properties).Count -ne 114) { throw 'CURRENT_MAP' }
$sources = [ordered]@{}
$runner = 'tools/Run-V5-Check.py'
$runnerSha = '44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
Exact (Join-Path $projectRoot $runner) $runnerSha
$sources[$runner] = $runnerSha
foreach ($property in $map.sdk_sources.psobject.Properties) {
    $row = $property.Value
    $path = [IO.Path]::GetFullPath($row.path)
    if (-not $path.StartsWith($projectRoot+'\software\v5\',[StringComparison]::Ordinal)) { throw 'SOURCE_SCOPE' }
    Exact $path $row.sha256
    if ((Get-Item -LiteralPath $path).Length -ne $row.bytes) { throw 'SOURCE_SIZE' }
    $relative = $path.Substring($projectRoot.Length+1).Replace('\','/')
    if ($sources.Contains($relative)) { throw 'DUPLICATE_SOURCE' }
    $sources[$relative] = $row.sha256
}
$qualified = [ordered]@{
    'standalone_validation/admission/pin_phase.py'='ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881'
    'standalone_validation/mixed_claims/imports_atomic.py'='8a8313376d736f25a45b6089f491373bc7e0206aa77b539dbff077fc4eb92595'
    'incremental_native/mixed_claims/receiver.py'='5436569971c272b129fbaec480d51d57a1ec521d43fd4d4ad14133b786691d5b'
    'selective_placement/discovery/discovery_store.py'='1c8543d4903754174b80d107ee923116ddb402d41a3b5af3f1d255abdfc6a328'
    'selective_placement/placement/__init__.py'='8fe08470d7fd15e96d1305f0e49a8b359cb53ce0c542bf7473b68d869159112e'
    'selective_placement/placement/codec.py'='6f32569d4807f96130350b85233161603f6860f082c75f81a8bfacf4f0a58999'
    'selective_placement/placement/ledger.py'='d955990c347ed466617c752893dded8b8494dd266a050b045352c77c48f21a91'
    'selective_placement/placement/controller.py'='ef1c9b59072127379e955bafeea001a22d6e3d10c9c46dca1304f85ab09e2b49'
    'examples/mirror_method/method_query.py'='0ddbc8dac7e60180f3f9aad3216873158d8b2722a9d31c48112e20262298c642'
    'examples/terminal_i/congruence_query.py'='07a323edd3b10f94f6fc7f9790191b1145666b547b4575c70c4a7261b3d8fadd'
}
foreach ($relative in $qualified.Keys) {
    $nameInRoot = 'software/v5/'+$relative
    if ($sources.Contains($nameInRoot)) { throw 'QUALIFIED_SOURCE_COLLISION' }
    Exact (Join-Path $projectRoot $nameInRoot) $qualified[$relative]
    $sources[$nameInRoot] = $qualified[$relative]
}
if ($ReviewedNetworkJson.Length -gt 16384) { throw 'REVIEWED_MAP_BOUND' }
$reviewed = $ReviewedNetworkJson | ConvertFrom-Json
$networkPaths = [ordered]@{
    'placement/network.py'='placement_network/placement/network.py'
    'placement/advertisement.py'='placement_network/placement/advertisement.py'
    'client/serve_placement.py'='placement_network02/client/serve_placement.py'
}
$networkKeys = @($networkPaths.Keys)
$keys = @($reviewed.psobject.Properties.Name)
if ($keys.Count -ne 3 -or @(Compare-Object $keys $networkKeys -CaseSensitive).Count -ne 0) { throw 'NETWORK_SOURCE_SET' }
$network = [ordered]@{}
foreach ($key in $networkKeys) {
    $relative = 'software/v5/'+$networkPaths[$key]
    $path = Join-Path $projectRoot $relative
    Exact $path $reviewed.$key
    $network[$key] = File-Row $path
    $sources[$relative] = $reviewed.$key
}
$adapter = 'software/v5/placement_network02/integration.py'
Exact (Join-Path $projectRoot $adapter) $ReviewedIntegrationSha
$sources[$adapter] = $ReviewedIntegrationSha
if ($sources.Count -ne 129) { throw 'PHYSICAL_SOURCE_COUNT' }
$installed = Join-Path $projectRoot 'product-local/v5-distribution-terminal-i-01/Mathematical Commons v5'
$originalPath = Join-Path $projectRoot 'product-local/v5-distribution-terminal-i-01/terminal-i01-inputs/installed-terminal-i-01-request.json'
Exact $originalPath '9df159b6b10b8e14b4b36bfd0557cba8790c278224a7c318bd03e888d61a7565'
$original = Get-Content -LiteralPath $originalPath -Raw -Encoding UTF8 | ConvertFrom-Json
$basisPath = Join-Path $checks 'incremental-native-integration-02-selection.json'
Exact $basisPath 'a88998e58082bfadc92378367fef52c644dadf1681e707219f771e9ce16e1c6f'
$basis = Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
$python = $basis.argv[0]; $pythonRoot = [IO.Path]::GetDirectoryName($python)
$runtime = [ordered]@{}; $pythonRows = @()
foreach ($property in $basis.runtime_pins.psobject.Properties) {
    if ($property.Name.StartsWith($pythonRoot+'\',[StringComparison]::Ordinal)) {
        Exact $property.Name $property.Value
        $runtime[$property.Name] = $property.Value
        $pythonRows += ,(File-Row $property.Name)
    }
}
if ($runtime.Count -ne 18 -or -not $runtime.Contains($python)) { throw 'PYTHON_CLOSURE' }
$supervisor = File-Row (Join-Path $installed 'base/RELEASE-MANIFEST.json')
if ($supervisor.sha256 -cne 'a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed') { throw 'SUPERVISOR_PIN' }
$executable = File-Row (Join-Path $installed 'assets/receipt/module_host.exe')
if ($basis.runtime_pins.($executable.path) -cne $executable.sha256) { throw 'QUALIFIED_RECEIPT_EXECUTABLE' }
$inputValue = [ordered]@{
    schema='DMKN_PLACEMENT_NETWORK_INTEGRATION_INPUT_V1'; map=(File-Row $mapPath)
    network_sources=$network; installation=$installed; supervisor_manifest=$supervisor
    receipt_executable=$executable; python_runtime=$pythonRows
    receipt=$original.parameters.receipt; journal=$original.parameters.journal; bundle=$original.parameters.bundle
    workspace_config=$original.parameters.workspace_config
}
foreach ($row in @($supervisor,$executable,$inputValue.receipt,$inputValue.journal,$inputValue.bundle)) {
    Exact $row.path $row.sha256
    if ((Get-Item -LiteralPath $row.path).Length -ne $row.bytes) { throw 'EXACT_INPUT_SIZE' }
    $runtime[$row.path] = $row.sha256
}
Save-New $inputPath $inputValue
$runtime[$mapPath] = (Digest $mapPath)
$runtime[$inputPath] = (Digest $inputPath)
if ($runtime.Count -ne 25) { throw 'RUNTIME_PIN_COUNT' }
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($python,'-I','-S','-B',('{snapshot}\'+$adapter.Replace('/','\')),'--output','{output}','--input',$inputPath)
    limits=[ordered]@{cpu_seconds=150;wall_seconds=300;memory_mib=512;active_processes=6;stdout_bytes=1048576;stderr_bytes=1048576}
}
Save-New $selectionPath $selected
[ordered]@{path=$selectionPath;sha256=(Digest $selectionPath);input=$inputPath;input_sha256=(Digest $inputPath);
    sources=$sources.Count;runtime_pins=$runtime.Count;executed=$false} | ConvertTo-Json
