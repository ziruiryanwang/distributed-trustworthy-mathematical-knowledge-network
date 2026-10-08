# EGRESS1 resource and lifecycle audit

Date: 2026-09-20. Independent reviewer: `qualification_contract_review`. Scope: bounded local selection, activation, serving-resource attribution, interval/physical fits, drain and release. No implementation, extraction, native execution, executable model, test or benchmark. This audit edits no proposal, earlier audit or frozen checkpoint.

Final disposition: **EGR-RES-001 and EGR-RES-002 are closed at the repaired cut identified below.** Initial-cut findings and handoff history are retained as historical observations, not current unresolved findings. This is a conditional source-contract review, not execution qualification or selection of EGRESS1.

## Initial held cut and disposition

The complete [proposal](../proposal.md) was read and independently hash-confirmed at SHA-256 `5C98D1E2A78D74CCEE83AE868560770A6B330249D015CCCA7DF9FACA871B7E8A`.

**One concrete resource/deadline handoff requires repair before this review can close:** provider-wide discovery has no specified pre-offer payer and lifecycle binding. Other inspected seams below are coherent conditionally at this cut, not qualified by execution. The separate authority/disclosure reviewer owns the detailed disclosure audit; this record does not claim to replace it.

Inherited passages inspected: [NET1 public-root scopes, publication/index activation, snapshots, service accounting and GC](../../../../spec/OPERATIONAL-CORPUS-V1-NETWORK.md); [NET2 retained executions/data leases, result spools and EXPORT_HEAD2](../../../../notes/analyses/CP-001E-exchange-scaling.md); [E exact custody and versioned release](../../../../notes/analyses/CP-001E-custody-contract.md); [H postselection public/index/anchor obligations](../../../../notes/analyses/CP-001H-resource-supply-and-discovery.md); and [I direct mutation/snapshot costs](../../../../notes/analyses/CP-001I-direct-broker-bindings.md). The author selected no broker, hint or DHT path, so this review does not demand those unselected mechanisms.

## EGR-RES-001: provider-wide discovery lacks a pre-offer payer/deadline binding

Classification: **missing local handoff mechanism** in the proposed finite-service contract, not a demonstrated native-soundness defect or a requirement for a new wire operation.

The source correctly says its named collection is only a local nomination/ownership lane. Remote FIND remains the existing provider-wide authorized public projection and has no egress-lifecycle selector. Later it states that a source-side service subaccount funds operations “for these public roots,” gives a separate per-exposure service ceiling, and requires before every offer that all resulting authority end no later than “this exposure's horizon plus 600 seconds.” It does not identify the relevant exposure for a provider-wide discovery call before the scan reveals returned roots.

### Minimal mixed-scope trace

1. Two EGRESS1 lifecycles A and B are publicly active at one provider. Relative to the present cut, A's admission horizon ends in 10 seconds and B's in 100 seconds; their distinct activation times can each satisfy the selected 24-hour duration. The same provider also has independently authorized public roots outside this policy.
2. An incoming token/pattern query can match A, B and an independent root. The request names its normal predicate/snapshot, not A's or B's local egress ID. A provider-wide snapshot can retain shared index versions and control state regardless of which matches fit the first output page.
3. Before offering the operation, the source must reserve finite scan/reply/snapshot resources and enforce the claimed tail deadline. Choosing the account or deadline from a root that appears later in the result is too late for that admission decision. A page with no match still consumes work.
4. A's horizon ends while the snapshot or reply is outstanding. Charging everything to B, to both A and B, to an unspecified shared class or to ordinary non-egress discovery gives different budget/ownership semantics. The proposal does not select one. Nor does it state which retained obligations remain attached to A's drain versus the independent grant or B's later endpoint.

Per-root native reads can name an exact replay and are not the same ambiguity. This finding also does not require all historical index snapshots to retain every corresponding proof closure: only their actual inherited index/control/protection obligations must be attributed and kept charged. Historical candidates may remain historical; they do not create fresh source authority.

### Required repair and permitted latitude

Define an owner-local binding **before offer/admission** for provider-wide FIND and its descendants: paying account(s), fixed counted shares or a single payer, admitted scope/cut, applicable endpoint, snapshot/result ownership and relevant drain records. Apply it to empty pages and unsuccessful work as well as successful matches. An ordinary continuation must retain its actual old snapshot binding under a fresh paid call; it cannot switch payer/scope for free when a new result appears.

One possible solution is a separately funded bounded shared discovery class with explicit treatment of mixed egress and independent public state. Another is a conservative exact multi-exposure binding made before admission with no uncounted obligations. The author may instead choose a narrower feasible local restriction. Existing wire predicates need not change. Whatever choice is selected must:

- preserve every independent grant and its actual resource/protection obligations;
- reconcile the per-exposure and parent ceilings without charging one physical allocation twice as new supply or charging it to neither;
- choose the applicable deadline before work rather than from result contents;
- keep shared snapshots, spools, replies, terminal outcomes and uncertain records charged through their real retirement;
- state the effect of one exposure's closure on this binding without claiming that another owner's grant is revoked or that old metadata grants fresh proof service.

The missing binding must not be hidden by assuming every query has one matching egress root. The proposal explicitly selects a provider-wide discovery interface. Root is coordinating this finding with the independent authority review; the source remains held for one author repair.

## Other inspected initial-cut seams

| Seam | Conditional source-level result |
|---|---|
| Nomination authority | A finite row binds the exact settled output/judgment/instance/replay and existing complete protection. Missing prerequisites are not supplied for free. One candidate or unsettled lifecycle per exact judgment prevents concurrent automatic witness replacement. Replay preserves the old request result; a new request needs new admission. |
| Planning and claim | A round completes its prescribed bounded scan before atomically claiming one revalidated nomination. PLAN_INCOMPLETE chooses nothing; stale choice ends the round without fallback. Unchosen rows retain only their original nomination authority/deadlines, not a new grant. After claim, failure stays terminal or fenced. |
| Native custody before publicity | The selected exact singleton E scope is separately activated. Cache ownership, export success or merely present bytes do not establish that custody. Prepared indexing is private until the guarded local public transaction commits; a failed activation can leave funded CUSTODY_ONLY, not a fictional public result. |
| Actual public cut | PUBLIC_ACTIVE is a source-local committed public/index state, not consumer delivery or benefit. The known-contact path avoids hidden broker/DHT actions. A target already selected into F/H routing requires a different admitted publication policy; EGRESS1 cannot silently omit those costs or revoke that existing work. |
| Finite interval versus retention | The 24-hour endpoint limits this grant's new service admissions; it is not a custody timer. Closure, clock loss or authority loss invokes a conservative gate plus guarded transitions. E's owner-release-required pin survives until the delegated controller actually performs the permitted versioned release. |
| Tail is a limit, not instant cleanup | The extra 600 seconds constrain actual admitted authority, with lower inherited limits prevailing. They are not a theorem that every execution, reply, snapshot, export, terminal record and physical generation disappears by then. After authority ends, required unsettled/recovery/control state remains counted. The provider-wide binding finding above prevents applying this condition unambiguously to all discovery calls yet. |
| Real recovery | Clean admission-epoch sealing preserves local deadlines and spending; actual clock/writer uncertainty cannot extend exposure or remint a daily budget. Fenced or unsuccessful release keeps the relevant obligations and slot charged. New authority is not inferred from an old timestamp or remote receipt. |
| Resource independence | Four slots include preparation, public, draining, releasing and uncertain states. The custody union includes the foundation; metadata, workspace, service, storage I/O, cleanup and other-role occupancy remain independent limits. Existing and new protection references overlap during activation; sharing physical bytes does not erase those handles or control costs. |
| Physical release | Removing this exact custody reference preserves other owners, seed/cache/use/export pins, snapshots and H anchors. Release is not reclamation. The full 16-GiB example cannot admit another 512 MiB merely because it is already valid in separately funded staging; a full four-slot state can refuse even zero-marginal-payload work. |
| End-to-end paper path | The favorable example continues from checked B-associativity through an actual committed native posting, an unknown-answer-ID query by an independent known-contact investigator, complete acquisition and a checked four-factor application. Further contribution needs its own nomination/resources. This is a conditional path with supplied scope/order/resources, not an executed nonvacuity result or causal acceleration. |

The finite accounting table is a set of simultaneous ceilings and required supply, not a claim that all maxima fit or that jobs finish within them. In particular, standing authority, a calendar boundary, failed serving or a policy name cannot create new hardware, I/O or cleanup grants. Lack of funds may stop progress without making a theorem false.

## Initial handoff boundary (historical)

Initial review is complete, but **EGR-RES-001 remains open at the held initial cut**. Final closure requires a repaired exact source and a targeted reread of the chosen pre-offer discovery binding, mixed-scope trace and its drain/accounting consequences. A reply from the author alone is not closure.

No useful-yield, long-term preservation, actual runtime isolation/recovery, broad-network reachability or measured throughput claim has been established. This audit neither selects EGRESS1 nor authorizes implementation. Earlier completed audits remain unchanged.

## EGR-RES-002: initial cost ranking depended on unperformed extraction

Classification: **preclaim information and resource-accounting gap**. Raised by root after this review's initial handoff and independently confirmed by this reviewer against the held initial cut. This is not attributed to this review as an independently originated finding.

The initial cost rounds ranked candidates using exact incremental public-index bytes. Nomination supplied already checked evidence, closure inventories and protection, but did not require a previously computed exact STRUCT2 descriptor/posting inventory. The first admitted STRUCT2 extraction occurred only after the selected nomination was claimed. Thus, for an otherwise eligible candidate whose exact postings were not already known, the prescribed preclaim ordering required either future information or additional unadmitted extraction during planning. Treating that missing number as zero would not fix the ordering or the work account.

The repair need not predict utility or actual extracted size. It must order candidates on information available before claim, reserve a finite amount for later publication work and fail honestly if that later preparation does not fit. Actual extraction remains an admitted postclaim operation.

## Repaired held cut and full reread

The complete repaired proposal was reread and independently hash-confirmed at SHA-256 `982C5613F88935F5EDA7F39DE3BA3980C4B7A331A9937C00461B46D3AD9C468F`, 26,589 bytes. No proposal edit was made by this reviewer. Closure here applies to that exact cut; it does not erase either initial countercase.

### EGR-RES-001 repair: fixed sponsor, whole-cut dependencies and minimum horizon

The source now specifies an owner-local decision **before offering fresh FIND work**. Among at most four PUBLIC_ACTIVE lifecycle records, it chooses the lowest-enrollment-serial account able to reserve the entire operation/reply/snapshot/control/settlement cost. Owner authority expressly allows that sponsor to fund the whole provider-public snapshot, including independently public entries and empty results. Consequently, neither the payer nor its authorization depends on learning which root a scan eventually returns. Root-specific reads/exports separately bind the actual root's grant; sponsorship is not read authorization.

The pre-offer binding also fixes the actual public-cut/disclosure-version summary, every currently PUBLIC_ACTIVE EGRESS dependency, and independent guards. Existing paid index/control state must provide the bounded summary; otherwise NEEDS_AUTHORITY_SUMMARY refuses the operation. This prevents the new binding rule from concealing an unbounded or unpaid corpus scan.

Write the bound dependency set as D and its public-admission horizons as h(d). The rule selects H = min {h(d) : d in D}. D is nonempty because it includes the active sponsor. New calls/execution claims require current guards and time below H; all operation, lease and delivery endpoints are bounded by H + 600 and tighter inherited or independent limits. Payer selection and deadline selection are separate decisions:

| Held-cut case | Payer selected before work | Binding and consequence |
|---|---|---|
| A ends at 10, B at 100; A can reserve the whole mixed public operation | A | D contains A and B even if either does not match. H = 10; independent entries and empty results do not change it. |
| Same horizons; A cannot fund the operation but B can | B | D still contains A and B, so H remains 10 even if the returned page contains only B or independent roots. B's later horizon cannot extend the old mixed binding. |

Fresh paid continuations retain the exact snapshot, payer and dependencies. They cannot migrate to B, silently filter A out of the old snapshot, or select a later endpoint after observing results. After A closes and leaves the current cut, B may separately sponsor a fresh query under a new binding. Independently funded grants survive on their own terms; closing this mixed binding is not revocation of all provider service.

Actual shared snapshot/spool bytes are charged once to the fixed sponsor, while every dependent lifecycle retains its reference/control obligations through settlement. A dependency that contributes the earliest horizon cannot disappear from accounting merely because a different account pays the shared physical allocation. Required unsettled/recovery state remains charged beyond any authority endpoint. Together these clauses answer the initial payer, mixed-scope, continuation and drain questions without requiring a new wire field.

Disposition: **closed at the repaired held cut**. This is conservative and may terminate useful B-related discovery early; no optimal availability or throughput claim is required for closure.

### EGR-RES-002 repair: available exact axes and a fixed reservation

Rounds 2 and 4 now rank first by exact marginal protected-payload union and then by exact already-known added custody metadata plus a **fixed 8-MiB publication/control reservation**, followed by enrollment serial and JudgmentID. Existing receiver-owned inventories supply the exact quantities. Missing inventories produce UNKNOWN_FIT, not free work or a guessed zero.

The 8 MiB is a reservation and stop limit, not a prediction of index size. It does not depend on inspecting an as-yet-unextracted candidate. The actual STRUCT2 extraction still runs once, after claim, using the admitted preparation allocation. Exceeding the reserved publication bound causes terminal preparation failure; it cannot silently increase a grant, publish a truncated mandatory cut or retry the same consumed nomination. Whole-node and aggregate metadata/transition fit remain independent requirements, so the constant does not waive other occupied records.

Disposition: **closed at the repaired held cut**. This repairs the causal ordering of information and paid work. It does not prove that the reservation is empirically well chosen or that cost ranking predicts mathematical value.

### Repaired lifecycle and supply observations

Ordinary horizon closure now explicitly cancels unclaimed operation **and delivery** tickets, including already committed responses not yet claimed for sending. Only already claimed work/delivery can continue under surviving authority. An operation running at the cutoff cannot later acquire a new delivery claim merely because it produces a response within the drain allowance. The H + 600 or root-horizon + 600 ceiling is not a new grant and does not promise all records can be retired by then.

Actual disclosure withdrawal is separately guarded and can terminate authority earlier; this audit relies on the separate authority/disclosure review for its detailed security assessment. For resource/lifecycle purposes, already sent bytes, cancellation attempts and remaining uncertain records stay counted. Neither ordinary expiry nor revocation automatically deletes E custody. Delegated release is an explicit versioned action, removes only this policy's reference and preserves other pins/owners. Failed or uncertain release occupies its lifecycle slot and retains its actual obligations.

The repaired source also explicitly charges recurring custody integrity/guard work, declines to infer remote observation/repair-import/handoff authority, requires whole-node supply for checker materials/resident native state/preexisting index state, and serializes expensive stages in the first schedule. These are necessary accounting boundaries, not guarantees that arbitrary real artifacts fit the illustrative maxima.

## Worked paper instance: joint arithmetic and chronology

The repaired fixture stipulates actual demands and supplied capacity; it does not estimate them from serialized theorem size or report a run. Both endpoints already own a qualified/protected 2-GiB shared core, including F and B/op_B. The 8-MiB associativity replay is new evidence. Historical acquisition and checking are explicitly charged outside this new lifecycle. The matching posting list has eight descriptors, the useful one is third, one at-most-64-row page completes the list and the receiver funds three type probes. The answer theorem ID is not supplied.

Using 1 GiB = 1,024 MiB, the stated simultaneous quantities give:

| Resource check | Arithmetic and applicable bound |
|---|---|
| Source disk | 4 GiB checking materials + 2 GiB core + 8 MiB evidence + 1 GiB temporary + 64 MiB metadata = **7 GiB + 72 MiB**, below supplied 12 GiB. The protected payload is 2 GiB + 8 MiB, below the separate 16-GiB custody ceiling. Shared bytes do not eliminate distinct protection records. |
| Source RAM | 3 GiB native + 32 MiB preparation + 8 MiB publication/control + 16 MiB snapshot/spool = **3 GiB + 56 MiB**, below supplied 8 GiB. The stated preparation increment is below its 256-MiB ceiling. Native resident size is independently stipulated, not inferred from disk bytes. |
| Source CPU and bounded planning | 0.5 + 4 + 20 + 20 = **44.5 CPU-seconds**, below the parent 3,600. Selector demand 0.5 is below 2 CPU-seconds and its 4,096 inspections below 65,536. Preparation demand 4 CPU-seconds/20 elapsed seconds is below 60/600. Service demand 20 CPU-seconds is below 600. The remaining upheld settlement/maintenance demand is not free. |
| Source service and I/O | 48 total attempts and 16 MiB traffic are below one exposure's 512-attempt/4-GiB ceilings and the larger parent ceilings. 6 GiB scrub + 64 MiB preparation + 16 MiB serving + 16 MiB settlement = **6 GiB + 96 MiB I/O**, below 32 GiB. Snapshot/reply/drain reservations are expressly included. |
| Receiver disk and RAM | Disk demand is 4 GiB checker materials + 2 GiB core + 8 MiB evidence + 80 MiB temporary/metadata = **6 GiB + 88 MiB**, below supplied 8 GiB. RAM demand is 3 GiB native + 192 MiB other peak state, also below 8 GiB. |
| Receiver work and transfer | 100 CPU-seconds for the supplied probes, acquisition, checking and final applications is below 240; 16 MiB transfer is below 64 MiB. Warm-core reuse avoids core retransmission but does not exempt new evidence from checking. |

The fixture uses one new lifecycle and one preparation, not four simultaneous maxima. Candidate/control records, retained state and preexisting index occupancy must be covered by the stated metadata/whole-node supply under the source's joint-fit premise. The arithmetic is not permission to omit them or to fill all independent ceilings simultaneously. No unadmitted repair or additional receiver acquisition is smuggled into the warm-core case.

Nomination at t = 0, activation at t = 60, receiver start at t = 120 and checked reuse by t = 500 are ordered within the supplied 24-hour public window. Activation plus 86,400 seconds gives h = **86,460**, as stated. The favorable trace settles service/snapshot obligations before h and reserves release through h + 60 = **86,520**, below the h + 600 outer tail limit. The late release remains funded by the original outstanding reservation across the interval boundary; a new day creates no allowance. Its chronology assumes the stipulated execution progress and maintained guards, not that CPU quotas alone imply wall-clock deadlines.

This is an arithmetically consistent **conditional source/receiver paper path**. It is not a measurement, a proof that real Lean artifacts occupy these sizes, a complete executable call trace, evidence of causal speedup, a cold-bootstrap result, or a demonstration of sustained decentralized growth. The source expressly preserves these limits.

## Final review boundary

Both concrete findings are closed at the exact repaired proposal hash above. No remaining resource/lifecycle countercase was identified in the inspected selected path. The initial source remains historically defective in the stated ways; later prose cannot retroactively qualify it.

This review neither selects EGRESS1 nor reviews its checkpoint integration. The separate authority/disclosure reviewer and fresh composition reviewer retain their assigned scopes. All prior completed audits and checkpoints remain unchanged. No implementation, native run or benchmark is authorized or claimed by this disposition.
