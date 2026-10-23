# Consumer-driven mathematical assurance: whole-architecture reaudit

2026-10-22, root synthesis. Requested by the user after observing expensive
certificate production. This is a source/evidence/theory audit, not a new
implementation or release claim. No proof, test, build or installation is
authorized by this document. All prior evidence, including failed snapshot01,
is retained. Independent challenges are linked at the end.

## Decision in brief

The current cryptographic production path is too expensive to be the normal
price of contributing small results. Its successful execution demonstrates a
capability, not an economical default. It does not establish that succinct
certification is inherently impractical, or that a different backend will be
cheap. We should not keep paying that price simply to advance the next receipt.

The recommended organizing principle is:

> Share mathematical objects and ordinary proof evidence cheaply. Establish
> exactly the assurance a consumer needs, using its already warranted knowledge.
> Produce reusable cryptographic compression only when it earns its cost or
> supplies an explicitly funded cold-access capability.

This is a substantial shift in priority, not a claim to invent optional
certification. Native deltas, mixed certified/native evidence, exact-frontier
replacement, source-free sealing preparation and selective-certification theory
already exist. The main new opportunities are durable *local mathematical*
reuse, alternative shorter witnesses, receiver-relative evidence selection,
and a materially cheaper certification relation/backend where needed.

No proposed saving may depend on accepting an unverified imported theorem,
pretending a peer's checked-status flag is a proof, or disguising a cold
dependency traversal as constant-time verification.

### Updated decision after the user's explicit permission for compromises

The latest instruction asks us to judge the design by whether it can become a
real usable contribution to humanity, and explicitly permits compromises. The
recommended compromise is **bounded initial learning, then durable incremental
use**, not weaker mathematical checking. Make a locally checked, persistent
library the ordinary workflow. Keep independently verified ancestry-free imports
as a separately requested capability where suitable evidence is available.

This is a genuine proposed relaxation of an earlier blanket cold-import service
requirement; it must not be presented as satisfying that earlier requirement
unchanged. It does not relax the strict delivery mode itself. A caller requesting
that mode still gets a genuine bounded warrant or an explicit failure, never a
silent switch to replay or peer trust. No runtime policy has been changed by
this audit.

Concretely, a new consumer may choose to check the relevant missing part of a
specialty library once, within a stated onboarding budget. It does not download
the entire world corpus. Later work reuses that locally established environment,
checks new deltas, and acquires only demanded semantics. The missing closure can
still be large; domains can overlap; invalidation and eviction can cause further
work. Neither the size nor the cost of onboarding is universally bounded by a
small constant. A weak device instead needs an available compact warrant, a
short alternative proof, or an explicitly different trust policy.

Making every independent contribution await an economical universal cold proof
would let the hardest receiving case constrain all mathematical exchange. The
better objective is affordable sound collaboration for common supported uses,
with an honest stronger service for clients that need it. Strict soundness,
replaceable peers, exact semantics and bounded resource exposure remain core.
Universal instant access, universal semantic coverage and compulsory per-result
compression do not.

## What the measurements actually establish

The completed U proof has these recorded costs:

| Boundary | Observed quantity | Interpretation |
|---|---:|---|
| U certificate, prefix plus remainder | 36,413.71875 CPU seconds | About 10.1 CPU-hours; includes the two enclosing operations |
| Same operations, summed active wall | 5,342.7958624 seconds | About 89 minutes, not ten elapsed hours |
| Final receipt | 223,610 bytes | Compact relative to a long ancestry, not necessarily smaller than a short direct mathematical proof |
| Later complete U-to-V operation | 84.5625 CPU seconds | Includes startup, binding, authoring, checking and cleanup |
| Its conditional native V check | 0.015625 CPU seconds | A nested measurement; assumes the independently verified U frontier |
| Its two aggregate verifications | 0.046875 CPU seconds each | Also nested; not the cost of directly checking U without a certificate |

These are actual local observations with their audited scope, not universal
cost constants. Historical development, earlier failed work, maintenance and
future service are not all included. In particular, dividing U production by
V's conditional check is **not** a valid measured speedup/slowdown ratio for
two ways of establishing the same theorem from the same initial knowledge.

The proof-stage breakdown nevertheless changes the engineering decision:
segment proving, not just process launch or final receipt serialization,
dominates U's production. The remainder alone spent 23,920.328125 worker CPU
seconds in 34 segment proofs and 10,340.640625 in lift/join/resolve. Removing
all that latter work for free would still leave expensive segment proving.
The final finish call was only 1.0625 CPU seconds. Optimizing a wrapper or
omitting final packaging cannot explain an orders-of-magnitude cure.

Across the full graph, segment workers consumed 25,216.953125 CPU seconds;
lift/join/resolve consumed 10,800.390625. Removing the latter entirely while
holding everything else fixed saves at most 29.66% of known enclosing CPU, an
ideal 1.422x speedup. This is a boundary on that optimization, not on all possible
proof systems. The already-tested restricted-support checker saved 14.893617%
of padded rows (30 versus 36 segments), below its prior 25% investment screen.
It remains a failed screen. A new judgment-witness proposal must remove
materially different work, not repeat that experiment under another name.

The unsuccessful installed snapshot01 was a different, small bootstrap-size
failure: no new cryptographic work ran. Fixing it is valid maintenance but is
not a solution to certification economics. Likewise the proposed removal of
unused Lean file hashing improves startup, not the dominant cryptographic bill.

Evidence: [U production outcome](../v5-2026-10-20/TYPED-PRODUCTION-REMAINDER-OUTCOME.md),
[U-to-V outcome](../v5-2026-10-20/TYPED-RENEWAL-ACTUAL02-OUTCOME.md),
[snapshot failure](../v5-2026-10-20/INSTALLED-PRODUCER-V-SNAPSHOT01-OUTCOME.md).

## The obligation belongs to acceptance, not necessarily to the author

There are three different activities:

1. Discovering a mathematical argument, potentially through expensive search.
2. Checking a supplied formal argument under an exact foundation/environment.
3. Producing a cryptographic argument that this checking was performed correctly.

The third is optional in ordinary mathematical proof exchange. Any participant
with the necessary evidence can perform it: the original contributor, a reader,
a custodian, or an independent proving service. The author need not own special
hardware, identify itself politically, or fund every prospective reader.

But the consumer still needs a warrant for its premises. Outsourcing a
certificate changes who pays and when; it does not make production free.
Moving that work to a server and reporting only client latency would be an
accounting mistake. Services can be replaceable and untrusted mathematically;
their outputs still have to be verified locally.

Our target should be a derivability judgment under policy P, with exact
declaration and environment commitments. It should not be the producer's
historical discovery process. Current guests already check formal witnesses;
they do not prove all LLM search or Lean tactic execution. That distinction
cannot be sold as an unimplemented optimization. The remaining question is
whether the witness/checking representation proves more, or performs much more
work, than a particular consumer needs.

## A small formal model for alternative assurance routes

Fix a sound adopted formal system P, including the supported declaration rules,
axioms, semantic identities and checker/certificate assumptions. Let K be the
consumer's independently established local mathematical environment. Let t
be an exact desired declaration, not a natural-language interpretation.

An acceptance plan is a finite acyclic evidence graph whose leaves are:

- declarations already warranted in K under still-supported assumptions;
- independently verified portable certificates for exact declarations/modules;
- allowed foundation axioms, explicitly named by P.

An internal node is either a native checked derivation using its warranted
parents, or an admitted certificate-verification rule. A specialized witness
checker is permissible only through a justified soundness theorem/refinement,
not because a service advertises it as fast. Definitions, universes, recursive
groups, type conversion and demanded computation remain part of the relation.

**Conditional soundness.** If every leaf is warranted, every inference preserves
derivability in P, and all semantic bindings and dependency checks are exact,
then the terminal t is derivable in P, except for the stated cryptographic
soundness error where cryptography is used. Proof: induction in a topological
order of the finite evidence graph. Hashes supply binding, not the base case
of that induction. Cryptographic composition needs its actual recursive
construction assumptions; this argument is not a proof of a particular SNARK.

Different valid plans may establish the same t. A shorter independent proof
can bypass the contributor's original lemma chain. The necessary graph is
therefore the chosen *justification graph*, not a sacred historical provenance
graph. Distinct proof encodings are not necessarily distinct mathematical
knowledge. When changing dependencies changes exported definitions/types or
the module commitment, use a new exact object or a checked transport result;
do not falsely label merely equivalent content as the same identifier.

Select among supported plans subject to the consumer's trust, CPU, byte,
latency and memory constraints. A heuristic selector is acceptable; its output
is untrusted and subsequently checked. We do not need, and cannot assume, an
algorithm that finds the shortest proof or cheapest plan for arbitrary math.
Shared DAG nodes must be charged once per actual execution, and alternative
plans may overlap; a naive per-theorem popularity score is not an optimizer.

## Preserve the cold no-ancestry requirement explicitly

For a selected plan, an accepted frontier cuts off old theorem proofs only
when **every dependency path being omitted** reaches a warranted boundary.
Let D be the distinct new checked proof DAG above that cut, S the demanded
semantic data, and F the selected certificate/interface data. The intended
receiver cost is a function of D, S and F, not of the complete hidden ancestry.
There is still work proportional to actual selected input and computation.

Caching and demand coordination alone do not create such a frontier. Consider
a previously unseen long chain held by an untrusted peer. The peer supplies
only its final theorem's type and claims all prior lemmas were checked. A hash
of the chain, a signature or many matching peer reports does not discharge
the missing mathematical premises under the present trust model.

Consequently a cold, ancestry-free import must obtain a supported certificate,
an independently checkable short alternative proof relative to its accepted
basis, or another explicitly adopted assurance mechanism. If none is available
within budget, the correct result is deferred/unavailable assurance. Ordinary
closure checking is an explicit different fallback, not a silent violation of
the no-replay contract. There is no promise that every advertised theorem is
immediately cheap for every new consumer.

This is an architectural boundary and counterexample, **not** a claimed general
complexity lower bound ruling out better proof systems. Neither undecidability
nor the cost of our current implementation proves that today's cryptographic
overhead is inevitable.

## The most promising non-cryptographic improvement

Mathematics often supplies an inexpensive certificate of the *answer*, without
a certificate of the entire computation that found it. Favor these whenever
the supported mathematics allows it.

For example, for integers a and b not both zero, an untrusted agent can supply
g > 0 and integers u, v, x, y satisfying

    a = g*u,   b = g*v,   g = a*x + b*y.

The first two equations make g a common divisor. Every common divisor divides
the last combination, hence divides g. Together with positivity this identifies
the positive greatest common divisor. A receiver can check these equations and
apply a previously warranted generic theorem. It need not replay the agent's
Euclidean algorithm, proof search, or a zkVM trace of that search. Integer bit
lengths and arithmetic checking are real costs; this is not constant-time GCD.

The general pattern is a small witness w and a formally justified checker c:

    c(x, w) = true  implies  R(x).

Examples include arithmetic witnesses, normalization certificates, solver proof
traces, verified rewriting and theorem transport. The generic soundness theorem
is reused; each instance needs only its own bounded evidence. It can be proved
and checked natively against a locally warranted basis, or certified once for
cold users. A new native oracle or untrusted computed boolean is not a proof.

This approach can be dramatically cheaper for suitable classes because it
changes the amount of work to be warranted. It has no universal compression
guarantee; some witnesses are large and some checking computations expensive.
Existing method-sharing experiments are relevant evidence, not a reason to
claim these particular examples are already implemented in our supported Lean
subset. The next workload should preserve the exact mathematical endpoint and
compare against an equally optimized ordinary method, not an inflated trace.

[SMTCoq](https://smtcoq.github.io/) is a concrete precedent for verified checking
of untrusted SAT/SMT proof witnesses. It is not a drop-in Lean implementation.
[Proof-carrying code](https://www.cs.cmu.edu/~fox/pcc.html) illustrates the broader
principle of inexpensive checking of supplied evidence without trusting the
producer's search or compiler. Our proposed use is an architectural inference,
not a performance result transferred from those projects.

## Durable local knowledge, without durable execution authority

Current live-owner caches are useful but limited. Closing an operation destroys
its admission handles; same-live native/checking caches do not amount to a
persistent accepted mathematical library. Persisted trust-domain adoption is
not itself a cache of accepted theorems.

A protected local accepted-environment cache is a promising substantive change:

- Establish entries only through genuine native/certificate acceptance.
- Bind them to exact mathematical objects, foundation, checker/support version,
  axiom policy, semantic dependencies and the actual assurance lineage. The same
  semantic fact can have different native or cryptographic warrants; withdrawal
  follows the route actually used unless a valid alternative is established.
- Protect local cache integrity and provenance through an explicit local trust
  boundary; arbitrary peer snapshots or ordinary JSON success flags cannot
  populate it. Safe serialization and crash-atomic publication are required.
- On reuse create a **new** operation with **new** resource and lifetime grants.
  Never deserialize old live handles, spent allowances or network authority.
- If supporting assurance is withdrawn or incompatible, refuse affected entries
  until re-established. Mathematical truth does not expire with an operation;
  the software's warrant for relying on a particular checker may change.

This can avoid repeatedly establishing known mathematics across local sessions.
It does not confer portable trust on another computer, solve cold onboarding,
or eliminate ordinary integrity checks. A bare content hash proves that a cache
is unchanged, not that its accepted flag was legitimately created. Under the
project's existing trusted-owner/stable-local-filesystem assumption this is
tractable, but must be explicit and independently reviewed.
The existing exclusion of hostile whole-directory rollback must remain explicit
unless a real anti-rollback mechanism is added. A newer local withdrawal must not
be overridden by a cached positive inside the supported storage model.

An alternative is a bounded long-lived checked environment in a local service.
That may amortize startup, but must preserve per-request budgets, isolation,
revocation and recovery. It should be compared with a persistent cache, not
added alongside it by default. Current synchronous pin-phase reuse must not be
silently stretched across awaits, processes or untrusted callbacks.

## Revised end-to-end protocol, not just a replacement prover

| Stage | Recommended behavior | Authority boundary |
|---|---|---|
| Contribution | Use the existing locally admitted contribution path to publish exact declarations, proofs/deltas and requirements; cryptographic sealing is not mandatory | Other nodes do not inherit the contributor's local checked status |
| Discovery | Search formal structure and applicability; expose available evidence variants and estimated acquisition/checking costs | Index rankings and cost quotes are untrusted hints |
| Assurance choice | Prefer already warranted local bases, short checked witnesses, and available certified cuts subject to the requested cold/warm contract | Every chosen plan still closes all premises |
| Acquisition | Fetch only the selected interfaces, evidence and demanded semantics; deduplicate exact shared objects | Hash membership alone is not theorem validity |
| Local use | Check the new derivation and reuse accepted mathematics under fresh operation grants | No remote executable proof tactic or unsafe compiled object becomes trusted data |
| Shared certification | Any willing, explicitly budgeted service certifies valuable exact cuts/methods; cache its portable result | No author exclusivity, mandatory service, global task list or automatic charge |
| Custody and return | Retain enough evidence/semantics for promised delivery classes; advertise new results and available warrants separately | Storage, discoverability and validity are distinct claims |

Certificate demand is an operational request, not human intention in the
mathematical acceptance relation. Nobody must submit a global research goal.
Any participant may investigate and contribute spontaneously. A certificate
service can be replaced; multiple compatible certified roots can coexist.
There is no need for a blockchain's total ordering or mining rule.

A completely unrestricted conditional-only publication API is not assumed to
exist and is not required for this change: current locally admitted mixed
contributions already avoid a new certificate per contribution. Unverified
candidate hosting would require separate spam/resource/status rules. Do not
build that new lane simply to make the architecture diagram more general.

Avoid certification-gated ranking that permanently buries valuable new work.
A valid but not-yet-cheap-to-import result can still be discovered as a
candidate. Conversely do not advertise a thin-client delivery guarantee merely
because the underlying ordinary proof is available somewhere.

Exact witness deduplication and certificate caching should use the established
object/statement/policy identities, with separately content-addressed witness
variants. A new proof backend cannot silently inherit another backend's trust
policy. Provider identity may help rate limits and service commitments; it does
not decide mathematical truth.

## When should the network invest in cryptographic compression?

For one exact cut and finite retention/policy horizon, let F be the additional
production/publication cost, H its incremental maintenance cost, and d_i the
cost of the best *supported, equally optimized* non-new-certificate plan for
consumer i minus the cost of using the new certificate. Include provider work,
failed attempts and relevant acquisition/validation overhead consistently.

Certification has a positive aggregate priced-resource margin only if

    sum_i d_i > F + H.

Use explicit nonnegative weights if CPU, bytes and storage-time are combined.
Peak memory and latency are separate constraints. Local warm uses often have
little or no d_i. A certificate that costs more to verify than the available
ordinary proof can have d_i <= 0. Popularity alone cannot repair that.

For illustration only, ignoring H, if F were the observed 36,413.71875 CPU
seconds and a genuinely otherwise-uncached use saved 0.01, 0.1 or 1 CPU second,
break-even would exceed about 3.64 million, 364 thousand or 36.4 thousand such
uses respectively. These are arithmetic scenarios, **not** measurements of
U's savings or a forecast of network demand. Large ancestral checking or
bandwidth costs may change the result considerably.

Demand-driven production permits batching and sharing of F. It does not make
observed lookup counts truthful evidence of future avoided work, nor does it
guarantee a shared rent-or-buy competitive ratio for changing DAGs. Failed or
duplicate certificate jobs, privacy, sybil demand and service monopolization
remain operational issues. A local budget holder must approve costly work;
an unauthenticated query must not trigger hours of proving.

Also account for **verification debt**. If selected certificate work arrives
at long-run rate lambda with mean required work E[W], capacity slack
lambda*E[W] < mu is a standard stable-design target under suitable stochastic
queue assumptions. It is not a universal necessary condition (a deterministic
critical-load schedule can be bounded). An average rate condition alone
supplies no bounded latency under arbitrary bursts/failures. The
existing deterministic arrival/service model supplies stronger conditional
bounds where its hypotheses hold. Without adequate capacity, the protocol
must postpone cold availability, change the witness/route, apply backpressure,
or obtain funded capacity. It cannot promise perpetual cheap cold access just
by naming a proof-service role.

## Cryptographic alternatives: serious options, not magic switches

| Option | Potential benefit | What still has to be established |
|---|---|---|
| Batch existing checkable deltas above selected frontiers | Amortizes fixed setup and avoids certifying every small theorem | Total new checking/proving remains; tail, latency and availability bounds must fit |
| Composite versus fully compressed receipts | Trades production/recursive compression against verifier work and bytes | Segment/assumption growth can reintroduce ancestry; cannot drop required resolution |
| Dedicated mathematical judgment representation/circuit | Avoids general VM instruction, parsing and memory overhead where unnecessary | Exact Lean-subset correspondence, binders, universes, conversion, induction/recursors, hashes and memory soundness |
| Folding/IVC | Incremental accumulation may reduce repeated recursive-verifier overhead | Encoding cost, final compression, branch/DAG composition, memory and construction-specific assumptions |
| Sum-check/GKR-style proof systems | Efficient prover for suitable structured circuits | Circuit depth/regularity, input commitments, interaction and public reusable-proof security |
| Interactive verification or TEE/quorum/optimistic routes | May lower selected costs under different assumptions | Not an unchanged substitute for independent portable mathematical assurance |

The [RISC Zero proof-system overview](https://dev.risczero.com/proof-system/)
distinguishes segment/composite receipts, succinct recursive receipts, and an
additional Groth16 layer. Our observed finish stage is not evidence that a
large avoidable Groth16 step dominates this workload. Nor should eliminating
zero-knowledge privacy be assumed to eliminate proof-generation cost: public
mathematics needs soundness and succinctness, and their costs remain.

[Nova](https://github.com/microsoft/Nova) supplies an actual folding-based IVC
implementation; its update and verification costs need not grow with the
number of earlier steps. This does not prove a fast encoding of our kernel or
arbitrary branching module certificates. Its commitment/compression choices
have different setup and verification assumptions. A literature comparison
must choose the exact construction, not the family name alone.

[General-circuit GKR work](https://eprint.iacr.org/2020/1247) demonstrates linear
prover work in arithmetic-circuit size with depth/structure qualifications for
succinctness and verification. That is reason to investigate, not a benchmark
for Lean dependency checking. An interactive transcript selected by its own
prover is not automatically a reusable noninteractive proof for every reader.

The highest-payoff backend investigation is therefore first to define the
smallest exact mathematical relation and estimate its witness/checking work,
then compare concrete encodings. Do not port the whole application into another
zkVM and hope its name solves the architecture. Do not restart a completed
certificate merely to collect another performance number.

## Security, discovery and availability consequences

### A deeper bottleneck: ordinary checking must not inherit every zk restriction

Root inspected `software/v5/delta/native.rs`: the current native delta executable
includes the same `modules/receipt/src/relation.rs` used for certification.
Native here means ordinary execution of the restricted relation, **not** an
independent broad Lean-kernel library mode. The relation fixes its foundation,
canonical schema and policy and disables the native checker's nat/string
extensions. The supported semantics are consequently narrower than general
Lean/Mathlib even when no cryptographic proof is requested.

This is a more central product constraint than another producer wrapper fix.
Avoiding certificates alone will not make normal Lean mathematics interoperable.
Neither will caching the same narrow judgments. The architecture should separate
the exchange of exact mathematical modules from the evidence profiles able to
warrant them: a broad, data-only locally checked profile can coexist with a
narrower succinct-certified profile, with no automatic cross-profile authority.
The current authoring frontend is not that new checker. Its imported theorem
and opaque interfaces are intentionally assumptions for producing a conditional
witness; successful elaboration cannot discharge those assumptions.

This is not permission to accept arbitrary downloaded `.olean` files, execute
peer tactics in a trusted process, or turn an author's success report into a
proof. A wider local lane needs a precise safe declaration decoder, actual
kernel checking from grounded imports, exact axiom/universe/definition/group
handling and a warranted environment-restoration boundary. It is new central
engineering, not a configuration switch. Reuse Lean/checker infrastructure where
sound and compatible; do not rebuild the entirety of dependent type theory or
claim full Mathlib support before its actual import boundary is established.

The next design decision must therefore settle the checked-library import
boundary **before** persisting a schema that hardwires every local fact to the
current cryptographic journal. Existing certified receipts keep their exact
meaning; a new local profile cannot relabel them or manufacture compatibility.

The two goals interact, but neither cryptography nor native checking solves
semantic search. Keep formal indexes replaceable and bounded, with coverage
relative to their snapshots. Cost-aware candidate selection can reduce wasted
acquisition, but cannot guarantee recall or arbitrary semantic equivalence.
Discovery/provider verification costs must remain in the growth comparison.

A certificate cannot restore lost definition bodies or export interfaces.
Custody should prioritize the objects required by actual retained delivery
contracts: interfaces, computational semantics, portable warrants, and ordinary
witnesses needed for future checking or migration. Deleting all original proof
evidence after certification can make checker upgrades or assurance withdrawal
irrecoverable without rediscovery. Keeping everything forever is not free;
choose an explicit retention/recovery policy rather than claiming both benefits.

A succinct proof faithfully proving a buggy checker is still unsafe mathematics.
[Lean's validation guidance](https://lean-lang.org/doc/reference/latest/ValidatingProofs/)
distinguishes hostile input from honest use, and warns about unsafe compiled
inputs and arbitrary actions in meta-code. Native-first must not mean executing
peer tactics or trusting downloaded `.olean` files without appropriate
validation/isolation. This system's supported formal subset and exact checker
correspondence remain central security obligations.

[Lean4Lean](https://arxiv.org/abs/2403.14064) provides an external checker and
formal verification of parts of the kernel. It is relevant assurance work,
not proof that all of our checker, importer or certificate stack is verified.
Changing the proof backend never removes that semantic obligation.

## Recommended next decisions, ranked by marginal payoff

1. **Do not commission V certification on the current route merely because U
   now exists.** Preserve the capability evidence and unexecuted producer02
   repair. Resume a heavy proof only for a specifically justified protocol
   obligation or measured/modelled benefit with a finite full budget.
2. **Define one useful checked-library mode and its exact import boundary.**
   Separate ordinary mathematical coverage from the restricted certified
   profile. Reuse the existing exchange/discovery/custody and mixed-evidence
   primitives where compatible; do not duplicate them. Settle sound local
   initial checking, safe restoration, policy compatibility and explicit
   no-history versus ordinary delivery modes before the persistence schema.
   Separate persistent warranted mathematics from short-lived operational
   authority. Then select the smallest consequential implementation.
3. **Select a mathematical witness/method that avoids expensive history.**
   Favor a short independently checked derivation or reflected certificate for
   the same endpoint. Compare against optimized ordinary sharing and existing
   local caches. Do not promise a universal shortest-proof finder.
4. **Audit and shrink the actual relation before choosing a new prover.**
   Identify unavoidable type/conversion/dependency work versus VM/representation
   overhead. A theoretical operation/memory model should screen dedicated
   checking, folding and structured-circuit options before any long test.
5. **Integrate cold delivery and shared service only with explicit limits.**
   A thin client must know whether a candidate has an available independent
   warrant. Certificate availability, proof-service capacity and evidence
   retention are part of the deliverable, not future free infrastructure.

This retains the decentralized Lean-based commons and its strict mathematical
acceptance goal. It changes which work is routine, which is amortized locally,
and which is selectively purchased as shared infrastructure. The most credible
route is a hybrid evidence system, not mandatory cryptographic certification
of every result and not unverified social consensus.

### What would count as useful growth under this revised design?

For a fixed baseline, successful mathematical endpoints and service horizon,
sharing is useful if the avoided independent discovery/construction cost and
newly enabled capability exceed acquisition, checking, indexing, retention,
failures and optional certification costs. Use the same initial library and
local optimizations in both routes. A new record is not automatically a new
capability, and the baseline must not be forced to rediscover facts it already
possesses. This argument does not require crypto to beat ordinary sharing.

For one stable local policy epoch with no eviction, an incremental library can
in principle charge each distinct newly needed declaration's validation once,
plus actual integrity, lookup, semantic computation and transaction work on
later uses. Its relevant size is the demanded dependency working set, not the
whole network corpus. This conditional bound follows from a memoized acyclic
validation traversal; it is not a claim that the current software implements
it, that a demand closure is always small, or that checking a declaration is
constant-time. Updates, assurance withdrawal and cache eviction add real costs.

The immediate falsifiable milestone should be one coherent public workflow:
learn a nontrivial relevant library without a new SNARK; close/reopen a valid
local environment without rechecking its prior proof terms or reviving old
resource grants; discover a previously unknown applicable result; check a
substantive extension; and make it usable at another local node. Ordinary and
strict-certificate delivery outcomes must be visibly different. This should
exercise the identified semantic gap rather than repeat polymorphic congruence
fixtures. The exact workload and bounded test selection remain future work.

Before broad distribution, this mode still needs hostile-input isolation,
recovery, actual supported Lean coverage, an independently operated exchange
pilot when available, and license/maintenance decisions. Passing the milestone
would advance the product substantially, not complete those separate obligations.

## Audit inputs and independent challenges

- [Demand-oriented protocol](DEMAND-PROTOCOL.md).
- [Certificate economics and backend alternatives](CERTIFICATE-ECONOMICS.md).
- [Trust boundaries and counterexamples](TRUST-AND-LOWER-BOUNDARIES.md).
- [Independent synthesis trust review](CROSS-AUDIT.md), against its recorded
  earlier digest; later compromise and interoperability additions are not
  retroactively covered by that review.
- [Fresh independent practicality challenge](PRACTICALITY-CHALLENGE.md), addressing
  the user's explicit permission for compromises and the useful-library priority.
- [Source-grounded broad Lean acceptance seam](LEAN-NATIVE-SEAM.md), including
  selected-source identity checks and the existing authoring/admission distinction.
- [Existing selective-certification policy](../v5-2026-10-17/SELECTIVE-CERTIFICATION-POLICY.md).
- [Existing operating-region theorem](../v5-2026-10-20/GROWTH-OPERATING-REGION.md).
- [Existing distinction between sharing and certification benefit](../v5-2026-10-20/TYPED-RENEWAL-NEXT-PRIORITY.md).

External references above were checked against primary project/paper pages on
2026-10-22. They support mechanisms and assurance distinctions, not a claim of
measured end-to-end improvement in our software. No license, remote deployment,
purchase, additional experiment, or replacement executable acceptance policy is
adopted. The selected next investigation is the ordinary checked-library
acceptance contract and one representative compatibility trace, not more proof
production. It must record the proposed cold-service compromise explicitly
before any implementation changes the public contract.
