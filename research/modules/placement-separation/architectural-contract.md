# Stable placement authority and immutable logical index runs

Date: 2026-09-20. Author: `placement_scope_separation`. Status: **UNSELECTED architectural investigation, held for independent review**. This is a bounded candidate, not a selected extension or a complete wire specification. No opcodes, capability numbers, object types or schema versions are allocated. No implementation, executable model, extraction, native checking run or benchmark has occurred.

## Decision being investigated

Separate the authority that owns a provider's routing placements from the immutable local runs used to organize that provider's mathematical index. Keep exact finite membership and support obligations, but do not require a remote ownership change solely because a local run is split or merged.

The target improvement is precise: **pure local representation-preserving compaction can have zero remote route mutations**. It does not mean zero local work, zero renewal, free eligibility checking, free collection, seamless adoption from existing groups, or unlimited growth. No mathematical truth depends on whether this optimization is selected.

## Exact evidence and existing compatibility boundary

The following line references identify the frozen evidence used for this investigation; the linked documents define the contracts.

| Evidence | Consequence |
|---|---|
| [F exact coverage](../../../notes/analyses/CP-001F-exact-routing-coverage.md), lines 39–47 | A holder group has an immutable scope namespace. Holders do not obtain/check the whole source scope. Each cell/provider row has one actual owner; changing groups requires old DROP before new PUT. |
| F exact coverage, lines 62–88 | New groups are empty; mutations/renewals use exact current roots and versions; old lifecycle generations, snapshots and delayed GC retain real charges and fences. |
| [G structural retrieval](../../../notes/analyses/CP-001G-structural-retrieval.md), lines 187–215 | ProviderAd2 omits scopeID. Its producer anchor chain really emits the key. FeatureScope is an immutable exact target/token commitment; operation 20 creates FULL_FEATURE and every renewed token needs support inside that exact scope. |
| [G bindings](../../../notes/analyses/CP-001G-profile-and-consumer-bindings.md), lines 39–51 | Existing K4 ads and maps are explicitly profile-bound. The holder checks bounded metadata, not theorem evidence. Old group modes cannot be changed in place. |
| [H shared coverage](../../../notes/analyses/CP-001H-resource-supply-and-discovery.md), lines 100–146 | Provider-wide target postings can borrow one provider/token row, but the selected publication owner is still an exact immutable scope containing its eligible anchor. |
| H, lines 148–160 | Consolidation transfers actual owned rows into a new immutable scope even though native objects and target postings need not change. |
| [O normalization](../reciprocal-operability/batch-normalization-contract.md), lines 38–78 | Logical splitting changes owner scopes, invalidates dependent caches before mutation and performs actual group migration; no group-free bookkeeping shortcut is selected. |
| [N recovery](../reciprocal-operability/routing-recovery-contract.md), lines 9–37 | Recovery is tied to a finite admitted key/owner/path/eligibility cut. Changing a publication-scope owner invalidates the affected claim; physical replacement under the same owner need not. |

The missing distinction is not native correctness versus untrusted metadata: F/G already make that distinction. It is **stable operational authority versus immutable logical membership scope**. A holder's inability to check a whole scope does not license the producer to violate its agreed scope contract.

## Four separate state domains

Fix one provider p and exact foundation/extractor pair F/E. All sets below are finite, receiver-owned and inside admitted count/byte/work allocations. Separate providers do not share ownership by presenting the same evidence or key.

**Semantic publication cut C.** This records the exact selected public descriptor/evidence entries, their completed deterministic token sets, actual current eligibility dependency versions, and the actual provider FIND posting relation. An entry i includes its target reference, StructuralDescriptor ID, PublicIndexDescriptor ID, exact InstanceReplay ID and descriptor/selection versions. Alternative replay contexts remain distinct where the inherited consumer requires them. A digest alone is not the map or proof that its records are eligible.

**Physical run layout R.** Immutable local runs, posting segments, manifests and their physical retention references implement the selected semantic relation. Changing R need not change which entries are selected, their tokens, or their evidence/publication authority. Old run roots remain charged while scans, preparation, outcomes or other real owners retain them. Not every proposed split/merge preserves C; a layout rewrite that omits a posting is not pure compaction.

**Placement authority A.** A separately typed owner-local authority record binds `(p,F,E,namespaceID,authorityGeneration)` and a finite local lifecycle/allocation. Its namespace identity remains immutable while its admitted membership changes. It is not a FeatureScope hash, not an assertion about a target union, not native evidence and not permission to use arbitrary resources. A declared namespace generation cannot be resurrected by an old snapshot or copied receipt. Concrete canonical allocation, persistence and exhaustion rules remain to be specified before protocol selection.

**Actual remote placement state.** For every key k, one owner record binds A, current desired anchor/ad, monotone owner/eligibility transition versions, intended copy obligations and exact observed group/cell/row states. During actual migration it records old and new owners per row rather than overwriting observation with intention. Holder groups retain immutable authenticated provider/F/E/mode/A bindings, exact member roots/counts/bytes, nonwrapping state versions, local lease gates and allocation histories. A namespace can have many independently admitted holder groups. New empty groups do not restore forgotten rows.

**Per-holder uniqueness.** The proposed new mode inherits F's uniqueness discipline under its new exact binding: at most one ACTIVE group exists for `(holder,p,F,E,A/generation)`, including an empty ACTIVE group. Matching OPEN is idempotent with respect to group creation: it returns that exact current group's observation without extending its lease or creating a second group; mismatched immutable bindings are rejected. Opening/reservation/recovery transitions must serialize so concurrent or uncertain attempts cannot allocate duplicate ACTIVE groups. The actual new request/result encoding remains unspecified. If the existing group cannot admit another member, additional grouping requires a genuinely separate admitted namespace with its own obligations, or a future explicitly different multiplicity contract and corrected cost bound; an extra group cannot silently reuse this uniqueness premise. CLOSED/EXPIRED/unreclaimed generations, opening/uncertain reservations and old-mode migration overlap remain separately charged and are not bounded by the ACTIVE uniqueness rule.

The distinctions matter even when one implementation stores several records in the same database. Neither semantic-cut IDs nor namespace IDs are bearer capabilities. The single authoritative local writer and existing one-shot spending/disclosure boundaries remain required.

## Minimal replacement support relation

For one exact producer cut C and current dependency observation v, define `Support(C,v,i,k)` only when all of the following hold:

1. i is an explicitly selected entry in C, not a dangling record from a retired run.
2. i has a complete accepted native replay under the locally adopted F; its actual required closure is retained/protected and currently permitted for the relevant public service under v. An old acceptance observation cannot waive a current incident, withdrawal or protection guard.
3. Its exact completed STRUCT2 descriptor under E includes k. Hardware interruption is not completed extraction. The descriptor/target/root/replay relationships satisfy G's unchanged typed bindings.
4. Its actual PublicIndexDescriptor structural hint, signed-ad anchor descriptor and anchor replay agree when i is used as that key's anchor. The provider identity, F/E and signed key are exact.
5. The required current provider FIND posting for i and k exists at the declared semantic cut. Possessing an anchor's bytes alone does not make selected new targets searchable.

Define `EligibleAnchor(C,v,k,ad)` to mean there is one such exact i and ad binds its chain under the ordinary signature/revision rules. The witness is an explicit producer-owned reference, not an existential claim accepted from another agent. A change to that witness is not invisible because its emitted token happens to be the same.

For each selected entry j and each emitted token k, the coverage obligation resolves the unique current `(p,F,E,k)` owner record. It requires `EligibleAnchor`, j's own current eligibility/posting, actual required-copy and ancestor-marker observations with their ages, and a settled owner state. Failure of any clause yields the corresponding PENDING/PARTIAL/DEGRADED/TRANSFERRING/UNKNOWN observation. Shared tokens do not establish a conjunction match, query recall, future availability or native acceptance.

The replacement is therefore not “any token can enter a dynamic namespace.” It removes **membership in one immutable owner FeatureScope** as the support boundary, while replacing it with membership in the exact finite current producer publication cut and explicit per-key anchor support. This changes the producer contract and needs a new name/profile; it is not old FULL_FEATURE with a looser interpretation.

## Eligibility summaries, borrowers and linearization

Before a group mutation/renewal is authorized, the producer must establish support for the exact requested membership and anchor bindings under current relevant guards. A reusable summary binds at least A/generation, exact groupID/memberRoot, every grouped ad/anchor, and the precise local dependency versions that establish support. Its actual representation may be incremental, but a count, namespace name, old scope hash or one surviving theorem is insufficient. Any dependency whose uncertainty can affect support dirties the dependent assertion; paid revalidation or nondecision follows.

A group memberRoot can remain unchanged while native/disclosure support changes. Conversely, a physical index manifest may change while support is preserved. The summary implementation must distinguish these cases using a complete paid preservation or dependency argument. This document does not specify an efficient universal dependency-summary data structure, infer O(1) revalidation, or authorize skipping a scan when the retained summary cannot justify the exact current relation.

Borrowers keep a reference to the stable provider/key owner record. Cached coverage binds its exact relevant owner/eligibility version, not merely a stable namespace. At the authoritative local transition boundary, mark affected ownership/support assertions dirty or transitional and advance the applicable nonwrapping version **before** dispatching a change that could invalidate the old assertion. A single versioned indirection can invalidate many cached borrowers without instantly rewriting all of them; each consumer must actually recheck the version before a new current claim. Recomputing their aggregates or enumerating reverse dependents remains separately metered. An implementation retaining unversioned copied ownership requires a paid complete update or must decline the transition.

Pure compaction publishes one guarded new local layout cut only after exact semantic preservation has been established against the still-current input versions. If a concurrent eligibility edit changed those versions, commit fails/replans rather than mixing cuts. The authoritative transaction can advance the local layout/snapshot cut while preserving the same finite semantic-map commitment and support dependency versions; these identities are not one interchangeable global epoch. It does not announce a foreign atomic operation. Source scans already bound to old authorized immutable index cuts remain historical and retain their real allocations; new scans bind the new current cut and its authority. Existing current-vs-historical disclosure rules still apply to delivery.

Withdrawal/incident linearization prevents **new producer authorizations** from using invalidated support. It cannot cancel a previously issued remote mutation that is already claimed, erase existing remote leases, or recall delivered bytes. Outstanding exact actions must be settled/cancelled under their real one-shot state; possibly committed rows remain uncertain/charged. A late admitted renewal can leave a stale routing lead, which the current provider must not turn into native/public authority. A claim of quiescent withdrawal additionally requires those restoring actions to be settled and actual DROP/expiry conditions observed. No global instantaneous withdrawal is promised.

## Transition and obligation table

| Transition | Producer authority and semantic work | Remote effect and truthful status |
|---|---|---|
| Create A | Authenticate local owner; allocate fresh nonreused namespace/generation and finite lifecycle/work/stock | New negotiated empty groups only when separately admitted, with per-holder ACTIVE uniqueness and matching idempotent OPEN; no inferred rows or coverage |
| Add selected entry with already owned tokens | Check/protect actual native closure; complete extraction; commit exact postings/borrowed obligations under current guards | Existing ads may remain untouched only if their own anchors remain eligible; coverage waits for all real dependencies |
| Add genuinely new token | Establish explicit support; admit owner/row/group/lookup/marker/renewal obligations against supplied limits | Actual lookup and permitted OPEN/PUT, with partial outcomes retained; no free placement |
| Pure logical compaction | Freeze finite input plan; build exact output relation; reserve peak state and work; compare relevant current versions; commit new R with C preserved | No change to A, ads, group ownership or member roots is required; normal renewals and independent failures continue |
| Replace anchor under same A | Establish new complete eligible chain; invalidate affected cached support; advance ad revision and guarded owner-support version | Paid same-group PUT replacement where allowed; exact per-row observations, lost outcomes and old snapshots count |
| Remove entry / native incident | First invalidate affected current assertions; preserve independent custody/disclosure duties; choose actual surviving supports or mark degraded | Replace/DROP affected members before a newly authorized containing-group renewal; otherwise withhold renewal. Existing stale leads are not native authority |
| Refresh holders/path | Preserve admitted owner where valid; update actual old/new placement observations and capacity | Existing paid placement/withdrawal mechanics; different holders do not imply independent failure domains |
| Split/replace placement authority | Admit finite overlap, exact destination support, per-row transfer and borrower invalidation plan | Real old-owner DROP before new-owner PUT at the same cell/provider; no new atomic move primitive |
| Retire A | Stop new authority; settle outstanding actions and all member/custody/history obligations | Close/expire actual groups lawfully; retain generation-fenced histories and physical bytes until real release |
| Recovery after uncertain state | Restore coherent exact source/holder history or fence/readmit; never infer membership from a familiar count | No old grant replay, namespace resurrection, version wrap or GC against replacement generation |

Every transition needs bounded parse/plan/commit work, actual metadata/RAM/I/O admission and one-shot authority. A merely affordable happy-path estimate is not an admission test. Concurrent mutation and renewal use the exact existing group expected-version/member-root serialization. Stable namespace identity does not relax that contention.

## Conditional no-remote-compaction proposition

Write `RepEq(C,R,R')` when both layouts represent exactly the same finite canonical selected-entry records, descriptor/token sets and posting relation in C. It requires equality of the exact identifiers/versions, not equality merely of row counts or token unions. Checking it may use completely justified bounded persistent-map invariants or admitted traversal of the full selected relation; the cost is supplied either way. It is **not** mathematical equivalence of two theorem statements, equality modulo Lean conversion, or a universal semantic search. Different proofs/representative contexts cannot be substituted through this predicate just because their conclusions look the same.

Let state before compaction have a finite selected semantic publication relation C, layout R, actual ownership O and remote placement state P. Assume:

- The admitted local transformation establishes `RepEq(C,R,R')`, without changing any relevant native/disclosure/retention guard.
- O, signed ads/anchor chains, required cells/markers and actual remote group owners/member roots are unchanged.
- All local commit, storage and outstanding-reader obligations fit their real allocations; current eligibility summaries are either valid for the unchanged relations or lawfully rebound before reuse.

Then each coverage clause above has the same semantic witness and placement observations before and after the local layout commit. The representation change therefore requires **zero new remote route mutations** to preserve that observation. Its proof is clausewise substitution of unchanged C/O/P; no holder interprets a logical run ID as its placement authority.

This is a noninterference claim, not a network liveness theorem. Remote leases may expire or holders fail concurrently; the same observations remain historical, not newly refreshed. If a token, selected entry, anchor, eligibility dependency, path or placement owner changes, the hypotheses fail for the affected obligation. The proposition establishes neither efficient local equality checking nor that compaction can finish within a requested deadline.

## Small positive trace

Use one provider, fixed F/E and fresh candidate placement authority A with actual resource admission. Initially target x emits `{a,k}` and target y emits `{b,k}`. Both are independently checked/retained/public, and the actual provider index contains their corresponding postings. Use x as the eligible anchor for k. There are three unique provider keys, not four token incidences requiring separate ownership.

1. Real initial operations place a, b and k at four selected admitted holders each. Actual group IDs, roots, leases, snapshots and source support summaries are recorded. There are twelve selected rows; the holder sets need not coincide.
2. The local layout has runs Rx and Ry. A paid exact transformation creates Rxy and commits it only if the selected semantic/support inputs remain current. The three signed ads and twelve rows are unchanged; no remote migration is required by this compaction.
3. Independently checked target z emits `{c,k}`. Its local postings and borrowed k obligation are admitted. Only new key c needs its actual lookup and four placements; k's eligible anchor remains x. Existing obligations still require their scheduled renewals.
4. A subsequent paid compaction of Rxy and Rz likewise changes no remote ownership if the stated relations are preserved. Old physical runs remain charged until their actual readers/outcomes/protections permit release.

This is nonempty index growth and discovery-preservation reasoning. It is not a measured useful-mathematics yield, a calendar, a theorem that z is valuable, or evidence that the initial placements or native checks have been executed.

## Counterexamples and recovery traces

### False free renewal

Let one active group contain ads for a anchored by x and b anchored by y. Both roots and the namespace remain byte-identical. Withdraw x's relevant public authority, leaving y eligible. Renewing the unchanged group from its old memberRoot summary improperly renews a: the group root describes membership, not current support. Correct behavior first invalidates the dependency summary, then either installs a separately eligible anchor for a or successfully drops a before a newly authorized renewal. If that funded work cannot complete, the group is not newly renewed. This can degrade b's future availability too; shared renewal creates a real blast-radius tradeoff.

Safe withholding alone is not a successful continuing service policy. Before selection, supply a bounded incident-repair queue and lease-aware paid DROP/replacement opportunities so that, under the stated finite incident load and willing holder response, an invalid member can be removed and the surviving exact group renewed before its required deadline. Cheap invalidation may be local; the removal, map update, outstanding-action reconciliation and renewal are not free. Admission must account for this reserve, or explicitly reduce new input, repartition through paid transfers, or report degraded service. Unlimited incidents, unavailable holders or exhausted supply prevent a universal recovery guarantee; repeatedly withholding the valid member forever is not called operability. An exact scheduling/queue bound is an open contract, not supplied by this architectural note.

### Stale borrower

Run Rz borrows k's owner record at version 8. The anchor is invalidated while Rz's cached aggregate remains unchanged. The invalidation boundary advances the relevant owner/eligibility version and marks it degraded. Rz cannot claim current coverage by reading version 8 from its old run manifest. If the consumer never resolves the current version, stable namespaces merely hide a stale-cache bug; that implementation violates the proposed contract.

### Version and generation ABA

A source restores an old backup after namespace/group retirement and attempts renewal with the same familiar identifiers. Reusing a namespace generation or wrapping a version could make the request resemble a current action. Require durable nonreuse/exhaustion discipline and exact one-shot authority; uncertain recovery takes a new authority/readmission path. A delayed sweep naming the old group/storage generation must not delete the replacement row. Exact generation derivation and recovery encoding are still preselection specification obligations.

### Compaction failure and rollback

Before the local layout commit, a partial output is temporary charged state; existing R stays authoritative. Release the unfinished output only through its actual no-reader/no-owner fence. After commit, rollback is another guarded layout transition preserving the then-current semantic relation; an old retained R may not contain later contributions. Reinstalling it blindly would lose postings and could resurrect withdrawn support. Native bytes remain governed by their independent custody/protection owners throughout.

### Migration from old FULL_FEATURE groups

For a key currently owned by old FeatureScope S, creating A does not move its row. A new group PUT at the same cell/provider conflicts until the exact old-owner DROP is settled. If the DROP reply is lost, reconcile the retained action outcome or exact authoritative observation before insertion; do not assume absence. After the new PUT, an old-group sweep remains fenced. Other real copies can provide continuity only while actually eligible/reachable. During partial migration, expose TRANSFERRING/PARTIAL and retain all charges. Returning to old mode is another paid owner transfer, not a rollback flag or in-place mode mutation.

### Adversarial namespace proliferation

One authenticated provider opens many namespaces or repeatedly retires/reopens one conceptual collection. Without provider-wide count/byte/control admission this evades per-namespace limits. Count opening, active-empty, active-nonempty, retiring, uncertain and unreclaimed generations together against actual aggregate supply. Repeated names, identities or interval boundaries do not replenish spent authority. A namespace carries no duty for a holder to accept arbitrary future keys.

## Bounded lifecycle, capacity and resource controls

The candidate requires explicitly admitted finite ceilings for selected semantic entries/incidences, distinct owned keys, namespace generations, active/retired/uncertain groups, selected/transient rows, layout histories, summaries, snapshots, outstanding actions and total bytes. CPU, RAM, disk, I/O, traffic, per-call limits, concurrent executors, periodic renewals and finite preparation calendars must fit jointly. These quantities are parameters of a supplied profile, not new default grants in this note.

Stable authority cannot exceed the inherited holder member/byte limits. A holder may refuse new keys in an existing group while the namespace remains otherwise valid. Several bounded namespaces may be needed, or real capacity-driven repartitioning may be required. Such repartitioning has paid ownership-transfer and borrower-invalidation costs. Logical compaction does not solve it.

Keep exact admission for new members and their retention through the existing lease deadline. Extending a lease pays actual additional byte-time and operation work. Grouping does not renew ancestor markers, establish current reader overlap, keep an unlimited contact cache, or supply independent hardware. Local and remote old maps/snapshots/outcomes/fences remain counted until actual reclamation; source arithmetic does not command remote GC.

Larger stable groups reduce some control overhead but concentrate serialized mutation contention and incident-driven renewal refusal. Any efficient dependency-summary design must be evaluated under large shared-support incidents, not just unchanged-anchor happy paths. Deciding to retain a stable anchor is a real custody cost and never overrides owner withdrawal or native invalidation.

## Cost comparison and shifted work

Let U be the number of unchanged owned keys in a merge, r the chosen copies per key, M the actual willing holder population and Ui the disjoint owned-key counts across current publication owners. For fixed selected placements without extra generations:

- Current H/O scope migration changes rU row owners, requiring `2rU` successful DROP/PUT mutations, plus actual OPEN/CLOSE, retries, summaries, map updates and history. With general batching, mutation count and call count are different; batching unrelated authorities is impossible.
- Candidate pure compaction requires zero such remote mutations under the proposition. Local relation construction/verification, hashing, maps, peak storage and history release remain real costs.
- Current settled group count is bounded by `sum_i min(M,rUi)` across immutable publication owners. If one admitted stable namespace can contain the same settled key set, its corresponding bound is `min(M,r sum_i Ui)`: there are at most M such nonempty ACTIVE groups by per-holder uniqueness, and each contains at least one of the `r sum_i Ui` selected rows. These are upper bounds for the settled selected groups, not equality or universal savings. Multiple capacity-driven namespaces change the sum again. Empty, opening, uncertain, retiring, expired and unreclaimed generations, and any old-mode adoption overlap, retain their separate actual stock/renewal charges; this bound does not bound all lifecycle state.
- In a highly dispersed network M may be at least rU, and almost every row can still occupy its own group. Grouping then gives little renewal saving. Nothing here restricts the network to 256 or any other small number of holders.
- New-key placement, changed anchors, real holder/path recovery, markers, ordinary renewals and paid failures remain. Adoption from current groups incurs a genuine migration before later savings are possible.

For an insertion-only bounded epoch with fixed keys, current H charges logarithmically many scope migrations to an inserted key. Stable authority removes the **logical-compaction contribution** to that charge, not churn or capacity-driven ownership changes. The candidate supplies no numerical service improvement until actual membership distributions, summary costs, contention, retained tails and native workload are measured under equal supplied resources.

## Existing-interface alternatives

| Alternative | Already possible | Remaining limitation |
|---|---|---|
| Retain old immutable publication owner scopes while locally reorganizing FIND data | Their unchanged eligible anchors/groups need no scope transfer merely because local storage layout changes | Old owner scopes/groups remain real; tiny-scope multiplication and scope/renewal limits persist. This is not H's completed consolidated-owner state. |
| New entries borrow already covered tokens | H already allows zero new routing work when all their tokens are covered and anchors remain eligible | Native checks/postings are not free; novel keys still need an eligible immutable publication owner under current mode. |
| Use ungrouped K4 ads | Existing negotiated G record domain permits the base route path; [F routing](../../../notes/analyses/CP-001F-dissemination-and-routing.md), lines 65 and 106, has per-row PUT/renewal | Loses grouped renewal amortization; moving an existing grouped row still requires lawful old-owner removal. |
| Keep a fixed immutable scope that supports all future used keys | Compatible only where those actual target descriptors and emitted keys were already present and remain eligible | Unknown future novel keys cannot be inserted by pretending they were in that immutable scope. |
| Known-contact native or candidate-only broker service | [I direct bindings](../../../notes/analyses/CP-001I-direct-broker-bindings.md), lines 7–11 and 159–161, provide the explicit contact-based alternative | No selected unfamiliar-broker routing. This changes discovery assumptions and is not an equal-service replacement for the routed path. |

No new architecture is necessary for those restricted cases. The proposed module targets continued novel-key growth with grouped placement authority independent of logical index-run reorganization.

## Change impact and incomplete consumer contracts

| Consumer | What remains unchanged | Required new specification before selection |
|---|---|---|
| F holder mechanics | Authenticated owner, expected root/version, bounded paid mutations, row exclusivity, lease gates and GC fences | A distinct negotiated stable-authority group mode/open contract and exact result/profile binding; no old ScopeID reinterpretation |
| G records/native/query path | ProviderAd2/K4 anchor bytes, exact STRUCT2 extraction/FIND semantics, independent full native checking | Separate name/status for current finite support/coverage; explicit capability/consumer whitelists and fallback behavior |
| H sharing | One provider/key owner, actual provider-wide postings, counted borrowed obligations | Replace owner FeatureScope support with the finite guarded relation above; separate logical runs from placement authority and specify summary updates |
| N recovery | Paid finite key/path jobs, real holder admission/reader overlap and honest age observations | Fresh owner-cut binding for A/generation and relevant support versions. Existing N cuts do not automatically acquire the new meaning. |
| O normalization | Exact target partition/mass preservation can remain useful locally | New mode's local-run transformation is not O's selected remote-owner transfer. Mixed old/new inputs and migration need explicit admission/status rules. |
| P joint growth epoch | Its native reciprocal trace and actual old-mode obligations remain historical evidence | Do not subtract P's carry costs retrospectively or claim its schedule validates the candidate. An independently supplied comparison is needed. |
| Current continuation witness | Selected F/G/H/O behavior and actual P day-24 inherited state | No candidate savings may enter that proof unless a separately selected/admitted migration is explicitly added later. |

Still unspecified: canonical stable-authority identity/state persistence; new capability and OPEN/result schemas; mixed-profile error/status dispatch; precise finite summary representation and invalidation completeness; namespace capacity allocation/partition policy; finite incident-repair scheduling and its surviving-member service bound; concurrent local support authorization versus remote action settlement; restart/migration conformance suite; and an actual jointly supplied operating case. Existing F/G one-shot mechanics constrain these obligations but do not define every new field or consumer automatically.

The narrow proposition is supportable without resolving those details. A deployable protocol is not. The next step is an independent architectural audit deciding whether this separation warrants exact profile work, followed by resource/consumer comparison against the unchanged-interface alternatives. This source neither selects that profile nor closes actual native feasibility, continued supply or useful-growth qualification.
