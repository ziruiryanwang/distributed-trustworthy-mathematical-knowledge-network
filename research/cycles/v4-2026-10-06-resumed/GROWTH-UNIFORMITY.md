# Growth without free answer-specific advice

2026-10-06. Mechanism theory checkpoint; canonical project root only. No runtime
or product change. This corrects the operational interpretation of
`NET-BENEFIT.md`'s existential `Cap_F^W(K,b,e)`; the numerical receiving records
and conditional route-cost algebra are not changed. Independent reviewer owns
the challenge/adoption decision. No global task list, identity authority or
human-intention acceptance field is introduced.

## Decision

Use **policy-realized, endowment-relative capability** for claims about research
or deployable growth. Retain an existential workflow frontier only as an explicitly
oracle-selected feasibility upper bound, never as evidence that an agent can find
the workflow. A fixed workflow language is not enough: workflow selection, new
program/advice construction and proof discovery must themselves occur inside the
charged causal process, or be declared pre-existing/exogenous information.

The strongest currently supported claims remain cheaper warrant checking,
actually available reuse/finite construction, and conditional service/cost
theorems. Current harnesses do not establish autonomous research discovery or a
causal rate of new mathematical insight.

## The defect, even for a fixed uniform workflow language

Let a single fixed interpreter expose `submit_and_verify(p)` for arbitrary proof
bytes p. For every provable endpoint x having a short proof p_x, there exists an
input p_x that the interpreter can submit and check at the cost of reading and
verifying those bytes. Equivalently, a fixed enumerable program family contains
`print(p); submit_and_verify(p)` for every finite p. No separate interpreter is
needed for each endpoint; the language/family was fixed in advance.

Thus

`there exists a supported workflow producing x within b`

can be true merely because an answer-containing input/program exists. It does
not imply that a fixed initially uninformed agent can obtain that input/program
within b. Charging its description length pays transmission/reading, not finding
or selecting it. Calling the class "uniform" does not repair an outer existential
quantifier that supplies the successful program or its argument for free.

This is a logical quantifier distinction, not a claim that an unconditional
lower bound for a particular arithmetic theorem has been proved. It resembles
the difference between verifying a supplied certificate and finding one. An
endowment already containing p_x legitimately supports cheap use of x; it does
not establish new discovery of p_x.

## A causal operational model

Fix before the comparison:

- F: the formal acceptance policy, including checker/cryptographic assurance.
- E: the agent's finite initial information and installed computational endowment.
  This includes code, model/adapter configuration, weights when locally available,
  local library/evidence, retained state and already known method descriptions.
- pi: one causal, computable policy/controller. Its next action depends only on
  its current state and information actually received. Planning, choosing tools,
  compiling new programs and changing its own policy are actions inside pi.
- K: a service process, not a magical set-membership oracle. It exposes the actual
  discover/acquire/check interfaces, costs, content and availability behavior.
- e: a service envelope/scheduler model and a resource-accounting convention.
- rho: the policy/environment randomness under a declared distribution/coupling.
  It must not encode hidden successful answers for free.

An optional local request q may describe a formal endpoint, computation or other
investigation. q is an agent/evaluator input, not a required global agenda. An
autonomous pi may instead select its investigations and candidate statements
internally; all such choices remain part of its trajectory.

Every newly used informative byte must have a declared causal origin:

1. it was already in E or explicitly supplied in q;
2. pi computed or sampled it using charged resources; or
3. a declared external service/human/other agent supplied it through an accounted
   interaction, with its production cost allocated or marked unknown when that
   cost is inside the claimed comparison.

A prompt or advice file containing the answer belongs to one of these categories;
renaming it "workflow configuration" cannot make it disappear. External LLM calls
are service actions: record their declared input/output and cost scope. Unknown
training, reasoning or human work is not silently measured as zero. Sunk initial
endowment need not be recreated on every operation, but matched arms must declare
the same relevant endowment, or separately charge/identify the difference.

This is an evaluation/model contract, not a proposed surveillance requirement.
The network's theorem acceptance continues to depend on formal evidence, not on
agents revealing their training data, internal thoughts or personal intentions.

## Repaired quantities

Let `Run(pi,E,q,K,e,rho)` be the complete causal trajectory. Let C(t) be its
componentwise cumulative resource cost, with nonnegative charges, and let A(t)
be the warrants/capabilities actually produced and checked by time t. Charges
include selection, failed attempts, discovery, transfer, checking and any
required return/custody work. Memory/capacity/deadline constraints need their
own feasibility predicates; they are not added numerically to CPU seconds.

For a formally specified endpoint x, define the event

`S_x(b) := an acceptable realization of x appears on this trajectory within b
and all required service/custody/deadline conditions hold`.

Fix either one q for the autonomous/output-process comparison or one request map
Q:x->q_x for the requested-endpoint comparison. For fixed delta in [0,1), define

`Cap(pi,E,Q,K,e,b,delta) := {x : Pr_rho[S_x(b) on Run(pi,E,Q(x),K,e,rho)] >= 1-delta}`.

Here x is an external mathematical index of a capability. The definition does
not give pi an answer, and it does not permit choosing a different pi, E, advice
string or random tape after seeing which one succeeds for x. If the experiment
passes x as a request, use a fixed request interface `q_x` and count only the
information actually present in q_x. A hardcoded proof in q_x makes the experiment
a verification/use experiment, not a discovery experiment.

For resource tradeoffs, retain the Pareto set of b satisfying this probability
condition, or a declared scalar cost quantile when an additive scalar resource
is appropriate. Do not impose a single scalar utility over all mathematics.
For an autonomous investigator, analyze its random accepted-output process A(t),
or specified downstream formal use relations, rather than inventing a task list
that the network must complete.

The delta=0 case is almost-sure success under the declared randomness/service
distribution, not success for every possible random tape or every support point,
and not a universal guarantee over an unspecified adversarial Internet.
An observed successful run is one trajectory; it is not automatically a bound
on this probability. Prospective theoretical models may supply such bounds,
but their assumptions must be stated and justified independently.

### What a feasibility set may still mean

A set `Reach(E,W,K,b)` based on existential choice from predeclared W can be useful
for protocol expressivity or ideal attainable cost. If W includes arbitrary
programs/advice, classify it as an oracle-selected upper envelope. If one wants
an operable multi-strategy policy, specify the scheduler/selector and charge its
evaluation, search and failed strategies; then it is simply part of pi. Restricting
description length alone does not replace that scheduler.

## Three distinct claims, not one ambiguous growth claim

| Claim | Legitimate initial input | What success establishes |
|---|---|---|
| Warrant verification/access | Supplied object/key, or an already known query | The selected formal claim can be obtained and accepted under the policy |
| Warranted reuse/construction | Known algorithm/schema, local formal input and available methods | A genuine accepted new instance/composition can be made with the charged route |
| Research discovery | Declared initial methods/library and a fixed causal investigation policy | That policy actually finds a method/statement/proof absent from its declared initial supplied evidence, under the stated novelty/equivalence criterion |

"Absent" here is not a computable test for absence from deductive closure.
Exact prior interface/warrant absence is a weak, inspectable criterion; stronger
semantic/capability novelty requires a stated finite criterion or a proof in the
specific case. Renaming a theorem is not research novelty. Discovery of a useful
existing theorem may be a real local access gain without global mathematical
novelty. Neither usage frequency nor this taxonomy changes formal validity.

In this project the actual explicit application and finite-semigroup calculator
have substantial preauthored algorithms, plans and proof schemas in E. They
establish real verified reuse/construction and checking boundaries. Their
execution CPU does not include all earlier research/authoring and cannot be
relabelled as an autonomous proof-discovery cost. Candidate02's preauthored goal
precedes offers and its query/custody is real; that is evidence of non-oracle
discovery through the selected API, not general mathematical research discovery.

## Monotonicity needs an executable fallback

For an existential feasible set, preserving all old witnesses implies set
inclusion. For a fixed realized policy pi, adding optional knowledge need not
improve success: extra search results may distract it, consume its finite budget,
change rankings or make it miss its previous successful path. Therefore

`K0 is contained in K1 => Cap(pi,E,Q,K0,e,b,delta) is contained in Cap(pi,E,Q,K1,e,b,delta)`

is false in general. A one-query agent choosing the first matching candidate is
a simple counterexample: append a lower-cost-to-advertise but unhelpful candidate
that the policy now tries first, exhausting its proof budget before the old one.

A correct nondegradation theorem specifies a controller that can emulate the
old route with the same observations/service guarantees and resource reservation.
If that fallback is actually chosen without extra cost, the old success event
can be coupled unchanged. If selection/emulation costs h, reserve h explicitly;
the theorem uses budget b+h, or requires saved slack covering h. A supposedly
optional global maintenance burden can invalidate the premise. No free oracle
may choose the better route after seeing both outcomes.

## What survives of the amortization and growth argument

The same-method inequality remains valid arithmetic:

`sum_i (lower(a_i) - upper(b_i)) > upper(G)`.

However a_i and b_i now refer to specified causal routes with declared pi/E and
the same required endpoint, assurance and service. G includes all differential
program/proof/advice construction and distribution costs inside the scope. If
these costs or lower bounds are unknown, the conclusion is conditional. No
existentially selected fastest independent prover may be billed as an actual
baseline, and no free prewritten answer may be supplied on only one side.

There is also a precise extra-work consequence. Suppose a shared subroutine
substitutes for a baseline one, returns the same required observations/warrant,
and leaves the continuation's relevant state unchanged. Suppose its complete
charged cost saves Delta>=0, while all other resource and service conditions are
preserved. Run a fixed prefix-preserving continuation policy gamma from that
same state and coupled random tape. With an additive resource budget R, the
set of gamma outputs realized by budget R is included in those realized by
R+Delta: the longer run contains the shorter prefix. Hence any first-success
time T satisfies

`Pr[T <= R+Delta] >= Pr[T <= R]`.

Strict improvement requires positive probability mass in `(R,R+Delta]` for a
specified acceptable new capability. It is not supplied by the inequality
alone. Gamma may fail forever, rediscover duplicates, be limited by another
resource, or have no meaningful new endpoint in that interval. If changed
outputs/timing distract gamma or service deadlines differ, the coupling premise
must be re-established. CPU saved by one owner is not automatically another
owner's funding. This is a deployable conditional mechanism, not an exponential
research theorem.

## Minimal software/research consequence

No new mandatory network policy engine is needed. Current source/selection pins,
exact input manifests, genuine receipt records, process-tree accounting and
preserved failures already support bounded workflow-level comparisons. For a
research-acceleration evaluation additionally predeclare the local policy/adapter,
initial endowment, external advice channels, source-generation cost scope and
endpoint/novelty relation. A source-free test using a preauthored proof plan should
explicitly say so. Agent APIs/skills may implement a policy; their development,
reasoning and calls cannot be exempted merely because the protocol sees only the
final proof.

Root should replace the earlier Cap interpretation and qualify its monotonicity
paragraph with this distinction. The existing cost records need no rerun; the
correction changes which growth conclusions follow, not their observed bytes
or measured CPU. Formal acceptance remains intention-independent throughout.
