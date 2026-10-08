# Exact-byte replica custody: implementation patch proposal

2026-09-21. **Source-only proposal; not applied, imported, executed, or qualified.**
The accompanying `REPLICA-IMPLEMENTATION.patch` is for subsequent independent
review after ordinary-abort recovery qualification. Only this note and that
patch were authored. Product, tests, installations, and qualification evidence
were not edited. An inert `git apply --check` passed against the cut below; that
establishes patch applicability, not Python correctness or behavioral success.

## Scope and pinned base

The complete `REPLICA-CUSTODY.md` was read first (SHA-256
`6E17FC07C8340108154FC51F2981DDFAF41513A811F4D3191F19FEDF7EE4093C`).
The actual acquisition, normalization, package validation, view construction,
service, read-only ledger, allocation, supervision, and recovery paths were
source-inspected. Paths below are relative to `software`.

| Patch target | Base SHA-256 |
| --- | --- |
| `py/peer_node.py` | `99B7F3AF3C4C4E0B66827157E743A75EAC320A54D04E90C1E4A9912991A90B18` |
| `py/service_worker.py` | `C94098CD5EE08ED8A4977843B138B3C0CFB905EE8A6F9D67CA9E39991ED21E86` |
| `py/peer_wire.py` | `B4AAD584E9F6F6D83872501D277C1F1CDE79E5A89618EFBF1260497BEB8D4946` |
| `py/node.py` | `DC0B2E20C27290270B595122C33385D51FF629B67EF52B94B97DD8A3990F6977` |
| `manage.py` | `DF319F00DBCF29702A04D6151564896AE4D040998AC5859CACE7CBE53580BB77` |
| `py/recovery_worker.py` | `EB574CEC2090CE3B337E289FCDF76C230B5C5BDB9E94E2DDB9CA39ABDB99C073` |

No changes to storage schema, wire schema/framing, receiver checking,
`peer_service.py`, or the mathematical codec are proposed. The `peer_wire.py`
change only clarifies the caller's authority in `build_view`'s docstring.
`recovery_worker.py` is based on the integrated ordinary-abort development cut,
not the older preserved peer-only installation.

## Small implementation boundary

`peer_acquire` carries the exact `received["package"]` pin into the committed
acquisition as `received_package`. Its existing `package` still means the
normalized/reused local candidate. Acquisition stays private: it creates no
view, publication, service, context admission, or acceptance.

The explicit ordinary-client request is:

```json
{"client":"local","request_id":"share-import-001","op":"replica_expose","args":{"acquisition":"acquisition:ACTUAL_RETURNED_HANDLE"}}
```

It accepts one acquisition, never a supplied package path, list, or candidate.
Old acquisitions lacking custody return `REPLICA_CUSTODY_UNAVAILABLE`; no
directory guessing or backfill occurs. Historical request replies remain
byte-exact historical replies without checking current file availability.

The shared `peer_node.replica_custody` helper is intentionally ledger-only:

- It authenticates same-client acquisition and remote records, configured
  endpoint data, original catalog/bundle/descriptor fields, historical P1
  snapshot membership, and the selected offer's metadata and normalized pin.
- It validates the original 64-hex request key and uses one indexed request-key
  lookup. The row must be a same-client terminal `peer_acquire` for that exact
  remote. Its exact response shape must name this acquisition and an
  authenticated matching candidate. Type-sensitive comparisons distinguish
  booleans from integers. Record/snapshot/entry reads are existing indexed
  readers; there is no history scan or registry.
- It checks the received path as the exact lexical
  `state/work/<original-request-key>/incoming` and its manifest pin against the
  advertised entry. It performs **no package filesystem reads or network IO**.
  Thus service startup can authenticate authority after source, incoming, or
  normalized copies disappear.

New-view preparation additionally rejects reparse/symlink traversal for the
incoming directory and every selected file, checks the raw manifest pin and
foundation, and calls the existing structural `revalidate` path on the original
received package. `Checker.package` / `source_codec.read_package` check full
typed IDs, payloads, inventories, exact closure, and supported replay structure;
metadata and symbols are rederived and compared. This path does not call
`Checker.offer`, `import_package`, export, or native acceptance.

The existing builder preserves the original manifest bytes and manifest object
order. The resulting single entry must equal the original advertised entry
field-for-field, including manifest digest, root, descriptor, metadata, bundle
digest, and length. A normalized representation is never substituted for the
original. `load_view` authenticates the newly flushed catalog, completion marker,
and bundle. The visibility transaction repeats the immutable ledger bindings
and writes only a view record plus normal terminal bookkeeping. Partial or
refused preparation remains charged staging; it cannot authorize serving.

## Exact selected-row service authorization

The service now validates every row against the corresponding catalog entry in
one read-only ledger snapshot, closing that snapshot before the finite session.
It recognizes only these two disjoint exact shapes:

| Basis | Exact row fields | Required authority |
| --- | --- | --- |
| Existing publication | `provider`, `sequence`, `descriptor_id`, `publication` | Exact existing `require_published` handle plus local entry descriptor/metadata/manifest pin |
| Replica custody | `provider`, `sequence`, `descriptor_id`, `basis`, `acquisition` | Exactly one row, `basis:"replica-custody"`, authenticated acquisition, and exact original advertised entry/foundation |

Both require P1, a positive integer sequence, no duplicate sequence, and the
catalog's exact typed descriptor. Extra fields, mixed shapes, wrong basis,
cross-client acquisitions, wrong catalog entries, or a multi-entry replica view
refuse. `publish` and publication-only `expose` eligibility are unchanged; there
is no fallback from a failed publication check to custody. Service validation
of publication rows is strengthened, not relaxed.

Serving imports the existing `peer_node` module solely for that inert helper,
after checking its configured source pin and installed module path. Its top-level
imports are standard library, storage, wire, and transport: no checker, codec,
Lean process, or stage allocator is loaded/invoked by the serving path. The
finite service still authenticates view bundles at startup and hashes the bytes
actually returned on each bundle request. Source packages and evidence remain
outside its HTTP namespace. An intact frozen view does not depend on its old
incoming/normalized/source copies; losing incoming prevents only new views.

## Operation, quota, pin, and recovery consequences

Adding `replica_expose` to `node.PEER_OPS` also includes it in request parsing,
peer preparation/commit dispatch, the hard native-allocation prohibition, and
the existing peer retained-file census ceiling. It is charged exactly the
existing 80-MiB `expose_request_bytes` grant, consuming a real request slot and
retained staging charge. No new grant, refund, stage, or quota-reset rule exists.
The owner wrapper selects the existing 120-second wall/CPU, 1024-MiB peer request
profile. Structural checking remains subject to existing cache/time limits.

Service supervision adds `peer_node.py` to its source pins: 11 source files plus
interpreter and configuration = **13 pins**, below the 16-pin ceiling. Public
node requests retain their existing 12 pins; recovery's original-source pins
and wrapper input counts do not grow. Fresh installation/configuration pins must
cover all changed sources. Old installed cuts and source-bound receipts are not
migrated or silently requalified.

The only recovery delta adds `replica_expose` to `PEER_OPERATIONS`, not to
`ORDINARY_OPERATIONS`. It uses explicit `recover_peer`, preserving both zero-stage
guards, original-attempt binding, original whole-Job quiescence, existing owner
lock, selected-row checks, fixed interrupted-peer refusal, counter preservation,
and unknown-outcome handling. Completion markers alone cannot promote orphan
views. This allowlist addition requires separately frozen tests on a later cut;
the ordinary-abort qualification does not cover it automatically.

## Independent review and subsequent controls

Before integration, independently review the helper's request/response/record
bindings, original-versus-normalized representation distinction, service import
closure and exact row matching, and atomic view/terminal boundary. Then freeze
new test sources and a fresh installation; this draft changes no tests.

Required discriminators include: private acquisition and unchanged heads;
wrong-client/legacy/missing custody; altered remote, request, terminal response,
candidate and historical membership bindings; out-of-domain/reparse paths;
changed/missing incoming bytes; valid noncanonical manifest presentation served
byte-identically versus forbidden normalized substitution; unchanged refusal of
ordinary `expose` on unpublished candidates; service row-shape/catalog tampering;
intact-view service after incoming/normalized/source loss; changed view-bundle
refusal; byte-exact replay without reconstruction; finite quota failure and
pending interruption through original-attempt native-free recovery with no
stage, charge refund, or visibility change beyond the selected terminal row.

The later positive seam remains A offline before B constructs its replica view,
B never natively admits the package, and C independently acquires, freshly
admits, and makes substantive downstream native-checked use. Receiver
`peer_find`/`peer_acquire`/`admit`/`submit` acceptance boundaries are unchanged.
Custody and hash equality establish neither authorship nor theorem truth,
permanent availability, independent-host fault tolerance, or a usable-v1 result.
Trusted local source/evidence, stable selected files during preparation, the
existing hash/SQLite assumptions, and finite explicit operator supply remain
premises; this is not a hostile-owner sandbox or repair mechanism.
