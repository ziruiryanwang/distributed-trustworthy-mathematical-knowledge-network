# Growth operating region: affordable reuse under finite service capacity

Source/theory only, 2026-10-20; no execution/code/Git. Extends GROWTH-WORKLOAD
and SELECTIVE-CERTIFICATION-POLICY with a demand interval, not a new calculator.

## Immediate decision and honest comparator

Keep the generic evaluator method M native-first. Its independent applications
already have a fixed two-native-node tail above BASE. The equally optimized
ordinary shared-library baseline may use M, identical indexes, representations,
caches and local optimizations. Against that route, native-first sharing itself
has zero incremental per-use saving: more users cannot manufacture a gain.
This does NOT imply zero certificate-versus-native saving: certifying M removes
one uncached native node and its proof transfer. That distinct margin is not
established to repay its 154-call production graph. The measured native check
is 0.03125 Job CPU seconds; no new M certificate has been produced.

Compare the same useful mathematical outcomes, not a particular inefficient
proof encoding. Let the ordinary comparator choose among its supported proof
routes, generic methods and caches. A new shorter proof or preaccepted library
can erase any proposed margin. If it already has the same certified route,
there is no claimed strict v5 advantage. We do not lower-bound ideal proof search.

## A finite deterministic operating-region theorem

Fix one supported policy/image and an available exact certified cut for horizon
T. The cut must cover every ancestral path claimed omitted; demanded semantics
remain charged. Fix nonnegative prices for additive physical resources; one
cost unit is this priced sum, not an unweighted mixture of CPU/bytes/duration.
Peak memory is a feasibility constraint, never an additive price by itself.
Both routes obtain identical final outcomes; failed network attempts fall back
to the same ordinary route, with all unsuccessful work charged. Assume:

- N opportunities occur in T; N >= lambda*T-sigma. In every interval of length
  t, admitted opportunities are <= sigma+lambda*t. Lambda has units uses/time,
  sigma uses. This is a deterministic traffic contract, not mean demand.
- At least alpha*N opportunities actually yield eligible warranted reuse,
  0 < alpha <= 1. Eligible means an otherwise uncached saving after the same
  baseline optimizations; warm hits cannot be relabeled cold. Their ordinary
  route costs at least d more than the successful selected route, in cost/use.
- Extra discovery, unsuccessful candidates, fallback overhead and other
  per-opportunity costs are <= q cost/use, including provider work. Components
  already included in d are not counted again. Shared baseline costs cancel.
- F bounds incremental creation/certification/publication/adoption and failed
  production cost. h*T bounds ongoing incremental custody/index/repair/service
  and retirement cost, h in cost/time, for this horizon. No unpaid perpetual
  retention, zero-cost replicas, independent-failure or free subsidy assumption.
- For every actual service queue j, work arrival in any interval t is bounded
  by B_j+(lambda*u_j+r_j)*t, where B_j=sigma*u_j+b_j. Here u_j is worst-case
  work/use, r_j maintenance/repair work/time, b_j its burst, and a dedicated
  work-conserving FIFO server supplies C_j work/time. Include failed requests
  and all routes in these queue-local bounds; a network-wide average is not one.

Set g=alpha*d-q and Lambda=min_j((C_j-r_j)/u_j), for u_j>0; queues with u_j=0
must have r_j<C_j. For this preselected supported horizon T, require

    g > 0,  Lambda*g > h + (F + sigma*g)/T,
    (h + (F + sigma*g)/T)/g < lambda < Lambda.

Then the selected route has strictly lower full priced cost for this workload:
`D >= N*g-F-h*T >= T*(lambda*g-h)-F-sigma*g > 0`.
Proof: each eligible reuse saves >=d; subtract all opportunity, fixed and
ongoing costs. For each queue, its arrival curve has rate below C_j; the maximum
vertical excess over C_j*t is B_j, so backlog is <=B_j from an empty start.
This is a deterministic per-queue bound; it is not an unproved end-to-end SLA.
The stated open interval is nonempty; its midpoint is a witness. We cannot make
T arbitrarily large beyond supported policy/retention life to force payback.
If g<=0 or Lambda*g<=h, no horizon supplies this positive guarantee; for finite
T the stronger displayed condition is necessary for this sufficient interval.

Standing retention sets a lower useful arrival rate; sustainable service sets
an upper rate. Capacity-infeasible payback volume is rejected. These are bounds
for specified algorithms, not observed demand or universal mathematical growth.

## Mapping and smallest software consequence

Current `RuntimeProfile`/workspace grants and acquisition budgets enforce finite
work; `serve_workspace` caps lifetime/connections/requests/replies. These are
useful enforcement hooks, NOT evidence for alpha, successful proof latency or
the above traffic/service contracts. `publish/reconcile` and semantic custody
already circulate native M. Quota-bounded custody is not a funded retention SLA.
General exact-J seal preparation already exists: do not implement it again.
I/A producers, exact-cut imports and withdrawable owners supply mechanisms,
not an already economical successful seal supply.

The missing source seam identified by core_search is bounded, authenticated
materialized conjunction postings. Current rare-anchor scanning costs
`A=sum_(provider,partition) min_f |P_f|`; a selected conjunction can instead scan
`B=sum_(provider,partition) |intersection_f P_f| <= A`. Small intersection alone
does not make A small. Template/schema binding, complete snapshot construction,
explicit fallback, index build/update/storage caps and costs are prerequisites.
This can improve q, u_j and alpha under fixed scan budgets for BOTH comparators;
do not credit the same improvement only to v5 or materialize all subsets.
Root should select this narrow source contract once current-schema absence is
confirmed, not a new economics ledger or another M proof/reciprocal demonstration.

Falsifiers: no positive cold margin; hot-key recall drives alpha to zero; changed
cache/derivation erases d; maintenance violates h/r/b; correlated loss removes
needed semantics; queues lack the promised service; or withdrawal shortens T.
Caps and failed charges remain real when these assumptions fail. Current M,
interface byte savings and completed capsules establish none of those bounds.
The existing growth definition remains warranted resource-bounded capability,
not theorem counts, human intention, global tasks or inevitable exponential gain.
