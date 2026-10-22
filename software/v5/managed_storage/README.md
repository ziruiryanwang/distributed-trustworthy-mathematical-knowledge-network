# Managed storage admission

This successor adds a prospective storage-admission check to the existing
managed owner. Before creating a manager or allocating a generation, it checks
that the declared reservation covers all permitted database pages, possible
rollback journals and bounded auxiliary files. The reservation is not an eager
allocation and is not a RAM requirement.

Use the [managed operator guide](../managed_operator/README.md) for ordinary
launches and lifecycle operations, then the [V2 contribution changes](../managed_contribution/README.md).
This page specifies only the additional storage changes. The old guides'126/127
SDK counts and supervised-manager schema describe their preserved predecessors;
this successor uses129 SDK entries, a130-entry owner snapshot and the storage
manager schema below. The public launcher, mathematical acceptance rules and
contribution protocol do not change.

Status at authoring,2026-10-22: small Python and Node controls have adopted
outcome audits; the fresh distribution build is in progress. The installed
four-command integration has not run. See [current evidence](../../../research/NOW.md)
for later adoption. This source directory is not an independently deployable
release or an instruction to modify a preserved installation.

## Required configuration changes

The public managed request stays `DMKN_V5_MANAGED_OWNER_V2`. Its complete
`manager_config` retains the existing epoch, clock model, registry/reservation
fields, protected roots, two slot specifications and `max_sessions`, and now
uses:

```json
{
  "schema": "DMKN_V5_TWO_GENERATION_MANAGER_STORAGE_V1",
  "storage_profile": "DMKN_V5_MANAGED_APPARENT_STREAMS_P4096_S65536_A1_V1",
  "writer_profile_sha256": "<derived lowercase SHA-256>"
}
```

This is a fragment, not a complete request. Do not add or omit fields from the
complete validated configuration. Each generation's
`location.limits.metadata` must contain exactly five explicit, nonnull integers:

| Field | Allowed range |
|---|---:|
| `entries` |32–65536|
| `bytes` |65536–134217728|
| `valueBytes` |1024–65536|
| `providersPerKey` |1–128|
| `pages` |256–65536|

An empty object no longer silently adopts Node defaults at managed allocation.
Existing six-store page caps and per-slot/per-generation `max_runs` still apply.
Logical byte/object quotas and SQLite page caps are joint restrictions: fitting
this envelope does not promise every logical quota can be filled.

## Deriving the writer identity

First adopt the exact release and supported base runtime. Authenticate the
release manifest and the actual selected source bytes; hashing an arbitrary
untrusted manifest does not make it authoritative. From that manifest construct
the complete logical SDK map:

```text
sdk_sources[logical_name] = {bytes, sha256}
```

For this successor it contains all129 entries, including the owner and inherited
writers—not only the14 changed files. Exclude installation paths and any extra
`owner/managed_owner.py` snapshot alias. Then construct exactly:

```text
value = {
  storage_profile: "DMKN_V5_MANAGED_APPARENT_STREAMS_P4096_S65536_A1_V1",
  base_manifest_sha256: <adopted base RELEASE-MANIFEST.json identity>,
  sdk_sources: <complete logical-name map above>
}
writer_profile_sha256 = SHA256(
  ASCII("DMKN-V5-MANAGED-STORAGE-WRITER-V1") || 0x00 || compact(value)
)
```

`compact` is the selected `formal_features.compact`: UTF-8 JSON, sorted object
keys, no extra whitespace, `ensure_ascii=False`, no nonfinite numbers. Use the
adopted implementation's encoding; do not hash a pretty-printed JSON document.

The installed owner independently authenticates the complete selected source
snapshot and reconstructs this digest. A copied configuration's asserted digest
is not sufficient. The owner supplies its verified digest through manager,
worker, composer and the supervisor's direct registry reopens. File-system
location and changing operation paths do not enter the digest, so relocation
does not by itself change writer identity. This is code identity, not a proof
that arbitrary code is correct.

## The conservative reservation rule

For the adopted profile, database page size is4096B and the journal-sector bound
is65536B. For a database capped at `N` pages, the sufficient apparent-byte bound
for its main file plus possible rollback journal is:

```text
D(N) = 139272*N + 327680

B_registry = D(registry_pages) + 131073

B_generation = sum(D(N_i) for six persistent stores)
             + R * (D(Node_pages) + 34816)
             + 131073
```

The six persistent stores are workspace ledger, module custody, packet custody,
discovery index, placement ledger and route journal. `R` is the generation's
configured maximum run count, not currently running or remaining runs. Each
run gets its own Node metadata database plus two identity/adoption files and
two channel files. The131073B term covers the bounded marker and one-byte lock.

Required inequalities are:

```text
B_registry <= registry_reserved_bytes
B_generation <= selected_slot.reserved_bytes
registry_reserved_bytes + cleanup_reserved_bytes
  + slot0.reserved_bytes + slot1.reserved_bytes <= owner_reserved_bytes
```

Both slots and every allowed run remain accounted for. An empty database,
failed start or closed run is not grounds for an occupancy discount. Existing
retirement and explicitly authorized whole-generation reclamation govern later
slot reuse; this check does not refund charges or guarantee cleanup progress.

The registry calculation precedes manager mkdir, lock and writable SQLite open.
The generation calculation precedes sequence/PROVISIONING reservation. If the
request came through a newly launched worker, its supervisor session may already
be charged when generation allocation refuses. That legitimate earlier charge
is not a generation allocation and is not refunded.

## Concrete integration-test profile—not production guidance

The selected empty-service integration uses registry64 pages, all six
persistent stores256 pages, Node256 pages and one allowed run per slot:

```text
D(64) = 9241088 B
B_registry = 9372161 B
D(256) = 35981312 B
B_generation = 7*35981312 + 34816 + 131073 = 252035073 B

slot0.reserved_bytes = slot1.reserved_bytes = 252035073
registry_reserved_bytes = 9372161
cleanup_reserved_bytes = 2097152
owner_reserved_bytes = 515539459
```

The four non-page Node metadata values explicitly preserve the prior defaults:
entries16384, bytes16777216, valueBytes32768 and providersPerKey32. Only the
page cap is reduced. The six actual main files each have a1MiB cap; the larger
reservation includes conservative possible journals, not expected occupancy.

The test also separately selects registry reservation9372160B (one byte short)
and a generation with workspace ledger257 pages (139272B beyond the exact-fit
slot). Expected refusals are respectively
`MANAGED_STORAGE_REGISTRY_RESERVATION` and
`MANAGED_STORAGE_GENERATION_RESERVATION`. These cases test admission boundaries;
they do not recommend256-page stores for real mathematical custody, establish
throughput, or validate a capacity-planning policy. Choose production quotas
from actual intended retained data and service load, then apply the same rule.

## Reopening and updates

The ordinary installed command remains the one in the linked operator guide.
Fresh creation is explicit; failed reopen never falls back to creation.
Reopening requires the identical enrolled manager configuration, its marker,
compatible bounded local layout and verified writer identity. Python connections
enforce the selected SQLite profile before schema operations. Every managed run
creates fresh Node metadata; existing Node metadata is not silently reopened.

Old supervised-manager schemas are not migrated. Any SDK byte change changes
the writer digest and refuses the old manager through this owner, even if the
change appears unrelated to storage. Preserve the old installation and state;
do not edit its marker/configuration to force acceptance. A reviewed explicit
migration or continued use of the old adopted writer is a separate decision,
not a feature supplied by this successor. The storage digest intentionally
binds the complete SDK/base identity, but not the changing release document or
operation identity; it does not provide automatic update compatibility.

## What this bound does not mean

The assurance is conditional on the adopted exact runtime/source/default-VFS
behavior, selected SQL/serializers and private ordinary paths with no other
writers, restores or hostile concurrent mutation. The argument and these
premises are recorded in the [runtime profile](../../../research/cycles/v5-2026-10-20/MANAGED-STORAGE-RUNTIME-PROFILE.md)
and [source integration review](../../../research/cycles/v5-2026-10-20/MANAGED-STORAGE-OWNER-PATHS-REVIEW.md).

It bounds apparent managed default-data-stream lengths. It does not reserve
free disk or bound physical allocation, filesystem metadata, snapshots/COW,
alternate streams, other applications, the shared installation, external
operation reports or private credential files. Those outputs retain separate
finite policies. `physical_envelope_adopted` remains false. Disk exhaustion can
still cause an operation to fail and retain charges.

It is also not a RAM bound: SQLite caches, in-memory temporary operations and
the other actors use the separately selected process-resource envelope. Neither
a large conservative storage reservation nor a small successful test measures
their actual RAM demand. No new proof of mathematical soundness, availability,
useful growth or worldwide deployment follows from storage admission alone.
