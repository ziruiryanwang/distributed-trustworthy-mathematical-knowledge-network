# Original-reference-backed generated deltas: minimal native contract

**Current conditional boundary:** native05's abstraction/partial-basis policy
and source/build have passing reviews below; the earlier04 refusal and one
diagnostic census are preserved. The actual05 correspondence continuation and
protected reference registration remain separate gates. The delta contract now
uses05's per-view abstract projections and dependency-closed usable basis, not
the earlier theorem-only/all581-public policy. Implement only a freshly selected
successor; never weaken the live registered-base premise to bypass a failure.

2026-10-24. Source/theory investigation by `reference_soundness_audit` under
`E:\Distributed Trustworthy Mathematical Knowledge Network`; canonical guard
passed. No native import, compiler, experiment, owner operation, package or Git
mutation was performed. This is a proposed successor contract, not implemented
or executed correspondence evidence. Earlier matcher/build reviews are reused,
not repeated. Root owns controller/store selection; native implementation has a
separate owner. See `ORDINARY-REFERENCE-LIVE-INTEGRATION.md` for that integration
owner's file-set and ordinary-authoring proposal.

## Decision

Use the existing build / private reread / exported reread module pipeline with
one new **reference-backed, all-new-delta** base mode. A protected original
reference supplies the base imports and allowed frontier. The new request carries
only genuinely new units; original units are not reconstructed, rechecked or
inserted as axioms. Keep the existing Init/generated-anchor route distinct.

The first generated module imports the exact registered original root vector.
Subsequent generated modules import only their preceding generated parent, using
the same public/non-import-all/non-meta edge. They inherit the same reference
base. No mixed unrelated roots, automatic branch merging, synthetic empty
wrapper, general new acceptance rule or certificate system is needed here.

This is module **materialization** of current owner-warranted units. Ordinary
source authored against the library produces candidates, which still pass the
existing strict owner admission before materialization. A successful source
compile, native pending report or saved correspondence report is not a warrant.

## Exact source facts that control the design

- `ordinary_module_anchor/OrdinaryModule04.lean` currently supports Init or a
  chain of generated `DMKNBridge_*` modules; its generated-plan parser is not an
  original-library reference parser. It already checks the new delta twice,
  writes five artifact parts, and requires separate private/exported rereads.
- Its `checkInventories` and `checkAnchorRecords` inspect frontend lookup after
  `setExporting`; they do not themselves inspect `toKernelEnv`. The new route
  must not infer the kernel view from those checks.
- Lean `Environment.toKernelEnv` returns `env.checked.get`. `setExporting`
  changes frontend lookup selection, not that checked kernel map.
- Lean `Import` defaults are precisely `importAll=false`, `isExported=true`,
  `isMeta=false`. `BaselineArtifactCore04.rootModules` uses those defaults.
- `importModulesCore` computes effective module import states through the
  original DAG. `mainModule?` selects the data constructing the kernel map;
  `publicModule?` supplies the public frontend map. They are distinct choices.
- The registered-reference matcher already relates private frontend/kernel and
  exported-import frontend/kernel to warranted original records. Its public
  frontier is a whole-unit closure under the union of both exported views'
  semantic dependencies, with separate `projection` and `kernel_projection`.

Inspected source identities:

| Source | SHA-256 |
|---|---|
| `software/v5/ordinary_module_anchor/OrdinaryModule04.lean` | `901e4fc06351f6ad658eba9b5ea23ab644648646c8567fc035b057aa1883cfe8` |
| `software/v5/ordinary_baseline/OrdinaryReferenceBase04.lean` | `c7c0636b7252a3f62d277bb7497a14f7686b7ec61fdd722d6bb05dbba0ca5b19` |
| Selected runtime `src/lean/Lean/Environment.lean` | `ee364e4788ce0560c87f621eeb3c4c3dfec62e8db4e15e099fd80e6adc533b86` |
| Selected runtime `src/lean/Lean/Setup.lean` | `eff05a30636e084ecf7c52e4019a1f5497d48b5b023b73f0e979abde91d419a5` |

## Why a wrapper preserves the approved interpretation

Let `A` be the exact original artifact map, `R` its ordered root imports, and
`E_l = importModules(R, A, level=l, loadExts=false, plugins=[])`, for
`l` private or exported. Every root edge in `R` has flags `(false,true,false)`.
Let a fresh modern module `W` contain only new declarations, with direct imports
**exactly** `R`. Import `W` through that same standard edge using `A` plus W's
exact five parts. Require no new module-key collision, no new declaration-name
collision with the original private environment, and no other imports/overlays.

The original-module effective import states are unchanged:

1. At private level, the importer forces `importAll=true` at every edge,
   independently of the declared import-all bit. The original graph is therefore
   visited exactly as in the registered private import. The extra wrapper adds
   its own module, not another interpretation of an original module.
2. At exported level, a standard root edge sends state
   `(importAll=false, isExported=true, needsData=true, needsIRTrans=false)` to
   each original root. Inserting W adds one standard edge and sends exactly the
   same state from W to each original root. Subsequent propagation, including
   the existing graph's private/meta edges and joins, is the same fixed-point
   calculation over the same header bytes.
3. `mainModule?`, `publicModule?` and the original module order consequently
   select the same original declaration data. `finalizeImport` cannot merge a
   new record into an original name because collisions are forbidden. Thus the
   kernel and the applicable frontend constant maps, restricted to original
   declarations, agree with their registered counterparts.

The argument inducts over a chain of such generated wrappers. It is a
source-grounded argument for this pinned importer, not a machine-checked Lean
metatheorem. It concerns mathematical `ConstantInfo` interpretations, not equality
of every environment field: module indices/headers grow, and frontend extension
state is deliberately outside this native `loadExts=false` lemma.

The proof fails if an import becomes nonpublic, import-all or meta; another root
is added; original artifact bytes/support change; a generated module shadows an
original name; or ambient lookup supplies a missing artifact. Those cases must
refuse or acquire a newly established correspondence. Do not silently reuse this
lemma for arbitrary merges or merely equal module names.

## Protected base data, not another proof payload

Represent the original reference separately from the generated chain. A concrete
base-plan record must bind the following data; root may choose field spelling:

| Data | Required interpretation |
|---|---|
| Reference ID, snapshot ID, support ID, semantic/foundation IDs | One locally registered live correspondence event and its exact current owner/support binding, not a peer claim |
| Exact ordered root names and fixed edge flags | The same root vector used for correspondence; flags may be fixed by the schema rather than repeated |
| Complete original module artifact map | All five pinned parts for each selected module, including runtime/Init dependencies; no runtime-path fallback |
| Private/exported original module-name lists | Expected original loaded-module census/order from the registered event; exclude appended generated wrappers when comparing |
| Public whole-unit frontier | Unit ID, exact name/export-ID bindings, original kind, ordered universes, frontend projection and kernel projection |
| Public basis interpretation | All581 original rows with separate per-view projections/absence and the exact ordered usable-basis subset derived by05; private availability is not public authorization |
| Generated chain | Existing locally registered generated modules/parts, exact parent imports, new-name census and current warranted bindings |
| Exact plan digest in request/pending/final records | One base and chain throughout all phases; neither a request-supplied path nor a saved native response confers authority |

The original private proof closure and actual correspondence event remain retained
as registration evidence, but are not serialized into every delta request. The
controller must authenticate that the reusable public frontier is the one derived
by that event, is whole-unit and closed, and still agrees with current warrants.
An arbitrary subset of names with matching kinds is not a replacement frontier.

Reference limits are distinct from generated-delta limits. Do not accidentally
put the original library inside the old 32-generated-module/256-MiB chain budget
or silently truncate it. Reuse the snapshot's finite original-artifact limits,
and separately preserve finite new-delta and generated-chain limits. All limit
or budget failures are explicit refusals; no automatic allowance renewal follows.

## Native successor obligations

### Before either checking pass

Parse the selected reference-base plan and generated chain. Form one disjoint
artifact map: original snapshot plus registered generated modules. Require exact
module/part identities, modern modules, no conflicting module key or output
path, and correct ordered direct imports for every generated module. Set
`searchPathRef` to `[]` in this route. The whole import closure, not only project
roots, is explicit. Keep `plugins=[]`, `loadExts=false`, finite kernel limits and
the pinned importer/checker profile.

Restore the base at private level and at exported level. For each, check the
original-module census against the registered corresponding list, generated
headers against their exact plans, and output-module names against the original
map as well as the generated chain. No undeclared extra original dependency or
extra generated module is acceptable. The immutable import-chain premise above
provides semantic identity; metadata checks alone do not.

For each original frontier binding, check compact record metadata in **both**
actual maps. Private records must have the original kind and ordered universes,
with neither unsafe/partial nor new axiom records. At exported level inspect
`(env.setExporting true).find?` and `env.toKernelEnv.find?` independently. A view
record may be a safe axiom only when that view's registered projection is the
matching `erased_singleton_theorem`, `abstract_singleton_definition` or
`abstract_singleton_opaque` label for its original kind. A registered `full`
view requires its original record kind. No implicit projection change is
permitted. Preserve registered basis absences as well as present projections;
fixed permitted primitive axioms remain a separate exact policy, not abstract
selected units. Compact checks rely on immutable-import preservation and the
live registration, not on signature/kind metadata as independent authority.

### Decode and check only the new delta

Allowed external names are the **registered usable basis**, not all581 private
basis names, plus the authenticated public
frontier and registered generated ancestors; add preceding new outputs as each
unit is decoded. Imported ambient declarations are not authorized merely because
Lean can resolve them. Preserve complete generated groups, ordered universes,
metadata and the existing exact descriptor/inventory semantics.

For this new mode require **every requested unit to be new**. Reject a proposed
name present in either private kernel or private frontend, in any original or
generated-parent record. Do not invoke the old installed-singleton-theorem
matching shortcut; `units_matched=0` and `matched_unit_indices=[]`. If an
ordinary original theorem is needed, add it through a separately established
reference frontier instead of silently treating a collision as a new delta.
This conservative rule removes an extra correspondence case and does not change
the legacy Init mode's supported matching behavior.

Run unchanged `CheckedExtension.checkBatch` twice: once over the private base,
once over the exported-import base. The latter uses its actual kernel map, not
an assumed public projection. Both must accept the **same** new inventories.
Require all new records' exact inventories in the kernel and applicable frontend
maps. Preserve the existing bounded stage-two census and `doCheck=true` path.
Private success never waives exported incompatibility, including conversion
lost through theorem-body erasure.

### Write and reopen

Write from the exported-pass environment, with only the exact selected imports
and new declaration census. Recheck new names/values in kernel, private frontend
and public frontend before writing. Added declarations must not overwrite or
promote hidden original records; the existing checked-new-recursor exposure is
not a general import-promotion mechanism.

Keep the worker's three separate native phases. It binds plan/request/parent
parts across build, private reread and exported reread and hashes all five output
parts. Each fresh reread validates exact written header/imports/name census,
original/parent preservation and **new inventory equality in the actual kernel
as well as the relevant frontend view**. Original proofs are not decoded again.
The pending report alone is not accepted; both rereads and the clean enclosing
event must succeed before the controller registers the generated module.

## Smallest implementation path and evidence

1. Fresh successor of `OrdinaryModule04`: add a tagged reference-base parser/import
   provider and all-new mode; reuse existing decoding, checked batches, writing
   and phase structure. Extend the new-record comparisons to both real maps.
2. Root's protected store/planner and worker successors supply/authenticate the
   reference base, stop closure acquisition at its public frontier, select exact
   imports, and retain the reference identity in generated descendants. Original
   records must not masquerade as generated `added_names` entries.
3. Native exact-map parsing can reuse the pinned non-main artifact helper.
   A fresh shared no-main helper is justified only if both the delta and
   extraction successors actually need it. Do not refactor/rebuild the frozen
   correspondence matcher merely to obtain an unused generic abstraction.
4. Use one integrated small workflow to distinguish the new boundary: a genuine
   new delta uses an approved original definition and theorem; a second delta
   uses the first through a wrapper; normal source authoring retains original
   notation/attributes. New source output is extracted and strictly admitted,
   never accepted from compilation alone. Select a few decision-relevant
   refusals (outside-frontier reference, name collision, altered import/part)
   within the same finite workflow, not another broad predecessor campaign.

Ordinary `--setup` authoring may load approved frontend extensions for notation,
instances and tactics. That does not fall under the native map-preservation lemma
and must not bypass later admission. It is an approved local execution workflow,
not a hostile-source sandbox or a transferable binary-trust promise.

## Cost and claim boundary

The new proof work is two checks of the delta, not two replays of all ancestral
proofs. The retained costs include importing the selected original/generated
artifacts, artifact integrity checks, bounded header/frontier metadata, and
encoding/comparing the new records. Those bytes and checks can still be large.
This contract removes mandatory **ancestral proof checking and proof-inventory
reencoding** from warm materialization; it does not establish constant-time
imports, no ancestral artifact I/O, worldwide discovery, net useful growth or a
finished deployable v5. It is the smallest identified extension that makes an
approved ordinary library reusable in the existing strict module pipeline.

## Priority correction: abstract computational interfaces and partial basis

The actual02 discriminator's private correspondence completed6 units/9 names,
then exported matching refused `PUBLIC_COMPUTATIONAL_OR_NONSINGLETON_ERASURE`.
That diagnostic lacks a name and is used by fixed-basis matching as well as
selected-unit matching; it does **not** identify `casesOn` or another particular
declaration. The saved selected definitions `Flag.casesOn`, `flip.match_1` and
`flip` each have singleton `all` metadata. A small exported-view census, not a
repeat export/snapshot campaign, is the next source-selected discriminator.

The earlier singleton-theorem-only paragraphs describe the current implementation.
The following stronger relation and basis policy are accepted by root **in
principle**, pending actual census and separately selected source changes. The
delta implementation remains on HOLD; no refusal is reclassified as a pass.

### Interpretation rather than preservation of every computation rule

Let `G` be the independently warranted original environment and `H` an imported
interface view. Each available constant in H must refer to exactly its registered
original identity in G. Permit either:

1. **Full:** exact original record, including all retained computational metadata.
2. **Abstract checked constant:** a safe axiom-shaped record with exactly the
   original name, ordered universe parameters and type, whose original is a
   fully warranted safe singleton definition, theorem or opaque declaration.

The second case is an interface interpretation, not permission to assume a new
mathematical axiom. The original checked declaration supplies its interpretation.
No new name, type, universe order or original identity is supplied by the view.
Its original body remains retained in the private warrant; the public view does
not claim that body is available for reduction.

For the initial implementation keep inductive types, constructors, recursors and
quotient primitives **full**. Keep multi-declaration cases unsupported for
abstraction until a separately checked whole-group relation is selected. Restrict
def/theorem/opaque abstraction to the descriptor and original record's genuine
singleton `all=[name]`, not merely one supplied inventory row. This is a narrow
engineering profile, not a claim that all group abstraction is mathematically
impossible. Foundation axioms remain exactly the existing permitted primitives.

The underlying simulation argument is:

> If H's constant signatures have their exact warranted interpretations in G,
> every retained computational rule of H is the same valid rule in G, and
> H adds no new primitive rule or axiom, then each H typing derivation translates
> into a G typing derivation under the identity mapping of registered names.

Justification by the typing/conversion rules: variable, sort, binder, application
and let rules are unchanged; the constant rule uses an identical type/universe
signature whose original declaration is known valid; beta/zeta and function eta
are unchanged; retained delta steps use the same checked original body. Erased
bodies provide no new delta steps. Inductive/constructor/recursor metadata,
projection/structure-eta rules, quotient and literal primitives are unchanged
under this profile. Proof irrelevance uses the same interpreted proposition/type
judgments. Hence each available conversion step maps to one valid in G, allowing
the conversion rule to carry through. Additional reductions in G may make it
more capable, but cannot invalidate the interpreted judgment.

This is a conditional metatheoretic argument at Lean's intended typing/reduction
semantics, not a new mechanically proved refinement of its entire kernel. The
bundled distribution does not supply the kernel C++ type-checker source here.
The pinned kernel's sound implementation of these rules remains the same trust
premise as ordinary checking. Keeping the actual private and exported new-delta
checks also retains a concrete final original-environment check: a predicted
public success is never substituted for that execution.

One need not claim that every retained full body can itself be rechecked inside
the weakened view: erasure may remove conversion it originally used. Its rule
and signature are interpreted using the already checked original declaration.
The principle is valid interpretation of the available inference/reduction
rules, not inventing a second independently complete foundation. Nevertheless,
the reusable interface below must have explicit dependency closure; missing
records cannot be silently installed as axioms to make that closure appear full.

### Source support and the important non-example

Pinned `Lean/AddDecl.lean:114-126` explicitly exports theorem, safe definition and
opaque records as axiom-shaped interfaces under the relevant exposure settings.
`Environment.lean:1089-1117` checks that an exported record has the same
`ConstantVal` signature as its private record. `mkModuleData` selects the exported
frontend records for the public artifact while retaining full private records.
Thus the proposed abstraction matches an actual Lean interface mechanism.

By contrast, `Environment.subsumesInfo`'s singleton-theorem limitation governs
**merging duplicate names from separate modules**. Two different checked
definitions `f:=0` and `f:=1`, each exported as `f:Nat` together with their own
equations, must not be merged by signature. Our proposal never does that: exact
original unit/snapshot/context identities choose one interpretation, and a
conflicting identity or generated name refuses. The duplicate-merging restriction
is therefore not the correct abstraction-soundness criterion.

Keep separate view labels for full, erased singleton theorem, abstract singleton
definition and abstract singleton opaque (exact spellings are a schema decision).
Report original kind and identity unchanged, plus the frontend/kernel projection
separately. A full record is not a promise of transitive computational transparency:
its body may call an abstract helper. Ordinary checking decides whether a desired
calculation is supported; retrieval/UI must not promise lost reductions.

### A usable public basis is not necessarily all581 private seed records

The private fixed foundation remains the exact581 checked rows. Some rows are
private proof helpers; requiring every one in both public maps is unnecessary
for unrelated usable interfaces. Equally, simply skipping missing rows while
continuing to advertise all581 would be incorrect.

Use this finite construction at reference registration:

1. For each private basis name, separately inspect exported frontend and actual
   kernel lookup. Validate every **present** record by the full/approved-abstract
   interpretation above. Record each view's availability and projection.
   A mismatching present record is a refusal, never treated as absence.
2. Start with the intersection of the two available-name sets. For each member,
   compute the union of semantic dependencies of its two actual records using
   the existing complete scanner. An abstract record contributes its type only;
   a full record also contributes body/rules and kernel-relevant metadata.
3. Remove any member requiring a basis dependency outside the candidate set;
   repeat until stable. A reference outside the private basis must be explicitly
   resolved through a selected warranted unit or refused, never presumed to be
   a primitive. In the fixed-basis-only case, this is the greatest closed subset
   of common availability, uniquely determined by finite deletion. A reverse-edge
   queue implements it in linear graph work; even a simple bounded iteration
   terminates after at most581 deletions.
4. The public nonbasis closure may stop only at this `usable_basis`, not at any
   private seed name. Its needed full bodies/metadata continue through the
   existing conservative common-view closure. A needed basis symbol removed by
   the fixed point makes that proposed reusable interface unsupported.

Report both availability sets and the ordered usable-basis subset, plus enough
projection metadata to bind their interpretations. The protected controller
authenticates the actual event and exact subset; report parsing only checks its
shape/subset binding. Future delta decoders grant external names only from the
usable basis, registered public nonbasis frontier and generated ancestors.
The all581 private basis check remains a checking/profile premise, not a claim
that every basis helper is publicly available.

The closed-subset construction adds no derivation rule. Restricting an interface
to fewer constants and computation rules preserves the interpretation into G;
its closure prevents missing dependencies from becoming implicit postulates.
This deliberately retains the current conservative common-view model. A more
permissive model with distinct internal kernel and frontend domains may support
additional libraries, but is not required to remove the blanket581 condition
and is not selected here.

The wrapper-preservation argument still applies after this change: it preserves
the registered per-view records and absences, including abstract projections and
the selected usable subset. It does not turn an abstract interface back into a
transparent definition. The new reference policy, schemas and controls must be
implemented and reviewed before that conditional delta contract is actionable.

## Exported-view diagnostic source review

The narrow source/API review of `ReferenceViewProbe.lean` is **PASS for diagnostic
source scope only**, at SHA-256
`a5f08241b50da63a1a7314854669dbe3b32b59455a24add8cbc1855f7cf516cf`
(181 lines). The reviewer read the complete earlier `718dcc17...` source,
checked the pinned Lean declaration/group fields, frontend/kernel lookup APIs,
bounded JSON helpers and syntax patterns, then verified that the final source
differs only by replacing the two nongroup `.null` defaults with the exact string
`"not_applicable"`. Reversing those two substitutions reproduces the earlier
source hash. The runtime reviewer found the null incompatibility with the
unchanged lexical JSON parser before any build; this is not a runtime failure or
a reason to broaden that parser.

The source performs one explicit exported import against the supplied artifact
map with name-search fallback empty, plugins empty and extensions disabled. It
reports separate frontend/kernel presence, kinds, safety/group metadata for the
581 basis and nine selected names, plus the ordered loaded-module census. It
does not decode declaration expressions, compare signatures/bodies, check
proofs, register authority or change the matcher. `import_count=1` counts an
import operation, not the number of root modules. Nongroup metadata uses the
exact sentinel pair; it does not pretend those records have singleton groups.

This clearance is not a compiler pass, parser-integration test, launch selection,
correspondence proof or accepted reference. The root-owned runtime wrapper must
bind the exact retained input/artifact bytes and fresh output and interpret the
report as diagnostic only. Build/runtime review and actual outcomes are separate.
The abstraction and usable-basis policy remains conditional pending that census
and a separately reviewed implementation.

## Actual exported census: saved-evidence audit and implementation decision

**2026-10-24 PASS for the selected diagnostic outcome, not correspondence or
registration.** The one operation is
`experiments/v5-local-checks/ordinary-reference-view-probe-01`. The reviewer
performed read-only saved-evidence analysis, not another import, build, snapshot
copy or third hash pass over the 389,559,024-byte artifact closure.

| Authoritative artifact | SHA-256 |
|---|---|
| `selection.json` | `7493844f3b97578f473b42e059bae5bfcab833a6f0c66fb43b38c17f58db0726` |
| `RESULT.json` | `5ce334c81948523b33e2288facd8fa714a6aaa54a2264d11d21414fcd7085a3e` |
| `probe/PROBE.json` | `263aeef23e1c7fdeac24d019ea703be72723e2740e5f093f1f0ee1b7d1633952` |
| `probe/view-report.json` | `d12bbf9ff4a62629ecc311387a03fc5b8f94bbd0d0e55c13a755545ca950c3de` |

The audit independently rehashed the 182 selected input pins at most 2 MiB and
all seven source snapshots, with no mismatch. The other 18 selected, larger
runtime/support inputs retain the executed exact-pin checks; they were not
rehashed by this audit. The selected wrapper's completed path revalidated the
entire snapshot before and after the single native call. Its fixed manifest
`f47f738b...`, source-report and replay-request hash bindings agree; the reported
650 distinct loaded names equal the manifest's complete module set. The retained
closure remains 650 modules / 3,250 parts / 389,559,024 bytes. These are evidence
bindings under the existing protected-local-state premise, not a new hostile-OS
or hermetic-toolchain guarantee.

All 590 report labels exactly match the ordered saved 581-row inventory plus
the nine selected unit names. The frontend and kernel fact records are identical
for every row; every present record reports safe and nonpartial. Independently
recounted per-view totals are 60 absent and 153 axiom-shaped records. The summary
and stdout are semantically identical (their JSON object key order differs);
the command record agrees with the result's argv. The two stderr messages mark
the one import and the 590-row / 315,916-byte report, with no error diagnostic.

The authoritative outer result is `COMMAND_EXITED_ZERO_AND_CLOSED`, child exit
zero, process reaped and Job closed, no termination request or cleanup errors,
zero active/terminated processes at closure. Cost is 28.5745279 wall seconds,
23.78125 Job CPU + 1.890625 outer-wrapper CPU = 25.671875 known CPU seconds,
with peak Job private commit 532,553,728 bytes. Nested controller/supervision
figures are not added again. No mathematical acceptance or protected reference
was registered.

### What the diagnostic actually establishes

The 581 fixed-basis rows partition identically in both views:

| Observed shape relative to the original row | Count |
|---|---:|
| Absent original definitions / theorems | 53 / 6 |
| Axiom-shaped original singleton definitions | 25 |
| Axiom-shaped original singleton theorems | 124 |
| Original permitted axiom kind retained | 3 |
| Original definition / theorem kind retained | 189 / 2 |
| Original inductive / constructor / recursor kind retained | 53 / 67 / 55 |
| Original quotient kind retained | 4 |

Thus common **availability** contains 522 basis names. This is not yet the
dependency-closed usable subset. All 25 abstracted definitions and all 124
abstracted theorems have singleton original `all=[own name]` in the saved
inventory; this was checked independently, not inferred from their axiom-shaped
public records, which carry no such group metadata.

`Nat.gcd`, zero-based basis inventory index 171, is the first public record in
the deterministic inventory order that violates04's theorem-only erasure guard:
its original kind is definition and both public shapes are axioms. The retained
`compareSourceBasis` preserves inventory order, and04's `matchBasisViews` walks
that array. This identifies a concrete earliest unsupported public projection;
the original unnamed error log remains unchanged and is not retroactively
presented as having named its failing invocation.

The selected `Flag` inductive, its constructors/recursor, `Flag.casesOn`,
`flip.match_1` and `flip` retain their original kinds in both public views.
`flip_low` is axiom-shaped in both, and its private `hidden_low` proof helper is
absent in both. Retaining kind is **not** an exact full-record comparison:
signatures, bodies and metadata still require the new matcher. In particular,
the census does not prove that public declarations are derivable or that the
three computational fixture definitions satisfy the full correspondence rule.

### Exact recommended successor boundary

The observed fixed-basis computational abstractions and missing private helpers
make the proposed change concrete, not hypothetical. Select only the following
successor before continuing protected reference registration:

1. Keep full private581 correspondence and every selected private unit/warrant
   unchanged. No public absence may weaken private checking.
2. Validate each present frontend and kernel record independently against its
   exact original. Permit full correspondence or the justified safe singleton
   definition/theorem/opaque abstraction with exact name, ordered universes and
   type. Original group metadata, not a public axiom label, proves singletonness.
   Keep primitive axioms and quotient/inductive/constructor/recursor rules exact.
   Any present mismatch refuses; it cannot be reclassified as absence.
3. Report all581 original basis rows with separate per-view projection/absence
   and an ordered greatest common dependency-closed usable subset. The selected
   conservative implementation may reject basis dependencies outside fixed581;
   it must not invent an implicit primitive or feed selected units back into the
   basis. Scan the union of actual frontend/kernel semantic dependencies, using
   types only for abstractions and bodies/rules/metadata for full records.
4. Stop selected public closure only at that usable subset. Keep excluded
   private helpers private. The absent `hidden_low` is harmless only if every
   retained public dependency omits it; erasing `flip_low`'s proof removes its
   proof-body edge, but its type dependencies must still be checked.
5. Bind that report to the protected actual event and original unit/snapshot/
   context identities. A same-signature declaration from another environment is
   not interchangeable. Delta decoders receive only usable basis names, checked
   public frontier and permitted generated ancestors; keep real private and
   exported delta checks.

This is a **sound-policy clearance in principle**, under the earlier explicit
interpretation argument, not clearance of unwritten05 code. The numeric usable
subset, exact signature/body correspondence, protected registration and actual
delta use remain open. Abstraction promises a warranted interface, not restored
computation. No further census campaign is warranted by these observations.

## Native05, V2 binder and retained-support build: source clearance

**PASS within the conditional source/theory scope below; no execution or
registration claim.** Final reviewed source identities:

| Source under `software/v5/ordinary_baseline/` | SHA-256 |
|---|---|
| `OrdinaryReferenceBase05.lean` | `ec8248e4f96e9dd39bc78cb3e89ac0c5057d17f459dc152555d84678a5444c09` |
| `reference_report02.py` | `d153b061ed2e6551edaaf24d8e367d39797eeb81a3a97200f73829f36665688e` |
| `build_reference05.py` | `c9476a5f7b27f294234bcf2defc0769e4ae44f6e8f2f1783bdf11090a69d188d` |
| `select_reference05_build.py` | `6dccd19a3cf0bc07a7a824ebd40291cf44502a2be8950efc0b2eec2f60b62e96` |

The complete native05 source and its04 diff were read. The only late correction
was the selected quotient dependency branch: each full quotient primitive adds
all four `BootstrapProbe.quotNames` plus `Eq` to the semantic reference graph.
The author and reviewer identified this together. The inherited04 scanner had
relied on all581 basis records being present; partial public availability makes
an explicit whole-primitive-group dependency necessary for the selected profile.
This conservative repair adds no primitive rule and does not alter old04 bytes.

Native05 preserves exact private basis/unit matching. A selected singleton is
established by both the decoded descriptor and exact output inventory, with
`names=#[own]` and `all=[own]`; basis singletonness comes from the exact private
record. Public axiom-shaped def/theorem/opaque records require exact original
name, ordered universes and type. Full records retain the complete ordinary
inventory comparison. Every present frontend and kernel basis record is checked
independently, including one-sided availability; a present mismatch refuses.
Public graph scanning unions both views and shares aggregate node/edge limits
with private and selected-public scanning. No selected public dependency may
terminate at an excluded basis name.

For the fixed point, let C0 be the names present in both validated views and let
D(n) be the union of their semantic dependencies. Starting at C0,05 deletes n
only when D(n) is not contained in the current set. For any closed X contained
in C0, induction maintains X contained in every intermediate set: a deleted n
has a missing dependency and therefore cannot belong to X. At termination the
remaining set is itself closed, so it is the greatest such subset. In-place
iteration order does not change this result. Every counted changed round
removes at least one name; there are at most581 such rounds, and closed cycles
are retained. Outside-fixed-basis dependencies refuse before pruning under the
selected conservative profile. This proves the finite graph algorithm's
property, conditional on the separately reviewed semantic scanner and original
interpretation relation; it is not a metatheorem about arbitrary Lean artifacts.

The V2 binder was reviewed against the actual descriptor/inventory encodings and
`ordinary_evidence._names`. The fixed legacy basis row stores universe **count**
in field2, while native05 emits actual ordered parameter names. The binder
checks that list's syntax, bounds, uniqueness, nonanonymous names and count;
exact original signature equality belongs to the live native matcher. It binds
all581 rows in fixed order, per-view projection kinds, a unique ordered subset
of common availability, pruning-round consistency and aggregate counters.
For selected public abstractions it also checks the exact descriptor/inventory
singleton relation, including definition hints and safe opaque metadata.
It does not independently establish basis singletonness, maximal closure,
signature/body equality or authority. Neither `BoundReferenceReport` nor its
caller-supplied expected hash is a certificate: registration still needs the
protected current warrants, artifact binding and exact clean native event.

The fresh build adapter/selector were read completely. They use the already
adopted build04 provenance and exactly12 retained files: core04 and five helpers,
each `.olean` and `.o`. Only05 is compiled, through three codegen/object/link
commands producing four outputs. Source snapshots, copied support, generated
outputs, metadata and original pins are checked again before the receipt.
The selected envelope remains120 wall seconds /60 aggregate CPU seconds /
1,536 MiB /four processes, with the105-second inner deadline,104 MiB inner
cooperative spool and bounded logs. It neither imports the original library nor
runs the matcher or an owner operation. A candidate build receipt is not
mathematical correspondence, and the actual matcher continuation remains a
separate root selection. No old successful stage is repeated by this build.

The binder review was completed under root's earlier assignment before a later
parallel reassignment arrived; the native author was promptly asked to avoid
repeating it and to focus on the continuation's cross-component contract.

## Actual build05 saved-output audit

**PASS for the candidate build only.** The selected operation at
`experiments/v5-local-checks/ordinary-reference-native-build-05` completed once;
the reviewer only read its saved evidence. Exact pins:

- Selection: `e5cdf8a52f6dace0518a42fc88b461caab5edda9ed0caaf91183cc07af9f8226`.
- Result: `19f5936d91cf501ada9c1bd2d15de318106d799194ded1cc514570c726ec5095`.
- `build/BUILD.json`: `12d2708d8f636dca4c163e2aa733ddfb49d2c437193657d999a5413c593a3111`.
- `build/INPUTS.json`: `8db3cdad3403be923bb790263312e344f9797b8548666d398bf6cb12d9bccf94`.
- `build/NATIVE-OUTPUTS.json`: `6c7b989645c123d44f003e6d6166546197263a1a7ca2bc304d9e462626b724c5`.
- `build/objects/OrdinaryReferenceBase05.exe`: 1,008,640 bytes,
  `918aebc5f3f20f305d7c684ff6c1200c164c1503712eaa2e3657fce697bd4aab`.

The three saved command records exactly match the selected source codegen,
object compilation and link scopes, all exit zero, with matching stdout records
and empty stderr. The audit independently checked five source originals and
snapshots, the staged05 source, all12 original/copied retained support pairs,
four generated outputs and both metadata pins. All47 input-map bindings agree
between selection/input document/receipt;31 small input files were independently
rehashed, with larger runtime pin checks retained from the executed adapter.
Every checked byte count/hash agrees. Final support/object censuses are12/4;
independently summed pre-receipt spool is exactly21,956,620 bytes.

The outer result is clean:10.3232148 wall seconds,6.859375 Job CPU plus1.421875
outer-wrapper CPU =8.28125 known CPU seconds,636,276,736 peak Job private bytes,
zero active/terminated processes, no cleanup errors, reaped child and closed
Job. No duplicate build, original-library import, owner operation or certificate
production was performed.05 is a successfully built candidate, not yet an
executed correspondence result or accepted live reference.

## Actual continuation01: correspondence boundary outcome

**PASS for the selected conditional correspondence boundary, not protected
registration or mathematical admission.** This audit covers the one completed
`experiments/v5-local-checks/ordinary-reference-continuation-01` operation:

| Artifact | SHA-256 |
|---|---|
| `selection.json` | `0f6dd64b3f02e60a0dfd5cffb0b029a1e19abd249abb494eda373b00b97e11dd` |
| `RESULT.json` | `d99cf73be401a1f381bda619370d3bee5a6a0b54e2a53527c5eb55bad39bb02a` |
| `continuation/CONTINUATION.json` | `d68a062eac3bbed9bb3a749c14b8fac6238d66cff9b0cd9f8f2b0042b40f34cb` |
| `continuation/INPUTS.json` | `a735155fbab0533bf4e610ad1eef4a268925ab9ec349a0dd37de7a2698f75668` |
| `continuation/positive-report.json` | `e82cf595e5176fb1d952da0bda2c1d0360203b210f9c9fe83aa098f71375d52e` |
| `continuation/changed-body-request.json` | `2bc5d9b0089ff847000306aab53d6f0765a5fcd8e9e3abd82e77c7ec15440c1f` |

The reviewer independently checked all nine source snapshots and189 small pins
from207 selected input pins, with no mismatch;18 larger runtime/support pins
retain their executed exact checks. Retained/matcher receipt maps agree with the
selection. The unchanged positive request hash is `638b89e4...`, exactly the
saved workflow02 test request. The operation used the existing snapshot and
validated it before/after; this audit did not copy, rehash or import its389MB
parts. No source/native operation or report mutation was rerun by the reviewer.

The actual positive native call exits zero after matching six private units/nine
names and five public units/eight names. Each public output's name, export ID,
original kind and ordered universe parameters agrees with its selected unit.
The Flag group and three computational definitions are now **full-correspondence
results** in both actual frontend/kernel maps, rather than merely the census's
matching kinds. `flip_low` is an exactly related erased singleton theorem in
both maps; the checked private `hidden_low` unit is not in the public frontier.

All581 basis rows agree with the exact fixed inventory's ordered names, kinds
and universe counts. Common availability and usable basis are the same522 names
in exact inventory order, with34,350 added scan nodes,2,296 union dependency edges
and zero pruning rounds. Thus this fixture exercises validation/closure with no
deletions; the general deletion algorithm is justified by the source argument
above, not falsely reported as experimentally exercised here. The usable list
contains no absent basis record. No arbitrary basis abstraction is inferred from
kind alone: the actual05 signature/singleton checks precede its report.

The second native call exits one with the exact diagnostic
`PRIVATE_INVENTORY_MISMATCH name=DMKNBaselineFixture.flip` and creates no negative
report. The reviewer independently confirmed that the negative request differs
only in the actual flip body, in both its descriptor and matching inventory
location; its signature, metadata, other units and identity labels are unchanged.
The two changed body encodings agree with each other. This is a genuine rejection
of wrong full-body correspondence, not an earlier descriptor-shape failure.

Nine in-memory report mutations reached their expected exact refusal codes in
the source-bound completed run: context, targets, private census, a definition
mislabeled as erased theorem, node census, unit-byte census, basis node budget,
absent basis made usable and wrong basis abstraction kind. The saved case name
`erase-computational-definition` means the fourth of these; it must not be
interpreted as rejecting the newly permitted justified definition abstraction.
These parser controls establish no authority for arbitrary saved reports.

The eleven cases comprise one actual positive, nine parser mutations and one
actual negative. Exactly two native calls ran (6.560207 and2.5554634 seconds);
database/owner/network forbidden-call lists are empty. Outer completion is
`COMMAND_EXITED_ZERO_AND_CLOSED`, child reaped, Job closed, no termination or
cleanup errors, zero active/terminated processes. Full cost is51.3395015 wall
seconds,45.1875 Job CPU +2.15625 outer-wrapper CPU =47.34375 known CPU seconds,
934,391,808 peak Job private bytes. Nested controller/native timings are not
added again. The fresh pre-receipt spool contains five files/439,280 bytes.

The input context/support labels are explicitly test-only; no current accepted
owner, warrant admission or protected reference was fabricated. This closes the
selected interface-policy discriminator. Further census, fixture rebuilding or
repetition is not warranted. Next implement protected registration and ordinary
new-delta use with the same reviewed relation.

## Challenge of the concrete protected store/view/plan proposal

Reviewed `ORDINARY-REFERENCE-PUBLIC-VIEW-REPAIR.md` at
`46a837d296c6a1f028a92d42b43aee79dc834917c7eb5749643cb3c1720bc13e`,
specifically its new concrete API, not a duplicate semantic audit. **No additional
architecture blocker to fresh source selection**, with the following explicit
implementation conditions communicated to root and the proposer:

- One fresh typed realization sidecar with original-reference and generated-delta
  variants is appropriate. Do not inherit incompatible frozen generated-only
  schemas/globals, migrate old stores implicitly, or create a second authority
  service. The real current owner and lock remain authoritative.
- Reserve once before creating the final snapshot location, then bind exact match
  inputs once under the same grant/deadline. A saved reservation or Python object
  cannot recreate the live grant. Clean failure is distinct from unknown cleanup;
  orphan/closed output continues to count against store capacity.
- Construct the full private warrant table only from the authenticated request
  and current owner during the actual live commit. On reload revalidate every
  fixed-basis/private-output binding against a just-validated real current context.
  The table may omit proof bodies because their exact identities and original
  live event are retained; it may not omit private helper/import obligations.
- `load_reference` needs a **separate protected-report metadata parser**. First
  authenticate the protected record/store/support and exact previously committed
  V2 report hash. Then parse bounded schema, historical identities, roots/module
  sets, projections, usable subset and whole-unit frontier, binding public
  name/export IDs to current warrant-table entries. Do not manufacture a
  `Q.ReferenceRequest` with missing private bodies or call the live binder as if
  it independently re-established those old inputs. The new parser reopens a
  trusted local commit; it is not a peer-report admission API or correspondence
  proof. The same immutable-local-state/no-hostile-admin premise remains explicit.
- Preserve historical `registration_context_root` in the reference report/record;
  a new request uses its current context. Current authorization comes from fresh
  warrant-table validation, not requiring those roots equal or silently rewriting
  the retained report. Immutable returned views are data, not authority after
  owner closure or across an unvalidated later operation.
- Count the actual final/staged files within the768-MiB reference envelope,
  including any duplicate request/report copies.512+64+96+32+32MiB leaves32MiB
  for remaining files; assuming both a temporary and final full request fit would
  be wrong. Prefer the selected final paths and record-last publication, retaining
  existing exact-ID recovery for ambiguous commit. Generated128-MiB operations
  and256-MiB chain artifacts retain their separate limits.

The concrete native envelope is compatible with the reviewed wrapper lemma:
separate pinned32-MiB V2 report,16-MiB replay map and4-MiB generated plan, fixed
standard import edges, exact reference/parent/plan IDs and only new4-MiB work.
Reopened metadata and compact checks derive their semantics from the original
protected event plus immutable import preservation, not from shape alone. The
proposal is ready to implement under these boundaries; its implementation and
actual protected registration/delta use are not yet audited by this note.
