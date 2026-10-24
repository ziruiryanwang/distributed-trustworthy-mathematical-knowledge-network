# Next practical benefit decision: ordinary formal-contract lookup

2026-10-23. Source/theory decision by `practical_growth_next`; no runtime,
implementation, project import, network, owner-state or Git operation. Root owns
selection. This note does not reopen completed compatibility or cost campaigns.

## Decision

After the current ordinary-project interoperability work, develop **one local
formal-contract query seam**, initially limited to alpha-normalized exact type
lookup over known vocabulary. A normal Lean project should be able to state a
general contract, search for an existing implementation without its name/ID,
inspect the returned type, and reuse its theorem through the supported ordinary
package or inert-evidence route. This is a narrow discovery capability, not a
claim to solve arbitrary goal search or establish useful growth by itself.

First settle the source-level query/extraction contract. Do not immediately
commission a broad experiment or add several alternative search profiles. With
no user-owned Lean project available, a controlled example must remain labeled
as such. If independent workload formulation does not naturally produce a known
formal contract, do not force it into this mechanism merely to obtain a pass.

## Why this direction, and what already exists

- `software/v5/discovery/ordinary_export_adapter.py` currently accepts only
  object/declaration kind, type symbols, result head and binder-domain heads.
  Its `kind-symbol-memoized-spine-head-v1` profile has no declared-type key.
  Broad polymorphic queries can therefore select a fixed fraction of the corpus.
- Earlier `discovery/module_export_adapter.py` already supplies a declared-type
  key in another representation. Reuse the idea and existing posting machinery,
  not that representation's hash namespace or a second indexing service.
- `instantiation_discovery/discovery/conclusion_fingerprint.py` already provides
  substitution-stable bounded path observations. `ordinary_body_adapter.py`
  ports that observer to ordinary DAGs for definition bodies. Do not invent
  another general fingerprint engine. These filters do not solve the present
  exact-contract gap; for a conclusion such as `h t = k t`, wildcarding the
  parameters can leave an enormous equality bucket.
- Existing `OwnerExportCommand.lean` exports an actual theorem and dependency
  closure. It is **not** a type-only query API. Requiring a proof before asking
  whether a theorem exists would invert the user's workflow.

This is a marginal-payoff judgment: one small known-contract capability is more
defensible now than a reducer, learned relevance service, resident checker,
certificate campaign or another body-search fixture. Those may be useful later;
their payoff has not been established by this missing capability.

## Proposed contract, before implementation selection

A query contains the exact semantic/foundation namespace, a closed original
type DAG, ordered universe parameters and an exact binding for every referenced
constant/projection symbol. It contains **no** purported theorem UnitID, proof,
acceptance flag or authority. Query extraction may elaborate owner-approved
local Lean syntax in its existing project context; it must not execute peer
source or fabricate an accepted theorem preview. A scratch assumption, if ever
used internally, stays query-only and cannot enter exported accepted evidence.

Derive a versioned type key bottom-up from the bounded DAG:

1. Replace referenced names by their exact portable SymbolIDs.
2. Ignore binder labels and universe-parameter labels, retaining original
   ordered parameter positions. Bound variables already use de Bruijn indices.
3. Hash each structural node from its tag, retained fields and child hashes.
   Preserve binder annotations, let flags, literal values, projection indices,
   parameter arity and universe syntax. Different sharing/numbering must not
   change the result. Do not expand shared DAGs into trees.
4. Use the same function for an independently supplied query and a returned
   bounded type preview. Bind the key/profile revision into the discovery
   namespace. Existing snapshots remain untouched; reindexing costs are real.

The key represents one explicit syntactic quotient, **not** Lean definitional
equality. Parameter permutation, hypothesis reordering, specialization,
unfolding, proof irrelevance inside types and equivalent formulations need not
match. Hash equality is only a candidate filter under the hash assumption;
the actual candidate still passes exact preview/evidence binding and unchanged
mathematical admission/application checks. No query can grant theorem authority.

Bound parsing bytes/depth, DAG nodes, parameter count and total feature work
before expensive processing. Reuse existing preflight/codec principles. For
bounded primitive fields, bottom-up key extraction is linear in supplied DAG
nodes; actual encoded field bytes must also be charged. There is no imported
proof/body traversal or conversion computation in the key extractor.

For queried provider-partition buckets `B[p,j,key]`, complete selected-bucket
inspection is output-sensitive to `sum |B[p,j,key]|`, plus routing, authenticated
index work and returned bytes. A common type or many differently proved copies
can still make this linear in corpus size. Finite budgets must return explicit
incompleteness, never global absence. Exact type keys improve selectivity only
for workloads with genuinely small buckets and available compatible providers.

## One realistic workflow and an honest comparator

Candidate workflow: independent tree-evaluator/compiler-correctness projects
want a reusable uniqueness principle over a shared tree vocabulary. A consumer
states the generalized contract from its own application before seeing a peer
theorem name, ExportID or source. It then discovers the method, checks/imports
it once, discharges its actual evaluator equations, and proves an application.
The existing `workloads/EvaluatorUniqueness.lean` supplies possible mathematics,
not evidence that this search protocol or ordinary-V2 import already works.

Its source has four genuine constructor-equation premises and a short induction
proof. This is a plausible reuse interface, **not** evidence of expensive local
discovery. Do not assign a large avoided cost to that induction. Full-type
lookup also requires the consumer to choose the same binder/premise order; if
independent formulation fails that test, record the limitation rather than
feeding it the producer's statement. Choose a different naturally known
contract or stop; do not add equivalence machinery automatically.

Keep three routes distinct:

- `L`: equally optimized independent local development, with its actual starting
  library, caches, tactics, direct proofs and one-time generalization allowed.
- `O`: ordinary source/package sharing with the **same** index/query compiler,
  known vocabulary, caching and available trusted local dependencies.
- `D`: the commons' inert-evidence acquisition/checking route with the same
  mathematical endpoint and explicit assurance policy.

`O` is an allowed implementation of our commons, not an opponent that `D` must
beat. If `O` is the useful affordable route, expose and support it. Distinguish
`L` versus sharing benefit from `O` versus `D` delivery/assurance tradeoffs.
Do not give newly discovered remote results to `L` for free, or hide existing
library lemmas from it. Charge source approval/isolation costs where applicable;
an already approved local package is not a new hostile-input execution event.

## Benefit obligation and next smallest decision

Reuse the existing [history comparator](../v5-2026-10-20/PROOF-SEARCH-REUSE-COMPARATOR.md),
[claim target](../v5-2026-10-20/GROWTH-CLAIM-TARGET.md) and
[finite operating region](../v5-2026-10-20/GROWTH-OPERATING-REGION.md).
For a stated additive resource vector or fixed nonnegative resource prices,
sharing requires a justified positive region of

```text
sum_i (C_local,i - C_share,i)
    > incremental creation + publication + certification_if_any
      + index/custody/maintenance + failed searches and production.
```

Use whole cache-aware project histories, not repeated cold charges to one
consumer. Provider work and selected context reconstruction are included.
Finite demand and service capacity must support payback within the actual
retention/policy horizon. The cited theorem's `g = alpha*d - q > 0` and feasible
demand interval remain conditional until costs/demand assumptions are justified.
There is no current positive physical-cost margin for the proposed workflow.

The minimum next unknown is **whether an ordinary project can emit a bounded
query-only type with the same symbol/universe bindings as the indexed preview,
without knowing the theorem or reconstructing its proof**. Inspect and specify
that seam first. If root selects implementation, the first discriminator should
cover that changed boundary: independent query, alpha-renaming/sharing invariance,
genuine structural nonmatches, budget refusal and one actual checked use. No
large timing campaign is justified before those obligations hold.

Stop or redirect if the desired contract is unnatural to formulate, existing
package search already resolves the workload more cheaply, keys remain too hot,
new symbol mappings demand full closure replay just to query, or metadata/search
overhead erases plausible saved work. Do not repeat the already audited body
search, SAT proposal, certificate production or compatibility campaigns. Growth
means warranted reusable capability under a feasible resource budget, not more
hash keys, theorem counts or inevitable exponential mathematical discovery.
