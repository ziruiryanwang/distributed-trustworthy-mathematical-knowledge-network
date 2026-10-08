# Direct-contact broker protocol audit

Date: 2026-09-20. Independent concept audit of the proposed `BROKER_DIRECT1` capability 9, organizational types `0x8125/1` through `0x8128/1`, and operations 21 through 23. The author note and frozen H/earlier files were not edited. No implementation, test execution, executable model, native replay, extraction or benchmark was performed.

## Reviewed cut and claim scope

The following SHA-256 values identify the reviewed source bytes. The direct-binding, BROKER1 and trust-boundary notes were read in full. The inherited sources were read at the particular encoding, negotiation, descriptor, execution, disclosure, replay, snapshot and generation-seal contracts relevant to this audit; this is not an independent re-audit of every native or routing mechanism.

| Source | SHA-256 |
|---|---|
| `notes/analyses/CP-001I-direct-broker-bindings.md` | `97BF54F50DA9EBE347380EE22BF78749E149FCE48DD542BB892158FE40B9172F` |
| `notes/analyses/CP-001I-untrusted-search-brokers.md` | `2A404FAE9F79FE7ED40D1430CAF8AB0B0738CE35F53F340A4BA490C2ECB83C1F` |
| `notes/analyses/CP-001I-candidate-service-trust-boundary.md` | `497C105A3EFD4502A8D7107489E8CDB78DC37D0696451C1E4040E3952D88E62F` |
| `notes/analyses/CP-001G-structural-retrieval.md` | `1F295806C580224811C10A0A8273A53D35C0FDDC7D8085EBC5F9F224F47CDDCA` |
| `notes/analyses/CP-001G-profile-and-consumer-bindings.md` | `456FC9876D73F90CACF456BA0F55166F25F2ABB2FCDAEF05CAE5A82B52A65EED` |
| `spec/OPERATIONAL-CORPUS-V1-NETWORK.md` | `46529C8040D8D58F9CB6C27FB4DBC148C525AFC0B0FCCA49788A71FD2136871B` |
| `spec/OPERATIONAL-CORPUS-V2.md` | `B3A339FEF326D6E9F195A6BD186457B294ACFC1935B14B74C113C8E4C33B4A91` |
| `notes/analyses/CP-001E-exchange-scaling.md` | `4BB30F0CCCEC9019EAF6CFF337F5280795FE23F7FA4CD462713E808CB9DB4426` |

This review establishes paper-level compatibility or identifies a missing condition at these exact bytes. It does not establish implementation correctness, practical throughput, Byzantine snapshot completeness, useful recall, unfamiliar-broker discovery or evidence availability.

## DB-AUD-001: Put the comparison and acknowledgment observation inside the mutation linearization transaction

Status at reviewed cut: open precision requirement for the exact concurrent contract. Severity: material if the numbered algorithm is implemented as separate compare and commit phases. This is not a counterexample to a correctly linearized compare-and-update implementation.

The mutation section says that the execution constructs its candidate change and atomically commits row, lead, posting and index-cut changes. Its numbered steps nevertheless put the current-self comparison in step 3 and the commit in step 5. It does not explicitly require the comparison, no-op decision and acknowledgment observation to be revalidated by that transaction. One local authority writer serializes final writes; by itself that does not validate an earlier executor read.

Smallest stale-check schedule:

1. Source A has selected lead `l0` at descriptor `d`.
2. Two independently admitted executions propose `l1` and `l2`, both expecting `LeadDigest(l0)`.
3. Both compare while `l0` is still current and prepare their changes.
4. The authority writer atomically commits `l1`, then atomically commits the previously prepared `l2`.

Every individual write can satisfy the explicitly listed row/posting atomicity requirement, yet the second write overwrites a selected value that no longer equals its expected prior. The corresponding withdrawal schedule compares `l0`, races with its removal, then commits a stale proposed replacement. The intended rule must reject such a stale prepared change at its actual commit point.

The same issue affects no-op acknowledgments: an `ALREADY_LISTED` computation can observe the requested lead, race with an update or withdrawal, and then name a later public cut at which its reported self lead is absent or different. The specified acknowledgment invariant requires one consistent observation, even when no metadata changes.

Specific repair: define one authority-writer linearization transaction that checks the current selected self value, decides idempotence/conflict/absence, checks policy and capacity, applies any row/lead/posting change, and selects the exact acknowledgment cut and self-lead option. Expensive syntax validation or preparation may occur before it. Every prepared precondition must be revalidated inside it. Recomputing or retrying preparation consumes the same finite admitted grant; exhaustion yields the specified charged nondecision rather than a stale commit. Owner-local selection changes participate in the same serialization.

No new wire field is necessary for this repair. It also does not solve DB-AUD-002.

## DB-AUD-002: Value comparison permits ABA; do not claim general stale-intent or withdrawal fencing

Status at reviewed cut: an established semantic limitation, not a contradiction in the sentence that explicitly allows a mutation when its exact comparison succeeds. It must be made explicit in the required delayed-submit conformance case. A stronger withdrawal guarantee would require a design amendment.

Even with DB-AUD-001 repaired, comparing only absence or a lead digest permits return to the same value. Smallest absence trace, all within one live admission epoch and offer lifetime:

1. The selected self lead is absent. Two independently paid submissions of `l0` are prepared with expected prior `[0]`; one remains unclaimed or delayed before its mutation linearization.
2. The other submission commits `l0`.
3. A later valid withdrawal expecting `LeadDigest(l0)` removes the lead, possibly retiring the row and postings.
4. The delayed expected-absent submission reaches its linearization point. Selected-self absence is again true, so it can commit `l0`.

This is not replay of an already executed action. NET2's exact-action single-execution record cannot reject it as such. Nor does a successful withdrawal automatically revoke every other independently admitted operation for the same source and descriptor.

A nonempty ABA variant also exists: `l0 -> l1 -> l0`; a delayed update or withdrawal expecting the digest of `l0` can then succeed. Hashing the lead more strongly cannot distinguish two occurrences of the same canonical value.

Smallest repair if value-CAS is the intended interface: explicitly state that source withdrawal changes the current selected value but does not fence previously issued distinct mutation intents after an ABA cycle. Include both paper cases: a delayed update expecting a now-absent nonempty lead conflicts; a delayed expected-absent insert after insert/withdraw can list again. A client requiring stronger local cancellation must settle or cancel its own outstanding calls and respect NET2's distinction between cancellation before claim and uncertain/running work. No impossible instantaneous global cancellation should be implied.

If the intended property instead forbids all pre-withdrawal intents from restoring the lead, add a bounded checked generation/revision or equivalent issuer-admission fence to the mutation precondition. The design must specify absence after removal, unknown-state discovery, revision exhaustion, owner-local edits, outstanding offers, garbage collection and epoch retirement. Reclaiming the only tombstone while its old request can still be admitted recreates the counterexample. An unbounded permanent tombstone set is not an acceptable repair under the selected finite profile.

## Other reviewed seams

| Seam | Paper result at this cut |
|---|---|
| Exact decoding and typed identity | Inherited deterministic CBOR supplies exact positional arrays, bounded uint64 values, typed ContentIDs and rejection of extensions. `D` retains `0x8124/1`, its own content identity `d`, and its exact original semantic target tags. Changing leads changes a candidate row, not `d`. |
| Hidden native bindings | Broker validation compares syntax and visible R values only. A constructor target continues to refer to a group replay; no fabricated independent constructor root or broker-side native fetch is required. A forged visible claim remains a client acquisition/checking obligation. |
| Capability separation | Reciprocal capability 9 permits only the new metadata codecs/operations. It does not imply capabilities 7 or 8, foundation adoption, a native service role, or a routing role. Native STRUCT2 collection separately needs its actual 3+7+8 contract. Empty native-profile advertisements are consistent with metadata-only service. |
| Other-source ownership | A self mutation is bound to the authenticated source. A fifth lead cannot displace another source. Last-lead removal must retire current row and current postings together. Old snapshots remain historical under their own authority. |
| Exact-action replay | NET2 binds the exact typed ServiceCall, offer and redemption action. Replaying a committed action returns prior metadata or expired status and cannot run the operation again. This does not solve the distinct unexecuted-intent ABA case. |
| Immutable pagination | Snapshot roots freeze rows, lead values and posting lists. The shortest required-token posting and canonical `d` order remain fixed. Only complete tests and committed matches advance the inclusive next boundary. A full output buffer, interrupted test or zero-progress partial page cannot skip a matching row. |
| Query changes and ceilings | Holder, predicate, original lower boundary, planner, disclosure generation and expiry remain bound to retained state. Existing snapshots accept only the matching continuation, not a redirected seek. A continuation may lower the initial ceilings but cannot increase them. |
| HMAC authority | Separate snapshot and continuation domains, holder/epoch binding, retained-root agreement, and a digest of the exact snapshot token prevent a valid continuation from silently selecting another snapshot under the intended HMAC construction. A token alone supplies neither the retained state nor a paid execution. |
| Admission seal and restart | The new note explicitly selects expiry/revocation of broker snapshots at seal or uncertain restart, rather than importing NET2's optional surviving-data-lease behavior. Already claimed local executions retain only exact funded continuations and cannot recreate a revoked snapshot. The explicit exception is coherent. |
| Metadata delivery withdrawal | Inherited NET2 records the exact disclosure scope/version with the immutable outcome and rechecks it atomically at delivery claim. Revocation cancels unclaimed disclosure; already claimed sends follow bounded cancellation and cannot recall transmitted bytes. Current-index changes alone do not rewrite an authorized historical snapshot. |
| Typed outcomes | `CONFLICT` is an acknowledgment outcome under top-level OK, not a new NET2 error code. Gracefully committed query budget stops use PARTIAL. Body identity, exact call identity and canonical body length are bound without a foreign mathematical assessment. No-body errors preserve inherited semantics. |
| Finite resources | Per-call scan, row, byte, CPU, wall and memory bounds coexist with aggregate stock, snapshot, traffic, execution and recurring-work ceilings. Counts are expressly not simultaneous throughput promises. Recurring cleanup, control work and failed attempts are charged. No native evidence resources are supplied by the broker profile. |
| Authority and decentralization | Rows remain inert hints with bounded public-native contacts. They create no generic CAS access, source export authority, local tool permission, compulsory broker, public research goal or routing advertisement. |

HMAC drafting observation: the note specifies token fields, algorithms and domains, but could state its wrapper and MAC preimage as explicitly as `LeadDigest` and the inherited NET1 cursor wrapper. For example, select canonical `encode([encodedTuple,mac32])` bytes and one exact domain-delimited MAC preimage, and write the continuation tuple's order explicitly. Because these tokens are issuer-private opaque formats, the present wording does not by itself demonstrate an interoperability failure or a cryptographic attack; this observation is not elevated to another security finding.

## Byte and resource checks

The page budget arithmetic is conservative: at most 16 KiB of candidate payload plus at most 16 KiB of all framing, token, envelope and result metadata fits the minimum 32 KiB encoded-result ceiling when those categories account for every encoded byte. At 1 MiB, 64 maximum-allowance rows need not fit once framing is included; the note explicitly makes 64 a ceiling rather than a promise.

The row's stated 16 KiB allowance is loose: a 4096-byte descriptor and at most four 1024-byte encoded leads, plus the small candidate/byte-string/list framing, fit in roughly 8.1 KiB under this exact grammar. No optimization depends on filling the entire 16 KiB allowance. A conformance example should distinguish a maximum permitted bound from an actually constructible maximum-sized row.

The retained posting ceiling equals `131072 * 32 = 4194304`, matching the maximum number of token memberships if every allowed retained row version contributes 32 tokens. Copy-on-write roots, indexes, records and spools still consume additional actual bytes. The profile's stock count does not waive those costs or inherited hard limits.

The recurring service CPU and traffic ceilings can bind before the 20,000-execution count when every execution approaches its maximum. This is consistent with the explicit simultaneous-resource qualification and cannot be converted into a promised execution rate.

## Disposition

Before selecting these exact direct-service bindings, make DB-AUD-001's linearization requirement explicit and resolve DB-AUD-002 by choosing and documenting the intended guarantee. The remaining reviewed seams admit the stated conditional paper arguments. This is not a claim that the optional wider broker-routing sketch, client retry policy, comparative economics or an implementation has passed this protocol audit.

## DB-AUD-003: Snapshot occupancy is an independent gate on the 10,000-attempt fixture

Addendum scope: the root requested a bounded cross-module audit of snapshot lifecycle against the small known-contact economics fixture. The relevant small-fixture passages of `notes/analyses/CP-001I-broker-economics-and-availability.md` were reviewed at SHA-256 `F5E82A4A52A4FD8223D831782920FB71003FFF53094753745A30EE1BDA732A9F`. The direct-binding note remained at `97BF54F50DA9EBE347380EE22BF78749E149FCE48DD542BB892158FE40B9172F`. No broader economic qualification or measurement is claimed.

Status at those cuts: open supply/lifecycle condition. The direct note permits eight live snapshots, each with a lifetime up to 600 seconds, but selects neither an earlier routine retirement rule nor a shorter supplied lifetime. The economics fixture says its per-node caps can tolerate all 10,000 one-page attempts choosing one node. Its CPU/traffic inequalities and generic burst/queue caveat do not establish enough snapshot turnover, even for smooth arrivals.

Smallest capacity countercase: eight fresh queries create eight snapshots; each snapshot remains allocated for 600 seconds. Each query may finish its one allowed page quickly, but an END outcome merely omits the next continuation; it does not explicitly retire its snapshot. MORE or PARTIAL outcomes are even clearer: the investigation may stop after this one page while the broker retains the untouched lease. Subsequent new-snapshot queries lack a slot until retirement. No hostile flood, CPU exhaustion or packet loss is required.

With 600-second residence for each occupied slot, steady-state start capacity is at most

`8 * 86400 / 600 = 1152 new snapshots per day`.

For 10,000 fresh-snapshot attempts per day, the necessary average occupancy condition is

`mean charged slot residence <= 8 * 86400 / 10000 = 69.12 seconds`.

This average condition is not sufficient for burst admission, and the 600-second maximum is not proof that every implementation actually retains each snapshot that long. The finding is that an allowed lifecycle defeats the claimed supplied workload; the fixture must select and account for a qualifying lifecycle.

### Minimal repair without another operation

A selected short lifetime plus an explicit stock/admission condition suffices. It does not require any one-page attempt to reach END, and it does not require a new close opcode. A concrete possible policy is a maximum 60-second query-snapshot lifetime within the protocol's 600-second hard ceiling. Ideal slot turnover then allows `8 * 86400 / 60 = 11520` starts/day. Starts spaced every `86400 / 10000 = 8.64` seconds have at most seven simultaneously live 60-second leases, before separately considering reservations and retirement lag.

The actual sufficient condition must state that the workload's admission schedule fits at most eight total snapshot-slot reservations and live allocations at every instant. Count issued offers reserving a future slot, provisional/running creations, snapshots whose response was lost, and any allocation that has not yet been safely retired. A lifetime measured only from completed snapshot creation does not bound earlier offer-reservation occupancy or an unfunded cleanup backlog. Existing execution, queue, reply-spool, pinned-version, byte and recurring-work conditions still apply independently.

The lifecycle should close these exact points:

1. Reserve each required slot and its bounded retirement/finalization resources before admitting work. A failure before a snapshot becomes live releases only genuinely unallocated or terminalized capacity. Admission cannot promise an additional live snapshot merely because a paid query has finished computing.
2. Give each created snapshot an immutable issuer-local expiry, selected by the supplied policy and never renewed by continuation, repeated calls, lost replies or accounting-interval rollover. END may conservatively retain its otherwise unreachable snapshot until that same short expiry; early END retirement is an optional optimization, not necessary for the repaired fixture.
3. At expiry, prohibit new use of that snapshot and return the declared stale result. Retire its live query authority and reclaim its slot with funded local work. Existing calls retain only their exact finite claimed allocations and may not mint or renew a snapshot. The contract must specify whether expiry cancels their unfinished query or permits an already fixed result to finish; neither choice can create a later valid continuation.
4. Track any still-pinned row/index data and immutable result buffers separately until their actual last authorized reference ends. Releasing a query slot does not release those physical bytes or their delivery allocation. A pending page is still an immutable historical result, with its own finite reply ticket and exact disclosure generation.
5. Specify the relationship between snapshot retirement and an already computed result's delivery scope. If normal query-lease expiry only ends future query use, an independently retained, already computed body can remain deliverable under its unchanged live disclosure scope and finite reply deadline. If the chosen policy also revokes derived unclaimed disclosures, delivery must cancel accordingly. In either case owner disclosure withdrawal continues to cancel unclaimed deliveries, and a historical expired token never becomes current authority.

An honest revised economics statement is conditional on that complete occupancy and cleanup schedule, as well as the existing CPU/traffic/execution limits. It may claim the stated admitted one-page workload fits under those premises. It cannot promise admission for any arbitrary arrival pattern or claim complete scanning, useful results, receipt of every page, or continuation availability after the shorter expiry.

### Lost responses, END and a possible explicit close

A lost first response is the important orphan case. The client may never learn the snapshot token, while NET2 exact-action replay supplies only its bounded prior outcome metadata and need not retain or redeliver the original body. The broker must charge that orphan until its finite retirement. A fresh query can create another charged snapshot. The short-expiry occupancy premise must cover both, or admission must refuse the new one; loss cannot reset capacity or client budgets.

A one-page investigation is not synonymous with an END scan. A 64-row output ceiling or work interruption can leave MORE/PARTIAL after that page, and the investigator can legitimately stop rather than buy continuation. Thus an automatic END-release rule alone does not establish the proposed workload. It also needs careful handling of concurrent paid continuations and already committed result delivery before their inputs or spools are reclaimed.

Without a new operation, the holder's authority is to stop requesting further pages; local lease expiry and owner withdrawal perform retirement. NET2 CANCEL may terminalize a particular unclaimed operation or reply, but is not a specified remote release of every snapshot created by an already finalized operation. It must not silently acquire that extra effect.

An optional later close operation would need exact capability/opcode/argument/result bindings, authenticated-holder authorization, snapshot/epoch matching, idempotent already-closed behavior, atomic ordering against continuation claims, and funded retention/GC rules. Unknown or unauthorized closure requests must not reveal another holder's state. Closing future query authority must not invalidate an immutable computed outcome or make its bytes free; pending disclosure and claimed-send cancellation still follow their exact scopes.

Such an opcode is not a free optimization. In the worst case one close per attempt adds 10,000 paid broker executions: `10000 queries + 10000 closes + 96 ingestions = 20096`, above the supplied 20,000-execution allowance. CPU, request/reply traffic, control records and cleanup also need explicit revised inequalities. Close cannot solve lost-first-response orphans when the holder never receives the token. These costs make short finite leases plus a precise occupancy premise the smaller sufficient repair for this fixture.

### Closure conditions for DB-AUD-003

Close this finding only after the author selects a lifecycle that fixes actual slot residence, preserves result/disclosure accounting, and makes the economics fixture conditional on the resulting concurrent occupancy and arrival schedule. A shorter selected TTL with those conditions is sufficient; adding an operation is optional. A statement that every attempt uses one page, or that END lacks a continuation, is insufficient by itself.

## Independent re-review of the repaired direct contract

The complete direct-binding note was reread at SHA-256 `2CE9222631ED95AE0CE7B31C875AA4CD72EA5D0440B7BC1A8E34FB84D7F2EFB2`. This re-review uses the same concept-only scope and unchanged inherited-source cuts above.

**DB-AUD-001 is closed at this cut.** One authority-writer transaction now reads the actual current lead, rechecks preparation, decides no-op/conflict/policy/capacity, commits row/posting effects and selects the acknowledgment cut. The numbered algorithm expressly places steps 2 through 5 in that transaction. Owner-local changes share the same serialization, and failed repreparation cannot gain a new grant. The two-prepared-writes trace now forces the later decision to observe the earlier committed change; no-op acknowledgments name their actual observed cut.

**DB-AUD-002 is closed as an explicit guarantee choice.** The contract deliberately selects plain value-CAS, records both absence and nonempty ABA traces, and distinguishes a distinct unexecuted action from an exact-action replay. Withdrawal claims only the current removal observation. Quiescent source-side withdrawal requires settling or cancelling outstanding mutations and stopping new ones, with explicit limits for uncertain running work and owner-local selection. No stronger revision-fencing property is claimed or supplied.

The HMAC drafting observation is also resolved: token bytes are canonical `encode([tupleBytes,mac32])`; each MAC has its exact domain, zero delimiter, u64be tuple length and tuple bytes. Both tuple orders and the full snapshot-wrapper digest binding are explicit. This closes the format ambiguity without introducing new authority.

**DB-AUD-003's protocol lifecycle conditions are closed at this cut; its economics timing composition is assessed separately below.** Occupied slots include reservations and retired roots still used by scans. END atomically closes future scan claims, MORE/PARTIAL do not, and lost first responses or aborted first scans can leave charged orphans until finite expiry. Retired slots are not released before their actual root/scan obligations end. Immutable outcomes, result buffers and exact disclosure authority remain in their separately charged NET2 allocations. Normal query retirement does not by itself erase a still-authorized reply, while actual disclosure withdrawal and the expressly selected seal policy retain their cancellation effect. No close opcode or hidden free close execution was added.

The direct note now gives the exact all-times occupancy condition over reservation and actual release ticks, identifies the 1152/day countercase, and restricts the small fixture to its shorter-lifetime and temporal premises. It does not claim that a one-page attempt reaches END. Already claimed scans cannot turn retirement into a renewed continuation authority.

## Independent closure of the snapshot/economics composition

The revised small-fixture, snapshot-stock, temporal-supply and paid-execution passages of the economics note were reread at SHA-256 `0E3AFB634128694DC5B5160954BF0EE73BA445E8CC2110F86EFA961DDF092DE2`, against the unchanged repaired direct cut `2CE9222631ED95AE0CE7B31C875AA4CD72EA5D0440B7BC1A8E34FB84D7F2EFB2`. This is a limited timing/accounting cross-check, not an independent qualification of unrelated comparative economics or useful yield.

**DB-AUD-003 is closed for the explicitly conditional finite workload at these cuts.** The reservation schedule is spaced by 8.64 seconds and starts without old residue or unrelated slot users. Each charged reservation lasts at most 66 seconds, including up to two seconds to create or relinquish the provisional snapshot, up to 60 seconds of lease, up to two seconds of final claimed-scan references, and up to two seconds of reclamation. The exact half-open interval argument gives at most `ceil(66 / 8.64) = 8` occupied slots. Thus the fixture counts every required phase rather than replacing actual residence with the token's TTL.

This bound remains valid when every page is MORE/PARTIAL or its first response is lost: no early END retirement or received release acknowledgment enters the argument. The explicit creation, reference-release and reclamation premises must actually hold. A spool that retains snapshot roots beyond them invalidates this workload condition; it does not disappear from accounting. Allocations continuing after the 86400-second interval remain charged. The fixture does not silently apply an initially empty one-interval schedule to a later interval with old residue.

The independently checked arithmetic is:

| Quantity | Result |
|---|---:|
| Complete charged slot residence | `2 + 60 + 2 + 2 = 66` seconds |
| Maximum occupancy under the stated spacing | `ceil(66 / 8.64) = 8` slots |
| Occupancy with full 600-second residence at that spacing | `ceil(600 / 8.64) = 70` slots |
| Ideal 600-second turnover with eight slots | `1152` starts/day |
| New paid executions | `10000 + 0 + 192 + 400 = 10592 < 20000` |
| Broker CPU allowance used | `10000 * 0.25 + 192 + 500 = 3192 <= 3600` CPU-seconds |
| Stated broker traffic bound | `10000 MiB + 192 * 8 KiB + 1 GiB = 10.76708984375 GiB < 16 GiB` |

The 192 ordinary submissions correctly fund both sources' self leads for 96 new candidates. The additional 400 paid mutations cover their stated replacements, withdrawals, conflicts and fresh mutation retries within the separate 500-second allowance, leaving at most 100 seconds of that allowance for other cleanup/control work. Failed operations already count in their actual operation category; they are not excluded from the denominator or counted twice. The fixture grants no continuation queries, close calls or additional query retries outside its 10000 new-query bound. Exact-action replay creates no paid reexecution but retains its actual control and response charges. The remaining 9408 execution-count headroom alone supplies no CPU, traffic, snapshot occupancy or new workload guarantee.

No unresolved finding from this bounded protocol audit remains at the two repaired cuts. This closure establishes the stated paper contracts and conditional arithmetic only. Actual admission timing, cleanup costs, memory use, successful delivery, native acquisition, useful application yield and sustained service outside the declared finite trace remain separate qualification obligations.
