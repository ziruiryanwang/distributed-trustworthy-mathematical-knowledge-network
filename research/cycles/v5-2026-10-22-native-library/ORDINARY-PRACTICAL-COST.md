# Ordinary commons: whole costs, scale limits, and the next consequential change

2026-10-23. Source/theory audit by `portable_integration_audit`.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
No tests, builds, Python execution, network operation, store mutation or Git
operation was performed for this cost audit. The active A/B integration and
its outcome reviews belong to other owners. This note does not predeclare them
successful.

## Decision

**Executed discriminator, 2026-10-23:** the independently audited
[body-search check](ORDINARY-BODY-DISCOVERY-OUTCOME.md) examines three postings
across both stages versus eight under the exact predecessor query. Both false
candidate branches count. Search replies nevertheless total 202,790 bytes versus
103,356; the extra body index and evidence acquisition are additional costs.
This supports an optional vocabulary-discovery route, not a default planner or
an overall speedup. Its use is justified only when avoided candidate handling
outweighs extra query, transfer, extraction and amortized maintenance costs under
the caller's resource prices. The check does not instantiate that inequality.
Preserve this result and move to generic contribution; do not optimize its
serialization simply to manufacture a headline win on the fixture.

**Subsequent narrowing, same day:** root and independent review preferred the
[two-stage body-fingerprint design](ORDINARY-APPLICABILITY-DESIGN.md): discover
a vocabulary from an actual local property's raw definition-body pattern, then
search its learned exact symbol. It reuses existing path/STAR machinery and
needs no reducer. The broader bounded-unfolding proposal below remains the
original cost analysis, not implementation authority. All cold/local/search
cost limits and the full-cost growth condition remain applicable.

Finish the ordinary public acquire–check–use–contribute cycle before adding
another mechanism. After that, the highest expected marginal payoff is **one
bounded, vocabulary-independent applicability/type-view profile for the existing
specialist discovery indexes**. Its purpose is to find an unfamiliar abstraction
from its formal structure when the consumer does not already know that
abstraction's identifier. It is not a new mathematical authority, universal
equivalence test, global task allocator or mandatory learned model.

The concrete current weakness is stronger than missing pagination: the small
Stable-method query can select a fixed fraction of all polymorphic theorems.
More peers, partitions or copies of that same broad index do not repair its
selectivity. Existing conjunction postings should be reused where appropriate,
not invented again, but a conjunction whose intersection is huge remains huge.

Local context costs are a second real limitation. They are recorded below so
that “no old proof replay” is not mistaken for constant-cost reuse. However,
implementing a resident checker first would change the protected admission-event
boundary while leaving unfamiliar-method discovery unresolved. Bounded project
contexts and existing multi-unit batches are the simpler immediate operating
choice. This ordering is a marginal-payoff judgment, not a measured universal
ranking of optimizations.

## What is being scaled?

Distinguish four quantities:

| Quantity | Meaning | Who needs it? |
|---|---|---|
| `N` | Total independently published mathematics across the network | No ordinary client must enumerate it. |
| `K` | One chosen locally warranted context | Current native extension loads this context. |
| `D` | Missing evidence closure for a selected acquisition, stopped at this owner's accepted frontier | A cold ordinary receiver must acquire/check it. |
| `S(q)` | Posting population actually examined for a selected formal query and provider set | Discovery pays this even if few results are returned. |

A network can be huge while each participant maintains several bounded project
contexts. Conversely, a single ever-growing local branch can become expensive
even when the public network is small. No result about `K` or one tiny fixture
establishes a bound in `N`.

The current catalog permits selecting earlier roots as parents; it does not
require one global or even one owner-wide head. Each chosen root nevertheless
has a one-parent lineage. Arbitrary branch merging and demand-minimal semantic
module DAGs are not supplied by that fact.

## Cold learning: pay for the missing warrant, not for the entire network

Let `A` be the exact locally accepted units under the current semantic,
foundation and checking policy. For requested exports `X`, define `D(X,A)` as
the supported dependency closure reached before encountering warranted units
in `A`. Generated declaration groups are indivisible units. Dependencies
needed by types, definition bodies, recursors and proofs must be included
according to the actual admission relation, not a name-only approximation.

An ordinary cold receiver cannot replace this closure by another peer's
“accepted” flag, signed statement or snapshot hash. It needs the missing
checked evidence, an independently supported succinct warrant, a different
checked derivation, or an explicitly different trust policy. The adopted
[architecture reaudit](../v5-2026-10-22-architecture-reaudit/ARCHITECTURE-REAUDIT.md)
therefore makes bounded initial learning followed by durable incremental reuse
the normal route. This is an explicit practical compromise to the earlier
blanket cold no-ancestry demand, not a proof that cold ancestry disappeared.

A useful accounting decomposition for one operation is:

```text
C = C_search(q) + C_locate(D) + C_transfer(D) + C_parse(D)
    + C_context(K) + C_check(D | K) + C_commit(D) + C_author_use.
```

These terms count the actual selected receiver/provider work; they are not
claims that every implementation term is independent or additive in wall time.
Use an additive resource vector, or fixed nonnegative prices, for sums. Peak
memory and deadlines remain separate feasibility constraints. Acquisition is
output-sensitive: it cannot cost less than delivering and reading the selected
uncached evidence bytes in this explicit-evidence route. There is no universal
small upper bound for `|D|`, or for dependent-type conversion/checking time as a
function of the number of declarations.

Within one unchanged policy epoch, with retained acceptance and a memoized
dependency traversal, each distinct missing unit need be checked at most once
per owner. For acquisitions `D_1,...,D_m`, the ideal new-check work is charged
to their newly required union, not the sum of repeated ancestor occurrences.
This bound assumes no eviction, withdrawal, incompatible rebinding, policy
change or corruption. Such events create genuine new costs. It does not erase
current repeated parsing or context reconstruction.

The new signature-only owner-authoring seam is narrower still. A missing
singleton theorem already warranted locally can be made available in a fresh
scratch authoring environment through its exact signature without fetching
proof-only ancestors. A transparent definition still needs the semantics used
in construction/conversion. Scratch placeholders are not accepted mathematics;
the exported new contribution still passes the exact binder and ordinary
admission relation. This optimization does not exempt first acceptance from
the preceding cold-learning obligation.

## Warm reuse: what current source actually costs

Relevant source is under `software/v5/ordinary_lean/`:

| Source seam | Established behavior | Cost consequence |
|---|---|---|
| `portable_catalog.py`, `context` / `_context_rows` | Walks all selected root records, validates them, rebuilds the full binding dictionary and module plan. | At least linear visits in selected names and root records on each call. |
| `portable_catalog.py`, `_artifact` | Checks exact artifact bytes, with a verified-artifact cache within the owner process. | A fresh owner hashes the selected snapshot bytes; reopening is not a free warm hit. |
| `portable_catalog.py`, `reserve_extension` | Calls `context` and copies its binding dictionary before inserting new bindings. | Another full-context metadata pass, not only new-unit work. |
| `ordinary_admission.py`, `preflight` / `admit` | Revalidates the plan, stages/reads back evidence, obtains context and reserves. Exact reused units return `REUSED` without a new native worker. | Reused acceptance avoids kernel checking, not all parsing, custody or metadata cost. |
| `LocalSnapshot.lean`, `writeCheckedBatch` | Serializes `checked.added` and one parent import. | Snapshots are delta chunks, not full cumulative environment copies. |
| `LocalSnapshot.lean`, `restoreLocal` | Validates the complete selected import chain and imports its protected local modules, with plugins/extensions disabled. | Fresh native extension loads the selected context without kernel-replaying old proofs. |
| `OrdinaryWorkflowWorker.lean:208–212` | Iterates all parent kernel constants to rebuild the decoder's allowed-name set. | Explicit additional linear name work in every fresh extension. |

Let `n(K)`, `r(K)`, `b(K)` be selected names, root chunks and artifact bytes.
For bounded-size names/records and ordinary dictionary operations, the explicit
metadata visits are `Omega(n(K)+r(K))`; variable-size encodings add their byte
cost. Fresh owner integrity hashing reads `Theta(b(K))` bytes. Write:

```text
C_context(K) = C_lineage_and_bindings(K) + C_integrity_if_uncached(K)
               + Load(K) + C_allowed_names(K).
```

`Load(K)` and its resident memory `M(K)` are intentionally left separate.
This audit has not established Lean import's mmap/deserialization/page-touch
behavior and does not claim that import deep-copies every old proof byte.
The explicit lineage and name loops already establish the recurring scaling
issue without such a claim.

If a branch adds one bounded-size declaration per operation and each operation
reconstructs all prior names, its metadata visits sum as
`sum_(i=1..m) Omega(n_0+i) = Omega(m*n_0+m^2)`, up to configured bounds.
There is no corresponding conclusion of quadratic snapshot payload storage:
the snapshots already contain deltas. Batching reduces repeated startup and
context passes; it does not change the semantics or make an unbounded `K` fit
bounded RAM. Existing admission already accepts bounded multi-unit batches.

A root-bound immutable metadata cache would be a plausible small later
optimization. Its key must include the selected activation/policy/support
state, and corrupt or withdrawn support must not remain usable through stale
memoization. A resident native worker is more invasive: current promotion
depends on an exactly bound request and clean worker completion. Long-lived
sessions need an explicit substitute event/commit rule, cancellation, limits,
failure recovery and invalidation; “the RPC said OK” is not that rule.
Demand-scoped module DAGs could address oversized context loads, but require
exact strengthening/dependency/group/merge rules rather than arbitrary removal
of parent declarations. Neither is the first follow-on selected by this audit.

## Discovery: bounded work is not selective work

The ordinary adapter currently extracts declaration kind, exact type symbols,
result head and top-level binder-domain heads. It avoids naive repeated
application-spine expansion. The active small workflow searches with:

```json
[
  {"tag":"declaration-kind","value":"theorem"},
  {"tag":"binder-domain-head","head":{"tag":"forallE"}}
]
```

This is legitimately an unknown-result-ID query, but can match `Theta(N)`
polymorphic theorems. The consumer does not yet know the private `Stable`
ExportID, so using that ID as its input search key would beg the discovery
question.

For provider `p`, partition `j` and selected atomic features `F`, let
`P_(p,j,f)` be the posting list for feature `f`. The current rarest-anchor
algorithm can require:

```text
A(q) = sum_(p,j) min_(f in F) |P_(p,j,f)|
```

anchor examinations to exhaust the selected provider snapshots. Membership
probes, parsing, proof construction/verification, summaries and result transfer
are additional costs. The fixed 256 partitions redistribute this work; they
do not turn a common feature into a selective one. Multiple providers may
duplicate postings, and identity deduplication after receipt does not erase
their scan or transfer costs.

Candidate-only answers authenticate returned membership, not every skipped
interval. A scan/byte cap may stop safely before the useful candidate appears.
Neither exhausted budgets nor absent results establish global absence. Even a
complete answer for one committed snapshot would not prove coverage of all
published mathematics or correct feature extraction.

The existing [paired-feature profile](../../../software/v5/conjunction_index/CONJUNCTION-INDEX.md)
already materializes a bounded configured conjunction. If the relevant
intersection is small it can reduce scanning to that intersection. This is a
real existing mechanism, not missing research. Its old module-export adapter
is not automatically an ordinary V2 integration, however. More importantly,
pairing “theorem” and “has a forall-headed binder” still leaves a huge
intersection. We need a more informative queryable view, not merely more
copies of these two keys.

## Single proposed follow-on: bounded applicability views

Reuse the existing inert formal expression representation and specialist
posting indexes. Add a versioned, explicitly configured view that extracts
alpha-invariant binder/application-path structure from a declaration's type.
Allow bounded unfolding of selected transparent definitions only where needed
to expose this structure. Do not unfold theorem proofs or demand arbitrary
normal forms. Keep exact symbols where the client knows them; permit structural
roles where it does not. This is a search hint, not a conversion judgment.

For example:

```lean
Stable f P := ∀ x, P x → P (f x)

stable_compose :
  Stable f P → Stable g P → Stable (fun x => f (g x)) P
```

A bounded expanded type view exposes preservation hypotheses for `f` and `g`
and a preservation conclusion for their composition. That relationship can be
described using binder roles, repeated-variable paths and application shape
without knowing the new predicate's identity. It is materially more specific
than “this is a polymorphic theorem.” A local agent may derive such a query
from its formal goal or choose it heuristically; the network need not infer
human intention or maintain unsolved tasks.

The minimum contract, before any source selection, is:

1. Fix view revision, semantic/foundation namespace, expression traversal and
   binder normalization. Bind a view to the exact original declaration/type
   and exact definition IDs used for expansion. No remotely executed extractor.
2. Cap visited nodes, expansion steps/depth, acquired definition bytes, feature
   count and retained index bytes. Memoize by exact expression/environment
   identity. Stop explicitly with an incomplete-view marker rather than silently
   claiming a full normalization. DAG substitution can expand exponentially;
   the cap is part of the design, not an assumed polynomiality result.
3. Emit bounded useful path/signature keys. Reuse the existing selected
   conjunction mechanism only for a small declared set of useful combinations;
   never materialize all feature subsets. Preserve the old profile unchanged.
4. Clients query several explicit compatible providers within aggregate limits.
   Preview/evidence resolution remains exact. Recheck or reconstruct needed
   views for candidate relevance; acquire/check mathematics through ordinary
   admission. False or incomplete hints may waste search, but cannot grant
   theorem authority.
5. State corpus, view and partition coverage separately. Opaque or inaccessible
   definitions, capped expansions, incompatible vocabulary, overgeneral keys,
   provider omissions and adversarial hot keys have explicit incomplete outcomes.

Let `s(q)` be the aggregate selected posting population after these keys, `h`
the bounded feature count per indexed declaration and `v` the bounded view
extraction work. The source-level target is query cost proportional to selected
postings/proofs/results, plus routing and summary overhead—not to an obligatory
scan of `N`. New-record extraction costs at most its explicit `v` allowance;
posting maintenance is charged for at most `h` keys and the relevant tree work.
Total index storage remains proportional to the indexed corpus times retained
features/proof structure; it does not vanish because client queries are small.

A sublinear search claim requires the workload/coverage assumption
`s(q)=o(N)` plus bounded provider fanout and sustainable posting service. Nothing
here proves that assumption for arbitrary mathematics. Some structural patterns
will remain common. If a realistic query has no selective view, returning
incomplete results or using another specialist index/ranker is honest; asserting
logarithmic semantic search is not.

The smallest decision-changing check is initially source-level: can the consumer
express the method's applicability pattern without private symbols, and can
the extractor expose it within bounds? If yes, one targeted unknown-vocabulary
search integration with diverse decoys can check implementation compatibility.
No large-scale timing campaign is needed to establish the existing broad-query
counterexample. Small success would still not prove broad mathematical recall.

## Growth: full histories and a nonempty feasible benefit region

Use the existing [comparator](../v5-2026-10-20/PROOF-SEARCH-REUSE-COMPARATOR.md),
[growth target](../v5-2026-10-20/GROWTH-CLAIM-TARGET.md), and
[operating-region theorem](../v5-2026-10-20/GROWTH-OPERATING-REGION.md).
Do not create another accounting mechanism. The theorem is algebraic and
applies to ordinary sharing as well as its originally described certified
route after replacing the route-specific costs and availability premises.

The comparator receives the same starting mathematics, representation,
checking policy, caches, tactics and local optimizations. It may derive a short
alternative proof or generalize a result once and cache it. One local agent's
later uses are not charged repeated cold derivation. An ordinary source/package
sharing route is a serious competing implementation of the commons, with its
actual discovery and hostile-source isolation costs, not an artificially
handicapped opponent. A newly discovered peer result is not initial local
knowledge for free, but already installed Std results are.

Let `L_i` and `R_i` be the full incremental costs to the same accepted endpoint
using the best allowed comparator route and the selected commons route. Shared
cost cancels only when it is actually shared. Count producer discovery once;
charge additional generalization, publication, evidence, index, custody,
failed searches, failed production and withdrawal costs. The basic condition is:

```text
sum_i (L_i - R_i) > F + maintenance_and_service.
```

For a realistic operating class, take independently maintained projects whose
accepted frontiers already contain the shared background but not the new
method. Each consumes a bounded missing delta once; later applications are
cache hits in both routes. A positive margin is possible if discovery plus
this delta's checking/install cost is smaller than the project's actual
alternative discovery/derivation/integration cost. It is not necessary for
the original contributor to produce a cryptographic certificate. There is
also no reason to expect a positive margin for the elementary Stable example:
an optimized local proof may be cheaper. That example is compatibility evidence,
not the desired positive-growth witness.

More precisely, over supported retention/policy horizon `T`, suppose:

- Opportunities satisfy the finite demand/burst contracts of the cited theorem.
- At least fraction `alpha` yield warranted, otherwise uncached savings at
  least `d`; all other cases can fall back to the same local method.
- Extra per-opportunity search/failure/provider overhead is at most `q`, with
  no double counting of terms already inside `d`.
- Incremental fixed cost is at most `F`, ongoing cost at most `mu*T`.
- Each service queue has capacity `C_j`, per-opportunity work `u_j`, maintenance
  rate `r_j` and the stated burst/service discipline. Set
  `Lambda = min_j ((C_j-r_j)/u_j)` for positive `u_j`.

Let `g = alpha*d - q`, demand rate `lambda`, and demand burst `sigma`. Then:

```text
g > 0,
Lambda*g > mu + (F + sigma*g)/T,
(mu + (F + sigma*g)/T)/g < lambda < Lambda
```

give a genuinely nonempty supported interval, with its midpoint a witness.
The full saving is at least
`T*(lambda*g-mu)-F-sigma*g > 0`. Queue-local burst bounds limit backlog as
in the original theorem; average global spare capacity is not sufficient.
No imaginary infinite retention horizon may be chosen to force payback.

This is an explicit sufficient condition and proof of conditional nonemptiness,
not a claim that today's measurements instantiate it. In particular, `d>0`
must concern the allowed actual comparator history, not an ideal prover lower
bound; `alpha` includes successful discovery and acquisition, not only valid
theorems; and large local `K` can erase `d`. The proposed applicability view
can lower `q` or increase eligible `alpha` only if its own index-build,
maintenance, provider and candidate-validation costs are included. Give the
same useful index to an ordinary-package comparator if it can use it. If it
then wins, adopt that simpler route rather than manufacturing a v5 advantage.

This is the appropriate philosophy of growth: more warranted reusable
capability for a stated feasible resource budget, independent of human
intention. The system need not formally decide whether a theorem is globally
novel or valuable. Local agents choose work; usage/relevance heuristics choose
investments; exact checking determines admissibility. Theorem count, private
renaming and cached repeated applications do not by themselves establish growth.

## Source snapshot and authority boundary

The inspected source snapshots were:

| Path under `software/v5/` | SHA-256 |
|---|---|
| `ordinary_lean/portable_catalog.py` | `aeaf0c7d507baa6b63d401c432ca71557bf29b6b576b1f6cd8381e4e87c7473e` |
| `ordinary_lean/ordinary_admission.py` | `9653a710a089393d189830a26aa8dd0723ee75859ce577d9713dae569b5e8575` |
| `ordinary_lean/LocalSnapshot.lean` | `488a76f4b8599a95bdc748c5e89187bc55e23f63d34cf52952702d93ff68795c` |
| `ordinary_lean/OrdinaryWorkflowWorker.lean` | `442c2d479d4df6b1c7ee456cb521b8c760b54258a3f8d5fb71a15fa391c77f9b` |
| `discovery/ordinary_export_adapter.py` | `fb732a01996a821ff52f95dcb8fbd6a7a89f9aecbbb6492e24198dcf79132600` |
| `discovery/candidate_query.py` | `b5d87baa539ce734b95891ea7358db96f137b39520151fd05c8e8272efe2d639` |
| `conjunction_index/CONJUNCTION-INDEX.md` | `acffe03fddf762773daf7f553139c5ac00e4298735518312a06366f5518493f9` |

Theoretical findings above do not authorize changing these used bytes, rerunning
passing campaigns, or adding a new experiment allocation. Root owns source
selection and integration. The next decision is one product improvement to
useful discovery after the functioning ordinary reciprocal path—not a new
certificate campaign or another complete architecture rewrite.
