# Restore a retained route under fresh owner service authority

2026-10-21, core_release. Source-only contract, not implementation or execution.
Basis: lifecycle seam `76856b8d`; frozen advertisement `b5523f82`, controller
`ef1c9b59`, ledger `d955990c`, guarded index `1c8543d4`, and fresh service02
`319ddf07`. Exact selected sources were read. No new manager or registry is
needed for this operation; generation retirement/reclamation remains separate.

## Minimal API and meaning

```python
await service.advertise_retained(request_id, until=original_run_deadline)
```

Trusted local owner only: no token argument, HTTP route, DHT-selected write
destination or remote grant. The exact live service object and its newly
issued in-memory controller grant authorize it. Narrow first version requires
the existing ledger state **SEALED_SERVING**. OPEN admission remains unchanged.

Return the existing **current-run route facet only**, with its actual run ID,
representative request ID and advisory status. It is not a new placement
receipt, custody renewal, mathematical warrant or remote discovery guarantee.
Old `service_not_after_ms` stays historical; requiring it to remain live would
make restart impossible. Original receipt bytes/horizons are never rewritten.

## Reopening is already possible, but not with arbitrary configuration

Open the exact retained Workspace/placement/route stores with all three create
flags false and a fresh exact locator with fresh state/evidence paths. Both
core `start_run` and route-journal `open` consume their original durable run
caps, even for SEALED_SERVING; neither checks the expired publisher window.
This requires **spare original max_runs**. An original max_runs=1 generation
cannot restart by changing its config: exact-byte configuration checks refuse.
Provision a new test generation for at least two runs from its creation; do
not edit a used generation or its consumed counters.

The route journal also binds service epoch/generation/namespace/profile,
max_cells/max_runs, **same read endpoint**, and journal page cap. Reopening at
a different read endpoint or larger page cap is not this operation. Partial
open may consume a core run before route-open failure; no rollback/refund or
unconditional equality of the two run counters is assumed.

Old route rows do not block restoration: their primary key is `(cell, run)`.
The newly funded run gets a new row/opportunity. Existing `_facet` selects the
latest historical row across runs; before current-run restoration that is not
evidence of live intent. Return a current-run facet only after finding or
creating the current-run row; never relabel an old run as current.

## Exact selected-record predicates

The operation loads **one bounded** manifest/receipt, not its proof ancestry.
Check row BLOB lengths before loading; manifest <=16384 bytes and outcome
<=65536 bytes. Require all of the following before charging a route attempt:

1. Exact current service/Workspace/ledger/adapter/index/module/packet/locator
   identities and immutable config, live fresh grant/CPU/call/deadline budget,
   live read listener and nonfailed current locator. Consume one original
   controller service call even if the later selected-row check refuses.
2. Ledger `meta.state == SEALED_SERVING`; the selected request exists and has
   `phase == RECEIPT_COMMITTED`, a non-null bounded outcome and matching
   request identity. Parse its canonical manifest with `P.manifest`; recompute
   `P.request_id(manifest, saved_grant_id, generation)` without a bearer token.
3. Receipt has the existing closed success schema, false assurance flags,
   exact service epoch/generation/namespace/profile, request ID and reservation.
   Its export/hash/size/packet/horizon/body sequence match the manifest. Body
   response sizes remain within original requested ceilings. Do not accept a
   partially custodied/indexed row as a committed representative.
4. Derive `(cell, feature)` with `P.cell` from the saved fingerprint. Require
   exact manifest cell, receipt INTENT_ONLY route/stripe0, and membership of
   that feature in the validated receipt record. Record ID, export object ID,
   hash/size and locator module/name agree with the receipt/manifest.
5. Exact current index object row exists by export ID, has that record ID and
   byte-equivalent validated record; `index._record(record_id)` agrees. The
   saved immutable snapshot exists and equals the receipt snapshot with its
   validated hash/domain; object `admitted_seq` is no later than its local cut.
   The selected feature/partition/object posting exists, where partition is
   the first object-ID byte. Its corresponding feature head exists. These are
   primary/unique-key reads, not an unbounded search of an unrelated corpus.
6. Selected local group/name mapping still exists and matches the record's
   group index, within original opening size; the packet digest row still has
   the exact module and size/length and its module/profile offer exists. Every
   originally requested body row exists under its exact module/hash with a
   compatible size. Do not pull, rebuild or insert anything when a row is
   missing: refuse this representative.

Metadata existence is deliberately **not fresh byte-integrity or availability
certification**. No packet proof/blob or theorem ancestry is rechecked here.
The original checked immutable-store invariants justify reuse in the ordinary
local-storage model; later exact acquisition still hashes/checks selected data.
Disk corruption can turn a hint into a miss, never into mathematical acceptance.
A stronger fresh custody acknowledgement would be a separate funded operation.

For complete body matching, use the existing stored declaration descriptor's
universe index/name mapping, not an arbitrary same-hash body from another
module. If obtaining that descriptor requires the selected bounded opening,
read that opening only; do not invoke the old `_local_group` helper outside
its `_current` structural-budget context or scan every module.

## New owner guard, not a weakened publisher guard

Use a separate retained-operation guard at entry, before route COMMIT, before
publish, after its await and before final journal COMMIT. It repeats exact
owner/role/liveness, SEALED_SERVING, selected-row/domain and horizon checks.
Require finite `now_monotonic < until <= current_service_deadline`. Require
current wall time below the original representative retention_end_ms, which
remains <= original generation retention_not_after_ms. Also require the fresh
run's nominal active end within that representative horizon: sample monotonic
`m` before wall time `w`, and require
`w + ceil(1000 * (current_service_deadline - m)) <= retention_end_ms`.
If not, choose a shorter fresh run before opening, not an in-place deadline
change. Repeat this check in the guard; restart is not additional retention.
These use the existing wall-clock model; no strict UTC or rollback-resistant
clock guarantee is invented by this API. The post-active shutdown/TTL lag
described below remains a possible stale-hint interval, not a renewed promise.

Do **not** call `_publish(value, old_policy, ...)`: its original publisher
write/admission check is correct for new submissions and must remain unchanged.
Do not authenticate/renew the old token, call submit/reconcile, reset recovery,
re-admit the export, update the receipt or reset original placement charges.
Refactor only the common finite dispatch body so ordinary submit retains its
original guard and restoration supplies its separately explicit owner guard.

## Charge before publish; one opportunity per current cell/run

Hold the existing advertisement busy slot. Under the new guard, look up
`routes WHERE cell=? AND run=current_run`. If present, return that actual
current-run observation without another dispatch, even when its representative
request ID differs or its phase is uncertain. No row mutation or reallocation.

Otherwise use the existing immediate guarded transaction to check current-run
row count < max_cells and insert DISPATCH_ATTEMPTED with current run ID,
selected request ID, feature and time. **Commit before** the existing locator
publish command. Its allowance is the already funded one publish per cell/run;
the H+2L+1 command reservation, Node limits and journal page cap are unchanged.
Validate the existing closed response bindings and record its bounded final
observation under the same guard. Store no new receipt or blob.

Crash before reservation: no route attempt is authorized. Crash/exception after
reservation, including before actual send: preserve uncertainty and the charge.
Successful send followed by expiry/failed observation COMMIT is also uncertain.
Never retry within that run. A later separately funded run may intentionally
publish again; that is not a refund or replay of publisher authority. No
transport failure can change the retained mathematical object or receipt.

## Expiry, concurrency and bounded representative selection

Expiry prevents a new publish/observation commit; it does not erase an existing
route row or packet. The ordinary finite Node/service lifetime bounds ongoing
intent maintenance. DHT hints may outlive shutdown/horizon through their TTL;
they remain advisory stale hints, not an extended custody promise. Immediate
global withdrawal at a retention timestamp is not promised.

The service wrapper must track at most **one owner restoration task**. Unlike
HTTP submit, it is not automatically tracked in intake_provider.tasks. Close
must cancel/drain it together with intake under the **same original drain
cutoff**, not grant another full interval. The shared busy state blocks another
restore/submit; duplicate/status never starts restoration. If the owner task
cannot drain, retain the existing live-actor refusal to close SQLite. This is
one local task handle, not a new manager, work queue or registry.

The API requires an explicit request ID; there is no hidden global scan. An
owner restoring several cells selects at most L=max_cells distinct cells and
spends original controller calls/CPU and current-run row capacity. If IDs are
not already known, use an explicitly bounded keyset walk of the local requests
primary key, counting every examined row (including rejected rows), with
`ORDER BY id LIMIT k`, a declared scan cap <= original max_requests <=4096,
and original deadline/byte limits. Only committed candidates load bounded
manifest/receipt BLOBs; choose deterministically one still-supported candidate
per distinct cell. Stop partially when budget ends, reporting incomplete
coverage. There is no indexed cell/horizon column in requests: `DISTINCT` or
JSON filtering is not magically an O(L) lookup. No new index/schema is required
for this finite first operation, and no exhaustive coverage claim follows from
a partial scan. Call-cap charges prevent unlimited failed candidate retries.

## Minimum implementation/evidence boundary

If selected: two fresh successor modules only, advertisement and service;
existing ledger/index/wire protocol stay unchanged. No new registry, migration,
deletion, re-fetch, proof production or distribution copy is needed.

Discriminator: create a prospectively two-run generation; commit one placement,
seal/close, start a separately funded fresh locator/service over exact retained
stores, restore its cell, then discover/read it after original publisher loss.
Compare original receipt/index/custody bytes and counters unchanged apart from
new core/route run charges and route row. Negative controls need only wrong/
partial/missing representative, expired horizon, same-run uncertain replay,
max_runs/config mismatch and expiry during owner restoration. Existing passing
wire/controller suites are not a new campaign. This establishes sustained
bounded route reuse, not perpetual storage or net useful-growth benefit.
