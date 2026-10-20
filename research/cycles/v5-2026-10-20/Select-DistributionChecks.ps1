# Seven tiny controls, or one file-only installation; unchanged bounded runner.
param([switch]$Install)
$ErrorActionPreference='Stop'
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$prior=Join-Path $checks 'direct-contact-controls-01-selection.json'
if ((Digest $prior) -cne '120597af89c992d48cd288f1ff9d0c033fbd23dd74c04b21fec49a652c1d11bd') { throw 'PRIOR_CHANGED' }
$old=Get-Content -LiteralPath $prior -Raw | ConvertFrom-Json
$sources=[ordered]@{}
$keys=@('tools/Run-V5-Check.py','software/v5/distribution/distribution.py')
if (-not $Install) { $keys += 'software/v5/distribution/test_distribution.py' }
foreach ($key in $keys) {
    $sources[$key]=Digest (Join-Path $projectRoot $key)
}
if ($sources['tools/Run-V5-Check.py'] -cne '44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651') { throw 'RUNNER_CHANGED' }
$runtime=[ordered]@{}
foreach ($property in $old.runtime_pins.psobject.Properties) {
    if ((Digest $property.Name) -cne $property.Value) { throw 'RUNTIME_CHANGED' }
    $runtime[$property.Name]=$property.Value
}
$name='distribution-controls-01'
$argv=@($old.argv[0],'-I','-S','-B','{snapshot}\software\v5\distribution\test_distribution.py',
        '--output','{output}')
$limits=[ordered]@{cpu_seconds=20;wall_seconds=60;memory_mib=128;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
if ($Install) {
    $name='distribution-build-01'
    $inputPath=Join-Path $checks 'distribution-01-input.json'
    $inputValue=Get-Content -LiteralPath $inputPath -Raw | ConvertFrom-Json
    if ($inputValue.distribution_source.sha256 -cne $sources['software/v5/distribution/distribution.py']) { throw 'BUILD_SOURCE_PIN' }
    $destination=Join-Path $projectRoot 'product-local\v5-distribution-01\Mathematical Commons v5'
    if (Test-Path -LiteralPath $destination) { throw 'FRESH_INSTALLATION_REQUIRED' }
    $argv=@($old.argv[0],'-I','-S','-B','{snapshot}\software\v5\distribution\distribution.py',
            'build',$inputPath,(Digest $inputPath),$destination)
    $limits=[ordered]@{cpu_seconds=60;wall_seconds=180;memory_mib=128;active_processes=2;stdout_bytes=1048576;stderr_bytes=1048576}
}
$path=Join-Path $checks ($name+'-selection.json')
if ((Test-Path -LiteralPath $path) -or (Test-Path -LiteralPath (Join-Path $checks $name))) { throw 'NOT_FRESH' }
$selected=[ordered]@{
    schema=$old.schema;name=$name;sources=$sources;runtime_pins=$runtime
    argv=$argv;limits=$limits
}
$raw=[Text.UTF8Encoding]::new($false).GetBytes(($selected|ConvertTo-Json -Depth 12)+"`n")
if ($raw.Length -gt 1048576) { throw 'SELECTION_BOUND' }
$stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
[ordered]@{path=$path;sha256=(Digest $path);sources=$sources.Count;runtime_pins=$runtime.Count;executed=$false}|ConvertTo-Json
