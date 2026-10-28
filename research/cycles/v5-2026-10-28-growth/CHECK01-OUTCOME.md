# Observation-modes check01: failed proofs, successful retained import

2026-10-28 independent saved-output audit. No native operation or replay.

**Outcome: CLOSED FAILED. No new theorem is accepted.** The exact ordinary
source check exited 1 with clean closure: direct child reaped, final active
processes 0, Job closed, cleanup errors empty, no termination request. It used
55.2315531 wall seconds and 3.9375 known CPU seconds (2.84375 Job + 1.09375 outer
wrapper; do not add the nested supervision counter again). Peak Job private
commit was 893,644,800 bytes within the selected 1280 MiB limit.

## Actual output and interpretation

Saved stdout is 5,921 bytes; stderr is empty. The diagnostics identify three
source repairs: restore the needed `rfl` after the Boolean rewrites, explicitly
include the proof-only section hypothesis `atomic_law`, and disambiguate three
constructor applications as `Mode.zero`/`Mode.one`. Missing hypotheses produced
further application/type errors; those diagnostics are not separate discoveries.
The earlier static prediction that rewriting would close the Boolean goal was
wrong. Source02 and the failed run remain unchanged.

The import/axiom output is decisive:

| Declaration | Actual axiom output |
|---|---|
| `FiniteMapRefinement.Context` | No axioms |
| `ResetEffects.minimum_outcome` | `[sorryAx]` |
| `ResetEffects.guarantee_iff` | `[sorryAx]` |
| `ResetEffects.contextual_iff` | `[sorryAx]` |
| `ResetEffects.skip_not_refined_by_reset` | `[sorryAx]` |
| `ResetEffects.write_then_reset_false` | `[sorryAx]` |

The retained compiled Context was imported at the relocated module path. No
missing Context/imported-Plan code-generation diagnostic occurred. This supports
the cheap import route, but the failed new declarations provide no proof warrant.
There are **zero** `OrdinaryProducer.*` compiler outputs and the intentionally
unused candidate JSON is absent. No owner, publication, database or network
operation was selected by this check.

## Exact-input audit

Current read-only rehashes match all 81 nonruntime selected/snapshotted inputs:
70 helper companions, package PROFILE, six scratch input files, input manifest,
source body and both source snapshots. The wrapper contains the exact source02
body once. Its five relocated module companions retain the original identities
listed in CHECK-ROUTE. The frozen runner checks all 102 external pins before
invocation; this audit did not repeat the larger 23-file runtime rehash. That
explicit runtime selection is not a hermetic toolchain proof.

Evidence under `experiments/v5-local-checks/observation-modes-check01`:

- `selection.json`: `7da96e76cfeb32992ea04d90a9e087a5972927da4dea315be18e6b70e75f659a`.
- `RESULT.json`: `86d171274f4ddc3d8b01fd721561287ae3602a20be0bad52e3aef706a63bbebc`.
- `command/stdout.txt`: `89b8ea274ca5495a319b23408093be8d7003532eae20bf4805820c408700785b`.
- Empty `command/stderr.txt`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

The selected wrapper remains `025fd5e2…`, source02 `ee736d99…`, and input
manifest `633d0053…`. A fresh corrected source must be independently reviewed
and separately selected before another check. The current failure is preserved,
not retrospectively qualified.
