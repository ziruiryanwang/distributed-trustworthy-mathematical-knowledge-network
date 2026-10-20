# Cold certification: source assurance and the next efficient import boundary

Independent source-only challenge by `core_release`, 2026-10-20. No code,
runtime, proof, installation, memory investigation or Git change was made.
Full v5 remains unfinished. This is neither a new security audit nor a claim
that a bounded reviewed path establishes worldwide mathematical soundness.

## Decision

**Select explicit type-only, untrusted frontend imports as the next local-PC
implementation, retaining the unchanged independent mathematical checker.**
Root and `core_growth` independently identified the exact eager-body obstacle;
this note supplies the assurance challenge, not a competing implementation.

No new acceptance bypass was established in this inspection. The highest-payoff
concrete issue is that the frontend demands a definition's entire body closure
even when the proposed proof only needs its type. This contradicts the desired
demand-local usage cost, despite the native representation already supporting
an exact imported definition with a missing body. A small frontend mode can
remove that cost without changing what mathematics is accepted.

## Exact inspected authority path

Logical Python paths were resolved using `sdk_sources` in
`experiments/v5-local-checks/distribution-connected-01-input.json`, rather than
assuming the similarly named historical files were current.

| Boundary | Current source and observation |
|---|---|
| Exact I/A ownership | `software/v5/client/runtime.py:181` constructs the original receipt/aggregate/native owners from the adopted profile; there is no remote success-flag constructor. |
| Receipt-backed aggregate member | `software/v5/aggregate_claims/aggregate_admission.py:169` verifies the selected exact header in the same call; `aggregate_claims/bindings.py:106` independently binds the exact member journal and index/path. |
| Mixed mathematical extension | `software/v5/runtime_efficient/mixed_claims/receiver.py:253` verifies or revalidates original claim handles; `:269` installs exact authenticated frontier journals; `:280` checks every new witness and exact parents; `:302` checks target summary and live frontiers before promotion. |
| Conditional module semantics | `software/v5/modules/receipt/src/relation.rs:43` binds each parent to the exact image/foundation/policy and module opening; `:61` requires strict exact parent rank; `:77` establishes descriptor/native correspondence; `:112` checks every local declaration under those explicit premises. |
| No arbitrary theorem erasure | `software/v5/modules/native/checker/src/tc.rs:195` requires every newly checked theorem to inhabit Prop. Imported sealed proofs are not a general license to erase computational definitions. |

The inspected `module.rs`, `tc.rs` and module `relation.rs` hashes respectively
match the retained guest-build-05 selection:
`6c9b6acbf0cae9698b9fa035bad38df8c1e307dd1e78d6971b27f58511c58455`,
`f1b5f2e15f231aea52ae3452435c2b91a69a6baf8c010f68214b3e0cf57fa52b`,
`3625bc9c7708e5a03580e1e61bc7019f5b7cf6ad48ee37f6d749919d245e2eb8`.
This identity check does not independently rebuild or prove the image.

The previous `v5-2026-10-07/ASSURANCE.md:95` already identifies the necessary
adaptive, branching recursive-soundness assumption. Finite rank descent proves
semantic induction only after grounded cryptographic closure is established.
The I relation consumes exact lower-rank I journals. The A relation retains
separate seal-height descent for A assumptions and exact mathematical rank for
new module deltas (`aggregate_claims/relation.rs:66`, `:131`, `:153`). These are
different measures, not permission to treat a cyclic receipt claim as a base
case. Hash commitments and a successful native transcript alone are not that
grounding. No new numerical cryptographic error bound follows from this review.

## Concrete body-closure obstacle

`software/v5/runtime_efficient/mixed_claims/imports_atomic.py:677` visits every
selected declaration type, then `:681-692` requires every transparent
definition's body and recursively visits its references. A body can pull in
another declaration whose body causes the same requirement. Thus a use of
`d_n : Nat` can traverse `d_n := d_(n-1)` through an arbitrarily long selected
semantic chain even when the agent only wants `Eq.refl d_n`.

The corresponding frontend genuinely enforces this eager representation:
`software/v5/authoring/native02/AuthorLean.lean:763` reads and installs the body
as a Lean definition, and `:699` compares that body and reducibility hint.
Simply omitting bodies in the Python context is therefore not an implementation.

In contrast, `software/v5/modules/native_rows.py:174-183` already emits
`moduleImportDef` with the exact committed body hash and original hint when an
imported body is absent. The exact descriptor kind is retained. Native
`env.rs:359` demands a definition value when unfolding actually needs one;
it does not interpret a missing definition as a mathematical axiom or a new
opaque constant. This is the decisive existing alternative to redesigning the
mathematical relation or producing another receipt.

## Why untrusted abstraction preserves the acceptance boundary

Let `V` denote the unchanged independent acceptance procedure, including
receipt premises, reconstructed exact declarations and the local native check.
Let `R(C,e)` reconstruct a witness from certified imports `C` and arbitrary
frontend output `e`. A new frontend generator `G` may use abstract placeholders.
The proposed path is still:

```text
e := G(type-only frontend context, local source)
w := R(exact certified imports, e)
accept only if V(w, exact authenticated premises) accepts
```

For every output of any such `G`, acceptance remains acceptance by `V` on an
ordinary reconstructed witness. Therefore changing `G` does not enlarge the
language accepted by `V`, provided `R` and `V` retain their existing contracts.
This argument does not require trusting the generator, proving frontend
equivalence, or asserting that its abstract environment models full Lean
definition reduction. The new mode changes proposal completeness and cost,
not mathematical authority.

Required invariants:

- The frontend-only placeholder has the exact authenticated name, universe
  arity and type, and is allowed only for an explicitly selected imported
  definition. Foundation records and local declaration policy are unchanged.
- The final witness restores the **definition** kind, body commitment and
  reducibility hint from authenticated descriptors, not from placeholder rows.
- New local axioms remain rejected. The exporter currently rejects nonboundary
  axioms at `AuthorLean.lean:274`; `modules/source_rows.py:254` separately
  forbids local axioms/quotients. Neither check should be weakened.
- Final correspondence, native checking, parent verification and accounting
  remain mandatory. Frontend success continues to mean untrusted data only.
- Inductive groups and recursor-rule bodies remain on their existing checked
  path. No initial shortcut for recursor or positivity metadata is justified.

## Practical limitations and discriminating controls

Abstraction is incomplete. If a hidden definition is a function-type alias,
the frontend may be unable to recognize an application. If a hidden type
constructor occurs in a new inductive declaration, frontend positivity may
fail even where the original transparent definition would establish positivity.
Such refusals do not violate soundness. Keep the eager mode available; do not
claim equal frontend expressiveness or universal savings.

`mixed_claims/authoring_atomic.py:273-288` returns an **untrusted** mixed packet;
it does not yet admit the new theorem. The final native call occurs at
`runtime_efficient/mixed_claims/receiver.py:280-300`. A missing demanded body
there currently fails and revokes the operation (`:313`), rather than returning
a resumable structural demand. Do not silently advertise a same-operation
native-demand retry. Such a retry is a separate state-machine change, not a
prerequisite for an honest first type-only mode.

One positive control should retain a certified `d : T`, omit its unneeded body
and private body-only dependencies, author a genuinely type-only result, then
pass the existing native reconstruction/check. One negative control should
require a computational conversion and demonstrate refusal without a body.
Pure controls should additionally reject forged placeholder names/types,
attempted local axioms and a relabeled definition/opaque kind. No proof
production is needed to decide whether this representation change works.

## Existing high-severity assurance debt, not another new mechanism

The construction-specific recursive trust case and checker-to-Lean assurance
remain open; existing reports already record them. There is also still no live
local revocation gate in the installed owner path:
`runtime_efficient/admission/verifier.py:117` checks only closed/deadline state.
The 10/12 `NEXT-AGGREGATE-COST-DECISION.md:480` appendix already designs the guard,
so repeating it is not a new finding.

A future coherent implementation should start at the actual `RuntimeProfile`
factory and the receipt base owner, not at an unused helper: Aggregate calls
`ReceiptVerifier._active` (`aggregate_admission.py:103`), mixed owners call their
original receipt/aggregate owners (`runtime_efficient/mixed_claims/receiver.py:132`),
and import sessions repeat those gates (`imports_atomic.py:114`). A fresh base
owner, aggregate constructor forwarding, factory and bounded policy guard can
carry a conservative whole-installation support closure without copying every
downstream module. Source/image/parameter support metadata must be reviewed and
bound at adoption; unknown metadata must refuse. This remains real release debt,
but the presently selected body-closure correction has greater immediate payoff
for the user's two central scale/growth goals.
