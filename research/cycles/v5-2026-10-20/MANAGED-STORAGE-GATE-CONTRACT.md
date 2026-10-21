# Supported managed-storage gate: concrete contract

2026-10-21, support_guest. Source-only under
`MANAGED-STORAGE-IMPLEMENTATION-SELECTION.md`. No product edits/imports/runtime,
database opening, inventory sweep, secrets, deletion or Git. Root has deferred
implementation while addressing the actual contribution outcome. This contract
does not adopt existing127's physical-envelope flag.

## Exact scope and two necessary gates

Basis: current127 input33bd99d7/release2cb30fae. Relevant selected logical sources:
lifecycle bec62143; sessions b4cfab61; reclaim19713fc4; workspace8531ee14;
module store39e8eee8; packet store c039af08 (limits from4304e529); discovery
1c8543d4; placement ledger d955990c; route journal5aa23ee7; composer40436584;
location controller eeb82d5d; Node roles128a5bd4 and intent220bff26. Node's base is
this release's `base/overlay/quota_store.mjs`. Resolve through the127 map,
not historical namesakes. Reuse SPACE-BOUND; core_release owns exact runtime/
pager/VFS correspondence.

The smallest consequence has two pure pre-write gates:

- Fresh manager enrollment: supported profile and registry/owner arithmetic
  **before** manager mkdir, lock or SQLite creation.
- Generation allocation: complete generation arithmetic **before** the
  transaction that increments sequence and stores PROVISIONING.

Checking only after `PlacementService.open` or at reclamation is too late.

## Exact writer inventory and cap paths

Let m=immutable manager config, g=generation config, s=m.slots[slot],
R=g.placement.max_runs. Require 1<=R<=s.max_runs<=4096 and charge **all R**,
including failed and not-yet-started runs, never current/remaining/active runs.

Each database below includes its possible `-journal`. Paths are relative to
the generation root.

| Main file | Exact cap path | Strict integer range |
|---|---|---:|
| workspace/workspace.sqlite | g.workspace.ledger_pages |256..65536|
| workspace/modules/modules.sqlite | g.workspace.module_limits.db_pages |256..268435456|
| workspace/packets/evidence-packets.sqlite | g.workspace.packet_limits.db_pages |256..268435456|
| workspace/index/discovery.sqlite | g.workspace.index_limits.max_db_pages |256..268435456|
| workspace/placement.sqlite | g.placement.ledger_pages |256..65536|
| workspace/placement-routes.sqlite | g.service_limits.journal_pages |256..65536|
| run-%04d/location-state/metadata.sqlite, each1..R | g.location.limits.metadata.pages |256..65536|

No separate delta-packet database exists in this selected Workspace. Module
groups/bodies, packet blobs and index CAS objects stay in these databases.
Logical `storage_bytes`/object quotas are not substitute page caps.

Node resolves missing **or null** metadata fields with JS `??`:

| Field | Default | Range |
|---|---:|---:|
| entries |16384|32..65536|
| bytes |16777216|65536..134217728|
| valueBytes |32768|1024..65536|
| providersPerKey |32|1..128|
| pages |16384|256..65536|

Recommended new-profile compatibility choice: require exactly these five
explicit nonnull integers. Preserve old default-bearing configs only in frozen
old profiles; no migration. If defaults are retained instead, normalize the
exact missing/null rule before binding/sending, never `value or default`.
The intent class supplies fixed providerPrefix; caller metadata cannot select
another storage-profile prefix.

| Non-SQLite path | Supported maximum bytes | Required pre-write obligation |
|---|---:|---|
| generation.json |131072|Existing lifecycle _write_new checks before xb.|
| workspace/owner.lock |1|Fresh one-NUL writer; reject oversized existing lock before append-mode reopen.|
| each run/location-state/identity.key |1024|Serialize/check0<byteLength<=1024 before writeFile; current1024 is only a read cap.|
| each run/location-state/adopted.json |1024|Same explicit pre-write check.|
| each run/location-channel/config.json |16384|Existing controller checks serialized bytes before directory/files.|
| each run/location-channel/source-map.json |16384|Same existing check, separately rounded.|

Directories: generation root, workspace, its empty operations/modules/packets/
index, plus each run root/state/channel. Thus **14+6R files,6+3R directories,
20+9R entries**, matching reclaim.layout(R). WAL/SHM, super-journals, disk temp/
sort/statement files, VACUUM/backup outputs and mathematical operation artifacts
are not allowed by this profile.

Current Node stdout/stderr and channel counters are memory/pipe state. No
transcript, closure.json, supervisor log or stderr file is written inside a
generation. Do not add guessed files or silently introduce a new persistent log.

## Deterministic envelope

Use the separately adopted profile's fixed P,S,A and the existing formula:

```text
J(N) = N*(P+8) + 2*S*(N+2) + S
round_A(x) = ((x+A-1)//A)*A
D(N) = round_A(N*P) + round_A(J(N))
E_generation = round_A(131072) + round_A(1)
E_run = 2*round_A(1024) + 2*round_A(16384)
B_generation = sum(D(N_i), i=1..6) + R*(D(N_node)+E_run) + E_generation
B_generation <= s.reserved_bytes
```

Core_release's current profile direction is P4096, conservative S65536.
A=1 means **apparent data streams**, not physical allocation. A larger quantum
requires an explicit supported-filesystem premise; do not infer it from page
size or let a caller lower it. No startup exception is included: use the
pre-schema guards below. Directory/filesystem metadata, snapshots/COW, paging,
OS dumps and unrelated writers remain separate; no free-disk promise.

Use exact Python integers; no floats, coercion, occupancy credit, deduplication
credit or assumed journal disappearance. Compute from immutable configs and
selected constants on every allocation; do not trust a caller's saved result.
Return component totals/profile identity as inert observation; no new audit file.

### Registry, cleanup and both slots

Manager files: generations.sqlite, its possible journal, manager.json and
one-byte owner.lock. Its root and two slot directories are fixed. Registry cap
is m.registry_pages (64..4096). Marker pre-write cap is131072:

```text
B_registry = D(m.registry_pages) + round_A(131072) + round_A(1)
B_registry <= m.registry_reserved_bytes
m.registry_reserved_bytes + m.cleanup_reserved_bytes
  + m.slots[0].reserved_bytes + m.slots[1].reserved_bytes
  <= m.owner_reserved_bytes
```

Retain existing1..2^50 exact integer bounds on reservations. Charge both slots
even when empty. The shared immutable installation is a separately identified
fixed cost, not a per-run copy or silently included in managed-root reservation.

Reclaim facets/bitmaps/progress are embedded in the two capped slot-record blobs
(max131072 each), not extra files. Session state is a single replaced meta blob
(max16384), not an append-only per-session history. Registry D already covers
their main/journal peak: do not multiply it by max_sessions or invent cleanup
logs. Retain existing positive cleanup_reserved_bytes as charged headroom and
its per-facet encoded-length check.

**Important limitation:** this scalar does not reserve free SQLite pages.
Registry SQLITE_FULL can still leave cleanup HOLD, with all charges preserved.
The proposed gate bounds peak storage; it does not guarantee reclamation
progress. A stronger promise needs a separate schema-capacity/pre-reserved-row
argument, not a larger unexplained cleanup number.

## Pre-write and compatibility obligations

1. Preserve F.uint's `type(value) is int`: reject bool, float, string, null and
   out-of-range caps before reservation. Validate cap-bearing nested dictionaries
   and existing workspace/placement/location/service bindings before allocation,
   not first during later store construction. Node Number.isSafeInteger receives
   the same normalized bounded values.
2. Bind one supported profile into a fresh manager schema/config and hence the
   existing generation config hash. Caller-selected P/S/A or version strings
   cannot authorize adoption. Old127 sources/state and false flags stay frozen.
3. Every writable SQLite connection must establish/check page_size4096,
   auto_vacuum=NONE, DELETE, FULL, effective MEMORY temp and exact max_page_count
   **before BEGIN/CREATE/INSERT/schema initialization**. Reuse one reviewed guard
   rather than seven divergent validators. Keep normal spilling to the bounded
   durable main journal; do not use MEMORY main journals or disable spilling.
4. Both identified builds have DEFAULT_AUTOVACUUM; an in-memory probe conceals
   the file default. Node intent.open calls super.open first, and base open
   already creates/indexes/writes/commits. A post-super guard is insufficient.
   Select a pre-schema base successor or reviewed managed-only open override.
   No empirically guessed empty-startup allowance repairs this ordering.
5. Fresh supported enrollment only; no opportunistic old-DB adoption. On manager
   reopen authenticate manager.json/root/config/profile **before** writable
   SQLite open, not its current later location. Hot-journal recovery can write
   before later PRAGMAs. Retain composer's prior generation-marker/config check.
   Check only fixed-path metadata against main/journal bounds and reject unknown
   WAL/temp files, aliases and incompatible lineage before writable reopen.
   Same-profile hot journals are accounted, never deleted to recover allowance.
6. Serialize/check both identity buffers before either file write. Keep existing
   marker/controller caps and exclusive creation. Supported locks are one byte;
   refuse oversized old locks without truncation. Preserve custody-only hosting
   (no live math client/grants; operations directory empty). Do not broaden
   reclamation or remove proof artifacts to make the equation fit.

These are safety conditions for a future selected successor, not instructions
to edit current installations. Exact runtime/VFS source correspondence from
core_release is still required; a calculator or tiny guard test cannot by
itself set physical_envelope_adopted=true.

## External outputs are not secretly free

Public boot/request/source snapshots and parent/child supervisor evidence are
disjoint from the managed root. So are managed-result.json (pre-write1MiB),
managed-ready.json and the private credential (helper cap8192). Ready currently
has bounded constituents but no independent total-length pre-write guard; add
one if that external-output guarantee is claimed. Credentials intentionally
survive generation reclamation.

These have separate operation envelopes, not a proven lifetime manager-disk
bound. Administrative calls can create disjoint evidence without a generation
run; sampled post-output censuses are not pre-write quotas. Do not advertise
owner_reserved_bytes as covering all retained public outputs. Extending that
scope requires a separate evidence-retention/allocation policy, not a slot
constant in this task.

## Minimum future refusal/control groups

No tests are selected by this note. If needed after implementation:

1. Strict scalar/metadata shape: bool/float/null/missing/zero/out-of-range refuse;
   valid edges do not coerce.
2. Arithmetic: exact fit passes, one byte short fails; R+1 adds exactly one
   Node DB+journal+four-file allowance; both slots/registry/headroom are counted.
3. Earliest gate: insufficient registry/owner refuses before manager writes;
   insufficient slot before sequence/PROVISIONING/directory mutation.
4. Profile ordering: mismatch refuses before first schema statement; inert
   connection controls test order, not actual pager correctness.
5. File/lineage bounds: exact-size files pass, one-byte excess refuses before
   write; wrong marker/profile/oversized lock or DB journal preserves old bytes.
6. Failure monotonicity: failure after legitimate reservation preserves original
   slot/run/R/profile charges; no refund/retry/deletion/profile downgrade.
   Reuse existing lifecycle evidence; no service/reclaim or broad campaign rerun.

Stop at an enforceable supported managed-data-stream allocation contract.
Mathematical, routing, retention and old evidence semantics stay unchanged.
