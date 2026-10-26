# Reopen the interrupted owner through its existing bounded status API

2026-10-26. Source-only decision by `interrupted_owner_recovery`. Canonical guard
passed. No product import, owner/status call, database opening, recovery operation,
native execution, state change or Git action was performed for this note. The
separate INTERRUPTED-INTAKE-OUTCOME owns the saved-run facts and their limits.

## Decision

After preserving the stopped run and the closed pre-reopen state, the smallest
useful existing operation is one public **`owner status --context-root`** against
the already adopted basis, with a four-row root inventory. This can both retire
abandoned reservations and validate the known committed context without running
Lean, retrying intake, reinitializing the basis or editing a database privately.
Root must separately select it after the interruption audit and a fresh process/
exclusive-access check. This note does not authorize execution.

This is not a read-only operation. Do not infer clean old-process closure from a
successful later reopen, or recreate a missing old RESULT/RUN report. The old run
remains interrupted/unconfirmed and its cause and unmeasured cost remain unknown.

## Source argument and exact effects

The actual package is
`experiments/v5-local-checks/parse-reuse-package01/distribution/package`.
Its `owner.py:233-263, 410-440, 507-523` exposes the existing status route:
validate actual support and adoption/store/limits; open custody and catalog;
read at most `limit + 1` root rows; read custody counters; optionally invoke
`PortableCatalog.context` for the explicitly supplied root; close both stores.
The status branch never calls initialize, admit, a native worker, source export,
network acquisition or intake.

Opening has these material effects and constraints:

- `support/transport/ordinary_acquisition.py:88-149` opens custody first, sets
  SQLite DELETE/FULL/page-count pragmas and may recover its bounded rollback
  journal. Its counters are inert storage accounting, not mathematical acceptance.
- `installation/py/portable_catalog.py:143-242` checks identity/ordinary paths,
  takes the existing nonblocking Windows one-byte owner lock, opens SQLite and
  permits bounded DELETE-journal recovery. WAL/SHM sidecars are refused.
- The same catalog open executes `UPDATE operations SET state='INTERRUPTED'
  WHERE state='RESERVED'`. No old deadline or live event authority survives
  reopening. It neither frees the retained reservation charge nor deletes its
  artifacts. It never converts an abandoned reservation/report into a root.
- A WITHDRAWN catalog refuses; an IMPORTING destination cannot reopen ACTIVE.
  No lock, marker, sidecar, operation or journal may be deleted to bypass refusal.
  Check known refusal conditions before launch where ordinary file inspection can
  establish them. Custody is opened before the catalog lock, so root must serialize
  all accesses to both stores; the catalog lock alone does not supply that premise.

`PortableCatalog.context` at lines 530-548 follows only stored root rows back to
the basis, checking the bounded lineage, identity/name/import binding and snapshot
length/hash. For native roots, lines 390-437 require the corresponding operation
to be COMMITTED with the exact root and artifact charge. `_commit_checked` at
637-684 is the only native promotion seam: after a live clean checked event it
atomically inserts the root and changes that operation to COMMITTED. Recovery
does not rerun that seam. `_artifact` at 317-332 hashes bytes; it does not load or
execute a retained `.olean` file.

Thus a reopened, validated committed root is local stored authority under the
existing trusted-controller/protected-state premises. A root inventory ID or
an orphan `.olean`/worker report alone is not. A committed root can survive loss
of the caller's final stdout; absence of stdout neither proves rollback nor
authorizes manufacturing a new success report. Arbitrary same-account state
tampering or checker compromise is outside those premises and instead invokes
the fresh-state procedure in `software/v5/UPDATE-AND-RECOVERY.md`.

## Preservation before any mutating-capable reopen

1. Preserve the failed run's selected sources, selection, LAUNCH and all logs;
   do not overwrite or fill in missing terminal reports.
2. Obtain a fresh matching-process census and serialized ownership. The old
   missing tool handle is not, by itself, a complete process-tree proof.
3. Before SQLite can recover/delete a journal or modify reservation rows, retain
   a bounded exact closed-state copy of catalog and custody, including existing
   journals, locks, markers and operation artifacts. Use a fresh location, ordinary
   nonredirected files, complete relative-path/length/hash census and verified
   readback. Do not label a live copy consistent. Root chooses this file-only
   preservation after the other audit establishes the actual finite census; it
   must not copy an unexpectedly huge or changing tree without a new decision.
   The backup is evidence, not an alternate owner to open or migrate.
4. Reuse the same installed implementation and original quotas/store ID. No new
   basis or mathematical intake is needed just to inspect what survived.

If safe stopped ownership or supported intact state cannot be established, hold
the reopen. Do not turn an uncertain lifetime into a retry-until-pass campaign.

## Exact prospective public operation

Use a fresh existing-runner allocation, suggested name `std-recovery-status01`.
Root must verify that name and its diagnostics are unused. The direct child argv
is the following, with the runner substituting its ordinary fresh placeholders:

```text
D:\Python314\python.exe -I -S -B
"E:\Distributed Trustworthy Mathematical Knowledge Network\experiments\v5-local-checks\parse-reuse-package01\distribution\package\run.py"
--profile-sha256 37fcb52050beada7c1f9cdabd957d57a6a3a5adfc8b822d873595773734ff750
--python-runtime D:\Python314
--lean-runtime "E:\Distributed Trustworthy Mathematical Knowledge Network\software\runtime\lean-4.34.0-windows"
--diagnostics {output}\owner-status
--wall-seconds 35 --cpu-seconds 10 --memory-mib 512
--active-processes 1 --stdout-bytes 1048576 --stderr-bytes 1048576
owner -- status
--catalog "E:\Distributed Trustworthy Mathematical Knowledge Network\experiments\v5-local-checks\std-catalog01"
--custody "E:\Distributed Trustworthy Mathematical Knowledge Network\experiments\v5-local-checks\std-custody01"
--store-id eaca70ad43af5c6ec9a362f1b44f5ac9b45e7924703f25648f2398eea32b1d7f
--custody-limits {snapshot}\software\v5\ordinary_std_intake\custody_limits.json
--context-root 3034986549a52b2a0b46f5fffe2c650879453f43ff85d4ef38cf3ff73b7a7d62
--limit 4
```

No `--parent-root`, `--output`, source, project, bundle or intake option belongs to
this command. The launcher adds profile/runtime/allocation arguments to owner;
do not duplicate them after `owner --`. Limit four accommodates the intended
basis plus three possible committed batches while bounding inventory; it is not
a claim that all four exist. The source allows limits 1..256.

Suggested outer allowance: **60 wall / 20 inclusive Job CPU seconds / 768 MiB /
two active processes / 1 MiB per stream**. This reuses the independently adopted
`ordinary_multi_source_package/STATE-OUTCOME.md` status envelope, whose actual
four-module context check cost 1.625 known CPU seconds. The new known basis has
one 669,968-byte snapshot. Package/support hashing and possible journal recovery
remain work; the earlier result is not a guarantee. Public 35 seconds is the API
minimum, not a predicted duration. No native worker or per-batch reservation is
entered. Keep the first success/refusal and do not automatically enlarge limits.

## Pins and required saved evidence

Reuse the adopted package's exact 154-file map and the existing 23 runtime pins,
not an unpinned software directory. PROFILE is shown above; INSTALLATION is
`a7403d6b798a654f7e5c76a863304bf415ad6016c6634a35513e73657ab0f9eb`;
implementation is
`89450cdf07416e0c07cb3ef51ae3f4e1c0393c12376207582b1f03bbb5a6de60`.
Root's new direct selection should pin the existing runner, original quota and
this decision; no new selector or harness is needed. Immutable init evidence and old intake
selection bind the context and interruption. Do not pin mutable database/journal
bytes as unchanged runtime inputs: legitimate reopen may change them. Preserve
them separately as above. An exact final source/input count belongs to the actual
selection, not this recommendation.

Independently checked source hashes for the traced route:

| Path in package | SHA-256 |
|---|---|
| owner.py | 56ef042f652fcb88cae7d16ab74883016a469e2e82777c1a173f842f5ef8245a |
| installation/py/portable_catalog.py | aeaf0c7d507baa6b63d401c432ca71557bf29b6b576b1f6cd8381e4e87c7473e |
| installation/py/ordinary_admission.py | 98c88eb0e7ea5e101f6ccd8e94b56a0cc248167c317a0440ba00dc86f503cd9a |
| support/transport/ordinary_acquisition.py | 076130f7a34b505df33ee550501d1c4276bb46e408ff226df765225933a0658e |

Original custody quota SHA-256:
`0342d3558227a97c665832209a0b88a9dc39aef2106ced5b500b9cb145c8a7ce`.
Adopted init RESULT:
`f15c18645b910fb13a7503ed6a026bb61e2c72c856d7db493a23d40bea5163a6`.

Require owner `ok:true`, operation status, matching new PROFILE/implementation,
store/catalog/custody/quotas, `LOCAL_OWNER_OPEN`, no close error, worker CPU zero,
and clean public/outer closure. Selected context must equal the adopted basis,
with one module, 581 names and 669,968 artifact bytes. That validates the known
base, not any new Std extension. Record every root inventory row, `has_more` and
custody counters without treating counters as accepted-unit counts.

If other roots appear, do not choose the lexicographically last as the latest
mathematical parent. A separately selected exact context validation and manifest/
event correspondence may resolve unreported committed work; this first command
does not validate every inventory entry. If it refuses on withdrawal, lock,
identity, journal, uncommitted-root, artifact or corruption checks, preserve that
result and stop this route. Do not privately repair rows or force it open.

A later status report is not an allowed parent report for every existing helper
preparer; do not relabel it as init/intake. It can supply explicit local recovery
knowledge under the existing public API. No automatic intake, contribution,
release update or new mathematical claim follows from it.
