# Growth mechanism: cheap warranted capabilities, not receipt accumulation

2026-10-06 UTC. Owner: `/root/growth_mechanism_v4`. Theory/source investigation;
no runtime, publication, installation or product mutation. This is a candidate
for adversarial review, not a claim that v4 meets the full goal.

## Decision

The commons should accumulate **reusable parameterized capabilities**, with
mathematical acceptance separate from a local decision about how much to spend
making each capability accessible. A theorem schema, an exact definition and a
verified algorithm can jointly provide a capability; another theorem filename
need not. Reuse should be optional, with a bounded exploration cost and a
preserved direct route with explicitly bounded interference. Expensive
certification should be an investment option,
not a compulsory tax on every local mathematical discovery.

There are three consequential design choices:

1. Keep cheap bounded proof deltas above a certified cut, and promote a delta
   to a succinct certificate when a local resource policy justifies the cost.
   The raw route needs a real checker and explicit assurance profile, not a
   conditional native result. An unsealed delta is not automatically a permitted
   parent of the current contributor.
2. Make bundles and theorem/algorithm schemas first-class **local policy units**.
   Reuse a parameterized capability across independently chosen investigations;
   do not rank mathematical value by instance count or isolated lemma popularity.
3. Preserve direct reasoning and exact access as alternatives. Optional search,
   bad rankings and a huge irrelevant corpus must have bounded interference with
   an agent that could have succeeded without them.

The existing philosophy already distinguishes logical closure from resource-
bounded capability, and CORE-MODEL already states a break-even identity. The new
contribution here is an implementable online decision rule with a pathwise
bound, a precise baseline-preserving search contract, a constructive mechanism
for algorithm-family speedups, and the actual composition barriers that software
must remove. None requires a global mathematical agenda.

## Epistemic position and formal objects

Adopt an operational, resource-sensitive interpretation, compatible with
formalism, structuralism or realism: the system stores warranted descriptions
and transformations that finite agents can actually use. It does not claim to
create new members of a fixed foundation's unrestricted deductive closure.
Mathematical content and its material accessibility remain different objects.

Fix a foundation/checker profile F, an endpoint equivalence relation E and a
local resource order. E must preserve the claimed formal result and assurance
policy; a weaker specialization or unchecked answer is not an equal endpoint.
Resource vectors retain CPU, elapsed time, memory, storage and traffic separately.
A scalar theorem below concerns one declared additive unit, not an implicit
conversion between them.

A usable capability is a tuple

```text
C = (F, exact interface, semantic data, acceptance evidence,
     admissible application procedure, finite resource envelope).
```

The application procedure may be the elementary operation of specializing a
theorem and proving its explicit remaining premises. It may instead be a
verified algorithm with a soundness theorem. Executable tactics/model policies
are not imported as mathematical authority. Their outputs still cross the
ordinary checker boundary. Endpoint choice belongs to the local agent.

For a particular local policy pi and accessible state K, define
`Cap(pi,K,b)` as endpoints it can produce with acceptable evidence within budget
vector b under the specified environmental assumptions. This is not generally
decidable or directly enumerable. A witnessed execution proves membership;
absence from a bounded search does not prove nonmembership.

An expanded archive need not expand the realized Cap of a fixed heuristic:
search distraction, storage eviction and unavailable dependencies can reduce it.
By contrast, the set of **available algorithmic options** is monotone when the
old environment, direct algorithm and resources remain available unchanged.
Calling that existential monotonicity realized growth would be a mistake. The
scheduler below gives one realizable, deliberately weaker guarantee.

There is no universal positive scalar value for every valid theorem. If C is
cheap for q1 but not q2, and D reverses the advantage, changing local workload
weights reverses their ranking. This does not make validity subjective. It makes
resource investment relative to circumstances, like caching or algorithm choice.

## Mechanism A: reusable schemas can change the algorithm, not just its notation

Suppose a checked theorem has the interface

```text
forall x, Preconditions(x) -> Result(x).
```

Given exact x and checked witnesses of Preconditions(x), elementary theorem
application produces Result(x). It does not require rediscovering the schema's
proof for every x. The proof cost bound includes instantiation, premise proofs,
conversion, selected semantic data and the assurance mechanism. It does not
erase expensive preconditions or arbitrary demanded computation.

More consequentially, a bundle can contain a definition of an algorithm A and
a theorem proving its output relation. The mathematical object then supplies a
reusable solver for an entire specified family, not just one answered question.
That is a defensible philosophical unit of productive knowledge: a warranted
inferential/computational action made accessible to other finite agents.

### A constructive cost transformation, without an optimal-proof lower bound

For a monoid with fixed-size element representation and multiplication costing
at most M in a chosen abstract machine, exponentiation by squaring computes
`a^n` using O(log(n+1)) multiplications. The elementary linear algorithm uses
`n` multiplications. Correctness follows from the monoid laws and exponent laws;
the binary algorithm's recurrence halves the exponent each step and performs
at most a constant number of multiplications per binary digit. Count bit
inspection/arithmetic and intermediate representation costs too: with the
stated fixed-size carrier, these do not reintroduce n multiplications.

A shared verified binary-power implementation plus its correctness theorem
therefore supplies a concrete transformation from one correct algorithm to
another with a provable asymptotic operation-count advantage on the declared
family. For example, fixed-dimension matrices over a fixed finite field satisfy
the bounded representation premise. The comparison is with the specified
linear implementation, not the best possible independent mathematician.

This claim is theoretical and requires no large performance campaign to prove
its multiplication count. Actual CPU constants, correct integration and the
chosen carrier implementation remain separate implementation obligations. It
does not establish a new algorithmic discovery, nor is this algorithm currently
qualified in the restricted F43 product. It is an architectural target showing
what meaningful reusable capability looks like.

Sharp contrast: if the carrier is an arbitrary opaque endofunction and the task
is to evaluate `f^n(x)`, packaging function composition as multiplication does
not make evaluation logarithmic. The compact composition representation may
still execute f n times. Nor does proving an iteration identity once imply that
an optimal direct prover must repeat induction. The current `iter`/`plus` seed
is useful vocabulary; its mere existence is not this speedup result.

### Why this supports independent investigations

The parameters and preconditions are formal interfaces, not a global task list.
Different agents can discover them while pursuing unrelated local goals. A
later agent may construct a new data structure or algorithm and prove that it
satisfies the same premises. It thereby gains the entire certified capability
without the network deciding what it intended. Applications do not all count
as distinct knowledge increments; the new reusable interface, a reduced cost
frontier or a genuinely new algorithmic option is the relevant change.

## Mechanism B: locality at a certified cut, with a seal barrier

Consider a proof derivation whose external assumptions are selected certified
Prop interfaces. All other proof/definition data needed for the new result is
inside a finite delta D. If the checker actually checks D and authenticates all
external interfaces, acceptance depends only on D, the selected interfaces and
their receipt verification. No theorem proof below that cut is required.

Write c(D) for new local checking work, s for demanded semantic data, p for
selected parent interface/receipt work, and h for bounded framing/identity work.
The route has cost `c(D)+s+p+h`. This is a decomposition of the selected
algorithm, not a claim that c(D), conversion or interface size is constant.
If profile bounds constrain these components, ancestral proof length is absent
from the per-reader bound even as the network corpus grows.

The scale investigation identifies an actual promising seam: `host.rs execute`
checks genuine non-development parent receipts, runs the pinned guest relation
and demands its exact successful journal. A release wrapper would also need an
independently pinned image/profile, exact capsule/member binding, inert bounded
packet and complete resource containment. Local execution and receipt checking
have different trusted computing bases; a policy may accept both, but their
assurance labels must not be conflated.

**Composition barrier:** the current relation permits only certified external
Prop parents. A locally executed unsealed result is not thereby an eligible
parent. To reuse it, one must either certify it, or construct and check a larger
bounded delta containing its proof and needed dependencies above the same
certified cut. The current one/two-output restrictions do not already provide
arbitrary checked multi-declaration islands. A leaf-only raw reader would reduce
read/certification cost but would not close sustained reciprocal growth.

Repeated inlining eventually reaches a packet/work limit. At that boundary the
agent must (a) seal a checked frontier, (b) choose a different shorter proof, or
(c) decline/defer the work. There is no silent recursive fetch of unsealed
ancestors. A genuine seal costs resources and is a prerequisite for continued
cheap compositional reuse, not a free cleanup step.

## Mechanism C: online rent-or-buy with a real guarantee and no future-demand oracle

This theorem supplies a local certification/retention policy only where its
premises hold. It is not a universal claim about theorem utility.

### Exact finite model

An arbitrary, possibly adaptively chosen sequence of requests needs the same
capability or indivisible bundle. Both routes deliver an E-equivalent endpoint
under a policy that explicitly accepts both assurance modes. The i-th request
has a common cost v_i and an extra unpromoted cost r_i >= 0. The nonnegative
r_i is known before the decision for request i. A one-time investment B > 0
removes that extra cost for all remaining requests in the epoch. There is no
expiry, eviction, budget failure or hidden later maintenance; otherwise those
effects need a different model. B includes all incremental certification,
transfer/index/retention costs assigned to this epoch and is available now.

Policy: retain S, the extra cost of prior rented requests. Before request i,
if `S+r_i >= B`, buy and use the promoted route; otherwise rent and set
`S := S+r_i`. After buying use the promoted route. No future requests, demand
distribution, publisher identity or universal usefulness score is needed.

Let R = sum r_i. The offline comparator, knowing the whole sequence, pays
`OPT_extra = min(R,B)`. Buying later cannot beat buying at the first request
for this stationary no-expiry model.

**Proof.** If the policy never buys, R < B and its extra cost is exactly OPT.
If it buys, earlier S < B while the triggering prefix's total rents would be
at least B; thus R >= B and OPT_extra = B. Policy extra cost is S+B < 2B.
Adding the common nonnegative sum v_i preserves the 2-competitive bound on total
cost. The conclusion is pathwise, so the requests may be generated by arbitrary
independent or adaptive investigations. It does not assume stochastic demand.

This is the elementary deterministic ski-rental argument, fully supplied here;
no literature theorem is being used without stating its premises. The word
competitive compares this particular two-route investment problem, not all
possible proof strategies or semantic values.

### What changes with actual software information

- Measured historical CPU is not a known future r_i. An estimate may drive the
  heuristic policy, but it does not inherit the exact theorem.
- If r_i is learned only after a completed rent, buying once paid S >= B gives
  extra cost `< 2B+r_max` provided each rent increment is bounded by r_max.
  On a bought trace OPT_extra = B; the overshoot is an explicit additive term.
- If certification has an uncertain cost bounded above by B, the threshold
  guarantee is relative to the declared conservative B, not an oracle optimum
  using the unknown lower actual price. Failed attempts and reserved resources
  remain charged. With no bound or unavailable investment, abstain.
- If promotion does not remove a positive per-use premium, do not buy for
  this economic reason. Smaller bytes, future interoperability or a different
  assurance preference may independently justify buying, with their own claim.
- If promoted and unpromoted routes are not accepted under the same endpoint
  policy, this is an assurance choice, not a rent-or-buy speedup comparison.
- Repeated short leases or eviction invalidate a one-time permanent-buy model.
  Fresh epochs need fresh accounted investment; do not reset accumulated spending
  and apply the guarantee across free fictitious restarts.
- Overlapping bundles and shared cache/prover capacity can couple prices and
  feasibility. Independent per-row 2-competitive statements do not imply a
  2-competitive global allocation. Apply the theorem to one explicitly indivisible
  admitted bundle with stable marginal costs, or label the coupled selector a
  heuristic. Buying a can change the rent/buy prices for b, violating stationarity.

Current large seed production cost is a historical observation, not a forecast
of B for a new theorem. Global popularity cannot be substituted for local r_i.
Foreign demand reports may be advisory. An operator may voluntarily fund public
benefit beyond its local returns; the system must not claim that private online
optimization automatically solves public-good underinvestment.

## Mechanism D: bounded optional search preserves a direct route

Keep baseline direct reasoning A0 in its original environment, without adding
unrequested imports, changing reduction rules or evicting protected baseline
data. Run a library-aided A1 in separate bounded state. Accept the first valid
E-equivalent result. A1 includes discovery, transfer, checking, application and
its own failures, not just its successful final call.

Under a preemptible one-resource scheduler, give A0 fraction 1-epsilon and A1
fraction epsilon, where 0 < epsilon < 1. If their isolated completion costs are
t0 and t1 and there is no cross-route interference, completion requires at most

```text
min(t0/(1-epsilon), t1/epsilon) + accounted scheduling overhead.
```

The argument is direct: after elapsed resource T the routes receive their
respective shares, so either has completed when its share reaches its isolated
requirement. Arbitrarily bad retrieval cannot create an unbounded slowdown of
A0. This is a bounded-robustness guarantee, not a theorem that optional search
always accelerates it. An LLM-controlled workflow does not automatically obey
this schedule merely because a prompt recommends it.

For the present command API a simpler enforceable variant is a sequential
prepaid search/application allowance H followed by the untouched baseline.
If A1 fails within H and the baseline remains available, total cost is at most
`H+t0` plus explicitly charged setup/switching. This needs command containment,
not a speculative autonomous prover scheduler. H can be chosen by the local
agent, or by a replaceable heuristic. No theorem says the best H is known.

CPU scheduling alone does not bound wall-clock network stalls, shared-memory
pressure, disk I/O or agent-token costs. Those require separate caps/partitions;
a blocked unkillable checker or eviction of A0's data violates the premises.
Use the additive version until the implementation actually isolates and schedules
both routes. A limit response is UNKNOWN/INCOMPLETE, not theorem absence.

## Complementarity and a bounded local policy

Let two checked components a and b each have zero benefit alone, while their
joint use closes a task that neither alone can solve within budget. Then the
marginal value of b after a is larger than its marginal value before a. Thus
submodularity/diminishing returns cannot be assumed for mathematical capability.
Greedy per-lemma popularity can discard every component of a useful bundle.

The minimum practical policy is therefore:

1. Accept mathematical objects under the checker independently of scores.
2. Keep a bounded candidate window containing exact individual interfaces and
   explicitly nominated small bundles, with full union-cost accounting.
3. On an actual local application, record the exact selected bundle, completion
   and costs once. A proof occurrence is a use signal, not causal necessity or
   an estimated amount of effort saved.
4. Reserve a bounded exploration portion for low-history candidates; exploitation
   uses local signals/estimates. Both are heuristics. Never claim finite-window
   exploration guarantees discovery of every rare valuable theorem.
5. Apply the proven investment rule only to rows whose two-route economic model
   is justified; otherwise label estimates heuristic or abstain. A scoring field
   never changes acceptance, execution authority or resource reservation.

Existing CACHESEL1 already has bounded local observations, exploratory slots,
bundle accounting and lifecycle controls. Do not duplicate it as a new global
ranking subsystem. Its older native-replay cost signal is not automatically a
valid r_i for the new certified/delta routes. Adapt the cost/protocol bindings
only after the chosen successor is real.

## Immediate product contracts and outstanding central obstacles

| Boundary | Required data/invariant | Present implication |
|---|---|---|
| Capability identity | Exact F/profile, kind, formal telescope, semantic IDs, evidence mode | Reuse existing typed capsules; no natural-language-intention field |
| Local delta acceptance | Exact adopted image, inert packet, certified cut, expected journal/member, finite resources | Existing host execute is a candidate primitive, not a shipped safe reader |
| Re-contribution | Sealed result or complete bounded new delta above a certified cut | Unsealed acceptance is not automatically reusable as a current Prop parent |
| Promotion decision | Cost unit, immutable epoch/object/bundle ID, B, r basis, spent S, allowance and decision | Exact guarantee only with stated model; estimates separately tagged |
| Application telemetry | Once-only event, exact inputs/output, result, actual nested cost scope | Local advisory data; neither popularity nor use count authenticates truth |
| Optional search | Explicit budget, incomplete status, preserved exact/direct route | Sequential bounded exploration is implementable before an automatic portfolio |
| Semantic composition | Complete bounded demanded definition DAG and exact body/typing dependencies | Current F-closed-only definitions do not yet support layered vocabulary |

The last row is a major growth limitation. The current contributor permits only
F-closed new definitions, a fixed43 foundation lacking List, at most four
contributed definitions per Prop, and no contributed-definition dependency
chain. It can preserve vocabulary, but cannot compose arbitrarily many layers of
new vocabulary except by inlining to F or changing the profile. This is not
fixed by a better popularity score or a faster receipt verifier.

A scalable successor should distinguish theorem proof ancestry (never required
for an accepted certified parent) from **demanded semantic dependencies** (must
be present and checked when used in types/conversion/computation). Exact acyclic
definition manifests plus bounded, cacheable, explicit acquisition can support
layered vocabulary. Opaque interfaces can defer bodies only where the logic and
declared transparency permit; a body hash alone does not supply conversion.
This is a central design requirement, not an implemented v4 extension in this
note. Its cost may grow with the actually demanded semantic DAG, never secretly
with the whole network corpus.

## What can and cannot be concluded about growth

Theoretical guarantees available now are conditional and substantial:

- A verified algorithmic capability can provably reduce costs for a specified
  family relative to a specified algorithm, without running a large benchmark.
- A bounded delta above certified leaves has no theorem-proof-history term in
  its selected checking cost; new computation and interfaces remain payable.
- A correctly instantiated online investment policy is within factor two of
  the hindsight two-route optimum on every request sequence, without oracle
  demand. This prevents one common way of wasting certification resources.
- Capped optional search cannot arbitrarily delay a protected direct baseline
  when the precise isolation/containment premises hold.

These do not imply all locally chosen investigations succeed, all mathematical
value is detectable, or global useful knowledge grows exponentially. An
architecture can furnish warranted algorithmic improvements without guaranteeing
that agents discover enough valuable inputs to exploit them. Under fixed finite
resources and a positive minimum cost per accepted distinct output, output rate
is bounded. Infinite sustained or exponential claims need explicit increasing
resources, growing opportunity families and preserved discovery/availability.

No additional campaign should merely estimate an already proved recurrence.
The decisive implementation work is (1) safe bounded delta reader and honest
assurance labels, (2) actual bounded delta re-contribution/rollover or an explicit
seal barrier, (3) local policy records/caps rather than an automatic certification
tax, and (4) a plan for compositional semantic vocabulary. Focused tests should
challenge those changed contracts. Benchmarks are needed only for unknown
constants/compatibility, not as a substitute for this model.

## Sources and deduplication

- [Previous philosophy](../v4-2026-10-02/PHILOSOPHY-OF-GROWTH.md), read in full:
  explicit/implicit knowledge and the previously inspected SEP logical-omniscience
  source. This note does not claim a new metaphysical theorem.
- [Previous core model](../v4-2026-10-02/CORE-MODEL.md), read in full: ancestry
  locality, existing net-benefit identity and failed typed-row optimization.
- [V3 growth design](../v3-2026-09-27/GROWTH-DESIGN.md), inspected including its
  model critique: no spectral/exponential model adoption or duplicate trial.
- [Existing local cache policy](../../modules/cache-selection/proposal.md),
  inspected for existing bundle/use/exploration/lifecycle mechanisms; not a new
  implementation authority and not inherited certified-route economics.
- [Current authored contributor API](../../../experiments/certified-foundation-restore-01/project/companion/CONTRIBUTOR-API.md),
  read in full: actual F-closed definitions, parent restrictions, packet caps,
  prepare/advance separation and assurance caveats.
- [Existing endpoint analysis](../v4-2026-10-02/GROWTH-ENDPOINT-SELECTION.md),
  read in full: avoid repeating cheap E1/map wrappers and do not claim the
  existing iteration seed proves economic advantage.
- [Search crowding decision](../v3-2026-09-29/SEARCH-CAPABILITY-CROWDING-DECISION.md),
  read in full: candidate diversity is not application success or causal utility.

All new inequalities/online-policy bounds are derived above. The binary-power
example is a standard elementary constructive argument, not an unverified
claim about this product's currently supported carrier/library.

## Semantic vocabulary: the next composition boundary after bounded fragments

2026-10-06 additional root-assigned investigation. Design recommendation only;
no guest/schema/foundation change is selected. The fragment lane should close
first. Its proof-only-definition test matters here: the semantic context required
to check a proof is not necessarily the definitions mentioned by its output type.

### Minimal acyclic definition object

Use a new, explicit profile for a definition node d with the following fields:

```text
foundation/profile
ordered universe parameters
closed generic type T
closed generic value v
safety = safe, declared transparency/reducibility
exact direct dependency IDs occurring in T or v
```

Name-free declaration content is committed first; the canonical name is derived
from its resulting ID. References to another contributed definition use that
definition's exact already established ID, not a mutable author name or a
globally agreed sequence number. Recompute the dependency list from expression
nodes; a peer-supplied shorter list is not authority. Commit the two sets
`typeDeps(d)` and `bodyDeps(d)` separately if useful for planning, but acceptance
checks their exact union and every actual occurrence.

For the minimal successor, reject mutual/self recursion and new inductive
groups. A finite manifest supplies a topological order of the demanded closure;
every nonfoundation reference points to an earlier exact node. Generic universe
parameters are checked once in each declaration's own telescope. Applications
instantiate them as usual. Hash collision resistance authenticates identities;
it does not prove acyclicity, typing or availability. Those checks remain explicit.

**Conditional conservative-composition theorem.** Suppose F has the intended
typing/substitution properties. For each topologically ordered node d_i, its
declared type is well formed and its safe body v_i is checked at that type in
`F + d_1 + ... + d_(i-1)`. Adding the declared transparent definition introduces
no new old-language theorem beyond F. Proof: successively replace the fresh
constant d_i by its universe-instantiated body, in reverse dependency order.
Ordinary type substitution and definitional conversion preserve each judgment;
acyclicity makes the finite translation terminate. This is a meta-level
relative-soundness argument, not a proof that our current exporter/checker or
every Lean feature implements it. Restricting the first extension to nonrecursive
safe definitions keeps the required theorem elementary and reviewable.

This extension is materially different from merely permitting an arbitrary
data-valued axiom. The body and its typing obligation are part of the object.
No popularity score or declaration-name hash supplies a missing body witness.

### Exactly what a receiver must materialize

There are three different needs, which should not be conflated:

1. **Reference/signature use.** To type a term mentioning d, the local checker
   needs an authenticated interpretation and a well-formed type for d, including
   the semantic signatures required by that type. A bare ID is insufficient.
2. **Transparent conversion.** If type checking needs to delta-reduce d, the
   exact body and its resulting dependencies are needed. A hash cannot perform
   the reduction. If types themselves compute with d, this can happen before
   any apparent execution of the user's algorithm.
3. **Evaluation.** Executing d needs its demanded computation/data, even after
   a certificate proves that d has the advertised type or satisfies a theorem.
   Proof succinctness is not a universal shortcut for evaluating programs.

The simplest sound implementation is eager finite semantic closure: obtain all
definitions reachable from the chosen type/proof input, authenticate and check
them in topological order, then run the ordinary checker. This can be expensive
but has an honest locality property: it visits the selected semantic closure,
not the whole network corpus or the theorem proof history below certified cuts.
Use explicit limits on nodes, bytes, nesting, visits and conversion work. If the
closure exceeds them, refusal is the correct finite-profile result.

An optimized implementation can cache exact checked declarations, keep signatures
available and materialize bodies on demand, but lazy loading must be an actual
checker-supported discipline. It cannot create undeclared constants first and
hope their types later work. Unavailable required bodies mean deferred/refused
conversion, not permission to assume equality. Sharing downloaded bodies across
requests is legitimate only while exact profile/identity/checking guards remain
valid; cache eviction changes availability, not mathematical truth.

### Opaque data interfaces are possible, but are a distinct relation

There is a principled opaque alternative. A certificate could authenticate an
exact witness `F |- v : T`; a local proof may then reason about an opaque
constant c:T under a view explicitly bound to that witness. Any resulting
derivation can be interpreted by substituting v for c. Crucially, the opaque
view supplies no delta-reduction equation for c. A proof requiring the actual
definition's computation does not automatically work through this interface.

This has a different contract from silently importing every received Definition
as a body-free axiom under its old transparent identity. Its evidence must bind
the exact underlying DefinitionID, T, universes, view mode and allowed conversion
rules. If T depends on other definitions, their required signatures/semantics do
not vanish. Revealing a body later requires an authenticated refinement/rebuild
discipline; the same installed local declaration cannot silently acquire a new
value or reducibility policy. An opaque view needs its own authenticated view ID
or an equally explicit profile-level distinction.

The current guest accepts body-free **Prop** parents and genuinely checked
definition bodies. It does not implement this data-witness abstraction relation.
Adding it now would require a new guest/image and corresponding interpretation
argument. It is therefore not a free option inside the current fragment patch.
It is useful longer-term for huge implementation bodies whose clients need only
typed operations and proved laws, not transparent computation.

### Conditional size and work bounds

Let D be the actually demanded distinct semantic nodes, E their dependency edges,
and S their total distinct serialized bytes. With content-addressed duplicate
suppression, acquisition and a standard graph traversal require O(S + |D| + |E|)
data processing, plus routing/availability work. With a hash table this is an
expected lookup-work statement under its assumptions; balanced maps give their
usual logarithmic factors. Topological checking adds `sum check(d)` and later
conversion/evaluation work C. None of those latter terms is claimed linear in
S, and a correct timeout does not show that the mathematical object is invalid.

Relative to an already checked exact local cache K, missing transfer payload is
the union `D minus K`; checking reuse is allowed only under the pinned trust
guard. The planning traversal still needs enough authenticated metadata to
establish the required closure. "All dependencies cached" is not O(1) knowledge
without a maintained validated closure summary.

Generic declarations can be stored once, while use at different universe
arguments creates distinct specialization/conversion states. An expansion
algorithm's useful bound is by the number W of distinct reachable
`(declaration-or-expression, substitution)` states, not just source node count.
If each such state processes at most b schema fields, its transformation work
is O(bW), plus output bytes and checker work. W itself may be large; the composer
therefore needs a hard state/work bound and substitution-sensitive memoization.

Do not assert that all inlining is exponentially large: the existing DAG can
share identical subexpressions. Conversely DAG sharing cannot make every
normal form or demanded execution small. For opaque arbitrary f, evaluating
`f^(2^n)(x)` can still require 2^n black-box calls despite a tiny repeated-squaring
composition DAG. Interfaces should preserve useful abstraction, not promise to
abolish computational complexity.

The theorem-proof cut and semantic closure are therefore orthogonal. A reader
can avoid every ancestral theorem proof while still needing a large semantic
closure for its own chosen operation. A huge network does not force that closure
to be global, but neither does decentralization guarantee it is always small.

### What parameterization already buys without a new guest

Many abstractions do not require a new contributed data definition. Quantify
over their carrier, operations and laws:

```text
forall (A : Sort u) (op : A -> A -> A) (unit : A),
  Associative(op) -> LeftIdentity(unit,op) -> RightIdentity(unit,op) ->
  Result(A,op,unit).
```

The law names above may be expanded as ordinary Pi/equality expressions, not
new trusted constants. Exact law proofs are residual premises, never assumed
because an agent labels something a monoid. Existing Sort/function/Nat/Eq
vocabulary can express many such interfaces. An F-closed definition can itself
take the operations as parameters, e.g. iteration or a generic recurrence.
Its users obtain a reusable theorem schema without shipping every concrete
implementation through the network's semantic layer.

This is real abstraction: the theorem does not inspect implementation bodies
that its proof never needs. It is not a complete replacement for compositional
definitions. Applying a schema to concrete operations still needs authenticated
local types and the required laws; publishing a concrete instance must fit the
current profile. Large telescopes, repeated law bundles and parameter passing
can be cumbersome, and new inductive data structures remain unsupported. Church
encodings or inlining can sometimes represent them but are not a universal
efficient substitute for native types and disciplined modules.

For a selected schema proof of size L used at substitutions theta_i, proof-term
reuse replaces repeated copies of that chosen proof with checked applications.
The new application pays the exact interface, theta_i, premise witnesses and
conversion. This is a bound for that proof transformation, not an Omega(L)
lower bound on every independent proof: a direct agent may discover a shorter
solution. Only the separate algorithm-family argument can establish a provable
algorithmic cost improvement under its stated model.

### Recommended dependency order

After the bounded fragment reader/composer is actually integrated, first expose
and document **parameterized interfaces plus explicit law obligations** through
the existing F/guest. This immediately enlarges the class of useful reusable
capabilities at no new cryptographic image/foundation cost. A locally verified
fragment can carry the generic law proof; it need not be expensively sealed
before one local use. Native/guest conformance must still validate the selected
ordinary source and contribution path.

Then implement the smallest acyclic transparent Definition DAG with eager bounded
closure and exact caching, in a deliberately new profile. This removes the
current F-closed-only vocabulary barrier while keeping the proof-theoretic
justification simple. Measure only unknown implementation constants; the
conservative-extension and closure-complexity arguments do not require a broad
benchmark campaign. Preserve explicit semantic refusal boundaries.

Defer certificate-backed opaque data views until a concrete dependency-heavy
client genuinely benefits and the abstraction/refinement relation is specified.
They are promising for scale, but silently pretending they already exist would
weaken the trust boundary. No phase introduces a global unsolved-task list,
mandatory intended meaning, attribution authority or full-corpus ledger.
