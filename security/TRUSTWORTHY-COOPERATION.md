# Trustworthy mathematical work and reuse without political attribution as a trust root

## 1. Objective

The network must let agents do useful work independently and learn from unknown agents without building stable mathematics on false or malicious results. Coordination is optional and non-epistemic. Its trust rule is:

> **Any agent may propose; only receiver-local, context-bound, checkable evidence may create stable automatic support.**

Correctness should come from proof-carrying objects and small approved checkers whenever possible. Operational identity and capabilities regulate roles, scarce resources, cell membership, availability commitments, semantic-review authority, and failure-domain measurement. Political attribution—credit, discovery priority, prestige, ownership, and public reputation—is not a correctness prerequisite.

## 2. Identity boundary

### P0 operational identity

Use authenticated operational principals where required:

- stable rotating cell/service principals for federation membership, validator roles, resource accounting, and revocation;
- scoped semantic-intent reviewer or budget-authority principals when an exact nonmechanical contract or resource grant depends on them;
- short-lived worker/session keys for control-message integrity and proof of capability possession;
- receiver-issued work, storage, routing, and child-spawn capabilities;
- lease renewal, cancellation, quarantine, and budget changes;
- key compromise/revocation during an active operational epoch;
- local calibration and measured failure-domain separation.

These credentials may be pseudonymous and need not identify a real person. They confer scoped authority, never theorem truth. Mechanical formal closure in the current strict P0 profile requires exactly local replay or a receiver-locally checked domain certificate. Succinct arguments remain unavailable to that profile until a later versioned policy satisfies the measured break-even, setup/key-to-relation, TCB, and soundness gates. When intended meaning or usefulness cannot be mechanically decided, any authorized reviewer becomes an explicit, fallible trust root for exactly that semantic contract.

### P2 political attribution

Postpone:

- public authorship and credit;
- global discovery priority;
- prestige and ownership;
- permanent real-world identity;
- a universal reputation score;
- institutional or constitutional politics.

## 3. Resource-bounded adversary

Counting malicious identities is meaningless when identities are cheap. For cell \(i\) and time window \(W\), define an enforced exposure vector:

\[
B_i(W)=(B_{\mathrm{ingress}},B_{\mathrm{parse}},B_{\mathrm{retain}},
B_{\mathrm{graph}},B_{\mathrm{route}},B_{\mathrm{execute}},
B_{\mathrm{validate}},B_{\mathrm{recompute}}).
\]

An attacker may create unlimited endpoint labels, submit arbitrary unique objects, form circular support graphs, lie about capability/progress/cost, blackhole leases, poison semantic indexes and caches, flood challenges and decompositions, and construct parser/proof/archive/graph bombs.

The attacker cannot break selected cryptographic primitives, forge receiver-issued capabilities, escape correctly configured sandboxes, or make a sound approved checker accept an invalid certificate.

Availability and liveness require maliciously induced **admitted** load to remain below a deployment's declared fraction of service capacity. Without an admission authority, scarce resource, or identity mechanism, a globally permissionless overlay cannot guarantee Sybil, eclipse, storage, or queue-liveness resistance.

## 4. Fact lifecycle

Each cell maintains distinct stores:

- \(R_i\): bounded receive buffer;
- \(Q_i\): bounded schema-valid quarantine/candidate store;
- \(A_i\): locally admitted durable facts.

They are connected by transitions \(R_i\to Q_i\to A_i\), not literal inclusion: durable \(A_i\) may outlive its raw and quarantine records. For a candidate delta \(\Delta_{j\to i}\) from another cell:

\[
N_i=
\{f\in\Delta_{j\to i}\mid
\operatorname{Admit}_{P_i}(f,\operatorname{Closure}(f))
=\texttt{ACCEPT}\},
\qquad
A_i'=A_i\cup N_i.
\]

Foreign admission is not authority. Equal authentication and policy/validation roots do not imply honest enforcement. Direct set union is valid only for immutable facts already committed by one logical admission authority and copied among its explicitly crash-fault replicas. Mutable grant/ticket spend state and capability authorization state are never merged this way. Every independently operated cell, including one advertising equal roots, receives candidate deltas and re-admits them. Byzantine replicas require receiver re-admission or a separately modeled BFT admission log. The ingest pipeline is:

\[
\text{bounded frame parse}
\rightarrow \text{typed CID/schema check}
\rightarrow \text{grant-backed demand-ticket check}
\rightarrow \text{quarantine}
\rightarrow \text{dependency closure}
\rightarrow \text{sandboxed evidence validation}
\rightarrow \text{local integration}.
\]

For a receiver state \(s\) and candidate \(f\), unadmitted noninterference requires:

\[
\operatorname{Admit}_{P_i}(s,f)\ne\texttt{ACCEPT}
\Longrightarrow
A_i(s\cdot f)=A_i(s)
\land
V_{P_i}(A_i(s\cdot f),O_i)=V_{P_i}(A_i(s),O_i),
\]

apart from bounded screening telemetry and explicit overload signals. Unadmitted input cannot evict validated caches, create children, trigger unbounded recomputation, or enter semantic indexes.

## 5. Demand-bounded promotion

Formal validity is not a scarce-resource allocation rule. An adversary can generate indefinitely many distinct, correct, trivial theorems. Therefore:

The normative resource protocol has six distinct objects: a receiver-issued `BudgetGrant`; a public non-spendable `DemandOffer`; an issuer-authenticated `DemandTicket` bound to a holder key or bounded gateway; an atomic per-candidate `DemandReservation`; one atomic `DemandExecutionClaim`; and an exactly-once `DemandSettlement`. Ticket issuance atomically reserves the ticket's full vector ceiling and redemption allowance from its grant. The grant ledger maintains

\[
\operatorname{finalizedSpend}[g]
+\operatorname{reservedTicketCeilings}[g]
+\operatorname{reservedChildGrantCeilings}[g]
\preceq\operatorname{totalCeiling}[g],
\]

plus the analogous finalized/reserved redemption-allowance inequality. Count authority is separately monotone:

\[
\operatorname{consumedTicketIssueAllowance}[g]
\leq\operatorname{ticketIssueLimit}[g],
\quad
\operatorname{consumedGrantFanout}[g]
\leq\operatorname{childGrantLimit}[g].
\]

The ticket ledger maintains

\[
\operatorname{spent}[d]
+\operatorname{outstandingReservations}[d]
+\operatorname{reservedChildren}[d]
\preceq\operatorname{totalCeiling}[d]
\]

componentwise, plus a cumulative redemption-count ceiling and

\[
\operatorname{consumedTicketFanout}[d]
\leq\operatorname{childTicketFanoutLimit}[d].
\]

Every vector component and count/fanout scalar is finite, canonical, and nonnegative; overflow and underflow fail before mutation. Every grant and ticket has a durable `ACTIVE | TERMINAL` allocation state. New ticket issuance and reservation require the corresponding allocation to be `ACTIVE`; terminalization writes an irreversible tombstone. Existing identical action/digest replay is resolved before that check and returns its stored result, but a fresh action against a terminal grant or ticket fails.

A ticket cannot become usable until its parent allocation commit is durable. Root-grant and root-ticket constructors require canonical absent parent tags; child transitions require the exact parent ID, so no object can cross root and child accounting. Root-ticket issuance checks a live grant and nonreclaimably consumes \(1+\) the ticket's descendant-ticket fanout from the grant's ticket-issue allowance. Child-grant issuance likewise consumes the child's ticket-issue allowance and \(1+\) its grant-fanout allowance without later reclamation. Child-ticket issuance has its own atomic transition: it checks a live parent, identical issuer/epoch/grant, authorized delegation, holder/audience attenuation, equal or receiver-approved attenuated scope and service class, artifact-kind inclusion, mechanically checked child-predicate implication, equal or approved stricter contract, no later expiry, positive redemption allowance, parent resource/redemption balance, and parent descendant-fanout balance; it reserves the full work allocation and consumes \(1+\) child fanout before visibility.

A terminal root ticket returns only unused resource/redemption allocation and moves actual spend and consumed redemptions into the grant's finalized counters. A terminal child ticket atomically removes its full reserved ceiling/redemption allowance from the parent ticket and adds the child's actual spend/consumed redemptions to the parent's counters. A terminal child grant analogously subtracts its full resource/redemption reservation from its parent grant while adding the child's complete finalized spend/redemptions to that parent. All terminal transitions are digest-first idempotent, require no live descendants, and never reclaim issue/fanout authority. Thus neither zero-work child creation nor nonzero child-grant spend can create objects, tombstones, or recycled ancestor capacity beyond the root bounds.

Each reservation atomically reserves both its vector and one redemption slot and binds `(ticketID, redemptionActionID, requestDigest, candidateCID)` before closure fetch or expensive checking. Replay with the same digest returns the prior record; a different digest is equivocation. Its durable state is

\[
\texttt{RESERVED}
\longrightarrow
\texttt{RUNNING}(\textit{executionActionID},\textit{principal},\textit{meterID})
\longrightarrow
\texttt{FINALIZED}.
\]

Exactly one atomic execution claim may start protected work. It has a receiver-derived expiry bounded by both reservation expiry and a frozen maximum duration in crash-safe `ReceiverTime(writerTimeEpoch, monotonicTick)`. Every writer activation durably advances the time epoch; prior-epoch deadlines expire and prior-epoch running claims recovery-finalize before new protected work, so clock reset cannot extend a claim. Every paid subaction binds that exact running reservation, execution ID, and authenticated principal and passes one crash-durable receiver meter/hard envelope. Claimant-reported use is never authoritative. `FinalizeReservation` derives validation/promotion spend from that meter; each component records authoritative metering or a conservative bound fixed by claim time, up to the full remaining component. An unclaimed cancellation releases its resource vector but consumes its redemption slot; a running claim never returns to `RESERVED`, and hung/crashed execution finalizes `UNKNOWN` with authoritative plus conservative-gap charges.

The local-authority transaction records optional promotion, released balance, ticket counters, the immutable settlement, authoritative references that make staged local bytes durably retained, in-transaction graph/index metadata, and deterministic outbox intents. Its promotion vector charges that retained-byte/storage allocation and every mutation inside the same authority transaction. Atomicity never extends to an external object-store copy, another database/index, or remote replication. Referenced bytes may be staged only in an inert non-admitted namespace, checked, and metered as pre-verdict staging; an unreferenced orphan is garbage-collectable. Actual external copying, indexing, replication, and notification effects MUST originate only from a `PROMOTE` outbox intent and use a distinct ticket/reservation/claim afterward; an outbox intent supplies no authority and remains `PENDING` until separately funded completion. No later transition may promote or charge the already settled reservation. A publicly visible offer therefore cannot be stolen and spent as a bearer ticket; sibling tickets cannot oversubscribe one grant; concurrent claims cannot multiply one reservation; zero reports cannot recycle actual use; and finalized allocation cannot be resurrected.

The receiver issues demand for a local work item, requested dependency, selected interest subscription, curated namespace, reproduction/diversity request, or bounded exploration lane. It may issue a local grant and then a local ticket, reservation, and execution claim for autonomous work; no sponsor or program is required, and Core v0 has no unaccounted grant-direct checking path. `AdmissionCheck` follows the exact object type: formal evidence needs its mechanical contract, while a heuristic partial may pass only bounded schema/scope/sandbox checks and remains non-supporting. Promotion is not support, and self-asserted importance, dependency fanout, novelty, or checker acceptance cannot bypass demand admission. The exact schemas, issuance, reservation, claim, metering, settlement, cancellation, and expiry behavior are normative in [Cooperation Core section 2.2](../spec/COOPERATION-CORE-v0.md).

## 6. Proof-carrying stable knowledge

Every reusable justification, and every receiver decision to rely on it, binds:

- exact signed judgment and receiver-local `RelianceQuery`; a producer work item is optional;
- theory and context roots;
- evidence contract and acceptance procedure;
- proof/certificate and complete relevant dependencies;
- checker/verifier profile, binary, options, adapter, and policy epoch;
- axioms, unsafe features, and side conditions;
- composition and fidelity witnesses where the reliance query requires them.

The normative construction is [Cooperation Core section 5](../spec/COOPERATION-CORE-v0.md). A justification has a signed head and finite signed prerequisites. Locally accepted direct evidence is a zero-dependency justification. One signed least fixed point \(K_P\) permits mixed support/refutation composition; \(D_P\) and \(R_P\) are its projections. The strict signed fixed point \(U_P^{\mathrm{strict}}\) recursively excludes both polarities of every exactly disputed judgment.

\[
\operatorname{Stable}_P(q;A,O)\iff
\exists T:
\begin{aligned}[t]
&\operatorname{root}(T)=\operatorname{requiredSignedJudgment}(q)\\
&\land\operatorname{FiniteActiveTree}_P(T)\\
&\land\operatorname{CheckContract}_P(\operatorname{Contract}(q),T)
=\texttt{ACCEPT}\\
&\land\operatorname{ExactContextMatch}(q,T)
\land\operatorname{ClosureAvailable}(T,O).
\end{aligned}
\]

Every node in \(T\) belongs to \(U_P^{\mathrm{strict}}\). The tree-level contract check binds permitted axioms, validation bases, reuse class/native availability, exact reviewer scopes, composition evidence, and required failure-domain diversity, preventing evidence accepted for a permissive query from leaking into a stricter query with the same judgment. A work item deterministically supplies one such query when applicable; standalone evidence is queried directly. Publisher/authorship identity, raw identity or reviewer counts, popularity, scheduler rank, remote `ACCEPT`, and foreign admission are absent from formal closure. An exact receiver-authorized reviewer or failure-domain principal may satisfy only the named contract that explicitly requires it; that operational fact never establishes theorem truth by itself.

## 7. Grounded support

The central safety statement is:

\[
\operatorname{Stable}_{P_i}(q;A_i,O_i)
\Longrightarrow
\exists T:
\begin{array}{l}
T\text{ is a finite signed tree rooted at the signed judgment required by }q;\\
\text{every leaf is receiver-locally accepted and context-bound;}\\
\text{every internal composition is locally checked;}\\
\text{the exact tree satisfies }q\text{'s exact acceptance contract;}\\
\text{no active defect intersects }T;\\
\text{no remote identity, count, ranking, or foreign admission is a premise.}
\end{array}
\]

Because all justification dependencies are finite, every element of a least fixed point has a finite rank. Induction on rank proves the statement. A malicious cycle \(A\leftarrow B\leftarrow A\) without an accepted leaf has no finite rank and supports nothing. Exact `(1,1)` state closes neither polarity in the strict profile. Explicit induction, coinduction, or fixed-point mathematics uses separate formal rules; it cannot exploit graph cycles as evidence.

## 8. Evidence bases

| Basis | Automatic closure rule | Main trust base |
|---|---|---|
| Local native replay | P0 preferred | Exact environment, small checker, local runtime |
| Domain certificate | P0 preferred when available | Certificate checker and its correctness relation |
| Succinct argument | Later, after cost/TCB threshold | Encoded relation, proof system/VM, cryptography, verifier key/setup |
| Signed remote attestation | Hint by default | Signature plus trusted remote operator and complete remote stack |
| Human/agent review | Provisional unless local policy authorizes role | Named local review process and exact rubric |

A valid signature authenticates that a key asserted a result; it does not establish the result. Succinct-verifier acceptance implies the encoded existential relation only up to the proof system's declared negligible computational-soundness error and TCB. The receiver must pin and validate setup/public parameters and bind the verifier key or universal-circuit commitment to the exact encoded relation, proof system, and security parameter; a well-formed key for another relation is irrelevant. Knowledge soundness is a separate requirement when possession or extractability of a witness is claimed. Acceptance does not establish that a native checker execution occurred and does not strengthen the relation, its implementation, or the mathematical formalization. Succinct arguments are not current strict-P0 bases; one without an available native artifact closure is additionally `OPAQUE_RELIANCE` and cannot satisfy a public reusable-knowledge contract.

## 9. Dependency boundaries

Record four closures separately:

1. logical declarations, definitions, axioms, and proof terms;
2. elaboration/build parser, macros, plugins, packages, compiler, and sources;
3. execution program, runtime, inputs, solver, and certificate checker;
4. semantic theory, context, translation, side conditions, and obligation contract.

No mutable lookup or network access is allowed during validation. Declared and measured logical dependencies must agree for the accepted adapter. Hidden imports, prohibited axioms, unsafe/native shortcuts, unsupported features, and unresolved closure facts fail closed. Closure traversal has node, depth, fanout, byte, and term-size limits.

## 10. Sandboxing

Separate isolation tiers for parsing, unpacking, elaboration/build, small checking, agent execution, and checkpoint restoration.

Hostile jobs receive:

- no ambient credentials or network;
- read-only admitted object storage;
- fresh bounded temporary storage;
- non-root principals;
- syscall/device restrictions or microVM isolation for multi-tenancy;
- CPU/fuel, wall-time, memory, process, file, inode, output, and I/O ceilings;
- `UNKNOWN(RESOURCE_LIMIT)` when declared time/fuel/memory bounds end without a verdict, `REJECT` for declared malformedness or certificate invalidity, and `ERROR` only for unexpected checker/sandbox/runtime integrity failure.

Parsers stream and reject duplicate keys, excessive nesting, decompression bombs, archive path/symlink traversal, oversized graphs, and unsafe checkpoint serialization. A container digest alone is neither a security boundary nor a reproducibility proof.

## 11. Malicious workflow containment

### Publication hints

An unsolicited `PublicationHint` is a bounded expiring availability claim, not a candidate admission, validation request, storage contract, unbounded forwarding mandate, or task. Before a receiver selects it and creates a reservation, it may alter only a separate expendable hint cache, bounded telemetry, advisory ranking, and quota-charged dissemination of the same bounded frame through a matching authenticated subscription/home shard. Dissemination requires locally canonicalized discovery keys, deduplication, decreasing TTL/hop bounds, and fixed per-home/per-key/per-receiver quotas; it cannot fetch or forward payload closures and cannot recursively amplify beyond those quotas. Enforce strict frame size, hint count, discovery-key count, provider count, TTL, per-peer/shard rate, and aggregate anonymous quotas. Endpoint rotation cannot multiply these limits. Fetch payloads lazily only after receiver demand.

### Challenges

An unverified challenge is a bounded attention signal. It cannot invalidate support. Checked opposite-polarity evidence changes the strict conflict view without deleting either raw side; a confirmed dependency/checker defect or immutable locally admitted reliance override may separately block a path. Override facts name exact prior IDs they supersede; the supersession graph is acyclic, and concurrent incomparable release/blocking actions resolve fail-closed until an authorized fact explicitly supersedes all competitors. Every event that can change accepted justifications, grounded/strict signed sets, path blocks, contract results, or closure availability publishes the new state, conservative dirty signed roots, and next reliance epoch in one linearizable transaction. If one atomic tuple is unavailable, an in-progress epoch makes affected queries return `STALE`/`UNKNOWN` until a second durable epoch advance completes or recovery conservatively dirties the partition. An older cached result yields no acceptance unless its exact finite tree is rechecked under one current epoch snapshot and the epoch is re-read unchanged immediately before response; mere claimed disjointness from partially traversed dirty nodes is insufficient. Reverse-impact traversal is resumable and processes a bounded number of edges per step. This makes proof-then-counterexample and counterexample-then-proof cache races fail closed while preserving a separately rechecked clean alternative.

### Decompositions

Proposals cannot spawn children until a receiver atomically reserves child demand/resource tickets. Alternative plans share the parent envelope. A decomposition cannot weaken the parent acceptance or fidelity contract; `remainder=EMPTY` requires a coverage certificate. Ordinary dependency cycles are rejected or converted to an explicit cycle-breaking obligation. Composition runs only through an approved content-addressed checker, not arbitrary proposal-supplied code.

### Failure capsules

Use `HINT`, `REPRODUCED_RUN`, and `CERTIFIED_EXHAUSTION`. Only certified exhaustion plus checked search-region containment may suppress an attempt. Failures never refute a theorem.

### Leases and capability ads

Self-reports are advisory. New endpoints receive small probe allocations. Heartbeats cannot renew duplicate suppression beyond a maximum interval without validated progress. Progressive routing contacts previously untried cells and work stealing recovers from blackholes. Endpoint renaming does not multiply aggregate onboarding quotas or diversity weight.

### Search and caches

Provider records, semantic rankings, remote cache results, and failure-domain claims are hints. Verify payloads by CID and evidence contract. Candidate/negative traffic uses separate bounded cache classes and cannot evict stable positives. Similarity never merges mathematics. Mandatory diversity treats unknown or self-reported lineage as correlated unless the receiver has measured or authorized contrary evidence.

### Valid but unwanted content

Checker acceptance does not grant storage or replication. Distinct valid tautologies, vacuous formalizations, artificial contexts, and declared high-importance facts remain bounded by demand tickets, exploration quotas, and locally computed utility. Live protocol behavior has no frozen root or global usefulness metric. External evaluation suites may freeze benchmark tasks and weights without exposing those annotations to ordinary admission or scheduling.

### Formalization fidelity

A proof of a wrong, vacuous, or assumption-strengthened formalization closes only that exact formal judgment. Any informal parent requires its separate fidelity justification. If fidelity is nonmechanical, the exact authorized reviewer principal and `REVIEWED` reliance grade remain visible.

### Prompt and checkpoint content

Natural-language fields are quoted untrusted data. They cannot modify system instructions, grant tools, or authorize side effects. Foreign checkpoints are data-only or resume in a fresh sandbox.

## 12. Receiver-issued capabilities

A capability may bind:

```text
issuer cell and active authorization epoch
capability ID and parent capability ID
holder subject key
allowed actions/message types
allowed ticket/reservation/execution IDs, principals, or maximum already-reserved per-action vector
nonreclaimable child-capability fanout
finite nonreclaimable fresh-action-record allowance
scope, expiry, and unique action ID
```

The capability is permission-only with respect to mathematical work and has no independent work spend vector. Its finite action-record allowance pays only bounded authorization-ledger bookkeeping from the receiver's aggregate control reserve; it cannot fund CPU, artifact storage, validation, retention, replication, bandwidth, or attention. A protected resource action must additionally name the exact unique `RUNNING` reservation, execution action ID, and authenticated execution principal whose ticket, scope, candidate, and receiver meter authorize that action. A capability caveat can narrow those bindings or impose a ceiling no larger than the reserved vector; it cannot mint, reserve, claim, meter, or enlarge work resources. Every fresh accepted capability action atomically consumes one unit of its finite action-record allowance; rejected fresh IDs create no durable per-ID record. Child-capability issuance checks exact parent binding and strict attenuation, then atomically and nonreclaimably consumes both \(1+\) the child's delegated fanout allowance and \(1+\) the child's complete action-record allowance from its parent before visibility. Thus root limits bound both capability objects and accepted replay records across the whole preauthorized subtree. Actual child work separately requires a child demand ticket, reservation, and unique metered execution whose work allocation is reserved from its parent.

The issuing cell keeps an atomic, crash-recoverable authorization ledger. Duplicate `actionID` delivery with the same digest returns the prior result without a second debit; a different digest is equivocation. A new request must prove possession of the holder key, match scope and exact execution caveats, use an active unrevoked epoch, and atomically check/debit its nonreclaimable action allowance at its issuer. Expiry, child retirement, and epoch compaction never restore allowance; a retired epoch rejects every fresh action. Caveat attenuation does not by itself prevent replay; the bounded action ledger supplies idempotence, while the grant/ticket/reservation/claim/meter ledger alone supplies resource conservation.

Each cell also enforces aggregate unauthenticated ingress, onboarding, publication-hint key/fanout, coordination-scope creation, and service-class-admission limits. A sender-created identity, topic, namespace, goal, or coordination scope cannot mint a positive-share queue. This supplies receiver-side bounded exposure without making real-world human identity a prerequisite. A global shared budget is optional and requires preallocated nonoverlapping escrow or consensus over the narrow spend state; otherwise only issuer-local bounds are claimed.

## 13. P0 adversarial gates

1. Forged remote `ACCEPT`, review, priority, cancellation, and policy assertions do not alter stable state.
2. A weaker, malicious, or equal-policy independent peer's admitted fact does not enter the receiver's \(A_i\) without receiver-local admission.
3. A two-node or thousand-node circular signed-support graph supports nothing without an accepted leaf.
4. A direct checked counterexample closes `REFUTE`; mixed-polarity prerequisites compose; exact `(1,1)` closes neither polarity; a clean alternative tree survives.
5. Challenge floods consume bounded resources and do not invalidate valid support.
6. A high-fanout defect or ordinary exact opposite-polarity admission publishes the fact, dirty seeds, and next epoch at one linearization point and immediately prevents stale reuse while every recomputation step remains bounded; clean alternatives survive after exact current-tree checking.
7. False failure capsules suppress no strategy; certified finite-region exhaustion suppresses only checked subsets.
8. Concurrent, duplicated, reordered, partitioned, and crash-recovered grant/ticket issuance, ticket/grant finalization, capability actions, demand reservations/claims, and cancellation preserve issuer-local resource, redemption, nonreclaimable ticket/grant/capability fanout, and capability action-record bounds.
9. Unlimited alternative decompositions remain inside one atomically reserved descendant budget.
10. A blackholing lease holder or poisoned initial top-\(k\) cannot suppress progressive retry.
11. Pseudonymous endpoint churn receives only aggregate bounded onboarding work and no false diversity credit.
12. Candidate, negative, unique-CID, and valid-tautology floods do not evict the protected working set or exceed demand/exploration reservations; public offers cannot be consumed as bearer authority.
13. Semantic-index poisoning changes only bounded discovery/routing, never equivalence, support, or merge.
14. Corrupt provider bytes fail CID checking; provider blackholes cause bounded fallback or explicit unavailability.
15. Proof, term, archive, decompression, graph, build, and checkpoint bombs terminate within ceilings.
16. Hidden network/package access and mutable dependencies are rejected.
17. Transport without checked target-side evidence cannot close an obligation.
18. A correct proof of a seeded wrong/vacuous formalization cannot close its semantic-intent parent.
19. Every delivery order of concurrent quarantine, release, supersession, and duplicate override facts produces the same fail-closed active-override view.
20. Malicious admitted load below every declared resource/class envelope does not starve honest fair-share work or mandatory validation.
21. A proof admitted under a forbidden axiom, weaker validation basis, or wrong reviewer scope cannot close a stricter obligation with the same root judgment.
22. Rejected, unknown, errored, expired-in-flight, and crash-recovered validation attempts charge receiver-authoritative pre-verdict work plus conservative bounds for measurement gaps; claimant reports cannot release capacity, actual external promotion effects cannot run before `PROMOTE`, and each later effect uses a separate funded execution.
23. A malicious member claiming matching policy roots cannot inject an admitted fact by inter-cell anti-entropy; same-authority replica merge is tested only under the declared crash-fault model.
24. At least \(10^5\) unique hints from rotating endpoints remain within aggregate hint quotas, cause no closure fetch, validation, protected indexing, child creation, or payload replication, and cause no hint forwarding outside bounded matching subscription/home-shard quotas.
25. Sender-created goals, topics, namespaces, identities, or coordination scopes do not increase the finite receiver service-class count or reserved queue shares.
26. An optional coordination organizer cannot mint a receiver's grant, weaken a work item's contract, cancel unrelated autonomous work, or revoke already valid mathematical evidence.
27. Changing only evaluation-suite targets, weights, or hidden labels changes no live admission, promotion, scheduler input, or stable-support decision.
28. A valid artifact from unrelated prior work is reusable when its exact closure and support tree satisfy the receiver's contract; missing producer-purpose or program metadata is not a rejection reason.
29. After a root ticket, child ticket, or grant reaches `TERMINAL`, replay of an existing identical action returns its stored result while every fresh issuance, reservation, or execution-claim action fails; a sibling cannot spend released capacity concurrently with a resurrected allocation.
30. Child-ticket attempts that cross grants, extend expiry, widen holder/audience, artifact kinds, predicate, contract, admission scope, service class, or descendant fanout, or exceed parent vector/redemption/count balance are rejected before child visibility.
31. A capability and a full-ceiling ticket cannot authorize two resource spends: the capability has no resource balance, and every protected action binds the exact unique running reservation, execution ID, principal, and receiver meter.
32. Competing settle/promote requests produce one immutable `FinalizeReservation` result whose spend equals per-component authoritative/conservative accounting; the local transaction may create nonauthorizing outbox intents but cannot claim external atomic effects, and no crash or replay exposes a settled-but-later-promotable or underreported intermediate state.
33. Thirty-two concurrent execution claims for one reservation commit exactly one `RUNNING` binding; losing claimants receive no protected service, and the winner's aggregate parallel subactions stay inside one hard envelope.
34. An untrusted zero-use report after nonzero protected work cannot reduce spend. Missing, rolled-back, or integrity-alarmed measurement charges the frozen conservative bound, potentially the full reservation.
35. A running claim's receiver-derived expiry is bounded by both reservation expiry and a frozen maximum execution duration in crash-safe receiver time; writer restart advances the time epoch and recovery-finalizes old running claims before new work, so a hung claim never returns to `RESERVED` or extends through clock reset.
36. Reserve/cancel with `maxRedemptions=1` consumes the sole redemption slot, so zero-resource cancellation cannot generate an unbounded settlement/tombstone loop.
37. Nested zero-work child ticket/grant create/terminalize loops stop at the root's nonreclaimable issue/fanout allowances even though unused resource/redemption allocation may be released.
38. Cache `ACCEPT` followed by a locally checked exact opposite-polarity justification produces immediate non-acceptance before reverse traversal; the final epoch is re-read before any current acceptance is emitted.
39. Root grant/ticket constructors reject nonabsent parent tags, and child transitions reject absent or nonmatching parents; root and child accounting classifications cannot diverge.
40. A flood of distinct authenticated capability actions cannot create more replay records than the root capability subtree's finite nonreclaimable action allowance; the final unit is an atomic debit, rejected IDs are not retained individually, and compaction restores no allowance.
41. A nonzero-spend child grant rolls its complete finalized spend/redemptions into the parent while removing its full reserved allocation; terminalization cannot release the full allocation and thereby fund a sibling replay of already spent capacity.
42. Crash at every fact/dirty-seed/reliance-epoch publication boundary yields the old tuple, new tuple, or fail-closed in-progress state, never a new current epoch followed by later fact visibility under that unchanged epoch.
43. Crash at staged-object, settlement/admission, outbox, and external-effect boundaries yields only garbage-collectable inert staging, one local commit plus pending intent, or a separately funded completed effect; no post-settlement work spends the old reservation.
44. A forbidden-axiom derivation paired with an unrelated or fabricated clean attestation fails: local acceptance applies policy to the receiver-replayed footprint and any corroborating attestation must exactly bind proof, accepted result, checker, environment, policy, and measured footprints under a valid authorized signature.

## 14. Hard limit

Trustworthy mathematical work and reuse can postpone political attribution. They cannot postpone operational principals, authorization, demand admission, resource control, and explicit semantic-review trust where those roles affect the result. A fully anonymous, permissionless system with unlimited unique submissions cannot guarantee queue liveness, storage preservation, routing integrity, fair allocation, or eclipse resistance. DTMKN therefore uses authenticated cells, bounded gateways, scoped operational capabilities, receiver-owned service classes, and demand tickets in P0 while preserving receiver-local evidence as the basis of mathematical correctness. None of these controls requires a shared research program.
