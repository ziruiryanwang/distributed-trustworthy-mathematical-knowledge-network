# Retained advertisement: two fresh source successors

2026-10-21, core_release. Implements the selected explicit-request-ID operation
only. No automatic scanner, manager, deletion, HTTP change, product import,
runtime, test, proof or Git operation. Used predecessors remain unchanged.

| Fresh source under software/v5/retained_advertisement | Bytes | SHA-256 |
|---|---:|---|
| `placement/advertisement.py` | 23256 | `5aa23ee76115355ad319ae4acfd4ab418e010166e53b6ed02c82eb25d34d4510` |
| `client/serve_placement.py` | 22670 | `7e735337d595894e25fd07a8dcc9ad8cd3ba9f1c042ba930684b7798232cb7fa` |

Bases are advertisement `b5523f82` and service02 `319ddf07`. Core ledger,
controller, index, wire, Node and mathematical receiver are unchanged.

## Callable contract

```python
facet = await service.advertise_retained(request_id, until=service.deadline)
```

Local trusted owner only. No token parameter or public transport route. Return
is the existing route facet from **this run**, not a new receipt. Shared-cell
repetition returns the original current-run representative's ID, not a fabricated
new representative. An old historical route is never labeled current.

The fresh operation consumes a controller call and requires SEALED_SERVING,
exact live original owner roles/config, finite original deadline, read listener
and locator. Its retained guard never reuses/weakens the publisher's original
write-window policy. `_publish` keeps its original checks; only the common
charge-before-command body is extracted into `_dispatch`.

## Selected retained object, not proof ancestry

Read lengths before loading the selected bounded manifest/reservation/outcome;
require RECEIPT_COMMITTED, canonical manifest and recomputed request ID. Reuse
the frozen closed receipt validator, then bind reservation/recovery, original
export/packet/body/horizon, locator and derived fingerprint/cell.

Read exact index record, original and latest snapshots, admitted sequence,
feature posting/head and committed cell. Check name/group mapping, packet row
and offer, and permitted body metadata under the exact descriptor universes.
Read/validate **one selected bounded group opening** to obtain its descriptor;
do not use the old controller `_local_*` helpers outside their structural-budget
context. No packet proof/body blob is read, reverified or reinserted; no export
re-admission, pull or custody copying occurs. This is restored advisory routing,
not a new fresh-byte availability certificate or mathematical acceptance.

Before each route transaction COMMIT and dispatch, and after its await, the
guard repeats exact saved-row equality, local metadata and fresh owner/clock
bounds. It requires original retention still live and nominal current service
end within that horizon: sample monotonic m before wall w and check
`w + ceil(1000*(original_service_deadline-m)) <= original_retention_end_ms`.
The selected opening is not repeatedly decoded by those guards. Existing
wall-clock assumptions and stale-hint/TTL limits are unchanged.

## Durable effects and task lifetime

The original route journal reserves `(cell,current_run)` and its attempted
charge before publish. An existing row never republishes, including after
uncertainty. Post-send expiration/failure leaves the durable attempted row;
there is no same-run retry/refund or receipt rewrite. A fresh separately funded
run can intentionally restore again, subject to original immutable max_runs.
No special same-run resumption or new journal schema was added.

Independent review identified that reservation COMMIT itself can consume the
remaining wall-clock horizon. `_dispatch` therefore checks its guard again
immediately after that COMMIT and before `publish`. Refusal at this point keeps
the durable attempted charge and sends no command. The same pre-send check also
strengthens ordinary submission without changing its original window policy.

The service registers one `_retained_task`. Caller cancellation propagates;
a surviving task stays tracked. Close cancels it before HTTP shutdown, then
joins it using the **same** `intake_until` cutoff, not another drain allowance.
`cleanup.retained_closed` and explicit task-done/no-handle tests gate SQLite
closure, including cancellation before the task enters its busy slot. An actor
that survives the original drain causes failed cleanup, not hidden continuation
or a new budget. The service02 locator-close repair remains unchanged.

`_now_ms` remains the narrow wall-horizon seam for focused controls. Expected
refusals have `PLACEMENT_RETAINED_*` codes; owner task concurrency uses
`PLACEMENT_SERVICE_RETAINED_BUSY`. Original submit/status behavior and wire
schemas remain unchanged. Reopening still requires exact previous config/read
endpoint and spare original core/route run caps.

Exact sources are ready for independent changed-boundary review and core_growth's
focused simulated controls. This checkpoint is not a test or release pass;
root alone selects execution and later adoption.
