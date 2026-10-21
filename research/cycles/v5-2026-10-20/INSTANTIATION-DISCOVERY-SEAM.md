# Discovering parametric results from concrete goals

2026-10-20, source/theory candidate. Root records the earlier core_search source
finding and gives the precise proposed relation below. No implementation, runtime
or mathematical acceptance is selected here. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## The actual missing operation

Current selected `type_pattern/discovery/module_export_adapter.py` already strips
outer `forall` binders for `result-head`. Adding another conclusion-head feature
would duplicate it. Whole-type variant keys deliberately preserve the entire
telescope and tree: they do not retrieve a general theorem from an instance of
its conclusion. Existing unordered edge features lose positional information.

Proposed next operation: use a *small substitution-stable conclusion fingerprint*
to retrieve candidate general results without guessing their full telescope.
This is a term-indexing filter, not a new prover, unifier or definition of value.
It requires shared exact symbol identities; unknown-vocabulary transport is a
different problem. It does not change mathematical admission.

## Finite profile and matching relation

A namespace fixes a canonical list of 1 to 3 distinct expression-child paths,
each at most 12 edges. Edges are semantic names already used by the adapter
(`fn`, `arg`, `domain`, `body`, `type`, `value`, `struct`), never JSON metadata
indices. A profile change means a different index namespace and charged indexing,
not a free in-place migration. Initial design does not combine optional profiles.

Validate the complete declaration type under its existing bounded codec. Strip
exactly its outer telescope of k `forall` nodes, leaving conclusion t. A path
observation walks t, carrying q, the number of binders introduced *inside t* on
the walked path. Entering a lambda/forall body or let body increases q; domains,
let types and let values do not. Before either following an edge or observing a
node, a `bvar j` with q <= j < q+k yields STAR for the entire remaining path.
Thus every descendant of an instantiable parameter is also a wildcard.

Otherwise observe a rigid token at the selected location:

- Exact exported/foundation symbol identity for a constant (relocating local
  references to their containing module), ignoring universe arguments.
- LOCAL(j) for a locally bound variable j < q.
- The expression constructor tag for other nodes. Ignore sort levels, binder
  annotations and projection metadata in this initial filter.
- ABSENT if a requested child does not exist at a rigid node. ABSENT is not STAR.

No undeclared outer variable is permitted by the validated source. A rigid
constant's universe instantiation cannot change this observation because its
universe arguments are deliberately omitted. Further semantic distinctions can
be tested after acquisition, not invented by the fingerprint.

Index exactly one domain-separated key for the resulting d-component vector,
including the exact profile/namespace. For a locally supplied goal expression g,
validate it in its explicit closed encoding and observe the same paths with k=0.
Construct all vectors obtained by optionally replacing each observation by STAR,
deduplicate, and issue at most 2^d <= 8 separate ordinary queries. Locally open
goals are outside this first helper's contract: reject dangling `bvar` indices
instead of treating them as trusted constants or inventing a context API.

First helper scope is explicitly CLOSED goals only. No existing public open-goal
context API is assumed. Wrapping an open goal in `forall` is not a transparent
workaround: it changes the observed tree and requires a separate context contract.
The helper must perform bounded iterative preflight on local Python input before
canonicalization/copy/recursive codec validation, reusing the current type-pattern
preflight limits where appropriate.

Do not automatically conjoin the goal's `result-head`, type-symbol or edge keys.
Substitution can replace a parameter-headed conclusion and introduce new symbols;
those extra predicates can remove otherwise compatible theorems. Safe optional
conjuncts require separate proofs or must be explicitly coverage-narrowing choices.

## What can be proved

Let sigma be a well-scoped simultaneous capture-avoiding substitution for the k
stripped parameters. Let g = sigma(t), with no beta/delta/iota normalization or
other rewriting of the raw expression tree. Then the index vector for t belongs
to the set of at most eight query vectors generated from g.

Proof, componentwise: if the path encounters an outer parameter, the index token
is STAR, which the query family includes regardless of the replacement subtree.
Otherwise substitution preserves every walked constructor and its child position.
It preserves local de Bruijn indices beneath the same internal binders, rigid
constant identities, and rigid absence. The index token therefore equals the
goal token. Choose the corresponding retain/STAR choice at each component.
Universe substitution is harmless because the observations omit universe levels.

This proves *key compatibility* for this syntactic relation, not actual retrieval
under a finite route plan. Retrieval additionally requires an indexed object,
reachable honest-serving snapshot, sufficient query/page budget and acquisition.
The test does not prove the substitution exists, respects dependent parameter
types, satisfies hypotheses, or produces a proof. Arbitrarily many false positives
are possible. Beta-reduced applications and definitionally equal forms can miss.

## Concrete discriminator, not a growth demonstration

For shared symbols f and Eq, compare types `forall x, f(f(x)) = x` and
`forall x, f(f(x)) = f(x)` against the concrete goal `f(f(a)) = a`, where a has a
constant encoding. At the root equality's final argument (`arg` in its curried
application), the first theorem emits STAR, the second emits APP, and the goal
emits CONST(a). The goal query family contains CONST(a) and STAR, not APP.
It therefore retains the first candidate and eliminates the second at this path.

These are structurally meaningful candidate types, not asserted true theorems.
Actual use must still acquire warranted mathematics and check an instantiation.
This example establishes a distinction the raw whole-type key cannot express;
it does not demonstrate positive net growth or representative search quality.

## Resource consequences and decision boundary

One added posting per declaration, not all wildcard variants at publication.
After existing bounded input validation, extraction adds at most 36 path steps
and a small vector hash. Goal processing validates once and emits at most eight
small queries. No scan of all network theorems is part of the algorithm. Ordinary
posting lists can still be huge; every actual request/page/candidate remains
bounded by the existing search/location/acquisition envelopes.

The adaptive-query APIs supply the OR across keys without a new wire protocol.
Eight syntactic keys do not imply eight funded queries: all prospective search,
location and acquisition costs must fit one original envelope. Acquire useful
selected results before rotating, since raw candidate capabilities retire.
Order, stopping and caching are local agent policy. An unqueried key is explicit
incomplete coverage, never evidence of theorem absence. A wildcard-heavy bucket
may yield no net benefit; limited search and the existing fallback policy remain.

Highest-value next decision: independently challenge this relation and compare it
with existing term-indexing primitives before selecting source changes. Require
a precise minimal public helper/profile, preallocation limits, binder-capture
counterexamples and a structural discriminator. Do not start an expensive theorem
or cryptographic production campaign to evaluate this index relation.

## Existing technique, not a novelty claim

This is a bounded adaptation of established term fingerprinting. Stephan Schulz's
[Fingerprint Indexing for Paramodulation and Rewriting](https://wwwlehre.dhbw-stuttgart.de/~sschulz/PAPERS/schulz_fp-index.pdf)
uses positional samples and compatibility filtering, distinguishing a variable,
a position below a variable, and rigid absence. The proposed filter collapses
the first two to STAR, intentionally sacrificing selectivity, and maps a tiny
query family to existing exact distributed keys instead of adding a trie service.
The paper's first-order empirical results do not transfer to our dependent-type
encoding or distributed service costs; the binder argument above remains needed.

Lean's own [discrimination-tree source](https://github.com/leanprover/lean4/blob/master/src/Lean/Meta/DiscrTree/Main.lean)
also uses wildcard candidate filtering, but includes reducible normalization and
context-dependent argument handling. It is a useful local-agent retrieval engine;
it is not directly a deterministic source-free distributed-key extractor. This
proposal deliberately needs only authenticated interface syntax, not missing
transparent bodies or a shared live Lean metaprogramming environment. A specialist
provider may add richer local retrieval without becoming mathematical authority.
