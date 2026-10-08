# Tentative v3 receiver: Windows usage

**Draft: real receipt qualification is still pending.** Archive identity and
extracted Python startup have actual passing audits; they do not establish
successful mathematical-certificate verification. The commands below match
the actual packaged CLI. They are operator instructions for after root adopts
the pending receipt outcome, not a claim that those commands were run here.

This guide accompanies `DRAFT-START-HERE.md`. It does not modify frozen package
files, native v2, node state or any earlier result. Licensing is undecided;
this local handoff does not authorize external publication or redistribution.

## What you need

- A Windows x64 machine with an ordinary writable directory you control.
  The packaged Python and verifier are supplied; a separate Python, Lean,
  compiler, prover installation or guest image file is not required.
- The independently adopted receiver archive and checksum below.
- One inert bundle directory containing **exactly** `bundle.json`,
  `capsule.json`, `journal.bin`, `receipt.bin` and no extra files/subdirectories.
- A fresh output path whose parent already exists. Installation, bundle and
  output must not overlap. Avoid junctions, symbolic links and linked path
  ancestors; the receiver rejects those paths. Do not put logs inside the
  installation or bundle.

The archive is 56,577,912 bytes (about 56.6 MB / 54.0 MiB). Extraction contains
597 files totaling 97,142,933 bytes (about 97.1 MB / 92.6 MiB): 596 assets plus
the 78,872-byte profile. Allow additional space for the unchanged ZIP and each
check's snapshots/logs. The receiver's operation-storage ceiling is 96 MiB;
this is a maximum, not a measured per-check requirement. Windows system DLLs
remain host dependencies. Different-host qualification has not been done.

## Extract this exact local archive

These commands use the current project paths and choose a **new** operator
directory, leaving the already qualified extraction untouched. Execute them
only after the draft's real-receipt qualification hold is cleared. If using
another machine, replace the initial project/archive location with your own
ordinary absolute path; retain the independently adopted checksums.

```powershell
$v3Project = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
Set-Location -LiteralPath $v3Project
$v3Archive = Join-Path $v3Project 'product-local\certified-verifier-package-01\mathematical-commons-v3-receiver.zip'
$v3ArchiveSha = 'db862cc0c0b86a53d7f9e47c9c5c32ba4cc4406f805d1f08d6fb37b78b4f9ec4'
$v3UseRoot = Join-Path $v3Project 'product-local\receiver-operator-01'

if ((Get-FileHash -LiteralPath $v3Archive -Algorithm SHA256 -ErrorAction Stop).Hash.ToLowerInvariant() -ne $v3ArchiveSha) {
    throw 'Archive checksum mismatch; do not extract or execute it.'
}
if (Test-Path -LiteralPath $v3UseRoot) {
    throw 'Choose a new operator directory; preserve the existing directory.'
}
New-Item -ItemType Directory -Path $v3UseRoot -ErrorAction Stop | Out-Null
Expand-Archive -LiteralPath $v3Archive -DestinationPath (Join-Path $v3UseRoot 'unpacked') -ErrorAction Stop
$v3Receiver = (Resolve-Path -LiteralPath (Join-Path $v3UseRoot 'unpacked\certified-receiver') -ErrorAction Stop).Path
$v3ProfileSha = '6dc5cef431843e15ec6e8647892a0462bc5bd7a76554d541ff76d4d8719af297'
if ((Get-FileHash -LiteralPath (Join-Path $v3Receiver 'profile.json') -Algorithm SHA256 -ErrorAction Stop).Hash.ToLowerInvariant() -ne $v3ProfileSha) {
    throw 'Profile checksum mismatch; do not execute this receiver.'
}
```

Neither checksum should be learned solely from an untrusted sender together
with its archive. Independent adoption is what says *which checker you trust*.
The full wrapper also validates all installed asset bytes before and after
checking. Keep the installation unchanged: adding a README, cache or unrelated
file inside it can correctly cause refusal.

## Verify a four-file bundle once

The reviewed integration runner fixes the forthcoming genuine sample location
to the following absolute path:

```text
E:\Distributed Trustworthy Mathematical Knowledge Network\experiments\certified-verifier-integration-01\receipt-01\bundles\L
```

**At draft creation this bundle is not yet available or qualified.** It will
be written by the selected integration only after the real final L receipt
is adopted. Do not manufacture it from an expected journal, incomplete proof
checkpoint, fake receipt or a copied PASS record. This rank-zero sample tests
receipt acceptance, not recursive parent-assumption discharge.

After qualification, continue in the same PowerShell session:

```powershell
$v3Bundle = Join-Path $v3Project 'experiments\certified-verifier-integration-01\receipt-01\bundles\L'
if (-not (Test-Path -LiteralPath $v3Bundle -PathType Container)) {
    throw 'The genuine sample bundle is not available; qualification remains pending.'
}
$v3Bundle = (Resolve-Path -LiteralPath $v3Bundle -ErrorAction Stop).Path
$v3Check = Join-Path $v3UseRoot 'check-001'
if (Test-Path -LiteralPath $v3Check) {
    throw 'Choose a fresh check path; do not overwrite a previous attempt.'
}

& (Join-Path $v3Receiver 'runtime\python\python.exe') -B -E -s -S `
  (Join-Path $v3Receiver 'cert_verify.py') `
  --profile (Join-Path $v3Receiver 'profile.json') `
  --profile-sha256 $v3ProfileSha `
  --bundle $v3Bundle `
  --run $v3Check
$v3Exit = $LASTEXITCODE

Write-Output "Receiver exit code: $v3Exit"
$v3ResultFile = Join-Path $v3Check 'RESULT.json'
if (Test-Path -LiteralPath $v3ResultFile -PathType Leaf) {
    $v3Report = Get-Content -LiteralPath $v3ResultFile -Raw -ErrorAction Stop | ConvertFrom-Json
    $v3Report | Select-Object status, receipt_verified, native_admission, verifier_calls, cleanup_errors
    $v3Report.job
} else {
    Write-Output 'No RESULT.json was created. Read the terminal refusal; no acceptance is established.'
}
```

For another already produced bundle, change only `$v3Bundle` to its ordinary
absolute directory. For another attempt use a new check name. A run is one
bounded verification, not an automatic retry or proof-generation request.
These instructions do not rerun the research qualification campaign.

The packaged profile permits at most 120 worker CPU seconds, 180 sampled wall
seconds and 1 GiB worker private commit, with separate controller ceilings of
120 CPU seconds and 512 MiB. Limits are checked by the implementation and are
not hard real-time overshoot guarantees. Hitting a limit is refusal, not
permission to remove checks or edit the pinned profile in place.

## Read the result correctly

Successful completion requires exit code `0` and the wrapper's exact status:

```text
PASS_EXPERIMENTAL_COLD_CERTIFICATE_VERIFIED_NOT_NATIVE_ADMISSION
```

The same fresh `RESULT.json` records `receipt_verified: true`,
`native_admission: false`, one real verifier call, no cleanup errors and a
closed Job with zero active processes. It contains the actual command, pins
and accounting. The output retains all four exact input snapshots under
`inputs`, verifier logs under `logs`, and private `cold`/`temp` directories.
Inspect `logs\stderr.txt`, `error`, `final_error` and `cleanup_errors` when
present. The wrapper's final controller accounting is also printed to stderr;
stderr output alone is not a failure criterion.

Anything else is **not accepted**. A nonzero exit, missing result, changed
asset, malformed bundle, wrong image/journal, invalid seal or resource failure
must not be converted into success. Retain the failed directory and costs.
Preallocation refusals may print `REFUSED_NO_SUCCESS` without a result file.
A malformed or unsupported bundle can fail without showing the theorem false;
refusal means this invocation did not establish the required certificate.

A RESULT file is a local observation, not a portable proof token. Another
receiver must verify the actual bundle under its independently adopted
profile. Do not use the driver's private `stage` branch or a raw success
marker as a substitute for the whole wrapper's checks.

## What successful checking would mean

The result concerns precisely the proposition/interface committed by the
capsule and all 148 journal bytes, under:

- Logical profile `dmkn-experimental-certified-01`.
- Image `7a8589ef226cc222696afa93f0fca96a0f3d56ca03fcdebdc9008f7e79a3f0d0`.
- Foundation `4eeaab61471a4ab9f93209af9aad66fcb45f6322783b919851d4d95ea33f9f80`.

The real Succinct/Poseidon2 receipt must bind successful execution of that
checker and a fully discharged final claim. The CLI accepts no ancestor proof
body, parent-history archive, source proof, ledger or guest-image path. It
does not generate a new proof. This is the intended history-independent
**receiver** boundary; actual child-contribution qualification is separate.
Cold verification means a fresh verifier with those explicit inputs, not
another physical machine or an OS sandbox preventing every other file read.

The guest uses an experimental external checker. Its equivalence to Lean's
native kernel and production adaptive recursive assurance are not established
by these finite tests. Thus `receipt_verified` must **not** be interpreted as
native Lean admission or authority to inject an unproved axiom into ordinary
Lean. Use a separately qualified certified importer/contributor with its own
required verification, or use the unchanged native v2 path and its native
checks. This archive is not that full contributor or decentralized node.

No correctness certificate establishes usefulness, novelty, availability,
net end-to-end speedup or exponential knowledge growth. Producer proof cost,
failed attempts, static installation hashing and receiver time all matter.
For the exact assurance scope see the project checkpoint
`research/cycles/v3-2026-09-27/CERTIFIED-PROFILE-ASSURANCE.md`.

## Root's remaining handoff replacements

This section prevents pending work from becoming an accidental release claim.
No executable command above contains a fabricated receipt hash.

| Item to finalize | Current exact state / required update |
|---|---|
| Archive and profile hashes | Actual values are already inserted above; replace only if a separately adopted successor changes bytes. |
| Sample bundle | Exact future path is `experiments/certified-verifier-integration-01/receipt-01/bundles/L`; confirm its actual four-file pins and adopt its genuine receipt before clearing the hold. If copied to delivery, replace the example bundle path with that exact adopted copy. |
| Real receipt result | **PENDING**: root must insert the actual `receipt-01/RESULT.json` status/hash and independent outcome-audit link, or retain refusal/pending status. |
| Costs | **PENDING**: insert observed cold-wrapper CPU/wall/memory and receipt bytes from that actual result, separately from production and failed-proof costs. Do not use limits as timings. |
| Recursive contribution | **NOT established by rank-zero L**: insert only separately audited ordinary-child certificate/import outcome; otherwise retain this limit. |
| Final status | Replace draft/qualification-hold wording only to the scope actually supported. Included `API.md`/`PLAN.md` preserve historical source-only wording; a dated final report must state precisely what supersedes it without editing frozen package bytes. |

Authored by `v3_efficiency` from the actual extracted CLI/API, extraction
result, startup outcome audit and source-reviewed integration paths. Read-only
inspection plus this new Markdown file only; no extraction, verifier or test
was launched while preparing it.
