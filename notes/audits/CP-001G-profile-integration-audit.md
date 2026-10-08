# CP-001G: independent profile and integration audit

Date: 2026-09-20. Auditor role: `commons_independent_audit`, independent of the root-owned profile-binding/integration documents and the structural-retrieval author. This auditor authored the PI1 composition note; the mathematical core of that note is independently reviewed in [the separate composition audit](CP-001G-composition-cross-audit.md), not self-certified here.

Scope: exact type/schema/profile bindings, proof-root consumers, indexes/cursors, group ownership and closure/support boundaries in the G integration. This is a document/source-contract audit. No network service, native replay, executable model, exporter, benchmark or implementation was run.

## Reviewed versions

| Document | SHA-256 of reviewed version |
|---|---|
| [Profile and consumer bindings](../analyses/CP-001G-profile-and-consumer-bindings.md) | `5492C0919199D4DADD33D11ED6FF1FF6AD45C7AF544F51895D1558BC2F7917A8` |
| [V4 integration](../../spec/OPERATIONAL-CORPUS-V4.md) | `F2404DFB0EFA87F47EDF2A0762E404C60B76B7A5A0DD628F56B6694AB912E17D` |
| [Structural retrieval, integration paragraphs](../analyses/CP-001G-structural-retrieval.md) | `502054E55BBCD4DF9F50294326019F7BEB40A15A12B53AD5AF50203822571980` |
| [PI1 composition and consumer table, consistency input](../analyses/CP-001G-proof-instance-composition.md) | `22ACBD948A92084226A02918AE5D85E50CF71F3425E02A4972A9FB5ABEF9F5C7` |

The complete root profile-binding and V4 documents were read. Relevant inherited V1/2/3 record/authority rules, exact-routing group-map/cell/lease/GC contracts, PI1 consumer contracts and current STRUCT2 integration paragraphs were compared. This audit is not a replacement for the separate detailed extractor/query-recall audit.

## Summary disposition

No remaining mathematical-acceptance or disclosure-authority bypass was identified in the reviewed integration. A concrete same-type/schema advertisement contradiction was found in concurrent drafts and repaired before this disposition. A routing-holder foundation-adoption ambiguity and minor FULL_EXACT capability wording were also clarified. All findings in this audit are closed at the focused final addendum below.

These conclusions are bounded by the documents and cases below. They do not establish implementation correctness, practical library coverage, native checker soundness, measured retrieval quality, or global discoverability.

## Findings and dispositions

### PI-G-INT-01: two meanings for ProviderAd schema 2

**Finding in earlier concurrent drafts.** The structural document at hash `7A05BA4598D613E0A26FA7E0BDD7CAC88849BA77CC7C6F8770EE20B877988670` allocated `0x8022/2` as K4-only, with a direct `0x8124/1` structural-descriptor anchor. The root binding assigned that same type/schema to all code-4 K0/K1/K2/K3/K4 ads with a `0x8111/3` public-root anchor. It also allowed service-specific capability sets, whereas the structural draft required a complete routing/group stack even for a structural query.

**Why it matters.** Typed content identity must select one exact grammar/meaning. Two honest implementations following different selected notes could reject one another's ads or parse the same position as different typed content. A later native proof check cannot repair missing interoperable discovery. This was a specification blocker, not a theorem falsity result.

**Repair reviewed.** Structural version `502054...` uses the root's one exact schema-2 payload for all F4 keys. K4 binds the chain

```text
ProviderAd2 -> PublicIndexDescriptor3 -> StructuralDescriptor1
         \---------- same exact InstanceReplay ----------/
```

The final structural record must contain the exact K4 token, foundation and ExtractorID, and its semantic target must correspond to that exact replay root. Query, route and grouped-service capability sets are separately stated. A direct structural-descriptor anchor is no longer an alternative interpretation of that ProviderAd type.

**Disposition:** resolved in reviewed versions. No frozen F record was edited or reinterpreted.

### PI-G-INT-02: routing syntax support is not foundation adoption

**Finding.** An earlier phrase required the actual adopted/advertised foundation for PI1 content service without clearly distinguishing a native receiver from a routing-only metadata holder. Read too broadly, it would make routing admission require native adoption/import, contrary to the nonrecursive metadata-service boundary.

**Repair reviewed.** The root binding now explicitly requires adoption/qualification for independent native acceptance, while a routing-only holder requires the negotiated codecs and local storage authority but need not adopt the mathematical foundation, import its bootstrap, fetch its anchor, or check its theorem.

**Disposition:** resolved. Codec support, role willingness, local mathematical adoption and checked theorem acceptance remain four separate predicates.

### PI-G-INT-03: FULL_EXACT branch capability wording

**Observation.** STRUCT2's integration paragraph preserves the "old FULL_EXACT" cap5+6 branch while describing new FULL_FEATURE cap5+6+7+8 groups. The root profile correctly requires capability 8 for all F4 PI1 service, including F4 exact-group anchors. The lower note should explicitly distinguish frozen F3 FULL_EXACT cap5+6 from F4 FULL_EXACT cap5+6+8.

**Disposition:** resolved by the focused post-review amendment recorded below. This is not permission to accept a code-4 exact-group ad without capability 8.

## Exact identity and native evidence boundary

The root selects NativeRules code 4 and a new FoundationID. This is consistent with PI1's changed replay/witness-reference/generated-name contract. It does not pretend that old rule-3 artifacts preserve their IDs across the foundation change. Semantic schema-2 objects are retained only with their actual F4 identities and references.

ProofInstance `0x0023/1` is distinct from legacy Proof `0x0014/2`; InstanceReplay `0x0015/3` is distinct from Replay2. Root tag 4 is admitted only in the new union. Witness-term instance references never become an unnoticed semantic NativeTermDAG alternative. This blocks the simple type-confusion path "insert a PI ID in an old ProofID slot and trust the old verdict."

The mathematical module and opposing-evidence consumers use new schema 3 records and exact instance/replay root checks. An opposing proof still has the same-context negation requirement. Neither a negative proof ID nor a status observation establishes unconditional inconsistency when the hypotheses differ.

The V4 reciprocal trace has no direct advertisement-to-acceptance edge: each receiver must acquire its exact selected evidence, check under its own adopted foundation, establish protected availability/current policy, and then perform an actual checked application. The trace does not smuggle in a common research goal or global latest-version authority.

## Public descriptors, evidence alternatives and index cursors

The schema-3 public-root descriptor has one fixed five-field payload. Its optional judgment field is present exactly for proof-instance roots and equals the instance target; all roots bind the exact replay. A group root may expose a constructor structural view without inventing an independent constructor proof/declaration root.

The optional structural hint is a typed ID, not generic CAS-read authority. Structural query pages carry their bounded descriptor payloads inline. Native source types and proof objects remain accessible only through the exact permitted root/export scope. Unavailable hints can be ignored or pursued through separately paid public search; a hint cannot authorize reading private metadata.

Exact-judgment rows are `0x8111/3`; structural mode-6 rows are `0x8124/1`. Their ordering is over their own actual descriptor IDs. Snapshot/cursor commitments bind mode, result-record schema, predicate/extractor/planner and the existing holder/scope. Thus a cursor from one descriptor universe cannot silently resume in the other. This matters even though both record kinds are colloquially called descriptors.

Evidence-family selection and deduplication retain `(ProofInstanceID,InstanceReplayID)` rather than merely JudgmentID or instance ID. Consequently changing B without changing the proof body cannot silently merge footprints, cached checks or custody obligations. Multiple structural views sharing one root also do not collapse solely because the native root matches; they are distinct query/index records when their exact bytes differ.

A complete query scan remains a statement about the named provider snapshot and selected predicate, not all mathematical relevance or the global network. Budget exhaustion leaves a matching/unprocessed row at its exact continuation boundary. Pattern matching and source-type acquisition cannot discharge native premises.

## Advertisements, group maps and stale ownership

ProviderAd2 carries the exact typed root-descriptor and replay IDs under F4. For K4, the publisher's actual structural anchor supplies the token. A holder can check the bounded record shape, key/ad kind, peer/signature and local authority without obtaining the anchor. It therefore cannot certify mathematical eligibility; that remains a producer obligation and later receiver check. This distinction avoids both hidden native imports during route admission and false truth claims from signatures.

The map `0x8023/1` retains its exact operational cell-bearing Patricia grammar. A new key/ad domain is explicitly selected by immutable group mode, foundation and negotiated profile; no old F3 group's bytes are reinterpreted as F4 membership. The original cell/provider key and collision check remain, and the K4 record remains well within the inherited per-node bound. This is contextual operational bookkeeping, not a native representative map.

Operation 16 fixes FULL_EXACT/K1; operation 20 fixes FULL_FEATURE/K4 and its ExtractorID. Operations 17-19 use the retained group's mode/foundation/extractor plus authenticated owner, exact expected root/version, lifecycle and lease. An ordinary PUT/DROP cannot bypass group ownership. A signed ad grants no mutation authority by itself.

The inherited delayed-GC fence still names exact old group and row/storage generation. Reusing a cell/provider position under a new group cannot make the old sweep delete the replacement. Closed/expired but unreclaimed rows, snapshot-held state and empty/uncertain groups remain charged. The new group type does not make renewal global, merge different holders' authority, or remove ancestor-marker refresh costs.

Feature-scope renewal requires every actual grouped token to remain supported by an eligible public descriptor in that exact scope, not merely one surviving theorem somewhere. A feature bug can impair recall and require index rebuilding; it cannot clear a mathematical checker incident or assert a missing theorem's acceptance.

## Status, advice, archives and custody

Status uses `0x800A/3` with the exact PI root union and proof-instance/judgment options present only for tag 4. Its signed cut is a local historical observation. It does not bypass the receiver's current evidence/incident/availability guards. NET2 admission epoch retains its original operational meaning.

AdvisoryManifest/LibraryViewPage/CollectionGuidePage have explicit schema-2 allocations under F4. The manifest permits only its listed view/guide kinds and exact page types. Theorem target references remain semantic JudgmentIDs; replay hints are schema 3. Thus neither a proof-instance selector nor a presentation recipe becomes semantic syntax or remote executable metadata through an old advisory field.

BUNDLE1, generic typed-CID inventories and archive byte encodings can retain their layouts because the new eligible-type domain and root scope are explicit. Their actual permitted closure is PI1's exact traversal, including its B-map and witness-term nodes. A same-target alternative proof outside that traversal is not readable or retained under the root merely by having the right type.

The offline archive's root schema identifies the required reader; its foundation identifies the native basis. Neither field authorizes installing that software. Complete exact bytes and independently adopted compatible checking material remain prerequisites to local acceptance.

Custody and use pins commit exact replay roots. Replacing one witness with another proof of the same statement does not discharge a promise to retain the original replay. Incidents and current-use summaries include binding-relevant maps/terms/foundation objects, not only leaf theorem IDs. This prevents a decoder/map incident from being incorrectly cleared because the visible JudgmentID is unchanged.

## Paper adversarial cases examined

| Case | Required outcome under the reviewed contract |
|---|---|
| F4 is advertised without PI1 capability 8 | Unsupported profile/codec; no inferred native support |
| ProofInstanceID appears in a legacy Proof2 field | Schema/type mismatch; no old certificate transfer |
| Public descriptor's target differs from its named instance | Descriptor binding failure after required exact inspection; no proof of the claimed target |
| Structural cursor reused for an exact-root descriptor scan | Snapshot/mode/schema mismatch; no skipped or relabeled rows |
| K4 ad points to a structural hint without that token | Invalid publisher binding/false lead, never native theorem acceptance |
| Routing-only holder sees a new F4 key | Bounded untrusted metadata handling, without bootstrap/anchor fetching |
| FULL_EXACT group receives K4 | Atomic group mutation fails before owner/root/version changes |
| FULL_FEATURE group receives another extractor's K4 | Exact extractor mismatch; no in-place group reinterpretation |
| Old closed group's sweep reaches a replacement row | Generation/ownership fence prevents deletion of the new row |
| PI body unchanged but representative map replaced | Different replay/context; recompute actual support and required checks |
| Root scope is used to request unrelated alternative proof bytes | Scope membership denial; type similarity is insufficient |
| Advisory manifest names an unlisted structural/recipe object | Reject member-kind/type binding; no extended read or execution authority |
| Export archive names a checker distribution not locally adopted | Remains inert input; no automatic installation or acceptance |

These are logical traces over the selected record/authority rules, not executed conformance tests.

## Remaining qualification boundary

The concept now gives consistent typed contracts for the new evidence family and its main operational consumers. This audit does not prove that a future implementation obeys them under concurrency, crashes, malformed input, native computation, feature floods or persistent storage faults. The same exact cases need implementation qualification after coding is authorized.

The root's current-knowledge and growth limits are appropriately qualified: a node has finite evidence and observation scopes, independent providers can be unreachable, and a complete proof can be too expensive to acquire or check. These are not weakened by the new format, and the document does not promise universal recall, optimal proof choice, permanent preservation or exponential novelty.

## Focused final addendum

The STRUCT2 author clarified that frozen F3 FULL_EXACT uses cap5+6 while new F4 FULL_EXACT uses cap5+6+8. The amended paragraph was reread directly at STRUCT2 hash `28A766D3DC505DE72032121024535A75B7D7BDBB49E435E47B636532165A55AC`. FULL_FEATURE remains cap5+6+7+8; its immutable mode is not inferred from a submitted row. PI-G-INT-03 is closed. The final contract has no remaining open finding from this profile/consumer audit.

This focused closure covers that exact capability clarification, not arbitrary subsequent revisions or execution qualification. The earlier hash table records the principal review cut and this addendum records the later reviewed delta.

## Final editorial integration check

Reread the final V4 and profile-binding documents, the checkpoint/navigation/disposition updates, and the selected mechanism status/registry headings and audit links. The final changes identify the selected paper specification and completed bounded reviews; they do not claim executed native/network qualification. V4's precedence now explicitly gives the profile-binding note authority over operational codecs and each mechanism note authority over its algorithm, while leaving an unresolved contradiction a defect rather than implementation freedom. No inadvertent change to the reviewed evidence, authority, schema or support semantics was found in this editorial cut.

| Final selected file | SHA-256 |
|---|---|
| V4 integration | `83CA494F72319691E2FBD72348ABC6523F67B940D597A2A672A2F17AC94DE3B0` |
| Profile/consumer bindings | `456FC9876D73F90CACF456BA0F55166F25F2ABB2FCDAEF05CAE5A82B52A65EED` |
| PI1 composition | `0E1D443FBF13727A0011BD101135BAADD79F48074137B90E5CC2FCAF63A34E3E` |
| STRUCT2 | `1F295806C580224811C10A0A8273A53D35C0FDDC7D8085EBC5F9F224F47CDDCA` |
| G checkpoint | `279B764C3FFBE7228D419FB03733E864214C2783C9C1E855D2A676C69EE53C5F` |
| G audit disposition | `32D362126AD5FB6BF39CF19D0EBDDDB236EF6F524DD36FDA2FC2AC91E7CF8F18` |

The client audit now exists in `notes/audits/CP-001G-client-cross-audit.md`, with its relative analysis link adjusted; the disposition and client mechanism link to that location. This check covers navigation/status integration, not a new independent reassessment of the client author's projection repair or the other reviewers' entire source investigations. CURRENT-DESIGN correctly points to V4/G and remains explicitly mutable/outside frozen manifests. The root's final document/integrity pass still must create and verify the referenced G manifest after this last audit write.
