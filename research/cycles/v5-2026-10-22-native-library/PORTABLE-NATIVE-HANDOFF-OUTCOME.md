# Portable parent to new native extension: independent outcome

2026-10-23. Reviewer: `admission_event_audit`. **PASS for one actual native
alias check above the imported local parent.** This establishes compatibility
of the retained snapshot/module names with the V2 local admission path. An alias
is neither novel mathematics nor a useful-growth, discovery or release result.

Run: `experiments/v5-local-checks/ordinary-portable-extension-01`.
Selection: `50fff86a153be77f63350b6018d2f2f94b6e473567bb953172519ec33fe0ed49`.
Parent manifest: adjacent `ordinary-portable-extension-01-parent.json`, SHA-256
`75530a5541b99dfa2e448a8acfe3bdf42e7578b9e291e2fbbd81e047b536688e`.

## Exact saved evidence

Paths below are relative to the run; `p/` abbreviates `portable-extension/`.

| Artifact | SHA-256 |
|---|---|
| `RESULT.json` | `4a05e1df5782a3c24088da6b5adeddf060e16d452596c9871db4afacaaef9aa9` |
| `p/EXTENSION-RESULT.json` | `5c9a28dc499d3d6485c4c43184acd23f55a69cd8cf82c4aa62c7c05f9d226cab` |
| `p/evidence.json` | `4335a7b8f10daddd72eee1b6c30b613afe8d9e1e96c394ab7cd39e235b0ef369` |
| `p/call/units.json` | `bd276e7ee754e21576268d5bc326c551e33e208e3d535e143d60f1a2c265bb03` |
| `p/call/plan.json` | `79175bd474e6d51d4b066d6dc115fb0969bf33da51ed702beb32ec83e7f2ab32` |
| `p/call/SUPERVISION.json` | `b7fc041402c0b9acc8574a762615ddd41df11b1733032b36831e140caf667d15` |
| `p/call/worker-report.json` | `6ca1391eb08773c7f9b6ebbe72f34d5ebe47c4bc3b70852bed6c6c3ee8111327` |
| New 9,080-byte native artifact | `26852b1fe567ef31f83c355d0818be8c8a7d5b1294c60910e3343b0d8da2d4be` |
| Original imported database | `2feb73516d3dcfec985ee49d7cbdca01da57619df186fce4b318d5ac5ba1216e` |
| Private extended database | `b04745de7ee0dc9bad89fa05dc64cd75d5729d21a16fe956abf90639b03f5bd3` |

Parent root:
`324c8a9688a0fea60631553221f483fb1ef25ccd7d1025de493513eb05c22a4d`.
New root:
`c03d2e54af10ff86837a233b0ab1d191a799c1ca86eff1014fc74f89990c9ee1`.
New UnitID:
`c6d19a249736fe883e2a54c989cd08a8d4b582bdee2034db4f6f15f64eee78bf`.
New alias ExportID:
`5e7022e9bd0b65f148956acd8607542153136993b68fefa6e99c462bc6efa2c8`.

## Actual checks

All eight snapshotted source pins and 38 runtime/input pins match. All 2,874
selected original parent files still match the prospectively selected lengths
and hashes. The private copy retains the same non-database file bytes. Both
databases were opened only with `mode=ro&immutable=1`; their hashes are identical
before and after this review. No importer, checker, copy, product catalog reopen
or test was rerun, and no old proof-DAG parsing campaign was performed.

The private database has exactly six roots. Its five earlier root records,
import row and activation/meta row equal the original imported database exactly.
One operation is `COMMITTED`, with the new root and 9,080 artifact bytes. Its
root record has `origin=native-check`, the exact implementation/operation IDs,
singleton input UnitID and a singleton new alias binding. Its record hash equals
`e76e4792a415f18ce177add7dba246868c63c4d1617687c0bf95cc44cb4d2597`.

The 14,634-byte evidence produces exactly
`DMKN.ReadFootprint.Portable.snapshot_predicate_applyBatches_alias01`, using
the previously accepted
`DMKN.ReadFootprint.Consumer.snapshot_predicate_applyBatches`.
The review independently reconstructed its UnitID, alias ExportID and batch
request hash. The target's universe parameters and type are unchanged. The proof
is exactly one target-constant node instantiated at those universe parameters.
All 20 explicit imports resolve to the original 3,629 protected parent bindings;
the alias name was absent from that map. The actual worker input file is exactly
the canonical singleton list containing this complete unit, not the old units.

The actual worker plan names exactly the five retained snapshots, with their
saved module names, parent modules, sizes and name counts. The new child imports
the original last module name (`DMKNLocal.r98e65adc...`), not a module name
invented from the translated parent handle. Saved argv binds this exact plan,
singleton units file, new root, output artifact and worker report. The actual
worker report agrees on the new module, original parent module, sole alias,
one checked unit and artifact size; the artifact's actual hash matches the
committed record. The resulting map contains precisely 3,630 names.

The exact reviewed controller commits only after its clean actual worker event,
then closes and reopens the private catalog and compares the complete resulting
context. The successful saved result is downstream of that comparison. The
reviewer inspected the persisted commitment read-only rather than manufacturing
a second actual event or trusting an arbitrary peer PASS file.

## Terminal closure and costs

Outer and nested worker supervision both report exit 0, clean Job closure,
direct child reaped, no cleanup error, no termination request, and final active 0
and terminated 0. Both native stdout/stderr files are empty. Outer stderr is
empty and outer stdout is 2,709 bytes. No operation remains live in this evidence.

Outer Job CPU is 37.5 seconds; outer wrapper CPU is 0.703125 seconds. Thus known
inclusive CPU is **38.203125 seconds**, with outer wall **54.800297 seconds** and
peak Job private commit 686,309,376 bytes. Nested worker Job CPU is **2.53125
seconds**, already included in the outer figure, not an additive cost. The
controller reports 34.828125 CPU seconds; this development harness includes
private catalog copying, retained-file/support checks and outcome bookkeeping.

These numbers do not measure the marginal cost of a normal contribution to an
already open owner catalog, nor prove scalable cold loading. Do not repeat or
optimize this compatibility experiment merely to polish its benchmark. The next
high-payoff boundary is the ordinary public discovery/acquisition/admission loop,
with durable republishable evidence and explicit missing-import handling.
