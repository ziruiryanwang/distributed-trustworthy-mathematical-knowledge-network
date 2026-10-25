# Asymmetric repair calculus: standalone mathematical handoff

Formal source: `TheoryA.lean`, namespace `RepairTheory`, Lean 4.34.0, importing
only `Init`. Status at this handoff: source reasoning complete, **not compiled**.
Any later compilation/admission status must be supplied separately with the exact
source revision. The module uses the modern `module` / `public import Init` /
`public section` header and exposes its definitions for downstream reduction.

## Idea and intended interpretation

A repair is an idempotent operation on a type. A state is fixed by a repair when
the operation leaves it unchanged. The directional relation `Follows r s` means
that running `s` preserves every state already fixed by `r`. Thus it certifies
the order “r, then s.” It does not assert that the operations commute.

This is a small synthesis of familiar retraction and invariant mathematics, not
a claim of literature novelty. The useful interface is directional composition
with an exact description of the resulting constraint, together with the clear
separation between settledness and canonical choice.

## Core interface

All of the following names are under `RepairTheory`.

| Name | Mathematical content |
| --- | --- |
| `Repair α` | Fields `apply : α → α` and `stable : ∀ x, apply (apply x) = apply x`. |
| `Fixed r x` | `r.apply x = x`. |
| `Follows r s` | `∀ x, Fixed r x → Fixed r (s.apply x)`. |
| `follows_iff r s` | Directional preservation is equivalent to `r(s(r(x))) = s(r(x))` for every x. |
| `merge r s h` | A repair applying r first and s second, for `h : Follows r s`. |
| `merge_settles r s h x` | The merged output is fixed by both r and s. |
| `merge_fixed_iff r s h x` | `Fixed (merge r s h) x ↔ Fixed r x ∧ Fixed s x`. |
| `follows_merge_iff r s t h` | t follows the compound repair iff it preserves the conjunction of the r and s constraints. |

The last equivalence quantifies only over jointly fixed inputs. Explicitly its
right-hand side is

```lean
∀ x, Fixed r x → Fixed s x →
  Fixed r (t.apply x) ∧ Fixed s (t.apply x)
```

This matters because a completed prefix can be treated through its joint fixed
states. Requiring t to preserve each earlier constraint on *all* individually
fixed inputs is sufficient but can be unnecessarily restrictive.

## Finite schedules

`run rs x` applies a list of repairs from left to right. `Settled rs x` is the
recursive conjunction saying every repair in the list fixes x. `Safe rs` says
each later repair preserves the fixed states of each earlier repair:

```lean
Safe [] = True
Safe (r :: rs) = ((∀ s, s ∈ rs → Follows r s) ∧ Safe rs)
```

The principal guarantees are:

- `run_preserves`: a sequence whose members all preserve one repair's fixed
  states also preserves that constraint, without needing `Safe` for the sequence.
- `run_of_settled`: any sequence leaves an already settled state unchanged,
  without a safety hypothesis.
- `run_settles`: a safe sequence settles all its constraints after one run.
- `run_fixed_iff`: for a safe sequence, `run rs x = x ↔ Settled rs x`.
- `run_stable`: a safe sequence is idempotent.
- `schedule rs h`: packages a safe sequence as an ordinary `Repair α`, so the
  same composition and fixed-point interface applies to that completed block.

The proofs are structural induction on lists and equality transport. The
composition proof uses preservation to remove the middle r from s(r(s(r(x)))),
then uses idempotence of s. No order, metric, finiteness of α, decidable equality,
choice principle, or convergence assumption is required for the generic theory.

## Models and established limitations

`choose b : Repair (Option Bool)` fixes both `some false` and `some true`, and
sends `none` to `some b`. `choose_follows a b` proves compatibility for every pair
of choices. Nevertheless `choice_order_matters` proves that running false then
true from `none` differs from running true then false. Mutual preservation and
the same final fixed-point set do not determine a unique repaired output.

On Boolean pairs, `zeroLeft` sets the first component to false, `zeroRight` sets
the second to false, and `copyRight` copies the second component into both fields.
`zeroRight_follows_zeroLeft` makes their ordered merge available.
`copyRight_follows_joint` proves that copying preserves the joint constraint
after both components have been zeroed. In contrast,
`copyRight_does_not_follow_zeroLeft` uses `(false,true)` to refute preservation
of the first-component constraint alone. This is a concrete strictness witness
for the compound interface's weaker preservation requirement.

`Safe` is a sufficient list discipline, not a characterization of every sequence
whose final output is settled. An intermediate violation can be repaired later.
The results assert neither termination of arbitrary repeated incompatible repairs
nor canonical outputs, optimal repair cost, completeness of a constraint system,
or the existence of repairs for arbitrary predicates. Repairs and preservation
proofs are supplied data. Infinite schedules are outside the module.

## Portability boundary

Ordinary structures, recursive definitions on lists, equality proofs, and simple
finite models are used. Structure/recursor generation and list recursion may
exercise more frontend machinery than a theorem-only package. Definitions are
`@[expose]` to make modern-module downstream reduction intentional. No `sorry`,
new axiom, unsafe declaration, executable plugin, or external command is used.
Kernel compilation, reconstruction/admission, dependency-closure size, and actual
recipient usability are still unobserved at this source-only checkpoint. A source
reader may inspect and use the exact module without this author's private record.
