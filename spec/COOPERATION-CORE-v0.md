# DTMKN Cooperation Core v0

## 1. Status

This is a technical pre-specification for `CP-002`. It describes autonomous mathematical work, publication, trustworthy reuse, and optional cooperation. It includes the operational identities and authorities required for resource safety, control integrity, semantic-review contracts, and failure-domain measurement. It deliberately omits political attribution, publication priority, prestige, payments, and constitutional governance.

A valid execution requires no campaign, shared root goal, sponsor, common budget, or common stopping rule. Coordination is secondary to end-to-end mathematical efficacy and reliability; every coordination mechanism is an optional execution policy whose marginal benefit and overhead must be measured.

## 2. System model

Let:

- \(\mathcal A\): agents;
- \(\mathcal B\): federated blackboard cells;
- \(\mathcal O\): immutable typed objects;
- \(R_i\): bounded raw-frame buffer at cell \(i\);
- \(Q_i\): bounded schema-valid candidate/quarantine store;
- \(A_i\): locally admitted durable facts;
- \(O_i\subseteq\mathcal O\): locally available admitted objects;
- \(P_i\): local scheduling, acceptance, retention, and view policy.

These are distinct operational stores connected by transitions

\[
R_i\longrightarrow Q_i\longrightarrow A_i,
\]

not nested sets. A durable fact may outlive the raw frame and quarantine entry from which it was derived.

For a candidate delta \(\Delta_{j\to i}\subseteq A_j\) advertised by cell \(j\), receiver \(i\) computes:

\[
N_i=
\{f\in\Delta_{j\to i}\mid
\operatorname{Admit}_{P_i}(f,\operatorname{Closure}(f))
=\texttt{ACCEPT}\},
\qquad
A_i'=A_i\cup N_i.
\]

Foreign admission is never authority: \(f\in A_j\) does not imply \(f\in A_i\). Matching authentication, schema, admission-policy, validation-root, or policy-epoch identifiers does not change this rule. Every independently operated cell transports only candidate fact identifiers and required closures, and the receiver re-admits them.

Direct set union is restricted to immutable facts already committed by the **same logical cell and admission authority** and copied among its replicas. Core v0 gives that replica set a crash-fault model: a replica may stop, restart, lose, delay, duplicate, or reorder messages, but it cannot fabricate an admission decision. A fact carries the authority's committed admission-decision identifier. Control/spend state is never merged by set union. If replicas may be Byzantine, they must instead use receiver re-admission or a separately specified narrow BFT admission log. Two independently operated cells are never one replica set merely because their policy roots match.

Raw or quarantined input is not durable anti-entropy state and cannot evict stable objects or alter a stable view. Within the preceding same-authority crash-fault boundary, immutable admitted-fact merge is associative, commutative, and idempotent. Mutable-looking statuses are deterministic projections \(V_{P_i}(A_i,O_i)\). Leases, load, queue delay, and capability summaries are ephemeral hints; their loss may waste resources but cannot invalidate accepted evidence.

The protocol is at-least-once. Duplicate messages, attempts, and object transfers are expected.

### 2.1 Operational authorization

Political identity is optional. Operational identity is P0 where a protocol role depends on it: cells and validators may have stable, rotating service principals; workers use short-lived session keys. Every mutating control request requires authenticated proof of possession and receiver-issued authority. A capability has at least:

\[
\tau=\operatorname{Auth}_{k_i}(
i,e,\operatorname{capID},\operatorname{parentID},pk_s,
\operatorname{scope},\operatorname{fanoutLimit},\operatorname{actionRecordLimit},
\operatorname{reservationCaveats},\operatorname{expiry}).
\]

Here \(i\) is the issuing cell, \(e\) is its active authorization epoch, and \(pk_s\) is the holder's ephemeral subject key. `actionRecordLimit` is a finite canonical nonnegative allowance for the complete fresh-action subtree. `Auth` is schematic: CP-002 must select a caveat-bearing MAC or signature construction and an idempotent authorization ledger. A bare bearer MAC plus a nonce does not prevent replay or concurrent use.

Capabilities authorize actions or roles such as child-ticket requests, cancellation, lease renewal, quarantine, validation, or semantic review. They are **permission-only** with respect to mathematical work: they carry no CPU, artifact-storage, bandwidth, validation, retention, replication, or attention vector. Their finite `actionRecordLimit` funds only issuer authorization-ledger bookkeeping from a separately bounded aggregate control reserve; it is not transferable work authority. Every accepted action that can consume protected resources beyond that fixed control/ingress reserve must bind the unique `RUNNING` execution claim of one `DemandReservation`, including its exact execution action ID and authenticated execution principal. Capability caveats may restrict admissible `ticketID`, reservation IDs, execution IDs, or principals and may impose a per-action upper bound no larger than the bound already reserved, but cannot create or enlarge a work allocation. Capabilities do not establish mathematical correctness, authorship, priority, or prestige.

The issuer maintains an atomic, crash-recoverable authorization ledger. For every new accepted control request \(q\):

\[
\begin{aligned}
\operatorname{AcceptControl}_i(q)\Longrightarrow {}&
\operatorname{issuer}(q)=i
\land\operatorname{VerifyPoP}(pk_s,q)\\
&\land\operatorname{action}(q)\in\operatorname{scope}(\tau)
\land\operatorname{epoch}(\tau)=e_i\\
&\land\operatorname{NotExpired}_i(\tau)
\land\operatorname{NotRevoked}_i(\tau)\\
&\land\operatorname{requestDigest}_i[
  \operatorname{capID},\operatorname{actionID}(q)]
  \in\{\bot,H(q)\}\\
&\land\operatorname{consumedActionAllowance}_i[\tau]+1
  \leq\operatorname{actionRecordLimit}(\tau)\\
&\land\bigl(
  \neg\operatorname{ConsumesProtectedResource}_i(q)
  \lor(\exists! z,x,h:\operatorname{RunningExecution}_i(z,x,h)
  \land\operatorname{reservationID}(q)=\operatorname{reservationID}(z)
  \land\operatorname{executionActionID}(q)=x
  \land\operatorname{ExecutionPrincipal}(q)=h
  \land\operatorname{ReservationAuthorizes}_i(z,q)
  \land\operatorname{MeterAdmits}_i(z,x,h,q)
  \land\operatorname{CapabilityCaveatsMatch}_i(\tau,z,x,h,q))
  \bigr).
\end{aligned}
\]

Every mutating request binds a unique `actionID`. The issuer first looks up an existing `(capID, actionID)` record: the same request digest returns the prior result even after expiry, while a different digest is rejected as equivocation. For an ordinary fresh accepted request, the same authorization-ledger commit atomically adds one to `consumedActionAllowance` and creates its replay record; a rejected fresh ID creates no per-ID durable state beyond bounded aggregate abuse telemetry. Freshness, revocation, role, caveat, unique-running-execution binding, metering, and fanout checks apply only when no record exists. `MeterAdmits` is an atomic receiver-side debit or hard-envelope check against the one execution meter; claimant-reported usage never satisfies it. A root capability must carry the canonical absent parent tag. Child-capability issuance is an idempotent receiver transition. For parent \(p\) and child \(c\), it requires authorized issuance, exact `parentID(c)=capID(p)`, strictly attenuated scope/reservation caveats and expiry, and

\[
\begin{aligned}
\operatorname{consumedFanout}[p]+1+\operatorname{fanoutLimit}[c]
&\leq\operatorname{fanoutLimit}[p],\\
\operatorname{consumedActionAllowance}[p]+1+\operatorname{actionRecordLimit}[c]
&\leq\operatorname{actionRecordLimit}[p].
\end{aligned}
\]

For child issuance, the \(+1\) in \(1+\operatorname{actionRecordLimit}[c]\) is the issuance action's own replay-record debit: the specialized commit atomically adds that entire quantity once, rather than adding a second generic unit. It also atomically adds \(1+\operatorname{fanoutLimit}[c]\) to `consumedFanout[p]` before child visibility; neither allocation is reclaimed. Each child separately satisfies \(\operatorname{consumedActionAllowance}[c]\leq\operatorname{actionRecordLimit}[c]\). Thus root allowances bound both the complete capability-object subtree and every durable accepted-action record beneath it. Retired authorization epochs may compact bounded replay records into authenticated terminal summaries under a frozen replay-retention rule, but every fresh action against a retired epoch fails and compaction can never restore either allowance. This authorization accounting allocates only bounded control-ledger bookkeeping, never mathematical-work resources. Child task or ticket creation separately reserves work budget through section 2.2. A federation-wide work budget therefore requires pre-partitioned nonoverlapping escrow or consensus over the narrow grant/ticket ledger; capability replication never supplies work-resource conservation.

Anonymous candidates are allowed through bounded gateways. A remote control action without the required capability is ignored.

### 2.2 Demand-scoped admission

Every paid local or imported action descends from a receiver-issued ledger account:

Every receiver-local authority identifier is a tagged tuple

\[
\operatorname{ReceiverLocalID}=(\operatorname{issuerCell},
\operatorname{issuerEpoch},\operatorname{localID}).
\]

The abbreviated `budgetGrantID`, `admissionScopeID`, and `serviceClassID` fields below always have this type. Their issuer and epoch must equal those of the enclosing receiver-issued object. A sender-created bare name, topic, goal, namespace, or coordination scope is not a receiver-local authority identifier.

```text
BudgetGrant {
  budgetGrantID: ReceiverLocalID
  issuerCell
  issuerEpoch
  parentBudgetGrantID?: ReceiverLocalID
  holderOrLocalPolicy: HOLDER(subjectKey) | LOCAL_POLICY(policyRef)
  admittedServiceClassIDs[]: ReceiverLocalID
  admittedScopeIDs[]: ReceiverLocalID
  totalCeilingVector
  totalRedemptionAllowance
  ticketIssueLimit
  childGrantLimit
  expiry
}
```

A grant is a root grant exactly when `parentBudgetGrantID` carries the canonical absent tag. The root-grant constructor MUST reject every nonabsent parent field. A child-grant transition MUST instead bind `parentBudgetGrantID(c)` to the exact parent grant ID before reserving any authority. No authenticated object can be treated as a root by allocation or terminal accounting while carrying a parent reference.

A receiver may issue a grant to its own local research policy. A grant is resource authority, not mathematical or scheduling evidence. Core v0 has no grant-direct paid action: autonomous local checking also obtains a local ticket, reservation, and unique execution claim. Child grants and tickets reserve their complete vector ceilings and redemption allowances from the grant before becoming usable.

Each grant and ticket has a crash-recoverable allocation state in `ACTIVE | TERMINAL`, initially `ACTIVE`. Define `GrantAllocationLive_i(g)` and `TicketAllocationLive_i(d)` to mean that the authenticated object exists in issuer \(i\)'s authoritative ledger and its durable state is `ACTIVE`. For an issuer-qualified grant ID \(h\), `GrantNotExpired_i(h)` and `GrantNotRevoked_i(h)` mean the corresponding checks on the unique authenticated grant object stored under \(h\); absence or ambiguity is false. Live-state predicates are about unreclaimed allocation, not freshness: expiry or revocation may block new work while terminal accounting remains possible. A terminal transition writes an irreversible tombstone. An idempotent action lookup always occurs before the live-state check, so an exact previously recorded action can still return its stored result after terminalization; a fresh action ID against a terminal object always fails. `ticketIssueLimit` is a nonreclaimable allowance for the complete ticket subtrees issued by a grant, and `childGrantLimit` is a nonreclaimable descendant-grant fanout allowance; neither is a recyclable direct-child counter.

For every grant (g), its crash-recoverable issuer ledger maintains, componentwise,

\[
\operatorname{finalizedSpend}[g]
+\operatorname{reservedTicketCeilings}[g]
+\operatorname{reservedChildGrantCeilings}[g]
\preceq\operatorname{totalCeiling}(g),
\]

and

\[
\operatorname{finalizedRedemptions}[g]
+\operatorname{reservedTicketRedemptions}[g]
+\operatorname{reservedChildGrantRedemptions}[g]
\leq\operatorname{totalRedemptionAllowance}(g).
\]

Here a live ticket contributes its entire unreclaimed `totalCeilingVector` and `maxRedemptions`, not merely what it has already spent. A child grant contributes its entire unreclaimed resource and redemption allocations. Separately,

\[
\operatorname{consumedTicketIssueAllowance}[g]
\leq\operatorname{ticketIssueLimit}(g),
\qquad
\operatorname{consumedGrantFanout}[g]
\leq\operatorname{childGrantLimit}(g).
\]

Both counters are monotone and nonreclaimable. Issuing a root ticket \(d\) consumes \(1+\operatorname{childTicketFanoutLimit}(d)\) units of the grant's ticket-issue allowance. Issuing child grant \(c\) consumes \(\operatorname{ticketIssueLimit}(c)\) units of its parent's ticket-issue allowance and \(1+\operatorname{childGrantLimit}(c)\) units of its parent's grant fanout before visibility. Thus a nested zero-work create/terminalize loop cannot create unbounded tickets, grants, tombstones, or action records.

Proof validity does not create an entitlement to checking, retention, indexing, replication, or attention. A publisher advertises possible object availability with the bounded `PublicationHint` in section 3.2. A receiver may separately advertise willingness to consider a matching candidate with this non-spendable object:

```text
DemandOffer {
  offerID
  receiverCell
  admissionScopeID: ReceiverLocalID
  serviceClassID: ReceiverLocalID
  routingKey
  candidatePredicateRef
  contractRef
  artifactKinds[]
  lanePolicy
  coordinationScopeRef?
  expiry
}
```

An eligible worker or bounded public gateway first obtains a receiver-authenticated authority object:

```text
DemandTicket {
  ticketID: ReceiverLocalID
  issuerCell
  issuerEpoch
  parentTicketID?: ReceiverLocalID
  budgetGrantID: ReceiverLocalID
  authorizationPrincipal: HOLDER(subjectKey) | LOCAL_POLICY(policyRef)
  audience: HOLDER(subjectKey) | PUBLIC_GATEWAY(laneID)
  admissionScopeID: ReceiverLocalID
  serviceClassID: ReceiverLocalID
  candidatePredicateRef
  contractRef
  artifactKinds[]
  totalCeilingVector
  perRedemptionCeilingVector
  maxRedemptions
  childTicketFanoutLimit
  expiry
}
```

Every resource vector is a finite componentwise nonnegative quantity in frozen canonical units. Every redemption allowance, issue limit, capability fanout limit, ticket fanout limit, grant fanout limit, and corresponding counter is a finite canonical nonnegative integer; every issued ticket has positive `maxRedemptions`. Ledger arithmetic over vectors and scalars rejects negativity, overflow, underflow, and noncanonical encodings before state mutation. The resource vector explicitly covers cheap parsing beyond the anonymous ingress allowance, closure fetch, validation, retained bytes, graph insertion, index insertion, replication, and bounded attention/task creation. The issuer signs or MAC-authenticates the complete ticket. A spendable ticket is never an unbound public bearer token. A public offer is claimed through an authenticated control request; if accepted, the receiver creates a worker-bound ticket or authorizes a gateway that atomically creates bounded per-candidate reservations.

For a new idempotent issuance action (a), issuing a root ticket (d) from grant (g) requires one atomic transition satisfying

\[
\begin{aligned}
\operatorname{IssueTicket}_i(g,a,d)\Longrightarrow {}&
\operatorname{VerifyGrant}_i(g)
\land\operatorname{GrantAllocationLive}_i(g)
\land\operatorname{AuthorizedGrantIssuer}_i(g,a)
\land\operatorname{budgetGrantID}(d)=\operatorname{budgetGrantID}(g)\\
&\land\operatorname{parentTicketID}(d)=\texttt{NONE}
\land\operatorname{issuer}(d)=\operatorname{issuer}(g)=i
\land\operatorname{epoch}(d)=\operatorname{epoch}(g)=e_i\\
&\land\operatorname{serviceClassID}(d)\in
\operatorname{admittedServiceClassIDs}(g)\\
&\land\operatorname{admissionScopeID}(d)\in
\operatorname{admittedScopeIDs}(g)
\land\operatorname{expiry}(d)\leq\operatorname{expiry}(g)\\
&\land 1\leq\operatorname{maxRedemptions}(d)
\land\operatorname{perRedemptionCeiling}(d)
\preceq\operatorname{totalCeiling}(d)\\
&\land\operatorname{NotExpired}_i(g)
\land\operatorname{NotRevoked}_i(g)\\
&\land\operatorname{finalizedSpend}_i[g]
+\operatorname{reservedTicketCeilings}_i[g]
+\operatorname{reservedChildGrantCeilings}_i[g]
+\operatorname{totalCeiling}(d)
\preceq\operatorname{totalCeiling}(g)\\
&\land\operatorname{finalizedRedemptions}_i[g]
+\operatorname{reservedTicketRedemptions}_i[g]
+\operatorname{reservedChildGrantRedemptions}_i[g]
+\operatorname{maxRedemptions}(d)
\leq\operatorname{totalRedemptionAllowance}(g)\\
&\land\operatorname{consumedTicketIssueAllowance}_i[g]
+1+\operatorname{childTicketFanoutLimit}(d)
\leq\operatorname{ticketIssueLimit}(g).
\end{aligned}
\]

The action first looks up `(budgetGrantID, issuanceActionID)`: the same digest returns the prior ticket, and a different digest is equivocation. Only a new action performs the checks and atomically records the full ticket resource/redemption allocations and the nonreclaimable \(1+\operatorname{childTicketFanoutLimit}(d)\) issue allowance, creates the ticket in `ACTIVE` state, and then makes it visible. A root ticket is therefore bounded by both its own ledger and its grant; sibling tickets cannot each spend the same grant balance.

Child-grant issuance is a distinct atomic transition with the same issuer/epoch, holder, scope/class, expiry, liveness, authorization, resource, redemption, and idempotence checks against its parent grant. It additionally requires

\[
\operatorname{parentBudgetGrantID}(c)=\operatorname{budgetGrantID}(g),
\]

so a root-form object cannot enter child accounting and a child-form object cannot enter root accounting. Proposed child grant \(c\) is invisible unless

\[
\begin{aligned}
\operatorname{consumedTicketIssueAllowance}[g]
+\operatorname{ticketIssueLimit}(c)
&\leq\operatorname{ticketIssueLimit}(g),\\
\operatorname{consumedGrantFanout}[g]
+1+\operatorname{childGrantLimit}(c)
&\leq\operatorname{childGrantLimit}(g).
\end{aligned}
\]

The commit consumes both allowances nonreclaimably and reserves the child's full resource and redemption ceilings. The child then accounts within its allocated allowances. Terminalization may release unused resource/redemption allocation but never any issue or fanout allowance.

Child tickets use a distinct normative transition. For a new issuance action \(a\), parent ticket \(p\), and proposed child \(c\):

\[
\begin{aligned}
\operatorname{IssueChildTicket}_i(p,a,c)\Longrightarrow {}&
\operatorname{VerifyTicket}_i(p)
\land\operatorname{TicketAllocationLive}_i(p)
\land\operatorname{GrantAllocationLive}_i(\operatorname{budgetGrantID}(p))\\
&\land\operatorname{GrantNotExpired}_i(\operatorname{budgetGrantID}(p))
\land\operatorname{GrantNotRevoked}_i(\operatorname{budgetGrantID}(p))\\
&\land\operatorname{AuthorizedDelegation}_i(p,a,c)
\land\operatorname{parentTicketID}(c)=\operatorname{ticketID}(p)\\
&\land\operatorname{issuer}(c)=\operatorname{issuer}(p)=i
\land\operatorname{epoch}(c)=\operatorname{epoch}(p)=e_i\\
&\land\operatorname{budgetGrantID}(c)=\operatorname{budgetGrantID}(p)
\land\operatorname{PrincipalAttenuates}_i(c,p)
\land\operatorname{AudienceAttenuates}_i(c,p)\\
&\land\operatorname{SameOrApprovedScopeAttenuation}_i(c,p)
\land\operatorname{SameOrApprovedServiceAttenuation}_i(c,p)\\
&\land\operatorname{artifactKinds}(c)\subseteq
\operatorname{artifactKinds}(p)
\land\operatorname{PredicateImplies}_i(c,p)=\texttt{ACCEPT}\\
&\land\operatorname{SameOrApprovedStricterContract}_i(c,p)
\land\operatorname{expiry}(c)\leq\operatorname{expiry}(p)\\
&\land 1\leq\operatorname{maxRedemptions}(c)
\land\operatorname{perRedemptionCeiling}(c)
\preceq\operatorname{totalCeiling}(c)\\
&\land\operatorname{NotExpired}_i(p)
\land\operatorname{NotRevoked}_i(p)\\
&\land\operatorname{spent}_i[p]
+\operatorname{outstandingReservations}_i[p]
+\operatorname{reservedChildren}_i[p]
+\operatorname{totalCeiling}(c)
\preceq\operatorname{totalCeiling}(p)\\
&\land\operatorname{usedRedemptionSlots}_i[p]
+\operatorname{maxRedemptions}(c)
\leq\operatorname{maxRedemptions}(p)\\
&\land\operatorname{consumedTicketFanout}_i[p]
+1+\operatorname{childTicketFanoutLimit}(c)
\leq\operatorname{childTicketFanoutLimit}(p).
\end{aligned}
\]

`AuthorizedDelegation` is satisfied only by the parent ticket's local policy/holder or by a live permission capability containing `ISSUE_CHILD_DEMAND_TICKET` and bound to \(p\); it supplies no additional budget. The two `SameOrApproved...Attenuation` predicates accept equality or a receiver-authenticated attenuation relation in the active epoch. `PredicateImplies_i(c,p)` mechanically verifies that every child-admissible candidate is parent-admissible. `SameOrApprovedStricterContract_i(c,p)` accepts the identical contract or a receiver-approved contract known to be no weaker for this delegation. Principal and audience attenuation prohibit changing a holder-bound parent into a public or unrelated audience.

The issuer first looks up `(ticketID(p), issuanceActionID)`: the same complete-child digest returns the previously recorded child even after \(p\) becomes terminal, and a different digest is equivocation. Only a new key executes the guards. In one commit, the transition reserves the child's full resource vector and redemption allowance in \(p\), adds \(1+\operatorname{childTicketFanoutLimit}(c)\) to the parent's nonreclaimable `consumedTicketFanout`, creates \(c\) in `ACTIVE` state, and only then makes \(c\) visible. No child with a cross-grant reference, widened predicate, artifact kind, scope, service class, contract, principal, audience, expiry, or fanout is valid merely because it carries a receiver signature.

Each root or child ticket has a crash-recoverable issuer-local ledger satisfying, componentwise,

\[
\operatorname{spent}[d]
+\operatorname{outstandingReservations}[d]
+\operatorname{reservedChildren}[d]
\preceq \operatorname{ceiling}[d],
\]

and its settled plus outstanding redemption count plus redemption allowances reserved for children never exceeds `maxRedemptions`. It also maintains

\[
\operatorname{consumedTicketFanout}[d]
\leq\operatorname{childTicketFanoutLimit}(d),
\]

where the counter is monotone and never reclaimed. Every issued ticket has positive `maxRedemptions`; resource and redemption allowances bound work, while the separate fanout allowance bounds all descendant ticket objects even when zero work is performed. Tickets are spendable only at their issuing receiver.

Before closure fetch or any expensive validation, the holder or authorized gateway submits a fresh `redemptionActionID`, a request digest, and the candidate CID. The receiver verifies the ticket, audience, epoch, revocation, expiry, cheap scope header, per-redemption bound, cumulative vector, and redemption count in one atomic transition. It then returns an unclaimed reservation. Define

```text
ExecutionPrincipal =
    HOLDER(subjectKey)
  | LOCAL_EXECUTOR(executorID)
  | GATEWAY_SESSION(laneID, subjectKey)
```

Every execution principal is authenticated in the issuer's current operational epoch and must be authorized by the ticket audience or local policy. The reservation commit derives `reservationID` canonically as the issuer-qualified tagged pair `(ticketID, redemptionActionID)`; callers cannot select a second alias for the same redemption.

```text
DemandReservation {
  reservationID: ReceiverLocalID
  ticketID
  redemptionActionID
  requestDigest
  candidateCID
  reservedVector
  reservationExpiry
}

DemandExecutionClaim {
  reservationID: ReceiverLocalID
  ticketID
  redemptionActionID
  executionActionID
  claimDigest
  executionPrincipal: ExecutionPrincipal
  meterRecordID
  claimedAt
  executionExpiry
}

DemandSettlement {
  reservationID: ReceiverLocalID
  ticketID
  redemptionActionID
  requestDigest
  candidateCID
  executionActionID?
  executionPrincipal?: ExecutionPrincipal
  finalizationDigest
  terminalResultDigest?
  meterRecordDigest?
  measurementBasisByComponent:
    ResourceComponent -> NONE_UNCLAIMED | AUTHORITATIVE_METER | CONSERVATIVE_UPPER_BOUND
  outcome
  validationSpentVector
  promotion: NONE | PROMOTED(admissionDecisionID)
  promotionSpentVector
  totalSpentVector
  releasedVector
}
```

Formally, for request \(r\) and requested reservation vector \(b\),

\[
\begin{aligned}
\operatorname{Reserve}_i(d,a,r,b)\Longrightarrow {}&
\operatorname{VerifyTicket}_i(d)
\land\operatorname{TicketAllocationLive}_i(d)
\land\operatorname{AudienceOK}_i(d,r)
\land\operatorname{GrantAllocationLive}_i(\operatorname{budgetGrantID}(d))
\land\operatorname{GrantNotExpired}_i(\operatorname{budgetGrantID}(d))
\land\operatorname{GrantNotRevoked}_i(\operatorname{budgetGrantID}(d))
\land\operatorname{ServiceClassAllowed}_i(d)\\
&\land\operatorname{AdmissionScopeMatch}_i(d,r)
\land\operatorname{CandidateHeaderMatch}(d,r)\\
&\land\operatorname{NotExpired}_i(d)
\land\operatorname{NotRevoked}_i(d)
\land b\preceq\operatorname{perRedemptionCeiling}(d)\\
&\land\operatorname{usedRedemptionSlots}_i[d]+1
\leq\operatorname{maxRedemptions}(d)\\
&\land\operatorname{spent}_i[d]
+\operatorname{outstandingReservations}_i[d]
+\operatorname{reservedChildren}_i[d]+b
\preceq\operatorname{totalCeiling}(d).
\end{aligned}
\]

`usedRedemptionSlots` is the sum of settled redemptions, outstanding reservations, and redemption allowances reserved for child tickets. The resource vector and one redemption slot are reserved in the same transition.

The reservation request is idempotent by `(ticketID, redemptionActionID)`. The issuer first looks up that key: the same request digest returns the recorded reservation or settlement even after ticket or grant terminalization, while a different digest is rejected as equivocation. Ticket/grant liveness, validity, freshness, and debit checks apply only to a new key. A reservation binds the exact candidate CID, and all validation and optional promotion spend must fit its vector.

The issuer ledger maintains the crash-recoverable state machine

\[
\texttt{RESERVED}
\longrightarrow
\texttt{RUNNING}(\textit{executionActionID},\textit{executionPrincipal},
\textit{claimDigest},\textit{meterRecordID})
\longrightarrow
\texttt{FINALIZED}(\textit{settlementID}).
\]

A new reservation starts in `RESERVED`; `RESERVED` and `RUNNING` both count as outstanding until the final transition. Before any receiver-paid fetch, parse, validation, storage, index, graph, replication, or attention operation begins, an authorized execution principal \(h\) submits a fresh execution action ID \(x\) and complete claim digest \(c\). The atomic transition satisfies

\[
\begin{aligned}
\operatorname{ClaimReservation}_i(z,x,h,c)\Longrightarrow {}&
\operatorname{ReservationState}_i(z)=\texttt{RESERVED}
\land\operatorname{VerifyExecutionPrincipal}_i(h,c)\\
&\land\operatorname{ClaimPrincipalAuthorized}_i(z,h)
\land\operatorname{ClaimDigestMatches}_i(z,x,h,c)\\
&\land\operatorname{TicketAllocationLive}_i(\operatorname{ticketID}(z))
\land\operatorname{GrantAllocationLive}_i(\operatorname{budgetGrantID}(z))\\
&\land\operatorname{NotExpired}_i(z)
\land\operatorname{NotExpired}_i(\operatorname{ticketID}(z))
\land\operatorname{GrantNotExpired}_i(\operatorname{budgetGrantID}(z))\\
&\land\operatorname{NotRevoked}_i(\operatorname{ticketID}(z))
\land\operatorname{GrantNotRevoked}_i(\operatorname{budgetGrantID}(z))\\
&\land \operatorname{claimedAt}_i
<\operatorname{executionExpiry}_i(z,c)
\leq\min\!\left(
\operatorname{reservationExpiry}(z),
\operatorname{claimedAt}_i+\operatorname{MaxExecutionDuration}_i(z)
\right).
\end{aligned}
\]

The issuer first looks up `(reservationID, executionActionID)`: an existing identical claim digest returns the stored `DemandExecutionClaim` even after expiry or finalization, while a different digest is equivocation. Only a fresh key checks the guards. Every issuer time is a lexicographically ordered `ReceiverTime(writerTimeEpoch, monotonicTick)`. Before each writer activation, restart, or failover can accept work, it durably increments `writerTimeEpoch` under the single-writer fence; ticks are monotone only within that epoch. A deadline from an earlier writer-time epoch is expired. Recovery finalizes every prior-epoch `RUNNING` claim as `UNKNOWN(EXECUTION_LOST_OR_EXPIRED)`, using authoritative observations plus conservative bounds for all gaps, before the new writer admits protected work. An implementation may replace this conservative expire-on-writer-change rule only with a specified crash-persistent nondecreasing clock whose rollback and uncertainty handling fail closed.

`claimedAt` is the issuer's `ReceiverTime` at the claim commit, `MaxExecutionDuration` is frozen by receiver service class, and `executionExpiry` is receiver-derived as the earlier allowed bound in the same time epoch; none is claimant-extensible. Thus clock reset or repeated reboot cannot extend a reservation, ticket, grant, or running execution. Exactly one claim may atomically change `RESERVED` to `RUNNING`; every conflicting or fresh later claim fails. The same commit creates a crash-durable receiver-controlled meter and a fenced execution admission. No protected executor, sandbox, fetch, or mutating service is exposed before that commit. Every paid subaction is idempotently admitted against the exact `(reservationID, executionActionID, executionPrincipal)` and the single cumulative meter; the issuer enforces

\[
\operatorname{protectedUseUpperBound}_i[z,x]
\preceq\operatorname{reservedVector}(z)
\]

with atomic debits and/or a hard sandbox envelope. Consequently neither concurrent API calls nor replay can make the receiver provide more protected service than the reservation, even when one execution internally uses parallel workers.

Settlement and optional promotion occur in one normative transaction. For a `RUNNING` reservation \(z\) created from ticket \(d\), its unique execution claim \((x,h)\), terminal checker record \(u\), and promotion choice \(m\in\{\texttt{NONE},\texttt{PROMOTE}\}\), the transition derives rather than accepts its spend vectors:

\[
\begin{aligned}
\operatorname{FinalizeReservation}_i(z,x,u,m)\Longrightarrow {}&
\operatorname{RunningExecution}_i(z,x,h)
\land\operatorname{MatchingTerminalResult}_i(z,x,h,u)\\
&\land\operatorname{outcome}(u)\in
\{\texttt{ACCEPT},\texttt{REJECT},\texttt{ERROR},\texttt{UNKNOWN}\}\\
&\land (v,w,\eta)=\operatorname{AuthoritativeAccount}_i(z,x,u,m)\\
&\land \mathbf 0\preceq v
\land \mathbf 0\preceq w
\land v+w\preceq\operatorname{reservedVector}(z)\\
&\land\bigl(m=\texttt{NONE}\Longrightarrow w=\mathbf 0\bigr)\\
&\land\bigl(m=\texttt{PROMOTE}\Longrightarrow
\operatorname{outcome}(u)=\texttt{ACCEPT}
\land\operatorname{PromotionTimely}_i(z,u)\\
&\qquad\land\operatorname{AdmissionScopeMatch}_i(d,u)
\land\operatorname{CandidatePredicateMatch}_i(d,u)\\
&\qquad\land\operatorname{ContractRefMatch}_i(d,u)
\land\operatorname{ClosureResolved}_i(u)\\
&\qquad\land\operatorname{AdmissionCheck}_i(d,u)=\texttt{ACCEPT}
\land\operatorname{RetentionPolicy}_i(d,u)\bigr).
\end{aligned}
\]

`AuthoritativeAccount` is computed only from the issuer's crash-durable meter, sandbox counters, object-store/graph/index transactions, and conservative recovery rules; `WorkReport.measuredResourceVector` and claimant-supplied spend are ignored. Its \(\eta\) output is a total finite map over the resource-vector components, not a scalar summary. With complete trustworthy metering, every charged component maps to \(\texttt{AUTHORITATIVE_METER}\) and the charged vectors equal the authoritative categorized use. If any interval or component is missing, unauthenticated, rolled back, or integrity-alarmed, that affected component maps to \(\texttt{CONSERVATIVE_UPPER_BOUND}\) and is charged at a receiver-declared conservative upper bound fixed no later than claim time; unaffected components retain their authoritative basis. When no smaller sound bound is available, the affected charge is the full remaining reserved component. `NONE_UNCLAIMED` is permitted only for an unclaimed cancellation with zero protected execution. No amount is released on the basis of an untrusted or incomplete report.

The single local-authority commit (1) consumes the unique execution claim and changes the reservation to `FINALIZED`; (2) removes \(\operatorname{reservedVector}(z)\) and one outstanding redemption slot from \(d\); (3) adds \(v+w\) to `spent[d]` and one to `settledRedemptions[d]`; (4) writes the immutable `DemandSettlement`, including `candidateCID`, the execution binding, \(u\), the meter-record digest and per-component basis map \(\eta\), \(m\), \(v\), \(w\), \(v+w\), and \(\operatorname{reservedVector}(z)-(v+w)\); and (5), only when \(m=\texttt{PROMOTE}\), writes the local admission decision, local transactional metadata, and any deterministic idempotent outbox intents.

The atomicity claim ends at one authoritative transaction boundary. Content bytes referenced by that transaction must already have been durably staged in an inert non-admitted namespace, CID-checked, and charged as validation/staging work while the execution was `RUNNING`; they are not retained/admitted until the transaction references them, and an unreferenced crash orphan is safely garbage-collectable. A filesystem visibility change outside that namespace, another database, protected index mutation outside the authority transaction, remote replication, or downstream notification is never falsely described as atomic with this commit and MUST NOT execute speculatively before the promotion verdict. Each such actual effect originates only from a deterministic outbox intent committed in the `PROMOTE` branch and is later executed through a distinct ticket \(\to\) reservation \(\to\) claim \(\to\) finalization path. An outbox intent records desired work but grants no resource authority; until a separately funded effect completes, the corresponding availability/replication state remains `PENDING`. No later transition may add promotion or spend to the finalized reservation. The issuer first looks up the settlement for \(z\): the same `finalizationDigest` returns the stored settlement, while a different digest is rejected; a late terminal result cannot replace recovery finalization.

An unclaimed `RESERVED` reservation may be cancelled or expire through an atomic `CancelUnclaimedReservation` transition. It races with `ClaimReservation`, so exactly one can win. Cancellation writes `FINALIZED`, removes the outstanding slot, adds one to `settledRedemptions`, records `CANCELLED_UNCLAIMED`, zero resource spend, no promotion, `NONE_UNCLAIMED` for every resource component, and release of the full resource vector; the redemption slot is never reclaimed, and exact action replay is idempotent. Thus reserve/cancel cannot create unbounded settlement records under a finite `maxRedemptions`. A `RUNNING` reservation can never be cancelled, reassigned, or returned to `RESERVED`. If it crashes or reaches `executionExpiry` without a timely durable terminal result, issuer recovery constructs `UNKNOWN(EXECUTION_LOST_OR_EXPIRED)` and finalizes through the same authoritative-accounting transaction. It charges receiver-authoritative use plus conservative bounds for every measurement gap, up to the full reservation, and permits no promotion.

Every terminal outcome therefore charges authoritative or conservatively bounded parse, fetch, validation, inert staging I/O/temporary byte-time, and other pre-verdict work. In the `PROMOTE` transaction, \(w\) additionally charges the durable retained-byte/storage allocation made visible by the authoritative reference, all graph/index mutations actually inside that same authority transaction, local metadata, and outbox-intent creation. External object-store copies, indexes outside that transaction, replication, and downstream work require a separate funded execution. Only soundly known unused reservation is released. Ticket/grant expiry or revocation prevents new reservations and fresh execution claims but not finalization of a `RUNNING` claim or zero-spend cancellation of an unclaimed reservation. Crash recovery must leave a reservation in exactly one of `RESERVED`, `RUNNING`, or immutable `FINALIZED`, never silently reusable, multiply executing, underreported, or settled without its optional promotion decision.

A ticket becomes reclaimable only through `FinalizeTicket_i(c,a)` after `TicketAllocationLive_i(c)` holds and \(c\) has no `RESERVED` or `RUNNING` reservation and no live descendant. The transition is one durable commit that writes \(c\)'s irreversible `TERMINAL` tombstone and performs its parent accounting. For a root ticket \(c\) issued from grant \(g\), it atomically removes \(c\)'s full allocation from `reservedTicketCeilings[g]` and `reservedTicketRedemptions[g]`, adds its actual cumulative spend and consumed redemptions to the grant's finalized counters, and releases only unused resource/redemption allocation. Ticket issue/fanout allowance is never reclaimed.

For a child ticket \(c\) issued from parent ticket \(p\), terminal accounting instead performs, atomically and componentwise,

\[
\begin{aligned}
\operatorname{spent}[p]'&=
\operatorname{spent}[p]+\operatorname{actualSpend}[c],\\
\operatorname{reservedChildren}[p]'&=
\operatorname{reservedChildren}[p]-\operatorname{totalCeiling}[c],\\
\operatorname{settledRedemptions}[p]'&=
\operatorname{settledRedemptions}[p]+\operatorname{consumedRedemptions}[c],\\
\operatorname{reservedChildRedemptions}[p]'&=
\operatorname{reservedChildRedemptions}[p]-\operatorname{maxRedemptions}[c].
\end{aligned}
\]

Thus a child cannot recycle capacity it already spent, and its nonreclaimable ticket-fanout allocation remains consumed. The issuer first looks up `(ticketID(c), terminalActionID)`: the same terminal digest returns the recorded transition, and an equivocal digest is rejected. Only a fresh key checks `TicketAllocationLive`; after the commit, every fresh reservation, execution claim, or child-issuance action against \(c\) fails even if its signed expiry is still in the future.

`FinalizeGrant_i(g,a)` first looks up `(budgetGrantID(g), terminalActionID)`: the same terminal digest returns the stored result, a different digest is equivocation, and only a fresh key checks `GrantAllocationLive_i(g)` and absence of every live child grant or ticket. It atomically performs the appropriate root or child accounting and writes the irreversible `TERMINAL` tombstone. A root grant, identified by `parentBudgetGrantID = NONE`, releases its remaining unallocated resource/redemption authority by becoming terminal; it does not erase finalized spend or nonreclaimable issue/fanout counters.

For a child grant \(c\) whose exact parent is \(g\), terminalization instead performs in the same commit

\[
\begin{aligned}
\operatorname{finalizedSpend}[g]'&=
\operatorname{finalizedSpend}[g]+\operatorname{finalizedSpend}[c],\\
\operatorname{reservedChildGrantCeilings}[g]'&=
\operatorname{reservedChildGrantCeilings}[g]-\operatorname{totalCeiling}[c],\\
\operatorname{finalizedRedemptions}[g]'&=
\operatorname{finalizedRedemptions}[g]+\operatorname{finalizedRedemptions}[c],\\
\operatorname{reservedChildGrantRedemptions}[g]'&=
\operatorname{reservedChildGrantRedemptions}[g]
-\operatorname{totalRedemptionAllowance}[c].
\end{aligned}
\]

The no-live-descendant precondition ensures every child spend and redemption has first reached \(c\)'s finalized counters. The transition never returns \(c\)'s ticket-issue allowance or \(1+\operatorname{childGrantLimit}(c)\) grant-fanout allocation to \(g\). Afterward every fresh ticket/child-grant issuance action fails. Grant or ticket expiry/revocation blocks new issuance, reservations, and execution claims but never blocks reservation finalization or terminal accounting. Revocation alone never reclaims allocation. These exact transitions preserve every ancestor inequality across replay, crash recovery, terminalization, and sibling concurrency; an implementation that merely releases a child grant's full reservation without rolling its finalized spend into the parent is nonconforming.

A result normally receives durable promotion only if it matches an admitted local work item, a requested dependency, an interest subscription selected by receiver policy, an authorized curated-library request, a diversity/reproduction request, or a small explicitly budgeted exploration lane. The receiver may issue the underlying budget grant for its own autonomous work; no external sponsor is required. The paid path is `grant -> ticket -> reservation -> execution claim/meter -> check -> local atomic finalization/outbox`. Promotion exists only as the `PROMOTE` branch of `FinalizeReservation`; there is no post-settlement `Promote` transition, and every actual external effect requires a separate funded execution after its committed outbox intent.

`AdmissionCheck` is object-type-specific. A formal-evidence ticket requires the declared mechanical check; a typed heuristic partial or failure hint may require only bounded schema, scope, provenance-of-execution, and sandbox checks and remains explicitly non-supporting. Durable promotion never by itself means mathematical support. Unsolicited valid objects and `PublicationHint` records may remain in a bounded cold/exploration lane, but they do not enter the protected working set or durable anti-entropy merely because a checker accepts or a publisher advertises them. This prevents an unbounded stream of distinct valid tautologies from consuming the network without suppressing ticketed partial work or allowing concurrent redemption of one ticket.

## 3. Mathematical types

### 3.1 Theory, context, and judgment

```text
Theory {
  logicProfile
  imports[]
  declarations[]
  exports[]
}

Context {
  theoryID
  parameters[]
  localDefinitions[]
  assumptions[]
}

Judgment {
  contextID
  conclusion
}
```

A `Theory` is a semantic module, not an entire execution image. A `Context` makes assumptions and local definitions explicit. Alpha-normalization may remove irrelevant binder names; it must never change domains, hypotheses, coercions, or quantifier order.

### 3.2 Goal template, standalone work item, and optional coordination

```text
GoalTemplate {
  kind
  exactQuestionOrJudgment
  semanticIntentRef?
  inputRefs[]
  hardConstraints[]
  acceptableOutputTypes[]
  evidenceContract
  fidelityContract?
  acceptanceProcedure
}

RelianceQuery {
  requiredSignedJudgment
  exactContextID
  evidenceContract
  fidelityContract?
  acceptanceProcedure
}

WorkItem {
  goalTemplateID
  coordinationScopeRef?
  parentWorkItemCIDs[]
  dependencyWorkItemCIDs[]
  requestedServiceHints[]
}

WorkAdmissionRecord {
  workItemCID
  receiverCell
  issuerEpoch
  admissionScopeID: ReceiverLocalID
  budgetGrantID: ReceiverLocalID
  serviceClassID: ReceiverLocalID
  localPriorityClass
  replicationPolicy
  retentionPolicy
}

CoordinationScope {
  scopeID
  previousVersion?
  focusGoalRefs[]
  sharedPolicyRefs[]
  reviewerAuthorities[]
  routingHints[]
  sharedBudgetPolicy?
  stoppingRule?
}

PublicationHint {
  hintID
  objectCID
  objectKind
  exactStatementOrGoalKey?
  contextID?
  closureCommitment?
  discoveryKeys[]
  providerRecords[]
  coordinationScopeRef?
  expiry
}

InterestSubscription {
  subscriptionID: ReceiverLocalID
  receiverCell
  issuerEpoch
  authority: HOLDER(subjectKey) | LOCAL_POLICY(policyRef)
  exactKeys[]
  structuralPredicates[]
  discoveryShards[]
  acceptedObjectKinds[]
  maximumHintRate
  expiry
}

```

Kinds include `PROVE`, `REFUTE`, `FIND_PREMISES`, `FORMALIZE`, `CHECK_FIDELITY`, `CERTIFY_RELATION`, `COMPLETE_MORPHISM`, `REPRODUCE_COMPUTATION`, `EXPLAIN`, `MINIMIZE_ASSUMPTIONS`, `DECOMPOSE`, `INTEGRATE`, and `REPAIR`.

`RelianceQuery` is the receiver-local question “may I rely on this exact signed judgment under this exact contract?” It can be constructed directly for a standalone artifact. A `GoalTemplate` deterministically compiles its proof/refutation acceptance condition to a reliance query when evidence satisfaction is relevant; other output kinds declare their own acceptance relation.

`WorkItem` is a portable operational request; later prose may call it an obligation. Mathematical identity belongs to the goal template. The portable object contains only advisory service hints. Receiver-local budget, admission scope, service class, urgency, replication, and retention authority live in a separately authenticated `WorkAdmissionRecord`, so importing an immutable work item cannot import the sender's queue share or budget choice. `coordinationScopeRef` is optional and non-epistemic. The work graph may have disconnected components and no distinguished research root. Mathematical evidence and signed justifications may also be published without a work item.

`PublicationHint` and `InterestSubscription` are discovery objects, not evidence or resource authority. Their key, provider, and scope fields are bounded and advisory. A subscription is authenticated by its named receiver at its active epoch; a forged object naming another receiver is discarded and cannot induce reflection traffic. `EvaluationSuite` is a test-harness schema, not a Cooperation Core object or API. Live nodes never receive benchmark membership, observer weights, treatment labels, contrasts, or hidden annotations.

If the goal includes informal or semantic intent, proving the formal child closes only that child. The parent requires a distinct accepted fidelity justification under its parent-owned contract. A nonmechanical fidelity decision names its scoped operational reviewer authority and remains `REVIEWED`, never silently `MECHANICALLY_CHECKED`.

### 3.3 Goal and attempt keys

\[
\operatorname{GoalKey}=H(
\operatorname{kind},\operatorname{exactGoal},\operatorname{semanticIntentRef},
\operatorname{inputCIDs},\operatorname{contextID},
\operatorname{acceptableOutputTypes},\operatorname{evidenceContract},
\operatorname{fidelityContract},\operatorname{acceptanceProcedure}).
\]

Every component is absent-by-tag or an exact immutable CID. Consequently this key may index satisfaction without confusing an exact formal query with a semantic-intent parent or a different acceptance contract.

\[
\operatorname{AttemptKey}=H(
\operatorname{GoalKey},\operatorname{strategyFamily},\operatorname{method},
\operatorname{executableCIDs},\operatorname{parameters},
\operatorname{exactInputSnapshot},\operatorname{environment},
\operatorname{resourceCeiling},\operatorname{nondeterminismPolicy},
\operatorname{toolAPIOrModelVersion},\operatorname{seed}).
\]

Equal attempt keys are eligible for single-flight execution only within a controlled executor domain. A remote same-key claim is a hint until its result passes the local evidence contract. Equal goal keys share known outputs but deliberately permit alternative attempt keys.

### 3.4 Decomposition

```text
Decomposition {
  parentWorkItemCID
  childTemplates[]
  dependencyHyperedges[]
  childInputOutputInterfaces[]
  compositionProcedure
  claimedCoverage
  remainderGoalTemplateID | EMPTY
  estimatedResourceVector
}
```

A decomposition is a fallible proposal. Alternative decompositions coexist. The remainder is mandatory: `EMPTY` is a claim that the composition procedure must validate.

A proposal creates no child work until the receiving cell grants a permission capability where required and reserves descendant budget through a child ticket. All alternatives are charged through the parent `WorkAdmissionRecord`'s issuer-local budget grant; an optional shared program can fund work only through an explicit grant. The decomposition may propose a witness generator but cannot replace or weaken the parent-owned acceptance procedure. `EMPTY` requires a checked coverage certificate.

Before activation, the receiver computes strongly connected components in the workflow-dependency graph. A new ordinary dependency cycle is rejected or converted into an explicit `CYCLE_BREAK`/fixed-point obligation with a distinct checked contract. Cyclic workflow dependencies never become evidence and never close merely by mutual completion claims.

### 3.5 Capability advertisement

```text
CapabilityAd {
  endpoint
  hardCapabilityPredicates[]
  domainAndMethodCentroids[]
  cachedEnvironmentSketch
  availableResourceVector
  queueDelayDistribution
  empiricalOutcomeDistributions[]
  expiry
}
```

Persistent human identity is unnecessary for mechanically checked outputs. Stable rotating service principals are permitted where cell membership, resource accounting, semantic-review authority, or measured failure-domain separation depends on them. Capability claims are advisory and should be calibrated with unpredictable probe tasks and receiver-observed outcomes. Ads expire and are shared only with relevant cells.

### 3.6 Resource offer and optional lease

```text
ResourceOffer {
  workItemCID
  predictedAcceptProbability
  predictedInformationGain
  resourceQuantiles
  completionTimeQuantiles
  strategyFamily
  accessibleInputSketch
  failureDomainDescriptor
}

Lease {
  attemptKey
  holderEndpoint
  localDurationHint
  heartbeatSequence
  checkpointRef?
}
```

A lease is an evaluated optimization: it suppresses accidental duplication but confers no ownership, priority, validity, or exclusion right. Clock synchronization is not a safety assumption. Nodes judge staleness using locally elapsed time since the last observed heartbeat. Heartbeats alone cannot renew suppression beyond \(L_{\max}\); continued suppression requires a locally validated progress checkpoint. A blackholed task therefore becomes eligible elsewhere. Disabling leases leaves mathematical validity, admission, and the base local research path intact.

### 3.7 Attempt and work report

```text
Attempt {
  attemptKey
  workItemCID
  exactInputSnapshot
  strategyDescriptor
  resourceEnvelope
  checkpointPolicy
}

WorkReport {
  attemptKey
  inputSnapshot
  state: PARTIAL | CANDIDATE | FAILED | INCONCLUSIVE
  artifacts[]
  dischargedObligations[]
  residualObligations[]
  uncertaintyAndLimitations
  measuredResourceVector
  resumableCheckpoint?
  failureCapsule?
}
```

Reports remain admissible after a lease expires or without a lease. Every `WorkReport` field—including `dischargedObligations`, resource use, uncertainty, and failure domain—is untrusted input. It changes no completion or capability state until the receiver checks the relevant contract or records its own measurement.

### 3.8 Failure capsule

```text
FailureCapsule {
  strength: HINT | REPRODUCED_RUN | CERTIFIED_EXHAUSTION
  workItemCID
  exactContext
  methodFamily
  exploredRegion
  resourceBound
  reproducibleObstruction?
  usefulIntermediates[]
  rulesOut
  doesNotRuleOut
  suggestedContinuation[]
}
```

It is promoted only when it prunes meaningful work or carries reusable information. `HINT` and `REPRODUCED_RUN` may influence ranking within bounded TTLs but cannot suppress work or refute a goal. Only `CERTIFIED_EXHAUSTION`, plus a locally checked containment relation, may suppress a proposed search:

\[
\operatorname{Suppress}(b,a)
\Rightarrow
\operatorname{CertifiedExhaustion}(a)
\land
\operatorname{CheckedContainment}(R_b\subseteq R_a).
\]

Changing context, method, executable, parameters, resource ceiling, nondeterminism policy, or search-space definition normally invalidates negative-cache reuse. If containment or coverage is `UNKNOWN`, the capsule remains a hint.

### 3.9 Evidence

```text
Evidence =
    Derivation(judgment, proofArtifact, dependencies, checkerProfile, succinctArgument?)
  | Counterexample(judgment, witnessOrModel, satisfactionCertificate, scope)
  | ComputationCertificate(statement, program, inputs, certificate)
  | RelationCertificate(relation, certificate)
  | ReviewEvidence(subject, rubric, findings)
```

`ReviewEvidence` never becomes mechanical certification merely by count.

Every assessment records its basis:

```text
ValidationBasis =
    LOCAL_REPLAY
  | DOMAIN_CERTIFICATE
  | SUCCINCT_ARGUMENT
  | TRUSTED_ATTESTATION
```

`LOCAL_REPLAY` and locally checked `DOMAIN_CERTIFICATE` are exactly the validation bases enabled for strict P0 formal closure in Core v0. A remote signature is only an advisory cache/routing hint unless local policy explicitly trusts its operational validator role. `SUCCINCT_ARGUMENT` is a schema-reserved later basis, not a strict-P0 option in this version. A future versioned policy may enable it only after the adoption gates in the SNARK assessment. A succinct argument, when later supported, is a separate object:

```text
SuccinctArgument {
  subjectRoot
  relationID
  publicInputsRoot
  verifierKeyID
  proofSystemID
  argument
  policyEpoch
  nativeArtifactAvailability: AVAILABLE | UNAVAILABLE
}
```

The first two bases may produce `MECHANICALLY_CHECKED` in Core v0. A later versioned profile may also assign that grade to a receiver-locally verified succinct argument, but the grade does not make that basis eligible for the current strict P0 contract. `TRUSTED_ATTESTATION` produces an explicitly trust-dependent assessment; it is not mechanical validation of the theorem merely because its signature is checked. Neither succinct arguments nor trusted attestations are current strict-P0 formal leaves.

Succinct verification has computational rather than deterministic soundness. For security parameter \(\lambda\), encoded relation \(R_K\), and every probabilistic polynomial-time adversary \(\mathcal A\), the selected proof system must make

\[
\Pr\!\left[
\begin{array}{l}
(pp,pk,vk,tr)\leftarrow\operatorname{Setup}(1^\lambda,R_K,\textit{proofSystemID});\\
(x,\Pi)\leftarrow\mathcal A(pp,pk,vk,tr):
\operatorname{KeyValid}(pp,vk,R_K,tr)=1
\land\operatorname{Verify}(pp,vk,R_K,x,\Pi)=1
\land\neg\exists w\,R_K(x,w)=1
\end{array}
\right]\leq\operatorname{negl}(\lambda).
\]

Here `Setup` includes the selected system's honestly generated or transparently derived public parameters, proving/verifier keys, exact encoded relation (or universal-system relation commitment), proof-system ID, and validation transcript. The receiver accepts only a pinned tuple `(pp,vk,R_K,tr)` for which `KeyValid` binds that verifier key to the declared relation and setup assumptions; setup randomness and adversary randomness are both inside the probability. For a transparent system, `Setup` is its specified deterministic public-parameter and relation-commitment derivation. If the claim includes possession or extractability of \(w\), the declared system must separately satisfy the required knowledge-soundness definition. Verifier acceptance establishes only the encoded existential relation up to the declared error and TCB; it does **not** establish that the native checker was executed, or strengthen the logic, formalization, or checker implementation. Public native artifacts should remain available for reuse and independent reconstruction.

### 3.10 Relation and theory morphism

```text
Relation {
  left
  right
  kind
  translation?
  conditions[]
  evidence[]
}

Morphism {
  sourceTheory
  targetTheory
  mappedSubtheory
  symbolMap
  obligations[]
}
```

Relation families:

- structural: `DEPENDS_ON`, `DISCHARGES`, `DECOMPOSES_INTO`;
- logical: `IMPLIES`, `EQUIVALENT`, `SPECIALIZES`, `GENERALIZES`, `CONTRADICTS`;
- theory-level: `MORPHISM`, `INTERPRETS`, `CONSERVATIVE_EXTENSION`;
- integration: `INSTANCE_OF`, `ABSTRACTS`, `REFACTORS_TO`;
- discovery-only: `SAME_SCHEMA`, `ANALOGOUS`, similarity;
- workflow: `ATTEMPT_SUBSUMES`, `BLOCKED_BY`.

Discovery-only edges cannot support substitution, merge, transport, or obligation closure.

### 3.11 Justification and challenge

```text
SignedJudgment {
  polarity: SUPPORTS | REFUTES
  judgment
}

Justification {
  head: SignedJudgment
  requiresAll: SignedJudgment[]
  evidence
  validationPolicy
}

Assessment {
  subject
  inputSnapshot
  policy
  grade
  reuseClass: PUBLIC_REUSABLE | OPAQUE_RELIANCE
  validation
  validationBasis
  polarity
}

ChallengeNotice {
  subjects[]
  conflictType
  exactScope
  minimalDivergenceWitness?
  affectedDependencies[]
  reproductionOrRepairTasks[]
}

DefeatEvidence {
  subjects[]
  locallyCheckedCounterevidenceOrDefect
  exactAffectedSupportPaths[]
  validationPolicy
}

LocalRelianceOverride {
  overrideID
  issuerCellOrAuthority
  subject
  exactScope
  action: QUARANTINE | SUPERSEDE | RELEASE
  supersedesOverrideIDs[]
  policyEpoch
  authorizationDecisionID
}
```

Multiple justifications for one signed conclusion are OR alternatives. A locally accepted direct proof, certificate, or counterexample is represented as a zero-dependency justification, so mixed-polarity composition has one explicit type. Remote assessments and challenge notices are hints. A bare notice cannot block stable support or force unbounded impact recomputation. Only locally checked `DefeatEvidence`, a confirmed dependency/checker-policy defect, or a locally admitted `LocalRelianceOverride` disables a support path. Ephemeral control messages never alter a stable view directly.

Override resolution is a deterministic projection of admitted facts. Every supersession edge points from a new override to exact prior override IDs for the same governed scope. If a named predecessor has not arrived, the new object remains pending in quarantine and yields `UNKNOWN(MISSING_OVERRIDE_PREDECESSOR)`; it is reconsidered after closure arrival. Self-reference, cycles, and cross-authority cancellation are rejected. An admitted override with no admitted successor is maximal. No maximal override means no override block; only maximal `RELEASE` actions mean released; any maximal `QUARANTINE`/`SUPERSEDE`, or concurrent incomparable release and blocking actions, resolves fail-closed to `QUARANTINED/DISPUTED`. A later authorized resolution must explicitly supersede every competing maximal override. It cannot cancel an unseen future quarantine.

## 4. Orthogonal task state

Do not store a single status field. Derive:

```text
Completion = OPEN | CANDIDATE | SATISFIED | LOCALLY_EXHAUSTED
Activity   = IDLE | LEASED
Health     = CLEAN | CHALLENGED | STALE
```

`LOCALLY_EXHAUSTED` records a budget/stopping rule, never impossibility. `SATISFIED` requires direct accepted evidence or an accepted composition witness. Lease expiry affects only `Activity`.

## 5. Evidence state and support semantics

```text
Grade      = HEURISTIC | REVIEWED | ATTESTED | MECHANICALLY_CHECKED
ReuseClass = PUBLIC_REUSABLE | OPAQUE_RELIANCE
Validation = UNCHECKED | ACCEPT | REJECT | ERROR | UNKNOWN
Polarity   = SUPPORTS | REFUTES
```

`OPAQUE_RELIANCE` is not a stronger grade. A locally verified succinct argument whose native proof/certificate/witness closure is unavailable must carry that reuse class. It may satisfy only an evidence contract that explicitly permits opaque succinct reliance and declares the proof system, security parameter, relation, public inputs, verifier key, TCB, soundness error, and any knowledge-soundness requirement. The strict P0 and every public reusable-knowledge contract require `PUBLIC_REUSABLE` and an available native artifact closure; therefore an opaque argument is excluded from their accepted-justification set even when its succinct verifier returns `ACCEPT`.

Let \(\mathcal G\) be the set of exact context-bound judgments and let the signed-judgment space be

\[
\mathcal L=\{\textsf{SUPPORTS},\textsf{REFUTES}\}\times\mathcal G.
\]

For policy \(P\), admitted fact set \(A\), and locally available object closure \(O\), let \(J_P\) be the finite-dependency justifications whose signed heads and signed prerequisites are explicit and whose:

- exact evidence, dependencies, context, and validation metadata are available in \(O\);
- evidence and composition contracts were accepted locally under \(P\);
- validation basis and grade are permitted by \(P\) for the justification's declared signed head and acceptance procedure;
- immutable justification fact is admitted in \(A\).

A direct proof, certificate, or counterexample is a zero-dependency justification. Let \(\operatorname{Blocked}_{P,A}(j)\) be derived from locally accepted defects, dependency/checker incidents, and the deterministic active-override projection from section 3.11. Submitter-supplied impact lists never define it. Let \(\operatorname{opp}(\sigma,x)\) reverse the polarity of signed judgment \((\sigma,x)\).

The raw grounded signed set is the least fixed point:

\[
K_P=\mu X.
\{\operatorname{head}(j)\mid
j\in J_P
\land\neg\operatorname{Blocked}_{P,A}(j)
\land\operatorname{requiresAll}(j)\subseteq X\}.
\]

Derivability and refutability are projections of this simultaneous signed construction:

\[
D_P=\{x\mid(\textsf{SUPPORTS},x)\in K_P\},
\qquad
R_P=\{x\mid(\textsf{REFUTES},x)\in K_P\}.
\]

Hence:

\[
\operatorname{state}_P(x)=
(\mathbf 1[x\in D_P],\mathbf 1[x\in R_P]).
\]

This gives unknown, supported, refuted, or inconsistent. Raw state preserves both sides. The strict P0 active signed set is:

\[
U_P^{\mathrm{strict}}=\mu X.
\{\operatorname{head}(j)\mid
j\in J_P
\land\neg\operatorname{Blocked}_{P,A}(j)
\land\operatorname{opp}(\operatorname{head}(j))\notin K_P
\land\operatorname{requiresAll}(j)\subseteq X\}.
\]

Every element inserted into an approximant is itself undisputed, so the recursive premise also excludes every disputed dependency. Thus an exact `(1,1)` judgment closes neither polarity, while a clean OR-alternative tree remains usable. Mixed-polarity compositions are explicit rather than hidden inside a nominally zero-dependency checker. A different local policy may expose disputed paths for analysis, but it must not label that behavior as the strict profile.

A finite active support tree \(T\) chooses one accepted justification at every node, has that justification's exact signed prerequisites as its children, ends at accepted zero-dependency leaves, and contains only nodes in \(U_P^{\mathrm{strict}}\). Stable reliance quantifies over the tree rather than only its root judgment. For a `RelianceQuery` \(q\), locally admitted facts \(A\), and locally available closure \(O\):

\[
\operatorname{Stable}_P(q;A,O)\iff
\exists T:
\begin{aligned}[t]
&\operatorname{root}(T)=\operatorname{requiredSignedJudgment}(q)\\
&\land\operatorname{FiniteActiveTree}_P(T)\\
&\land\operatorname{CheckContract}_P(
  \operatorname{evidenceContract}(q),
  \operatorname{fidelityContract}(q),
  \operatorname{acceptanceProcedure}(q),T)=\texttt{ACCEPT}\\
&\land\operatorname{ExactContextMatch}(q,T)
\land\operatorname{ClosureAvailable}(T,O).
\end{aligned}
\]

`CheckContract` evaluates path-dependent requirements over the exact tree, including permitted axioms and unsafe features, validator/checker basis, reuse class and native-artifact availability, reviewer scope, failure-domain diversity where required, and composition/fidelity evidence. A tree accepted for a permissive query therefore cannot close a stricter query with the same root judgment. Normatively, the formal-closure portion of every current strict-P0 tree satisfies

\[
\operatorname{StrictP0Basis}(T)\iff
\forall n\in\operatorname{FormalNodes}(T),\quad
\operatorname{basis}(n)\in
\{\texttt{LOCAL_REPLAY},\texttt{DOMAIN_CERTIFICATE}\}
\land\operatorname{ReceiverChecked}_P(n).
\]

`CheckContract` must enforce this predicate, not infer eligibility from the broader `MECHANICALLY_CHECKED` grade. In particular, `SUCCINCT_ARGUMENT`, `TRUSTED_ATTESTATION`, and `OPAQUE_RELIANCE` never satisfy a current strict-P0 contract; opaque reliance also never satisfies a public reusable-knowledge contract. A `PROVE` goal template compiles to a query whose required polarity is `SUPPORTS`; `REFUTE` compiles to `REFUTES`; every other evidence-bearing goal kind declares the required signed relation in its acceptance procedure. Define

\[
\operatorname{Close}_P(o;A,O):=
\operatorname{Stable}_P(\operatorname{RelianceQueryOf}(o);A,O)
\]

only as convenience for an admitted work item \(o\). Standalone evidence uses `Stable` directly and requires no synthetic network goal or producer work item.

All CID, closure, base-evidence, composition, defect, and availability checks are premises for membership in the accepted-justification set; they are not optional hidden abbreviations. For one exact validation key:

- `UNCHECKED` means no validation attempt has begun and is not a terminal result;
- `ACCEPT` means the declared procedure terminated and established its acceptance relation;
- `REJECT` means it terminated and definitively established malformedness, contract violation, or certificate invalidity;
- `UNKNOWN(reason)` means there is no decision under the declared relation and bounds, for example because a named closure is unavailable, the declared procedure is incomplete, or its time/fuel/memory ceiling was reached;
- `ERROR(reason)` means there is no trustworthy execution result because of an unexpected checker crash, internal invariant failure, sandbox failure, corrupt runtime, or trusted-computing-base integrity alarm.

Neither `ERROR` nor `UNKNOWN` is refutation, promotion authority, or negative-cache suppression. Both finalize through `AuthoritativeAccount`: each sound resource component charges receiver-authoritative use, and every missing, rolled-back, unauthenticated, or integrity-alarmed component charges its frozen conservative upper bound within the reservation. Neither outcome releases capacity from a claimant report. Starting an attempt leaves `UNCHECKED`; retries create new immutable assessments rather than overwriting history. `STALE` remains a health/cache-use state, not a validation value; an unusable old assessment may surface as `UNKNOWN(STALE_RELIANCE_EPOCH)`.

Because dependencies are finite, every member of either signed least fixed point has a finite rank. Induction on that rank proves grounded support from accepted leaves and accepted composition edges. An ungrounded strongly connected component has no rank and supports nothing. Explicit inductive, coinductive, or fixed-point mathematics must use its own checked evidence contract rather than ordinary circular justifications.

## 6. Correctness rules

### Checked derivation

\[
\frac{\operatorname{Check}_K(T,\pi:\Gamma\vdash\varphi)=\texttt{ACCEPT}}
{\operatorname{supports}(\Gamma\vdash\varphi)}.
\]

### Checked counterexample

\[
\frac{M\models T\quad M\models\Gamma\quad M\not\models\varphi}
{\operatorname{refutes}(\Gamma\vdash\varphi)}.
\]

### Certified morphism and transport

Let \(D\) be the exact mapped source subtheory named by the morphism.

\[
\frac{
\text{mapped declarations type-check}
\quad
\forall a\in\operatorname{Ax}(S|_D),\;T\vdash m(a)
}{\operatorname{certified}(m:S|_D\to T)}.
\]

\[
\frac{
S|_D\vdash\varphi\quad
\operatorname{deps}(\varphi)\subseteq D\quad
\operatorname{certified}(m:S|_D\to T)\quad
\text{side conditions discharged}
}{T\vdash m(\varphi)}.
\]

For automatic reuse or obligation closure, the target-side derivation or a small certified transporter output MUST be locally checked. Unreplayed transport is discovery/provisional evidence only. The certified morphism binds exact endpoints, mapped dependency subtheory, translation implementation, side conditions, checker profile, and axiom policy.

### Failed-attempt conservativity

`FAILED(attempt, goal)` never implies `REFUTED(goal)`. It influences deduplication only through a checked `ATTEMPT_SUBSUMES` relation.

## 7. Protocol

### 7.0 Receive and admit

An unsolicited `PublicationHint` follows only:

\[
\text{bounded frame parse}
\rightarrow \text{canonical hint/schema check}
\rightarrow \text{key/provider/fanout/TTL quota}
\rightarrow \text{bounded expendable hint cache}.
\]

Before receiver selection and reservation, a hint may affect only this cache, bounded telemetry, advisory ranking, and the bounded dissemination transition below. It cannot trigger closure fetch, validation, durable indexing, candidate anti-entropy, payload replication, child creation, or stable support.

`DisseminateHint` may forward only the canonical bounded hint frame—not its object closure—through a matching authenticated subscription or its bounded home shard. The transition requires a locally admitted canonical discovery key, a computed routing key, deduplication, a decreasing hop/TTL bound, and available per-home, per-key, and per-receiver hint-routing quota. Each acceptance creates at most the configured fixed number of next-hop frames and no recursive fanout outside those quotas. Forwarding is charged as expendable discovery traffic and grants no fetch, validation, promotion, queue-share, or replication authority. Thus subscribed discovery is possible without allowing a hint flood to amplify into unbounded work.

For a candidate selected by receiver policy, every receiving cell applies:

\[
\text{bounded frame/size parse}
\rightarrow \text{typed CID and canonical schema check}
\rightarrow \text{cheap demand scope check}
\rightarrow \text{atomic demand reservation}
\rightarrow \text{atomic execution claim and meter creation}
\rightarrow \text{quarantine}
\rightarrow \text{closure resolution}
\rightarrow \text{sandboxed validation}
\rightarrow \text{local atomic settlement/admission and optional outbox-intent commit}.
\]

Unadmitted data does not enter durable anti-entropy, support graphs, routing queues, protected caches, or semantic indexes. Admission by another independently operated cell is a hint, not authority even when policy identifiers match. Inter-cell anti-entropy performs the filtered transition in section 2. Direct admitted-set union is limited to already committed facts copied inside one logical admission authority's declared crash-fault replica set.

Validation distinguishes four closures:

1. **logical:** declarations, definitions, axioms, and proof terms used by the kernel;
2. **elaboration/build:** parser, elaborator, macros, plugins, packages, compiler, and source inputs;
3. **execution:** program, runtime, inputs, solver, and certificate checker;
4. **semantic context:** theory, context, translations, side conditions, and obligation contract.

Every checked result states which boundary it establishes. All material references are typed immutable content IDs; no mutable lookup or network access occurs during validation. Unsupported native mechanisms, hidden imports, nondeclared axioms, or unresolved closure facts fail closed.

### 7.1 Create local work, publish artifacts, and optionally coordinate

A cell may create a standalone goal template and portable work item, then bind it to local policy with a `WorkAdmissionRecord` and local budget grant. Before paid execution or validation it issues a local ticket from that grant, reserves through the ticket, and atomically claims the unique metered execution. An agent may also investigate without a work item and publish a typed artifact plus a bounded nonspendable `PublicationHint` using resources it controls. Neither path requires a shared root, campaign, sponsor, or common stopping rule.

Interested receivers discover hints or query exact/structural indexes, then independently decide whether to issue a ticket from a receiver grant, reserve resources, and admit one execution claim. An optional `CoordinationScope` may publish shared focus goals, policies, reviewer authorities, routing hints, a shared-budget policy, or a stopping rule. Its focus set may be empty and has no distinguished root. A scope can authorize or route work only through receiver-recognized capabilities and grants; it cannot alter evidence validity or revoke unrelated reuse. `sharedPolicyRefs` are proposals or execution policies: they cannot mutate an existing evidence/fidelity contract, and receiver adoption of a different validation rule creates a distinct exact policy/contract identifier.

### 7.2 Discover and reuse

Search in this order:

1. exact goal and object keys;
2. matching receiver interest subscriptions and discovery shards;
3. decidable domain normal forms;
4. structural symbol/dependency indexes;
5. certified theory morphisms and logical relations;
6. candidate semantic retrieval;
7. prior counterexamples, failure capsules, and partial results.

Return reusable evidence together with unsatisfied side conditions. Never hide a mismatch behind a similarity score.

### 7.3 Decompose

Planners publish competing decompositions. Critics check interfaces, hidden coupling, claimed coverage, resource amplification, the remainder, and workflow cycles. Ready children enter local queues only after exact dependencies are satisfied and the issuer has atomically reserved child demand/resource tickets.

### 7.4 Route and execute

Hard constraints filter agents/cells. Local schedulers rank remaining candidates, and agents publish structured reports. Soft leases and work stealing are optional execution mechanisms, not Core safety requirements. When enabled, they use the semantics below: leases only suppress duplicate attempts for a bounded interval, checkpoints may justify bounded renewal, and steal requests carry immutable work descriptors plus receiver-issued authority. The active-coordination experiment enables cross-cell leases/stealing without changing the local solver in its passive control.

### 7.5 Validate and integrate

Cheap schema/context checks run at ingestion. Expensive proof/certificate checking is demand- and risk-driven but mandatory before formal acceptance. A remote `Assessment(validation=ACCEPT)` never closes an obligation by itself. Accepted evidence creates locally admitted signed justifications and may unlock dependent obligations only through a contract-accepted tree in \(U_P^{\mathrm{strict}}\) from section 5. High-fanout results are prioritized using only receiver-admitted dependency edges.

Every justification admitted to \(J_P\) has already passed typed-CID, exact-context, closure-availability, evidence-contract, local-validation, composition, and active-defect checks. Consequently the normative closure predicate is the section 5 tree predicate, not a second weaker formula. Agent count, authorship, popularity, scheduler score, remote review count, foreign admission, and publication history are absent.

If an obligation has `semanticIntentRef`, an accepted formal derivation closes only its formal proof child. The parent additionally requires an accepted fidelity justification. Where this cannot be mechanical, the exact intent-contract reviewer authority and reliance grade remain visible.

### 7.6 Challenge and repair

Preserve all sides, find the smallest reproducible divergence, resolve exact contexts, replay or recompute, search for distinguishing examples, and publish a scoped resolution or explicit alternative. A `ChallengeNotice` consumes only bounded attention.

Every admitted fact, defect, override, policy/contract change, or closure-availability change that can alter \(J_P\), `Blocked`, \(K_P\), \(U_P^{\mathrm{strict}}\), `CheckContract`, or `ClosureAvailable` is published by one linearizable transaction that atomically exposes the tuple consisting of the new state, conservative exact signed dirty seeds, and the next monotone reliance epoch. No reader may observe epoch \(e+1\) without the associated change or observe the change while epoch \(e\) remains current. A store unable to commit that tuple atomically MUST use an in-progress epoch/seqlock state under which every affected query returns `STALE`/`UNKNOWN`, followed by a second durable epoch advance when publication completes; crash recovery cannot clear the in-progress state without either completing or conservatively dirtying the whole policy partition. Admission of a justification with head \(s\) records at least both \(s\) and \(\operatorname{opp}(s)\); it preserves both raw polarities and does not reinterpret an ordinary counterexample as `DefeatEvidence`. Thus admitting an exact opposite-polarity zero-dependency justification and advancing the epoch become visible at the same linearization point.

A cached assessment from an older reliance epoch may return `ACCEPT` only after the receiver rechecks, under the current epoch, the cached exact finite tree's active-node membership, opposite-polarity absence, closure, and full tree contract. A mere claim that its path is disjoint from currently traversed dirty nodes is insufficient. The query/cache response is linearized against one epoch snapshot and must re-read that the epoch is unchanged immediately before emitting `ACCEPT`; a concurrent epoch change forces `STALE`/`UNKNOWN` and retry. Without that current-epoch freshness certificate it also returns `STALE`/`UNKNOWN`. Consequently a cached `PROVE x` acceptance followed by admission of an exact `REFUTES x` justification—and symmetrically cached refutation followed by proof—returns non-`ACCEPT` immediately, before reverse traversal. A clean alternative may become accepted only after its own exact current tree is checked.

Epoch increment and dirty-seed insertion are constant or logarithmic foreground work. Reverse-impact traversal processes at most a policy-bounded number of edges per transition and persists a resumable cursor; demand-funded path checking or later traversal performs the remaining work. If an event's affected exact scope cannot be bounded safely, the receiver dirties the whole relevant policy partition rather than permitting an old acceptance. Submitter-supplied impact lists are hints.

### 7.6.1 Hostile execution sandbox

Parser/decoder, dependency unpacking, elaboration/build, small checker, generator execution, and foreign checkpoint restoration use separate isolation tiers. Hostile execution has no ambient credentials or network, a read-only object store, fresh bounded temporary storage, a non-root principal, syscall/device restrictions, and hard CPU/fuel, wall-time, memory, process, file, inode, output, and I/O limits. Multi-tenant builds SHOULD use microVM-grade isolation.

Canonical parsers stream with limits on header size, nesting, object count, graph degree, decompression ratio, path/symlink traversal, and duplicate keys. Foreign checkpoints use a safe typed data format; arbitrary executable or pickle-like deserialization is forbidden. A declared parser/checker limit reached without a verdict yields `UNKNOWN(RESOURCE_LIMIT)`; a declared malformedness result yields `REJECT`; an unexpected sandbox, runtime, or checker integrity failure yields `ERROR`.

### 7.7 Abstract and refactor

Repeated subgoals generate lemma obligations. Repeated structures generate interface/generalization proposals. Promotion requires checked instance morphisms and specializations plus receiver-observed reuse, a preregistered held-out result, or measured cost reduction. Immutable sources remain; refactoring creates a new theory and preservation obligations.

## 8. Scheduling

Cells—not millions of agents—form the routing substrate. Core v0 uses a fixed authenticated cell-membership epoch. Each admitted work item, exact object query, or interest shard receives a domain-separated `routingKey`; optional coordination-scope material may be one input but is never required. Rendezvous hashing maps the key to a small set of home cells. Homes are routing/deduplication caches, not admission or mathematical authorities. Worker discovery and task acquisition must be bounded; registration plus worker pull is the first testbed candidate, not a mathematical or Core safety requirement.

\[
\operatorname{routingKey}
=H(\texttt{"DTMKN/routing/v0"},\operatorname{keyKind},
\operatorname{canonicalDiscoveryKey}).
\]

`canonicalDiscoveryKey` is one of an exact goal key, object CID, or a receiver-approved canonical interest key. A `PublicationHint` carries only a bounded number of `discoveryKeys`; after schema and quota admission, each receiving/home cell canonicalizes them and computes the corresponding routing keys locally. Sender-supplied text is never used directly as a routing or fairness principal. Implementations rate-limit admitted key creation and hot-key load.

Each receiver maps admitted requests into a finite receiver-controlled `serviceClassID` registry. Cells use per-service-class and per-capability-class weighted fair queues or deficit round robin with aging. A sender-created identity, topic, goal, namespace, or coordination scope cannot create a new positive-share queue; unclassified traffic shares a bounded aggregate onboarding/exploration class. Optional ranking is applied only inside a bounded candidate set.

Tasks first contact a bounded top-\(k\) set of cells. Every failed routing epoch contacts at least one previously untried exploration target. In the fixed 3–5-cell Core v0 roster, the exploration horizon is the entire eligible roster; later larger deployments must either retain full eventual exploration or weaken the liveness claim to the explicitly sampled horizon. Individual worker advertisements are not gossiped globally. With \(M\) cells, \(N\) workers, fixed home replication \(r\), and bounded candidate set \(k\), the design target is:

\[
\operatorname{messagesPerTaskEvent}=O(r+k+\log M),
\]

independent of \(N\).

A recommended local score is:

\[
\begin{aligned}
S(a,t)={}&P_{\mathrm{solve}}(a,t)(V_t+\beta U_t)
+\gamma I(a,t)
-\pi^\top\mathbb E[C_{a,t}]\\
&-\lambda_L\mathbb E[L_{a,t}]
-\lambda_X X(a,t)
-\lambda_Q Q(a)
-\lambda_R R(a,t)\\
&+B_{\mathrm{explore}}(a,t)+B_{\mathrm{age}}(t).
\end{aligned}
\]

Definitions:

- \(V_t\): direct receiver-local value for the current task or interest;
- \(U_t\): expected downstream obligations unlocked;
- \(I\): information gain from success or informative failure;
- \(C\): resource vector;
- \(L\): latency;
- \(X\): transfer/locality cost;
- \(Q\): congestion;
- \(R\): correlation with existing attempts;
- \(B_{\mathrm{explore}}\): exploration/rare-capability bonus;
- \(B_{\mathrm{age}}\): starvation prevention.

The score does not determine mathematical truth, durable admission, or reported evaluation value and need not be globally comparable. \(V_t\), \(U_t\), and priority are computed from receiver-local work, interests, and reliance; submitter and optional program claims are hints. Hidden benchmark annotations are not scheduler inputs. Core v0 begins with static tags plus measured completion/cost distributions. Learned contextual ranking is an ablation or later feature after held-out calibration data exist.

Self-reported capability, progress, cost, and diversity are advisory. New endpoints receive small onboarding capabilities; larger grants follow receiver-observed, locally validated outcomes and unpredictable probes. A lease cannot suppress all alternatives indefinitely, and progressive fanout recovers from blackholes. Mandatory diversity counts two attempts as distinct only when the receiver has measured or authorized evidence of different relevant failure domains; unknown lineage counts as correlated.

## 9. Network and storage protocol

Core v0 reuses:

- rendezvous/consistent hashing over authenticated cells for exact home selection;
- scoped pub/sub for new ready tasks, results, and urgent challenges;
- bounded-fanout gossip for ephemeral capacity/frontier summaries;
- Merkle anti-entropy for already committed durable facts inside one logical cell's crash-fault replica set, and candidate-inventory anti-entropy between independently operated cells in subscribed exact-key, structural, or interest shards;
- structural indexes and optional local ANN indexes for candidate semantic discovery;
- direct content-addressed transfer for large payloads.

Never broadcast every task to every agent. Gossip summaries and references, fetch payloads lazily, batch small objects, use TTLs, and verify fetched data by exact content key.

Provider records and ANN results are hints. Corrupt bytes fail the requested CID. Candidate semantic relations live in quota- and TTL-bounded heuristic indexes, cannot enter support, and cannot evict admitted exact/certified data. Query multiple paths plus a bounded ranking-independent exploration route where eclipse or monoculture matters. A permissionless adversarial DHT has no generic eclipse resistance; it is not a Core v0 dependency. Later membership/DHT work requires a separate Sybil and eclipse model.

Stable reusable support records a retention/availability contract for its exact object closure. Equal fact references without equal available closures may legitimately yield `UNKNOWN`; content addressing proves integrity, not availability.

## 10. Caching and action reuse

Cache at agent, host, cell, and durable federation levels:

- immutable objects and closure packs;
- exact action results by attempt key;
- validation results by proof/checker/environment/options;
- search indexes;
- bounded scoped failure capsules.

Use cost-aware admission. Exact duplicate attempts may single-flight locally. Similarity never auto-merges. Negative cache entries are scoped and normally expire. Separate validated positives, provisional candidates, negative/failure data, payload staging, and indexes so junk cannot evict the stable working set. Remote cache entries are hints unless their certificates validate locally; `ERROR` and `UNKNOWN` never mean refutation.

## 11. Load control

For each resource and compatible-capability class \(k\):

\[
\rho_k=
\frac{\text{admitted expected work rate}}
{\text{available service capacity}}<1.
\]

The utilization condition is necessary but not sufficient: each class also declares burst bounds and a positive reserved service share for every receiver-admitted service class. A globally underloaded system may still overload its only rare-capability queue.

Core requires bounded acquisition and queues, finite receiver-owned service classes, declared positive service floors under a frozen admission envelope, a protected validation reserve, overload controls, cancellation propagation, and circuit breakers. Pull scheduling, WFQ, DRR, aging, checkpoint/preemption, and their concrete parameters are testbed candidates: any implementation that satisfies the declared service and resource contracts is conforming. Shed approximate index refresh, low-value speculation, and redundant generation before mandatory checking.

Every parent constrains descendant compute, communication, depth, artifact size, graph insertion, recomputation, and replicas through atomically charged demand tickets, reservations, unique execution claims, authoritative meters, and nonreclaimable descendant-issue allowances; permission capabilities independently bound allowed actions, nonreclaimable authorization fanout, and accepted replay records through their finite action-record allowance. Rejected fresh action IDs create no durable per-ID state. Every cell also enforces aggregate anonymous ingress, onboarding, hint-key/fanout, parsing, storage, pub/sub, validation, coordination-scope creation, and service-class-admission limits. One admitted task or publication cannot create unbounded induced work without another receiver decision.

## 12. Speculation and replication

Small diverse portfolios, successive halving, and tail-latency hedging are testbed candidates rather than Core conformance requirements. When enabled, every speculative branch uses ordinary ticket/reservation/claim accounting, declared diversity evidence, receiver-controlled cancellation, authoritative metering, a cell-wide speculation cap, and overload rules that shed speculation before mandatory validation. Hedging additionally requires a frozen conditional runtime threshold.

Replication policy distinguishes storage, repeat execution, independent reconstruction, and method/tool/formalization diversity. Allocate optional checking by expected error impact and value of information. One checked proof may establish conditional derivability; diversity is mainly for detecting specification, environment, implementation, and correlated-process mistakes.

## 13. Partition behavior

During partitions:

- local work continues;
- duplicate attempts are allowed;
- leases never determine result validity;
- local results remain admissible;
- no partition deletes another's artifacts.

After healing, replicas of one logical cell may reconcile immutable facts already committed by their common admission authority through set union. They may not union independently spent ledgers; partitioned committing replicas require either nonoverlapping pre-allocated escrow or a narrow consensus/primary protocol. Every independently operated cell—including a cell with identical advertised policy roots—exchanges candidate deltas and reapplies receiver-local admission. Exact duplicates deduplicate, alternatives coexist, conflicts create bounded tasks, and affected views recompute. Global exactly-once execution and globally strict resource budgets are non-goals unless a narrow shared spend ledger is explicitly introduced.

## 14. Invariants and liveness

1. Research scheduling, popularity, and foreign admission cannot create validation acceptance.
2. Every satisfaction assessment binds a `RelianceQuery`—direct or deterministically derived from a work item—plus exact inputs, context, available closure, validation basis, policy, and reliance epoch.
3. Parent satisfaction requires direct accepted evidence or accepted composition; ordinary workflow completion is insufficient.
4. A proof of a formal child cannot close a semantic-intent parent without the separate fidelity contract.
5. Leases have no mathematical authority.
6. Duplicate messages, attempts, and capability action IDs are idempotent.
7. Inter-cell anti-entropy exchanges candidates; every independently operated receiver applies its own admission even when policy roots match.
8. Direct set union applies only to immutable facts already committed by one logical admission authority under its declared crash-fault replica model; mutable spend state never uses this merge.
9. Conflicts are preserved; exact `(supported, refuted)` state is not automatically reusable in the strict profile.
10. Only certified exhaustion plus checked containment can suppress work; ordinary failures remain hints.
11. Similarity cannot justify semantic deduplication, substitution, support, or merge.
12. Automatic reuse preserves exact contexts, dependencies, contracts, and validation boundaries.
13. Unvalidated challenges cannot disable support.
14. Once a defect is admitted, no stale affected path returns `ACCEPT`; recomputation work per transition remains bounded.
15. Mandatory diversity uses locally observed or authorized failure domains, not raw counts, endpoint names, or self-report alone.
16. Task, decomposition, validation, graph, retention, and replication amplification are bounded by scoped demand tickets, per-candidate atomic reservations, unique execution claims, authoritative meters, and nonreclaimable descendant-issue allowances.
17. Capability replay cannot enlarge permission, nonreclaimable fanout, or action-record allowance; every fresh accepted capability action atomically consumes one finite control-record unit, and child issuance reserves the child's complete allowance. Capabilities allocate no mathematical-work resources. Root constructors require absent parent tags, while child transitions bind exact parents. Demand replay, sibling-ticket issuance, concurrent reservations/claims, exact child-ticket/child-grant spend roll-up, terminalization, and concurrent child issuance cannot exceed any ticket or ancestor grant ledger's componentwise ceiling, nonreclaimable issue/fanout allowance, or redemption allowance, and no fresh action can resurrect a terminal allocation.
18. Equal admitted facts, available objects, terminating checker outcomes, schemas, policy, and reliance overrides yield equal views.
19. Missing or ambiguous validation material and unavailable closures fail closed as `UNKNOWN`, never acceptance.
20. Unadmitted input may change bounded screening telemetry only; it cannot change stable views, protected caches, routing queues, or durable anti-entropy.
21. Every stable support or refutation path is a finite grounded signed tree with receiver-locally accepted leaves, and its exact tree satisfies the receiver's `RelianceQuery`; a producer work item is not required.
22. Quarantine, supersession, and release affect stable reliance only through immutable locally admitted facts or a versioned policy.
23. A decomposition cannot weaken its parent's acceptance or fidelity contract.
24. A valid artifact has no right to durable promotion without receiver demand or an exploration debit.
25. Every base work, publication, evidence, and reuse path is valid with `coordinationScopeRef` absent.
26. Coordination-scope membership is excluded from native evidence validity and stable support; a different evidence/fidelity contract has a distinct exact ID.
27. Before receiver selection and reservation, a publication hint changes only bounded expendable hint state, telemetry, advisory ranking, and quota-charged nonamplifying hint dissemination; it cannot trigger payload work.
28. A sender-created identity, goal, topic, namespace, or coordination scope cannot create a receiver service class or positive queue share.
29. Evaluation-suite targets, weights, and hidden annotations cannot change live admission, promotion, validity, scheduling, or stable support.
30. One admission has a statically bounded induced-cost vector before another decision is needed.
31. No task, publication, or worker event requires broadcast or state proportional to total worker count \(N\).
32. Untrusted natural-language fields and checkpoints cannot change system instructions, grant tools, or execute outside a sandbox.
33. Exactly one atomic execution claim can move a reservation from `RESERVED` to `RUNNING`; every protected action binds that exact running reservation, execution ID, and authenticated principal, and one receiver-controlled meter/hard envelope bounds their aggregate use.
34. Every settlement component records either authoritative receiver-side accounting or a conservative declared recovery upper bound; claimant-reported usage cannot release capacity, and a running reservation never returns to `RESERVED`.
35. Any event that may change strict support, path blocking, contract acceptance, or closure availability publishes the changed state, dirty seeds, and next reliance epoch at one linearization point (or remains in a fail-closed in-progress epoch); an older cached `ACCEPT` cannot survive without an exact current-epoch tree check.
36. Receiver deadlines use crash-safe ordered time: a writer restart/failover cannot move time backward or extend a grant, ticket, reservation, or running claim, and old-writer running claims recovery-finalize before new protected work.
37. Atomic promotion covers one local authoritative transaction only. Pre-verdict work may create only inert non-admitted staging under the running claim; every actual nontransactional or remote effect originates after a committed `PROMOTE` outbox intent and requires a distinct funded execution. An outbox intent alone is neither authority nor completed availability.

The liveness claims are separate:

- **queue liveness:** a continuously ready task already admitted to an honest cell eventually starts another attempt if its compatible class retains positive fair-queue share, a capable non-crashed worker is reachable infinitely often, jobs are bounded, and admitted load remains within the declared envelope;
- **routing liveness:** under the fixed Core v0 roster, eventual communication, and progressive exploration of every previously untried eligible cell, a retained task eventually reaches a matching reachable cell if one exists;
- **subscribed-discovery liveness:** a persistently retained hint reaches a subscribed reachable receiver only under fair hint dissemination on a matching exact-key, structural, or interest shard; arbitrary unsolicited work has no global discovery, validation, retention, or attention guarantee;
- **replica dissemination liveness:** under fair anti-entropy, facts already committed by one logical admission authority and their retained closures eventually reach its subscribed reachable crash-fault replicas;
- **inter-cell candidate liveness:** under fair candidate anti-entropy, retained candidate identifiers and available closures eventually reach subscribed reachable independent cells, but local admission may legitimately reject them.

These guarantee an attempt or delivery, not a mathematical solution or a bounded delay without stronger assumptions.

Replica evidence convergence holds only within one logical admission authority, under its declared crash-fault model, quiescence, equal committed retained facts, equal available closures, equal schemas/checker outcomes/policy/reliance overrides, eventual dissemination, and terminating validation. Independent cells may legitimately diverge even when configured with equal policy roots because each re-admits candidates and may observe different availability or local incidents.

## 15. Minimal APIs

```text
create-local-work-item
admit-work-item-locally
create-coordination-scope
publish-artifact
publish-publication-hint
disseminate-publication-hint
subscribe-interest
issue-budget-grant
issue-demand-ticket-from-grant
issue-child-demand-ticket
advertise-demand-offer
reserve-demand
claim-demand-reservation
cancel-unclaimed-demand-reservation
finalize-demand-reservation
finalize-demand-ticket
finalize-budget-grant
issue-permission-capability
admit-candidate
search-integrated
propose-decomposition
advertise-capability
offer-resources
claim-attempt
heartbeat-or-checkpoint
submit-work-report
submit-evidence
submit-failure-capsule
propose-relation
certify-relation
challenge
impact
record-reliance-override
validate-fidelity
evaluate-reliance-query
propose-abstraction
validate-refactor
show-frontier
show-knowledge-state
```

## 16. Open questions for CP-002

1. Which object fields determine exact goal identity across Lean surface/elaborated forms?
2. Which dynamic decompositions can be compiled into acyclic snapshots safely?
3. How are finite search regions represented so failure subsumption can be checked?
4. Which incremental support engine and dirty-root index scale while preserving fail-closed queries?
5. Which caveat-capability construction and authorization ledger enforce proof of possession, idempotence, attenuation, and nonreclaimable fanout while every protected resource action remains bound to the unique running execution and authoritative grant/ticket/reservation meter?
6. Which hard capability vocabulary minimizes routing regret before learned ranking is justified?
7. How are receiver-local utility and downstream unlock estimates kept separate from external frozen evaluation value and hidden benchmark annotations?
8. Which exploration-ticket and fair-queue policies prevent both valid-junk flooding and rare-domain starvation?
9. Which leases, checkpoint intervals, and speculation limits minimize waste under heavy-tailed runtimes?
10. What operational identity/failure-domain evidence is necessary for resource control, semantic review, and diversity without importing political attribution?
11. Which exact Lean workload supplies formalization mismatches, controlled ground truth, and held-out reuse?
12. Which retention contracts make accepted proof closures recoverable without unbounded storage?
13. Which canonical `PublicationHint`, `InterestSubscription`, `CoordinationScope`, `budgetGrantID`, `serviceClassID`, and domain-separated `routingKey` schemas pass the zero-scope trace?
14. What minimum local research loop demonstrates nontrivial useful task closure before federation and coordination are evaluated?
