# CP-001H independent audit: complete export and group recovery

Date: 2026-09-20. Auditor: `commons_reciprocity`, independently of the EXTRACT1 author. Scope: specification and read-only pinned-source review. No implementation, extraction, build, native replay, proof execution, test or benchmark was performed. Frozen G and earlier files remain unchanged.

## Audited revision and verdict

Read [EXTRACT1](../analyses/CP-001H-complete-export-and-group-recovery.md) in full. Audited SHA-256:

`48ED502D1C9D08378452EC62AC1639DE8D05AEC797CE3C549097971963B9C369`.

No blocking contradiction was found in its collection/candidate/native-check boundaries, two-map normalization, source cache keys or guarded group-recovery proposal. Its two recovery routes are explicitly candidates, and neither source-record possession nor a claimed source build supplies receiving authority.

One nonblocking inventory-completeness clarification was recommended: name `InductiveVal.isRec` and `isReflexive` explicitly in the source-versus-derived inventory comparison, along with the already required `numNested`. It was subsequently repaired and checked as recorded below. The pinned restoration path preserves all three fields.

This audit does not demonstrate that an actual complete mathlib cut has been exported or that completed-record recovery always yields a descriptor with the original input's exact syntax. The note correctly declines those stronger claims.

## Source cut and body availability

The immutable complete-cut requirement is appropriate. A source declaration name without its actual selected body/kind cannot distinguish a theorem's complete record from its public axiom-shaped projection. Changing lookup results during traversal would also make a single declared cut ambiguous.

The note preserves the frozen full-private producer boundary and the separate capture route. It also acknowledges that combined imports can coalesce same-name/type theorem bodies, so an absent alternative cannot be recovered merely from its statement. Both points matter operationally even when political attribution is postponed.

Source names are used only to resolve an exact selected source graph before normalization. Deriving its dependency order before quotienting theorem statements avoids confusing a legitimate earlier source proof with the selected root's representative. Candidate references and native current-use support remain separate claims.

## Semantic and witness normalization

The `sigmaS`/`sigmaI` distinction agrees with frozen PI1. A semantic type/value/group descriptor uses semantic theorem judgments; every theorem occurrence inside a witness expression uses its actual proof instance, including annotations and binder-domain expressions. Following an ordinary declaration from a witness does not change that declaration's internal grammar.

The conventional export of an ordinary closed source theorem into an empty contextual telescope is explicit. It is not silently identified with a judgment that splits the same closed Pi expression into a nonempty telescope and conclusion. Explicitly contextual client roots retain their own precise split, and each witness is closed once.

The admitted normalization operations are narrow: ordered universe names become indexes; source names become the exact kind-appropriate references; admitted binder/metadata/let/hint fields follow their selected normalization. Arbitrary delta expansion or proof-argument erasure is excluded. The cited MData typing/WHNF cases justify only that expression wrapper's erasure, not the removal of arbitrary term-level annotation functions.

Open DAG subterms retain scope obligations despite physical sharing. Exact universe arity and explicit substitutions also remain binding; they cannot be reconstructed from printed names or guessed usage.

## Independent group-record source inspection

Directly read pinned Lean commit `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`:

- `Lean/Declaration.lean:261–300` provides `InductiveVal`'s parameter/index counts, ordered `all` and `ctors`, `numNested`, `isRec`, safety and `isReflexive`.
- `328–342` provides the constructor's owning inductive, index, parameter/field counts, type and safety.
- `348–388` provides recursor-rule constructor selectors/field counts/RHSs and recursor group/count/K/safety information.

These are substantive inputs to completed-record recovery. An encounter order, source suffix or public frontend structure label is not an alternative source for them.

Directly read `kernel/inductive.cpp:1182–1348`:

- `mk_aux_rec_name_map` derives nested auxiliary recursor names using the **first original inductive** and an increasing positive suffix; the order follows the actual expanded native inventory.
- `check_no_nested_aux:1222–1232` explicitly rejects both constant names and projection structure names under `_nested` in supplied input expressions.
- `add_inductive:1235–1255` checks closed input expressions, performs uniform-occurrence checking and nested elimination, and returns the ordinary generated environment directly when there are no nested auxiliaries.
- For nested cases, `1257–1314` starts from the prior environment, restores the original ordered group list, restores constructor types, and restores ordinary/auxiliary recursor types, selectors and RHSs. Temporary auxiliary type records are not simply exposed as external types.
- `1315–1345` checks the restored nested applications and the rewritten constructor types, recursor types and rule RHSs in the resulting environment.

These observations support EXTRACT1's stated candidate-recovery route and exact replay obligations. They do not prove that the completed record syntax is identical to the original `inductDecl` input or that all retained environments contain every needed source artifact.

## Clarification C1: derived inductive flags

At `Declaration.lean:283–300`, `isRec` and `isReflexive` are explicit fields. The restored inductive record at `inductive.cpp:1297–1300` retains `numNested`, `isRec`, safety and `isReflexive`, along with the ordered group/constructor information.

The note already requires the source `numNested` count and several exact generated fields. Explicitly include the remaining derived inductive flags in the source-correspondence comparison or specify a qualified derivation that establishes their match. This is an exact-record/interface completeness clarification, not permission to trust a publisher's flags as native truth.

If a source and independently reconstructed target disagree on such a field, the stated exact source correspondence is not established. Native acceptance of the independently reconstructed target is a separate question and must not be revoked merely because a stronger source-comparison route failed.

## Captured input versus completed records

The captured-input route has a direct descriptor candidate but still needs the actual completed generated inventory and fresh receiving reconstruction. Capturing only the input would not itself supply a check of what the source operation generated.

The completed-record route properly starts from the actual ordered `all` list and checks matching records, ownership, index and universe/parameter contracts. Mapping this group's type formers into the group's local-reference grammar must not capture external groups or treat constructors/recursors as local type-former indexes.

Both routes preserve actual order. They need not choose the same candidate syntax when their retained inputs differ, and the note does not pretend otherwise. Generated native rules are derived by the receiver rather than accepted as trusted sender-supplied `RecursorVal`s.

The exact comparison can be conservative. A syntactic mismatch under the allowed normalization means that this **exact correspondence predicate** failed. It is not a proof that no weaker checked correspondence or useful mathematical target exists. EXTRACT1 states this distinction explicitly and therefore does not overstate the effect of its strict inventory check.

## Cache and incremental-work boundary

The candidate-cache key binds the actual selected source input, target foundation, normalization/codec/recovery interpretation, contextual split and direct substituted reference boundary. An unchanged source name or file expression does not freeze the referent's identity. This is the correct reason that `def d := h` must be reconsidered when h's actual mapped referent changes.

Direct dependency identities permit unchanged candidate bytes to be reused without a global workspace-revision key. They do not make a source-correspondence certificate or native acceptance certificate reusable. In particular, if a source generated inventory or a target B realization changes while some candidate input descriptor remains the same, the independently required inventory/native checks still apply.

The cost statement is appropriately limited to compatible incremental candidate construction. Changed mappings can propagate through many IDs. Native conversion, source recovery, group generation and representative replanning are charged separately; a small source edit is not promised to have constant total cost.

## The REDUCE1 conversion boundary

EXTRACT1 correctly states that a complete candidate can fail native replay. The [REDUCE1 paper family](../analyses/CP-001H-proof-computation-and-reconstruction.md) makes that limitation concrete: the same semantic definition can use an opaque-backed canonical accessibility representative and no longer support the original fixed reflexivity proof's conversion. No changed group interface is necessary for that obstruction.

Consequently candidate completeness and native validity must remain distinct from original-body preservation and selected-conversion preservation. A repaired proof of the same target can establish target validity without being the original transformed source body. EXTRACT1's third success state names a **stated scope of correspondence**, not a universal all-conversions guarantee; H integration should retain that explicit scope when using REDUCE1's finer outcome predicates.

The appropriate response is a new compatible B with renewed checks or a newly checked equality/transport proof, as separately specified. Opaque declarations do not become transparent, source imports do not confer acceptance, and the source rank argument does not supply missing computational conversion.

## Conclusion and unperformed qualification

The inspected source supports the proposed collection and group-record recovery mechanisms, with strict independent reconstruction and mismatch reporting. C1 was the only requested clarification in this bounded review and is closed below. The following remain unperformed obligations: complete source-cut acquisition, broad practical library recovery, candidate encoding, actual generated-inventory comparison, full native replay under selected B, frontend usability and measured incremental costs.

## Clarification closure

On 2026-09-20, reread the amended source-field and generated-inventory passages in EXTRACT1 revision:

`82A57C2C808D57941D565BE2111797C73293537C4ABE9B525D2E66951E8E47DB`.

They now explicitly list `numNested`, `isRec` and `isReflexive` among the compared fields, while stating that a derived-flag disagreement fails the exact source-correspondence claim rather than automatically invalidating an independently checked target. C1 is closed for this inspected revision. No further issue was identified in that focused reread.

## Sources

- [Audited EXTRACT1](../analyses/CP-001H-complete-export-and-group-recovery.md), hash-bound above.
- [Pinned Lean native record definitions](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Declaration.lean#L261).
- [Pinned nested restoration and rechecking](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/inductive.cpp#L1182).
- [Frozen complete producer analysis](../analyses/CP-001F-lean-producer-client-path.md).
- [REDUCE1 computation/reconstruction analysis](../analyses/CP-001H-proof-computation-and-reconstruction.md).
