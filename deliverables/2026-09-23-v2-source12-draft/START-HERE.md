# Mathematical commons v2: local release handoff

2026-09-23. **Draft handoff; final qualification and delivery integrity pending.**
This page selects the actual source12 package, not a new rebuild. Root copied
the archive, manifest and package receipt here and verified their exact hashes.
Do not interpret this draft or the directory name as a completed v2
release. [QUALIFICATION.md](QUALIFICATION.md) records passed and pending gates.
Final delivery also requires a passing adjacent `HANDOFF-INTEGRITY.md` binding
the actual copied files and final versions of both pages.

The previous completed [source10 local handoff](../2026-09-23-short-header-local-candidate/START-HERE.md)
remains available and unchanged.

## What the software does

Independent local agents discover mathematical candidates, check them with
Lean 4, use admitted definitions and theorems, and contribute checked results.
Peers exchange inert canonical packages; acceptance is performed by each
receiving node. No central acceptance server, shared root goal, global task
list or human-intention test is required. Research choices remain with the
local agent. The package does not contain a bundled autonomous researcher or
an already complete corpus of mathematics.

This successor adds the selected nested-inductive/auxiliary-recursor path and
completes publication of an inductive group itself, without a wrapper theorem.
Admission exposes checked receiving names and types for the group's members.
The selected Rose group has actual source12 native acceptance evidence;
reciprocal use and the changed native refusal controls are still pending in
this draft. This is not support for every Lean construct or all of mathlib.

## Exact selected files

These identities are the actual tested packaging output in
`product-local/group-roots-package-12`, copied unchanged beside this page.
Do not rebuild, overlay a used installation or substitute a predecessor's pins.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| [math-commons-source.zip](math-commons-source.zip) | 3,796,749 | `365c2727de1563d16e0981109ce44ead53298e7490a5cc6045218459c482c9e7` |
| [SOURCE-MANIFEST.json](SOURCE-MANIFEST.json) | 20,300 | `034cfbb7ae2b2121cfe930b0f40924aa737124ed4e6f4d8ac75780473f3d7b45` |
| [PACKAGE-RESULT.json](PACKAGE-RESULT.json) | 455 | `45a0e016d027ebb9cc2593f410d2784f33d4c355502d4328c19247176c67a51f` |

The archive contains 114 source payloads plus its manifest. It excludes Lean,
Python, prebuilt support, initialized nodes, private identities and experiment
outputs. The package receipt's original development-packaging status stays
unchanged; it is not the qualification report. A digest identifies bytes,
not a publisher, license, proof of safety or mathematical truth.

## Required environment

Use Windows x64, PowerShell 7, fixed local NTFS/non-reparse directories and
exclusive cooperative-owner control. Supply these runtimes separately:

- Complete Lean 4.34.0 Windows distribution.
- Qualified Python 3.14.6 distribution with SQLite **3.50.4**, OpenSSL 3.5.7,
  TLS 1.3 and ALPN. An arbitrary Python 3.14 installation is not equivalent.
- The real PowerShell 7 executable resolved by `Get-Command pwsh`; do not
  assume the walkthrough's illustrative `C:\Program Files\PowerShell\7` path
  exists on your machine.

Always invoke Python with `-B -E -s -S`. There is no runtime downloader or
third-party Python installation step in this package. Runtime executable pins
and the trust boundary are recorded in [QUALIFICATION.md](QUALIFICATION.md).
Those pins are not complete-distribution attestations or a clean-machine test.

Keep installation, runtime, each node's state/scratch, private keys, and
operator request files in their documented nonoverlapping domains. A node's
state and scratch must share a fixed local NTFS volume. The default node
requires a free-space sample of at least **5 GiB + 64 MiB**, excluding extra
runtime/build/second-node needs. Space checks are not OS reservations. Use
fresh installation/build/state/scratch directories; no in-place upgrade or
old-database migration is provided.

## Install and run after final handoff acceptance

The extracted `TLS-WALKTHROUGH.md` contains the complete verified installation,
owner identity, two-node pinned-TLS, finite hosting and reciprocal workflow.
Use its commands, replacing every example path consistently. Use the exact v2
pins above, not inherited examples or hashes from an untrusted download.

Set the guide's package variables as follows after the three delivery files
and final integrity report are present. `$Package` is an operator-selected
download directory; the path below names this local handoff.

```powershell
$Package = 'E:\Distributed Trustworthy Mathematical Knowledge Network\deliverables\2026-09-23-v2-local-release'
$ExpectedArchive = '365c2727de1563d16e0981109ce44ead53298e7490a5cc6045218459c482c9e7'
$ExpectedManifest = '034cfbb7ae2b2121cfe930b0f40924aa737124ed4e6f4d8ac75780473f3d7b45'
Get-FileHash -Algorithm SHA256 -LiteralPath "$Package\math-commons-source.zip"
Get-FileHash -Algorithm SHA256 -LiteralPath "$Package\SOURCE-MANIFEST.json"
Get-Command pwsh
```

Require exact hash agreement before extracting or executing package code.
Choose a fresh example deployment such as `E:\MathCommonsV2Demo01`, separate
from the project source and any existing deployment. Follow the guide's
extraction and **all 114 payload** length/hash checks before building. Build
with the verified installation and separately supplied runtime:

```powershell
# Example values: choose actual fresh paths and the qualified runtime.
$Py = 'D:\Python314\python.exe'
$Demo = 'E:\MathCommonsV2Demo01'
$Install = "$Demo\install"
$Lean = 'E:\MathCommonsRuntime\lean-4.34.0-windows'
& $Py -B -E -s -S "$Install\build.py" --lean-runtime $Lean --work "$Demo\build-work-01"
```

Require exit zero and `LOCAL_SUPPORT_BUILD_COMPLETED_NOT_MATH_ACCEPTANCE`.
Then continue the guide's fresh identity and configuration steps, using actual
DER certificate pins, never test keys. `CONFIGURED_NOT_INITIALIZED` is not
bootstrap acceptance; each owner `init` must return `OK, accepted:true`.
Do not build/configure twice or delete a failed allocation to make it look new.

For existing configured nodes, these are the central public entry points:

```powershell
# $Config and $Request are actual absolute paths selected by the operator.
& $Py -B -E -s -S "$Install\manage.py" status --config $Config
& $Py -B -E -s -S "$Install\manage.py" request --config $Config --request $Request
```

The first reports current heads, capacity and pending work, with no ordinary
request/stage credit; it writes administrative evidence in scratch. It does not
recheck old mathematical files. The second sends the saved exact request once.
`make_request.py` creates request files but does **not** send them. Preserve
request IDs and original bytes; an uncertain response is not permission to
invent a replacement request ID.

Give agents the extracted `AGENT-QUICKSTART.md`, `API.md`, current local context
and P1 snapshot, and owner-approved peer aliases. The normal sequence is:

1. `peer-find` / `peer-acquire`, then fresh local `admit` for a selected result.
2. Author locally against the returned checked receiving interface; `submit`.
3. `publish` against the current P1 snapshot; `expose` the local publication.
4. The owner separately funds finite `host` or `serve`; another node acquires
   and freshly checks the result. Exposure does not start a server.

Acquisition changes P1's snapshot; admission changes the accepted context.
Use actual current replies, not initialization handles after later changes.
Returned `leanName` is the receiving Lean spelling; use the canonical
`name/reference/type/u` fields as formal authority. Do not split pretty names
to reconstruct canonical names. Group auxiliary recursor types and universe
arities must be read from the checked interface, not guessed.

The complete guide also documents custody-only and mixed catalogs. They
share retained results without claiming new mathematics. Finite hosting
requires enough catalog/page/bundle allowance and an explicit owner grant;
there is no permanent central server, automatic listener or indefinite service.

## Stop conditions and scope

Local Lean source is executable owner-authorized input, **not hostile-code
sandboxed**. Peers supply only bounded inert packages. On refusal, blocked or
unknown state, lost replies, or uncertain cleanup, preserve requests, replies,
state and scratch. Read `RECOVERY.md` and `API.md`; do not reset counters,
delete journals, or edit installed/configured bytes. Narrow recovery does not
cover arbitrary corruption, power loss or missing evidence.

This handoff targets local same-host use. No second physical host was available;
independent-host/Internet operation, complete global discovery, permanent
retention, broad-library compatibility and sustained useful growth are not
established. Licensing remains undecided; no public redistribution permission
or external publication/deployment authorization is supplied. The broader
mathematical-commons goal remains open.
