# Missing imported library results: reuse the complete-proof extractor

2026-10-23, `project_hook_design`. Source/theory only: no product edits, imports,
builds, tests, whole-library scans, external access or Git operations.

## Decision

**Yes, the essential extraction mechanism already exists and has worked for an
installed-library lemma. No, the current portable public package does not yet
expose general approved-project ingestion.** Reuse the selective complete-proof
extractor and existing independent receiver, not the new-target authoring hook.
Do not relax `CURRENT_MODULE_TARGET_REQUIRED` to solve this separate problem.

The real gap is product integration and portable identity/batch planning, plus
explicit approved-project artifact selection. It is not a missing proof system,
need for certificates, or justification for trusting compiler success.

## Exact reusable mechanisms

- `MissingImportExporter.run` loads one selected installed Std environment via
  `importModules ... (plugins := #[]) (loadExts := false) (level := .private)`.
  Targets must exist as safe complete nonaxiom records and be absent from the
  protected parent. It emits inert `DMKN_ORDINARY_MISSING_IMPORT_BUNDLE_V1`.
- Its memoized, sequential parent-lookup protocol stops only when the protected
  controller supplies an exact accepted symbol ID. An absent name requires its
  complete declaration and recursive missing dependencies. Names are not warrants.
- `Export.selectedFromBoundary` accepts imported targets; its lazy
  `IndexedSource` needs no up-front environment census for ordinary definitions
  or theorems. `BootstrapProbe.makeUnit` turns actual `.thmInfo` into `.thmDecl`
  including the proof value, and similarly includes definition/opaque bodies.
- The same scheduler topologically orders missing units, checks closure/budgets
  and rejects boundary/group straddles. A genuinely missing inductive group
  triggers `indexSource`'s bounded environment census to recover complete actual
  inductive/constructor/recursor records; this exception must stay explicit.
- `SuccessorExport.selectedAbove`/`selectedInterpreted` also use this scheduler
  without an imported-target ban, but have their own boundary-correspondence
  premises. `selectedDeferred` deliberately stops at imported names and rejects
  imported targets: it is NOT the missing-proof extractor.
- Legacy `run_successor_admission.successor_envelopes(..., supplement=...)`
  already plans supplemental units before unchanged consumer units, using exact
  parent IDs and provisional earlier-unit IDs under one combined allowance.
  It does not accept either lane itself; the unchanged receiver checks both.

These source paths are under `software/v5/ordinary_lean/`. The legacy controller
contains V1 identity domains, fixed context/profile constants and experiment
layout assumptions. Calling it directly is not a generic portable V2 API.

## Existing evidence: do not repeat the mechanism experiment

The saved missing-import completion extracted `List.map_congr_left`'s two-unit
closure using 34 point lookups and 32 accepted boundary imports (36,382 bytes).
The subsequently adopted seven-unit admission checked those two units plus the
unchanged five consumer units. NOW records independent adoption `468c1fba`.
See MISSING-IMPORT-COMPLETION-PLAN and COMBINED-ADMISSION-IMPLEMENTATION.
This is retained installed-Std/legacy workflow evidence, not a new audit, generic
project qualification or proof that the current portable package exposes it.

## Visibility and actual proof availability

Lean 4.34.0's module system can export a theorem as an axiom-shaped signature;
an ordinary public import may therefore have no proof value for extraction.
This is not evidence the theorem is false, nor permission to ingest its axiom.
NativeOwnerExporter already rejects `TARGET_PUBLIC_AXIOM_VIEW_NOT_PROOF`.

The separate `.private` import requests full data through the selected module
closure. Lean's Environment source documents that this behaves as if module
annotations were absent. Modern module data uses matching `.olean`,
`.olean.server` and `.olean.private` parts; shared-object references require
loading compatible parts together, not independently reading a private file.
The current importer may also load IR parts. Merely keeping public signatures
or compiled machine code does not recover erased/missing proof terms.
If the private record is still an axiom, absent, unsafe, or incomplete, refuse;
obtain actual proof-bearing artifacts separately or use a different workflow.

No plugins/extensions are initialized by the selected extractor. This reduces
execution surface but does not make arbitrary `.olean` files safe to deserialize.
Only owner-approved local artifacts/toolchain may be loaded. Peer exchange stays
inert. Fixed runtime precedence must prevent approved project paths shadowing
the selected Init/Lean foundation. Never auto-fetch/build an unknown package.

## Acceptance and cost conditions

The fixed foundation has 456 units/581 names and its permitted axiom descriptors.
`CheckedExtension.allowedDeclaration/checkBatch` permits safe definitions,
theorems, safe opaque declarations and complete safe inductive groups; no new
axioms, quotient initialization, unsafe/partial declarations or `sorryAx`.
`Lean.reduceBool`/`Lean.reduceNat` and forbidden generated names also remain out.
All new units require actual `addDeclCore ... (doCheck := true)` and exact
generated-record comparison against the real accepted receiver environment.

An acquired theorem's scratch construction axiom has a different role: it names
an already warranted receiver theorem for candidate authoring. It cannot supply
the proof of missing library B. Missing B needs an actual proof-bearing record.
Acceptance still proves the receiver interpretation of exported terms, not full
semantic equivalence with a possibly different same-named local package.

For missing closure U and accepted boundary K, traversal/checking depends on U
and reached boundary lookups, not replay of every proof already in K. However,
private module loading can require its whole transitive artifact environment;
new-group recovery can require a bounded census. Neither cost is O(|U|) merely
because the later traversal is selective. Choose narrow modules, keep one
extractor environment live, end extraction before receiver checking, and refuse
over-budget work. A cold large missing closure may make package sharing cheaper.

## Smallest justified public seam

Add an explicit owner-approved **local-library completion** operation, distinct
from new-target contribution and selected only when names are genuinely missing.
Inputs: exact portable S/F/parent, finite missing names, approved module/path
selection, fresh outputs and one remaining aggregate allowance. Existing helper
supports installed Std only; generic project paths need a separately reviewed
successor, not silently deleting its `INSTALLED_STD_MODULE_REQUIRED` protection.

Reuse the private importer, bounded parent lookup and shared closure scheduler.
Port the existing combined-planning invariant to the current V2 evidence domains:
supplement targets equal the missing set; boundary IDs match protected K;
supplement outputs are provisional, absent from K and disjoint from consumer
outputs; exact raw consumer units/claimed IDs stay unchanged; no undeclared
extra dependency is introduced; one combined node/byte/unit/time allowance.
Only after complete planning call the existing `owner.preflight/owner.admit` and
retention flow. Do not insert supplemental IDs into the protected parent early.
The current `portable_candidate.bind_candidate` has no supplement parameter;
this small explicit planner is necessary, not an already shipped capability.

Initially expose explicit completion of a retained candidate, so successful
authoring need not be repeated. A standalone ingest facade may use the same
extraction/checking seam; it must not become a second acceptance implementation.
Recheck candidate/parent/prepared bindings, preserve its bytes and diagnostics,
and make any changed parent an explicit new operation rather than silent rebase.

Minimum new evidence: pure V2 identity/collision/combined-budget controls, then
one public completion over existing eligible state after source review. Reuse
the retained legacy extraction/acceptance evidence; no new difficult theorem,
basis rebuild or large corpus experiment. Generic-project compatibility still
needs an actual approved compatible project; none is currently selected.
Stop expanding this route if safe pinned package sharing with the same assurance,
warm caches and useful discovery costs less overall. The commons can complement
that workflow through selective discovery/custody rather than replace it.
