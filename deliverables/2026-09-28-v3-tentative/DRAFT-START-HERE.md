# Tentative v3 receiver — DRAFT, not yet release-qualified

This is a draft handoff guide, not an announcement that v3 or the broader
mathematical commons is complete. Root must add the final archive checksum,
actual qualification report and exact supported claims before promoting it.
The current selected installation is known; packaging, relocation/startup and
real cold-verification outcomes must be adopted independently. Licensing is
undecided. This is a local internal package, not authorization to publish or
redistribute it.

## What this component does

It checks one proof-carrying mathematical bundle without installing Lean or
downloading the proof histories of all its ancestors. A bundle contains exactly
four files: `bundle.json`, `capsule.json`, `journal.bin`, `receipt.bin`.

The capsule describes the formal proposition. The journal ties that proposition
to a particular mathematical foundation and checker. The cryptographic receipt
attests that the adopted checker produced that journal. The receiver checks
both the structural binding and the real receipt; a peer's success label is
not enough. This is a receiver, not the entire decentralized research network
or an autonomous theorem generator.

## The layers, in plain language

| Layer | Job | What it does not establish |
|---|---|---|
| Formal object | Give the exact typed proposition and its foundation commitment | Importance, novelty or human intention |
| Mathematical checker | Check the contribution under a fixed experimental guest program | A proved equivalence between this checker and Lean's kernel |
| Cryptographic receipt | Certify execution of that exact checker and journal, with required assumptions discharged | A different checker or theorem merely because a peer labels it similar |
| Local receiver | Bind the four bundle files, verify the real receipt, enforce limits and report costs | Native Lean-node admission, theorem generation or global availability |
| Agents and exchange | Let independently operated agents obtain/reuse/contribute objects | This small archive does not yet supply the complete scalable loop |

Proof creation and proof verification have different costs. A succinct receipt
can make receiving a result cheaper without making the original proof cheap.
Producer costs and failed attempts must remain charged. This draft makes no
net useful-growth, exponential-growth or end-to-end speedup claim.

## What is in the archive

Expected archive name: `mathematical-commons-v3-receiver.zip`.
Expected extracted folder: `certified-receiver`.
Root must provide its actual independently adopted SHA-256 before release.

The selected tree contains596assets plus `profile.json`: about97.1MB before
zip compression, including its own Python runtime, verification executable,
six unchanged binding/helper/data modules and source/API notes. It excludes
Lean, a compiled guest-image file, SDK/compiler caches, ancestor proof packets
and private operator state. Windows system DLLs remain host dependencies.
Supported-host and relocation claims require the final actual test report.

No separate system Python or Lean installation should be required by this
receiver. Native v2 remains unchanged and separately available; this package
does not upgrade its state or silently add a new native acceptance mode.

## Run it after qualification

These are the intended PowerShell steps. Do not treat them as evidence that
the pending qualification gates have passed.

1. Obtain the archive and its checksum from an independently trusted local
   handoff. Check that checksum, then extract it to an ordinary directory you
   control. Preserve the extracted files exactly; added files can cause refusal.
2. Obtain an inert four-file bundle. Keep it outside the receiver directory.
   Select a fresh output path, with an existing owner-controlled parent.
   Installation, bundle and output paths must not overlap.
3. From the directory containing `certified-receiver`, run:

```powershell
$receiverPath = (Resolve-Path -LiteralPath '.\certified-receiver').Path
$bundlePath = (Resolve-Path -LiteralPath 'C:\MathBundles\example-bundle').Path
$resultPath = 'C:\MathChecks\check-001'

& "$receiverPath\runtime\python\python.exe" -B -E -s -S `
  "$receiverPath\cert_verify.py" `
  --profile "$receiverPath\profile.json" `
  --profile-sha256 '6dc5cef431843e15ec6e8647892a0462bc5bd7a76554d541ff76d4d8719af297' `
  --bundle $bundlePath `
  --run $resultPath
```

Replace the two example `C:\...` paths; `check-001` must not already exist.
The profile checksum above is the actual selected installation's checksum,
not a value to obtain from the untrusted bundle. If the final package selects
different bytes, root must supply a new adopted checksum and update this guide.

The successful status is
`PASS_EXPERIMENTAL_COLD_CERTIFICATE_VERIFIED_NOT_NATIVE_ADMISSION`.
Read the fresh `RESULT.json`, terminal exit and resource/cleanup outcome
together. On failure, retain the directory and diagnostics; do not edit a result
to mark it accepted or overwrite the same path. A copied RESULT is not a proof
token that another receiver may trust instead of verifying the receipt.

## Fixed trust boundary

Logical proof profile: `dmkn-experimental-certified-01`.

Foundation commitment:
`4eeaab61471a4ab9f93209af9aad66fcb45f6322783b919851d4d95ea33f9f80`.

Adopted checker image ID:
`7a8589ef226cc222696afa93f0fca96a0f3d56ca03fcdebdc9008f7e79a3f0d0`.

The receiver requires a real non-development succinct Poseidon2 receipt for
this exact image and all148bytes of the expected journal. Security depends on
the selected checker relation, its implementation, the cryptographic system
and parameters, hash assumptions, verifier implementation and supported host.
It does not prove the experimental Nanoda checker equivalent to Lean's kernel.
Successful checking is therefore precisely scoped experimental evidence, not
unqualified authority for all of mathematics.

The software assumes cooperative owner-controlled local files and a functioning
Windows host. Resource checks are sampled, not hard real-time guarantees.
“Cold” means a fresh verifier process supplied the receipt, journal and adopted
image identity, without ancestor proof inputs. It does not mean a different
physical machine or complete denial of every other filesystem read.

## Reading the included source notes

The byte-preserved `PLAN.md` and `API.md` contain historical “proposal” or
“not implemented/qualified” wording from source selection, and historical
research-path references. They are useful interface/design records, not the
final qualification status or mandatory paths on your machine. Once root
adopts actual results, the final dated handoff report must explicitly supersede
that historical status with its exact demonstrated scope. Until then, this
guide remains DRAFT/unqualified. Do not infer a pass merely from code existing
or a zip being created.

Remaining central work is an actual trustworthy ordinary-agent parent-to-child
contribution loop, honest full-workflow costs, usable installed contribution,
and broader scale/availability evidence. Attribution, mandatory root goals and
global task lists are not prerequisites for this receiver.
