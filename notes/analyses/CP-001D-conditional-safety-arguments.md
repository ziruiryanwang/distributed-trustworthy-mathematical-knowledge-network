# CP-001D: conditional safety arguments and countermodels

Date: 2026-09-19  
Status: Paper arguments for the operational design; not mechanized proofs or implementation results

These arguments accompany the [integration contract](../../spec/OPERATIONAL-CORPUS-V1.md). Each separates the mathematical conclusion from its implementation and environmental premises. Naming a premise does not establish it. In particular, native kernel soundness, faithful reconstruction, crash durability, isolation, and cryptographic binding require their own qualification.

## Model and observation boundary

A mathematical root has an exact replay closure \(C\), a native profile \(L\), and a receiver-selected policy \(P\). Let \(G_C\) be the dependency graph after resolving the selected theorem witnesses. A group of mutually defined inductive types is one native checked declaration unit, not a circular justification of theorem witnesses.

One local authority serializes admission, policy, retention, and reliance epochs. A remote provider has its own unrelated state. The letters \(i,j\) denote authorities, not unique human beings.

For a resource dimension \(r\), let \(G_r\) be a finite grant ceiling, \(U_r\) the terminal charged usage, and \(Q_r\) the sum of outstanding reservations. This notation applies to cumulative resources; live storage, peak memory, and deadlines have separate occupancy/time predicates.

## Exact native composition

**Claim.** Given a finite acyclic replay graph, faithful reconstruction, accepted fixed foundation, and sound checked Lean declaration insertion, replay acceptance establishes the root's exact derivation relative to that foundation and its explicit assumptions.

**Argument.** Topologically order declaration units \(v_1,\ldots,v_n\). At the first unit every nonlocal constant belongs to the checked fixed foundation. Checked insertion establishes the unit's judgment using those constants. Assume the invariant for all earlier units. At \(v_k\), dependency resolution admits only foundation constants and earlier checked units. No unresolved theorem type is installed as an axiom. Checked insertion therefore establishes the next exact declaration. Induction gives the root. Closing a telescope by dependent function binders and closing its proof by matching lambdas gives the precise conditional judgment; it does not eliminate hypotheses.

For safe definitions/theorems in the core fragment, acyclic proof-only auxiliaries can be eliminated by finite substitution. The larger profile's checked inductive groups, quotient machinery, and opaque declarations need their stated native metatheory; they cannot all be justified by the same textual substitution argument. Its correctness conclusion remains relative to that explicitly stronger foundation and extension discipline.

This is a composition theorem, not a proof of Lean's implementation or consistency. A reconstructed term may be a different result from what its producer wanted. If it checks, it establishes the actual encoded judgment.

## Why contextual opposition is not automatically a defect

Let \(\Gamma\vdash p:\varphi\) and \(\Gamma\vdash n:\varphi\to\bot\). Then application gives

\[
\Gamma\vdash n(p):\bot.
\]

Closing the telescope gives \(\vdash\Pi\Gamma.\bot\), not necessarily \(\vdash\bot\). For example, take \(\Gamma=(P:\mathrm{Prop},h:P,k:P\to\bot)\). Both a conditional proposition and its conditional opposite can be proved by eliminating \(k(h)\). Their derivations are valid, and the telescope has no inhabitants in a consistent interpretation. Discarding either theorem merely because its contextual opposite exists would reject valid mathematics.

Consequently:

- contextual negative evidence is a checked relation that may establish incompatibility of hypotheses;
- a refutation of the closed judgment \(\Pi\Gamma.\varphi\) is a distinct judgment \((\Pi\Gamma.\varphi)\to\bot\);
- alternatively, checked inhabitants of the complete dependent telescope allow the two contextual derivations to be instantiated into closed contradictory evidence;
- a closed contradiction under a commonly admissible basis triggers a local foundation/checker inconsistency investigation. It does not identify which historical checker result was wrong.

The body/context split must survive both content identity and incident handling. A negative result from proof search or an unavailable proof supplies neither kind of negative evidence.

## Transport adds no mathematical authority

**Claim.** Holding the exact supported root, replay closure, checker, and policy fixed, changing a provider, signature, route, model score, or request principal cannot turn a native rejection into acceptance.

**Argument.** None of those variables is an input to the mathematical checking relation. They influence which bytes are offered, whether resources are allocated, and whether an operational observation is authenticated. The final mathematical relation consumes exact verified bytes and local admitted checking material. A discrepancy in offered versus checked identities is rejected, not resolved through provider reputation.

The same observation does not imply equal service. Two principals can have different funded access permissions without making a theorem true for one and false for the other.

## Resource conservation across ordinary and crash transitions

**Invariant.** For each cumulative dimension,

\[
U_r+Q_r\le G_r.
\]

**Initial state.** \(U_r=Q_r=0\).

**Reservation.** A new bound \(b_r\) is admitted only if \(U_r+Q_r+b_r\le G_r\); adding it preserves the invariant.

**Claim.** A unique execution claim changes no reservation amount. A second claimant cannot obtain another execution against the same reservation.

**Settlement.** For a completed reservation of size \(b_r\), charge \(a_r\) with \(0\le a_r\le b_r\) and replace \(Q_r\) by \(Q_r-b_r\), \(U_r\) by \(U_r+a_r\). The sum cannot increase. Sound meters plus hard enforcement must establish the bound; a meter that merely notices an overspend afterward does not prove it.

**Unclaimed cancellation.** Removing the work reservation is safe, but consumed issue/redemption/control-record allowances are not restored. Otherwise repeatedly reserving and cancelling zero-work jobs could create unlimited records.

**Uncertain running crash.** Do not reset the reservation. Fence the old executor and charge a conservative bound for any measurement gap, up to the reservation ceiling. Finalize once. A restarted worker requires a new allocation.

**External delivery.** Computing a response and sending it are different executions. The response-delivery allocation is already reserved but remains outstanding after computation settlement. TLS writes are metered while that separate execution is running. A lost response does not cause computation to run twice. Replay metadata and any fresh fetch still consume their own bounded service.

Live allocations use an analogous occupancy argument: new pins, buffers, queues, and scratch space are admitted before allocation, and are released only after the corresponding use terminates or ownership is transferred atomically. Neither CPU conservation nor a token count bounds disk bytes by itself.

## Epoch safety is local and linearized, not instantaneous global knowledge

Assume every locally admitted change relevant to reliance atomically publishes its facts, a conservative dirty scope, and a new reliance epoch. A status calculation reads epoch \(e\), evaluates the exact required evidence, and commits a positive observation only if the authoritative epoch is still \(e\).

**Claim.** The committed positive observation is coherent with one local state.

**Argument.** If a relevant change committed before the final epoch check, the epoch differs and the positive result is not committed as computed. Otherwise the evaluation can be linearized at that check/commit boundary. The serial writer excludes an unnoticed relevant interleaving at the boundary.

A message can be delayed after this commit. Therefore it states “reusable at node \(i\), epoch \(e\), at the observation boundary,” not “still reusable when you read this.” Another node performs its own current checking before use. Unchanging epochs do not excuse expired retention deadlines: the use gate independently checks expiry and fails closed until the local expiry transition is published.

If an evaluator cannot afford to establish that a dirty scope is irrelevant, it returns nondecision. Background descendant traversal is a recovery optimization, not the condition that first invalidates stale use.

## Closure-preserving retention and deletion

Let \(R\) be receiver-authorized live roots and \(P\) active use/export pins. A protected content generation belongs to

\[
\operatorname{Protect}=\bigcup_{x\in R\cup P}\operatorname{Closure}(x).
\]

An incoming reference is not in \(R\) or \(P\) merely because it exists. All memberships require local funded authority.

**Claim.** A collector cannot remove bytes needed by a currently admitted protected use, assuming exact reference accounting and the specified writer/worker fence.

**Argument.** The writer can mark a generation DELETE_PENDING only after an atomic recheck that it is outside Protect and has no transaction protection. New pins cannot bind a DELETE_PENDING generation. Physical deletion therefore cannot race with a newly accepted pin of that same generation. A new import either cancels deletion before its worker claim or installs and verifies another physical generation before publishing availability. After a crash, DELETE_PENDING is unavailable until explicitly recovered, regardless of whether debris still exists on disk.

Reference sharing is safe: releasing one root removes only that root's protection. Any remaining root or active pin keeps the shared generation in Protect. A grace interval reduces race opportunities but does not replace the atomic exclusion argument.

This proves local closure preservation under the premises, not survival after destruction of every replica.

## Pinned pagination does not skip unexamined entries

Fix an immutable index snapshot and a base posting sequence \(a_1,\ldots,a_n\). Let k be the last fully examined position in this proof, not just the last emitted match. ORG1's actual cursor encodes the next unprocessed exact entry \(a_{k+1}\), or its explicit end marker; it does not serialize this ordinal k. The next page therefore starts at \(k+1\).

During a page, advance \(k\) only after membership testing and either committing a matching entry to the bounded output or conclusively recording it as a nonmatch. If output capacity cannot hold a match, leave that entry unexamined for continuation. If interrupted mid-test, likewise leave it for retry.

By induction on pages, every cursor prefix consists only of fully handled entries. Thus an honest completed scan with sufficient successive allocations omits no match in the declared extracted-key predicate. Duplicate delivery after interruption is harmless under exact-ID deduplication.

This theorem does not establish unbounded progress. Each page, the snapshot lease, and query processing need enough resources. A single entry whose test cannot finish within any permitted page allowance can cause repeated nondecision; an implementation must return an explicit limit outcome rather than falsely announce completion. It also does not prove that a malicious server indexed every relevant artifact.

## Two different progress claims

**Decision termination.** With a stable local executor/supervisor, enforced finite deadlines, and funded finalization/recovery, an admitted attempt eventually reaches a success, rejection, nondecision, or error outcome. Timing out is progress of the operational state machine, not successful knowledge acquisition.

**Successful import.** Fix a finite supported valid closure and a desired receiver. If some admitted attempt obtains every missing object from authorized responsive providers, completes checking and promotion within its actual byte/CPU/memory/time allowances, encounters no relevant invalidating policy change, and obtains fair local service, it commits checked retained content. A finite replay induction and finite transfer plan establish the conclusion.

Merely assuming eventual packet delivery is insufficient. Counterexample: every response arrives one second after its offer/export/import deadline. All packets eventually arrive, but no successful attempt occurs. Eventual success therefore requires a sufficiently timely interval plus a funded retry, or an already sufficient bounded attempt. Infinite free retries are not assumed.

An export lease shorter than the transfer's possible maximum similarly provides no unconditional success theorem. Select a scope and allowance that fit one lease, or retain acquired immutable objects and request a new admitted export snapshot.

## Scale and knowledge growth are not protocol theorems

Finite nodes cannot promise to retain every distinct valid result under unbounded arrivals. Suppose a required independent payload stream has rate \(\lambda\), mean additional bytes \(b>0\), and retained fraction \(p\). A finite growth allowance \(g\) requires \(p\lambda b\le g\); fixed total storage over an unbounded horizon also requires release, added capacity, or sufficient lossless representation savings.

Counting theorems, proof terms, keys, or purported uses does not establish useful new capability. A valid proof may duplicate earlier content; an apparent reuse edge may be deliberately inserted; a rare theorem may be valuable despite low observed demand. Usage-based policy remains reasonable if it is explicitly local, bounded, monitored, and backed by exact-ID access and some exploration.

No system theorem here promises exponential useful discovery. The reciprocal mechanism can enable acceleration: a checked contribution becomes an independently reusable premise, and subsequent checked contributions repeat the cycle. Whether that mechanism produces meaningful acceleration is an empirical question under stated workloads and costs.

## Review use

These arguments identify where a draft must be repaired when it claims more than its premises establish. They do not replace adversarial traces, native conformance vectors, measured capacity, or implementation verification. The [paper cases](CP-001D-operational-paper-cases.md) instantiate the invariants and counterexamples.
