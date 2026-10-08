# Independent audit: placement authority versus logical index runs

Date: 2026-09-20. Reviewer: `placement_independent_architecture_audit`. Status: **independent architecture review complete; finding A1 closed on the repaired held cut below**. The source remains UNSELECTED. This is an architecture review, not protocol selection, an execution qualification or an operability finding. No implementation, executable model, native execution, extraction or benchmark was performed.

## Reviewed cuts and independence

| Read-only source | Bytes | SHA-256 |
|---|---:|---|
| [Architectural contract](../architectural-contract.md) | 32199 | `0C567A689309A528103E6AE9C3DE8C5A4460C4AB610D0E25AE04D387C0DF4815` |
| [Module card](../README.md) | 3619 | `00B70A92C4DFFCFF19BB4B7F66D3CCA5AF91AC553D5930661A572798002E64B9` |

Both byte lengths and hashes were checked locally before the initial review. The reviewer did not author the architecture source or its module card. The only file written by this assignment is this audit. References in the initial findings below identify the lines in that initial held source and frozen predecessor evidence; they do not authorize changes to those predecessors. The final repair review records its distinct complete cut below.

## Verdict

The central separation is coherent and worth a bounded exact-profile investigation. In the proposed model, a representation-preserving rewrite of a local index need not change remote placement authority. The conditional zero-remote-compaction proposition follows from its stated premises. No counterexample to that narrow proposition was found.

The initial cut lacked one explicit premise in the candidate group-count bound: at most one settled nonempty ACTIVE group for a fixed holder/provider/foundation/extractor/placement-authority generation. Without that premise, the advertised `min(M,rU)` namespace bound need not hold. Finding A1 is now closed by the repaired source's stronger at-most-one-ACTIVE-group rule, including empty groups, and explicit idempotent OPEN/serialization obligations. This repairs the cost argument and eventual OPEN invariant; it does not change the representation-preservation proposition.

The candidate is not an operable protocol. Canonical identities, exact negotiation and dispatch, durable namespace accounting, dependency summaries, an incident-repair service bound and an equal-resource operating comparison remain open. Those are correctly identified as open in the source; their absence must not be converted into either a false completion claim or a demand that this narrow architecture proposition solve the whole system.

## Finding A1: explicit group-uniqueness premise needed

This section preserves the initial finding and counterexample. Its final disposition is CLOSED at the exact repaired cut recorded below.

The source's cost comparison, line 156, bounds a single stable namespace by `min(M,r sum_i Ui)` selected settled groups. F's corresponding bound relies on the exact invariant at [F exact coverage](../../../../notes/analyses/CP-001F-exact-routing-coverage.md), line 41: one ACTIVE group per provider/scope at a holder. The candidate deliberately replaces the scope binding, and line 38 says a namespace can have many admitted holder groups without explicitly retaining this per-holder uniqueness condition.

Small counterexample with the candidate's ordinary four-copy setting:

1. One provider owns two distinct keys under one stable authority A. Let `U=2`, `r=4`, `M=4`.
2. Both keys have one selected copy at each of the four holders. There are eight rows total; no row has two owners and no historical, empty or uncertain generation is being counted.
3. At each holder, place the first key in one A-bound group and the second key in another disjoint A-bound group. All groups are ACTIVE and nonempty.
4. If this arrangement is allowed, there are eight selected groups, but `min(M,rU)=min(4,8)=4`.

Row exclusivity, finite admission and immutable A bindings alone do not exclude this arrangement. The source may intend to inherit F's uniqueness invariant, but the new binding should make that premise explicit.

Smallest repair: require at most one settled nonempty ACTIVE group per exact `(holder,provider,F,E,A/generation)` for this cost bound, with matching idempotent OPEN behavior in any eventual profile. A stronger at-most-one-ACTIVE-group invariant is also compatible with the old discipline. If multiple active groups under one authority at one holder are deliberately permitted, use the actual multiplicity in the bound instead, or use separately admitted authority namespaces. A request to combine existing groups is a paid transfer, not a free local identification.

In either formulation, empty/opening, uncertain, retiring, expired and unreclaimed records remain separately charged. This repair does not turn a selected-group bound into a bound on all lifecycle stock. It does not promise that the one permitted group has capacity to admit arbitrary further keys.

Root was notified before source editing. The finding is medium-priority for this architecture decision: it blocks an unqualified use of the affected cost formula, but not the conditional no-remote-compaction proposition.

## Conditional proposition: why the narrow argument holds

The source defines `RepEq(C,R,R')` using exact selected-entry records, descriptors, tokens and the actual provider posting relation, not merely token-union or row-count equality. Let an obligation for selected entry j and token k be the conjunction of:

- j's current selected membership, native/disclosure eligibility and actual FIND posting;
- the explicit eligible anchor bound to the signed ad;
- a settled provider/key owner and current owner/support version;
- the required actual row, cell/path and marker observations with their stated ages.

Under the source's hypotheses, replacing R by R' preserves the exact semantic entries and postings. It changes neither the anchor nor the relevant support guards. Ownership, ad bytes, remote member roots and selected placement observations also remain unchanged. Every conjunct therefore keeps the same witness or observation. No conjunct requires a holder action merely because the physical run layout changed.

This is a useful noninterference fact, not a magical compaction algorithm. The local rewrite still needs a finite admitted plan, exact relation preservation, temporary storage and an atomic guarded local publication boundary. The holder lease clock is not stopped. A preexisting observation does not become more recent, and a holder failure or expiry concurrent with the rewrite remains a failure or expiry. These qualifications are present in source lines 89–99.

The argument would fail under weaker hypotheses. For example, an old index with postings `(x,k)` and `(y,k)` and a replacement containing only `(x,k)` has the same token union but loses y's discovery path. This is excluded by exact posting equality. Likewise, replacing the replay or descriptor that witnesses the anchor violates exact binding even if a human judges the new theorem equivalent. The candidate correctly avoids mathematical-equivalence or human-intention oracles here.

An unchanged semantic cut is sufficient, not necessary, for zero remote mutations: H already permits a new target to borrow existing valid token routes. The source accurately treats that growth transition separately from pure compaction.

## Support and current eligibility

The replacement support boundary is precise enough for architecture reasoning:

1. A selected entry names exact target, structural descriptor, public descriptor and replay bindings.
2. Native acceptance, current protection and permitted public service are independently required.
3. Exact completed extraction witnesses the token; an interrupted extraction is not a completed descriptor.
4. An anchor's ad, structural hint and replay must agree.
5. The corresponding actual provider posting exists.

This does not let a namespace, group root, signature or single unrelated surviving theorem certify all members. The source's definition also requires each borrowed target's own current eligibility and posting, so an eligible anchor is not a substitute for the target being discoverable.

This is consistent with [G structural retrieval](../../../../notes/analyses/CP-001G-structural-retrieval.md), lines 187–215: ProviderAd2 contains no ScopeID; its holder checks bounded routing metadata, while the honest producer retains exact native/descriptor eligibility duties. G's old FULL_FEATURE rule additionally requires support in the exact immutable declared FeatureScope. Removing that last boundary is a genuine contract change, even though it does not change native theorem checking.

The new producer publication cut is finite and locally controlled. It is not a network-wide authoritative ledger or a universally shared set of mathematics. A malicious producer can still publish bounded false leads; the independent native acceptance path is unchanged. The candidate neither claims that support metadata makes a malicious producer honest nor relies on identity as mathematical truth.

## Borrowers, compaction commits and withdrawal races

The candidate's borrower discipline preserves the necessary local ordering: invalidate affected support/owner assertions and advance their nonwrapping version before dispatching an action that could invalidate old coverage. A borrower must resolve the current version before making a new current claim. An immutable old manifest containing a copied coverage bit does not satisfy that obligation. Source line 64 correctly distinguishes cheap version invalidation from the separately metered work of recomputing aggregates or enumerating dependents.

The same principle appears in [O normalization](../../reciprocal-operability/batch-normalization-contract.md), line 50. The candidate does not invent free fan-out updates or silently assume an existing unversioned implementation has the required indirection.

For pure compaction, an eligibility edit between preparation and the local commit makes the relevant guard stale. The commit must fail or replan, not install an old support observation as current. Old snapshot scans can continue only through their retained exact cuts and existing delivery guards. A future concrete layout implementation must preserve G's selected predicate and descriptor ordering as well as the relation itself; it may not resume a cursor against an unrelated physical layout by treating a manifest ID as semantic identity.

The local-versus-remote withdrawal distinction is handled correctly. Minimal race:

1. At a valid local support cut, the producer authorizes an exact renewal; the remote operation becomes claimed but its result is delayed.
2. A local incident invalidates the anchor, increments the relevant support version and stops new authorizations and current public service.
3. The previously claimed remote renewal commits later. Its row can survive as a stale routing lead until lawful removal or expiry.

This is not a native soundness violation and does not refute the local authorization gate. It would refute a claim of instantaneous remote withdrawal. Source line 68 explicitly disclaims that stronger claim and requires outstanding restoring actions to be settled before quiescent withdrawal is claimed. Group expected-version/member-root serialization alone is not a global revocation barrier.

One detail should be settled during exact-profile work, not guessed from this audit: authorization for a DROP of an invalid member must not require that member to regain native support. Support checks should bind the exact resulting or newly renewed live membership, while deletion uses authenticated ownership and expected-state guards. The source's prescribed DROP-before-renewal recovery is consistent with that reading; no contradiction was found.

## Compatibility and changed-consumer coverage

The source correctly refuses to reinterpret old FULL_FEATURE groups. [G profile bindings](../../../../notes/analyses/CP-001G-profile-and-consumer-bindings.md), lines 39–51, bind exact ad/map domains and immutable modes; [G structural retrieval](../../../../notes/analyses/CP-001G-structural-retrieval.md), lines 209–215, bind operation 20 to the exact immutable FeatureScope contract. A candidate A identifier cannot simply be supplied as an old scope hash with weaker support semantics.

The reviewed consumer map is adequate for the architecture stage:

| Consumer | Audit conclusion |
|---|---|
| Holder mechanics | New negotiated mode/open/result binding is needed; row exclusivity, expected-state serialization, local leases and GC fences remain. Finding A1 makes the per-holder uniqueness premise explicit. |
| G records and native/query path | Existing ad bytes need not gain a scope field; exact whitelist, status and query/snapshot bindings still need review under the new mode. Native acceptance is unchanged. |
| H sharing | The unique provider/key owner survives, but exact support is no longer defined by membership in an immutable owner FeatureScope. Explicit support/borrower versions must replace that dependency. |
| N recovery | A/generation and support versions need a fresh admitted owner-cut interpretation; old N cuts do not inherit it automatically. Physical holder replacement under a stable owner remains distinct from authority replacement. |
| O normalization | The candidate's pure local compaction is not O's selected remote-owner transfer. Mixed-mode input needs explicit paid migration and honest status. |
| P and current continuation | Their old-mode calendars and obligations cannot be discounted retrospectively using candidate savings. |

The N distinction is confirmed by [N recovery](../../reciprocal-operability/routing-recovery-contract.md), lines 9 and 29–37. The source also explicitly lists the missing canonical identities, error/status dispatch, summary representation, persistence, incident repair and restart/migration suite. This review found no hidden assertion that inherited mechanics automatically specify all those new fields.

Adoption still requires old-owner DROP before same-cell new-owner PUT. If the DROP outcome is lost, familiar ad bytes do not prove the row is absent. Root/member/version reconciliation and counted uncertainty remain necessary. A delayed old-generation sweep cannot remove the new owner's row. These are substantive compatibility requirements, not paperwork; source lines 132–134 preserve them.

## Costs and whether the change is worth further work

The important savings is removal of an avoidable class of remote mutations, not a guarantee of reduced renewal traffic. For U unchanged owned keys with r fixed selected copies, an old-mode owner transfer needs rU successful removals and rU successful insertions. The candidate's pure local rewrite needs none of those ownership mutations. Both statements exclude actual extra generations, failures and separately charged control work. A batch mutation count is not an RPC count.

The source correctly retains these costs:

- Exact local relation construction or verification, hashing, peak layouts, retained old snapshots and eventual physical cleanup.
- Native checks and custody for new results, actual local postings, novel-key lookup and placement.
- Ordinary renewal, markers, changed anchors, holder/path refresh, uncertain outcomes and authenticated action settlement.
- Capacity-driven authority splits and real migrations, including migration from the old mode.
- Eligibility-summary construction/invalidation and the incident-driven blast radius of a group containing both invalid and still-valid members.

In a dispersed network where almost every selected row lands at a different holder, namespace consolidation can leave renewal count essentially unchanged. Nevertheless, avoiding local-compaction-induced DROP/PUT work can still matter. Conversely, a workload with few logical compactions or many independent anchor incidents may see little benefit or a net loss once summary and incident costs are counted. No universal ranking follows.

The existing alternatives in the source are genuine:

- Keep old immutable publication owners while reorganizing local FIND storage. This already avoids remote changes for that narrower operation, but leaves the old scope/group inventory and its limits.
- Borrow already covered tokens. H already permits this; novel tokens and changing anchors remain real work.
- Use ungrouped K4 advertisements under the existing negotiated record path. Per-row leases lose group amortization; old group-owned rows still require lawful removal.
- Serve through known native contacts or the direct candidate broker service. This changes unfamiliar discovery assumptions and is not an equal-service substitute.

The ungrouped alternative is supported by [F routing](../../../../notes/analyses/CP-001F-dissemination-and-routing.md), lines 65 and 106, together with G's negotiated K4 record domain. The contact limitation is explicit in [I direct broker bindings](../../../../notes/analyses/CP-001I-direct-broker-bindings.md), lines 7–11 and 159–161. A fixed immutable owner scope cannot magically acquire unknown future tokens.

Recommendation: after A1 is repaired, pursue a bounded exact-profile proposal and an equal-resource comparison. The next research decision should compare continuing novel-key insertion plus repeated local compaction, with and without anchor incidents, across both overlapping and dispersed holder placements. Count adoption cost and peak histories. Require a finite paid incident-repair schedule that can restore surviving valid members before the stated lease deadlines under a declared finite incident load. This is a specification/comparison requirement, not authorization to run code or benchmarks.

If no jointly supplied case beats unchanged-scope or ungrouped alternatives at relevant service levels, reject or defer the profile. It is not justified merely because the noninterference lemma is true.

## Dependency-ordered next module

The next module should be one minimal stable-authority binding and support-repair contract, not a new network architecture. Its work has the following dependency order:

1. **Exact bounded identity and dispatch.** Define the canonical A/generation identity, persistence/nonreuse/exhaustion rule, immutable holder binding, OPEN idempotence/uniqueness and exact negotiated request/result/status domains. Retain authenticated provider ownership, existing bounded CAS batches, one-shot outcomes and generation-fenced cleanup. Old FULL_FEATURE mode must reject the candidate meaning. This fixes what objects, bytes and operations the comparison is actually counting.
2. **Finite support authorization with a paid fallback.** Define exact selected-entry and per-key anchor dependencies, group-member/root binding, current-version checks, borrower invalidation and local commit order. An admitted full scan of a finite named relation is an acceptable initial fallback; a clever incremental summary is not a prerequisite. Give the scan's explicit visited-entry/member limits, workspace and resource budget. Unknown support or exhausted scan work yields nondecision, not an O(1) claim.
3. **One invalid-member removal and surviving-member renewal.** Specify how authenticated DROP remains possible when the removed member lacks support, how the resulting exact member root is reconciled, and how claimed pre-incident operations are settled. Bind the renewed survivor's current support to that actual post-DROP root/version. Supply a finite service reserve/calendar and a declared incident-response premise; safe withholding by itself does not discharge this step.
4. **Equal-service paper comparison.** Use the same finite selected keys, actual holder incidence, lease and new-input duties, native/custody obligations, incident load and resources for the candidate and existing alternatives. Include old-mode adoption, transient stock and declined work. Only then decide whether selecting a candidate profile or refining the summary implementation is justified.

Steps 1–3 are prerequisites to a claim of positive ongoing operational cost advantage. The architectural row-mutation difference can already be compared symbolically, but an end-to-end saving cannot be inferred before the new support/repair overhead has a bound. Exact bytes and finite admitted scan costs suffice for the first paper comparison; implementing or benchmarking an optimized summary is neither assumed nor authorized by this audit.

Smallest successful trace for that module:

- One A-bound group contains distinct ads `a(x)` and `b(y)` with exact current native/public support and actual postings. A second immutable local run borrows b through the current owner version.
- A guarded local compaction preserves the exact semantic relation, changes only layout references and issues no remote mutation. Old readers retain paid historical layout state.
- A finite incident then removes support for x. Local current claims are invalidated first; the borrowed b remains a distinct eligible obligation. After settling an already claimed pre-incident renewal, a funded DROP removes a, and a funded renewal of the actual new root preserves b before its required deadline. No removed theorem is required to become valid again in order to authorize its deletion.

Smallest defeating trace for the same promised service level:

- Use the same two members and incident, but the only available support plan rescans more entries than its admitted work bound, or no paid DROP/reconciliation slot remains before b's lease deadline.
- The producer must withhold renewal of the dirty group; b consequently lacks the promised maintained service even though y itself remains eligible. The design is safe but this workload is not operable under that allocation. Repeatedly carrying b forward as merely degraded is not a successful comparison case.

Separately, a peer that lacks the new negotiated mode cannot be tested by sending an A value through old operation 20. Honest fallback is an independently admitted old-mode or ungrouped service, with its real costs and discovery differences, or a clear unsupported-mode outcome.

## Handoff and remaining status

Initial review requested one bounded source repair, A1. Root coordinated the source author's repair before the independent reread. The exact closure is recorded below; there are no remaining architecture-audit findings against that repaired cut. The declared preselection protocol and operating obligations remain open, not silently waived by this verdict.

No claim of operability, continuing useful growth, executed native feasibility or goal completion is made. The architecture removes a plausible avoidable coupling. It does not solve the system's continued resource supply, search quality, useful mathematics yield or long-term retention obligations.

## Exact repair review and A1 closure

The reviewer checked these complete held cuts after the coordinated repair:

| Source | Bytes | SHA-256 |
|---|---:|---|
| [Repaired architectural contract](../architectural-contract.md) | 33728 | `8FFD596DB086647971FB6E42AF5A2E2F38FE7D3FB1658C14DEC3D7686DA25C38` |
| [Unchanged module card](../README.md) | 3619 | `00B70A92C4DFFCFF19BB4B7F66D3CCA5AF91AC553D5930661A572798002E64B9` |

Repaired source line 40 now requires at most one ACTIVE group, including empty ACTIVE groups, per exact `(holder,p,F,E,A/generation)`. Matching OPEN returns the existing group's observation without extending the lease. Concurrent and uncertain opening/recovery paths must serialize instead of creating duplicate ACTIVE groups. Capacity overflow requires a separate admitted namespace or an explicitly different future multiplicity contract with a corrected bound. Concrete new-mode encoding remains openly unspecified.

Line 158 supplies the missing bound argument: by uniqueness, the settled nonempty selected groups number at most M; because each contains at least one selected row, they also number at most `r sum_i Ui`. Their number is therefore at most the minimum. The initial two-groups-per-holder counterexample is now excluded by an explicit architecture invariant, not by assuming the desired bound. Empty, opening, uncertain, retiring, expired, unreclaimed and old-mode adoption state remain outside this selected-stock bound and retain their actual charges.

The reviewer reread the affected state and cost sections, the unchanged card, the proposition at repaired lines 89–101, and the old/new-mode compatibility and changed-consumer boundaries. The repair does not weaken exact support, borrower versions, current-guard checking, native independence, old-owner migration or the UNSELECTED status. It introduces neither free additional capacity nor an in-place change to old FULL_FEATURE groups. The source/card review-status prose remains a conservative held-source description; this audit supplies the independent disposition without editing those artifacts.

**Final disposition: A1 CLOSED; conditional architecture proposition supported; exact-profile/support-repair investigation recommended; candidate NOT SELECTED and NOT OPERABILITY-QUALIFIED.** The next module remains the dependency-ordered minimal contract above, followed by an equal-service resource comparison. No protocol identifier, execution permission or project-completion claim follows from this review.
