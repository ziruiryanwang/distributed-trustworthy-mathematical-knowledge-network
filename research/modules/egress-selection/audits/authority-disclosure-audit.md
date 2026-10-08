# EGRESS1 independent authority and disclosure audit

Date: 2026-09-20. Reviewer: `commons_decentralization`, independent of the proposal author. Status: **EG-AUTH-001 closed at the repaired exact cut below; no remaining blocking authority/disclosure finding within this scope**. No implementation, native execution, extraction, executable model or measurement. This audit does not select EGRESS1 or amend frozen contracts.

## Exact reviewed cut and scope

Confirmed SHA-256 and read the complete [proposal](../proposal.md) at:

`5C98D1E2A78D74CCEE83AE868560770A6B330249D015CCCA7DF9FACA871B7E8A`.

Subsequently independently rehashed and reread the **complete repaired proposal** at `982C5613F88935F5EDA7F39DE3BA3980C4B7A331A9937C00461B46D3AD9C468F`. The original diagnosis and repair requirement below are preserved as review history; the final section records closure at that later cut, not approval of the initial wording.

The author’s earlier gap investigation is not independent review. This review concerns full-closure disclosure, exact source identity, native-only discovery, custody/publication separation, revocation and release authority. Detailed resource feasibility and scheduling are the separately assigned reviewer’s scope; the observations below do not certify that every maximum fits simultaneously.

Inherited contracts read include:

- [NETWORK](../../../../spec/OPERATIONAL-CORPUS-V1-NETWORK.md), scoped reads, reply disclosure checks, local checking/publication, retention and snapshots. Its NET2/current-profile amendments take precedence over historical versions.
- [E exchange](../../../../notes/analyses/CP-001E-exchange-scaling.md), exact inventory scopes, independent lease protection/disclosure, and seal/snapshot continuity.
- [E custody](../../../../notes/analyses/CP-001E-custody-contract.md), admission, explicit owner release and handoff.
- [G consumer bindings](../../../../notes/analyses/CP-001G-profile-and-consumer-bindings.md), PI1 public descriptors, capability negotiation and complete replay consumers.
- [F exact routing](../../../../notes/analyses/CP-001F-exact-routing-coverage.md), selected public cuts; [H resource/coverage](../../../../notes/analyses/CP-001H-resource-supply-and-discovery.md), selected targets and retained anchors.
- [V6](../../../../spec/OPERATIONAL-CORPUS-V6.md), distinct candidate/evidence/application events; [CACHESEL1](../../cache-selection/proposal.md), its explicit lack of publication and custody-release authority.

## Original finding EG-AUTH-001: admission cutoff is not a disclosure rule

Location: proposal “Closure of exposure, drain and explicit release,” especially the first paragraph and the paragraph imposing the horizon-plus-600-second endpoint.

The first paragraph groups the ordinary horizon, clock loss, explicit authority/disclosure revocation and guard failure. It closes new public-root admissions/current snapshots, removes this public grant, and retains historical snapshot interpretation/allocations. The later paragraph permits already admitted work to finish or be cancelled under inherited authority and bounds its endpoints by horizon plus 600 seconds. These statements do not explicitly select what survives **ordinary** horizon closure, or distinguish it from an actual withdrawal of the disclosure authority on which an existing reply/export depends.

### Minimal trace

At time `h - 1`, the source admits an export/read and creates a still-live export/snapshot pin. A computation commits an exact immutable response, but its separate delivery ticket is not yet claimed. At h the owner explicitly revokes the relevant disclosure scope/version. Its physical pin and some operational records remain funded until a time no later than `h + 600`.

Keeping those records/bytes cannot authorize the unclaimed response. NETWORK’s disclosure rule requires a delivery claim to revalidate the same exact scope/version and audience; withdrawal cancels an unclaimed disclosure and handles affected derived scopes through their actual authorization. If delivery was already claimed, withdrawal requests bounded cancellation, without promising recall of bytes already handed to transport. E’s export pin is explicitly independent of disclosure permission.

The proposal’s generic appeal to inherited authority points toward that safe result, so this review does **not** claim it demonstrably authorizes a private read. The defect is an under-specified operational branch at precisely the boundary this new policy controls. “Historical,” “admitted,” and “still allocated” cannot substitute for identifying live disclosure and execution authority.

### Required repair

State distinct outcomes for the relevant branches:

1. **Ordinary horizon closure:** specify whether all new executions funded by this exposure stop, including fresh paid calls on already issued leases, or whether a precisely bounded subset may still be admitted under independently surviving data authority. State the source of that authority and its applicable deadline/guards. The policy may conservatively select no new execution after h; that is a design choice, not an inherited universal requirement.
2. **Actual disclosure revocation:** explicitly preserve the mandatory scope/version/audience check, prevent unclaimed revoked disclosures, handle affected derived scopes, and apply bounded cancellation to already claimed sends. Do not imply that drain allocation or the 600-second ceiling overrides revocation.
3. **Protection and release:** retain physical and operational protections until their actual inherited termination/fencing conditions permit this scope’s versioned release. The 600 seconds is an upper bound on otherwise valid authority, never a fresh lease, execution grant, future delivery promise or automatic deletion event.

No new wire operation or remotely selectable collection is necessary for this repair. Clock/native incidents retain their applicable inherited conservative guards; ordinary clean admission rollover must not be mistaken for a new exposure or a disclosure revocation.

## Boundaries that compose at the reviewed cut

| Boundary | Source-level conclusion |
|---|---|
| Exact evidence and disclosure | Nomination binds JudgmentID, ProofInstanceID and the actual InstanceReplay. Preparation and public commit recheck the **whole** closure, not merely the conclusion. G’s closure includes the actual representative map and selected support. A private dependency blocks publication; a replacement witness cannot borrow the old replay’s permission. |
| Custody before publication | The independently qualified/protected exact singleton is activated through E before any public cut commits. A preparation failure can leave custody-only state; it is not public success. No native check or import is silently replaced by a nomination. |
| Native-only interface | The named collection is expressly a local nomination/ownership lane. Remote FIND uses the existing provider-wide authorized public projection and existing schemas/capabilities. No new collection argument, private CAS endpoint or remote egress command is introduced. |
| F/H isolation | Exclusion from automatic routed publication is checked before admission and again before public activation. An included target declines with `NEEDS_ROUTED_PUBLICATION_POLICY`; existing routing obligations cannot be disabled or charged as zero. This does not establish wide-area discovery. |
| No borrowed authority | Source service and receiver work require their own offers/tickets, scopes and allocations. A nomination, index entry, foreign observation or source signature creates no receiver pin or remote funding. This policy selects no broker, HINT or route operation. |
| Own grant versus other obligations | Removing this grant/posting ownership preserves another owner’s authorized entry. The explicit E release concerns the exact singleton and expected versions, not every copy of its bytes. Other custody/cache/use/export/anchor references survive under their own contracts. |
| Finite exposure versus preservation | The 24-hour interval is not pin expiry or an availability SLA. Failed release remains protected and counted. No receipt establishes a replacement custodian, permanent survival or permission to release someone else’s protection. |

These are conditional contract-composition checks, not evidence of runtime isolation or successful release. At the initial cut, EG-AUTH-001 remained material to the timed boundary despite the other separations being explicit.

## Nonempty successful disclosed-to-used path

The favorable trace is a genuine conditional path, not only refusal. Its premises must remain explicit: actual qualified compatible evidence, fully authorized closure, native-only configuration, sufficient source/receiver resources, relevant completed extraction, favorable consulted-prefix placement and actual progress during the live service interval.

Under those premises, E custody protects the exact B-associativity replay; the atomic public commit exposes its actual exact/STRUCT2 postings. A later investigator knows the source contact and its own B/op_B interface, not the answer theorem ID. Its ordinary Eq operand-pair query can retrieve the associativity descriptor because both theorem operands have the same rigid op_B head. Complete authorized evidence acquisition and independent native checking remain necessary after discovery.

The proposed four-factor use is mathematically nonempty. Writing `*` for this exact op_B and `a_B` for the checked associativity witness, the two applications

`a_B (x*y) z w : ((x*y)*z)*w = (x*y)*(z*w)`

and

`a_B x y (z*w) : (x*y)*(z*w) = x*(y*(z*w))`

compose by checked equality transitivity at the receiver. This is a paper explanation of the source trace, not an executed proof or a new source requirement. Its resulting artifact still needs its own later nomination, custody/disclosure and service path; neither prior application nor `PUBLIC_ACTIVE` publishes it automatically.

Conversely, an entirely sound result with private selected support must remain local under the stated refusal. A complete locally retained result can become unavailable to strangers after lawful public withdrawal. Neither case is mathematical invalidity, and no inspected contract promises that arbitrary unknown contacts find this source.

## Initial-cut disposition

EG-AUTH-001 was the sole open authority/disclosure finding at the initial cut. The initial audit requested one root-coordinated author repair with the separate resource review, followed by a fresh held hash for complete rereading. Only this audit file was authored; no proposal or frozen file was edited.

## Repaired-cut review and closure

Reviewed full source: `982C5613F88935F5EDA7F39DE3BA3980C4B7A331A9937C00461B46D3AD9C468F`. Root supplied the held cut after a coordinated author repair; the reviewer independently confirmed its hash before reading it completely. Closure is based on those exact bytes, not the repair request or an author's assurance.

### EG-AUTH-001 repair

The repaired “Closure of exposure, drain and explicit release” now selects distinct branches:

- **Ordinary horizon:** close new offers/calls/execution claims, including fresh calls on old leases; cancel unclaimed operation **and delivery** tickets, including already computed responses. Only previously claimed operations/deliveries may continue under their still-valid guards/endpoints. A computation finishing afterward cannot obtain a new delivery claim. This is an expressly chosen conservative service cutoff, not a claim that all inherited leases universally behave this way.
- **Actual disclosure withdrawal:** invalidate the exact authorization/version and affected dependent read/export/snapshot/delivery scopes immediately. Cancel unclaimed affected work; running work rechecks before commit; already claimed sends receive bounded cancellation. Already disclosed bytes are not recalled, and an independent grant survives only if it does not depend on the withdrawn permission.
- **Drain and protection:** the root horizon, or the mixed-query horizon H, plus 600 seconds bounds otherwise valid authority only. Records and recovery obligations can remain charged beyond that ceiling. E's pin survives until the explicitly authorized, version-checked release transition; retained bytes or drain resources do not create permission.

The minimal initial countercase is therefore resolved: a computed but unclaimed response at h cannot begin delivery after either the selected ordinary cutoff or actual revocation. A delivery claimed earlier is not treated as still unclaimed; its permitted continuation/cancellation follows the appropriate branch. No new remote certificate or operation was introduced.

### New whole-cut discovery binding

The repaired source adds a fixed pre-work sponsor for provider-wide FIND. This reviewer checked its **authority composition**, not merely whether some account can pay:

1. Sponsorship explicitly permits funding the whole ordinary provider-public snapshot, including nonmatches and independently public roots. It does not change the predicate or create a remote collection/sponsor field.
2. Before work, the binding includes the fixed payer, actual cut/disclosure-version summary, all currently active EGRESS dependencies and applicable independent guards. If bounded existing control state cannot establish this, the request declines rather than scanning private material for free or assuming authorization.
3. H is the minimum horizon of those EGRESS dependencies. With A ending at 10 and B at 100, a B-sponsored snapshot containing A still stops at 10, even if the page happens to return only B. The source explicitly includes this reverse-sponsor case. Payer identity and result contents do not extend scope authority.
4. An old cursor cannot migrate to B or silently drop A. A separately admitted fresh query after A's withdrawal can use the new current cut. A dependent permission revoked before H still invalidates the old scope; independent grants are not globally revoked merely because A ended.
5. Root-named evidence reads/exports independently bind their actual eligible source grant. Paying for FIND never confers permission to read a proof's closure.

For mixed snapshots, the full-cut dependency binding and H govern new claims and the selected cutoff; this is not merely a reminder to stop future continuations. Previously claimed work remains subject to the explicit disclosure branch and tighter inherited limits. A generic 600-second grace cannot bypass a shorter dependent horizon or its revocation.

### Continued positive path and other boundaries

The complete reread preserves whole-closure permission before custody/public commit, exact PI1 replay identity, native-only publication with explicit F/H exclusion, and release of only this policy's owning reference. A concurrently independent grant or H anchor keeps its own actual authority/protection and costs; old snapshot state cannot be rewritten as a new grant.

The new pre-extraction publication/control reservation is an allocation and stop limit, not a disclosure certificate or prediction that unchecked metadata are correct. Its eventual public transaction still validates the actual complete prepared cut and exact closure permission.

The successful path is now supplemented by explicitly stipulated source/receiver resources, an eight-descriptor posting with the result in third position, and completed independent reuse before the horizon. This makes the favorable known-contact path less vacuous while retaining the two actual associativity applications explained above. The warm core is charged prehistory; actual export, native compatibility, sizes, timings and usefulness remain unperformed premises. This review does not convert those stipulated quantities into measurements or certify every resource dimension beyond the separate resource audit's scope.

**Final disposition:** EG-AUTH-001 is closed at the repaired hash above. No remaining blocking authority/disclosure contradiction was identified within this review's scope. The result establishes paper-level composition of the selected authority transitions, not implementation qualification, global discovery, uninterrupted service, durable remote handoff or perpetual preservation. Root integration/selection remains a separate decision. Later substantive changes to closure permission, snapshot dependencies, cutoff, publication or release require renewed review.
