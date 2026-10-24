# Mixed ordinary modules with exact installed-theorem reuse

2026-10-23. **Source-only successor; not compiled, executed, installed or adopted.**
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Root's [selection](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-INSTALLED-THEOREM-SELECTION.md)
and the [independent theoretical review](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-THEOREM-INTERFACE-REVIEW.md)
govern this narrow change. The current distribution remains on module03.

## Useful change

A new commons theorem may depend on an ordinary installed theorem such as
`Nat.add_zero`. The old module bridge refused every existing-name collision.
This successor can interpret that already installed name by the **exact full
theorem independently warranted in the selected local context**, while writing
and checking only the actually new module declarations.

This is not trusting a remote native module, accepting a public axiom as proof,
enlarging the foundation or discovering theorem identity from its statement.
The complete selected evidence and all proof-only dependencies are still
collected through the unchanged `module_closure.py`. First export still pays
for that selected closure. No provenance subsystem or proof-equivalence engine
is introduced.

## Three successor files

| File | Boundary changed |
|---|---|
| `OrdinaryModule.lean` | Classify exact installed singleton theorem matches; check new units privately and publicly; write only additions; reread both categories. |
| `module_worker.py` | Preserve the three sequential phases and exact byte binding, with V2 pending/final report fields. |
| `module_export.py` | New policy/cache identity; exact report partition validation; expose matched versus checked counts in `MODULE.json`. |

The callable export signature, native phase argv and full V1 request shape stay
unchanged. The new policy is
`DMKN_ORDINARY_INIT_EXACT_THEOREM_MATCH_PUBLIC_MODULE_V2`. Success is
`CHECKED_LOCAL_MODULE_WITH_EXACT_INSTALLED_THEOREM_RELATION`, not a claim that
the emitted module repeats every installed proof body. Pending/final report
schemas are `DMKN_ORDINARY_MODULE_PENDING_V2` and
`DMKN_ORDINARY_MODULE_OUTPUT_V2` respectively.

## Acceptance and compatibility relation

The unchanged decoder sees only the exact fixed basis and earlier selected
outputs. For each decoded unit, inspect final actual private Init records:

1. If no advertised output exists, put the complete unit in the added batch.
2. If any advertised output exists, require a theorem descriptor, exactly one
   output equal to the descriptor name, and `all = [name]`. Require the descriptor
   to encode exactly the selected theorem inventory, then require the actual
   private record to equal that full inventory. Check the actual key/name and
   existing safety restrictions. Every other collision refuses.
3. Check the full added batch with unchanged `CheckedExtension.checkBatch` in
   private Init; expose additions through the existing mechanism and verify
   the complete selected inventory.
4. In actual exported Init, each matched theorem must be the exact full theorem
   or a safe axiom-shaped handle with exactly its original name, ordered universe
   parameters and encoded type. The private full theorem supplies the proof;
   the public handle supplies only its usable interface.
5. Check the added batch again in that actual public environment, using the same
   unchanged checker. This check is mandatory: proof-body erasure can break
   conversion, including uses involving `Acc.rec`. Proof irrelevance is not
   permission to ignore such a failure.
6. Write only additions. Separate fresh-process private and exported rereads
   check the exact own-module census, additions and respective matched relation.
   The worker promotes the V2 pending report only after both succeed; the
   controller independently checks its request binding, partition and artifacts.

The ordered matching indices partition the original request, not an arbitrary
new list of assertions. Both matched/added names and inventories are projected
from the exact selected units. `units_checked` counts only additions (checked in
each of two passes); `units_matched` counts existing theorem matches. Matched
units are never reported as newly kernel-checked.

The substitution argument is conditional on the original local warrants,
complete exact dependency interpretation, foundation and selected kernel/codecs.
An installed `axiom False` without a separately warranted full theorem fails
those premises. Same-spelled but different computational dependencies fail
the unchanged evidence/dependency relation. Same statement with a different
private proof conservatively refuses; that is not a claim the other proof is false.

## Deliberate refusals and unchanged limitations

- Existing definitions, opaque declarations and generated/mutual groups still
  refuse. Only a genuinely singleton theorem may take the matching branch.
- Public absence, wrong kind, safety flag, universe/type mismatch, changed proof
  for a full public theorem, and public conversion failure refuse.
- If no units would be added, native construction emits
  `NO_NEW_MODULE_DECLARATIONS` before writing artifacts. No empty module or
  success manifest is manufactured. The controller retains its normal failed
  operation record and native diagnostic; an all-installed resolution API is
  not implemented. This outcome does not assert public compatibility or invalidity.
- No source notation/attributes, executable IR semantics, general Mathlib support,
  ancestry-independent cold cost, network availability or useful-growth advantage
  is established by this source change.

## Pending validation

Independent source review precedes any root-selected execution. The saved mixed
`Nat.add_zero`/new-theorem closure is the changed-boundary positive discriminator;
it needs actual ordinary consumer use after both rereads. Focused refusals should
cover full private proof mismatch, wrong public signature, non-singleton metadata,
computational/group collision, all-matched output, tampered report partition and
failure before final adoption. Existing unmodified campaigns must not be rerun.

No Python import, Lean run, compilation, test, package/owner mutation or Git
operation was performed while authoring this source. Existing used sources and
evidence remain unchanged. This checkpoint is implementation for review, not a
runtime or release result.
