# Test-only file staging. No product import, constructor, host, build or proof.
# Root must separately select this script and its four reviewed source digests.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$InitSha,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ProducerSha,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$AdoptionSha,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$EntrySha
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$projectRoot='E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks=Join-Path $projectRoot 'experiments\v5-local-checks'
$target=Join-Path $checks 'release-producer-component-01'
$installation=Join-Path $target 'installation'
$base=Join-Path $projectRoot 'product-local\v4-library-commons-02\commons-v4'
$stable=Join-Path $checks 'typed-production-controls-01\sources\software\v5'
$aImage='9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865'
$iImage='9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e'
$foundation='d931d114155cf3cf0dc0b868aa88c6d38b8ada8ecafe267a5934934075782481'
$policy='5edfd0ee15b141b7304e26c1a39cd11f7f7e721713cf099813ae4f4442fad377'
$copies=[ordered]@{}; $files=[ordered]@{}; $originals=[ordered]@{}

function Ordinary([string]$path,[bool]$directory=$false,[bool]$fresh=$false) {
    $full=[IO.Path]::GetFullPath($path)
    if ($full -cne $path -or -not $full.StartsWith($projectRoot+'\',[StringComparison]::Ordinal)) { throw 'EXACT_CANONICAL_SCOPE' }
    $cursor=$full
    while ($cursor) {
        if (Test-Path -LiteralPath $cursor) {
            $item=Get-Item -LiteralPath $cursor
            if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'NO_REPARSE_PATH' }
            if ($cursor -cne $full -and -not $item.PSIsContainer) { throw 'ORDINARY_PARENT' }
        }
        $cursor=[IO.Path]::GetDirectoryName($cursor)
    }
    if ($fresh) {
        if (Test-Path -LiteralPath $full) { throw ('FRESH_OUTPUT_REQUIRED:'+ $full) }
    } elseif ([bool](Get-Item -LiteralPath $full).PSIsContainer -ne $directory) { throw 'ORDINARY_PATH_KIND' }
    return $full
}
function Relative([string]$name) {
    if (-not $name -or $name.Length -gt 1024 -or $name.Contains('\') -or $name.StartsWith('/') -or
        $name.EndsWith('/') -or $name.Contains('//')) { throw 'RELATIVE_NAME' }
    $parts=$name.Split('/')
    if ($parts.Count -gt 32) { throw 'RELATIVE_DEPTH' }
    foreach($part in $parts) {
        if ($part -in @('.','..') -or $part -match '[\x00-\x1f:*?"<>|]' -or $part.EndsWith('.') -or $part.EndsWith(' ') -or
            $part -match '^(?i:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)') { throw 'RELATIVE_COMPONENT' }
    }
    return $name.Replace('/','\')
}
function Pin([string]$path,[string]$expected,[long]$maximum=134217728) {
    [void](Ordinary $path)
    $size=(Get-Item -LiteralPath $path).Length
    if ($expected -cnotmatch '^[0-9a-f]{64}$' -or $size -lt 0 -or $size -gt $maximum -or
        (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $expected -or
        (Get-Item -LiteralPath $path).Length -ne $size) { throw ('PIN_CHANGED:'+ $path) }
    return [ordered]@{path=$path;bytes=$size;sha256=$expected}
}
function Same-Pin($left,$right) {
    return $left.path -ceq $right.path -and $left.bytes -eq $right.bytes -and $left.sha256 -ceq $right.sha256
}
function Remember($row) {
    if ($originals.Contains($row.path) -and -not (Same-Pin $originals[$row.path] $row)) { throw 'ORIGINAL_PIN_CONFLICT' }
    $originals[$row.path]=$row
}
function Read-Pin($row,[long]$maximum=8388608) {
    $actual=Pin $row.path $row.sha256 $maximum
    if ($actual.bytes -ne $row.bytes -or $actual.bytes -le 0) { throw 'DOCUMENT_SIZE_CHANGED' }
    Remember $actual
    return Get-Content -Raw -Encoding UTF8 -LiteralPath $row.path | ConvertFrom-Json
}
function Select-Copy([string]$relative,$source) {
    [void](Relative $relative)
    if ($copies.Contains($relative)) { throw 'DUPLICATE_PAYLOAD' }
    $actual=Pin $source.path $source.sha256
    if ($actual.bytes -ne $source.bytes) { throw 'SOURCE_SIZE_CHANGED' }
    Remember $actual
    $copies[$relative]=$actual
    $files[$relative]=[ordered]@{bytes=$actual.bytes;sha256=$actual.sha256}
}
function Ensure-Parent([string]$path) {
    $parent=[IO.Path]::GetDirectoryName($path)
    if (-not $parent.StartsWith($target+'\',[StringComparison]::Ordinal) -and $parent -cne $target) { throw 'OUTPUT_PARENT_SCOPE' }
    if (-not (Test-Path -LiteralPath $parent)) { [void][IO.Directory]::CreateDirectory($parent) }
    [void](Ordinary $parent $true)
}
function Copy-Selected([string]$relative,$source) {
    $destination=Join-Path $installation (Relative $relative)
    [void](Ordinary $destination $false $true); Ensure-Parent $destination
    $incoming=[IO.File]::Open($source.path,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::Read)
    try {
        $outgoing=[IO.File]::Open($destination,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
        try { $incoming.CopyTo($outgoing); $outgoing.Flush($true) } finally { $outgoing.Dispose() }
    } finally { $incoming.Dispose() }
    $actual=Pin $destination $source.sha256
    if ($actual.bytes -ne $source.bytes) { throw 'COPIED_SIZE_CHANGED' }
}
function Digest([byte[]]$raw) {
    $algorithm=[Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($algorithm.ComputeHash($raw))).Replace('-','').ToLowerInvariant() }
    finally { $algorithm.Dispose() }
}
function New-Json([string]$path,$value) {
    $raw=[Text.UTF8Encoding]::new($false).GetBytes((ConvertTo-Json -InputObject $value -Depth 64 -Compress)+"`n")
    if ($raw.Length -le 0 -or $raw.Length -gt 8388608) { throw 'GENERATED_DOCUMENT_BOUND' }
    [void](Ordinary $path $false $true); Ensure-Parent $path
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($raw,0,$raw.Length);$stream.Flush($true) } finally { $stream.Dispose() }
    return Pin $path (Digest $raw) 8388608
}
function Installed-Pin([string]$relative) {
    if (-not $files.Contains($relative)) { throw 'UNSELECTED_INSTALLED_ROLE' }
    return [ordered]@{path=(Join-Path $installation (Relative $relative));bytes=$files[$relative].bytes;sha256=$files[$relative].sha256}
}
function Descriptor-Pin([string]$relative) {
    if (-not $files.Contains($relative)) { throw 'UNSELECTED_DESCRIPTOR_ROLE' }
    return [ordered]@{path=$relative;bytes=$files[$relative].bytes;sha256=$files[$relative].sha256}
}

[void](Ordinary $target $true $true)
[void](Ordinary $checks $true)
$profilePin=Pin (Join-Path $checks 'typed-production-controls-01-profile.json') '1242b0a8430e68032bbedbddcb3c6539fbdc95a2a5cf567936545c5f891246cc' 1048576
$old=Read-Pin $profilePin 1048576
$basePin=Pin (Join-Path $base 'RELEASE-MANIFEST.json') 'a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed'
$baseManifest=Read-Pin $basePin
if (-not (Same-Pin $basePin $old.base_profile.support_profile.supervisor_manifest)) { throw 'EXACT_OLD_BASE_MANIFEST' }
$pythonRows=@($baseManifest.files.PSObject.Properties | Where-Object { $_.Name.StartsWith('receiver/runtime/python/',[StringComparison]::Ordinal) })
if ($pythonRows.Count -ne 584 -or ($pythonRows | ForEach-Object {$_.Value.bytes} | Measure-Object -Sum).Sum -ne 30459330) { throw 'EXACT_COMPLETE_PYTHON_PAYLOAD' }
foreach($property in $pythonRows) {
    Select-Copy ('base/'+$property.Name) ([ordered]@{path=(Join-Path $base (Relative $property.Name));bytes=$property.Value.bytes;sha256=$property.Value.sha256})
}
foreach($relative in @('operator/commons.py','receiver/helpers/domains.py','receiver/helpers/run_stage.py')) {
    $row=$baseManifest.files.$relative
    Select-Copy ('base/'+$relative) ([ordered]@{path=(Join-Path $base (Relative $relative));bytes=$row.bytes;sha256=$row.sha256})
}
Select-Copy 'base/RELEASE-MANIFEST.json' $basePin
$coreModules=@('aggregate_lifecycle','aggregate_lifecycle.producer','aggregate_lifecycle.snapshot',
    'aggregate_small','aggregate_small.producer','production','production.producer',
    'aggregate_claims','aggregate_claims.bindings','aggregate_claims.input','aggregate_claims.prepare_mixed',
    'mixed_claims','mixed_claims.packet','delta','delta.packet','delta.receiver','delta_claims',
    'delta_claims.claims','delta_claims.receiver','admission','admission.bindings','admission.verifier',
    'modules','modules.codec')
$oldSources=@{}; foreach($row in $old.source_pins) { $oldSources[$row.path]=$row }
$sourceRoles=[ordered]@{}
foreach($name in $coreModules) {
    $relative=$name.Replace('.','/')
    if ($name.Contains('.')) { $relative+='.py' } else { $relative+='/__init__.py' }
    $source=Join-Path $stable (Relative $relative)
    if (-not $oldSources.ContainsKey($source)) { throw 'EXACT_RETAINED_LIFECYCLE_SOURCE' }
    $destination='sdk/v5/'+$relative
    Select-Copy $destination $oldSources[$source]
    $sourceRoles[$name]=$destination
}
$freshSources=[ordered]@{'__init__.py'=$InitSha;'producer.py'=$ProducerSha;'adoption.py'=$AdoptionSha;'operator.py'=$EntrySha}
foreach($name in $freshSources.Keys) {
    $source=Join-Path $projectRoot ('software\v5\release_production\'+$name)
    $pin=Pin $source $freshSources[$name] 1048576
    Select-Copy ('sdk/v5/release_production/'+$name) $pin
}
$sourceRoles['release_production']='sdk/v5/release_production/__init__.py'
$sourceRoles['release_production.producer']='sdk/v5/release_production/producer.py'
$sourceRoles['release_production.adoption']='sdk/v5/release_production/adoption.py'
$helperPath=Join-Path $stable 'aggregate_small\operator.py'
$helperRows=@($old.base_profile.support_profile.runtime_pins | Where-Object {$_.path -ceq $helperPath})
if ($helperRows.Count -ne 1) { throw 'SOLE_RETAINED_OPERATOR_HELPER' }
Select-Copy 'sdk/v5/aggregate_small/operator.py' $helperRows[0]
$imageRecord=Read-Pin $old.base_profile.image_adoption.result
$snapshotRecord=Read-Pin $old.snapshot_host_build.result
$roleInputs=[ordered]@{
    stage_host=$old.base_profile.support_profile.host
    snapshot_host=$snapshotRecord.executable
    guest_image=$imageRecord.image
}
$expectedRoles=[ordered]@{
    stage_host=[ordered]@{bytes=68039168;sha256='263841ae256af217de2c00452c7f0688a2e9e58e6aa6d95457d5118aef04ff3c'}
    snapshot_host=[ordered]@{bytes=6630400;sha256='a9438205bbb091623f12bd10a7e9a0a2b437c873003fec3cb000c7d8dbbd7a05'}
    guest_image=[ordered]@{bytes=1868700;sha256='0bb44c54238f78fe04a385b689ddcce9a1b8770eac5a2f0ae9e71de1b62b0d46'}
}
$rolePaths=[ordered]@{stage_host='assets/producer/stage_host.exe';snapshot_host='assets/producer/snapshot_host.exe';guest_image='assets/producer/aggregate_image.bin'}
foreach($name in $roleInputs.Keys) {
    $row=$roleInputs[$name]; $expected=$expectedRoles[$name]
    if ($row.bytes -ne $expected.bytes -or $row.sha256 -cne $expected.sha256) { throw 'EXACT_RETAINED_RUNTIME_ROLE' }
    Select-Copy $rolePaths[$name] $row
}
if ($imageRecord.image_id -cne $aImage -or $sourceRoles.Count -ne 27 -or $copies.Count -ne 620 -or
    ($files.Values | ForEach-Object {$_.bytes} | Measure-Object -Sum).Sum -gt 268435456) { throw 'BOUNDED_COMPONENT_PLAN' }
$created=$false
try {
    [void](Ordinary $target $true $true)
    [void][IO.Directory]::CreateDirectory($target); $created=$true
    [void][IO.Directory]::CreateDirectory($installation)
    foreach($relative in $copies.Keys) { Copy-Selected $relative $copies[$relative] }
    $descriptorSources=[ordered]@{}; $corePins=[ordered]@{}
    foreach($name in $sourceRoles.Keys) {
        $descriptorSources[$name]=Descriptor-Pin $sourceRoles[$name]
        $corePins[$name]=Installed-Pin $sourceRoles[$name]
    }
    $descriptorRoles=[ordered]@{}; $rolePins=[ordered]@{}
    foreach($name in $rolePaths.Keys) {
        $descriptorRoles[$name]=Descriptor-Pin $rolePaths[$name]
        $rolePins[$name]=Installed-Pin $rolePaths[$name]
    }
    $descriptor=[ordered]@{schema='DMKN_RELEASE_AGGREGATE_ARTIFACTS_V1';foundation=$foundation;policy=$policy;
        relation_image=$iImage;aggregate_image=$aImage;roles=$descriptorRoles;sources=$descriptorSources}
    $descriptorRelative='assets/producer/ARTIFACTS.json'
    $descriptorPin=New-Json (Join-Path $installation (Relative $descriptorRelative)) $descriptor
    $files[$descriptorRelative]=[ordered]@{bytes=$descriptorPin.bytes;sha256=$descriptorPin.sha256}
    $manifest=[ordered]@{schema='DMKN_V5_DIRECTORY_RELEASE_V3';files=$files;
        component_scope='OPERATIVE_PRODUCER_COMPONENT_ONLY_NOT_FULL_DIRECTORY_DISTRIBUTION'}
    $manifestPin=New-Json (Join-Path $installation 'V5-RELEASE.json') $manifest
    $runtime=[Collections.Generic.List[object]]::new()
    $oldRuntime=@($old.base_profile.support_profile.runtime_pins | Where-Object {$_.path.StartsWith($base+'\',[StringComparison]::Ordinal)})
    if ($oldRuntime.Count -ne 16) { throw 'EXACT_16_RETAINED_RUNTIME_PINS' }
    foreach($row in $oldRuntime) {
        $relative=$row.path.Substring($base.Length+1).Replace('\','/')
        $selected=Installed-Pin ('base/'+$relative)
        if ($selected.bytes -ne $row.bytes -or $selected.sha256 -cne $row.sha256) { throw 'RETAINED_RUNTIME_CONTENT' }
        $runtime.Add($selected)
    }
    foreach($pin in $corePins.Values) { $runtime.Add($pin) }
    $helper=Installed-Pin 'sdk/v5/aggregate_small/operator.py'
    $entry=Installed-Pin 'sdk/v5/release_production/operator.py'
    $runtime.Add($helper);$runtime.Add($entry)
    if ($runtime.Count -ne 45) { throw 'EXACT_45_RUNTIME_ROWS' }
    $python=Installed-Pin 'base/receiver/runtime/python/python.exe'
    $pythonDll=Installed-Pin 'base/receiver/runtime/python/python314.dll'
    $support=[ordered]@{schema='DMKN_V5_PRODUCER_PROFILE_V1';supervisor_manifest=(Installed-Pin 'base/RELEASE-MANIFEST.json');
        host=$rolePins.stage_host;python=$python;python_dll=$pythonDll;
        source_pins=@($corePins['production'],$corePins['production.producer']);runtime_pins=@($runtime.ToArray());
        image_id=$aImage;foundation=$foundation;policy=$policy}
    $hostMap=[ordered]@{release=$manifestPin;descriptor=$descriptorPin;stage_host=$rolePins.stage_host}
    $imageMap=[ordered]@{release=$manifestPin;descriptor=$descriptorPin;guest_image=$rolePins.guest_image}
    $snapshotMap=[ordered]@{release=$manifestPin;descriptor=$descriptorPin;snapshot_host=$rolePins.snapshot_host}
    $profile=[ordered]@{schema='DMKN_RELEASE_AGGREGATE_LIFECYCLE_PROFILE_V1';
        base_profile=[ordered]@{schema='DMKN_RELEASE_AGGREGATE_OWNER_PROFILE_V1';support_profile=$support;
            source_pins=@($corePins['aggregate_small'],$corePins['aggregate_small.producer']);relation_image=$iImage;
            host_build=$hostMap;image_adoption=$imageMap;stage_memory_ceiling_mib=4096};
        source_pins=@($corePins.Values);snapshot_host_build=$snapshotMap;
        release=[ordered]@{root=$installation;manifest=$manifestPin;descriptor=$descriptorPin}}
    $freshProfilePin=New-Json (Join-Path $target 'profile.json') $profile
    $installationPins=[ordered]@{}
    foreach($pin in @($support.supervisor_manifest,$support.host,$python,$pythonDll,$manifestPin,$descriptorPin,
                       $rolePins.guest_image,$rolePins.snapshot_host)+@($runtime.ToArray())) { $installationPins[$pin.path]=$pin }
    foreach($relative in @('operator/commons.py','receiver/helpers/domains.py','receiver/helpers/run_stage.py')) {
        $pin=Installed-Pin ('base/'+$relative);$installationPins[$pin.path]=$pin
    }
    if ($installationPins.Count -ne 56 -or ($installationPins.Values | ForEach-Object {$_.bytes} | Measure-Object -Sum).Sum -gt 536870912) { throw 'EXACT_BOUNDED_INSTALLATION_UNION' }
    foreach($relative in $files.Keys) {
        $row=Installed-Pin $relative
        $actual=Pin $row.path $row.sha256
        if ($actual.bytes -ne $row.bytes) { throw 'FINAL_PAYLOAD_REBIND' }
    }
    foreach($row in $originals.Values) {
        $actual=Pin $row.path $row.sha256
        if ($actual.bytes -ne $row.bytes) { throw 'ORIGINAL_INPUT_CHANGED' }
    }
    $actualFiles=@(Get-ChildItem -LiteralPath $installation -Recurse -File)
    if ($actualFiles.Count -ne $files.Count+1 -or $files.Count -ne 621) { throw 'EXACT_COMPONENT_FILE_CENSUS' }
    foreach($item in $actualFiles) { [void](Ordinary $item.FullName) }
    $preparation=[ordered]@{schema='DMKN_RELEASE_PRODUCER_COMPONENT_PREPARATION_V1';status='FILES_STAGED_AND_HASH_VERIFIED_ONLY';
        installation_root=$installation;profile=$freshProfilePin;manifest=$manifestPin;descriptor=$descriptorPin;
        python=$python;python_dll=$pythonDll;entry=$entry;helper=$helper;core_sources=$corePins;
        installation_pins=@($installationPins.Values);original_inputs=@($originals.Values);
        payload_files=$files.Count;declared_payload_bytes=($files.Values | ForEach-Object {$_.bytes} | Measure-Object -Sum).Sum;
        copied_python_files=584;copied_python_bytes=30459330;constructor_calls=0;host_calls=0;proof_calls=0;
        mathematical_admission=$false;full_distribution_validation=$false;authority='ROOT_SELECTED_TEST_COMPONENT_NOT_PUBLIC_RELEASE'}
    $saved=New-Json (Join-Path $target 'PREPARATION.json') $preparation
    Write-Output (ConvertTo-Json -InputObject $saved -Compress)
} catch {
    if ($created -and -not (Test-Path -LiteralPath (Join-Path $target 'PREPARATION-FAILED.json'))) {
        try { [void](New-Json (Join-Path $target 'PREPARATION-FAILED.json') ([ordered]@{
            status='COMPONENT_STAGING_FAILED';overrides_preparation=$true;error=$_.Exception.Message;
            constructor_calls=0;host_calls=0;proof_calls=0;mathematical_admission=$false})) } catch { }
    }
    throw
}
