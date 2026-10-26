# General-theorem retrieval: reuse the existing bounded observer

2026-10-26 America/Chicago. Author: `pattern_retrieval_options`.
Source/theory comparison only. No product import, runtime, state opening, native
build, test, network call, Git mutation or external sharing was performed.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Decision

**Do not design another matcher or discrimination-tree protocol.** The project
already has the relevant limited theorem-instantiation filter, its local-context
argument and focused controls. Its existing implementation uses the earlier
module expression format; the current ordinary type-preview path does not expose
that capability. The ordinary definition-body observer supplies the current DAG
representation bridge, but indexes definitions rather than theorem conclusions.

If `INSTANCE-GAP.md` establishes a consequential candidate-enumeration gap in a
provider's existing portable corpus, the smallest credible successor is a
**type-preview conclusion observer reusing these two implementations and the
existing exact-feature index**. Strip theorem foralls rather than definition
lambdas; do not fetch theorem proofs to derive the hint. Retain the explicit
raw-instance contract below. This is a representation/API integration, not a
new retrieval algorithm or a proof of useful growth.

If existing selective symbol/head queries already make the candidate set small,
use those queries and ordinary Lean application. If a trusted ordinary project
already has suitable Loogle/Lean library search, use it. Neither an exact-key
miss nor the existence of code that could be ported justifies a new profile.

## Evidence reused rather than repeated

| Read source | What it actually supplies |
|---|---|
| `software/v5/ordinary_formal_query/formal_query.py` and `discovery/ordinary_export_adapter.py` | Current exact whole-type key; at most eight exact-feature conjuncts; symbol, terminal-head and binder-domain-head alternatives. No substitution or conversion. |
| `software/v5/instantiation_discovery/discovery/conclusion_fingerprint.py` | One source conclusion fingerprint, 1–3 selected paths, at most eight separately funded goal alternatives, explicit context wrapper, STAR-before-child handling. |
| `software/v5/discovery/ordinary_body_adapter.py` | Direct nonexpanding ordinary-DAG observer, portable symbol bindings, local-context handling, same wildcard query family, source-bound singleton definition-body records. |
| `research/cycles/v5-2026-10-20/INSTANTIATION-DISCOVERY-CONTRACT.md`, `INSTANTIATION-GOAL-CONTEXT.md`, `INSTANTIATION-DISCOVERY-REVIEW.md`, `INSTANTIATION-OUTCOME.md` | Existing raw-substitution coverage argument and scoped eight-group saved control result; not proof of current ordinary theorem integration. |
| `research/cycles/v5-2026-10-22-native-library/ORDINARY-APPLICABILITY-DESIGN.md`, `ORDINARY-NEXT-BENEFIT-DECISION.md` | Existing current-DAG bridge, scope discipline, and warning that parameter-heavy equality buckets can remain huge. |
| `research/cycles/v5-2026-10-24-growth-selection/PREEXPORT-TOOLS.md`, `PREEXPORT-CODE-GAP.md` | Previously inspected pinned upstream Loogle/client capabilities and trust/corpus limitations; do not repeat the closed upstream investigation. |

Observed current SHA-256 source identities:

- `formal_query.py`: `7901236768784a399f9ae5c56b374d040bce56536b0a47a6ee85093440cabcee`.
- `ordinary_formal_query/discovery/ordinary_export_adapter.py`: `3ddbed2156a393b08543a5da88c89b5c5b9c2b4f65689c46fbd7623cec38db0a`.
- `instantiation_discovery/discovery/conclusion_fingerprint.py`: `ac32cf53a4bf91bb012b4ba4f6701103580a51718e8c898156d5fef0b26f1bb3`.
- `discovery/ordinary_body_adapter.py`: `310980b1dab7339c68e4262c02bcff28b81cf61c08bf7c82c54b31966a4aaf32`.

These pins identify inspected source, not selected future executable bytes.
The historical old-format 2-to-1 posting discriminator is already completed; it
must not be rerun or relabeled as ordinary-preview evidence.

## Alternatives and realistic boundaries

| Option | Appropriate setting | Cost and remaining obligation | Decision here |
|---|---|---|---|
| Ordinary Lean library search / Loogle | An owner-approved matching-toolchain project or an existing useful advisory provider | Environment/index construction and upkeep; candidate matching and sorting; local proof application. Remote hints lack exact portable export identity and current upstream JSON has no authenticated corpus revision. | First choice when already suitable; same tools belong in the optimized ordinary-library comparator. |
| Existing coarse portable features, then bounded candidate-only syntactic matching | A genuinely small symbol/head cohort | Pay each preview before matching. Repeated-variable consistency and local context require a scoped matcher; actual Lean typing/discharging still follows. | No new matcher is necessary merely to consume a small cohort; ordinary Lean can try selected candidates. This does not fix huge enumeration. |
| Existing fixed-path conclusion fingerprint, ported to ordinary type DAGs | Portable previews already exist, broad cohorts are large, a few rigid positions separate useful families | One additional source key; up to eight OR queries; full input validation; posting/service/maintenance costs. Wildcard populations can be enormous. | Smallest conditional change. Reuse prior observer and exact-feature machinery; source-selection decision belongs to root. |
| Full discrimination or substitution tree over portable terms | A justified repeated workload needs richer structural selectivity than fixed paths | More indexing nodes/state, branching, repeated-variable constraints, binder/universe conventions, authenticated-service and persistence integration. Higher-order/dependent matching is not inherited from first-order libraries. | Defer. No evidence yet pays for this mechanism. |

Loogle is not a commons-specific advantage. Its existing local/remote clients
already perform useful candidate generation and, in an appropriate trusted local
environment, try applications. Upstream finite display limits do not bound its
matching/sorting work. Loading an untrusted package solely to obtain a Loogle
index is not inert-data checking: ordinary Lean initializers and environment
extensions can execute. The portable-preview route has a different ingestion
boundary, not an automatic search-quality superiority claim.

## Precise conditional coverage, inherited from earlier work

Fix a finite immutable corpus snapshot C and one exact namespace/profile P.
Let a source type be `forall Delta, t`, where stripping all leading foralls
leaves conclusion t and a telescope of k parameters. Let the query be an explicit
syntactically closed wrapper `forall Gamma, g`, with caller-supplied context
length n; strip exactly n foralls, not every forall in the goal.

The supported relation is:

`RawInstance(Delta, t, Gamma, g)` iff a simultaneous capture-avoiding substitution
sigma from source parameters to expressions scoped in Gamma, together with a
syntax-preserving universe instantiation, makes g the same raw expression as
sigma(t), modulo binder display labels and the profile's deliberately omitted
metadata. There is no reduction or rewriting in this relation. For clarity, the
stronger condition of exact raw-tree equality after substitution is sufficient.

This relation is an **assumption of the coverage theorem**, not a decision made
by the fingerprint. It neither establishes that sigma exists nor that the
dependent telescope's parameter types/hypotheses are satisfied.

For each selected child path, source observation returns:

- STAR immediately on encountering a stripped parameter, even if path edges
  remain;
- LOCAL(j) for a variable bound inside the conclusion at its final position;
- the exact portable constant identity at a constant final position;
- otherwise its retained constructor tag or ABSENT for a missing child.

At internal depth q, `bvar j` is internal when `j < q`; source parameters have
`q <= j < q+k`. Increment q only through lambda/forall/let bodies, not their
domains, let types or let values. This prevents capture and node-depth confusion.
The same DAG node can occur at different depths, so node-only observation caches
are unsound. Walking a few fixed short paths needs no expanded tree or such cache.

The query observer distinguishes Gamma variables from internal variables. A final
Gamma variable forces STAR because no source fingerprint contains a context
token. A missing child *below* a rigid Gamma variable remains ABSENT. At every
other coordinate emit both keep and STAR alternatives. With d paths and c final
context coordinates, the family has at most `2^(d-c) <= 8` keys.

**Key-coverage lemma.** If inputs pass the fixed supported syntax/resource bounds,
rigid constants use identical portable identities, and RawInstance holds, the
source's fingerprint belongs to the query's generated family. A path either
encounters a substituted parameter, producing STAR, or remains in unchanged
rigid syntax; capture-avoiding substitution preserves internal binder indices.
Universe terms do not invalidate the lemma because the observation omits them.
The same applies to other fields deliberately omitted from the fingerprint.

**Retrieval corollary, with separate premises.** That candidate is returned only
if its correct derived key is actually indexed in C; a selected reachable provider
serves that snapshot; all needed alternative keys, relevant partitions, pages and
candidate ordinals are visited within their shared allowance; and the provider
does not omit it. Hash assumptions apply to committed identities. Authentication
of returned membership does not prove extraction completeness or honest omission
behavior. A bounded early stop or skipped all-STAR branch weakens coverage.

Do not automatically conjoin the goal's symbols or result head with this family:
substitution can introduce symbols/head structure absent from the general theorem.
The type `forall P : Prop, P -> P` is the elementary counterexample. Optional
extra conjuncts are a caller-chosen narrower search, requiring their own premise
if a no-false-negative claim is desired.

## What not to infer from a positive or negative filter

A repeated source variable maps to STAR at every sampled occurrence. The filter
does not enforce equal substitutions: a shape for `x = x` can survive a query
`a = b`. Dependency constraints, instances and proof premises are ignored by this
hint. Ill-typed but scoped input may share a fingerprint with valid mathematics.
All positives are candidates; after exact acquisition, actual local application
must still be typechecked and its obligations discharged.

Universe erasure increases recall and false positives. Reusing the exact-type
key's ordered universe arity as an automatic filter would lose valid instances.
Conversely a syntactic universe matcher must not silently pretend to implement
Lean's level equalities/constraints. These are reasons to keep this index weak and
let Lean perform actual application, not reasons to weaken mathematical checking.

A beta-reduced query can miss a raw instantiated source, as can delta unfolding,
iota/projection computation, let elimination, eta conversion, rewriting, premise
reordering or changed vocabulary. Adding reduction means a new explicit resource
and coverage contract. Fuel-limited reduction is incomplete; unrestricted
reduction can be expensive and require acquiring missing transparent semantics.
The current problem does not justify reopening the deferred reducer.

A full substitution tree may enforce variable consistency and reject more false
positives, but cannot turn arbitrary Lean definitional/semantic equivalence into
a cheap complete search relation. A candidate-only bounded matcher could return
`MATCH`, `NO_RAW_MATCH`, or `UNKNOWN_BUDGET`; the second is not a mathematical
nonapplicability result. Under-binder assignments must lower/shift scope and reject
capture, and higher-order flex applications require an explicit policy. No new
matcher should be selected without a real limitation of existing Lean application.

## Whole-cost and scale model

Let B be serialized type bytes, N validated DAG nodes, k stripped parameters,
d selected paths and L their maximum length. Reading/validating the whole
bounded preview remains charged. Extra source observation takes at most
`k + d*(L+1)` node visits after validation; it never traverses proof history or
expands the DAG into a tree. Query construction adds at most `2^d` short vectors.
This is a structural accounting bound, not a CPU/wall-time SLA. Name/literal
bytes, parsing, hashing, provenance binding and index updates still cost work.

For each attempted provider p, partition s and alternative a, let A[p,s,a] be
fixed service/authentication/routing overhead and V[p,s,a] the charged driver
visits. A realistic variable query cost contains

`C_query + sum_(p,s,a) (A[p,s,a] + C_scan*V[p,s,a]) + C_returned_previews + C_local_application`.

The summation includes failed attempts. Provider/partition and OR-query fanout
multiply: eight keys is not eight free global lookups. One aggregate allowance,
explicit partial outcomes and acquisition before expiring candidate handles are
still required. Partitioning spreads load but does not remove a hot bucket's
population or guarantee semantic selectivity. A source with wildcard observations
at all selected paths belongs to an unavoidable fallback cohort.

Provider construction/maintenance costs include every relevant input read and
fingerprint, one extra posting per admitted source and any new namespace's entire
inherited posting set. Serving old and new profiles can duplicate all inherited
postings. Sparse pair access only accelerates conjunctions that are present; it
does not add missing structural information or eliminate wildcard alternatives.

For Q future queries, an economical port needs something like

`sum_q (current_full_cost(q) - fingerprint_full_cost(q)) > incremental_build + maintenance + holding`.

Both sides use equally optimized local/ordinary sharing baselines, the same
actual corpus and available caches. The inequality is conditional; this note
does not provide measured constants or a growth result. Even a discrimination
tree has work proportional to visited branches and emitted candidates. Many
wildcard branches, weak queries, or many actual matches give linear corpus work.
Neither variant warrants logarithmic general semantic search.

## Falsifier and minimal next decision

Before root selects an ordinary-preview port, require a controlled source-level
family and an independently supplied formal goal where existing exact/symbol/head
features and chosen sparse pairs cannot distinguish a large distractor cohort,
but one small predetermined path profile can. The useful source must be a raw
instance under the stated relation; do not copy its name, ID or full type into
the query. Loogle is an allowed alternative, not a handicapped comparator.

Reject the port for that workload if useful matches require the huge all-STAR
cohort, chosen paths do not separate distractors, existing selective features
already suffice, or the workflow first needs remote normalization/unknown symbol
transport. Failure of the prospective whole-cost inequality also rejects a
performance claim even if recall and implementation controls pass.

A false-negative key on any supported capture-avoiding raw instance falsifies
the coverage implementation. Targeted changed-representation checks should include
parameters before missing edges, internal versus context binders, shared DAG
nodes at different depths, universe omission, malformed/scope refusal, and exact
source-preview bindings. Reuse the old observer's argument and saved evidence;
do not repeat native proof, transport, pair-index or cross-build campaigns.

No full tree, distributed normalization, new proof authority or general matching
engine is justified now. Root can select the bounded ordinary-preview integration
only if the separate concrete gap survives. Otherwise close this investigation
with the existing-tool route and move to a different central obstruction.

## Literature attribution

This reuses established term-indexing ideas, not a novel algorithm. Prior project
notes already inspect [Schulz's fingerprint indexing](https://wwwlehre.dhbw-stuttgart.de/~sschulz/PAPERS/schulz_fp-index.pdf)
and pinned [Lean discrimination-tree code](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Meta/DiscrTree/Main.lean).
Lean LibrarySearch's separate wildcard-heavy fallback is particularly relevant:
omitting such candidates makes primary search faster by changing coverage, not by
proving that wildcard-heavy theorems are useless. The links are retained prior
research pointers, not newly fetched or independently revalidated upstream work
in this source-only assignment.
