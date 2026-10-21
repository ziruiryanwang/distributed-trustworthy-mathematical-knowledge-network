# Bounded declared-type variant fingerprint

Decision: GO in principle for one OPTIONAL structural candidate-selection key.
This is a small standard variant-indexing technique, not semantic equivalence,
subgoal matching, automatic transport, growth evidence or a replacement index.
Current109 source: `conjunction_index/discovery/module_export_adapter.py`.
Its exact type key is address-bound; edge/symbol sets discard global structure.
This gap is real and is not fixed by the existing materialized atomic pairs.

## Domain and proposed minimal API

`pattern_spec(codec, owner_module_id, universes, type_expr)` returns one feature
specification `{"tag":"declared-type-pattern","value": fingerprint}`.
Input is a bounded, validated module-codec declared-type AST, not Lean source,
an unelaborated string or a theorem proof. Use the same helper on both sides.
The local query needs its own owner and its local formal type, not remote IDs.
An optional new feature/profile namespace must bind the algorithm version,
foundation and policy; never reinterpret existing exact-type keys or records.
One feature per declaration; ordinary feature/work/byte caps remain mandatory.
This does not require remote definitions, proof bodies or a global vocabulary.

## Canonicalization C

Validate universe arity, syntax, scope and ordinary codec limits first.
Resolve nonfoundation references to exact identities `(owner, name_bytes)`:
local n becomes `(input_owner, canonical(n))`; external M.n becomes `(M,n)`.
In particular, local n and external input_owner.n are ONE identity, not two.
Do not use bare names, ownership tags or an unqualified name as that identity.
Foundation references retain their exact structured name and distinct tag.

Traverse the complete ordered expression tree in fixed constructor-field order.
At the first occurrence of each nonfoundation identity, assign the next slot
0,1,...; replace every occurrence by that slot. Use ONE table for const and
projection-name references. Retain every other field: node tags, ordered child
positions, repeated occurrences, de Bruijn indices, binder flags, projection
indices, universe argument lists and complete sort/level syntax.
C is canonical encoding of the declared universe arity plus that changed AST.
No beta/delta/eta reduction, commutative reordering, let elimination, unfolding,
occurrence deduplication or module-boundary grouping is performed.
Different constants in the same module may match constants in different modules;
this relation concerns individual symbols, not ownership or implementation.

## Universe and ordinary binders

Ordinary binder names already vanish into de Bruijn positions in the codec.
Universe binder names already vanish into ordered integer parameter positions.
Keep those indices and the total arity, including unused parameters, unchanged.
Thus consistent spelling-only alpha-renaming is free; binder permutation is not.
`max(u,v)` versus `max(v,u)` and different implicit/explicit binder flags remain
different patterns even when a more semantic treatment could identify them.
The declaration's own name and kind are outside C; kind stays a separate feature.

## Exact characterization and hash boundary

For two valid inputs under the same profile, C(A)=C(B) iff their types agree
after a bijection between the finite sets of OCCURRING nonfoundation identities,
fixing foundation symbols and every retained field. Equivalently, an injective
renaming of the occurring A symbols carries the whole A type to the B type.
Proof: a renaming preserves first-occurrence positions, hence assigned slots.
Conversely equal canonical trees pair each slot's A and B identities; unique
slots make this correspondence bijective and all aligned occurrences agree.
The universe arities must also agree. No semantic property follows from this.

Fingerprint = domain-separated SHA-256(C). Canonical-byte equivalence above is
unconditional; digest equality implies it only if the compared inputs do not
collide. Collision resistance is a computational assumption, not injectivity.
Recomputing a candidate's key authenticates structural matching only. Its exact
descriptor/locator and normal mathematical admission remain separate gates.

## Concrete improvement over current address-independent features

Take nonfoundation T : Type and f : T -> T. Compare the standard law types:
A: forall x : T, f (f x) = x         (involution)
B: forall x : T, f (f x) = f x       (idempotence)
Both have exactly the same old type-symbol and type-edge sets, binder-domain
head T and result-head foundation Eq, plus the same declaration kind/imports.
Both laws are genuine for f=identity; the distinction is not a fake-result trick.
Their address-bound exact-type keys differ, but cannot be reproduced from an
independent T'/f' vocabulary. Their new fingerprints differ because the RHS
trees differ. A local involution schema can find an unknown-ID involution
candidate and exclude the idempotence-only shape without learning T/f IDs first.
No implication says that the found f computes the caller's desired function.
The agent must inspect and reuse the acquired vocabulary or prove a transport.

## Cost, alternatives and payoff limit

Let B be input bytes, L canonical-pattern bytes, s distinct nonfoundation names.
Validation plus traversal/hash costs expected O(B+L) with an ordinary dictionary;
a deterministic ordered map gives O(B log(s+1)+L). Memory is O(B+L+s) for a
materialized implementation; count all levels/name bytes, not just expr nodes.
All terms are bounded by the profile, independent of the global corpus size.
One extra digest/posting per indexed declaration is not a free global index.
Query work still depends on routing and that pattern's posting bucket size m;
in the worst case m equals the entire corpus. No selectivity theorem is claimed.

Discrimination trees index constructor paths; substitution trees additionally
support instantiation/generalization retrieval. A rigid-constant tree needs IDs;
wildcards with sharing constraints require matching, not this digest lookup.
This key implements only normalized whole-type VARIANT retrieval through our
existing distributed exact-key mechanism, preserving repeated-symbol equality.
It will miss specialized subgoals, reordered binders, equivalent formulations
and different level syntax. Generic law schemas can still be enormously hot.
Stronger typed matching/partial-pattern indexes remain separate future options.

Prefer this bounded optional key over building a new tree service now because
it fixes the demonstrated bootstrap collision with one derived feature and no
new retrieval algorithm. Retain ordinary acquired-vocabulary exact-symbol search.
Do not claim worldwide discovery, applicability or net benefit from this seam.
Before adoption require cross-owner equality, altered sharing/tree/level refusal,
local/external identity coalescing, bounds and old-profile compatibility checks.
