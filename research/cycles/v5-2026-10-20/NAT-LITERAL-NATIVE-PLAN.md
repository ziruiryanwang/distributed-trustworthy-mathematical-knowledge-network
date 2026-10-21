# One exact ordinary-source export and fresh relocated check

2026-10-20, core_growth. SOURCE-ONLY plan; no run, code, build or funding selected.
Root is `E:\Distributed Trustworthy Mathematical Knowledge Network`; paths below are relative to it.

## Fixed mathematical input

```lean
set_option autoImplicit false
namespace OwnerV5
def addTwo := fun n : Nat => Nat.add n 2
theorem addTwo_spec : forall n : Nat, addTwo n = Nat.succ (Nat.succ n) := fun n => rfl
end OwnerV5
```

Export both roots. The right-hand side uses NO numeral: fresh checking tests actual
two-successor reduction, not copies of one bad normalization. Retain source/SHA/rows/census.

## Smallest existing API path; no fabricated session or parent

Use `software/v5/authoring/test_native_frontend.py`'s `foundation_view` and
`request` helpers (source SHA `3f13702cea308fff9e0552c9465f1b00361fa3d8fda2824de9193c4cca90f547`).
Construct an explicitly UNTRUSTED frontend packet with the exact adopted foundation
view, `imports=[]`, and a domain-separated binding of this foundation/source/root
selection. This is test input, not an ImportSession, live handle or receipt.
The real frontend compares every foundation descriptor/value against pinned Init.
Do NOT invoke that helper's old controls/main or imported-tree fixture.
Reuse `authoring/worker.py` (`aeaad858...`) for its real frontend process and
same-call request/config/export bindings, under the retained outer supervisor.
After success, derive local_names from actual rows and require exact export census.
Use the selected Nat-lowering successor of `decode_source`, no external mappings;
validate its actual complete spec/bodies and exact original-to-lowered transcript.
Call existing `modules.receipt.witness.make_input(environment, foundation_rows,
image_words, parents=[])`. It emits the supported relocated rows, full local proof
bodies, rank zero and NO module assumptions. Require zero residual literal tags.
Invoke existing `native_delta.exe check IMAGE INPUT` once on that actual input.
This runs the unchanged relation, canonical/row correspondence and fresh native
type/proof checking. Require `CHECKED_CONDITIONAL_RELATION_NOT_ADMISSION`, exact
input hash/module/journal, `parents=[]`, rank zero and clean process termination.
Foundation remains the exact adopted fixed premise. No parent proof is invented;
no module receipt verification or cryptographic proof production is necessary.

## Exact retained bindings and finite supervision

Use `distribution-coherent-01-input.json` SHA `1903bb44...` as source of existing
runtime pins, not an installed rebuild. Frontend:
`experiments/v5-local-checks/author-lean-link-01/link/AuthorLean.exe`, SHA `1f73b8b0...`.
Checker: `experiments/v5-local-checks/delta-native-build-02/native_delta.exe`,
SHA `37a0af1b08e7176fb0d387b3e8439266d7c2c0befe5b08bc3cdd4c90c62d3e40`.
IMAGE is `9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e`
from the retained delta-author profile, NOT the aggregate image field.
Foundation: `experiments/v5-local-checks/receipt-prepare-01/prepared/foundation.json`
SHA `736792e5...`; use its exact foundation/policy IDs. Pin selected Python dependencies,
the lowering successor, new adapter, foundation, executables and actual Lean runtime
DLL/Init dependencies. Full hashes come from the retained map, never these prefixes.
Outer runner: `tools/Run-V5-Check.py` SHA `44a7bf1b...`, frozen v4 supervisor/Job.
Suggested one-shot ceiling: 60 CPU / 120 wall seconds, 512 MiB, four active processes,
bounded logs. Root must record final exact selection after source/control review.

## Stop and result boundary

Stop on first unexpected refusal/exhaustion; preserve all input/logs/charges, no retry/build. Record literal
occurrences, actual Nat/OfNat/add closure, canonical sizes and native checked roots.
Success is bounded source-lowering plus genuine fresh checking, NOT public SDK
admission, cross-module Nat interoperability, a growth benchmark or final v5.
