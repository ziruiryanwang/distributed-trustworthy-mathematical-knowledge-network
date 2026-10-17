# Independent aggregate producer controls review

Current disposition: **PASS_ACTUAL_SYNTHETIC_CONTROL_OUTCOME** for the one
root-executed allocation below. No test was executed or repeated by this
reviewer. Source/exact-plan review and narrow outcome scope remain distinct.

Reviewed the complete new `software/v5/aggregate_production/test_producer.py`,
its author checkpoint, changed aggregate product seams, retained helper imports,
and exact runner/selector. No product edits, imports, test/native/proof/build
calls or Git changes were made. Canonical root was used throughout.

## Exact source and plan

Plan: `experiments/v5-local-checks/aggregate-producer-controls-01-selection.json`,
SHA-256 `40a4d0082169575d028dbeeed637fd500e8053a735e98433078331c02bf713f9`.

| Selected source | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/aggregate_production/test_producer.py` | 22,939 | `c9026b00d1a97a31122b72e541d59a2f12952b3c71dc6f8ae77fca59eec7cc42` |
| `software/v5/aggregate_production/producer.py` | 44,253 | `796eb24619370a30192db6d0f63b914516919e7cae90aee32a1750736331b86b` |
| `software/v5/aggregate_production/__init__.py` | 152 | `0ca27c691b5afe5ad93086251afb3259491f2ebcaf6e2a9b7ff7b209d4489bb2` |
| `software/v5/production/producer.py` | 28,111 | `5555e944d7473731e3e9095e85c5c57ce89c5f59187f78c5b248b4c1227532f3` |
| `software/v5/production/__init__.py` | 164 | `c66f4ce32e6a929bf3d0a178fb9c62e6aaaebe45b441a98e4d2bc10b68d916ae` |
| `tools/Run-V5-Check.py` | 5,735 | `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651` |

All six current sources match; total 101,354 bytes. All 20 selected runtime/data
files, totaling 17,180,768 bytes, were independently hashed with zero mismatches.
They are the retained installed Python map and precisely two retained assembly
JSON inputs. The latter are `proof-memo-image-assembly-01/RESULT.json` (2,282 bytes,
`50de313fbc8f20b3f48d971f3183bf66f1079cafe18af460538b414d715a2f4e`) and
`selection.json` (23,126 bytes,
`60b1955f8b7f70b9238693ffb9c31018dc19a2089d6aec13b3238d2810f33600`).

The seven-element argv uses the pinned installed Python, `-I -S -B`, only the
selected test snapshot and fresh `{output}\evidence`. The exact finite limits
are 20 Job CPU seconds / 60 wall seconds / 512 MiB / two processes / 1 MiB per
stdout and stderr. The run directory was absent at exact-plan review.
`Select-AggregateControls01.ps1` only prepares this immutable selection; it
preserves the old runtime/limits and replaces the specific source/entrypoint,
adding the two exact data pins. No launch or prior campaign restart occurs in it.

## Control assessment

Exactly ten test methods exercise the actual aggregate pure/dispatch boundaries:

- Genuine retained `{snapshot}` and `{output}` argv reconstruction, with an
  omitted expansion refusing and literal `{root}` correctly left alone.
- Shared graph identity and minimum/maximum counts; finish still needs all
  segment checkpoints when its resolved frontier already exists.
- Aggregate 71-byte checkpoint framing and truncation/key/binding/legacy/finish
  refusals, without claiming SDK payload verification.
- Header and strict JSON types/duplicate keys/digest checks; exact ordered
  parent, capsule and dependency argv.
- A complete synthetic two-segment/one-assumption path through all five kinds:
  seven fake host calls, six reported fake prover stages, no admission.
- First-failure stopping and measured-versus-reserved charging when supervision
  fails or CPU accounting is missing.
- Worker/output reservation refusal before calls; each fake call checks that
  its exact reservation was saved first; retained finalization tail charges.
- Post-PASS request corruption causing a real finalization override and closed
  owner. Only newly generated synthetic data is deliberately corrupted.
- Complete same-allowance history, retained successful checkpoints, carry scope
  and fresh-owner omission refusal; valid continuation preserves prior costs.
- Ordered parent receipts and unchanged allowance budget as lineage bindings.

The fake fixture fills every accessed owner attribute and uses real file pinning,
request parsing, graph, checkpoint checks, reservations, history and finalization.
The synthetic header and checkpoint byte layouts match the intended structural
paths. The tests import no legacy test module and execute no fake host file.
Every fixture and fake-call record is retained. No concrete source/plan blocker
was found. The small finite envelope is reasonable, not a promised outcome.

## Scope and required outcome audit

Constructor/build-image adoption, complete snapshot adoption and the supervisor
are explicitly mocked. Synthetic stdout uses the product schema but its payloads
are labeled synthetic and never become admission handles. These controls cannot
establish real host behavior, receipts, cryptographic soundness, prover price,
hostile-input isolation or v5 readiness. A real constructor-adoption integration
remains distinct after the reviewed stage host is built.

For any executed outcome, inspect the outer terminal/closure/binding report,
exact six source snapshots and twenty data/runtime pins, ten unskipped controls,
retained fixture evidence and intentional override, before adopting a narrow
synthetic control result. Preserve a failure without automatic retry. No proof
allocation or actual producer run is authorized by this review.

## Actual saved outcome audit

Root executed the exact selection once in
`experiments/v5-local-checks/aggregate-producer-controls-01`. Independent
source/data-only inspection of the saved outcome finds **10 tests, zero
failures, zero errors, zero skips**, with matching named test stderr and inner
report. The outer process exited zero, was reaped, closed its Job, had zero
active/terminated processes, no requested termination and no cleanup errors.
Root separately reports the enclosing tool session terminal with exit zero.

| Evidence | SHA-256 |
|---|---|
| Outer `RESULT.json` | `de04c7c8909d1d816f25f6fa200de821f01580e98a96974ac39de3b360f1e311` |
| `evidence/CONTROL-RESULT.json` | `199c67fba3d1dabbbff3e6e5dd2c13e68310fa226ddec72310378639bef85464` |
| `evidence/FAKE-CALLS.json` | `8b8b9625434246c219d060c723afde6967195e088072a1eb1d4a15d1e65ef356` |

The saved selection is exactly `40a4d008...bf713f9`. All six original sources
and exactly six snapshot files still match; all twenty runtime/data pins match.
The four recorded loaded-module paths lie inside that selected snapshot and
match the selected package sources. Actual argv, workdir and limits are exact.

There are 182 retained evidence files and sixteen fake supervisor calls. Every
call's saved reservation matches its recorded argv and selected CPU reservation.
Of 134 distinct file-pin triples collected from fixture JSON, 133 match current
bytes. The sole mismatch is the deliberately appended whitespace in the new
`finalization/attempt-1/request.json`; its sole overriding marker records
`SYNTHETIC_PIN_CHANGED`. The saved apparent prefix PASS is therefore correctly
not usable as a successful continuation. No retained input was altered.

The complete fixture records seven calls, six checkpoints, a synthetic final
artifact and no mathematical admission. Nonzero exit charges measured one-unit
CPU; missing accounting and supervisor interruption retain four-unit reservations
and mark accounting unknown. Both unfunded fixtures make zero calls and retain
the finalization tail charge. The valid lineage's second attempt preserves two
prior worker units and four accumulated checkpoints. The omitted-history,
truncated-history and changed-parent/budget output directories do not exist.
These values are **synthetic dispatch assertions**, not actual proof CPU prices.

Actual measured enclosing cost is **1.3125 inclusive Job + 0.28125 wrapper =
1.59375 known CPU seconds**, with **3.1034299000166357 wall seconds** and
23,236,608-byte peak Job private commit. The wrapper's nested supervision CPU is
already included, not added again. The recorded observations retain normal
final-report/exit-tail limits; no zero-tail-cost claim follows.

Adopt the narrow ten-control outcome and preserve all used source, fixtures and
reports. No repeated controls are needed. There were no actual native host,
guest, build or cryptographic proof calls, and no constructor-adoption or full
v5 qualification follows. The separate one-link build and real retained-input
adoption remain the next relevant integration boundaries.
