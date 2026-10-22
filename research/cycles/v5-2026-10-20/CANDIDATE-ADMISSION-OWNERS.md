# Candidate admission: lower owner source checkpoint

2026-10-22, `storage_outcome_audit`. **IMPLEMENTED SOURCE; NOT RUN.**
Root's [implementation selection](CANDIDATE-ADMISSION-IMPLEMENTATION.md) governs.
Only three fresh files below `software/v5/candidate_admission/` were written;
used predecessors, installations and evidence are unchanged. No imports, tests,
runtime, Git mutation or new experiment were performed.

| New relative path | Bytes | SHA-256 |
|---|---:|---|
| `admission/clean_refusal.py` | 6462 | `7c1386cce693185ac7d6e1dda149993c892ac5b2d417242fb7e02b873648e5a7` |
| `admission/verifier.py` | 17835 | `ec6474cdd0580df89f9c646a41c0d909ec20e83da0a42274e0510a6e01bbbaea` |
| `aggregate_claims/aggregate_admission.py` | 20129 | `ce2cfc95f08699c679128448d9d9f5131cf54acbefa91225db2689a2b1574f5c` |

Predecessors are I verifier `32289cac...` and A admission `2ef830f8...`.
Read-only focused diffs confirm the existing execution/binding/handle body is
shared, not independently reimplemented. Existing `receive` passes
`allow_refusal=False` and cannot return `None`. New `try_receive` has identical
arguments: a normal live handle on success, `None` only on the complete clean
branch, and revocation of its original owner on every escaping exception.

## Concrete changes

- Private `validate_report(report, *, argv, cwd, limits)` enforces the selected
  supervisor's exact19-field report and7-field final Job shape; same call/limits;
  exit1, no error field, empty stdout; strict cleanup/termination flags; finite
  final CPU/wall/wrapper metrics, actual log caps, observed memory cap and Job
  counts. It never mutates its inputs or decodes diagnostics.
- `validate_output(supervisor, directory, report, *, byte_cap, entry_cap, active)`
  checks actual ordinary logs, including permitted zero-byte files, and invokes
  a streaming bounded own-directory census. The directory is the operation root,
  not its `command` child. The caller first validates the report structurally.
- I/A opt-in nonzero branches validate that same-call report, fresh original
  pins/trust, actual outputs, then write bounded refusal evidence and census
  again. The saved evidence explicitly says final owner guards are pending;
  it is not a reloadable result. Exact receipt/header reread, another independent
  pin/trust phase, active guard and original deadline check precede `None`.
- I's opt-in attempt has a32-entry / `len(receipt)+1MiB` own-output bound, also
  checked on positive completion. Its total possible retained bytes are bounded
  by already charged submitted bytes plus one MiB per charged operation; no
  refund or new owner allowance. A retains its existing output reservation.
- Positive opt-in admission follows the same original success binding and handle
  insertion, with fresh post-child/final checks. Refusal never writes any handle,
  member or cache registry. Existing registries are neither scanned nor restored.

## Source pins and integration

The base constructor now requires `admission/clean_refusal.py` in runtime pins;
installation checks bind its original module object, canonical source path and
file pin. A's required-origin map also includes that helper. The selected runtime
profile already builds its source/runtime pin maps from all selected `v5/*.py`
rows, so the new130th logical SDK row supplies this dependency without a runtime
profile source change. Root must include it in the fresh source/preparation map.

Fresh `PP.phase` scopes begin after the child has finished, end synchronously,
and do not borrow earlier validation caches. No phase created here spans a
subprocess. Final checks occur after all potentially blocking evidence I/O.

Independent source review, root's focused predicate/transition controls and a
separate finite actual refusal/continuation boundary remain pending. This source
checkpoint does not assert runtime success, new mathematics or completed v5.
