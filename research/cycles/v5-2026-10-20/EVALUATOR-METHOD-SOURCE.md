# Evaluator uniqueness: source checkpoint

Source-only implementation selected by root following
[frontier feasibility](INTERFACE-FRONTIER-FEASIBILITY.md). The active installed
map was inspected in
`product-local/v5-distribution-interface-01/Mathematical Commons v5/V5-RELEASE.json`
(release `c249d086`). Implementation uses that SDK, not superseded logical-path
source. No runtime, imports, Lean/native/guest/prover, tests, builds, RAM inquiry
or Git mutation was performed by this author.

## Review inputs

| Fresh source | SHA-256 |
|---|---|
| `software/v5/workloads/EvaluatorUniqueness.lean` | `e9beebfd492cfe3a809ee02fd1d010ca043ea33814161b580c5d62d97fcbb686` |
| `software/v5/evaluator_method/actual.py` | `0d8c2d0d93f01f14f72f684c0cda3c36dd571a56d4f1371b1fcdc9b3fb5f9a15` |

The mathematical source received core_growth's independent source-level PASS;
see [method theory](EVALUATOR-METHOD-THEORY.md). Adapter/selector review is
separate and pending. No compilation or mathematical acceptance is claimed yet.

## Exact method and route

For arbitrary `A`, `B`, `L : A -> B`, `N : B -> B -> B` and distinct arbitrary
`h k : Tree A -> B`, four explicit premises describe their leaf/node equations.
`OwnerV5.evaluator_unique` concludes `h t = k t` for every tree `t`.
The proof uses the certified Tree recursor, leaf equality transitivity/symmetry,
and the parent's `binary_congr` in the node induction. It adds no axiom or
definition, performs no fold/map unfolding, and uses no function extensionality.

The only parent is genuine BASE I receipt `850c33b2`, not the earlier native
projection descendant. The two semantic openings are original indices **0 and
10**, totaling five declarations, plus two recursor-rule bodies. Default eager
mode suffices because no ordinary definition is imported. This narrower
selection is not credited as a new capability caused by interface-only mode.

The adapter uses the existing public route:

1. Real `RuntimeProfile` and validated workspace/authoring operation.
2. `admit_receipt` on the exact genuine BASE bytes; obtain its live journal.
3. `import_context` with those two groups and two rule bodies.
4. `author` once on the exact reviewed Lean source.
5. `workspace.packets.put`, then `client.admit_local`, then inspect the fresh
   admitted result. No public `admit_packet` method exists in this SDK.

No publication, certification production, snapshot, guest execution, network
request, implicit retry, new API/client lane or allowance renewal is selected.

## Binding and accounting

The owner pins original receipt, semantics bundle, Lean source and the retained
old child witness. Saved historical bundle acceptance fields are not authority.
Post-call inspection binds source request, actual frontend export/worker report,
prepared packet and actual native-admitted module. It checks the original I
journal, original group openings, exactly two rule bodies, same I image/rank1,
one local theorem with two universes, eleven outer binders and the distinct
`h t = k t` conclusion. The actual proof must use Tree.rec and binary_congr once.

Inspection saves exact canonical `method-witness.json` and reports total bytes,
rows, parent groups, bodies and local declarations against the pinned retained
fold-map witness. **These are different targets and contexts:** the comparison
does not prove a controlled speedup or affordable cryptographic certification.
The packet and witness are not a newly generated I receipt.

The exact current route makes two I verification attempts: initial receipt
admission and the same claim checked inside mixed packet admission. It also
makes one native delta attempt and one authoring attempt. Root's selector
reserves 10 + (10 + 10) + 45 = 75 worker CPU seconds; no cache hit is assumed.
Import limits are one source/member/receipt; packet limits one delta/edge.
Both real client and workspace close even after failure; cleanup, cancellation
and original deadline failures remain visible. Reports remain inert evidence.

Root's `Select-EvaluatorMethod.ps1` matches the adapter parameters and input pins.
The executable decision remains root's after independent source review.
