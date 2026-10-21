# Managed custody storage: reuse the existing envelope, do not run a new experiment

2026-10-21, core_release. Source/theory only. No product/config edits, imports,
runtime, storage test, deletion, migration, secret access or Git mutation.

## Decision

The central question is already answered in principle by
[PLACEMENT-LIFECYCLE-SPACE-BOUND](PLACEMENT-LIFECYCLE-SPACE-BOUND.md), with the
two-slot lifetime composition in
[PLACEMENT-LIFECYCLE-SEAM](PLACEMENT-LIFECYCLE-SEAM.md). Reuse these arguments.
An OS quota, more RAM and a disk-filling experiment are not prerequisites for a
conditional finite **managed data-stream** bound for trusted local code and
an adopted SQLite/VFS profile. They would not remove the need to justify the
actual source/profile correspondence.

The current implementation has **not adopted that bound**. Its explicit
`physical_envelope_adopted: false` remains correct. A finite slot reservation,
page caps and a successful final census must not be relabeled as a prospective
peak-space guarantee. This is a narrow deployment obligation, not a new
reclamation design or reason to delay the contribution integration.

## Current selected source, not the older proposal

Resolve the current126 SDK through
`experiments/v5-local-checks/distribution-managed-owner-01-input.json`, SHA-256
`4a9bfd78afd328d629ee6ad967f7f9378034db86cdee86bef751c5c50e6778a1`.
The source changes relevant to applying the older argument are:

| Boundary | Actual selection and consequence |
|---|---|
| Six persistent stores | Workspace `8531ee14`, modules `39e8eee8`, packets `c039af08`, discovery `1c8543d4`, placement `d955990c`, routes `5aa23ee7`. All request DELETE/FULL, MEMORY temporary storage and a finite page cap. They do not uniformly bind/read back the entire proposed profile before writes. |
| Generation registry | Supervised lifecycle `bec62143` checks4096-byte pages, DELETE, FULL, MEMORY readback and the page cap. This is stronger than the older proposal but not exact runtime/VFS adoption. |
| Node metadata | Installed `base/overlay/quota_store.mjs` checks4096-byte pages and cap; selects DELETE/FULL/EXCLUSIVE. Its default is16384pages (64MiB main file),16384entries and16MiB logical bytes. It does not select MEMORY temporary storage. |
| Node extension | Actual `portable/location/intent.mjs` is body_location `220bff26`, not the older portable_runtime namesake. It calls `super.open()` before its additional scan. Fresh-start allowance is still necessary if a future guard is inserted only afterward. |
| Per-run outputs | Actual body_location controller `eeb82d5d` checks each config/source-map serialization is at most16384bytes before writing. Stderr is retained in memory, not an automatic generation-tree log. |
| Identity outputs | Actual maintained_roles `128a5bd4` writes an adopted local Ed25519 serialization and a fixed-field JSON record. Its1024-byte reopen read caps are not, by themselves, pre-write caps. Bind the selected serializer or check lengths before writing. |
| Generation marker | Lifecycle `_write_new` checks at most131072bytes before writing. Its bounded slot/run records are stored inside the capped registry. |
| Fixed deletion grammar | Reclaimer `19713fc4` has20+9R possible files/directories for R durably charged runs. Extra files, WAL/SHM, nonempty mathematical-operation directories and links cause HOLD, not automatic deletion. |

The six databases are `workspace.sqlite`, `modules/modules.sqlite`,
`packets/evidence-packets.sqlite`, `index/discovery.sqlite`, `placement.sqlite`
and `placement-routes.sqlite`, plus their exact optional `-journal` files.
Every run contributes one Node database/journal and four bounded non-SQLite
files. The generation also has its marker and workspace lock. No payload hash
sweep or new index is needed to calculate an envelope from this grammar.

## Three distinct claims

1. **Logical capacity:** existing object/request/run/page counters constrain
   accepted work. A page count is meaningful only with the actual page size.
2. **Quiescent apparent size:** `reclaim.py` adds regular-file apparent lengths
   after closure and requires `max_apparent_bytes <= slot.reserved_bytes`.
   This refuses oversized reclamation plans; it does not prevent an earlier
   larger write, capture every transient file, or enforce an OS quota.
3. **Prospective managed data-stream peak:** under the supported runtime/file
   profile, the existing argument bounds the simultaneous main databases,
   rollback journals and explicitly bounded other files. Filesystem metadata,
   snapshots/COW, other local writers and reserved free space remain separate.

A completed small run demonstrates neither the worst-case maximum nor that
configured maxima can all be reached. Consequently no saturation experiment
would establish the required universal upper bound.

## Concrete mismatch to avoid

The preserved custody-only service fixture
`experiments/v5-local-checks/bounded-reclamation-service-01/bounded-reclamation-service-result.json`
(SHA-256 `21ee791482d385521467673ad67630f7f6626ceb840c7adaf6ea61b7ce263a5b`)
selects the following page caps:

| Store | Pages | Main-file allowance at4096bytes/page |
|---|---:|---:|
| Workspace ledger |1024|4MiB|
| Modules |16384|64MiB|
| Packets |32768|128MiB|
| Discovery |16384|64MiB|
| Placement |256|1MiB|
| Route journal |256|1MiB|
| Six-store total |67072|262MiB|

Its empty metadata configuration selects another64MiB Node main-file allowance
**per run**, before journals. Therefore a64MiB slot reservation cannot be
justified by summing these configured maxima. This does not show the fixture
actually consumed262MiB, or that its other restrictive quotas permit doing so;
it shows this proposed sufficient bound would reject that configuration.
A tighter bound using every reachable SQL/workload state is possible in
principle but has lower marginal payoff than using deliberately small store
caps and a correctly sized conservative reservation for future managed hosts.
Do not alter the used fixture or reinterpret its successful scoped outcome.

## Reused sufficient invariant and minimal adoption consequence

From SPACE-BOUND, let P=4096, N be the database page cap, S an adopted bound on
the SQLite journal-header sector size, and A the allocation rounding quantum:

```text
J(N,P,S) = N(P+8) + 2S(N+2) + S
D(N,P,S,A) = round_A(NP) + round_A(J(N,P,S))

B_generation = sum(six persistent D values)
             + R * [D(N_node,P,S,A) + E_run]
             + E_generation
```

The prior derivation is conditional on its pinned pager behavior, no page
relocation/ATTACH/VACUUM or unlimited error-retry loop, effective in-memory
temporary storage, supported schema and bounded ordinary-file writers. This
note does not independently strengthen that argument into a theorem about the
installed binaries. In particular S=4096 must not be inferred from P=4096.

The smallest future source consequence is to validate this inequality **before
allocating a generation**, not to add another storage backend or global quota
service. Adopt one supported SQLite/runtime/VFS profile, establish it before
unbounded writes, bind finite output sizes, and reject configurations for which
the calculated bound exceeds the charged slot. Include the analogous registry
and cleanup reserves in the owner inequality. Preserve every permitted run's
envelope until whole-generation reclamation, even after a failed start.

The selected fixed grammar is useful: forbid unmanaged persistent logs inside
the generation rather than attempting to budget arbitrary wrappers. Any public
owner's reports/credential files outside that grammar must have their own
explicit finite output allowance; they cannot be made free by calling them
external. The fixed shared installation is charged once, not once per run.

Minimum adoption work, if root selects it:

- One exact runtime/profile argument covering both Python and Node SQLite;
  version strings/readbacks alone do not establish a modified build's behavior.
- One small reusable pre-write/profile guard and deterministic envelope
  calculator, wired into the selected stores/owner without changing mathematics,
  discovery, receipts, lifecycle phases or wire formats. The existing post-open
  Node seam needs its finite fresh-empty-startup allowance or a base-store guard.
- Future configuration caps/reservations that satisfy the calculated inequality,
  plus explicit writer caps for the few non-SQLite files lacking pre-write caps.
- At most tiny changed-boundary refusal checks for profile mismatch/insufficient
  reservation, if needed. No full disk, RAM survey, prover or broad rerun.

The current false adoption flag stays false until these premises are established.
Even afterward, disk exhaustion caused by other applications remains a safe
refusal/recovery case, not a broken promise of exclusively reserved free space.
The actionable result is a bounded, inexpensive source-adoption task; return
engineering priority to working contribution, certified reuse and useful growth.
