# RC0 core and constructive-fixture review

2026-10-21, independent adaptive review. **PASS for the selected source-level
core/fixture boundary and proceeding to one bounded native differential control
run after root's complete build/harness review.** No compilation, product import,
native test, guest execution or proof was run by this reviewer. This is neither
a machine-checked refinement theorem nor permission to adopt a new trust image.

## The central proposition

The necessary obligation is stronger than ordinary mathematical plausibility:

```text
RC0_accept(C) = (J, ordered Parents)
    implies original_fixed_I_relation(W(C)) = (J, ordered Parents).
```

The original I image is
`9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e`.
W is the constructive original-format witness, not a fake I receipt. The new
aggregate must discharge exact parents under its own freshly adopted image.
Identical J bytes do not make a native conditional result portable authority.

The argument below is a reviewed source argument. Two finite differential
instances are useful implementation discriminators, not proof of universal
compiler/checker correctness or the full v5 release gate.

## Resolved findings before runtime

- The first parser would accept syntactic `App(Lambda(...), argument)`, contrary
  to the selected restricted normal fragment. Recursive parsing now explicitly
  refuses that shape, including an inner redex in a longer application spine.
  This restriction applies to imported types, local types and proof syntax.
- An earlier eager `imax(a,0) = 0` rewrite was mathematically sound but insufficient
  for a blanket *original-pointer* correspondence under arbitrary enclosing
  expressions. Root/growth replaced it with raw IMax interning. The independent
  review concurs with the source proof in `RESTRICTED-COMPOSITION-IMAX-ADDENDUM.md`:
  zero-ending right spines are recognized only at an actual root-Sort comparison
  or the theorem-Prop check. No nested normalization is smuggled into structural
  equality. This removes, rather than assumes, a complicated term-flow invariant.
- Final theorem comparison now has the original `inferred, declared` orientation;
  application comparison remains `domain, argument_type`.

No remaining concrete semantic blocker was identified in the selected core.
Unsupported mathematics is deliberately refused. In particular, this is not a
general Lean kernel replacement, a transparent-definition import protocol, or a
beta/delta/eta conversion solver.

## Construction and checking correspondence

### Commitments, visibility and foundation

The six exact frame fields are schema, image, rank, local_spec, parents and proofs.
The code binds the old I image, adopted F/P, exact group commitments/openings and
strict mathematical rank. The caller's ordered parent journal list is preserved;
imported groups are processed in the original `(module,index)` order. Duplicate
parents/imports/qualified declarations refuse. Only singleton ordinary theorem
declarations with empty metadata and null value commitment enter RC0.

All selected imported types are installed before checking their explicit type
reference closure. A local theorem becomes visible only *after* its type and proof
have checked. Consequently missing imported dependencies and local self/forward
references do not become implicit declarations. A parent J remains a premise:
the core does not assert that it has verified a receipt for that premise.

The compiled foundation table is a projection of the exact adopted 413-row,
23,313-byte F, not an independent axiom declaration. Eq's type is native index6,
with parameter name2 and binder names4/9/9. Eq.trans is native type103, parameter
name11, binder names4/5/28/29/30/31. Its successive Eq arguments are `(3,2,1)`,
`(4,2,1)` and `(5,4,2)`. Preserving binder-origin metadata matters below an
application; simply erasing those names globally would strengthen conversion.

The controls independently reconstruct these signatures from the canonical F
prefix supplied in the original witness, checking its size and SHA-256 before
comparison. Reconstruction follows native name/level/expression rows and actual
declaration records; it does not derive expected types from the production table.
The two original-relation positives independently bind that prefix to real I
semantics. No full F replay is added to the production RC path.

### Structural equality and the original quick branches

Arena keys compare complete structures, not hash equality alone. They include
qualified addresses, universe structure, binder origin and binder style. Thus
equal internal nodes map to equal native interned expressions under the same
local-context correspondence. Internal fresh-local IDs never repeat.

For unequal nodes, RC accepts only:

- actual root Sorts whose levels are both recognized as zero;
- actual root Pi/Pi or Lambda/Lambda, after comparing their domains and opening
  both bodies with one shared fresh local.

These correspond to `tc.rs::def_eq_quick_check`, `def_eq_sort` and
`def_eq_binder_multi/aux`. In particular, unequal App nodes do not recursively
compare their operands: a binder-name or universe-zero equivalence hidden under
an application remains refused. The original quick path is reached before its
potentially body-demanding general conversion fallbacks.

The zero predicate is `Z(Zero)` and `Z(IMax(a,b)) iff Z(b)`, false otherwise.
Induction on the right spine gives native `simplify(l)=Zero` whenever Z(l).
Native `leq` simplifies its arguments, so this implies native `is_zero(l)` and,
for two recognized zero levels, `eq_antisymm(l,r)`. All such traversal is charged
and depth-bounded. Raw IMax remains raw during inference and level substitution.

### Substitution and inference

Public binder scope is checked at parse time. Opening replaces the one outer
bound variable at the traversal offset, preserves inner indices, and refuses an
unopened higher variable. Production replacements have no loose bound variables:
outer scopes were opened first. Closing abstracts only the selected immutable
local and preserves outer locals. Per-operation caches include the binder offset.

Universe substitution is simultaneous: a replacement is returned unchanged, not
recursively substituted again. The cache is per substitution call. Inference
caches immutable expression IDs whose fresh-local context is already explicit;
the environment only grows and never rebinds an address.

Application inference requires an already syntactic Pi, compares its domain in
the original orientation and opens the result. Repeated single opening agrees
with the original batched telescope instantiation. Lambda inference checks each
domain as a type and closes the inferred body type into a Pi. Pi inference folds
raw imax in the same right-associated order as the original native telescope
loop. Sort inference uses raw successor. Source bvars cannot reach inference
unopened. These are structural cases, not assumptions about arbitrary conversion.

For each new theorem, reference closure, the type's sort/Prop classification,
proof inference and final exact/quick comparison precede insertion. The original
W has precisely the selected sealed-theorem imports and checked local declarations;
there are no transparent definitions, extra axioms, omitted theorem bodies for
new declarations, or inserted unsupported declaration groups.

## Bounds needed by the *original* relation

Rejecting over-budget inputs is part of the refinement, not merely a performance
preference. The reviewed conservative virtual-W arithmetic is:

```text
rows <= 413 + 768 + 8 + 8192 + 24 = 9405
bytes <= 23313 + 768*512 + 8192*256 + 8*128 + 24*256 + 262144 + 4096
      = 2787089 < 3 MiB
JSON value nodes <= 23313 + 32*(8192+24) + 8*(768+8) + 32768 + 1024
                 = 326225 < 350000
expression + level correspondence visits <= 8192 + 65536 = 73728.
```

The 768 name-row allowance covers at most64 qualified addresses, at most11
absolute name components each, plus universe names. Only zero and eight public
positional universe levels exist. At most16 imports and8 local declarations are
added to F. Rows encode native indices rather than recursively copying syntax;
the original local descriptor/parent payload fits within the already bounded
frame. The named row-size bounds cover the allowed name strings, eight-universe
lists and fixed declaration/term record shapes.

These values are below the retained original input limits (16MiB, one million
JSON nodes, 250,000 rows/correspondence visits,16,384 declarations). Public syntax
depth48 and full-frame JSON depth64 also keep the original serialized W below
the actual JSON parser recursion boundary; the nominal original depth limit alone
would not have sufficed. No old W needs materializing on the production path.

Internal frame work is at most200,000 charged steps, with separately bounded
expression and universe arenas of32,768 entries each. The control path does not
claim these are cycle counts or a complete process-memory bound. The aggregate's
8,192 source visits are an *acceptance* cap charged after a bounded core call:
a refusing stream can process accepted8,192 plus final-frame8,192 visits. Its
16 bounded core calls give a3,200,000 work-step cap. This distinction is preserved
in the source/comments and controls; neither refusal nor a new frame refunds work.

## Root's constructive fixtures

`fixtures.py` is source-reviewed as a pure untrusted builder. Its first theorem
has four universes and16 binders. With `f : B -> C -> D`, `g : A -> A -> B`,
`h : A -> A -> C` and three equalities on A, it applies the acquired binary
congruence theorem to g, to h, and then to f. This yields the full contextual
equality `f (g a b) (h b c) = f (g a' b') (h b' c')`, not an unrelated constant
or a restatement that discards the acquired theorem.

The second theorem has18 binders: it applies that exact first theorem, then
foundation Eq.trans with an additional equality from the middle endpoint to d.
All16 first-theorem arguments are passed in order and all four universe positions
are preserved. The fixed parent opening is checked by the builder, while predicted
J bytes are explicitly inert data. The original-W emitter seeds the adopted F,
emits ordered moduleImportTheorem rows, then each local theorem's real proof with
anonymous public binders and scoped positional universe names.

The selected native test must compare **all encoded J bytes and ordered parent
journals**, not merely theorem names, hash prefixes or an expected boolean.
Original-witness equality of image/rank/spec/parents is checked first. The successor
also checks that its parent J exactly equals the first RC conclusion.

## Source pins and scope

| Source | SHA-256 |
|---|---|
| lib.rs | a912c40b1b8c1532d76f99208cc0e52fee20fc381c1387916c739e47b20fcc26 |
| syntax.rs | 34cb81eb6d629f49f4c579841c45c6674f494a28a657a0bb337a8e3a8e44a2db |
| foundation.rs | 12ce087696b026892cf8a52f8dc93b860fac8b0312ad1024b39a7fbda552b2f3 |
| typing.rs | 3376e13a48ad3caefdd7dff3c8604915eae0921cad95d04aa0f81407de29cc08 |
| relation.rs | 540af158f61654f50aa50335dec7811b43448f3520050edf953db7e75060670b |
| fixtures.py | b6f2014319b97b94b04ac9a8caf4068031f7f0e4a854a00aff596d6c47b9e51d |

Files are under `software/v5/restricted_composition`. Aggregate/build/runner
review belongs to the release reviewer; this note does not replace it. Focused
controls are specified in `RESTRICTED-COMPOSITION-CONTROLS.md`. Root alone selects
runtime, adopts outcomes and decides whether evidence warrants a new guest or
proof expenditure. No historical campaign or already completed sharing audit
is restarted by this note.
