# Checked extensible libraries: exact boundary and smallest migration

2026-10-06 UTC. Source/theory-only checkpoint by growth mechanism agent.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
No product edits, runtime, new guest, proofs, benchmarks or deployment were
performed for this note. The proposed relation below is **not implemented**.

## Decision in one paragraph

The current fixed-foundation lane supports genuine abstract, type-parametric
mathematics and repeated contributed-definition composition. It is incorrect
to call it logically incapable of growth or to require arbitrary Lean/mathlib
support for this milestone. Its concrete limitation is that contributed
definitions must become independently F-closed bodies, not reusable checked
named environment extensions. The compiler shares equal body DAG nodes; ordinary
repeated composition therefore need not explode exponentially. Nevertheless,
each independently transported flattened capsule carries its reachable semantic
body again. The smallest useful next seam is **authenticated acyclic named
definitions and opaque theorem interfaces**, followed by a checked simple
inductive group if a source workload needs it. The latter is a discriminating
extension test, not a claim that mathematics requires an ever-growing trusted
axiom foundation. A new guest relation/policy is required for this seam; a host
allowlist change alone cannot provide it.

## Existing behavior, not a hypothetical restriction

Source paths in this section are relative to the selected frozen successor
`product-local/v4-sealer-commons-02/commons-v4`.

| Source boundary | Established behavior | Consequence |
|---|---|---|
| `source/guest/src/relation.rs:414-441` | A nonbaseline `def` is safe, transparent and singleton; both type and value pass `foundation_closed`; other nonbaseline declaration kinds refuse. | Direct contributed-definition references and novel inductive groups cannot enter this relation unchanged. |
| `source/guest/src/relation.rs:368` | Parser enumerates inductive types/constructors/recursors. | Representation syntax exists, but only exact fixed-support inductive records currently reach acceptance. Parsing support is not contribution authority. |
| `source/guest/src/relation.rs:380-395,489-522` | Imported nonbaseline axioms are exact selected **Prop** interfaces; actual checks use a restricted axiom list and exact declaration/check census. | An unverified data type or operation cannot safely be smuggled in as an arbitrary axiom. |
| `source/guest/src/journal.rs:10-39,64-80` | Member kinds are proposition and F-closed definition; definitions have empty requirements; image/foundation must match. | No module-kind/environment-root contract or automatic mixed-image import exists. |
| `receiver/cert_capsule.py:324,626` | `DEFINITION_OUTSIDE_FIXED_SUPPORT` and `F_CLOSED_DEFINITION_NO_PARENTS`. | Relaxing only the compiler or exporter does not change receiver admission. |
| `receiver/cert_application.py:83` | Unknown constant arity is refused. | New modules also require authenticated universe/signature lookup. |
| `source/native-relation/native_check.rs` | Includes the exact guest `relation.rs`. | Native-fast is the same restricted relation, not an arbitrary-Lean escape hatch. |

The fixed support is 43 records/66 reserved names (`source/guest/src/fixed.rs`).
Those counts describe this implementation profile, not an expressiveness theorem.
The previously acquired Iter/D1/D2 path already shows abstraction and composition
within the supported fragment. An agent can quantify over a type, operation and
laws and prove general algebraic facts without contributing a novel datatype.
Whether a particular mathematical development can be encoded acceptably remains
a source/workload question; neither broad impossibility nor broad completeness
has been proved here.

The bundled checker is reusable rather than requiring a new kernel:
`source/checker/src/tc.rs:82-91` dispatches inductives to
`check_inductive_declar` and genuinely checks definition/theorem bodies.
`source/checker/src/inductive.rs:80-132` checks inductive specifications and
constructors, constructs expected recursors, checks their names, and compares
nonnested declarations. Its positivity routine is at758 and invoked at909.
This is source evidence of an existing checking path, **not** a proof of kernel
soundness, Lean correspondence or a qualified public contribution path.

## Do not confuse flattening, sharing and evaluation

`experiments/definition-compiler-01/definition_compiler.py` gives the actual
transformation. In `Compiler.emit`, a selected definition constant is replaced
by its closed body with simultaneous universe substitution. The memo key is
`(source, domain, index, substitution)`; output nodes are content-interned.
No beta normalization or term substitution occurs. The final output is checked
for F closure. Inputs and output have finite limits; a refusal is not success.
The existing test source contains an eight-round shared composition test; this
note does not rerun it or promote it into a kernel/performance result.

Consider the well-typed schematic family, over an arbitrary type A:

```
D0 : (A -> A) -> A -> A := fun f x => f x
D(k+1) := fun f x => Dk f (Dk f x)
```

Use equal universe instantiations and do not normalize applications. In one
compiled capsule the two inserted Dk bodies are identical DAGs and share nodes.
For the unconstrained structural family, its distinct reachable body-node count
satisfies `S(k+1) = S(k) + Theta(1)`, hence `S(k) = Theta(k+1)`. This is a
counterexample to the assertion that repeated acquired-definition inlining
necessarily causes exponential serialized DAG growth. Integer-index/name
encoding adds representation overhead; this node-count statement is not an
exact byte/runtime benchmark. Fixed implementation bounds eventually refuse
large k, so this is a scaling diagnosis before bounds, not infinite execution.

There is still an aggregation cost: if n independently reusable capsules retain
all D0 through D(n-1), each self-contained capsule includes its own flattened
reachable DAG. Their total logical row occurrences are
`sum(k=0..n-1) Theta(k+1) = Theta(n^2)`. Distinct immutable capsule blobs do not
by themselves provide cross-capsule row interning. A content-addressed named
definition library stores each constant-size new definition body and import
edge once, for `Theta(n)` declaration/edge nodes. This is a comparison of
semantic representations, not proof that the current physical store consumes
quadratic bytes after every possible compression or that checking time is
quadratic. A final consumer of Dn may still need its O(n) selected semantic
closure; converting or computing it can cost more.

Indeed Dk applies f `2^k` times. Demanding the full result for a strict f can
require exponential computation even with optimal named sharing. This is not
remedied by a receipt. Distinct universe specializations also have separate
compiler states; no O(raw-input-nodes) bound is claimed. No source-backed
exponential serialization failure has been established here.

Thus the existing lane is compositional **extensionally** for its permitted
definitions, but not a persistent named-module interface. Avoid the stronger,
false statement that it is simply noncompositional.

## Proposed contract: checked environment extension

Let P identify the exact kernel/serialization/reduction/axiom policy and F its
fixed base foundation. A module descriptor has:

```
ModuleDescriptor = (
  schema, P, F,
  ordered external imports [(ModuleID, exported slot, full interface digest)],
  ordered local declarations with local-slot references,
  export table,
  full universe, safety, opacity and reduction metadata
)
ModuleID = H(domain || canonical(ModuleDescriptor))
```

The descriptor binds types and definition bodies, and group/constructor/recursor
data where present. It also binds theorem proof payload commitments; proof
payloads may be stored separately. Equal public types do not silently make
distinct definitions interchangeable. A public signature projection may omit
opaque theorem proof bodies, but must remain cryptographically tied to this
checked descriptor. Canonicalization is structural, not a universal semantic
equivalence/novelty test.

**No self-hash cycle.** Local references use declaration ordinals, not a ModuleID
that already occurs in the bytes it hashes. External references contain already
computed dependency IDs. After hashing, a deterministic injective realization
maps `(ModuleID, local slot)` into kernel names. Validation checks exact
reconstruction, slot kind, universe arity and declaration binding. Source aliases
are local presentation metadata, never declaration identity. The acyclic import
DAG has no hash fixed-point assumption; permitted internal inductive recursion
is handled as one checked local group.

Write `ValidEnv(P,F,E)` for a well-formed kernel environment built only by the
permitted extension rules, and `Ext(E,D,E')` for exact installation of D.
The intended certificate asserts:

```
authenticated imported environment E satisfies ValidEnv(P,F,E)
and CheckExtension(P,E,D) succeeds
and E' = Ext(E,D) has the committed exported interface/reduction data.
```

This is a relation specification, not a completed formal proof. Its conditional
soundness argument is induction on the finite import DAG: verified parent
extensions establish each imported environment; exact name/type/body/policy
binding establishes the checker input; sound extension checking preserves
well-formedness; valid output proofs establish their propositions. Cryptographic
receipt soundness transfers an actual guest execution claim, not a proof that
the checking algorithm is correct.

The certificate composition must close trust recursively: the new guest verifies
its direct imported-module receipts (or an equally strong authenticated aggregate)
under exact adopted image/policy rules, and its output receipt attests both those
valid imports and this extension. A cold receiver verifies the terminal module
receipt or the selected terminal frontier, **not every ancestral receipt**. A
signed assertion of `ValidEnv`, or a journal merely listing parent hashes, is not
this mechanism. Selected semantic declaration closure may still be fetched as
specified below; certificate ancestry and semantic data are distinct costs.

### Crucial import rule

A receipt binding some declarations is insufficient if their imports were
arbitrary assumptions. Imports must themselves be verified valid extensions of
the same authenticated environment policy, including full types/universes and
opacity/reduction behavior. Their identity commitment must match the actual
declarations installed in the child's checker. No arbitrary type/operation
axioms are introduced merely to avoid fetching their semantics.

An imported **opaque proposition theorem** can be represented by its exact
verified interface warrant without its proof ancestry, under the same policy's
permitted Prop proof-erasure rule. A transparent definition, constructor or
recursor cannot generally be replaced by a free axiom: kernel conversion and
computation can depend on its body/rules. Selected definition bodies and any
required conversion closure remain real authenticated data and charged work.
Opaque computational constants, theorem uses in dependent types, and changes
to reducibility require explicit kernel-policy treatment, not analogy with
ordinary proof erasure. The first seam should support the existing transparent
definition/opaque-Prop regime only.

### Merge without global consensus

Two modules may be incomparable in the dependency DAG. Their merge is permitted
only if P/F match, every shared `(ModuleID,slot)` realizes the same declaration,
no reserved/imported name is shadowed, all declared dependencies resolve and the
combined external dependency graph is acyclic. Content-addressed injective names
and exact immutable bindings permit a compatible union. Different aliases or
isomorphic but distinct datatypes do not justify identification; explicit proved
maps/equivalences are separate mathematics. No total global order or ledger of
all results is required. A bounded local environment/import index and local
policy-qualified cache suffice for selected compatible modules.

## Smallest implementation sequence

1. **Named acyclic definitions first.** Admit safe transparent D2 whose type/body
   references exact authenticated earlier D1 instead of flattening D1. Keep the
   existing opaque proposition warrant rule. Initially fetch the complete
   selected semantic declaration closure and genuinely check it; this alone
   improves representation but does not remove repeated checking.
2. **Certified environment installation.** A new guest checks each extension and
   exports its policy-qualified environment/interface commitment. The receiver
   verifies its certificate and installs exact authenticated declarations using
   a separately reviewed checked-import path. Child checking trusts only this
   justified boundary; unchanged generic parsing is not such a boundary.
   First implementation may conservatively retain/fetch all selected semantic
   closure. Cache keys bind policy, module/interface and reduction data. Old
   theorem proof ancestry remains absent. Skipping every semantic-body read or
   proving cost independent of selected semantics is not promised.
3. **Simple contributed datatype when demanded.** Reuse the existing kernel's
   whole-group checker with new relation roles/census. Certify the whole group,
   not disconnected type/constructor/recursor declarations. Begin with a
   nonmutual, nonnested, non-indexed strictly-positive polymorphic datatype.
   Do not claim arbitrary inductives from this first qualification.

Steps 1 and 2 are different changes: importing all bodies and rechecking them
is safe but does not establish modular verification savings. Step 2 must show
how the trusted checker environment is constructed from warranted declarations;
a direct unsafe insertion API can be a small additional TCB only if its exact
binding and well-formedness preconditions are reviewed and qualified. A new
relation/image/codec/journal is needed, plus native/application/receiver bindings
and finite limits. The available checker logic avoids inventing a kernel, but
does not eliminate this trust-boundary engineering.

Conservative migration is dual-stack: keep the old image/receipts untouched;
assign the module relation a new policy/image namespace. Recheck/re-certify old
objects when importing into the new lane unless an explicit authenticated
old-image import bridge is built and qualified. The old journal validator
requires the same image, so compatibility cannot be asserted by field relabeling.
F's **axioms** need not grow: checked definitions/theorems/positive datatypes are
intended conservative library extensions under the chosen type theory. Formal
conservativity/soundness remains a kernel/metatheory assumption here.

## Concrete datatype + layered-law discriminator

This is a proposed source workload, not a new mandatory release requirement,
existing runtime result or arbitrary library compatibility promise.

Use an independently named module with ordinary Lean-style finite sequences:

```
Seq (A : Type u) : Type u
nil  : Seq A
cons : A -> Seq A -> Seq A
```

The actual declared recursor and its computation rules belong to the group.
Then separately contribute `append`, then polymorphic `map`, each defined using
the acquired recursor and earlier declarations. Prove identity/composition and
append laws under these exact IDs. A downstream independent consumer acquires
the modules and contributes the distribution law
`map f (append xs ys) = append (map f xs) (map f ys)` under the same interfaces.
This is ordinary reusable data/operation/law layering, not an artificial new
axiom or proof-count gain. Generated equations/auxiliaries must appear in the
actual exported dependency closure; the schematic six names are not an assumed
complete Lean export. Renaming the module does not give native `List` identity.

Today the new inductive group is refused by `unsupported nonbaseline declaration`,
and its dependent operations by F-closure checks. The native-fast relation has
the same refusal. A function-encoded alternative may be possible in F but has
different recursion/elimination, interoperability and cost obligations; it is
not automatically identical to this datatype. A workload needing only abstract
operations/laws should use the already functioning abstract fragment instead.

Decisive qualification: ordinary source/export -> canonical module -> genuine
native/new-guest extension check -> certificate -> cold selected consumer ->
substantive downstream returned law. Independently reject altered constructor
or recursor rules, positivity/universe violations, missing/substituted import or
body, wrong ModuleID/slot, opacity mismatch, name shadowing, dependency cycles
and a false law. Reuse the already qualified transfer/custody machinery where
unchanged; do not repeat a broad network campaign for this relation boundary.

## Growth consequence and honest limits

The mathematical growth benefit is a persistent reusable vocabulary: agents
can add abstractions, operations and laws with stable authenticated dependencies,
without promoting each addition into a globally trusted foundation whitelist or
recopying its entire definition ancestry into every later capsule. This improves
the representational substrate for reciprocal growth; it neither selects agents'
questions nor defines universal usefulness. It is compatible with no global
task list, no human-intention acceptance and locally chosen investigation.

The stated representation bound establishes one conditional structural saving.
Net workflow savings additionally require demand sufficient to amortize extension
checking/sealing, custody and discovery, and a semantic closure small enough for
the consumer's budget. Certificates avoid theorem-proof-history replay; they do
not magically fund proving or guarantee small computation, complete search,
permanent availability, globally fresh status or exponential useful growth.
The n=10/a=0 compact preparation result reached this experiment's capacity/funding
limit, not a general affordability lower bound or user-imposed release criterion;
this module proposal does not supply a newly funded complete compact cut.

The immediate decision is therefore **retain useful F-closed operation now;
select the named-extension seam when reuse/representation demand warrants it**.
Do not describe this unimplemented proposal as shipped capability or silently
make all of Lean/mathlib a prerequisite for releasing a clearly scoped commons.

## Independent challenge checkpoint

The independent reaudit agent read this entire proposal at15:51UTC and found
no blocking counterexample to its formulation or DAG/aggregate distinction.
Its two requested clarifications are incorporated: recursive certificate trust
closure avoids ancestral receipt download, and the compact preparation limit
is experimental rather than a general affordability bound. This is a conceptual
source review, not implementation, kernel qualification or user acceptance.
The separate `experiments/compact-sealer-01/COST-FLOOR-DESIGN.md` investigates
actual pure-Prop cost; that packet has no foundation declaration rows, so this
extension contract cannot attribute its cost to repeated foundation checking.
