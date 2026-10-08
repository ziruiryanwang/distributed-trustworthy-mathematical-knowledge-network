# Mathematical commons v2: local release handoff

2026-09-23. **Local source13 v2 handoff.** Independent audit confirms the
selected reciprocal path: a node freshly checked a received Rose datatype,
used its main and auxiliary recursors in new count definitions, and returned
a theorem that the first node freshly admitted after the sender stopped.
The original literal-bearing theorem's publication refusal remains preserved;
the successful continuation used an explicitly revised statement spelling,
not a product patch or automatic normalization.

[QUALIFICATION.md](QUALIFICATION.md) states the exact evidence and limitations.
Delivery acceptance additionally requires a passing adjacent
`HANDOFF-INTEGRITY.md` binding the actual copied files and final versions of
both pages. An absent, failed or mismatched integrity report means the handoff
is incomplete. The source12 draft and its exact package remain separately
preserved at `../2026-09-23-v2-source12-draft`.

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
The selected Rose group has actual source12 native acceptance evidence.
Source12's attempted reciprocal contribution then safely refused an advertised
auxiliary name: Lean's checked kernel map and source-visible frontend map were
not both populated. Source13 registers the already-checked recursor in the
frontend and verifies both bindings; it does not invent a replacement theorem
or weaken checking. Actual Count source submission and substantive main/
auxiliary recursor use pass the selected independent audit. The separately
audited source-only continuation completes return publication, TLS transfer
and fresh receiving admission within the type fragment described below.
This is not support for every Lean construct or all of mathlib.

## Exact selected files

These are the actual source13 packaging identities in
`product-local/auxiliary-frontend-package-13`, bound by the fresh preparation
result. Root copied and hash-verified the unchanged trio here; final delivery integrity is
a separate required gate. Do not use the source12 draft archive
as a source13 repair, overlay a used installation or substitute predecessor pins.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| [math-commons-source.zip](math-commons-source.zip) | 3,797,631 | `d9d213e1b5a8b91dcefd2c238b35a3156910b4053a045f2d426b89b12bd9bca8` |
| [SOURCE-MANIFEST.json](SOURCE-MANIFEST.json) | 20,300 | `6a3e2b6aab0f6af14b15943a7510df3fb90606ca5213af56c29dee08704f5ecc` |
| [PACKAGE-RESULT.json](PACKAGE-RESULT.json) | 455 | `0c094c4509ce72a1def23624531c163c5cd321b3ff8b936f1e6b4db6cbacd1e2` |

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

## Install and run

The extracted `TLS-WALKTHROUGH.md` contains the complete verified installation,
owner identity, two-node pinned-TLS, finite hosting and reciprocal workflow.
Use its commands, replacing every example path consistently. Use the exact v2
pins above, not inherited examples or hashes from an untrusted download.

Set the guide's package variables as follows after the three delivery files
and final integrity report are present. `$Package` is an operator-selected
download directory; the path below names this local handoff.

```powershell
$Package = 'E:\Distributed Trustworthy Mathematical Knowledge Network\deliverables\2026-09-23-v2-local-release'
$ExpectedArchive = 'd9d213e1b5a8b91dcefd2c238b35a3156910b4053a045f2d426b89b12bd9bca8'
$ExpectedManifest = '6a3e2b6aab0f6af14b15943a7510df3fb90606ca5213af56c29dee08704f5ecc'
Get-FileHash -Algorithm SHA256 -LiteralPath "$Package\math-commons-source.zip"
Get-FileHash -Algorithm SHA256 -LiteralPath "$Package\SOURCE-MANIFEST.json"
$Pwsh = (Get-Command pwsh -ErrorAction Stop).Source
```

Keep this resolved `$Pwsh` value when following the guide; replace its
illustrative PowerShell executable assignment instead of overwriting this one.
Proceed only if the adjacent integrity report passes for these exact files.
Require exact hash agreement before extracting or executing package code.
Choose a fresh example deployment such as `E:\MathCommonsV2Demo01`, separate
from the project source and any existing deployment. In TLS-WALKTHROUGH
section 1, run its extraction and **all 114 payload** length/hash checks, but
stop before its final `build.py` command. Then build **exactly once** using the
snippet below. Alternatively use the guide's build command and skip this
snippet; never run both. Use the verified installation and separately supplied
runtime, and keep path variables consistent across both pages:

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
and P1 snapshot, and owner-approved peer aliases. Also give them this handoff's
Publication type fragment section below: the frozen packaged API does not
enumerate that newly encountered restriction. The normal sequence is:

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

### Publication type fragment

Successful `submit` does **not** guarantee `publish` will succeed. This cut's
public metadata/type-symbol index accepts only type-DAG variables, sorts,
constants, application, lambda and Pi (tags 0–5). Literal, let and projection
nodes in the public type currently refuse with
`CANDIDATE_TYPE_FRAGMENT:NATIVE_SYNTAX_OUTSIDE_TYPE_FRAGMENT`, even when the
submitted mathematical artifact passed native checking. This is a supported
publication-fragment limit, not evidence that its theorem is false.

For the encountered natural-number literal `1` in a theorem statement, the
selected source-level remedy is explicit `Nat.succ Nat.zero` in that statement,
with unchanged count definitions/proof and fresh native submission. This exact
continuation passed publication, return transfer and fresh admission.
Equivalent mathematical spelling changes the
formal type encoding and its content identity; the old literal-bearing theorem
does not thereby become published. The system does not automatically normalize
types or rewrite admitted packages. Do not infer from this specific equivalent
spelling that every rejected type has a supported or inexpensive translation.

### Continued work needs available capacity

Read `status` before planning further work. In the retained qualification
nodes, the successful exercise leaves A one authorized native stage and B
zero; B needs deliberate owner renewal before another `submit` or `admit`.
This is that experiment's consumed allocation, not a default imposed on a
fresh installation. The documented renewal path does not erase prior charges.

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
