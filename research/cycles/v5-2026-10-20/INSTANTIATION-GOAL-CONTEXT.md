# Explicit local goal contexts: decision before implementation

2026-10-20, core_growth. Source/theory only. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
This is a proposed extension to `INSTANTIATION-DISCOVERY-CONTRACT.md` (`c9991ed4`),
not an edit of that contract or authority to implement/run anything.

## Decision

**GO:** add the keyword-only argument `context_binders=0` to `goal_queries`.
The expression argument remains a syntactically closed codec expression, now
interpreted as an explicit wrapper `forall Gamma, g`. Validate the entire wrapper
before stripping **exactly** the supplied number n of leading forall nodes.
Observe the remaining g; do not strip any additional quantifiers belonging to g.
This supports ordinary local tactic contexts without changing source postings,
namespace/profile, public result shape, mathematical acceptance or adaptive APIs.

Validate n with `codec.uint(n, codec.DEFAULT_LIMITS.max_depth)` before encoding
or copying any expression (current maximum 192). Bool/negative/oversized values
fail. Apply the existing bounded preflight and `codec.validate_expr` to the whole
wrapper, then require at least n leading forall nodes. Charge n stripping visits.
The whole-wrapper byte/node/depth bounds still apply; no validation of a detached
open body through a fictional codec context argument is permitted.

## Observation and scope

For goal observation begin at g with internal binder depth q=0 and context size n.
At any final selected node:

- `bvar j`, j<q: LOCAL(j), as before;
- `bvar j`, q<=j<q+n: internal observation CONTEXT(j-q), encoded `["context",j-q]`;
- any larger index: error, never a new symbol or wildcard.

Contexts use de Bruijn order: index0 is the most recently introduced Gamma binder.
Increase q only when walking a lambda/forall/let body. Domains, let types and let
values do not enter the node's new binder. Under an internal lambda, `bvar 0`
is LOCAL(0), whereas `bvar 1` denotes CONTEXT(0) when n>=1. Nested internal binders
behave identically. A context variable is rigid within g, not a source variable
that may be instantiated; this distinction must not be erased by the observer.

Source observation is unchanged: strip the entire theorem telescope of size k;
an encountered bvar q<=j<q+k is STAR before following another edge. Source vectors
contain no CONTEXT token. Goal context variables are rigid nodes: a requested
child below one is ABSENT, not CONTEXT or STAR. This matters because a source
rigid constant at the same path can also yield ABSENT. Only a *final* CONTEXT
observation receives the query optimization below.

Example: stripping n=1 from `forall a:A, forall x:A, R(a,x)` leaves the goal's
own forall. The path through its body sees x as LOCAL(0), a as CONTEXT(0).
Stripping n=2 instead describes a different selected context/goal boundary; the
caller must explicitly choose it. No implicit heuristic chooses n.

## Compatibility lemma and query optimization

Let Delta be the source telescope, t its conclusion, Gamma a well-scoped context
of size n, and sigma a simultaneous capture-avoiding substitution of Delta's k
parameters by terms scoped in Gamma. Assume g=sigma(t) as a raw expression tree,
with no reduction. For each selected path, source observation is either STAR or
equals the goal observation: before an instantiable parameter it returns STAR;
otherwise substitution preserves constructors, rigid symbol identities, child
absence and internal de Bruijn indices. Inserted Gamma references are shifted
under internal binders, and j-q removes exactly that shift. Internal binders
are never mistaken for Gamma binders.

Since a source observation cannot be CONTEXT, any final CONTEXT goal coordinate
can only match source STAR. Therefore **force STAR at every such coordinate**;
enumerate retain/STAR choices only at the other coordinates. With dimension d
and c CONTEXT coordinates, this emits at most2^(d-c)<=8 singleton queries, with
the existing canonical deduplication/order. It avoids provably empty exact-CONTEXT
queries without weakening the key lemma. All-CONTEXT emits one all-STAR query;
it may still be a poor, huge bucket. n=0 reproduces the previous API exactly.

Do not force STAR merely because a context variable occurred earlier on a path
that ultimately returned ABSENT. That would omit valid rigid-absence candidates.
CONTEXT is an internal observer token only; no new source token, feature schema,
postings, namespace or distributed query protocol is required. Explicit profile
hashes and all existing raw-tree/constant/universe rules remain unchanged.

## Dependent contexts and limits of the claim

The wrapper can represent dependent telescopes such as `A : Sort u, a : A,
P : A -> Prop`. Full codec validation establishes syntactic binder scope for
each domain and for g. It does **not** establish that those domains or the goal
are well typed. Likewise the source parameter telescope can be dependent; this
lemma requires only the stated well-scoped substitution/tree equality, not that
the substitution satisfies parameter types. Typing and remaining hypotheses are
still checked when actual warranted mathematics is applied.

Context domains are not encoded in the fingerprint. Different typed contexts,
or ill-typed but scoped wrappers, may share keys. That is an allowed false
positive, never a proof. Do not automatically conjoin context-domain symbols,
goal-derived heads or context types. Metavariables and unsupported local Lean
syntax remain outside the selected codec. Local agents must serialize their
context/goal into the explicit wrapper correctly; the network does not infer it.

Minimum focused additions to the planned pure controls: n=0 equivalence; reject
insufficient telescope/open wrapper/bad n; dependent-domain scope; one internal
binder distinguishing LOCAL from CONTEXT; context variables below missing edges;
and force-STAR equivalence to deleting impossible CONTEXT-key branches. No new
provider, proof-production, installed-runtime or scaling campaign is needed.
