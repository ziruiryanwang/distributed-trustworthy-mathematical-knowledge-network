# CP-001D cross-audit: integration and indefinite operation

Date: 2026-09-19. Reviewer role: mathematical-profile contributor independently reading the root integration and sustainability notes. This is a paper/concept audit; no implementation or executable test is claimed.

## Scope and reviewed drafts

- [Integrated operational contract](../../spec/OPERATIONAL-CORPUS-V1.md), read completely at 322 lines before the repairs requested here.
- [Autonomy and sustainability](../analyses/CP-001D-autonomy-and-sustainability.md), read completely at 122 lines before the repairs requested here.
- Compared with [mathematical native-exchange contract](../../spec/OPERATIONAL-CORPUS-V1-MATHEMATICS.md), including practical Lean-Native/v1, typed replay roots, scoped negative evidence, and local-client reuse.

## Initial findings and applied repairs

| Finding | Evidence and reasoning | Requested repair |
|---|---|---|
| Typed reuse path should not invent a judgment for every root | Integration's first independent-reuse step says to resolve the exact judgment. Definitions, opaque declarations, and groups deliberately have no invented JudgmentID, as the integration's own identity section correctly says. | Resolve the exact typed root/profile, kind-appropriate statement or declaration type, and selected ReplayManifest/closure. |
| Actual record declarations must not be relegated to advisory metadata | Sustainability's client paragraph lists “structures/instances for elaboration” among conveniences outside mathematical identity. The intended claim is valid for structure registration and instance-search metadata, but an actual inductive record declaration and an instance value used by a proof are checked mathematical objects. | Distinguish elaborator registrations/search metadata from the checked structure/group and instance-value declarations. |
| Core/practical profiles do not have automatic cross-profile content identity | Integration calls Lean-Expr-6/v1 a “conformance subprofile.” The mathematical profile binds all terms/definitions/judgments to exact LogicProfileID. Content in one does not become byte-identical content in the other by set inclusion. | Say separate core conformance profile, and retain explicit profile-bound re-export/replay for crossing profiles. |

These were integration clarity/correctness repairs, not evidence that the selected native replay architecture was incoherent. A targeted reread confirms all three repairs were applied: typed-root resolution in the reuse path; the distinction between structure/instance declarations and elaborator metadata in sustainability; and explicitly separate core/practical profile identities. This audit does not edit root-owned documents.

## Checks that passed at paper level

The practical profile is not replaced by the six-type example. Integration explicitly includes safe opaque bodies, mutual/nested inductive groups, projections, standard explicit foundation assumptions, and the reserved-name bootstrap qualification gate. It does not claim an already implemented exporter or a universal import of arbitrary compiled libraries.

The corpus has no human-intention fidelity decision, mandatory originating question, work-item relation, shared root goal, or in-system research scheduler. Search and maintenance queues operate on existing formal content and bounded service requests. Private research methods remain outside the acceptance relation.

Source commands, plugins, tactics, peer `.olean`, and downloaded checker binaries are absent from mathematical acceptance. The client path returns native data, reconstructs checked generated-name declarations in the local Lean environment, and keeps optional elaboration conveniences outside corpus authority. Missing bodies and same-judgment theorem alias expansion are explicit compatibility constraints.

Scoped opposite evidence is not conflated with invalid conditional mathematics. Integration correctly says that uninhabited hypotheses can support both sides soundly and that a basis incident requires a separately checked closed contradiction under a compatible dependency/foundation basis. No arbitrary negative notice immediately disables the corpus.

“Indefinitely” is consistently an architectural capability under recurring capacity and preservation assumptions, not a theorem of eternal survival. The sustainability note explicitly separates historical derivation, local usable stock, globally recoverable stock, and bounded observed views. It refuses a synchronized complete global state under arbitrary partitions.

Resource renewal preserves outstanding reservations, live storage, pins, and promises. Clock uncertainty and counter exhaustion fail closed or require explicit migration. A timer, key change, proof count, or model suggestion cannot mint remote authority. Physical capacity and actual supplied storage remain necessary assumptions.

The replication example makes independence explicit before using q cubed and does not treat different keys as independently surviving replicas. Lost exact bytes cannot be recovered from their hash. The note distinguishes exact-byte retention from a later mathematically related replacement.

Blockchain and SNARK discussions remain correctly optional. Neither a global ordering ledger nor a succinct checking certificate solves exact reusable content availability, mathematical usefulness, or global index completeness. The succinct-proof discussion correctly requires proof-bound footprint extraction, not only a bare kernel-acceptance bit.

The integration qualifies eventual successful import more strongly than eventual message delivery: an actual attempt must fit its finite deadlines and resource allowance. It does not claim useful/exponential growth merely from adding artifacts.

## Adjacent transport defect found and resolved during cross-review

The organization reviewer noticed that NativeRefutation was not a permitted replay root, so it could not silently become peer-readable through native closure capabilities. The selected resolution is now explicit in the mathematical companion: publish/import the negative proof's ordinary ReplayID; reconstruct and verify its exact scoped-opposition target locally; keep the envelope as optional bounded derived relation metadata. No generic CAS-read authority or extra root kind is introduced.

## Bounded interface-inventory follow-up

Read [the interface inventory](../analyses/CP-001D-interface-inventory.md) completely. Its exact proof/definition/group/opaque root tags and optional ProofID/JudgmentID projections agree with the mathematical contract. It correctly treats the scoped-negative envelope as local derived metadata and transfers the negative proof's ordinary ReplayID. It does not add a fifth root or grant generic CAS access. Common content types and the distinction between native CIDs and byte-manifest IDs agree.

Two final wording clarifications were sent to the root owner and are now confirmed applied by targeted reread. The integration's client paragraph says instance-search registrations and explicitly keeps actual instance values among checked declarations. The interface's Module paragraph says that a Module is a local/offline batch wrapper whose peer operations decompose into individual ReplayID roots: a ModuleID is neither a replay root nor automatically readable through a member's native closure. These preserve existing native-root and authority semantics; they do not require a new record kind or implementation feature.

## Hash-bound reread checkpoint

The following hashes identify the exact final revisions examined in this targeted follow-up, including the integration's updated completion-scope header and final paragraph. Those clauses correctly identify a cross-reviewed candidate concept while leaving practical implementation qualification and the ultimate long-term project goal open. Any subsequent changes are not represented by these hashes; the parent final manifest must identify final exact bytes.

| File | SHA-256 of reviewed bytes |
|---|---|
| `spec/OPERATIONAL-CORPUS-V1.md` | `A8E67017578E30D00B71C8425F25AFA753B84F7056DCC160B1B480C472B1EB61` |
| `notes/analyses/CP-001D-autonomy-and-sustainability.md` | `8F955CDADF9B2C1732E76FBFCF55AC6C0B0161D11134B9040FDB1DC4139AECE6` |
| `notes/analyses/CP-001D-interface-inventory.md` | `B045B7750818007A7FB16D8B11071A8B0E9A310B5BBEACA45EF6B188499C8B35` |
| `spec/OPERATIONAL-CORPUS-V1-MATHEMATICS.md` | `949E0428ABBFDB6637CF087F6FB518206309B3E0DA7D13B4C73CA99D07D6926E` |

## Remaining qualification, not paper findings

Actual bootstrap bytes and native-name inventory, codec/adapter correctness, theorem/opaque-body extraction, nested-inductive round trips, realistic library closures, storage crash behavior, capacity calibration, and large-network routing remain implementation qualification obligations. This review finds no claim in the reviewed documents that these have already been executed. Passing this paper review does not certify production soundness, performance, or indefinitely positive recoverable knowledge growth.

## Review disposition

No blocking conceptual contradiction was found in the reviewed no-intention scope, practical trust boundary, client reuse loop, typed-root interfaces, or conditional indefinite-operation claims. All three original integration repairs and both final wording clarifications are confirmed applied. No finding from this bounded review remains pending. This supports the designation **paper-operable concept with explicit qualification gates**, not production qualification or evidence of executed native/network conformance. Final snapshot hashes belong in the parent checkpoint.
