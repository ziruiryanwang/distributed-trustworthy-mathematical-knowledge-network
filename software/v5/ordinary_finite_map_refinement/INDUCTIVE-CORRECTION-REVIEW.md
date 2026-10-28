# Parametric context correction: independent review

2026-10-28. Source/file review only. No Lean execution, product imports,
owner/database opens, Git or edits to the author's files.

**GO for BodyParametric.lean as the next bounded source candidate.** This removes
the observed executable-layout dependency by generalizing a datatype; it does
not suppress kernel checks or assert successful elaboration in advance.

The reviewer independently read the actual eager compilation path. Lean's
MutualInductive adds the inductive then unconditionally calls compileDecls before
its auxiliary constructions. LCNF handles inductives with compileInductives
before function-code postponement. CoreM dispatches that compiler call even when
ordinary async elaboration is disabled. A noncomputable inductive modifier is
explicitly rejected. The previous fill-local matcher option governs another
path. There is no supported avoidance in the proposed defer/matcher/modifier
choices; do not use them as a speculative fix.

The selected replacement instead declares Context(A) with generic payload fields.
No Plan constant appears in this new inductive or its constructor signatures.
MonoTypes.toMonoType substitutes generic dependent parameters with anyExpr/lcAny,
and the eager group therefore does not require Plan's missing layout metadata.
Later specialization to Context(Plan K V) occurs in the noncomputable fill and
proof-level uses. Existing noncomputable modifiers and the scoped matcher option
remain in place. No new executable use of the received Plan is requested.

For each K,V, substituting A=Plan K V gives the same five constructors with the
same recursive/payload positions as the intended original context grammar.
Each fill equation and every proof body is unchanged. Universes instantiate at
max(u,v), so the specialized context has the intended universe. This is a
structural correspondence of the intended mathematics, not definitional equality
or identifier equality between different inductive declarations. The failed
predecessor Context was never admitted, so no accepted result is rewritten.

Independent byte comparison confirms that reversing precisely the seven-line
declaration/doccomment replacement and the two Context(Plan K V) occurrences
reproduces used BodyMath.lean exactly. No theorem premise, proof body, source
option, target name or other bytes changed; LF endings remain unchanged.

| Reviewed source | SHA-256 |
|---|---|
| BodyParametric.lean, 6,902 bytes | `55988cf3fde26bc08173cbc352c1266ea836897ac56d70ec45c8e9e900d71b9d` |
| INDUCTIVE-CORRECTION.md | `2f144631b390e45efbb87e1fb81154570c4dec90d04a88a6186ee288e0c5d450` |
| preserved BodyMath.lean | `276e64eada849a8ed46a23b6ceee122124ef99c0b91a57fdd97b619de3708b89` |

All five pinned Lean source hashes in INDUCTIVE-CORRECTION independently match.
This argument addresses the observed compiler obstacle. Generated auxiliaries,
closure bounds and final exact-parent checking still require the next selected
public contribution outcome. No new harness, checker change, re-grounding of
Std, broader compiler implementation or duplicate positive test is justified.
