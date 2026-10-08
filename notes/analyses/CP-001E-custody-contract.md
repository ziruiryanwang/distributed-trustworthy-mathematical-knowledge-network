# CP-001E: local collection custody contract

Date: 2026-09-19  
Status: Selected concept contract; no implementation, executable model, or reliability measurement  
Scope: Local owner-authorized durable custody using existing paid native exchange; no new network opcode or remote permanence claim

## Selected boundary

The first custody profile is **local-only**. A node can maintain an exact finite preservation scope, funded durable pins, finite maintenance jobs, and a bounded authenticated local status interface. Another node may observe existing public provider/RetentionAck records or acquire explicitly public bytes through funded reads/exports. It does not receive a new authoritative wire assertion named `PreservedUnderPolicy`, a remote storage mandate, or a guarantee of forever.

This selection closes an operational gap in the [preservation analysis](CP-001E-preservation-over-unbounded-time.md). It does not modify frozen CP-001D and introduces no research goals, assignment registry, human-intention fields, or attribution requirement. Selecting already existing artifacts for storage is an operational collection decision.

The selected retention rule is a durable **owner-release-required allocation**, not an expiring warm cache. Its byte/count capacity is finite. Maintenance, status snapshots, imports, observations, and handoff attempts each use finite grants and deadlines. Expiry of one such job does not silently release a still-authorized durable pin. The owner can explicitly end this discretionary custody according to its policy; the contract does not make that discretion an infinite-lifetime promise to strangers.

The proposal assumes an explicitly qualified native foundation and checking route. The frozen v4.22.0 pin is historical, not a deployment recommendation while its subsequently reported kernel-soundness issues are being repaired/qualified. Physically retaining old evidence is different from permitting current mathematical reliance on it.

## Two preservation modes

Each immutable scope uses exactly one mode. A mixed collection is represented by two scopes, not an ambiguous per-result notion of preservation.

| Mode | Exact selected target | What a replacement may preserve |
|---|---|---|
| `EXACT_REPLAY` | A sorted finite set of exact ReplayIDs, each with its full native closure | The same canonical payload bytes/identities, although a qualified lossless physical encoding may reconstruct them |
| `JUDGMENT_RECOVERY` | A sorted finite set of exact JudgmentIDs, each paired with one or more selected current native proof/replay witnesses | A different independently checked permitted proof of the **same exact JudgmentID**, with complete retained replay closure |

EXACT_REPLAY supports proof and nonproof replay roots, including definitions or declaration groups. It does not treat a smaller proof of the same statement as retaining the original proof bytes. Once the last copy of one exact replay disappears, that exact-byte target is not fulfilled merely because someone can prove the statement again.

JUDGMENT_RECOVERY requires a proof-root ReplayID whose Proof actually names the exact target JudgmentID, permitted footprint, and qualified checking basis. The selected evidence map is explicit and versioned local state; a name, embedding, remote acceptance, or proposed future proof is not a witness. A target with no currently permitted complete evidence is degraded/unknown, even if it was historically proved.

A different foundation/profile or different statement encoding normally gives another JudgmentID. This initial custody contract does not silently identify it with the old target. Cross-foundation or representation-changing theorem transport requires a separately qualified checked mapping and an explicitly new owner-authorized scope/contract. A corrected checker cannot inherit a known-affected old ACCEPT by describing it as the same mathematics.

The statistical model of losing all r copies can be applied to the exact selected evidence representation. It cannot by itself prove that no alternative witness, archive, coded reconstruction, or future rederivation could recover the judgment. Which of those is admitted recovery evidence depends on the selected mode and actual checking contract.

## Local records

These are precise conceptual local records, not new public CAS types or remotely readable operational objects. Field order below fixes the selected logical shape for a future codec. References are exact typed IDs or local allocation handles; optional fields use an explicit absent/present tag. All counts, versions, timestamps, and arithmetic have checked ranges. Display labels, if retained, are nonauthoritative local metadata.

### Immutable policy

`CustodyPolicy = [version, mode, ownerAuthorityID, releaseRule, allowedNativePolicyID, checkingMaterialPolicyID, capacityVector, recurringWorkPolicy, replicaObservationPolicy, statusLimits]`.

- `version = 1` selects this contract.
- `mode` is one of the two modes above.
- `ownerAuthorityID` names the local authenticated authority permitted to activate/reconfigure/release the scope; a network peer cannot acquire it by sending a record.
- `releaseRule = OWNER_RELEASE_REQUIRED` is the only initial rule. An owner-controlled agent can exercise explicitly delegated local authority, but remote hints/receipts do not become release commands.
- `allowedNativePolicyID` fixes admitted foundation/checker/footprint policy; current local incident guards still apply.
- `checkingMaterialPolicyID` identifies exact locally supplied verifier/bootstrap/runtime-material requirements and their owner-controlled installation policy.
- `capacityVector` separates retained payload, native/control metadata, staging, maintenance CPU/I/O/network, queues, concurrency, and record allocations.
- `recurringWorkPolicy` specifies intervals, per-occurrence ceilings, periodic funding ceilings, fair cursors, and renewal authority; a timer is not a grant.
- `replicaObservationPolicy` specifies a finite target count and candidate-provider/observation limits; distinct keys are not automatically independent failure domains.
- `statusLimits` bounds authenticated local query work, snapshots, encoded replies, and history.

Its `PolicyID` binds those immutable fields. Changing it is a new owner-authorized policy transition, not rewriting an old promise or refilling resources because the hash changed.

### Immutable scope and mutable evidence selection

`CustodyScope = [version, PolicyID, orderedTargets]`.

For EXACT_REPLAY, a target is `[ReplayID]`. For JUDGMENT_RECOVERY, it is `[JudgmentID]`. The target sequence is sorted and duplicate-free. The future codec may use bounded immutable pages, but the admitted finite complete sequence and its scope commitment must be checked; a truncated list cannot masquerade as the selected collection.

`EvidenceSelection = [scopeID, selectionVersion, [[targetID, selectedReplayIDs]...]]`.

Each exact-mode target selects exactly itself. Each judgment-mode target selects between one and the policy's bounded number of qualifying proof-root replays when owned; an empty set is permitted only as an explicitly degraded unresolved state or after release. For an owned target, current qualification of each selection is bound to its exact current native assessments, not a preferred provider name. A released target's retained selection is historical metadata, not evidence of current protection or qualification. Alternative selected witnesses have separately visible costs and footprints.

`TargetOwnershipState = [localCustodyID, scopeID, ownershipVersion, [[targetID, ownershipCode, lastOwnershipTransitionReason]...]]`.

This bounded, sorted map has exactly one row per immutable scope target. Before whole-scope activation its rows are `UNACTIVATED`; the activation transaction changes every row to `OWNED`. After activation the only ownership transitions are `OWNED -> RELEASING -> RELEASED`. A released row cannot silently reacquire ownership; acquisition needs a new owner-authorized scope/local custody instance and full admission, even if the immutable target list happens to have the same scopeID. Target health/degradation is a separate facet and never changes ownership by itself. The immutable scope remains the original admitted target set; it is not a claim that every originally admitted target is still owned after explicit partial release.

`CustodyState = [localCustodyID, scopeID, stateVersion, lifecycleCode, evidenceSelectionID, targetOwnershipStateID, payloadPinHandle, metadataAllocationHandle, checkingMaterialHandles, budgetWindowID, maintenanceCursorID, faultSummaryID, lastTransitionReason]`.

Let `OwnedRoots(S)` be the union of the current evidence selections for target rows whose ownership code is `OWNED` or `RELEASING`. The pin handle protects exactly this scope's required root union and its physical generations under the local DAG-ownership/GC contract; missing/corrupt bytes are reported as faults, not concealed by the existence of the handle. A `RELEASED` target contributes no owning reference from this scope, even when its historical selected root IDs remain in bounded metadata. Other scopes, acquisition staging, or active-use/export handles may independently protect the same roots. Shared bytes can be stored once, but each scope's owning reference and metadata are accounted. Checking-material handles identify actually retained/admitted local material, not merely a URL or a claim that a compatible binary exists somewhere. Such material is not executed merely because a mathematical peer named it.

### Bounded operational records

`CustodyBudgetWindow = [windowID, localFundingAuthority, fundingGeneration, openingObservation, renewalCondition, ceilingVector, settledVector, outstandingVector, terminalRecordReserve]`.

`MaintenanceCursor = [localCustodyID, scopeID, scopeStateVersion, routineKind, inventoryCutID, nextPosition, partialIntegrityStateOption, coverageObservation, lastCompletedLocalTime]`.

`TargetFault = [localCustodyID, scopeID, targetID, code, exactAffectedIDsOrConservativeScope, localObservationBoundary, repairCursorOption]`.

`HandoffAttempt = [attemptID, localCustodyID, scopeID, targetID, exactOfferedReplayIDs, destinationNodeID, localDeadline, disclosureAuthorizationID, localAllocationHandles, stage, remoteObservationRefs, sourceReleaseDecisionOption]`.

No handoff record contains a foreign grant that can spend locally. `partialIntegrityStateOption` is bounded receiver-owned hash/scan state tied to an exact physical generation; if continuity/integrity cannot be established after interruption, resume from a safe earlier boundary or discard that partial state. Never count an incomplete object hash as a completed integrity check.

Detailed terminal handoff/job histories can be compacted under the local history allowance, while the authoritative resource ledger preserves its required replay/fencing information. Compaction does not release current custody pins, erase spent allocations, or permit a completed action to run again.

## Finite example policy

The following values make the contract runnable on paper. They are local defaults, not universal mathematics limits or measurements of hardware adequacy. They replace allocated shares within the node's existing budgets; they are not added on top of exhausted capacity.

| Dimension | Illustrative local custody allowance |
|---|---:|
| Active custody scopes | 8 |
| Targets per scope / aggregate targets | 4096 / 16384 |
| Selected replay alternatives per judgment target | At most 4 |
| Unique custody native payload union | 32 GiB |
| Local custody/index/assessment metadata | 256 MiB, also subject to node-wide mandatory control limits |
| Retained checking materials | 4 GiB, separately charged |
| Custody staging/workspace | 2 GiB |
| Maintenance CPU per authorized 24-hour funding interval | 3600 CPU-seconds |
| Integrity/repair storage I/O per interval | 8 GiB |
| Repair/observation application traffic per interval | 2 GiB, both directions combined |
| Paid remote observation/transfer calls per interval | At most 4096 |
| Queued custody jobs / running custody maintenance jobs | 16 / 2 aggregate |
| Stored provider observations per target | At most 4 |
| Terminal local handoff history | At most 256 records and 4 MiB |

The node's full aggregate capacity must actually include these allocations. If its general profile supplies only 32 GiB total storage, it cannot simultaneously allocate all 32 GiB to custody and pretend that checking materials/staging are free. Count and byte caps apply together. A target whose metadata or native closure cannot fit is declined before a custody commitment is activated.

Funding renewal is a fresh bounded local policy decision under the standing authorization. A new admission epoch, reboot, clock rollback, or failed remote request does not create a new daily allowance. If time-origin continuity needed to distinguish funding intervals is uncertain, preserve settled/outstanding charges conservatively and pause automatic renewal until its local policy can establish a new authorized interval. An explicit owner-authorized additional allocation can resolve that impasse; replaying an old renewal cannot.

This funding rule concerns future work. Its exhaustion marks maintenance underfunded/degraded and stops unadmitted work. It does not erase a still-live durable storage allocation. Releasing that allocation is an explicit transition below, not a side effect of a timer or another participant's demand.

## Admission and activation

The local lifecycle is

`PROPOSED -> ACQUIRING -> ACTIVE`,

with bounded `DECLINED`, `INCOMPLETE`, or `CANCELLED` outcomes before activation. ACTIVE can acquire degraded flags; those flags do not delete the artifact or rewrite its historical check.

1. An authenticated owner request names the exact scope and selected policy. The node checks all scope/count/schema bounds and reserves a finite acquisition/check/staging/metadata envelope before work.
2. Existing locally checked exact evidence and protected bytes may be reused under their current qualified guards. Missing evidence uses ordinary public-root reads or an owner-authorized archive/export path. Every provider independently funds serving.
3. EXACT_REPLAY reconstructs the exact required native closure. JUDGMENT_RECOVERY independently validates each selected proof/replay against its exact target and policy. Unsupported or over-budget targets remain incomplete, not mathematically refuted.
4. The node establishes required checking-material availability/admission without executing supplied peer code. A missing compatible qualified checker prevents a currently replayable claim even when all proof bytes are present.
5. Durable byte staging precedes the atomic activation transaction. That transaction binds the scope/evidence selection, complete target ownership map with all rows OWNED, exact union pin, metadata/checking-material allocations, current native/availability guards, resource settlement, and bounded maintenance cursor.
6. A failed/crashed uncommitted attempt creates no active custody. Its surviving candidate bytes remain inert or protected only by their separately existing allocations.

There is no all-or-nothing obligation to accept an arbitrary proposed collection. The initial activation succeeds for its exact complete scope or ends incomplete/declined. An owner can propose a smaller new scope; it cannot describe a silently truncated subset as the original activated scope.

## Selected autonomous maintenance

These routines inspect or preserve existing material. They are operational jobs, not mathematical investigations. One bounded scheduled occurrence obtains its own local grant/reservation/claim. A fault can create a nonauthorizing repair intent, not a recursively funded repair tree.

| Routine | One admitted occurrence | Progress and failure semantics |
|---|---|---|
| Byte-integrity scrub | Every 15 minutes, at most 64 MiB of hash-checked reading, at most 1 CPU-second and 30 wall-seconds | Persist an exact inventory/physical-generation cursor; only completed checks advance verified coverage |
| Native/availability guard review | Every 10 minutes, inspect at most 64 target records from a persistent fair cursor, with a finite CPU/wall allowance | Record current scoped nonreliance/unknowns; broad incident admission itself blocks stale reuse immediately, without waiting for this routine |
| Replica observation | Every 10 minutes, select at most 8 target entries and at most 2 already selected providers per entry | Each remote call is separately paid; age/stale responses remain limited observations |
| Repair | Admit at most 2 concurrent jobs from the aggregate 16-job queue, each with an explicit finite import/check envelope | Repair exact missing bytes or separately admit a permitted witness replacement; no free deadline extension |
| Handoff observation | Advance an already admitted finite attempt only while its deadline/allocation remain live | Missing successor, stale acknowledgment, or timeout is an observed failure/noncompletion |

At 64 MiB every 15 minutes, nominal scrub input is 6 GiB per uninterrupted day. A static 32-GiB payload needs at least 512 complete occurrences, about 5.33 days, ignoring metadata, interruptions, duplicate work, and additional costs. Therefore the routine reports achieved coverage, not a guaranteed five-day freshness theorem. The shared 8-GiB I/O budget must also cover repairs and other custody I/O; failures or competing work can lengthen the pass.

The 8-target/2-provider observation routine offers at most 2304 paid calls per uninterrupted day before failures/other work, within the illustrative 4096-call limit. It does not refresh every one of 16384 targets every ten minutes. Fair cursors distribute admitted opportunities; overload, missing service, or unavailable budgets can still leave old observations. The status interface must disclose that age and coverage.

Maintenance eligibility and current preservation coverage range over OWNED targets; RELEASING targets retain their existing protection until the release transaction finishes but do not admit new ordinary repairs or replacements. RELEASED targets are skipped. A maintenance occurrence rechecks its exact ownership/state version before committing changes; a stale job cannot restore a released owning reference or report its former target as currently preserved. Its already admitted work and temporary protections settle under their original finite grants.

Integrity reads can proceed over complete native objects or qualified stored byte chunks. A large object's incremental hash state is tied to a fixed protected generation and remains a partial check until the complete hash verifies. Generation replacement or uncertain recovery invalidates that partial coverage. Physical deduplication can share a completed check across scopes only when it names the same exact bytes/generation and applicable integrity policy.

A byte hash check is not a rerun of native proof checking. A checker/profile incident can require native revalidation; silent conversion into a successful byte scrub is forbidden.

## Faults and meaningful status separation

Custody maintains independent facets rather than a single reassuring boolean:

- `bytes`: complete/protected, detected incomplete/corrupt, or unknown;
- `native`: currently permitted qualified evidence, historical assessment with blocked basis, unsupported, or unknown;
- `checkingMaterials`: exact locally available/admitted, missing, or unusable under policy;
- `maintenance`: adequately funded for the current declared schedule, degraded, or paused;
- `replicas`: exact bounded observations with their scope/age, not a verified count of independent durable domains;
- `lifecycle`: proposed, acquiring, active, releasing, released, or cancelled.

Examples:

- A known kernel defect can make `native = blocked` while `bytes = complete/protected`. Retain the historical evidence under its authorized pin; do not claim it is current trusted mathematics or automatically delete it.
- A lost chunk can make `bytes = incomplete` while a historical native derivation assessment remains recorded. The current-use gate fails closed until a complete permitted path is reestablished.
- An uninhabited-context opposing theorem is not automatically a checker incident. Closed contradiction/basis investigation follows the native scope rules; custody cannot invent a stronger verdict.
- A missed maintenance period does not prove byte loss, but it weakens the recorded observation/maintenance coverage. Report degraded/unknown rather than either asserting safety or fabricating corruption.

Fault admission and current relevant guards use the native/storage incident mechanism. A local protection handle cannot conceal detected physical loss; a conservative breaker blocks affected use when exact affected roots cannot yet be enumerated. Remote allegations and remote receipt counts cannot directly disable the local checker or consume its protected repair class.

## Restart and expiry

Ordinary restart preserves committed durable custody scopes, pins, allocations, exact evidence selections, and spent resource history under the store's recovery assumptions. Running jobs receive conservative terminal recovery; their old claims are not restarted for free. Current status is unavailable/unknown until native policy, byte protection, recovery fencing, and current incident state are coherent.

Warm caches outside the custody allocation follow their own retention-clock rules. Clean invocation-generation sealing must not discard or refresh durable custody pins or their funding history. Actual writer/clock changes may invalidate maintenance/status cursors whose continuity cannot be established; they do not erase the underlying scope or turn it into unowned garbage.

Job, export, observation, and local-status snapshot deadlines are enforced independently. Expired remote observations lose their current routing/replica evidential role. An expired export prevents further reads under that lease. Neither event proves that the remote provider lost the bytes, nor grants a fresh lease, nor releases the custodian's local durable root.

A whole-disk rollback with uncertain authority history uses the existing new-authority/re-admission recovery boundary. A stale backup cannot resurrect old grants or claim current custody allocation by replaying a past status record.

## Replacement and release transitions

### Same-judgment evidence replacement

For JUDGMENT_RECOVERY, an owner-authorized automatic selection policy may propose a new proof of the same exact target. It must first reserve temporary double-storage and checking costs, independently admit the new exact replay, and pin it. One local transaction can then update the evidence-selection version and remove this target's old owning reference **only when** the exact target is still OWNED at the checked custody/ownership versions. That transaction preserves every independently required owning reference or active use/export pin, including another target within the same scope; it cannot reclaim old bytes while any such protection remains. A concurrent release prevents that replacement commit; its separately admitted acquisition costs and temporary protections still settle normally. If temporary space is unavailable, defer; do not delete the old evidence first.

EXACT_REPLAY cannot use this transition to discharge its original bytes. A lossless physical storage transform is permitted only when the exact old canonical payloads remain reconstructible under its separately qualified local storage contract and all resource/durability obligations remain fulfilled.

### Explicit owner release

`RELEASE_REQUEST(localCustodyID, scopeID, expectedStateVersion, selectedTargets)` is an authenticated local command. It checks the actual current policy, exact sorted duplicate-free target subset, target ownership versions, other live obligations, and active protections. Every selected target must belong to the immutable scope; already RELEASED rows produce an explicit already-released result without reacquisition or fresh work. A changed state version requires a fresh decision or bounded explicit reconciliation, not silent release of newly acquired ownership in another custody instance.

The transition atomically marks the chosen OWNED target rows RELEASING and advances custody/ownership versions. Its finishing transaction removes only those owning references that the local authority may release, marks the same exact rows RELEASED, and publishes resulting custody/current-use state changes. Crash recovery must see either the still-protected RELEASING state or the committed RELEASED state, never released bytes hidden behind an OWNED status. Remaining OWNED targets keep their evidence and ownership; `OwnedRoots(S)` is recomputed or incrementally maintained with exact shared-root reference accounting. Other scopes and active use/export pins continue to protect shared bytes. The scope lifecycle stays ACTIVE while any target remains OWNED, is RELEASING when only releasing/released rows remain, and becomes RELEASED when every target row is RELEASED. These aggregate codes do not substitute for per-target ownership status. Physical reclamation uses the normal metered generation-aware GC sequence; RELEASED is not a claim that every shared byte has already been physically deleted.

There is no automatic release merely because a remote acknowledgment arrived, a usage score fell, a funding window expired, or a different proof looks shorter. The owner may make an explicit discretionary release despite failed handoff when its actual policy permits it; the outcome must record that no durable remote guarantee was obtained.

## Handoff without a new wire operation

Handoff is a pair of independently authorized local processes, not a transferable ownership token.

1. The source owner admits a finite HandoffAttempt for exact selected replay roots and authorizes their disclosure. The source may announce ordinary bounded HINTs to its chosen destination or provide an already permitted exact export scope.
2. The destination's own policy decides whether to acquire those candidates. It uses ordinary paid reads/BUNDLE1 or an exact EXPORT_HEAD2 snapshot and independently checks the complete required closure. A source hint cannot force it to allocate custody.
3. Only the destination's own successful local custody activation establishes `ACTIVE` there. Its local event is supported by its actual allocations, full evidence, and current qualified guards.
4. The source can obtain existing signed RetentionAck/provider observations and perform separately funded scoped fetch checks. These establish at most their stated observation: a key's pin assertion or actual served bytes during the check. They do not prove future retention, independent failure domain, destination policy compliance, or indefinite service.
5. The source records `OBSERVATIONS_OBTAINED`, `PARTIAL`, `EXPIRED`, or `FAILED` for its attempt. It does **not** report network-wide `CUSTODY_TRANSFER_COMPLETE` solely from a remote signature, a shared URL, or a successful socket write.
6. Source release remains the explicit local transition above. An operator may rely on disclosed observations as a discretionary risk decision, but the protocol does not elevate them to a durable guarantee. Retaining both scopes is allowed when resources permit.

No new remote command asks another node to pin, renew, release, certify custody, or obey the source's policy. Existing export leases and disclosures remain finite/audience-bound; an incomplete handoff cannot extend them by replay. Exact-mode handoff transfers the same ReplayID closure. Judgment-mode transfer offers actual selected witnesses of the same exact target; any replacement is independently checked under the receiving policy.

## Bounded local status interface

Only an authenticated local client with custody-read authority can invoke the local query. It uses the same local resource admission framework as other protected reads.

`LOCAL_CUSTODY_STATUS = [localCustodyID, expectedScopeIDOption, targetFilterOrCursor, requestedLimit]`.

`CustodyStatusPage = [localCustodyID, scopeID, stateVersion, observationBoundary, mode, lifecycle, capacityObservation, maintenanceCoverage, targetFacetRows, nextCursorOption, truncationCode]`.

A target row contains `[targetID, ownershipCode, ownershipVersion, selectedReplayIDs, bytesCode, nativeCode, checkingMaterialsCode, pinObservation, faultScopeOption, maintenanceObservation, boundedRemoteObservations]`. RELEASED rows explicitly report no custody protection from this scope; any displayed old byte/native/replica observations are labeled historical with their boundaries, even if other local scopes happen to retain the same objects. OWNED and RELEASING rows remain distinct. All positive current native/use fields are observations coherent with their local commit boundary, not claims about delivery time or the entire network. If current clearance is unaffordable, the row says UNKNOWN; a historical successful assessment is not relabeled current.

The initial local interface returns at most 64 target rows and 256 KiB per page, with at most 0.25 CPU-seconds/two wall-seconds of work. It permits at most eight pinned local status snapshots, 4 MiB total extra snapshot state, and a 60-second snapshot lifetime. Count/byte ceilings apply together. A cursor binds authenticated local holder, exact local custody instance and scope/state cut, predicate, next unprocessed target, and original expiry; it cannot silently resume against a newer scope or a reacquired local custody instance that happens to have the same immutable scopeID.

Aggregate counts distinguish immutable originally admitted targets, currently OWNED targets, RELEASING targets, and RELEASED targets; pin counts come from the exact local authority state. Native/replica health aggregates that have not been recomputed at this boundary are explicitly labeled by their older observation cut, not asserted to be current for every root. Partial pages or budget exhaustion do not imply that the omitted targets are healthy, absent, or unpreserved.

These records remain local. The optional advisory-bundle whitelist is not enlarged to include them, and knowledge of their local IDs is not remote read permission. An operator can intentionally communicate a human-readable report outside the protocol, but it remains a scoped report rather than a new native or storage authority.

## Required paper/conformance cases

- An old proof's kernel basis becomes locally disabled: bytes stay pinned, native status blocks, no automatic cross-foundation replacement or false mathematical reuse.
- A judgment-mode replacement is checked but double-storage allocation fails: keep the old ownership reference and defer replacement.
- An exact-byte scope and a judgment scope share one proof: judgment replacement cannot release the exact scope's bytes.
- A durable scope survives restart while an old maintenance job is terminalized: no duplicate work claim or budget refill.
- A remote provider signs an acknowledgment and immediately becomes unavailable: source records a stale/failed observation, not completed durable transfer.
- A custody funding interval expires with no renewal: maintenance becomes paused/degraded, while still-authorized durable pins are not silently garbage-collected.
- The owner releases a target during an admitted export: the finite export protection survives until its actual expiry/termination; subsequent GC respects shared roots.
- The owner releases one of two targets sharing a closure: that target becomes visibly RELEASED, the immutable scope remains unchanged, the other target's complete owning reference remains, and a stale replacement/maintenance job cannot re-own the released target.
- A partial byte scrub crashes before final hash verification: no complete-integrity observation is synthesized from its prefix.
- Thousands of faults arrive: keep bounded scope/cursors and the 16-job queue, not one unfunded repair job per allegation.
- A local status page expires while the scope changes: return stale/nondecision, not mixed-scope completeness.

## What this contract establishes

It selects an implementable-on-paper owner-local mechanism for persistent scope ownership, bounded autonomous maintenance, meaningful status, and ordinary exact transfer to willing successors. It does not require a central custodian or confer theorem authority on storage operators.

Actual long-term accumulation still requires supplied capacity, compatible qualified checking materials, successful maintenance/recovery, and some custodians choosing to continue. No local record or blockchain-like history can regenerate evidence that is no longer reconstructible. This contract makes those obligations visible without converting them into a fictional remote permanence guarantee.
