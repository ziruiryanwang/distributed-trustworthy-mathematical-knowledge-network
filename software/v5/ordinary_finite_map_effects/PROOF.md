# Finite-map effects: source and proof boundary

Source-only implementation of `CONTRACT.md` and the adopted
`ordinary_intake_progress/NEXT-MATHEMATICAL-STEP.md` (`aa73a5ce...`).
No Lean elaboration, candidate export, native checking, owner operation or test
has run. The progress implementation and all used predecessors are unchanged.

## Source interface

`Body.lean` is a UTF-8 **source body**, deliberately without a module/import
preamble. The existing approved-project `ordinary_contribution.assemble_source`
adds its `module`, Init/meta-helper imports, selected project imports, `public
section`, protected request construction and contribution-export footer. Select
`Std.Data.HashMap.Lemmas` as the existing non-meta approved-project import. A
second maintained wrapper or copied standalone theory is unnecessary.

The proposed nine public output names are:

- `FiniteMapEffects.Plan`, `FiniteMapEffects.Exec`, `FiniteMapEffects.mustWrite`;
- `FiniteMapEffects.zero_effect_witness`;
- `FiniteMapEffects.preserves_nonempty`, `FiniteMapEffects.forces_nonempty`;
- `FiniteMapEffects.nonempty_iff`;
- `FiniteMapEffects.optional_then_writing_choice`;
- `FiniteMapEffects.optional_write_empty_outcome`.

An actual selection must encode these names in the existing structured-name
format and use a fresh compatible namespace/module. It must separately select
the exact approved project, source bytes and output paths. Do not pass the
producer's different extraction-project schema as `--project-authoring`.

## Mathematical argument

`Plan` has skip, insert, sequential composition and nondeterministic choice.
`Exec` is the five-rule relation from the adopted specification: skip, insert,
sequence, left choice and right choice. There are no guards, erase, failure or
loops. Both choices are possible independently at every occurrence.

`mustWrite` is structurally recursive, using false for skip, true for insert,
Boolean OR for sequence and AND for choice. It is a computable finite summary,
not an oracle or importance score. `@[expose]` preserves its ordinary reusable
definition interface. Lean's normal approved compiler support remains distinct
from the mathematical evidence exported for independent checking.

Four private helpers prove the required OR/AND true/false case splits by cases
on the first Boolean. Their reductions use the actual definitions
`Bool.or x y = Bool.rec y true x` and
`Bool.and x y = Bool.rec false y x`; impossible constructor equalities are
eliminated by `cases`. No simp database or imported convenience lemmas are used.

`zero_effect_witness` inducts on syntax. A false sequence summary supplies two
identity executions; a false choice supplies one. It constructs a path leaving
the exact input map unchanged, not merely an extensionally equal map.

`preserves_nonempty` inducts on an execution. Skip preserves its input, both
choice rules inherit the branch result, and sequence composes its two induction
hypotheses. Insert uses **`Std.HashMap.isEmpty_insert` directly**.

`forces_nonempty` also inducts on execution. For a true sequence effect, either
the first part forces nonemptiness and the second preserves it, or the second
forces it. A true choice effect forces either branch. Its insert case again uses
the actual acquired map theorem; it does not replace maps with an abstract model.

`nonempty_iff` states the complete weakest precondition:

\[
(\forall n,\;\operatorname{Exec}(p,m,n)\Rightarrow n.\mathrm{isEmpty}=\mathrm{false})
\iff (m.\mathrm{isEmpty}=\mathrm{false}\lor\operatorname{mustWrite}(p)=\mathrm{true}).
\]

The reverse direction uses preservation or forcing. For the forward direction,
case-split the Boolean effect; if false, apply the assumed universal result to
the identity execution. This converse is constructive and explicitly avoids a
vacuous universal argument. No empty-map constructor or key inhabitant is needed.

The positive example has an optional write followed by a choice with two writing
branches. Its effect reduces to true by computation. The negative example assumes
a symbolic empty initial map and exhibits the skip branch's exact empty result.
It is mathematical source, not an executed negative admission test.

## Dependencies and remaining source risks

The concrete map boundary is only `Std.HashMap`, `insert`, `isEmpty` and
`isEmpty_insert`, with explicit BEq/hash and lawfulness parameters. Their exact
portable identities and retained source/data pins are in NEXT-MATHEMATICAL-STEP.
The restored target unit is `ab6f1b22...` and its target export is `bf281176...`.
No concrete Nat instance, lookup theorem, map extensionality, List or new Std
export is required by this source design.

The exact saved fixed-basis inventory was inspected for Bool operations,
constructors/recursors/noConfusion, Eq transport, Or/And/Iff, Exists, True and
False. All are present. Source proof tactics are limited to introductions,
constructor/Boolean cases, structural induction and explicit applications.
Generated helper dependencies still require inspection after approved
elaboration; an unexpected dependency is a reason to localize the source, not
permission to invent a protected name binding.

The source contains thirteen named declarations, including four private Boolean
helpers, but that is **not** the number of exported whole units. Plan/Exec
generate constructors, recursors and auxiliary declarations; recursion and proof
elaboration can add helpers. The existing 32-new-unit, 4-MiB and 131,072-node
ceilings apply to the actual complete reachable closure. No fit is established
by counting visible source declarations.

The independent reviewer also identified the existing exporter cost boundary:
new inductives make `OrdinaryExport.selectedFromBoundary` run `indexSource` to
recover complete generated groups from the imported local kernel environment.
Its existing ceilings are 262,144 source records and 65,536 grouping records.
This is bounded approved-local-library work, not replay of all worldwide commons
knowledge. Its actual elapsed/memory cost and this candidate's fit are unknown;
neither a larger cap nor another indexing mechanism is selected here.

Actual contribution remains conditional on a separately adopted rich parent,
using the existing approved-project route and `acquired_targets=[]`. Compilation
alone cannot establish a commons warrant. A future finite selection must inspect
actual bindings and require normal independent admission of all new groups.

This is a small theory of a specified finite language, potentially reusable for
reasoning about emptiness guards. It establishes no general source optimization,
historical novelty, measured growth benefit, speedup or final-v5 completion. An
equally capable approved ordinary Lean library can prove the same mathematics.
