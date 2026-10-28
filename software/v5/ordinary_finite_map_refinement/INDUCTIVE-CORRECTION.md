# Separate a new context datatype from received runtime layouts

2026-10-28. SOURCE ONLY. Root owns execution and adoption. Preserve the used
BodyMath.lean and the failed contribution01 without modification. No Lean or
product execution, owner/database access, package rebuild or Git mutation was
performed for this correction.

## Observed boundary and source explanation

Contribution01 successfully reconstructed all 11 selected groups: 609 labels,
22 introduced names, nine checked units and two theorem signatures. The first
subsequent error is on the new Context declaration:
`FiniteMapEffects.Plan was not compiled; compileDecls must run on inductive types first`.
The matcher/cases and fill-reduction errors follow an incomplete Context
elaboration; they do not independently establish defects in the intended laws.
The actual source exporter ultimately refused `SORRY_REFERENCE`; no final
mathematical admission occurred. Failed source, logs and charges remain evidence.

The earlier source review correctly checked the borrowed theorem signatures
but missed the mandatory runtime-layout work of a new datatype whose fields
mention a received datatype. Fix that boundary directly, not the downstream
cascade one error at a time.

Pinned Lean 4.34.0 source establishes:

- `Elab/MutualInductive.lean:216-224` explicitly rejects `noncomputable` on
  inductives and constructors. A modifier is therefore not a possible fix.
- `elabInductiveViews:1563-1581` adds the mathematical inductive and immediately
  calls `Lean.compileDecls`, before generating casesOn, sizeOf and other useful
  elaboration support.
- `Compiler/LCNF/Main.lean:131-138` handles inductives by eagerly calling
  `compileInductives` and returning, before its function-code postponement
  branches. `compiler.postponeCompile` cannot bypass this work.
- `LCNF/ToImpureType.lean:287-301` computes constructor layouts and other
  cross-module compiler metadata. Its readers, and `LCNF/MonoTypes.lean:109-119`,
  deliberately reject missing metadata for existing inductives. A kernel-valid
  portable Plan declaration alone does not supply these caches.

The fill-local matcher option addresses a different path. Disabling compiler
checks, fabricating caches, globally replacing compileDecls or rebuilding the
received library's compiler infrastructure is neither necessary nor selected.

## Minimal representation correction

The fresh source is **BodyParametric.lean**, 6,902 bytes, SHA-256
`55988cf3fde26bc08173cbc352c1266ea836897ac56d70ec45c8e9e900d71b9d`.
It generalizes only the new context's payload parameter:

```lean
inductive Context (A : Type u) where
  | hole : Context A
  | seqLeft (inner : Context A) (right : A) : Context A
  | seqRight (left : A) (inner : Context A) : Context A
  | chooseLeft (inner : Context A) (right : A) : Context A
  | chooseRight (left : A) (inner : Context A) : Context A
```

The two explicit context uses, in fill's type and fill_summary_mono's binder,
become `Context (Plan K V)`. The context doccomment describes generic payloads.
All five noncomputable definitions, the local matcher option, proof bodies,
other theorem statements, selected output names and acquisition inputs stay
byte-identical. The change is one seven-line declaration/comment block plus
two type occurrences; mechanically undoing those replacements reproduces
BodyMath exactly (`276e64ea...`, 6,927 bytes, unchanged LF endings).

The eager inductive compilation now sees only the arbitrary parameter A, its
own recursion, and existing Init machinery. No Plan constant occurs anywhere
in that inductive declaration. Lean's LCNF monomorphization substitutes generic
parameters with its ordinary `lcAny` representation; it need not ask for Plan's
layout. The later instantiation `Context (Plan K V)` is in noncomputable fill
and mathematical theorem/definition types, not a new inductive compiler call.
The existing explicit modifiers and matcher option continue to prevent optional
function/matcher compilation that would need executable received definitions.

This is a normal polymorphic datatype, not a new trust mechanism. Final exact-
parent kernel admission, expression encoding and ordinary publication are
unchanged. No assertion is weakened to make the source pass.

## Preservation of the intended mathematics

For any payload A, contexts are finite terms of the grammar
`hole | seqLeft(context,A) | seqRight(A,context) |
chooseLeft(context,A) | chooseRight(A,context)`.
Specializing A to Plan K V gives precisely the originally intended five
constructors and field meanings. Its universe is `Type (max u v)`, as before.
The recursively defined fill has the same five equations. Consequently the
summary monotonicity, contextual refinement, equivalence and failure-witness
arguments retain their intended subjects and premises.

This is structural correspondence, not a claim of definitional equality between
two different inductive declarations. The predecessor Context was never accepted
by the product, so no accepted identity or existing public client is migrated.
The new generic datatype is also independently reusable with other plan-like
payloads; that is a modest abstraction improvement, not evidence of discovery
speedup or historical novelty.

## Next decisive check

After independent source review, root may select one fresh successor of the
existing public contribution operation, changing only the source snapshot and
run/output identities. Reuse actual discovered targets, exact P/F, package,
project descriptor, output names and original finite bounds. No new harness,
setup, compiler support build, copied producer module or automatic retry.

Require the same successful 11-group frontier reconstruction, complete new
source elaboration, actual exported closure within existing bounds and unchanged
final-parent native admission of the intended endpoints. Generated helper fit
and operational elaboration remain to be established; the source argument
removes the observed Plan-layout dependency but does not claim execution success.

## Pinned implementation references

All paths below are relative to `software/runtime/lean-4.34.0-windows/src/lean/`.

| Source | SHA-256 |
|---|---|
| Lean/Elab/MutualInductive.lean | `8a30233713df9a399c8a529511c6767668d9cfa82a46a8ae02b8c631231274d8` |
| Lean/CoreM.lean | `0e94919972c60e8f2bdc73ecc9845a745c9a3373fce4069b9e27ae52560c0a7a` |
| Lean/Compiler/LCNF/Main.lean | `61d0c60e60a5d39011e7e2110575518468edb38aac580aea755a5b6ae44c88f1` |
| Lean/Compiler/LCNF/MonoTypes.lean | `a5624363537d2c573c0656c002a01781dd6cc982f092ed8fa00adebe30a6f923` |
| Lean/Compiler/LCNF/ToImpureType.lean | `dc2e7718cb3018a3772222ed31986bd4bf9971e9c6e04144f090b8598b72cae3` |
