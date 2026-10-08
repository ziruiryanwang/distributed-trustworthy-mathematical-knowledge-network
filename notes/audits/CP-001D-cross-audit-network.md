# CP-001D independent cross-audit: operational network and organization

Date: 2026-09-19  
Reviewer: independent corpus/organization reviewer, separate from the NET1 author  
Scope: concept specification only; no implementation, executable model, or measured performance was reviewed  
Status: Bounded concept cross-audit completed; identified findings repaired in the hash-bound revisions below

## Audited artifacts and method

- [Operational network specification](../../spec/OPERATIONAL-CORPUS-V1-NETWORK.md).
- [Organization specification](../../spec/OPERATIONAL-CORPUS-V1-ORGANIZATION.md), inspected for cross-layer consistency; this reviewer authored ORG1, so that inspection is not independent review of ORG1.
- The native profile's selected root and ProofID/ReplayID contracts, supplied by its author and checked against the affected network clauses.

The initial recorded network revision had SHA-256 `5fef07308674fe4cdf12ba78ec63345f7d944aca64178c33253421e308381768`. The author revised the document during review. The final reviewed network revision has SHA-256 `46529c8040d8d58f9cb6c27fb4dbc148c525afc0b0fcca49788a71fd2136871b`; the cross-checked organization revision has SHA-256 `de06c32234248e74998b6f2b41139ce3b31690de9787505444a75d7efb0737f6`. The final organization change only updates its status to reviewed candidate paper specification, not implementation-qualified. Final network deltas explicitly bind the negative-proof-derived relation and distinguish control-budgeted HELLO from paid GET_ROUTES; both changed clauses were re-read. A hash identifies the reviewed bytes; it is not evidence that the specification has been proved correct.

The review used adversarial paper traces: late replies, lost replies, exhausted active-epoch metadata, different selected auxiliary proofs, private versus public content, misleading index answers, cursor boundary interruption, source disappearance, and finite deadlines under eventual delivery. No demand was made for globally optimal heuristics, universal numerical constants, unconditional availability, or a proof that mathematics grows exponentially.

## Findings and dispositions

### N1 — Eventual delivery did not imply the stated import liveness

Severity: material logical overclaim. Disposition: corrected in the live revision inspected during review.

The earlier progress argument combined eventual delivery with finite offer, service, export, and import deadlines. Counterexample: every requested response is eventually delivered, but always immediately after its admitted deadline. All providers can be honest, the closure finite, and local checking terminating; nonetheless every attempt can end nondecisively. A finite number of sufficiently large byte/CPU reservations does not remove that timing problem.

The revised specification separates bounded attempt termination from conditional successful import. Success now assumes one attempt whose necessary funded operations actually complete within their applicable deadlines, or a sufficiently long timely interval together with local policy that funds and starts a suitable attempt. It explicitly gives the late-response counterexample. This is an appropriate conditional claim; it is not a measured latency guarantee.

### N2 — Active-epoch replay metadata needed an operable retirement path

Severity: material operational incompleteness, not an identified resource-safety violation. Disposition: repaired and checked.

Offer-issuance keys remain remembered until their service epoch retires. The 32768-record/128-MiB default control cap is finite. A sufficiently long successful run can therefore exhaust its active-epoch replay/issuance metadata even when payload storage and compute remain available. Merely deleting old keys would be unsafe because old issuance requests could mint fresh offers. Refusing new work is safe, but not a sufficient specification of sustained operation.

Requested repair: a deliberate clean rollover that stops new admissions, drains or terminalizes admitted work, advances durable epoch authority, preserves accounting and the retired-epoch floor, then compacts retired replay records. It must not restore spent budget or weaken the original single-redemption rule. Such rollover need not interrupt mathematical retention roots or pretend to be a new network identity.

The final NET1 provides the OPEN/DRAINING/RETIRED/new-OPEN transition, a 75-percent metadata or 24-hour trigger, conservative reservation of terminal-record capacity, and checked counter exhaustion. Only epoch-scoped authority terminates; persistent funded storage allocations carry forward unchanged. Warm-cache clock separation was additionally refined as N9 below.

### N3 — Arbitrary incident hints did not have a compatible transport/read scope

Severity: cross-layer specification gap. Disposition: repaired and checked against the native author's precise relation contract.

`HINT` names a native ReplayID, and generic object reads require a public native closure or a live audience-bound export. The prose nevertheless described remote hints to arbitrary checker-incident/evidence content. A local operational incident is not necessarily a native replay root, and exposing generic private control records to make it fetchable would violate the existing authority boundary.

Requested repair: either provide a separately bounded typed incident mechanism, or narrow NET1 to ordinary native opposing-evidence replay plus locally authorized/out-of-band operational profile-disable events. Neither an incoming allegation nor an opposing theorem under possibly inconsistent hypotheses can directly revoke a checker or globally dirty the receiver's corpus.

NET1 chose the narrower mechanism. The transported root is the negative proof's ordinary ReplayID. The native profile explicitly makes `NativeRefutation` a bounded local derived relation, not another root kind or a generally readable annotation object. A receiver reconstructs and checks the exact target/negation correspondence from the negative native judgment. Operational checker-compromise reports remain out-of-band advisory inputs to local policy. The native contextual-opposition/closed-contradiction distinction governs whether any mathematical evidence supports a basis incident.

### N4 — Provider query needed an exact object-to-root relationship

Severity: minor interoperability/selection ambiguity. Disposition: repaired by simplifying the operation's exact target.

`GET_PROVIDER` requests an `objectContentID`, whereas each returned provider observation names a `rootReplayID`. The required relationship should be explicit: the requested object occurs in that observed root's authorized public closure, or the reply makes no such provider match. The observation still remains an untrusted route hint at the remote receiver; a responder's assertion cannot replace exact local acquisition and replay.

The final operation instead takes `[rootReplayID]` and returns only explicitly public observations for that exact replay root. It no longer claims to provide an arbitrary object-to-provider relationship or expose private reverse mappings.

### N5 — Publication withdrawal needed a delayed-reply policy

Severity: disclosure-semantics ambiguity. Disposition: repaired and checked.

An operation can read public bytes, commit an immutable response, and deliver it later using a separate ticket. Publication may be withdrawn in between. The specification should choose whether bounded in-flight disclosure authority is captured at computation commit or must still be valid at the delivery claim. It cannot promise retroactive recall of bytes already sent, nor mutate an already committed result under the same outcome identity. This is distinct from the mathematical-currentness problem in N7 below.

The final private reply intent binds a disclosure scope/version. Delivery claim atomically rechecks that version for the exact audience. Withdrawal cancels unclaimed delivery and applicable derived scopes without rewriting the result; an already running transfer receives bounded cancellation and charged settlement. Bytes already handed to TLS are explicitly not recallable.

### N6 — Cursor resumption representation needed cross-layer agreement

Severity: material interoperability issue if left inconsistent. Disposition: repaired and checked.

ORG1 now concretely encodes `[0]` for the initial source-list position, `[1,nextDescriptorID]` for the least descriptor not fully processed, and `[2]` for completion. The pinned list is ordered by exact descriptor ID. Resumption uses an inclusive lower bound. A matching descriptor becomes processed only after its output is committed to the page; a descriptor that does not fit the byte cap remains next.

A concurrent NET1 draft used "last fully examined descriptor" instead. Either convention can work with a complete, unambiguous protocol, but the same cursor cannot mean both. NET1 must refer to the concrete ORG1 next-unprocessed convention. The fixed snapshot, source-list choice, extractor and planner are bound; restarting against a newer list is not a continuation.

The final NET1 uses exactly the ORG1 union, inclusive-lower-bound semantics, and match-output-commit boundary. Its fixed query/snapshot/planner determines the same immutable base list.

### N7 — Delayed status must remain an observation of its commit snapshot

Severity: checked boundary; no open finding after revision.

The inspected revision uses `reuseAtSnapshotCode` and linearizes the positive status check at the immutable status computation commit, after a coherent epoch check. A later reply is explicitly not labeled current at delivery. A receiver independently checks its own native evidence/current epoch before reliance. This closes the stale-positive ambiguity without attempting to make network delivery atomic with another machine's current state.

### N8 — Small cross-layer bookkeeping clarifications

Severity: minor. Disposition: all listed points repaired and checked.

- The PeerDirectory's 256-KiB envelope must account for its local statistics, not merely its encoded remote contact payloads. Per-lookup tried sets also need a bounded local memory allocation.
- Service-call prose must permit the native tagged root kinds. Status fields ProofID/JudgmentID are optional for definitions, declaration groups, and opaque declarations, not fabricated identities.
- ORG-SAMPLE explicitly overrides the default root count to 131072, while leaving the NET1 hard 262144-root limit and the separate control-record limits intact. This prevents its 100000-root numerical example from silently exceeding a default 16384-root ceiling.

### N9 — Clean service rollover should not destroy still-funded warm caches

Severity: material efficiency/composition issue discovered while applying N2. Disposition: repaired through root-author integration review and cross-checked.

Tying every warm deadline to a service epoch would end all warm roots whenever finite replay metadata forces rollover, potentially every few minutes under load. This would make ORG1's one-/seven-day nominal cache model misleading and needlessly repeat acquisition/replay. Expiring such content would be safe, but not an efficient reciprocal corpus policy.

The final contract separates a remote `serviceEpoch` from the receiver's `retentionClockGeneration`. Clean same-process service rollover changes capabilities and compacts replay keys, but preserves funded warm allocations and their exact original deadlines. A real restart, writer takeover, or uncertain time-origin continuity advances the retention generation and fails old warm reuse closed. No deadline is extended, no spent resources are restored, and persistent pins retain their separate release rules. ORG1's numerical stock bounds now explicitly assume an uninterrupted retention-clock generation.

## Boundaries checked without a new adverse finding

- Reassembled canonical object identity is verified, rather than accepting chunk checksums alone.
- Every receiver independently admits native evidence and its exact selected replay closure; a foreign signature or index ranking has no mathematical authority.
- A changed ReplayID remains a different assessed evidence candidate even when the ProofID is unchanged.
- `PUBLIC_SERVE` publication requires explicit authority for the full disclosed dependency closure; checking/retention alone does not publish private dependencies.
- Generic reads do not expose arbitrary private CAS, grants, meters, checker policy internals, or control records merely because a caller knows their hashes.
- Computation and reply delivery have separately funded, single-redemption execution claims; a lost reply does not repeat the original operation or authorize free egress.
- Warm-root expiry is tested by the use predicate before delayed housekeeping; epoch rollback does not restore spend authority.
- Full locally retained replay closure makes ordinary source disappearance irrelevant to unaffected local replay. Provider receipts alone never establish that local condition.
- Public index pages distinguish a completed local scan from an empty budget-limited scan; no remote signature proves global or Byzantine-server-local completeness.
- Discovery is bounded and one-hop per request. Collection-aware peer selection plus finite later rounds can improve reach within known contacts, without claiming global completeness or Sybil-independent failure domains.
- Physical GC generations and `DELETE_PENDING` exclude reuse/delete races, including reimport of the same content identity.
- Formal validity is separated from receiver resource selection. Unsupported or over-budget content is not mathematically false.

## Assumptions and unresolved implementation obligations

The concept still relies on the native checker's stated soundness basis, correct dependency/axiom extraction, canonical encoders, SHA-256/Ed25519/TLS/HMAC assumptions, the single-writer authority fence, authoritative metering, host isolation, conservative crash recovery, and actual local disclosure policy. This review does not establish any of those implementation premises.

Discovery and successful acquisition additionally need a reachable willing path, sufficient selected storage/compute/traffic, and sufficiently timely delivery. Independence of replica failure domains is not implied by distinct keys. No universally complete index, globally instantaneous status, eternal availability, or exponential useful-growth guarantee follows.

Before implementation, the selected schemas, state transitions, durability ordering, allocator limits, parser limits, and conformance vectors require a final integrated review. Practical policy constants and heuristic ranking should be calibrated on representative workloads; calibration is not part of the mathematical acceptance predicate.

## Final revision disposition

The final hash-bound NET1/ORG1 revisions above resolve N1–N9 at concept-specification level. No remaining adverse finding was identified within this bounded review. This is not a mechanized safety proof, an implementation certification, a claim of complete adversarial coverage, or a prediction that the selected performance defaults will meet a workload. Later file changes require their own review scope and hash record.

## Supplemental independent review of the integration arguments and paper cases

The root author requested a further adversarial read after this audit note was first saved. Reviewed initial hashes were:

- [Conditional safety arguments](../analyses/CP-001D-conditional-safety-arguments.md): SHA-256 `1fec68ccfc903b229256993233dd2d7da5ee87c2edcf063a7182cee445e05d6d`.
- [Operational paper cases](../analyses/CP-001D-operational-paper-cases.md): SHA-256 `17116bc16bcbdfd089a34e470a23e3271444bc4064119ed4b2568f57832a9555`.

The finite-fold append proof, fold-of-blocks induction, homomorphism fold theorem, and final ordered aggregation consequence are mathematically correct as the stated paper derivations. They preserve the monoid hypotheses and do not infer permutation invariance. They remain uncompiled paper arguments, as explicitly labeled. The distinction between contextual contradiction and closed foundation inconsistency is also correct.

Four concrete refinements were sent to the root author:

1. The pagination proof/case uses an abstract last-processed position, whereas the selected ORG wire cursor stores the next unprocessed descriptor. Relate those explicitly and use next positions 8193 and 16385 in the 20000-entry fixture. This is the same cross-layer concern as N6, not a new theorem flaw.
2. The contextual opposition example uses a proposition Q not listed in its displayed telescope. Add `Q : Prop` or declare Q to be a fixed closed proposition, so the written judgment is literally well scoped.
3. The 2400-read-operation/50-ms-round-trip example yields 60 seconds from a four-slot/two-round-trip calculation alone. NET1-DEFAULT also caps new offers at 32/second with burst 64; its issuance alone needs at least `(2400-64)/32 = 73` seconds with the entire burst initially available, or about 75 seconds at sustained rate. These are independent bottlenecks. The 500-ms round-trip example still has a concurrency-only estimate near 600 seconds, which exceeds the default 300-second export lease.
4. The 42.15-day storage figure solves a geometric interpolation; the first integer full-day stock exceeding 150 GiB is at day count 43. That permanent-all-retention hypothetical must explicitly ignore root-count and metadata caps as well as checking capacity. ORG1 was clarified accordingly by its author/reviewer here.

The author applied all four refinements, and the changed clauses were independently re-read. Final supplemental revisions are:

- Conditional safety arguments: SHA-256 `59285df58e3c8ea641413b60da3993e3d5ac3338178ba49acaa5fd688724c06b`.
- Operational paper cases: SHA-256 `dfde5a2cc402bbb352d1d7d8b5831635b73671474a4ebbb872316250091a6614`.

No additional mathematical-soundness flaw was found in this bounded read. The claims remain conditional on declared checker, reconstruction, authority, metering, timing, and retention premises; these final hashes do not convert paper arguments into executed tests.
