# CP-001G: ordinary library interfaces and a usable local Lean client

Date: 2026-09-20. Status: selected source-backed local-client concept, with the [independent client audit](../audits/CP-001G-client-cross-audit.md) and its projection-metadata repair integrated. Frozen CP-001F remains unchanged. No build, extraction, native replay, proof execution, implementation or benchmark was performed.

## Outcome and scope

Ordinary Lean mathematics already contains the cases excluded by the restricted CP-001F capsule recipe: theorem constants inside statements, proof-bearing data definitions, and proof dependencies reached through the definitions appearing in an inductive interface. These cases do **not** show that an ordinary coherent library cannot be exported under F. They show why F's unchanged-background capsule route cannot be claimed to handle every independently selected proof branch without interface changes.

A second, independent issue concerns the local authoring experience. Complete checked declarations do not recreate Lean's class, instance, structure, projection and simplifier extensions. Some frontend operations also recognize exact declaration names that the kernel itself does not require. Merely hashing every non-kernel-reserved name and calling a class-registration function is therefore insufficient.

Select **CLIENT1**, a separate owner-local presentation workspace with exact semantic correspondence to admitted mathematics, a qualified finite frontend-name inventory, and a narrow inert recipe for reconstructing useful elaboration metadata. It produces ordinary complete candidate terms for independent receiving checks. It is not a new native trust authority, a source/plugin distribution protocol, or a mathematical equivalence bridge.

This note supplies representative actual source slices and paper import/application paths. It does not estimate the fraction of mathlib supported, claim that their complete native dependency graphs have been extracted, or infer successful compilation from reading source. The broader proof-instance representation belongs to the [CP-001G composition analysis](CP-001G-proof-instance-composition.md); mathematical interface transport belongs to the separately owned [BRIDGE1 analysis](CP-001G-interface-bridges-and-applications.md).

## Pinned sources and evidence grades

All Lean observations below use commit `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b` and matching mathlib commit `5ed2965256430c3649e86755f9576b54eca72435`, the F qualification candidates. URLs below include the exact commits.

Distinguish three levels of claim:

- **Read source fact:** the cited source declares or implements the displayed construction.
- **Paper representation consequence:** under the stated Native2 canonical representation and selected source occurrences, changing those references changes the corresponding content dependencies, or violates a capsule guard.
- **Unperformed qualification:** extracting the actual elaborated constant records, checking complete closures, reconstructing the native environment and measuring the resulting costs.

Source-level notation and tactics may elaborate to additional explicit arguments, helper declarations and proof terms. This note does not pretend to have observed those exact runtime records. The correct collector inspects them rather than assuming that a visible proof dependency has disappeared.

## Representative actual library cases

### Proofs stored in ordinary data: Finset.range

The pinned [Finset range source](https://github.com/leanprover-community/mathlib4/blob/5ed2965256430c3649e86755f9576b54eca72435/Mathlib/Data/Finset/Range.lean#L53) declares:

```text
def range (n : ℕ) : Finset ℕ := ⟨_, nodup_range n⟩
theorem mem_range : m ∈ range n ↔ m < n := Multiset.mem_range
```

The definition is at lines 53–54, and the theorem at 64–65. [Multiset.Range](https://github.com/leanprover-community/mathlib4/blob/5ed2965256430c3649e86755f9576b54eca72435/Mathlib/Data/Multiset/Range.lean#L71) supplies `nodup_range (n) : Nodup (range n) := List.nodup_range` at 71–72. This is a proof field in a data value, not an executable tactic marker or political source annotation.

Let T contain the source proof of `Multiset.nodup_range`, while the retained background A contains `Finset.range`. A's definition value then depends on T. F's capsule eligibility guard correctly refuses this unchanged-background plan. Replacing that occurrence by an opaque capsule changes the exact `Finset.range` value descriptor and hence its DefinitionID. A theorem statement referring to the changed range definition can consequently acquire a different JudgmentID.

This does not imply that the range operation has changed extensionally, nor does it justify dropping the proof field. It means that the selected syntactic identities are finer than extensional equality. A broader composition mechanism must either retain the original semantic declaration and associate the selected proof occurrence separately, or supply an explicit new checked interface/transport. It must not claim that different DefinitionIDs are identical merely because their proof fields are irrelevant to the returned natural numbers.

**Positive paper application path.** With one coherent selected library evidence environment, preserve the exact range definition and its support. Import the exact `mem_range` judgment and complete chosen evidence. Given native context `m n : Nat` and `h : m ∈ range n`, construct the explicit native application of `Iff.mp` to the instantiated `mem_range` proof and h. Independently checking that term establishes `m < n` under exactly that context. No simplifier metadata is necessary for this minimal path. CLIENT1 can additionally make the corresponding ordinary Lean application convenient; it cannot change the required native premises.

### A theorem constant inside another statement: Fin.castLE_castLE

The pinned [Lean Fin lemmas](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Init/Data/Fin/Lemmas.lean#L488) declare at 488–490:

```text
theorem castLE_castLE {k m n} (km : k ≤ m) (mn : m ≤ n) (i : Fin k) :
    Fin.castLE mn (Fin.castLE km i) = Fin.castLE (Nat.le_trans km mn) i := ...
```

`Nat.le_trans` appears in the proposition itself. The following `castLE_comp_castLE` at 492–494 has the corresponding function-level statement. This is not a proof-body-only dependency. The frozen canonical representation retains explicit applications and proof arguments; it does not quotient all statements by native proof irrelevance.

If a transformed slice includes the referenced transitivity theorem, replacing its occurrence in this statement by an opaque capsule violates F's unchanged-type guard. If two hypothetical independent branches select different complete witnesses of the same transitivity judgment, they may still express the same canonical statement before such rewriting. The source example is actual; the two independently selected witnesses are a paper composition scenario, not a claim about two observed mathlib builds.

**Positive paper application path.** Retain the same `Fin` group, cast definitions and statement-level theorem reference. Instantiate the imported `castLE_castLE` judgment with explicit k, m, n, km, mn and i. A broader proof-instance mechanism must record the actual selected transitivity evidence reached through the type, not only evidence reached through the theorem's value. A value-only dependency traversal would be incomplete.

### Proof-dependent definitions reach nominal inductive interfaces

The following chain uses ordinary finite-collection foundations:

- [Lean List.Perm](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Init/Data/List/Perm.lean#L86), lines 86–88: `Perm.eqv α : Equivalence (@Perm α)` and `instance isSetoid α : Setoid (List α) := .mk Perm (Perm.eqv α)`.
- [Mathlib Multiset.Defs](https://github.com/leanprover-community/mathlib4/blob/5ed2965256430c3649e86755f9576b54eca72435/Mathlib/Data/Multiset/Defs.lean#L71), lines 71–72: `Multiset α := Quotient (List.isSetoid α)`.
- The same file, [lines 352–353](https://github.com/leanprover-community/mathlib4/blob/5ed2965256430c3649e86755f9576b54eca72435/Mathlib/Data/Multiset/Defs.lean#L352): `Nodup s := Quot.liftOn s List.Nodup (fun _ _ p => propext p.nodup_iff)`.
- [Mathlib Finset.Defs](https://github.com/leanprover-community/mathlib4/blob/5ed2965256430c3649e86755f9576b54eca72435/Mathlib/Data/Finset/Defs.lean#L75), lines 75–79: the structure has fields `val : Multiset α` and `nodup : Nodup val`.

Thus theorem-dependent data definitions occur along the interpretation path of a constructor type. Moving the equivalence or quotient-respectfulness evidence into new capsules and recursively cloning every affected definition can propagate changes into a Finset GroupID. A newly reconstructed nominal group is not identified with the original group by proof irrelevance alone.

The selected broader requirement is therefore **interface-stable proof selection through the entire type/value/group support**, not merely proof-valued wrappers at final theorem roots. The composition analysis owns how that is represented and checked. CLIENT1 does not solve nominal group equality by assigning both groups the display name `Finset`.

For a single compatible export, the positive route remains precise: reconstruct the admitted list/quotient basis, the actual selected setoid proof, the Multiset definitions, and the original finite-set descriptor; regenerate its constructor/recursor inventory; then check the dependent definitions and proofs. Renaming all corresponding native group/member occurrences consistently is part of the qualified adapter, not a license to omit a dependency or identify unrelated groups.

### Sound noncomputable mathematics is not unsafe extraction

[Mathlib Data.Quot](https://github.com/leanprover-community/mathlib4/blob/5ed2965256430c3649e86755f9576b54eca72435/Mathlib/Data/Quot.lean#L359) makes the distinction unusually explicit:

```text
noncomputable def Quot.out (q : Quot r) : α :=
  Classical.choose (Quot.exists_rep q)

unsafe def Quot.unquot : Quot r → α :=
  cast lcProof

theorem Quot.out_eq (q : Quot r) : Quot.mk r q.out = q :=
  Classical.choose_spec (Quot.exists_rep q)
```

These declarations occur at 361–371. The adjacent source comments call the former sound but noncomputable and the latter computable but unsound. Export the actual safe logical choice construction under the admitted classical axiom policy; reject an unsafe dependency rather than equating it with the safe representative selector.

**Positive paper application path.** For an admitted relation r and q, import the exact safe `Quot.out` definition and `out_eq` evidence. The local agent can derive `Quot.mk r (Quot.out q) = q` by theorem application without executing a program that chooses a representative. Noncomputability is not native invalidity. Conversely, this design promises no executable representative algorithm for arbitrary r and q.

The same file [at 408–435](https://github.com/leanprover-community/mathlib4/blob/5ed2965256430c3649e86755f9576b54eca72435/Mathlib/Data/Quot.lean#L408) defines a `piSetoid` instance with equivalence proof fields, then `Quotient.eval` and noncomputable `Quotient.choice` whose source types use `(by infer_instance)` to select that setoid. The resulting native terms must contain the actual instance arguments. Reconstructing the instance search index is a frontend convenience; pretending an omitted instance is supplied by mathematical notation is not an export rule.

## Why native declarations alone do not restore the frontend

The following are directly inspected source mechanisms, not speculative missing features.

| Facility | Source-backed state beyond native declaration insertion |
|---|---|
| Classes | `Class.lean:70–78` stores class status in an environment extension; `isClass` queries it. `addClass:166–175` computes output-parameter metadata from the actual declaration type. |
| Structures | `Structure.lean:25–69` stores field names, projection names, binder metadata and parent information; `registerStructure:109–114` registers an elaborator descriptor. Its source comment requires parent/resolution-order setup as well. |
| Projections | `ProjFns.lean:19–33` separately records constructor name, parameter count, field index and class origin. `Meta/WHNF.lean:165–170` uses registered structure projection names to construct projection expressions, and `178–203` uses them in structure eta/constructor reconstruction. This is computational metadata, not merely a field-name display table. |
| Instances | `Meta/Instances.lean:50–101` stores discrimination keys, value, priority, synthesis order and scope. `addInstance:283–304` computes these from the current environment. `registerInstance:328–330` also sets frontend instance reducibility. |
| Simplification | `SimpTheorems.lean:453–473` builds theorem indexes and can generate auxiliary lemmas during preprocessing; `708–729` installs entries in a separately scoped simp extension. |

The source registration APIs are **not** the receiving verifier's validation API. For example, registering a structure descriptor only writes extension data; it does not itself establish that arbitrary caller-supplied projection metadata matches the checked constructor. CLIENT1 must validate the recipe before applying such local metadata operations.

The inspected WHNF path does not request a proof that a registered function equals the intended projection: `mkProjFn` directly constructs its application, and `toCtorWhenStructure` uses those results as constructor fields. Therefore a merely propositionally equal function cannot be installed as computational projection metadata on that basis. A checked equality may justify an explicit rewrite or transport, but it does not supply the definitional/structural behavior assumed by raw projection and eta machinery.

### A concrete name-sensitive frontend gap

The pinned [Expr source](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Expr.lean#L1708) recognizes `outParam` and `semiOutParam` by exact names, at 1709–1714. [Class.lean:106–124](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Class.lean#L106) uses that test and instance-implicit binder information when determining output parameters.

[BuiltinTerm.lean:226–227](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Elab/BuiltinTerm.lean#L226) constructs constants named `OfNat` and `OfNat.ofNat` for numerals; lines 243–244 similarly use `OfScientific`. [Meta/Coe.lean:82–85 and 106–107](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Meta/Coe.lean#L82) constructs the exact `CoeT`/`CoeT.coe` and `CoeFun`/`CoeFun.coe` names.

Consequently a globally renamed `outParam` declaration with the same logical identity-function body need not be recognized by `Expr.isOutParam`. Likewise, storing a checked class under a hash name does not redirect a frontend's hard-coded `OfNat` lookup. Kernel name-equivariance, where qualified, does not imply frontend name-equivariance.

This is repaired by a separate explicit frontend-name interpretation, not by expanding the native allowed-axiom set or assuming every source name must forever remain globally canonical.

## CLIENT1: selected local presentation bridge

### Two environments and an exact correspondence

Let E_C be the selected mathematical content/evidence view with its exact foundation, native objects, proof selections and current local guards. Let E_P be an owner-controlled authoring environment using the qualified Lean frontend. They are not the same acceptance authority.

Maintain a finite map σ from E_P declaration/group/member names to exact E_C semantic references, and a separate evidence-use map recording the actual selected proofs/support used by imported theorem occurrences. Under the sibling's proposed PI1/rule-4 contract, canonical Judgment/Definition/Group descriptors continue to contain semantic JudgmentID theorem references, not ProofInstanceIDs. Only the separate WitnessTermDAG proof-value representation uses explicit proof-instance references. The representative map B and actual checked support record which evidence realizes semantic theorem references. Kernel-reserved seed names retain their required meanings. A qualified finite `FrontendNames1` inventory additionally assigns the exact local names required by the selected frontend—such as the inspected numeral/coercion/parameter markers—to their exact admitted declarations. That inventory is local frontend configuration, not a new global theorem namespace or a source of mathematical axioms.

For each imported declaration d, the bridge checks a normalization correspondence: removing only the specified presentation annotations and rewriting every native reference through σ yields d's exact admitted canonical type/body/group descriptor, with the applicable proof-instance selection recorded separately. An unknown reference, changed body, altered universe order, unexpected generated member or ambiguous name binding fails this correspondence. Equal printed types are insufficient.

The presentation environment can reconstruct an inductive group under its required local frontend name, rather than attempting to register a transparent alias as though it were an inductive class. The native group descriptor and every member/projection occurrence still map to the exact admitted group. A native reconstruction/check and exact descriptor correspondence are required; assigning the same source spelling to two distinct groups does not unify them.

The F rule that ordinary canonical binder information is explicit/default remains the receiving rule. E_P may restore finite binder annotations from its adopted presentation recipe, but normalization must remove them back to exactly the same canonical object. Such annotation recovery does not allow new omitted premises in exported native applications. Frontend instance reducibility is separately scoped metadata; it is not a change to HEIGHT1's native regular heights.

### Inert recipe, not plugin import

A local `ClientRecipe1` names the exact foundation/native profile, selected semantic/evidence roots, presentation-adapter/frontend image, fixed syntax profile, and bounded arrays of the following records:

- **Name binding:** local name, exact typed semantic reference and selected evidence reference when applicable. Conflicts require an owner-selected namespace or explicit refusal; no arrival-order winner.
- **Binder view:** exact declaration reference, precise binder path and one of the fixed binder-info codes. No executable default tactic, macro quotation or arbitrary source expression is admitted by this record.
- **Structure view:** exact group/type selector, ordered constructor-field indexes, local field labels, exact projection references and a finite parent/resolution DAG. Verify arity, indexes, constructor inventory and actual projection behavior, not just field types. For example, two same-typed fields cannot be swapped by an unchecked metadata claim. Raw `ProjectionFunctionInfo`, structure projection names and computational eta/WHNF registration require locally qualified definitional/structural correspondence with the actual native projection: preserve its exact group, constructor, parameter count, universe arguments and field selector. Validate any parent-projection composition through the qualified frontend facility that actually represents that path; do not encode a composite as an invented direct field index. Exact normalized body correspondence is an admissible sufficient route; any broader definitional check must be qualified for the registered operation's actual computational assumptions. A merely propositional equality is **not** authorization for this registration. It may instead be used by an explicit independently checked proof-carrying rewrite/transport, while the function stays an ordinary function. If the required computational correspondence is unavailable or exceeds budget, use explicit native projection syntax or decline the convenience.
- **Class view:** an admitted inductive/class reference and expected finite output-parameter information. After frontend-name/binder reconstruction, derive the actual class metadata with the qualified local API and compare it to the recipe. Do not create an axiom to make registration succeed.
- **Instance view:** exact admitted declaration/evidence reference, finite local scope and bounded priority. Recompute its discrimination keys and synthesis order from the actual local type/projection metadata. Do not deserialize a peer's prebuilt search tree as authority.
- **Simp theorem view:** exact admitted proposition/evidence, bounded priority, orientation and pre/post flag. Derive the simplifier entries locally. Arbitrary remote simprocs, tactic callbacks and environment-extension payloads are outside this recipe.

Labels and priorities influence local search, not truth. The initial syntax profile is an already owner-installed fixed frontend grammar. Custom mathlib notations/macros/tactics require a separately owner-authorized installed frontend extension or are expressed through explicit ordinary applications; arbitrary peer-provided source is not executed to restore convenience. This deliberately supplies useful class/structure/instance/simp support without promising every existing surface-language extension.

### Staged construction and bounded failure

CLIENT1 is local import/authoring work, not a new remote opcode or advisory-record kind. A remote recipe, if ever transferred as ordinary data, has no activation authority. The owner selects a finite scope and grants actual parsing, metadata, native and elaboration resources.

A concrete initial local envelope may select at most 4096 **exposed surface declarations** and 64 MiB of recipe/extension bookkeeping, with at most 64 metadata entries staged per transaction. This is not a bound on the entire declaration closure needed to construct E_P: a small surface can depend on substantially more declarations, native types/bodies, group metadata and frontend bookkeeping. Admission separately requires explicit finite count/byte/CPU/memory budgets for that complete reconstructed dependency environment, all within the same owner's aggregate resources. Existing locally shared dependency state may be reused only under its actual protected allocation and qualified correspondence. Missing closure capacity gives partial/declined import before claiming the selected surface usable. Neither the 4096 surface allowance nor the 64-MiB metadata allowance supplies free hidden dependencies. These are example counted defaults, not a measured practical mathlib working set.

The operation is:

1. Capture exact native roots/evidence, supported frontend/adapter identities and current local authority; acquire complete input evidence through the independent native path.
2. Establish σ and the kernel/frontend required-name bindings. Reject conflicts before installing any partial public authoring namespace.
3. Reconstruct the finite declaration/group environment in dependency order with selected binder views, exact bodies and universe arguments. Validate normalization correspondence and generated inventories.
4. Validate/install structure and projection metadata, then classes and instances, then the selected simp set. Use only qualified local registration code. Extension registration may create auxiliary declarations: capture their complete bodies and either account for them as new candidate declarations or remove their use by an explicit checked transformation. Do not discard them because they were created by the simplifier rather than an author.
5. Commit a complete scoped presentation view, or discard the failed staged view under ordinary local cleanup accounting. An incomplete class/instance import is not reported as a complete ordinary Lean environment.
6. Admit each local elaboration/tactic occurrence under finite resources. The resulting term must have no unresolved metavariables or prohibited placeholders and must expose all actual typeclass arguments, transports and proof dependencies.
7. Normalize/export the output and its actual new support to the selected native representation. Independent receiving checks, footprints, current protection and publication remain the only path to corpus contribution.

A checked native declaration can remain usable by explicit application when a presentation recipe is absent or unsupported. Conversely, a successful frontend elaboration is not evidence that the exported term will satisfy the receiving foundation or its actual axiom policy. Missing metadata, source-to-content disagreement, unsupported proof composition, native rejection and resource nondecision remain distinct diagnoses.

### Evidence selections and branch composition remain explicit

σ does not erase proof choices. Under F, one workspace using a compatible exact witness map can use the positive cases above directly. Joining incompatible witness selections requires the actual qualified composition mechanism; CLIENT1 cannot make two imported environments compatible by giving their theorems one display alias.

For the proposed PI1 proof-instance format, CLIENT1 uses two distinct normalization paths. Canonical semantic judgments, definition type/value descriptors and group descriptors retain JudgmentID references through σ; explicit ProofInstanceIDs are not inserted into those semantic identities. Separate WitnessTermDAGs for proof implementations preserve their actual explicit instance references. Semantic theorem references reached through types, definitions or groups obtain their actual checked representatives from B, and their representative dependencies/footprints remain in the selected replay evidence. Merely consulting the descriptor of a target JudgmentID does not require that same judgment's theorem constant or force the root proof instance into B.

A change in B can change actual checking context or support even when semantic DefinitionIDs and GroupIDs remain unchanged. The client must not copy a prior branch's declaration/proof certificate into the new environment solely because those semantic IDs match; the selected PI1 checking/cache contract must bind actual representative dependencies and require the appropriate new checks. This matters for the source's proof-computation/accessibility-recursion caveat as well as for exact policy footprints. Any local simplification or representative substitution is recorded as the actual newly checked evidence choice, not an unproved preservation of every source derivation. No canonicalization by popularity or unproved semantic equivalence is introduced here.

## Concrete obligations and remaining limits

The selected mechanism goes beyond "restore metadata later": it specifies two distinct environments, exact normalization correspondence, a separate frontend-name inventory, allowed recipe classes, validation order, projection safeguards, auxiliary-declaration capture and a native-only output boundary.

The representative source cases require the following future conformance observations; none is reported as executed:

- Export/application of `Finset.mem_range` with its actual range, quotient, instance and proof-field support; compare explicit application with the selected local simp/instance convenience.
- Preserve statement-level `Nat.le_trans` occurrences in the `Fin.castLE_castLE` case and expose actual selected evidence reached through types.
- Preserve the original List-setoid/Multiset/Finset nominal chain under a compatible import; distinguish a genuinely new cloned group and any separately checked bridge.
- Admit the safe `Quot.out`/`out_eq` path under the classical policy while rejecting the adjacent unsafe `Quot.unquot` path. Never infer an executable choice algorithm from logical acceptance.
- Show that names/binder annotations restored for outParam/numerals/coercions normalize back to exact admitted content, with ambiguous reserved frontend bindings refused.
- Reject a structure recipe that swaps same-typed projection fields or offers only a propositional equality for raw computational projection/eta metadata; permit that equality only through explicit checked rewrite/transport. Also reject a stale instance recipe, an unbounded/cyclic search configuration, and any remote executable callback.
- Account for simp-generated auxiliary theorems in the complete exported closure and charge all failed/incomplete staging work.

These cases establish a concrete compatibility target, not a coverage percentage. The unresolved broad mathematical-composition question is owned by the proof-instance analysis; the unresolved mathematical interface-transport question is owned by BRIDGE1. A usable client must integrate their actual accepted contracts rather than hiding those issues inside an elaborator extension.

## Sources

- [Frozen v3 concept](../../spec/OPERATIONAL-CORPUS-V3.md) and [F proof-composition restrictions](CP-001F-proof-identity-composition.md).
- [F complete producer/client source audit](CP-001F-lean-producer-client-path.md).
- [Pinned Lean class extension and registration](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Class.lean#L14).
- [Pinned Lean structure metadata and registration](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Structure.lean#L25).
- [Pinned Lean projection metadata](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/ProjFns.lean#L19).
- [Pinned Lean projection use in WHNF and structure eta](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Meta/WHNF.lean#L165).
- [Pinned Lean instance indexing/registration](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Meta/Instances.lean#L283).
- [Pinned Lean simp construction and auxiliary lemmas](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Meta/Tactic/Simp/SimpTheorems.lean#L453).
- The exact source links attached to each representative declaration and frontend name-sensitive operation above.
