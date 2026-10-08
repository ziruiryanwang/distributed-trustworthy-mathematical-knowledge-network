# Continuing growth: operating-envelope triage

Date: 2026-09-20. Author/integrator: root. Status: reviewed triage after scoped independent arithmetic and composition reviews. This note records new consequences of selected contracts and confirms an existing expansion path; it selects no new protocol, controller, cadence or resource profile. Concept inspection and arithmetic only. No implementation, executable model, extraction, native replay or benchmark.

## Question and inherited boundary

Does successful finite [O normalization](../../../notes/checkpoints/CP-001O-published-batch-normalization.md) justify continuing the same growth and recovery schedule as a slot fills? No: O proves a finite logical-count result conditional on paid physical steps. [H](../../../notes/analyses/CP-001H-resource-supply-and-discovery.md) separately caps aggregate resources and explicitly distinguishes amortized work from daily bursts. [N](routing-recovery-contract.md) supplies only a finite 16,392-key refresh witness with pending new inputs.

The previous goal turn was progress: O closed an actual arbitrary-batch ingress choice. This investigation asks a different question, not whether O's reviewed finite proof should be redone. Its three numerical boundaries below concern one selected workload: eight common tokens and eight target-unique tokens per target, four copies, the H daily grant and N's declared costs. Other incidence, representation, batching or reclamation changes require their own accounting.

## The highest ordinary carry exceeds one whole daily call grant

Consider one completed 2,048-target incumbent and one disjoint READY_FOR_CARRY run of the same size in one provider's H slot. The incumbent owns the eight common keys and its 16,384 unique keys; the ready run owns its 16,384 unique keys and borrows the common eight. Both have the actual published rows specified here, but there is only one completed incumbent at that tier. Their union has 4,096 targets and 32,776 keys, below H's 33,000 owned-token ceiling.

Changing to the union's immutable scope transfers all actually owned keys of both parents. With four current copies per key, this is

`4 × (16,392 + 16,384) = 131,104 placement-row moves.`

Under O's selected one-row-at-a-time transfer path, each move requires its own DROP and PUT:

`2 × 131,104 = 262,208 calls > 262,144 calls/day.`

The deficit is 64 calls even if renewal, group OPEN/CLOSE, contact maintenance, native work, queries and repair were zero. Those duties are not zero. Thus this particular ordinary carry cannot finish in one funding-day grant using that path. A favorable small 10,240-call example cannot establish otherwise.

This is a calls lower bound for the selected serial single-row procedure and this actual four-copy state. H's generic bounded batches could combine several same-holder/group mutations in a separately supplied schedule; a mutation count is not a universal RPC lower bound for that alternative. Batching does not eliminate the actual row mutations or permit unrelated holders to participate in one atomic batch.

A multi-day transfer is not logically forbidden. It needs real continuing old/new leases, group eligibility, unresolved-outcome accounting, renewals, actual phase progress and retained-tail room across grants. Reboot or a new day does not erase spent work. No complete multi-day highest-carry calendar is supplied by this note.

## Full-size refresh cannot inherit the eight-day witness

For 4,096 targets under this incidence, U = 32,776. In the explicit case where each selected fresh lookup actually consumes 64 calls, lookup work alone is

`32,776 × 64 = 2,097,664 calls.`

Eight complete H daily grants supply only

`8 × 262,144 = 2,097,152 calls.`

The 512-call shortfall exists before a single renewal or placement operation. This rules out an eight-funding-interval full-64-lookup schedule for that set under those grants; it does not say every actual lookup must cost 64. Shorter useful lookups are an alternative service premise, not a conclusion from the cap.

If N's 80-call-per-job refresh/replacement reservation envelope and its remaining daily shares are retained, only 163,920 calls/day remain for 2,049 such reserved jobs. Reserving the full envelope for every key needs 2,622,080 calls; this is not a claim that every actual job consumes all 80 calls. Sixteen daily shares have 32,784 job slots, enough in the reservation-count dimension for 32,776 jobs; fifteen do not. Equivalently, ceil(32,776 / 2,049) = 16.

This is a funding/calendar-capacity calculation, not a selected sixteen-day recovery guarantee. Actual starts, completions, eligibility, new arrivals, remote admission, reader overlap, clocks, CPU/I/O, renewals and stock must still compose. N's own Δ+L+P result requires attained service premises. A changed publication owner already invalidates the affected N commitment under O; new keys also need readmission. There is no contradiction with N's original scope.

Funding intervals here are explicit complete grants, not an arbitrary rolling elapsed-time interval straddling extra grant boundaries. Bucket phasing cannot justify an unstated stronger deadline.

## A slower refresh cadence does not by itself repair peak stock

Apply N's conservative retained-generation accounting recipe to U = 32,776, retaining the same stipulated record sizes and a lifetime union of at most 20,000 holders:

| Managed state | Conditional accounting amount |
|---|---:|
| At most 4U new group generations plus 20,000 original groups, at 4 KiB | 151,104 × 4 KiB = 590.25 MiB |
| Old plus new four-copy row generations, at 2 KiB | 262,208 × 2 KiB = 512.125 MiB |
| Subtotal before all other metadata | 1,102.375 MiB |
| With N's further 256 MiB for other records, before extra side scopes | 1,358.375 MiB |

H's aggregate metadata ceiling is 1,024 MiB. Therefore the unchanged conservative witness cannot certify fit at this scope, even before side-scope state. Nominal row/group/target count ceilings do not supply the missing bytes.

This is failure of a sufficient upper-bound accounting recipe, **not** a proved unavoidable lower bound on every physical execution. Earlier actual reclamation, real group reuse or smaller actual records may reduce the peak. Each requires a concrete jointly funded stock/calendar argument and qualified representations. N's two-hour tail-settlement premise suggests a possible bounded-window analysis, but merely mentioning that premise does not supply the revised peak proof. Increasing the cycle to sixteen days alone does not change the retain-all recipe.

Consequently, neither the 4,096-target capacity number nor O's finite potential lets an operator extrapolate N's small-scope operational promise unchanged. H already requires current admission against every actual resource dimension.

## Existing additive expansion path: a new provider admits new work

Read-only inspection confirms an existing usable conditional consumer chain, not a missing capacity-market operation. Let A keep its existing roots, and let B be a known willing independently authenticated provider with actual locally authorized capacity. Select a finite exact cut R of new roots for B. Old roots at A are not released by this choice.

1. **Local nomination.** B's authenticated local client submits exact root replay IDs and source references with PUBLIC_REQUESTED through the [existing local interface](../../../spec/OPERATIONAL-CORPUS-V1-NETWORK.md). This is a request to B's local policy, not an incoming remote storage grant. A bounded HINT is optional inert candidate information, not an automatic import command.
2. **Exact current identity.** The inherited submission/custody operations use [G's selected code-4 PI1 bindings](../../../notes/analyses/CP-001G-profile-and-consumer-bindings.md), including exact InstanceReplayID, FoundationID, required capability and actual closure. The reference to a v1 interface does not restore superseded root schemas, qualification candidates or global-epoch rules.
3. **Acquisition and custody.** B reserves acquisition, checking, staging, metadata and checking-material capacity through [E's custody admission](../../../notes/analyses/CP-001E-custody-contract.md). B independently checks the exact complete support and durably stages bytes before atomic activation. A and any other sources separately authorize and pay their own serving. Incomplete or over-budget work is not active custody.
4. **Public exposure.** B separately authorizes PUBLIC_SERVE for the full exposed closure; private dependencies are not disclosed by root reference. Actual funded index insertion and actual provider/token ownership/placements follow [H's incremental contribution](../../../notes/analyses/CP-001H-resource-supply-and-discovery.md). An outbox intent is not an index or routing commit. E custody alone grants no public service.
5. **Independent reuse.** A later reader reaches B only under actual [F routing/overlap/service premises](../../../notes/analyses/CP-001F-dissemination-and-routing.md), pays for FIND and complete acquisition, and independently checks its actual mathematical application. B's new identity or signed advertisement proves neither native validity nor future availability.

This adds a willing provider for R without requiring a global roster, moving all old mathematical roots, or changing investigators' goals. The exact support of R may nevertheless include much of A's earlier mathematics. That closure, cold checker/core onboarding, actual resident native memory, proof serving and ongoing index/custody duties must be charged; “new roots only” is not “small incremental cost.” Warm-core assumptions require separately paid and qualified prehistory.

A compact demand decomposition is: B pays its missing exact closure and native/core setup, checking/staging, active custody and new index/routing maintenance; sources pay actually served bytes and service work; later readers pay discovery, missing closure, checking and application. Shared physical allocations may be counted once only where genuinely shared and owner-controlled. These categories are not new grants or performance measurements.

The chain remains conditional: current complete BOOT1/native interoperability has not been executed. Known willingness and allocated capacity are external supply, not things an autonomous agent can create by sending messages.

## Same identity is not the same expansion mechanism

H's multiple locally supplied slots can share a physical host, but a slot label is not a remote provider/query namespace. Under one provider identity, identical provider/token rows still have one owner, and provider-wide FIND plus the shared owner/borrower ledger remain coherent. Independent copied ledgers at the same provider identity can produce ROW_OWNER_CONFLICT for common keys.

Additional local slots must therefore compose with the actual single logical provider authority, postings and token-owner ledger, or use separately authenticated provider roles under separately admitted resources. More keys do not create hardware, failure-domain independence or new parent grants. A new independent provider cannot count A's existing rows as its own four copies; it advertises and funds its own provider-key records.

M's known-contact exposure is not an automatic slot-expansion controller and selects neither HINT nor routed publication. An automatic high-water threshold, willing-destination preference and new-arrival allocation policy remain optional owner-local choices. No such policy is selected here. The existing local submission path is enough to establish that expansion is not missing a wire primitive.

## Disposition and next evidence

The meaningful result is a sharper operating envelope, not another protocol amendment:

- O's finite result remains valid, but the largest ordinary serial carry needs more than one whole daily call grant.
- Full-size recovery needs a newly supplied cadence or cheaper actual lookup regime; sixteen days fixes only the stated job-call arithmetic, not the resource/time proof.
- N's unchanged retained-generation recipe fails the larger metadata cap, so peak-stock qualification cannot be replaced by an average-rate calculation.
- Known willing independent-provider admission already has an exact consumer path. The choices are actual larger/more efficient local service, a separately justified larger-slot schedule, supplied additive placement, or honest refusal/reduced coverage—not automatic capacity creation.

A further large-slot or automatic-expansion proposal is warranted only if it supplies the coupled missing calendar/stock/policy choices and serves a concrete intended deployment. Existing evidence plans need not be recopied. The decisive whole-system uncertainty remains actual complete native bootstrap, export, checked application and independently replayed derived contribution, alongside control/service conformance and causal useful reuse. All six native and eight reciprocal execution gates remain NOT RUN; execution still needs explicit authorization.

The independent [resource review](audits/growth-boundary-resource-audit.md) and [composition review](audits/growth-boundary-composition-audit.md) reread repaired cut `47B00C28B368F6AF037C7679629611B2A687C6FA0B8C6B5AD793E1A26E5A19E2`. Two precision repairs distinguish a completed incumbent from a colliding READY_FOR_CARRY run, and actual lookup cost from an 80-call reservation envelope; both reviews independently identified the lifecycle wording. The audits record their separate final editorial rereads. No blocking issue remains within their scoped review, but these derived boundaries and existing-path confirmation are not a new selection, measured performance or completion of the overall goal.
