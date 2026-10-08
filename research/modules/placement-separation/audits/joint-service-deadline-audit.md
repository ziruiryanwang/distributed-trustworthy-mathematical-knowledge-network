# Joint service envelope: independent deadline and service audit

Date: 2026-09-20. Reviewer: `joint_deadline_challenge`. Status: **complete repaired-cut rereview; no remaining service/deadline blocker identified within scope**. This is a paper specification audit, not a scheduler implementation, executable model, Lean run, extraction or benchmark. The reviewer owns this audit only and did not edit its source or predecessor contracts. No profile selection or operational qualification follows.

## Exact review boundary

The complete current source independently read and hash-checked is [joint-service-envelope.md](../joint-service-envelope.md), **31100 bytes**, SHA-256 `65F68CA344A9BA2C835E01D8585945B7BD1478DC425D4A75F859802BF7F0EA4E`. The complete initial cut also received an independent read/hash check: **30447 bytes**, SHA-256 `FC2F82726C13C1E229328CA40C7079E17595BF1F6223156C1FD1F7C08A0C313C`. This review examines service decomposition, guard-valid completion windows, effect-lane sequencing, holder-clock deadlines, executor conflicts and the exact finite churn counterexample. The independent [resource audit](joint-service-resource-audit.md) owns complete resource arithmetic and the growing-current-domain enumeration premise. Its final source-cut identity and own finding disposition must be checked separately; this review does not substitute for them.

The reviewer also read the complete three preserved predecessors and independently checked their hashes:

| Predecessor | Bytes | SHA-256 |
|---|---:|---|
| [Stable-group contract](../stable-group-contract.md) | 68458 | `EA9398969D640BDE89271E53274B4F0071D00436659F5BF8D03FC266AD250779` |
| [Equal-service comparison](../equal-service-cost-comparison.md) | 48606 | `467E52601C79B4E4B24253F8D9A6B94A2B06C13838893EA97391E617492EC6C5` |
| [Shared support catalog](../shared-support-catalog-contract.md) | 37431 | `655547D7AE5D4501A3603870F0578F02A44DE4B07F5992CED16ABE246C72EAF7` |

Relevant predecessor-audit passages were checked for the already repaired original-dispatch clock, complete supported/removal partition, full preparation-prefix latency, scoped-catalog deferral, and upper-envelope versus lower-bound distinctions. This is not a new review of every inherited selected protocol operation.

Before source hold, this reviewer sent root and the author the finite 60/15/5 timing challenge, the distinction between conservative certificate rejection and actual infeasibility, and the need for actual later-round lease supply. The held source incorporates those preflight suggestions. They are not findings against the completed source or separate discoveries made after hold. Root also directed the equal-service/per-policy-attempt fairness check. During review, root and the resource reviewer raised the distinct-arrival/current-row enumeration seam; it belongs to their recorded resource finding, not an independent deadline discovery here.

## Initial verdict

No blocking service/deadline defect was found in the initial held cut within this bounded review. The finite calendar and clock conditions support a conditional service certificate, and the supplied churn case defeats the chosen recipe despite ample aggregate daily work. Neither conclusion supplies an actual positive whole-service deployment, credible measured primitive bounds, sustained useful growth, or native qualification.

The result remains limited by the exact supplied operating assumptions. In particular, the counterexample does not rule out differently staged support algorithms, independently current summaries, a different permitted publication schedule or a different service offer. This initial verdict was supplied before the common replacement; the final rereview below supersedes the pending-review state without changing these limits.

## Authorization windows and deadline windows are different

For a catalog epoch beginning at `c_r`, the source requires a real start slot, complete preparation and the actual predecessor chain through the group's support-summary publication/authorization before the next relevant `C/R/V` change. Waiting, incumbent jobs and nonpreemptible blocking are not silently removed from that chain. Preparation is one work expense but its full latency precedes every dependent group's authorization; dividing preparation time by the group count is not permitted.

The two sufficient inequalities have different purposes:

`c_r + a_(r,g)^+ < c_(r+1)`

`c_r + z_(r,g)^+ < safeDeadline_g`.

The first provides a current structural/support authorization opportunity. The second places the actual holder renewal commit before a conservative expiration lower bound. Their conjunction is used with the inherited exact member maps, native/support inspections, mode predicates, final guard comparisons and actual primitive supplies. A small sum of daily CPU or calls implies neither inequality.

An incident after the local one-shot authorization boundary can coexist with a later commit of that already authorized operation. The source correctly does not require current guards to remain unchanged until every such remote commit. It instead prevents the obsolete authorization/result from restoring a current source-support assertion. Local authorization, actual remote effect, result reconciliation and current coverage are separate events. This preserves the inherited race semantics rather than treating a new source fence as global cancellation.

All per-member current dependency inspections remain in the scan path; a catalog hit or complete structural build does not certify native support. Classification and post-cleanup authorization are still distinct actual map/support scans. A shared catalog may support both only while its exact dependencies remain current. Unknown actual members need their separately admitted resolution/removal branch, not omission from a timing sum.

## The finite churn counterexample is decisive at its declared scope

The source's case supplies equal continuous source/holder clocks, actual expiry at time 600 and an original occurrence giving that exact conservative deadline. At time zero there is no independent current summary or already authorized renewal to bypass the invalidated work. Relevant selected-entry commits occur at `0,70,140,...,560` and invalidate this catalog-dependent policy without withdrawing the designated survivor's native support.

The stipulated sequential critical path is a 60-second complete current build followed by 15 seconds of full scan/authorization work, followed by a five-second renewal-commit path. It is an exact duration premise for this chosen recipe, not an inferred lower bound from an upper budget or an empirical claim. No partial work from an obsolete cut supplies the missing current summary. A differently staged implementation with earlier credited precomputation is outside this exact timing fixture.

Every early valid interval lasts 70 seconds, shorter than the required 75 seconds to current authorization. The last cut at 560 gives earliest authorization at 635, already beyond actual expiry 600; even the hypothetical still-active renewal completion would be 640. In the actual inherited lifecycle, an expired group cannot be renewed into uninterrupted continuity. A later reopening/repopulation would be a new separately admitted service interval, not a retroactive repair of this gap.

The arithmetic is consistent: eight interrupted prefixes take at most `8*70 = 560` elapsed seconds, and the final hypothetical complete path takes 80. Under the separately supplied at-most-one-CPU-second-per-elapsed-second bound, their attempted-path CPU allowance is at most 640, below a 700-second residual allocation. This is not the complete node bill: the source explicitly retains independently funded publication/native/custody/query work and their executor reservations. The failure can persist with ample physical stock and holder capacity because it concerns the absent valid authorization window.

Adding executors alone does not shorten this stipulated serial dependency chain. This observation is not a theorem that every implementation has that chain: concurrent precomputation, another qualified summary mechanism, shorter primitives or delaying offered commits changes a declared decision variable. The case establishes failure of the stated recipe under the stated service/event supply, not impossibility of all decentralized mathematical services.

## Conservative rejection is not a general impossibility proof

The source distinguishes three forms of statement correctly:

- Supplied upper duration/work bounds can support a sufficient admission certificate when all prefix conditions fit.
- Failure of those conservative inequalities rejects that certificate, not every possible implementation or schedule. The actual work can be smaller and actual expiry later than the conservative bounds.
- An impossibility conclusion for the stated plan needs actual count lower bounds or exact/lower timing and actual service-deadline premises. The 60/15/5 churn case supplies the latter; the dispersed adoption call exclusion is separately owned by the resource review.

The strict inequality at the valid-window/deadline boundary is a conservative admission rule. Equality or failure of an upper-bound test is not silently converted into an observed runtime failure. The source likewise does not infer a fixed common-clock renewal frequency merely from the inherited 48-holder-hour lease maximum.

## Occurrence-bound clocks and later rounds

The preserved clock rule is

`safeDeadline = s0 + remainingAtOriginalCommit/(1+rho)`.

Here `s0` is the retained original effectful invocation dispatch, or a proved earlier timestamp in the same continuous source monotonic origin. The response is tied to that invocation occurrence and its actual holder/group authority. If holder elapsed time is at most `1+rho` times source elapsed time throughout the required interval, this is a conservative source-clock expiration lower bound: the actual commit cannot precede `s0`, and exhausting the reported remaining holder duration cannot require less than that duration divided by `1+rho` in source time.

Replay/retransmission send times, later reply delivery, copied results and requested future lease durations cannot replace the occurrence basis. Missing continuity or clock-rate supply gives no deadline certificate. The source also correctly distinguishes the holder-speed upper bound used here from a positive holder-progress lower bound needed for a universal common-clock renewal-frequency lower bound.

A second renewal round cannot use the first round's requested lease as if it were a completed observation. The source supplies two legitimate conditional paths: obtain the actual fresh occurrence-bound observation before successor admission, or require an explicit minimum resulting lease/response primitive contract covering the planned branch. An upper lease limit alone is not that minimum. Future successful operation remains conditional on its actual supplied service, not a present fact.

## Effect lanes and shared service calendars

Every promised critical path includes actual old-effect settlement, including an outstanding OPEN. The strict SG lane is not released by timeout or by sending another effectful observation. If a possible old action removes a designated survivor, continuity from the original incident cut is not rescued merely by promptly settling it. These are explicit exclusions in the source and agree with the preserved group contract.

The calendar must represent all actual owners and shared physical hosts. Source CPU/calls do not entitle a holder, custodian or consumer to service. Incumbent use jobs and nonpreemptible blocking occupy their real slots. Genuine overlap may avoid adding two concurrent elapsed durations, but it does not merge their CPU, traffic, stock or authority budgets. The source permits a conservative serial certificate and requires a concrete calendar; it does not infer four usable executors, ideal parallelism or foreign queue bounds from an aggregate daily cap.

The conditional transition induction is sound at that boundary: each node of the admitted finite calendar receives its predecessor state, exact guards and supplied resources; its separately bounded primitive outcome establishes the next state before the relevant deadline. A failed primitive-supply premise leaves actual partial state and charges. It is not converted into an unbounded retry, an erased service gap or a successful branch assumed as an input.

## Equal service is not equal internal work

J480 remains a hypothetical 480-target old-mode incidence, not Q's 484-target successor or a realized native corpus. All alternatives compare the same external mathematical/query/publication/service demand while retaining policy-specific build, dirty and scan attempts. RETAIN-C and SG-C explicitly denote chosen catalog-dependent policies, not every legitimate RETAIN or SG implementation.

Old scoped or independently current summaries can survive events that invalidate catalog-dependent summaries. Ordinary unchanged renewals can reuse/rebind valid support; two passes do not force two builds or two full sweeps. SG receives no exclusive catalog credit. These distinctions prevent a smaller bill based on silently imposing extra work on a competitor or weakening the chosen service.

The source also preserves the noninterchangeable outcomes: actual holder-row continuity; current source coverage; exact FIND publication; unfamiliar-reader discovery; native acquisition/check/application; and continuing custody. The survivor continuity theorem does not discharge the others. Their finite jobs and permitted degraded intervals must be separately supplied. The local evaluation cohort is a research/service observation device, not a mandatory network mathematical task queue or human-intention acceptance rule.

## Bounded next-research recommendation

The smallest change to the failed timing premise, without postponing any offered C commit or query, is a qualified residual path with `build + authorization < 70` seconds and a supplied renewal-commit slot before actual expiry. For example, changing the supplied build duration from 60 to 50 while retaining the 15-second residual scan would open authorization at 65. This is a numerical qualification target, not evidence that such a bound is achievable, a whole-resource fit, or a future lease-extension guarantee. Continuing rounds still need their real original-occurrence observations and all current guards.

If complete preparation cannot meet that target, the smallest promising mechanism question is whether unchanged actual anchors can retain current support through a paid, exact change-specific bridge instead of a complete whole-current rebuild for every dependent scan. That would need a new bounded invalidation/currentness argument covering exact postings, actual anchor/native guards, changed rows, retained generations and fallback costs; the present coarse catalog/SG fences do not already permit it. A bridge must keep the same publication and query service and pay its own critical path. Delaying the 70-second commits is not a repair under this fixed offer. These are proposed research choices only, not proved mechanisms or selection recommendations.

## Coordinated replacement review and handoff

After root announced the common held replacement, the reviewer independently verified its **31100-byte** length and SHA-256 `65F68CA344A9BA2C835E01D8585945B7BD1478DC425D4A75F859802BF7F0EA4E`, then reread the entire source. Three changes were checked:

- The numeric per-member CPU division now explicitly requires `k >= 1`. A zero-sweep case must use the undivided reservation test; no service work is manufactured by the threshold.
- The exact timing case now explicitly says that the 15 seconds is residual scan/authorization work after the current catalog becomes READY, with no earlier credited precomputation in this supplied recipe. This closes the possible interpretation ambiguity discussed during review without converting the premise into a universal implementation lower bound. The times 635, 640 and the 640-CPU-second hypothetical-path allowance are unchanged.
- The growing-current-domain claim now starts with distinct selected current locator rows and requires every counted arrival to add at least one new distinct selected current row while all prior counted rows remain selected/current, without pruning, coalescing or replacement. It expressly excludes mere distinct retained submissions/replay objects and restricts the argument to finite admissible prefixes within actual caps. Thus build j genuinely has at least `e0+j` current rows, establishing the sum under its fresh-per-commit premise. This independently confirms that the source repair meets the minimal domain correction in the resource review's JS-RES-001; the resource reviewer owns that finding's final closure, and it is not a second discovery here.

The complete reread found no collateral service regression. Per-policy attempt counts, incumbent slots, actual owner supplies, current authorization versus later commit, complete scans, effect settlement, original-occurrence deadlines and fresh next-round lease premises remain intact. The three changes neither supply missing native measurements nor alter selection or execution authority.

**Final scoped verdict:** no remaining blocking service/deadline finding was identified on the named repaired cut. The envelope supports its conditional finite calendar test and the stated exact-recipe churn counterexample. It still supplies no positive whole-service operating witness, observed native/use success, automatic future funding or sustained-growth theorem. All missing complete resource/primitive/owner supplies remain unqualified. Root owns integration. Reviewer edit authority ends at handoff; later substantive source changes require a new exact cut and affected review.
