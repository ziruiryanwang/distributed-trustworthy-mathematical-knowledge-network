# Large-network Lean interfaces without historical proof replay

2026-09-27. Bounded independent investigation by `/root/v3_index`, assigned by
root after the user made very-large-network verification a priority. Canonical
workspace guard passed. Read-only inspection of the selected source16 native
receiver, frontend bridge, canonical planner and bundled Lean4.34.0 source APIs.
No product edit, build, proof execution, certificate implementation or new
experiment. The source16 and growth campaigns are not extended by this note.

## Finding and recommendation

**Yes: a local Lean proof can be checked using the *types* of previously
certified theorems without locally obtaining their proof bodies.** The useful
unit is a verified, foundation-bound theorem interface, not an entire historical
replay package. A remote certificate must establish that the interface is a
derived result under the allowed base assumptions. A receiving bridge can then
install a local typed premise for that interface and kernel-check new work
relative to it. Compositional certification discharges those premises back to
the base; it must never mistake arbitrary well-typed axioms for proved results.

This is an explicit new acceptance mode with an enlarged, stated cryptographic
TCB. It is not implemented by source16, not justified by a CID alone, and not
equivalent to turning off Lean checking. The first tractable scope is **sealed
Prop-valued theorem interfaces**, while retaining exact data needed for local
type checking and conversion. Preserve a strict body-available lane for work
outside that scope. Do not promise every Lean program/proof remains usable when
all theorem bodies or definition bodies are erased.

The central scale claim to target is:

> A fresh downstream node's verification/import work depends on its selected
> public interfaces and locally used computation, not on the accumulated proof
> histories hidden behind certified theorem interfaces or the whole network.

Avoid replacing this with a cache-only promise. Caching helps an already warm
node; compositional certificates must also let a **cold** node avoid replaying
the certified proof ancestry.

## What the current product actually does

`AgentReplayCore.receive` reconstructs the selected seed, then every row of the
prepared batch. `receiveOrdinary` decodes both `type` and `value`, constructs a
real definition/theorem/opaque declaration and calls `checkedAdd`, whose actual
`addDeclCore` call fixes `doCheck := true`. It then requires the checked body
exist and re-exports it. Groups are regenerated from inductive declarations,
with exact generated inventory correspondence. The Python planner and
re-exporter demand complete root closures and inverse equality.

The frontend's `sourceEnvironment` imports Init for authoring, compares shared
bindings, reconstructs missing checked declarations, and compares bindings
again. `collectExtension` captures every newly used nonselected dependency and
explicitly refuses external axioms. `BootstrapSupport.screen` accepts only
the three selected base axiom names; unchecked peer assumptions are not a
currently supported interface. Thus changing only a Python cache or omitting
old package objects would be refused—or would break the present evidence
contract if checks were simply removed.

Current full-body obligations provide useful strict reference behavior, but
their transitive historical replay is the wrong mandatory receiver boundary
for the proposed very-large network.

## Actual Lean APIs: the seam exists, with a significant caveat

The bundled `Lean/Declaration.lean` defines distinct `AxiomVal`, `TheoremVal`,
`DefinitionVal`, `OpaqueVal` and inductive declarations. A theorem declaration
contains a `value : Expr`; there is no ordinary body-free `thmDecl` constructor.
An axiom declaration contains name, ordered universe parameters, type and
`isUnsafe`, but no proof. `Lean.Environment.addDeclCore(..., doCheck := true)`
can install such a declaration while checking its type/parameters; **that does
not prove the type inhabited**. The external certificate is the missing
justification, and has to be verified before installation.

This is not an alien representation to Lean4.34.0:

- `Lean/AddDecl.lean` exports module theorems as `axiomInfo` interfaces when
  their bodies are not exposed, while checking the private theorem first.
- `Lean/Environment.lean:subsumesInfo` compares theorem/axiom name, type and
  universe parameters without requiring identical proof bodies.
- The same source explicitly says theorem bodies are **mostly** opaque and
  warns that `Acc.rec` may unfold theorem proofs during type checking.
- `Lean/Util/CollectAxioms.lean` stores precomputed imported axiom dependencies
  so normal axiom collection need not walk all imported module bodies.

These are concrete implementation precedents, **not** authentication of an
untrusted `.olean` file or theorem certificate. Imported axiom summaries and
body-erased module data are untrusted network inputs until their exact semantic
binding is established. A module hash/signature alone authenticates bytes or
an issuer, not derivability.

The `Acc.rec` caveat means the tempting statement “proof bodies are never used
in conversion” is false for this pinned runtime. Checking a new proof only
against sealed premises can reject some source proofs or computations that
work with full theorem bodies. This is a compatibility/completeness limitation,
not permission to insert a fake body or trust failed type checking. Publish a
sealed-interface support profile and expose clean “body required/unsupported”
outcomes. A broader erasure theorem remains a formal obligation, not something
established by this source inspection.

## Required public theorem interface

A certificate-backed interface should commit at least to the following exact
fields, under an unambiguous canonical schema:

| Field | Why it is necessary |
|---|---|
| Foundation and base-axiom policy | Prevent silently importing a theorem of another logic or assumption set |
| Checking/certificate relation version and program identity | Bind the computation actually certified; same output string is insufficient |
| Declaration category: sealed theorem in Prop | Prevent confusing a proof with arbitrary executable data/definition |
| Full ordered universe parameters and canonical type | Arity alone cannot authenticate parameter order, level expressions or the statement |
| Exact semantic references in that type | Equal textual names do not imply equal definitions, types or foundations |
| Interface/computation environment commitment | Bind all symbols and conversion behavior the certified checking relation used |
| Derived-import commitment and validity/composition policy | Prevent importing unchecked premises hidden inside a locally successful check |
| The theorem/result identity | Bind the certificate to the exact requested object; optionally also a specific proof-instance commitment |

The current system distinguishes a semantic judgment from an exact proof
instance. Keep that distinction. A certificate that merely proves some witness
exists for T authenticates T, not necessarily the current proof-instance CID.
To authenticate a particular omitted proof object, the certified relation must
also recompute/bind that object's commitment from the prover's private witness.
Multiple certified proofs of the same judgment may coexist without requiring
downstream nodes to download them all.

The profile must establish that T really has sort Prop, including its universe
scope, rather than trusting a caller's `kind = theorem` label. Lean's kernel
`check`/`whnf` APIs and a checked declaration supply useful implementation
primitives; exact wrapper behavior still requires a bounded implementation
test. No metavariables, loose variables, name overwrites or unbound universe
parameters may enter an accepted interface.

## Formal composition obligation

Let B be the fixed well-formed base environment and A its allowed logical
axioms. Let I be a finite selected interface environment. The local checking
environment E contains:

1. B and exact selected computational declarations;
2. fresh constants `c_i : T_i` for verified sealed theorem imports;
3. the new declaration/proof q to be checked.

The bridge must establish an **environment realization**, not just a list of
unrelated true propositions: there is a mapping rho into a well-formed extension
of B which preserves names/references, universes, types and every conversion
rule actually exposed locally, and which maps each derived premise `c_i` to a
proof `p_i : rho(T_i)` using no logical axioms outside A. The realization covers
the whole selected environment, including types and definitions depending on
imports, not merely the final proof's surface list of theorem names.

The required preservation lemma has the shape:

`Realizes(B, E, rho) and KernelCheck(E, q, T)`
`    imply Derivable(B plus legitimate definitions, rho(q) : rho(T)).`

For acyclic theorem imports with identical computational declarations, this is
the familiar substitution/extension argument: replace each typed derived
premise by its certified proof, in dependency order. Local stock Lean checks
the new proof conditionally; the certificate system supplies the realization
and discharges the conditions. Neither a locally accepted `axiom False` nor a
successful `KernelCheck` under that axiom establishes a base theorem.

The cryptographic relation must ensure each child certificate establishes the
same kind of validity under the same accepted base/policy, with an anchored,
well-founded composition rule. Two claims “False follows from the other claim”
cannot authenticate each other through a cycle. Do not mistake a Merkle proof
of membership in an arbitrary set for a proof of that set's validity. A
recursive/aggregated certificate should certify child validity internally so
the cold receiver does not have to recursively fetch all predecessor
certificates. The cryptography review owns concrete recursion assumptions.

This is a conditional soundness argument relative to Lean/base soundness and
the certificate system's computational soundness. It is not an unconditional
formal proof of consistency of Lean or its selected classical axioms.

### Compatible union is an additional obligation

Separate certificates for E1 and E2 do not justify merging arbitrary environments
with equal textual names. The merged environment must admit **one** realization
rho. A conservative merge rule requires the same base/profile; injective exact
identity-to-name bindings; exact agreement on every shared name's category,
ordered universes, type, semantic references and reduction mode; and identical
commitments for shared computational bodies/inductive groups. Its combined
derived-premise graph must satisfy the same well-founded validity rule.

Two opaque data constants with the same type but different hidden implementations
are not interchangeable; independently certified facts about them may conflict
if their identities are collapsed. Keep distinct proof-instance identities as
distinct sealed names even when their judgments match. Optional judgment-level
aliases require an explicit theorem/interface rule, not an unchecked name merge.
Given compatible exact bindings and discharged imports, prove the single-
realization/typing-preservation lemma for the union. This is the semantic
interface obligation that the cryptographic relation must actually certify.

## What can and cannot be erased

| Remote declaration | Safe intended local view | Data that remains needed / limitation |
|---|---|---|
| Certified theorem in Prop | Exact typed derived premise with no old proof body | Type/interface support; certificate-bound assumption discharge; some proof-dependent computation may cease reducing |
| Transparent definition | Exact type and body, or an explicitly different sealed abstraction profile | Its body may be required for definitional equality; body commitment alone cannot perform reduction |
| Opaque constant returning data | Potential sealed typed constant only with a certified inhabiting implementation and a specified abstraction boundary | Not automatically a theorem; runtime evaluation/extraction still needs an implementation; do not coalesce distinct data implementations by type |
| Inductive group | Kernel-validated group and generated computational interface, or a separately certified exact rule installation path | Positivity, universe/parameter constraints, constructors, recursors, projections and reduction rules; they are not merely theorem headers |
| Base axioms/quotient primitives | The exact adopted base | Cannot silently expand because a peer supplies a certificate under another policy |

For example, if a new proof closes a goal by reducing `f x`, it needs f's
definition and any further conversion support. Erasing f's body turns that
conversion into a stuck term. One useful optional abstraction is to expose a
sealed function plus **certified equation theorems**, so clients rewrite
explicitly rather than rely on hidden delta reduction. That changes the
authoring/interface contract and must not be portrayed as preserving every
existing Lean source proof unchanged.

For remote inductives, making each constructor/recursor an arbitrary axiom
does not reproduce their computational behavior; installing unchecked
recursor reduction rules is much more dangerous. The initial scale seam should
retain ordinary kernel group construction from finite declarations (proof
dependencies already sealed), not add a universal unchecked environment import.

Exact term/type signatures can themselves have large support closures. This
design removes **proof-history** replay, not the information-theoretic cost of
reading the actual statement or the computation needed by the current goal.
Stock Lean stores the environment it checks against; its ordinary constant
lookup is not an authenticated remote oracle. A demand-loaded environment or
a certificate for an entire remote checking computation would be another
specified mechanism, not a capability already supplied by `addDeclCore`.

## Concrete local authoring/verification seam

A smallest defensible new lane would follow this sequence:

1. Fetch selected interface bytes and their aggregate certificate. Resolve the
   exact semantic/type/computation support needed locally. Validate canonical
   encodings, all public commitments and the certificate relation/profile.
2. Enter each verified sealed theorem into a **private derived-premise
   registry**, keyed by its complete identity and interface. Refuse any
   missing certificate, policy mismatch, altered type or duplicate binding.
3. In a fresh checking environment, install the typed premise with
   `axiomDecl`, `isUnsafe := false`, and `doCheck := true`. Keep imported
   derived premises distinct from foundational axioms and unverified offers.
4. Build the ordinary source frontend from the same exact selected bindings.
   Imported Init syntax/tactics remain authoring conveniences, not remote
   mathematical authority. Expose the certified constant through both relevant
   Lean environment maps; retain no-overwrite/type/universe checks.
5. Elaborate and capture only genuinely new declarations plus exact used
   certified leaves. Check the new proof with the kernel against those leaves.
   No `sorryAx`, `debug.skipKernelTC`, `addDeclWithoutChecking`, unsafe/partial
   declaration or arbitrary extra axiom is an allowed substitute.
6. Produce a new certificate whose statement binds the new proof/interface
   and discharges its certified leaves to B. Export new proof data when wanted,
   but do not require reconstructing absent historical proof bodies merely
   to satisfy an old full-batch inverse export format.

The registry is checked evidence, not a caller-controlled whitelist of
`DTMKN.*` names. Do not globally add remote names to `allowedAxioms`. A name
prefix or signature is not proof. Current `screen`, `sameSourceBinding`,
`collectExtension`, replay-plan closure and inverse-export assertions must
gain a separately versioned interface-aware rule; their existing strict lane
must not be weakened in place or described as having checked omitted bodies.

`collectAxioms` will normally see these local placeholders as axioms unless
given authenticated derived-assumption summaries. Provide two honest reports:
the immediate certified premises used, and the transitively certified base
assumption policy. Never use an untrusted imported axiom-summary extension as
the reason to accept a certificate-backed theorem. Literal absence from a
diagnostic `#print axioms` output is not the security property.

Logical FoundationID may remain tied to the same mathematical base if nothing
logical changes, but a new `CheckingProfileID`/certificate-relation and import
schema must bind this distinct evidence path. Determine explicitly whether
the present Foundation/native-rules encoding also requires a version change;
do not reuse its old full-replay promises merely because the base axioms match.

## Security and engineering TCB

The base Lean kernel and exact foundational semantics remain trusted. The new
lane additionally trusts: certificate verifier and cryptographic assumptions;
correct binding of the certified computation to its program/runtime; canonical
decoder and interface commitment logic; a gate that installs only verified
derived premises; and environment realization/composition correctness. A
succinct proof of a buggy permissive checker is still a proof of that buggy
computation. This does not remove existing kernel/toolchain/host assumptions.

The present prohibited `sorryAx`, `Lean.trustCompiler`, `Lean.ofReduceBool`,
`Lean.ofReduceNat` and other reserved bypasses must remain excluded by the
certified relation, not only by the receiving UI. The current permitted
`propext`, `Classical.choice`, `Quot.sound` policy is a logical policy; proof
verification security is a different cryptographic assumption layer. State
both instead of calling the resulting system “trust-free.”

Interface integrity is not proof-data availability. Producers/custodians may
retain full proofs for auditing, recertification under a new kernel version,
or clients needing proof-sensitive computation. A cold ordinary receiver need
not download them merely to use a sealed certified theorem. Withholding may
prevent those stronger services without letting a false theorem pass.

## Next central discriminants, not another broad campaign

Before selecting an implementation, root should pin one certificate backend
and one exact theorem-interface relation. Then a small bounded test should
establish all of the following, with proof bodies genuinely absent at receiver:

- A fresh local theorem substantively uses a certified remote theorem and
  passes actual kernel checking against its sealed interface.
- A fresh downstream verifier validates its composed certificate without
  fetching either ancestor proof body or traversing the certificate history.
- Type/foundation/universe/order/kind tampering, extra base axiom, name rebinding,
  unanchored cyclic certification and an uncertified `False` premise refuse.
- Missing conversion data and an `Acc.rec`-sensitive example either succeed
  under the specified sealed profile or clearly refuse; no claimed universal
  compatibility and no hidden fallback downloading the whole history.
- Increase the hidden predecessor proof-history size while holding the same
  selected interface/new theorem fixed. Measure cold receiver bytes/CPU and
  separately all prover work. A warm cache result does not meet this test.

Until those tests run, the result here is a specific feasible interface design
direction plus explicit outstanding obligations—not a scalable implemented
release or a measured succinct-proof win. Finishing optional prior growth
campaigns cannot substitute for resolving this acceptance boundary.

## Concrete first native discriminator: draft, no runtime authority

Root requested a smaller **native-only** test while the real certificate backend
is unresolved. It must be described as a locally checked premise-registry and
proof-erasure experiment, never as cold remote cryptographic verification.

### Proposed profile: SEALED-THM-1

This is an explicitly proposed profile, not selected product behavior:

- External derived constants must be kernel-confirmed Prop theorems, with exact
  full interface/type/universe/reference bindings and valid selected evidence.
- Local premise declarations are body-free, safe `axiomDecl` entries installed
  only through the evidence-gated registry; every new proof still uses actual
  `addDeclCore(..., doCheck := true)`.
- Selected base primitives and ordinary computational definitions retain their
  exact adopted behavior. A theorem requiring external proof-body reduction
  is unsupported in this profile.
- There is **no automatic download/replay of all ancestry** when conversion
  sticks. Report `NEEDS_TRANSPARENT_EVIDENCE`/`SEALED_CONVERSION_UNSUPPORTED`.
  A client may instead use a separately certified equation lemma and ordinary
  propositional rewriting, or deliberately select a different transparent
  audit profile. Either choice has its own recorded costs and claims.
- The native discriminator accepts only `LOCAL_KERNEL_EVIDENCE_V0`, rooted in
  its trusted local issuer run. It has no successful SNARK/STARK verification
  branch. An alleged remote cryptographic certificate is unsupported, not
  silently treated as this local evidence.

### Fixed mathematical chain

Use the existing pinned foundation's equality and function application, with
two independently ordered universe parameters for the imported interface.
No new axiom, custom inductive, proof-search challenge or network service is
needed. These are the proposed exact declaration headers, in the fresh reserved
test namespace `ScaleIface`; the final executed source/encoding still needs its
ordinary root review and pins:

```lean
theorem ScaleIface.L.{u, v}
    {alpha : Sort u} {beta : Sort v} (f : alpha -> beta)
    {x y : alpha} (e : x = y) : f x = f y

theorem ScaleIface.M.{u, v, w}
    {alpha : Sort u} {beta : Sort v} {gamma : Sort w}
    (f : alpha -> beta) (g : beta -> gamma)
    {x y : alpha} (e : x = y) : g (f x) = g (f y)

theorem ScaleIface.N.{u, v, w, z}
    {alpha : Sort u} {beta : Sort v} {gamma : Sort w} {delta : Sort z}
    (f : alpha -> beta) (g : beta -> gamma) (k : gamma -> delta)
    {x y : alpha} (e : x = y) : k (g (f x)) = k (g (f y))
```

These are signatures, deliberately not complete executable theorem commands.
The concrete roles are:

1. **Issuer A:** genuinely kernel-check a polymorphic congruence theorem
   `L : forall {alpha : Sort u} {beta : Sort v} (f : alpha -> beta)`
   `    {x y : alpha}, x = y -> f x = f y`.
   Its proof is a usual equality elimination. Record exact checked type,
   universe order, canonical reference and proof commitment. Keep the full
   proof in evaluator evidence, but do not put it in B's input packet.
2. **Consumer B:** install L from the selected local-evidence registry as a
   sealed typed premise. Kernel-check and export M, whose selected proof is
   `ScaleIface.L g (ScaleIface.L f e)` with the appropriate universe instances.
   It contains two actual applications of the exact L constant. Bind a fresh local checked-evidence
   record to M; the new result is not merely a copied declaration header.
3. **Consumer C:** receive only M's exact interface/local-evidence record plus
   the base, not L's proof or M's proof body. Kernel-check N using the selected
   proof `ScaleIface.M f (fun b => k (g b)) e`; its beta conversion needs no
   remote theorem body. Verify actual proof-body
   dependence on M in the checked output.

Freeze the actual fully expanded canonical types, ordered universe parameters,
exact names and encodings before any run. The headers above are **not** a ready
executable harness or permission to specialize carriers after failure. This is
a kernel-interface test, not evidence of mathematical
novelty, proof-search advantage or useful-growth benefit.

The first root-owned harness should use a trusted locally bound issuer result
and an explicit exact-input allowlist; B/C may not manufacture evidence records
or read A's old proof files. Process roles, arguments, file maps and actual
proof absence must be audited. Procedural/file-input separation is not claimed
to be a hostile OS sandbox unless actual confinement is added and qualified.
Hashing a record is not certificate verification: its authority here comes
solely from the separately audited local issuer execution.

### Fixed refusal table

Use fresh native environments for these bounded cases; do not edit successful
evidence records or broaden the accepted profile after a failed case:

| Control | Required result |
|---|---|
| Missing local checked-evidence record | Refuse before adding the derived premise |
| Altered type/universe order/identity or alleged certificate bytes | Refuse exact binding; no inference from a matching textual name |
| Well-typed but unproved `False` offered as a premise | Refuse absence of permitted evidence; kernel acceptance as an axiom is not success |
| A data declaration such as `n : Nat` under theorem category | Refuse non-Prop interface even if the issuer can supply an inhabitant |
| Attempted base-name or existing-constant replacement | Refuse namespace/identity collision before mutation |
| `sorryAx`/extra foundational axiom/unsafe or partial source | Refuse the original base/policy gate |
| Known proof-sensitive conversion requiring an absent theorem body | Explicit unsupported/body-required refusal, with no ancestry fallback |

The last case needs its own exact small `Acc.rec`/well-founded-reduction source
selected before launch. Source comments establish a real concern but do not
supply a verified reproducer; do not invent an expected successful reduction
without checking the actual pinned kernel behavior. An ordinary transparent-
definition-body omission can separately establish the basic conversion refusal.
The retained `notes/analyses/CP-001H-proof-computation-and-reconstruction.md`
is source-backed/paper analysis, not an executed native counterexample; the
parallel reviewer confirmed it records no Lean execution. Reuse its reasoning
without relabeling it as an already-run refusal control.

### Bounded scope and honest result

Proposed allocation: one new isolated test harness build and at most four
fresh native invocations (issuer, B, C, refusal table), using existing selected
runtime/finite process containment. Proposed whole-allocation ceilings are
600 wall seconds,450 inclusive Job CPU seconds,4096MiB private commit and eight
processes, with at most300 wall seconds for the single build and60 wall seconds
for each native invocation. These are prospective hard ceilings, not measured
cost predictions or permission to loosen existing product limits. Root must
review/adopt the final caps, source and runner pins before execution; no run
is authorized by this note. No product patch, managed node initialization,
publication/network campaign or repeated predecessor suite is required merely
to answer the native compatibility question.

A pass would establish locally grounded theorem-interface erasure and checked
subsequent contribution through stock Lean for the selected sealed subset.
It would **not** establish an external certificate verifier, recursive
certificate soundness, cold-network scalability, public publication compatibility
or a release claim. The old full-package inverse-export protocol still needs
an explicitly redesigned interface-aware counterpart before product integration.

### Exact proposed source and process split

Use a fresh root-selected experimental directory, for example
`experiments/lean-sealed-interfaces-01`, only after selection. No directory or
source file is created by this proposal. Keep source roles distinct:

| Proposed file | May contain | Must not contain/import |
|---|---|---|
| `Common.lean` | Generic interface parsing, exact local-evidence gate, Prop/type/universe/policy validation, fresh base reconstruction, body-free importer, kernel-check/output helpers | L/M/N proof constructors; issuer/consumer modules; preinstalled derived mathematical constants |
| `Headers.lean` | Closed L/M/N type expressions, exact expected universe order and test names; no installed declarations | Any L/M/N proof expression or dummy proof |
| `IssuerA.lean` | L's genuine equality-elimination proof and local checked-output/evidence emission | B/C modules or fabricated derived evidence |
| `ConsumerB.lean` | M's new expression `L g (L f e)` and publication-like delta export | L's proof, A module, A saved environment or A proof archive |
| `ConsumerC.lean` | N's new expression `M f (fun b => k (g b)) e` and delta export | L or M proof values; A or B module; saved ancestor checking environments |
| `Refusals.lean` | Fixed altered/missing permit/header cases, fresh environments and expected refusal labels | A/B/C module imports or a successful certificate-verifier mock |

`ConsumerB`/`ConsumerC` construct their new kernel expressions against runtime
sealed entries. Do **not** compile them by importing `IssuerA` or `ConsumerB`
just to make the mathematical constants visible at Lean source compile time.
The desired expressions can name the exact runtime constants using `Expr.const`
and be checked with the existing kernel API. This tests the kernel/import seam;
ordinary frontend source elaboration is a later, separately stated integration
gate, not something this narrow expression harness has already established.

Compile separate role executables or run separate role modules whose complete
dependency graph contains only Common/Headers and pinned foundational support.
The build dependency manifest must show that the B binary/module does not link
the A proof module and C does not link A/B proof modules. A single executable
containing all three proof constructors behind role flags would fail the strict
input-separation intent even if its selected branch did not call them.

Common may reuse the selected foundation receiver, including its fixed base
proofs; those are B, not the new L/M proof ancestry. The actual checking
environment starts with `mkEmptyEnvironment 0` and the exact adopted base. The
environment in which the harness implementation itself was compiled is not
silently adopted as mathematical checking authority. Record exact base counts
and namespace membership before every derived import.

The runtime boundaries are:

1. A starts fresh, checks L and exits. Its complete proof and native evidence
   remain under root/evaluator ownership. Root audits them and creates an exact
   B input packet containing only the base references, L's full interface and
   a pinned `LOCAL_KERNEL_EVIDENCE_V0` authorization. The authorization's origin
   is this audited local run, not a hash pretending to be cryptographic proof.
2. B starts as a separate native process with only its declared B input packet,
   proof-free support and M's new expression. Before import, L is absent. After
   import, L is precisely `.axiomInfo` with `value? = none`, the bound type and
   universe order; no other stored L declaration exists. B checks M and exports
   its new proof/interface, used-premise list and exact resulting environment
   projection. Then B exits and its local evidence is audited.
3. Root creates C's packet from the audited M interface/local authorization,
   not from B's full environment or M proof package. C starts fresh: both L
   and M absent before import; afterwards only M is present as a body-free
   derived premise. L need not be installed because M's type does not mention
   it. C checks N, whose checked new body must actually apply M.

At B's beginning, all its newly supplied proof-bearing input bytes concern M,
not L. At C's beginning, all such input bytes concern N, not L/M. Registry
records contain commitments/authority metadata, never an embedded old body or
a serialized old environment. No input field instructs a consumer to fetch an
ancestor archive. An observed non-Prop declaration or missing type support
refuses before any new premise is installed.

Evidence must bind distinct process IDs/start records, exact per-role input
file/module maps, input byte counts, explicit file-read allowlists, and before/
after environment inventories. Audit all consumer file reads through the
small reviewed support path; no source/body lookup back into evaluator paths.
Merely showing different Python objects, clearing one dictionary entry or
counting zero calls to an API while old values remain loaded is insufficient.
Exact byte-string absence alone is also weak: the module graph/environment
inspection must rule out alternative embedded representations of old proofs.

Same-host root archives are preserved, not deleted to create a misleading
isolation claim. A bounded Windows Job limits resources, not filesystem access;
unless actual access-control isolation is selected and tested, the claim is
audited input/process/environment separation for trusted experimental code,
not inability of malicious code to open some other file on the host.

This split does not add calls beyond the proposed four native invocations.
The “one build” means one bounded build allocation for the disjoint role
artifacts and shared proof-free support, not one executable embedding all roles.

## Inspected local sources

Line numbers are navigation aids for these held bytes, not external literature
citations. Bundled source comments reveal implementation intent/API behavior;
this inspection does not prove source-to-binary compiler correctness.

| Source | Relevant places | SHA-256 |
|---|---|---|
| source16 native/AgentReplayCore.lean | collectExtension117; checkedAdd373; receiveOrdinary385; receiveGroup419; receive496 | `dc875826d4ccc9ffecaf7762694f10de495235c0aa40f8fb87272316c7fa2b96` |
| source16 native/AgentClient.lean | sameSourceBinding152; sourceEnvironment160; checkSource214 | `059bc05ef03ea32827f926bbd2e7a37094277581eae39fb360a6adaafea7ba6b` |
| Lean/Declaration.lean | declaration records and constructors | `fcb928c1686f0655279a790f92bd61f8c0d6df3be51a5eccaa2880de058e5e24` |
| Lean/Environment.lean | addDeclCore701; subsumesInfo2245ff; kernel check/whnf2790ff | `ee364e4788ce0560c87f621eeb3c4c3dfec62e8db4e15e099fd80e6adc533b86` |
| Lean/AddDecl.lean | module theorem-as-axiom export; checked private declaration | `7e6e74107d8f0116dff7cde2de3e60ed556bbab3ca56309311ea90dfc931bd40` |
| Lean/Util/CollectAxioms.lean | imported summaries versus direct body traversal | `64f340d42f18c51ee83527f03fa69cc26415dd71dcf7fe71031b7760be90007d` |

Here “source16” is `product-local/foundation-byte-reuse-source-16`; Lean sources
are under `software/runtime/lean-4.34.0-windows/src/lean`. The exact native/base
policy was also inspected in `native/BootstrapSupport.lean` and `py/codec.py`.
