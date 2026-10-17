# Data-only selector. Root supplies an independently adopted successful build.
# No Python/product import, compiler, layout, proof or automatic launch.
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^geometry17-snapshot-host-build-[0-9]{2}$')][string]$BuildName,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$BuildResultSha256
)
$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$checks = Join-Path $projectRoot 'experiments\v5-local-checks'
$name = 'geometry17-layout-01'
$selectionPath = Join-Path $checks ($name+'-selection.json')
$configurationPath = Join-Path $checks ($name+'-configuration.json')
$profilePath = Join-Path $checks ($name+'-profile.json')
$packetPath = Join-Path $checks ($name+'-packet.json')
$output = Join-Path $checks $name
foreach ($path in @($selectionPath,$configurationPath,$profilePath,$packetPath,$output)) {
    if (Test-Path -LiteralPath $path) { throw ('NOT_FRESH:'+ $path) }
}
$utf8 = [Text.UTF8Encoding]::new($false,$true)
function DigestBytes([byte[]]$raw) {
    $hash = [Security.Cryptography.SHA256]::Create()
    try { ([BitConverter]::ToString($hash.ComputeHash($raw))).Replace('-','').ToLowerInvariant() }
    finally { $hash.Dispose() }
}
function Pin([string]$path) {
    $item = Get-Item -LiteralPath $path
    if ($item.PSIsContainer -or $item.Length -le 0 -or $item.Length -gt 134217728) { throw 'PIN_FILE_BOUND' }
    for ($part=$item; $null -ne $part; $part=$part.Parent) {
        if ($part.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'NO_REPARSE' }
        if ($part -is [IO.FileInfo]) { $part=$part.Directory; if ($part.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'NO_REPARSE' } }
    }
    [ordered]@{path=$item.FullName;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
}
function ReadJson([string]$path) {
    if ((Get-Item -LiteralPath $path).Length -gt 2097152) { throw 'JSON_BOUND' }
    [IO.File]::ReadAllText($path,$utf8) | ConvertFrom-Json
}
function Quoted([string]$value) {
    $text = [Text.StringBuilder]::new()
    [void]$text.Append('"')
    foreach ($character in $value.ToCharArray()) {
        $code = [int]$character
        if ($code -eq 34) { [void]$text.Append('\"') }
        elseif ($code -eq 92) { [void]$text.Append('\\') }
        elseif ($code -eq 8) { [void]$text.Append('\b') }
        elseif ($code -eq 9) { [void]$text.Append('\t') }
        elseif ($code -eq 10) { [void]$text.Append('\n') }
        elseif ($code -eq 12) { [void]$text.Append('\f') }
        elseif ($code -eq 13) { [void]$text.Append('\r') }
        elseif ($code -lt 32 -or $code -ge 127) { [void]$text.Append(('\u{0:x4}' -f $code)) }
        else { [void]$text.Append($character) }
    }
    [void]$text.Append('"'); $text.ToString()
}
function Canonical($value) {
    if ($null -eq $value) { return 'null' }
    if ($value -is [string]) { return (Quoted $value) }
    if ($value -is [bool]) { if ($value) { return 'true' } else { return 'false' } }
    if ($value -is [byte] -or $value -is [int] -or $value -is [long] -or $value -is [uint32] -or $value -is [uint64]) {
        return $value.ToString([Globalization.CultureInfo]::InvariantCulture)
    }
    $map = $null
    if ($value -is [Collections.IDictionary]) { $map=$value }
    elseif ($value -is [System.Management.Automation.PSCustomObject]) {
        $map=@{}; foreach ($property in $value.psobject.Properties) { $map[$property.Name]=$property.Value }
    }
    if ($null -ne $map) {
        [string[]]$keys=@($map.Keys); [Array]::Sort($keys,[StringComparer]::Ordinal)
        $pairs=@(foreach ($key in $keys) { (Quoted $key)+':'+(Canonical $map[$key]) })
        return '{'+($pairs -join ',')+'}'
    }
    if ($value -is [Collections.IEnumerable]) {
        $items=@(foreach ($item in $value) { Canonical $item })
        return '['+($items -join ',')+']'
    }
    throw ('CANONICAL_UNSUPPORTED_TYPE:'+ $value.GetType().FullName)
}
function WriteNew([string]$path,[byte[]]$raw,[int]$maximum=1048576) {
    if ($raw.Length -le 0 -or $raw.Length -gt $maximum) { throw 'NEW_DATA_BOUND' }
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($raw,0,$raw.Length); $stream.Flush($true) } finally { $stream.Dispose() }
    Pin $path
}
$runtime=[ordered]@{}
function AddPin($expected) {
    $actual=Pin $expected.path
    if ($actual.path -cne $expected.path -or $actual.bytes -ne $expected.bytes -or $actual.sha256 -cne $expected.sha256) { throw 'INPUT_PIN_CHANGED' }
    if ($runtime.Contains($actual.path) -and $runtime[$actual.path] -cne $actual.sha256) { throw 'CONFLICTING_PIN' }
    $runtime[$actual.path]=$actual.sha256
}
function AddFile([string]$path) { $p=Pin $path; AddPin $p; return $p }
function NoOverride([string]$path) {
    if (Test-Path -LiteralPath (Join-Path (Split-Path -Parent $path) 'FINALIZATION-FAILED.json')) { throw 'FINALIZATION_OVERRIDE' }
}

# Gate all data creation on actual one-link success and exact root-adopted bytes.
$build=Join-Path $checks $BuildName
$resultPin=AddFile (Join-Path $build 'RESULT.json')
if ($resultPin.sha256 -cne $BuildResultSha256) { throw 'ROOT_ADOPTED_BUILD_RESULT' }
$result=ReadJson $resultPin.path
if ($result.schema -cne 'DMKN_V5_GEOMETRY17_SNAPSHOT_HOST_BUILD_RESULT_V1' -or
    $result.status -cne 'PASS_GEOMETRY17_SNAPSHOT_HOST_ONE_LINK_ONLY' -or
    $result.snapshot_host_links -ne 1 -or $result.proof_calls -ne 0 -or $result.host_calls -ne 0 -or
    $result.job.active_processes -ne 0 -or $result.job.terminated_processes -ne 0 -or
    @($result.commands).Count -ne 1 -or $result.commands[0].status -cne 'COMMAND_COMPLETED' -or
    $result.commands[0].exit_code -ne 0 -or @($result.commands[0].cleanup_errors).Count -ne 0 -or
    $result.commands[0].job_after.active_processes -ne 0 -or $result.commands[0].job_after.terminated_processes -ne 0) { throw 'GENUINE_CLOSED_ONE_LINK_REQUIRED' }
$buildPins=[ordered]@{result=$resultPin
    attempt=(AddFile (Join-Path $checks ($BuildName+'-attempt.json')))
    selection=(AddFile (Join-Path $checks ($BuildName+'-selection.json')))
    source_map=(AddFile (Join-Path $build 'source-map.json'))
    command=(AddFile (Join-Path $build 'compile-command.json'))}
foreach ($p in $buildPins.Values) { NoOverride $p.path }
$attempt=ReadJson $buildPins.attempt.path
$buildSelection=ReadJson $buildPins.selection.path
if ($attempt.status -cne $result.status -or $attempt.result_sha256 -cne $resultPin.sha256 -or
    $buildSelection.name -cne $BuildName -or $buildSelection.authorizes_compile_only -ne $true -or
    $buildPins.selection.sha256 -cne $result.selection_sha256 -or
    (Pin (Join-Path $build 'selection.json')).sha256 -cne $result.selection_sha256 -or
    $buildPins.source_map.sha256 -cne $result.source_map_sha256 -or $buildPins.command.sha256 -cne $result.commands_sha256) { throw 'BUILD_RECORD_BINDINGS' }
AddPin $result.executable
if ($result.executable.path -cne (Join-Path $build 'geometry17_aggregate_host.exe')) { throw 'EXACT_NEW_EXECUTABLE' }
$sourceMap=ReadJson $buildPins.source_map.path
foreach ($property in $sourceMap.psobject.Properties) {
    AddPin ([ordered]@{path=(Join-Path (Join-Path $build 'source') $property.Name);bytes=$property.Value.bytes;sha256=$property.Value.sha256})
}
foreach ($property in $result.refined_libraries.psobject.Properties) { AddPin $property.Value }
foreach ($pair in @(@('environment-profile.json','environment_sha256'),@('INPUT-MAP.json','input_map_sha256'))) {
    $p=AddFile (Join-Path $build $pair[0])
    if ($p.sha256 -cne $result.($pair[1])) { throw 'BUILD_AUXILIARY_BINDING' }
}
$oldBuild=Join-Path $checks 'prover-allocation-build-01'
foreach ($file in @('RESULT.json','compile-commands.json','environment-profile.json','selection.json','source-map.json','INPUT-MAP.json')) {
    $p=AddFile (Join-Path $oldBuild $file); NoOverride $p.path
}
$p=AddFile (Join-Path $checks 'prover-allocation-build-01-attempt.json'); NoOverride $p.path

$seedPin=AddFile (Join-Path $checks 'selected-frontier-preflight-01-profile.json')
if ($seedPin.sha256 -cne 'd561265970d67ac888909c9edd93578a4dd5298b2ec810b1fe382cab1eaced6c') { throw 'RETAINED_SEED_PROFILE' }
$seed=ReadJson $seedPin.path
$support=$seed.support_profile
$support.host=$result.executable
$support.source_pins=@((Pin (Join-Path $projectRoot 'software/v5/production/producer.py')),(Pin (Join-Path $projectRoot 'software/v5/production/__init__.py')))
foreach ($p in @($support.supervisor_manifest,$support.host,$support.python,$support.python_dll)+@($support.source_pins)+@($support.runtime_pins)) { AddPin $p }
$manifest=ReadJson $support.supervisor_manifest.path
$install=Split-Path -Parent $support.supervisor_manifest.path
foreach ($relative in @('operator/commons.py','receiver/helpers/domains.py','receiver/helpers/run_stage.py')) {
    $row=$manifest.files.$relative
    AddPin ([ordered]@{path=(Join-Path $install $relative);bytes=$row.bytes;sha256=$row.sha256})
}
foreach ($property in $seed.image_adoption.psobject.Properties) { AddPin $property.Value; NoOverride $property.Value.path }
$imageResult=ReadJson $seed.image_adoption.result.path
AddPin $imageResult.image

$modules=@('aggregate_geometry','aggregate_geometry.layout_owner','aggregate_geometry.adoption','aggregate_geometry.snapshot',
    'aggregate_small','aggregate_small.producer','production','production.producer','aggregate_claims','aggregate_claims.bindings',
    'aggregate_claims.input','aggregate_claims.prepare_mixed','mixed_claims','mixed_claims.packet','delta','delta.packet','delta.receiver',
    'delta_claims','delta_claims.claims','delta_claims.receiver','admission','admission.bindings','admission.verifier','modules','modules.codec')
$sources=[ordered]@{}; $ownerSources=@(); $sourceBytes=0
foreach ($module in @($modules)+@('aggregate_geometry.prepare_h2')) {
    $relative='software/v5/'+$module.Replace('.','/')+$(if ($module.Contains('.')) {'.py'} else {'/__init__.py'})
    $p=AddFile (Join-Path $projectRoot $relative); $sources[$relative]=$p.sha256; $sourceBytes+=$p.bytes
    if ($modules -ccontains $module) { $ownerSources+=,$p }
}
foreach ($relative in @('software/v5/aggregate_geometry/run_layout.py','tools/Run-V5-Check.py')) {
    $p=AddFile (Join-Path $projectRoot $relative); $sources[$relative]=$p.sha256; $sourceBytes+=$p.bytes
}
if ($sources.Count -ne 28 -or $ownerSources.Count -ne 25 -or $sourceBytes -gt 2097152) { throw 'SOURCE_CLOSURE_OR_RESERVE' }
$selectorPin=AddFile $PSCommandPath

$wirePin=AddFile (Join-Path $checks 'selected-frontier-layout-01/evidence/wire.bin')
$headerPin=AddFile (Join-Path $checks 'selected-frontier-layout-01/evidence/header.bin')
$parentPin=AddFile (Join-Path $checks 'module-base-production-01/finish-0/receipt.bin')
if ($wirePin.bytes -ne 113849 -or $wirePin.sha256 -cne '898660ddeea92cefccbf793e35b1ee49ef4867c9daec24b5344f37a1ed375500' -or
    $headerPin.bytes -ne 192 -or $headerPin.sha256 -cne '49dd845edaec83f5b0cba5af38653f768e51ed95a4bb6ea7824c10bdd1c3169e' -or
    $parentPin.bytes -ne 223594 -or $parentPin.sha256 -cne '850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47') { throw 'EXACT_RETAINED_H2_INPUTS' }
$wire=[IO.File]::ReadAllBytes($wirePin.path); $parent=[IO.File]::ReadAllBytes($parentPin.path)
[byte[]]$first=$wire[629..($wire.Length-1)]; [byte[]]$target=$wire[441..624]
if ((DigestBytes $first) -cne '88b71b8282afc99297bf6564d22616fce6211eed9a9e18afa1cb42a41d1206e1' -or
    (DigestBytes $target) -cne '07734789fd165d5c29667a2925c09b882d346db97a511c75644f2cb4b8ccd0da') { throw 'EXACT_SELECTED_WITNESS_TARGET' }
$base='['+(@($wire[61..244] | ForEach-Object { $_.ToString([Globalization.CultureInfo]::InvariantCulture) }) -join ',')+']'
$receiptHex=([BitConverter]::ToString($parent)).Replace('-','').ToLowerInvariant()
# Existing exact witness bytes are inert payload. prepare_h2 must regenerate the
# complete packet and wire/header/parent byte-for-byte at the eventual dispatch.
$packetText='{"claims":[{"receipt_hex":"'+$receiptHex+'","statement":'+$base+',"tag":0}],"deltas":['+
    $utf8.GetString($first)+'],"frontiers":[{"claim_index":0,"journal":'+$base+',"member_index":0,"siblings":[]}],"schema":"DMKN_MIXED_DELTA_PACKET_V1"}'
$profile=[ordered]@{schema='DMKN_GEOMETRY17_LAYOUT_PROFILE_V1';support_profile=$support;source_pins=$ownerSources
    relation_image=$seed.relation_image;snapshot_host_build=$buildPins;image_adoption=$seed.image_adoption}
$profileRaw=$utf8.GetBytes((Canonical $profile)+"`n")
$domain=$utf8.GetBytes("DMKN-GEOMETRY17-LAYOUT-PROFILE-V1`0")
$profileId=DigestBytes ([byte[]]($domain+$profileRaw))
# Recheck all existing inputs before creating any selected data; preserve partial
# selection data on any later failure, never overwrite or silently rerun.
foreach ($path in @($runtime.Keys)) { if ((Pin $path).sha256 -cne $runtime[$path]) { throw 'FINAL_INPUT_REBIND' } }
$packetPin=WriteNew $packetPath ($utf8.GetBytes($packetText)); AddPin $packetPin
$profilePin=WriteNew $profilePath $profileRaw; AddPin $profilePin
$configuration=[ordered]@{schema='DMKN_GEOMETRY17_LAYOUT_SNAPSHOT_REQUEST_V1';profile_id=$profileId
    profile_document=$profilePin;packet=$packetPin;target_journal=([BitConverter]::ToString($target)).Replace('-','').ToLowerInvariant()
    envelope=[ordered]@{packet_bytes=33554432;receipt_bytes=8388608;witness_bytes=16777216;claims=8;frontiers=32;deltas=16
        edges=128;openings=4096;bodies=8192;rows=250000;nodes=500000;depth=128;rank=[uint64]::MaxValue}
    cycles=67108864;po2=17;diagnostic_mode='stats';output_directory=(Join-Path $output 'evidence')
    reference_inputs=[ordered]@{wire=$wirePin;expected=$headerPin;parents=@($parentPin)}
    limits=[ordered]@{worker_cpu_seconds=60;controller_cpu_seconds=30;wall_seconds=120;memory_mib=512;active_processes=2
        stdout_bytes=1048576;stderr_bytes=1048576;output_bytes=218103808;output_entries=544}}
$configurationPin=WriteNew $configurationPath ($utf8.GetBytes((Canonical $configuration)+"`n")); AddPin $configurationPin
if ($runtime.Count -gt 256) { throw 'OUTER_RUNTIME_PIN_COUNT' }
$selection=[ordered]@{schema='DMKN_V5_LOCAL_CHECK_V1';name=$name;sources=$sources;runtime_pins=$runtime
    argv=@($support.python.path,'-I','-S','-B','{snapshot}\software\v5\aggregate_geometry\run_layout.py',
        '--configuration',$configurationPath,'--configuration-sha256',$configurationPin.sha256,'--selection',$selectionPath)
    limits=[ordered]@{cpu_seconds=120;wall_seconds=180;memory_mib=1024;active_processes=3;stdout_bytes=1048576;stderr_bytes=1048576}}
$selectionPin=WriteNew $selectionPath ($utf8.GetBytes((Canonical $selection)+"`n"))
[ordered]@{selection=$selectionPin;configuration=$configurationPin;profile=$profilePin;packet=$packetPin
    build_result=$resultPin;sources=$sources.Count;runtime_pins=$runtime.Count;source_bytes=$sourceBytes
    selector=$selectorPin;executed=$false;authority='DATA_SELECTION_ONLY_ROOT_MUST_SEPARATELY_ADOPT_AND_RUN'} | ConvertTo-Json -Depth 6
