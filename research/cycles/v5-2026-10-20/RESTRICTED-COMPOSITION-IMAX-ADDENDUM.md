# RC0 refinement correction: preserve native imax structure

2026-10-21. Root authorized this unused-source correction before selecting a
build. It supplements CORE-PLAN and REFINEMENT; no test or certificate is claimed.

## Exact original behavior

`modules/native/checker/src/util.rs::imax` interns `Level::IMax(l,r)` unchanged.
Its `succ`, `mk_sort` and expression interning likewise preserve structure.
Thus eager RC reduction of `imax(l,0)` to zero does not, by itself, justify
original native pointer identity for an arbitrary enclosing expression.

`level.rs::simplify` does implement right-zero imax reduction, recursively.
`leq` simplifies its two inputs before `leq_core`; `eq_antisymm` is the conjunction
of the two order tests. `is_zero(l)` calls `leq(l,0)`. Independently,
`tc.rs::def_eq_quick_check` invokes `def_eq_sort` before binder comparison, and
`def_eq_sort(Sort(l),Sort(r))` calls `eq_antisymm(l,r)`.

## Selected conservative algorithm

RC now interns raw imax nodes everywhere, including universe substitution.
Its bounded predicate Z is:

```text
Z(Zero) = true
Z(IMax(a,b)) = Z(b)
Z(Param(_)) = Z(Succ(_)) = false
```

Each visited node charges the existing monotone work budget and depth limit.
By induction on the inspected right spine, `Z(l)` implies original
`simplify(l)=Zero`: the base is immediate, and for an imax whose right side
simplifies to zero, every applicable original simplify branch returns zero.
Consequently `Z(l)` implies original `is_zero(l)`; and `Z(l) && Z(r)` implies
original `eq_antisymm(l,r)` because both simplified inputs are zero.

The comparator now admits exactly three routes:

1. Complete internal structural identity, retaining raw universe and binder
   metadata, hence the constructive original term interning correspondence.
2. Both nodes are actually root Sorts and their levels both satisfy Z. This
   follows the original explicit `def_eq_sort` quick branch.
3. Both nodes are actually root Pis or both root Lambdas. Compare domains,
   open both bodies using the same fresh local and recurse, as before.

Z is also used to require a new theorem's inferred sort to be Prop. It does not
rewrite the type, alter a constant signature, or equate expressions underneath
applications. In particular, an imax/zero mismatch hidden inside an application
cannot pass by RC's exact interning, even though a more general Lean conversion
could establish it. Refusing such additional valid terms is intentional.

This removes the need for a subtle invariant about where generated Sorts can
flow. Public levels remain zero/parameter only; there is no general universe
solver, application congruence, beta/delta fallback or mathematical-policy change.

Corrected `typing.rs` SHA-256:
`3376e13a48ad3caefdd7dff3c8604915eae0921cad95d04aa0f81407de29cc08`.
The independent control author has been notified of the root-Sort positive and
nested-application refusal boundary. Root owns any later build/execution.
