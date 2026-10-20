# Stage one execution-only screen through the existing bounded local runner.
param([Parameter(Mandatory=$true)][string]$ReviewedAdapterSha)
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Require-Digest([string]$path,[string]$expected) {
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or (Digest $path) -cne $expected) { throw ('PIN_CHANGED: '+$path) }
}
function Pin([string]$path,[string]$expected) {
    Require-Digest $path $expected
    [ordered]@{path=$path;bytes=(Get-Item -LiteralPath $path).Length;sha256=$expected}
}
function New-Json([string]$path,$value) {
    $raw=[Text.UTF8Encoding]::new($false).GetBytes(($value|ConvertTo-Json -Depth 24)+"`n")
    if ($raw.Length -gt 1048576) { throw 'STAGED_BOUND' }
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
}
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$parent=Join-Path $projectRoot 'product-local\v5-distribution-interface-01'
$install=Join-Path $parent 'Mathematical Commons v5'
$prepPath=Join-Path $parent 'evaluator-operations\installed-evaluator-method-01-request\preparation.json'
Require-Digest $prepPath 'edfd3b4aa8697c29c7338b4e24a95cefda262e2c29876ecbcc1bc625c14b5718'
$prep=Get-Content -LiteralPath $prepPath -Raw|ConvertFrom-Json
$mapPath=Join-Path $checks 'distribution-interface-01-input.json'
Require-Digest $mapPath 'a0d5fad85893bdda55ae10530cd59bc513d4fe90654a2b0661aad624793159b2'
$map=Get-Content -LiteralPath $mapPath -Raw|ConvertFrom-Json
$sources=[ordered]@{}
foreach($relative in @('modules/__init__.py','modules/codec.py','modules/model.py',
    'modules/native_rows.py','modules/receipt/__init__.py','modules/receipt/witness.py')) {
    $row=$map.sdk_sources.('v5/'+$relative)
    $sourceKey='software/v5/'+$relative
    Require-Digest (Join-Path $projectRoot $sourceKey) $row.sha256
    $sources[$sourceKey]=$row.sha256
}
$sources['tools/Run-V5-Check.py']='44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651'
$sources['software/v5/evaluator_method/snapshot.py']=$ReviewedAdapterSha
foreach($p in $sources.GetEnumerator()) {Require-Digest (Join-Path $projectRoot $p.Key) $p.Value}
$runtime=[ordered]@{}
foreach($row in @($prep.producer.python,$prep.producer.python_dll)+@($prep.producer.runtime_pins)) {
    Require-Digest $row.path $row.sha256
    if (-not $row.path.StartsWith($install+'\',[StringComparison]::Ordinal)) {throw 'INSTALLED_RUNTIME_SCOPE'}
    $runtime[$row.path]=$row.sha256
}
$work=Join-Path $parent 'evaluator-operations\installed-evaluator-method-01\work'
$name='evaluator-snapshot-01'
$configPath=Join-Path $checks ($name+'-input.json')
$selectionPath=Join-Path $checks ($name+'-selection.json')
$output=Join-Path $checks $name
foreach($path in @($configPath,$selectionPath,$output)) {
    if(Test-Path -LiteralPath $path){throw ('FRESH_OUTPUT_REQUIRED: '+$path)}
}
$config=[ordered]@{
    schema='DMKN_EVALUATOR_SNAPSHOT_SCREEN_V1'
    host=(Pin (Join-Path $install 'assets\receipt\module_host.exe') '74a58215351a641d9efbbffbc389b5faea350c46f5c1e1a48bf76cf77b99d6c9')
    image=(Pin (Join-Path $install 'assets\image\module_image.bin') 'd76f623bb1de5c840fd2ef9c1ac35fc6aba2de74cda0f62c11c161f6973da31f')
    witness=(Pin (Join-Path $work 'method-witness.json') '8b84084486b0aadceb9ee353a28654b2777e297a726693135c575d5c50e85f5a')
    receipt=(Pin (Join-Path $checks 'module-base-production-01\finish-0\receipt.bin') '850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47')
    accepted_result=(Pin (Join-Path $work 'evaluator-method-result.json') 'adc7fe79bf6870c01c00df4fdd68567129b3d20217c938a4b125d8b7616ac9e3')
    output=(Join-Path $output 'evidence')
}
foreach($key in @('host','image','witness','receipt','accepted_result')) {
    $row=$config[$key];$runtime[$row.path]=$row.sha256
}
New-Json $configPath $config
$configSha=Digest $configPath
$runtime[$configPath]=$configSha
$selection=[ordered]@{
    schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($prep.producer.python.path,'-I','-S','-B',
        '{snapshot}\software\v5\evaluator_method\snapshot.py',$configPath,$configSha)
    limits=[ordered]@{cpu_seconds=120;wall_seconds=240;memory_mib=1024
        active_processes=3;stdout_bytes=1048576;stderr_bytes=1048576}
}
New-Json $selectionPath $selection
[ordered]@{selection=$selectionPath;selection_sha256=(Digest $selectionPath)
    config=$configPath;config_sha256=$configSha;sources=$sources.Count;runtime_pins=$runtime.Count
    runtime_invoked=$false;proof_calls=0
    argv=@($prep.producer.python.path,'-I','-S','-B',(Join-Path $projectRoot 'tools\Run-V5-Check.py'),$selectionPath,(Digest $selectionPath))
}|ConvertTo-Json -Depth 8
