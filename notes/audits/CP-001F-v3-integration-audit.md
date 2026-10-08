# CP-001F: independent v3 integration and exact-routing coverage audit

Date: 2026-09-20. Status: bounded integration and exact-routing review complete, with the repaired-byte dispositions below. Concept/specification only; no implementation, native execution, network execution, builds or benchmarks. Earlier pending cuts are retained explicitly as review history, not current open findings.

## Reviewed scope and initial bytes

The initial full review target is [Operational mathematical commons v3](../../spec/OPERATIONAL-CORPUS-V3.md), SHA-256 `B66889CD31835D3D3C07F1C93D1D042697982F0421CD028870128F08026B47CC`.

This audit owns the integrated HEIGHT1/native identity, capsule restrictions, complete-source/receiver boundary, migration-cache integration, routing-registry/capability bootstrap, and forthcoming exact-routing coverage contract. A different reviewer owns the full base ROUTE1 audit. Reviewing the routing-registry seam here does not duplicate that review or assert independent verification of every base routing algorithm.

The prior [migration/composition cross-audit](CP-001F-migration-cross-audit.md) records the exact reviewed source-note hashes, countercases and repaired M-CACHE/C-BOUNDARY findings. This integration review checks that v3 has not weakened those repairs.

## Initial integration checks

| Boundary | Reviewed result at this cut |
|---|---|
| Native hint identity | HEIGHT1 uses NativeRules rule code 3 and a new NativeRulesID/FoundationID; code 2 and old certificates are not reinterpreted. |
| Bootstrap and contributed hints | The same deterministic body-reference height rule applies to ordinary safe transparent seed and contributed definitions; checked UInt32 range and exact qualified metadata for any generated regular constants are required. |
| Producer evidence | Explicit global-private collection, completed body-bearing records, full type/value support and real axiom inventory are retained. Public axiom-shaped projections are not substituted for proof evidence. |
| Receiver authority | Source tooling, serialized Lean modules, plugins and environment extensions remain outside native receiving acceptance. Exported inert descriptors still require fresh exact reconstruction/checking. |
| Capsule eligibility | Complete fixed background witness domain must be disjoint from the wrapper judgments; source-name disjointness alone does not suffice. Proof-dependent/nominal interfaces are not falsely covered. |
| Evidence policy | Opaque capsules retain checked bodies and actual support; alternate witnesses do not inherit another witness's native-environment certificate or footprint. |
| Migration memoization | The integrated key includes actual capsule/background and target reference/witness choices; hits are only candidate syntax, not current acceptance. |
| Migration custody | Source/target coexistence, separate target custody and explicit source release remain; checking alone does not discharge old source obligations. |
| NET2 registry | Existing capabilities 1–4 remain; capabilities 5 and 6 and operation codes 11–19 are explicitly allocated. Group capability 6 requires 5. |
| Mutual negotiation | HELLO request retains its old shape; reciprocal authenticated HELLO exchanges obtain both HELLO_REPLY capability advertisements before new calls. No inferred one-sided negotiation. |
| End-to-end claims | Local reuse, public contribution and another agent's checked application remain distinct; no routing or popularity observation becomes native truth. |

The native-rule shape was checked against the frozen [v2 contract](../../spec/OPERATIONAL-CORPUS-V2.md): NativeRules is `0x0003/1` with family, rule code, feature codes and exact permitted axiom paths; Foundation binds NativeRulesID and source/seed identity. Changing the rule code therefore actually propagates to foundation-bound mathematical identities. This is not merely a display-label amendment.

The same frozen contract already assigns capabilities 1=BUNDLE1, 2=EXPORT_HEAD2, 3=FIND_WINDOW and 4=ADVISORY_READ1, and adds capability advertisements to HELLO_REPLY only. The v3 reciprocal-exchange construction is consistent with that existing directionality. It does not require a hidden capability field in HELLO.

## Precision request: same-foundation identity preservation

The capsule section's statement that the original JudgmentID is retained should be read within one exact foundation and unchanged canonical root interface. It is not a promise to preserve an old rule-2 JudgmentID when first moving that root to rule 3. The HEIGHT1 and migration sections already explicitly require new FoundationIDs and consequent dependent identity changes, so no acceptance contradiction was found; adding this qualification locally would remove an avoidable ambiguity for implementers.

## Exact-routing review target and findings

The complete first exact-routing coverage draft was subsequently reviewed at SHA-256 `C5E882788BC806E8AC91063FACF4183DA21286D5EE69AA955474E2D072E488A9`. It supplies bounded exact scopes, explicit group operations, atomic batch mutation, lifecycle-gated serving, finite leases and paid incremental reclamation. The three findings below were sent to its owner for repair; no native acceptance bypass is claimed.

### F-GROUP-COUNT: selected replica target is not an actual group bound

The draft states `G <= min(M,rN)` for one scope, with r=4 selected copies. That is not a correct upper bound on its actual admitted groups.

For N=1, let depth-zero placement admit three copies but fail to obtain the fourth. The inherited base algorithm permits these partial shallow placements to remain while the publisher tries a deeper cell. Let the deeper cell admit four copies at different holders. There are now seven retained memberships and potentially seven nonempty provider-holder groups, although rN=4. Empty groups opened before a rejected batch, uncertain committed placements after a lost response, and replacement-before-old-release transitions are further sources of counted groups not represented by rN.

This affects actual state and recurring-resource claims even when all nodes are honest. The maximum group allocation can still prevent memory overflow by declining work, but that does not make the asserted bound true or show that every declared target can be maintained under the example envelope.

Required repair: distinguish an idealized settled chosen placement set with exactly r copies per target from **all** actual live, empty, uncertain and retiring groups/rows. State the corresponding actual-group bound using actual maintained memberships plus empty groups, and charge overlap/failed placement/reclamation. A settled-set cost example is useful only with its extra assumptions explicit. The integrated v3 summary must carry the same qualification.

The first repair at exact-note SHA-256 `D846BBA2E8ED7E729CEEB54A52ABC7FFD365810B0601D59230BD168216299938` correctly separates selected/transient membership allowances, empty groups and actual resource admission. A remaining lifecycle countercase was returned: one holder can retain a CLOSED g0 awaiting paid GC/snapshot release while a new ACTIVE g1 exists for the same scope. Total physical group records can then exceed M even though only one group per holder/scope is ACTIVE. Thus `min(M,...)` must be restricted to the active-group count, with retired/uncertain physical records charged separately; it cannot bound the repaired definition of total actual G.

The final full exact-note reread at SHA-256 `F23B5F1B455EF790A41E6FB98D8586750D704EF0D023DC1D8F0D0D850DBFEFA3` separates G_selected, G_active and G_total. Only the first has the settled `min(M,rN)` bound; active groups use their actual active membership/empty-group stock and active uniqueness; total charged records additionally include closed/expired unreclaimed generations and opening/uncertain reservations, under the actual local cap rather than M. Renewal counts only actually renewed active groups. F-GROUP-COUNT is closed on those bytes.

### F-MEMBER-ROOT: exact commitment or opaque token, not both

The draft says memberRoot commits to a canonical map, but only suggests that the holder "can use" a Patricia map over hashed cell/provider keys. It does not fix the root byte grammar, hash domain or map/node commitment construction. The recovery section nevertheless says that the source persists expected before/after roots and can reconcile a lost response against an expected after-root.

Two conforming holders could therefore use different valid map commitment algorithms. A source can always echo an observed opaque root to detect stale state, but it cannot independently derive an expected new root from mutations without an agreed algorithm. The safe fallback of retiring/repopulating an uncertain group does not supply that missing shared derivation rule.

Required repair: either fix the exact commitment algorithm and byte representation, or explicitly define memberRoot as a fixed-width holder-issued opaque state commitment and remove independently computed after-root claims. In the latter case, lost delivery must use the retained exact action result, an independently specified authenticated transition binding, or the stated conservative reconciliation/repopulation path. Neither root equality nor a count supplies native mathematical authority.

The full repaired-note reread at `D846BBA2E8ED7E729CEEB54A52ABC7FFD365810B0601D59230BD168216299938` supplies an exact `0x8023/1` operational Patricia-map node grammar, key hash domain, empty/leaf/branch shapes, canonical split/prefix constraints, original-key collision check and node-size/type limits. Under the inherited exact ContentID contract this removes the ambiguity. F-MEMBER-ROOT is closed on those repaired bytes; the integrator must also register the new operational type.

### F-RENEW-PUBLIC: aggregation must preserve producer publication guards

Base ROUTE1 permits the honest producer to create/renew an ad only while its current local index has a matching public retained entry and disclosure permits the fields. Group renewal extends every current member's lease. The fine draft specifies holder-side group/root/byte checks, but does not expressly require the producer to reestablish eligibility of the exact renewed member set against current public/disclosure/retention state.

Countercase: J is withdrawn locally after its group was last populated; an unchanged warm GROUP_RENEW extends the group containing J without applying the pending removal. Native provider reads still fail closed, so this is not false theorem acceptance. It nevertheless renews an advertisement the inherited honest publication rule says must no longer be renewed.

Required repair: bind producer authorization to the exact current group membership and a current eligibility view/maintained exact summary. Dirty, withdrawn or changed-anchor rows require a paid DROP/replacement before renewing the surviving set, or the renewal is declined. A current maintained summary can avoid scanning every member, but its update/incident/disclosure guards must be explicit; an old group root alone cannot certify current publication eligibility.

The same repaired-note reread explicitly requires the producer's exact renewed member set to match current public/disclosure/retention and anchor eligibility, binds any summary to memberRoot and current relevant policy/incident versions, and refuses renewal until dirty/withdrawn/changed rows are revalidated or successfully removed/replaced. The remote holder does not certify native eligibility. F-RENEW-PUBLIC is closed on those repaired bytes.

The final full exact-note reread at `F23B5F1B455EF790A41E6FB98D8586750D704EF0D023DC1D8F0D0D850DBFEFA3` preserves both fixes. It also explicitly rejects base PUT/DROP attempts against group-owned rows, requires group batches to maintain exact roots/counts/versions atomically, and fences old-group reclamation by exact group and row/storage generation. Thus an old GC cursor cannot erase a newly owned row at the same cell/provider key. These added seams were read here; their discovery is not falsely attributed to this auditor.

## Initially pending exact-routing dependency

The integrated draft allocates group operations 16–19 and capability 6, and selects a finite FULL_EXACT lane with ordinary scope 4096 and expanded scope up to 65536. At this initial review cut, its linked detailed exact-routing note is not yet available. The allocation is therefore reviewed only for registry/directionality consistency, not for a completed group state machine, exact batch grammar, current membership conditions, renewal semantics or end-to-end coverage property.

In particular, this audit has not yet established that:

- the exact scope's canonical judgment membership and proof/service anchors stay coherent across public-index changes;
- bounded batch changes preserve atomic accounting and unambiguous retry/version semantics;
- renewal of one receiver-local provider group cannot revive deleted entries, transfer membership, acquire new disclosure rights, or become a global renewal claim;
- row, group, cell, signature, snapshot and byte limits account for the actual full maintained index;
- persistent progress and leases give the claimed coverage only during adequate overlapping placement/reader windows;
- a complete scope statement has an explicit observation boundary and cannot imply globally current knowledge.

The base ROUTE1 note's coarse 16-key publication lane is explicitly insufficient for rare exact-query coverage. The provider-catalog indistinguishability argument remains relevant until actual fine-key ownership memberships are maintained. Merely batching an uninformative catalog or relabeling selective advertisements FULL_EXACT would not address it.

## Composition clarification delta

A bounded delta reread of the composition note at SHA-256 `47422562B1099F485BD08BCC6F16B3333B83BB073EF9649E8B8A7C56752057DB` checked the explicit exported subset T_out, closed capsule type `Π Γ, φ`, closed capsule body, and wrapper payload application to the original context variables in de Bruijn order `n−1,…,0`. The existing reader alone supplies the outer lambda telescope. This clarifies rather than weakens unchanged root context/conclusion identity and the earlier canonical-witness guard.

The note also records its author's direct pinned source observations on unused universe parameters and exact constant universe-vector length, with complete upstream links. This reviewer read that added evidence as part of the delta but did not execute the example or independently reproduce those new upstream source excerpts in this audit. No additional defect was found in the reviewed clarification.

## Final wire-boundary delta review

The routing author subsequently fixed exact RouteContact and operation result arrays, positive count/lease/page ceilings, 16-byte observation identifiers, and the route-specific reason enum mapped into the inherited NET result codes. This auditor reread the changed wire sections against the original result-code table and NET2 capability extension; no new top-level result code or HELLO request field is implied. The fine-note delta selects the same mappings and bound, with no group-design change.

One additional small ambiguity was returned: `ProviderAd.publicContact` still said "existing contact shape", while the inherited contract has both offline bundle entries `[nodeKey,endpoints]` and GET_ROUTES contacts `[nodeID,endpoints,nativeProfileIDs,indexKeys]`, alongside the new three-field RouteContact. The final repair explicitly chooses the GET_ROUTES four-field contact, binds its nodeID to the advertised provider, fixes endpoint/profile/key limits, and requires the exact key foundation among advertised native profiles. This closes the wire-codec ambiguity; the untrusted routing nature of every contact is unchanged.

Reviewed final routing-wire bytes: [base ROUTE1](../analyses/CP-001F-dissemination-and-routing.md), SHA-256 `57EA2FF2473CC2AFD3FD68C2B7EA1FE84046DE765D97BC6706441EE2A4B83F05`. This is this auditor's wire-boundary/delta review, not a claim to have independently repeated the other reviewer's full base-route audit.

Reviewed final exact-routing bytes: [exact coverage](../analyses/CP-001F-exact-routing-coverage.md), SHA-256 `8367743A6708C7CAEF5478965859E3907A2D80B62F9FC774C518092A4B9DDE7F`. The complete earlier repaired design was reread at F23B5F1B455EF790A41E6FB98D8586750D704EF0D023DC1D8F0D0D850DBFEFA3, and the final wire delta was reread explicitly. All three design findings above remain closed in the final version.

## Final integrated-byte review and disposition

The final [v3 integrated specification](../../spec/OPERATIONAL-CORPUS-V3.md) was reread in full at SHA-256 `16C58E09530359CCE106881E0436D9001C6671FB2DC8F59B17B912A35DE669E1`.

It now states same-FoundationID capsule identity preservation explicitly, registers the exact operational map type `0x8023/1`, distinguishes settled selected-placement group counts from actual transient/retired physical stock, and preserves producer-current-eligibility, atomic group update and old-owner/storage-generation reclamation guards. The capability/operation allocations agree with the final routing notes. No additional concrete integration defect was found in this bounded reread.

F-GROUP-COUNT, F-MEMBER-ROOT, F-RENEW-PUBLIC, the public-contact codec ambiguity and the same-foundation wording request are closed at the cited repaired bytes. Earlier M-CACHE/C-BOUNDARY repairs remain intact under integration. There is no remaining unresolved finding from this audit at this cut.

This disposition means only that the stated concept findings were repaired and the reviewed integration is internally consistent within this audit's scope. It is not a formal verification of the complete protocol, a release approval, or evidence of native/library compatibility, affordable large-network maintenance, adversarial routing robustness, useful lemma-retrieval recall, or reciprocal-growth performance. Exact fine-key discovery remains conditional on actual placement/service and sufficient overlapping reader work; unknown useful statements still require the separately evaluated structural/relevance path. Those qualification obligations are retained, not satisfied by audit closure or hashes.

## References

- [Integrated v3 specification](../../spec/OPERATIONAL-CORPUS-V3.md).
- [Frozen v2 contract](../../spec/OPERATIONAL-CORPUS-V2.md).
- [Migration/composition cross-audit](CP-001F-migration-cross-audit.md).
- [Full producer/client path](../analyses/CP-001F-lean-producer-client-path.md).
- [Proof composition and HEIGHT1](../analyses/CP-001F-proof-identity-composition.md).
- [MIGRATE1](../analyses/CP-001F-foundation-evolution-and-migration.md).
- [Base ROUTE1](../analyses/CP-001F-dissemination-and-routing.md).
- [Exact-routing coverage](../analyses/CP-001F-exact-routing-coverage.md).
