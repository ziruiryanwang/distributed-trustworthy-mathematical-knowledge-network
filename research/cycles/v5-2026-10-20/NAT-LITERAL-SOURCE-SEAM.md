# Nat literal source seam: bounded lowering, unchanged mathematical checker

2026-10-20, core_search; source/theory only, no execution/compiler/proof/code change.
**GO in principle for a narrow SourceRows successor; no frontend/image rebuild.**
This is supported small-literal source interoperability, not general arithmetic
compatibility, efficient closed computation or useful-growth evidence.

## Actual selected path, not historical similarly named sources

`distribution-coherent-01-input.json` `1903bb44` selects frontend
`author-lean-link-01/link/AuthorLean.exe` `1f73b8b0`. Its build02 selection uses
`software/v5/authoring/native02/AuthorLean.lean` `9597caa0`; link01 consumes
build02's generated C `5cd6401e`. Selected `modules/source_rows.py` is `60c7255d`.
Selected mixed authoring is `interface_views/authoring_atomic.py` `081d9d18`;
ordinary `authoring/source.py` `834718f8` uses the same decoder.

Native02 `removeMData` leaves literals unchanged; `dumpExprAux` line195 emits
`natVal` as a decimal string. `dumpNatDeps` line245 checks original builtin Nat
and calls `dumpConstant`; its inductive branch emits the full types/constructors/
recursors group. `dumpDeps` recursively exports all used constant dependencies.
Thus the original export already contains required Nat closure; it is not a
missing frontend literal serializer. No selected preceding normalization exists.
Both finish methods check source/context/roots and derive the local name census,
then call `decode_source`. `SourceRows.expression` currently rejects `natVal`.
The resulting canonical spec is revalidated, and `emit_relation_rows`/NativeRows
regenerates relocated no-literal rows for the independent mathematical relation.

## Smallest affected boundary and exact preconditions

Add one tightly bounded `natVal` branch to a fresh SourceRows successor, plus
private original-Nat closure validation and expansion accounting. Preserve raw
exports, names, selected OfNat instances and every other expression constructor.
Do not change codec/schema, native row tags, semantic policy or receipt image.
Do not change `sameExpression`/`normalExpr` in the frontend: these check already
decoded foundation/import interfaces; normalized arithmetic imports use constructors.

Only actual raw native Nat literals qualify. The adopted22-declaration foundation
contains no Nat, so require the exact original local `Nat`, `Nat.zero`, `Nat.succ`
group; do not infer foundation authority from spelling or choose a relocated lookalike.
Require ordinary Nat's exact Type0/no-parameter/no-index shape and ordered zero/
succ constructors (zero has0 fields; succ has1 recursive Nat field), complete
generated recursor metadata/rules, and unambiguous existing local references.
Do not synthesize absent declarations or rewrite arbitrary overloaded `OfNat`.
The selected frontend preserves its original Init bindings and exports dependency
closure; original `Nat.add`, `OfNat`, its instance and helpers stay ordinary code.
Any unsupported dependency or group must refuse through existing checks.

For raw numeral k, lower to `Nat.succ` applied k times to `Nat.zero` BEFORE
relocation. The subsequent existing relocation changes all these exact local
references consistently to this module's Nat, zero and succ; no builtin numeric
primitive or equality with another module's Nat is thereby introduced.

## Two correspondence obligations, not a fake source attestation

Lean's pinned Expr documentation identifies rawNat k with its constructor term.
Homomorphic replacement preserves expression meaning by congruence in the ORIGINAL
native environment, while leaving OfNat's selected application intact. This small
translation argument, original rows and closure checks are the source-fidelity gate;
source hashes alone do not prove native execution or semantic equivalence.
Next, the unchanged independent relation checks canonical descriptors/body hashes
against regenerated relocated rows, then freshly checks the whole local extension.
That is a SECOND gate, not a comparison of original frontend rows to source text.
It may refuse conversion steps that relied on native primitives after relocation.
No new native-defeq process is required merely to replace finite raw numerals.

## Refuse expansion before allocating it

Accept only canonical nonnegative decimal spelling (`0` or nonzero-leading digits).
Compare decimal length/value against remaining limits BEFORE bigint conversion or
constructing k cells; do not loop on an unbounded attacker-controlled integer.
At occurrence depth d, k contributes 2k+1 expression nodes, 3k+2 codec validation
visits including references, and maximum codec depth d+k+1. Count every occurrence,
not only distinct source-DAG literals. Retain aggregate SourceRows work and all
unchanged group/spec/body depth192/node250000/byte16MiB checks; account enclosing
validator frames and UTF-8 bytes, not just the isolated numeral. No limit increase.
Preflight bounded normalized output size; final unchanged validators remain mandatory.

## Explicit failure boundaries and decisive examples

`fun n : Nat => Nat.add n 2` keeps its actual add/OfNat closure and is the chosen
small discriminator; successful checking is not yet observed. Source-level control:
`Nat.add 100 100 = 200` with reflexivity uses compact native numerals, but lowering
200 already exceeds depth192 and must refuse before building that chain.
`Nat.add 0 (Nat.pow 2 30) = Nat.pow 2 30` uses only small literals yet can require
huge recursive unary computation after relocation. Native optimized arithmetic and
the relocated logical bodies have different costs; literal bounds do not bound
conversion work. Existing finite checker containment/refusal must remain in force.
These are theoretical discriminators, not executed success/failure measurements.
A later consumer's builtin Nat is NOT the acquired module-qualified Nat. Reuse its
exact constructors/definitions; this lowering supplies no automatic numeric bridge.
