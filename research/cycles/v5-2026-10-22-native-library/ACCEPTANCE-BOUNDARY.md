# Ordinary Lean acceptance: a concrete data-only boundary

2026-10-22. Author: `lean_acceptance_boundary`. Source/theory only. No Lean
process, build, test, product mutation, certificate, or Git operation was run.
All paths below are under the canonical project root unless explicitly linked.

## Decision

**A small, genuine ordinary-Lean acceptance adapter is feasible.** Use the
already pinned Lean kernel, an explicitly selected original-named standard
basis, inert declaration data, and checked declaration insertion. Do not route
the broad lane through the current restricted cryptographic relation, import a
peer environment as evidence, or globally rename ordinary Lean declarations.

The old `software/native/BootstrapSupport.lean` is a strong implementation
reuse candidate: it already decodes expression DAGs with native Nat and String
literals, reconstructs original-named declarations, initializes Quot through
the kernel, and checks generated inventories. It is **not** the current installed
v5 authority, nor already a hostile-peer, persistent-library service. Its fixture
capture, entire-seed assumptions, and name-only axiom checks cannot be copied as
a complete product policy.

The smallest next implementation is one new, selected adapter around these
existing facilities, not another theorem prover:

1. Establish the exact pinned standard basis once by checked reconstruction.
2. Accept an ordered, bounded batch of safe original-named declarations above
   that basis or a protected locally accepted successor.
3. Check each declaration through `Lean.Kernel.Environment.addDeclCore`.
4. Return the actual checked mathematical delta and exact environment identity
   for persistence/publication integration; never a generic frontend-success flag.

This is broad **kernel-language** admission with explicit policy/size limits,
not a claim that every existing Lean project or all Mathlib is already supported.

**Independent-review correction, controlling for implementation:**
`REVIEW-BOUNDARY.md` identifies that the old codec's deliberate normalization
loses real ordinary source API information. In particular, binder names become
`x`, breaking named arguments, and definition hints/universe names/`all` metadata
change. Do not use the old decoder unchanged for new ordinary records. The
concrete metadata-preserving successor below resolves this before code selection.
The frozen normalized basis remains a semantic anchor, **not** an ordinary
`Init` replacement or a module to import alongside `Init`.

## Actual kernel pin and entry points

Local source root:

`software/runtime/lean-4.34.0-windows/src/lean/`

Lean v4.34.0, source commit
`293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`.
Acquisition and actual-version evidence are retained in
`experiments/lean-feasibility/toolchain-provenance.md`; no version command was
rerun here. The release includes Lean sources but the C++ kernel directories
are empty. This audit read exact-commit upstream `environment.cpp`, `quot.cpp`
and relevant `type_checker.cpp` passages directly.

```text
Lean.mkEmptyEnvironment (trustLevel : UInt32 := 0) : IO Lean.Environment

Lean.Environment.toKernelEnv : Lean.Environment -> Lean.Kernel.Environment

Lean.Kernel.Environment.addDeclCore
  (env : Kernel.Environment)
  (maxHeartbeats : USize) (maxRecDepth : USize)
  (decl : Declaration) (cancelTk? : Option IO.CancelToken)
  : Except Kernel.Exception Kernel.Environment
```

`Environment.lean:1530` creates an actually empty constant map, empty module
map and uninitialized quotient state. `toKernelEnv` forces `env.checked.get`
(`:649`); a frontend's incomplete or imported environment is not thereby valid.
The kernel entry is the `lean_add_decl` extern at `:296`. Supply finite root-
selected limits. The high-level sibling `Lean.Environment.addDeclCore` at
`:701` is also suitable when its `doCheck := true` parameter is fixed by the
adapter, but the kernel-only entry makes the acceptance route more explicit.

Do not call `addDeclWithoutChecking`, the high-level `doCheck := false` branch,
raw `lean_environment_add`, `lake_environment_add`, or constructor hacks. The
C++ checked theorem path checks that the type is a proposition and that the
body has that type. Safe definitions and opaque bodies are checked too.
An axiom's *type* is checked, but its proposition is not proved: the policy
layer must handle axioms separately.

## Fixed basis: reuse an existing checked artifact, not an arbitrary import

There is an existing ordinary original-name basis, distinct from the current
zk relation's 413-row/22-declaration foundation:

| Artifact | Observed contents / SHA-256 |
|---|---|
| `software/assets/foundation/seed-verified.json` | 456 declaration descriptors, 581 exported names; `a0acdc706f5e42dca21950c14db2307a18955c63ff953019aaff413d0a976001` |
| `software/assets/foundation/seed-inventory-json.json` | 581 expected output rows; `c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0` |

These counts and file hashes were read in this audit. Prior actual decoded
empty-environment reconstruction and generated-inventory evidence are recorded
in `experiments/lean-feasibility/RESULTS.md`; no prior result is relabeled as
qualification of the new adapter.

`BootstrapSupport.receiveSeed` (`:960`) compares source pin and inventory,
starts from `mkEmptyEnvironment 0`, reconstructs each descriptor with checked
`addDeclCore`, compares actual generated rows, and finally requires `quotInit`
to be true and the exact exported-name set. Its seed includes the ordinary
Nat, Bool, String support, Eq and Quot families and the three explicit axioms:

- `propext {a b : Prop} : (a ↔ b) → a = b`;
- `Classical.choice {α : Sort u} : Nonempty α → α`;
- `Quot.sound : ∀ {α : Sort u} {r : α → α → Prop} {a b : α},
  r a b → Eq (Quot.mk r a) (Quot.mk r b)`.

**Select exact descriptors/types/bodies, not only these names.** The old
`allowedAxioms` and `decodeDescriptor` name check alone would accept a malicious
`propext : False` if arbitrary caller-supplied basis rows became authority.
Fixing the exact complete seed bytes and expected inventory in a locally
adopted profile closes that substitution boundary. Later extensions admit no
new axiom or quotient-initialization descriptor in this profile. A different
foundation is a different explicit profile, not a peer-requested mutation.

### Why pinning the standard names is mathematically essential

The pinned C++ `type_checker::reduce_nat` recognizes constants such as
`Nat.add`, `Nat.mul`, `Nat.gcd`, `Nat.div`, `Nat.mod`, `Nat.beq`, bit operations
and shifts **by name**, and computes native literal reductions. `infer_lit`
returns the standard literal type; String lowering uses standard named support.
Arbitrarily defining `Nat.add` with another well-typed body and then using these
special reductions is not the standard Lean theory. Merely checking such a
definition's type does not establish its intended builtin semantics.

Therefore the basis must establish the exact standard builtin-support closure
before peer extensions; peers cannot overwrite these names. The old basis
roots explicitly include these special Nat operations, String support, Bool,
Eq, Quot, and the special wrapper definitions. Its literal-aware ordering is
useful precisely because implicit builtin dependencies are not all ordinary
`Expr.const` references. Do not replace it with arbitrary `import Init` or an
unchecked peer snapshot.

`Declaration.quotDecl` invokes `environment::add_quot`: it validates the Eq
shape, refuses occupied quotient names, creates the four standard primitive
declarations and marks `quotInit`. Preserve that actual initialization event.
The explicitly selected broad profile has `quotInit = true`; it is not a
quotient-free profile that may later acquire the flag by incidental file import.

## Inert wire representation and checked insertion

The existing basis codec already supplies most required syntax:

| Primitive | Existing source |
|---|---|
| Exact Lean name components, including string and numeric parts | `BootstrapSupport.nameJson/nameOf`, `:435`, `:714` |
| Level DAG: zero/succ/max/imax/ordered parameters; no universe metavariables | `encodeLevel/decodeDag`, `:480`, `:759` |
| Expr DAG: bound variables, sorts, constants, applications, lambdas, foralls, lets, projections, native Nat and String literals | `encodeExpr`, `:515`; `decodeDag`, `:759` |
| Safe def/theorem/opaque/inductive descriptor | `descriptorJson`, `:574`; `decodeDescriptor`, `:858` |
| Actual generated inventory including recursor rule RHS | `inventoryRow`, `:611`; `inventoryInfo`, `:903` |

The old codec rejects open roots, metavariables, bad backward indices, malformed
UTF-8, noncanonical natural magnitudes and unsupported tags. It retains DAG
sharing and verifies the canonical re-encoding. Binder names and metadata are
normalized; binder **annotations** are retained. Universe names are represented
by ordered parameters rather than unbound strings. This is declared
normalization, not exact preservation of every frontend annotation.

Reuse needs these explicit adapter adjustments before it is a peer boundary:

- Bind format/version, kernel/profile, exact parent environment and exports.
- Reject oversized bytes, record count, DAG node count and depth **before**
  excessive construction. The old decoder bounds some structures only through
  re-encoding; `readProjection` permits a whole 128 MiB JSON file. Neither is a
  final scalable input-stream design or sufficient standalone DoS protection.
- Accept only safe `defnDecl`, `thmDecl`, `opaqueDecl`, and `inductDecl` in an
  ordinary extension. `mutualDefnDecl` is unsafe/partial-only by Lean's own
  declaration definition. Safe mutual definitions are elaborated to ordinary
  recursor-based definitions and their individual dependencies.
- Require every external reference to resolve in the exact accepted parent or
  an earlier checked batch unit. No unresolved name becomes an axiom. Inductive
  self-references are supplied only inside the one kernel group constructor.
- Reject `sorryAx`, `Lean.reduceBool`, `Lean.reduceNat` and native-evaluation
  axiom dependencies in the strict profile, including hidden closure members.
  These native-evaluation mechanisms can call the interpreter and extend the
  trusted computing base; they are not ordinary kernel-only proof checking.
- Reject all name overwrites. Exact already-present records can be recognized
  as references/deduplication before insertion; never silently accept a new
  body under an existing name merely because a type matches.
- Preserve the existing generated-name/reserved-name defenses, and inspect
  actual generated constants, not only `Declaration.getNames`.

For each new declaration, use the checked entry, then compare actual output
against the advertised normalized descriptor/inventory. Install **actual
kernel-generated** constructors and recursors; the advertised inventory is
only a claim to compare. A failed batch leaves the prior accepted environment
unchanged. Resource exhaustion is not mathematical invalidity and confers no
partial implicit acceptance.

Ordinary references remain original Lean names, with a parent environment
identity selecting what those names mean. Native literals remain literals;
large numerals are not expanded into successor chains. The existing decoder
thus avoids a substantial representation restriction without any new proof
system.

## Reviewed concrete ordinary codec: preserve the real source API

The new format is `DMKN_LEAN_ORDINARY_V1`, with normalization
`erase-mdata-only-v1`. It is a fresh format; no old seed/package ID changes.
Use a binder-aware per-expression DAG, not a sidecar over the old normalized
DAG: old interning can collapse differently named binders to one node, so one
sidecar name per old node cannot recover the source records.

### Expressions and names

Keep the old three-part DAG `[levels, expressions, rootIndex]`. Keep level-node
tags zero/succ/max/imax/parameter-index. The caller supplies the declaration's
**original ordered** `levelParams : List Name`; parameter indices decode under
that exact list, never under `indexedParams` followed by a cosmetic field swap.

Retain expression tags 0/1/2/3/7/8/9 with the old shapes. Replace only these
node shapes, where every expression index points strictly backward:

```text
[4, binderName, binderInfo, typeIndex, bodyIndex]       lambda
[5, binderName, binderInfo, typeIndex, bodyIndex]       forall
[6, binderName, typeIndex, valueIndex, bodyIndex, nondep] let
```

`binderInfo` is the existing integer code 0..3. `nondep` is exactly 0 or 1.
Names use the existing component arrays, but split raw decoding from role
validation. An empty component array denotes an anonymous **binder** name;
numeric or internally named binders are inert labels. Declaration and constant
reference names still obey the selected nonanonymous/reserved-name policy.
Do not apply the old declaration-oriented `nameOf` rejection to every binder.
Universe names are exact unique bounded Names and are validated independently;
kernel checking ultimately checks their use.

Strip only `.mdata` wrappers recursively. Preserve lambda/forall names and
BinderInfo, let name/nondep, literal values, actual constant names and all level
structure. Intern encoded nodes including their retained metadata, or memoize
with `ExprStructEq`/`Expr.equal`; plain `BEq Expr` is unsuitable for exact
binder-aware identity. Enforce construction bounds before allocating the next
node. The preserved nondep flag is untrusted elaborator metadata, not a proof
of an absence-of-dependence proposition.

`AuthorLean.lean:181-234` has the required full-field exporter pattern, and
`:281-311` has exact level/hint/all declaration fields. Reuse those patterns
and the old DAG traversal, **not** `AuthorLean.dumpExpr` unchanged: its default
`removeMData` also erases binder names and nondep. The new function must do
exactly what its normalization identifier says.

### Ordinary declaration units

Choose these fixed-arity inert arrays for the new extension only:

```text
[0, name, levelParams, typeDag, valueDag, hint, all]   safe definition
[1, name, levelParams, typeDag, valueDag, all]         theorem
[2, name, levelParams, typeDag, valueDag, all]         safe opaque
[3, levelParams, numParams, types, inventory]          safe inductive group

hint  := [0] | [1] | [2, UInt32]                     opaque / abbrev / regular
types := [[typeName, typeDag,
           [[constructorName, constructorTypeDag], ...]], ...]
```

`levelParams` and `all` contain original Name values, not universe arity or a
forced singleton. Safety is fixed by these allowed tags, not chosen by a peer.
Require bounded nonempty duplicate-free `all` with the declaration's own name
included, preserving its original order. For ordinary safe lowered definitions
this metadata is not an authority edge or a requirement to trust unprovided
members; a claim to possess every member of a block requires a separate census.
The kernel ignores ordinary definition `all`, but consumers need not lose it.

Construct the corresponding safe `Declaration` directly. **Do not call old
`withHeight` on new extensions.** Preserve every hint tag/height; Lean documents
hints as reduction-order guidance rather than a new inference. This avoids
silently changing ordinary performance characteristics and record identities.

The group inventory uses a successor of old
`[name, kind, levelParams, typeDag, details]`, replacing universe arity by
original parameters and preserving every kind-specific field:

- definitions: value, exact hint, exact `all`;
- theorems: value and exact `all`;
- opaque values: value, false unsafe flag, exact `all`;
- inductives: parameters, indices, exact ordered `all`/constructors, nested
  count, recursive/reflexive/unsafe flags;
- constructors: exact owner, index, parameter/field counts, unsafe flag;
- recursors: exact `all`, parameter/index/motive/minor counts, k/unsafe flags,
  ordered rules containing constructor, field count and full RHS DAG.

The actual generated inventory is compared under `erase-mdata-only-v1`;
constructors/recursors still enter only through checked group generation.
The wrapper must not use old `inventoryRow`'s singleton normalization or its
regular-hint-only branch as an exact ordinary inventory. The extension format
has no axiom or `quotDecl` input tag. The fixed basis initializer is separate.

The enclosing operation binds format/normalization, selected kernel/profile,
exact parent environment, ordered units, selected exports and explicit resource
limits. Existing source maps/custody can carry those bytes; no blockchain,
global package registry or new cryptographic judgment is required.

### Basis matching and owner-side rebind

There are two intentionally distinct projections:

1. **Ordinary record projection:** erase mdata only; preserve the fields above.
   Use this for new-record identities, deduplication and actual-output comparison.
2. **Fixed-basis semantic projection:** original constant names and mathematical
   type/value/recursor structure, ordered universe parameters alpha-normalized,
   binder names erased but BinderInfo retained, let nondep normalized false;
   omit definition reduction hints and ordinary def/theorem/opaque `all` only.
   Preserve inductive/constructor/recursor group structure and flags. This is
   restricted to the locally selected normalized seed correspondence.

The second projection must be applied to actual owner-project dependency
records and actual accepted basis records, not to package labels. Its deliberate
erasures concern alpha names, optimization hints and nonlogical metadata; they
do not permit changed constants, different axiom types, proof bodies, reduction
rules or a proof substituted for an absent body. The exact accepted basis is
still fixed by its own bytes. Extension comparisons outside that fixed basis
use the first, more conservative projection.

Keep checker snapshots internal. An ordinary `Init` import and a checker basis
snapshot contain duplicate definitions; Lean `subsumesInfo` does not merge
arbitrary duplicate definitions. A different module name cannot cure that.

The owner-side bridge therefore:

1. Retains the owner's existing pinned ordinary module graph and conveniences.
2. Matches all required pre-existing meanings against accepted dependency locks
   using the appropriate projection above, including the transitive meaningful
   dependencies needed to establish that match. Mere names never suffice.
3. Reconstructs only missing new acquired declarations via checked insertion in
   the owner environment. This repeats checking of the new delta, not the old
   accepted library. Conflicting existing names fail rather than overwrite.
4. If it writes a local authoring module, that module imports the ordinary owner
   graph, not the isolated checker basis snapshot.
5. Exports the owner's resulting successor as inert proof data and independently
   checks it through the isolated mathematical admission path.

The owner environment and plugins may still be untrusted as mathematical
construction tools; the final independent check is necessary even after the
bridge match. The bridge improves normal usability and records intended exact
dependencies; it does not certify arbitrary owner's `.olean` or native code.
This concrete separation resolves the duplicate-definition and named-argument
issues without rewriting a user's project topology.

## Existing upstream replay: useful reference, not a turnkey service

`Lean/Replay.lean` provides

```text
Lean.Kernel.Environment.replay
  (newConstants : Std.HashMap Name ConstantInfo)
  (env : Kernel.Environment) : IO Kernel.Environment
```

It orders dependencies, calls checked insertion, reconstructs inductive groups
and compares advertised constructors/recursors with generated ones. This is
valuable precedent and reusable logic; ordinary Lean already has the basic
operation this project needs.

It is not the complete proposed boundary: it accepts arbitrary `.axiomInfo`,
skips unsafe/partial entries rather than proving a selected export closure,
uses `addDeclCore 0 0` without finite limits, assumes structurally usable
ConstantInfo inputs, permits duplicate theorem records with equal interfaces,
and discovers ordinary constant references rather than the entire implicit
literal-support policy. Derived equality also is not a substitute for the
adapter's specified normalization and exact semantic bindings.

Similarly, `LeanChecker.lean --fresh` detects some environment hacking by
replaying into a fresh kernel environment. It first loads `.olean` artifacts
and is not an independently sandboxed hostile-byte receiver or an axiom-policy
enforcer. Do not advertise invoking it as sufficient admission.

## Import and persistence conditions

`Lean.importModules ... trustLevel := 0` does **not** recheck imported proofs.
`Environment.finalizeImport` (`:2307`) builds constant maps directly from
imported ConstantInfo and sets `quotInit := !imports.isEmpty` (`:2363`).
`loadExts := false` avoids initializing imported extension state but does not
turn the imported constant map into checked mathematics or make arbitrary
compacted `.olean` bytes safe to deserialize.

For local persistence, the sibling persistence investigation may use official
module serialization **only** for an adapter-produced accepted environment.
The invariant must include:

1. Exact accepted basis/profile/checker and true checked quotient initialization.
2. Only locally emitted, integrity-protected snapshot chunks and their exact
   previously accepted import closure; no substituted peer `.olean`.
3. Restored mathematical constants/types/bodies/generated metadata equal the
   recorded accepted environment under the fixed normalization.
4. The importer may set `quotInit = true` only because this profile already
   established it; it is not a fresh proof or a generic state-equivalence rule.
5. No peer plugins, executable environment extensions or initializers in the
   acceptance process; exact module search roots, no ambient `LEAN_PATH` or
   `LEAN_SYSROOT` override. Pin actual resolved artifacts, not only `lean.exe`.

The primitive no-import initialization runs trusted application initializers
for its own linked Lean modules. That is part of the pinned adapter/toolchain
TCB, not permission to run arbitrary contribution code. Producer export from
an owner's normal local project can load that owner's chosen artifacts, but
its output remains untrusted inert mathematical data at the receiver.

## Why keep environment identities instead of globally renaming names

The core identity should bind the checker/profile, a compatible mathematical
environment and the exact extension contents. Separately bind source package
and pinned dependency identities for provenance/reproducibility and authoring
compatibility. Package name/version alone is not a proof-semantic identity.

Within one environment, retain names such as `Nat`, `List`, `Quot`, ordinary
namespaces and generated private names. This preserves kernel builtin meaning
and makes existing project proof terms reusable without replacing their entire
vocabulary by `DMKN.Mod.<hash>...` constants. Notation, typeclass tables, simp
attributes and tactics remain authoring conveniences, not warrant authorities.
They may be supplied by the owner's normal pinned local project; the final
proof is checked again against the receiver's semantic environment.

Two branches may merge when their common named dependencies denote exactly
compatible declarations and their additions do not conflict. Distinct versions
defining the same name differently cannot share one kernel environment by
wishful union. Keep separate environments or require a separately checked
translation. A package/environment identity prevents ambiguity but does not
itself prove that translation. Independent theorem proof witnesses can share
a semantic theorem identity only under an explicit policy; the first adapter
should not add that complexity by silently coalescing unequal records.

## Formal obligation and immediate implementation selection

Let `P` fix this kernel semantics, exact standard basis, permitted axiom schemes,
input normalization and forbidden evaluation routes. Let `Valid_P(E)` mean all
declarations in `E` are justified by that basis and checked extension rules.
For decoded `d`, the implementation must establish:

```text
Valid_P(E) and Allowed_P(E,d) and addDeclCore(E,d) = ok E'
    imply Valid_P(E').
```

This is conditional on kernel/adapter correctness, fixed builtin semantics,
resource isolation and integrity of local accepted state. Persistence preserves
this already-established judgment; arbitrary deserialization cannot create it.
The theorem is not a proof of fast type conversion, global completeness or
cheap initial acquisition.

**Recommended concrete selection after independent review:** reuse the exact
456-unit basis and the original-name DAG traversal/checked-generation machinery
in a new small source cut, with the metadata-preserving ordinary codec specified
above; add the parent-bound safe-extension operation and explicit resource/policy
checks. Coordinate with isolated protected local snapshot integration and the
separate owner checked-rebind bridge
before choosing the first actual workflow. Do not duplicate the old basis
qualification campaign, broaden the zk guest, or begin another cryptographic
certificate. Tests later need to target new boundaries: changed axiom type,
builtin replacement, hidden native-evaluation/sorry, missing dependency,
wrong-parent environment, malformed DAG, generated-recursion mismatch and
restart identity—not reprove that elementary congruence works.

The source-level decision is resolved: the checked-kernel seam exists and
substantial machinery can be reused. Remaining decisions are finite adapter
schema/resource choices and actual project compatibility, not an unresolved
need for a new foundational proof system.

## Primary source anchors

- [Pinned kernel declaration checking](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/environment.cpp)
- [Pinned builtin and literal reduction](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/type_checker.cpp)
- [Pinned quotient initialization](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/quot.cpp)
- Local `Lean/Declaration.lean:172-205` and `Lean/Environment.lean:185-310,701-731,1530-1544,2307-2459`.
- Local `Lean/Replay.lean`, `LeanChecker.lean`, and `Init/Core.lean:2342-2409`.
- Earlier detailed checked-reconstruction pitfalls:
  `experiments/lean-feasibility/source-capture-notes.md`.
