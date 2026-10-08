# Replica native 02: one receipt-contract correction

2026-09-21. Source-only author handoff. Allocation 01 failed at invocation 16;
its source, installed cut, charges, faults and evidence remain untouched. No
rerun, repair, recovery or mathematical acceptance is inferred from its prefix.
The independent allocation-01 outcome audit is separate from this source note.

## Evidence and cause

`py/supervise.py:298` sets `TRANSPORT_COMPLETE` for exit 0 and
`TRANSPORT_NONZERO_EXIT` for a cleanly supervised nonzero worker exit. The latter
is returned with genuine output after quiescence; it is not `TRANSPORT_FAILED`.

Allocation 01's exact tampered-service receipt records exit 1,
`TRANSPORT_NONZERO_EXIT`, direct-child reap, final active-zero, checked Job close,
zero limit terminations and no failure/cleanup/persistence error. Its worker
returns `SERVICE_REFUSED / BUNDLE_DIGEST_MISMATCH`; the installed wrapper returns
the matching refusal with exit 1. The harness incorrectly required
`TRANSPORT_COMPLETE` while simultaneously expecting worker exit 1, so its
`PUBLIC_TREE_QUIESCENCE` predicate failed before the later negative checks.

The actual receipt is
`product-local/replica-native-01/b/scratch/services/b-tampered/cases/serve/supervisor.json`.
No C admission or H submission/publication/exposure followed this failed gate.

## Exact fresh-source delta

New files only:

- `tests/replica_native_worker_v2.py`
- `tests/run_replica_native_v2.py`

They select fresh `product-local/replica-native-02` and
`software/qualification/replica-native-02` roots, with corresponding new worker/
coordinator source references. Neither root existed at handoff inspection.
The only behavioral correction is:

```python
expected_status = "TRANSPORT_COMPLETE" if worker_exit == 0 else "TRANSPORT_NONZERO_EXIT"
# In the existing require predicate, replace only the literal status comparison:
# receipt["status"] == expected_status
```

All success callers still expect exit 0. Only the fixed tampered B service
supplies expected exit 1. The receipt still must match that exact code, exact
pins/limits/files/request/command/output/event bindings, checked close, actual
active-zero/direct reap, no errors and zero limit terminations. Nothing permits
`TRANSPORT_FAILED`, an arbitrary nonzero negative, missing evidence or uncertain
cleanup.

The downstream negative branch was checked against the actual retained outputs:
it requires wrapper exit 1, exact wrapper-to-worker refusal correspondence,
worker `SERVICE_REFUSED/BUNDLE_DIGEST_MISMATCH`, false mathematical acceptance,
zero native stages and no readiness file. These conditions need no change.
`finish_service` then records its bound stop observation before C admission;
the positive A/B service checks and all later native gates remain unchanged.

## Unchanged allocation

Keep all 20 invocations, 13 new requests plus one replay, four mathematical
stages/eight children, two separate support compilations and 1016 MiB charges.
The same exact G/H inputs, one-space derivative, faults/quarantine, ports
42381/42382, public limits, outer 450 wall/CPU seconds, 6144 MiB/16 processes,
1 GiB endpoint allowance and 14 input pins plus launch are retained. No product,
fixture, workload, budget or prior evidence change. Fresh copying and checking
must occur; no acceptance is borrowed from allocation 01.

Independent source-delta and exact-launch review must precede root's single
execution of the separately selected allocation. Author performed only file/
source/evidence reads and new-file edits: no Python/Lean execution, import,
compilation, AST parsing, network or SQL operation.
