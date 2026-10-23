# Ordinary local catalog: focused source review

2026-10-22. Reviewer: `lean_workflow_trace`. Source-only review of
`local_catalog.py` under CONTROLLER-SELECTION; no execution or Git changes.

**Disposition: the reviewed corrected internal catalog is suitable for the
selected storage/reader controls, not yet public mathematical admission.**

## Findings resolved in root source

1. **Uncertain commit kept a live grant.** The original exception path blindly
   issued ROLLBACK, including after a possibly successful COMMIT. Root now rolls
   back only while a transaction remains active and closes the owner in a
   finally clause. Normal rollback/acknowledgment failures require reopening
   and exact root lookup. No old grant can authorize retry/replay on that closed
   owner. A rollback failure can still supersede the custom diagnostic, but
   the owner closes; this is not an acceptance bypass.
2. **Extra output could become uncharged.** A committed reservation shrinks to
   actual chunk bytes. Root added an exact one-file `chunk.olean` census before
   commit. Worker logs/requests must use separately charged paths. Failed or
   interrupted reservations remain charged and bytes remain preserved.

## Identity and authority

The selected marker binds exact native profile fields, fixed seed/inventory,
store identity and local quotas. The ordinary profile has no fake zk relation
or certificate locator. Basis name count581 is only a trusted caller contract;
the actual fixed-inventory reconstruction is still required before promotion.

Extension reservation reparses immutable evidence bytes, matches the actual
profile and every direct import identity to selected parent bindings, forbids
name overwrite, and permits an ordered batch to reference its earlier claimed
exports. Those claims gain authority only after the mandatory whole batch's
Lean check and actual output comparison. The root/request identity includes
the ordered evidence IDs and exact selected parent.

`_commit_checked` remains deliberately internal. It does not establish that a
worker ran, that the bytes are a Lean file, or that the output is correct.
**The real controller must bind selected worker/profile, parent, request bytes,
module name, actual export census, fresh grant and output directory to one
clean supervised execution before calling it.** A JSON PASS report is not that
binding. Dummy-file tests below exercise none of this mathematical prerequisite.

## Lifecycle and cost boundaries

One exact live owner/unchanged grant tuple and monotonic deadline are required.
Reopen changes old RESERVED operations to INTERRUPTED and cannot resurrect
their in-memory authority. Artifact size/digest checks precede a context's
first native use in an owner process; cached digest results rely on the explicit
no-concurrent-mutation local-storage premise. Native import must never precede
`context`'s successful completion or use a different returned path.

Withdrawal is sticky in a live owner. SQLite root insertion and operation-state
change are in one transaction. Full-disk/uncertain commit handling stays
fail-closed after the repair; retained incomplete creation/state is not silently
deleted. Failed output remains conservatively reserved.

Current quotas are finite stop conditions, not a retention/GC/renewal policy.
Long-running service will eventually need explicit capacity management. Further,
`context` rebuilds all bindings and reads each selected ancestor's record on
each reservation even when artifact hashes are cached. Warm Lean state does
not remove that Python-side cost. Batch requests now; after the real workflow,
consider a small immutable-root context cache/incremental extension if this
dominates. Do not start another storage framework or broad benchmark first.

## Prospective focused controls

Authored `software/v5/ordinary_lean/evidence_catalog_checks.py`, source only.
It requires one fresh selected output parent under `experiments/v5-local-checks`
and preserves all created state below `evidence-catalog-state`. Nine groups:

- raw numeric/depth/canonical/duplicate-key and exact evidence identity/census;
- synthetic ordered-batch storage commit and reopen;
- dependency/profile/uncommitted-root refusals;
- mutated/expired grants and interrupted-state refusal after reopen;
- same-length artifact corruption refused before any native import;
- exact output census and retained failed-reservation quota;
- withdrawal before promotion/reopen;
- injected failure before real SQLite COMMIT;
- injected acknowledgment failure after real SQLite COMMIT.

The last two require the old owner to close, preserve bytes, refuse old grants,
and distinguish absent versus actually committed roots after reopening. These
are precise injected storage failures, not process-crash or power-loss coverage.
No Lean worker runs; all artifact bytes explicitly say
`FAKE_BYTES_NOT_LEAN_STORAGE_CONTROL`. Synthetic581 names are not the real basis.
Success marker states `storageOnly=true nativeAdmission=false`.

Prospective runner: pin the reader, catalog and this test source in a fresh
Run-V5-Check snapshot; run selected Python with `-I -S -B`, passing that run's
output directory. No Lean rebuild, network or certificate work is needed.
Root must independently read/select the test source before execution.

| Reviewed source | SHA-256 |
|---|---|
| `local_catalog.py` corrected | `860a9d731290b2a7fbacd4852bb68185516329ee42845648f4ba3c3856d7c751` |
| `ordinary_evidence.py` | `fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6` |
| `evidence_catalog_checks.py` prospective | `d9d77fefdad4f4c57a5cb5bbfbdd551aa1dd835f603d7223684e1ca374a08ff8` |
