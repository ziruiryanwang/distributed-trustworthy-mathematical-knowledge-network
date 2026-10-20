# Select the existing builder with the exact tested withdrawal/pair successors.
# Creates fresh inputs only; does not execute a build or mutate an old install.
param([Parameter(Mandatory=$true)][string]$ReviewedBuilderSha)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) {
    (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Require-Digest([string]$path, [string]$expected) {
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or (Digest $path) -cne $expected) {
        throw ('REVIEWED_INPUT_CHANGED: '+$path)
    }
}
function New-Json([string]$path, $value) {
    $raw = [Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 64)+"`n")
    if ($raw.Length -gt 8*1024*1024) { throw 'JSON_BOUND' }
    $stream = [IO.File]::Open($path, [IO.FileMode]::CreateNew,
        [IO.FileAccess]::Write, [IO.FileShare]::None)
    try { $stream.Write($raw, 0, $raw.Length); $stream.Flush($true) }
    finally { $stream.Dispose() }
}
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$basisPath = Join-Path $checks 'distribution-interface-01-input.json'
Require-Digest $basisPath 'a0d5fad85893bdda55ae10530cd59bc513d4fe90654a2b0661aad624793159b2'
$basis = Get-Content -LiteralPath $basisPath -Raw | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or
    $basis.base_role -cne 'mathematical-client-location-v1') { throw 'INPUT_BASIS' }
$sources = [ordered]@{}
foreach ($property in $basis.sdk_sources.psobject.Properties) {
    $sources[$property.Name] = $property.Value
}
if ($sources.Count -ne 108) { throw 'BASIS_SDK_CENSUS' }
$overlays = @(
    @('v5/admission/trust.py','trust_withdrawal/admission/trust.py','a60fd123845c7cd732967f995363b3132ebab1522cd90870ab728e6a54dd83ee'),
    @('v5/admission/verifier.py','trust_withdrawal/admission/verifier.py','01fb93b5d0063110fe82978dcc8a593557b34eaa8b6497f596715ca65064e38c'),
    @('v5/aggregate_claims/aggregate_admission.py','trust_withdrawal/aggregate_claims/aggregate_admission.py','2ef830f849ff214b4e4b3c314332d8d3d3d23844c1a763828e1be5a5f37732aa'),
    @('v5/client/runtime.py','trust_withdrawal/client/runtime.py','70c52b5148c481ca840c6c55557c9bc5abf71f40d522365f0cb7b0398adbad39'),
    @('v5/client/remote_reader.py','trust_withdrawal/client/remote_reader.py','f8859ad37eb70d14016cec119a5b9114e19f11c7b74aa9a6c34eb87987c780eb'),
    @('v5/discovery/formal_features.py','conjunction_index/discovery/formal_features.py','3ae3fd9abb4e63124120c936f4b3805e7bcda9e95194497b2fe25b7e5e8623ba'),
    @('v5/discovery/authenticated_index.py','conjunction_index/discovery/authenticated_index.py','6c5ba1e563f26353b5d42da07558cb53a1a680e6258acc506291333bd3f17a20'),
    @('v5/discovery/discovery_store.py','conjunction_index/discovery/discovery_store.py','c62f357d64ab52959e8d732d89dd8b92d434313a95cdec128f096235bb2c80c4'),
    @('v5/discovery/module_export_adapter.py','conjunction_index/discovery/module_export_adapter.py','d1e8a437dec4ebe218ab1cc74e8e4bddd91ab4ade77f60e42dac9decb0d2c658'),
    @('v5/client/workspace_evidence.py','conjunction_index/client/workspace_evidence.py','233562c663c3633e126b6761d10542e48be9145edba8b3fb731a8eafbf9c2baa'),
    @('v5/client/workspace_atomic.py','conjunction_index/client/workspace_atomic.py','eea95a6bb12349e5fc7b1e80bc610710ccafc7cbbfd2b40d705d80cdc67c8022'),
    @('v5/client/direct_contacts.py','conjunction_index/client/direct_contacts.py','88ce2581a7432421e2619c57ad0645f29f66d400f94c5d12db8c74c5f3d78e51')
)
$replaced = 0; $added = 0
foreach ($overlay in $overlays) {
    $key, $relative, $expected = $overlay
    if ($sources.Contains($key)) { $replaced++ } else { $added++ }
    $path = Join-Path $projectRoot ('software/v5/'+$relative)
    Require-Digest $path $expected
    $sources[$key] = [ordered]@{path=$path; bytes=(Get-Item -LiteralPath $path).Length; sha256=$expected}
}
if ($sources.Count -ne 109 -or $replaced -ne 11 -or $added -ne 1) { throw 'SDK_DELTA_CENSUS' }
# Verify every retained input against its immutable byte pin. No import occurs.
foreach ($key in $sources.Keys) {
    $row = $sources[$key]
    Require-Digest $row.path $row.sha256
    if ((Get-Item -LiteralPath $row.path).Length -ne $row.bytes) { throw ('SDK_SIZE: '+$key) }
}
$sourceKey = 'software/v5/distribution_coherent/distribution.py'
$builder = Join-Path $projectRoot $sourceKey
Require-Digest $builder $ReviewedBuilderSha
$basis.sdk_sources = $sources
$basis.distribution_source = [ordered]@{path=$builder; bytes=(Get-Item -LiteralPath $builder).Length; sha256=$ReviewedBuilderSha}
$buildBasisPath = Join-Path $checks 'distribution-interface-build-01-selection.json'
Require-Digest $buildBasisPath '91cd374c422c9c6008054c2abc72fe2cd75fcc46d5252e200adf8f731c9dcae1'
$buildBasis = Get-Content -LiteralPath $buildBasisPath -Raw | ConvertFrom-Json
$runtime = [ordered]@{}
foreach ($property in $buildBasis.runtime_pins.psobject.Properties) {
    Require-Digest $property.Name $property.Value
    $runtime[$property.Name] = $property.Value
}
$buildSources = [ordered]@{'tools/Run-V5-Check.py'='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'}
$buildSources[$sourceKey] = $ReviewedBuilderSha
foreach ($key in $buildSources.Keys) { Require-Digest (Join-Path $projectRoot $key) $buildSources[$key] }
$name = 'distribution-coherent-build-01'
$inputPath = Join-Path $checks 'distribution-coherent-01-input.json'
$selectionPath = Join-Path $checks ($name+'-selection.json')
$parent = Join-Path $projectRoot 'product-local\v5-distribution-coherent-01'
foreach ($path in @($inputPath, $selectionPath, $parent, (Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED: '+$path) }
}
New-Json $inputPath $basis
$inputSha = Digest $inputPath
$runtime[$inputPath] = $inputSha
$selected = [ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1'; name=$name; sources=$buildSources; runtime_pins=$runtime
    argv=@($buildBasis.argv[0], '-I', '-S', '-B',
        '{snapshot}\software\v5\distribution_coherent\distribution.py',
        'build', $inputPath, $inputSha, (Join-Path $parent 'Mathematical Commons v5'))
    limits=[ordered]@{cpu_seconds=120; wall_seconds=300; memory_mib=128; active_processes=2; stdout_bytes=1048576; stderr_bytes=1048576}
}
New-Json $selectionPath $selected
[void][IO.Directory]::CreateDirectory($parent)
[ordered]@{input=$inputPath; input_sha256=$inputSha; selection=$selectionPath;
    selection_sha256=(Digest $selectionPath); sdk_sources=$sources.Count;
    replaced=$replaced; added=$added; installation_parent=$parent;
    parent_created=$true; build_executed=$false} | ConvertTo-Json
