# CP-001H: complete incremental export and native group recovery

Date: 2026-09-20. Status: selected producer/client specification with [independent review and C1 closure](../audits/CP-001H-export-cross-audit.md). Frozen G and earlier checkpoints are unchanged. No code, extractor, build, native replay, theorem execution or benchmark was run.

## Operating gap and selected scope

The [v4 design](../../spec/OPERATIONAL-CORPUS-V4.md) has a complete receiving evidence model, but a practical producer still needs a precise path from actual completed Lean declarations to those inert objects. "Walk the environment and rename everything" is insufficient: public records may omit bodies, names can be coalesced, nested groups have generated members, and unchanged source text can refer to changed dependencies.

Select **EXTRACT1**, an owner-local producer convention. It produces candidate PI1 evidence from a finite complete immutable source cut, with explicit semantic/evidence reference maps, group recovery, exact cache boundaries and diagnostic outcomes. It grants no receiving authority and no remote execution permission. Its output becomes usable only through the receiver's independent native path and current-use guards.

EXTRACT1 is not a theorem that every ordinary source proof survives canonical representative replacement. The [proof-computation analysis](CP-001H-proof-computation-and-reconstruction.md) examines that distinct issue. This note specifies faithful collection, candidate construction and observable disagreement rather than hiding conversion failure behind an exporter success flag.

## Source cut, not a changing bag of names

A source cut comprises the exact Lean build/source version, completed chosen declaration records, matched full artifact parts, an immutable lookup environment for all reached references, and any captured native declaration inputs needed for supported reconstruction. The complete-private collection conditions from [CP-001F](CP-001F-lean-producer-client-path.md) remain mandatory.

An owner can collect from a completed full-private environment or capture declarations when their complete checked records become available. Asynchronous placeholders, a public theorem projection without its actual body, a mismatched private artifact, or a name whose record changes mid-traversal do not form a completed cut. Incomplete capture remains incomplete even if the source file compiled elsewhere.

The cut need not record political authorship or a historical chronology. A finite topological order is derived from actual source dependencies; names are local lookup keys, not mathematical identities. A complete source record includes its actual kind, safety, ordered universe parameters, type, full required value, and group/member information. Syntax and frontend annotation fields are retained in the source record where needed to explain the canonicalization and CLIENT1 correspondence; they do not all become semantic fields.

If a combined import has already merged two same-named theorem records, EXTRACT1 can export the retained body but cannot recover the discarded alternative by knowing its statement. Preserving both implementations requires their actual separately captured complete cuts. This is technical evidence retention, not attribution policy.

The operation carries finite source-object, byte, expression, external-reference, work and staging limits under the owner's aggregate allocation. A source cut larger than its admitted traversal is not reported as fully exported. Byte sharing and existing local caches reduce actual work only when their exact compatibility is established.

## Two maps and three different successes

For source declaration/member names, maintain:

- `sigmaS`: the exact semantic reference—seed export, DefinitionID, JudgmentID, GroupID/member selector or OpaqueID.
- `sigmaI`: the exact ProofInstanceID for each captured source theorem implementation.

They are not interchangeable. A semantic definition/type/group uses sigmaS even when it contains a proof occurrence. A theorem's WitnessTermDAG uses sigmaI at every theorem occurrence, including occurrences inside annotations and binder types. Reached ordinary declarations retain their own semantic grammar. This is the PI1 boundary, not a producer-selected variation.

Distinguish:

1. `COMPLETE_CANDIDATE_EXPORTED`: exact selected source records were represented under the codec and all candidate references resolve.
2. `NATIVE_REPLAY_ACCEPTED`: the actual selected PI1 realization and all required native checks succeeded.
3. `SOURCE_CORRESPONDENCE_ESTABLISHED`: the stated source-to-target correspondence—including required generated-member and computational conditions—was checked for the declared scope.

The first does not imply the second. The second proves the target mathematics under its adopted basis, not an arbitrary intended source correspondence. Publishing honestly re-expressed mathematics does not require human-intention evaluation, but an exporter must not falsely label a failed source correspondence as an unchanged import.

## Dependency-first candidate construction

First derive a graph over **raw captured source declarations**, before collapsing their theorem statements to JudgmentIDs. Group members belong to their actual atomic native inductive group. All source theorem/opaque bodies, definition types/values, constructor types and required generated-rule support are inspected. A string resembling `Foo.rec_1` is not evidence of group membership.

Take a topological order of the actual supported graph; a local deterministic tie-break can use canonical source-name bytes. This choice may select a different valid evidence realization, but names are not inserted into semantic payloads as mathematical meanings. A cycle outside an admitted native group, missing declaration, unavailable body or prohibited axiom/kind stops this candidate path with its actual reason.

For each ordered unit:

1. Confirm the precise supported kind and safety. An allowed foundation axiom is the exact locally qualified seed declaration, not any axiom with a familiar name. A source native-evaluation axiom is not reclassified as a theorem.
2. Preserve universe parameter order and map parameter names to ordered indexes. Do not infer a canonical permutation from the names or from parameter usage; unused declared parameters and explicit instantiations remain meaningful encoding data.
3. Normalize only the admitted presentation fields: binder names/metadata, source names via the correct map, the declared native let setting, and transparent definition hints through HEIGHT1. Keep actual term constructors, type/value bodies, universes, literal values, scopes and selectors. Do not delta-normalize arbitrary definitions or erase proof arguments as a supposed deduplication optimization.
4. Remove transparent metadata expression wrappers only through the specified native rule. Pinned `type_checker.cpp:339`, `478–479` and `742–743` treats MData by processing its contained expression for typing/WHNF; this is source evidence for that particular erasure, not authority to strip term-level annotation functions recognized by the kernel.
5. Build the selected canonical level/expression DAGs with exact postorder sharing and no unreachable nodes. Compute direct semantic reference sets from the actual semantic terms. An open shared subterm is checked at all required binder depths or using the equivalent exact free-variable requirement; physical DAG sharing cannot erase scope obligations.
6. For a theorem, emit its exact semantic judgment and corresponding witness expression/instance. The initial ordinary source convention keeps the source's closed theorem type as the conclusion of an empty contextual telescope; an explicitly contextual client judgment can retain its separately supplied telescope. Do not silently identify these different wire splits. Close a contextual witness once, exactly as PI1 specifies.
7. Retain the chosen representative candidates and actual source occurrence information needed by the proof-computation planner, then construct the exact root-reachable B map. Source-earliest selection supplies a structural acyclicity construction, not guaranteed successful native conversion.
8. Independently check the final selected native replay. Failed checking leaves the candidates inert. Another realization or a checked transformation is separately recorded and rechecked; it does not inherit the failed candidate's footprint or source-correspondence claim.

The output is a finite exact root or bounded optional module, not a mandatory global collection manifest. Multiple root exports can share their actual CAS subgraphs and protected local input evidence.

## Recovering an actual inductive group

### Source facts at the selected pin

Read `src/Lean/Declaration.lean` at Lean `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`:

- `InductiveVal` at 261–300 contains ordered `all`, ordered `ctors`, `numParams`, `numIndices`, `numNested`, `isRec`, safety and `isReflexive`.
- `ConstructorVal` at 328–342 records the owning inductive, constructor index, parameter count, field count, type and safety.
- `RecursorVal`/`RecursorRule` at 348–388 records group names, parameters/indices/motives/minors, actual constructor rules and their right-hand sides, K-like and safety information.

Read `src/kernel/inductive.cpp:1181–1345` at the same pin. It assigns nested auxiliary recursor names from the first original inductive type and a positive numeric suffix. After temporary nested-inductive elimination, it restores the original group's `all` list, restores constructor types, restores recursor types/rules and their constructor selectors, and rechecks the restored terms in the resulting environment. The temporary auxiliary types do not become ordinary persistent externally referenceable types. The code explicitly rejects both constant and projection references into `_nested` in input expressions.

These observations support a recovery candidate from completed records. They do not prove that every completed environment retains the original syntactic `Declaration.inductDecl` input verbatim or that the proposed reconstruction has been executed.

### Two explicit producer inputs

**Captured-input route.** If the owner retained the completed native `inductDecl` input at the supported boundary, use its exact ordered type/constructor descriptor and universe/parameter information as the recovery candidate. Retain and compare the actual completed generated member records as well. The source's own success does not replace receiving reconstruction.

**Completed-record route.** If that input was not retained, choose one actual inductive record and recover the ordered group from its `all` list. Require all listed type records to agree on the group list, safety and shared parameter/universe contract; follow each ordered `ctors` list and verify actual constructor kind, owner, index, parameter count and universe correspondence. Construct candidate input type/constructor descriptors from those complete records, replacing references to this group's type formers by the admitted local indexes. Do not replace external groups, constructors or recursors by those local indexes.

The source-level ordering is not sorted away. Reordering mutually declared types or constructors can change member selectors, recursor interfaces and GroupID. Two producer routes can yield different but separately valid descriptors when their retained syntax differs; do not claim universal source-normal-form uniqueness. For interoperable export of one retained cut, the selected route and its exact descriptor input are fixed in the local extraction interpretation.

Both routes enumerate intended ordinary recursors and nested auxiliary recursors through the actual record inventory and the qualified generation rule. The complete source `numNested` count, recursor kinds, group association, universe lists, types and rules are checked; a coincidental source name or arbitrary suffix does not confer generated membership. An unexpected generated constant is not silently imported as an axiom or independent group.

### Native reconstruction is the authority

The receiving adapter builds exactly one semantic group at its content-derived names through the qualified native inductive operation. It derives the actual complete native inventory and computation rules, rather than accepting the exported `RecursorVal` as trusted data.

For the source-correspondence claim, compare the source inventory under the exact name/universe/member mapping with the receiver-derived inventory. Required fields include type/member ordering, universe arity/order, parameter/index/field/motive/minor counts, inductive `numNested`, `isRec` and `isReflexive`, constructor selectors, normalized types, recursor right-hand sides, K-like behavior and safety, subject only to the explicitly admitted presentation erasures. Extra or missing members, a changed selector, an unexpected external dependency or a mismatch in the stated exact correspondence yields a diagnosed mismatch, not identity by assertion. A disagreement in a derived flag fails this exact source-correspondence claim; it does not by itself invalidate an independently checked target declaration.

When restored record syntax is not exactly the same as the original input route would generate, EXTRACT1 does not call definitional equivalence exact byte correspondence. A separately justified checked mapping may still establish a weaker useful correspondence; otherwise the producer captures a better input or declines that import claim. Independently accepted target mathematics remains distinguishable from successful original-interface restoration.

Group generation can inspect dependencies. If changed proof representatives alter required conversion or reconstructed generated behavior, the actual result must be rechecked under that realization. PI1 does not license copying a prior group's environment certificate merely because its input GroupID is unchanged. A matched source group from a different foundation remains a migration input, not a same-ID group.

## Incremental caches without stale source-name authority

An export candidate cache key binds the exact selected source declaration/group input, target FoundationID, codec and normalization interpretation, selected recovery route, and the **direct source-reference resolution boundary**. For each directly reached source name/member it records the exact semantic and/or instance reference actually substituted in this term grammar. It also binds the chosen judgment telescope split when applicable.

Keying only by source spelling, source file text or the current module name is insufficient. For example, unchanged source `def d := h` can refer to a different body/interface for h in another complete source cut. Its canonical d must then follow the changed reference rather than reusing a stale content ID. Conversely, binding every cache entry to a single global workspace revision would unnecessarily invalidate unrelated unchanged exports. A verified exact per-unit source record and direct-resolution boundary permit bounded unchanged-unit reuse.

This is a candidate transformation cache, not a native ACCEPT cache. Reusing canonical output bytes does not reuse checking after B, checker/image, adapter interpretation, actual group inventory or current policy changes. Actual source and target custody remain separate. Evicting a source-side cache cannot delete target bytes still owed to a retained replay, and retaining source artifacts does not prove current target acceptance.

For a supplied compatible extension with fixed normalization rules and O(1) new direct references, candidate encoding can reuse unchanged canonical dependencies and create only the newly necessary syntax/direct-context nodes, plus exact map/index path-copy overhead. A changed dependency mapping can propagate through many downstream IDs; the export planner must charge that actual propagation and cannot promise constant-sized changes for arbitrary edits.

The canonical DAG traversal itself has work in the actual distinct syntax and required scope/reference operations. It must not unfold predecessor theorem bodies merely to encode an instance reference. Native conversion, changed realization planning and full cold source/group recovery remain separate potentially expensive costs.

## Required countercases and positive paper paths

- A public theorem record has no body while the private counterpart exists elsewhere: collection is incomplete until the actual matched complete record is acquired; an axiom-shaped view is not evidence.
- Two cuts keep the same local name but different declaration bodies: the exact source record/resolution key changes; stale output or native certificates cannot be reused by spelling.
- A mutual group is encountered through its second member: its actual ordered `all` determines the group, not encounter order.
- A user-defined name looks like an auxiliary recursor: actual kind, group association, counts and generated inventory determine the selector; the spelling alone is insufficient.
- A nested group has temporary `_nested` references in alleged external input: reject that unsupported/internal reference rather than treating it as an ordinary exported type or projection.
- A restored constructor is propositionally but not exactly equal to the candidate generated type: do not claim exact descriptor correspondence from propositional equality.
- A source declaration uses a theorem in both its type and its implementation: the semantic and witness grammars resolve each occurrence through their specified maps, retaining all actual support.
- A later proof uses a computation-transparent witness while the source-earliest canonical representative is opaque-backed: candidate collection can succeed while replay fails; report and use the separately checked computation-aware path rather than claiming complete import.
- A finite coherent group and its descendants are recovered and fully reconstructed with matching inventory: its exact canonical GroupID/member references can be reused by independent agents without retaining source author names.
- An unchanged already qualified dependency cut receives an independent new theorem instance: only actual new source/target syntax and changed direct/representative/index paths are candidates for incremental work; native and current-use guards remain required.

## Sources and evidence limit

- [Frozen complete producer evidence path](CP-001F-lean-producer-client-path.md).
- [Frozen PI1 composition](CP-001G-proof-instance-composition.md).
- [Frozen CLIENT1 correspondence](CP-001G-library-interoperability.md).
- [Pinned Lean declaration records](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Declaration.lean#L261).
- [Pinned nested-inductive restoration](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/inductive.cpp#L1181).
- [Pinned metadata typing](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/type_checker.cpp#L339).

The listed upstream portions were inspected read-only. EXTRACT1 selects a finite source/candidate/reconstruction contract; it does not claim that a real broad-library export has succeeded or that every canonical representative choice preserves native computational behavior.
