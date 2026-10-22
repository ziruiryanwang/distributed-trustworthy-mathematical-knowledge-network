# File-only preparation. No build, service or mathematical operation is run.
param([Parameter(Mandatory=$true)][string]$ReviewedSourcesJson)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
function CheckPin([string]$path,[string]$expected) {
    $item=Get-Item -LiteralPath $path
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or $item.PSIsContainer -or
        (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) -or
        (Digest $path) -cne $expected) { throw ('REVIEWED_PIN_CHANGED:'+ $path) }
}
function NewJson([string]$path,$value) {
    $raw=[Text.UTF8Encoding]::new($false).GetBytes(($value | ConvertTo-Json -Depth 64)+"`n")
    if ($raw.Length -gt 8*1024*1024) { throw 'JSON_BOUND' }
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
}
$checks=Join-Path $projectRoot 'experiments/v5-local-checks'
$basisPath=Join-Path $checks 'distribution-managed-storage-01-input.json'
CheckPin $basisPath 'a629df82718f6a9d0560cacbfdc459739c15a56a1f2a46dd87929a1db51c22a4'
$basis=Get-Content -LiteralPath $basisPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($basis.schema -cne 'DMKN_V5_DISTRIBUTION_INPUT_V3' -or
    $basis.base_role -cne 'mathematical-client-location-v1') { throw 'INPUT_BASIS' }
$sources=[ordered]@{}
foreach ($row in $basis.sdk_sources.psobject.Properties) {
    CheckPin $row.Value.path $row.Value.sha256
    if ((Get-Item -LiteralPath $row.Value.path).Length -ne $row.Value.bytes) { throw 'BASIS_SOURCE_SIZE' }
    $sources[$row.Name]=$row.Value
}
if ($sources.Count -ne 129) { throw 'EXACT_BASIS_129' }
$required=@('evidence_network/transport.py','placement/controller.py','client/workspace_evidence.py',
            'client/workspace_staged.py','client/semantic_reader.py','client/managed_owner.py')
if ($ReviewedSourcesJson.Length -gt 16384) { throw 'REVIEWED_MAP_BOUND' }
$reviewed=$ReviewedSourcesJson | ConvertFrom-Json
$keys=@($reviewed.psobject.Properties.Name)
if ($keys.Count -ne 6 -or @(Compare-Object $keys $required -CaseSensitive).Count -ne 0) { throw 'EXACT_REVIEWED_SET' }
foreach ($name in $required) {
    $logical='v5/'+$name
    if (-not $sources.Contains($logical)) { throw 'REPLACEMENT_MUST_EXIST' }
    $path=Join-Path $projectRoot ('software/v5/exact_packet/'+$name)
    CheckPin $path $reviewed.$name
    $sources[$logical]=[ordered]@{path=$path;bytes=(Get-Item -LiteralPath $path).Length;sha256=$reviewed.$name}
}
if ($sources.Count -ne 129 -or
    @($sources.Keys | Where-Object {$_.StartsWith('v5/',[StringComparison]::Ordinal)}).Count -ne 108) { throw 'EXACT_MAP' }
$builder='software/v5/body_location/distribution.py'
$builderSha='eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813'
if ($basis.distribution_source.path -cne (Join-Path $projectRoot $builder) -or
    $basis.distribution_source.sha256 -cne $builderSha) { throw 'BUILDER_BASIS' }
CheckPin (Join-Path $projectRoot $builder) $builderSha
$basis.sdk_sources=$sources
$buildBasisPath=Join-Path $checks 'distribution-managed-storage-build-01-selection.json'
CheckPin $buildBasisPath '4df4b09b82c00e4ad70351eeb385b6d6a900fdaf70565b41c716400ee0246f54'
$buildBasis=Get-Content -LiteralPath $buildBasisPath -Raw -Encoding UTF8 | ConvertFrom-Json
$runtime=[ordered]@{}
foreach ($row in $buildBasis.runtime_pins.psobject.Properties) {
    if ($row.Name -ceq $basisPath) { continue }
    CheckPin $row.Name $row.Value
    $runtime[$row.Name]=$row.Value
}
$runner='tools/Run-V5-Check.py'
$runnerSha='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
CheckPin (Join-Path $projectRoot $runner) $runnerSha
if ($runtime.Count -ne 28 -or -not $runtime.Contains($buildBasis.argv[0])) { throw 'EXACT_RUNTIME' }
$name='distribution-exact-packet-build-01'
$inputPath=Join-Path $checks 'distribution-exact-packet-01-input.json'
$selectionPath=Join-Path $checks ($name+'-selection.json')
$parent=Join-Path $projectRoot 'product-local/v5-distribution-exact-packet-01'
foreach ($path in @($inputPath,$selectionPath,$parent,(Join-Path $checks $name))) {
    if (Test-Path -LiteralPath $path) { throw ('FRESH_OUTPUT_REQUIRED:'+ $path) }
}
NewJson $inputPath $basis
$inputSha=Digest $inputPath; $runtime[$inputPath]=$inputSha
$buildSources=[ordered]@{}
$buildSources[$runner]=$runnerSha; $buildSources[$builder]=$builderSha
$selection=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$buildSources;runtime_pins=$runtime
    argv=@($buildBasis.argv[0],'-I','-S','-B','{snapshot}\software\v5\body_location\distribution.py',
           'build',$inputPath,$inputSha,(Join-Path $parent 'Mathematical Commons v5'))
    limits=[ordered]@{cpu_seconds=120;wall_seconds=600;memory_mib=128;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
NewJson $selectionPath $selection
[void][IO.Directory]::CreateDirectory($parent)
[ordered]@{input=$inputPath;input_sha256=$inputSha;selection=$selectionPath;
    selection_sha256=(Digest $selectionPath);sdk_sources=129;preparation_sources=108;
    replaced=6;added=0;unchanged=123;installation_parent=$parent;build_executed=$false} | ConvertTo-Json
