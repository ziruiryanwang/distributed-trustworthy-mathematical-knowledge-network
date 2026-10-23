# Ordinary Lean workflow: extensional map reasoning without renaming the world

2026-10-22. Source-only compatibility trace by `lean_workflow_trace`.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
No Lean execution, export, proof, build, test, installation or Git mutation.
This is a concrete implementation decision input, not executed evidence.

## Decision

**Use a normal, exact-dependency Lean environment as the ordinary sharing unit.**
Preserve its ordinary constant names and normal local authoring support. Bind
their meaning to a kernel/semantic profile and exact dependency locks. Never
merge incompatible meanings merely because they have the same printed names.
Do not force this lane through the existing relocated, quotient-free relation.

The selected compatibility specimen is the standard-library extensional hash-map
lookup/update family, specifically `Std.ExtHashMap.getElem?_insert`. It is useful
in ordinary verification of data structures and update logs; it exercises actual
quotient semantics, dependent interfaces, typeclasses and standard notation.
It is not another renaming or numeral-size variation of the existing fixture.

The existing stock theorem is a compatibility target, **not new mathematical
knowledge or evidence that the network beats a normal installed library**.
Actual growth work must subsequently exchange a genuinely peer-only extension
and charge an equally optimized ordinary-sharing baseline.

## Exact existing mathematical specimen

The local pinned runtime is `software/runtime/lean-4.34.0-windows`. Its source
tree contains the following declaration in
`src/lean/Std/Data/ExtHashMap/Lemmas.lean:205`:

```lean
theorem getElem?_insert [EquivBEq α] [LawfulHashable α] {k a : α} {v : β} :
    (m.insert k v)[a]? = if k == a then some v else m[a]? :=
  ExtDHashMap.Const.get?_insert
```

The surrounding variables include universe-polymorphic key/value types,
`BEq α`, `Hashable α`, and `m : ExtHashMap α β`. Those are formal parameters,
not an instruction to trust any implementation of equality or hashing.
The lawfulness hypotheses are essential. Dropping them changes the statement.

The theorem says: looking up a key after insertion returns the inserted value
when the keys compare equal, and otherwise returns the previous lookup.
Adjacent relevant results include `getElem?_erase` at line243, proof-bearing
`getElem_insert` at line254, and `getElem_insert_self` at line260. Their common
family covers both optional lookup and lookup with an explicit membership proof.

The source-level dependency route is:

1. `Std.Data.ExtHashMap.Lemmas` imports `Std.Data.ExtHashMap.Basic` and
   `Std.Data.ExtDHashMap.Lemmas`, with an `import all` of dependent-map Basic.
2. `ExtHashMap.Basic:61` wraps `ExtDHashMap α (fun _ => β)`.
   `:79` delegates insertion; `:129` delegates optional lookup;
   `:167` supplies the `GetElem?` instance behind `m[a]?`.
3. `ExtDHashMap.Basic:64-68` stores
   `Quotient (DHashMap.isSetoid α β)`. Its insertion at `:117` uses quotient
   lifting and a proof that insertion respects the map equivalence relation.
4. `ExtDHashMap.Lemmas:244` proves the constant-value lookup law using
   `m.inductionOn` and `DHashMap.Const.get?_insert`.
5. `ExtDHashMap.Basic:9-10` imports the underlying `DHashMap.Lemmas`, including
   internal declarations used by the implementation.

This is a source trace, not a complete kernel-expression dependency census.
An actual exporter must discover every constant in types and values, including
private auxiliaries, instance arguments, recursors and proof dependencies.
Source imports alone can overapproximate that closure but cannot replace it.

Source hashes (SHA-256; identify the inspected files, not an execution result):

| Runtime-relative source | SHA-256 |
|---|---|
| `src/lean/Std/Data/ExtHashMap/Basic.lean` | `7fd6ba490503b0a8fdb9ffa202343ec0af14a03fe2760f026104a48b82a88966` |
| `src/lean/Std/Data/ExtHashMap/Lemmas.lean` | `5e11c1595a09ccdb242d7acd2e75db9f08f790479cca66d14eb07c9f5641acb8` |
| `src/lean/Std/Data/ExtDHashMap/Basic.lean` | `564092bfa7f9a408d3e72351adc655c27f7a30f39224d08c6f8baafc477782ca` |
| `src/lean/Std/Data/ExtDHashMap/Lemmas.lean` | `5b1c8234fd634dd593f7c0b512b36f04469bd745d19a77e8f48688dfd1e0879e` |

## Why the existing restricted lane is not a substitute

| Concrete boundary | Existing source | Consequence for this specimen |
|---|---|---|
| Foundation is 22 declarations; no new quotient primitives | `software/v5/modules/receipt/src/policy.rs:7-38` | The ordinary `Quot`/`Quotient` semantics cannot be obtained by relabeling an old certificate or caching the current relation. |
| Export refuses new quotient constants | `software/v5/authoring/native02/AuthorLean.lean:314` | Complete export of this ordinary quotient-backed library is not an available broad-lane feature. |
| Imported names relocate to `DMKN.Mod.<ID>...` | `software/v5/authoring/API.md:164-185` | A relocated `ExtHashMap` or relocated Nat is not automatically the caller's existing standard-library object. The authoring API explicitly lacks normal notation/instance registries. |
| The native bridge still uses restricted expressions | `software/v5/nat_literals/source_rows.py:267`; `modules/receipt/src/policy.rs` | Native bounded Nat expansion does not supply general native String literals or a quotient profile. String-key applications would additionally need literal compatibility. String keys are not required to establish the quotient gap. |
| Discovery is representation-specific | `software/v5/discovery/module_export_adapter.py:11-18`, `:160-169` | Tags, symbols and object IDs bind the old module format; resolution specifically says to verify an applicable module certificate. A broad profile needs its own extraction/locator adapter. |

The new lane should use the selected Lean kernel semantics rather than manually
reimplement these map primitives. Quotient support is not an optional frontend
convenience: the underlying mathematical type uses it. The acceptance boundary
must deliberately adopt supported quotient primitives and the actual allowed
axiom policy; this note does not assert an exact transitive axiom census.

## What real participants would do

The names below describe a proposed public workflow, not currently implemented
commands. The minimum public abstraction is an ordinary project context, not a
caller manually assembling receipt parents, scoped handles and relative names.

### Contributor A: ordinary authoring, inert exchange

A starts with an ordinary Lean project, a pinned toolchain and dependency lock.
It uses `Std.ExtHashMap`, `m[a]?`, existing instances and normal namespace names.
A obtains an elaborated declaration and exports inert types/values plus exact
dependency references. Local source, tactic evaluation and executable compiler
plugins are outside the receiver's mathematical acceptance process.

For the compatibility specimen, A exports the already existing lookup law and
its missing semantic closure. This tests sharing; it does not claim authorship
or novelty. For the later useful workflow, A publishes a separately developed
update-log method over these exact map definitions.

The public offer binds an exact semantic profile, environment/dependency roots,
declaration identity, type/definition commitments and available evidence class.
The original source and display documentation can be attached but cannot replace
the inert proof evidence. Local acceptance is not a transferable truth flag.

### Receiver B: unfamiliar-result discovery

B has a normal project using the same exact map definitions. Its agent searches
for a lookup law involving `ExtHashMap.insert`, optional lookup and equality,
without receiving the theorem ID in advance. A normal structural formal query
is scoped to those exact symbols/profile, not the text strings alone.

Replaceable providers return candidates and coverage/budget information. B
inspects the full proposition and explicit typeclass assumptions before choosing
one. Index ranking remains untrusted; an unknown/omitted result is not a theorem
refutation. Already known candidates should be cheaply suppressed using the
local accepted declaration identities.

The index engine's bounded postings/coverage mechanisms can be reused, but the
ordinary-profile adapter must bind its own normalized expression features,
environment-locked symbols and evidence resolver. Exact global semantic matching
between unrelated definitions is not promised. No network-wide scan is implied.

### B: acquire and independently admit only the missing extension

B resolves the offer against its exact accepted local environment. Common exact
declarations do not need proof replay. Every missing declaration is checked in
dependency order, or established through an applicable stronger evidence route.
Unresolved dependencies are not silently inserted as axioms. Transparent bodies
and quotient computation rules must be available when the check needs them.

The output is a locally warranted extended environment under a stated profile
and axiom policy. That is distinct from the untrusted export, a successful Lean
source compile, a publisher signature, or a portable cryptographic certificate.
The local persistence boundary must preserve this judgment across sessions.

If B has already adopted all of the matching `Std` library, this lookup law may
already be present. Then B should discover/use it locally; downloading and
rechecking it would be redundant work, not a demonstration of network benefit.
If B has only the relevant Basic module, the Lemmas extension may be genuinely
missing locally. Neither case requires pretending the world lacks ordinary
Lean package sharing.

### B: author normally and return a substantive extension

B's local elaborator must see the same exact meanings under ordinary names.
The locally built/owner-approved package provides notation and instances; any
additional peer plugin must not automatically execute inside the checker.
Imported theorem interfaces may be used conditionally during untrusted authoring,
but final exported proofs must be checked against warranted imports before
local promotion. There is no implicit inference from frontend success to truth.

A plausible later peer-only family is a small update-log library with commands
`put(k,v)` and `erase(k)` and `run(log,m)` defined by a fold over the exact map
operations. Useful formal endpoints include:

* If a log never touches a queried key (using the same `BEq` and lawfulness
  assumptions), its execution preserves that key's optional lookup.
* If two logs touch disjoint keys, executing one then the other commutes as
  extensional maps: `run(p ++ q,m) = run(q ++ p,m)`.
* A downstream agent combines independently checked commutation/lookup laws for a locally
  chosen transaction workload and contributes its generalized extension.

These are candidate workload endpoints, not newly proved declarations or a
claim that the standard library lacks equivalent facts. A later source census
must check existing lemmas and choose a genuinely absent application abstraction;
the intended benefit is not a renamed restatement. No global work queue or
human-intention field is introduced.

The return path publishes independently checked inert new declarations and exact
dependencies. Another holder can serve the same immutable evidence after A or B
goes offline. The new receiver must establish its own warrant and may reuse a
matching local basis. Initial missing-closure costs remain explicit; strict
ancestry-free delivery remains a different requested evidence class.

## Semantic identity without global source renaming

Lean's environment is a name-indexed `ConstMap`
(`src/lean/Lean/Environment.lean:208-224`), and lookup takes a `Name` (`:283`).
Package IDs do not make two different declarations with the same Lean name
coexist inside one ordinary kernel environment.

Use two levels of identity:

1. An exact semantic package/module root binds the profile, declaration/group
   records and exact semantic dependency roots. A source version or file hash
   alone is not proof of this binding. Avoid hashing an entire consumer
   environment into every shared declaration ID: unrelated extensions should
   not rename stable common knowledge.
2. An environment manifest maps ordinary Lean names to those exact declarations
   and lists the composable checked modules. Elaboration metadata has a separate
   locked identity; its content is not a mathematical acceptance certificate.

For `Nat`, `List`, `Std.ExtHashMap` and the relevant instances, the receiver either
has the same locked meaning or it does not. Matching display names, version
strings or apparent theorem types are not enough. The first implementation can
require exact matching semantic records for shared declarations, including
group identities and relevant bodies. Richer equivalence/translation is deferred.

| Combination | Correct ordinary outcome |
|---|---|
| Two branches use exact common dependencies and disjoint fresh namespaces | Check each new extension in the joined context; retain old names. |
| Both import the exact same declaration/group | Reuse the matching already warranted entry; do not check it twice solely because it arrived twice. |
| Same name has different type, value, universe policy or dependency meaning | Report a semantic conflict; isolate environments or require an explicit checked translation. |
| Different versions happen to prove equivalent-looking statements | No automatic identity or policy match; exact comparison or an independently justified bridge is needed. |
| Only notation, instance priority or pretty-printing differs | Keep mathematical dependency binding exact; resolve authoring convenience locally without letting it alter accepted terms. |

One may eventually merge theorem interfaces with different proof witnesses, but
that is not a license to ignore their actual warrant policies or dependencies.
Keeping the first broad lane conservative here is much cheaper than preserving
all normal Lean code through universal semantic renaming.

Package locks also do not abolish private-name problems. An exported proof can
reference compiler-generated/private constants; exact exported declarations
must retain those names and dependencies. Public API names remain readable, and
conflicting private universes stay isolated rather than silently overwritten.

## Smallest consequential next implementation

Implement the ordinary declaration acceptance/exchange boundary against one
exact supported Lean profile, with selected quotient support and no unchecked
peer environment import. Pair it with protected persistent local knowledge and
one explicit ordinary-profile discovery adapter. Do not broaden the zk guest
first and do not repair the old relocated representation to impersonate `Std`.

The first useful discriminator is whether the existing exact map family can be
exported as inert data, independently admitted over a compatible checked basis,
reopened, and used in normal source without semantic renaming. A native Nat/List
case can be a small parser/bootstrap check, but must not replace this real
quotient/library-readiness boundary or be advertised as broad coverage.

The true unresolved choices are the companion acceptance/persistence contracts:
trusted initial basis versus checked bootstrap, the exact supported axiom and
quotient initialization policy, inert declaration codec, and restoration of
legitimate checked state. Once those are settled, this note supplies the
concrete library target and public workflow, not another generic architecture
workstream. No proof campaign is justified by this trace alone.

## Baseline and evidence discipline

For compatibility, ordinary local Lean with the same locked dependencies is the
reference behavior. For growth, compare local-only work, ordinary peer/package
sharing and optional certification using identical mathematical/representation
capabilities. A lookup lemma already in both libraries earns no new-knowledge
credit. Initial basis checking, failed queries, decoding, indexing, storage and
provider service belong in the full cost, not merely the tiny terminal proof.

No timing or kernel-acceptance conclusion follows from the source trace. It does
establish an actual missing semantic/usability boundary and a realistic path
for deciding whether the proposed ordinary lane is worth implementing.
