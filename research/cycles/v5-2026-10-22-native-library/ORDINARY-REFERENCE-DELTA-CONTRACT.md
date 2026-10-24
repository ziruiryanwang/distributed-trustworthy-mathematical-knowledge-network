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

## Protected original-reference implementation: independent source review

**SOURCE-CLEAR for the reviewed original-reference path, conditional on the
selected installed profile and real owner; no execution or acceptance result.**
The following exact source versions were read independently in full:

| Source under `software/v5/ordinary_reference/` | SHA-256 |
|---|---|
| `reference_registration.py` | `c58ef1394ac41675ed3f46e1d29b570fdd75f527a2a09146f6f43f9d85a5b25d` |
| `reference_match_worker.py` | `318df42ad2504d90ba499346eb5eb9e0e221ee50e88221e0fa79bc90f71b5ec7` |
| `reference_store.py` original-reference version | `4c491692a0babe752671b2b307a9597fcc6d129e79f43eaee665366ae0aaa136` |
| `protected_metadata.py` | `6fac21a5366576618bee617205f5a0497a91b3d1cf176ebe97323711d88b4d7a` |

The store author is now extending the same unused source for generated deltas.
This review does not silently clear those concurrent additions or their later
file hash. The reviewed store version declared generated variant fields and a
plan helper but did not implement generated reserve/commit/reload.

The original operation's single budget is created before profile, metadata or
snapshot preparation, then claimed once for its one native match. The same
deadline and charged CPU remain in force through binding and commit. Unknown
cleanup is recorded without invoking the expired ordinary budget callback;
actual measured CPU or a conservative full reservation is charged. Clean failure
may close its reservation but cannot publish a reference. The worker runs one
selected matcher under the existing Job with fixed argv, isolated Python and
an explicitly selected Lean binary directory; it is not a security sandbox.

The store reserves before snapshot preparation, writes the snapshot and large
request at their final protected locations, and binds `MATCH-INPUTS.json` once
to the live grant. The private commit rechecks the actual clean event, exact
request/inventory/warrant/report files, the live report binder and current owner
warrants. It closes clean operation history before nonoverwriting record-last
publication. `_commit_attempted` makes `abandon` a no-op after ambiguous or
successful publication, preserving exact-ID recovery rather than reopening a
failed allowance. A reporting failure cannot turn an uncertain commit into a
fresh retry. Complete current private warrants include all581 fixed-basis names
and every selected private output; the earlier request constructor already
requires every nonbasis import to be supplied by that selected closure.

The separate reopen parser authenticates a protected committed report and
warrant table, then validates bounded identities, projections, ordered usable
basis, whole-unit public frontier, roots/module sets and counters. It does not
construct a fake full request, reinterpret a saved report as new acceptance or
need old proof bodies. The caller must supply a freshly owner-validated current
context while the real owner is live. Historical registration context remains
unchanged. Snapshot reopen still hashes the retained selected artifacts; avoiding
proof replay must not be described as avoiding those actual local-byte costs.

Two concrete source findings were corrected before the controller hash above:

- `OperationBudget` permits logs up to8MiB, but this store retains at most1MiB
  per supervisor log. A legal overlarge log could poison subsequent census even
  after clean native failure. Registration now requires `log_bytes <= 1MiB`.
- A proposed alias guard referenced nonexistent `protected_metadata.R`. The
  independent parser imports only the common admission core, deliberately not
  the live binder. The invalid attribute guard was removed; actual store/parser/
  binder identities remain pinned and module-consistency checked.

The768-MiB reference envelope counts final inputs, report, snapshot, both logs,
`FAILURE.json`, closure and staged record, without a second96-MiB request copy.
Native05 itself bounds report bytes before writing. The common support descriptor
intentionally requires the new delta pipeline's files: this source clearance is
not permission to deploy registration with an incomplete installed profile.

## New reference-backed module and worker: independent source review

**SOURCE-CLEAR under the protected-controller premises; not build or runtime
qualification.** Reviewed complete sources:

- `ReferenceModule.lean`:
  `6660c657e10b7f34bcb2ecc1c32361c34075ff137197be9d87bb54780e03303e`.
- `reference_module_worker.py`:
  `fdaf97a8bfa90f257645f8a6a016cfac765de2346e4523a3c96f7eb8995884ff`.

The native tool's old-reference metadata is not a fresh signature proof. Its
justification is the prior protected exact match, immutable authenticated
artifact map and the already-reviewed standard-wrapper preservation argument.
The controller must freshly validate current complete warrants, same support,
exact reference identity and all generated ancestor records before calling it.
Native digest strings are labels; the worker/controller, not the Lean parser,
authenticate the pinned bytes. An independently supplied saved plan/report does
not satisfy these premises.

Under those premises, the new mathematical boundary is appropriately narrow:

1. Decoder external names are exactly the usable closed basis, checked public
   reference frontier and generated ancestor frontier. All original basis names
   remain metadata-checked, but absent or pruned names are not decoder-authorized.
2. Every new name must be absent from both full private frontend and kernel maps,
   including hidden original records. The all-new lane has no singleton matching
   shortcut, and reports zero matched units/names.
3. The same decoded batch is checked separately over private and exported import
   environments. The existing checker uses `addDeclCore(..., doCheck := true)`,
   rejects axioms/unsafe/partial declarations and compares exact native-generated
   inventories. Both actual frontend and kernel inventories are checked; only
   actually checked new recursors can be exposed by the existing helper.
4. Imported module order, complete generated-module headers, standard direct
   imports and actual constant names are constrained. A fresh output module
   cannot collide with an original/generated module. Original and generated
   artifact maps are explicit; mathematical imports clear `searchPathRef`, load
   no plugins and do not load extensions.
5. After writing, separate fresh processes reread the output privately and
   exported, compare complete new inventories and header structure, and preserve
   the checked predecessor mappings. The worker finalizes the report only after
   build plus both rereads succeed and all selected input/ancestor/output pins
   still match. No phase retries or independent renewed allowance exist.

The original frontier retains its8192-unit/262144-name bound, distinct from the
generated1024-unit/16384-name chain and32-unit/4096-name new batch. Parent artifacts
are rehashed at phase transitions; this is explicitly retained I/O cost, not
ancestral proof checking. The build adapter must supply real compiled dependency
objects where needed; a retained `.olean` is not a linkable `.o`. Actual build,
protected generated-store integration and useful delta execution remain separate
root-selected work. The reviewer ran no imports, compiler, native operation,
experiment, owner/database operation or Git mutation during these reviews.

## Reference-aware new-closure collector: independent source review

**SOURCE-CLEAR as pure preparation, not admission or reference authentication.**
Reviewed `software/v5/ordinary_reference/reference_closure.py` at
`65c4913fb1b6cc3df8a69c5c5cb5b1b6ab464e4aa1878d05331bdb85318ceec0`.
The caller must construct its `Frontier` from freshly owner-authenticated
reference/generated views and provide real current-warrant, custody and budget
callbacks. The collector itself neither opens an owner nor makes a saved view
authoritative.

All581 fixed-basis identities and the complete original private warrant table
are checked. Authorization to stop new dependency traversal is strictly smaller:
only usable basis names, complete public reference units and complete generated
ancestor units. A reserved hidden or unusable original name refuses rather than
being fetched and reintroduced as a supposedly new declaration. Generated names
may not overlap any original reserved name. Reference8192-unit/262144-name and
generated1024-unit/16384-name bounds are separate from the new32-unit/4-MiB work
allowance, so a small extension does not inherit a32-unit ceiling on its library.

Fetched evidence must supply the requested actual name/export identity, every
output's current warrant, consistent selected target unit IDs, disjoint complete
groups and all declared imports. Group siblings already fetched are reused
without fetching the same unit again. The existing bounded planner then orders
only new units above the authorized frontier, with no missing dependencies or
reused unit IDs. A target already entirely in that frontier returns no new request
and no native work; it cannot be counted as a new contribution. No old proof body
is fetched by this collector. The exact request binds the reference, optional
generated parent, current context, module name and plan hash. No runtime test was
performed for this source review.

## Generated realization lifecycle and controller: changed-boundary source review

**SOURCE-CLEAR for the now implemented generated path; still unexecuted.**
Reviewed complete generated additions in `reference_store.py`
`ff10bedc7fc88ecaee4dedc19a286c4cb37b69d15dc3f1907bc172d4737a67ba`
and the root controller `reference_module.py`
`3eca9fd21633aeaf924c1f203ac9f609dfb3c8342985c231492b62c6ba3c88df`.
The original registration/store clearance above remains a separately identified
review, not retrospective evidence that these later additions already existed.

The controller creates its original budget before loading or acquisition,
verifies the installed common support, loads current protected reference/parent
views, and checks selected targets against the real owner context. Complete
frontier coverage returns an explicitly reused realization with zero fetch/native
calls; partial coverage collects only genuinely new complete units. One live
reservation binds reference, optional generated parent, canonical sorted targets
and materialization key before plan/input creation. All expensive work remains
inside the same allowance, including the single supervised worker's three native
phase invocations. A reporting mismatch found during review was corrected:
success now reports `worker_calls=1` and `native_calls=3`, not one native call.

The store binds each new unit's complete output identities and inventory digests,
rejects every original-private or generated-ancestor unit/name overlap, and
checks current warrants. The native request and plans are retained once at their
final locations. New-target realization may include already public ancestor
targets but cannot hide an unmaterialized target. Pre-native reservation covers
actual input/plan bytes plus final and pending reports, trace, supervision, both
logs, failure, staged record and closure inside the32-MiB metadata/128-MiB
operation envelope; maximum-size incompatible combinations refuse before native.

Private commit requires the real clean event, exact report/request inventories,
zero matched units, both checking passes, fresh current base/parent validation,
and exact generated artifact census/pins. It checks prospective chain capacity
and generated-plan size before record-last publication. Native failure never
publishes; ambiguous publication preserves exact-ID recovery. Reload walks at
most32 protected records, requires one common original reference and exact
standard predecessor imports, rejects all unit/name/module collisions, verifies
all generated current warrants and artifact pins, and reconstructs only bounded
metadata/frontier. Old proof requests are not replayed. The4-MiB chain-record/
plan,1024-unit/16384-name and256-MiB artifact limits remain explicit.

The final registration support-descriptor adjustment was separately read at
`f5bdab6ac053cce9a04aa03bae4f264b1015aeb29c773ed1a78293f32f77c64c`:
it hashes the seven required native module families rather than indiscriminately
putting an entire large authoring profile into a64-helper identity table. Actual
profile verification still inventories and verifies every helper file. Ambiguous
same-name native artifacts across helper directories refuse; installed packaging
must therefore provide an unambiguous selected support map. The removed invalid
`PM.R` guard stays removed; common actual store/request/reopen/parser module
identities are checked. Snapshot rehashes on load/reserve/commit/reopen are real
local I/O costs, not a hidden claim of constant-time reuse.

## Compile-only ReferenceModule adapter: source clearance

**SOURCE-CLEAR for one bounded compiler invocation only.** Reviewed fully:

- `build_reference_module.py`:
  `535bbaa8253037e3884aaf1c8d37f8410e4aa49b75370a0690688a65959494d6`.
- `select_reference_module_build.py`:
  `cd1e52fa4eac80d47bda4ab92165f8e74d93b67940425c8f3d57edae63a7c4de`.

The selector pins the native source and build adapter, five source snapshots,
retained provenance, eleven support files and23 runtime files, then writes one
fresh finite selection. The adapter verifies clean predecessor results and
their selected receipts, copies exactly six retained legacy `.olean` files plus
five modern `OwnerRebind` parts, and runs one `lean -o ... ReferenceModule.lean`
command. There is no `--run`, invocation of its `main`, codegen/linking, old helper
rebuild, fixture compilation, selected original-library import, snapshot copy, owner operation
or registration. Source compilation may still reveal incompatibility between
these retained supports; the adapter does not assume success.

The outer envelope is120 wall seconds/60 aggregate CPU seconds/1536MiB/four
processes, with1-MiB logs. Inner control retains its105-second/50-controller-CPU
bound and104-MiB cooperative spool reservation. Exact copied/source/input pins,
final directory censuses, generated `.olean` and metadata readbacks are required
before a candidate build receipt. Any failure preserves fresh outputs with no
retry. The build's output is compiler evidence only, not an executed reference
delta, installed release or mathematical acceptance. This reviewer did not run
the selector, compiler or any native operation.

## Actual ReferenceModule build01: saved-output audit

**PASS for the single compile-only operation.** The reviewer read saved files
from `experiments/v5-local-checks/ordinary-reference-module-build-01`; no command
or library experiment was rerun. Exact artifacts:

| Artifact | SHA-256 |
|---|---|
| `selection.json` | `18dc8fb7f82a9b6162aaa363fdf41aa686d2dbc5ffc0b5d5bf5bb10e0ab5fdff` |
| `RESULT.json` | `d7075a3ba48e82330075a593ca4f85615f39277fc959d345cf3df74471c16071` |
| `build/BUILD.json` | `dd51cef62552b523f9e5b5bbade9cb978c8816d0361a8a4d28162d9193362a0c` |
| `build/INPUTS.json` | `1e0e56969e960f386b8053f19b98bf375edf2a15ebd66536b1c9f682088d4add` |
| `build/NATIVE-OUTPUTS.json` | `9b3d7c002290a7363002f60961631b58f0fb57b26b490b8bc74b0d7fee5be0c3` |
| `build/objects/ReferenceModule.olean` | `ac7cb316d687f9cb68a82de432f8678301006759f33e5f211dbf8650ae491b05` |

All52 input bindings agree between selection, input map and receipt. The audit
independently rehashed41 inputs at most8MiB, all eleven original/copied support
pairs, the five source snapshots, the staged native source, output and metadata;
there were zero size/hash mismatches. Eleven larger runtime pins retain the
executed exact pre/post checks rather than being unnecessarily rehashed by this
audit. The selected original-library snapshot was neither read nor copied.
Final support/output/source censuses are11/1/1, and the independently summed
pre-receipt spool is exactly19,572,584 bytes, matching the receipt. The output
`.olean` is3,348,496 bytes.

Saved stdout contains exactly the selected one compiler command, exit zero,
followed by the compile-only receipt status; stderr is empty. The overall result
is `COMMAND_EXITED_ZERO_AND_CLOSED`, direct child reaped, Job closed, no cleanup
errors or termination request, and zero active/terminated processes. Full outer
wall time is55.4865745 seconds; Job-supervised wall through cleanup is54.5390755
seconds. Known CPU is15.25 Job seconds plus1.734375 outer-wrapper seconds =
16.984375 seconds. The separately reported0.296875 supervision CPU is contained
within the wrapper accounting and is not added again. Peak Job private commit
is651,235,328 bytes. The compiler command itself took51.4936435 wall seconds.

This demonstrates source compilation against the selected mixed retained support,
not execution of the tool's `main`, private/exported reference imports, protected
registration, generated-delta use or final v5 readiness. Used source/selection/
build evidence stays frozen; the next useful work is integrated actual use under
a distinct root selection, not another compilation of these same bytes.

## Public owner facade: source-only changed-boundary review

Reviewed `software/v5/ordinary_reference_package/owner.py` at
`d0a11e437c02040485389b7e822bd3bc0cfe34272a1a101061d1e7a44299e5ab`,
including a complete read-only comparison with the preserved
`ordinary-preview-assembly-01/package/owner.py`. **SOURCE-CLEAR for the three
new dispatch paths, conditional on the separately selected profile's actual
shared-module wiring; no public command was executed.** Existing operations
are retained without mathematical-policy changes. Additions are confined to
`intake-baseline`, `register-reference`, `export-reference-delta`, their exact
argument partitions, bounded input reads and failure/result retention.

The facade requires explicit parent roots, forbids external output trees for
these protected operations, opens the existing real owner/custody once, and
passes its original allowance to the selected controller. Baseline intake uses
the unchanged strict batch-admission API rather than granting trust to a library
binary. Registration accepts an approved project/artifact locator and exact
bundle, not a saved correspondence report. Delta export accepts only protected
reference/parent IDs. Realization results survive later reporting failure, and
partial-intake/unknown-commit detail is retained rather than described as rollback.

One nonblocking reporting distinction was sent to root: the intake budget's
`observed_worker_cpu` is explicitly partial observation, although the facade adds
it into its generic top-level worker-CPU field. The intake result retains the
correct `resources` scope and conservative `reserved_cpu`; top-level reporting
should preserve that qualification too and must not promote partial observation
to a full-cost measurement. Conservative reservation is authorization accounting,
not additional measured CPU consumption.

The normal-source proposal was also read without redoing the prior mathematical
policy audit. Explicit protected `--setup` artifacts plus an external exporter
can avoid reconstructing the original library while preserving its original
extensions. Required implementation boundaries are exact setup/output bindings,
current usable/public/generated-only IPC answers, whole new declaration groups
owned by the authored module, and unchanged candidate binding/admission. Imported
elaborator metadata and owner source remain approved executable input, not a
hostile-source sandbox. Extracting a helper environment from the reviewed native
prefix must remove its executable `main` and pin the resulting derivative.
Portable generated proof-unit deltas do not thereby transport newly authored
notation or arbitrary extensions. This proposal review is not source/runtime
clearance for the forthcoming authoring worker or extractor.

## Ordinary reference source tools: independent source review

**SOURCE-CLEAR for the native worker/exporter boundary and one two-command
compile-only selection, not integrated owner execution.** Fully read versions:

| Source | SHA-256 |
|---|---|
| `reference_author_worker.py` | `8633631b597c66bcfcc380279ee95876a47b2b4b2903a5c87ae31116c7af2402` |
| `ReferenceSource.lean` | `810d6245d6989b6dec6ce28962cd118f24252b2fe42e214ae58fcd3c34962751` |
| `ReferenceEnvironment.lean` | `a5aee6d1ca7e1b8ce295fd725da0a2dd90f1dddc69e081e860325d7f170b6587` |
| `build_reference_source.py` | `7287ddd595c8ef54fad3e659923b26934283b80be6f00ad4a4b585c4927e0951` |
| `select_reference_source_build.py` | `672e93f19ae0369c04b058f3f9e07d9167abba8753a5e196c4907df3159c8cbd` |

The helper is mechanically equal to the already reviewed ReferenceModule prefix
through `checkBaseHeaders`, with namespace rename, introductory comment and final
namespace closure only; it has no executable `main`. The worker binds fresh source
and setup, enforces16-MiB setup/2-MiB source limits with bounded reads, runs one
compiler under the controller's Job, and pins all five fresh artifacts within
64MiB. Its exact setup options require `Elab.async=false`. Parent/controller
authentication of every original/generated import artifact remains essential;
the worker's syntax checks are not mathematical or provenance authority.

The exporter imports exact selected artifacts with no plugin/extension
initialization and no search-path fallback, checks original/generated headers and
records, and requires every exported new name to belong to the authored module.
Selected targets are public, safe full declarations. Its dependency resolver
admits only the explicit usable-basis/public-original/generated frontier or new
owned names, with actual current-warrant IPC replies. It produces candidate V2,
not accepted mathematics; unchanged binding and real new-unit admission remain
required. The final generated-artifact alias comparison removes the native
Windows path prefix through the existing `reportPath` before ordinary `pathKey`.

The build selector pins eight sources,23 runtime files and eleven retained support
parts. The adapter verifies predecessor build01 closure/receipt and all support,
stages only the two native sources and invokes exactly two `lean -o` compiler
commands. It neither invokes their mains nor imports a selected user library,
recopies support/snapshots, executes an owner operation, or grants acceptance.
Outer allowance is150 wall/90 aggregate CPU seconds/1536MiB/four processes;
inner allowance is135 wall/75 controller CPU seconds with64-MiB cooperative
spool. Final source/input/support/output censuses and pins are required. The
reviewer ran no selector/compiler/native operation. Controller/package seams
remain separately reviewed, and actual compile success is not assumed.

## Source authoring controller and public package: integrated source review

**SOURCE-CLEAR under the selected protected-owner/runtime premises.** This
verdict is a source-contract result, not executed registration, contribution,
reuse, assembly or v5 release. Fully read final versions:

| Source | SHA-256 |
|---|---|
| `ordinary_reference/reference_authoring.py` | `5029cd2a5e21aa4666883d6d1ef84d004cfaf8ec48cccd69dd48d5bf137f4a22` |
| `ordinary_reference_package/owner.py` | `e5ba6e86999e5f71e544852dad0d7c0258ed12c38d4ee94f18617722fd565da8` |
| `ordinary_reference_package/profile.py` | `43a061ac8275a7ab0669d1242efd4525fc6622902f2354bd5db4c11a16fefbd3` |
| `ordinary_reference_package/assemble.py` | `9245bdd2f257858b519f8384f52245048ea505a7ebb7033e8f3d2fd1e8cc28d6` |
| `ordinary_reference_package/select_assembly.py` | `92554210128bb243080ff9cf074c1c598e0b03d83fe67dd11fcba07e321d58a3` |

The authoring controller requires a real already-open owner, exact protected
reference and optional generated parent, absent new output names, a disjoint
fresh output tree and one parent allowance. Stage budgets use its remaining
allowance rather than reset maxima. Original/generated artifacts go directly
into Lean's explicit setup map; original proof bodies are not reconstructed for
source authoring. Before/after revalidation covers protected references, all
selected support, source/setup/plan bytes and five compiled parts. Exporter IPC
answers are restricted to actual current owner warrants intersected with the
usable basis and exact original/generated public frontiers. Candidate V2 is
bound with the unchanged binder and submitted to real admission; compiler output
or the exporter report cannot create a warrant.

Three source findings were corrected before clearance. Setup options now exactly
match the worker's `Elab.async=false` requirement, and setup limits agree at16MiB.
Accounting no longer throws from a `finally` and masks an extraction exception's
cleanup/accounting report. A failed admission can perform native work or commit
before returning, so initialized-zero worker CPU is not treated as a full known
measurement: full remaining stage reservation is charged conservatively, partial
observations are labeled and the original error is preserved. An admission entry
with no returned acceptance explicitly records `possible_unreported_commit` and
requires protected owner-status inquiry rather than automatic retry. A known
accepted root survives subsequent preview/publication/reporting failure.

The new public `contribute-reference` operation requires source/output names,
explicit current parent/reference IDs and a fresh external output, and excludes
unrelated operation-specific arguments. It uses the selected reference profile
and the same real owner/custody as all other operations. Registration/delta paths
remain separate. Baseline intake's top-level CPU report now explicitly labels
its partial core observations and separately retains conservative reservations;
those reservations are not claimed as measured processor consumption.

The loader pins every payload before import, validates the installed shared core,
rejects preloaded aliases and requires the V2 correspondence report. Ordinary
authoring keeps its existing helper directory. The reference profile uses exactly
twelve isolated files: six retained legacy `.olean`s, five modern OwnerRebind
parts and the newly compiled ReferenceEnvironment `.olean`. Duplicate native
module names cannot accidentally select the ordinary-authoring copies. Complete
profile verification still checks all auxiliary payloads even though reference
support identity uses its narrower stable role set.

The assembler/selector are file-only. They require exact clean predecessor
builds and three explicitly supplied actual source-build receipt/result/selection
hashes, two successful compile commands, source identity and all eleven old
helper matches before copying the new environment helper. They preserve132
predecessor files, change only owner/profile and add31 payloads, yielding165
payload files and137 auxiliary profile entries. All selected inputs and copied
outputs are rehashed; PROFILE is published last. Outer allowance is90 wall/
50 aggregate CPU seconds/512MiB/two processes; inner allowance is75 wall/
45 controller CPU seconds. This clearance requires independently adopted actual
source-build evidence and the exact reviewed source-map pin; it does not supply
either by assumption. No import, selector, assembly, native command, owner/store
operation or Git mutation was performed by this reviewer.

The remaining useful discriminator is an integrated actual controlled workflow,
not repeated source audits or another certificate campaign. Normal original
notation/extensions are retained, but newly authored extension metadata stays
only in the retained local source artifact; portable deltas carry mathematics,
not arbitrary executable extensions. Resource ceilings and selected syntax remain
explicit implementation bounds, not worldwide-growth or arbitrary-project claims.

## Actual source-build01: failure and reusable successful prefix

**Whole operation FAILED; the Environment compilation alone succeeded.** Saved
stdout records its exit-zero compiler command followed by Source's Lean parser
error at23:38 (`unexpected identifier; expected '}'`) and exit one. The failure
receipt agrees. No Source `.olean`, BUILD success receipt, owner operation or
mathematical acceptance exists. The isolated failure must not be relabeled as a
complete two-source build. The next source fix/continuation is a fresh selection;
recompiling the already successful Environment is unnecessary.

| Saved artifact | SHA-256 |
|---|---|
| `selection.json` | `aa6026c11c205472b8bc800c6af477c720da0f5a119f5dda362258d93af1c0fe` |
| `RESULT.json` | `cbe0bdd69220a1793321b291b36b55cee73c9cee9722c50f75835eddd494750d` |
| `build/INPUTS.json` | `3e8de58e928004d3aa92bad124f430ccf4d437cd1b89e3cbbe15f561fa42ea69` |
| `build/BUILD-FAILURE.json` | `4c51dd23ff0c59084591b4573d249ffcd5eaf5eed992b0aa58e47c44473a54ab` |
| `build/objects/ReferenceEnvironment.olean` | `a082feb7bfcf3b28199c4438baafc11e3e00b4ad37af07e3507473e1e452c698` |

The independent read-only audit confirms47 selected/input bindings,36 current
small-input hashes,all eight source snapshots,eleven retained helper pins and
both staged native source pins with zero mismatch. Eleven larger runtime files
retain the outer runner's original selected pin checks and unchanged-runtime
premise; no unnecessary large rehash was performed. Environment's sole retained
object is2,378,696 bytes and independently rehashed as above. The failed adapter
did not reach its planned final whole-input rehash or success receipt; later reuse
must explicitly revalidate the successful prefix inputs/output, not fabricate
the missing receipt.

Actual closure is clean despite exit one: child reaped, Job closed, no cleanup
errors or termination request,zero active/terminated processes. Outer wall time
is12.3216304 seconds; known CPU is8.515625 Job +1.421875 wrapper =9.9375 seconds,
with wrapper-supervision0.03125 contained in the wrapper,not added twice. Peak
Job private commit is640,319,488 bytes. Successful Environment compile wall was
8.3845987 seconds and failed Source compile wall1.3911803 seconds. This reviewer
performed only saved JSON/log/source inspection and hashing,not compiler reruns.

## Source02 single-command continuation: source review

**SOURCE-CLEAR for exactly one repaired-source compiler invocation.** The
read-only comparison confirms `ReferenceSource02.lean`
`79a13b525b20f96b82b1ecaf4da5561248998968b073d82db8b855ca88133ef2`
changes only the nested limits-record layout: the same field values now use
separate consistently indented lines. No acceptance, dependency or protocol
rule changes. The whole previous source remains preserved.

Fully read `build_reference_source_continuation.py`
`9063669bb434b39a141e755203f5b5e794de34d63682423827432de2bcd2a13b`
and `select_reference_source_continuation.py`
`8c1988195fc32628f6287b262a6e98796d2c0774e6d19081b1c84b4a66dea038`.
They explicitly authenticate the failed01 RESULT/selection/failure/INPUTS,
successful Environment/failed Source exact command vectors and exit statuses,
both original source snapshots/staged files and the sole exact Environment
artifact. They revalidate original support/runtime through the pinned base
builder; a missing successful BUILD receipt is never fabricated. The new
selection has eleven source snapshots,twelve reused helper artifacts and23
runtime files. Only Source02 is compiled; Environment and the eleven prior
helpers are referenced in place,not rebuilt or copied.

Fresh limits are90 wall/60 aggregate CPU seconds/1536MiB/four processes; the
inner controller retains75 wall/45 controller CPU seconds and32-MiB cooperative
spool. Exact final input/snapshot/output/metadata checks are required. No `main`,
selected library,owner operation or mathematical acceptance is invoked. The
reviewer ran no selector or compiler. Package assembly must adopt the actual
successful continuation plus its explicitly retained partial Environment rather
than the obsolete all-success build01 schema.

## Actual Source02 continuation01: saved-output audit

**PASS for one compile-only continuation.** Exact saved evidence:

| Artifact | SHA-256 |
|---|---|
| `selection.json` | `8c81e10c81c6c8fe9e392294eb1425f35ae2291fa24e157f3d98939fd15f03ba` |
| `RESULT.json` | `90f9f8d28edd56aef6ff5a43da5718b557beff95cd71205f8d194df534126265` |
| `build/BUILD.json` | `f35a2fd9abb6e45c735b0cf60d50c0b0115d90e25e2b3eb0e21d8762fb49c835` |
| `build/INPUTS.json` | `f6f07fa318dcaa0ae20e64745d01c5ef5de4573b07c37b929e5a35c33e9d0883` |
| `build/NATIVE-OUTPUTS.json` | `b61d9489633e12f57a2e0ce7ea61fd394bb739fcb7df249152c1c53eb0c7f836` |
| `build/objects/ReferenceSource02.olean` | `d0fdb8a8bb9b6ac225586d84be788e6a8b842640677fefabac12701b886a7bea` |

The audit confirms59 identical selection/input/receipt bindings,48 independently
rehashed small inputs,all eleven exact source snapshots,twelve retained support
artifacts and the staged source/generated output/metadata pins with zero
mismatches. Eleven larger runtime files retain the executed before/after checks.
The new object is1,472,712 bytes; exact pre-receipt fresh spool is1,505,609 bytes,
matching the receipt. Directory censuses agree with one source,one object,two
metadata files and the final BUILD receipt. The retained Environment stays at
its separately audited failed01 prefix location and exact hash; it was neither
rebuilt nor copied. The failed01 source/failure records remain unchanged.

Stdout contains exactly one successful Source02 compiler command and the
compile-only receipt; stderr is empty. Direct child is reaped,Job closed,
zero active/terminated processes,no termination request or cleanup errors.
Outer wall is4.0165953 seconds; known CPU is2.6875 Job +0.90625 wrapper =3.59375
seconds. Peak Job private commit is625,217,536 bytes. Compiler command wall is
1.4538278 seconds. These are actual small local compilation costs,not an
executed exporter,reference contribution,network or growth result. No command
was rerun by the auditor. Shipping Source02 text under the logical
`ReferenceSource.lean` role does not require installing its validation-only
compiled Source02 object; the exact compiled Environment remains its dependency.

For the forthcoming integration, one high-value negative control is sufficient:
an owner source theorem `reference_false : False := by sorry` should compile but
never become accepted mathematics. Require actual successful source compilation
and a refusal attributable to `sorryAx` at the external-frontier/forbidden-name
boundary,with no admission entry/new root and clean charged closure. A parser
or unrelated source failure would not establish this property. This targets the
new compiler-to-extractor boundary without repeating old matcher mutations; it
is a proposed test,not an executed result or independent runtime authorization.

## Assembly review correction: receipt parser seam

**HOLD assembler selection pending a narrow parser correction.** On reviewing
the partial-prefix successor `assemble.py`
`51487e666df7a8237b1fb555fd5e5d101bffc738a14fef040c86b04f2291fb26`,
the reviewer identified a preexisting missed seam: `document()` uses the
preserved loader's `owner_json` for all exact-pinned documents. That parser
rejects every floating-point number. Actual assembly and compiler receipts
contain finite wall/CPU measurements,so reading those records cannot succeed.
The earlier assembler-only source clearance is withdrawn; controller,owner,
profile,native and actual compile results are unaffected. This is a source
review correction,not a newly executed failure.

The successor's changed source map and retained-prefix provenance agree with the
actual audited continuation: Source02 is shipped under the original logical
source role; Environment comes from its exact successful failed01 prefix; the
validation-only Source02 object is not installed. Fix only the document-parser
boundary: profiles/manifests retain their strict parser,while hash-bound outcome
receipts need duplicate-key/nonfinite-safe parsing that accepts finite floats.
No native rerun or broad package rewrite is warranted. Root and the author were
notified before clearance of this successor.

**Repair reviewed; assembler source clearance restored** at
`c4628e67b8bf5109fedb839cf0815c874d1febc224106dc3dae496756754ef7f`.
Only exact-pinned diagnostic documents use the new parser,which rejects duplicate
keys,JSON nonfinite constants and numeric overflow while accepting finite floats.
PROFILE and installation manifests still use the original integer-only parser.
The successful Source02 continuation and partial Environment mapping remain
explicit; the old failure is preserved in the assembly receipt. Unchanged
selector/profile retain their prior source clearances. No selection or assembly
was executed by the reviewer.

For the proposed `sorry` control,positive-extraction exit-zero cleanup is not the
right predicate. Existing exchange may request whole-Job termination after the
expected premature EOF,even after the exporter has emitted its semantic refusal.
The control must retain any such request/terminated-process facts and require
complete final CPU accounting,direct child reaping,closed Job,joined readers,
no cleanup errors and zero active processes. Exact `sorryAx` refusal,successful
source compilation,no admission entry/new root and preserved artifacts remain
required. This establishes an expected semantic refusal with completed cleanup,
not a claim that every negative-path process exited voluntarily.

## Actual reference assembly01: saved package audit

**PASS for file-only package integrity/census,not runtime adoption.** Independent
hashing confirms all165 payloads and137 auxiliary profile entries,24 selected
source snapshots,13 original/copied retained artifact pairs,and all132 unchanged
predecessor files. Exactly31 payloads were added and owner/profile were the only
two changed predecessor files. Package census is167 files including PROFILE and
ASSEMBLY; copied payload size is exactly57,976,127 bytes. The reviewer recomputed
the20-source payload-map digest
`e0a3a23992c874589e04f2fd25262cfe6ec1dff1a806bd8c586d58bc7c00009a`.
All207 selected input bindings were checked;203 small inputs were independently
rehashed while four larger runtime files retain the executed before/after checks.
No size,hash,map or census mismatch was found.

| Artifact | SHA-256 |
|---|---|
| `selection.json` | `54f943d465b6546f386dbfe5631a1d2d7ed11f310c9bb51002f35e593826796c` |
| `RESULT.json` | `4e9b05ad04a91ae9ffe59d7d3c97330912ee6193f4446f2a03b2abc0b6dc04a6` |
| `package/PROFILE.json` | `2d965cb67cb6729dfe42380146377bb1ab85ef42713c1de3f6668da09ba2fb13` |
| `package/ASSEMBLY.json` | `ae7ff57af40576ca2b7683baf188d366f3803b5c3e44f7a72f0f25540ef81671` |

The receipt retains actual successful continuation and partial-Environment
failure provenance separately. Source02 text is correctly mapped to the logical
ReferenceSource role,and the helper census remains isolated from ordinary
authoring. No validation-only Source02 `.olean` was inserted into the package.
Actual child exit is zero with clean reaping/Job closure,no termination request
or cleanup errors,zero active/terminated processes and empty stderr. Wall time
is6.6451448 seconds; known CPU2.421875 Job +0.78125 wrapper =3.203125 seconds.
Peak Job private commit is19,382,272 bytes. This reviewer inspected saved files
and hashes only,no imports,owner/store opens,native launches or reassembly.

## Eight-call public workflow: independent source review

**SOURCE-CLEAR,not an executed workflow result.** Fully read
`public_workflow.py` at
`32b331c8e853c38e328eaf6cd8a96c349b57b8b4d8ad8b72e81a2f48d078d300`
and `select_public_workflow.py` at
`a345b30accf7efd1740b6697ca5036d726fecc1cbee1ec6c595235df7370a1f5`.
Checked the reused pinned helper methods,actual product result schemas,fixture
source and refusal call ordering without importing or running them.

Exactly eight public owner processes initialize a fresh owner,intake the six
retained units,register their original library,author A,materialize A's new-only
delta,author B over that delta,refuse one compiled sorry theorem,and query exact
final public state. The harness does not invoke product APIs or write accepted
state directly. Existing approved fixture artifacts are reused; only the real
registration makes its required protected copy. Four new theorems are bounded
integration examples,not novel discovery or useful-growth evidence.

Assertions tie actual accepted roots/units/export identities to their retained
evidence and real admission-worker reports. They inspect proof constants and
exact imports to establish A's use of original `flip_low`,B's use of A's
involution theorem,and B's continued original-theorem use. B's setup must import
the generated module,and delta units must exclude old fixture units. No result
is counted merely because a source compiler or saved correspondence succeeded.

The negative marker was corrected before selection: existing OrdinaryExport
checks `CheckedExtension.requireName` before the dynamic boundary callback,so
the expected cause is `ORDINARY_EXTENSION SORRY_REFERENCE`,not the later
resolver's outside-frontier message. `False` was independently confirmed in the
actual522-name usable public basis,preventing an unrelated missing-type refusal
from satisfying the test. Successful compilation/five pinned artifacts,explicit
extraction refusal,no admission entry or output,and subsequent exact four-root
public census are required. Expected extraction cleanup facts remain disclosed.

The final call ledger replaces a full CPU reservation only after finite
nonnegative final CPU,zero active processes,at least one attached process and
direct-child reaping establish complete observation. Otherwise the full grant
and incomplete status are preserved. All calls consume one540-wall/420-CPU
parent allocation with remaining per-call caps; the outer envelope is600 wall/
480 aggregate CPU seconds/1792MiB/eight processes. No automatic retry or extra
negative campaign is selected. The auditor did not execute the selector or any
of these public commands. After this integration,component polishing requires
a new central-payoff justification; the growth architecture may need revision.

## Actual public workflow01: failed protected registration, successes preserved

**Independent saved-output audit, 2026-10-24: FAILED, not a reciprocal-workflow
pass.** Read the saved files and selected source only; no product import, owner
or database opening, native process, retry or state change was performed.

Exactly three of eight selected public calls ran. `init` admitted 456 basis
units (581 names) at root
`138c02d2de87fcc82cdfd11ac292ee9a9fb2ff41761f00174c6793337f1f8ee4`.
`intake-baseline` admitted the six retained units/nine exports, 31,083 evidence
bytes, at root
`72b399a0e3ad4a1673ec369115c255dd0f3016ae2956572c5def4ce1081f96b1`.
Those two actual accepted results remain successes. Intake explicitly did not
register the original library or create a peer-transferable warrant. Neither
source contribution, new-only delta, compiled-sorry refusal nor final status ran.

Registration made its protected snapshot and completed the actual native match:
six private units/nine names, five public units/eight names, 581 basis rows and
522 usable names, zero pruning rounds. Its native command exited zero, reaped
cleanly, closed its Job, left zero active/terminated processes and had no cleanup
error or termination request. Its stderr contains phase diagnostics, not a
failure. This is correspondence evidence only, **not registration acceptance**.

The deterministic commit failure is an integration mismatch in the protected
operation census. `reference_store.py` allows only `stdout.txt` and `stderr.txt`
under `supervision/`, but the selected supervisor also writes the actual
2,012-byte `supervision/command.json`. The census therefore raises
`REFERENCE_OPERATION_FILE`. The source calls `_close_operation` before this
census and performs record staging/rename only afterwards. Actual
`CLOSED.json` consequently says `LIVE_CORRESPONDENCE_CLEAN_BEFORE_COMMIT`, while
`FAILURE.json` records phase `PROTECTED_COMMIT` and no new catalog acceptance.
The protected records directory is empty; no staged record was observed. Do not
treat the close marker or the saved matcher report as a committed reference.

The workflow's generic `SMOKE_UNCLEAN_PROCESS_TREE` error here is its
expected-exit-zero check rejecting actual exit 1; the saved process evidence
does **not** show a leak or unclean reaping. The outer command exited 1, closed
its Job, reaped the child, left zero active/terminated processes, and reports no
termination request or cleanup error. Wall time was 120.1050634 seconds; known
CPU was 76.4375 Job + 1.265625 outer wrapper = **77.703125 seconds**. Peak Job
private commit was 993,980,416 bytes. Nested child CPU is already included in the
outer Job and must not be added again. The three public-call Job totals were
22.609375, 3.265625 and 49.046875 seconds. Registration's native CPU was 6.03125;
its controller CPU was 42.875, an important non-native cost rather than a reason
to pursue certificate optimization. Intake's partial native observation remains
separate from its conservative 60-second reservation.

Rechecked all 199 retained input sizes and 196 inputs at most 32 MiB by SHA-256;
three larger runtime pins retain their executed checks. All four selected source
snapshots hash-match. No mismatch was found. Exact evidence under
`experiments/v5-local-checks/ordinary-reference-public-workflow-01`:

| Artifact | SHA-256 |
|---|---|
| `selection.json` | `99796dea391f7ead5f97bb80ed3131e15ed9bdf042230a69a54ed8f485e7ac5b` |
| `RESULT.json` | `9742b6dbcf8c9453cf5a6f8095b1bb373f149e863b4e6e4e1e240fc65f9da061` |
| `workflow/INPUTS.json` | `641699aa6224025b06a6263f8c29031e3294dea52dca5f590870c2b686b4a673` |
| `workflow/WORKFLOW.json` | `b99ae315a7f17cf5df9019d739f0d6577c65df929bdb8044bec42cbbd2a81734` |
| `workflow/PLAN.json` | `756db69649e3f6486b5d5a0fc504abe3039b0aac03d5a525eff7ed3d840d6891` |

The failed protected operation is
`97440ed1f77850e5b58a7256172246dc45efbded96ed160faef827e65b86874a`
under `workflow/catalog/ordinary-realizations-v1/operations/`. Its report hash is
`dee3a15c91a42c12cf3bab6319ab8f4ce7490d7d012a07320b167016d977e936`;
SUPERVISION hash is
`716f799f9faca87edba8ccc8c9d62838693193e85d67cee5b6e43ddf63808769`;
command hash is
`71bee39bb7586be5a14cc9d2bf80149c813e0f620c578999c0e9b5d031d26acb`.

Disposition: preserve all successes, failure and costs; do not rerun initialization,
intake or native correspondence merely to repair a diagnostic-file allowlist.
A selected successor can narrowly repair bounded census handling, but adopting
the old partial operation would require an explicit recovery design, not a forged
live event or silent retry. First address the growth/compatibility decision that
may change this architecture. This audit grants no runtime or migration authority.

## Independent changed-boundary review: source02 census/classification repair

**SOURCE-CLEAR, 2026-10-24; no execution or integration pass.** Read the complete
three-hunk predecessor/successor diff, affected caller/census/reservation code and
the frozen `relocated_smoke.clean` validator. Independently confirmed final pins:

| Fresh source | SHA-256 |
|---|---|
| `ordinary_reference/reference_store02.py` | `bc15b9dd7c4386f05f58c36b9cd01887f709c6a75b6cb8418eec6309559080b1` |
| `ordinary_reference_package/public_workflow02.py` | `8193ae500a1108f84c321132d09c486844a9db4bcc963ce6caf4835fcc53f16b` |

The store now permits exactly the one additional bounded diagnostic filename
`supervision/command.json` at at most 1 MiB; ordinary-file checks and global
entry/metadata/total caps still apply. Its bytes remain metadata, not a warrant
or accepted report. No arbitrary filename, nested subtree or new commit route is
allowed. The change applies to both existing operation kinds, which use the same
supervisor behavior.

Initial review caught the required coupled delta reservation: its prior 23 MiB
allowance omitted the added command file. The final source reserves 24 MiB plus
the 4,096-byte close record, retaining the same 32 MiB metadata and 128 MiB
operation caps. Arithmetic: final/pending reports 16, trace 1, supervision 1,
command 1, logs 2, failure 1 and staged record 2 MiB. Request/inventory/input
lengths are still separately included. This can only tighten prospective
admission. Original-reference 8 MiB control overhead already accommodates the
extra file. No live grant or old reservation was changed.

The workflow now first checks cleanup against the actual integer exit code,
then separately rejects disagreement with the intended zero/one outcome. The
unchanged cleanup validator still requires the corresponding success/failure
status, clean reaping, closed Job, no termination/cleanup errors, zero active and
terminated children and finite CPU. Actual nonzero failure therefore cannot
become a pass; its diagnostic is simply no longer mislabeled an unclean tree.
All saved replies and charging occur before the check, as before. The intended
negative's detailed refusal assertions are unchanged.

The successor retains old package/run constants and is not a selected runnable
continuation. No product import, parser execution, experiment, package/state
change, snapshot copy, owner operation or retry was performed by this reviewer.
The source repair does not retroactively register the failed reference. Root
must separately select any future integration/recovery semantics. The next
architectural priority remains substantive applicability/growth, not relaunching
the eight-call workflow to turn a local diagnostic green.
