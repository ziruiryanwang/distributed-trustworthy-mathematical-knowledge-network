# Growth-first decision: make independent mathematical work useful elsewhere

2026-10-24. Source/theory review by project_intake_native, under root's explicit
assignment. This revision follows the user's growth-first steering and replaces
this note's earlier immediate cross-owner network recommendation. No experiment,
native import, owner opening, implementation or Git operation is selected here.
The reference workflow already in progress has its own bounded selection; this
note does not predeclare its result. Full deployable v5 remains unfinished.

## Decision: useful circulation, not catalogue expansion

The next architectural question is:

> When does timely access to independently produced, compatible mathematical
> methods increase what another finite agent can accomplish, after paying for
> discovery, checking, adaptation, failures and the service itself?

The promising causal mechanism is **complementary independent work plus cheap,
timely method reuse**. One agent develops an abstraction or method for its own
investigation. Other agents discover it while working on different problems,
combine it with their own knowledge and avoid repeating some work. Newly enabled
results may themselves be useful elsewhere. No global allocation of research or
mandatory unsolved-task list is needed.

The software must improve a concrete part of that chain compared with searchable
Git/package sharing: time to discovery, compatibility, small-delta admission,
safe use without approving arbitrary remote code, or continued availability.
Ordinary sharing itself is a valid product capability; it need not be replaced
by a new mathematical economics theory. Certificates do not cause invention.

**Next priority:** compare compatibility and applicability costs for one
substantive reusable-method exchange before commissioning more networking.
Root's current synthesis selects interchange above ordinary packages and explicit
checked structure-transport bundles as the hypothesis to challenge. Retain existing
proof identities; identity redesign is deferred, not the selected next mechanism.
Check whether the current type preview and explicit applications suffice. These
questions can change the architecture. Preserve the working native-first route
while deciding; do not implement another campaign by momentum.

## Foundation and comparators: reuse the established arguments

Under fixed axioms, a proved theorem does not enlarge unrestricted deductive
closure. Conservative definitions can nevertheless add useful vocabulary.
The existing philosophy checkpoint already resolves this apparent paradox:
finite agents are not logically omniscient; growth is **resource-bounded warranted
capability**, not statement count. We need not choose between realism, formalism
and structuralism to enforce derivability under a pinned policy.

Validity is independent of human intention. Local interests affect investigation,
not mathematical acceptance. Evaluation workloads are external analytical tools,
not protocol-level intentions or a mandated network agenda.

Keep three comparisons distinct:

1. **L: independent optimized local libraries.** Same initial mathematics,
   toolchain, caches, proof techniques and local optimization abilities. Warm
   reuse is not repeatedly charged as fresh discovery.
2. **O: ordinary searchable sharing.** L plus plausible packages, Git/source
   publication, metadata and locally approved tools. Do not withhold a contribution
   already accessible here merely to manufacture a commons advantage.
3. **C: the commons.** The proposed selective discovery, compatible reuse,
   independent admission and custody route. It may implement much of O.

L versus O/C asks whether sharing helps. O versus C asks whether our integration
and assurance choices earn their costs. A gain in the first is not a proof of
the second. If O already offers identical safe discovery and admission at equal
cost, C has no strict intrinsic advantage; it can still be a useful implementation.

Compare complete histories with equal producer and consumer endpoints. If the
producer discovers method M for its own work under both routes, common discovery
work cancels, but extra generalization, publication and certification do not.
If sharing induces creation of M, charge that induced work. Neither charge all
producer work only to sharing nor pretend sharing-induced production is free.

## A causal model: circulating a useful new method earlier

Suppose M is genuinely new to the relevant consumers, not necessarily new to
all mathematics. Its arrival is an external event caused by ordinary independent
investigation. Let lambda(t) be the rate of otherwise uncached consumer needs in
a finite horizon T. Let p_C(t) and p_O(t) be the probabilities that a need obtains
and successfully uses M through each route. They include discovery, availability,
compatibility and discharge of its premises, not merely index membership.

First assume identical optimized post-adoption local behavior and a saving d(t)
per successful use against the same pre-adoption route. Let H be the incremental
fixed and maintenance cost of C over O, and q(t) its incremental per-opportunity
search/screening/failure/service cost, excluding costs already in d(t). Then:

~~~
E[Delta_C-O] =
  integral_0^T lambda(t) [(p_C(t)-p_O(t)) d(t) - q(t)] dt - H.
~~~

This is an accounting identity for the stated coupled model, not observed demand.
If savings and uptake are correlated, use conditional expected savings inside
each route's term rather than factor a common d(t). Both routes may have failures;
compare equal final endpoints or separately report completion probabilities.

A simple non-tautological sufficient case is an **adoption window**. Assume O
cannot supply M before tau_O, C can supply it after tau_C < tau_O with success
probability at least p, and the saving on those uses is at least d > 0. Suppose
C and O otherwise have equal outcomes/costs except total incremental overhead
bounded by H_total. If need arrivals have expected rate at least lambda throughout
that window, then:

~~~
E[Delta_C-O] >= lambda p d (tau_O-tau_C) - H_total.
~~~

Here p is a lower bound conditional on each counted eligible opportunity and
its relevant history/context, including capacity and availability; d bounds
the saving conditional on that successful use. A marginal uptake percentage
from a different population is not enough. These conditional assumptions and
linearity of expectation do not require independent or Poisson arrivals.

This exposes concrete implementation obligations: earlier publication/discovery,
cheap compatible admission, and adequate uptake. It does not stipulate that a
Git repository always has a release delay: direct branch/source sharing may make
tau_O as small as tau_C. Then the window advantage vanishes. We must inspect the
actual competing workflow, not choose an artificially slow release policy.

For a new verified algorithm, d can come from a source-level cost comparison of
the old supported algorithm and new method on a declared input family. For a
new structural theorem, d can come from replacing a specified repeated derivation
with instantiation plus remaining obligations. In either case, allow the baseline
all known shortcuts and generalization. A long selected proof or slow tactic is
not a lower bound on the best possible mathematical solution.

This model justifies faster propagation of a genuine capability, not autonomous
generation of useful mathematics. It may support a product whose main advance is
safe, fine-grained integration rather than a novel discovery algorithm.

## Heterogeneity and complementarity are the source of leverage

Agents investigate different structures, have different auxiliary results and
use different methods. Work worth doing for one agent can remove work from
another agent's path. This is an information and effort externality: independently
incurred mathematical work becomes useful elsewhere.

For one consumer need, let E_j mean producer j supplies a compatible useful
method during the horizon. Under explicit independence, useful supply has
probability 1-product_j(1-Pr(E_j)). Without independence, only the general bounds
max_j Pr(E_j) <= Pr(union_j E_j) <= min(1,sum_j Pr(E_j)) follow.
Cloned agents, common training and common interests can cause high correlation.
More peers or replicas are not evidence of more distinct knowledge. Retrieval
and availability must still turn potential supply into successful use.

Specialization can increase useful supply but also destroy overlap. The valuable
population is neither identical workers repeating work nor unrelated workers
unable to use one another's results. Shared formal interfaces help this balance;
peer count alone does not measure it.

### Bundle-specific synergy, not a global supermodularity assumption

Consider a fixed allowed portfolio: a local route reaches an endpoint at cost L;
a general method m together with a structure-specific bridge n reaches it at
R < L. Neither alone changes the best route. Gross saving G then satisfies
G({})=G({m})=G({n})=0 but G({m,n})=L-R > 0.

This counterexample violates diminishing returns, so general submodular-library
optimization cannot be assumed. It does not prove global supermodularity either:
libraries also contain substitutes, overlap and costly abstractions. Arbitrary
usefulness can exhibit both increasing and diminishing returns.

Even when gross best-policy capability is monotone because the old route remains
available, **net** gain after acquisition/curation cost need not be monotone.
An actual fixed search policy can also be distracted by additional candidates.
Do not infer that automatically admitting/indexing more valid mathematics always
helps a given user. Selective local acquisition does not change a contribution's
mathematical validity; usefulness ranking must not become a truth rule.

An illustrative pattern is a general transport/fusion theorem plus a new proof
that a particular structure satisfies its premises. Together they enable new
checked applications. This is a pattern, not evidence that a familiar fold theorem
is absent from an optimized Lean library or would beat its existing tactics.

Consequences:

- Singleton usage frequency can miss valuable complements. Discarding everything
  not yet used can prevent later combinations.
- Retaining all possible complements forever is not justified: most may never
  help, while storage, screening and admission still cost resources.
- Discovery can expose a method's explicit premises and compatible supporting
  bridges, rather than ranking only isolated statements and popular names.
- Bounded exploration, bundles and specialist curation are reasonable local
  strategies. Frequency is fallible demand evidence, not unbiased social value.

A checked statement of the form "for every x, P(x) implies Q(f(x))" can already
be a reusable method; another contribution can make P cheap in a new structure.
Actual premise discharge and useful endpoints matter. Forced citations and many
syntactic composition paths do not establish causal benefit or novelty.

Do not introduce a reproduction matrix merely to call its spectral radius greater
than one. Its entries would need independent assumptions about distinct useful
outputs, actual discovery/adoption and resource-feasible investigations. Finite
demand, duplicates, saturation and per-output cost can invalidate a stationary
branching model. The present causal argument needs no exponential-growth promise.

## Which architecture changes could earn their cost?

| Candidate | Productive mechanism | Comparison that decides it |
|---|---|---|
| Native-first compatible method exchange | Share discovery once; apply the result in different local contexts | Finding, adapting and accepting M costs less than the strongest supported alternative |
| Stable mathematical interfaces | Reuse already warranted common mathematics despite incidental proof packaging | Exact meaning can be related without arbitrary equivalence or untrusted aliases |
| Applicability-oriented discovery | Find useful methods and complements before paying full admission | Useful uptake improves at bounded total search/provider cost |
| Selective certification | Reduce repeated genuinely cold checking/transfer for high-demand material | Production and maintenance investment is repaid in a feasible horizon |

The first three currently have higher expected payoff than further certificate
production. Existing find/preview/receive and protected-reference mechanisms may
already support much of them. Learned rankers and local-agent skills can propose
applications; their output remains subject to ordinary checking. Automatic
generalization is optional, charged local work, not a required network service.

### Does this require a new network rather than better packages?

Not by itself. Git can publish a branch immediately, serve immutable content,
retain versions and distribute source. Existing package tools can supply caches
and pinned dependencies. Ordinary theorem-search services can index those
libraries. If that combination supplies the same method equally early with the
same assurance and integration effort, circulation theory selects it just as
readily as a custom peer protocol.

The plausible extra role is an **interchange and adoption layer**: publish a
small supported mathematical delta without merging it into one curated repository;
discover it through replaceable formal indexes; inspect its exact contract;
independently check only the missing supported closure; and reuse it in an
otherwise ordinary local Lean project. Source repositories, static stores and
existing peers can remain authoring/custody transports. No new blockchain,
mandatory universal corpus, central curator or model-training service follows.

Even these are comparison hypotheses. Git can share small branches; an optimized
package route can cherry-pick definitions and check extracted proof evidence.
Fine-grained exchange wins only if its amortized extraction/indexing/admission
cost is lower, or its safer automation improves actual adoption. The producer's
extraction work and the receiver's version adaptation must be included. Same
checker/assurance requirements apply to both routes; do not penalize only one for
hostile-source handling. If ordinary packages are simpler and adequate, expose
the useful checked-exchange layer on top of them rather than demand that users
move all mathematics into a replacement ecosystem.

This is a real architecture fork: a lean interoperability product versus a much
larger bespoke discovery/custody system. The default should preserve compatibility
with ordinary Lean work and require evidence before replacing infrastructure.
Existing peer code is not a reason to choose the larger system; prior investment
is sunk. Conversely, existing code need not be discarded if it already supplies
the selected interchangeable service cheaply.

### Mathematical interface identity is not political attribution

**Current disposition: deferred hypothesis, not selected implementation.** Root
retains current exact proof identities. A nonauthoritative interface cluster or
explicit bridge can support discovery without changing acceptance identity.

Current portable export identity includes an evidence-unit identity. Different
proof witnesses or grouping can therefore yield different IDs despite familiar
names and statements. Shared names/package versions alone prove no equality.
This can shrink a receiver's common warranted frontier and force acquisition.

Investigate separating **mathematical interface identity** from **witness identity**
for a narrowly justified subset. For opaque proposition-valued theorem exports,
two independently accepted proofs of the same exact type in the same exact
semantic dependency environment can support the same theorem interface while
their evidence objects retain different identities and costs.

This is NOT permission to rewrite current IDs. Exact universes, declaration kind,
policy and semantic dependencies must bind the interface; imported references need
a checked correspondence/substitution argument. Transparent bodies, inductive and
recursor groups, and computational semantics cannot be discarded. Hashing types
whose dependencies remain proof-sensitive does not solve recursive fragmentation.
An interface hash proves no theorem; independently accepted evidence still does.
Start with exact structural compatibility, not arbitrary mathematical equivalence.

Existing CP-001F/G/H already investigated semantic judgment/proof-instance
separation. Do not rediscover it as a new mechanism. In particular,
CP-001H-proof-computation-and-reconstruction.md gives a source-backed paper Acc
countercase: proof substitution can obstruct an unchanged data-valued native
conversion despite equality at a proposition. Mathematical substitutability is
not operational replay preservation. Changing representatives needs affected
environment rechecking or explicit checked transport, with actual support and
costs; old caches/acceptance do not transfer just because an interface matches.

The decision matters to growth because cheaply combining independent contributions
requires a common usable language. A library with millions of individually valid
but unnecessarily incompatible copies may have poor practical composability.

### Inspect applicability before expensive acceptance

Existing preview exposes exact types and bindings, not truth, definition bodies
or guaranteed solvability of premises. A method interface should make parameters,
premises, outputs and necessary semantic dependencies inspectable. Bounded
unification, selected patterns and proof-producing application suggestions can be
local heuristics; cost estimates remain fallible.

First ask whether the current interface already supports the chosen use. Only
missing decision-relevant information warrants another schema. Original locally
approved notation/instance/simp metadata survives protected authoring; portable
declaration deltas do not preserve arbitrary new extension registrations.
A method fundamentally requiring executable tactics may be better supplied by
an explicitly locally approved package, or a narrower explicit theorem interface.
Do not disguise arbitrary executable peer code as inert mathematics.

## Current structure-transport hypothesis: precise challenge

Reuse CP-001G BRIDGE1 and its independent audit, not its historical numerical
search budgets or unimplemented claims. Given checked b:B, f:B->A and
ell:forall a:A,P(a), application gives exactly ell(f(b)):P(f(b)). To obtain
Q(b), require actual native conversion or a checked transport
t:forall x:B,P(f(x))->Q(x). Then t b (ell(f(b))) has the desired type. A map
alone supplies no arbitrary property transfer and does not identify A with B.

For example, transferring associativity back along an injection additionally
needs operation preservation. Without injectivity a constant map to a singleton
can preserve operations from a nonassociative source; without preservation an
arbitrary injection conveys no algebraic law. Residual premises remain conditional
arguments in a properly extended local telescope, never accepted missing proofs.
Paths ending in the same type can have different values and support. The bundle
must expose its actual maps, premises, transports and final result, not only an
endpoint-type label or a claimed equivalence.

The generic theorem is not our new knowledge. CP-001G already records pinned
mathlib injective/surjective semigroup transport. Root's new direct source check
also finds pinned Init LeftInverse.injective and List.foldl_hom/foldr_hom. Thus
flip/involution-to-injectivity and generic fold transport are interoperability
controls, not strong growth cases. A credible case must instead obtain a genuinely
new-to-consumer structure-specific bridge, method or checked instantiation whose
premises the optimized stock library does not already discharge cheaply.

The bundle can initially be ordinary checked declarations plus nonauthoritative
pointers/roles, followed by explicit application under existing acceptance. No
new truth protocol, automatic bridge synthesizer, semantic-ID migration or global
type ontology is needed. Common shared interfaces are voluntarily reused when
cheap; maps relate genuine differences rather than erase them. CP-001G's possible
2m hub maps versus m(m-1) pairwise maps is a count under actual transportability
assumptions, not a bound on proof cost, search cost or universal hub existence.

The key remaining falsifier is economic: a Git/package consumer may already
receive the exact bridge and apply the same transport just as cheaply. Compare
that route with identical generic mathematics and assurance requirements. Credit
our system only for demonstrably cheaper/earlier discovery, safer automatic
adoption or reduced compatible-closure integration. If the generic premise or
bridge is trivial under the stock library, reject the growth case before running
it. If imported class/simp registrations are essential, ordinary explicit proof
arguments or a locally approved package may dominate new metadata machinery.

## Full-cost and large-scale limits

Reuse the established inequality rather than inventing another economics helper.
For opportunity i, let A_i be successful compatible reuse, d_i the conditional
saving including successful-route costs, q_i extra costs not already counted,
and F+M(T) incremental fixed and maintained service cost:

~~~
E[Delta] = sum_i Pr(A_i) E[d_i | A_i] - sum_i E[q_i] - F - M(T).
~~~

No independence is needed for linearity. Bounds Pr(A_i)>=p,
E[d_i|A_i]>=d>0 and E[q_i]<=q yield expected benefit for
n(pd-q)>F+M(T), provided pd>q and n fits actual retention/service capacity.
The existing deterministic operating-region theorem adds eligibility fractions,
burst envelopes and per-queue supply assumptions when those can be defended.
Expectation is not a run-by-run guarantee. Use resource vectors or declared
nonnegative prices; peak memory and latency remain separate constraints.

Let N be global mathematics, K local warranted knowledge, D(X,K) missing proof
closure and S(q) examined postings. Acceptance need not enumerate N, but cold
checking depends on D, selected context loading/hashing can depend on K, and
search work depends on S(q). Native-first reuse does not promise cold
ancestry-free trust. Foreign reports/catalogs or familiar binaries do not replace
actual local warrants or a separately justified certificate/trust policy.

As N grows, supply may improve while clutter raises q and lowers successful p.
Finite specialist coverage, cached frontiers and selective investment are operating
choices, not proofs of recall. Page caps and a DHT do not solve semantic relevance.
Conjunctions can still have huge intersections; instantiation can introduce goal
symbols absent from a useful stored theorem. Snapshot coverage is not global
completeness. Availability requires paid retention and repair, not advertisements.

Current finite serve holds the owner lock and exposes selected custody exclusively.
Continuous service will need explicit publication/state concurrency design. That
is real release work, but it should follow selection of the useful exchange model,
not displace it merely because another implementation step is available.

## Falsifiers and the minimal next evidence

Sharing cannot earn the proposed gain when the comparator already finds and uses
the same method equally cheaply; direct local proof is cheaper; useful overlap
or compatibility is negligible; retained evidence disappears; overhead consumes
all avoided work; or payback needs exceed capacity/retention. A wrapper, renamed
duplicate or new filename is not a counterexample. Accept negative evidence.

Select one compact **use-case and cost argument** before another campaign:

1. Name independently motivated producer/consumer contexts and a reusable method
   or complementary pair. Reuse existing checked material if suitable. A tiny
   flip/reflexivity example establishes mechanics, not meaningful growth.
2. Specify complete L/O/C histories and the strongest plausible competing route.
   Check whether a known library theorem, tactic, cache or direct Git workflow
   already erases the supposed gain. Do not ban it after discovering this.
3. Draw exact dependencies and portable frontiers on paper. Identify whether
   identity fragmentation, applicability, unavailable metadata or genuinely costly
   checking blocks economical use. Do not assume reference registration transfers
   another owner's trust.
4. Derive a feasible region from source-level bounds and existing costs. Expose
   unknown uptake, adaptation and demand rather than fabricating payoff. Include
   producer, discovery, curation, failed-search, checking and service work.
5. Gather only evidence that changes the decision: a correspondence argument if
   identity is the obstacle; a compact query inspection if recall is the obstacle;
   a changed-boundary integration if current APIs suffice. No new certificate,
   broad proof-search campaign or repeated package demonstration is implied.

An opportunity-cost stopping rule applies before each proposed action: name the
competing decisions, the outcome that would switch the decision, likely avoided
downstream waste, and the action's full cost. If both plausible outcomes select
the same architecture, defer the test. If a source-level shortcut erases d, stop
that benefit case instead of constructing a harder fixture. If exact common
snapshots already align sufficiently, do not migrate identity merely because a
more general interface scheme is attractive. If applicability or useful demand
is the unknown, more transport/package tests cannot resolve it. Prefer the
smallest observation with a credible chance of changing the next costly choice;
this rule does not require a fabricated numerical estimate of research value.

The user has no external Lean project. Controlled examples do not supply evidence
of real adoption, heterogeneous demand or broad practical superiority. Theory can
still eliminate bad architectures and justify a stated nonempty operating region.
That is useful progress, not completion of deployable v5.

## Reused evidence

- Current GOAL/NOW and the Oct22 architecture reaudit govern reality-led,
  consumer-driven native-first priorities.
- v4-2026-10-02/PHILOSOPHY-OF-GROWTH.md supplies explicit/implicit knowledge and
  noncircular evaluation. Its certificate-specific implementation is historical.
- v5-2026-10-20/GROWTH-CLAIM-TARGET.md, PROOF-SEARCH-REUSE-COMPARATOR.md and
  GROWTH-OPERATING-REGION.md supply optimized histories, full costs and capacity.
  This note adds heterogeneous supply, bundle synergy and timely circulation;
  it does not claim a measured positive margin.
- ORDINARY-PRACTICAL-COST.md records local context costs and the search case with
  fewer postings but more bytes; neither is a universal scale result.
- ordinary_lean/ordinary_semantics.py:export_id, preview peer APIs and
  ORDINARY-REFERENCE-LIVE-INTEGRATION.md supply current identity, discovery,
  protected-import and metadata boundaries. No new runtime was needed.
