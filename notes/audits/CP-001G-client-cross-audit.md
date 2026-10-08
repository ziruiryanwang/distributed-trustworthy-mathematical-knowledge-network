# CP-001G: independent CLIENT1 correspondence and operability audit

Date: 2026-09-20. Reviewer: STRUCT2/decentralization analyst, independent of the CLIENT1 author. Scope: paper/source audit only. No implementation, proof run, build, extraction, executable model, network-protocol run or performance measurement.

## Materials and evidence boundary

Read the complete [CLIENT1 analysis](../analyses/CP-001G-library-interoperability.md), including its source cases, two-environment correspondence, inert recipe, complete-closure accounting and evidence-selection section. Initial reviewed SHA-256 was `6B625CBB8B41EEB4CC67C183B664BAC82D82FB582307115263A4B2C25771267C`. Also inspected the PI1 representation and the parent-owned profile/consumer binding at their relevant boundaries. The frozen E/F specifications were not changed.

Independently fetched and read these pinned Lean `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b` source portions:

- [ProjFns.lean](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/ProjFns.lean): complete projection/auxiliary-parent metadata record and insertion file.
- [Structure.lean](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Structure.lean): field/parent/structure records, registration and constructor access through line 150.
- [Meta/WHNF.lean](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Meta/WHNF.lean): `mkProjFn`, constructor/eta reconstruction, projection metadata use, `reduceProj?`, and class-projection unfolding excerpts.
- [Class.lean](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Class.lean): class extension, output-parameter derivation and `addClass` in lines 66–180.
- [Elab/BuiltinTerm.lean](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Elab/BuiltinTerm.lean): exact-name numeral/scientific elaboration around lines 217–254.
- [Init/Data/Fin/Lemmas.lean](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Init/Data/Fin/Lemmas.lean): the `Fin.castLE_castLE` statement including `Nat.le_trans`.

Independently checked pinned mathlib `5ed2965256430c3649e86755f9576b54eca72435` [Finset.Range](https://github.com/leanprover-community/mathlib4/blob/5ed2965256430c3649e86755f9576b54eca72435/Mathlib/Data/Finset/Range.lean#L53) and [Data.Quot](https://github.com/leanprover-community/mathlib4/blob/5ed2965256430c3649e86755f9576b54eca72435/Mathlib/Data/Quot.lean#L359) excerpts against the note's displayed declarations. Other source-linked facts remain the author's inspected-source claims, not a claim that this reviewer independently reconstructed all dependency closures.

## Finding C1: propositional projector equality is not computational projection metadata

Severity: local operability/specification issue; independent native checking still protects accepted corpus mathematics.

The initial Structure-view recipe admitted projection matching through "exact body correspondence or a separately checked equality." These are not interchangeable authorities for Lean's raw structure/projection extensions. `addProjectionFnInfo` stores caller-supplied metadata without establishing the advertised projector's behavior. `WHNF.mkProjFn` consults structure metadata when constructing field expressions for native-style constructor/eta processing. It does not automatically insert a provided propositional equality proof at that use site.

Countercase: let a structure have a list-valued field. A function returning the reverse of the reverse of that field can be proved propositionally equal to the field, while it is not generally the native projection by definitional reduction on an unknown list. A checked equality theorem can justify an explicit rewrite. It does not make every uninstrumented frontend use of that function a computational field projection.

Required repair: raw projector/eta metadata needs qualified definitional or exact structural correspondence to the intended constructor/field/parameter selector. A merely propositional equality can be used only through explicit proof-carrying rewrite/transport, or the projection convenience is declined. This distinction must also cover auxiliary parent projections and same-typed fields; type compatibility alone is insufficient.

The finding was sent to the CLIENT1 author, who agreed, independently inspected the pinned WHNF path, and applied the repair. The reviewer then reread the actual saved source discussion, revised Structure-view contract and conformance case. The repaired text requires qualified computational correspondence, preserves group/constructor/parameter/universe/field selectors, distinguishes composite parent paths from direct field indexes, and reserves propositional equality for explicit proof-carrying use. C1 is **closed at paper-specification scope**.

## Checked boundaries

| Boundary | Audit conclusion |
|---|---|
| Presentation names versus semantic identity | The finite mapping rewrites actual references and compares exact canonical descriptors. It does not identify two nominal groups by display name or ignore differing universe order/body. |
| Two evidence grammars | Semantic descriptors retain JudgmentID references, while proof implementations record actual proof instances. A presentation alias does not erase the selected representative map, replay support or current policy footprint. |
| Canonical/native versus frontend binder information | Finite annotation restoration is allowed only when normalization returns the exact selected canonical object and final applications expose actual arguments. No hidden-premise acceptance rule is added. |
| Ordinary-agent usefulness | Class/instance/simp/structure recipes address real frontend state absent from a kernel declaration set. Explicit native application remains a viable smaller fallback. Broad unmeasured mathlib compatibility is not asserted. |
| Name-sensitive frontend operations | The inspected class/numeral code really uses names/metadata beyond kernel validity. A separately qualified required-name inventory is necessary; arbitrary hashed renaming is not enough. |
| Finite selected frontend scope | 4096 exposed declarations is explicitly a surface limit, not the full dependency environment. Complete declaration/group/evidence and metadata work needs separately admitted finite resources. No hidden free closure is implied by a small recipe. |
| Dynamic/auxiliary declarations | Metadata registration and simplifier preprocessing can create declarations. The note requires complete new bodies/support to be exported or an explicit checked elimination; such declarations are not dropped as incidental tooling. |
| No executable remote import | The recipe is inert owner-local data. No source, plugin, tactic callback, simproc or arbitrary extension payload is activated by receiving a recipe or descriptor. Fixed frontend code is owner-installed and qualified separately. |
| Failure and partial state | Staged incomplete views are not reported as a complete authoring environment. Elaboration success is separate from native acceptance, and unsupported metadata/closure limits can produce decline/nondecision. |
| Safe classical versus unsafe execution | The checked source distinguishes logical noncomputable choice from unsafe quotient unwrapping. The specified native boundary retains that distinction. |

The source cases support the intended pressure on the concept: proof values occur in ordinary data, theorem references can appear inside statements, and nominal interfaces can transitively depend on those references. Reading these source declarations is not a completed extraction or a proof that every independently selected source branch composes under PI1. The CLIENT1 note correctly assigns that separate obligation to the actual PI1 reconstruction/checking mechanism.

## Remaining qualification obligations, not paper-audit successes

- The installed frontend image, finite supported syntax/convenience profile and complete `FrontendNames1` inventory need actual qualification. The listed name-sensitive examples alone are not a complete inventory of all Lean/mathlib frontend assumptions.
- A complete recipe/export/reimport round trip must be checked for the source cases, with native evidence, generated group inventories, explicit instances and simplifier auxiliaries captured.
- Complete dependency admission, memory and time costs must be measured; current example limits are not evidence that large libraries fit.
- Projection/parent metadata must be tested against wrong same-typed fields, merely propositionally equal functions and unsupported parent encodings, without relying on eventual corpus rejection to conceal a broken authoring view.
- Changing semantic representatives requires the selected PI1 checking/cache discipline. No earlier environment certificate may be copied simply because a semantic DefinitionID/GroupID stayed the same.

These limits do not block freezing a clearly labeled preimplementation concept. They do block claiming that an ordinary remote library already imports, elaborates and exports successfully.

## Final disposition

C1 is closed on the repaired CLIENT1 note with SHA-256 `4734C588E4B9BA66DF8BC93C442B3A43496A3C4EBD4AE00993987FAB3787C4DC`. No additional contradiction was identified in the inspected CLIENT1 correspondence, finite-scope or inert-import boundaries at this paper/source-audit scope. The outstanding qualification obligations above remain explicit. This is not a formal soundness proof of the frontend adapter or a substitute for independent native checking.
