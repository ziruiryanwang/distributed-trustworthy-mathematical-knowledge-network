# Equality-aware conclusion fingerprints: sound in principle, payoff unproved

2026-10-26 America/Chicago. Author: `pattern_retrieval_options`.
Root-requested source/theory follow-up to `INSTANCE-GAP.md` and
`PATTERN-OPTIONS.md`. Only this checkpoint is changed. No implementation,
import, test, native operation, state opening, external call or Git mutation.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Decision and necessary refinement

The proposed correlation filter has a valid no-false-negative **key coverage**
argument for the stated raw capture-avoiding substitution relation. Restricting
paths to `fn` and `arg` makes sampled positions share one outer binder context;
repeated source parameters must therefore instantiate to exactly equal query
subterms. It removes the reflexivity/commutativity obstruction that independent
STAR observations cannot remove.

This is a defensible **candidate for a bounded source contract**, not yet a
decision that a new provider profile is worth implementing. The existing exact
generalization solves the supplied example; Lean/Loogle remain strong alternatives.
No real-workload advantage or useful-growth result follows from this fabricated
separating family.

Three details are required for the argument and its selectivity:

1. Each source emits **one exact maximal correlation relation**, together with
   its token vector. Do not additionally emit weakened/empty relations for that
   same source. The query's empty-relation alternative matches sources whose
   recorded relation is exactly empty; it does not mean "ignore correlations."
2. Every member of a nontrivial source equality block must have token STAR.
   Enforce that during query generation too. This reduces the crude 40-key
   bound to **15 keys** for three positions, before further query restrictions.
3. Query equivalence must compare endpoint **expressions**, not DAG node numbers,
   pretty-printed strings, low-detail observation tokens, or expression heads.
   Shared nodes and differently shared but equal terms must behave identically.

No full matcher, new tree protocol, imported proof inspection or reduction engine
is necessary to define this filter.

## Objects and normalization boundary

Use the existing validated ordinary type DAG and exact portable constant
bindings. Select one immutable profile with d distinct canonically ordered paths,
`1 <= d <= 3`, each length at most 12 and containing only `fn` or `arg`.
The empty path is permitted. These edges exist only at application nodes.

For a source `forall Delta, t`, strip the complete leading forall telescope;
let k be its length. For a query wrapper `forall Gamma, g`, validate the complete
wrapper and strip exactly its explicit context count. Both operations retain
existing syntax, scope, byte and DAG bounds. No caller-supplied relation can
replace derivation from the exact source preview.

The old source token observer is retained: a stripped parameter gives STAR
before traversing any remaining path; a missing edge at a rigid node gives
ABSENT; an endpoint otherwise gives its exact portable constant token or node
tag. Universe arguments, literal values and the old omitted fields remain absent
from these coarse tokens. No beta/delta/iota/zeta/eta reduction is performed.

Because only application edges are followed, every reached position is at
internal binder depth zero. Reaching a lambda, forall or let with further edges
gives ABSENT; their bodies are never entered. Such expressions can still occur
as complete endpoints or inside complete endpoint subterms.

For endpoint equality use one fixed **syntactic** quotient: ignore binder display
labels and universe-parameter display labels, but preserve ordered universe
positions, all actual level expressions, exact portable constant identities,
bound-variable indices, constructors, binder annotations, let flags, literals,
projection structure/field metadata and children. This is the existing exact
type-key discipline applied to subexpressions inside one query, not Lean
definitional equality. The entire query's common universe/context interpretation
is fixed before comparing endpoints.

The strongest easy coverage premise is exact raw-tree equality after uniform
term/universe substitution. The chosen harmless display-label quotient can be
applied to both sides. Do not broaden the premise to arbitrary semantic equality
or to equality merely after erasing universe expressions: the endpoint relation
is deliberately stronger than the coarse observation tokens.

## Source relation: repeated parameters, not arbitrary repeated STAR

For each path i record, in addition to its old observation, whether traversal
**ends exactly** at stripped parameter `bvar a`, with no path edge remaining.
Call this optional value `endpoint_parameter[i] = a`. An early encounter with a
parameter still produces STAR but has no endpoint parameter annotation. A rigid
missing edge has no endpoint either.

For each parameter a, collect all positions ending at that parameter. Retain only
blocks of cardinality at least two. Sort indices in each block and sort blocks
canonically. These disjoint blocks form R_t, the source's nontrivial equality
partition. Singleton parameter occurrences impose no equality condition.

The combined source key commits to the exact profile, old observation vector V_t
and this exact R_t. Its partition refers to **profile position numbers**, not
source parameter indices; changing an unused telescope binder therefore does not
change the relation. Exactly one combined key is derived per source.

Do not record all STAR positions as equal. In particular, reaching source x before
the end of `arg/fn` does not say what the query's final `fn` subterm will be. Even
two paths descending into one substituted x can select different subterms. The
endpoint restriction is essential to this simple argument.

## Query relation and key enumeration

Traverse each path in g without wildcard stopping. Retain its endpoint DAG index
if every requested edge exists. Missing endpoints do not participate in equality
blocks. Coarse observations use the old rules: final Gamma variables force STAR;
a missing child below such a rigid variable is ABSENT.

Let E_g be exact syntactic equality among available endpoint subterms in the
fixed common query context. Generate candidate relations R whose disjoint
nontrivial blocks are subsets of E_g equivalence classes. This means every pair
inside a block is equal; it does **not** require R to equal E_g. The same query
term may instantiate several distinct source parameters, so strict refinements,
including the empty relation, must remain available.

For each such R:

- force STAR at all positions in its nontrivial blocks;
- force STAR at final Gamma-variable observations as before;
- enumerate keep/STAR for all other coordinates;
- emit only canonical, deduplicated combined keys under that exact R.

Never place these alternative keys together in an AND query. Each alternative
is a separately selected/funded query, or part of a separately specified bounded
union operation if one is later selected. No union protocol is required here.

The empty relation is a genuine exact key component. If sources with nonempty
R_t are also indexed under the old relation-free fingerprint and a search falls
back to that lane, those sources can return again. Such an explicit broader
fallback may be useful, but it forfeits this filter's rejection guarantee and
must be reported separately. It must not be hidden inside "empty relation."

## Coverage theorem and proof

Assume:

- the source type and closed query wrapper satisfy the supported format/bounds;
- paths/profile and rigid portable identities agree;
- sigma simultaneously substitutes the source telescope's parameters by terms
  scoped in Gamma, with capture avoidance and one consistent universe substitution;
- g is sigma(t) as raw syntax, up to the fixed display-label quotient.

Then the query's generated key family contains the source combined key.

**Token component.** The previously reviewed STAR-or-equality lemma applies.
A source path that encounters a substituted parameter is STAR. Any path avoiding
parameters has unchanged rigid syntax and child existence. The query's final
Gamma-variable case necessarily came from a source STAR. Restricting to fn/arg
does not invalidate these earlier cases.

**Relation component.** If positions i and j lie in one source block, both
source paths end exactly at the same parameter a. No path enters a binder.
Capture-avoiding substitution therefore places the same sigma(a), with the same
zero surrounding internal shift, at both query positions. Both query endpoints
exist and are equal under the selected endpoint quotient. Thus every source block
is contained in an E_g class, so R_t is among the enumerated relations.

**Combination.** Every position of R_t already has source token STAR. Forcing
STAR there cannot remove V_t. At every other position, the old keep/STAR family
contains the required source token. Hence the combined (V_t,R_t) key occurs.

This proves key inclusion only. Actual retrieval still requires correct source
indexing, selected reachable providers/snapshots, enough allowance for the relevant
alternatives/partitions/pages, and nonomission by the provider. Membership proofs
for returned records do not prove these premises. Truth and actual applicability
still require exact acquisition, ordinary admission, correctly typed arguments
and discharged proof/typeclass premises.

## Difficult cases resolved by the restriction

- **Binders inside substituted terms:** sigma(a) may contain lambdas, foralls or
  lets. Both copies have identical internal scope and the same surrounding Gamma;
  exact endpoint comparison includes their bodies without interpreting them.
  No source path crosses those binders, so different external shifts do not arise.
- **Repeated DAG nodes:** equal node IDs suffice within a validated immutable DAG,
  but different IDs do not imply unequal syntax. Endpoint canonicalization must
  identify structurally equal sub-DAGs despite different sharing/numbering.
- **Universe instantiation:** repeated occurrences of one term parameter receive
  the same substituted term, including all its levels. Omitting universe levels
  in coarse tokens is harmless; treating unequal instantiated levels as equal in
  the endpoint test would only add false positives, not establish applicability.
- **Raw beta redexes:** replacing f by a lambda leaves its application raw. A
  separately reduced query can miss; neither the old token lemma nor this new
  relation claims reduction closure.
- **Partial paths:** an early source STAR never gains a correlation annotation.
  An absent query endpoint cannot occur at the counterpart of a direct endpoint
  parameter under the coverage premises. Excluding absent endpoints from R is safe.
- **Typed but syntactically unequal subterms:** definitional equality, proof
  irrelevance or local hypotheses may make them interchangeable in Lean. This
  index can exclude such matches; they are outside the stated raw-instance relation.
- **More source equality than query equality:** an incompatible repeated parameter
  block cannot arise under uniform raw substitution. This is precisely a safe
  rejection for the supported relation, not proof of global nonapplicability.

Extending paths to binder bodies would require endpoint comparisons modulo
scope shifts/context correspondence, or a more conservative relation. The
present proof is not authority to make that extension silently.

## Separating the supplied family, with correct path numbering

Write the conclusion as the explicit curried expression
`Eq A (op x y) (op y x)`. Consider semantic positions:

| Position | Raw expression-child path | Commutativity endpoint | Reflexivity endpoint | Query endpoint |
|---|---|---|---|---|
| alpha: left operand's first argument | fn/arg/fn/arg | x | x | f a |
| beta: left operand's second argument | fn/arg/arg | y | y | g b |
| gamma: right operand's first argument | arg/fn/arg | y | x | g b |

Assume `f a` and `g b` are syntactically unequal. All source coarse tokens are
STAR. Commutativity has block {beta,gamma}; reflexivity has {alpha,gamma}.
The query E_g contains the former but not the latter. Therefore the commutativity
key is generated and the reflexivity key is not, for every supported number of
unused leading binders in the distractors.

The conceptual order (alpha,beta,gamma) gives blocks {1,2} and {0,2}.
Canonical compact-JSON path sorting actually orders (gamma,beta,alpha), producing
blocks {0,1} and {0,2}. A future contract must use the latter indexing if it retains
the existing canonical-order rule. The proof is invariant to the renumbering.

The empty-relation query does not return the correlated reflexivity source,
because that source has only its exact nonempty combined key. Hash collisions
are excluded under the existing identity assumptions. This proves discrimination
of this family, not usefulness of the remaining candidates or cheap whole search.

## Costs, fanout and sustainable benefit

For d=3 the possible partitions are: empty relation, three single-pair relations,
and one triple relation. With block positions forced STAR, their maximum numbers
of token masks are respectively `8`, `2+2+2`, and `1`: **15 keys** total. For d=2
the maximum is 5; for d=1 it is 2. Missing endpoints, unequal endpoints and final
Gamma variables reduce these counts. At most three endpoint-equality comparisons
are relevant; their subterm sizes are not necessarily small.

Source observation still reads k telescope entries plus at most `d*(L+1)` path
positions after complete input validation. It additionally groups at most three
small endpoint parameter indices and emits one combined posting. No source proof,
dependency history or normalization is traversed.

Query exact endpoint equality adds real work. Reuse the existing bottom-up
structural-key normalization rather than expanding sub-DAGs. One DAG pass can
compute bounded normalized class keys/digests for levels and expressions, retaining
O(N) per-node results and charging all encoded fields/bytes. If hashes are used
as equality, state the collision assumption; a collision can merge unequal classes
and add false positives. Exact collision-resolving structural interning/comparison
is another implementation choice, whose dictionary/comparison costs need explicit
bounds. Do not claim constant comparison work or a hard linear-time CPU guarantee
from having only three sampled endpoints. A bounded comparison that cannot decide
equality must conservatively allow the relation, or mark coverage incomplete;
treating UNKNOWN as unequal can create false negatives.

Every emitted alternative multiplies selected provider/partition/service overhead.
Fewer returned candidates may still cost more because up to 15 key searches replace
one broad query. Aggregate allowance, failed-search charges and explicit skipped
alternatives remain necessary. Sparse ordinary access paths and routing costs are
unchanged. Large empty-relation or all-STAR cohorts remain possible. A one-key
source record does not imply small buckets or sublinear semantic search.

Let J be incremental construction, reindexing and deployment cost; M_Q maintenance
and holding cost over Q queries; and F(q) the **entire** correlation-assisted query
cost, including query canonicalization, all attempts, transport, previews and actual
application. Let O(q) be the best *available and actually supported* alternative
among generalized exact-type queries, coarse selective search, approved local
Lean/Loogle, or direct local proof, including its own setup/maintenance allocation.
A useful region requires

`sum_q (O(q) - F(q)) > J + M_Q`.

An illustrative sufficient condition is positive average saving delta per query
and `Q*delta > J+M_Q`. This is a conditional amortization argument, not measured
evidence. It cannot assign delta from candidate counts alone. Both methods have
the same library, caches, affordable local reasoning and honest source-approval
options; do not disable generalization or Loogle to manufacture a win. Equivalent
ordinary library services can use the same filter, so this is not a proof of a
decentralization-specific advantage.

The supplied commutativity goal admits a simple exact generalization, already
supported publicly, which may be cheaper. Correlation could be more helpful where
a caller knows the desired conclusion but not the remote telescope/premise order,
and relevant portable previews already exist while importing a whole executable
project or using a suitable external search provider is unavailable or costly.
Those are workflow assumptions needing evidence, not established user behavior.
Correlation does not make unknown premises easy to satisfy.

## Falsifiers and next decision

The key-coverage proposal fails if a supported raw instance has a source equality
block not represented among query alternatives, particularly via incorrect binder
scope, early STAR grouping, node-ID comparison or omitted refinement partitions.
Its claimed discriminator fails if correlated sources are indexed through an
empty-relation alias, or if the ordinary service queries only the old token key.

Before code, root should select a fixed profile and an actual supported portable
workflow that survives exact generalization and Lean/Loogle comparison. If such
a workflow is absent, retain this theorem as a feasible option and **do not**
implement it merely because it now distinguishes an artificial family. A very
small source/codec integration can later test changed-boundary mechanics; no
native build, large corpus or repeated transport campaign is needed to decide
the theorem or fabricate positive economics.

Conceptually this is equality-aware path/fingerprint indexing: ordinary term
matching has always required consistent substitutions for repeated variables,
and discrimination/substitution indexes exploit related constraints. The earlier
Schulz/Lean references support that general lineage. No novelty claim or exact
literature priority for this small combined-key encoding is made; no additional
primary source was fetched in this bounded assignment.
