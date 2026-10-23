# Demand-oriented mathematical reuse without compulsory per-contribution proving

2026-10-22. Author: storage_integration_adapter. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

This is a source/theory architecture audit, not implementation authorization or
a v5 release claim. Assembly work stopped at the user's redirect. No test,
build, proof, native check, product edit, Git mutation or operation rerun was
performed. Existing failures, expensive proofs and partial successors remain.

## Main decision

**Make ordinary checked contribution cheap; make mathematical acceptance
explicit; purchase portable proof compression only where its whole cost is
justified.** A contributor should not have to produce a cryptographic proof for
every result. A recipient should not have to trust the contributor. These are
compatible requirements, but not equivalent to promising that every arbitrary
cold request can always be satisfied cheaply and immediately.

The central new implementation opportunity is a **protected local accepted
mathematical environment that survives operation boundaries**, separate from
ephemeral operation capabilities and resource grants. The central distributed
policy opportunity is **shared, demand-selected frontier certification**, not
certification on every publication. Neither is an excuse to weaken cold
independent acceptance.

For a cold reader, if no suitable certificate, independently checkable short
reproof, or other sound bounded evidence is available, the no-ancestry-replay
route must return NEED_WARRANT or UNAVAILABLE_WITHIN_BUDGET. It must not silently
download/check an unbounded history, trust a remote checked badge, or call its
failure to serve the result a solved scalability problem. Providing enough
useful, available bounded-cost warrants is a real remaining service obligation.

## Current architecture: what is already present

This audit resolves current logical sources through the retained130-entry input
map `experiments/v5-local-checks/distribution-candidate-preflight-01-input.json`
(SHA-256 `25e7c849e41f394498e21a60cc7800ecffb67b0cee1b3911d7164977ce4f2364`).
The later installed-producer144-source assembly preserves those130 entries.
Historical guide paragraphs must not be used as evidence that implemented
mechanisms are missing.

| Mechanism | Current evidence and boundary |
|---|---|
| Ordinary new native deltas above certified I/A frontiers | Implemented in the mixed evidence path. Actual U-to-V renewal uses a genuine U receipt, imports its interface and independently checks V's new witness without U's theorem ancestry. V need not already have its own receipt. |
| Exact-J frontier replacement | Mixed import sessions explicitly choose existing/incoming representations of the same exact journal. Selecting a certified representation terminates that branch's serialized native ancestry. Exact semantic conflicts and unestablished journals are rejected. |
| Generic exact-target seal preparation | `aggregate_claims.prepare_mixed.prepare_mixed_seal` already selects the complete required backward closure, preserves witness bytes, exact target and genuine receipt candidates, and constructs a sealing input. Do not build this again. |
| Native complete-closure checking | `native_closure` already checks a small complete DAG with no cryptographic assumptions. It still replays that closure and has no ordinary semantic/source-authoring integration. It is not the strict cold ancestry-free route. |
| Formal discovery, exact acquisition, custody, semantic reuse | These are already substantial separate components. Index authentication is not mathematical authority; semantic bodies remain independently needed when computation demands them. |
| Same-live caches | `candidate_preflight/client/workspace_evidence.py` caches receipts, aggregates and packets inside the live client. `incremental_native/mixed_claims/receiver.py` memoizes exact conditional native checks from its last admitted packet, while re-establishing current premise obligations. |
| Persistent local checking-policy adoption | `validation_phase/admission/trust.py` persists the adopted support identity and withdrawal marker. This is not a persisted database of accepted mathematical facts. |
| Cross-operation mathematical authority | The inspected installed APIs do not expose a protected persistent accepted-environment import. `candidate_admission/admission/verifier.py` clears handles on close. Same-live caches and native memoization clear on closure/revocation. Saved reports are explicitly not reloadable authority. |
| Reused installation checks | `standalone_validation/admission/pin_phase.py` coalesces stable synchronous checks only within one phase, then rechecks; it expressly is not an acceptance cache. Do not propose this existing phase optimization as new persistent reuse. |
| Selective/rent-or-buy certification theory | Already present in the guide, SELECTIVE-CERTIFICATION-POLICY and growth notes. Repeating that inequality does not implement an economical shared service or establish sufficient demand. |

The guide's statement that the delta route is merely proposed is stale relative
to current source and actual renewal evidence. Conversely, the small native
closure component is not already a durable general Lean library. The current
core remains a restricted Lean-compatible checking profile, not full Lean or
Mathlib support; changing scheduling does not settle checker correspondence.

## Separate six things the protocol currently risks conflating

1. **Discovery:** a query finds a candidate declaration/module or evidence
   representation. A relevant result need not have been mathematically accepted
   by this reader. Index coverage and candidate status must be explicit.
2. **Conditional checking:** a witness establishes that an exact extension is
   valid if named exact parent judgments are valid. This is a useful checked
   derivation, not unconditional discharge of those premises.
3. **Independent warranted acceptance:** the local checker has established all
   premises under its adopted foundation, policy and implementation assumptions.
4. **Custody:** exact bytes are retained and retrievable for a stated horizon.
   Retention is neither acceptance nor an assurance of perpetual availability.
5. **Reuse:** the accepted interface and demanded semantics can participate in
   a new local checked derivation. Validity alone does not supply missing bodies.
6. **Portable certification service:** someone produces and retains a compact
   independently verifiable warrant for selected mathematics. It may be the
   contributor, a consumer, a university, or an independent service. None becomes
   mathematical authority merely by being a service operator.

These are facets, not one global linear ledger. Different peers may discover,
hold and warrant different representations. A publication flag cannot imply
that every peer has accepted the result. No global research agenda, universal
task list, attribution system or consensus vote is required.

An openly published unverified or conditional packet remains untrusted data.
The current integrated publication path generally starts from locally admitted
evidence. A new unrestricted conditional-only publication lane is not assumed
implemented and is not the first recommended change: it also creates spam,
indexing, status and storage obligations. Existing cheap locally admitted mixed
packets already remove the need for a new certificate on every contribution.

## Precise acceptance and locality contract

Fix a foundation F, semantic policy P and adopted checking implementation A.
An exact journal J binds the mathematical module/interface commitment and the
relevant instance metadata. Let Valid(J) be its intended mathematical judgment.
Let R_A(w,J;J1,...,Jk) denote the conditional native checking relation. The needed
semantic property is

    R_A(w,J;J1,...,Jk) and all Valid(Ji) imply Valid(J).

This is conditional on the adopted checker-to-mathematics correspondence; it
does not follow from an execution hash. Cryptographic warrant verification has
its own soundness and recursive-composition assumptions. Hash commitments bind
selected bytes but do not prove the extension relation.

For reader i, define K_i as exact judgments that its trusted local acceptance
mechanism has already established and whose required policy support remains
accepted. A receiving plan consists of a finite acyclic native-delta graph D,
authenticated interfaces/needed bodies, and leaves established either by K_i
or by fresh successful verification of an adopted portable warrant. Every local
node must be checked against its exact parents. Topological induction proves
the requested target valid. A missing parent, circular support, stale cache or
incorrect interpretation is not a base case.

### Exact cut condition

For child-to-premise graph G and chosen available warranted cut S, delete the
outgoing edges of each selected cut member. The remaining native work is
Reach(G_S,target) minus S. All paths to every omitted ancestor must intersect S.
This is the existing exact-cut argument, not a newly invented proof system.

Replacing one popular node does not cut every branch. If T depends on certified
X and native Y, and Y depends on Z, T still requires Y and Z unless another
accepted cut or independently checked alternate derivation removes that path.
Merely placing Y in an aggregate commitment does not help without a valid
membership opening and actual representation selection.

For a successful plan, the intended receiving cost is

    C_i = C_frontier-verification + C_uncached-tail-checking
        + C_interfaces-and-needed-semantics + C_acquisition-and-controller.

There is no required term for proof ancestry behind S. There can still be large
interfaces, computational bodies, tails and search costs. Resource-vector bounds
must cover total bytes/nodes/edges/checks/CPU/peak memory/latency, not depth alone.

**Cold** means K_i contains no project-specific preaccepted mathematics beyond
the explicitly adopted foundation. Such a reader cannot use another reader's
K as its own. A strict ancestry-free request selects a finite tail envelope
independent of the omitted global history, and requires a supported certificate
or short complete proof to close its frontier. Choosing a bound after silently
fetching all history does not satisfy that contract.

**Warm** means useful exact judgments are already in K_i. A warm reader can
accept small extensions without rechecking old proofs even where no portable
certificate exists. This is local continuity, not a transferable proof claim.

## Persistent mathematical validity, fresh operational permission

Closing a process or exhausting its CPU allowance does not logically make a
proved theorem false. Current ephemeral handles intentionally combine valid
mathematical observations with owner liveness and finite operation authority.
That safe implementation choice should not be mistaken for a mathematical
necessity to forget every accepted fact between operations.

The proposed split has two different records:

- **Accepted-fact record:** exact J and semantic commitment, foundation/policy,
  accepted checker/verifier support identity, evidence class, checked immediate
  dependencies and trusted-local validation origin. It states an already
  established judgment. It contains no unspent CPU, deadline or live process.
- **Operation capability:** a newly issued reference to a permitted accepted
  judgment, bound to a fresh owner, current policy support, current context,
  resource grant and deadline. Closure revokes this capability but need not
  erase the underlying fact record.

### Sufficient trust conditions for a local accepted-environment cache

1. Only the locally adopted acceptance kernel/validation service can create or
   promote records. Remote API input, copied PASS JSON, a signer or a database
   row supplied by a peer cannot create one.
2. The cache has authenticated integrity and atomic commit under an explicit
   local trusted-OS/storage model. A hash beside mutable data is not sufficient
   against an attacker able to rewrite both. A protected service-owned store or
   local authenticated root can be an implementation; no claim of hostile-host
   security is implied. Untrusted evidence blobs remain separate from authority.
3. A record commits the exact semantic environment and checking support, not
   just a theorem name or source filename. Every imported premise was actually
   established before promotion. Definition bodies, universes, declaration kinds,
   module/group identities and dependency versions cannot drift underneath it.
4. At reuse, the required policy/checker support remains adopted. A withdrawal
   invalidates permission to rely on affected cached facts and their dependent
   records until independently re-established under an accepted support set.
   Switching backend/policy or checker bug repair does not automatically
   grandfather prior results. Conservative domain-wide invalidation is a safe
   first design; dependency-selective invalidation is an optimization.
5. Withdrawal/invalidation must survive restart under the stated threat model.
   The current TrustDomain explicitly excludes hostile whole-directory rollback;
   a persistent cache must either retain that limitation clearly or add a real
   anti-rollback mechanism. A cached positive must not override a newer denial.
6. Restart verifies the protected cache root/epoch and metadata before issuing
   fresh capabilities. It need not replay every proof if that record is trusted
   local state; it may have to check selected data integrity and environment
   deserialization. Deserialization and native-environment restoration become
   explicit trusted implementation boundaries.
7. New operations receive new finite grants. Prior failure charges, consumed
   allowances, suspended jobs and old handles are never resurrected. An uncertain
   partial validation transaction cannot become a committed accepted fact.

**Inductive argument:** start with a trusted empty/basis cache. The sole promote
operation inserts J only after successful sound validation and established
dependencies. Integrity-preserving storage retains that invariant across process
boundaries. Current-policy checks and new capabilities restrict permissible use;
they do not derive new mathematics. Hence cached local reuse is sound under those
explicit local assumptions, without trusting another machine's assertion.

A conditional-check memo is weaker: it can retain R_A(w,J;parents), but a future
operation must still establish the same parents. A bare memo or history-of-use
flag must not be promoted into an unconditional cached J. Legitimate promotion
instead passes through the normal acceptance transaction, which records the
actually established parent assurance lineage and current adopted policy.
The installed incremental native memo already respects the conditional boundary;
the proposed durable acceptance transaction is a separate implementation seam.

The cache can avoid repeated receipt/native checks and repeated construction of
already accepted environments. For m operations needing the same established
closure, an idealized comparison changes m*C_check into
C_check + m*C_lookup + C_cache-maintenance; the new incremental cost is worthwhile
only if (m-1)*C_check exceeds lookup/maintenance overhead and actual unchanged
semantics/authoring work is not counted as eliminated. Current large operation
overheads suggest potential payoff but do not measure that inequality. Source-
pin phase deduplication and same-live cache hits must remain in the baseline.

This cache changes local software trust/state design and requires focused
review. It is not implemented by persisting existing handles. It does not let
a new arbitrary cold consumer skip its initial mathematical validation, and
exporting its database as a supposedly checked snapshot changes the trust model.

## Demand-oriented protocol, using existing primitives

### Contributor path

An agent chooses its own mathematical work, reuses current local accepted facts
and available frontiers, and checks the new delta. It offers the exact immutable
packet plus applicable interface/semantic custody through existing publication
and discovery machinery. It need not run a cryptographic prover. Local index
providers can choose bounded admission/retention policies; contribution does
not create a permanent global storage entitlement.

The contributor also advertises available evidence variants and bounded cost
hints. Hints are untrusted planning data, never acceptance. Do not conflate
"locally checked by supplier", "bounded complete proof supplied", "receipt
available" and "request for certification". Current exact offered variants
should be reused before introducing a new general record framework.

### Consumer path

1. Discover formal candidates under a bounded search/coverage contract.
2. Select a mathematical target and exact admissible evidence instances. Consult
   local K_i and existing custody before any new network or certification work.
3. Try an already available sound bounded route: valid local cache, short native
   tail above accepted cut, available portable receipt, or supported independently
   checkable alternate proof. Choose by estimated whole incremental cost and
   resource feasibility, not by a universal priority for receipts.
4. Independently validate the selected route and authenticate semantics. Only
   then issue fresh local reuse capabilities. Preserve existing valid work when
   the implementation has an explicitly clean refusal boundary.
5. If the strict cold route cannot close its premises within budget, return a
   typed unmet warrant/capacity condition. Optionally ask a service for a quote,
   continue other research, or use a separately explicit native-replay contract.

An optional replay route is honest and sometimes useful, but it is not a
successful strict cold ancestry-free delivery. Nor is a deferred request a
successful availability result.

### Shared certification service

A service accepts an exact target/cut, accepted proof profile, finite input
material and an explicit cost/latency contract. It reuses already available
certificates, coalesces identical jobs within its own scope, executes only funded
work, retains successful checkpoints, and returns a normal portable certificate.
Recipients independently verify it. The service may be untrusted for mathematical
correctness; it is still trusted only to the extent of any claimed delivery SLA.

Job identity must bind the actual obligation and accepted profile. Exact-J
renewal and a new proof instance of the same semantic module are not silently
interchangeable. An alternate proof can be accepted as a separately checked
instance; rewriting exact-J ranks/premises to fit it is forbidden. Current
variant-selection APIs already expose this distinction.

No universal scheduling ledger is necessary. Local services can use bounded
in-flight coalescing and explicit custodian/provider advertisements. A request
lease is a coordination hint, not proof of exclusive global work. Partitions
can cause duplicate investment; its cost must be included. Usage counts alone
are trivially inflateable demand signals. Bounded owner commitments or budgets,
not apparent popularity, should authorize expensive jobs. A payment mechanism
is not needed to model the physical resource commitment.

Certificates need corresponding selected member openings and demanded semantic
custody. Independent providers must be replaceable. Outsourcing computation
changes who bears resources and may improve hardware efficiency; it does not
automatically reduce total work, guarantee timely service or preserve data after
all custodians vanish.

## Full-cost decision model

Compare the same outcomes over horizon H under equally optimized libraries:

- L: isolated local development, with ordinary compilation/proof search and cache;
- O: ordinary shared proofs/methods, valid local caches and the same indexes;
- C: O plus selectively available portable certificates or other warranted cuts.

Sharing can beat L without C beating O. Conversely, a cold-availability reason
to buy a certificate need not be an economic saving. Keep these two objectives
separate. Methods and abstractions can enable useful downstream work without
counting every theorem record as additional mathematical capability.

For candidate cut S and reader events i, let d_i be the optimized feasible O
cost and c_i(S) the C cost, including required acquisition, checking, semantics
and attributed service. Let F(S,H) include extra certificate generation,
unsuccessful attempts, coordination, publication, retention, replication,
repair, updates and retirement. With fixed nonnegative physical-resource
prices w, choose S economically only when justified estimates/bounds support

    sum_i w dot (d_i - c_i(S)) > w dot F(S,H).

Use a resource vector when prices are not justified. Peak memory and deadlines
are feasibility constraints, not resources to add indiscriminately across uses.
Payments between participants are transfers, not a second physical CPU charge.
Warm hits in both routes contribute almost no cold-verification saving.

Current retained U production used36,413.71875 known CPU seconds. That is a real
warning against compulsory per-contribution proving, not a proof that all
certificates are uneconomical. Actual02's conditional native V check used
0.015625 Job CPU seconds; this is not the complete counterfactual receiving
cost for U or V. If the
true per-reader certificate saving is nonpositive, no number of readers makes
that CPU-only comparison favorable. If positive, the relevant count is genuinely
otherwise-uncached, eligible admissions within supported retention/policy life.

### Rent-or-buy: narrow theorem, not a global solution

For one fixed cut, suppose a successful certificate costs known all-inclusive S,
each next extra direct-check cost delta_i>=0 is known before choice, baseline
per-use costs cancel, and one controller prevents duplicated buys. Rent while
accumulated rent plus the next delta_i stays<=S; otherwise buy before that use.
The incremental cost is at most2*min(S,sum delta_i). If no buy occurs it equals
the rental total; if a buy occurs prior rent<=S and total<=2S.

Unknown cost, failed production, changing caches, unavailable data, maintenance
outside S, independent competing buyers, or a direct route forbidden by the
strict cold budget remove that guarantee. In those cases the rule is a bounded
heuristic or capacity decision, not a theorem about the deployed network.

### Frontier choice is not simply "certify the most used theorem"

A general DAG can have complementary cuts. Let T depend on A and B, and both
depend on expensive old Z. Certifying only A still leaves Z via B; only B still
leaves Z via A; both can remove Z. The marginal ancestry saving of B is larger
after A is certified. Thus a blanket diminishing-returns/submodular claim for
frontier benefit is false. A greedy popularity rule needs its own assumptions
or is only a heuristic. Existing exact closure enumeration can price small
candidate cut sets without a global optimizer or another proof backend.

## Verification debt and genuine continued operation

Demand-driven certification does not repeal capacity conservation. Distinguish:

- Generated mathematical data, which may remain locally useful without a seal.
- New required **compression work** for the chosen cold-delivery service class.
- Available certificate production, retention and repair capacity.

Let A(t) be admitted required compression work up to t, after truthful reuse and
coalescing, measured in a suitable work unit. Let S(t) be successful service in
the same unit. With no initial backlog, the unfinished-work backlog is bounded
below by max(0,A(t)-S(t)); a proper queue model additionally accounts for timing.
If liminf A(t)/t exceeds limsup S(t)/t, backlog cannot remain bounded. A small
snapshot runtime or a timeout ceiling does not establish a successful service
rate. Multiple recipients requesting one cut should be coalesced, not counted
as multiple compulsory proof jobs; new unrelated demanded cuts cannot be
coalesced merely by counting them together.

In a deterministic work-conserving single-server work model with zero initial
backlog, assume the interval arrival curve A(t)-A(s)<=b+a*(t-s) for every
0<=s<=t, and guaranteed rate mu>a throughout each backlogged interval.
Then backlog<=b. A rate-latency service model needs its explicit latency term
(for service curve mu*(t-L)^+, backlog<=b+a*L). An origin-only bound
A(t)<=b+a*t is insufficient: a late accumulated burst can exceed b.
General parallel proof jobs require memory/concurrency,
burst, tail-latency, failures and maintenance reservations, not just mean CPU.
The current evidence does not establish such an SLA.

If genuinely necessary certification demand persistently exceeds capacity, the
system must add resources, reduce the cost with a justified method, reduce the
served target/delivery class, tolerate waiting/refusal, or relax the assurance
contract explicitly. Contributor productivity can continue locally, but cold
network availability then lags behind knowledge creation. Calling the backlog
"optional certification" does not make the original global reuse goal satisfied.

Batching compresses a supported cut and may amortize fixed overhead; it does not
guarantee arbitrarily high throughput. Starting renewal before a finite tail is
full helps only if completion latency and incoming work are bounded. Retention,
opening availability and service funding are separate from mathematical validity.

## Cheaper proof routes: opportunities and limits

| Route | Where it can help | What it does not establish |
|---|---|---|
| Protected persistent local accepted environment | Avoid repeat validation/import of previously established exact math across local operations; incremental contribution can remain cheap | No portable warrant for a new cold peer; not safe by deserializing old tokens or trusting remote reports |
| Ordinary proof exchange and DAG deduplication | Avoid repeated discovery/elaboration and duplicate proof bytes; check each distinct missing node once | A large cold missing closure still costs its missing work; compiled artifacts need their own stated trust basis |
| Direct short reproof/proof reconstruction | A new proof can derive the same result from the consumer's existing warranted basis with much less history | A shorter proof is not guaranteed discoverable or checkable cheaply for arbitrary mathematics; tactics are not authority and their imported lemmas still need warrant |
| Reflection/specialized certificates | Polynomial identities, decision procedures or other supported families may have small independently checked certificates, sharing a proved checker/soundness method | Correctness of the specialized checker and its connection to the accepted mathematics must be justified; it is not a generic replacement for every Lean declaration or hidden premise |
| Demand-selected checkpoint compression | Pay once for cuts that remove repeated eligible cold work; bounds subsequent selected tails | Proof cost and service backlog remain; certifying an unrelated popular node does not cut every needed path |
| Alternative succinct/recursive backend | Could reduce trace/prover overhead substantially while retaining independent cold verification | Requires a new concrete assurance/implementation case; a backend name or asymptotic slogan supplies no measured constants or automatic checker correspondence |
| Outsourced proving | Shifts hardware and operating burden; untrusted prover outputs can remain independently checked | Does not itself lower total resource use or guarantee availability; contributor relief is not system-cost elimination |
| Trusted library snapshots or quorum attestations | Can give rapid cold import under explicit trust in the publisher/threshold and its checking practice | Not the current independent no-trusted-peer assurance; many signatures do not turn a false checked flag into a mathematical proof |
| TEE attestation | May certify which checker ran under a stated hardware/firmware/attestation trust model | Adds vendor/attestation/side-channel/rollback assumptions; not equivalent to cryptographic proof of correct checking |
| Optimistic/fraud-proof acceptance | May amortize ordinary checking where an honest available challenger can reproduce a disputed step | Without that assumption and timely data/challenge access, absence of challenge does not imply correctness; strict acceptance must wait for independently sufficient evidence |

There is **no asserted impossibility theorem** that every independently checked
cold mathematical result needs expensive cryptography or its original history.
A short ordinary proof can avoid both. The actual claim is narrower: the current
architecture has no generic rule that turns arbitrary asserted checked state
into cheap independent evidence. Choosing an evidence route must exhibit and
check its real justification rather than assuming a universal compression oracle.

## Minimal consequential next design work

1. Specify the persistent accepted-environment boundary and fresh-capability
   issuance over current TrustDomain/resource accounting. First assess whether
   retaining a protected local daemon/environment is sufficient before designing
   crash-durable cache migration. No saved PASS loader or allowance reset.
2. Define explicit consumer delivery modes and outcomes, especially strict cold
   bounded delivery versus optional native complete replay. Preserve current
   exact-J and semantic bindings. Do not add a new protocol merely to label
   distinctions an existing API can expose clearly.
3. Make the operating policy native-first and cache-aware. Certification is an
   independently selected shared service investment, not publication tax. Reuse
   existing generic seal preparation and finite scheduler if chosen.
4. Select one concrete high-demand cut or short proof family whose whole-cost
   advantage or essential capacity role can be argued from actual dependencies.
   A tiny new theorem requiring hours of proving is not a sensible default
   continuation merely because the previous integration seam now exists.
5. Keep the cold frontier/service coverage obligation visible: under specified
   workloads and finite support horizons, enough useful requests must complete
   within budget. Correct refusal alone does not make the final system usable.

These changes preserve decentralized independent mathematical trust while
separating durable knowledge, short-lived permission and occasional shared
compression. They are architectural candidates with explicit obligations, not
claims that a complete deployable v5 has already been achieved.
