# CP-001H: exact-name foundation and bootstrap contract

Date: 2026-09-20. Status: selected concept refinement with [independent bootstrap review](../audits/CP-001H-bootstrap-cross-audit.md) and bounded source audit. No Lean build, native execution, artifact extraction, implementation, exploit, executable model, or benchmark was performed. Frozen CP-001G and earlier checkpoints are unchanged.

Source pin: Lean `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b` (`v4.34.0`). Matching mathlib remains `5ed2965256430c3649e86755f9576b54eca72435`; the bootstrap in this note uses Lean logical declarations, not the whole mathlib library. Every source line reference is to the Lean pin.

## Outcome and scope

Select **BOOT1**, a name-local, checked, source-derived foundation construction. Its immediate corrections are concrete:

- Retain the exact safe logical definitions of `outParam`, `semiOutParam`, `optParam`, `autoParam`, and `eagerReduce` as seed roots. Their exact names affect kernel behavior; they are not all disposable frontend metadata.
- Bind every arithmetic/literal/quotient name below to its exact qualified declaration and generated role. A matching type is insufficient for a builtin arithmetic name.
- Exclude `Lean.reduceBool` and `Lean.reduceNat` throughout bootstrap as well as ordinary contributions. The pinned kernel still contains direct calls to native evaluation for these names.
- Close the source seed over actual type, body, proof, projection, inductive-group, and implicit literal dependencies. Reconstruct groups and quotients with checked native operations, never by installing extracted `ConstantInfo` as authority.
- Construct SeedProfile before FoundationID, using only inline name-local proof evidence. There is no need for a FoundationID hash fixed point.
- Preserve an explicit finite bootstrap order and generated inventory. Failure to ground that order or match the inventory blocks this candidate; it does not license fallback axioms, ambient imports, or relaxed names.

BOOT1 is a construction/qualification contract, not a claim that the complete seed bytes or their digests now exist. This source audit identifies the required fixed-name families and selects the missing mechanism. It does not establish complete correctness of the runtime, adapter, or all source declarations.

The companion H source-to-content analysis owns ordinary source export, PI1 reference rewriting, and completed inductive-group recovery. This note owns the fixed-name boundary and name-local seed. A source exporter must map a retained seed declaration to its exact seed export, not re-export its body as an ordinary F-bound semantic object.

## Why checked insertion alone does not select a foundation

Let K be the pinned checking program, S an ordered seed descriptor sequence, and E(S) the checked environment obtained from S. Three different obligations are required:

1. **Binding:** S is exactly the locally selected sequence, including all types, values, names, declaration kinds, safe flags, binder information and authorized primitive initialization. A peer does not choose S merely by advertising its hash.
2. **Construction:** the receiver reconstructs E(S) using the selected checked operations and verifies their generated output. A serialized environment is not evidence of construction.
3. **Correspondence:** the exact meanings bound to K's fixed names agree with the kernel's builtin behavior. Merely checking that some body has type `Nat → Nat → Nat` does not prove that it implements the arithmetic assumed by K's `Nat.add` reducer.

For example, retaining a different safe well-typed definition at the exact name `Nat.add` while keeping the builtin reducer would create two incompatible interpretations. The remedy is exact source-derived, locally authorized meaning and primitive-role binding, not reputation, identity voting, or accepting an arbitrary declaration because its name is familiar.

The conditional foundation assumption remains substantive: K and the pinned runtime implement the selected logical rules correctly, and the source-derived builtin definitions agree with those rules. This note narrows what must be inspected; it does not derive consistency of Lean from its own acceptance.

## Concrete kernel-sensitive name inventory

The following is the audited semantic inventory for the inspected kernel paths and the name-sensitive helpers they call. All nonforbidden entries are selected fixed seed meanings, with complete safe logical closure. Generated recursors are additionally inventoried by their owning groups; they are not guessed from spelling.

| Exact name or family | Observed behavior and pinned source | BOOT1 disposition |
|---|---|---|
| `Nat` | `kernel/expr.cpp:78–79` calls exported `lean_lit_type`; `Lean/Expr.lean:621–627` maps a natural literal to this exact type | Exact checked Nat inductive group, with its source constructor roles and generated recursor |
| `Nat.zero`, `Nat.succ` | `type_checker.cpp:637–641,702–712`; `inductive.cpp:1359–1365` converts a literal to zero/successor form | Exact constructors of that same Nat group, not independent definitions of matching types |
| `Nat.add`, `Nat.sub`, `Nat.mul`, `Nat.pow`, `Nat.gcd`, `Nat.div`, `Nat.mod`, `Nat.beq`, `Nat.ble`, `Nat.land`, `Nat.lor`, `Nat.xor`, `Nat.shiftLeft`, `Nat.shiftRight` | Builtin reductions at `type_checker.cpp:644–732`; exact initialized names at 1328–1341 | Exact safe source definitions and complete selected proof/dependency closure; no rebinding or name-only acceptance |
| `Bool`, `Bool.false`, `Bool.true` | Nat predicate reducers produce Bool constants at `type_checker.cpp:692–699`; `library/util.cpp:689–710` and `library/constants.cpp:145–149` bind their exact names; `type_checker.cpp:1177–1183` additionally recognizes `Bool.true` | Exact Bool group and constructor ordering; include it before any seed operation capable of producing those constants |
| `String` | `Lean/Expr.lean:621–627` supplies the exact type of native string literals | Exact pinned String structure and full logical closure; this pin's constructor is `String.ofByteArray`, not an invented `String.mk` |
| `String.ofList` | `inductive.cpp:1368–1379,1394`; string-literal comparison at `type_checker.cpp:1145–1155` | Exact safe source definition, not an alias substituted for an older constructor |
| `Char`, `Char.ofNat`, `List`, `List.nil`, `List.cons` | String expansion constructs `List.{0} Char` using these names at `inductive.cpp:1396–1401` | Exact groups/definitions and universe instantiations, with checked logical support |
| `Eq` and its sole constructor | `quot.cpp:19–44` checks exact Eq type shape and the type of its unique constructor before quotient initialization | Exact source Eq group, including constructor `Eq.refl` and binder-info metadata; the kernel obtains the constructor from the group rather than requiring its spelling in this check |
| `Quot`, `Quot.mk`, `Quot.lift`, `Quot.ind` | `quot.cpp:47–102` constructs them; `quot.h:27–83` recognizes their exact computation/elimination forms | One authorized quotient-initialization descriptor after Eq; compare exact generated kinds/types/universe lists; raw peer quotient records are prohibited |
| `outParam`, `semiOutParam`, `optParam`, `autoParam` | `inductive.cpp:222,227` calls `consume_type_annotations`; `expr.cpp:363–365` delegates to `Lean/Expr.lean:1738–1745`, whose recognizers at 1709–1727 use these exact names | Add all four exact safe logical definitions to seed roots; retain their logical argument data, not executable elaboration behavior |
| `eagerReduce` | `type_checker.cpp:168–185` recognizes its two-argument application and enables eager comparison; Bool reflection uses the flag at 1181 | Add exact safe identity definition from `Init/Core.lean:57`; count the pinned checking behavior as part of K, not a new axiom |
| `Lean.reduceBool`, `Lean.reduceNat` | `type_checker.cpp:614–634` calls `ir::run_boxed_kernel`; reached from `whnf` at 762 and lazy conversion at 1101 | Forbidden in every seed descriptor and external reference closure; never insert a declaration at either name |

The source definitions of the arithmetic roots are located at `Init/Prelude.lean:1773,1794,1809,1823,1893,2127,2186,2274`; `Init/Data/Nat/Gcd.lean:35`; and `Init/Data/Nat/Bitwise/Basic.lean:50,58,66,79,95`. These are source anchors, not substitutes for extracting their full elaborated safe values and support. Their `extern` annotations do not turn compiled implementations into accepted proof evidence.

The expanded String logical path was established in [CP-001F](CP-001F-lean-producer-client-path.md): it includes byte arrays, UTF-8 encoding and proof-bearing data. BOOT1 retains that conclusion. It does not revive the withdrawn `String.mk` root merely because earlier prose mentioned it. A source declaration with a similar friendly name has no special status.

### Annotation gadgets are logical definitions, not installed tactics

Their source meanings are explicit:

| Definition | Source meaning | Source anchor |
|---|---|---|
| `optParam` | `(α : Sort u) → α → Sort u`, returning α | `Init/Prelude.lean:675` |
| `outParam` | `(α : Sort u) → Sort u`, returning α | `Init/Prelude.lean:693` |
| `semiOutParam` | `(α : Sort u) → Sort u`, returning α | `Init/Prelude.lean:716` |
| `autoParam` | `(α : Sort u) → Lean.Syntax → Sort u`, returning α | `Init/Tactics.lean:2653` |
| `eagerReduce` | `{α : Sort u} → α → α`, returning its argument | `Init/Core.lean:57` |

`autoParam` therefore brings in the **logical datatype** `Lean.Syntax` and its necessary support. `Prelude:4934–4976,5026–5096` shows the path through SourceInfo, names, strings, raw substrings/positions, arrays, and syntax constructors. This does not import parser tables, execute the syntax as a tactic, or include every function that operates on syntax. A datatype whose values describe programs is not a permission to execute those programs.

The selected contract does not replace `Lean.Syntax` by a smaller guessed type or erase a retained logical default argument. Even where an annotation can be unfolded extensionally, silently changing it would alter canonical source correspondence and potentially recursor reconstruction. Seed transparent definitions use the already selected HEIGHT1 reconstruction rule, not their producer's reducibility hints as authority.

### Internal names, generated interfaces, and ordinary local names

Some fixed strings are not declarations to bootstrap:

- `_kernel_fresh`, `_ind_fresh`, `_nested_fresh`, and the default `_uniq` are internal fresh-name prefixes. See `type_checker.cpp:1320,1345`; `inductive.cpp:1386–1389,1403–1404`; `util/name_generator.cpp:91–95`.
- `_nested` is a temporary nested-inductive namespace. `inductive.cpp:1222–1231` rejects it in both constant references and projection structure names in submitted group types/constructors. Such temporary references must also be absent from the final regenerated inventory.
- `dontcare` is a substitution dummy used for unused binders (`type_checker.cpp:799–805`), not a theorem or useful seed declaration. `__expr_for_default_constructor__` and `__local_decl_for_default_constructor` are construction sentinels (`expr.cpp:131–137`; `local_ctx.cpp:127–133`).
- `name::mk_internal_unique_name()` supplies numeric-root internal names (`util/name.cpp:417` and `util/name.h:85–98`); those are not source declarations to import as foundation members.
- `.rec` and the nested helper names obtained from `.rec` by `append_after(next_idx)` are generated group members. Inventory their actual qualified outputs; do not accept every constant whose name looks like a recursor.
- Strings such as `u`, `v`, `a`, `motive`, binder names and `_ih` suffixes in this code are local/universe naming devices, not a global reserved declaration family.

For seed input and final declaration inventories, prohibit the internal prefixes, numeric-root internal names and sentinels above as declaration names or constant/projection references. Closed term validation separately excludes free/metavariable escapes. Do not blanket-ban every underscore-prefixed source name: legitimate private logical helpers can be needed in the exact source closure. Their names are admitted only by the locally frozen seed inventory, not by a wildcard.

The current ReservedNames schema contains **exact-name entries**, not wildcard prefix entries. Represent exact forbidden names with `[]`; enforce internal-prefix exclusion through the fixed decoder/reconstruction name discipline. Do not silently reinterpret an exact entry as a prefix rule. Every ordinary contributed constant name is receiver-generated under the disjoint `DTMKN` naming scheme, including PI1 `.w` names; a peer cannot choose `_nested`, `Nat.add`, or a native-evaluation name as its declaration name.

## Selected BOOT1 derivation algorithm

This is the finite algorithm selected for later qualification. Its input is a complete, immutable, error-free, owner-controlled source collection at the pin, with full actual declaration kinds/bodies. Its output, when successful, is the canonical descriptor sequence, export list, reserved-name table and exact generated inventory. The source collection is extraction input, not receiver authority.

### Root set and logical closure

Start with the earlier core logical groups, `Iff`, `Nonempty`, the exact three permitted axiom schemes, the quotient operation, every nonforbidden name in the inventory above, and each name's owning inductive group where relevant. Use `String.ofList` and the actual String constructor/support for this pin. No mathlib-wide root is added merely because a producer imports mathlib.

Iterate the following closure to a least finite fixed point over the completed source collection:

1. Include every constant referenced in each selected type, value and constructor type, every projection's structure declaration, and the exact level instantiations. This includes actual theorem and opaque bodies, even when they are erased at runtime or proof-irrelevant.
2. If a selected declaration is an inductive, constructor, or recursor, resolve its owning source group and include the complete original group descriptor and all its constructors. Regenerated ordinary/nested recursors are outputs of that one group operation; do not add arbitrary raw recursor records as inputs.
3. Include the implicit literal support roots below, because literal syntax does not explicitly contain its type or expansion constants. Include Eq before quotient initialization and the Bool group before the Nat predicates that can produce Bool constructors.
4. Diagnose an unresolved name, missing full body, unsupported declaration kind, nonpermitted axiom, unsafe/partial dependency or forbidden name distinctly. None may be filled with a source signature or imported abstract axiom-shaped public view.

The only admitted primitive-axiom descriptors are the exact pinned schemes `propext` (`Init/Core.lean:1607`), `Classical.choice` (`Prelude:809`) and `Quot.sound` (`Prelude:4776`). Checking their types does not prove them. Every other actual axiom is prohibited, including fresh compiler-evaluation axioms regardless of their names. The forbidden-name list supplements this exact axiom rule; it does not replace it.

Include all retained safe logical declarations and all regenerated members in the seed's export list. This selected uniform rule avoids an ambiguous category of hidden fixed-name support that is present in the environment but neither exportable nor genuinely forbidden. Exporting its inert logical descriptor does not export a plugin, source file permission, or author attribution policy. SeedProfile already permits a variable finite export list; no external name-local reference grammar is introduced.

### Literal-aware stage ordering

Explicit reference closure alone is insufficient. For example, a natural-literal node contains no reference to Nat, and string expansion creates Char/List/String references not present as constant nodes in the original literal. Conversely, demanding that **all** Nat arithmetic roots precede **every** natural literal would impose an artificial self-dependency on ordinary arithmetic definitions.

Define the support basis N as the complete checked Nat group, B as the complete checked Bool group, and L as the complete checked logical support of `String`, `String.ofList`, `Char`, `Char.ofNat`, `List.nil` and `List.cons`, including their groups and selected dependencies. Add these selected conservative stage constraints:

- A descriptor containing a natural-literal node requires N already constructed. It does not thereby require `Nat.gcd`, `Nat.div`, or every other arithmetic root.
- A descriptor containing a string-literal node requires L already constructed. This strong gate covers both literal typing and possible later expansion during its check without modifying the kernel to add a new dynamic hook.
- A descriptor referring to `Nat.beq` or `Nat.ble`, including their logical dependencies, requires B. Their own declarations also require B through their types.
- Quotient initialization requires the complete Eq group and an uninitialized quotient state with all four quotient names unused. Later descriptors referring to Quot require that operation already completed.
- Annotation gadget references require their exact earlier declarations; `autoParam` requires its actual Syntax support, not a syntactic promise that it will never be inspected.

Construct atomic dependency units: one safe definition/theorem/opaque/authorized axiom per unit, one complete inductive group per unit, and one quotient initialization unit. Group-local recursive occurrences permitted by the native inductive checker are not external precedence edges. Generated member references point to the owning unit. Safe compiled recursive functions must have their actual noncyclic elaborated logical bodies; a raw unsafe/partial mutual-definition operation is not an accepted shortcut.

Use dependency-respecting Kahn ordering, breaking ties by the canonical smallest emitted source-name path of the ready unit; the quotient unit has its fixed output names for this comparison. Compute this order from a prevalidated closed collection, before checking. A nonempty residual graph is a named dependency/stage obstruction. Do not choose an arbitrary SCC insertion, insert forward axioms, or call unchecked insertion to escape it.

This deliberately conservative string gate may reject a source closure whose pre-support declarations themselves contain string literals. We have not extracted the full closure and do not claim that this obstruction is absent. If it occurs, BOOT1 returns that exact obstruction and this candidate remains unqualified. Relaxing the stage gate or introducing a proved literal-elimination/bootstrap transformation is a separately specified correction, not an implicit fallback. The finite ordering algorithm and its possible failure are selected now; actual successful ordering remains evidence to produce later.

### Checked replay and inventory comparison

Replay the ordered descriptors in a genuinely empty environment through the checked declaration entry point. Forbid a path to `lean_add_decl_without_checking`, source import, plugin loading, arbitrary runtime extensions or the environment's raw constant insertion API. The pinned kernel itself uses internal `add_core` during its authorized inductive/quotient construction; that is different from exposing raw insertion to the adapter or peer.

Preserve exact native binder-info codes in bootstrap descriptors. Quotient initialization compares Eq shapes structurally (`quot.cpp:33,42`), so the ordinary contribution rule that normalizes binder information must not accidentally be applied to seed Eq. Seed universe parameters and local binders remain canonically represented as the existing bootstrap grammar prescribes.

For a safe definition, reconstruct the exact selected type/value and derive HEIGHT1 before insertion. For a theorem, check that its type is Prop and check its full exact body; for an opaque declaration, check its full body while preserving opacity. The source-backed checked routes are `environment.cpp:160–222`. Authorized axioms enter only at their exact prescribed types; quotient initialization is exactly one descriptor `[4]`.

For each inductive unit, regenerate all types, constructors, ordinary recursors, nested helper recursors and their reduction metadata using the checked operation. Compare the complete normalized output against the selected source correspondence and frozen expected inventory, including group ownership, constructor order/fields, universes, parameter/index counts, safety, recursor rules and every retained reference. The H exporter contract determines completed source group recovery. A source name that merely ends with `.rec` is not an ownership certificate.

For quotient initialization, compare exactly the four generated declarations and quotient-initialized state. The constructor operation at `quot.cpp:53–56` refuses preoccupied names. Calling it twice would return an already initialized environment at 48–49; BOOT1 nevertheless requires exactly one initialization descriptor, avoiding multiple canonical inputs for the same intended event.

After every unit, preserve no-overwrite and closed-prefix invariants; after all units, verify no unexpected declaration escaped into the final inventory. Sort every emitted declaration name by its canonical name-path bytes to obtain seed export indexes. ReservedNames maps each retained name to precisely that index and includes the exact forbidden-name entries. The table is locally fixed data, not publisher authority to extend the foundation.

## Noncircular identities and seed proof evidence

Use the inherited canonical typed hashes. Let C be the source commit, D the name-local descriptor sequence, X the sorted export-name list, and V the exact rule/feature/axiom record. Compute in this dependency order:

\[
S = H_{0x0002/1}([C,D,X]),\qquad
N = H_{0x0003/1}(V),
\]
\[
R = H_{0x0004/1}([S,\operatorname{ReservedEntries}(X)]),\qquad
F = H_{0x0001/2}([0,C,S,N,R]).
\]

D has no S, R or F reference. Its constant references are bootstrap-only `[6,namePath]`, with full inline name-local types and values; its terms omit FoundationID. R depends on S; F depends on S, N and R; none points back to F. This is a directed acyclic hash construction, not an identity cycle. The SeedProfile/ReservedNames source-commit and export-index consistency checks remain mandatory.

A seed theorem's proof is **not** an F4 ProofInstance object. It is the exact name-local value in its seed theorem descriptor. Its references to earlier seed theorems resolve to their fixed checked seed declarations. Changing that value changes D, hence S and F, even if its proposition stays the same. Ordinary PI1 semantic/evidence separation begins after F exists; seed construction is a finite selected trust basis, not an attempt to import the whole future corpus into itself.

A local implementation may index/serialize the generated seed inventory for diagnostics and qualification. That record must be derived from S plus the selected K/N reconstruction semantics, or committed by an explicitly versioned future schema. Do not silently add an inventory digest field to the existing SeedProfile payload. No new hash is claimed merely because this Markdown inventory has an editorial checksum.

Changing the retained seed or export order gives a new SeedProfileID, ReservedNamesID and FoundationID. It does not relabel older content or certificates. This is a newly qualified seed candidate under the selected F4/NativeRules-code-4 family, not a claim that a previously frozen actual F4 digest is unchanged: no complete actual seed or FoundationID digest has yet been derived. The descriptor and ReservedNames grammars already express these additions; no new schema is required just to include five extra fixed-name roots and their closure. PI1/HEIGHT1 remain the selected rules. If an implementation instead changes the native interpretation, reference grammar, or encoded payload shape, it must take the corresponding explicit new rule/schema boundary. Integration selects the authoritative profile; frozen F4 text is not rewritten in place here.

## Name-barrier argument against native evaluation

Let A be the exact seed declaration-name set, G the receiver-generated contributed names, I the internal temporary-name set, and U contain at least `Lean.reduceBool` and `Lean.reduceNat`. Enforce:

\[
A\cap U=\varnothing,\quad G\cap U=\varnothing,\quad
A\cap G=\varnothing,
\]

with input constant/projection references resolving only to an actual A or G member or an allowed group-local reference. Seed descriptor names and all name-local references are screened before any replay. U is prohibited even in an unreachable branch or a proof/type annotation; ordinary axiom classification is an additional check. These are declaration/reference-name restrictions, not a ban on inert string data that happen to spell a forbidden name.

The inspected ordinary kernel reductions synthesize the fixed Nat/Bool/Char/List/String/Quot names or declaration-owned generated members inventoried above, not a U name. Substitution, projection, beta/delta reduction and checked group reduction draw their referenced constants from existing checked terms/rules. Subject to correct implementation and the inspected synthesis coverage, induction over reconstruction/reduction therefore preserves absence of U. The equality tests at `type_checker.cpp:618,626` cannot succeed, so those calls to `ir::run_boxed_kernel` are unreachable on admitted evidence.

This is a conditional **name-closure argument**, not a claim that a C++ kernel executes no machine code, that all native runtime arithmetic has been formally verified, or that sandboxing is unnecessary. Trusted builtin natural arithmetic and literal processing are still part of K's runtime boundary. Host bugs, resource exhaustion and supply-chain failures remain separately contained and qualified.

If a future kernel revision adds a new fixed-name execution hook, this inventory and argument must be reopened under a newly qualified source pin. A dynamic blacklist of two historical names is not the long-term specification: the rule is closed authorized seed/contribution references plus audited kernel-generated names and no peer-selected execution authority.

## Footprints and conditional guarantees

Seed exports are not footprint black boxes. For each reached export, recursively traverse its fixed type, body, theorem/opaque evidence, owning group rules, actual dependencies and required builtin feature support. Derive and bind a separate actual support/axiom summary for each export; do not charge every installed seed axiom to every proof merely because that axiom is present in the initial environment. Distinguish explicit axiom schemes from primitive quotient rules and literal/arithmetic behavior. A proof-irrelevant seed theorem still carries its actual assumption dependencies. Conservative construction-stage prerequisites are not automatically logical axiom uses of each later result.

For a descriptor sequence accepted by BOOT1, the following argument is by induction on its ordered units:

- Every fixed input reference resolves to an already checked prefix or the current valid native group-local context; implicit literal prerequisites also hold.
- Every added nonaxiom is checked with its actual selected evidence; generated declarations arise only from the qualified group/quotient operations; no previous meaning is overwritten.
- Every explicit axiom is one of the exact three selected schemes, and the native-evaluation names remain absent.
- The resulting environment and its exports are bound to S and the selected K/N interpretation; F commits to that selection before ordinary F-bound content is processed.

Consequently, under the hash-binding, decoder, checked-reconstruction, source/builtin-correspondence and kernel-soundness assumptions, a later accepted proof establishes its stated contextual judgment over this exact foundation and recorded footprint. This does not imply that every true theorem is discoverable, every source library is exportable, every checker run terminates within a budget, or mathematics grows exponentially. It provides the reliable substrate on which useful decentralized reuse and contribution can be assessed.

## Bounded evidence and next qualification boundary

This audit inspected fixed-name uses in all `.cpp`/`.h` files of `src/kernel`, the literal-type and annotation-consumer definitions exported from `Lean/Expr.lean`, the Bool-constructor helper in `library/util.cpp`/`constants.cpp`, and the internal-name helpers in `util/name.cpp`/`name_generator.cpp`. Relevant logical definition/type sources were read at the locations above. That is a bounded source-path/name inventory, not an exhaustive security audit of the repository, compiler or runtime. Foreign helper correctness and actual emitted artifact contents are not established by these reads.

The next qualification evidence must instantiate this exact algorithm: complete full-body seed collection, actual closed/staged ordering, canonical descriptors and indexes, checked replay, generated-inventory correspondence, exact axiom/rule closure, and deployed adapter/image binding. None has been fabricated in the concept phase. In particular, the string-stage gate and the complete safe closure of the Syntax/String/numeric support remain specific outstanding checks, not promises already fulfilled.

The project gain is practical: independent agents can agree on exact reusable mathematical meanings without agreeing on authors, historical attribution or a global ledger. A peer's contribution cannot silently redefine arithmetic, replace another seed theorem's proof, introduce a compiler oracle, or expand the foundation through a familiar source name. That is the fixed substrate for reciprocal mathematical accumulation, while independent local agents remain free to choose what to prove and reuse.
