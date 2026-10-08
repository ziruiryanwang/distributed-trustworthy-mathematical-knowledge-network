# Compact semantic DAGs: an end-to-end nonexpansion contract

Root design selection under D18. This is a proposed successor representation,
not the current certificate format or a runtime authorization. D17's smaller
preserved-identity repair remains first on the proof-cost path. This document
states a concrete alternative if semantic expansion remains an obstacle; it
must not be described as implemented or measured performance.

## Why the representation is a central scalability issue

The current codec commits to expression/level **trees**. The native export is
already a DAG, but `module_correspondence::Inventory::expression/level` rebuilds
trees, and `codec._expr/_level` revisits shared syntax at each occurrence.
`module_correspondence` even expands a new theorem's proof syntax although that
proof is deliberately absent from its public mathematical identity. Moving
children instead of copying them during construction improved constants; it
does not remove this DAG-to-tree expansion.

For an opaque binary symbol `f : A -> A -> A`, define syntactically

    t_0 = a
    t_(n+1) = f t_n t_n.

The input arena needs at most two new application nodes per level. An expanded
expression has T_(n+1) = 2 T_n + O(1) occurrences, hence T_n = Theta(2^n).
The well-typed interface `t_n = t_n` does not require disclosing an ancestral
theorem proof. Nevertheless a tree-valued interface can already be enormous.
This is a representation lower bound for that encoder, not a lower bound for
Lean checking, optimal proof search, all mathematical interfaces, or all inputs.

A byte-compressed transfer that expands back into these trees before hashing,
correspondence or indexing does not remove the problem. The successor must
preserve sharing through acquisition, commitment validation, namespace and
universe normalization, native construction, and structural feature extraction.
Definitional reduction itself can still be expensive; no syntax format makes
arbitrary type checking linear.

## Semantic boundary: preserve exact syntax, not arbitrary equivalence

Use an explicitly versioned canonical arena for the existing supported syntax.
Its tags distinguish expressions, levels, names and declaration references.
The supported constructors remain the current codec's constructors initially:

| Domain | Constructors |
|---|---|
| Level | zero, positional parameter, successor, max, imax |
| Expression | bound variable, sort, constant with level arguments, application, lambda, forall, let, projection |
| Reference | foundation name, owner-relative local name, exact external ModuleID plus name |

Binder style remains committed. Binder display names remain erased, exactly as
in current correspondence. No beta/eta/delta normalization or commutativity of
universe max is silently added to identity. Ordered universe parameters are
alpha-renamed to positions, not arbitrarily permuted. Unsupported literals or
annotations require an explicit source-normalization/format policy; an unused
native row accepted by today's parser must not accidentally become a public
expression supported by the new format.

"Typed arena" means separate syntactic domains with range-checked references;
it does not mean a shape validator establishes Lean typing. Kernel validation,
adopted foundation, exact imported certificates, visibility, positivity and
derived recursor checks remain separate mandatory obligations.

## Object granularity and canonical order

The first proposed representation has independently authenticated objects:

- One group interface arena, rooted in its ordered declaration type vector and
  associated metadata. Atomic inductive groups remain indivisible import units.
- One body arena per demanded definition/opaque value or recursor rule, rooted
  at its expression and committing its universe arity.
- One witness-only arena for local theorem proofs. A proof is checked, not added
  to the public theorem's identity merely to obtain convenient serialization.

Sharing is guaranteed **within each object**, not magically across every object
in the network. Repeated shared types in separately acquired objects contribute
to the sum of their sizes. A module-wide arena with selective node openings is a
possible later tradeoff, not required for this first sound design.

For each object:

1. Validate bounded, backward-only references in each syntactic domain. Reject
   cycles, forward references, unknown tags, out-of-domain indices and excess
   allocation before following them. Metadata references to declarations obey
   the existing group-visibility relation, not syntax-node topological order.
2. Intern equal syntactic nodes by their complete finite constructor keys after
   their children have been interned. Equality compares complete keys; a local
   hash-table collision may cost work but cannot identify unequal mathematics.
3. Traverse the ordered roots in their specified order, children in constructor
   field order. On the first visit to a distinct node, visit its children and
   assign its index on completion. A visited table avoids revisiting subgraphs.
   Use an explicit stack, not unbounded language recursion.
4. Emit exactly this deterministic postorder arena. No unreachable node, unused
   dictionary item or duplicate structural node belongs to canonical content.
   Names/references use exact tagged bytes; a deterministically sorted dictionary
   can avoid repeated long strings. Dictionary IDs are implementation indices,
   not alternative mathematical identities.
5. A receiver reconstructs the canonical numbering without unfolding terms and
   requires exact agreement with supplied numbering/content. Noncanonical wire
   layouts refuse; author tools may normalize their own input before publication.

Existing order in a group declaration vector remains identity-bearing unless a
separate group-order migration is explicitly chosen. Canonicalization removes
arbitrary *sharing/layout*, not every presentation difference. Two distinct
proofs, definitionally equal terms or reordered independent declarations need
not receive the same identity.

### Uniqueness lemma

Fix the ordered root expressions as finite ordered trees and the precise tag,
name, universe-position and reference interpretation above. Any two finite DAGs
whose unfoldings are those roots yield the same canonical arena.

Proof: induction on finite subexpression height identifies every constructor
key by its already identified children. Thus structural interning yields the
same equivalence classes of subexpressions. Deterministic root/child traversal
visits those classes in the same first-completion order, assigning the same
indices. Unreachable classes are absent. Serialization is injective over the
resulting tagged, length-delimited records. The argument defines an unfolding
mathematically; the implementation never materializes it.

This proves uniqueness of exact normalized syntax, not uniqueness modulo all
Lean definitional equality or mathematical equivalence.

## Scope validation without expansion

Let b(e) be the minimum number of surrounding term binders needed for the raw
de Bruijn syntax e to be well scoped. Compute it once, bottom up:

    b(bvar i)        = i + 1
    b(sort u)        = 0
    b(const c us)    = 0
    b(app f x)       = max(b(f), b(x))
    b(lam/forall A t)= max(b(A), max(b(t)-1, 0))
    b(let A v t)     = max(b(A), b(v), max(b(t)-1, 0))
    b(proj c i t)    = b(t).

Use checked arithmetic or a rejecting sentinel when i+1 exceeds the bound.
Similarly let u(l) be zero for level zero, i+1 for positional parameter i,
u(child) for successor and max for max/imax. Propagate the maximum of referenced
level requirements through expressions. Require b(root)=0 and u(root)<=k for a
closed declaration/body with k universe parameters. The proof is structural
induction; the binder-body clause is exactly the additional surrounding binder.

This validates repeated open syntax under all of its occurrences without a
separate traversal at every binder depth. It **does not permit context-free type
inference caching**. The same `bvar 0` has different types in different local
contexts. Any kernel inference or reduction cache must retain the actual context,
universe substitution and environment/visibility information its result depends
on. The existing checker has to justify its own cache keys separately.

Structural heights and input/edge counts can likewise be computed bottom up.
Bound stack height, counts and total bytes independently. A tiny DAG with huge
expanded size is not malformed solely because its hypothetical unfolding is
huge, but inference work remains metered and may fail with resource exhaustion.

## Native correspondence without a second expanded description

The current native source names universes by name-table indices and constants
by absolute qualified names. The canonical objects use ordered positional
universes and owner-relative references. Therefore a native-node index alone
is NOT a sufficient memoization key for correspondence.

Normalize each used native node under the exact context

    (owner ModuleID, ordered universe-parameter name-index vector, node index).

The relevant foundation/local/external interpretation is also fixed by the
operation's adopted inventory. If it can vary within an operation, its immutable
identity must be included in the key. Separate level/term domains are mandatory.
Intern the owner plus exact ordered parameter vector once as a ContextID; use
`(domain, ContextID, native index)` for repeated memo lookups. Charge constructing,
comparing and interning those vectors, rather than repeatedly pretending a long
vector is a constant-size key.
Term binder depth is not required to reconstruct raw de Bruijn syntax; scope is
checked by b above. Never omit a context dependency merely to improve a bound.

Compute the normalized children, intern their finite keys, and compare canonical
roots/arena content against the committed interface/body. Do not call the legacy
`Inventory::expression` to build JSON trees inside the new checker. For local
theorem proof syntax, validate references/scope by a DAG pass and then give its
nodes to the unchanged native inference relation; there is no reason to produce
an uncommitted expanded proof tree just to discard it.

Let I be the number of **distinct normalization instances**, summed across all
owner/universe contexts and authenticated objects. Do not call this simply the
number of native nodes: one raw node can legitimately normalize differently in
several declarations. Let I_E count context-instantiated edges/level-vector
entries and I_B count context-instantiated payload/key bytes and context-vector
construction work. Put explicit aggregate budgets on I, I_E and I_B, including
failed matches. This makes the real context cost visible rather
than hiding it in a purported O(number-of-nodes) claim.

Namespaced references remain owner-relative inside a body commitment. The same
relative body bytes used by different owners do not by themselves assert equal
denotation. An opening must be used with its certified owner's declaration and
visibility context. External references continue carrying exact ModuleIDs.
Do not introduce a self-hash cycle by embedding the current ModuleID where the
existing scheme intentionally uses a local relative reference.

## Encoding and commitments

Prefer one bulk, injectively encoded object hash, not a cryptographic hash for
every term node. Retain the adopted SHA-256 security assumption for this design;
a proof-friendly hash migration is a separate decision with separate obligations.
Existing group-level Merkle openings can still supply selective authentication.

A concrete binary candidate uses a new version/domain, u8 constructor tags,
fixed little-endian u32 counts/indices, explicit length-prefixed UTF8 strings,
raw 32-byte external digests, and exact record counts with end-of-input required.
The maximum object byte length is checked before allocating count-sized arrays;
all computed lengths use checked arithmetic. No platform-sized integers,
implicit struct padding, serde enum layout, duplicate optional fields or alternate
integer spelling may influence the public encoding. Complete tag/field tables
and cross-language vectors must precede code selection; this paragraph alone is
not a finished wire-format specification.

The hash frame must bind the representation version, object kind and length.
Body identity also binds universe arity. Group leaf identity binds the existing
index/order and exact metadata plus canonical arena. A receiver processes the
actual bounded bytes; an authenticated digest is not permission to accept an
unparsed node graph or an arbitrary assertion of its root's type.

No old BodyID/ModuleID can be obtained by interpreting new bytes under an old
domain. This changes mathematical content-address **format**, semantic policy
descriptor and image. Old receipts remain receipts for their old statements.
An explicit semantic translation can relate old/new syntax when both are
available, but a digest-only translation cannot invent new certificates. The
current recursive relation requires matching image IDs, independently of whether
some mathematical identities are preserved by an implementation-only change.

## Resource statement and its limits

For selected authenticated objects let B be their encoded byte total, V their
distinct nodes, E their edges, D their declarations/metadata, I the context-keyed
normalization instances above, I_E/I_B their instantiated edges/bytes, and H the
total ancestral theorem-proof size.
Under fixed-width bounded constructor keys and an expected-linear intern table,
structural preprocessing is expected O(B+V+E+D+I+I_E+I_B), apart from explicitly
charged dictionary sorting. A deterministic balanced-map
implementation gives comparison-cost-weighted logarithmic factors instead;
adversarial hashing behavior must not be hidden in a worst-case linear claim.
Variable-length names, universe vectors and metadata are charged in B/E for
stored objects and I_E/I_B for repeated normalization contexts. Dictionary
sorting/lookup has its own byte-comparison cost; it is not made linear merely
by using a hash table elsewhere.

Index feature extraction also needs an end-to-end DAG contract. Enumerating
every root-to-node path recreates exponential work, and retaining a union of all
features at every node can be superlinear. Prefer bounded set-based node-local
features and fixed-depth/size summaries, with explicit work and output caps.
Charge summary size times its context instances. If legacy features encode
expanded occurrence paths, changing them is a versioned discovery-policy change,
not assumed feature equivalence. Candidate validity is still checked from the
actual acquired interface under its declared feature version.

The acquisition/correspondence/commitment part has no mandatory term in expanded
syntax-tree size or H. Full receiving is still

    T_cert + T_selected_arena + T_new_kernel_work
      + T_demanded_semantics + T_network_and_custody.

Kernel work may depend on demanded reductions and genuinely new proof complexity.
Discovery may return many answers or exhaust a finite budget. These terms are
not bounded by V alone. Cryptographic proof production still has a cost that
must be amortized only where an actual benefit region exists.

## Consequential implementation decision and minimum new evidence

Do not interrupt D17 with an unreviewed migration. After its same-workload screen,
select this successor if expanded semantic processing is still central or if
the next actual workload reaches the existing expansion bounds. The concrete
editable seams would be fresh canonical-arena codec/decoder, source exporter,
direct native correspondence, commitment/policy entry and versioned structural
index feature extraction. Existing public admission, routing and custody stay
reusable only where exact profile/opaque-byte compatibility actually permits it.

Required changed-boundary evidence, without repeating unrelated campaigns:

1. Equivalent DAG layouts and explicit duplicates canonicalize to one encoding;
   altered tags/children/owner references/universe positions do not.
2. Scope recurrence accepts/rejects nested binders correctly, including one
   shared open node under different depths; native typing is never inferred
   from the scope result.
3. The t_n family has linear encoded/node/edge/normalization counts at increasing
   n. No exponential expanded reference tree is built to test the large cases.
4. Small retained expressions agree with legacy correspondence where expansion
   fits; counters account for repeated owner/universe contexts honestly.
5. Cycles, forward/cross-domain references, extra/unreachable nodes, malformed
   counts, overflows and truncated/trailing encodings refuse before unbounded
   work. Failed queries/decodes consume the caller's original budget.
6. A real current-policy module and imported child exercise the new certificate
   path. Pure representation controls are not mathematical admission or a v5
   release, and never substitute for the unfinished reciprocal workflow.

This is a bounded architectural move: eliminate mandatory syntactic expansion
while retaining the original mathematical relation and explicit resource limits.
It is not a new foundation, a universal usefulness oracle, or a promise of cheap
normalization of every mathematical definition.
