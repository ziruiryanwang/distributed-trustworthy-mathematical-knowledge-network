# A full-cost operating region for reusable mathematical methods

2026-10-06 resumed v4. Companion to [NET-BENEFIT](NET-BENEFIT.md), not another
experiment or a replacement for its actual cost scopes. This supplies a concrete
independent-recomputation comparator and a falsifiable positive region. It does
not assert that the conditional region has been measured in a deployed network.

## Exact method supplied by the actual mathematics

The acquired, actually checked `V4Growth.associative_square_blocks` law states,
for any carrier A, associative operation mul, initial a and natural m,n,

`Iter (fun x => mul x a) (Iter double_successor (Plus m n) 0) a`

`= Iter (fun x => mul x x) m (Iter (fun x => mul x x) n a)`.

Here `double_successor k = Plus k (succ k)`; Plus and Iter are exact acquired
definitions, not informal arithmetic smuggled into the checker. The selected
compiler path constructs a portable D1 for one squaring block and D2 for two
blocks. The new T2 law relates the actual compiled D2 body to the same left
side. Its actual public compilation/application/return and separate final
receiving continuation now pass the
[independent outcome review](../../../experiments/compact-commons-01/PUBLIC-ACTUAL-REVIEW.md).
The original full gate remains FAILED_NOT_RETRIED after its last pre-guest
deadline-reservation refusal; the passing continuation does not relabel it.

Define two explicit implementations, with r=m+n:

- **Independent recomputation LEFT:** construct c by c:=0 then repeat
  c:=2c+1 r times; start y:=a; perform y:=mul(y,a) c times.
- **Acquired method SQUARE:** start y:=a; perform y:=mul(y,y) n times and then
  m times, passing the *already evaluated* y to both arguments.

Their exact numbers of mul calls are `2^r-1` and `r`. Proof: c satisfies
c(0)=0 and c(r+1)=2c(r)+1, so c(r)=2^r-1 by induction; the second program has
exactly two loops of lengths n,m. The acquired law proves equal outputs for
every supplied associativity witness. This count is valid without timing trials.
The source proof, cost derivation and independent source/theory review are in
[CAPABILITY-FAMILY-DECISION](../v4-2026-10-06/CAPABILITY-FAMILY-DECISION.md) and
`experiments/capability-family-01/SOURCE-THEORY-REVIEW.md`.

This is a comparison with a **specified correct independent algorithm**, not
with the optimal mathematician. An independent agent may rediscover squaring,
already know it, exploit finite-semigroup periodicity, or solve a special case
more cheaply. In those cases the commons' advantage is reduced or absent.
No theorem about minimum independent proof-search effort follows.

## Matched assurance and what is actually being delivered

The matched endpoint is an exact mathematical input/output relation under the
same foundation, explicit associativity obligation and local acceptance policy.
The baseline is generously allowed its correctness argument at zero incremental
cost; charging that argument only helps the reuse comparison. The acquired
route must pay for obtaining and checking its actual theorem/definition data.

For computation, both routes must use the **same trusted or independently
validated local executor** interpreting their formal definitions, or both must
produce equally checked evaluation evidence. Merely printing the result of a
Python loop is not a proof of its numerical value. Conversely the network need
not run a universal evaluator to distribute a checked reusable algorithm and
its law: a local agent can adopt its own conformant execution mechanism.

There are accordingly two distinct endpoints:

1. **Warranted method:** return a portable formal implementation and checked
   universal law for it. The present theorem/definition pipeline targets this.
2. **Certified concrete value:** return y for particular inputs together with
   evidence checked under an equal policy. This additionally needs a qualified
   evaluator/evaluation-proof bridge and an accepted concrete associativity
   witness. The earlier public D0->D1->D2 gate does not establish that endpoint.
   The separate [finite-semigroup-02 actual review](../../../experiments/finite-semigroup-02/ACTUAL-REVIEW.md)
   now establishes it for the exact C3/seed1/r31/value2 case, with a genuine
   wrong-value rejection under the same unchanged guest/cap. Its assurance is
   local checked execution over a certified frontier, **not a new transferable
   succinct certificate**. A fresh receiving/return boundary remains separate.

The operation-count theorem is a property of the supplied method and specified
execution strategy. It is not an observed runtime improvement of the current
guest. In particular, the earlier actual Nat->Nat/function-composition instance
is **not** a positive evaluation example: applying the composed function may
still call its opaque original function2^r times. Algebraic composition counts
there describe representation construction, not final function execution.

## Full-cost theorem with an explicit nonempty region

Fix one finite service interval, concrete supported carrier implementation and
the matched assurance policy above. Use a single declared additive cost unit;
CPU time is permissible only when all relevant costs have corresponding CPU
bounds. Network traffic, wall deadlines, memory and money keep independent caps.

Assume:

- Each baseline mul call consumes at least `l>0` units on the selected implementation.
- Each shared SQUARE step, including mul, assignment and loop control, consumes
  at most `u` units on that same implementation. No duplicated delayed evaluation
  is hidden in the arguments; actual operand/output sizes fit the bound.
- K(r) is an upper bound for **all additional reuse-route work** for this selected
  r in this interval:
  initial production/certification when not shared equally; both successful and
  failed authoring/derivation attempts; distribution/installation/adoption;
  actual query/acquisition; premise proofs; definition compilation; proof checking;
  evaluator adoption; result certification if required; return/publication;
  retention, replication, renewal and repair; agent planning; monitoring and all
  remaining differences. Baseline-favorable common costs may be canceled only
  by a justified matched-service argument. No missing component is assigned zero.
- Both routes' remaining resource caps and their exact output relation are met.
  The receipt is genuine, the required formal law applies, and demand for this
  one chosen endpoint actually occurs. No future request distribution is needed.

Then baseline cost is at least `l(2^r-1)` and reuse cost is at most `K(r)+ur`.
Consequently, whenever

`l(2^r-1) > K(r) + ur`,

the reuse route has a strict full-cost advantage of at least their difference.
Proof: substitute the per-call lower and whole-route upper bounds and use the
exact call counts. Ignoring baseline's counter construction is conservative.
One may vary r in an existence argument only with a justified family-wide bound
on K(r). For example, an unbounded mathematical model with K(r)<=C(1+r)^p for
fixed finite C,p,u and l>0 eventually satisfies the inequality. That is not an
established cost bound for this guest or its fixed finite input profile. Within
the actual0..64profile, a uniform funded Kmax can instead be used, but there may
be no admissible r with positive gap. A nonempty **product** operating region
needs at least one explicitly supported r and valid cost bounds at that r;
the pointwise inequality alone supplies no existence proof. The conditional
numerical examples below state exactly such per-instance premises.

Unlike an uninstantiated reuse-frequency inequality, this mechanism exploits a
known exponential-versus-linear cost transformation on a precisely specified
family. It does not rely on guessing how many future agents will reuse a lemma.

### Concrete conditional sensitivity, not invented measurements

For illustration in CPU units, suppose a locally justified implementation bound
is l=1microsecond per baseline multiplication and u=1millisecond per complete
squaring step. This permits a factor1000difference between the lower and upper
primitive bounds. These two bounds are **model premises, not measured product
constants**. Each row below separately assumes its K bounds K(r) at the listed
supported r; it is not extrapolated from a cheaper r. With those premises,
exact sufficient one-use examples are:

| All-in additional cost cap K | r | Baseline lower bound | Reuse upper bound | Guaranteed model gap |
|---|---:|---:|---:|---:|
| 30 s | 25 | 33.554431 s | 30.025 s | 3.529431 s |
| 300 s | 29 | 536.870911 s | 300.029 s | 236.841911 s |
| 3,000 s | 32 | 4,294.967295 s | 3,000.032 s | 1,294.935295 s |
| 100,000 s | 37 | 137,438.953471 s | 100,000.037 s | 37,438.916471 s |

All entries follow by integer call counts and the stated bounds, not by
extrapolating a guest benchmark. Their falsifiable conditions include fixed
bounded operand representations, conformant shared evaluation, affordable
associativity evidence, bounded all-in overhead and actual use at the indicated
r. If multiplication is a cheap projection, the independent agent can choose
a better baseline; the theorem does not create an advantage over that baseline.
If outputs grow exponentially, u may not stay bounded; that row then does not
apply. If the whole-route K is unknown, no rigorous positive decision follows.

The independently measured5.53125s compact receiving cost belongs to a different
fixed function-composition endpoint;2.609375s is the compact installation cost.
They are **representative prior component evidence**, not measured components
or bounds for this future computational route. Do not subtract their sum from
a concrete finite-semigroup K as if that work had been observed. The upcoming
public computational loop will supply its own actual components; it cannot justify
assigning zero to unknown reasoning, evaluator or long-term service costs.

## Why this is an extension of feasible outputs, not extra names

Fix the same assurance endpoint and a budget R. For the declared algorithms,
LEFT can reach only r with `l(2^r-1)<=R` as a necessary condition. SQUARE can
reach every supported r with `K(r)+ur<=R` as a sufficient condition under the model.
Whenever an integer r satisfies

`K(r)+ur <= R < l(2^r-1)`,

the warranted SQUARE method puts that exact computational capability within
budget while this specified independent method cannot. This is a strict
separation of **cost-indexed feasible workflows**. It does not prove a strict
separation from every conceivable local method or create a new theorem in the
foundation's deductive closure. Equal outputs for several r may even coincide.

The novel commons capability is that an independently operated recipient can
obtain the warranted implementation/law without reauthoring its producer's
derivation and can compose a new portable operation from it. A plain theorem
alias would not establish this data-valued construction path. Actual D1 and D2
must be carried and independently checked; their identifiers or the number of
new files alone establish nothing about usefulness.

This resource-relative account is compatible with structural realism, formalism
and constructive practice. It does not assert philosophical constructivism's
logical restrictions or ban classical Lean principles. The theory needed here
is operational: finite agents gain warranted inferential/computational options;
truth is not a popularity contest and optional local value is not universal value.

## Software-actionable adoption rule

An agent needs no global task list. For the endpoint it independently chooses:

1. Obtain the exact available method/law and its assurance policy with a bounded
   search/acquisition allowance; failed work remains in K.
2. Discharge the actual associativity/representation/executor obligations or
   retain them visibly as hypotheses. Do not infer them from a method name.
3. Supply a whole-route upper quote and its resource premises, including chosen
   custody duration/replica count and any required concrete-value certification.
4. Compare with a specified available independent algorithm, including better
   already-known methods. Apply the proved criterion only to valid bounds;
   estimates may drive a clearly labeled heuristic or abstention.
5. Run only within funded limits. Preserve a direct fallback without unbounded
   compulsory search. A cheaper method being available is not a mandate to use it.

The existing rollover advisor covers a narrower seal-versus-retain decision,
not this complete algorithm selector. Do not relabel its cost intervals as
having verified these semantic or evaluator premises. The current public API
and canonical theorem/definition data can expose the inputs to a local agent;
agent research strategy need not become a central-system planner.

## Current closure and strongest remaining blockers

For the **commons warranted-method endpoint**, integrated portability/composability
of the algorithm body and accepted law now has the actual public D0->D1->D2
construction/return and independent final receiving outcome described above.
The earlier final deadline refusal remains a charged failure. Actual output
bodies, genuine checking, return custody and malformed-body rejection distinguish
this from a package archive; general Lean library semantics remain outside it.

The finite-semigroup bridge now genuinely checks the same exact normalized value
that failed its first fixed-cap run, through a smaller evaluation witness. The
second operation costs16.453125 known CPU seconds including its negative; the
first failed9.5625seconds remain charged. Their combined known cost is26.015625s,
excluding earlier source production, installation, public-loop, research and
subsequent custody/receiving. Positive alone costs8.03125inclusive child CPU
seconds. These are observed scoped components, not a complete K bound.

For a stronger **observed net concrete-computation claim**, remaining requirements
are a complete same-assurance K at the actual endpoint and a justified baseline.
The ordinary reciprocal return/receiver path for this new value also remains
separate from its local positive/negative qualification. Do not execute the
exponential reference merely to reproduce its exact static count. Do not call
the C3 reference comparison an improvement on its optimal periodicity method.
The product now supplies a bounded expert proof-producing computation API, not
a general algebra evaluator or broadly qualified Lean/mathlib capability library.

## Stronger counterfactual: the same optimized method without shared certification

The naive-versus-squaring comparison above identifies a useful property of the
method. It does not isolate the commons' contribution. For that question hold
the **same optimized algorithm, exact mathematical result and assurance policy**
fixed on both sides. Also hold the available initial local library fixed.

Consider independently checking consumers who know the optimized implementation
but do not yet possess equally acceptable evidence for a selected law L. In the
specified independent route, consumer i reconstructs or replays a particular
complete proof of L at cost a_i, then uses the optimized method. In the shared
route, one producer certifies L once, funded custodians retain its certificate,
and consumer i acquires/verifies it plus its own demanded interface/local proof
at cost b_i. The methods' common execution cost X_i cancels; different execution
or proof assurance is not a permissible shortcut in this comparison.

Let S be the complete one-time source-proof and certification cost on the shared
route, A all extra distribution/installation/adoption,
M(t) all custody/discovery/renewal/repair over the finite service interval, and
F the complete extra failed-attempt/agent/coordination/other cost. Avoid double
counting any production already included in a_i or b_i. Both routes start from
the same available mathematical and software endowment. If source production is
already present in that endowment, do not charge recreating it on just one side;
if the producer is one of the consumers, do not count its source construction
again in its b_i. The common algorithm execution X_i includes any equally required
instance proof/evaluation on both routes, and cancels only if those costs really
match. Both routes must satisfy the same adopted acceptance policy; the policy
may allow either complete checking or a genuine certificate for the same relation.
If a consumer rejects that certificate policy, it is outside this comparison.
With every changed component assigned exactly once, the route model is

`C_independent = sum_i (X_i + a_i)`,

`C_shared = S + A + M(t) + F + sum_i (X_i + b_i)`.

With justified lower/upper bounds, a sufficient advantage condition is

`sum_i (lower(a_i) - upper(b_i)) > upper(S + A + M(t) + F)`.

For a homogeneous contract with a_i>=a, b_i<=b and a>b, at least
`floor(upper(S+A+M+F)/(a-b))+1`actual consumers suffice. With unknown demand or
unbounded certification/service cost, the comparison remains undecided. Shared
production may be funded cooperatively, but private cost-minimizing agents do
not automatically fund that public benefit. The theorem is about a specified
full-proof route, not a lower bound on every possible independent derivation.

The structural reason this model can have a positive region is stronger than
a guess that a lemma will be popular. Under the certified-cut contract the
selected receiving route has no term for complete ancestral proof bytes/work H:
it pays the selected interface, valid receipt and new proof P. A direct route
that explicitly reads a complete H-byte proof pays at least H bytes of such
reads. Consequently, for sufficiently large selected H and finite certification/
service investment, it can have a positive byte-work region after enough actual
uses. Turning that structural separation into CPU advantage requires actual
bounds for a_i,b_i; byte length is not a CPU conversion factor. The direct
checker still must be able to complete its own selected baseline within its caps.

### What the existing evidence actually instantiates

- The genuine rank0 frontier receipt is223,610B with a192Bjournal. The adopted
  compact receiving path verifies it and performs a complete local proof check;
  it does not download ancestral theorem proofs behind that certified frontier.
  Parent verification was0.03125CPU seconds in the public receiving continuation,
  **nested** inside5.625known total receiving CPU seconds for that exact T2.
- The received T2 packet itself is31,162B and its guest check has55segments,
  27,131,515rows and33,533,271instructions. **T2 is unsealed**: its proof above
  the genuine frontier is still replayed by every fresh consumer. This software
  does not already substitute a T2 receipt for those55segments.
- The observed124.265625known CPU seconds for public construction/exchange plus
  the receiving continuation includes selected negatives, two leases and a
  retained admission failure. It is not S, not a per-use b_i, and not a measured
  cost of certifying T2. The one time frontier's complete producer cost and a
  matched independent full-proof replay cost are not calibrated by these records.
- Existing actual certificates and the checked preparation/advisor boundary
  establish mechanisms for an optional later cut. A fresh T2 seal would need a
  justified whole-route quote, successful proof and funded custody. No expensive
  new seal is selected merely to populate this formula. The recurrent-cut
  argument supplies bounded-replay continuation only under successful funded
  cuts, not a free infinite lifetime for unsealed fragments.

Thus this stronger counterfactual is an actionable conditional **certification
amortization** theorem with current software cost handles, not an observed
same-method research advantage. The primitive receipt-verification timing alone
must never be substituted for b_i.

### A nonempty same-method region without inventing a benchmark

The most useful deployment question is the required independent-warrant cost,
not an unsupported estimate of how clever independent agents are. Put
`G = S + A + M(t) + F`. For n actual matched consumers and a per-consumer shared
upper bound b, the homogeneous threshold is exactly

`a > b + G/n`.

For fixed finite G and a>b this region is nonempty at the finite consumer count
already derived above. This is a theorem about shared warrant production, not
about the particular power algorithm; all optimized execution still cancels.
If independently obtaining the warrant is cheaper than that threshold, do not
claim an economic win. If comparable warrant bytes are already owned, use the
null case below. Demand commitments are a sufficient planning input, not a
global task list or a mathematical acceptance criterion.

The following **conditional budget example** shows exactly what a conservative
evidence-anchored operating decision would require, without claiming that these
bounds have been established:

| Input | Value in this example | Status and required justification |
|---|---:|---|
| Shared receiving plus all marginal service b | <=12 CPU s | More than twice the observed 5.625 s T2 receiving endpoint; acquisition, serving, renewal and any other per-use work must fit the remaining allowance. A timing margin is not a proved bound. |
| Noncertification fixed service allowance | <=512 CPU s | More than four times the recorded 124.265625 s public-loop CPU plus the separate 2.609375 s compact install. These historical scopes are context, not proof of a future whole-route upper bound. All remaining differential setup, failures, planning and finite custody must fit or the allowance is invalid. |
| Complete successful certification S | <=100,000 CPU s | An explicit funded successful-route premise, NOT a measured T2 seal price or an authorization to run a prover. |
| Independent warrant cost a | >=64 CPU s | Must be justified for the named equal-assurance independent route; it is not inferred from the 24.234375 s full receiver or the squaring count. |
| Actual matched consumers n | 2,000 | A conditional finite workload, not observed or forecast demand. |

Under precisely those premises, G<=100,512 and the gap is at least
`2000*(64-12)-100512 = 3,488 CPU s`. The strict break-even count is1,933:
`1932*52=100464` is insufficient and `1933*52=100516` exceeds the fixed cap.
This supplies an explicit nonempty full-cost **model** region with ample
receiving/service margins relative to actual component evidence. It is not a
measured whole-route advantage; no numerical lower bound for a, upper bound for
S, long-term service bound or 2,000-consumer demand has been established. If
any premise is missing, the software must label this as an estimate or abstain.
It must not silently replace the missing premise with a favorable zero.

One need not wait for such a numerical campaign to establish the structural
reason for sharing. For a named route that must read H proof bytes per independent
consumer, let J be each consumer's complete certificate/interface/new-proof
byte-work and K the complete one-time/distribution/custody byte-work. If H>J,
then `n(H-J)>K` gives a strict byte-work advantage. This needs explicit byte-event
definitions and all demanded definition bytes; it is not a CPU theorem. The
certificate protocol's independence from ancestral H is what makes H>J possible.
The actual implementation already has that boundary at its genuine frontier;
the unsealed T2 replay remains inside J until a successful new cut exists.

### Turning savings into continued useful work: a finite-epoch theorem

A saving is not newly created hardware, money or mathematical truth. The
operational consequence is a larger feasible work allocation on the same
participating resources, conditional on who controls and actually reallocates
them. This distinction matters in a decentralized network: one receiver's saved
CPU cannot pay a remote prover unless an owner has committed transferable
funding or computation there. The current software has no automatic market.

For one finite epoch, hold the original consumer capabilities, assurance,
availability and deadline contract fixed. Suppose the named independent route
has lower cost L, the shared route has complete upper cost U, and `Delta=L-U>0`
in an explicitly selected additive resource dimension. Suppose the owner has
reserved budget B>=L, the independent route is itself feasible within B under
all its service caps, and the shared route actually completes within U. Then
at least Delta of the *already provisioned* budget can be allocated beyond
the shared delivery. More directly, any additional owner-chosen
workflows with total upper cost W<=Delta fit together with the shared route
within B, since `U+W<=L<=B`.

The additional workflows must separately fit wall, memory, transfer and custody
constraints and actually produce their declared warranted capabilities; a
CPU inequality alone does not promise their mathematical success. Only
successfully realized relations or reductions of their resource frontier count,
not number of trials, theorem names or syntactic variants. The comparison is
against the named independent workflow, not an unproved lower bound on every
possible algorithm. No premise says a finite agent can solve every new problem.

For repeated epochs e, let Q_e be newly owner-provisioned usable resources and
Z_e unspent, actually controllable reserve. Let O_e fund old custody, renewals,
repair and all other outstanding obligations; let U_e fund current admitted
work including successful cuts; and let W_e fund optional additional work.
A conservative admission invariant in each represented resource is

`O_e + U_e + W_e <= Z_e + Q_e`,

`Z_(e+1) = Z_e + Q_e - actual_epoch_cost >= 0`.

The identity assumes actual costs fit the admitted upper bounds and obligations
are assigned once to their due epochs. Local counters/reservations can enforce
spending limits, not make a promised successful route finish within them. A
failed or late job still consumes its actual charge; it must not reset Z by
opening a new epoch. Each custodian enforces its own invariant; aggregate spare
capacity is not sufficient if a hot key or indispensable prover is overloaded.
Every renewed lease needs an actual provider with capacity and the delivery/
renewal margins in [SCALING-CONTRACT](SCALING-CONTRACT.md).

With bounded repeatable per-epoch obligations, provisioned capacity and successful
capability work, these inequalities have an elementary nonempty stationary
region: choose fixed finite O,U,W and provision Q>O+U+W. The reserve does not
decrease. Sharing makes the admissible W larger by Delta when the equal-service
comparison supplies that gap. This proves a **conditional sustainable allocation
mechanism**, not indefinite mathematics production from a fixed stock of free
resources. Permanent retained bytes still require growing funded storage or
explicitly selective/expiring custody. Renewed CPU-time capacity does not renew
disk space. Nor does the model prove exponential growth: that would require
additional justified assumptions about expanding useful opportunities, resource
supply, successful research and continued access, none supplied here.

### Software consequence: local quotation and funded continuation

The existing `rollover_policy.py` implements the narrow operation-linked part:
same-interface/epoch/service bindings, complete component vectors, budget and
peak caps, bound-versus-estimate separation, unknown-demand abstention and
finite retain-versus-seal comparison. Its output cannot fund a prover, establish
cost premises or change the mathematical checker. Its23focused contracts pass;
do not relabel them as validating this numerical example.

For the current release, expose that advisor beside the discover/acquire/apply/
return API and document the following local rule: use exact already-owned
mathematics first; bound optional discovery; retain old capabilities unless
replacement is explicitly funded; choose a cut only with a valid complete quote
and available capacity; otherwise retain or defer within hard limits. Failed
search/application/certification and renewal charges must remain in the owner's
complete account. The current software has durable transfer reservations and
per-operation charge/result records, **not an automatic cross-operation CPU
reserve allocator or global cost ledger**. The owner must maintain external
accounting/manual reservations across those records to satisfy the repeated-
epoch theorem. An agent may use estimated demand for optional custody/ranking, but
must not promote its estimate into a proof or a network-wide obligation.

A broader same-warrant adoption selector and an automatic multi-owner reserve
allocator are **not implemented** by that advisor. They are not prerequisites
for the present manual/API-controlled mechanism: independent owners can provide
finite quotes and commitments, and the actual workflow enforces its unchanged
caps. Before automatic economic admission is claimed, the corresponding route
bindings, durable charge accounting and reservation authority need their own
implementation. Do not build a global research planner or claim autonomous
self-financing from this local policy. The substantial current software effect
is cheaper trustworthy receiving, bounded source-free reuse, actual acquired
definition construction and a funded optional cut decision at each completed
fragment.

### The decisive local-library null case

If a consumer already has the same optimized algorithm, applicable checked law,
equally acceptable assurance and sufficient local availability, then its a_i can
be ordinary cheap local reuse—not reconstruction/replay from scratch. Against
that strong baseline there is no intrinsic positive commons advantage. The
commons may add acquisition, checking and maintenance cost. Its benefit instead
concerns agents who lack the artifact, portability between incompatible local
contexts, replacing required independent proof replay by a certified cut, or
future contribution/availability, each of which needs its own cost/service scope.

This null case is a feature of an honest growth theory. A commons is not meant
to outperform already-owned perfect knowledge by repeating it. It makes warranted
methods available to more independent agents and lets them build and return
new capabilities without trusting another agent's undocumented success label.
