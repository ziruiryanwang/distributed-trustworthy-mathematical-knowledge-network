# Interrupted intake: recover state before interpreting cost

2026-10-26. `intake_cost_localization`. Source and small saved-data inspection
only. Canonical guard passed. No product import, owner/status call, database
opening, experiment, source mutation, selector invocation or Git action occurred.
The separate interruption audit owns the complete saved-file census; the separate
recovery decision owns the exact safe public command. This note does not duplicate
those audits or authorize another intake.

## Decision

**Use the existing protected status/context mechanism first, under a separately
reviewed finite selection. Do not infer a parser, kernel, memory or time failure
from this interruption.** The saved data cannot identify a costly phase or supply
an actual intake CPU/peak-memory measurement. It therefore does not justify a
wider parse cache, larger grant, repartitioning, certificate route or benchmark.

The real user obstruction remains establishing a reusable rich mathematical base.
Recovering the eligible local parent is necessary before choosing the next action.
If a future fresh intake is justified after recovery, retain bounded intermediate
diagnostics so an interrupted process does not again erase every phase/cost clue.
That is a small operability change, not a profiling project or proof of speedup.
No implementation is selected here.

## What the existing instrumentation establishes

The stopped selection is `std-intake01`, SHA-256
`2125ea3708989b3a424c47c3e2a3f56c458254cbe3bfd8d7907cacf538f4cddc`.
Root reports the former runtime handle missing and no matching live Python/Lean
process at 22:32 UTC. Neither observation identifies the historical stopping cause.

The independent interruption auditor reports twelve saved run files, including
four empty logs, with no outer RESULT, public RUN/SUPERVISION or owner report.
Catalog files contain only the adopted basis call/artifact, no new admission-call
directory or operation artifact and no WITHDRAWN marker. Database timestamps are
not acceptance authority and were not used to infer database contents.

Source explains why these observations are insufficient:

| Existing boundary | Persistent evidence and limitation |
|---|---|
| Outer runner | `tools/Run-V5-Check.py:106-120` calls supervision first; total CPU/wall and RESULT are written only after it returns. Missing RESULT supplies neither a final resource measurement nor clean closure. |
| Public launcher | Installed `run.py:337-359` writes prospective LAUNCH before supervision. SUPERVISION and RUN follow return. LAUNCH's `NO_CHILD_LAUNCHED` is its initial intent record, not a terminal finding that nothing ran. |
| Public owner | Installed `owner.py:353-641` holds SUPPORT/OPEN_OWNER/INTAKE_BASELINE phase and cost locally; final JSON is printed after `run` returns. Empty stdout does not locate the interrupted phase. |
| Intake | `baseline_intake.py:272-330` holds phase, batch position, confirmed root, observations, reservation and CPU measurements in memory. A caught exception reports them, but abrupt termination need not execute that handler. |
| Admission | `ordinary_admission.py:550-655` stages custody and reserves a grant before creating the native-call directory. `_execute` then writes installation/plan/units and only afterward enters native supervision. |

Under the selected code and normal preservation of its writes, a native extension
cannot be entered without a new call directory; the code does not remove that
directory afterward. Its absence therefore supplies no evidence of an executed
native extension and conditionally excludes that point on the normal path.
It does **not** distinguish support loading, input validation, whole-manifest
planning, actual batch reread/preflight, admission planning/serialization, custody
staging, catalog validation, or an interruption before the child actually ran.
Absence of an artifact alone would be weaker still: native failure could precede
artifact creation. No saved marker authorizes a new mathematical root.

Ordinary caught budget/refusal paths normally produce an intake/owner failure
report and closed supervisor reports. None is retained here. That is an unknown
outcome, not evidence that a particular limit was reached. Likewise, elapsed
calendar time since the files were created is not the process's measured runtime.

## Cost implications

The completed focused controls, file-only assembly and basis initialization cost
58.84375 known CPU seconds, as already adopted. The interrupted intake's CPU and
peak commitment are **unknown, not zero**. Preserve an explicit unknown addend;
do not turn the configured 300/330-second caps into measured consumption or erase
this attempt from later full-cost comparisons.

The prior source count remains valid: eight strict reads per fresh successful
unit, 359,302,744 scan-input bytes for the full closure, and approximately
`C_controller + 180 < 300 - C_startup - 1` for all three completed grants under
the actual integer accounting. This is a conditional workload/allowance model.
The interrupted run supplies no completed phase time to calibrate it. The known
13-to-8 structural improvement neither failed nor became a measured speedup here.

## Minimal future diagnostics, if root selects that change

One auxiliary-payload successor is feasible in principle:
`reference/baseline_intake.py` can record its own entry, metadata batch boundaries,
actual read/preflight boundaries, admission entry, and each actual returned
confirmed prefix. Existing `owner`, admission, catalog and native bytes can remain
unchanged. Its PROFILE binding must change; the controller implementation ID can
remain unchanged **only after an exact support-map comparison confirms that this
auxiliary file is outside the implementation descriptor**. This must not be
misrepresented as changing the identity of old checked state.

Prefer the existing `ordinary` path validation and exclusive, flush/fsync
`PortableCatalog._write_fresh` mechanism. A fresh dedicated
`owner.directory / "intake-diagnostics" / <random local token>` subtree is a
possible location: the current catalog validates its named state files rather
than forbidding unrelated diagnostic subdirectories. Keep it distinct from
`operations/`, `imports/`, existing native `admission-calls/`, source inputs and
runtime support. Validate every ancestor, refuse collisions/links and never
rewrite a prior attempt. The existing owner lock serializes this operation.
This location is a design candidate, not permission to create it now.

Do not put progress on stdout or stderr: the public route expects one final JSON
document and treats nonempty stderr as failure. Do not use stack introspection,
monkeypatching, a global cache, a new subprocess, or a callback receiving mutable
Evidence/proof trees. A private diagnostic sink need receive only bounded scalar
phase/batch/count/time fields and already-known identity strings.

Useful bounded records are:

- Entry with selected parent and manifest hash; no claim of manifest validation.
- Metadata batch begin/end, allowing one batch's parser/planner/quota work to be
  distinguished from later admission. `_plan_all` can accept an internal optional
  sink while keeping direct callers without a sink unchanged.
- Actual batch read/preflight begin/end and admission intent before calling
  `owner.admit`.
- After a genuine return, first update `confirmed`, `entered` and `observations`
  exactly as today; then record the returned prefix and resource observation.
- Terminal success/failure when ordinary control flow permits it.

The existing maximum of 64 batches bounds this to a small fixed multiple of 64
records, not one record per theorem/node. Give both record count and total bytes
explicit ceilings, include diagnostic I/O in existing time/CPU/spool accounting,
and allow only one write per boundary. A per-invocation byte bound is not a global
disk-retention guarantee; repeated local operations still require retention
policy just as existing admission-call diagnostics do.

These records can distinguish metadata, reread/preflight and the aggregate admit
interval. They **cannot** split custody, catalog validation and native CPU inside
`owner.admit` without a separate core change. Existing native-call artifacts can
help after that boundary; do not promise finer timing from a one-file change.
Nor can a baseline-only sink diagnose owner bootstrap before intake entry.

## Authority and failure rules for those diagnostics

A begin record means intent, not completion. A returned-prefix record describes
an actual local return but is not a portable warrant and must never be read back
to authorize admission, reconstruct a grant, select an automatic resume cursor,
or replace protected context validation. Process death can still occur between
the catalog's atomic commit and the next diagnostic write. Recovery must therefore
continue to use the actual protected status/context, even when logs exist.

Before admission, a diagnostic write failure may stop the operation without a new
native call. After admission returns, the controller must update its confirmed
prefix before any fallible diagnostic I/O. A later diagnostic failure cannot
roll back that commit or erase the prefix from an available failure report.
In exception reporting, a secondary logging failure must not replace the original
error or its possible-unreported-commit flag. Partial diagnostic files are retained
and treated as incomplete, not repaired in place or counted as successful records.

Only if root selects this diagnostic seam should a small changed-boundary test
cover write failure before/after a synthetic admission return, bounded records,
no mutable-object leakage and preserved prefix/uncertainty semantics. There is no
reason to repeat parser/kernel/transport campaigns or run a new performance suite.
Actual recovery and its outcome remain the immediate prerequisite.

## Inspected source pins

Paths are in `experiments/v5-local-checks/parse-reuse-package01/distribution/package`
except the final runner row. No product source was imported.

| Source | SHA-256 |
|---|---|
| owner.py | 56ef042f652fcb88cae7d16ab74883016a469e2e82777c1a173f842f5ef8245a |
| run.py | 47a2b63c73f1bd8346c5881c6d6a76abac86d33aa8e55bfc19bf3359ea924a39 |
| reference/baseline_intake.py | 9b243232603206b3a0925f639a0b8b1a6cbf0de8ca093ad4aa3642c595ff1142 |
| installation/py/ordinary_admission.py | 98c88eb0e7ea5e101f6ccd8e94b56a0cc248167c317a0440ba00dc86f503cd9a |
| tools/Run-V5-Check.py | 44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651 |

The unchanged catalog reserve/commit/open source and baseline bundle limits were
also inspected. Full v5 remains active; this is a recovery/observability decision,
not rich-library acceptance, a diagnosis of the interruption or a growth result.
