# Mathematical commons: Windows v1 source candidate

2026-09-23. **Locally qualified Windows v1 source candidate: source09.**
Its focused census tests, fresh support build and installed mixed-role workflow
have passed their scoped independent audits. This is not a perfect release,
public deployment or completion of the global mathematical-commons goal.
The project license remains undecided; no external publication or deployment
is authorized. Do not substitute the failed source08 installation or its ZIP.

The final file-delivery gate is separate: consult
[HANDOFF-INTEGRITY.md](HANDOFF-INTEGRITY.md) for its exact checked scope and
disposition. If that adjacent report is missing, unsuccessful or does not bind
this archive and these release pages, treat the handoff as incomplete.

## The software

This is a decentralized Lean 4 mathematical commons framework. A local agent
can discover candidate results, obtain inert packages, freshly check them,
use admitted mathematics in its own source, and submit/publish a contribution.
An owner can serve selected publications and retained acquisitions together
through one finite, authenticated peer catalog. Receiving nodes still perform
their own mathematical admission; no central acceptance server is required.

Agents choose their investigations. There is no mandatory global task list,
shared root research goal, natural-language intention test or automatic agent
included. The download is software plus a selected foundation/common vocabulary,
not the complete body of mathematics or an already populated global network.

## Exact delivery

Use this exact packaging trio and the adjacent support/integrity reports:

| File | Identity / purpose |
| --- | --- |
| [math-commons-source.zip](math-commons-source.zip) | Source09, 3,782,752 bytes; SHA-256 `015894dea22164802b9683cf6545a6c9ab04ec2098c9fd9684b8fff34e9014ed` |
| [SOURCE-MANIFEST.json](SOURCE-MANIFEST.json) | 114 payloads, 20,300 bytes; SHA-256 `7d1aa2c3dd6a6592c79e522857cd684576c6a1308167f44c02e183744499306a` |
| [PACKAGE-RESULT.json](PACKAGE-RESULT.json) | Original 455-byte record; SHA-256 `41022e5cbd834c179e8a18dc0f6b778a6759601f6bfb21e30e21a551bcd2eb62` |
| [RESULTS.md](RESULTS.md) | Exact support, evidence and limitations |
| [HANDOFF-INTEGRITY.md](HANDOFF-INTEGRITY.md) | Required final copied-artifact/document check; consult its exact checked scope and disposition |

The source ZIP includes operator/agent documentation, source, immutable assets
and its manifest. It excludes runtime binaries, build outputs, used databases,
test state, credentials and experiment harnesses. A hash identifies bytes; it
does not authenticate an untrusted publisher, grant a license or prove a theorem.
Obtain expected digests through a deliberately trusted handoff.

## Prerequisites

Use Windows x64 and PowerShell 7 with exclusive cooperative-owner control of
fixed local NTFS, non-reparse directories. Supply the complete Lean 4.34.0
Windows runtime and the selected Python distribution separately. Always invoke
Python with `-B -E -s -S`. No third-party Python package installation is required
by these entrypoints; arbitrary Python/SQLite versions are not qualified.

The following Python prerequisite metadata was actually observed on this host:

| Component | Observed selection |
| --- | --- |
| Python | 3.14.6, build `c63aec6`, June 10 2026, MSC v1944, AMD64 |
| Standard-library SQLite | 3.50.4 |
| OpenSSL | 3.5.7, June 9 2026 |
| Python TLS capabilities | TLS 1.3 and ALPN available |
| Selected executable | `D:\Python314\python.exe` |
| PowerShell | 7.6.5.0; use the actual application path returned by `Get-Command pwsh` |

That executable's SHA-256 is
`03168c01b7b7491423350e82c26fee71f35b43694d1319d3c668bda6903a0c38`.
The supplied local Lean runtime is at
`E:\Distributed Trustworthy Mathematical Knowledge Network\software\runtime\lean-4.34.0-windows`;
the final support report binds the tested runtime selection. These local paths
are conveniences, not required installation names or public download links.
Executable pins are not whole-runtime attestations. There is no dependency
downloader or qualified clean-machine acquisition recipe in this package.

On this host, `Get-Command pwsh` resolves to
`C:\Users\Uisjs\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe`.
Replace the walkthrough's illustrative `$Pwsh` path with that actual path;
its `C:\Program Files\PowerShell\7\pwsh.exe` example is absent on this host.
Likewise replace all example runtime/deployment paths consistently. Do not
drop the required Python startup flags when substituting executable paths.

Provide the space margins in the extracted documentation. A default node's
initial free-space check is at least 5 GiB + 64 MiB, before additional runtime,
build, second-node and diagnostic needs. Logical resource grants are not OS
disk reservations or guarantees of continued supply.

## Start from the extracted ZIP

After the adjacent integrity report confirms the exact delivery:

1. First run `Get-FileHash -Algorithm SHA256 -LiteralPath <saved-file-path>`
   separately on the saved ZIP and adjacent `SOURCE-MANIFEST.json`, and compare
   both digests with the completed delivery table above. Do not proceed on a
   mismatch or a missing required integrity report. View
   `TLS-WALKTHROUGH.md` inside the verified ZIP without executing code, then
   follow its fresh-extraction, payload-verification and source-build recipe
   with your selected paths and these exact pins. Require the documented
   structured success for each command; a zero exit code alone is not
   mathematical acceptance.
2. Create new, separate install/state/scratch/build-work directories. Generate
   new owner keys using the included identity helper; never copy test keys,
   experimental `.olean` files or a used database. Configure and initialize
   fresh nodes using the walkthrough. No research directory or harness is
   needed for ordinary operation.
3. Give a local agent the extracted `AGENT-QUICKSTART.md` and `API.md`, its client
   label, current context/snapshot and owner-authorized peer aliases. The request
   helper creates a file only; `manage.py request` sends it to the local node.
   Keep returned handles and exact request bytes. Source is owner-authorized
   executable input, not a sandbox for arbitrary peer programs.
4. Use `HOSTING.md` for explicitly funded finite service. Sharing a view does
   not start hosting. A two-entry, one-page view needs four successful requests
   for its catalog, page and two bundles; the walkthrough's three-request
   singleton grant is not enough. No permanent daemon or autostart is installed.

The alternative `QUICKSTART.md` demonstrates explicit plaintext loopback; do
not combine its `--peer` configuration with the TLS guide's `--network` profile.
The current profile is config 6 / physical database 5, wire/catalog 2 and
stage-plan 2. Use fresh bound installations even when version numbers match.
There is no in-place upgrade or used-state migration.

Source09's only product delta from source08 repairs resolved-path namespace
comparison in live/output stage censuses and adds bounded refusal diagnostics.
The 4096-entry cap, byte/resource limits and mathematical checking are unchanged.
Its focused 12-test run and independent outcome audit pass. A separate fresh
source09 support build also passed; its receipt binds the selected Python and
Lean executables. The failed source08 build remains failed, with its cost
retained. The independently audited installed run published Beta from unchanged prior source,
served it with acquired-only D1 in one catalog after the original supplier
stopped, and freshly admitted both at a receiver. This is not new mathematical
authorship. Its disposition is
`PASS_SELECTED_SOURCE09_INSTALLED_MIXED_ROLE_NOT_WHOLE_V1`. These results do
not identify the old build failure's exact cause or establish whole-v1 readiness.

## Mathematical and operational boundaries

The checked corpus is extensible with new definitions and proofs within the
selected Lean capture/foundation/resource profile; it is not limited to a fixed
list of demonstration IDs. It does not promise arbitrary Lean4 or mathlib
compatibility. `Init` syntax availability does not imply that every dependency
can be captured. Additional axioms, unsafe/unsupported declarations or oversized
closures refuse; rejection for this reason is not a claim that a theorem is false.
See [RESULTS.md](RESULTS.md) for the tested scope and trust boundary.

Keep capacity and hosting finite. Use `status`, explicit `renew`, historical
context selection and documented recovery only where supported. On unknown or
pending outcomes, preserve requests/state/scratch and stop dependent work;
do not create another request ID as an automatic retry or reset counters.
Plan exposure before irreversible exhaustion; general restore, migration and
indefinite retention are not provided.

Same-host tests do not establish independently hosted deployment, Internet
availability, broad retrieval quality or sustained/exponential growth. The
license is undecided: this local artifact does not grant public redistribution
rights. No external service is started or left running by this document.
