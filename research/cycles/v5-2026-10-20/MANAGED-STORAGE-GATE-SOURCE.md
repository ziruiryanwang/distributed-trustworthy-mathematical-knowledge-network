# Managed storage gate helper: source-only implementation

2026-10-21, core_release. **Authored, not wired or adopted.** This implements
the selected small helper under MANAGED-STORAGE-GATE-SOURCE-SELECTION, reusing
contract246bafdf, decision81073cdf and runtime profilee36470bb. No new pager
theory, RAM survey, runtime probe, database open or experiment was performed.

New source: `software/v5/managed_storage/placement/storage_profile.py`,
9331 bytes, SHA-256
`3b535a337c1731ead3b9930c7cbe1f7c340a17152bd8b57e32981552ec061c90`.
No existing source, installation, schema, caller, acceptance rule or adoption
flag changed. Independent source review is still required.

## Five small APIs

- `database_envelope(pages)`: exact main+journal components under fixed
  P4096/S65536/A1. It implements the existing conditional formula directly;
  no caller can lower sector/rounding constants or claim occupancy credit.
- `node_metadata(value)`: exactly the five explicit, nonnull bounded integer
  fields from the contract. Missing/null values, bools, floats, strings, extra
  keys and unsupported ranges refuse; no JavaScript defaults are inferred.
- `registry_envelope(manager)`: validates the registry cap, all three manager
  reservations, both slots and each slot's run cap. Requires registry bound
  <= registry reservation and registry+cleanup+both slot charges <= owner
  reservation, even when slots are empty.
- `generation_envelope(manager,slot,generation)`: rechecks the owner gate,
  all six persistent caps, explicit Node metadata and1<=R<=slot.max_runs<=4096.
  Charges R complete Node main+journal/four-file envelopes and the generation
  marker/lock; requires total <= slot reservation. It never uses runs consumed,
  active occupancy, cache contents or a prior saved report.
- `configure_connection(connection,max_pages=...)`: receives one exact Python
  sqlite3.Connection, never creates/opens a database. Requires autocommit-style
  isolation_level=None, no active transaction, standard row/text factories,
  one named main file and the adopted build's TEMP_STORE=1 readback. Before
  profile changes it refuses a non-DELETE journal, over-cap page count, or a
  nonempty database with incompatible page size/auto-vacuum. It then configures
  page4096, auto_vacuumNONE, DELETE/FULL, MEMORY temporary storage, normal
  spilling and the finite cap, and checks exact readbacks before any caller DDL.

The Python helper intentionally supports the known TEMP_STORE=1 build profile,
not arbitrary SQLite compile configurations. Readbacks do not certify binary
correspondence, default VFS or file lineage. There is no caller-supplied adoption
boolean, no VACUUM, no MEMORY main journal and no global patch. On any guard
failure the caller must refuse/close rather than continue schema writes; the
helper does not own or close the connection.

Registry/generation envelope outputs contain newly constructed scalar/dictionary
observations, calculation_only=true and physical_envelope_adopted=false. The
database and metadata primitives return inert component/value dictionaries,
not adoption assertions. The connection
observation also explicitly leaves runtime/profile adoption false. Input configs
are not modified. Exact F.uint validation rejects bool-as-int and coercion.
The functions validate storage-bearing fields, **not** the complete manager/
workspace/placement/location/service schemas or their cross-role bindings.
Those remain required pre-allocation caller checks.

## Arithmetic correspondence

With A1, each database's total is exactly

`D(N)=4096*N + N*(4096+8) + 2*65536*(N+2) + 65536`.

Registry/generation marker+lock allowance is131072+1 bytes. Every run's four
other files cost2*1024+2*16384 bytes. There is no per-run loop or occupancy scan:
six component calculations and one exact multiplication by R suffice. Returned
counts are14+6R files,6+3R directories,20+9R entries, matching the settled grammar.
No cleanup history or delta database is invented. Cleanup headroom remains
charged but cannot guarantee free registry pages or reclamation progress.
External public outputs and the shared installation are explicitly excluded;
directory/filesystem metadata, COW, unrelated writers and free disk remain
outside this apparent-stream bound.

## Exact next insertion seams, not current wiring

Resolve these through the selected127 input33bd99d7 (the combined observed
successor only changes owner/service, not these store openers).

| Gate | Selected insertion point |
|---|---|
| Fresh manager allocation | supervised_generations/placement/lifecycle.py, ManagedGenerations.open: after full fresh profile/config validation but before line170 mkdir, lock open or registry creation. Call registry_envelope. |
| Manager reopen | Same open: authenticate manager.json/root/config/fresh-profile lineage and fixed file metadata before line180 writable sqlite3.connect; current line209 marker check is too late. Do not adopt old profiles or delete hot journals. |
| Generation charge | lifecycle.py allocate: after complete schema/cross-role/storage validation, before line363 reserve closure and line382 transaction that advances sequence/PROVISIONING. Call generation_envelope on immutable copied config. |
| Registry connection | lifecycle.py immediately after line180 connect, before line195 schema script; replace duplicated profile setup with the guard, retaining local cache/other policy. |
| Actual custody workspace | terminal_i/client/workspace_evidence.py immediately after line106 connect, before line112 schema script. This is the selected8531ee14 opener, not older client/workspace.py. |
| Module store | custody/module_store.py after line47 connect, before line58 schema script. |
| Packet store | terminal_i/evidence_network/custody.py after line91 connect, before line99 schema script; delta/custody4304e529 supplies limits, not another database. |
| Discovery store | selective_placement/discovery/discovery_store.py after line69 connect, before line83 schema script and its later writes. |
| Placement ledger | selective_placement/placement/ledger.py after line36 connect, before line45 schema script. |
| Route journal | retained_advertisement/placement/advertisement.py after line65 connect, before line72 schema script. |

These are future fresh successors, never edits to the listed frozen bytes.
All seven Python connection guards need already-established ordinary path and
supported hot-journal lineage premises; even a PRAGMA read can trigger recovery,
so this helper cannot retroactively contain unknown old journals.

Node needs an equivalent reviewed pre-schema guard in a fresh managed-only base
open override or exact base successor. body_location/portable/location/intent.mjs
open currently calls super.open first, which already writes in
base/overlay/quota_store.mjs; post-super configuration is insufficient. A Python
helper cannot configure Node's eventual connection. Preserve the original base
schema/census/counter semantics and fixed provider prefix.

The coherent caller integration must additionally bind a fresh profile in
manager/generation identity, reject oversized lock/main/journal files before
writable reopen, enforce both Node identity buffers <=1024 before either write,
retain original marker/config/source-map caps and custody-only empty operations
layout, and reject unsupported extra files. No actual eligibility/adoption flag
may turn true merely because this pure calculation returns.

## Next decision

After the priority public contribution outcome, root can select that coherent
caller/schema/Node integration and independent review. At most tiny new
arithmetic/order/refusal controls are warranted for changed boundaries. Do not
rerun broad lifecycle, mathematical, search, memory or saturation campaigns.
The current module alone does not yet gate a single actual allocation.

