# Evaluator uniqueness: constructive method and exact use boundary

Source-only mathematical review. No compilation, native check, guest execution,
proof production, RAM inspection or new campaign is authorized by this note.

## Precise theorem

The following signature uses the actual certified BASE namespace. `open` changes
name resolution only; it introduces no mathematical declaration or trusted alias.

```lean
set_option autoImplicit false
noncomputable section
universe u v
open DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5
namespace OwnerV5
theorem evaluator_unique {A : Type u} {B : Type v}
    (leaf : A → B) (node : B → B → B) (h k : Tree A → B)
    (h_leaf : ∀ x, h (Tree.leaf x) = leaf x)
    (h_node : ∀ l r, h (Tree.node l r) = node (h l) (h r))
    (k_leaf : ∀ x, k (Tree.leaf x) = leaf x)
    (k_node : ∀ l r, k (Tree.node l r) = node (k l) (k r))
    (t : Tree A) : h t = k t := by
  induction t using Tree.rec with
  | leaf x => exact Eq.trans (h_leaf x) (Eq.symm (k_leaf x))
  | node l r ihl ihr =>
    exact Eq.trans (h_node l r)
      (Eq.trans (binary_congr node ihl ihr) (Eq.symm (k_node l r)))
end OwnerV5
```

This is a source proposal, not a compilation claim. Equality is pointwise:
the conclusion does not require function extensionality. Universes u,v are
independent; there is no equality assumption between h and k, decidable equality,
termination axiom, inhabitance assumption, or algebraic law on `node`.

## Proof and nonvacuity

The exact Tree recursor reduces the obligation to its two constructors. At a
leaf, both evaluators equal the specified leaf interpretation. At a node, the
induction hypotheses give equality on each immediate subtree; imported
`binary_congr` transports both equalities through the common binary operation.
Transitivity and symmetry close the result. Finite structural induction proves
the result for every Tree, not only fixtures or one constructor.

The premises are satisfiable for every A,B,leaf,node: the existing mathematical
fold is an evaluator satisfying both computation equations. When A is inhabited,
trees with arbitrary finite branching exist, so the result is not restricted to
an empty domain. No universal inhabitedness is needed for validity. Setting h=k
is allowed, but does not justify the general theorem: arbitrary distinct source
implementations with the same equations are also covered. Their equation proofs
are real application obligations, not ignored assumptions or new axioms.

## Useful downstream instance: fold fusion

Let f:B→C preserve leaf and node operations between two algebras:
`f(leafB x)=leafC x` and
`f(nodeB b1 b2)=nodeC(f b1)(f b2)`. Instantiate the theorem with
`h(t)=f(fold leafB nodeB t)` and `k(t)=fold leafC nodeC t`.
Fold's computation equations and the two preservation laws discharge the four
premises, yielding `f(fold leafB nodeB t)=fold leafC nodeC t` for every t.
Thus the method transports interpretations without repeating structural
induction. It also applies to a separately proved alternative evaluator; no
claim is made that an arbitrary optimized evaluator satisfies these equations.

This is a factoring of reusable reasoning, not free access to opaque semantics.
An application using fold must obtain its required bodies or certified equation
lemmas and discharge the stated premises. The method alone neither certifies
those equations nor proves reduced computation of the evaluator.

## Exact existing route and what would count as evidence

The sole parent is genuine I module
`2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e`, rank zero.
Its receipt is `experiments/v5-local-checks/module-base-production-01/finish-0/receipt.bin`
(SHA-256 `850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47`).
Supply original group 0 (Tree/leaf/node/rec), group 10 (binary_congr), and the
two committed recursor bodies from `receipt-prepare-01/prepared/base/bundle.json`.
The existing ordinary route is `admit_receipt` → `import_context` → `author`,
then public `workspace.packets.put` → `client.admit_local`. The prior feasibility
note's `admit_packet` label was imprecise: `_admit_packet` is private, not a
public client method. The result must bind exactly this I premise at rank 1.
No new producer lane or changed checker is needed to obtain/check the witness.

Expected structural advantage: omit all nine definition groups/bodies used by
the old fold-map child. Mandatory foundation rows, recursor semantics, local
proof checking and cryptographic assumptions remain. Actual total witness size
is an execution question. A native witness is not a new I receipt; neither its
size nor a successful theorem proves cheap certification, workload benefit,
exponential growth, broad Lean coverage or final v5 readiness. A future growth
claim must credit saved downstream induction while charging equation proofs,
discovery, checking, certification and service under its stated comparator.

## Independent source inspection

`software/v5/workloads/EvaluatorUniqueness.lean`, SHA-256
`e9beebfd492cfe3a809ee02fd1d010ca043ea33814161b580c5d62d97fcbb686`,
implements precisely the displayed theorem with fully qualified BASE names
(instead of `open`) and names L,N for leaf,node. PASS source-level mathematical
review: two universes, all four laws, arbitrary h/k/t, exact Tree.rec and genuine
binary_congr use; no definition unfolding, axiom or extensionality shortcut.
The selected two groups contain five declarations, not the recent six-declaration
interface test. Default eager mode suffices; no ordinary definition is imported.
Compilation/native acceptance and adapter integrity remain separate evidence.
