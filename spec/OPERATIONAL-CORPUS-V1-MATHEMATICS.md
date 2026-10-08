# Operational corpus v1: mathematical artifacts and native checking

Date: 2026-09-19. Status: proposed concrete paper specification for independent review. No implementation, completed bootstrap build, or executable conformance run is claimed.

This document selects a practical Lean 4 native-exchange design and a smaller core conformance profile. It specializes [the corpus-first knowledge contract](FORMAL-KNOWLEDGE-CONTRACT-v0.md) and L1 of [the layered decomposition](../notes/analyses/CP-001C-layered-problem-decomposition.md). Existing checkpoints remain historical and unchanged. V1 contains no human-intention fields, unfinished-mathematics registry, producer work-item requirement, or research scheduler. External clients choose their own methods and investigations.

## Selected profile and supported mathematics

The intended operational profile is **Lean-Native/v1**, specified in the practical-profile section below. It supports native safe definitions, theorems, opaque declarations with checked bodies, mutually/nested inductive groups, structures and projections, and an explicit standard-Lean foundation allowance. The smaller **Lean-Expr-6/v1** is retained as an initial conformance/test profile, not a claim that a six-type fragment alone fulfills the project's diverse mathematical scope. Unless explicitly extended below, the core encoding and checking contract is shared.

The core conformance profile **Lean-Expr-6/v1** selects:

- Lean 4's native kernel at official release tag `v4.22.0`, resolved on inspection to source commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.
- A receiver-created empty kernel environment with trust level zero.
- Exactly six pinned elementary inductive groups: `True`, `False`, `Eq`, `Nat`, `Bool`, and `List`, introduced through the checked kernel inductive-declaration operation.
- No logical axioms, quotient initialization, externally supplied inductive declarations, unsafe definitions, partial definitions, opaque declarations, or mutually recursive declaration blocks.
- External contributions are acyclic safe definitions and theorem derivations represented as a small native-expression DAG, plus typed envelopes for modules and native refutations.
- Every external declaration is passed through the checked native kernel operation. No peer-supplied `.olean`, source file, tactic, macro, plugin, compiled library, or executable is loaded by the verifier.

The release is a deliberately fixed historical target, not a claim that it is the latest Lean version. Its exact source and admitted behavior are inspectable. Changing that target is a new locally adopted profile, not a mutable dependency.

The core supports arithmetic, finite/list reasoning, higher-order functions, and parameterized algebraic theorems. Recursion is represented using admitted recursors. An algebra interface can be a telescope of carrier, operations, unit, and law assumptions; it need not be a newly declared `Monoid` record. That is useful for checking the protocol's simplest end-to-end examples, but it is not the practical library-compatibility strategy. Ordinary Lean structures, inductive families, classical developments, and exported library closures use Lean-Native/v1. No claim of universal mathlib coverage is made before an exporter and representative native replay have been qualified.

## Why direct native replay is the acceptance path

The pinned official source exposes `Lean.Kernel.Environment.addDeclCore`, described as type-checking a declaration before adding it. It also exposes an explicitly unchecked declaration-addition operation. The C++ kernel implementation distinguishes those paths and checks theorem types and values on the checked path. Consequently, “the tool produced a Lean environment” is not itself sufficient evidence that every declaration was checked.

Ordinary module import builds an environment from serialized constant information and may also load environment extensions or plugins under its import options. A native constant lookup checks against declarations already in the environment; it is not the protocol's proof that each imported declaration body has been replayed from an independently accepted closure. Setting a trust-level option is not permission to treat arbitrary serialized environments as safe input.

Compiling untrusted source in a sandbox can protect host resources under the sandbox assumptions. It does not by itself establish the logical provenance of the resulting environment: source-level metaprogramming, options, unchecked APIs, axioms, or extensions are still a larger acceptance boundary. This profile avoids that boundary. Source compilation and artifact extraction occur outside mathematical acceptance; the receiver consumes inert native data and rechecks it.

The verifier never calls `addDeclWithoutChecking`, a raw environment insertion API, an elaborator, `evalConst`, a compiler, module import on peer material, or a plugin loader while processing a submission. “Native” here means native kernel expressions, not execution of publisher-native machine code.

## Foundation, seed, and source binding

### Fixed logical rules

The selected logic includes the pinned Lean kernel's dependent function types, universes, impredicative `Prop`, definitional proof irrelevance, definitional equality and reduction, and the admitted inductive rules. These are trusted foundational rules even in the core profile, whose explicit axiom set is empty. Empty axiom footprint is not a proof of kernel correctness or an unconditional consistency theorem. The practical profile's explicit additional foundation is specified separately below.

### The six seed declarations

The following signatures describe the exact seed groups. Binder names in this table are explanatory; the seed encoding uses indexed binders. `Type u` abbreviates `Sort (u+1)`.

| Order | Group and declaration type | Parameters | Constructors |
|---|---|---|---|
| 0 | `True : Prop` | 0 | `True.intro : True` |
| 1 | `False : Prop` | 0 | none |
| 2 | `Eq.{u} : (A : Sort u) -> A -> A -> Prop` | 2: A and the first compared value | `Eq.refl : (A : Sort u) -> (a : A) -> Eq A a a` |
| 3 | `Nat : Type` | 0 | `Nat.zero : Nat`; `Nat.succ : Nat -> Nat` |
| 4 | `Bool : Type` | 0 | `Bool.false : Bool`; `Bool.true : Bool` |
| 5 | `List.{u} : Type u -> Type u` | 1: the element type | `List.nil : (A : Type u) -> List A`; `List.cons : (A : Type u) -> A -> List A -> List A` |

The names, signatures, and constructor order follow the selected declarations in the pinned `src/Init/Prelude.lean`. The `Eq` descriptor presents its first compared value as a uniform parameter, with the second as its index. Each group is a separate safe `Declaration.inductDecl`; mutual and nested groups are absent.

Initialization starts with an empty environment, inserts those six descriptors in table order using the checked kernel, and obtains constructor/recursor declarations from the kernel itself. The only externally referenceable seed exports are each listed type, its listed constructors, and its generated `.rec` recursor: twenty exports in total. Sorting those twenty qualified names by their canonical name-path encoding defines stable `seedExportIndex` values. Generated recursor types, universe-parameter order, and reduction metadata are the deterministic output of the pinned kernel applied to these fixed descriptors. They are recorded in the bootstrap inventory and checked against it when a verifier image is admitted.

No `casesOn`, `recOn`, `noConfusion`, `Nat.add`, `List.append`, theorem, or other Prelude declaration is admitted merely because it exists in Lean's ordinary library. Such helpers may be contributed later as ordinary checked definitions or theorems if their native bodies fit the fragment. No `.olean` from Prelude is imported into the mathematical environment.

### Seed descriptor encoding and authority

`SeedProfile` encodes source commit bytes, ordered bootstrap declaration descriptors, and permitted export names. A core group descriptor consists of its name components, ordered universe parameters, parameter count, complete declaration type, ordered constructor names/types, and `isUnsafe = false`. Seed-local references use export names, with self-reference allowed only in constructor positions accepted by the kernel's inductive checker. This bootstrap representation is not a remotely extensible foundation-authority mechanism.

The descriptor terms use the binder/level encoding defined below, with seed references rather than content-addressed external references. This table and the pinned native recursor-generation operation determine the bootstrap inputs and outputs; no profile field means “whatever the current installation contains.”

The source-pinned bootstrap inventory, canonical descriptor bytes, their ContentIDs, exact generated export types, verifier image hashes, and reference verdicts must be produced and inspected during implementation qualification. They have not been generated in this concept phase. This is a release conformance gate, not a permission to choose the seed later. A mismatch with the selected signatures or recursor output blocks activation of that verifier image.

Profile adoption is a local software-authority action. A peer advertising a `SeedProfile` or `LogicProfile` does not cause the receiver to load it or accept its axioms. Every other profile is `UNKNOWN(UNSUPPORTED_PROFILE)` until explicitly supported and locally adopted.

### Profile commitments and noncircular bootstrap representation

`LogicProfile` payload is `[releaseTagBytes,sourceCommitBytes,seedProfileID,featureSet,syntaxLimits]`. The release tag is ASCII `v4.22.0`; the commit is its twenty raw hexadecimal-decoded bytes. `featureSet` is a sorted duplicate-free list of numeric feature codes: 0 core expressions, 1 safe inductive contributions, 2 projections, 3 checked opaque contributions, 4 standard explicit axioms, 5 native string literals. Core selects `[0]`; practical selects `[0,1,2,3,4,5]`. `syntaxLimits` is `[maxExprNodes,maxLevelNodes,maxTermDepth,maxUniverseArity,maxPayloadBytes,maxNatMagnitudeBytes]` with the limits below. Checker executable identity remains a separate assessment field: profile identity commits to specified behavior, not one compiled binary.

`SeedProfile` payload is `[sourceCommitBytes,orderedBootstrapDescriptors,sortedExportNamePaths]`. A native name path is an array of components `[0,utf8Bytes]` or `[1,uint64]`, for string or numeric components; string bytes must encode Unicode scalar values canonically. No component is inferred from an alias. Export paths are sorted by their canonical CBOR bytes. A bootstrap descriptor is a locally authorized inert representation of one of the pinned safe definition, theorem, opaque, inductive, exact foundation-axiom, or quotient-initialization declarations. Its native expressions use the same node/level grammar but replace external constant references by `[6,namePath]` and omit the `LogicProfileID` field. Bootstrap binders retain their exact native binder-info codes, because kernel bootstrap checks such as quotient initialization compare expected seed types. Ordinary contribution binders remain normalized as specified below. Names, ordered universe parameters, full types/values, and declaration-kind metadata are all committed in descriptor bytes. Quotient initialization has the single descriptor `[4]`; axioms have `[5,namePath,universeArity,typeDAG]`; ordinary bootstrap definition/theorem/opaque kinds use tags 0/1/2 and `[tag,namePath,universeArity,typeDAG,valueDAG]`; inductive bootstrap tag 3 uses `[3,universeArity,numParams,[[typeName,typeDAG,[[ctorName,ctorTypeDAG],...]],...]]`. All non-axiom safety flags are fixed safe, and definition hints use the fixed reconstruction rule below. Bootstrap DAGs are `[levelNodes,exprNodes,root]`, with binder nodes `[tag,binderInfo,domain,body]`, `binderInfo` in 0 default, 1 implicit, 2 strict-implicit, 3 instance-implicit. All seed free parameters are indexed.

Thus SeedProfile contains no reference to itself or LogicProfile, and LogicProfile can safely commit to SeedProfile. The release qualification must publish actual complete canonical seed descriptors and inventory, not just this human-readable selection rule. This concept has not generated those bytes and therefore does not claim an assigned or production-ready LogicProfileID.

## Practical Lean-Native/v1 profile

This is the selected operational target, not a future promise that core-only deployments support arbitrary libraries. It changes the admitted fragment while retaining independent receiver replay. All native behaviors below are pinned to the same Lean release; changing those behaviors produces another profile.

### Standard foundation and checked compatibility bootstrap

The practical foundation permits precisely three explicit axiom schemes with their exact pinned native types:

- `propext : {a b : Prop} -> Iff a b -> Eq a b`.
- `Classical.choice.{u} : {A : Sort u} -> Nonempty A -> A`.
- `Quot.sound.{u} : {A : Sort u} -> {r : A -> A -> Prop} -> {a b : A} -> r a b -> Eq (Quot.mk r a) (Quot.mk r b)`.

The displayed types elide only mechanically inferred parameters of `Eq`/`Quot.mk`; bootstrap descriptors contain every native argument. `Quot`, `Quot.mk`, `Quot.lift`, and `Quot.ind` enter through the locally authorized native `quotDecl` initialization operation, not remotely supplied `ConstantInfo`. Their primitive quotient computation/elimination rules are a distinct foundation feature. The three axioms are not claimed proved by checking their types; they are explicit locally selected assumptions. `sorryAx`, `Lean.trustCompiler`, `Lean.ofReduceBool`, `Lean.ofReduceNat`, unsafe compiler axioms, and every other peer axiom are excluded. A new admitted axiom scheme requires a new locally adopted foundation profile.

The compatibility bootstrap includes the six core types, `Iff`, `Nonempty`, these three axioms, quotient primitives, and the exact safe native dependency closure of the following reserved-name roots in the pinned Lean sources: `Nat.add`, `Nat.sub`, `Nat.mul`, `Nat.pow`, `Nat.gcd`, `Nat.mod`, `Nat.div`, `Nat.beq`, `Nat.ble`, `Nat.land`, `Nat.lor`, `Nat.xor`, `Nat.shiftLeft`, `Nat.shiftRight`, `String`, `String.mk`, `Char`, and `Char.ofNat`. Closure includes all type/body/constructor dependencies and selected proofs; it excludes executable annotations, compiler output, and unrelated declarations. Encountering any other axiom or unsafe/partial dependency blocks this proposed bootstrap rather than importing it silently. Each non-axiom declaration is replayed through the checked native path. The exact source-derived safe descriptors, order, permitted exports, and generated recursor inventory must be frozen in SeedProfile and independently inspected at qualification. A compiled library is an untrusted extraction source, not authority for those descriptors.

This extra bootstrap is substantive: the pinned kernel recognizes certain native names for natural arithmetic/literals, strings, equality, and quotients. Renaming every constant to a hash loses some intended native behavior; allowing publishers to bind arbitrary definitions to reserved names can change its meaning unsafely. Therefore only exact locally frozen bootstrap declarations retain those native names. Ordinary contributed names are generated from IDs. The kernel source's reserved-name inventory must be audited during qualification; the listed roots are the selected intended coverage, not evidence that an exporter or bootstrap has already passed that audit. In particular, string literal expansion must see exactly the expected checked `String`/`Char`/`List` support declarations. If this qualification fails, the practical release is not ready; a six-seed demonstration does not satisfy this gate.

Per-result footprints distinguish `UsedExplicitAxioms`, primitive/rule features, and the baseline adopted kernel/profile. A receiver can decline a proof that reaches choice while accepting another proof of the same practical-profile JudgmentID that does not. This does not claim the receiver has proved the stronger foundation consistent or that its installed environment literally lacks unused axioms. A strict constructive deployment can adopt a separate restricted profile and require fresh profile-bound objects/replay.

### Safe inductive groups without identifier cycles

Add `InductiveGroup` (type `0x0018`) with payload `[LogicProfileID,universeArity,numParams,typeDescriptors]`. `typeDescriptors` is an ordered nonempty list of `[typeDAG,constructorTypeDAGs]`, where constructor types retain their order. These DAGs are inline `[levelNodes,exprNodes,root]`, share the declared universe arity, and have no free term variables. They use ordinary external constant references plus the special local constant reference `[5,typeIndex]` for a type being defined in this same group. The index is bounded by the group size; no local constructor or local recursor reference is admitted as an input. The native inductive checker determines whether each local recursive occurrence is well formed and strictly positive. Limits are the ordinary term limits plus at most 4,096 type descriptors and 65,536 constructors per group and the same 64 MiB object cap.

The GroupID commits to these binder-indexed descriptors before any global native name is chosen. Reconstruction uses `DTMKN.i.<fullGroupID>.t<index>` for each type and its child `c<index>` names for constructors, then submits one safe `Declaration.inductDecl` with the group's shared universe list and parameter count. This gives mutual/nested groups a noncircular content identity: local references are bound indexes, not attempted references to their not-yet-known GroupID. Ordinary definitions/theorems still cannot introduce logical-support cycles.

Only the native kernel constructs `InductiveVal`, `ConstructorVal`, and `RecursorVal` information and reduction rules. The receiver does not trust a submitted recursor type, positivity certificate, or raw `ConstantInfo`. External member references are `[3,GroupID,selector]`, where selectors are `[0,typeIndex]` for a type, `[1,typeIndex,constructorIndex]`, `[2,typeIndex]` for its `.rec`, or `[3,k]` for the kernel-generated auxiliary first-type `.rec_k`, with k positive. The pinned source assigns these auxiliary recursors for nested groups. The receiver checks that the selected member actually exists in the generated group inventory with its exact kind. It records the actual complete generated inventory and scans types and recursor rules for external dependencies. It rejects unexplained extra native names or undeclared external dependencies.

Structures are single-constructor inductive groups with ordinary projection expressions/functions. No peer structure registration or elaborator extension is needed for kernel acceptance. Elaborator-generated `casesOn`, `recOn`, `noConfusion`, equation lemmas, projection functions, and related helpers are exported separately as checked definitions/theorems; they are not all automatically produced by the kernel. A nested group is supported through the pinned kernel's actual nested-inductive operation, not by assuming its auxiliary recursors have the same names in a different Lean version.

### Projections, strings, and opaque declarations

Practical `NativeTermDAG` additionally admits node `[8,structureRef,fieldIndex,baseExprIndex]` for `Expr.proj`. `structureRef` is either a seed reference naming an inductive type or a group reference with selector `[0,typeIndex]`. The native checker checks the structure type, one-constructor condition, field index, dependent field types, and Prop-elimination restrictions. A supplied record label or field name is not evidence.

Node `[9,utf8Bytes]` is a native string literal, with valid shortest UTF-8 encoding of Unicode scalar values and a 1 MiB byte limit. Native String/Char support comes exclusively from the pinned bootstrap above. String literals are inert values, never source paths or commands.

Add `OpaqueDefinition` (type `0x0019`) with payload `[LogicProfileID,universeArity,typeTermID,valueTermID]`. This distinct kind is reconstructed with safe `opaqueDecl`, generated name `DTMKN.o.<fullOpaqueID>`, `all = [generatedName]`, and its actual body independently checked. Its external constant reference is `[4,OpaqueID]`. The exact body remains part of identity and footprint even though native reduction does not unfold the opaque constant. Missing bodies are `UNKNOWN(MISSING_BODY)`; the exporter cannot replace them by an axiom or transparent definition. Mutual safe source definitions/theorems must be exported as their lowered acyclic kernel declarations. Native `mutualDefnDecl` is unsupported because its variants require unsafe/partial definitions in the pinned API.

### Practical replay and semantic-context extensions

For this profile, ReplayManifest payload is `[root,sortedWitnessPairs,sortedDefinitionIDs,sortedGroupIDs,sortedOpaqueIDs]`. Root is `[0,ProofID]`, `[1,DefinitionID]`, `[2,GroupID]`, or `[3,OpaqueID]`. The root kind and reachable closure determine the profile; disagreement rejects. All lists are lexicographically sorted by full canonical ID bytes, duplicate-free, and exactly reachable; root declarations occur in their corresponding list. Every group is one atomic replay vertex: its bound internal inductive recursion is not a cross-artifact proof dependency. The graph of these vertices, safe definitions, opaque declarations, and selected proofs must be acyclic. Replay ties use canonical ContentID bytes.

Practical SemanticContext permits DefinitionID, JudgmentID, GroupID, and OpaqueID refs. For an inductive member reference it includes the group's full descriptors and external dependency closure; for opaque references it conservatively includes the exact type/body dependency closure. Generated recursor/member metadata is derived, not separately trusted. Group-local references never escape their owning descriptor. SemanticContext excludes choices of theorem witness as before, but the actual selected axioms/rule uses and proof-only groups are visible in ReplayID and the result footprint.

The core substitution argument for proof-only safe definitions/theorems must not be stretched to say every fresh inductive type can be syntactically inlined. For the practical profile, soundness instead assumes the correctness of the pinned safe inductive-extension and quotient rules as well as the explicitly adopted axioms, and records the entire checked extension actually used. Statement identity being proof-independent does not certify a smaller foundation or context of checking.

Practical Module payload is `[LogicProfileID,sortedDefinitionReplayPairs,sortedRootProofReplayPairs,sortedGroupReplayPairs,sortedOpaqueReplayPairs]`. Every pair contains its artifact ID followed by ReplayID; pairs sort by canonical pair bytes, duplicates forbidden. Every export therefore has an exact selected ReplayManifest for current import, not merely a declaration ID. No collection manifest grants execution authority. Every root can be independently submitted; a module is optional.

### Workable library export path and explicit limitations

An untrusted exporter runs in a producer-controlled Lean environment at the selected version, with all desired source/library imports available there. It walks complete native declaration closures, collects actual theorem/opaque bodies, groups inductive members by their original native mutual-group information, reconstructs the original inductive descriptors from type/constructor information, and emits normalized descriptors and source-to-content maps. Generated nested recursors are associated with the native group, not reintroduced as axioms. The receiver regenerates/checks the group and all dependent terms. Incorrect reconstruction, wrong universe ordering, omitted proof, or a mismatched generated member therefore causes failed replay rather than hidden trust in the exporter.

Statement-addressed theorem names can introduce an artificial replay cycle even when the original source graph is acyclic. For example, source `p2 : P := p1` with an earlier `p1 : P` maps both closed statement types to the same JudgmentID. Selecting p2 as that judgment's witness while retaining a reference to that same judgment in its body creates a forbidden self-edge. The exporter must expand the earlier p1 proof body at that occurrence, including explicit universe and argument substitution, or choose p1 itself as the exported witness. It emits the resulting new native proof term and lets the receiver check it; it does not bypass cycle detection or rename the statement arbitrarily. The same expansion resolves same-JudgmentID collisions along a finite source proof graph when complete earlier bodies are available. Expansion may increase resource cost or exceed bounds; this is a compatibility/resource outcome, not evidence that the original acyclic Lean proof was circular mathematics. A genuinely cyclic selected artifact map is still rejected.

Some compiled-module configurations can hide theorem/opaque values or retain them only in a separate/full environment. Their type signatures alone are insufficient. The concrete fallback is to elaborate the original sources in the producer's own environment with proof bodies available, or use an exporter hook at declaration creation; the verifier still receives only inert native data. No claim is made that every arbitrary `.olean` supplies enough data for this extraction. Producer elaboration may execute tactics/plugins in the producer's chosen sandbox; that is a producer operational risk, not a receiver proof-acceptance step.

Noncomputable classical mathematics is supported through the exact three-axiom allowance and safe native terms. Proofs using `native_decide`-style compiler-trust axioms do not qualify merely because the source compiled; the producer must provide another proof with an admitted footprint or a later explicitly different verifier profile. Kernel `decide` proofs using ordinary reduction are eligible. Libraries at a different Lean version require re-elaboration/export at the pinned version or an explicit separately adopted versioned profile. Exporting an equivalent reformulation gives a distinct artifact unless exact canonical identity is preserved.

The practical release gate is successful, separately replayed examples covering ordinary algebra structures and instances, quotient constructions, classical proofs, dependent families, mutual and nested inductives, native strings and natural arithmetic, and a representative pinned mathlib slice with every proof body available. A failure report must name the exact unsupported feature or missing data. This paper design selects the data path and obligations; it does not claim that these examples were executed or that every library theorem already fits the configured resource bounds.

## Canonical encoding and common content identifiers

The mathematical and network layers share one CAS envelope. Mathematical object types occupy the low range listed below; network/service types occupy `0x8000..0x80FF`.

The canonical payload language is an RFC 8949 deterministic CBOR subset containing only definite-length arrays, unsigned integers in `0..2^64-1`, and byte strings. Integers and lengths use their shortest encoding. Maps, negative integers, text strings, floats, CBOR tags, indefinite-length forms, duplicate alternative encodings, and trailing bytes are forbidden. Fixed arrays have exactly the schema's arity. Optional fields use an explicitly defined tagged union; they are not omitted or assigned an implicit default.

For a payload b of byte length n, type t, and schema v,

\[
d=\operatorname{SHA256}(
\texttt{ASCII("DTMKN-CAS")}\Vert\texttt{00}
\Vert\operatorname{u16be}(t)\Vert\operatorname{u16be}(v)
\Vert\operatorname{u64be}(n)\Vert b).
\]

A ContentID is the canonical CBOR array `[1,t,v,d]`, where algorithm 1 is SHA-256 and d is exactly 32 bytes. All types in this profile use schema 1. IDs are typed values, not unqualified digest strings.

| Type | Object |
|---|---|
| `0x0001` | LogicProfile |
| `0x0002` | SeedProfile |
| `0x0010` | NativeTermDAG |
| `0x0011` | Definition |
| `0x0012` | SemanticContext |
| `0x0013` | Judgment |
| `0x0014` | Proof |
| `0x0015` | ReplayManifest |
| `0x0016` | Module |
| `0x0017` | NativeRefutation |
| `0x0018` | InductiveGroup, practical profile only |
| `0x0019` | OpaqueDefinition, practical profile only |

Large objects can be transported in network chunks, but a chunk ID or byte-manifest ID is not the mathematical object's ID. The receiver verifies the complete canonical payload commitment after reconstruction. Compression on transport cannot alter canonical payload bytes or their identity.

### Collision handling

An incoming payload whose computed ContentID differs from the requested ID is rejected as corrupt/misaddressed data. It does not disable an already retained correct object.

If two distinct canonical payloads both verify to the same complete ContentID, the receiver has positive collision evidence. It preserves the incident bytes under unambiguous local incident storage, quarantines that content identity and current dependent reliance, and reports `UNKNOWN(CONTENT_ID_COLLISION)` or an integrity error. It must not choose one payload by popularity, arrival order, or lexicographic order. A malicious claim of a collision without the two verifying payloads cannot cause this transition.

The safety statement is conditional on no successful hash-binding failure; computational collision resistance supplies only the selected cryptographic bound, not an absolute or infinite-time guarantee. Migration after a demonstrated break cannot retrospectively disambiguate old references without additional retained binding evidence.

## Native term representation

### Universes

A term carries an ordered universe-parameter arity. Its level DAG supports only:

| Tag | Level |
|---|---|
| 0 | zero |
| 1 | successor of a referenced earlier level |
| 2 | maximum of two referenced earlier levels |
| 3 | impredicative maximum of two referenced earlier levels |
| 4 | parameter index below the declaration's universe arity |

Universe metavariables are forbidden. Parameter indexes map to receiver-generated names `u0`, `u1`, and so on. No algebraic quotienting of universe expressions is performed for identity; equivalent level expressions can have different term IDs. The native checker still applies its own definitional level equality when checking.

### Expressions

`NativeTermDAG` has payload `[LogicProfileID,universeArity,levelNodes,exprNodes,rootExprIndex]`. The permitted expression nodes are:

| Tag | Fields | Native interpretation |
|---|---|---|
| 0 | `[0,index]` | bound variable, with de Bruijn index 0 nearest |
| 1 | `[1,levelIndex]` | `Sort` |
| 2 | `[2,constantRef,levelIndexes]` | fully explicit constant application at universe levels |
| 3 | `[3,functionIndex,argumentIndex]` | application |
| 4 | `[4,domainIndex,bodyIndex]` | lambda |
| 5 | `[5,domainIndex,bodyIndex]` | dependent function/forall |
| 6 | `[6,typeIndex,valueIndex,bodyIndex]` | let binding |
| 7 | `[7,magnitudeBytes]` | natural-number literal |

In the core profile, `constantRef` is exactly one of `[0,seedExportIndex]`, `[1,DefinitionID]`, or `[2,JudgmentID]`. The practical profile adds group/opaque references specified above. Group-local tag 5 is valid only inside its own inline group descriptor; bootstrap-local tag 6 is not accepted in external contributions. A term cannot name a source module, filesystem path, mutable alias, arbitrary native name, or external function.

Natural-number magnitude is big-endian without leading zero bytes; zero is the empty byte string. The receiver maps it to the native natural literal constructor. The accepted representation contains no machine-width truncation. The pinned kernel's natural-number literal/arithmetic support and underlying arithmetic runtime are consequently part of the TCB.

Binder names are omitted, binder information is always reconstructed as explicit/default, and lets use a fixed conservative `nondep = false` setting. These choices concern elaboration metadata; all elaboration has already occurred outside acceptance. Every implicit argument and typeclass instance needed by the term is explicit in the native application structure.

Free variables, expression metavariables, metadata nodes, quotation syntax, tactic syntax, executable IR, macros, and arbitrary extension nodes are unsupported. The core additionally excludes projections and string literals; the practical profile admits their precise nodes above. Clients may externally remove metadata or transform a proof, but the resulting native artifact must pass ordinary replay. No receiver-side unproved lowering is assumed.

### Canonical DAG and bounds

Within each term object, children precede parents. The canonical order is first-visit left-to-right postorder from the root with exact structural sharing; identical node records are represented once. No unreachable node is allowed and the root is the final expression node. Level nodes are likewise reachable from expression levels and canonically ordered. Canonicality checking uses the encoded DAG, memoization, and bounded comparisons; it must not unfold an exponentially large tree.

Each term has at most 1,048,576 expression nodes, 65,536 level nodes, 4,096 structural depth, 1,024 universe parameters, and 64 MiB canonical payload bytes. Every integer/index additionally satisfies its schema range. A natural literal has at most 1 MiB magnitude bytes. These are profile syntax limits, not statements that larger mathematical proofs are invalid. A later profile can choose other limits with a distinct ID.

The default admitted closure is bounded by 512 MiB, 16,384 objects, and declaration-dependency depth 512, subject to the receiver's tighter budget. A receiver cannot exceed the network hard envelope of 8 GiB, 65,536 objects, or dependency depth 1,024 by choosing a larger local budget. Syntax depth and declaration-dependency depth are different bounds.

Scope is checked at every use position. A shared open subterm may occur under different binder depths; checking it once at one depth is insufficient. An equivalent implementation can compute the required binder depth bottom-up and verify it at roots: the requirement for bound variable k is k+1; application takes the maximum; lambda/forall reduce the body's requirement by one while retaining the domain's requirement; let treats its type/value outside and body inside the new binder. Level-parameter bounds are separately checked.

## Meaning identity, judgment identity, and proof identity

These distinctions are normative. A module label, human alias, transport source, reviewer, service principal, or original investigation is not a mathematical identity component.

### Safe definitions

`Definition` payload is `[LogicProfileID,universeArity,typeTermID,valueTermID]`. Both terms are closed in term variables; parameters are represented by explicit Pi/lambda binders. A construction is a definition with its exact type and value. A definition returning `Prop` or a proof still obeys the same checking and footprint rules.

Its `DefinitionID` commits to type, body, profile, and exact referenced declarations. Renaming it externally does not change that ID. Changing its body, even to a definitionally equal one, creates another ID. The profile does not attempt universal semantic canonicalization.

The receiver reconstructs a native `defnDecl` with a generated name, safety `safe`, fixed reducibility hint `regular 0`, and `all = [generatedName]`. It does not honor publisher-supplied hints or declaration flags. Recursive definitions must already be expressed using admitted recursors or earlier safe definitions; a definition cannot refer to itself.

### Semantic contexts

`SemanticContext` payload is `[LogicProfileID,sortedSemanticRefs]`. A semantic reference is a typed `DefinitionID` or `JudgmentID`. Its set is the exact transitive closure needed to interpret the judgment's telescope types and conclusion: definition references contribute both type and body references; judgment references contribute only their exact telescope/conclusion references. Seed references are covered by the profile and are not repeated here.

The receiver recomputes this set from the supplied immutable objects. Missing, extra, duplicate, mistyped, or cyclic references reject the claimed context manifest. All lists are ordered lexicographically by canonical ContentID bytes. The context cannot silently include an unproved theorem as a trusted assumption; native insertion of any referenced theorem additionally requires a selected checked proof in the replay closure.

### Contextual judgments

`Judgment` payload is `[SemanticContextID,universeArity,contextTypeTermIDs,conclusionTermID]`.

The context is an ordered telescope. Entry k may use precisely the preceding k variables. The conclusion may use the entire context. There are no stored local definitions; an external exporter substitutes them or represents their meanings through explicit accepted definition references. Binder names and source-level implicitness have no identity role.

The native checking type is the closed Pi closure of the telescope and conclusion, but the wire identity retains the context/body split. This is essential for exact refutation scope. Two judgments with different hypotheses, different quantifier placement, different definition references, different universe arity/order, or different profiles have different JudgmentIDs unless their canonical payloads actually coincide.

An isolated `Judgment` record is a typed statement descriptor, not an established theorem. V1 may fetch it as inert closure data; it does not acquire checked-corpus status without evidence. There is no persistent public unsolved-conjecture registry created by receiving these descriptors.

### Proofs and replay selections

`Proof` payload is `[JudgmentID,proofTermID]`. The proof term has that judgment's universe arity and may use its complete telescope. The receiver closes it with the matching lambda telescope before native theorem insertion.

Different proof terms can have the same JudgmentID and different ProofIDs. Imported theorem constants refer to JudgmentIDs, not a mutable preferred proof and not a publisher name.

The exact proofs selected to justify those constants belong to a separate `ReplayManifest`:

`[root,sortedWitnessPairs,sortedDefinitionIDs]`, where `root` is `[0,ProofID]` or `[1,DefinitionID]` in the core profile. Practical roots additionally admit `[2,GroupID]` and `[3,OpaqueID]`, and their manifests have the additional group/opaque lists specified above.

Each witness pair is `[JudgmentID,ProofID]`. The manifest includes the root judgment for a proof root, and exactly one chosen proof for every theorem reference transitively needed by the root's terms, statement, and reachable declarations. Each mapped ProofID must name that exact JudgmentID. Each listed declaration is exactly one reachable declaration, including the root in its kind's list where applicable. There are no extra pairs/declarations and no duplicate keys. Lists sort by canonical ID bytes; witness pairs sort by JudgmentID then ProofID. The receiver recomputes reachability and rejects a mismatch.

A complete package may carry separate replay manifests for alternative proofs. One manifest cannot ambiguously choose two proofs for the same judgment. The same ProofID can be replayed under distinct valid manifests; those are distinct ReplayIDs and distinct validation keys. A ProofID alone does not promise complete availability or a currently acceptable basis.

This separation avoids a hash cycle between theorem naming and its proof. Judgment identity does not include its own proof. Proof identity refers to an already determined judgment. Replay identity then commits to the selected finite evidence closure, including the exact typed root.

### Proof-only conservative auxiliaries

A proof may use definitions or lemmas not mentioned in its statement's SemanticContext. Its replay environment therefore contains that semantic context plus the selected proof auxiliaries. In the core profile, every such auxiliary is an acyclic checked safe definition or theorem and introduces no axiom or inductive rule; it is a conservative extension for the original statement language under the usual substitution argument. Practical-profile inductive/opaque auxiliaries instead obey the complete-extension and explicit-footprint soundness conditions above; this elementary substitution argument is not asserted for them.

Validation records both `SemanticContextID` and `ReplayID`. It does not pretend that the kernel literally checked against a smaller environment that was not used. The core profile's proof-only definition/theorem auxiliaries can be eliminated by substitution of their checked definitions/derivations. This is a conditional metatheoretic argument about that restricted profile, not an unproved claim about arbitrary Lean extensions. Practical statement identity is still proof-independent, while all actually used extension rules and explicit assumptions remain in the assessment.

### Native names and no self-reference

The receiver assigns external definitions names under `DTMKN.d`, theorem constants under `DTMKN.j`, and practical opaque constants under `DTMKN.o`, followed by the hexadecimal canonical full ContentID. Practical group type/constructor/recursor names use the `DTMKN.i` mapping specified above. Seed exports retain their pinned native names. The mapping is injective subject to the content-binding assumptions and cannot be chosen by a publisher.

No declaration contains its own generated name in its identity payload. It refers to prior content IDs. Even if an adversary supplies cyclic identifiers, the combined selected definition/proof graph is checked for cycles before kernel insertion. A cryptographic fixed-point difficulty is not used as a substitute for that graph check.

### Modules

Core `Module` payload is `[LogicProfileID,sortedDefinitionReplayPairs,sortedRootProofReplayPairs]`, where pairs are `[DefinitionID,ReplayID]` or `[ProofID,ReplayID]` respectively. The practical profile adds group/opaque pairs as specified above. Pairs sort lexicographically by their canonical CBOR bytes, with no duplicates. It is a bounded collection manifest, not an execution/import command. `Import(ModuleID,exportKind,index)` uses the explicit kind tag 0 proof, 1 definition, 2 group, or 3 opaque and a zero-based index into that list to resolve the exact root/replay pair; the module adds no mathematical authority.

A module permits batch transfer and shared closure. Human-readable aliases, if an external client keeps them, are not part of this profile's mathematical objects. Adding, removing, or replacing an export creates a new ModuleID without renaming unchanged content.

## Grounding and exact dependency closure

Build the selected replay graph with vertices for reachable definitions and chosen proofs, extended in the practical profile by checked opaque declarations and atomic inductive groups. Edges point from each vertex to every external declaration or selected theorem proof referenced by its type, telescope, conclusion, constructor types, generated-member rules, or value; referenced bodies are traversed transitively. The manifest must select all such theorem witnesses. Bootstrap exports refer to their pinned checked or explicitly authorized foundation closure.

The graph must be finite and acyclic. Replay uses a topological order, breaking ties by canonical ContentID bytes. Every imported theorem is inserted only after its selected proof has passed checked native replay. There is no “declare theorem type first as an axiom” shortcut.

Both profiles reject mutual theorem-support cycles, definition cycles, and mixed cycles where a definition needs a theorem whose proof needs that definition. Practical safe mutual/nested induction inside one checked group is an admitted kernel rule, not such an unsupported external support cycle. Circular module plumbing does not become a proof rule.

A manifest is complete only when the receiver's syntactic traversal and native reconstruction resolve every constant and seed export. Runtime network lookup, mutable names, callbacks to the producer, and ambient installed library imports are forbidden during checking. A missing object yields nondecision, not a guessed dependency or a theorem assumption.

### Closure layers

| Closure | Included or excluded in this profile |
|---|---|
| Mathematical | Seed profile; every semantic object, definition, selected proof, term DAG, and replay manifest |
| Native checker | Locally selected executable image, source revision, build/runtime profile, and fixed options |
| Producer elaboration/build | Not needed for acceptance; may exist only in an external client's workspace |
| Transport/retention | Exact payloads or reconstructible bytes under L2 contracts; a CID alone is insufficient |

Cold replay needs the complete mathematical closure and an independently obtainable compatible checker distribution. A source archive alone is not an already runnable checker. Binary portability and reproducible builds remain separate release qualifications.

## Axiom and trust-feature footprint

The core allowed explicit axiom set is empty. The practical allowed set is exactly the three schemes above, separately from primitive quotient rules. The kernel's foundational features and checked bootstrap are identified in `LogicProfileID`; they must not be mislabeled as a proof that no trusted assumptions exist.

The receiver traverses all referenced types, proof/value terms, definition bodies, and selected theorem proofs, not merely constants exercised by one reduction trace. This produces a conservative syntactic footprint, including dead or unused references when they occur. It is not a claim of globally minimal logical assumptions.

Every reachable declaration must be a pinned bootstrap export or a permitted completely checked native contribution. In core, external kinds are only safe definitions and selected theorems. Practical also permits checked groups and safe opaque bodies. Any unadmitted axiom, unsafe/partial constant, unsupported declaration kind, unexpected primitive, or missing declaration prevents acceptance. In particular, `sorryAx`, compiler-trust/native-evaluation axioms, and hidden custom axioms are admitted by neither profile. `Classical.choice`, `propext`, and `Quot.sound` are excluded by core but explicitly available under the practical profile and subject to the receiver's result-footprint policy.

The word “forbidden” is relative to the selected profile/policy, not a claim that classical mathematics or another foundation is invalid. An explicit Pi-bound hypothesis remains visible conditional mathematics; it cannot be dropped from the judgment.

Footprint output records exact reachable declaration IDs, selected proof IDs, bootstrap exports, actual primitive/rule features, and the actual reached explicit axiom set. Core's explicit set is empty; practical's is a subset of the three admitted schemes. Bootstrap exports are not footprint black boxes: their internal types/bodies and selected proof dependencies are traversed against the frozen inventory. Publisher-provided dependency or axiom reports are never authoritative. A proof copied from a library is subject to the same traversal and replay as any other proof.

## Parser and validation stages

All expensive work follows the receiver's existing bounded grant/reservation/execution-claim mechanism. This section specifies mathematical effects, not a second resource ledger.

| Stage | Required action | Possible stopping result |
|---|---|---|
| 0. Bounded envelope screen | Check common type/version/length frame under aggregate ingress allowance | Not admitted; unsupported profile; malformed envelope |
| 1. Canonical decode and ID | Decode only the selected CBOR subset, check exact arities/ranges/canonicality, recompute ContentID | Reject malformed or mismatched bytes |
| 2. Inert closure acquisition | Fetch exact references into bounded staging; validate every payload ID | Unknown missing/unavailable closure or resource limit |
| 3. Native fragment and scope | Validate term/level DAGs, permitted constructors, index scopes, exact profile agreement, and size/depth limits | Reject malformed native input; unknown unsupported fragment |
| 4. Recompute manifests | Recompute SemanticContexts, selected witnesses, and complete reachable declarations; reject extraneous/missing mappings | Reject manifest inconsistency, or unknown unavailable inputs |
| 5. Grounding and footprint | Detect cycles; verify permitted seed refs and declaration kinds; determine deterministic replay order | Reject cyclic support/forbidden dependency |
| 6. Checked seed construction | Create empty environment and replay selected pinned bootstrap; only exact locally authorized axioms/quotient initialization may enter; validate inventory | Error on local image/bootstrap mismatch |
| 7. Native declaration replay | Reconstruct exact terms and supported declaration kinds; insert through checked `addDeclCore` with receiver limits; regenerate inductive members | Accept each declaration, reject type/evidence mismatch, bounded nondecision, or execution error |
| 8. Result reconciliation | Bind actual typed root, kind-appropriate optional JudgmentID/ProofID, ReplayID, checker/image/options, policy, and measured footprint; ensure no unrecorded dependency | Accept exact mathematical artifact or fail closed |
| 9. Local admission/current reliance | Apply current local incident/retention policy and epoch rules before exposing current strict reliance | Admitted result, or current nonacceptance/unknown |

A reusable verified seed environment may be cached only as receiver-created state under an exact checker/profile key; cache restoration is within the local TCB and recovery model. It is never a peer environment import. Likewise, cached declaration checks must bind exact ProofID/ReplayID/checker/policy and current incident state; “same theorem name” is not a cache key.

### Native reconstruction details

Each Definition becomes a checked safe `defnDecl`. Each Proof becomes a checked `thmDecl` whose type is the closed Pi telescope and whose value is the corresponding lambda closure. The kernel verifies that the theorem type is in `Prop`, that the value has that type, that universe instantiations have the correct arity, and that applications/reductions respect the exact imported declarations. For a non-propositional construction, use a Definition rather than pretending it is a theorem.

Definitions are checked before insertion; a failed definition cannot reserve a usable mathematical name. Theorems are checked after all selected dependencies. The verifier uses synchronous checked operations with no unresolved asynchronous declaration promises. It never relies on an elaborator's error-recovery theorem or a fallback `sorry` value.

### Outcome taxonomy

Validation values remain `ACCEPT`, `REJECT(reason)`, `UNKNOWN(reason)`, and `ERROR(reason)`; `UNCHECKED` is a pre-attempt state. A separate service outcome may be `NOT_ADMITTED` before mathematical work is authorized.

- `ACCEPT`: all declared checks completed for this exact artifact, closure, checker, and policy.
- `REJECT`: a completed check establishes malformed encoding, profile-limit violation, wrong manifest, cycle, forbidden dependency, ill-typed declaration, or invalid supplied evidence. It does not assert that the conclusion has no other proof.
- `UNKNOWN`: missing closure, unsupported profile/fragment, known bounded incompleteness, cancellation, time/fuel/memory limit, or insufficient authorized resources. Unsupported new inductive types are not called false mathematics.
- `ERROR`: unexpected native crash, local invariant violation, bootstrap/image mismatch, sandbox failure, or integrity alarm prevents a trustworthy result.

Unknown critical object types are not reinterpreted as the nearest known type. Dynamic resource exhaustion is nondecision; a fixed syntactic profile bound can be a profile-conformance rejection. Resource accounting finalizes under the inherited rules for every outcome.

## Standalone contribution and import semantics

A producer may submit a Proof, Definition, or practical-profile InductiveGroup/OpaqueDefinition plus its exact ReplayManifest and closure; a Module of such objects; or a NativeRefutation envelope backed by the required native proof replay. No originating question, human intention, or unsolved-task record is requested.

The root union and profile-specific manifest arity above are mandatory and never inferred from a bare digest. ProofID/JudgmentID are present only for a proof root; a group or construction is not falsely presented as a proof. Network publication, current status, validation assessments, and retention all bind the selected ReplayID for every root kind.

A checked standalone declaration is eligible for the local mathematical corpus even if it has no observed use. Retention, indexing, service, and replication require their separate receiver-authorized resources. A node declining storage does not refute the contribution.

When importing a theorem, a client obtains its exact JudgmentID and a selected native proof/replay closure. The theorem's native constant has the closed Pi type; applying it requires explicit argument and premise terms in the client's new proof. The new output is checked under the same rules. Matching aliases, printed names, embeddings, or a foreign `ACCEPT` cannot discharge this instantiation.

When importing a definition, the exact body and type remain authoritative. A different implementation with a proved equivalence is a different DefinitionID plus a checked relation, not a replacement behind the same ID.

### Returning knowledge to an ordinary local Lean agent

The corpus returns a neutral native package: selected profile, typed root, ReplayID, complete inert declaration/term objects, and the locally scoped assessment. It does not return a peer `.olean` for trusted direct import. A producer-side import adapter reconstructs the same generated constant names in a matching pinned Lean environment and uses checked declaration insertion there before the agent builds on the result. A clean matching environment is the safe compatibility baseline; if an existing environment contains incompatible reserved/bootstrap names, the adapter must use an isolated matching environment or produce a separately checked translation, not overwrite meanings behind existing names.

After that, the local agent can use exact generated names directly in explicit Lean terms, ask tactics/LLMs to search with those declarations, and create private human-friendly aliases, notation, instance registrations, or simplifier hints. Such elaborator metadata is a client-local usability layer, not part of mathematical authority. The corpus can distribute inert advisory metadata, but executable macros/plugins, auto-running tactics, or unreviewed instance/rewriting registrations are never required to accept the theorem. Full source ergonomics may require reconstructing useful local metadata; merely having native kernel declarations is sufficient for explicit term reuse but not a claim of seamless source-level library UX. Any new contribution produced by these local tools is exported/rechecked through the same mathematical contract.

## Scoped negative evidence, counterexamples, and actual inconsistency

V1 selects **native negative evidence**, not a second model-finder or SAT/SMT checker inside this profile.

For a contextual judgment J with telescope Γ and conclusion φ, define `Neg(J)` by preserving the exact profile, ordered Γ, and universe parameters, and replacing only the body by `φ -> False`. Constructing that body performs the required capture-avoiding lift under its new function binder. The SemanticContext is recomputed and must agree on all non-seed semantic meanings.

The historical object name `NativeRefutation` has payload `[targetJudgmentID,negativeProofID,negativeReplayID]`. It is valid only when the negative Proof's JudgmentID is exactly the canonical `Neg(J)`, its ReplayManifest is rooted at that proof, and the complete native replay accepts. Its precise meaning is **same-context opposing evidence**: a derivation of Γ ⊢ φ → False. It is not a proof that Γ ⊢ φ is underivable or that an already checked conditional theorem is invalid. An arbitrary model-checker's output is not such a Lean proof.

In the v1 peer protocol this envelope is a bounded **local derived relation**, not another ReplayManifest root kind and not a generic network CAS-read capability. A peer publishes the negative proof's ReplayID as an ordinary proof root. After native replay, a receiver may recognize a conclusion syntactically of the form `φ -> False`, recover the domain φ under the identical telescope/universe parameters, rebuild the canonical positive Judgment/SemanticContext, and check exact `Neg` correspondence before storing its scoped-opposition annotation. This reconstruction does not assert a proof of the target or create a public unsolved-task registry. A locally supplied NativeRefutation envelope is merely a proposed relation to check against those same exact objects. It is retained, if useful, within bounded local relation metadata attached to the negative replay; it has no independent publication/retention authority and does not enlarge that replay's network read scope. Nodes may rediscover the relation from the negative native proof without fetching this annotation object.

The distinction is essential. If Γ contains `(h : P, k : P → False)`, then both Γ ⊢ P and Γ ⊢ P → False are valid, and together they prove Γ ⊢ False. The context is inconsistent/uninhabited; the kernel has not failed, and neither conditional derivation should be retracted. Even a context `(h : False)` supports every conclusion soundly as conditional mathematics. Consequently, a contextual opposition edge is searchable mathematical information, not by itself a current-reliance veto or checker incident.

For an empty context, accepted opposite proofs under a compatible joined dependency basis can compose to a closed proof of `False`. For a nonempty context, the same holds only if an additional checked substitution supplies actual closed inhabitants for every telescope entry, respecting dependent types and earlier entries. The receiver must replay the composed closed contradiction under its exact finite union of dependencies and allowed axiom/rule footprint; incompatible profiles or conflicting witness choices cannot be silently combined. A closed contradiction supports a **basis inconsistency incident**. It does not identify which theorem, axiom, checker, adapter, or implementation is at fault. A locally adopted incident policy may suspend affected reliance while retaining the evidence and historical records.

An external counterexample finder can construct a native proof of the negation and submit it. For a closed target `forall x : A, F x`, a witness a and a proof of `F a -> False` can be assembled into the native term `fun h => n (h a)` and checked. The witness need not be interpreted from prose; it appears in exact native evidence or a separately checked construction.

The context/body split must not be erased. A proof of `not (forall Γ, φ)` is not generally a proof of `forall Γ, not φ`. In particular, finding one n for which `F n` fails can refute the closed universal statement, but does not provide `Γ=(n:Nat) ⊢ not F n` for every n. To express the closed universal statement, publish that distinct Judgment explicitly and target its negation. No automatic opposition edge is created across this scope change. A checked proof of the closed negation defeats that exact closed proposition under its assumptions; it still does not make a different conditional theorem invalid.

NativeRefutation uses exact negative evidence as a sufficient initial rule. It does not claim completeness for every semantic countermodel notion. `ERROR`, `UNKNOWN`, a failed proof search, and missing data never create a refutation.

## Current status and alternative proofs

A validation assessment binds the tuple

\[
(\operatorname{rootID},\operatorname{ReplayID},\operatorname{LogicProfileID},
\operatorname{CheckerImageID},\operatorname{OptionsID},
\operatorname{PolicyID},\operatorname{ResultFootprintID}).
\]

Budgets/metering and the local snapshot/reliance epoch accompany that assessment; they are not theorem identity. A historical kernel acceptance is distinct from current strict reuse. A locally admitted checker/basis incident or closure loss can block current reliance while leaving the immutable proof bytes and historical check record intact. Same-context negative evidence alone is not such an incident; the distinctions and closed-contradiction rule above apply.

Current strict reuse traverses one exact selected native declaration/proof DAG and the relevant locally adopted incident state at a coherent epoch. Scoped opposition may be displayed alongside the judgment without invalidating sound conditional derivations. Reuse fails closed on paths affected by an actual applicable incident. If a complete alternative ReplayID remains acceptable, the same JudgmentID may still be usable through that alternative. Finding an invalid proof does not refute its judgment.

The v1 corpus does not accept arbitrary remote Horn-rule support graphs as replacements for native proofs. Structural dependency edges come from the native terms/manifests. A node can translate this verified structure into the inherited Core support representation, but every formal composition step is already backed by the native replayed derivation.

No exact opposition lookup can assert “there is no contrary evidence anywhere.” It can inspect the receiver's locally admitted exact evidence under its declared observation scope. Bounded scans may return `UNKNOWN`; failure to find an alternative proof in a heuristic index is not a mathematical nonexistence conclusion.

## External exporter and library interoperability

An external client can use a ordinary Lean environment, source files, tactics, LLMs, or other tools to produce candidate native expressions. A proposed exporter:

- reads elaborated declaration types and bodies from that client's environment;
- replaces local names by exact DefinitionID/JudgmentID references;
- resolves every theorem reference to a selected native witness;
- indexes bound variables/universe parameters and removes non-authoritative binder names;
- normalizes only the representation choices specified here;
- emits a complete acyclic manifest and reports any unsupported declaration or expression.

This exporter is untrusted. The receiver independently decodes, recomputes dependencies, reconstructs native terms, and checks them. A fabricated type, omitted axiom, erroneous metadata erasure, wrong de Bruijn index, or incorrect source mapping therefore cannot create acceptance unless the receiver's own checks fail.

Library import is not automatically available for arbitrary Lean libraries. New source-defined structures, inductive families, quotient constructions, opaque constants, or classical axioms are outside Lean-Expr-6/v1 but supported along the practical Lean-Native/v1 route above when complete supported closure is available. Unadmitted axioms, unavailable bodies, changed compiler versions, and resource limits remain explicit compatibility constraints. An external client may construct a supported alternative formalization and prove its claims; the system records exactly that new artifact and does not claim it imported the original statement unchanged.

Safe recursive definitions compiled into admitted recursors and safe helper definitions can fit the selected profile. Definitions depending on unadmitted recursors cannot. Export failure is a compatibility result, not a judgment that the library is wrong.

## Version shifts and mathematical duplicates

- Exact canonical duplicates have the same ContentID and are idempotent. Repeated publication creates no fresh mathematical authority or storage entitlement.
- Alpha-renaming binders or external aliases changes no canonical term. Reordering actual telescope binders or universe parameters changes identity unless the canonical bytes remain identical; transport between them requires checked evidence.
- Definitionally equal expressions may have different IDs. Kernel conversion can make a particular application valid without creating a global identity quotient.
- Alternative proofs share a JudgmentID only when the exact profile/context/body match. Their ProofIDs and selected ReplayIDs remain distinct.
- A new native kernel/source profile creates a new LogicProfileID, new seed identity, and profile-bound derived IDs. Nothing is silently relabeled “latest.”
- Replaying old mathematical content under a new profile produces new assessments and, where representation/profile identity changes, new objects plus an explicit checked relation. Old artifacts remain interpretable under their old profile if the necessary checker distribution is retained.

A receiver may adopt a different profile admitting new axioms or kernel features, but that cannot change an existing profile's meaning. Practical safe contributed inductive groups use its already adopted checked inductive-extension rule; they are not remotely authorized new axiom schemes. No publisher message can extend the receiver's foundation.

## Trusted computing and execution boundary

The local acceptance TCB contains:

- the canonical decoder, bounds/scope checks, DAG reconstruction, hashing, and exact-reference resolver;
- the seed descriptors, their local authorization, and the native seed-construction/export-inventory check;
- the pinned Lean kernel, runtime/FFI, native natural-number arithmetic, generated-name adapter, and declaration constructor adapter;
- complete dependency/footprint extraction and replay-map reconciliation;
- the local policy/current-epoch evaluator and authoritative admission store;
- the compiler/toolchain and executable image supply chain to the extent not displaced by independently verified builds;
- the operating system, hardware, process isolation, and resource enforcement needed for the claimed execution integrity.

Proof search, producer elaboration, external source export, foreign storage, indexes, models, and remote signatures are outside this boundary. They can propose arbitrary bytes.

The checker worker receives only a bounded read-only closure and fixed local checker code. It has no network access, publisher-controlled search path, dynamic plugin loading, writable shared library path, or tool-execution permission. Its output is a bounded typed result channel. OS process isolation contains faults and resource use; it does not prove that a buggy kernel is logically sound. Unexpected worker or runtime integrity failure produces no acceptance.

Verifier diversity remains useful but is not obtained by running the same binary under many public keys. A future independent checker must specify precisely which subset and trust assumptions it validates. Its availability is not assumed for this initial path.

## Paper examples and counterexamples

### Independent arithmetic accumulation

In the six-group seed, define addition by recursion on its second argument:

\[
\operatorname{add}(m,n)
=\operatorname{Nat.rec}
\bigl(\lambda\_.\operatorname{Nat}\bigr)
m
\bigl(\lambda k\ r.\operatorname{Nat.succ}(r)\bigr)
n.
\]

The complete definition is closed by lambdas over m and n and is admitted as a safe Definition. Let J have context `(m : Nat)` and conclusion `Eq Nat (add m Nat.zero) m`. Its proof body is `Eq.refl Nat m`; native reduction of the recursor at zero makes the types definitionally equal. This is a paper derivation, not a claim that this document ran a checker.

A second investigator imports the DefinitionID and checked proof, defines `twice n = add n n`, and proves `twice Nat.zero = Nat.zero`, either by direct reflexivity or by an explicit application of the first theorem after unfolding the exact definition. A third can define a list sum using `List.rec`, reusing add. No theorem request, record type, human-intent field, or mathlib installation is needed.

The direct-reflexivity and imported-lemma proofs can have distinct ProofIDs for the same exact JudgmentID. Whether one is smaller or cheaper depends on its complete ReplayManifest and costs; same conclusion does not imply disposable redundancy.

### Algebra without a new structure declaration

A monoid-law development can quantify over `(A : Type u)`, `(op : A -> A -> A)`, `(e : A)`, and explicit associativity/left-unit/right-unit proofs. A list fold is defined using `List.rec`. Its concatenation theorem is a contextual theorem over those binders. A group refinement adds inverse and inverse-law binders; those are visible assumptions, not hidden axioms.

This supports formal abstraction within the core conformance profile. The practical profile additionally supports actual checked record declarations and native projections, so ordinary algebraic hierarchies need not be forced into telescope-only encodings. Neither representation is automatically identified with mathlib's `Monoid` or `Group`; exact exported declarations or explicit checked relations determine interoperability.

### Practical structure-based accumulation

A first client exports a safe single-constructor `MonoidLike (A : Type u)` group with operation, unit, associativity, and unit-law fields. The receiver checks its constructor telescope and regenerates its recursor. Local notation and the original record name are not required to establish that group; its type is named by GroupID plus the type-member selector. A second client imports the group and defines a list fold using its checked operation/unit projections, then proves a fold-over-concatenation theorem with all structure and element-type parameters explicit. A third specializes that exact theorem to a checked concrete monoid instance. The specialization is another checked native term, not trust in an alias or an embedding-similarity match.

This example uses the practical features needed by real Lean algebra hierarchies: record types, dependent fields, native projections, generated recursors, and ordinary helper theorems. Source-level typeclass search can assist each local client after client-side instance registration, but that search is neither a consensus mechanism nor the evidence of the resulting specialization. A faulty exported instance fails its own law proofs or the downstream theorem check. These are paper-level interface cases; no structure or proof was implemented/executed in this concept phase.

### Required failure distinctions

| Input or event | Required result |
|---|---|
| Peer supplies a `.olean` containing an asserted theorem | Unsupported input; never import it into the native environment |
| Peer supplies Lean source with `#eval` or a tactic | Unsupported input to acceptance; external client may export supported native data |
| Proof includes `sorryAx` hidden under a helper definition | Reject forbidden transitive dependency |
| Claim descriptor is supplied without a selected proof | It remains inert; no theorem constant is installed |
| Two selected theorem proofs require one another | Reject cycle before native insertion |
| A safe new record type appears | Practical: reconstruct/check its inductive group and projections; core: unknown unsupported fragment |
| Binder index changes which assumption is used | Native scope/type checks determine the exact new object; no text-based matching |
| Same type has two valid proof terms | Separate ProofIDs; retain alternatives under local policy |
| One proof uses an unavailable dependency | Unknown for that ReplayID; another available replay may succeed |
| Source alias points to a new definition body | New DefinitionID; no mutation of an existing judgment's meaning |
| Natural-number literal exceeds operational memory | Bounded nondecision or fixed profile-limit rejection, not refutation |
| Native checker crashes on a proof bomb | ERROR and bounded recovery; no accepted result |
| A single bad instance is offered against an open pointwise judgment | No same-context refutation unless the required native negative judgment is actually proved |
| Both Γ ⊢ φ and Γ ⊢ ¬φ replay successfully | Record contextual opposition; do not invalidate conditional derivations merely because Γ is uninhabited |
| Opposite proofs plus a checked closed dependent substitution compose to False | Record a closed basis-inconsistency incident; do not guess a unique guilty premise |

## Conditional propositions and conformance obligations

**Native acceptance safety.** Assume correct canonical decoding/reference binding, no content-address collision, faithful native reconstruction, correct bootstrap construction, sound native kernel behavior for the selected admitted rules, and correct footprint/policy evaluation. If the procedure accepts a proof root, it establishes exactly its native contextual judgment under the selected profile, actual checked declaration extension, and recorded explicit axiom footprint. A definition/opaque/group root instead establishes its native well-formed checked declaration, not an invented theorem. No proof may silently use an unselected theorem witness, unavailable body, new axiom, or ambient library. Logical consistency is conditional on the foundation; acceptance does not itself establish foundation consistency or real-world relevance.

Proof sketch: induct over the replay topological order. Bootstrap non-axiom declarations enter by checked native operations; only exact locally adopted axiom schemes and quotient rules are initialized as foundation. Each external safe definition, theorem, opaque declaration, or inductive group is checked against already accepted predecessors. Within a group the native inductive checker supplies the admitted recursion/positivity rules. No missing theorem or body is installed as an axiom. The final Pi/lambda closure check establishes the exact contextual judgment of a proof root. Core proof-only definitions/theorems admit the substitution argument above; practical soundness records and assumes the safe extension rules actually used instead of pretending all such extensions were inlined away.

**Standalone independence.** Fix the exact root, ReplayID, local checker/policy, and available closure. Changing the publisher, transport route, original goal, or private research method does not change the native checking relation. Those fields are absent from mathematical object identity and checker inputs.

**Finite grounding.** Every accepted non-seed theorem reference has a selected proof at strictly smaller topological rank. Therefore no unsupported strongly connected component can create a native proof constant. Kernel induction is an explicitly admitted rule and is not such a dependency cycle.

**Profile-bound portability.** Given the exact closure and a correctly operating qualified checker image for the same profile, native replay requires no original producer, source elaborator, model service, mutable registry, or network callback. This is not a guarantee of universal hardware compatibility or affordable replay of every valid artifact.

Required later conformance evidence is concrete:

- canonical encoding/ContentID vectors, including noncanonical and collision-incident fixtures;
- exact core seed bytes and twenty-export inventory, plus the complete practical compatibility bootstrap and reserved-name audit;
- rejection of every unsupported Expr/declaration kind and every new axiom path;
- round-trip scope/universe mapping on dependent telescopes and shared open DAG terms;
- exact manifest reachability, missing-witness, cyclic-support, and alternative-proof cases;
- native add/mul/list core examples, plus practical algebra structures, quotient/classical proofs, dependent families, mutual/nested induction, strings, and a representative pinned mathlib slice;
- source-export errors that are caught by receiver replay;
- no peer module/plugin/source execution on the acceptance path;
- current-epoch behavior under a checker incident and dependency loss;
- contextual opposite proofs retained as valid conditional mathematics, contrasted with independently replayed closed contradiction incidents;
- core conservative auxiliary-elimination argument and practical safe-extension/footprint implementation correspondence;
- exact missing-body and unsupported-native-evaluation reports without fallback to axioms or executable peer imports.

These are release qualification obligations, not implementation work authorized or performed by this note. Cross-foundation transport, arbitrary new axiom schemes, compiler-trusting native-evaluation certificates, and succinct proofs are outside this v1 selection; none is a hidden required adapter. New safe native inductive groups are explicitly in the practical profile. SNARKs could later certify exact checking computations only under a separately specified circuit, public-input binding, availability policy, and cryptographic trust assumptions; their absence does not block native replay.

## Remaining engineering risk, without an unspecified mathematical route

The protocol, two fragments, identity rules, bootstrap-selection rules, and checking route above are selected at concept level. The principal remaining risks are implementation correctness of the new inert codec/adapter, complete practical reserved-name/bootstrap qualification, reconstruction of mutual/nested inductive groups and generated recursors, retention/extraction of theorem and opaque bodies, replay cost for realistic closures, and supply-chain/runtime assurance. A prototype must demonstrate these rather than treating an API name or a core arithmetic example as evidence of practical library compatibility.

No ready-made interoperable exporter for this newly specified wire format was verified during this concept task. It must be implemented later and remains outside mathematical trust. The new verifier adapter is necessarily in the TCB until independently verified; using Lean's kernel does not erase that adapter risk. If the selected seed cannot be reproduced with the pinned checked kernel or the adapter cannot preserve the stated expressions, deployment is blocked rather than silently falling back to peer `.olean` import or source execution.

## Sources inspected for this decision

Official sources were read at the pinned revision or version below. They establish existing API/type behavior; the CAS format, native exchange profiles, and propositions above are this project's proposed design, not claims that Lean already implements this protocol.

- [Official v4.22.0 tag reference](https://api.github.com/repos/leanprover/lean4/git/ref/tags/v4.22.0), resolving to `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.
- [Pinned Lean environment API](https://github.com/leanprover/lean4/blob/ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05/src/Lean/Environment.lean): checked and unchecked declaration paths; empty environments; module import; plugin/extension options.
- [Pinned C++ kernel environment implementation](https://github.com/leanprover/lean4/blob/ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05/src/kernel/environment.cpp): checked definitions/theorems, theorem-in-Prop condition, checking bypass entry point.
- [Pinned kernel type checker](https://github.com/leanprover/lean4/blob/ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05/src/kernel/type_checker.cpp): constant lookup, universe-arity checks, unsafe/partial restrictions.
- [Pinned native declaration types](https://github.com/leanprover/lean4/blob/ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05/src/Lean/Declaration.lean): definition safety, theorem/definition/inductive variants, reducibility hints, and the statement that safe recursion is compiled into recursors rather than primitive recursive definitions.
- [Pinned native expression types](https://github.com/leanprover/lean4/blob/ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05/src/Lean/Expr.lean).
- [Pinned Prelude definitions](https://github.com/leanprover/lean4/blob/ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05/src/Init/Prelude.lean): the selected six inductive groups; examples of unsafe compiler constants, `sorryAx`, `Classical.choice`, quotient initialization, and natural-number special handling that are not all safe to import indiscriminately.
- [Pinned native inductive checker](https://github.com/leanprover/lean4/blob/ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05/src/kernel/inductive.cpp): checked group construction, parameters, constructors, and generated recursors.
- [Pinned quotient initialization](https://github.com/leanprover/lean4/blob/ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05/src/kernel/quot.cpp): exact equality checks, reserved quotient names, and primitive quotient declarations.
- [Pinned Init.Core](https://github.com/leanprover/lean4/blob/ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05/src/Init/Core.lean): `propext`, `Quot.sound`, and the distinct compiler-trust/native-evaluation paths deliberately excluded here.
- [Lean 4.22 reference: inductive types](https://lean-lang.org/doc/reference/4.22.0/The-Type-System/Inductive-Types/).
- [Lean 4.22 reference: propositional equality](https://lean-lang.org/doc/reference/4.22.0/Basic-Propositions/Propositional-Equality/): equality, definitional proof irrelevance, and the distinct roles of additional axioms.
- [RFC 8949](https://www.rfc-editor.org/rfc/rfc8949.html): CBOR; this specification adopts only the explicitly defined deterministic subset.
