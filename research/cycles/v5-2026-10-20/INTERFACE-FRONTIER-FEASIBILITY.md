# Interface frontier: bounded feasibility decision

**GO for one source-to-witness discriminator of the concrete method below;
NO-GO for another proof campaign or a rerun of the old child.** The smaller
method uses an existing genuine I parent and no new verifier image. It is a
new useful mathematical target, not a cheaper certification of the old target.
Interface-only does not itself make the old direct-I workload cheaper.

## Why the previous child cannot simply lose its bodies

The actual failed `receipt-source-integration-01` child is `fold_map_received`
(`4adbc049e4d1e29ec045d64c7dba9e27bdd506dfa6c7fb707f022be40439e742`).
Its saved input has 113,220 bytes, 1,355 rows, one parent, 11 parent groups,
11 bodies and one local theorem. Source export has 526 rows. Its leaf `rfl`
and node case genuinely require reduction of imported `map`/`fold`; presenting
these as opaque does not prove those conversion obligations. The body-only
closure cannot be discarded for this unchanged proof. Imported theorem proofs
were already absent. Snapshot failed at `33557665 >= 33554432` cycles;
there is no completed child capsule or receipt to reuse.

## Concrete substantive alternative: evaluator uniqueness

Fix the exact BASE I parent
`2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e`.
This is the same BASE used in the recent interface-only actual run. Its genuine
I receipt is `experiments/v5-local-checks/module-base-production-01/finish-0/receipt.bin`
(223,594 bytes; SHA-256 `850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47`).
Semantics/summary are in `experiments/v5-local-checks/receipt-prepare-01/prepared/base/bundle.json`.
Select only its group 0 (Tree, leaf, node, rec) and group 10 (binary_congr),
with the two committed recursor-rule bodies: these are actual original BASE
indices, not ordinal positions in the recent selected subset. For arbitrary A,B,
operations L:A→B and N:B→B→B, and evaluators h,k:Tree A→B, prove:

    (∀x, h(leaf x)=L x) ∧ (∀l r, h(node l r)=N(h l)(h r)),
    (∀x, k(leaf x)=L x) ∧ (∀l r, k(node l r)=N(k l)(k r))
    imply ∀t, h t = k t.

Implementation should use four separate equation premises, not conjunction
machinery. Tree.rec proves the leaf case by transitivity and symmetry; the
node case composes h's equation, binary_congr N on both induction hypotheses,
and the symmetric k equation. No funext, new axiom, fold/map unfolding or
new inductive type is needed. This is an extensional correctness/transport
method for different evaluators, not reflexivity or a renamed existing result.
Applications must establish their evaluator equations; the method does not
prove their computational cost or provide those premises for free.

Relative to the old selected imports, all nine ordinary-definition groups
and their nine bodies disappear; Tree's full types/recursor rules remain.
The new local theorem/proof size is not yet known, so a total witness-byte,
segment or runtime reduction cannot honestly be asserted. This narrower
context was already expressible in the pure-I API: it is not a new capability
caused by interface-only. The distinction avoids a false causal claim.

## Unchanged costs and exact route

The old adopted I image `9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e`
still requires the exact 413-row foundation, all selected descriptor/type/rule
checks, the new local proof, exact same-image/foundation/policy parent binding,
rank 1 and one genuine BASE receipt assumption. Its cost is not just JSON size.
The existing producer graph remains 3s+1 host calls for s segments/one parent;
the known BASE run took 110 segments and 126,105.625 worker CPU seconds in its
final attempt, excluding carried earlier work. This is context, not a floor
or prediction for the child. Fixed cryptographic calls do not vanish.

Use the current ordinary client: `admit_receipt` → `import_context` with its I
warrant, the two selected openings and two supplied bodies → `author` →
`admit_packet`. I semantics must be supplied; the receipt does not contain them.
The existing author emits the exact V2 native witness under the old I basis;
no new producer/client lane is needed. Then stop and compare selected closure
and total witness against the retained failure. This resolves local-proof-size
uncertainty, not certification affordability. The mixed packet is not an I
receipt; a later direct-I production handoff is a separate decision. Root must
separately select execution; no planner, guest, proof or checker change here.
No saved native descendant such as
project_summary is substituted for a genuine I parent. A changed I image also
cannot silently accept the old same-I parent. Full v5/growth remain open.

Source/evidence anchors: `software/v5/workloads/ReceivedFoldMap.lean`;
`experiments/v5-local-checks/receipt-source-integration-01/evidence/preparation/snapshot/child-input.json`;
`software/v5/client/workspace_atomic.py::{admit_receipt,author}`;
`software/v5/interface_views/workspace_evidence.py::{_context_data,import_context}`;
`software/v5/interface_views/authoring_atomic.py::MixedSourceOperation.finish`;
`software/v5/modules/receipt/src/{relation.rs,main.rs,policy.rs}`;
`COLD-CERTIFICATION-ROUTES.md`. Review used only saved files/source; no runtime.
