# Structural query retirement and helper binding

Owner: core_growth. Selection: `ITERATIVE-DISCOVERY-SELECTION.md`.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
No import, runtime, test, proof, build or Git mutation was performed.

## Exact source lineage

Fresh `software/v5/iterative_queries/evidence_network/transport.py` derives from
`software/v5/evidence_network/transport.py`, predecessor SHA-256
`f4734bff9bdfd2ac3fc7ae770a9bc3f0d4b6e47a41ab60fd65fa21ab50f7b880`.
Fresh `software/v5/iterative_queries/client/semantic_reader.py` derives from
`software/v5/interface_views/semantic_reader.py`, predecessor SHA-256
`eb925191365d9f4daf04b86804f484e4096713f7ad9dd4b0919d1ab584bbe641`.
Both predecessors were hash-checked and remain unchanged. Reader is the current
interface-only-capable source, not the earlier supplier-resilient implementation.

## Narrow retirement method

`EvidenceAcquisition.retire_generation()` takes no arguments. Already closed
scopes return without consulting or changing shared authority. Otherwise it
requires `budget.pending is None`, zero structural inflight and zero structural
reserved bytes. It marks the old scope closed, clears offered-packet authority,
expires its structural deadline, and removes both endpoint lookup maps.
It never closes or replaces the shared AcquisitionBudget, issuer, custody store,
grant, verification cache or original deadlines. Held bytes remain untouched.

The serialized direct-query orchestrator separately checks/settles all search
reservations, marks the old SearchSession non-ACTIVE, snapshots compact costs,
clears stale candidate/staging maps without resetting cumulative counters, and
replaces client references. Those are not delegated to this transport method.
Saved contact objects reject through the old exact binding because its
acquisition is closed; saved structural paths have no usable endpoint/deadline.
Calling old terminal `close()` now returns before the pending-budget check, so
it cannot close a successor's shared ledger even during its pending request.
Terminal close of the current active scope retains the existing budget close.

## SemanticReader generation guard

Construction captures exact initial client search and acquisition objects.
`_active()` additionally requires both identities still match and the captured
acquisition, if any, is not closed. All ordinary actions already enter `_call`,
which checks `_active()` before any helper mutation or delegated call, and after
successful completion. Changed/retired generations therefore fail before work;
the existing exception path marks that helper FAILED. There is no helper registry.
`close()` and inert accounting `report()` remain available after rotation and do
not close the client. No helper import, admission, supplier fallback, interface
mode, warrant or mathematical acceptance rule is changed.

## Source-only argument and handoff

Diffs contain only the retirement method, early closed return in terminal close,
one descriptive docstring, and reader identity capture/checks. The README states
the agreed opt-in API, additive envelope, no-refund/fixed-deadline rules, stale
handle retirement and the single sealed import restriction. Core_search owns
that envelope and orchestration; core_release independently owns controls/review.
Focused later controls should distinguish old saved helper/contact/search
refusal, pending-retirement refusal and old-close safety from mathematical tests.
No executed behavior or beneficial mathematical growth is claimed here.
