# CP-001D: operational paper cases

Date: 2026-09-19  
Status: Specified executions and hand-checked derivations, not executed tests or measured benchmarks

Companions: [integrated design](../../spec/OPERATIONAL-CORPUS-V1.md), [mathematics](../../spec/OPERATIONAL-CORPUS-V1-MATHEMATICS.md), [network](../../spec/OPERATIONAL-CORPUS-V1-NETWORK.md), [organization](../../spec/OPERATIONAL-CORPUS-V1-ORGANIZATION.md), and [conditional arguments](CP-001D-conditional-safety-arguments.md).

Names A, B, and C denote independently operated nodes and their external investigators. Symbolic identifiers below stand for distinct correctly calculated IDs in a future conformance fixture; they are not claimed production hashes. Byte and timing numbers are explicit hypothetical fixtures. This paper does not claim a compiled Lean artifact or measured end-to-end run.

## Bootstrap without a central service

A new operator installs a locally selected Lean-Native/v1 verifier distribution and admits its exact foundation/profile inventory. Installing software is a local trust decision; a theorem peer cannot perform it through a proof package.

For an offline start, the operator imports a portable archive. The importer treats member names and all contents as inert data, checks canonical identities and closure completeness, and runs native replay with local limits. A manifest of unavailable URLs is not an archive. A valid old assessment in the archive is a foreign/historical observation, not local acceptance.

For a connected start, the operator imports a contact bundle or supplies one peer key/address. The node pins the expected key, completes the bounded handshake, negotiates supported profiles/limits, and requests one paid bounded index page. It can fail because the peer is absent, unwilling, incompatible, or malicious. None implies mathematical falsehood. Another contact bundle or offline archive is an independent recovery path.

There is no requirement that the operator obtain a universal roster or download the whole existing corpus before making a new local contribution. A zero-contact node can check and retain its own supported work. Global discoverability requires eventual communication with willing peers; it is not obtained from local correctness alone.

## A nontrivial three-generation mathematical chain

### A: finite folds in an arbitrary monoid

Take a type \(A\), an operation \(\cdot:A\to A\to A\), and \(e:A\), with checked fields

\[
(a\cdot b)\cdot c=a\cdot(b\cdot c),\qquad
e\cdot a=a,\qquad a\cdot e=a.
\]

Lean-Native/v1 can represent this as a checked structure/inductive group with explicit fields. The core conformance profile can instead use a telescope with the same types and law assumptions. These are distinct formal interfaces, not automatically equal identifiers.

Define a right fold \(F\) by the admitted list recursor:

\[
F([])=e,\qquad F(x::xs)=x\cdot F(xs).
\]

Define append in the usual first-list recursion. A proves

\[
T_{\mathrm{append}}:\quad
\forall xs\,ys,\quad F(xs{+\!\!+}ys)=F(xs)\cdot F(ys).
\]

For the empty list, the equation is \(F(ys)=e\cdot F(ys)\), the symmetry of left identity. For \(x::xs\), the induction hypothesis and associativity give

\[
F((x::xs){+\!\!+}ys)
=x\cdot F(xs{+\!\!+}ys)
=x\cdot(F(xs)\cdot F(ys))
=(x\cdot F(xs))\cdot F(ys).
\]

This is a finite induction proof over an exact interface, not evidence that arbitrary generated source compiles. A's exporter must supply the fully elaborated native terms, definitions, checked structure descriptors, and selected witnesses. The receiver checks them independently.

### B: block composition and homomorphisms

B obtains A's exact reusable closure, constructs its own definitions, and proves

\[
T_{\mathrm{blocks}}:\quad
\forall xss:\operatorname{List}(\operatorname{List}(A)),\quad
F(\operatorname{concat}(xss))
=F(\operatorname{map}(F,xss)).
\]

The empty case reduces to \(e=e\). In the cons case, concat unfolds to append; applying A's exact \(T_{\mathrm{append}}\) and B's induction hypothesis gives

\[
F(xs{+\!\!+}\operatorname{concat}(xss))
=F(xs)\cdot F(\operatorname{concat}(xss))
=F(xs)\cdot F(\operatorname{map}(F,xss)).
\]

The right side is the defining equation of the outer fold. A's result is actually used as a premise; an imported lemma name alone is insufficient.

B separately defines an exact homomorphism interface \(h:A\to B\) between two specified monoids, with \(h(e_A)=e_B\) and \(h(x\cdot_A y)=h(x)\cdot_B h(y)\), and proves by list induction

\[
T_{\mathrm{map}}:\quad
h(F_A(xs))=F_B(\operatorname{map}(h,xs)).
\]

The base case uses the unit-preservation field. The cons step uses operation preservation and the induction hypothesis. This theorem remains conditional on those explicit fields; the corpus does not assume every function preserves a monoid.

### C: reusable hierarchical aggregation

C independently imports B's closures after A has left the network. It applies the checked congruence rule to \(T_{\mathrm{blocks}}\), then instantiates \(T_{\mathrm{map}}\):

\[
h(F_A(\operatorname{concat}(xss)))
=F_B\!\left(\operatorname{map}
  \bigl(\lambda xs.\,h(F_A(xs)),xss\bigr)\right).
\]

The final step also uses a checked map-composition identity. This gives a reusable theorem for ordered block aggregation. It does not require an in-system research assignment, intention annotation, novelty vote, or natural-language translation.

Order matters. Reordering blocks is not justified in a general monoid. A contribution claiming permutation invariance without an appropriate extra premise must fail checking; strings under concatenation provide an external counterexample intuition. A correctly checked commutative-monoid refinement is another judgment with an explicit stronger interface.

### What this chain demonstrates and what it does not

The chain exercises new structures, recursion, induction, lemma instantiation, polymorphism, hypotheses, and cross-node reuse. It is richer than arithmetic reflexivity examples. It is still a paper chain: exporting and independently replaying representative Lean and mathlib artifacts is a later qualification obligation.

It demonstrates that the architecture has a place for useful cumulative mathematics without human intention fields. It does not establish a numerical acceleration factor, uniqueness, minimal proofs, or exponential growth.

## Exact operational trace for that chain

Assume the locally installed foundation fits the selected deployment. Beyond that shared admitted basis, let A's selected replay closure contain 1200 objects and 12 MiB of distinct payload; B's add 300 objects and 3 MiB; C's add 100 objects and 1 MiB. Assume total closures, metadata, and checking costs fit the actual negotiated limits. These are fixture values, not measurements.

| Step | Authority and transition | Durable outcome |
|---|---|---|
| A exports | A's external client emits replay root \(R_A\) and inert native closure | No acceptance yet |
| A submits locally | A reserves fetch/check/staging/metadata resources and obtains one execution claim | Bounded operational work exists |
| A checks | Exact hash/dependency reconciliation; checked kernel replay; local policy | Native assessment for the exact root |
| A retains | Durable object staging precedes atomic admission and pin allocation | \(R_A\) is locally reusable under A's epoch |
| A shares | Local disclosure approval covers the full closure; paid indexing and HINT publication | Public serving becomes available; remote discovery is still conditional |
| B selects | B's bounded local/peer search yields A's candidate; B selects it independently | Candidate, not inherited acceptance |
| B acquires | B reserves its own receiving/checking work; A separately authorizes each read/reply | Exact closure present in B's inert staging |
| B admits | B independently checks and pins \(R_A\) | B's reliance no longer needs A online |
| B develops | External Lean client receives the exact selected interface and checked closure, constructs B's proofs | Private candidate work, outside the corpus |
| B contributes | B's new replay root \(R_B\) includes selected witnesses for actual A dependencies | Independent checking and funded retention, not mutation of \(R_A\) |
| A disappears | B loses a provider observation but still has its full local closure | No change to B's native derivability from that event alone |
| C imports | C fetches \(R_B\) from B, independently replays, and builds \(R_C\) | Third-generation checked knowledge survives the original source |

Physical deduplication at B can reuse A's exact stored objects when admitting B's extra 3 MiB. It does not omit those objects from the logical dependency closure. An export to C must include every dependency C lacks, not just B's incremental three MiB.

For a 12-MiB large-object transfer fixture, 256-KiB chunks give 48 chunks and at least 12 GET_CHUNKS calls if four chunks are returned per call, plus manifests/control. In the actual 1200-object fixture, small objects may require many more calls because each call is object-bound. Wire efficiency must be measured against the real object distribution, not inferred from total bytes alone.

## Exact duplicate, new witness, and misbound output

Start with a current locally retained pair \((P_A,R_A)\).

1. A second publisher announces the same exact pair. One current assessment and available closure suffice; no proof check is required solely because a new key advertised it. Ingress and reply costs still exist.
2. A publisher supplies a different ProofID \(P'_A\) for the same JudgmentID. Check it as another witness. Formal validity does not entitle it to another automatic permanent pin.
3. The same ProofID is supplied under a different ReplayID selecting another auxiliary witness. Its closure/footprint/check cost is not the old replay's assessment. The receiver must bind the selected witnesses.
4. A descriptor names judgment J while its supplied Proof points to K. Reject the binding. Even if the proof of K is correct, it cannot silently answer the request for J.
5. A shorter proof depends on a larger auxiliary library. Compare complete closure and reconstruction/checking costs; a shorter displayed term need not save any resource.

These distinctions allow alternative evidence and implementation improvements without treating every syntactic variant as automatically important new knowledge.

## Missing dependencies and non-grounded evidence

| Fixture | Check performed | Required outcome |
|---|---|---|
| One omitted definition body | Receiver recomputes references rather than trusting inventory | Fetch within remaining authority or UNKNOWN_MISSING_CLOSURE |
| Correctly hashed but ill-typed proof | Native checked insertion | EVIDENCE_REJECTED, not proof that no valid witness exists |
| Hidden sorry/custom axiom | Traverse all declared types/bodies/selected witnesses | Forbidden foundation dependency; no silent axiom insertion |
| Same statement under wrong profile | Exact profile binding | Separate identity and unsupported/disallowed outcome |
| P's selected proof needs Q, Q's needs P | Cycle detection before theorem insertion | Reject non-grounded selected replay |
| Safe mutual inductive group | One checked native group with allowed constructor recursion | Not confused with circular theorem justification |
| Unsupported native declaration | Fixed profile feature check | Typed unsupported/nondecision; do not reinterpret bytes |
| Closure exceeds remaining budget | Receiver-owned envelope | Stop with nondecision; no recursively extended reservation |

If a premise is only advertised by another node but its proof is absent, the receiver cannot temporarily install its type as an axiom to make downstream replay succeed.

## Conditional opposition fixture

Use \(\Gamma=(P:\mathrm{Prop},Q:\mathrm{Prop},h:P,k:P\to\bot)\). Native proofs establish both \(\Gamma\vdash Q\) and \(\Gamma\vdash\neg Q\) by eliminating \(k(h)\). Their closed theorems say that contradictory hypotheses imply either conclusion. Both belong to formal mathematics.

Required behavior: record the exact scoped relation; do not treat it as a checker failure or silently strip \(\Gamma\). If a separate accepted artifact supplies a closed inhabitant of the entire telescope under the same admitted foundation, instantiate both proofs and obtain closed False; that is the distinctly stronger basis incident.

For a closed universal theorem \(\forall n,F(n)\), a checked counterexample at \(n_0\) can prove \(\neg(\forall n,F(n))\). It does not prove the pointwise open judgment \((n:\mathrm{Nat})\vdash\neg F(n)\). Exact context/quantifier placement determines the relation.

## Pagination while the corpus changes

Let a fixed snapshot's shortest posting list have 20000 entries and its first predicate match be at position 19000. Allow 8192 inspections per page.

- Page one can return zero matches, PARTIAL_SCAN_BUDGET, and a cursor naming the next unprocessed entry at ordinal 8193.
- Page two can return zero matches and a cursor naming the next unprocessed entry at ordinal 16385.
- Page three can inspect the rest, return the match, and END_OF_LOCAL_MATCH_SCAN.

A new contribution between pages belongs to a later snapshot. The old scan remains coherent but does not include it. If the old snapshot lease expires, the next call returns STALE_CURSOR. Restarting the query is explicit and may repeat earlier results.

If output bytes fill just before a matching record is added, the cursor must leave that record for continuation. If the membership test is interrupted, the record is likewise retried. Neither an empty partial page nor a full output page establishes global or local mathematical absence.

## Computation, delivery, cancellation, and restart

| Cut | Durable state | Recovery and safety |
|---|---|---|
| Before an offer is committed | No issued authority | An unauthenticated replay creates no entitlement |
| Offer committed, CALL absent | Work/reply capacity reserved, finite admission deadline | Expiry releases unused work but not consumed issuance allowance |
| Two identical CALLs race | Single reservation/claim wins | One operation; repeated status delivery remains metered |
| Checker succeeds, admission transaction absent | Inert bytes and uncommitted outcome | Conservative terminal recovery; no accepted theorem from the orphan |
| Admission commits, advertisement absent | Retained root, exact assessment, nonauthorizing outbox intent | Root survives; a later separately funded publication may run |
| Service result commits, reply not sent | Immutable computed result; delivery allocation outstanding | Delivery worker claims separately or expires; never rerun computation to resend |
| Reply bytes partly written, delivery worker crashes | Computation result known; actual delivery uncertain | Conservatively settle delivery; neither side infers peer receipt from socket write |
| CANCEL wins before execution claim | Terminal unclaimed action | No execution; redemption cannot be reused |
| CANCEL races with running worker | Existing reservation remains spent/outstanding until terminal | Fence/terminate; late worker output cannot promote after cancellation won |
| Restart after old cursor/offer issuance | Durable new service epoch | Old authority rejected even if individual replay record later compacted |

An arbitrarily rolled-back whole-disk backup is not an ordinary crash. Without a trustworthy current epoch/accounting history, recover with a new authority identity and re-admit retained mathematical bytes. Do not reopen old spend capabilities.

A status reply computed at epoch 50 may be delivered after a local incident at epoch 51. It remains an observation explicitly labeled 50, never a guarantee about delivery time. A consuming node independently checks current local use; it does not import the remote current flag.

## Retention release versus active export

Suppose a public proof root has one durable pin and one independently funded export pin.

1. The owner releases the durable pin. The export pin continues to protect the exact closure until its actual finite expiry/termination.
2. A different retained root shares some dependency chunks. Releasing the first root does not release the second root's protection.
3. After all protections expire, the collector rechecks the exact storage generations and marks unprotected generations DELETE_PENDING under the writer.
4. New use cannot bind DELETE_PENDING generations. Actual deletion is metered afterward; a crash leaves unavailable debris or a completed absent generation, not a false available claim.
5. A new contribution requiring those bytes must cancel an unclaimed deletion or install a fresh verified generation before admission.

Replacing a proof by a smaller checked witness is insufficient to discharge an exact-original-byte promise. A retention contract promising availability through a term also cannot be silently converted into best-effort cache eviction.

## Invalid input, valid-junk flood, and metadata exhaustion

A million offers of syntactically different valid tautologies in one hour need not be checked or retained. They share finite control/hint buffers and exploration allocations. Distinct keys do not create more capacity. Outside admission, a node can decline or drop traffic with no durable record per rejected object.

This protects bounded resources; it does not solve mathematical usefulness. A rare good theorem can be missed. The policy must expose that limitation and preserve direct exact-ID import and bounded exploration rather than call its selected sample the whole body of knowledge.

If proof bytes fit but the required exact dependency graph, assessments, index references, and crash records do not, promotion is declined. A bounded payload with millions of tiny references is not “cheap” merely because its byte total is modest.

## Checker incident with a clean alternative

Let a judgment have two checked replay alternatives \(R_1,R_2\). A locally admitted checker-build incident affects only the assessment basis for \(R_1\). The incident transaction publishes its conservative scope and next epoch before background repair.

Any cached positive using \(R_1\) is immediately unusable under the new local state. A current check of unaffected \(R_2\), with complete bytes and permitted foundation, can support the same judgment. If both assessments used the defective build, different proof terms do not automatically make \(R_2\) clean. Rechecking under an explicitly admitted unaffected basis is necessary.

One hundred thousand affected assessments do not become one hundred thousand unfunded repair jobs. Keep a bounded incident description and progress cursor; admit finite rechecks through maintenance resources. Safety can be immediate while recovery takes days.

## Honest capacity, overload, and transfer latency

The organization companion's ORG-SAMPLE assumes 60480 CPU-seconds/day across ordinary and exploratory native checking. At an explicitly hypothetical mean two CPU-seconds, its optimistic throughput is 30240 checks/day. At the full 60-second reservation cost without reusable unused allocation, it is only 1008 checks/day. Both statements concern resource envelopes, not guaranteed observed throughput.

With candidates arriving at \(1000\,2^{d/7}\) per day, offered load exceeds the optimistic checking envelope near day 34.43. Permanently retaining all candidates of 256 KiB each fills 150 GiB spare capacity at about 42.15 days by geometric interpolation, hence at the first integer completed-day count 43 in the stated discrete model. This hypothetical ignores the earlier checking bottleneck and root-count/metadata limits. The actual bounded node refuses work rather than growing an unbounded backlog.

Many small objects expose another bottleneck. If 1200 objects each need a manifest and one chunk call, the protocol needs roughly 2400 paid read operations, excluding additional discovery. At 50 ms request/response latency, the two-stage OFFER/CALL exchange costs roughly 100 ms per operation before service overhead. Four continuously occupied network slots give a concurrency-only estimate near 60 seconds. The separate 32-offers/second default caps issuance at roughly 75 seconds sustained, or at least (2400-64)/32 = 73 seconds with its full initial burst; the actual lower bound must respect both limits. Neither estimate counts serialized dependency discovery, parsing, TLS setup, retries, or checking. At 500 ms latency, the concurrency estimate is near 600 seconds and can exceed a 300-second export lease.

These figures are thought experiments, not benchmarks or guaranteed bounds. They motivate the explicit choice between smaller scoped exports, longer locally admitted leases within the profile, known closure enumeration before download, warm chunk reuse, and a later batched-transfer profile. The base concept must report resource/lease nondecision honestly when a closure does not fit.

## Acceptance of this paper suite

The suite is complete only as a design exercise: each scenario has a specified path and failure distinction. It does not certify that a kernel adapter, exporter, database, scheduler, or network implementation satisfies that path.

The next executable qualification, when separately authorized, should turn these exact identities, traces, and bounds into conformance fixtures and representative realistic Lean closures. It must not begin by replacing an unimplemented assumption with a successful-status flag.
