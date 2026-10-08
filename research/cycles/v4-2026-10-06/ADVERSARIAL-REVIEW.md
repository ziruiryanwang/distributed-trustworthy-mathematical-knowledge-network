# Adversarial review: growth that the architecture can actually support

2026-10-06 UTC. Owner: `/root/growth_challenge_v4`. Independent theory/source
review; no runtime, product edit, qualification claim or frozen-artifact change.
The canonical workspace guard passed. This is a live checkpoint, not yet the
cross-review of the other two October 6 proposals.

## Initial verdict and the central correction

The October 2 philosophy correctly distinguishes deductive closure from
resource-bounded accessible capability. Its cost accounting is also sound. But
the resulting engineering direction became too narrow: another experimentally
completed endpoint is neither necessary nor sufficient to justify an entire
growth mechanism. The central next object should be an executable **resource
policy with a conditional capability theorem**, not a population-level claim
inferred from one expensive proof campaign.

Theory can establish guarantees relative to explicitly specified algorithms,
costs and environments without proving that an LLM is optimal or that a sampled
workload represents all mathematics. These are substantive guarantees when
their assumptions are observable, enforceable or replaceable by bounded local
decisions. Calling an unobserved heuristic estimate a bound does not qualify.

This review distinguishes four claims:

1. **Logical acceptance:** exact conditional derivability under the selected
   foundation/checker/certificate profile. Popularity never enters this claim.
2. **Mechanism advantage:** an implemented reuse route has a derived cost or
   capability advantage over a named baseline algorithm under stated inputs.
3. **Policy advantage:** a deployed selection/search policy finds advantageous
   routes often enough after its overhead, mistakes and investments are paid.
4. **Ecological growth:** independently chosen future investigations collectively
   produce more useful mathematics over time. This additionally depends on
   effort, incentives, diversity, availability and changing demand.

The first two can often be established largely by theory plus focused conformance
tests. The last two are not established merely by an arithmetic break-even
identity. Conversely the absence of an empirical ecological-growth estimate
does not invalidate a correctly stated mechanism theorem.

## Strong counterexamples the design must survive

### Complementarity defeats single-lemma greedy scores

Let the local downstream task be to derive `R` given a separately held `P`.
Object A exposes `P -> Q`; object B exposes `Q -> R`. In a declared reasoner
whose only cheap route uses these applications, neither A nor B alone makes
the task cheap; their pair does. With utility defined as budgeted completion,
`U({A}) = U({B}) = U(empty) = 0`, while `U({A,B}) = 1`.
The marginal contribution of B increases after adding A, violating diminishing
returns. A greedy algorithm whose approximation theorem requires submodularity
cannot inherit that theorem for arbitrary mathematical libraries.

This example does not claim that R has no other proof; it specifies a bounded
reasoner/cost regime. Existence of another route must be considered by the
deployment policy, not excluded by definition when claiming a general result.

**Decision consequence:** permit bounded, exact bundles/contexts as resource
candidates and retain an explicit exploration allocation. Do not require each
lemma to have individually positive realized utility before publishing it or
before admitting a complementary bundle. No need for a global hypergraph
service: exact dependency and context records already identify small bundles.

### Compression is not the same as useful generalization

Object A is a very short proof of an already cheap special case; object B is a
larger polymorphic law that makes a family of later endpoints cheap. Ranking
solely by certificate size favors A even when B yields greater benefit.
Conversely an abstraction with smaller source syntax can impose expensive
definitional normalization on every consumer and be worse than direct code.

**Decision consequence:** keep representation bytes, checking cost, demanded
evaluation cost and applicability separate. Report benefit for formal interface
families or observed exact endpoints, not source-line reduction. A polymorphic
type is a checkable generality fact; practical coverage of future work is not.

### Usage is not a counterfactual saving

Two policies may both cite the same lemma, but one could have obtained an easier
direct proof. A cheap wrapper can receive arbitrarily many automatic citations.
An attacker can emit many distinct identities and plausible usage claims. An
honest index can produce the same feedback bias by displaying already-popular
objects more often, hiding rare but useful alternatives.

**Decision consequence:** external usage is an untrusted ranking hint, never
proof of acceptance, subsidy eligibility or a lower bound on resource benefit.
Only the local node's own costs and successes are authoritative for its own
resource accounting. Peer hints must consume bounded attention and cannot
automatically trigger unbounded verification, replication or certification.
Exact hashes remove byte duplicates, not semantic duplicates or coordinated
wrappers. Rate limits require a cost/capacity boundary, not merely new public
keys; no global political identity registry is needed for the local rule.

### Survivorship can reverse a claimed improvement

Suppose 90 reuse attempts fail after cost 1 and ten succeed after cost 2. Direct
work always succeeds after cost 3. Reporting mean successful reuse cost 2 versus
3 hides the much lower completion rate and the 90 failed attempts. A producer
reporting only its popular successful outputs likewise omits failed searches
and discarded proofs.

**Decision consequence:** accounting includes every selected attempt, failure,
query, rejected candidate and retained investment. A report names whether its
denominator is requests, successful endpoints, distinct statements or consumers.
Partial observations are allowed, but missing costs are unknown rather than 0.

### Endogenous effort can erase a paper growth claim

If every extra available theorem provokes a proportional increase in tasks,
CPU consumption can rise despite cheaper individual tasks. If all agents use
the same ranking model, duplicated investigations can rise while formal
publication count grows. A positive reproduction matrix assumed per theorem
may hide resources that scale with the number of theorems.

**Decision consequence:** compare capability at a stated aggregate resource
opportunity and permit diversity in local discovery/retention policies. Do not
make a common ranker or a universal investigation agenda a consensus rule.
The network enables independent work; it does not control enough variables to
promise indefinite exponential realized output on fixed hardware.

## A useful universal bound: protected fallback, not free optionality

Let a direct algorithm A finish a selected endpoint after T units of its own
work. Let a local interleaving policy reserve at least a fraction `1-alpha` of
service for A while spending at most fraction alpha on optional network/reuse
work, where `0 <= alpha < 1`. Assume:

- A's state/input/randomness can be preserved independently of optional work;
- service is measured in an additive unit the executor actually meters;
- neither branch monopolizes an unmetered shared resource;
- the scheduling invariant holds up to additive quantum/dispatch overhead h;
- both branches use the same endpoint acceptance/assurance predicate.

Then A receives T units by total charged work at most

`T / (1-alpha) + h`.

Proof: the service invariant gives A at least `(1-alpha)(W-h)` work after total
work W. Substitute the claimed bound. Whichever branch completes first can be
returned only after the common endpoint check. This is a baseline protection
theorem, independent of whether candidate quality is good, bad or malicious.

It is **not** equal-budget nonregression. At fixed total budget B, the guaranteed
baseline opportunity is only approximately `(1-alpha)(B-h)`, not B. Running a
network prelude of cost e followed by A similarly gives only an additive `T+e`
bound; it cannot guarantee baseline success at the original B. A claim that
optional search is free because the agent can ignore results is false whenever
the search itself is mandatory and paid.

For coarse nonpreemptible jobs, h must include bounded overrun and accounting
overhead. CPU protection is not wall-time protection under network waiting or
memory contention. A child process budget does not meter an external human/LLM
reasoner's deliberation. Therefore an initial implementation can honestly
offer **search-budget isolation and an explicit fallback recommendation**, not
claim this full theorem for an uncontrolled agent. Expose the limits instead of
inventing a scheduler for research strategy inside mathematical acceptance.

**Consequential design requirement:** a local policy API returns the remaining
baseline budget after optional work and preserves stop/skip/direct alternatives.
It must never silently spend an entire research budget on exhaustive discovery.
This is more actionable than globally estimating mathematical importance.

## Concrete-route theoretical comparisons are enough for some claims

Let a specified baseline checker recheck a shared derivation of cost P for each
of N fresh consumers. Let an actually sound certificate route pay J once, and
each consumer pay v for verification plus u for its selected semantic interface
material. With common downstream work canceled legitimately, baseline work is
`N*P`, reuse work is `J + N*(v+u)`. Thus the certificate route improves this
part of the concrete workflow iff `P > v+u` and
`N > J/(P-v-u)`.

This is not an algorithmic lower bound on every baseline: a warm native cache,
shorter proof or different assurance model may be cheaper. It is nevertheless
a valid architecture theorem about the specified cold-consumer workload. The
implementation question is whether the shipped paths implement those costs
and assumptions, not whether a giant population experiment has been run.
Current observed expensive J makes the threshold consequential; a succinct
reader alone does not make every small new theorem worth certifying eagerly.

**Decision consequence:** separate producing an accepted local result from
deciding to pay a certificate for wide cold reuse. The latter may be optional,
batched, delegated or demand-triggered, but a not-yet-certified object cannot
be mislabeled as meeting the selected cold-reader acceptance profile. Reusing
an existing genuine certificate is different from paying its sunk cost again.

A ski-rental-style threshold can be a useful research candidate when repeated
uses have observable comparable rental costs and a known fixed purchase cost.
It cannot be called competitive if rental savings are invented, maintenance is
omitted, purchase may fail, or demand shifts between incompatible profiles.
Do not import a familiar online-algorithm theorem without checking its model.

## Sufficient conditions for an honest first deployable growth layer

The following is a mechanism envelope, not a requirement to prove universal
mathematical value or run a prescribed task list:

- A locally chosen investigation supplies an exact formal interface/query and
  finite discretionary resource allowance; its motivation stays outside core.
- Bounded discovery returns candidates and explicit coverage status. Missing
  results never become a claim of global nonexistence.
- Validity is decided using the exact existing certificate/foundation boundary,
  independently of benefit score. Semantic material required for use is paid.
- The local policy can skip discovery, reject costly candidates, choose direct
  work, retain/reuse an admitted result, or consider an exact small bundle.
- Resource estimates are labeled guaranteed, measured or heuristic. Optional
  work obeys enforceable budgets even when estimates are wrong.
- Cost/benefit evidence is local, typed by profile/resource/horizon, and charges
  failed attempts. Popularity can reorder bounded candidate consideration but
  cannot expand spending authority by itself.
- Exploration and retention are adjustable local policies, with no assertion
  that any fixed split is globally optimal. A zero-exploration configuration is
  permitted but loses any claimed discovery-of-rare-complements rationale.
- Public documentation supplies at least one concrete algorithmic advantage
  theorem and its operating thresholds, alongside actual conformance evidence.

This gives agents practical control over reliable accumulated capability. It
does not yet prove that independent contributors will subsidize all valuable
public goods. That coordination/economic question is real but should not be
disguised as a reason to add a blockchain or a global usefulness consensus.

## Concrete-source challenge: bounded unsealed deltas

After the initial checkpoint, root and scale proposed avoiding mandatory costly
child certification for every cold use. A receiver would execute one bounded
inert proof packet under the adopted guest relation, independently authenticate
all selected certified parent receipts, and keep the outcome local. This is a
consequential direction, not an existing qualified acceptance mode.

I inspected the current foundation-restore project's `host.rs`, guest
`main.rs`, `relation.rs` and Cargo configuration. The following findings are
source-grounded, not a runtime claim:

- `host.rs::execute` computes an image ID from its supplied ELF, verifies the
  exact selected parent receipts, executes the framed input with cycle/segment
  limits, requires successful halt and exact expected journal, and labels its
  stdout `EXECUTED_ONLY_NOT_A_CERTIFICATE`.
- Guest `main` calls the actual mathematical relation and then `env::verify`
  once for each validated header parent journal before committing its output.
  The host supplies the same exact genuine receipt set. This correspondence
  supports a source argument for local conditional acceptance without treating
  an unresolved conditional native proof as an unconditional theorem.
- The generic host **does not itself adopt/pin an approved image**: it computes
  the ID of whatever ELF path it receives. A public receiver must bind the
  fixed approved ELF/image/profile; otherwise a sender can choose a program
  that emits the expected journal without checking mathematics. Pinning an
  arbitrary image's self-consistent ID is not approval of that image.
- Local execution and a final cryptographic child certificate have different
  trusted computing bases. Both can establish the same formal proposition
  under their respective explicit assumptions. Do not call their assurance
  assumptions literally identical or publish a local success flag as a proof.
- The packet is bounded at 4 MiB, but the selected receipts and semantic data,
  guest cycles, SDK/host memory and aggregate transfer also require limits.
  A packet byte cap alone is not a complexity bound on checking. Refusal at a
  cap means no accepted result; it is not an excuse for implicit recursive
  ancestor fetching.

### The essential growth obstacle: the unsealed child is not a usable parent

The current relation permits only one or two output theorem/definition members,
refuses extra theorem declarations, and forbids output self/cross-member
references. All selected external Prop interfaces require genuine certified
parents. Therefore:

`certified A -> locally checked unsealed B`

does **not** yet provide the implemented next step

`unsealed B -> locally checked C`.

A local acceptance record cannot fill that missing parent receipt. Possible
honest solutions are checked proof-term substitution/inlining into a new bounded
packet over the same certified cut, an independently specified bounded
multi-declaration delta relation, or paying for a genuine certificate of B.
Inlining itself must preserve binder/universe/name semantics and exact accepted
interfaces; a source-level concatenation is not a proof of correct substitution.
Repeated inlining grows work/bytes until a declared cap; eventual **resealing is
a funded barrier**, not a free operation. The producer can alternatively keep B
private or publish the bounded artifact only for readers that can use its exact
endpoint without using it as a premise in the existing contributor API.

This does not make the bounded-delta reader useless. It can avoid enormous
per-output certification for long-tail results and provide local trustworthy
access independent of certified proof ancestry. But calling a reader-only
implementation the solution to reciprocal multigeneration growth would be a
material overclaim. The release must expose the barrier in its main capability
table and agent API, not only a late limitations paragraph.

### Assurance-sensitive rent-or-buy decision

The classical rent-or-buy comparison requires interchangeable successful
endpoints. It can compare two ways for this receiver to obtain local accepted
knowledge if the receiver explicitly accepts both assurance profiles. It
cannot compare a local accepted result to a portable final certificate as if
the former already supplies the latter's reuse affordance. If a consumer needs
B as a certified parent, the local-only route does not rent that service at
all. Acquisition availability, sealing failure, profile change, byte transfer
and renewal are likewise not automatically in the classical theorem.

Thus the initial policy should report `local-consumption`, `certified-parent`
and `portable-certificate` demands distinctly, with abstention when a route
cannot satisfy the requested mode. A production decision can then use theory
without confusing a cheaper but different deliverable with a speedup.

## Review of the proposed reciprocal closure repair

Root subsequently proposed proof substitution as the smallest consequential
composition repair: source elaboration may see an unsealed interface as a
conditional premise, but the exported proof is transformed to replace that
premise with its complete proof over certified cut points before the actual
guest check. This directly addresses the preceding reader-only objection.

The justification is the admissibility of substitution/cut, not trust in the
transformer. For an exact shared environment E and genuine certified premises
Gamma, suppose `E,Gamma |- q_i : Prop` has proof `d_i` and
`E,Gamma,q_1,...,q_k |- p` has proof `d`. Substituting each closed `d_i` at
the corresponding instantiated constant in d produces a candidate derivation
in `E,Gamma`. In dependent type theory, this substitution must also preserve
universe instantiation and dependent types. The final pinned checker decides
whether the concrete transformed candidate really inhabits the requested p.
An erroneous transformer can cause refusal or resource exhaustion, but cannot
grant a false result if that final acceptance boundary remains sound.

The safe pipeline is therefore:

1. Preserve the exact requested output capsule and profile.
2. Elaborate/export with local fragment interfaces explicitly conditional.
3. Replace every local fragment premise by its closed instantiated proof;
   collect only actually required exact F/semantic definitions/certified cuts.
4. Emit one bounded, dependency-topological packet with no leftover unsealed
   axioms. Recompute actual parent selections, rank and expected output journal.
5. Require exact requested output-capsule equality, genuine cryptographic
   authentication of every selected cut parent, and successful final guest
   execution or final child certification.

This restores multigeneration closure **only while the flattened delta remains
within the enforced envelope**. Every published unsealed object carries its
complete current delta over certified cuts; later consumers do not recursively
chase other unsealed objects. A capped failure requires an explicit genuine
reseal or a different proof, not hidden ancestor expansion. Contributed
definitions remain limited by the current F-closed relation; substitution of
Prop proofs alone does not add chained abstract data definitions or inductives.

### Changed-boundary review requirements, not an experimental research campaign

- Simultaneous universe substitution respects parameter arity and order and
  recursively handles zero/succ/max/imax/param levels. Sequential replacements
  can capture another parameter's name and are not equivalent.
- A proof inserted below local term binders must be genuinely closed in term
  variables. Internal de Bruijn references under its own binders remain bound;
  blindly shifting an already closed proof can break it. Reject free locals,
  free bound variables and unsupported expression forms.
- Reusing a fragment at different universe instantiations requires distinct
  memoization keys. Caching only by theorem name or proof hash can conflate two
  different instantiated terms.
- Duplicate exact semantic definitions can share; same rendered names with
  different exact descriptors must refuse. Arbitrary name resolution must not
  replace a certified commitment.
- Available contexts are not necessarily used contexts. A child that does not
  use an offered local fragment must not acquire its full certified frontier
  accidentally. Trim exact parent-member selections after proof closure; a
  genuine receipt's complete journal still authenticates the selected subset.
- Recompute rank from actual selected certified cut parents, not from an
  unsealed object's displayed rank. No unsealed acceptance log is a receipt.
- Bound input, unique transformed nodes, instantiated fragments, recursion
  depth, intermediate bytes, output bytes and compute before/during expansion.
  Checking only the final serialized size permits an expansion resource attack.
- Tests must include two instantiations of one fragment, a fragment beneath a
  binder, tampered proof/type/definition, wrong universe arity, omitted cut
  receipt, unused offered context and bounded expansion refusal. Final real
  guest checking, not a transformer self-reported success, is the oracle.

With DAG memoization keyed by fragment and complete universe substitution,
construction work can be bounded by the visited child nodes plus the distinct
instantiated fragment nodes. That is a representation bound, not a polynomial
bound on dependent type checking; the actual execution cap remains necessary.
This repair is substantially more relevant to growth than another isolated
endpoint certificate: it lets subsequent independent work reuse a checked
long-tail result before that result has individually paid for a SNARK.

## Completed theory cross-review

Read both complete `GROWTH-MECHANISM.md` and `SCALE-OPERATING-ENVELOPE.md` after
their drafts became available. **No blocking logical flaw found in their scoped
conditional mechanisms.** This is not adoption of an implemented acceptance
mode, proof of global useful growth or a deployment pass.

The growth note's exact threshold proof is pathwise: for known nonnegative
premiums and fixed successful permanent purchase B, renting only while cumulative
premium remains below B and buying on the next threshold-crossing request costs
less than `2B` when hindsight optimum is B, and exactly optimum when it never
buys. The document correctly distinguishes unknown-cost heuristics, resource
vector coordinates, policy-compatible but different assurance modes, public-good
underinvestment, complementary bundles and cap-triggered sealing. Its concrete
algorithmic-family example is marked as a prospective capability, not an already
supported F43 product. Its portfolio and prepaid-search bounds include overhead
and do not promise same-budget nonregression.

The scale note's local fragment theorem and proposed substitution seam agree
with the inspected source boundaries. It explicitly pins the adopted image,
rejects foreign execution flags, charges semantic/receipt data, preserves the
conditional native boundary and distinguishes direct native contexts from the
actual certified frontier after substitution. Its bounded-search claims do not
assert complete global recall or a maintained DHT implementation.

Three precision corrections were requested and their actual replacements read:
`1-product(1-p_j)` means at least one independent holder is available, not all
holders simultaneously; mean load `<= capacity` is the general necessary balance
while strict headroom is the chosen robust operating condition; renewal counts
are logical record-refresh actions, not necessarily separate network calls when
batched. These are closed theoretical wording/math findings, not new tests.

Root then selected concrete source work under `experiments/certified-frontier-01`.
Its separately authorized [SOURCE-REVIEW.md](../../../experiments/certified-frontier-01/SOURCE-REVIEW.md)
records changed-source findings and their status. Do not confuse this theoretical
review with that later source review or either with a runtime result.

## Sources actually read

- October 2 PHILOSOPHY-OF-GROWTH.md, CORE-MODEL.md and GROWTH-CLAIM-AUDIT.md.
- September 27 GROWTH-DESIGN.md, including its critiques of both user references.
- Current canonical AGENTS.md/GOAL.md and current NOW/WORK sections.

This checkpoint's small counterexamples and inequalities are derived above;
they are not attributed to an uninspected external source. Existing project
literature citations remain literature context, not new external verification.
