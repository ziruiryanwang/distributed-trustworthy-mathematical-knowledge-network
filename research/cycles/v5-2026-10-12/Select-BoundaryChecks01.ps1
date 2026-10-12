$ErrorActionPreference = 'Stop'
$projectRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
if ((Get-Location).Path -cne $projectRoot) { throw 'CANONICAL_WORKDIR' }
$local = Join-Path $projectRoot 'experiments\v5-local-checks'
$definitions = @(
    @{name='aggregate-refusal-build-01';schema='DMKN_V5_AGGREGATE_REFUSAL_BUILD_V1';authority='authorizes_compile_only';paths=@(
        'software/v5/aggregate_claim_controls/refusal.rs','software/v5/aggregate_claim_controls/build_native.py',
        'software/v5/aggregate/census.rs','software/v5/aggregate_parse_once/census.rs')},
    @{name='proof-validation-controls-01';schema='DMKN_V5_PROOF_VALIDATION_CONTROLS_V1';authority='authorizes_serde_compile_and_syntax_tests';paths=@(
        'software/v5/modules/native/proof_validation/module_correspondence.rs',
        'software/v5/modules/native/proof_validation/correspondence_controls.rs',
        'software/v5/modules/native/proof_validation/control_root.rs',
        'software/v5/modules/native/proof_validation/control.py')}
)
foreach($definition in $definitions) {
    foreach($suffix in @('','-selection.json','-attempt.json')) {
        $path=Join-Path $local ($definition.name+$suffix)
        if(Test-Path -LiteralPath $path){throw ('NOT_FRESH:'+$path)}
    }
}
foreach($definition in $definitions) {
    $sources=[ordered]@{}
    foreach($relative in $definition.paths) {
        $item=Get-Item -LiteralPath (Join-Path $projectRoot $relative)
        $sources[$relative]=[ordered]@{bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
    }
    $selection=[ordered]@{schema=$definition.schema;name=$definition.name}
    $selection[$definition.authority]=$true
    $selection.sources=$sources
    $selectionPath=Join-Path $local ($definition.name+'-selection.json')
    $raw=[Text.UTF8Encoding]::new($false).GetBytes(($selection|ConvertTo-Json -Depth 10)+"`n")
    $stream=[IO.File]::Open($selectionPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$stream.Write($raw,0,$raw.Length);$stream.Flush($true)} finally {$stream.Dispose()}
    [ordered]@{path=$selectionPath;bytes=$raw.Length;sha256=(Get-FileHash -LiteralPath $selectionPath -Algorithm SHA256).Hash.ToLowerInvariant();executed=$false}|ConvertTo-Json
}
