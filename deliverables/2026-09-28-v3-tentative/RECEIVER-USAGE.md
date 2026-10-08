# Tentative v3: verify the supplied mathematical certificate on Windows

The packaged receiver has now **passed an actual relocated-installation test**:
it verified the genuine L bundle, and the selected four altered-proof/binding
controls were refused. This guide supersedes the draft's pending-receipt status,
not the scope of that result. It is an experimental receiver component, not a
completed scalable contributor/network or native Lean acceptance mode.

Licensing remains undecided. This local handoff does not authorize external
publication or redistribution. Native v2, frozen package bytes and prior
evidence are unchanged.

## What you receive

| Artifact | Actual size | Purpose |
|---|---:|---|
| `mathematical-commons-v3-receiver.zip` | 56,577,912 bytes | Receiver, copied Python runtime, executable, fixed policy and binding helpers |
| Extracted `certified-receiver` | 597 files / 97,142,933 bytes | About 97.1 MB / 92.6 MiB; 596 assets plus `profile.json` |
| `lemma-L-bundle.zip` | 223,898 bytes | Genuine four-file sample, flat at archive root |
| Extracted L bundle | 4 files / 226,089 bytes | Capsule, manifest, journal and 223,522-byte cryptographic receipt |

Use Windows x64 with ordinary writable directories you control. No separately
installed Python, Lean, compiler, prover or guest image is required. Windows
system DLLs remain host dependencies; another physical machine has not been
qualified. Allow extra disk space for ZIPs and each operation's snapshots/logs.
The 96 MiB operation-storage ceiling is a maximum, not observed per-check use.

Installation, input bundle and output directory must not overlap. Output must
be new and have an existing parent. Avoid junctions/symbolic links and linked
path ancestors. Keep logs and extra files outside the installation and bundle.

## 1. Check both archives and extract fresh copies

Run this in PowerShell. The first paths use the current local handoff. If you
move the archives elsewhere, change their paths and the new operator directory;
retain the independently adopted checksums. Nothing below overwrites the
already tested installation or an existing check.

```powershell
$v3Project = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
Set-Location -LiteralPath $v3Project
$v3Archive = Join-Path $v3Project 'product-local\certified-verifier-package-01\mathematical-commons-v3-receiver.zip'
$v3SampleArchive = Join-Path $v3Project 'deliverables\2026-09-28-v3-tentative\lemma-L-bundle.zip'
$v3UseRoot = Join-Path $v3Project 'product-local\receiver-operator-01'
$v3ArchiveSha = 'db862cc0c0b86a53d7f9e47c9c5c32ba4cc4406f805d1f08d6fb37b78b4f9ec4'
$v3SampleSha = 'd6f2012e152b77e0e51ad189e156769c76ceddc9dd4604c4480fbbeac6f561f9'

if ((Get-FileHash -LiteralPath $v3Archive -Algorithm SHA256 -ErrorAction Stop).Hash.ToLowerInvariant() -ne $v3ArchiveSha) {
    throw 'Receiver archive checksum mismatch; do not extract or execute it.'
}
if ((Get-FileHash -LiteralPath $v3SampleArchive -Algorithm SHA256 -ErrorAction Stop).Hash.ToLowerInvariant() -ne $v3SampleSha) {
    throw 'Sample archive checksum mismatch; do not use it.'
}
if (Test-Path -LiteralPath $v3UseRoot) {
    throw 'Choose a new operator directory; preserve the existing one.'
}
New-Item -ItemType Directory -Path $v3UseRoot -ErrorAction Stop | Out-Null
Expand-Archive -LiteralPath $v3Archive -DestinationPath (Join-Path $v3UseRoot 'unpacked') -ErrorAction Stop
Expand-Archive -LiteralPath $v3SampleArchive -DestinationPath (Join-Path $v3UseRoot 'lemma-L') -ErrorAction Stop
$v3Receiver = (Resolve-Path -LiteralPath (Join-Path $v3UseRoot 'unpacked\certified-receiver') -ErrorAction Stop).Path
$v3Bundle = (Resolve-Path -LiteralPath (Join-Path $v3UseRoot 'lemma-L') -ErrorAction Stop).Path
$v3ProfileSha = '6dc5cef431843e15ec6e8647892a0462bc5bd7a76554d541ff76d4d8719af297'
if ((Get-FileHash -LiteralPath (Join-Path $v3Receiver 'profile.json') -Algorithm SHA256 -ErrorAction Stop).Hash.ToLowerInvariant() -ne $v3ProfileSha) {
    throw 'Profile checksum mismatch; do not execute this receiver.'
}
```

The sample extraction contains exactly `bundle.json`, `capsule.json`,
`journal.bin`, `receipt.bin`, with no enclosing directory. No research-run path
is needed by the invocation. For other contributions, obtain an ordinary
four-file bundle and supply its path instead; do not create a fake receipt
from an expected journal or a copied success record.

Learn the receiver archive/profile checksum from an independently trusted
handoff, not solely from an untrusted sender together with its archive.
Independent adoption says **which checker you trust**. The full wrapper also
checks every installed asset before and after verification. Preserve the
installation exactly: added caches, files or edited documentation may refuse.

## 2. Verify the sample once

Continue in the same PowerShell session:

```powershell
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

For another bundle change `$v3Bundle` to its ordinary absolute directory and
choose a new check name. Exactly one verification is attempted. There is no
automatic retry, proof generation or fallback to native acceptance. These are
normal operator commands, not instructions to repeat the research campaign.

The selected profile permits at most 120 worker CPU seconds, 180 sampled wall
seconds and 1 GiB worker private commit, with separate controller ceilings of
120 CPU seconds and 512 MiB. These are checked finite limits, not hard real-time
overshoot guarantees. A limit refusal does not authorize removing checks or
editing the pinned profile in place.

## 3. Interpret success or refusal

Successful completion requires exit code `0` and this exact status:

```text
PASS_EXPERIMENTAL_COLD_CERTIFICATE_VERIFIED_NOT_NATIVE_ADMISSION
```

The same fresh `RESULT.json` records `receipt_verified: true`,
`native_admission: false`, one real verifier call, no cleanup errors and a
closed Job with zero active processes. It retains actual commands, byte pins
and accounting. Four exact input snapshots are under `inputs`; verifier logs
are under `logs`. The private `cold`/`temp` directories are not proof inputs.

Anything else is **not accepted**. Read `error`, `final_error`,
`cleanup_errors` and `logs\stderr.txt` where present. A preallocation refusal
may print `REFUSED_NO_SUCCESS` without creating `RESULT.json`. Retain failed
outputs and costs; do not overwrite them or edit a result to mark acceptance.
The wrapper always prints final controller accounting to stderr, so stderr
output alone does not indicate failure.

A changed asset, malformed bundle, wrong image/journal, invalid seal or
resource exhaustion can cause refusal. That does not necessarily prove the
mathematical proposition false; this invocation simply did not establish the
required certificate. A copied RESULT is a local observation, not a portable
proof token. Another receiver must verify the actual bundle itself. Do not
replace the wrapper with the driver's private `stage` branch or a raw success
marker.

## What has actually been measured

The qualified positive command used the copied Python and public wrapper from
the ZIP-extracted installation. It took **2.1469851 seconds wall time and
1.375 inclusive worker CPU seconds**, including installation checking and the
verifier child process. The verifier's internal marker reported 13 ms; that
is **not** the complete receiver cost. These are one machine/one sample,
not a throughput benchmark or a guarantee for other bundles.

The actual test also refused:

- A canonical one-word seal corruption, through the complete wrapper.
- A forged outer journal with a matching expected journal, at the installed
  driver's claim-binding gate.
- A wrong expected image with corresponding expected-image journal.
- A wrong expected packet commitment in the journal.

The last three deliberately test the installed driver directly to reach the
specified binding boundary; they are not three additional whole-wrapper tests.
All selected Jobs closed with no active processes or terminations. The phase
made zero native Lean, guest-execution or proof-generation calls. The genuine
receipt is 223,522 bytes; the sample's rank is zero and it has no parent
assumptions. **This receiver test does not test recursive assumption discharge.**

These costs exclude proof production, earlier failures, setup and the separate
test controller. Proof generation was expensive and its retained costs are not
erased by cheap verification. No net end-to-end speedup, useful-growth or
exponential-growth claim follows from this measurement.

## Fixed assurance boundary

The receipt concerns the exact capsule interface and all 148 journal bytes,
under logical profile `dmkn-experimental-certified-01`, image
`7a8589ef226cc222696afa93f0fca96a0f3d56ca03fcdebdc9008f7e79a3f0d0`
and foundation
`4eeaab61471a4ab9f93209af9aad66fcb45f6322783b919851d4d95ea33f9f80`.

A real Succinct/Poseidon2 receipt binds successful execution of that checker
and a fully discharged final claim. This CLI has no argument for ancestor
proof bodies, proof-history archives, source proofs, global ledgers or a guest
image file, and it does not generate a new proof. The qualified path verifies
the bundle without supplying such ancestry to its verifier process. Cold
means a fresh verifier with these explicit inputs; it does not mean a second
physical machine or an OS sandbox denying all unrelated file access.

The guest uses an experimental external checker. Its equivalence to Lean's
native kernel and production adaptive recursive assurance are not established
by these finite tests. Therefore successful receipt verification must **not**
be interpreted as native Lean admission or permission to inject an unproved
axiom into ordinary Lean. A contributor/importer needs its own separately
qualified certified interface and verification path; alternatively, unchanged
native v2 performs its normal native checks. This archive is not that full
contributor or decentralized node.

Correctness certificates do not establish importance, novelty, availability
or mathematical usefulness. The independent ordinary-child certificate
campaign is a separate central gate; its outcome must be read from its actual
final report, not inferred from this rank-zero sample.

## Evidence and historical notes

The actual receipt-phase result has SHA-256
`1108b785ab5795b73bd9eb9ce6dae514123164829bd3034402774db99ab89cac`.
Its independent outcome audit is
`experiments/certified-verifier-integration-01/RECEIPT-OUTCOME-AUDIT.md`, SHA-256
`1a41897e5a57a289741184c812b19c1a8296b4637daea69182c590fce7a08188`.
The genuine sample receipt SHA-256 is
`5ac187a57279f2fbaeab05dc37cc302541ca006bbb5fd172a22ccde54ab2e4d7`.
Root's dated delivery results and integrity report bind the final handoff;
the research paths are evidence references, not mandatory runtime inputs.

Included frozen `API.md`/`PLAN.md` retain their historical source-only wording.
This dated actual receiver result supersedes that wording **only for the
qualified archive/startup/L-receipt/refusal scope above**. It does not silently
qualify an installed contributor, arbitrary Lean support, production recursive
security or the entire commons. No package file was edited and no runtime
was rerun to author this guide.
