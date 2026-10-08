# CP-001F: source-grounded Lean producer and local-client path

Date: 2026-09-20. Status: bounded source audit and selected concept refinement. No Lean execution, build, artifact extraction, exploit, implementation, or benchmark was performed. Frozen CP-001E and earlier checkpoints are unchanged.

Source scope: Lean `v4.34.0`, commit `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`; limited compatibility evidence from mathlib `5ed2965256430c3649e86755f9576b54eca72435`. Every Lean line reference below is to that fixed commit, not the moving main branch.

## Outcome

The practical native-exchange plan has an owner-controlled route to complete theorem/opaque bodies, but “import the library and inspect its environment” is not precise enough. In Lean's module system, ordinary imported public information can deliberately replace theorems and unexposed definitions/opaques with axiom-shaped records. Switching to a private view afterward cannot recover bodies that were never selected for import. A single `import all` is also not a promise of complete transitive body availability.

Select a dedicated **full-data producer collector** using explicit global `OLeanLevel.private`, complete matched artifact parts from the owner's pinned build, and actual completed constant records. It exports inert descriptors only. If those artifacts are unavailable, the owner may rebuild the original source and retain full outputs or capture each module's completed checked declarations. Neither route requires changing public visibility or enabling `forceExpose` throughout the library. No route makes compiled input authoritative for the receiver.

The body acquisition step can preserve the original source declarations without changing their mathematics. Rewriting native names, canonicalizing metadata, resolving theorem-witness collisions, and rechecking the resulting content-named declarations are additional obligations; successful body retrieval alone does not prove lossless protocol export.

## Concrete source evidence

| Question | Verified source path and observation |
|---|---|
| Do theorem/opaque constant records contain bodies? | `Lean/Declaration.lean:142–167`: `TheoremVal` and `OpaqueVal` both contain `value : Expr`. |
| Does the usual body accessor return them by default? | `Lean/Declaration.lean:479–510`: `ConstantInfo.value?`, `hasValue`, and `value!` default to `allowOpaque := false`; theorem and opaque values require `true` or explicit record-kind inspection. |
| Where is public information weakened? | `Lean/AddDecl.lean:113–127`: a module theorem is exported as `axiomInfo` unless `forceExpose`; definitions and opaques are similarly projected when the declaration body is not being exported. The private record still has its actual kind/body. |
| Does `public theorem` imply public proof body? | No. The theorem branch checks `header.isModule` and `forceExpose`, not `isExporting`. Public name/signature visibility is not full proof visibility. |
| Where are private names handled? | `Lean/AddDecl.lean:138–151`: private declarations are omitted from public export unless the separate compatibility option `privateInPublic` applies. `forceExpose` is not a universal override of private-name policy. |
| What does `forceExpose` mean? | `Lean/AddDecl.lean:223–230`: it preserves the full declaration representation in public scope, even for theorems, subject to declaration visibility handling. It is a producer API parameter, not an import-body-recovery operation. |
| How are definition exposure attributes interpreted? | `Lean/Elab/MutualDef.lean:1343–1393` derives exposure from declaration kind, section attributes, and `expose`/`no_expose`, then adjusts `isExporting`; it explicitly prevents export of private declarations from theorem bodies. |
| What is the public/private environment distinction? | `Lean/Environment.lean:554–614` stores separate base/async maps. The public view may contain fewer constants and less data per constant. `setExporting`, at 652–657, changes the selected view, not the imported data. |
| What does an ordinary frontend choose? | `Lean/Elab/Import.lean:150–160`: a file using `module` imports at `.exported` on the command line, `.server` in the language server, and `.private` without the module annotation. Thus “normal import” has no single body-availability meaning. |
| Is full local data serialized? | `Lean/Environment.lean:1858–1884`: `mkModuleData` at `.private` collects all local stage-2 constants from `env.toKernelEnv`, rather than the public filtered view. `writeModule`, at 1901–1917, writes exported/server/private parts for module files; non-module files use the complete old-style single part. |
| Can the importer select full transitive data? | `Lean/Environment.lean:2433–2448`: explicit `level := .private` means all data as if imports had no module annotations. At 2180–2182, the global private level forces `importAll` during traversal. |
| Does `import all Root` guarantee the same? | No. Without global `.private`, `importAll` propagates as the conjunction of the current flag and each import edge's `importAll`; ordinary downstream import edges can restrict their dependencies again. |
| Where does the selected part become the actual constant map? | `Lean/Environment.lean:2023–2031` selects private versus exported module data; `finalizeImport`, at 2332–2385, constructs the environment constant maps directly from those records. This is not replay of all imported declaration bodies. |
| Does disabling extensions make this a receiver checker? | No. `importModules` can load plugins and serialized runtime data; `loadExts` controls initialization of persistent extensions, not logical rechecking. The source documentation at 2427–2431 only says the constant map can be accessed without extension initialization. |

The `@[export ...]` attribute in `Lean/Compiler/ExportAttr.lean:24–67` is different again: it selects an unmangled code-generator symbol for C/interoperability. It is not a theorem-evidence export or a mathematical acceptance permission. `@[extern ...]` likewise concerns compiled execution, not omission of a safe definition's logical body from our evidence.

## Countercases that the producer contract must handle

### Public axiom-shaped information is not complete evidence

Take an ordinary successfully proved public theorem in a module. The public `ConstantInfo` projection can be `.axiomInfo`, with its proof body absent. An exporter which treats every imported `.axiomInfo` as an authorized axiom silently expands the foundation. An exporter which treats it as a theorem whose proof is “the import succeeded” makes the same error indirectly.

The required disposition is to acquire its full body/kind or report incomplete producer evidence. A public abstracted definition can also appear axiom-shaped; it must not be misclassified as an actual source axiom merely from that view. Genuine nonpermitted axioms, once identified in the complete selected closure, are a different failure category.

### The default accessor can miss an available body

Even a full `.thmInfo`/`.opaqueInfo` has `value? = none` under the accessor's default flag. Therefore “value? returned none” does not by itself prove that a library omitted the body. The collector must distinguish record kind, visibility/import level, and the accessor option. Selecting `allowOpaque := true` exposes stored values for extraction; it does not alter native opacity or authorize unfolding opaque constants during checking.

### Private view is not transitive import-all

Suppose a module collector imports all of module A, and A ordinarily imports B. Under the restricted global level, A's own private data may be available while B is represented by its exported data. A's proof can depend on a B theorem whose body is absent from this selected environment. Setting `isExporting := false` only selects the environment's private map; it does not retrospectively reload B's private part.

Global `OLeanLevel.private` is the selected full-data collection mode. Alternatively, per-module complete capture must be closed transitively by the collector. A shallow “proof body found” check is insufficient.

### Partial artifacts and unchecked snapshots

The private module part is not a self-contained substitute for the corresponding exported/server parts. The fallback reader at `Environment.lean:2078–2091` reads the module parts together, with compacted regions referring to earlier parts. The artifact-map path at 2231–2236 can also be limited by the producer's supplied list. The collector must have a complete mutually matching artifact family, not combine files from different builds or reuse a previously restricted artifact map.

`Environment.checked`, at 569–574, is a task completed by asynchronous checking; `toKernelEnv`, at 648–650, obtains that completed task. `AddDecl.lean:159` publishes preliminary information before its asynchronous native check. Its error-recovery code, at 191–220, can add fallback axioms, including `sorryAx`-based types, to suppress cascading elaboration errors. Consequently the collection boundary is an error-free completed declaration/module snapshot with actual kinds/bodies, not an arbitrary editor environment or an early callback.

Even that completed producer snapshot is not trusted by the receiver: the owner may have run metaprograms, unchecked APIs, modified tools, or compiler-assisted tactics. Every selected exported declaration still needs the independent inert-data checking path.

## Selected full-data producer path

The following is the selected concept path, not code executed in this checkpoint.

1. **Owner-controlled acquisition and build.** Select the exact Lean/mathlib/dependency sources, toolchain and build configuration. Obtain or build complete matching module artifacts, including private parts. This tooling may run source elaboration, tactics, compiler code and package initialization only under the owner's chosen local sandbox/resource authority. It is outside receiver acceptance. No network publication of private source metadata or bodies is implied by collecting them.
2. **Dedicated full-data collection session.** Use an explicit global `.private` import level, no source edits to promote declarations, and a complete artifact map. In an extraction-only session prefer no external plugin list and `loadExts := false`; read raw completed constant records rather than using tactics, typeclass search or realization callbacks that require initialized extensions. This reduces producer-side work/behavior but does not turn serialized artifacts into safe untrusted receiver input.
3. **Immutable completion boundary.** Require completed checks/error-free owner build outputs before capture. When capturing a live module, wait for the checked task and inspect the resulting kernel map, not preliminary async signatures. Record the exact body-bearing declaration kind, universe parameters, type, value, native group information and safety classification. Reject or diagnose actual fallback/unsupported records.
4. **Transitive evidence collection.** Starting from selected exact source declarations, follow references in types and bodies, including actual theorem/opaque bodies and private helper declarations. Group inductive types with their constructor descriptors and regenerated-member identities. Every reference must resolve in the complete selected source collection. Missing bodies/private artifacts, a genuine prohibited axiom, and a malformed source collection remain distinguishable.
5. **Source-to-native normalization.** Produce the exact inert Native2 objects and explicit source-to-content correspondence described below. Nothing grants author/source names mathematical authority. Compiler annotations, executable extensions, IR, native binaries, source macros, tactic syntax, and public/private import flags do not become accepted proof evidence.
6. **Independent receiving replay.** A fresh receiving path reconstructs the qualified seed and submitted native declarations, resolves exact selected witnesses, checks every required body/group, verifies the actual permitted axiom footprint, and applies the current availability/incident guards. A local collector can invoke the same independent validation as preflight; success of its source build or extraction is never the verdict.

If complete build artifacts cannot be obtained, the fallback is an owner-controlled original-source rebuild retaining private parts, or capture after each module's completed native declarations. It is not replacing missing proofs with source signatures. Rebuilding without modifying original visibility preserves the source's declared interface behavior; changing `forceExpose`, removing `module`, or rewriting imports throughout mathlib is neither required nor selected as the default remediation.

The collector may need substantial storage and work because full `.private` import traverses more than the mathematical root closure before extraction. That is a measurable producer cost, not a claim that every receiving node imports all of mathlib. Per-module capture/indexing may later reduce peak collection cost without changing the final evidence requirement.

## Source names, content names, and local reuse

### A correspondence object is necessary

The collector's working correspondence must map a source occurrence in its exact owner-controlled environment to one of:

- an exact qualified seed export;
- an exact DefinitionID or OpaqueID;
- a JudgmentID together with the actual selected source proof material;
- a GroupID and a checked member selector;
- an explicitly diagnosed unsupported/missing item.

It must rewrite every native constant reference and projection structure name, preserve universe instantiations, and handle group-local recursive indexes before content IDs are available. Source private-name prefixes and aliases cannot be copied into external native references. Conversely, literal/primitive reserved seed names cannot simply be hashed into unrelated user constants: the kernel's builtin reductions depend on their qualified fixed meanings.

This map is producer-local evidence for extraction, not a new public author/provenance registry. It can be discarded after sufficient exact export/diagnostics are retained. The receiving node derives its own content-to-generated-native-name mapping.

### Full import itself can choose a theorem witness

`Environment.lean:2249–2283`, `subsumesInfo`, permits same-name, same-type, same-level-parameter theorem records with different proof bodies to coalesce; it explicitly does not compare theorem values. `finalizeImport:2335–2342` applies that choice while constructing the map. Thus an ordinary combined full-data environment is not necessarily a complete historical catalogue of every module's proof alternative.

For basic export the collector records the actual body it retrieved, computes its actual closure, and replays it independently. It must not claim that this is the original body from every contributing module. Where exact source-branch alternatives are required, collect their completed module records separately before global coalescing and normalize an explicit selection. The [proof identity/composition analysis](CP-001F-proof-identity-composition.md) owns the deeper collision, witness-union, alias-expansion, and fixed-hint compatibility arguments. No proof-irrelevance slogan substitutes for those arguments or the actual native replay.

### Two local-client boundaries

The selected minimum client is an **explicit native application workspace** backed by the checked content-name environment. It assembles actual native argument applications/transports and rechecks the result. Inert alias, binder, class and rewrite views can help it find or construct candidates; they do not install peer code or prove omitted arguments.

An ordinary Lean authoring environment is a distinct optional owner-controlled producer workspace. It may run locally authorized notation, elaboration, typeclass search and tactics. A collection of content-addressed native declarations does not automatically recreate all of Lean/mathlib's environment extensions, structure registrations, syntax, scoped instances or simplifier state. `Environment.lean:2427–2431` explicitly warns that many `CoreM`/environment operations may not function with extensions uninitialized.

Therefore the concept must not promise that “import accepted objects” alone immediately gives a conventional `import Mathlib` development experience. A qualified local bridge must maintain the exact native correspondence and locally selected elaboration conveniences. Any new result produced through that richer workspace is exported back to inert terms and independently rechecked. No remote `.olean`, plugin, arbitrary source snippet or advisory text is promoted into receiver authority to make the bridge convenient.

## Version-specific String bootstrap is larger than a renamed constructor

The prior audit observed that the selected kernel uses `String.ofList`. This source review establishes the logical path behind that name:

- `Init/Prelude.lean:3540–3546`: String is a structure with byte-array data and a proof that the bytes are valid UTF-8; its constructor is `String.ofByteArray`.
- `Prelude:3560–3561`: `String.ofList data` is the structure value with `List.utf8Encode data` and the corresponding constructor proof of validity.
- `Prelude:3517–3518`: `List.utf8Encode` uses `List.flatMap String.utf8EncodeChar` followed by `List.toByteArray`.
- `Prelude:3486–3512`: the character encoder uses the character's numeric value, byte conversions and arithmetic branches.
- `Prelude:3525–3530`: `ByteArray.IsValidUTF8` is an inductive predicate whose constructor uses equality with the encoded character list.
- `Prelude:3466–3470`, 3420–3460: list-to-byte-array construction uses logical ByteArray/Array operations and their types.
- `kernel/inductive.cpp:1368–1379` expands native string literals into a list of `Char.ofNat` applications and applies the reserved string operation; initialization at 1394 binds `String.ofList`.

This is a verified portion of the direct dependency path, not a computed complete canonical bootstrap inventory or its measured cost. The exact transitive safe type/body/constructor/proof closure is still an extraction/replay obligation. The three-axiom allowance must be checked over that actual closure; no inferred “small String seed” claim is justified.

The `extern` annotations on `String.ofList`, `String.ofByteArray` and byte operations do not erase their logical definitions/constructors. We retain the safe logical model and omit executable annotations from accepted descriptors. This permits broad ordinary data/library mathematics without granting arbitrary C/runtime execution during contributed proof checking. Native literal/arithmetic behavior already implemented by the qualified checker remains an explicit part of its own trusted boundary.

## Compiler-assisted proofs and realistic library compatibility

In this selected Lean release, the modern native-evaluation proof path is not characterized adequately by blocking just two historic primitive names:

- `Lean/Meta/Native.lean:31–87`, `nativeEqTrue`, builds a temporary Bool definition, compiles/evaluates it, and then adds a fresh `Declaration.axiomDecl` asserting that the expression equals `Bool.true`.
- `Lean/Elab/Tactic/Decide.lean:57–68` uses that axiom in the native-decide proof; lines 190–193 select the native configuration for `native_decide`.
- The same native infrastructure documents use by `bv_decide`. This does not mean every tactic with “decide” in its name introduces an axiom: `Decide.lean:78–86` distinguishes native, kernel, and elaborator checking paths.

The selected remediation is **actual transitive axiom/declaration-kind checking**, already required by the foundation contract. A fresh compiler-generated axiom remains forbidden even if its name does not contain `Lean.reduceBool`, `Lean.reduceNat`, or an obvious tactic marker. A permitted alternate proof must be supplied and rechecked; native computation cannot be relabeled as an ordinary kernel proof.

The inspected pinned mathlib test `MathlibTest/Tactic/Inclusion/NativeLinter.lean` explicitly expects warnings that `+native` is not allowed in mathlib because it trusts the compiler. This is evidence of a compatibility-oriented policy, not a scan proving that every mathlib declaration and dependency obeys our profile. No fraction of supported mathlib has been measured here. Broad mathlib support remains the practical target; the right response to an ineligible witness is an alternate eligible witness or an exact unsupported-footprint report, not retreat to the six-type demonstration.

## Required outcome distinctions

| Producer/replay condition | Required meaning |
|---|---|
| Public projection or wrong accessor hides a body | Attempt full-data retrieval; no axiom substitution and no assertion that the proposition is false. |
| Full private artifact or dependency body unavailable | Incomplete evidence/source-artifact outcome, naming the missing kind/closure item. |
| Actual nonpermitted axiom or unsafe/partial dependency found | The selected evidence does not satisfy this foundation policy; a different eligible proof may exist. |
| Source-to-content rewrite fails, alias selection conflicts, or regenerated group differs | Export/replay compatibility failure with the exact case; source correctness alone does not certify the transformed artifact. |
| Producer build error, incomplete async snapshot or `sorry` fallback | Invalid/incomplete producer candidate; never automatic ACCEPT. |
| Receiver resource exhaustion/interruption | Mathematical nondecision, not falsity or permission to skip a dependency. |
| Complete transformed evidence passes the selected independent replay | Acceptance for those exact objects, witnesses and qualified checking basis, still separate from current retention/use. |

## Qualification obligations selected by this note

- Compare public versus full-data extraction of a theorem, an unexposed definition, an opaque declaration, a private proof helper and a transitive dependency.
- Exercise both explicit global-private collection and the separately captured completed-module fallback with matching build outputs.
- Demonstrate that `allowOpaque`/kind handling preserves actual theorem/opaque bodies and does not change native opacity.
- Reject actual arbitrary/compiler-generated axioms while distinguishing public abstraction from a source axiom.
- Round-trip ordinary structures/instances, dependent families, quotient/classical mathematics, nested groups and the version-specific String closure through content renaming and fresh receiver replay.
- Include duplicate source theorem witnesses, statement-address alias collisions and native-hint changes under the composition analysis's exact selected rule.
- Demonstrate useful explicit local application, and separately document which richer Lean authoring conveniences require locally qualified extensions.
- Measure exporter full-data working set, generated closure size, local body availability, cold/warm receiver cost and unsupported reasons over a declared realistic mathlib slice.

These are future qualification obligations, not completed tests or authorization to implement. The selected path removes a concrete body-availability ambiguity while leaving receiver soundness unchanged and preserving the intended practical mathematical scope.

## Sources

- [Pinned AddDecl](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/AddDecl.lean#L101).
- [Pinned constant values/accessors](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Declaration.lean#L479).
- [Pinned environment views and serialization](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Environment.lean#L1858), [import traversal](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Environment.lean#L2107), [full-data API](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Environment.lean#L2420), and [same-name theorem coalescing](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Environment.lean#L2249).
- [Pinned frontend import-level selection](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Elab/Import.lean#L141), [declaration visibility](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Elab/DeclModifiers.lean#L57), and [body exposure](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Elab/MutualDef.lean#L1343).
- [Pinned compiler export attribute](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Compiler/ExportAttr.lean#L24).
- [Pinned String logical model](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Init/Prelude.lean#L3416) and [kernel literal expansion](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/inductive.cpp#L1368).
- [Pinned native-evaluation axioms](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Meta/Native.lean#L30) and [decide configuration paths](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Elab/Tactic/Decide.lean#L57).
- [Pinned mathlib native-linter examples](https://github.com/leanprover-community/mathlib4/blob/5ed2965256430c3649e86755f9576b54eca72435/MathlibTest/Tactic/Inclusion/NativeLinter.lean).
