# Use the prebuilt mathematical investigator

This handoff lets you use the already built investigator package without compiling
its support or applying six overlays yourself. It preserves the exact 154 package
files and their existing mathematical checking rules. You still need approved
external runtimes, your own local state/data and explicit operation budgets.
This is not an automatic installer, runtime downloader or mathematical database.

**Keep this guide outside the package and use it as the current entrypoint.**
The package's own historical README remains unchanged. The companion coherent
commons source handoff provides the current selector, query companions, mirror
and operational guides. Obtain that existing source archive separately; do not
copy its files into the hash-bound runtime package or rebuild merely to use it.

Everything remains **local and unpublished**, and the license is undecided.
Neither this handoff nor its receipt authorizes redistribution, external deployment
or a public release. Selected components have scoped local evidence; packing is
not a new proof, native execution result or completion of the full v5 goal.

## What to obtain and approve

You need two distinct kinds of approved files:

- This prebuilt `package.zip`, its external `RECEIPT.json` and this current guide.
  The ZIP contains only the 154 unchanged runtime-package files. Its receipt
  records the complete map, archive digest and selected PROFILE/INSTALLATION.
- The existing coherent commons source archive and its own approved receipt.
  Its root `README.md` explains source verification. It supplies scripts such as
  `software/v5/ordinary_multi_source_package/prepare_selected.py` and the two
  query companions; these intentionally stay outside the runtime package.

Independently approve the executable package, sources and runtimes **before
running any supplied Python or native code**. Obtain the expected archive digest
through an independently trusted selection/channel; a receipt traveling beside
an untrusted ZIP does not authenticate either. File hashes identify bytes, not
publisher reliability or software safety. An approved archive remains executable
software, not inert peer mathematical evidence.

The current exact package identifiers are:

| Item | SHA-256 |
|---|---|
| PROFILE.json | `ca257419f464c2e9d968011983673160377f743ebbe2a27e2399b510dce1ce67` |
| installation/INSTALLATION.json | `32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2` |

These identify this already built version, not arbitrary future builds. The
terminal packing receipt must say
`PACKED_AND_RELOCATED_EXACT_PREBUILT_NOT_EXECUTED`, with 154 files and 39,148,493
payload bytes. That status covers exact packaging/relocation only. It is not a
substitute for source/runtime approval or evidence that an operator command ran.
Partial output without the terminal receipt is not a successful handoff.

## External runtime requirements

Use independently approved **Windows x86-64, little-endian, 64-bit**, and the
exact selected **Python 3.14.6 / Lean 4.34.0** distributions. Run the actual selected
Python with `-I -S -B`. Version strings alone are insufficient: INSTALLATION pins
python.exe/python3.dll/python314.dll and Lean's bin/lean.exe, libInit_shared.dll,
libc++.dll and libleanshared.dll/libleanshared_1.dll/libleanshared_2.dll.

Provide their complete ordinary runtime support: Python stdlib, SQLite and TLS;
Lean libraries/toolchain components used by the chosen operations. Those nine
named hashes do not attest all transitive runtime/OS dependencies. Do not replace
them with a newer interpreter or assume Linux/macOS support. This prebuilt route
avoids compiling the investigator's helper software; it does **not** remove Lean
from mathematical authoring/checking or make proof checking free.

Use protected ordinary absolute Windows drive paths, without symlinks, reparse
points or shared hard-linked files. Keep package, source, runtime and state under
authorized local control. Windows Jobs constrain resources, not filesystem or
network privileges: they are not a hostile-source sandbox. Never automatically
execute received projects, source, plugins or compiled theorem artifacts.

## Extract once into a fresh directory

After independently approving the receipt and expected archive digest, select
real paths. The placeholder below must come from that independent approval,
not be computed from the ZIP and treated as its own authentication:

```powershell
$prebuiltArchive = 'C:\commons-downloads\package.zip'
$prebuiltExpectedSHA = 'REPLACE_WITH_INDEPENDENTLY_APPROVED_ARCHIVE_SHA256'
$prebuiltPackage = 'C:\commons-packages\investigator-01'
if ((Get-FileHash -Algorithm SHA256 -LiteralPath $prebuiltArchive -ErrorAction Stop).Hash.ToLowerInvariant() -cne
    $prebuiltExpectedSHA) { throw 'Archive identity mismatch; do not extract or execute.' }
if (Test-Path -LiteralPath $prebuiltPackage) { throw 'Select a fresh package directory.' }
Expand-Archive -LiteralPath $prebuiltArchive -DestinationPath $prebuiltPackage -ErrorAction Stop
if ((Get-FileHash -Algorithm SHA256 -LiteralPath "$prebuiltPackage\PROFILE.json" -ErrorAction Stop).Hash.ToLowerInvariant() -cne
    'ca257419f464c2e9d968011983673160377f743ebbe2a27e2399b510dce1ce67') { throw 'Wrong extracted PROFILE.' }
if ((Get-FileHash -Algorithm SHA256 -LiteralPath "$prebuiltPackage\installation\INSTALLATION.json" -ErrorAction Stop).Hash.ToLowerInvariant() -cne
    '32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2') { throw 'Wrong extracted INSTALLATION.' }
```

Keep the archive, receipt and this guide outside `$prebuiltPackage`. Check the
extracted PROFILE and INSTALLATION hashes against the exact selected values
above and preserve the full receipt map for independent inspection. Do not add
files, replace manifests or execute anything from a partial extraction. The
unchanged public launcher checks its bootstrap support, and the product loader
checks its manifest-bound executable/support roles and named runtime attachments
before use. The archive packer separately checks all 154 files, including the
eight historical documents; runtime loading does not recheck those documents.
The offline selector and `--help` alone do not validate all native artifacts.

## Start using it; skip build and overlay stages

Verify the separate coherent source extraction following its root README. Then
set the current guide's variables to the already extracted runtime package:

```powershell
$investigatorSource = 'C:\commons-source'
$investigatorPythonRoot = 'C:\tools\Python314'
$investigatorPython = "$investigatorPythonRoot\python.exe"
$investigatorLean = 'C:\tools\Lean434'
$investigatorWork = 'C:\commons-work' # Select an existing protected parent directory.
$investigatorPackage = $prebuiltPackage
$investigatorProfile = 'ca257419f464c2e9d968011983673160377f743ebbe2a27e2399b510dce1ce67'
```

In `software/v5/ordinary_investigator_bundle/guides/BUILD-MODULE.md`, skip the
entire native build and overlay instructions: the exact-module **and** multi-source
overlays are already present. Start at the operation-selection/initialization
instructions, using the current multi-source selector, not that guide's older one:

```powershell
& $investigatorPython -I -S -B `
  "$investigatorSource\software\v5\ordinary_multi_source_package\prepare_selected.py" `
  --package $investigatorPackage --profile-sha256 $investigatorProfile `
  --request 'C:\commons-requests\request.json' `
  --output 'C:\commons-requests\prepared-01'
```

The request path must contain your actual complete chosen operation, not a
preprovided research task. Preparation writes inert configuration/arguments; it
does not execute them. Inspect the result and launch the chosen operation through
the unchanged package's `run.py` with the selected runtimes, fresh diagnostics,
finite wall/CPU/memory/process/output limits and its full terminal closure checks.
The complete invocation forms are in the source handoff's current guide and
`software/v5/ordinary_network_kit/START-HERE.md`, with this selector override.
Do not call a private worker/preparer to bypass validation.

For a new mathematical owner, initialize your **own** fresh catalog/custody with
explicit persistent limits and retain its actual checked parent root. No author's
owner state is supplied. For an existing compatible owner, preserve its original
store ID/limits and follow update/recovery rules; do not initialize again to get
newer reports. Old-PROFILE reports remain old reports. The multi-source source
guide explains the direct public receive route for an explicit existing parent;
never edit a report to force selector acceptance.

Use `software/v5/ordinary_investigator_bundle/guides/QUESTIONS.md`,
`software/v5/METHOD-DISCOVERY.md` and
`software/v5/ordinary_investigator_bundle/guides/CONTINUE.md` in the source handoff
with this actual package/PROFILE for formal discovery, checked acquisition, local
Lean theory development and returning selected mathematics. No pre-existing Lean
project or central research agenda is required. Actual peers and mathematics are
not created by extraction; choose the smallest adequate offline/local route first.
Storage-only mirror operators use their existing source/Python companion instead
and do not need this native investigator download.

Preserve errors and outputs: failure need not roll back accepted-state prefixes.
Never delete locks, rewrite recovery markers or silently renew an exhausted
allocation. Use the current source handoff's `software/v5/UPDATE-AND-RECOVERY.md`
and exact context identities. Retrieval and search still do not establish truth;
independent checking remains required. No automatic update, relay or service runs.

## Maintainer-only archive production

Recipients do not need this utility. An independently approved maintainer may run
`pack_handoff.py --package <exact-approved-package> --assembly-receipt <original-assembly-receipt>
--output <fresh-output-leaf>` using approved Python `-I -S -B`. The exact selected
PROFILE, INSTALLATION and original ASSEMBLY digest are fixed in that utility;
it cannot package an arbitrary application. No native/product imports occur.

It writes deterministic ZIP_STORED `package.zip`, validates its actual member
bytes/metadata, extracts once into fresh `relocated/`, verifies the exact complete
tree, copies this guide outside it, rechecks inputs and then writes terminal
`RECEIPT.json`. The relocation is a maintainer validation artifact, not shipped
owner state or an extra installation step for recipients. Keep the original
ASSEMBLY receipt unchanged; its historical source path is not a runtime dependency.
Cooperative ceilings are 120 wall/60 CPU seconds; use approved enclosing process
containment when hard limits are needed. All failures retain partial outputs;
there is no overwrite, automatic retry, cleanup, runtime download or publication.
