# Independent finite-map effect review

Disposition: **mathematical argument passes; source correction recorded; actual
elaboration, export and admission remain unperformed**. No rich parent is
accepted after the actual intake failure, so commons contribution remains held.
This review did not run Lean, tests, owner/native operations, databases or Git.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`;
checkpoint: `research/cycles/v5-2026-10-26-local-discovery/CHECKPOINT.md`.

## Mathematical challenge

The equivalence is valid for the specified finite, total, write-only language
whose two nondeterministic branches are always available. Let `N(m)` mean
`m.isEmpty = false`, and `W(p)` be the Boolean summary. Three constructive
statements give the result:

1. `Exec p m n` and `N(m)` imply `N(n)`, by execution induction. Insert uses
   exactly the acquired `Std.HashMap.isEmpty_insert`; sequence composes the
   invariant and choice selects an already covered branch.
2. `Exec p m n` and `W(p)=true` imply `N(n)`. In sequence, a true left summary
   establishes nonemptiness and the right execution preserves it; a true right
   summary forces it directly. In choice, Boolean AND requires either chosen
   branch's summary to be true.
3. `W(p)=false` supplies `Exec p m m` for every `m`. False OR gives both identity
   witnesses for sequence; false AND gives one identity branch for choice.

Thus `N(m) ∨ W(p)=true` suffices for every result. Conversely, if every result
is nonempty, split `W(p)`: true establishes the right disjunct; false applies the
universal premise to the identity witness and establishes `N(m)`. This is not
a vacuous universal argument and uses no classical choice or map extensionality.

The positive example's summary reduces to true. The negative example constructs
an actual empty result from a symbolic empty input via the skip branch. It does
not require an empty-map constructor, concrete key instance or lookup lemma.
For correlated guards, unreachable alternatives, erase, failure or loops, this
is not an exact source-program analysis. Neither compiler transformation
correctness nor practical guard-removal benefit follows without another model.

## One authorized source correction

Original unused `Body.lean`: 5,485 bytes, SHA-256
`a1595a907eaa27885805e4acd9483e1864618fe9ea69bb6ec59d7fe8d0a93cb2`.
Root authorized only the following pre-execution correction in `nonempty_iff`:

```diff
-    | true => exact Or.inr effect
+    | true => exact Or.inr rfl
```

`cases effect : mustWrite p` generalizes that expression in the goal and then
cases the new Boolean. The true branch's right disjunct is `true = true`, while
`effect` records `mustWrite p = true`; reflexivity is the appropriate term for
the rewritten goal. This follows from the pinned Lean 4.34 tactic source:
`Lean/Elab/Tactic/Induction.lean:884–929` generalizes annotated targets and
modifies the goal. This is a static source diagnosis, not a recorded compiler
failure. The false branch correctly retains `effect` to construct its witness.

Corrected source: **5,482 bytes**, SHA-256
`1bf285a61e8436b694cac26c8a59f21bf0adadfd25b9e2efefd95f3e06284a7e`.
No other source line changed. `PROOF.md` remains 6,802 bytes, SHA-256
`f172082b56c520eb72dd9eb33ef3c03e31b75d4ff5c369746c0288b333f323ec`.

The dependent-induction alternatives have the intended explicit field shapes:
skip takes its map; put takes map/key/value; sequence takes two executions and
two induction hypotheses; each choice takes one execution and one hypothesis.
The implicit plan/map indices are not user-named without `@`. Lean's actual
`getNumExplicitFields`/`introN` handling at lines 314–337 and 501–506 supports
this reading. Boolean helpers use definitional OR/AND reductions, and syntax
induction's identity witnesses share the same initial map as required. No
remaining mathematical defect was found; this does not replace elaboration.

## Dependency and size boundaries

The body fits the existing approved-project source-body interface: no duplicate
module/import preamble, no new executable wrapper, no new axiom or `sorry`.
The import wrapper must select `Std.Data.HashMap.Lemmas`; exact receiver bindings
still come from the independently checked parent, not source import convenience.

The actual saved basis inventory additionally confirms `And`, `And.intro`,
`And.left`, `And.right`, `And.rec`, `And.casesOn`, `Eq.ndrec`, `Eq.casesOn` and
the used Bool operations/recursors/noConfusion. Hence the conjunction helpers
and equality transport introduce no identified missing foundation name. The
two map insert cases directly use the intended received theorem.

Thirteen source declarations are not thirteen whole export units. Reachable
private helpers, recursive-definition helpers, generated constructors/recursors
and complete inductive groups must all be counted. Actual unresolved-name and
whole-group census must satisfy the existing **32 units / 4 MiB / 131,072 nodes**
without changing caps, splitting groups or inventing imported identities.
Private helper names must retain their exact semantics; avoiding a name is not
a justification for changing a checker's normalization rule.

There is a separate existing cost boundary: new Plan/Exec inductives trigger
`OrdinaryExport.indexSource` once to recover generated group members. That scans
the approved local imported environment, with 262,144 total-record and 65,536
grouping-record caps. It is not a worldwide-corpus scan, but its actual cost and
fit are not implied by the short source. The existing deferred-export route
still stops at safe imported constants and later requires exact protected
resolution. No extra mathematical library, indexing mechanism, budget increase
or runtime is selected by this review.

This is a substantive small abstraction and exact law, not historical novelty
or demonstrated growth advantage. An equally capable approved ordinary Lean
library can prove it too. Continue only when actual dependency grounding and
the intended reuse justify their full costs; the current native intake defect
must be resolved before a commons contribution can be selected.
