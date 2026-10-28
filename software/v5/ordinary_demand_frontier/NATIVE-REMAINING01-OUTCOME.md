# Remaining01: harness blocked normal custody readback

2026-10-28. Independent saved-data/source review only; no product import,
database open, runtime, Git or old-source/evidence change.

**FAILED before a new native admission call. Neither negative is qualified.**
False-parent scratch authoring succeeded and constructed exactly one Above.d
unit above F; the candidate states `Above.d = Nat.succ (Nat.succ Nat.zero)`
with explicit `@Eq.refl Nat Above.d`. Its authoring process exited zero and
closed cleanly. The continuation then failed in ADMISSION because its guard
incorrectly permitted only the acquired Above.d evidence read.

The unchanged admission source `_stage` writes the newly bound candidate into
inert custody and reads it back before reserving any extension or launching the
native checker. That second, ordinary read triggered
`FRONTIER_NATIVE_FORBIDDEN_OR_REPEATED_EVIDENCE_FETCH`. The wrapper then reported
`FRONTIER_NATIVE_SEMANTIC_NEGATIVE_INCONCLUSIVE_EARLY_REFUSAL`, correctly declining
to treat this as mathematical rejection. The failed read was rejected before
being appended to the old trace, so that trace alone cannot identify its UnitID;
the exact staged-read ordering and candidate file identify the source cause.

Saved directory census still contains the same four admission-call and four
operation directories. There is no new failed native call and no missing-case
directory. Candidate custody bytes may remain and must be preserved; no quota
or state reset is needed. No final root inventory was reached, and this reviewer
did not open the database. The next public reopen must revalidate the same four
accepted roots and four calls before proceeding.

Outer wall: 4.5493878 seconds. Job CPU: 3.75 seconds; outer wrapper CPU: 0.5
seconds; total known CPU: 4.25 seconds. Child exit 1, no termination, zero final
active processes, child reaped, job closed, empty cleanup and owner-close errors.

| Preserved evidence | SHA-256 |
|---|---|
| remaining01 outer RESULT.json | `5f5d207351d077514ececb4377a72f3554a1594f419c1600dc8d2adf440d5934` |
| workflow OUTCOME.json | `2508130372a899036325891a4ea647b1353254aaaff851804ae7ae1be96d6d6b` |
| false-parent candidate.json | `a6e71f8ee09c3216a0a90886e6485cd39adc7e8cd8328c75e890fae282c848ec` |
| false-parent FAILURE.json | `43c096ccb21159fde6ef9f1d6f21645c9c2fdb5859be789a93b488943d1aa084` |

## Fresh correction for root review

Root assigned this reviewer authorship of fresh `native_remaining02.py` after
the failure audit. Therefore this section describes the correction; it is not
an independent review of the newly authored source. Used native_remaining.py
and all original evidence remain unchanged.

The successor restores the original workflow's bounded pass-through read trace:
at most 16 reads, never Base.c evidence, plus at most one Above.d read. Exact
postconditions require two reads for false-parent and one for missing-name.
The second negative read's strictly parsed evidence unit must equal both the
freshly exported candidate unit and the actual native-input unit, with exact
semantic ID, P and theorem target. This permits the required custody readback
without permitting ancestor retrieval or counting an unrelated read as the new
candidate. The unchanged strict theorem-shape and final-native-refusal assertions
remain. The four remaining01 failure files above become before/after pins and
their clean, unaccepted guard-failure precondition is checked on entry.

No product change, new comparison mechanism, repeated basis/positive/alternate
compilation, state reset or larger allowance is introduced. The fresh run keeps
180 wall/100 CPU internally and 210 wall/120 Job CPU/2048 MiB/eight processes
externally. Standard-library AST parsing passed; no workflow import or execution
ran. Root must review and select the successor separately.

Fresh source: 18,477 bytes, SHA-256
`a63573855cfcbb1c755f5e82a99fa268e618d8919593e7f59f0114c670998f26`.
