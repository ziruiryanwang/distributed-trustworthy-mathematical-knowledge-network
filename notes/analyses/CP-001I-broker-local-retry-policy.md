# CP-001I proposal: bounded owner-local retry and suppression

Date: 2026-09-20. Status: illustrative heuristic module under independent audit, not a selected release default, wire extension or executed result. No implementation, scheduler, background job, native replay, test or benchmark. Frozen H and earlier artifacts remain unchanged.

## Question and boundary

An untrusted candidate can waste work repeatedly; suppressing every failure forever can instead hide a useful result after a temporary source outage. Select a small **local** policy that distinguishes those cases, bounds total work and makes temporary suppression expire under stated conditions.

This module runs only when an owner-authorized investigator is already making an admitted candidate visit. It installs no timer, wake-up, scheduled task, remote callback, mandatory research goal or public task registry. An investigator may stop at any time. A returned next-eligible time is information for the local caller, not authority to arrange future execution.

Dependencies are the proposed [BROKER1 same-replay lead grammar](CP-001I-untrusted-search-brokers.md), the [receiving trust boundary](CP-001I-candidate-service-trust-boundary.md), and the unchanged NET2 acquisition, local recovery, native checking and current-use contracts. This module does not choose another proof, change a foundation, relax policy or grant a read scope. All policy constants below are adjustable local engineering choices; their cost or utility is not claimed optimal.

The [direct broker service](CP-001I-direct-broker-bindings.md) is an upstream metadata stage, not a PUBLIC_NATIVE source trial. Its mutation acknowledgments, STALE_CURSOR, PARTIAL, NOT_SERVABLE or UNSUPPORTED_PROFILE cannot update native-source buckets merely because a broker and source share a NodeID. Received candidate bytes may survive snapshot expiry under their actual local retention; they carry no surviving broker or native read authority. A new broker query keeps the same already-spent client account and applicable native failure history. Broker pages, source trials and native checking all draw from the actual encompassing investigation allocation; this module's eight-call tranche is not additional funding for those other stages.

## Input and output contract

One visit receives an already bounded candidate descriptor d naming exact foundation F, semantic target t and replay R, with one to four canonically ordered distinct source identities and same-R public-native leads. It also receives the caller's exact local investigation account, current policy/disclosure guards and admitted resource vector.

The visit returns exactly one of:

- **TRY_ONE:** a local one-shot reservation ticket for one currently eligible exact source lead and bounded acquisition tranche under the existing account. The visit is a planner: it has not dispatched that trial.
- **DEFER_UNTIL:** no source trial now; stated transient cooldowns prevent it, with the earliest meaningful issuer-local eligibility time.
- **NEEDS_NEW_ADMISSION:** resource or policy/adoption/disclosure conditions prevent this action; no new authority is inferred.
- **EXACT_CANDIDATE_SUPPRESSED:** a retained complete native/codec rejection applies to this exact unchanged checking input.
- **NO_USABLE_LEAD:** the current bounded lead set is absent or fails its required grammar/connection policy; the result is not theorem falsity.

All outcomes consume the actual local inspection/accounting work. They neither prove availability nor guarantee that a trial will complete. Successful native acquisition, acceptance and application remain separate downstream events.

The ordinary owner-local acquisition caller is the sole dispatcher. TRY_ONE is neither a second work instruction after execution nor a network capability. It must consume the exact ticket through the transition below before creating any source invocation.

## Finite episode and cache envelope

An *episode* is one existing owner-admitted local investigation account, not a network object or autonomous job. Before it can initiate work, it must have finite actual byte, CPU, memory, staging, call and elapsed-time allocations. Counts below supplement those allocations; they do not supply them.

An illustrative envelope is:

| Quantity | Aggregate episode or cache limit |
|---|---:|
| Candidate visits in an episode | 32 |
| Lead records inspected by this module | 128 |
| Source trials initiated | 32 total across all candidates and sources |
| Concurrent source trials | 1 |
| Existing service calls in one acquisition tranche | At most 8, also charged to the episode's total call/byte/CPU allocations |
| Episode elapsed-time horizon | At most 2 issuer-local hours, with actual shorter inherited deadlines prevailing |
| All retained retry, failure and cursor records | 1024 records total across candidates, sources and failure classes |
| Retry/cache resident bytes, including indexes and retained diagnostics | 512 KiB total |

A record has at most 512 canonical local bytes, and actual resident-byte admission can stop earlier. Store compact exact bindings and bounded reason data, not complete proof bodies, remote error logs or arbitrary endpoint histories. References to existing receiver-owned context objects do not make their retention free; if the matching context can no longer be established, the cached observation cannot apply as an exact rejection. A parent acquisition stage may admit different larger finite allocations, but a broker result or an exhausted tranche cannot grant them. All variants, source trials, retries and failed negotiations debit the same actual account.

Reserve and durably charge a source-trial token before creating its work. An uncertain or lost reply does not refund that token or create a new invocation identity. Unused byte reservations may be released only through the inherited exact local accounting rules; such release does not manufacture another trial token. Partial verified objects remain in their separately charged staging/retention scope and can be reused only under its actual guards.

The retry cache is not the spending ledger. Evicting, expiring or clearing a cache entry cannot erase episode expenditure or recreate expired invocation authority. Remote arrival volume and new source keys cannot replenish any limit. In-flight reservations and necessary reconciliation state remain counted and cannot be evicted merely to free another work slot.

## Failure classes and exact cache keys

Use receiver-owned exact tuples, not a negative bit attached only to a theorem statement. Equality of a hashed implementation key must still mean equality of its relevant exact tuple under the inherited binding assumptions. A cache record is local scheduling evidence, never a portable mathematical verdict.

| Observation class | Scope of the retained observation | Policy |
|---|---|---|
| UNAVAILABLE | F, R, source identity and transport/service role; actual failed connection/negotiation/timeout observation | Temporary source cooldown; a new endpoint string alone does not reset it |
| NOT_SERVABLE | Same source/replay role, exact attempted public or holder-bound scope and observed refusal/nonavailability | Temporary cooldown; no inference that another source or scope cannot serve R |
| CORRUPT_RESPONSE | Exact source, F/R, call/requested CID/range and failed byte/range/integrity observation | Stronger temporary cooldown for that source/replay; do not mark the unseen mathematical content or every source invalid |
| EXACT_CODEC_REJECT | Hash-correct exact typed object bytes and the selected codec/profile interpretation | Suppress that exact unchanged invalid object while the record is retained; not a target-wide failure |
| EXACT_NATIVE_REJECT | Exact F/R and expected target, actual complete realization/check inputs, qualified checker/rule interpretation and completed mismatch | Suppress that exact unchanged completed checking case while retained; other proof instances/realizations are separate candidates |
| RESOURCE_NONDECISION | Exact stage/candidate, spent or insufficient allocation generation and actually retained progress generation | Do not classify as invalid. A further trial needs separately sufficient still-live admission and compatible retained progress |
| POLICY_INCOMPATIBLE | Exact action/candidate and relevant local foundation, axiom, disclosure or current-use policy guard | Re-evaluate only under the actual applicable guards; expiry cannot grant policy permission |

An unsupported profile is not a native mismatch. An interrupted, timed-out, crashed or allocation-exhausted checker did not produce EXACT_NATIVE_REJECT. A returned payload whose hash fails is CORRUPT_RESPONSE, not evidence that the requested CID itself encodes malformed data. Completed checking must also bind the expected target: a valid different result is not acceptance of the requested one.

The exact rejection classes do not receive automatic time-driven native rechecks. Identical immutable invalid bytes do not improve merely by waiting. A changed relevant checker qualification, actual realization, object/replay identity or expected target gives a different case; an explicit owner-admitted diagnostic recheck is also possible. Neither path relaxes acceptance. Cache eviction may cause a later ordinary check to rediscover the same failure, but that work still needs ordinary funding. No theorem-wide or network-wide blacklist is introduced.

## Observation identity, retry obligations and applicability

Separate three identities. An immutable **observation** binds the local episode generation, trial ticket, actual invocation and result identity, F/R/source/role, actual stage, requested data and scope, and qualified clock observation. A **retry obligation** describes the attempted action across distinct invocations. A **bucket key** is `(transientClass,F,R,sourceNodeID,role,obligation)`. Neither an invocation ID, endpoint string nor broker snapshot is in this stable key. No broader source-wide aggregate is selected here.

Use these precise obligation forms:

| Class | Stable obligation | Successful discharge |
|---|---|---|
| UNAVAILABLE | Connection; or negotiation with the exact requested capability/profile tuple; or an exact later operation/data/scope request, with its distinct failed stage | Success at that same stage/obligation; a connection success does not clear a later-read timeout |
| NOT_SERVABLE | Exact operation/requested data and actual attempted public or holder-bound scope identity plus authorization generation | Verified successful service of that obligation under that scope; new scope negotiation is a different obligation |
| CORRUPT_RESPONSE | Operation kind and exact requested typed CID/range or equivalent exact expected integrity-bound response; not the unique invocation ID | Obtaining and independently validating that exact data/response, possibly within a complete acquisition that includes it |

A corruption obligation does not vary merely because a read token or endpoint changed: integrity of the same expected bytes remains the obligation. A refusal or scoped service-timeout does vary with actual scope. Connection/negotiation keys bind the requested semantics, not nonce/session identities. If a request is not expressible by an exact bounded retained context, stop or omit this optional suppression record; never approximate it into a stronger rejection. All referenced contexts and indexes are charged.

Define `Applies(k,a,context)` only when the bucket's F/R/source/role agree and its stable obligation is an actual obligation in the proposed next bounded action plan `a`. A cached old-scope refusal does not apply to fresh negotiation or a genuinely different authorized scope. An unknown future scope is not invented to match or evade a bucket. After negotiation supplies an actual scope or the plan learns a new exact object/range, recheck applicable buckets and current policy before that stage under the same ticket and remaining tranche. It may stop there without further source work. This intentionally does not provide a source-wide anti-Sybil or rate-control guarantee; parent admission caps still apply.

Each bucket retains one exact obligation, a saturating count, deadline/origin, and bounded latest-observation binding, not an unbounded failure history. New exact invocation failures map to the same bucket when these stable fields match. A successful discharge deletes only matching buckets; unrelated success deletes none. Deletion permits a subsequent genuinely new failure to start at one. Deadline expiry alone does not delete or reset the count. Every observation, ticket, bucket, cursor, reference and necessary settlement fence counts within the 1024-record/512-KiB allocation (and its parent accounting allocation); inability to retain it cannot create uncharged state.

## Temporary suppression rule

Maintain a saturating failure count n from 1 through 8 for each stable transient bucket just defined. On the first exactly settled failure in an absent bucket set n=1; on each later distinct settled failure increment it, up to 8. Repeated delivery of one observation never increments it. Set its duration to

\[
\tau_c(n)=\min(3600\text{ seconds},\;b_c\,2^{n-1}),
\]

where the illustrative bases are 30 seconds for UNAVAILABLE, 120 seconds for NOT_SERVABLE and 300 seconds for CORRUPT_RESPONSE. The count saturates at 8. Set `notBefore` using the receiving owner's qualified monotonic clock, not a broker/source timestamp. These are heuristic load controls, not estimates of recovery probability or proofs of culpability.

A lead is transiently eligible only when every applicable retained cooldown has elapsed. Source-identity/replay binding prevents an endpoint-only edit from resetting its cooldown; all endpoint addresses still pass current connection/disclosure policy. A genuinely new source identity may be considered separately, but remains within the four-lead and global work/cache caps. This policy does not claim Sybil resistance.

A successful response clears only the failure obligation it actually discharges. A successful connection can clear the corresponding connection-failure record. A verified successful response for the previously refused exact read can clear its refusal record. Corruption is cleared only by obtaining and validating the affected exact requested data or by the independently completed selected acquisition that includes it; an unrelated good header is insufficient. Ordinary passage of time restores retry eligibility without asserting the source has recovered. Success never resets episode expenditure.

On a distinct newly settled failure, the corresponding counter increments and a new bounded cooldown starts at the recorded local settlement tick. Replaying that observation does not move the tick. A peer cannot extend a cooldown by merely sending an unsolicited failure claim; the local record requires an actually admitted attempt and its actual observation. Other candidates/sources do not inherit a failure just because they share a token or theorem statement.

## One-visit selection rule

Keep a bounded per-candidate circular cursor over the current sorted source identities. The cursor is local scheduling state, not a preference embedded in the mathematical artifact.

1. Charge the visit and inspect candidate-wide profile/policy and exact rejection/resource guards. A source/scope-specific refusal is not a candidate-wide native rejection. On an actual candidate-wide failure, return the scoped outcome above without starting source work.
2. Inspect at most the candidate's four current leads, charging each inspection. Begin strictly after the last selected source identity in canonical circular order. A missing prior identity acts as an ordinary ordering boundary; lead additions do not reset the cursor to the smallest key.
3. Select the first lead whose planned action passes grammar, connection/disclosure policy, applicable transient deadlines and actual funding conditions. Atomically reserve/charge its complete finite tranche and trial token, create one local ticket and advance the cursor. Advance at reservation, not success, so one failing source does not monopolize visits. A reserved but never dispatched trial remains charged against the 32-trial ceiling.
4. Return TRY_ONE with that ticket. Perform no source trial inside the planning visit. The sole acquisition caller may dispatch at most one trial by the one-shot transition below. Negotiated role, actual public scope or fresh holder-bound export, exact R, item/range checks and native staging follow the ordinary contracts. A different replay is another candidate, never a silent substitution.
5. If none can be selected, compute the scoped result by the next paragraph. Do not register a callback, sleep until its time, create a new account, or schedule another visit.

Let L be the at-most-four current lead/action plans passing nontransient grammar, current policy and actually reservable funding guards. For each l in L let `T(l)=max(now, all notBefore values with Applies(k,l,currentContext))`; the empty maximum is now. If L is nonempty, the earliest transient eligibility is `T*=min(T(l):l in L)`. Return DEFER_UNTIL only when every such plan is cooling down and T* lies before a still-live admission horizon permitting that action. If the horizon or known deadline/resource condition prevents it, return NEEDS_NEW_ADMISSION with that reason; the time may be diagnostic but is not sufficient authority. If L is empty, return NEEDS_NEW_ADMISSION for actual policy/funding barriers, or NO_USABLE_LEAD if no lead passes grammar/connection policy. Retain bounded per-lead reasons when causes differ. No timestamp asserts that currently allowed guards or resources will still hold then.

## One-shot ticket and outcome settlement

A ticket binds its unique local identity, episode/admission generation, exact candidate/F/R/source/role, planned action, reserved tranche and horizon, actual guards and cursor transition. Its owner-controlled state is RESERVED, CONSUMED, SETTLED or FENCED_UNKNOWN. Only the ordinary acquisition caller can atomically move RESERVED to CONSUMED after revalidating current guards and remaining allocation. It durably records this transition before creating the trial's invocation identities. Duplicate ticket delivery cannot create another trial; uncertain prior consumption is fenced/reconciled, not assumed unused. Rejected revalidation terminalizes the reservation without restoring its trial count.

Only that consumed trial may allocate its at-most-eight distinct existing-service invocations, all inside the same parent call/resource budget. Before each new stage, revalidate actual scope, applies-to-plan cooldowns, policy and remaining resources. One trial is in flight at a time; an unresolved consumed ticket occupies that slot. No new ticket can hide its uncertain work by evicting the retry cache.

Settlement atomically records the exact locally observed completion identity in the bounded durable work ledger and applies its bucket increment or discharge at most once. Duplicate completion delivery reads that prior settlement; it neither increments n nor rebases time. A crash between recording and cache update requires atomic recovery/reconciliation, not replaying an unfenced counter update. If a bucket was evicted after settlement, replay of the old observation cannot reconstruct it as a new failure. Necessary deduplication/fence records are retained until all possible deliveries of that ticket are retired under the inherited account/epoch recovery rules. Later foreign or retired observations are ignored as scheduling input, not accepted as new attempts.

Settlement/recovery storage and work are reserved before dispatch. If they cannot be supplied, no ticket is admitted. A hard interruption can leave FENCED_UNKNOWN and a resource nondecision; it does not grant a new source call. No completion schedules another visit, resets episode spending or proves a mathematical judgment.

Lead churn, another candidate chosen by the investigator, snapshot expiry and source refusal can still prevent useful progress. Changing broker snapshots does not erase source/replay failure keys. Changing the evidence alternative creates a separate exact checking case, but does not create additional investigation funding.

## Clock, restart and uncertain-state discipline

Every deadline binds its monotonic clock origin/generation. Under a continuously valid origin, use its actual elapsed ticks. Wall-clock corrections, remote timestamps and copied broker metadata cannot accelerate cooldown expiry or refresh episode authority.

After a restart with a demonstrably continuous qualified clock and intact retained state, the original deadlines may be compared as usual. Otherwise, rebase each retained transient cooldown to the new current monotonic time plus its stored capped duration, at most one hour. This conservatively restarts suppression; it does not pretend to know elapsed downtime. Repeated clock-origin changes can postpone eligibility indefinitely, so the progress statement below expressly requires a sufficiently long stable origin.

Old running work, uncertain calls, export/cursor leases and episode budgets retain the inherited recovery fences. An episode whose spending/deadline continuity cannot be established does not resume spending: it is terminalized or reconciled under that contract. A fresh owner-admitted account is distinct authority, not a consequence of restart or cache loss. Old exact rejection records can apply only if their complete interpretation/check-input guards still match; uncertain or incomplete records become unknown scheduling data, not stronger negative verdicts.

When the cache is full, admit no additional uncharged state. Settled records may be evicted by a bounded local recency policy; do not evict necessary in-flight/recovery state. Eviction loses suppression/cursor history, not mathematical evidence or accounting history. A receiver can choose to stop rather than spend work reconstructing evicted state. The fairness statement therefore requires the relevant cursor/records to remain retained.

## Conditional claims and minimal countercases

**Finite-work claim.** Within one episode, no transcript can cause more than 32 admitted visits, 128 lead inspections or 32 initiated trials through this module, and all actually executed work also fits its admitted resource/deadline vector. Asking for admission after exhaustion creates no further admitted visit; the caller's own dispatch/refusal handling still needs its parent resource allocation and is not claimed costless. The argument is induction over local admission: every transition consumes a previously reserved finite counter/allocation; no response, expiration, cache eviction or restart replenishes it. This relies on the inherited durable single-owner accounting/recovery assumptions.

**Bounded transient eligibility.** Fix a retained lead, relevant fixed guards and a clock origin that stays valid. After its last actual transient failure or conservative restart rebase, every applicable cooldown expires within one hour if no new actual failure/rebase occurs. Therefore transient suppression alone cannot prevent eligibility at visits after that time. This is not a timer-triggered retry, source-availability guarantee, sufficient native budget or policy permission.

**Conditional within-candidate fairness.** Suppose a candidate keeps a fixed lead set of size m at most four and its cursor remains retained. If a particular lead stays eligible, the investigator continues to admit visits/trials of that candidate, and no common policy/resource barrier prevents selection, that lead is selected within at most m subsequent source selections. The circular cursor cannot pass a persistently eligible lead without selecting it. No fairness across investigators, candidates, arbitrary lead churn or stopped investigations is claimed.

Minimal countercases define the limits:

- A temporary timeout cached permanently at JudgmentID would suppress a later healthy source or alternate proof. Exact transient keys and bounded deadlines prevent that strengthening.
- A valid header followed by corrupt dependency bytes would repeatedly erase failure history if every success cleared every class. Obligation-specific clearing prevents that reset.
- Resetting all budgets after an expired entry, new broker snapshot or crash permits unlimited work. The separate persistent account and recovery fence forbid it.
- A complete native mismatch for one realization does not rule out a new checked repair or another exact replay. Its rejection key cannot suppress those different cases.
- A resource stop followed by the same insufficient grant is not useful recovery. Progress requires sufficient remaining or freshly admitted resources; this policy does not manufacture them.
- A reboot every few minutes, cache thrashing or permanent policy refusal can prevent retries. Those executions violate the stated stable-clock/retention/eligibility premises; the policy must report the actual barrier rather than claim eventual success.

## Concept exit and remaining evidence

The proposed module closes one narrow question: finite local work and class-correct suppression can coexist with bounded transient eligibility and conditional round-robin revisitation, without a global scheduler or task registry. Independent review should check the cache keys, one-hour bound, exact-success clearing, reservation-before-dispatch rule and restart/counter interactions.

The constants, replacement heuristic and tranche size need later workload qualification. Useful recovery rate, source correlations, latency, retained-progress benefit and resistance to cache churn remain empirical questions. The module proves neither eventual evidence acquisition nor useful mathematics. It is ready for paper audit, not deployment or automatic background activation.
