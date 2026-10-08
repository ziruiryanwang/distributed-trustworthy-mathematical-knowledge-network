# Operator quickstart: current Windows development cut

2026-09-21. **Source-grounded draft; not yet qualified by a fresh operator.**
This is a normal command/API walkthrough, not a release announcement. The
current tree includes newly integrated replica work whose qualification is
separate. Older passing tests apply to their preserved source cuts, not
automatically to every command below. Do not use a historical installation for
this walkthrough or edit an installation already bound to node state.

## Prerequisites and directories

Use Windows x64, the complete Lean 4.34.0 Windows distribution, and the selected
Python distribution used for qualification (`D:\Python314\python.exe` here).
The store **requires SQLite 3.50.4** in Python's standard-library `sqlite3`;
an arbitrary Python 3.14 installation is not a qualified substitute. Python
must support the Windows runtime/Job interfaces. No third-party Python package
installation is specified by these entry points. Always pass `-B -E -s -S`.

There is a locally packaged development source archive, but no public release,
dependency acquisition command or independently reproduced clean-machine recipe.
The archive is unsigned and the project license remains undecided. A
maintainer must first supply a selected complete source cut containing
`build.py`, `manage.py`, `py/`, `native/`, `assets/`, and `assets-lock.json`, plus
the selected runtimes and their integrity/version information. Do not copy
prepared experiment outputs, an old `build/`, or node databases into a new
installation. The following paths are **example operator choices**, not
existing downloadable artifacts:

| Purpose | Example |
| --- | --- |
| Fresh installation, with no `build/` yet | `E:\MathCommons\install` |
| Complete Lean runtime | `E:\MathCommons\lean-4.34.0-windows` |
| Fresh build work, initially absent | `E:\MathCommons\build-work-001` |
| Alpha state / scratch, initially absent | `E:\MathCommons\alpha-state` / `E:\MathCommons\alpha-scratch` |
| Beta state / scratch, initially absent | `E:\MathCommons\beta-state` / `E:\MathCommons\beta-scratch` |
| Owner request files | `E:\MathCommons\requests` |

Create the request-file directory using your normal file manager/editor. Write
request files as UTF-8 JSON, without a BOM, duplicate keys, comments, or extra
fields; preserve each file unchanged after first use. JSON path separators in
strings must be escaped (`\\`) or written `/`.

State and scratch must be distinct nonoverlapping directories on the **same
fixed local NTFS volume**, outside installation/runtime. Do not use drive roots,
network shares, reparse-point substitutions, or competing untrusted writers.
The selected runtime may instead be inside installation, but may not contain it.
Default node configuration needs a free-space sample of at least 5 GiB + 64 MiB
(4 GiB remaining authorization + twice the 32-MiB metadata cap + 1 GiB margin).
Provide extra space for runtimes, builds, other nodes and diagnostics. This is
not an OS disk reservation or a guarantee against disk loss.

## Build and initialize

Run these in PowerShell. Replace all example paths consistently. Build once for
this fresh installation; support compilation is not mathematical acceptance.

```powershell
& 'D:\Python314\python.exe' -B -E -s -S 'E:\MathCommons\install\build.py' --lean-runtime 'E:\MathCommons\lean-4.34.0-windows' --work 'E:\MathCommons\build-work-001'
& 'D:\Python314\python.exe' -B -E -s -S 'E:\MathCommons\install\manage.py' configure --state 'E:\MathCommons\alpha-state' --scratch 'E:\MathCommons\alpha-scratch' --lean-runtime 'E:\MathCommons\lean-4.34.0-windows' --client local --peer beta=43112
& 'D:\Python314\python.exe' -B -E -s -S 'E:\MathCommons\install\manage.py' configure --state 'E:\MathCommons\beta-state' --scratch 'E:\MathCommons\beta-scratch' --lean-runtime 'E:\MathCommons\lean-4.34.0-windows' --client local --peer alpha=43111
```

Require `LOCAL_SUPPORT_BUILD_COMPLETED_NOT_MATH_ACCEPTANCE`, then
`CONFIGURED_NOT_INITIALIZED` for each configure. Stop on any different outcome;
retain partial build/configuration paths. Do not delete them to force a retry.
This two-state, shared-installation example is **same-host only**, not independent
administration or multi-host deployment. Peers are immutable configured aliases
to literal loopback ports; at most two aliases are allowed.

Save this as `alpha-init.json`:

```json
{"client":"owner","request_id":"init-001","op":"init","args":{}}
```

Invoke it, and separately create/invoke `beta-init.json` with the same contents
against Beta's configuration:

```powershell
& 'D:\Python314\python.exe' -B -E -s -S 'E:\MathCommons\install\manage.py' request --config 'E:\MathCommons\alpha-state\config.json' --request 'E:\MathCommons\requests\alpha-init.json'
& 'D:\Python314\python.exe' -B -E -s -S 'E:\MathCommons\install\manage.py' request --config 'E:\MathCommons\beta-state\config.json' --request 'E:\MathCommons\requests\beta-init.json'
& 'D:\Python314\python.exe' -B -E -s -S 'E:\MathCommons\install\manage.py' status --config 'E:\MathCommons\alpha-state\config.json'
```

Initialization must return `status:"OK", accepted:true`. Retain each node's
`contexts.local` and `snapshots.P1` separately. Status reports authorization,
usage, pending state and heads without ordinary request/stage charges, but writes
bounded diagnostic evidence in scratch. It does not recheck live mathematical
files. Stop for pending/unknown state or insufficient capacity.

## Submit and publish locally

All following ordinary JSON examples use `manage.py request` exactly as above,
with the indicated node's configuration and a separate saved request file.
`UPPERCASE_HANDLE` strings are placeholders: replace them with the complete
returned strings. Never construct handles or move one between nodes/clients.
IDs/client labels contain 1–64 ASCII letters, digits, underscores or hyphens.

On Alpha, save `alpha-submit.json`:

```json
{"client":"local","request_id":"submit-001","op":"submit","args":{"context":"ALPHA_CONTEXT","source":"universe u\nnoncomputable def Compose (A B C : Sort u) (g : B -> C) (f : A -> B) (a : A) : C :=\n  g (f a)\n","root":"Compose"}}
```

This composition shape has genuine checking evidence on an earlier cut; this
guide itself remains unexecuted. Successful submission returns `accepted:true`
and `artifact`. It does **not** publish or advance the context. Publish it:

```json
{"client":"local","request_id":"publish-001","op":"publish","args":{"artifact":"ALPHA_ARTIFACT","snapshot":"ALPHA_CURRENT_P1_SNAPSHOT"}}
```

Use the initial P1 snapshot if no intervening publication/acquisition changed
it. Otherwise obtain current handles with a new ordinary request:

```json
{"client":"local","request_id":"info-001","op":"info","args":{}}
```

`info` returns `context`, `snapshots.P1` and historical checked descriptions.
Publication success returns `candidate` and a new `snapshot`; its candidate-only
flags correctly do not grant acceptance to another node. Local enumeration is:

```json
{"client":"local","request_id":"find-001","op":"find","args":{"provider":"P1","limit":4,"max_bytes":16384}}
```

Continue a page with the returned `snapshot` and `cursor`, keeping `limit` and
`max_bytes` fixed and using a fresh ID. This is enumeration, not a global query
engine. Candidate metadata is untrusted until local admission.

### Source and reuse profile

Source is inline, at most 65,536 UTF-8 bytes; `root` names one declaration.
It runs as **owner-authorized executable local input**, not sandboxed arbitrary
peer code. The environment reconstructs selected formal declarations; it is
not an ordinary imported mathlib project with all tactics/notation. Use exact
receiving names from `description`, not the producer's original source names.
Do not assume printed infix syntax is registered: use `Eq` instead of assuming
`=` works. Prefer `noncomputable def` for mathematical definitions; ordinary
`def` can request unavailable executable compiler infrastructure. Broader
syntax remains insufficiently documented/conformance-tested.

For a needed ordinary definition body, copy its complete public reference
projection into this separate inspection schema, then use `manage.py inspect`
instead of `request`:

```json
{"client":"local","context":"OWN_CONTEXT","reference":[1,"EXACT_PUBLIC_DEFINITION_ID_PROJECTION"],"max_bytes":65536}
```

The displayed `reference` is a placeholder shape; substitute the actual entire
projection, not a digest. Inspection returns canonical type/body information,
not a proof strategy or new acceptance.

## Expose, acquire, check and contribute back

On Alpha, explicitly expose the candidate returned by publication:

```json
{"client":"local","request_id":"expose-001","op":"expose","args":{"selected":["ALPHA_PUBLISHED_CANDIDATE"]}}
```

Use the returned `view` in another PowerShell terminal:

```powershell
& 'D:\Python314\python.exe' -B -E -s -S 'E:\MathCommons\install\manage.py' serve --config 'E:\MathCommons\alpha-state\config.json' --client local --view 'ALPHA_VIEW' --session alpha-serve-001 --port 43111 --seconds 360 --max-requests 128 --max-bytes 268435456
```

For explicitly bounded continued hosting of one view, see `HOSTING.md` and
`manage.py host`; this uses finite owner grants, not an automatic permanent daemon.

This command remains running until its finite session ends. In the receiving
terminal, inspect `alpha-scratch\services\alpha-serve-001\ready.json`; it must
appear while this same invocation is running and name the selected port/catalog.
A stale ready file is not proof of a live service. There is no public-network
or SSH setup step in this guide. On Beta, invoke these requests sequentially:

```json
{"client":"local","request_id":"peer-find-001","op":"peer_find","args":{"peer":"alpha"}}
```

Choose a row from its bounded catalog; use that row's receiver-owned `remote`:

```json
{"client":"local","request_id":"acquire-001","op":"peer_acquire","args":{"remote":"BETA_REMOTE"}}
```

Acquisition returns `candidate`, `acquisition` and `snapshot`, but **no native
acceptance**. After it succeeds the serving node need not remain online for
local admission. Use Beta's current context:

```json
{"client":"local","request_id":"admit-001","op":"admit","args":{"context":"BETA_CONTEXT","selected":["BETA_ACQUIRED_CANDIDATE"]}}
```

Require `accepted:true`; retain its new `context` and receiving `description`.
Beta may now investigate independently using those exact names, submit its own
source with the new context, and publish/expose the returned artifact/candidate
as above. Serve its view on 43112 with a fresh Beta session ID. Alpha then uses
its configured `beta` alias for its own find/acquire/admit sequence. Receiving
acceptance is always local; copying the producer's success is insufficient.

For custody without inventing a new theorem, the **new, separately qualifying**
operation is:

```json
{"client":"local","request_id":"replica-001","op":"replica_expose","args":{"acquisition":"BETA_ACQUISITION"}}
```

Its returned one-entry `view` uses the same `serve` command and original bytes.
Ordinary `expose` does not accept acquired-only entries. Replica exposure is
custody, not publication, proof of authorship or mathematical admission.

## Capacity, retries and failures

Defaults authorize 128 ordinary requests, 16 stages and 4 GiB cumulative
reserved bytes, not unlimited operation. Failed admitted work stays charged.
Owner configuration can initially choose `--initial-requests`,
`--initial-stages`, `--initial-reserved-mib`, `--initial-metadata-mib` and
`--context-packages`; do not edit initialized configuration. The five common
packages count toward the default 16-package context ceiling. Historical
context selection is available through the API; it does not enlarge one
proof's actual dependency closure.

After checking status and supplying physical capacity, save an owner grant:

```json
{"schema":1,"op":"renew","grant_id":"grant-001","config":"CONFIG_DIGEST_FROM_STATUS","add":{"requests":1,"stages":1,"reserved_bytes":142606336}}
```

Invoke `manage.py renew --config ABS_CONFIG --request ABS_GRANT` with the same
Python flags. Optional `metadata_cap_mib` raises the cap to 32/64/128/256 MiB.
Ceilings remain 4096 requests, 256 stages, 64 GiB authorization and 64 successful
grants; entries, context and other bounds remain independent. Pending state
blocks fresh grants. Renewal never refunds usage, checks mathematics or repairs
state. Exact successful grant replay does not grant twice.

For ordinary requests, identical ID **and identical bytes** replay a recorded
terminal response; changed bytes conflict. Historical replay is not current
status. On transport failure, `accepted:null`, pending state or unknown outcome,
retain the original request and returned evidence directory. Do not create a
new ID on the assumption nothing committed. The public wrapper creates evidence
automatically; normal success requires no hand-built plan or receipt.

For a supported interrupted ordinary operation, an operator may save:

```json
{"op":"recover_ordinary","client":"owner","args":{"client":"local","request_id":"ORIGINAL_ID","supervisor_receipt":"E:/MathCommons/alpha-scratch/calls/ORIGINAL_CALL/supervisor.json"}}
```

Invoke `manage.py recover --config ABS_CONFIG --request ABS_RECOVERY`. Select
the **original** call receipt, not a later retry. Recovery authenticates original
whole-tree quiescence before terminalizing a pending request; it preserves all
charges/files and promotes no partial Lean output. Supported peer operations
use `recover_peer` instead. Bootstrap is outside both pending-recovery modes.
A deliberate new request is appropriate only after the prior outcome is known.
One real ordinary-abort sequence passed independent audit on its preserved cut;
this is not arbitrary crash repair or automatic qualification of later changes.

Each service grant is at most 360 seconds, 128 requests and 256 MiB; restarting
requires an explicit new unique session. There is no installed daemon, automatic
restart, or public `stop` command. Prefer allowing the bounded session to end;
forced termination is a failure, not evidence of safe completion.

There is no qualified backup/restore, in-place upgrade, used-state relocation,
garbage collection or general hot-journal recovery command. Stop on damaged
state, missing original evidence, unsupported journals or exhausted hard limits;
preserve installation, state, scratch and runtime. Never delete journals,
partial stages, receipts or counters to force progress. Offline preservation is
not a tested restore procedure. Release packaging, broader source conformance,
fresh-operator execution and independent-host operation remain open requirements.

## Source basis

Read against `build.py`, `manage.py`, `py/node.py`, `py/peer_node.py`,
`py/service_worker.py`, `py/peer_service.py`, `py/domains.py`, `py/storage.py`,
`py/capacity.py`, `py/admin_worker.py`, `py/recovery_manage.py`, `API.md` and
`CORE.md`. No product import, execution, network operation or SQL query was
performed to author this document. API/CORE historical qualification labels
must be read alongside the newer allocation-specific outcomes.
