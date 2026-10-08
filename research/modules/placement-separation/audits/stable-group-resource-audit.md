# Stable-authority group resource and finite-service audit

Date: 2026-09-20. Reviewer: `stable_group_resource_audit`. Status: **final independent repaired-cut review; R4 and R5 CLOSED; bounded resource/row-continuity argument supported conditionally; candidate UNSELECTED**. The reviewer owns this audit only and has not edited the candidate, executed a model, run Lean or extraction, measured a workload, or allocated protocol identifiers. Initial findings are preserved below; the final source cut and disposition appear in the coordinated repair review.

## Reviewed cut and scope

The complete initial held source was read and its file length/hash independently checked:

| Source | Bytes | SHA-256 |
|---|---:|---|
| [Stable-group candidate](../stable-group-contract.md) | 63002 | `B0BEA1B9E8316DC9BE2E28F8B21C3C4D6433468DB312DEA90D05467A26305B9E` |

The candidate builds on the [architectural contract](../architectural-contract.md), 33728 bytes, SHA-256 `8FFD596DB086647971FB6E42AF5A2E2F38FE7D3FB1658C14DEC3D7686DA25C38`, and [architecture audit](architectural-audit.md), 25513 bytes, SHA-256 `92708433406724338026FDF282531995D8777291A308D7BFA1B822943FD4CFAB`. The relevant inherited mechanics were checked against [F exact groups](../../../../notes/analyses/CP-001F-exact-routing-coverage.md), [G structural retrieval](../../../../notes/analyses/CP-001G-structural-retrieval.md), [G profile bindings](../../../../notes/analyses/CP-001G-profile-and-consumer-bindings.md), the [NET2 integration](../../../../spec/OPERATIONAL-CORPUS-V2.md), its inherited [NET invocation and delivery contract](../../../../spec/OPERATIONAL-CORPUS-V1-NETWORK.md), and the repaired reserve discipline in the [continuation contract](../../reciprocal-operability/continuation-admission-contract.md).

This is a resource/service review, not a second wire-authority audit. It asks whether the specified finite scanner and repair procedure have explicit resource obligations, whether their conditional timing argument is valid, and whether the claimed service is the service actually established. It does not assess measured cost, practical large-network throughput or useful mathematical yield.

The reviewer made three pre-hold observations, relayed through root for author-controlled repair. The source author incorporated them before producing the reviewed cut. They are recorded below as pre-hold closures, not retrospective findings against this exact cut. Root separately raised the replay-clock problem after hold; this reviewer independently confirmed its counterexample. The incomplete classification premise was found in this held-cut review. Independence means separate source review and no source edits; it does not imply that reviewer suggestions never influenced the author's earlier draft.

| Pre-hold observation | Closure verified in the initial held cut |
|---|---|
| R1: count the full traversal | e includes traversed excluded/tombstone records; d counts total dependency visits; b includes repeated reads; added p counts actual posting/index-node visits |
| R2: name the maintained service | The theorem now promises named-holder row/lease continuity, explicitly allowing temporary source current-coverage UNKNOWN and excluding stronger end-to-end service |
| R3: preserve the promised row across old actions | Every admitted old-action outcome must preserve ACTIVE lifecycle and the exact survivor; prior CLOSE/expiry or its removal defeats that original continuity premise |

## Initial disposition

This section records the initial held-cut disposition, before the coordinated repair. Its OPEN statuses are historical and are superseded only by the exact repaired-cut closures at the end of this audit.

The bounded source-accounting and scanner design is supportable at the expressly conditional concept level. The source does not hide native checking inside a metadata scan, treat group cardinality as all-state storage, manufacture budget at recuts, or infer practical scaling from a two-member example.

Two local clarifications are required before endorsing the stated sufficient finite-service theorem:

| Finding | Required repair | Initial status |
|---|---|---|
| R4: replay-send clock substitution | Bind a lease lower bound to the persisted original effectful dispatch occurrence, never a later replay/retransmission send; unavailable time origin gives UNKNOWN | OPEN |
| R5: unknown residual support | Explicitly require a complete supported/definitely-unsupported partition in the simple positive episode, with usable complete support for every retained member; an UNKNOWN branch is not covered by the successful duration theorem | OPEN |

These do not justify weakening the safe failure branches. They tighten the premises under which positive row continuity may be claimed. Even after repair, the profile remains UNSELECTED, without an instantiated large equal-service comparison, qualified primitive cost bounds or operational performance evidence.

## Finite scan and dependency accounting

The repaired pre-hold cardinalities count actual traversal rather than only favorable selected records. The meanings needed for an admitted scan are:

| Quantity | What must be counted | What is not a substitute |
|---|---|---|
| `e` | Every distinct record in the named inventory traversal, including excluded/ineligible/tombstone records traversed | Current selected-target count alone |
| `m` | All actual members of the reconciled group map | Desired or historically observed membership |
| `i` | Total token/posting record visits, including rereads | Distinct emitted tokens |
| `d` | Total assessment/support dependency-record visits for actual required anchors | Only distinct native objects, publisher-declared dependencies or one current guard |
| `p` | Actual physical posting/index-node visits for the supplied traversal/lookups | An index root or an assumed constant-time lookup |
| `b` | Total input bytes read, including repeated anchor-search reads | Unique stored payload bytes |

For a canonical nonempty binary Patricia tree with m leaves, there are m-1 internal branches, hence 2m-1 nodes. An empty map has its one empty representation. The candidate's `2m+1` traversal allowance is therefore a valid loose upper bound under the inherited canonical-map invariant. It is not a substitute for validating that invariant or retaining the signed ad bytes referenced by leaves. Their actual bytes, decoding, signatures and map/history checks remain paid.

One initial inventory traversal visits at most e entry records. The deliberately simple exact-anchor search can then inspect up to e records for each of m members, yielding at most `m*e` entry comparisons. Checking each actual anchor's completed token list costs at most `32m` token comparisons under STRUCT2. This is an ordinary finite algorithm, not an efficient semantic-equivalence search. It may be a poor algorithm at the intended scale.

The selected subset contributes at most 32e distinct emitted-token incidences. That does not bound total visits i after rereads or traversal of retained excluded postings. The held source makes this distinction explicitly. It also counts the repeated m-by-e reads in b unless an independently supplied resident-cache plan pays the necessary RAM and preservation costs. There is no free conversion from repeated disk/table access to comparisons.

The source's schematic work envelope is:

`Wscan <= Wdecode(b) + Wmap(2m+1) + Wentry(e) + Wposting(i,p) + Wdependency(d) + Wcompare(m*e+32m) + Wcommit`.

This is a specification of what conservative supplied cost functions must cover, not a measured runtime theorem. The source separately requires actual decoding, hashing, signatures, reads, dependency inspection, I/O, output/scratch, peak RAM and duration to fit. For example, any transaction-history validation or larger record comparison used by a future implementation must be included in those real functions/inputs; counting only the headline comparisons would fail the supplied envelope. Missing bounds cause non-admission.

The required dependency relation is not inferred from an ad. Reuse of an existing native assessment requires its exact replay/checker/foundation/footprint and current protection/disclosure/incident guards. If a required assessment is missing or dirty, metadata scanning does not silently reconstruct a Lean proof or reacquire its closure. Native rechecking, acquisition, retention and extraction are separately funded operations. An unrelated excluded or dirty entry may be traversed without becoming an anchor and does not invalidate a fully supported surviving member merely by remaining in the inventory. Incoherent inventory structure is a different failure: it prevents establishing the named input cut.

The complete input/guard comparison before summary publication is essential. Visiting the last dependency does not by itself make the result current. A relevant change before the authoritative guarded commit yields STALE_INPUT; partial output remains charged scratch. A valid summary binds actual group root/version and exact anchors, not merely A or the number of rows.

## Classification, cleanup and the second scan

The source correctly pays for two logically different passes in the baseline:

1. Classification of the actual post-settlement map produces supported, unsupported and unknown dispositions, using the current inventory and dependency cut.
2. After actual cleanup, a second authorization scan checks the exact resulting map/root/version before RENEW.

The second pass is not replaced by the planned number of removals. A prior PUT may have changed an ad CID; a DROP may fail or have an unknown outcome. Only actual reconciled membership supplies the second scan's input. Bounds must cover the possible post-settlement size/bytes/dependencies of any already-authorized prior call, not only the last confirmed map.

DROP's asymmetric gate is necessary. If two members are unsupported and only one removal fits each batch, the first DROP must be allowed while the other invalid member still exists. Authentication, ownership, exact expected state, disclosure and paid work authorize deletion; no native support is needed for the removed or other residual members. RENEW remains forbidden until every residual member has current complete support. The same distinction permits retirement without first repairing the theorem being withdrawn.

The held source safely stops when a member's support is unknown. R5 concerns the positive theorem's premise, not this safe state machine. The three-way classification cannot be silently replaced in a proof by a two-way valid/invalid partition.

## R5: complete support partition needed for the positive episode

Counterexample to an unqualified reading of the initial sufficient-duration statement:

1. The actual active map contains `a(x)`, `b(y)` and `c(z)`; the incident definitely withdraws x. b has complete stable support. c's exact native assessment is dirty or absent, while the named inventory itself is coherent.
2. The old action settles on time and preserves all promised survivor rows. All traversed records/bytes and both scan runtimes fit their supplied bounds. There is one definitely invalid member, so the numeric parameter i can be one.
3. Classification returns unsupported a, supported b and UNKNOWN_SUPPORT c. The stated state machine cannot turn this into the stipulated complete cleanup-and-renewal path. It yields nondecision or requires separately funded revalidation/replanning.

Stable support for b and bounded scan time do not establish current support for c. A scan that returns UNKNOWN may finish within its duration bound. It follows that `L < safe margin` alone, together with one supported survivor and i known invalid members, is not sufficient for a successful renewal.

Repair the simple positive premise by requiring every possible admitted actual post-settlement member to lie in an exhaustive known partition: definitely unsupported members in the exact i-member removal plan, or retained members with complete usable current anchor assessments/dependencies. No residual unknown membership/support may remain in this particular episode. This is an independently falsifiable input/readiness premise. It must not say merely that the scanner or entire repair succeeds. Ordinary cases with unknown support remain safe failures or separately admitted larger episodes, with their additional work/deadlines.

## Outstanding actions, work conservation and retained state

The source lane is stronger than one call per returned groupID: it is keyed by `(holder,p,F,E,A)` and includes OPEN before a groupID exists. This prevents an uncertain opening from being hidden under a second tentative generation or used as a supposedly harmless status read. The strict service recipe has at most one unresolved effectful operation in that lane. It does not create an extra effectful call to force a convenient observation.

Effect settlement and accounting settlement are correctly distinct. Coherent exact retained lineage may establish that an operation committed, releasing the serialization lane, while original outcome, delivery and reservation liabilities remain. Unknown timeout does not release the lane. Invocation replay returns inherited metadata under paid control bounds, not a new execution or unlimited result-body fetch. A delayed result settles its own historical occurrence; it cannot overwrite a higher current version or newer incident fence.

For cumulative work, the candidate uses the repaired continuation inequality:

`alreadySpent + unspentIncumbentReserve + unspentRepairReserve + unspentOptionalReserve <= currentGrant`.

Its terms are disjoint residual authority, not repeated copies of the entire admitted plans. If a realized prefix consumes x within a reserved bound, x moves from the corresponding unspent reserve to spent authority; it is not simultaneously retained in both terms. Unknown outcomes retain conservative charges instead of restoring capacity. Aftercare is assigned to its named disjoint reserve rather than counted again under incumbents. A new observation or stock recut does not renew the grant.

The separate stock test is:

`currentChargedStock + repairPeakOverlap <= actualStockCap`.

It must hold componentwise at each actual source/holder, including metadata, physical bytes, RAM and concurrent live records. A source's admitted work does not confer capacity on a holder. Planned deletions contribute zero release credit. A completed local release barrier permits remeasurement, not subtraction of the same release twice. Foreign CLOSE/expiry is a service gate, not an acknowledgment of foreign physical reclamation.

At-most-one ACTIVE group is not an all-state bound. Empty active groups, opening reservations, uncertain effects, closed/expired unreclaimed generations, old maps, snapshots, retained outcomes, repair cursors and overlapping old-mode migration state remain charged. OWNER_RELEASE_REQUIRED native custody is independent of routing lease expiry. The candidate preserves these distinctions.

Identification also consumes resources. A coarse provider fence is cheap to advance, but enumeration of its affected groups and subsequent support repair is priced by Qidentify and the actual finite group list. Full repair capacity cannot block authoritative invalidation; instead it withdraws the corresponding availability promise and exposes degradation. This is safe bounded overload, not successful repair.

## Encoded batching and operation counts

Every cleanup batch must satisfy both inherited limits: at most 64 mutations and 64 KiB for the whole control body, including the new header. Consequently `ceil((u+v)/64)` is only a mutation-count lower bound on the number of batches. It is not a safe cost reservation without actual encoded bytes.

The singleton fallback is conservative only after every complete singleton request is known to fit the candidate binding. If one cannot fit, that action is unsupported; there is no hidden larger message channel. Once this condition and the actual per-call admission constraints hold, i invalid members can be removed with at most i singleton DROP calls, followed by one RENEW. The `i+1` count covers only those new group mutations/renewal. It excludes old settlement/control/delivery work, scan jobs, lookups, native checks, record creation, and aftercare. The source labels that exclusion correctly.

Actual byte-time extension for RENEW follows F: it is not a full free reallocation, and replay does not extend it. Counter headroom is also a real admission constraint. A plan that fits bytes/calls but cannot perform its old-effect increment, cleanup transitions and renewal without stateVersion exhaustion is not admitted.

## Lease lower bound and R4

For a continuous source monotonic time origin, let c be the source-time coordinate of the holder's relevant lease observation/commit, and let `Lremaining` be the holder-local duration remaining at that observation. Under the supplied relative-rate assumption, expiration occurs no earlier in source time than

`c + Lremaining/(1+rho)`.

If s0 is the original effectful dispatch time of that exact admitted occurrence, causal execution gives `c >= s0`. Hence

`deadlineLowerBound = s0 + Lremaining/(1+rho)`

is conservative. Current remaining safe margin subtracts the actual current source time from this bound, so delivery delay consumes margin. The result is not a synchronized global expiration timestamp and cannot survive an unknown source/holder clock discontinuity by guesswork.

The initial held wording says that the exact call was sent at s and its commit cannot precede its send. NET2 permits retransmission/replay of that same invocation identity. Suppose the operation was first sent at s0, committed at c, and its retained result is replayed following a much later send s1, with `s0 <= c < s1`. The old commit-boundary remaining duration does not restart at s1. Substituting s1 into the formula overstates the lower bound by an unearned amount. An authenticated exact call/result binding alone does not distinguish original execution from later replay delivery.

R4 therefore requires retaining the original occurrence-bound effectful dispatch time, or another established earlier lower bound on that dispatch, with the necessary monotonic-origin continuity. Retransmission, replay, later response receipt and renewed local observation cannot refresh it. If no such coherent record survives, no positive deadline lower bound is available through this recipe. A genuinely new admitted RENEW supplies its own occurrence and observation; it is not a replay of the earlier one.

This finding originated in root's held-cut review and was independently tested here. Its repair is a necessary binding clarification, not a need for globally synchronized clocks.

## Conditional serial service argument

Subject to R4/R5 repair, the simple finite theorem has a valid dependency-ordered proof. Its necessary premises include:

- Coherent actual group/history inputs and sufficient supplied resource/counter/calendar admission at source and holder.
- At most one old unresolved effect, settling within its declared bound; every allowed old outcome preserves the ACTIVE lifecycle and each row promised from the incident cut, including its original conservative lease margin.
- A complete known unsupported/retained-supported partition after settlement, with complete coherent support inputs and no additional relevant guard edit in this simple episode.
- Conforming authenticated holder transitions, admitted successful-operation prerequisites, available primitive execution/delivery slots, and the independently supplied duration bounds.
- A safe deadline derived from the actual original observation occurrence and continuous clocks, not a later replay.

Let W be zero or one, s bound old-effect settlement, S bound each complete classification/authorization scan for all supplied post-settlement inputs, i be the known invalid removal count, d bound each singleton cleanup operation including its required settlement, r bound the new renewal path, and l bound identification/local commits/rebinding. Then the serial slot list is bounded by

`Lepisode = W*s + 2*S + i*d + r + l`.

The first prefix settles the only prior effect without losing a designated survivor. The complete classification identifies exactly the removal set from the actual map. Each authenticated DROP removes only its named invalid row; it preserves every promised survivor and yields the next exact expected state. The second complete scan establishes support for the actual residual map. Current guard checks authorize RENEW, whose exact transition preserves membership and extends the actual lease. The guarded result rebind cannot override an intervening incident. With `Lepisode` strictly below the old safe margin and no additional invalidation in this episode, all these transitions precede the old-service expiry bound.

This argument derives the compound cleanup/renewal result from exact transition rules and bounded primitive supplies. It does not require that the entire repair outcome be assumed. A responding primitive which refuses admission or loses its outcome is not the promised supplied primitive service; that is an independently observable failed premise, not an automatically successful retry.

The original-row preservation premise is essential. A prior CLOSE or a prior DROP of a promised survivor can finish promptly while making original row continuity impossible. The held source now explicitly excludes those outcomes for the positive claim. A smaller claim admitted after settlement cannot backdate continuity through the loss.

For Q frozen groups in the actual reserved deadline/age order, let `Pj = sum_(k<=j) Lk` include every predecessor in that serial calendar. Group j needs a safe margin strictly greater than Pj at the common admission cut. Induction over the slots gives each admitted completion before its own bound. `Q*max Lk` is a sufficient common margin, not a tight optimum. Incumbent use of the same executors must be included in the actual slot list. Aggregate CPU or call totals do not establish these deadlines; new arrivals cannot reset original ages or steal reserved slots.

The service object is only the survivor's exact row and containing lease at the named holder without an expiry gap. The coarse source fence can make its current coverage assertion UNKNOWN during repair. Neither this theorem nor the two-member trace establishes continuous native/public service, query completion, all-copy routing coverage, marker availability, reader reachability or continuing useful growth.

## Positive and defeating traces

The source's positive two-member trace is a legitimate small conditional witness. At `(version 8,R0)`, a prior eligible renewal is claimed. The incident withdraws a's support and dirties the source fence. Its old renewal settles at `(9,R0)` within the original margin. A complete classification finds a unsupported and b supported. DROP of a commits `(10,R1)` containing only b. A second paid scan of R1 and current guards authorizes renewal, giving `(11,R1)`. Throughout the remote sequence b retains its row/owner; a new current borrower assertion waits for the paid rebind. Old layouts, results, rows and custody state keep their real charges. No new native mathematical theorem is established by the symbols a/b.

The six one-unit slots versus a seven-unit margin are expressly a symbolic supplied fixture. They are not seconds, measured hardware capacity, a large-network workload or an adopted operating envelope. The general inequalities determine whether any real case can be supplied.

The most direct defeating trace keeps the same maps and resources but delays settlement of the prior effect beyond b's safe margin. The lane cannot fabricate cancellation or dispatch a second effectful call as a free observation. It must expose loss of the row-continuity promise. Later repair cannot retroactively erase the gap. Exceeding d/b/e or the m-by-e work bound similarly gives nondecision despite b being mathematically valid. These failures are not refutations of the conditional theorem once their premises are stated; they are reasons an operating workload may fail admission or service.

R4's replay-timestamp trace and R5's third unknown-support member test different omitted premises. They cannot be repaired merely by adding more favorable two-member examples.

## Efficiency and adoption remain open

The no-remote-compaction proposition removes one class of ownership mutations. It does not establish net savings or sustained growth. In particular the baseline coarse support fence is invalidated by selected-entry additions. If G dispersed groups each independently scan e inventory records, entry work can be proportional to `G*e`, before their member-anchor comparisons, dependency checks and I/O. The simple local organization may therefore replace migration traffic with a larger support-authorization burden.

A later equal-service comparison must use the same selected targets/keys, real holder incidence, initial/adoption duties, incidents, native/custody obligations, new arrivals, copy/path service and primitive supplies. It must report actual dirty intervals and declined work. Source current-coverage nondecision cannot be silently compared with continuous full service in the old profile. With widely dispersed holders, neither stable namespace identity nor group consolidation implies fewer renewal calls. Pure compaction also retains local preservation checks, old/new layout peaks and historical readers.

The conditional scanner/service contract is a prerequisite to that comparison, not its substitute. This review recommends completing the two bounded repairs, then comparing real finite supplied workloads before selecting the profile. It does not recommend another tiny favorable fixture as proof of practical network operability. No numerical wire allocation, implementation/execution permission, native qualification, measured throughput, usefulness finding or goal completion follows from this audit.

## Coordinated repair review

Root coordinated a single source-author repair after the complete initial resource and authority audits were available. The reviewer then read the entire repaired source, not just excerpts of the reported changes, and independently reconfirmed its bytes/hash:

| Repaired source | Bytes | SHA-256 |
|---|---:|---|
| [Complete stable-group candidate](../stable-group-contract.md) | 68458 | `EA9398969D640BDE89271E53274B4F0071D00436659F5BF8D03FC266AD250779` |

The initial resource-audit handoff was 26007 bytes, SHA-256 `EAC5E75EC41A7CA803122D48773CDFE54AFF146C7DFCA2BEEE3E21E38370A864`. This final audit preserves its initial counterexamples and reviewer provenance while appending the actual repair disposition. The candidate source, frozen architecture, prior checkpoints and registries were not edited by this reviewer.

### R4 closure: original invocation-bound clock basis

The repaired action inventory retains the exact original invocation occurrence, call commitment, dispatch-or-proven-earlier timestamp and monotonic-origin identity. The group inventory links each historical remaining-duration observation to that basis. Before an effectful dispatch escapes, the basis must already be retained. The deadline paragraph expressly forbids replacing it with a retransmission/replay send or later response-receive time. Fresh invocations with identical arguments are distinct occurrences and cannot borrow each other's observation.

The rate and continuity premises cover the relevant elapsed interval. Missing occurrence history, uncertain original time basis, discontinuous monotonic origin or unknown rate yields UNKNOWN_DEADLINE. A genuine fresh renewal may establish a new bound; replay cannot. These rules supply the missing causal premise `original commit time >= s0` in the lower-bound proof without introducing a global clock or an unbounded history store. The timestamp/occurrence records remain in the existing finite charged action inventory.

The source also includes an explicit equal-rate counterexample: original dispatch at 0, commit at 1 with ten units remaining, replay at 20. Actual expiry is 11; the conservative original-send lower bound is 10 and already past. The forbidden replay substitution would yield 30. This demonstrates both why the original rule was insufficiently explicit and why the repaired rule does not infer fresh service from a historical result.

**R4 CLOSED.** Root-origin finding, independently confirmed and now independently closed on the exact repaired cut.

### R5 closure: exhaustive known support for the retained map

The repaired simple theorem explicitly requires `Mpost = Keep disjoint-union Remove` for the actual coherent post-settlement membership. Every Keep member has complete current support for its exact ad/anchor and guards. Every Remove member is definitely unsupported and has owner-authorized routing removal. The promised incident-cut survivors belong to Keep. No actual member is omitted; the simple episode contains no UNKNOWN_SUPPORT member.

It defines `i = |Remove|`, requires the second complete scan to establish support for every actual member of the resulting exact Keep map, and states that finishing within the scan duration is not alone sufficient. Complete named inputs, stable guards, bounded conforming scanner work and exact cleanup transitions justify the successful path. This is not an assumption that the entire repair succeeded: the input support relation and primitive supplies can be separately inspected or falsified, and the algorithm must still classify, remove and revalidate the actual map.

An unknown member now explicitly leaves this theorem's scope. Native revalidation or a distinct owner-authorized conservative removal plan needs its own costs, remaining-membership specification and deadline; unknown is not mathematical falsehood and is not silently added to i. The new supported-b/unknown-c trace makes the failure concrete even when there are zero definitely unsupported members and both scans could finish quickly.

**R5 CLOSED.** The resource review's held-cut finding is repaired without weakening UNKNOWN failure, native independence or the all-member RENEW support gate.

### Affected bindings, costs and regression checks

The repair also addresses the authority review's SG-A1 negotiation finding. The source now states that existing HELLO_REPLY has capability codes, not a BindingID field. A future installed dedicated capability maps immutably to exactly one BindingID/codec/limit vector; calls/results check their explicit binding against that installed mapping. Remote manifests do not install codecs or change limits. The existing bounded capability list remains, and a new binding revision needs its own explicit allocation. This reviewer found no new resource or timing contradiction from that repair; the independent [authority audit](stable-group-authority-audit.md) owns its authority disposition. No new handshake field or resource-free negotiation service is inferred here.

The complete reread reconfirmed the following unchanged boundaries:

- Full traversal cardinalities, physical posting visits, repeated read bytes, m-by-e anchor search, complete native dependency guards and the second paid authorization scan remain explicit.
- DROP remains possible without revalidating invalid residual members; RENEW still needs all actual members supported. Required native revalidation is not hidden in scan timing.
- The one unresolved effectful lane includes OPEN, retains uncertainty and does not use an extra effectful observation call as free settlement. Delayed results preserve exact transition lineage and newer incident fences.
- Disjoint residual reserves, all-state peak storage, aftercare, no hypothetical release credit, per-holder admission and custody independence remain unchanged. Original-dispatch records add actual charged state, not new funding.
- The simple L formula still prices one old settlement, two complete scans, i singleton removals, one renewal and local work. Every singleton must fit the full encoded control ceiling. Counter and original-survivor preservation conditions remain.
- Multiple groups still need actual reserved deadline-prefix calendars. The theorem still concerns named-holder row/lease continuity, allowing temporary current-source coverage nondecision.
- Large equal-service/adoption comparison, supplied numerical primitive bounds and the potentially dominant `G*e` support-invalidation cost remain openly unresolved. The small symbolic trace is not promoted to practical throughput or sustained knowledge growth.

### Final scoped verdict

**R1-R3 remain closed from pre-hold review; R4-R5 are CLOSED on the 68458-byte repaired cut. No remaining resource/service contradiction was found within the stated conditional finite procedure.** The complete scanner, joint accounting obligations and finite named-holder survivor-row continuity argument are supported as a concept specification under their explicit independently supplied input, service, clock, storage and timing premises.

This is not an instantiated operating qualification. The candidate remains **UNSELECTED and NOT OPERABILITY-QUALIFIED**. It supplies no measured primitive bounds, large continuing-workload comparison, empirical efficiency, native execution evidence, useful-growth result or goal completion. Its next justified use is as a precisely bounded candidate in an equal-service resource/adoption comparison, not as permission to claim the intended global system already works efficiently.
