# EGRESS1: bounded producer-local public-exposure selection

Date: 2026-09-20. Author: `folded_reflection_audit`, acting as author, not independent reviewer. Status: proposal, not selected or qualified. No implementation, executable model, Lean execution, extraction, native replay or measurement.

## Exact seam and selected narrow path

Choose one optional policy connecting already checked local derived outputs to an owner-authorized public collection cut. [K](../../../notes/checkpoints/CP-001K-local-cache-feedback.md) selects discretionary local caches, not publication. [F](../../../notes/analyses/CP-001F-exact-routing-coverage.md) already covers every judgment in an explicitly chosen finite public cut and bounds its pending-next-scope queue. [H](../../../notes/analyses/CP-001H-resource-supply-and-discovery.md) already maintains selected targets and shared feature coverage. Neither needs a replacement protocol here.

EGRESS1 precedes those choices. It selects **native known-contact exposure only**: existing local `PUBLIC_SERVE` authorization, ordinary exact/STRUCT2 public postings, existing paid `FIND_WINDOW`, and native reads/NET2 exports. It selects no outgoing HINT, broker submission, DHT advertisement, ROUTE operation or remote custody request. The owner's named local collection is a local nomination/ownership lane, not a request-side collection selector: remote FIND still sees only its existing provider-wide authorized public projection/snapshot. The relevant target cut must already be excluded from automatic F/H routing scopes; verify that configuration before admission, without disabling any admitted publication work. If a configured selected cut includes the target, this narrow policy declines with `NEEDS_ROUTED_PUBLICATION_POLICY`; it cannot bypass F's pending queue or H's costs. Separately admitted publication elsewhere keeps its own authority and costs.

Initial consumers must already have an owner-chosen contact for this native source. Success demonstrates this direct subpath, not worldwide discoverability or the whole project's large-network operability. Native semantics remain [V6](../../../spec/OPERATIONAL-CORPUS-V6.md)'s PI1 family; source advertisements never replace receiver checking.

## Protection is custody, not a timed cache

Each selected exact InstanceReplay receives its own singleton [E EXACT_REPLAY custody](../../../notes/analyses/CP-001E-custody-contract.md) scope, using current PI1 bindings. This is an **owner-release-required pin**. Its exact proof instance and complete replay closure are preserved; a cheaper same-judgment proof cannot replace them inside this scope.

A 24-hour horizon governs this policy's **new public-service admissions**, not expiry of that pin. At the horizon, its new-service/current-index eligibility closes. A delegated owner controller then explicitly issues E's versioned local `RELEASE_REQUEST` after lawful drain. Failed release or uncertainty leaves the pin counted and protected. Neither timer nor low use silently releases custody. No automatic renewal is selected; a later exposure needs fresh explicit funding after settlement.

The owner supplies standing authenticated authority for this bounded selection, singleton custody activation, full-closure disclosure, finite source service, public-index transitions and the specified explicit release decisions. Standing authority is not extra hardware or an unbounded recurring grant. Without it, return `AUTHORITY_MISSING`. No mandatory contribution, human-intention field, public mathematical task or global utility score is introduced.

## Inputs, nomination and exact identities

One immutable policy/account binding fixes F/E, current native/footprint policy, the named native-only collection, owner authority, disclosure policy, resource supplies and a qualified receiver-local interval clock. One fenced local writer owns state. A nomination is an authenticated local request containing:

- An exact locally settled producer-output completion reference, JudgmentID, ProofInstanceID and InstanceReplayID. The instance targets that judgment and the replay is rooted at that instance. "Derived" names a local producer output; it is not proof of global novelty, independent authorship or useful inference.
- Complete independently checked native evidence, actual compatible realization/footprint and receiver-owned closure/inventory references under current guards. Export success alone is insufficient.
- A currently valid existing protection handle for the complete locally present closure. Nomination itself does not extend that handle, import missing bytes or perform a new proof search/check.
- Explicit owner permission to consider the entire closure for public disclosure, plus exact resource/account references. Actual disclosure eligibility is rechecked before exposure.

Incomplete prerequisites return `NEEDS_NATIVE_OR_PROTECTION_WORK`. Those separately admitted preparations are not hidden selector work. Nonproof roots may be dependencies but are not independently nominated in this first policy.

At most 32 candidate rows exist. Each records a never-reused enrollment serial, exact request/output/evidence bindings, nomination state, existing protection and a deadline no later than one hour after admission or the known protection end, whichever comes first. Unknown protection continuity is not an infinite deadline. No nomination is accepted when the bounded row/control reservation cannot fit.

At most one candidate or unsettled exposure exists per exact JudgmentID. A second nomination while that row exists returns `ALREADY_ENROLLED`, without replacing its witness, age, deadline or authority. An already independently publicly served target returns `ALREADY_PUBLIC` rather than gaining redundant custody automatically. Identity here is exact judgment identity, not semantic-equivalence clustering. Distinct statements, specializations and logically redundant variants can still compete.

Nomination states are `QUEUED`, `CLAIMED(roundID)`, `TERMINAL(outcome)` and `FENCED_UNKNOWN`. Replay of one request returns its once-only result under the inherited durable invocation discipline. Claim consumes that nomination permanently; failure never rearms it. After terminal settlement and bounded history retirement, a **new explicit paid owner request** may nominate the same output again. No all-time novelty or no-republication promise is made. Record eviction, reboot, a new key or a new policy hash never recreates spent invocation authority. Queued candidates whose protection/deadline/guards fail are terminalized without changing their independently owned bytes.

## Concrete finite selection

Each authorized 24-hour interval permits at most 32 nomination attempts and four selector rounds. Only explicit owner calls or an explicitly admitted standing local caller invokes them; completion, use and expiry signals create no callback grant. Unused rounds do not accumulate. Clock discontinuity preserves spending/reservations and stops automatic admission pending reconciliation, not a fresh daily allowance.

One round proposes at most one root. Rounds 1 and 3 select the oldest feasible candidate; rounds 2 and 4 select the smallest exact marginal protected-payload union, then exact already-known added custody metadata plus a fixed 8-MiB publication/control reservation, then enrollment serial and JudgmentID. Existing receiver-owned closure inventories supply the exact axes; unavailable inventories yield `UNKNOWN_FIT`. The 8 MiB is a conservative reservation/stop limit, not a free prediction of post-extraction index size. Preparation exceeding it fails terminally. Both choices ignore popularity and have no fairness or future-value optimality claim.

Scan at most all 32 queued rows under one frozen versioned snapshot. A candidate is feasible only with current complete evidence/protection, full-closure disclosure, a free lifecycle slot and exact resource fit below. Unknown/incomplete inventories are candidate-local `UNKNOWN_FIT`, never zero cost. Planning work shares the round's finite inspection bound. If the prescribed scan cannot finish, return `PLAN_INCOMPLETE` and choose nothing. Complete planning atomically claims the chosen nomination after revalidating its versions. Stale choice ends the round without choosing a replacement. Other queued nominations remain eligible only until their original deadlines; consideration alone does not create an operation or spend their one-shot claim.

After claim, every later failure is terminal or fenced for that identity. At most one exposure preparation is in flight. Additional rounds cannot re-enter a claimed lifecycle. No ranking score establishes mathematical truth or usefulness.

## Preparation, public activation and serving

Use these receiver-local states, not new wire objects:

`CLAIMED -> CUSTODY_ACTIVE -> INDEX_PREPARED -> PUBLIC_ACTIVE -> DRAINING -> RELEASED`.

Failures can produce `CUSTODY_ONLY`, `NOT_PUBLIC`, `DEGRADED`, `RELEASING` or `FENCED_UNKNOWN`; none is silently upgraded to successful exposure.

1. Reserve actual complete-closure custody, metadata, preparation, public service, maintenance, drain, release and recovery allocations before any activation. Account both the existing staging/protection and new ownership records during transition. Check the entire exposed native closure against owner disclosure authority: a public-looking conclusion cannot authorize a private dependency.
2. Activate E's exact singleton scope through its existing admission/atomic protection transaction. Reuse current qualified bytes only under their actual compatibility/protection records. No new native imports or reconstruction are selected here; if required, stop and settle. Custody activation alone is not publication.
3. Perform one admitted deterministic STRUCT2 extraction and prepare mandatory exact tables, actual structural descriptors/postings and reverse dependencies in private staging. Completed extraction with declared profile truncation is honest; runtime interruption is `NOT_EXTRACTED`, not a timing-dependent partial descriptor. Require the whole prepared bounded publication unit to fit; no silently truncated cut is activated. No F/H route placement follows.
4. In the existing single-writer local public-index transaction, revalidate custody, native/current-use guards, complete-closure disclosure, collection exclusion, exact prepared index and remaining allocations. Atomically commit this policy's public authorization and complete posting cut. The committed activation tick starts the 24-hour public-admission horizon. Before that transaction the target is not this policy's public target. Failure after custody activation leaves `CUSTODY_ONLY` and triggers only the explicitly funded settlement/release path.
5. Serve through unchanged native interfaces. Code-4 structural lookup negotiates the actual capabilities 3+7+8 and uses existing `FIND_WINDOW` operation 10; ordinary exact lookup remains available. Public native reads require `readScope=[0,InstanceReplayID]` and exact closure membership. NET2 inventory/bulk/export operations retain their exact negotiated schemas and per-call guards. No private CAS endpoint or new remote egress command exists.

`PUBLIC_ACTIVE` means the source committed a locally discoverable public cut under this grant. It does not prove any peer queried, downloaded, checked or benefited. Status includes actual activation/end ticks and clock generation, current versus historical index state, service exhaustion/failures and exact custody state. It asserts no remote routing placement; an independently configured routed publication reports its own pending/observed state.

A source-side service subaccount funds existing admission classes. Each request still needs ordinary bounded offers/tickets, requester authority and receiver budget. No caller is entitled to the whole account. Resource exhaustion or guard changes can stop service early; record actual availability intervals. This is an opportunity, not an availability SLA.

### Provider-wide discovery: payer and authority before work

Before offering a fresh FIND, choose the lowest-enrollment-serial currently PUBLIC_ACTIVE exposure whose account can reserve the entire bounded operation, reply, snapshot/control and settlement costs; inspect at most four lifecycle records. Standing authority explicitly permits that sponsor to fund the **whole provider-public snapshot**, including independent public roots and empty results. No result-dependent payer selection occurs. Root-named reads/exports instead bind that root's actual eligible grant before offering work; FIND sponsorship grants no proof-read authority.

Bind the sponsor, exact existing public-cut/disclosure-version summary, all currently PUBLIC_ACTIVE EGRESS lifecycle dependencies (conservatively including nonmatches), and applicable independent snapshot/disclosure guards. The existing paid index/control state must supply this bounded binding; otherwise decline `NEEDS_AUTHORITY_SUMMARY`, not an unmetered pre-offer corpus scan. Let H be the minimum horizon of those EGRESS dependencies. All new calls/execution claims require time below H and current guards; every resulting lease, operation and delivery endpoint is at most H+600 seconds and any tighter inherited/independent limit. The payer remains fixed even when another dependency supplies H.

Continuations retain that exact snapshot/payer/dependency binding but require fresh paid calls. They cannot migrate an old cursor to another sponsor or silently filter/rebase its cut. At H, stop fresh continuations; a consumer may separately start a new query on a new current cut. Actual shared snapshot/spool bytes are charged once to the fixed sponsor; reference/control obligations for every dependent lifecycle remain counted through settlement. Another independently funded grant is not revoked or treated as extra free supply.

For A ending at 10 and B at 100, an A-sponsored mixed snapshot stops new executions at 10. If A cannot fund the operation and B sponsors it, H is **still 10**, even if its returned page contains only B or independent roots. Both old bindings stop; B can sponsor a fresh later cut after A's withdrawal. No remote collection/sponsor field is added.

## Closure of exposure, drain and explicit release

**Ordinary horizon closure** selects no new execution: close this grant's offers/calls/execution claims, including fresh paid reads/pages on old export/snapshot leases, and its current-index membership. Cancel unclaimed operation and delivery tickets, including committed replies not yet claimed. Only already claimed operations/deliveries may finish under their exact surviving scopes/guards and endpoints; a later committed response cannot start a new delivery. This admission cutoff is not itself owner withdrawal of disclosure permission. Old leases/pins authorize nothing new. Other owners' grants/postings survive independently; snapshots remain historical, not silently filtered.

A clean service-capability rollover preserves the original local clock generation, activation/end ticks, spending and pin; it grants neither another 24 hours nor new service resources. Actual reboot, writer takeover or unestablished clock-origin continuity closes this policy's public gate conservatively. E's durable ownership survives, and its explicit release/reconciliation path remains required. An old wall-clock timestamp or new invocation generation cannot restore exposure or rearm a selected/uncertain nomination.

**Actual disclosure withdrawal** instead invalidates the affected exact authorization/version and its dependent read/export/snapshot/delivery scopes immediately. Cancel unclaimed affected executions and delivery tickets, including committed replies not yet claimed. Running work rechecks its guards before commit; already claimed sends receive bounded cancellation, with actual sent bytes charged and no recall promise. Independently authorized grants survive only if they do not depend on the withdrawn permission. Native/clock incidents retain their own conservative guards; they are not ordinary deadline extensions.

The root-specific horizon, or discovery's H, plus 600 seconds is solely an upper bound on otherwise valid authority. Its reserved drain resources create no execution, lease, disclosure or delivery permission. Required unsettled/recovery state can outlive that ceiling and remains charged. Revocation can end permission sooner. Actual clock uncertainty invokes NET recovery, never wall-clock inference.

After those grants are terminal or conservatively fenced, the delegated owner controller makes the explicit release decision for this exact singleton custody instance and expected versions. E's `OWNED -> RELEASING -> RELEASED` transactions remove only this policy's custody reference. Active exports/uses, other owners, seed pins, caches, H anchors and snapshots retain their independent references. Relevant independently configured publication obligations must settle under their own contracts; this policy neither revokes them nor charges their obligations as zero. GC is ordinary metered generation-aware reclamation; released ownership is not reclaimed bytes.

If release/recovery cannot safely finish, remain visibly `RELEASING` or `FENCED_UNKNOWN`, keep obligations counted and decline new admissions when slots/resources fill. There is no automatic reacquisition, renewal or assumption that a remote receipt is a replacement custodian. A fresh exposure after complete settlement starts a distinct paid lifecycle and does not erase earlier costs.

## Joint resource envelope

All numbers are finite illustrative ceilings, not measured Lean capacity. Smaller inherited grants bind first. The owner must supply actual whole-node headroom for these allocations alongside every other role.

| Dimension | Ceiling/required allocation |
|---|---|
| Candidate rows / bounded terminal history | 32 / 64, also within metadata bytes; required replay fences are not optional history |
| Concurrent preparations | 1 |
| Custody/exposure lifecycle slots | 4 total including preparation, public, draining, releasing and uncertain states |
| Nominations / selector rounds | 32 / 4 per authorized 24-hour interval |
| One selector round | 2 CPU-seconds, 10 local seconds, 16 MiB workspace, 32 fit evaluations, 65,536 aggregate closure/reference inspections |
| Preparation starts | One per claimed nomination; at most four per interval |
| One preparation | 60 CPU-seconds, 600 local seconds, 256 MiB incremental workspace, within parent stock/work supply |
| Custody payload union | 16 GiB including foundation; actual physically shared bytes separately counted once |
| Custody/index/control/selector/history metadata | 256 MiB aggregate, also subject to inherited count limits |
| Additional preparation/staging workspace | 2 GiB aggregate; total native/other-role resident state still needs whole-node fit |
| One exposure service subaccount | At most 512 remote operation attempts, 4 GiB total traffic and 600 CPU-seconds, including setup/control/replies and paid failures |
| Newly authorized interval work | At most 2,048 remote operations, 16 GiB traffic and 3,600 CPU-seconds across all this policy's stages; no per-lifecycle multiplication beyond this parent |
| Policy storage I/O | 32 GiB per funded interval across checking-material/inventory reads, extraction, serving, custody maintenance, settlement and reclamation; actual overlapping reservations still count |
| Drain/release/recovery | Explicit reserved actual grants and record stock inside those totals; at least one settlement path per admitted lifecycle, or no activation |

Previously admitted intervals retain outstanding reservations: crossing a day boundary cannot release or recharge them. Interval issuance, actual spend and future obligations are reconciled under the existing ledger. Exposure horizons can overlap intervals, so admission requires the full promised resource/stock calendar and actual transition fit, not merely today's mean. Remote-operation counts include this source's admitted service/control attempts; raw ingress retains NET1's independent bounded admission protection. Serving, custody upkeep, index work, expiry handling, uncertainty and GC all consume supplied resources. Unused service capacity does not fund unadmitted native checks or another root. A cold closure larger than the remaining transfer supply can be locally public yet unavailable to a particular cold reader within budget.

Custody integrity/guard cursors use actual reserved recurring local work. EGRESS1 supplies no automatic remote replica-observation, repair-import or handoff grant; a fault can degrade custody/service pending separate authority, not create work. Checking materials, resident native environments and preexisting index state need separately counted whole-node supply. Expensive policy stages are serialized in this first schedule.

## Conditional traces and utility limits

**Useful direct reuse.** Assume a qualified source has independently exported/checked the B-associativity result from J's record-interface recipe; its exact closure, disclosure and all actual resource/transition requirements fit. No answer theorem ID is supplied to a later investigator. The root wins an age round, receives exact custody and a committed public structural posting. Within the actual service interval, an independent investigator already knowing the source contact queries B's operation token, reaches the result within its page/probe allocation, acquires its complete exact evidence and independently checks a four-factor reassociation proof. The source pays serving and custody; the receiver pays retrieval/checking. Its further output can independently enter the same nomination path. This is a conditional nonempty circulation path, not a speedup or global-novelty claim.

**Worked supplied instance, not measurements.** Stipulate an already qualified/protected 2-GiB shared core, including F and B/op_B, at source and receiver. The exact associativity replay adds 8 MiB. Historical core/producer acquisition and checking remain charged prehistory; they are not provided free by EGRESS1. The source's finite matching posting list has eight descriptors, the useful theorem is third, one at-most-64-row page completes the list, and the receiver funds three type probes. No answer ID is supplied.

| Supplied demand for this instance | Explicit fit |
|---|---|
| Source disk: 4-GiB checking materials, 2-GiB core + 8-MiB evidence, 1-GiB temporary allowance, 64-MiB metadata | Below 12-GiB supplied disk; custody payload below 16 GiB. Existing/new pins share bytes but have distinct counted records. |
| Source RAM: 3-GiB actual native state, 32-MiB preparation, 8-MiB publication/control, 16-MiB snapshot/spool | Below 8-GiB supplied RAM; preparation below 256 MiB. These native sizes are stipulated independently of serialized bytes. |
| Selector 0.5 CPU-seconds/4,096 inspections; preparation 4 CPU-seconds/20 elapsed seconds; service 20 CPU-seconds; upkeep/release 20 CPU-seconds | Total 44.5 CPU-seconds below 3,600; each stage also fits its own ceiling. |
| Source 48 total service/control attempts and 16-MiB traffic; 6-GiB scheduled scrub plus 64-MiB preparation, 16-MiB serving and 16-MiB settlement I/O | Below 512 calls/4 GiB service and 32-GiB I/O; snapshot/reply/drain reservations included, no remote repair assumed. |
| Receiver 16-MiB traffic, 100 CPU-seconds for probes/acquisition/independent checking and final two applications; 3-GiB native RAM + 192-MiB other peak state | Supplied 64-MiB traffic, 240 CPU-seconds and 8-GiB RAM. Disk supply 8 GiB covers its 4-GiB checking materials, warm core, new evidence and 80-MiB temporary/metadata allowance. |

Nominate at t=0, commit public exposure at t=60 seconds, and let the independent receiver start at t=120 and complete checked four-factor reuse by t=500. Its warm exact core avoids retransmitting 2 GiB, not checking new evidence; a cold receiver needs separately supplied transfer/reconstruction and is not this case. Existing calls/snapshots settle before h=86,460; the reserved owner release finishes by h+60, without a new daily allowance. Supplied costs/order/progress and current guards make this an arithmetically consistent paper path, not evidence that actual Lean artifacts fit it or that sharing beats local proof.

**Full-capacity refusal.** Let F occupy 2 GiB and incumbent exposed roots require 14 GiB of disjoint residual payload, filling the 16-GiB custody union. A staged checked C needs another 512 MiB; separate whole-node staging capacity makes C's existing local bytes legitimate. C still cannot enter custody. Selection cannot release an incumbent term/pin/anchor to manufacture space. Return `DECLINED_RESOURCE`; existing obligations survive. Four unsettled lifecycle slots can similarly refuse C even when its marginal payload is zero.

**Private-support refusal.** C's conclusion and public-looking metadata are harmless, but its selected proof closure contains an owner-private lemma. Authorization for C alone does not authorize that dependency. No public cut commits until complete disclosure authority exists. C remains valid local mathematics, not remotely servable through this policy; remote callers learn no private-existence explanation.

**Delayed or redundant value.** Cheap distinct corollaries can occupy admitted prefixes and slots while a costly foundational result is refused. Conversely, an exposed zero-use result may become valuable only after its horizon and lawful release. Neither no observed use nor a new JudgmentID settles usefulness. Exact-ID deduplication does not detect all variants; checked logical equivalence does not establish equal retrieval/checking cost or permit deleting promised bytes. Genuine repeated self-use is not independent demand, and this selector gives it no publication priority.

Required outcomes distinguish nomination/fit failure, custody-only, prepared-but-not-public, committed local exposure, degraded/closed service, historical observation, external checked reuse and settled release. All failures/costs remain in later [reciprocity evaluation](../qualification-readiness/reciprocal-evidence-plan.md); RQ-RECONTRIBUTE needs actual later independent acquisition/application, not merely `PUBLIC_ACTIVE`. Future causal benefit remains an experiment. No full-network coverage, indefinite preservation or sustained-growth theorem follows from this optional pre-public-cut choice.
