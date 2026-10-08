# Independent challenge: selective discovery, not merely bounded replies

2026-10-06. Source/theory review by v4_central_reaudit. This is not a new runtime
selection. Existing candidate-discovery-01 has value as a bounded metadata,
pagination, custody and matching boundary, but its Eq-head bucket alone does
not solve rare-lemma discovery in a huge mathematical corpus.

## What sharding does and does not establish

The current conclusion-head/arity signature is computable from a local formal
goal, and exact-type-class representatives prevent renamed offers of one type
from consuming distinct representative rows. Fine shards can reduce provider
and local-page overload. They do not manufacture information about the location
of a rare relevant class. For one relevant class uniformly hidden among S
shards, m distinct shard probes succeed with probability m/S. Increasing S to
fix provider overload can therefore make bounded discovery worse. This is a
central design limitation, not an optional ranking polish.

The earlier good-shard theorem is mathematically correct but places retrieval
and successful use inside the definition of good. Its conditions alone do not
show an operational nonempty regime. The following derives a sufficient regime
from explicit occupancy, replica, page and relevance premises instead.

## Primitive occupancy and recall theorem

Fix a stable interval, one signature, C distinct exact type classes and S=2^b
shards. Assume the following before querying:

1. Each class has between1 and r_max distinct compatible retained holders;
   their advertisements are valid throughout the interval. There are no extra
   incompatible/malicious provider advertisements in this service model.
2. The routing/transport service actually reaches every matching holder when
   the total provider count is at most P. All queried holders complete the
   selected fixed-cut pages, not merely return a hint. Let L=floor(P/r_max).
3. A query can exhaust at least L representatives at each contacted holder
   within its allocated page/byte/time budget. Every selected descriptor fits
   an admissible row; truncation/oversize/expired cursors violate this premise.
4. R of the C classes have a usable representative or a bounded reachable
   alternate satisfying the actual matcher and subsequent checking obligations.
   Relevance is fixed independently of the shard randomness. This is a semantic
   workload premise, not a score or an observed network statistic.
5. Distinct class shard assignments are independent uniform draws. This is an
   explicit fixed-input hash/randomness model for honest classes, not a theorem
   from deterministic SHA-256 or a defense against adaptive adversarial grinding.
   The requester samples m distinct shards independently and uniformly.

If each shard has at most L classes, it has at most r_max L<=P holders: the
sum counts duplicate holders more than once, so it is a conservative bound.
Each holder has at most L representatives in that shard. Thus premises2-3
remove provider/page cap loss on this no-overload event.

For C_s classes in a particular shard, C_s has distribution Binomial(C,1/S).
By a union bound, overload probability is at most

`epsilon_load = min(1, S * Pr[Binomial(C,1/S) > L])`.

For any independently selected m-shard set, each relevant class misses it with
probability1-m/S, independently across classes. Consequently

`Pr[no relevant class in sampled shards] = (1-m/S)^R <= exp(-mR/S)`.

Under the stated service conditions the total failure probability is therefore
at most `epsilon_load + (1-m/S)^R` (capped at1). Additional separately bounded
service-failure probabilities may be added by union bound; they need not be
independent. This argument does not assume independent good-shard events or
mistake a hash function for an observed random workload.

A nonempty illustrative model: P=8,r_max=1,L=8,C=128,S=256,R=64,m=32.
Using `Pr[X>=9] <= choose(128,9)/256^9 <= (e*0.5/9)^9`, the overload contribution
is below0.000011. The relevance miss term is `(7/8)^64<0.000195`, so the total
is below0.000206 before service failures. This is explicitly a dense-relevance
model, not measured corpus coverage. For R=1 the rare-class obstruction remains.
Four discrete partition levels also give only a finite, quantized envelope.

## Minimal consequential refinement: rigid goal anchors with wildcard coverage

Use a new optional search-feature version, not a change to mathematical identity
or acceptance. A theorem conclusion is a first-order syntax pattern after the
supported outer telescope is removed; its telescope variables may be substituted.
Applications are binary constructors with edges f (function) and a (argument).
No reduction, rewriting, higher-order instantiation or binder-crossing matching
is silently included in this contract.

Choose one public, finite, prefix-closed position set P in advance, for example
application paths of length at most d. Only inspect paths traversing application
nodes; do not enter local lambda/Pi binders in this initial fragment. At offer
time, materialize for each reachable p in P:

- `Exact(p,c)` if the node is a rigid constant with exact adopted identity c;
- `Wild(p)` if the node is a substitutable outer-telescope variable.

Other nodes need no posting for this constant-anchor filter. Full descriptors
remain available for the existing advisory matcher. Query g derives an anchor
(p,c) solely from a constant occurring at its own supported position p; it need
not know a lemma name, identifier, type, answer or usefulness score. Its candidate
superset is the union

`U(p,c) = Exact(p,c) union union_{q prefix-of p} Wild(q)`.

**No feature false-negative lemma.** If a supported pattern t has a syntactic
first-order substitution sigma with sigma(t)=g, then t belongs to U(p,c).
Proof: follow p from t's root. If a telescope variable is met first at prefix q,
t has Wild(q). Otherwise all traversed constructors are preserved by substitution;
the node at p must be the same rigid constant c and t has Exact(p,c). A rigid
different constructor/constant cannot become c by this matching relation.

This includes applied telescope variables without the unsafe rule that their
raw argument tags must match the goal. If a variable in function position is
encountered, its wildcard prefix covers the entire affected goal subtree.
Beta/delta conversion and general higher-order matches lie outside the lemma;
they must retain explicit UNRESOLVED/fallback handling, not claim NO_MATCH.

For several goal anchors, every syntactic match belongs to their intersection
`intersection_j U(p_j,c_j)`. The minimum implementation need not do a distributed
join: choose one anchor union as the routing seed, then check all chosen anchors
and the existing matcher locally on received descriptors. Choosing the seed by
local statistics or a bounded probe is an efficiency heuristic, not proof of
recall or authority to accept a theorem.

### Coverage and resource contract

Keep rigid and wildcard postings as distinct streams. A requester may prioritize
the selective rigid stream and report its exact scope, but must not claim full
pattern recall if it omits, truncates or fails a wildcard stream. In particular,
a generic theorem whose conclusion is a telescope variable can be in a huge
Wild(root) stream. No structural indexing scheme makes such unconstrained
patterns selective. Generic local-library fallback, additional premise/type
features or heuristic ranking may help but require their own stated scopes.

Materialize representatives per feature and type class, not per theorem name.
Apply the existing bounded alternate-member policy, fixed-cut MAC cursors,
provider/shard caps, descriptor rederivation after custody, and final independent
checking unchanged. Advertise at most4|P| routes per represented class across
four partition levels, before holder-local deduplication (plus any separately
retained broad fallback routes). Querying one anchor requires at most|p|+2
posting streams: one exact plus at most|p|+1 wildcard prefixes. Count all their
probes, pages, matches, bytes, renewals and stored posting rows. Finite P bounds
publication work, not the number of classes in a generic posting.

The advertised feature set must cover every position promised by its namespace.
Silent per-object feature truncation invalidates the lemma. Refuse that optional
search profile, use a coarser declared profile, or expose a distinct coverage
status instead. It must never turn feature ineligibility into mathematical
rejection. Materializing bounded DAG paths must also have a traversal-work cap:
a compact shared DAG can denote many tree paths, but fixed P bounds the visits.

### Why this can improve the actual huge-network problem

Replace global Eq-class population C by the selected anchor-union population
C_a, and relevant classes R by those covered under the above exact theorem.
Primitive occupancy/recall now depends on C_a rather than every Eq theorem.
If unrelated mathematics grows without adding the selected rigid symbol/path
or relevant wildcard prefixes, neither C_a nor the required local pages grows.
This is a precise conditional locality property; it is stronger than assuming
a globally dense relevant Eq bucket and weaker than universal complete search.

Constants such as acquired operation/interface identities can discriminate
mathematical structures, while ubiquitous Eq/Nat constants may remain poor
anchors. A selected smallest-posting estimate is useful but untrusted. A malicious
provider may waste bounded search work, never contribute false accepted mathematics;
adversarial availability/selectivity needs a separate spam/admission model.

The decisive fresh test, if selected, should hold an independently authored
formal goal fixed, add many distinct nonmatching Eq types outside its anchor
streams, preserve a generic-variable positive control, and require acquisition
plus genuine checked application. It should also force wildcard truncation and
show honest incomplete coverage. Repeating broad-head pagination alone would
not test this refinement's central consequence.

## Disposition

### Concrete smallest profile under the current advertisement caps

Root's current finite service caps favor at most8 features per class rather than
all raw paths to depth d. Use the following generic instance of the same necessary
condition idea. After the supported telescope is removed, write the terminal
constant-headed conclusion as `H a_0 ... a_(n-1)`, with n<=8, using the existing
head/arity parser. The feature positions are exactly the outer argument indices
0..n-1, not positions tuned to the test theorem. For each argument follow its
left application spine, without entering binders:

- rigid head constant c yields `ArgHead(i,c)`;
- substitutable telescope-variable head yields `ArgWild(i)`;
- any other head shape is explicitly unsupported/unresolved for this anchor.

Publish at most one feature per argument. For a goal argument with rigid head c,
query `ArgHead(i,c) union ArgWild(i)`. This is a two-stream plan computed from the
local goal alone. If a supported first-order pattern matches the goal, the
pattern's argument at i either has the same rigid head c or a variable head:
following function edges either preserves the first rigid constant or reaches
a variable whose substitution may add application structure. Hence the two
streams retain every syntactic match in this profile. A variable used as a
function is covered, not incorrectly compared to a rigid goal head.

This does not traverse lambda/Pi bodies, normalize beta/delta redexes, or promise
all Lean-applicable lemmas. Such cases need the explicitly incomplete broad
fallback. Constant universes may be ignored by this coarse necessary-condition
filter, leaving actual universe/typing obligations to the existing matcher and
checker. The feature key must also bind the base conclusion signature and new
feature namespace so argument positions from different heads/arities do not mix.

For Eq, the three positions are carrier type, left side and right side; operation
heads in the latter two often distinguish unrelated mathematical structures.
The same schema works for any supported constant-headed predicate, with no theorem
identifier or semantic-domain enumeration. A highly generic variable head still
produces a large wildcard stream; that limitation remains visible.

With selected levels0 and8, there are at most16 feature routes plus2 separately
retained broad routes per class before local deduplication, compatible with a
finite128-per-publish request by grouping ordinary owner calls. Total persistent
advertisement/renewal quotas remain charged: an object-local bound is not a
promise that arbitrary many classes fit the node's4096 advertised-key budget.
Index each class/descriptor once; add materialized feature-to-class posting rows,
not duplicate theorem data. The existing base class signature must remain stable;
feature routes are additional search signatures, not changed mathematical types.

Candidate-discovery-01 is a useful initial transport/index boundary, not the end
of scalable applicable-lemma search. Root should retain its small integrated
query-to-use gate as interoperability evidence, then select this bounded
goal-derived filtering seam only if its publication budget and supported-pattern
coverage fit the intended deployment. No new implementation or launch is made
by this review. No global agenda, human intention or political identity enters
mathematical acceptance.
