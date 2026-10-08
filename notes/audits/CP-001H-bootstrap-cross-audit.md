# CP-001H: independent BOOT1 foundation/bootstrap audit

Date: 2026-09-20. Reviewer: resource/discovery analyst, independent of the BOOT1 author. Scope: concept consistency and bounded pinned-source inspection. No implementation, compiled-artifact extraction, Lean invocation, native checking run, exploit, model execution or benchmark.

## Disposition

No new concrete contradiction was identified in the inspected BOOT1 construction, fixed-name, axiom or identity contracts. The selected algorithm is a coherent **candidate construction with explicit failure**, not evidence that the complete bootstrap has already been constructed successfully.

The main practical unresolved condition is specific: the full actual type/body/group/literal closure must admit the prescribed stage order and fit the qualified reader/runtime budgets. In particular, BOOT1's conservative complete-String-support-before-string-literal rule can reject a closure that contains an early support string literal. The bounded source investigation below found **no such cycle on the inspected String/UTF-8/ByteArray/Char support spine**. It does not claim an extracted complete closure or a successful replay.

Reviewed target: [BOOT1 foundation/bootstrap contract](../analyses/CP-001H-foundation-bootstrap-contract.md), final inspected SHA-256 `D98A0E4B7A4D8B2653D67A5622DAE039B74BCC9AC73C44E20D9F261202C71F22`. The initial complete read was against `EC0CB2BFF3677C8FB7038BCA4BCBEF9E7CDF548F9BB819940E610EA219A69EA2`; the intervening author clarification distinguishes prohibited declaration/reference names from inert string values that happen to spell those names. That clarification was inspected. The reviewer did not edit the author note.

## Prior contracts checked

The inherited [bootstrap grammar](../../spec/OPERATIONAL-CORPUS-V1-MATHEMATICS.md) selects name-local descriptor terms, inline full theorem/opaque bodies, exact bootstrap binder-info codes, a single quotient-initialization descriptor, and a finite sorted export list. Its old release/root choices are superseded by the later pinned compatibility decisions, not revived by referencing its grammar.

The [Native2 registry](../../spec/OPERATIONAL-CORPUS-V2.md) binds Foundation2 to source commit, SeedProfile1, NativeRules1 and ReservedNames1; ReservedNames uses exact-name entries and its existing empty/present export-index options. The [E foundation audit](../analyses/CP-001E-foundation-security-audit.md) and [F full-body/String analysis](../analyses/CP-001F-lean-producer-client-path.md) establish the selected modern source pin, actual safe evidence requirement, corrected `String.ofList` role and prohibition on expanding axioms through axiom-shaped import views.

BOOT1 respects those boundaries. It changes the selected seed/export inventory and therefore the resulting FoundationID; it does not silently add fields to the SeedProfile grammar or relabel an earlier actual qualified digest. No actual final seed digest has been claimed in these notes.

## Independently inspected source evidence

All Lean URLs here use commit `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`.

| Source inspected | What was directly confirmed |
|---|---|
| [kernel/type_checker.cpp](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/type_checker.cpp), native/numeric reduction and initialization portions | `Lean.reduceBool`/`Lean.reduceNat` reach `ir::run_boxed_kernel`; ordinary Nat arithmetic uses exact initialized names; Nat predicates return Bool constructors; `String.ofList` is the exact initialized string operation. |
| [kernel/inductive.cpp](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/inductive.cpp), annotation-consumer and literal-expansion portions | Group local-parameter construction calls `consume_type_annotations`; string expansion explicitly constructs `List.{0} Char`, `Char.ofNat` arguments and `String.ofList`; natural-literal expansion uses Nat zero/successor. |
| [kernel/quot.cpp](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/quot.cpp), complete file | Eq group/type/constructor checks precede quotient construction; the expected Eq alpha binder is implicit; four quotient names are checked for occupation; quotient initialization produces exactly the four primitive declarations. |
| [kernel/environment.cpp](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/environment.cpp), checked declaration portions | Safe definitions, theorems and opaques check actual values; theorem types must be Prop; the unsafe-definition path is materially different and cannot substitute for safe reconstruction. |
| [Lean/Expr.lean](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Expr.lean), annotation recognizers/consumer | Exact `outParam`, `semiOutParam`, `optParam`, `autoParam` recognition and recursive head-annotation consumption. |
| [Init/Tactics.lean](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Init/Tactics.lean#L2653) | `autoParam` has an actual `Lean.Syntax` parameter and returns its type parameter; the selected logical declaration is not an installed tactic callback. |
| [Init/Core.lean](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Init/Core.lean#L57), eagerReduce and propext portions | `eagerReduce` is the stated identity definition; `propext` is an explicit axiom, not a theorem whose truth follows from checking its type. |
| [Init/Prelude.lean](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Init/Prelude.lean), selected portions described next | The actual logical UTF-8/byte/list/numeric path, proof-bearing character conversion, Syntax data fields and logical fallback of Array.get!Internal. |

This is a bounded independent sample of the author's larger named-kernel-path inventory, not a second exhaustive repository audit. Runtime arithmetic correctness, decoder correctness and compiler/image correspondence remain assumptions/gates, not facts proved by these reads.

## Investigation of the concrete string-stage cycle concern

The investigated failure hypothesis was not hypothetical wording alone: a safe function's logical body can contain `panicWithPosWithDecl` or a similar helper with source-position/message string literals. If such a body lies in the support L that BOOT1 requires before checking any string literal, the stage graph has a real obstruction. A runtime panic annotation or a whole-file string search is insufficient to demonstrate that dependency.

Read the following actual displayed logical bodies in the pinned Prelude:

1. `String.ofList` at 3560–3561 constructs `String.ofByteArray` from `List.utf8Encode data` and the explicit validity constructor proof. The validity predicate and String fields occur at 3525–3546.
2. `List.utf8Encode` at 3517–3518 uses `List.flatMap String.utf8EncodeChar` followed by `List.toByteArray`. The character encoder at 3486–3512 uses character numeric values, ordinary arithmetic branches and explicit UInt8/list construction.
3. `List.toByteArray` at 3466–3470 folds by `ByteArray.push`, starting from `ByteArray.empty`. The byte-array logical functions at 3420–3460 use Array data, empty and push.
4. `Array.push` uses `List.concat`; Array empty uses `List.nil`. `List.concat`, `List.append`, `List.flatten`, `List.map` and `List.flatMap` at 3127–3183 have the inspected structural recursive logical bodies, not index-with-panic calls.
5. `UInt8.ofNat` at 2478 uses `BitVec.ofNat`; the latter at 2414 uses `Fin.Internal.ofNat`, which retains `Nat.mod_lt` evidence. These are pinned source bodies, not extracted canonical declaration records.
6. Nat division/modulo and their fuel/ordering proofs were inspected in the 2116–2308 region. Their displayed logical bodies use decidable arithmetic branches and structurally fuelled recursion. No message-string/panic edge was observed in those bodies.
7. Char's validity predicate/group, private `isValidChar_UInt32` proof, `Char.ofNatAux` and `Char.ofNat` were inspected around 2844–2894. The invalid-codepoint branch constructs the zero character with explicit proofs; it is not a panic branch requiring a string message.

No message literal, `get!` or panic dependency was visible on that inspected support spine. Moreover, the adjacent **safe logical** `Array.get!Internal` at 3324 is `Array.getD a i default`, despite its runtime documentation talking about panic. Treating its runtime annotation as an automatic logical string dependency would be incorrect. The adjacent unsafe borrowed array primitive is a different declaration and cannot be admitted by conflating the names/kinds.

The separately inspected `Lean.Syntax` and `SourceInfo` group constructors refer to Name, String, raw substrings/positions, arrays and other logical data. They do not, merely by being a datatype, depend on every source function that manipulates those data. Later Name-manipulation functions containing explicit panic messages are therefore not automatically in `autoParam`'s type closure. Similarly, quoted examples in documentation are not native string-literal nodes in an accepted descriptor.

**Result of this investigation:** no concrete cycle was established in the bounded path. It is reasonable to retain the selected conservative stage gate as a candidate. It is not reasonable to mark that gate passed: implicit instance arguments, generated logical helpers, complete theorem bodies, group reconstruction and every transitive support node have not been extracted here. BOOT1 correctly says a detected residual dependency cycle blocks qualification and cannot be escaped through an axiom, unchecked insertion or a silent literal rewrite.

## Contract checks

### Exact-name meaning and execution barrier

The checker treats some names as logical primitives or special reduction operators, not merely labels. A different well-typed `Nat.add` body is therefore not an admissible foundation replacement just because it has the right arrow type. BOOT1 binds both name and exact selected safe meaning and explicitly retains source/runtime correspondence as a qualification assumption.

The inspected annotation path supports adding all four annotation gadgets to the fixed seed. Calling them only frontend metadata would miss their native group-checking use. The explicit `autoParam` logical Syntax dependency is correctly retained without granting any right to execute that Syntax as a tactic.

For the native-evaluation barrier, BOOT1 prohibits the two execution-hook names as declaration names and constant/projection references, screens seed as well as ordinary contributions, and requires all reconstructed references to resolve inside the authorized seed/generated sets. Its conditional induction also names the necessary premise that kernel-generated constants are covered by the inventory. It does not confuse string **data** spelling a forbidden name with a constant reference to that name. This is the appropriate reachability argument; a blacklist applied only to theorem roots would not suffice.

### Literal prerequisites and order

The stage rule for natural literals requires Nat, not every arithmetic function. This avoids forcing a definition such as Nat.div to precede its own body literals. Bool support is required before the native Nat predicate path can synthesize Bool constructors. String support is explicitly broader because native expansion creates Char/List/String references absent from a literal node's explicit constants.

Atomic units distinguish permitted internal group recursion from external dependency cycles. Kahn ordering with a fixed tie-break is a finite reproducible procedure on a validated finite source collection. A cycle produces an obstruction, not a miraculous bootstrap. The exact generated group inventory and source-group recovery remain important: reconstructing only an apparent recursor-shaped name would not establish membership or safe replay.

### Checked insertion and authorized axioms

The inspected native insertion source supports BOOT1's distinction between checking actual safe definitions/theorems/opaques and accepting serialized ConstantInfo. BOOT1 also excludes the unsafe mutual-definition shortcut and requires exactly one authorized quotient initialization with empty names. Internal `add_core` calls belonging to that qualified primitive operation are not exposed as arbitrary peer insertion authority.

The axiom policy is exact: propext, Classical.choice and Quot.sound with their selected types. The public-import axiom-shape problem is addressed by requiring complete actual declaration kinds/bodies and refusing other axioms. This also blocks fresh compiler-generated evaluation axioms whose names are not the two historical native-execution hook names.

Per-export support traverses fixed theorem/opaque bodies and real declaration/group dependencies. It does not charge every installed axiom as though every proof used it, and it distinguishes explicit axiom use from builtin arithmetic/literal/quotient semantics and conservative construction ordering. That is a sound separation of declared assumptions and ambient installation under the specified conditional foundation model; minimal logical axiom dependence is not claimed to be computed.

### Candidate FoundationID construction

The inherited descriptor grammar already provides inline name-local bootstrap terms and proofs. It therefore supports the dependency order

`source commit + descriptor sequence + export list -> SeedProfileID -> ReservedNamesID`,

with NativeRulesID formed separately and FoundationID committing to the source/seed/rules/reserved-name IDs. No ordinary F-bound ProofInstance is needed inside the seed. Changing a seed theorem's proof changes the seed and foundation, even if its statement is unchanged; ordinary PI1 semantic/evidence separation starts only after that foundation exists.

The exact exported-name sorting and ReservedNames index consistency bind names without a hash fixed point. Including generated inventory as derived qualification output rather than silently adding another SeedProfile field preserves the chosen schema. Actual bytes and resulting IDs still need to be produced; the absence of a current digest is explicitly reported rather than filled with an editorial checksum.

## Gates that remain real

- A complete full-body source collection and correct source-group recovery must exist for the selected roots. The bounded source spine is not that collection.
- The full stage/dependency graph, especially the conservative String gate and nested Syntax/group support, must actually close and order successfully.
- Every safe body/constructor and every authorized primitive output must replay under the exact pinned qualified kernel and selected HEIGHT1 behavior, with exact generated-inventory correspondence.
- Exact native widths, UTF-8/literal bounds, hash/decoder behavior, source/runtime arithmetic agreement, checker image and resource containment need actual qualification.
- Full closure and reconstruction costs must fit supplied resources; source readability does not establish practical runtime/memory.

These are implementation-qualification gates, not newly found source counterexamples in this audit. They would become concrete candidate blockers if extraction/replay exposes the specified obstruction. No evidence here licenses declaring the ultimate decentralized software goal complete or the foundation already deployed.
