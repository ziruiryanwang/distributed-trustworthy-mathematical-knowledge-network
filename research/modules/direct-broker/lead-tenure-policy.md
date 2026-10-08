# TENURE1: optional broker-local source-listing turnover

Date: 2026-09-20. Root-authored candidate, NOT SELECTED; concept/specification only. No implementation, Lean execution or benchmark. This is a local policy for existing broker-owner selection, not a new wire operation, source-health certificate, global scheduler or mathematical acceptance rule.

## Purpose, inherited contracts and guarantee boundary

The [reviewed triage](../../cycles/2026-09-20-imported-exposure.md) identifies an honest failure: a full four-lead row may indefinitely name unavailable sources and reject a useful fifth source. I's query-snapshot expiry and reader retry do not replace those leads. TENURE1 offers a bounded **current-selection residence for each admitted listing installation**, conditional on continued local authority, qualified clock and explicitly supplied maintenance. It deliberately trades some healthy-source persistence for stale-slot turnover. No universal availability improvement or optimal usefulness ranking is claimed.

The inherited [I bindings](../../../notes/analyses/CP-001I-direct-broker-bindings.md), SHA-256 `2CE9222631ED95AE0CE7B31C875AA4CD72EA5D0440B7BC1A8E34FB84D7F2EFB2`, remain authoritative for operations21/22/23, exact call/reply accounting, plain value-CAS, lead grammar, metadata disclosure, immutable snapshots and resource limits. [BROKER1](../../../notes/analyses/CP-001I-untrusted-search-brokers.md) already permits separately authorized broker-owner selection. [V2](../../../spec/OPERATIONAL-CORPUS-V2.md) and unchanged [local authority/recovery](../../../spec/OPERATIONAL-CORPUS-V1-NETWORK.md) distinguish standing policy, each fresh finite execution grant, conservative restart and retained accounting.

The new choices are: one finite owner-admitted policy episode, an immutable nonrenewable tenure, a bounded installation-slot table, a paid cyclic maintenance caller and exact private incarnation fencing. Local agents can still explicitly publish imported checked results through existing controls. No automatic imported-result nomination, health probing, broker crawling, rejected-source queue or mandatory contribution is added.

The words **due**, **removed** and **released** are different. Due is a local maintenance target. Removed means an actual serialized current-index selection change committed. Released means the corresponding storage/control allocation was actually reclaimable and reclaimed. Due time alone implies neither of the latter. This policy supplies no wire-visible lease: LISTED/ALREADY_LISTED still attest only their actual acknowledgment cut.

## Authority, scope and immutable episode

One owner-admitted episode names:

- An exact broker-public metadata collection and its current owner-selection authority generation. All selected leads in that collection participate; an unmanaged parallel writer cannot bypass the table. Other collections must not alias these row keys in the same authoritative current index.
- Separate current metadata-disclosure authority. Selection maintenance does not grant disclosure; disclosure withdrawal does not itself authorize additional selection work.
- A qualified local clock origin g, activation cut a0, positive tenure tau, finite new-installation cutoff A and finite maintenance service horizon H. New installation at a requires `a + tau + Delta <= H`, checked without overflow, and `a <= A`. H is not permission to delete recovery records at H.
- A fixed number M of installation slots, with `1 <= M <= 262144`, no more than I's actual remaining lead capacity. The inherited four-lead-per-row, row/version/posting/byte/resident/control and per-source/global admission limits may bind much sooner.
- A scan width r, `1 <= r <= min(M,32)`, initial cursor `c0 in [0,M)`, supplied round-start spacing h, round completion bound w, admitted finite round count J and componentwise resources. `Delta = ceil(M/r)*h + w` is the conditional bound derived below, not a measured service rate.
- Standing authenticated authority for the scheduled local caller, exact due-incarnation removals, ledger updates and authorized cleanup. Every occurrence still claims a finite job from the same account. The episode names its finite calendar, not an indefinitely self-renewing timer.

An installation is admitted only with its original deadline and enough reserved service/transition/settlement stock through its due-sweep window. Specifically, the finite calendar must reserve/check a first post-due round start in `[e,e+h]` and C=`ceil(M/r)` successive rounds beginning there, with start gaps at most h and each round completing within w, unless earlier actual removal makes that installation's conclusion already true. Initial and terminal calendar coverage must be checked, not inferred from gaps between existing starts. Reserving the appointments is not evidence that they actually execute successfully; the progress theorem separately requires that supplied service. An episode cannot promise the bound from an aggregate daily CPU number alone. Already admitted unrelated duties and outstanding earlier reservations reduce the actual available supply; a new policy name or accounting interval creates no resources. Policy revision, clean admission rollover, endpoint changes, repeated submissions and invocation replay cannot change an installed incarnation's original due time.

These are local administrative settings, not additions to BrokerCandidate, HELLO, BrokerMutationAck or BrokerPage. Sources/readers cannot infer tau, the original admission time or remaining tenure from an I response. This matters for re-entry: useful retry schedules are separately supplied owner behavior, not callbacks or service promises created by TENURE1.

## State and representation

The authority maintains a fixed M-slot array, a charged exact `(descriptorID, sourceNodeID) -> slot` map, and a cyclic cursor `c in [0,M)`. Slot numbers do not move during an episode. An occupied slot holds:

`(d, source, incarnation, originKind, a, e, clockOrigin, episodeBinding, reservationRefs)`.

Here e=a+tau, `originKind` is INSTALL or ADOPT, and incarnation is a fresh private local installation identifier. One durable monotonically allocated counter under a persistent nonreused owner-local incarnation epoch suffices; checked arithmetic stops admissions before exhaustion. Recovery must establish nonreuse/fencing before accepting more work. Incarnations are not native identities, wire CAS revisions, timestamps or political attribution.

There is exactly one occupied slot for each currently selected managed `(d,source)` and no slot for an absent managed lead. Initial adoption assigns keys in canonical `(d,source)` order to consecutive slots starting0 and sets the cursor to the admitted c0. Fresh insertion chooses the least-numbered free slot at its actual commit. The row's current endpoint bytes remain in the ordinary I row, not frozen in the tenure record. Accepted endpoint updates preserve the slot, incarnation, a and e. Removing a lead and later inserting it creates a fresh incarnation, even if every lead byte is identical.

All current-row, exact-map, slot, counter, cursor and reservation changes participate in the same single-writer transaction as the relevant selection effect. A changed current row gets its ordinary new public cut; private cursor movement need not produce a public cut. Old public snapshots retain only their existing immutable roots, not authority to inspect this private table.

A maintenance job can retain at most r inspected slot/incarnation references and its finite ledger state. An old job reference can outlive the slot's removal/reuse, but remains charged and cannot affect the replacement incarnation. There is no per-lead queued timer/job: the M records are current policy metadata, not M pending executions. At most one tenure scan job is admitted at once, consuming actual shared concurrency/pending/control slots. This avoids assuming that hundreds of thousands of per-lead jobs fit I's128-item pending-work cap.

The exact map can use an ordinary bounded balanced tree; its actual comparisons, key bytes, references and mutation costs are charged. No expected-O(1) hash lookup or free full-row/posting repair is required for a bound. Table bytes, the map, in-flight references, outcomes, reconciliation records, current and retained index versions all count against actual broker-wide stock.

## Initial adoption without fictional history

Activation can start with an empty selected collection, but the useful case need not reset an incumbent broker. For an existing collection, first fund a bounded preparation over its complete exact current cut: enumerate every selected `(d,source)`, count all rows/leads/postings and actual retained dependencies, reserve its policy and worst admitted cleanup obligations, and verify all M/resource constraints. Serialize against current selection mutations during this preparation, or abort the attempt if the selected cut changes. Previously admitted mutations are settled or held under their actual finite grants; the preparation acquires no power to extend them. Query snapshots may continue only under their existing independently funded authority and stock.

One authority transaction then rechecks that same complete selected cut, installs the prepared slot/map state and starts the caller under the authenticated episode. All adopted records have a=a0 and e=a0+tau. This is explicitly an **adoption-relative** residence bound; no age is inferred from an old wire lead. Adoption can create a synchronized due cohort as large as M, whose service must be reserved before activation. Initial preparation/failure/interference costs are not erased by success or silently included in one remote submission grant.

TENURE1 does not repeatedly adopt an unchanged installed lead to reset its clock. Existing tracked records retain their original a/e through a compatible policy continuation. If continuity cannot be established, use the recovery/drain path below; a new active episode must not present `now+tau` as the surviving incarnation's deadline. Starting empty after an explicitly funded real removal is permitted, but the lost current coverage and old retained state remain real.

## Operation composition

These rules are additional local admission/state constraints, not replacements for I's prescribed wire outcomes:

| Event at actual I/owner decision cut | TENURE1 effect |
|---|---|
| Fresh op21 inserts an absent self lead | Reserve its finite lifecycle first; require a free actual slot, current authority/clock/episode and `a+tau+Delta <= H`. Atomically allocate fresh incarnation and install the row/slot/map. Otherwise decline under I; no pending-source promise |
| Fresh op21 updates the selected self lead's endpoints | Use I's actual expected-prior check; retain the existing incarnation and original a/e. Charge index/version/map work; it cannot be admitted as a new lease |
| Exact proposed lead already selected | Preserve I's ALREADY_LISTED no-op, including its permitted obsolete expected-prior behavior. No deadline refresh, enrollment, new incarnation or hidden expiry work |
| Exact invocation replay | Return its inherited historical outcome, with no new selection or tenure effect. Its LISTED observation may refer to an already removed incarnation |
| Fresh op22 withdraws current self lead | Preserve I's value-CAS semantics. Successful actual removal atomically clears its slot/map and current row/postings if last; do not erase old jobs/results/snapshots |
| Authorized owner-local removal | Remove the actual selected incarnation under its own finite authorization; clear its map/slot atomically; native custody and independent disclosure remain separate |
| Authorized owner-local endpoint replacement without an absent cut | Preserve its existing incarnation/tenure, just as a self update does |
| Owner-local insertion of an absent lead | Same fresh-installation and lifecycle admission conditions; prior source assertions remain inert. No bypass of global caps or tenure accounting |
| Due maintenance | Independently funded owner-local transaction removes only the exact still-current incarnation under the rule below; it is not executed inside op21 or op22 |

I step2 can still return ALREADY_LISTED while a lead is due but actual removal has not committed. That is an accurate selected-current-cut observation, not a renewal or a promised future listing. A new-source submission encountering a full row cannot evict a due foreign lead: its request still declines/defer-no-promise. A separately admitted maintenance job may later remove that lead; only an actual subsequent source/owner admission can fill the vacancy.

Private incarnation fencing does **not** strengthen I's wire CAS. For example, a delayed distinct op22 with the same lead digest can remove an identically reinserted source under I's allowed value-ABA. A delayed distinct expected-absent op21 may insert after intervening removal if actually admitted. Both obtain their real current effects and charges. TENURE1 promises neither durable source exclusion nor fifth-source fairness.

## Paid cyclic maintenance and atomic removal

The owner-supplied caller claims each scan from its finite episode calendar. It scans the next r array slots in cyclic order, counting empty slots, future-due slots, stale references and failed work. It cannot count only successful deletions. A round's actual byte/CPU/I/O/working-memory/ledger/transition-version allowance is reserved before claim, inside the shared broker account. Admission also preserves the resources needed to settle old work and admitted remaining lifecycle duties.

For each next slot, inspect its actual tuple and current clock under the writer's rules:

1. Empty, or occupied and not yet due: commit the counted inspection and cursor advance without a public mutation.
2. Occupied and due: prepare the bounded current-row/posting/state change under the job grant. At the serialized commit recheck owner selection authority, episode/clock guards, slot identity and exact incarnation. If it is the same current incarnation and still due, remove the **current endpoint variant**, clear its slot/map, and retire the current row and postings atomically if it was the last lead. Preserve and charge existing historical roots/outcomes. Advance the cursor with the committed decision.
3. If the slot changed during preparation, revalidate the actual next-slot state within the same bounded grant. A stale prepared removal cannot delete a new incarnation. Only an actual completed inspection/current guarded decision advances the cursor; an interrupted or unresolved decision is not a completed pass.
4. If authority, clock, resource, representation or accounting cannot be established, stop with an explicit charged nondecision; keep the last committed cursor and all real obligations. No next job or grant is minted. A later authorized occurrence resumes from that committed cursor. Exact job replay cannot double-advance it.

The first implementation recipe would serialize the small final authority transaction per inspected slot, not hold the writer across native work: this module performs no native fetch/check. Descriptor/row validation, sorted lead deletion, posting removal when last, index-root mutation, old-root pin accounting and durable finalization still cost actual work. A previously current row becoming unlisted is not a release of all its bytes.

The cyclic cursor does not change when a slot is allocated/freed. A still-current target stays in one slot until removed. New arrivals into other slots cannot keep moving it behind a scan frontier. If other writers prevent the admitted rounds from finishing, the service premise below fails; finite memory safety alone is not a liveness proof.

## Clock, withdrawal, rollover and finite drain

Clean NET2 admission sealing may pause new jobs and expires I snapshots as already specified. It preserves the policy's qualified clock, a/e, spent funds, cursor and unresolved obligations. Any sealing pause is included in the actual service bound h/w; a seal cannot be silently excluded from a promised expiry interval. A compatible caller resumption requires remaining admitted rounds and funding, not a new allowance from the new service epoch.

Uncertain clock origin, reboot or writer takeover invokes conservative recovery. Fence old job claims, stop new installs and stop this collection's new broker disclosures under the standing conservative gate; I's uncertain-restart snapshot/delivery rules still apply. Recover current rows, slot identities, reservations, old outcomes and spending before any positive active-policy claim. If original deadline continuity is established, continue those exact deadlines. Otherwise the recovery path, under still-valid owner authority and separately reserved recovery work, removes the surviving tracked current installations without assigning them fresh tenure. It does not infer elapsed downtime or call them mathematically invalid.

If the ledger/current-row correspondence or required authority cannot be established, keep the policy suspended and its collection closed to new disclosure until explicit owner reconciliation; do not treat hidden rows as deleted/free. A functioning stable recovery interval and actual authorized work are necessary for physical reconciliation. Repeated crashes can prevent progress; no bound crosses an unqualified clock interval.

Owner revocation of selection maintenance fences unclaimed and prepared maintenance commits. Reserved resources do not confer irrevocable destructive authority. The occupancy promise is then withdrawn/degraded for affected installations, while remaining state and settlement costs survive. Actual metadata-disclosure revocation separately follows I's snapshot/delivery rules. Neither event may be presented as a successful current-row removal. Deliberate disable/re-enable preserves original installation records where continuity is valid; otherwise explicit funded retirement/reconciliation is required before a new active policy.

At new-installation cutoff A, stop admitting new installations under this episode. Existing no-op observations retain I meaning; accepted endpoint changes cannot extend deadlines or consume protected removal resources. The preadmitted caller completes due work within H under its service premises. Once the installation gate is closed and all managed current leads are actually removed, stop routine scans and drain remaining jobs/versions/outcomes under their inherited guards. An empty table before A alone does not cancel future reserved scan service. H ends the promised maintenance window, not all retained evidence or accounting. Aftercare may outlive H; its stock and eventual authorized finalization remain allocated. New optional work cannot spend those reserves.

## Conditional invariants and progress

**T-SAFE: ordinary native trust is unchanged.** The policy changes only selected metadata. No transition grants native checking success, changes a replay/foundation, forces a local investigator's choice or releases source evidence. Independent acquisition/current native acceptance/use remains mandatory. Inductively, the new transitions create no native acceptance record.

**T-AGE: no implicit renewal.** While a managed `(d,source,incarnation)` remains continuously current, its a/e/clock origin are unchanged. The only admissions creating fresh a/e require an absent old installation and a fresh fenced incarnation, or the once-only explicit initial ADOPT cut. Operation-table cases preserve this invariant. This does not forbid a later newly admitted incarnation of the same source.

**T-FENCE: delayed cleanup cannot remove a replacement incarnation.** A removal transaction compares current slot and exact incarnation under the same authority writer as insertions. An endpoint-only update retains the incarnation and is removed when due; an intervening removal/reinsertion changes it and makes old cleanup stale. The claim is local to these cleanup transactions, not I's wire value-CAS.

**T-BOUND: bounded current residence.** Fix an installation i with due time e_i=a_i+tau in a continuously qualified clock interval and let C=`ceil(M/r)`. Earlier actual removal already satisfies the residence conclusion. Otherwise suppose current-policy authority persists, the slot/cursor invariants hold, and all inherited and new jobs fit their actual grants/stock. Require actual successful rounds with first start `s1 in [e_i,e_i+h]` and C successive successful covering rounds in total, with `s_(j+1)-s_j <= h`; every round completes decisions for its next r slots within w of its own start. This explicitly supplies the first post-due start and enough finite-tail coverage. If earlier actual removal or authorized complete drain ends the need for those rounds, no claim of their execution is made. Interference, seals, failed rounds and recovery consume real time and resources; they must fit this coverage or the bound is unavailable.

By the explicit coverage premise, `s_C <= s1+(C-1)h <= e_i+C*h`. If i has not already been removed, those C rounds make at least M completed cyclic slot advances and must visit its fixed slot; completed advances in any intervening partial round cannot move the cursor past a still-current due i without its guarded removal. An interrupted decision never advances the cursor. At i's visit, either earlier actual removal already suffices, or it is current and due and the transaction removes it. That decision completes by `s_C+w`. Therefore current-selection residence ends by

\[
e_i+\Delta = a_i+\tau+\lceil M/r\rceil h+w.
\]

The extra w handles within-round timing; a round that inspected i just before it became due need not revisit it immediately. The proof is for actual successful contiguous scans, not arbitrary attempts. A finite allocation that cannot supply those scans yields safe nondecision, not the bound. For ADOPT records replace installation age by the explicitly named adoption age.

Neither old snapshots, already delivered pages, native custody nor later incarnations are bounded by T-BOUND. If a source actually crashed with no surviving reinstallation intent, its old installation cannot occupy a current slot beyond the bound under these premises. Without the no-reinstallation premise, the same source identity can remain represented by successive installations. A competing honest source can repeatedly win each vacancy; per-incarnation turnover is not fair admission.

**T-OPPORTUNITY: sufficient, not automatic, escape.** After actual removal creates space, assume X remains an admissible independently supplied public source; a fresh funded X submission actually commits while a slot and all resource/authority guards are available; a reader obtains a fresh admissible broker view naming X early enough; and its paid source acquisition/check/use path meets the remaining deadline under separate native scopes. Then the added path can succeed using unchanged I/native operations. There is no hidden scheduling implication between these assumptions. A DECLINED request does not revive when a slot opens, and a historical view does not learn X.

## Resource certificate, not manufactured supply

A finite episode's admission certificate records actual residual per-owner vectors and all-times stock, together with an explicit calendar. At the broker, count at least:

| Category | Required charged quantities |
|---|---|
| Initial preparation/adoption | Entire selected-cut enumeration, all actually inspected bytes/references, map/slot allocation, interference/failed preparation, serialized activation and old cut retention |
| Installation/update/withdrawal | All actual remote/owner mutation attempts, syntax/authorization, slot/map work, changed index versions, I outcomes/control/reply spools; no-op observations are still paid operations |
| Scan | J actual claims, at most Jr planned slot inspections, and every actual preparation/revalidation/reference/index operation; failed rounds retain cost and consume calendar capacity |
| Current and historical stock | M-slot array, map, current rows/postings, all snapshot-pinned versions, in-flight prepared replacements, old job references, outcomes, logs and pending reconciliation |
| Removal and drain | Actual row/lead/posting changes, slot-map updates, writer/accounting/finalization, snapshot/result retention until real release, eventual cleanup and uncertain outcomes |

The maximum M is a count ceiling, not proof that the table fits memory or that the largest cohort can be processed within h/w. Actual representations and primitive costs remain qualification inputs. A table slot freed by removal can be reused only if the **additional current and historical state** also fits all limits. Four free lead positions do not imply a free row version, snapshot slot, execution ticket or byte allocation.

Local scans are not free remote opcodes. Conservatively, this candidate's owner accounting debits each fresh local scan job against the same20,000-per-interval paid-execution allowance used by its admitted broker calls, in addition to local job/control caps. This is a stricter local budget choice, not a wire change or an inference that I previously excluded local work from CPU/stock. Remaining CPU/traffic/working-memory/resident/I/O/durable-state limits are independent; a count fit does not buy any of them.

Let Q be query executions, U all source/owner mutation executions and J scan jobs in the actual admitted interval. Require `Q+U+J+otherChargedExecutions <= actualRemainingExecutionGrant`, with no duplication or exclusion of failed work. CPU/traffic/I/O/stock reservations use their own actual vectors, not that scalar. Reserve the complete worst admitted due cohort and its transition versions before installing its members. Rate `N/tau` alone cannot schedule synchronized removal of N leads.

For an interval of length L and a fixed successful round-start spacing h, about `L/h` rounds and `rL/h` inspections may be required even if few leads expire. A larger M can require a larger Delta or more service. Reducing h improves the conditional delay but spends more scan work; this is an explicit engineering tradeoff. An event heap or contention-triggered policy might reduce idle work, but would require its own bounded representation/service proof; no such saving enters this recipe.

**A recipe-specific scaling exclusion.** Consider the uniformly periodic variant over one entire applicable86,400-second accounting interval `[0,L)`, without early drain or aborted coverage, with first successful start in `[0,h]` and subsequent starts spaced by h throughout. Set M=262,144 and r=32, so C=8,192. To certify a scan lag Delta of at most3,600 seconds through this formula, even the optimistic relaxation w=0 requires `h <= 3600/8192 = 0.439453125` seconds. The interval contains at least `ceil(L/h)-1 >= 196607` fresh scan starts; starting at h and excluding the right endpoint is the conservative boundary case. This already exceeds20,000 before any query, source submission, adoption or other job. Positive w only tightens the constraint. Thus that uniform full-interval certificate cannot fit this candidate's shared execution-count policy. This does not prove an unavoidable actual deletion delay, defeat a targeted finite due-window calendar, exclude another local representation/policy, or establish a limit on decentralized network scale. The small trace below therefore cannot justify this maximum-table periodic default.

Source owners separately fund public preparation, complete evidence custody/service and every submission/no-op/conflict/retry. Readers separately fund historical failed trials, fresh queries, source acquisition, complete checking/application and settlement. Source use frequencies create no grants. Extra broker metadata turnover can raise both source and reader costs. A comparative study must include unsuccessful work and coverage gaps; this source supplies no measured net advantage.

## Finite recovery trace and countertraces

The following is a **new hypothetical policy trace**, not continuation of K50-R1500 or a reset of its resources. Its purpose is to expose causal dependencies, not instantiate native artifacts or supply a full numerical multi-owner cost comparison. The same starting row, real owner capacities and explicit caller attempts are used when contrasting this policy with leaving that row unchanged.

At analyst time0, broker E adopts one row d with four leads S1..S4 in canonical source order into M=8 slots0..3; slots4..7 are empty. tau=100, r=4, c0=4, h=4, w=2, hence Delta=10. Fix a genuinely funded finite calendar of99 scan starts4,8,...,396, alternating slot blocks, with slot block4..7 at100 and block0..3 at104. Every successful round completes within2 local seconds of its start, including the final round by398. The lead slots are stable and all clock relations below are supplied scheduling facts, not a conversion of another owner's ticks by a caller. No scan/native cost is measured.

All four sources become unavailable without withdrawing. At90, X's already separately prepared native source submits its exact same-replay self lead; it is declined while the row is full. A reader's old snapshot at98 contains only S1..S4. The100-round inspects the empty block. At104 the paid round inspects the due block and commits all four removals by106, including last-lead unlisting. The actual mutation/version/calendar premises are necessary for that completion, not implied by the four-count alone.

X's separately scheduled fresh submission starts108 and actually commits by110, using a free slot and new incarnation with due time210. The reader pays for its prior failed attempts and chooses a separately admitted fresh query at112; a complete adequate result naming X arrives by114. Reader acquisition/use success additionally requires actual remaining source/receiver admission, compatible complete native support and deadline fit. For example, supplied acquisition through154, independent checking/application through354 and settlement through364 would fit a400 deadline. These times are **external primitive-service premises**, not native execution results or tenure promises. They do not relax any receiving predicate.

New-installation cutoff A=120 and maintenance horizon H=400 admit the110 installation because `110+100+10 <= 400`. No later installation is stipulated. The scanner eventually removes X's broker incarnation by220 (the stated alternating calendar can do so by218). That removal does not revoke an already independently acquired native source scope or delete X's evidence. X's original public/custody/service and any export leases retain their own finite authority, resources and aftercare. The directory trace does not pay those by assertion.

The planned99 scan jobs reserve396 slot inspections, including empty slots, plus actual five lead removals, two last-lead unlistings, one X insertion, two X submission outcomes, query jobs and all finalization/old-version work. A policy implementation may stop scanning earlier after an authorized complete drain, but those savings are not assumed in the reserved calendar. All relevant old snapshots/results and local outcomes remain charged through their actual release, even beyond400. Existing I snapshot occupancy must hold at every time; choosing short leases or receiving END does not erase already retained outcomes.

With the same source attempts at90/108 and reader queries at98/112, **unchanged row selection** rejects X twice and cannot disclose X to this stipulated reader. This compares two local selection policies on the restricted contact graph, not every allowed owner intervention, broker choice or native route. A separately funded manual/agent owner replacement can also solve the case using existing operations. The failed unchanged-row client path is not fully costed here; no cost superiority follows from its lack of an X edge.

Countertraces are part of the offer:

- **Healthy sole source:** one honest source remains usable but makes no later listing attempt. Tenure unlists it; an E-only reader arriving later loses a useful discovery path that indefinite selection preserves. No health discrimination was claimed.
- **No re-entry:** X is declined once and never makes another funded attempt. Expiry makes vacancies, not X listings.
- **Competitive recapture:** each cleared slot is filled by an incumbent/new competitor before X's next actual admission. All installations have bounded residence, yet X can starve for any admitted finite horizon.
- **Endpoint churn:** the due incarnation's endpoint bytes change repeatedly. Stable incarnation/deadline makes it still removable; digest-only expiry would incorrectly miss it.
- **ABA:** old maintenance sees incarnation i, source withdraws/reinserts identical bytes as j, and old cleanup later runs. It cannot remove j. A distinct wire value-CAS withdrawal still can under I; these are different claims.
- **Expiry burst:** M adopted leads share one due time. Without the full scan/transition service, daily totals or r-per-job caps do not establish Delta. Nondecision remains charged and the promised service is degraded.
- **Old evidence of a route:** a live historical broker snapshot/page still names a removed incumbent or earlier X. Current selection absence alone cannot prove that a particular reader has no usable contact.
- **Clock/authority incident:** a restart or owner revocation interrupts the admitted calendar. Preserve/fence state and report suspended/degraded status; do not rebase tenure, claim current absence or spend revoked authority.

The preceding triage's inclusive-cut information bound explains why no blind tenure tuning guarantees both healthy-listing persistence and timely crashed-listing removal. Practical tuning is allowed; universal optimality is not an admission gate.

## Local status, qualification and disposition

Owner-local status reports the exact episode/clock, fixed configuration, ACTIVE/DRAINING/SUSPENDED/ENDED authority state, committed cursor, current managed-incarnation count, actual completed/failed rounds, due backlog, reserved/spent resources and actual removal observations. It distinguishes INSTALL versus ADOPT ages and current versus historical discovery. This is charged local control data, not a new remote health oracle or protocol field.

An ACTIVE configuration is not evidence that its service calendar was supplied; report missed-round/overdue observations and withdraw the Delta claim when its premises fail. Absence of a timer event is not native rejection. Wire responses keep their existing narrower meanings. A different optional owner policy may coexist only on disjoint state with real shared accounting and no bypass of this installation mapping.

Concept review must check the whole state/resource/clock composition and both useful and defeating traces. Subsequent qualification would need actual bounded representation/transaction/conformance evidence, source/reader interoperability and useful workload comparisons. Those are already routed by the [readiness module](../qualification-readiness/README.md); this note creates no duplicate evidence plan. All six native/eight reciprocal runtime gates remain NOT RUN.

Disposition pending independent full-cut review. Even a clean paper review would justify only an optional conditional local policy, not a default optimal turnover rate, universal source admission, sustained useful growth or deployment readiness.
