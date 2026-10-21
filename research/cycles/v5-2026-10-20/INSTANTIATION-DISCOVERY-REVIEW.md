# Instantiation-discovery seam: independent decision

2026-10-20, adaptive_audit. Source/theory review only; no implementation, test,
proof, build, used-source edit or Git mutation. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Decision

**GO for a minimal source design.** Root incorporated the three substantive
clarifications below in reviewed seam SHA-256
`c6267ab5fc7179b934108132925f759227466f16552b91120be355c73ec26a30`.
One obsolete sentence about an existing local-parameter representation should
be removed; the explicit closed-goal contract governs this implementation.
The proposed conclusion-path fingerprint has a valid no-false-negative
key-compatibility argument for its stated *raw syntactic instantiation* relation.
It adds a capability absent from current result-head and whole-type variant
keys. It is not general applicability checking or a growth theorem.

### Clarifications now required by the selected design

1. The first public helper must explicitly accept a **closed goal expression**,
   with an owner module identity and universe arity. The selected codec's public
   `validate_expr` starts with zero term binders and has no open-context argument.
   Wrapping an open goal in `forall` and then observing the wrapper with k=0 is
   *not* equivalent: it changes every selected path. Do not imply that an existing
   unspecified local-parameter representation solves this. Either reject open
   goals now or separately specify validated context/telescope stripping and
   rigid goal-context tokens. Do not strip arbitrary goal quantifiers implicitly.
2. Return the fingerprint query alternatives alone. Do not automatically AND a
   concrete goal's result-head, type-symbol set or whole-type pattern with each
   alternative. A substituted outer parameter may become a different head or
   introduce symbols absent from the general theorem. Example: a candidate of
   type `forall P : Prop, P -> P` has parameter result-head, while a concrete P
   has a constant/application head. Additional filters are optional caller
   restrictions and weaken the compatibility claim unless separately justified.
3. Bound local Python input **before** codec canonicalization/deep copying.
   Reuse the already bounded occurrence-counting preflight discipline of
   `discovery/type_pattern.py`; enforce profile/path lengths before encoding
   them. Codec syntax validation alone calls canonicalization before its node
   walk, so it is not a sufficient preallocation guard for arbitrary local input.

## Capture and wildcard argument

After stripping k leading forall binders, let q count binders *inside* the
remaining expression along a selected path. An outer parameter is exactly a
`bvar j` with q <= j < q+k. Check this before choosing a child and at the final
node. If encountered, the token is STAR for the entire remainder of the path.

For example, a path through an internal lambda body sees its own `bvar 0` as
LOCAL(0), but sees the stripped parameter represented by `bvar 1` as STAR.
Capture-avoiding substitution shifts inserted terms under that lambda; it does
not alter the existing LOCAL(0). Counting every bvar as STAR would lose this
distinction. Counting q in a lambda domain or let value would be wrong: only the
body is beneath that node's new binder. Nested domain expressions may of course
introduce their own binders while the path continues through them.

STAR must be checked before missing-child handling. For a selected path
`arg/fn`, an indexed parameter at `arg` can be replaced by an application whose
`fn` exists. Emitting ABSENT at the parameter would create a false negative.
Conversely, missing `fn` at a rigid constant stays ABSENT under substitution;
querying STAR as an alternative to ABSENT preserves wildcard candidates without
claiming the two tokens are equal.

Every path that avoids substituted variables has unchanged constructors and
child existence; its local indices and exact symbol identities are preserved.
Universe arguments/levels and metadata are ignored by the selected observation,
so their variation cannot falsify this statement. Relocation must use the actual
containing module for local references on both sides. The result is exactly the
componentwise STAR-or-equality lemma in the seam, subject to hash assumptions
when vectors become keys. No unification or dependent typing follows from it.

## Discriminator and precedent

The proposed Eq example works with the actual curried codec: final `arg` is the
right operand. `forall x, f(f(x)) = x` emits STAR there; the alternate right side
`f(x)` emits APP. A constant goal operand `a` produces CONST(a), whose two query
alternatives exclude APP. Both candidate types share the same Eq result-head;
whole-type keys preserve their telescopes and cannot match the closed goal.
For a nonconstant goal operand the exclusion may disappear, as expected.

This is a bounded path/fingerprint form of established term indexing. The updated
seam cites Schulz's fingerprint-indexing paper and explains its deliberate
variable/below-variable collapse; no first-order speedup is imported as evidence
for this dependent-type/distributed adaptation. The root read that primary paper;
this review independently challenges the actual proposed relation and source
seams, not the paper's experiments. The
project already records Lean's wildcard discrimination-tree precedent in
`notes/analyses/CP-001G-structural-retrieval.md` (source links pinned there).
In particular, that note records Lean LibrarySearch's treatment of wildcard-heavy
keys as a separate fallback. Do not present this mechanism as a novel algorithm
or revive the older native STRUCT2 protocol: that was a different representation
and coverage contract. Full discrimination/substitution trees can improve
selectivity, but introducing a new distributed tree protocol is unnecessary for
the current one-posting/eight-query bounded seam.

## Minimal actual integration

Resolve and preserve the current 111-source map. A fresh successor needs:

- one pure fingerprint helper with profile validation, bounded local query
  preflight, source conclusion extraction and at-most-eight query specs;
- adapter support for one new immutable profile, its feature-schema identity,
  profile-bound tag validation and exactly one fingerprint posting per record;
- an explicit new evidence-workspace schema/config branch, validated before
  filesystem mutation, retaining old modes unchanged;
- the corresponding source-map entry and concise public API documentation.

Existing record, snapshot, routing, acquisition and mathematical acceptance
protocols need no change. Existing adaptive query APIs already express the OR.
Do not combine this profile with pair/whole-type profiles implicitly. Enforce
new-tag refusal in older modes and immutable profile bindings on reopening.
The current adapter limits records to 128 features: the extra posting may cause
an explicit feature-cap refusal; silently omitting it would violate this profile.

## Cost and useful limits

After existing validation and telescope inspection, there are at most 36 edge
traversals and three final observations, not a claim that complete input handling
costs 36 steps. If stripping is newly repeated, charge its k visits too. Publication
adds one posting; query expansion costs at most eight tiny vectors. A new namespace
can duplicate all inherited postings when old and new profiles coexist, not just
the added posting. Reindexing, storage, provider service and failed searches count.

There is no bound independent of corpus size on the number of matching rows or
beneficial results. A STAR-heavy bucket can contain almost everything; three
poorly chosen paths can be useless. At most eight keys does not mean eight free
queries: every chosen alternative must fit the same finite search/location
envelope. Skipping fallback keys is an explicit coverage choice. Candidate
capabilities expire across query rotation; selected acquisition/warrant retention
must follow the existing lifecycle.

Select focused structural controls, not theorem production: internal-binder
capture; let-domain/value/body scopes; wildcard-before-ABSENT; local/external
reference relocation; universe omission; differing path profiles; the Eq
discriminator; malformed/open/cyclic/oversize input; and profile isolation.
A small generated family can check the componentwise property using a separately
implemented capture-avoiding substitution, but tests supplement the argument.
No cryptographic certificate or network scale experiment is needed to decide it.

## Final seam acknowledgement

Root removed the obsolete open-goal sentence. Read and adopt final seam SHA-256
`f5e68c211e14c808011f18e9527ce394465cba843c41c73ac084277d01d45ba5`.
The former wording caveat is resolved; the source-design GO remains unchanged.
