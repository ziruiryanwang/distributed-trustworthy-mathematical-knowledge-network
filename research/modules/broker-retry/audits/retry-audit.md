# Independent paper audit: owner-local broker retry policy

Date: 2026-09-20. Reviewer: `commons_decentralization`, independently reviewing the retry-policy author. Scope: local failure keys, suppression, selection, accounting, clock/restart behavior and conditional progress. No implementation, model execution, scheduler, native replay, artifact extraction or benchmark was run. Frozen G/H files were not edited.

## Reviewed artifacts and current verdict

Primary artifact: [CP-001I broker-local retry policy](../../../../notes/analyses/CP-001I-broker-local-retry-policy.md).

Initial reviewed SHA-256:

`95E57DDCBC8843C4F250772046BB181C6E71FDADFBE27C0EA221C13E86F56C73`.

Relevant companion artifacts read:

- [Candidate-service trust boundary](../../../../notes/analyses/CP-001I-candidate-service-trust-boundary.md), SHA-256 `497C105A3EFD4502A8D7107489E8CDB78DC37D0696451C1E4040E3952D88E62F`.
- [Untrusted search brokers](../../../../notes/analyses/CP-001I-untrusted-search-brokers.md), SHA-256 `2A404FAE9F79FE7ED40D1430CAF8AB0B0738CE35F53F340A4BA490C2ECB83C1F`.

Repaired author cut independently read in full and hash-verified:

`7E859F189A498090D054D5411136FA5569C8F86FCC036B69F6AFFC98615FAABB`.

The module has a sound intended separation: finite owner-funded investigation, local heuristic suppression, independently checked mathematical acceptance, and no autonomous retry authority. Its one-hour transient bound and fixed-lead circular-selection argument are conditionally valid. The initial review identified three local specification seams. All three are closed at the repaired cut above, with the exact-cut reasoning recorded below. No new concrete paper contradiction was found. None of the original findings was a demonstrated native-acceptance bypass; they concerned correct local suppression/work control.

| Issue | Current paper-audit status | Clarification independently verified |
|---|---|---|
| RET-AUD-001 | CLOSED at repaired cut | Exact observation identities are separate from stable retry-obligation/counter keys, with obligation-specific clearing |
| RET-AUD-002 | CLOSED at repaired cut | TRY_ONE is planner-only; one-shot ticket consumption and atomic idempotent completion settlement are explicit |
| RET-AUD-003 | CLOSED at repaired cut | Scoped Applies, minimum over per-lead maximum deadlines, horizon checks and after-negotiation rechecks are explicit |

These were bounded repairs to this module. They require no new global coordinator, theorem blacklist, transport extension or rewrite of the native trust boundary. The root agent owns author-note changes and the central issue ledger; this audit edits neither. The following original finding text is preserved as a trace of the counterexamples, not a claim that they remain unaddressed.

## RET-AUD-001: exact observation and stable retry counter are different keys

Location: “Failure classes and exact cache keys,” “Temporary suppression rule,” and obligation-specific clearing.

The failure table binds CORRUPT_RESPONSE to exact source/F/R and “call/requested CID/range,” while the backoff paragraph counts repeated failures in an applicable “class/source/replay record.” Those are not yet one unambiguous key definition. The text also requires a successful observation to clear only the actual failed obligation it discharges.

Minimal counterexample under the exact-invocation reading:

1. A settled paid invocation `i1` requests exact object/range `x` from source `s` for replay `R`, receives corrupt bytes, and creates an observation with count one and 300-second cooldown.
2. After that cooldown, a newly funded invocation `i2 != i1` requests the same `x` from `s` and again receives corrupt bytes.
3. If the cache key contains the exact invocation, the new record has count one again, not count two. The advertised escalating backoff for a repeated obligation is not obtained from those literal observation keys.

The opposite coarsening also needs a rule. If the implementation instead keeps one `(class,F,R,s,role)` counter, failures for two objects `x` and `y` can share it. A later valid response for `y` does not discharge the old failed observation for `x`; simply deleting that aggregate entry would contradict obligation-specific clearing. The same problem arises if a connection success clears an UNAVAILABLE counter which actually represents a negotiation or later-read timeout. The document's intended “corresponding obligation” condition is appropriate, but the record mapping has to make it enforceable.

This is an underspecified identity/aggregation seam, not a proof that every possible interpretation is incorrect. For example, “call” might have been intended to mean an operation kind rather than a unique invocation. That interpretation should be stated rather than left to implementations.

Concrete minimal repair:

- Define an immutable local observation identity binding the admitted trial, actual invocation/request, source, role, exact requested data/scope, actual failure stage/result and clock observation.
- Separately define the stable retry obligation/bucket key used for `n` and `notBefore`. State which fields intentionally persist across new invocation IDs, endpoints and broker snapshots, and which changed scope/stage/data obligation constitutes a different key.
- If a bucket intentionally aggregates several exact obligations, retain a bounded exact membership/summary sufficient for clearing, or choose a precisely stated conservative clearing rule. A valid unrelated response must not clear an undischarged obligation by accidental key collision.
- State whether successful discharge deletes or resets the corresponding counter, and that time expiry changes eligibility without silently resetting episode expenditure.
- Charge all observation/membership/counter state to the existing 1024-record/512-KiB limits; inability to retain a precise key is unknown scheduling information or an explicitly chosen eviction, not a stronger negative claim.

Retest criterion: two distinct settled failures of the same chosen stable obligation produce the intended next count, while a successful different obligation cannot erase it. A mere endpoint edit, new snapshot or replayed outcome cannot manufacture a fresh history. A deliberately different replay, relevant realization or scope remains independently classified according to the stated mapping.

## RET-AUD-002: TRY_ONE and source-trial execution need a single owner

Location: “Input and output contract,” reservation-before-work rule, and selection steps 3–4.

TRY_ONE is described as returning a selected lead and a reserved acquisition tranche. The selection procedure then says to perform the source trial in that same visit. This admits two ordinary interface readings: a planning policy which returns work for its caller, or an executing policy which already performed the work. The author should select one and bind its completion transition.

Minimal counterexample:

1. A visit reserves one trial token and follows step 4, starting a trial on source `s`.
2. The visit returns TRY_ONE with the selected lead/tranche.
3. A caller treating the documented output as a work instruction starts a second source trial with the same returned reservation, unless an explicit one-shot consume/fence rejects that interpretation.

The inherited exact-invocation rules can reject a repeated use of one invocation identity, but a tranche can contain up to eight distinct service calls. The policy must say which caller can allocate those invocation identities and that a second independent source trial is not licensed by one reservation. It should not rely on two layers guessing the same execution convention.

A related restart case is duplicate completion processing. One actual failed request can be replayed to a local outcome consumer after a crash. If both deliveries increment `n` or set a new deadline at the later receive time, the policy records two “new completed failures” from one admitted observation. That can extend suppression without another actual source attempt. Exact source-call charging alone does not specify idempotent updates to this new local retry state.

Concrete minimal repair:

- Choose either `select visit -> TRY_ONE(one-shot ticket)` with the ordinary caller as sole dispatcher, or an executing visit whose return reports the already consumed trial/outcome. A ticket is local state, not new remote authority.
- Bind the ticket to exact episode/admission generation, candidate/source/role, reserved tranche, current guards, cursor transition and one authoritative consumption state.
- Durably consume/fence it before any dispatch. A repeated use, uncertain prior consumption or lost return follows the inherited reconciliation path, never another trial token.
- Bind failure/success recording to the exact locally settled observation identity; apply it to the retry counter/clearing state at most once. Recording an outcome does not itself schedule another visit.
- Reserve/charge required settlement and reconciliation state; exhausted or expired admission does not authorize an uncharged new source call.

Retest criterion: a repeated TRY_ONE delivery cannot launch another trial, a repeated completion cannot increment/rebase twice, and a crash between reserve, cursor advance, dispatch and completion leaves either one consumed trial or a fenced unknown state. Cache eviction cannot remove the work ledger or the only necessary in-flight fence.

## RET-AUD-003: applicability and earliest eligibility require a small explicit predicate

Location: NOT_SERVABLE exact-scope key, “every applicable retained cooldown,” selection guards and DEFER_UNTIL.

The policy correctly says that refusal under one scope proves nothing about another scope. BROKER1 supplies only a PUBLIC_NATIVE lead; the caller may still need fresh negotiation to learn the actual public scope or obtain a new holder-bound export. The retry module should distinguish an observation's exact evidentiary scope from any deliberately broader local throttling policy.

Minimal scope counterexample:

1. Source `s` refuses read `x` under exact old scope `S1`, creating a retained NOT_SERVABLE record.
2. On a later admitted visit, source negotiation could establish a distinct allowed scope `S2` for exact `R`, or a local plan may only seek that fresh negotiation.
3. Applying the `S1` failure automatically to every PUBLIC_NATIVE action at `s,R` suppresses a different scope/action. That may be a consciously selected conservative load throttle, but it is not an inference that `S2` cannot serve the bytes and is not established by the exact-scope key alone.

Conversely, treating every newly issued scope/invocation identity as a wholly fresh source history could bypass an intentionally source-wide rate control. The policy should say which behavior it selects. No broker metadata may fabricate `S2` or its authority merely to evade a cooldown.

Minimal time counterexample:

1. Lead `a` has two applicable cooldown deadlines, 30 and 300 seconds from the current local origin.
2. Lead `b` has a deadline of 120 seconds and passes all nontransient guards.
3. The first actual transient eligibility is 120 seconds for `b`, not 30 seconds for `a`. If `b` instead fails a nontransient disclosure/resource guard, the transiently actionable time is 300 seconds for `a`, subject to the remaining episode horizon.

Returning the earliest stored deadline without the per-lead conjunction can consume repeated paid visits without any lead becoming eligible. The current prose says “earliest meaningful” but does not yet give this operator or distinguish candidate-wide and lead-local barriers.

Concrete minimal repair:

- Define a bounded local predicate `Applies(observation_or_bucket, planned_action, current_exact_context)`. Unknown future source scopes do not inherit read authority; comparisons may use only actual retained/requested context.
- Separate candidate-wide guards from source/action-specific guards. A cached refusal or disclosure prohibition at one lead cannot become a candidate-wide native rejection merely because it is checked early in the visit.
- Let `L` contain current leads/actions passing the stated nontransient grammar, policy and funding conditions. For each `l` in `L`, define its cooldown deadline as the maximum of its applicable retained deadlines, with an empty set immediately eligible. The next transient eligibility is the minimum of these per-lead deadlines.
- If `L` is empty, report the actual admission/policy/grammar barrier instead of presenting a timestamp as sufficient. If the minimum lies outside the still-live episode/tranche horizon, disclose that new admission would be required; a timestamp remains information, not a future-work grant.
- A broader source-throttling bucket is permitted as an explicit local heuristic, provided its exact membership, expiry/clearing and informational meaning are stated consistently with RET-AUD-001. It must not be called a mathematical or source-scope impossibility result.

Retest criterion: old-scope refusal, fresh negotiation, two simultaneous cooldowns, a permanently policy-blocked lead and an expired episode each produce the documented scoped outcome without creating authority or implying another source is invalid.

## Claims that survive the review under their stated assumptions

### Native acceptance and class boundaries

The following distinctions are correctly required by the author note and the companion receiver contract:

- Unavailable source, refused scope or corrupt response is not evidence that the theorem is false.
- Hash-mismatching response bytes cannot support EXACT_CODEC_REJECT for the requested object.
- A completed exact codec rejection binds the actual hash-correct typed bytes and supported interpretation; it is not a blanket judgment about another typed object/profile.
- A completed native rejection binds exact F/R, expected target, actual realization/check inputs and checker interpretation. An alternate proof or changed relevant realization is not the same failure case.
- Policy, unsupported capability and resource nondecision cannot be silently upgraded to completed native invalidity. An interrupted/crashed checker supplies no completed native-rejection event.
- If a retained exact context cannot be reestablished, the cache cannot apply its negative observation as an exact rejection. It does not authorize a guess from only a terminal JudgmentID.

These are conditional acceptance boundaries, not an audit of a future decoder/kernel implementation. In particular, codec rejection should remain tied to an actual required object under the selected checking/acquisition case; a malformed unrelated object received from a source cannot suppress every replay mentioning that source.

### Finite paid work

The separate episode spending ledger is the right invariant. Given durable single-owner accounting and the one-shot repair above, induction over admitted transitions bounds visits by 32, lead inspections by 128 and source-trial initiations by 32. Each trial's at-most-eight service calls remain additionally bounded by the episode's actual smaller call/byte/CPU/deadline allocation. The count caps provide no bytes, working memory or privilege by themselves.

New keys, descriptor variants, broker snapshots, source endpoints, alternate proof instances, cache eviction and source replies cannot mint fresh episode resources. Fresh owner-authorized episodes can of course create new paid work; therefore this is not an absolute lifetime cap on all future investigations. The note states that distinction and does not promise otherwise. Rejection of calls arriving after exhaustion still consumes the parent's bounded dispatch/refusal resources, as the author explicitly acknowledges.

### One-hour transient eligibility

Every declared duration has the form `min(3600, b * 2^(n-1))` with `1 <= n <= 8`, hence is at most 3600 seconds of the qualified local clock. After the last actual failure or conservative rebase, the maximum of any finite set of applicable deadlines is at most one hour later. Subject to fixed guards, retained state and a stable clock origin, transient suppression alone therefore expires within that bound.

This argument does not establish source recovery, a visit at that time, enough remaining episode time, native compatibility or successful mathematical use. Repeated rebasing can postpone eligibility forever; the note says so explicitly. Replayed observation delivery must not masquerade as a new actual failure, which is why RET-AUD-002 matters.

### Conditional circular fairness

For a fixed ordered lead set of size `m <= 4`, retained cursor and a persistently eligible lead `s`, each source selection moves strictly forward in circular order. Until `s` is selected, the cursor cannot make a full circuit: passing `s` would require skipping an eligible lead, contrary to first-eligible selection. Thus `s` is selected within at most `m` subsequent source selections, provided that many admitted selections of this candidate actually occur.

The theorem is about source selections, not wall time or arbitrary investigator visits. An exhausted 32-visit account, stopped investigator, changed lead set, evicted cursor or lead-specific funding/policy failure defeats its premises, not native safety. There is no fairness theorem across candidates, independent agents or changing broker panels, and no eventual-acquisition theorem.

### Restart, eviction and no autonomous work

The note properly requires an exact monotonic origin/generation, refuses remote/wall-clock acceleration, conservatively rebases retained transient deadlines on a new origin, and refuses to resume an account whose budget/deadline continuity is unknown. Cache eviction can lose suppression/cursor history but cannot reclaim spent trials or evict required in-flight reconciliation state.

No output installs a timer, callback, scheduled task, global research goal or automatic fresh account. A next-eligible time is advisory local information. An already admitted caller may choose another visit under actual authority, but the policy itself cannot create that authority. No global theorem blacklist or political attribution rule is introduced.

## Additional bounded seam audit: retry and direct broker service

Separately read [direct broker bindings](../../../../notes/analyses/CP-001I-direct-broker-bindings.md), candidate capability 9 and operations 21–23, at SHA-256 `97BF54F50DA9EBE347380EE22BF78749E149FCE48DD542BB892158FE40B9172F`.

Scope here is lifecycle, status meaning and resource composition. The other direct-service reviewer owns mutation atomicity and snapshot/pagination conformance; those were not independently re-audited as new findings here. At the time of this seam review, the three original issues still awaited their repaired source cut; the later exact-cut disposition below closes them. This additional seam review found no further concrete contradiction under the contracts' stated role/input boundaries.

### Role and status meanings cannot be collapsed

The direct broker supplies inert metadata through capability 9. The retry policy receives an already bounded candidate and chooses an actual same-R PUBLIC_NATIVE source lead. A broker and a native source can use the same physical node/key, but those are different service roles and authority scopes. Receiving the same top-level status code from them does not produce the same local failure event.

| Direct broker observation | Meaning for the retry module |
|---|---|
| BROKER_FIND NOT_SERVABLE | Broker metadata disclosure is denied; it is not a native-source/R refusal and cannot update that source's PUBLIC_NATIVE NOT_SERVABLE counter |
| UNSUPPORTED_PROFILE | This broker does not serve the requested metadata namespace/profile; it neither disproves the foundation nor installs/adopts it or supplies EXACT_NATIVE_REJECT |
| STALE_CURSOR | The broker snapshot/continuation is no longer usable; reacquiring metadata needs a new paid query, not a native-evidence retry or cleared source history |
| PARTIAL with a committed page | Only the returned exact candidate rows are available for candidate visits; unprocessed posting positions supply no candidate and no evidence-source failure |
| END with no useful row | Local finite snapshot coverage for that predicate/boundary, not mathematical nonexistence and not a target/native-check rejection |
| BUSY_NO_ADMISSION, LIMIT_EXCEEDED, ABORTED_RUNNING or uncertain call outcome | Scoped broker-service capacity/interruption/reconciliation outcome; no native corruption or invalidity inference |
| REQUEST_MISMATCH or malformed broker body | Exact request/metadata codec observation only; it cannot poison an unrelated correctly encoded row or native replay |
| LISTED or ALREADY_LISTED | Exact metadata/self-lead observation at a broker cut; no native acceptance, current source availability, retry-budget refill or release of a custody obligation |
| WITHDRAWN or ALREADY_ABSENT | Current self-lead metadata state; not theorem invalidity, global erasure or revocation of independently issued native scopes |
| CONFLICT, DECLINED or DEFERRED_NO_PROMISE | Scoped metadata mutation outcome; no queued publication promise, timer, callback or automatic new admission |

These distinctions follow from the direct operation/body bindings and the retry input's PUBLIC_NATIVE role. They do not require introducing new retry classes for every broker result. A separate owner-funded discovery caller handles broker query/mutation retries under its own exact-call rules. The retry policy must not infer a native failure merely from a shared NodeID or a familiar error-code spelling.

In particular, a malformed `0x8125/1` BrokerCandidate wrapper with otherwise valid descriptor D is not interchangeable with D's own `0x8124/1` object or the named native replay R. An exact malformed-wrapper cache may apply to those exact wrapper bytes; it cannot suppress a different correctly formed wrapper for the same d with a different valid lead set. Likewise, an unknown broker namespace is not a completed codec rejection of an unseen native proof.

### Independent lifetimes and explicit transitions

A broker snapshot expires within 600 issuer-local seconds and is not preserved across the direct service's admission seal/uncertain restart. A retry cooldown can last 3600 receiver-local seconds, and an investigation can have a shorter or up-to-two-hour local horizon. These lifetimes serve different purposes; no numerical equality or shared clock is required.

Minimal compatible trace:

1. The client receives a complete validly encoded candidate row in an admitted broker page and retains it as an untrusted local candidate under its own bounded state.
2. A selected native-source attempt fails and creates its exact local transient obligation.
3. The broker's old snapshot expires while that obligation remains in cooldown. Future metadata continuation is stale, but its expiry does not revoke already received inert bytes or reset the native-source failure record.
4. On a later independently admitted visit, the client may use its retained candidate or obtain a new paid broker page. Either path still needs actual fresh native source authority, current local policy and sufficient remaining/newly admitted resources.

No timestamp in a broker snapshot advances the client's retry clock. Conversely, restarting/rebasing the client's retry clock does not renew a broker snapshot or native export lease. Returning a next-eligible local time never schedules either a source retry or a broker query. Already transmitted metadata cannot be recalled merely by withdrawing the broker's disclosure scope; future disclosures and native reads remain governed by their own actual authorities.

A newer snapshot can change the bounded source lead list while d remains the same. The existing cursor rule handles a missing prior NodeID as an ordering boundary, and retained failure records remain keyed to their actual source/replay/obligation rather than the broker snapshot ID. This is compatible with direct row identity. The `m <= 4` fairness claim applies only while the lead set is fixed; broker selection/churn can defeat that premise without constituting a protocol contradiction.

### Resource composition and partial progress

For a shared owner investigation budget, a sufficient composition rule is, coordinate by coordinate,

`spent_or_reserved(discovery) + spent_or_reserved(retry_local) + spent_or_reserved(native_acquisition) + spent_or_reserved(settlement/recovery) <= admitted_parent_allocation`.

Only actual nonoverlapping allocations are summed; accounting may use explicit nested reservations without double-counting their already charged parent reservation. It must not give every new broker snapshot, source lead, eight-call tranche or local episode a free additional copy of the same parent budget. Durable release follows actual inherited rules; it does not refund consumed trial/visit counts.

The 32 source-trial limit is not a statement that only 32 broker pages can ever be issued. The retry module's bounded candidate visits likewise do not count every possible failed discovery call before a candidate exists. Those broker calls, including repeated zero-progress PARTIAL pages and stale-snapshot restarts, need the caller's finite cumulative discovery/parent allocation. The direct note's independently paid calls and the receiver trust note's aggregate investigation budgets provide that boundary. Exhaustion produces a stop or explicit new owner admission, not an implied callback or unlimited continuation.

The broker's per-node daily stock/work allowance is also not a client-side acquisition grant. Capability 9 and an admitted operation 23 fund neither capability-8 native source service nor local kernel checking. A source tranche must separately negotiate existing native capabilities/scopes and charge actual calls, bytes, CPU, staging and protected progress. Existing local hash-correct native bytes need not be downloaded again merely because their checking/protection guards need refresh.

An interrupted metadata scan can leave a usable returned subset, and interrupted native acquisition can leave verified retained partial objects. Their distinct snapshot/staging allocations and continuation/current-use guards remain in force. A page's partial progress is not a native proof-check result; native retained progress is not permission to resume a stale metadata cursor. None of these conversions is licensed by the retry policy.

Seam conclusion: the reviewed direct proposal and retry module can compose without a new authority or lifecycle contradiction if the above already-required role/operation distinctions and aggregate accounting are preserved. The repaired retry cut now explicitly incorporates this metadata/native status separation, retained-candidate lifecycle distinction and encompassing budget boundary.

## Exact-cut repair disposition

The reviewer independently read the complete revised retry note and verified SHA-256 `7E859F189A498090D054D5411136FA5569C8F86FCC036B69F6AFFC98615FAABB` while the root held it unchanged. This section closes the identified paper-contract findings, not implementation or empirical qualification.

### RET-AUD-001 — CLOSED

The revised “Observation identity, retry obligations and applicability” section separates immutable actual observations from stable obligations and defines `bucket = (class,F,R,source,role,obligation)`. Invocation identity, endpoint strings and broker snapshots are not stable-bucket fields. Connection, exact negotiation and later scoped operation failures have distinct obligation forms. Refusal binds actual scope/generation; corruption binds exact expected integrity data without the unique invocation or read-token identity.

The two-invocation counterexample now maps both actual failures for the same stable obligation to one bucket: first settlement creates count one, the next distinct settlement increments it. Deadline expiry alone does not reset the count. Success deletes only matching discharged obligations; a connection success cannot clear a later-read failure, and an unrelated header cannot clear corruption of a dependency. Different object/scope/stage obligations are not silently aggregated. All contexts and bounded observation/counter state are charged, and an unrepresentable context is not approximated into a stronger rejection.

This choice intentionally supplies no broader source-wide rate-control or Sybil theorem. New distinct scope obligations may have distinct history, while source calls still consume finite parent resources. That is an explicit limitation, not an unresolved ambiguity in the selected local heuristic.

### RET-AUD-002 — CLOSED

TRY_ONE now returns only a local one-shot reservation ticket; the visit is expressly a planner and performs no source trial. The ordinary acquisition caller is the sole dispatcher. Ticket reservation/charge and cursor advance are atomic, a reserved but unused trial remains charged, and dispatch requires durable RESERVED-to-CONSUMED transition after current-guard/resource revalidation. Duplicate delivery or uncertain prior consumption cannot authorize another trial.

The ticket binds exact account generation, candidate/source/role, planned action, tranche, horizon and guards. Its consumed trial alone can allocate at most eight separately charged native-service calls; unresolved consumed work occupies the one-in-flight slot. Exact outcome identity is settled atomically with its once-only bucket increment/discharge. A duplicate result cannot increment the counter or move its original settlement tick. Recovery is fenced if the record/cache update cannot be established atomically. Evicting the bucket does not let an old settled observation return as a new failure.

The repaired contract reserves settlement/reconciliation work and retains required deduplication fences until the inherited retirement rules reject later delivery. These are the needed one-shot and crash boundary conditions. They remain assumptions for a future implementation to satisfy, not proof that an implementation already does so.

### RET-AUD-003 — CLOSED

The revised `Applies` predicate requires matching F/R/source/role and an exact stable obligation actually present in the proposed action plan. Old-scope refusal therefore does not block an unrelated fresh negotiation or imply failure under a different authorized scope. Future scopes are not fabricated. The caller rechecks after negotiation or discovery of an exact object/range and can stop under the same ticket before the newly blocked stage.

Selection separates candidate-wide guards from source/scope-specific barriers. For the nontransiently admissible lead/action set L, it takes `T(l)` as the maximum applicable deadline (or now) and `T*` as their minimum. DEFER_UNTIL requires actual cooldown and a still-live usable horizon; otherwise the result states the actual admission/policy/grammar barrier. A reported time carries no guarantee that future guards or resources remain valid.

The two-deadline counterexample consequently returns 120 seconds for a valid second lead, or 300 seconds when only the first lead remains admissible, provided the live horizon permits that action. Scope learning can still consume a funded negotiation before discovering a later-stage cooldown; the contract explicitly permits that bounded cost and makes no broader source-suppression guarantee.

### Remaining conditional limits

The fairness result is about circular **selections/reservations**, not guaranteed dispatch, wall time, evidence acquisition or useful mathematics. It requires continued funded selections, stable lead set, retained cursor and persistent eligibility. An unused reserved ticket can consume finite capacity; this cannot be concealed as a successful trial. Clock rebasing, cache loss, source churn, exhausted account or stopped investigation remain the expressly stated countercases to stronger progress claims.

There is no new autonomous work, scheduled callback, global task registry or theorem blacklist. Exact complete native checking remains the only mathematical acceptance path. Later measurements/qualification must still establish actual cache/context/native memory fit, useful recovery rate, resource cost, latency and workload-dependent choice of constants.

## Exit test for this audit

The author repairs and independent exact-cut reread satisfy the exit test for RET-AUD-001 through RET-AUD-003. The paper module can proceed as a bounded class-correct local retry proposal, subject to its inherited accounting/checking assumptions and the remaining qualifications above. Closure does not certify executed behavior or useful mathematical growth. A later substantive source change requires a new reviewed hash and an audit of the changed obligations.
