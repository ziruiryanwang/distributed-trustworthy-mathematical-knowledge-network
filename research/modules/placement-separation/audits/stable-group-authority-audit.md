# Independent authority and concurrency audit: stable-authority groups

Date: 2026-09-20. Reviewer: `stable_group_authority_audit`. Status: **independent repaired-cut review complete; SG-A1 CLOSED on the exact final cut recorded below**. Candidate remains UNSELECTED. This review is conceptual and read-only with respect to the source. No implementation, executable model, extraction, Lean run or benchmark occurred. The initial finding and its original disposition are preserved as review history, not current open defects.

## Complete reviewed cut and independence

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| [Stable-group candidate](../stable-group-contract.md) | 63002 | `B0BEA1B9E8316DC9BE2E28F8B21C3C4D6433468DB312DEA90D05467A26305B9E` |
| [Reviewed architectural source](../architectural-contract.md) | 33728 | `8FFD596DB086647971FB6E42AF5A2E2F38FE7D3FB1658C14DEC3D7686DA25C38` |
| [Independent architectural audit](architectural-audit.md) | 25513 | `92708433406724338026FDF282531995D8777291A308D7BFA1B822943FD4CFAB` |

The reviewer verified these complete lengths and hashes locally. The entire candidate was reread after the explicit hold. Source line references below name this initial complete held cut, not a moving draft. The reviewer did not author the candidate or edit any source; the only written artifact is this audit.

Primary inherited evidence checked: [F exact groups](../../../../notes/analyses/CP-001F-exact-routing-coverage.md), [F routing/error bindings](../../../../notes/analyses/CP-001F-dissemination-and-routing.md), [G structural retrieval](../../../../notes/analyses/CP-001G-structural-retrieval.md), [G profile/consumer bindings](../../../../notes/analyses/CP-001G-profile-and-consumer-bindings.md), [inherited once-only outcome, delivery and recovery contract](../../../../spec/OPERATIONAL-CORPUS-V1-NETWORK.md), and [NET2 negotiation and admission-generation amendment](../../../../spec/OPERATIONAL-CORPUS-V2.md). NET2's explicit amendments govern the inherited network source; this audit does not restore superseded NET1 epochs or codecs.

Pre-hold review provenance is important. Root had already identified the unrelated-invalid-entry scanner problem and the post-RENEW incident/result race. This reviewer independently raised delayed original results after a newer transition, OPEN's potentially effectful reconciliation behavior, ambiguous wording of the 24-byte groupID, and the need to distinguish row-lease continuity from uninterrupted positive coverage. Root additionally requested the equal-version/later-expiry check. All of those corrections are already present in the held source. They are not unresolved findings against this cut and do not count as post-hold repairs.

## Initial held-cut verdict and bounded scope

The authority/concurrency design is coherent at the intended conditional level. Exact old/new mode separation, local nonreuse, holder ownership/CAS, support-before-authorization, asymmetric destructive cleanup, one unresolved namespace effect, monotone result reconciliation and guarded borrower observations have explicit compatible transitions. No counterexample was found to their conditional safety when the stated single-writer, coherent-history, complete-guard and independently supplied resource premises hold.

One bounded held-source clarification, SG-A1, is needed: specify how reciprocal existing capability advertisements establish the same BindingID, and state explicitly that this is a locally installed/allowlisted codec mapping, not peer-supplied executable specification. The source already preserves the native boundary and rejects unsupported codecs; the finding concerns completing its new negotiation contract without inventing an inherited HELLO field.

This is not approval to allocate identifiers, select the profile, implement it or claim operability. The full-scan fallback may be economically unacceptable; its validity does not establish that it improves the system. The finite service theorem concerns an actual survivor row at one holder, not complete decentralized discovery or native throughput. Those limits are explicit in the source and remain part of this verdict.

## SG-A1: bind the symbolic profile to installed capability meaning

**Priority: medium for contract completeness. Disposition on the initial held cut: OPEN.**

Candidate lines 30–32 require reciprocal authenticated capability observations with the exact same BindingID. They define Binding as a complete future manifest and do not allocate a concrete encoding. Inherited NET2 HELLO_REPLY carries the capability-code list and advisory manifest IDs; it has no free-form BindingID slot. The source does not yet state whether the future capability code uniquely names the locally installed binding, or whether an additional separately specified observation carries the hash.

Minimal ambiguity trace:

1. Two peers advertise the presently symbolic SG capability along with capabilities 5–8.
2. Each has a different revision informally called SG1. The inherited advertised lists alone do not expose their manifest hashes unless the future capability allocation is explicitly one-to-one with those hashes.
3. A per-call BindingID can make the receiver reject a mismatched call, but does not by itself explain how the sender satisfied the source's pre-dispatch reciprocal exact-binding condition.

This is not a demonstrated native-soundness attack. Inherited fixed-codec and unsupported-profile rules forbid trusting arbitrary remote formats. It is a missing exact negotiation premise in this new branch, especially because Binding is described as fixing canonical codecs and limits.

Smallest sufficient repair: a future installed binding assigns its dedicated capability code to exactly one immutable, locally allowlisted BindingID and its trusted local codec/limit implementation. Reciprocal receipt of that code establishes the declared shared mapping; every call/result still checks its exact BindingID. Different revisions must receive distinct negotiated meanings or be rejected. Receiving a manifest, digest or peer claim cannot install a codec, increase a bound, reinterpret an old opcode or adopt a mathematical foundation. No new HELLO payload or numeric identifier is needed in this concept document. An explicitly specified different negotiation extension could also close the finding, but must not be silently attributed to inherited NET2.

Until clarified, do not call the candidate's exact negotiation branch fully closed. The rest of this audit is conditional on this binding resolution and unchanged inherited authority rules.

## Identity, serialization and exact ownership

Source lines 38–54 separate provider authority from a mathematical set. A is the complete `(provider,F,E,generation16,serial64)` tuple; neither its hash nor possession of it authorizes spending. Serial reservation durably advances the high-water mark before publication, aborted reservations are not returned, and exhaustion stops creation. Uncertain rollback fences the old authority rather than guessing a counter. Fresh identifiers use their stated probabilistic collision assumption; no proof of distributed absolute uniqueness is asserted. Malicious cloning of the provider key remains outside the honest single-writer service premise and does not create theorem validity.

The corrected groupID has exactly 24 total bytes: 16-byte holder authority generation and 8-byte big-endian nonreused counter. The full immutable group binding includes BindingID, holder, groupID, provider, mode, F/E and A. A cannot silently select an old parser or change a group's mode.

Holder OPEN serializes absence lookup, reservations and creation. Therefore, by induction over those authoritative transitions, at most one ACTIVE group exists for a fixed `(holder,provider,F,E,A)`, including empty groups. Matching OPEN returns the existing state without extending its lease. CLOSED/EXPIRED/unreclaimed and uncertain generations are not erased by this uniqueness statement. If the permitted group has insufficient capacity, a second active same-A group is not an escape hatch.

The producer's source lane in line 156 uses the same namespace-level key before a groupID exists. This closes the draft ambiguity in which unresolved OPEN could otherwise acquire a separate generation-specific lane. OPEN reserves its possible new empty generation and cannot be called a harmless read while PUT/RENEW/CLOSE remains unresolved. The later OPEN boundary trace is explicitly after lawful settlement and outside the strict positive settlement recipe.

F's cell/provider row ownership remains exclusive. Exact expected version/root, row CID, ad revision, group/profile identity and current lifecycle gates are rechecked in the bounded authoritative transaction. A changed batch installs the entire map, counts, bytes and row state atomically or changes none. A repeated equal-byte/equal-revision PUT does not create new lease authority; different bytes at equal revision or a stale revision reject the batch. Base ungrouped operations cannot mutate a grouped row around its map/version accounting.

The abstract invariant is not that all placements instantaneously agree with the desired owner. During a paid old/new owner transfer, actual per-placement states may differ. The authoritative owner/history record must expose that partial transition, and same-cell destination PUT still waits for actual old-owner removal. Coverage cannot jump directly from an intended owner to a settled observation.

## Support scanning is finite evidence inspection, not a truth shortcut

The held source gives an exact entry identity, a finite selected relation and explicit dispositions for excluded/ineligible/tombstone records. Multiple replay contexts are not merged because they share a target. Descriptor-result deduplication remains G's separate exact FIND rule.

The scan checks the complete retained group map and the exact actual signed anchor for each member. A different theorem emitting the same token is not a substitute for the signed anchor chain. Native assessment reuse requires the actual qualified foundation/checker, exact replay/footprint and current protection/disclosure dependencies. Unknown required dependencies cannot become an all-supported certificate.

The formerly problematic unrelated-invalid case is handled correctly. The scanner traverses the named finite inventory coherently, but an excluded or dirty record unused by the actual group does not force that group's witnesses to regain support. Missing inventory structure is a different failure from an unrelated member's native status. Classification completes the supported/unsupported/unknown partition rather than stopping at the first explicitly withdrawn anchor.

Every positive summary binds A/Binding, semantic cut, support fence, group/root/version, actual member ads/anchors and relevant guard versions. Publication compares those guards atomically with the starting cut. Thus an incident between the last record inspection and summary publication invalidates authorization rather than creating a time-of-check/time-of-use gap. A coarse fence is cheap invalidation, not free rescanning; the source explicitly prices all retained records, repeated reads, physical posting paths and complete dependency visits. This audit does not qualify those cost functions.

The key integration premise is complete guard propagation. A native/protection/disclosure change must advance its authoritative guard before subsequent reliance. Where the affected-authority relation is not established, the provider-wide fallback dirties all summaries. An implementation that silently misses such a change violates the premise; neither hashes nor this audit detect it magically.

## Destructive cleanup remains possible after support loss

PUT and RENEW are support-dependent; DROP and CLOSE are not theorem-support-dependent. This asymmetry is necessary.

Consider two unsupported members and a bound allowing only one DROP per batch. Requiring all residual members to be supported before authorizing the first batch would deadlock. Under source lines 143–148, the owner can remove the first exact CID with current operational authority while the second remains invalid, then remove the second. Each batch uses the actual resulting root/version; none authorizes a containing-group renewal until the final exact remaining set passes the support scan.

This is not unguarded deletion. DROP still checks authenticated owner, group, expected state/CID, disclosure and budget. CLOSE gates only its routing group and schedules paid generation-fenced cleanup. Neither operation releases independent native custody, public export ownership or OWNER_RELEASE_REQUIRED pins. A stale old sweep cannot delete a replacement row generation.

Source selection cleanup and physical cleanup are distinct. Marking withdrawn x excluded/ineligible removes its support role at the current semantic cut. It does not assert that historical index snapshots, native evidence or old maps have been reclaimed. Their real retention owners continue to be counted.

## Authorization, incidents and delayed results

The relevant local linearization point is the source transaction that checks support/owner guards, consumes one-shot action authority and persists exact immutable call bytes. If invalidation wins first, no new support-dependent authorization follows from the old summary. If authorization wins first, the remote effect may already be claimed and can complete after the incident. No source transaction cancels a remote claim retroactively.

The incident procedure first advances the support fence and dirties current assertions, then drains the one unresolved namespace effect. It incorporates a late committed pre-incident PUT's actual changed CID/root, or a late RENEW's changed version/lease. It cannot use pre-incident expected state for subsequent cleanup. A timeout and NET terminal unknown are not evidence that the old mutation did not occur. Missing outcome/lineage retains uncertainty and charges; the successful finite trace explicitly assumes actual settlement within its primitive bound.

The new monotone reconciliation paragraph handles the pre-hold late-result finding:

1. An exact version-9 transition is established by coherent admitted observation/history; its effect lane is released while original delivery/accounting remains.
2. A later DROP commits version 10/root R1.
3. The version-9 original reply arrives.
4. It may settle its own history/accounting, but cannot replace version 10/R1, revive support or move the current lease knowledge backward.

Equal version is not a resurrection rule either. Immutable binding and membership/root/count/bytes must agree; a later known CLOSED/EXPIRED gate or support invalidation is not overwritten. Remaining-duration observations belong to their own commit cuts and cannot be compared as global wall-clock expiry times. Unknown higher lineage or incompatible same-version state fences further positive claims.

The other important race is incident-after-authorization but before result reconciliation. Source lines 187 and 197 preserve the actual remote result and spending while retaining the newer DIRTY/DRAINING obligation. A successful historical RENEW cannot restore SUPPORTED unless current guard comparison and paid rebinding/rescanning justify it. Once-only execution and current eligibility are separate state machines; the source now keeps them separate.

Quiescent withdrawal requires all restoring effects to be terminal or actually effect-fenced, removed/expired/closed invalid rows, and no live new restoring authorization. Issued DROP, local version change or expected future expiry alone is insufficient. Accounting/history may properly survive a quiescent withdrawal report.

## Borrowers, compaction and snapshots

A borrower resolves current owner/support versions, the applicable authority/provider fence, its own entry/posting eligibility and actual copies/paths before making a current coverage claim. A stable A is not a perpetual coverage bit. Updating one version can invalidate many cached borrowers, but the cost of recomputing their individual observations remains explicit.

Pure compaction prepares a finite new physical layout, establishes exact preservation of the semantic entry/descriptor/token/posting relation against current inputs, reserves both layouts and commits only the representation change. Under those hypotheses A, ads, group roots and native support do not change. Clausewise substitution then preserves the same historical placement witnesses without new route mutation. The candidate does not claim that equality checking is free or that equal token unions imply equal FIND results.

FIND snapshots keep their exact predicate/extractor/planner/schema/order/index cut and original cursor bounds. A cursor is not resumed against a different physical universe by renaming it. Old readers retain real roots/allocations, and current-versus-historical delivery guards remain independent. ROUTE_LIST still describes the named holder cut; later expiry does not rewrite that historical snapshot into current presence.

## Native boundary and service theorem scope

Holders authenticate and validate operational codecs, not proofs. A malicious provider can produce false leads under this scheme just as under the inherited routing boundary. Every receiver still obtains and independently checks actual native evidence under its own adopted qualified foundation before mathematical reliance. SG neither broadens a native read scope nor grants permission to fetch an entire operational map. No human intention, central ledger or shared research assignment is introduced.

The finite repair proof has a meaningful but narrow object. Assuming old-action outcomes preserve the promised survivor row, the original lease covers settlement, the scans and serial DROP/RENEW operations fit their admitted bounds, and the actual primitives respond as specified, each predecessor completes before the cumulative deadline. The final RENEW then prevents an expiry gap for that row at that holder. This is not obtained by assuming the repair conclusion itself.

The row-preservation premise explicitly excludes a prior CLOSE or DROP that removes the promised survivor, and forbids backdating post-settlement service to the incident cut. The theorem separately admits counter headroom. A coarse incident can make current source coverage UNKNOWN throughout repair even though the actual row remains live. No uninterrupted positive assertion, native disclosure, four-copy discovery or end-to-end query promise follows.

Bounded clock-rate/continuity and send-bound result causality are additional service premises, not inherited global time. If a call sent at s reports commit-boundary remaining lease L and holder elapsed time is at most `(1+rho)` times source elapsed time, expiry cannot precede `s + L/(1+rho)` on the source clock. Receive time would not justify the same bound. Unknown continuity or insufficient margin correctly declines the no-gap promise.

## Initial disposition and next review boundary

The initial held cut supports the conditional local authority/ownership/safety argument, subject to SG-A1's exact binding clarification. Pre-hold findings are repaired in this cut. No source edit, new operation, numeric allocation or runtime behavior was supplied by this audit.

After the coordinated binding repair, reread the exact new complete cut's negotiation/dispatch, affected consumer table, current-guard and outcome sections; record its complete hash here. An equal-service comparison remains independently necessary before considering selection. In particular, coarse invalidation may require expensive repeated complete scans across many dispersed groups; removing remote compaction mutations does not by itself improve total useful operation.

## Complete coordinated repair review

The author supplied and held this distinct complete replacement cut:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| [Repaired stable-group candidate](../stable-group-contract.md) | 68458 | `EA9398969D640BDE89271E53274B4F0071D00436659F5BF8D03FC266AD250779` |

The reviewer verified its exact complete length/hash, read all 342 lines, and rechecked the hash after the read. The author had ceased source editing before handoff. This is a complete-source rereview, not approval inferred from a patch description. References in this final section identify the repaired cut; earlier line references and open-finding text remain the historical initial review.

The coordinated repair covers SG-A1 and the separate resource review's R4/R5. This reviewer independently assessed all three changes and their interaction with authority/concurrency. R4 originated with root and was independently confirmed by the resource reviewer; R5 originated in the independent resource review; neither originated in this review's initial findings.

### SG-A1 closure: locally installed exact binding

Repaired lines 32–34 state that inherited HELLO_REPLY has capability codes and no BindingID field. Future local installation must establish an immutable one-dedicated-capability-code/one-BindingID mapping with its installed codec, limits and consumer semantics. A code cannot select among several revisions. A different revision needs a distinct dedicated negotiated meaning; a node lacking the mapping rejects it.

Reciprocal observation of that dedicated code now identifies the declared binding through locally installed semantics. Every candidate call/result also checks its explicit BindingID against the mapping, exact invocation and stored group. An advertised code accompanied by another hash is rejected before choosing a decoder or capacity vector. Remote manifests, hashes and profile names cannot install codecs, alter allowlists or limits, or adopt a mathematical foundation. The affected consumer obligation at repaired line 307 repeats the same rule.

This supplies the previously missing link without inventing a HELLO field, allocating a number, or modifying old opcodes. **SG-A1 is CLOSED.** Honest implementations of different installed revisions cannot accidentally satisfy the shared-binding condition merely by both using the informal name SG1. Malicious capability claims remain untrusted claims and gain no authority through this negotiation.

### R4 cross-check: original invocation time cannot be replay-refreshed

Repaired group/action inventories link each historical lease observation to its exact original NET invocation occurrence, persisted dispatch-or-proven-earlier time, and monotonic-origin identity. Lines 240–242 require that basis before an effect can escape. A later identical argument array under a fresh invocation is a different occurrence; an old result cannot borrow its newer time.

The lower-bound proof now has the right causal antecedent. If original commit c cannot precede retained s0, and holder elapsed time up to expiry is L with holder/source rate ratio bounded above by `1+rho`, the source expiry cannot precede `s0 + L/(1+rho)`. Retransmission or delayed delivery changes neither original c nor s0. A proven earlier timestamp remains conservative; a later replay-send timestamp is not conservative and is explicitly forbidden.

The repaired replay trace demonstrates the distinction: original dispatch at 0, commit at 1, remaining lease 10, actual expiry 11; replay at 20 cannot manufacture a lower bound of 30. The legitimate bound is 10 and is already past. Missing original occurrence/history, discontinuous monotonic origin or unknown relative rate yields UNKNOWN_DEADLINE. A genuine new renewal is separately admitted and cannot arise from replay metadata.

This repair strengthens, rather than bypasses, monotone result reconciliation. Old outcomes may settle historical accounting, but cannot refresh current lease knowledge, reopen the unresolved-effect lane, replace a newer group root, or restore a dirty support phase. No new outcome-fetch service, trusted wall clock or extra free result delivery is introduced.

### R5 cross-check: every retained member has support

Repaired lines 246–250 explicitly require the complete actual post-settlement membership to partition as `Mpost = Keep disjoint-union Remove`. Every Keep member has current support for its exact actual ad/anchor and all required guards. Every Remove member is definitely unsupported at that cut and separately authorized for routing removal. No member is omitted and this simple successful episode admits no UNKNOWN_SUPPORT member.

After exact authorized deletions, the actual remaining map is exactly Keep. The second paid complete scan must establish support for every actual remaining member, not merely finish within its duration bound. Stable relevant guards and complete retained inputs make that conclusion derivable for this named episode; bounded scan time alone does not.

The promised survivor belongs to Keep, and all possible admitted prior-action outcomes must preserve its row/lifecycle through settlement. Therefore the stronger premise does not silently reintroduce the prior-CLOSE or unknown-prior-PUT error. Deletions remain authorized operational cleanup, not a declaration that the removed theorem is false, and independent custody owners remain intact.

The added unknown-neighbor trace is decisive: supported b plus unknown c with no definitely unsupported member does not justify taking i=0 and renewing both. The ordinary state machine stops at classification nondecision. Revalidation or conservative owner-authorized removal of c requires a separately specified and paid plan; its costs and deadline cannot be hidden in the simple episode. This closes the service-proof premise without weakening current support safety or turning UNKNOWN into mathematical falsity.

### Unchanged boundaries and final disposition

The full reread confirms that these changes do not reinterpret old FULL_EXACT/FULL_FEATURE groups, loosen per-holder ACTIVE uniqueness, permit a second unresolved namespace effect, authorize DROP/CLOSE from a copied receipt, or remove exact version/root/ad checks. Late lower-version outcomes remain historical; equal-version membership agreement cannot revive an expired lifecycle or newer local support guard. Compaction still requires exact semantic/posting preservation, and borrowers still resolve current versions and actual path/copy observations.

Native checking, exact replay contexts, public disclosure, custody ownership, snapshot generations, generation-fenced cleanup and once-only spending remain separate. The updated theorem still promises only conditional no-expiry-gap service for named survivor rows at specified holders, not uninterrupted current coverage, network convergence, sustained throughput or useful mathematical growth. All scan, storage, timing and primitive-supply bounds remain independently supplied and unmeasured.

**Final verdict: SG-A1 CLOSED; coordinated R4/R5 repairs independently cross-checked; no remaining authority/concurrency finding identified in the repaired cut at this conceptual scope.** The conditional authority/support argument and narrowly stated finite repair transition are supported under their explicit premises. Candidate remains **UNSELECTED, unimplemented and not operability-qualified**. An equal-service comparison and later separately authorized implementation/qualification remain necessary; this audit supplies neither selection nor execution permission. The reviewer ceases edits after handing off this audit's final bytes/hash.
