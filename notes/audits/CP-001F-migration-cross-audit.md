# CP-001F: independent migration and composition-boundary cross-audit

Date: 2026-09-20. Status: bounded independent concept audit; no implementation, Lean execution, proof replay, build, benchmark or exploit execution. CP-001E and earlier checkpoints remain unchanged.

## Scope and immutable review target

This audit examines [the foundation-evolution and migration analysis](../analyses/CP-001F-foundation-evolution-and-migration.md), reviewed at SHA-256 `F1718D33BB784B1C93AC07B8E91661723F8F6CE979D8CB4E59101A76297643CE`.

The review asks whether MIGRATE1 preserves the distinction between exact old evidence, independently checked target evidence, semantic correspondence, finite local authority, custody, and currently reusable status. It also checks the translation-cache boundary against the separately owned [proof-composition analysis](../analyses/CP-001F-proof-identity-composition.md). The composition note was initially reviewed at SHA-256 `F2D411289AA2C3E5085FA558D679161E6B68788BB2DFC9F0B310E25C0699D44C`; its author is repairing the independently reported external-witness collision guard.

The auditor owns the separate [producer/client source-path analysis](../analyses/CP-001F-lean-producer-client-path.md), but does not edit either reviewed note. This is a concept-level consistency audit, not a proof that an implementation satisfies the contracts.

## Finding M-CACHE: bind composition context or prove it irrelevant

**Classification:** a cross-plan memoization contract is underspecified, not a demonstrated native-acceptance bypass.

The reviewed migration note requires a key containing the exact source typed object, selected source-witness context, source and target encoding/foundation, translation-policy identity, and translator image/adapter. Those are necessary. They are not by themselves an explicit commitment to every input admitted by the proposed capsule composition route.

That route selects a transformed theorem slice T, retained background A, and exact source-occurrence-to-target-record maps. A source theorem reference may become an opaque capsule reference when it lies in T, but remain a target theorem reference when it belongs to A. This is an observable difference in target syntax, support and possibly target witness compatibility.

For a simple countercase, let an object d reference a source theorem s and let the exact source witness for s remain fixed. One admissible translation context can retain s as an external theorem; another can include s in an eligible capsule slice. The source bytes and selected source W are identical, and the same overall composition algorithm can be used, but the two candidate target bodies differ. Choosing a different allowed background witness map can likewise affect the context into which a cached candidate is composable. This countercase does not require the source proposition to be false or either target proof to be invalid.

The stated key is sufficient only if the translation policy already defines a total deterministic choice of all such boundaries and maps from its keyed input, or if a separately justified context-independence result applies. The reviewed text does not select either condition explicitly. Treating the cache result as a completed translation for a new plan could therefore misreport the plan's actual correspondence choice, or repeatedly produce candidates incompatible with its target replay. Independent target checking still prevents a false mathematical acceptance; it does not prove that the requested translation recipe was followed.

**Required repair before cross-plan memoization is selected:** choose one of the following contracts.

- Make the qualified translation policy deterministic and root-independent for every cached object, and specify that the keyed input completely determines its capsule/background boundary, target declaration map, universe handling and witness choices.
- Bind an exact immutable `TranslationContextID` covering all variable composition inputs: selected capsule slice/background boundary, occurrence-to-target-declaration choices, relevant retained target witness maps, and the interpretation/composition-rule version. A local content commitment is sufficient only when the exact bytes and references it commits to are available and unambiguous under the ordinary binding contract.

Under either contract, the result of a translation cache hit is exact candidate syntax with its actual dependency/correspondence data. It does not inherit target checking, current availability, target grant, footprint admissibility, publication or semantic-equivalence authority. The independent target-check cache retains its separate exact evidence/current-basis key and guards.

A conservative exact whole-context commitment is correct but may reduce cache reuse. A later dependency projection may omit a context field only after showing that changing it cannot change this cached result or the claim being reused. The spec must not obtain efficiency by leaving a genuinely variable input unkeyed.

## Finding C-BOUNDARY: source disjointness is not canonical judgment disjointness

**Classification:** a sufficient eligibility guard in the initial composition note missed a retained-background/root collision; ordinary final replay admission still prevents unsound acceptance.

Take source declarations

\[
a : \mathrm{True} := \mathrm{True.intro},\qquad
b : \mathrm{True} := a.
\]

Select T containing b only, and retain a in background A with its exact proof p. There is no source dependency from A back into T, and the proposition True has no theorem reference. But a and b have the same canonical JudgmentID j.

The transformed capsule for b still references the retained theorem at j. The newly emitted root wrapper q requires W(j) = q, while the retained background requires W(j) = p. Source-name disjointness does not make this an admissible replay. This remains a boundary issue even though the internal capsule chain itself is acyclic.

The composition owner and root reviewer independently confirmed this case and selected a repair: check canonical judgment-domain compatibility of the entire retained witness closure with every newly emitted root pair. Their proposed sufficient initial guard uses disjointness, and expands T only after a fresh bounded eligibility scan; otherwise the route declines. The repaired bytes require a fresh audit/hash before this finding can be marked closed.

MIGRATE1's reference to a chosen composition algorithm must mean this actual final guard, not only source-level acyclicity or the existence of a checked opaque capsule. Re-expression can also create new canonical target collisions, so the guard is evaluated over the constructed target interfaces/maps.

## Reviewed migration properties with no defect found in this scope

### Target validity is not source semantic preservation

The note explicitly labels the initial result `REEXPRESSED_AND_RECHECKED`, rejects equality-of-name/type as a seed-map justification, and requires a separate checked interpretation or bridge for a stronger preservation claim. An old source accepted by a now-suspended checker can therefore supply inert candidate syntax without transmitting old acceptance authority. A target kernel check establishes only the reconstructed target judgment under the actual target basis.

This distinction is essential when a seed operation or representation changes. For example, the pinned String source path has materially different structure from merely renaming an old constructor. Target checking alone would not prove equality with the old operation; the note does not claim otherwise.

### Source acquisition, byte binding and collision handling

The note requires exact selected source bodies/witnesses, an exact supported old codec and a finite source DAG. It also says that an ambiguous old ID after a hash collision is insufficient. Read together with the inherited binding contract, migration may not select one of two colliding old payloads by popularity or by successful target checking.

For clarity in any future operational schema, distinguish acquisition of an existing source Native2 closure from fallback acquisition through Lean producer artifacts. The producer path is an evidence-acquisition method, not permission to substitute a newly exported proof with the same displayed statement for the exact old selected ProofID/ReplayID. If fresh producer output does not bind to the selected old objects, it is a separately identified new import/correspondence candidate. No contradiction was found in the present exactness requirement; this is an implementation qualification case.

Likewise, a collided identifier must not be the sole cache or source-scope selector. Existing incident evidence must quarantine the ambiguous binding; a migration that proceeds requires separately retained unambiguous occurrence/byte binding sufficient to resolve every selected reference. If that is unavailable, the correct result is incomplete/unsupported migration, not arbitrary disambiguation.

### Custody is not translated by successful proof checking

The source migration pin, source custody promise, target staging allocation and target custody scope are distinct. The source pin remains finite even when ordinary source custody is released. A changed target FoundationID generally changes JudgmentID, so a new target proof does not discharge an old exact-JudgmentID recovery promise automatically.

The note requires explicit owner release and does not infer deletion from COMPLETE. This avoids a delete-first upgrade and avoids converting exact-source custody into unspecified target semantic similarity. The lack of a universal preservation bridge is therefore not concealed in the storage transition.

### Historical completion is not current reusability

TARGET_CHECKED requires protected complete target evidence, native assessment and current guards at its commit. Publication uses ordinary separately authorized operations. The honest-status section separately reports historical checked results, currently reusable results and actual publication. Thus an incident, grant expiry or failed publication cannot be repaired merely by leaving an earlier COMPLETE row unchanged.

Future status implementations must preserve this separation: a historical completed migration is not a perpetual positive reuse pin. The current text supplies that distinction; no implicit perpetual protection claim was found.

### Crash and budget claims are conservative

The note charges source reads, target work and temporary double storage; requires durable target staging before a positive commit; terminalizes interrupted claims conservatively; and requires fresh authority without refunding already spent work. It does not claim that a remembered progress cursor reconstructs missing data or resurrects an expired source pin.

Surviving exact target objects and a still-applicable historical check may remain useful under their surviving allocations/current guards. That is separate from restarting the interrupted plan or declaring its requested publication complete.

### Cost and growth claims have the needed scope

The quadratic aggregate rewrite example is explicitly a linear-growth/whole-corpus-per-release model, not a universal migration lower bound. It separately notes the geometric-growth case and does not infer actual Lean timing. Incremental root selection and exact memoization can remove repeated work, but cannot turn an unsupported target primitive, missing source proof, cold byte volume, or changed checking authority into an O(1) operation.

New FoundationIDs generate representationally new JudgmentIDs. Separating these from mathematical discovery avoids a false exponential-growth claim while retaining truthful counts of actual acquired evidence.

## Residual qualification obligations

- Supply and review the actual supported translation rule for a declared source/target pair; this audit does not supply a universal foundation translator.
- Establish exact old-byte/reference binding after any real hash failure, or decline that affected migration scope.
- Demonstrate target-collision handling and context-keyed memoization on independently selected compatible and incompatible branches.
- Check target grants and incidents again at every ordinary positive use/publication transition, not only when native checking once succeeded.
- Measure selected migration work, temporary storage and reusable-prefix benefit over a declared realistic slice before making affordability claims.

## Repair review and final bounded disposition

The repaired migration note was reread in full at SHA-256 `C56B83B0FC99B9B8D174FCEF1D0246D31DC9B03A763BFC5E35ADD0C2B991A45A`. It now explicitly keys `TranslationContextID` over the finite transformation slice, retained background, capsule/retained occurrence policy, selected target background replay/witness maps and already available source-to-target references. Its context cannot depend circularly on the output's still-unknown ID. Omission requires a qualified deterministic independence argument; a cache hit remains only candidate syntax/correspondence. **M-CACHE is closed as a concept-specification finding on these reviewed bytes.** This does not assert an implemented cache or a measured hit rate.

The repaired composition note was reread in full at SHA-256 `9934E5ACEA2872C7B9E7366D8EBFCD711270773BBBAB5F7774006E7F13B65878`. It requires the complete retained background witness domain to be disjoint from every selected wrapper JudgmentID, scans types, bodies and generated-interface support, requires bounded slice expansion to repeat every eligibility check, and preserves the final ordinary exact-map check. **C-BOUNDARY is closed for this explicitly restricted capsule route on these reviewed bytes.** The guard does not establish universal proof-dependent-context composition.

The same bounded composition reread found no additional defect in the displayed subset-universe literal-expansion argument, the unchanged-root-JudgmentID claim under its eligibility assumptions, or the explicit `regular 0` versus derived-height paper family. The latter source observations were supplied by the composition reviewer, not independently reproduced as runtime tests here. The selected HEIGHT1 integration explicitly uses a new native-rule/foundation identity and applies the same checked derived rule to ordinary transparent bootstrap definitions; it does not silently reinterpret the old certificate basis.

The reviewed migration concept has the essential authority and custody distinctions. This audit found no direct path that turns old acceptance, source signatures or advisory correspondence into target native acceptance. Its two recorded findings are repaired within their stated scope. Residual translation, binding, real-library compatibility and resource qualification obligations above remain. This is bounded concept-audit closure, not proof of release readiness, universal translation completeness or evidence of an executed exploit.

## References

- [Reviewed migration note](../analyses/CP-001F-foundation-evolution-and-migration.md).
- [Reviewed proof-composition note](../analyses/CP-001F-proof-identity-composition.md).
- [Producer/client source-path note](../analyses/CP-001F-lean-producer-client-path.md).
- [Frozen V2 operational contract](../../spec/OPERATIONAL-CORPUS-V2.md).
- [Frozen native-scaling and exact witness-map contract](../analyses/CP-001E-native-scaling.md).
- [Frozen collision and opaque-declaration rules](../../spec/OPERATIONAL-CORPUS-V1-MATHEMATICS.md).
