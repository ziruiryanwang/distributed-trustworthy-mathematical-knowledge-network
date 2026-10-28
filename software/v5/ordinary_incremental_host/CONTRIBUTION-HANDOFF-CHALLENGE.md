# Contribution handoff: independent challenge

2026-10-28, query_scaling. **Support the selected standalone offline companion,
with the conditions below.** This is source/theory only: no implementation,
product import, native work, owner/database open, runtime or Git operation.
Root's `ordinary_contribution_bundle/SELECTION.md` selects the narrow follow-on;
source review and runtime selection remain separate.

## What is missing, and what already exists

The gap is an ordinary-user handoff between two existing file layouts. Public
contribution/completion already writes exact portable evidence beneath
`evidence/<UnitID>.json` and returns unit byte/hash pins plus selected target rows.
The host accepts those same bytes beneath `units/<UnitID>.json`, named by the
existing baseline manifest. Reusing `baseline_bundle.make_manifest` supplies the
format logic; no new export semantics, host API, native work or owner state is
needed. An expert can compose the existing APIs today. The new benefit is a
bounded, reviewable public procedure instead of bespoke manifest scripts.

The current operator preparer already extracts contribution targets for owner
publication, but does not consume its returned unit files or emit a manifest;
its recognized accepted-result cases omit completion. Its intake action consumes
an already existing bundle. Existing custody-return with `selected-units` can
export sparse whole units without ancestry traversal, but requires custody access
and is not a current shipped-kit role. It is useful if public files are missing,
not a reason to reopen an owner when the exact bytes already exist. Native
`produce-baseline` remains useful for other libraries lacking portable returns.

A standalone companion patterned on the pinned pure-codec loader in
`ordinary_preview_view/view_preview.py` is an appropriately small selection.
The five required pure modules are ordinary_evidence, ordinary_semantics,
portable_evidence, portable_candidate and baseline_bundle. The latter imports
portable_candidate even though projection does not run its authoring binder.
Do not load an owner/profile runtime merely to call these pure codecs or copy
the existing manifest grammar into a second implementation.

## Unit, target and dependency semantics

Preserve **every** `result.units` entry, in its supplied order, as its exact raw
bytes. Contribution returns all bound candidate units, not just those containing
requested targets. Completion returns supplementary support units followed by
the original consumer units; requested target names still name the original
outputs. Filtering to target-containing units can silently discard a newly
introduced definition that the target uses. Retain complete declaration groups;
do not extract a theorem from a larger unit or reserialize its evidence.

Validate the unit count/aggregate byte bounds, distinct UnitIDs, declared byte
length and SHA-256, parsed UnitID and exact selected semantic interpretation.
Validate each target against an actual output of its supplied unit: exact
structured name, UnitID and derived ExportID. A claimed name or matching hash
string alone is insufficient. Reject missing files, identity disagreement,
duplicate IDs/target bindings and conflicting target membership. Reuse the
baseline codec's structural and manifest checks as well.

These authoring routes currently cap the returned collection at 32 units and
4 MiB. Preserve those explicit bounds rather than silently raising them. Their
units were new relative to the author's selected parent when originally bound;
the projector cannot establish global novelty or that a destination host has
never stored them. A repeated handoff is still the same immutable content.

The supplied collection is **not necessarily dependency-complete**. Its imports
may refer to previously checked parent material absent from these files. Preserve
those exact import identities, without fetching, walking ancestry, opening a
catalog, inventing declarations or claiming availability. A host can retain the
new units while recipients obtain missing old imports elsewhere. A cold reader
may still need substantial dependency acquisition/checking. No new dependency
resolver or obligations format is needed for this projection.

## Reports select inert data; they do not attest success

Support explicitly recognized helper RESULT and outer contribution/completion
wrapper layouts. When an outer operation label and inner result-kind label are
both present, require their consistent interpretation. Keep the selected report
hash and any reported profile/status/cleanup information as provenance.

Do **not** require a successful outer wrapper, supervisor receipt or ADMISSION
chain merely to copy caller-selected, independently parsed inert files. The owner
wrapper can contain a complete durable result and later mark `ok:false` after
closure failure. The helper RESULT is also intentionally available before outer
closure. Such flags neither establish nor defeat the syntactic identity of the
selected bytes. Missing unit files or an unsupported result layout still refuse;
this is not a generic recovery feature that guesses absent rows from partial logs.

Historical report PROFILE values may differ from the approved codec package.
Record that difference without rewriting the report or repeating authoring.
Actual byte/semantic interpretation checks remain mandatory. The output receipt
must say inert projection and `mathematical_acceptance:false`; it must not turn
claimed original checking, cleanup or batch completion into a fresh attestation.

## Paths, output and disclosure

The caller selects a pinned report, an explicit local evidence directory, the
approved companion/codec package and a fresh output. Read only filenames derived
from validated UnitIDs inside that directory. Never follow `units[].file`,
preview paths, catalog/custody paths or source paths from the report. Those old
absolute paths are unnecessary for relocation and confer no file-read authority.

Produce the existing manifest/unit layout, exact target metadata and a bounded
preparation receipt. No saved preview file is required: unchanged host append
regenerates and resolves previews from the evidence. Any emitted append config
requires the caller's explicit whole-input sharing and partial-publication
selection; the report's claimed success cannot supply that permission. Host
root and descriptor pin are separately selected for the later host invocation.
After moving a bundle, its manifest/units remain portable; a local absolute-path
config must select its new local bundle location and receive a new config pin.

Output must be disjoint from report/evidence/package inputs, written freshly,
and preserve partial output on failure. A completed projection must check its
written byte pins and manifest binding. It does not itself append, listen,
publish, alter an owner or provide rollback. No automatic retry, cleanup deletion
or exact-generation transaction mechanism is warranted here.

## Fair payoff and the next evidence

Additional work is bounded by the selected report and returned unit bytes plus
fixed codec checks, an ordinary copy/readback, manifest construction and metadata.
The saving relative to another cold export is avoiding repeated old-closure
extraction and transfer solely to hand off already emitted new work. Against an
expert's optimized use of the same APIs, this is a usability saving, not an
asymptotic improvement. Existing owner publication can remain cheaper when the
author also hosts and no independent file handoff is needed.

Charge original creative exploration, failed attempts, owner-context loading,
authoring/admission, earlier file production, current copying and transfer,
duplicate inputs, curation, discovery, hosting and recipient checking. The
projector does not make that entire loop proportional only to new bytes, prove
useful concept growth or solve loss of the author's old dependency custody.

Changed-boundary validation needs retained contribution/completion data with a
support-only unit, exact relocation and manifest compatibility, both recognized
report layouts, provenance-only failed/old-profile flags, and altered/missing
unit or target refusals. Source/final file checks can establish the unchanged host
input contract; any selected runtime should exercise only this new input seam.
No new theorem production, replay of the passed host lifecycle or broad export
campaign is required. Stop after this handoff is usable and reassess the next
workflow obstacle.

## Source anchors

- `ordinary_demand_frontier/ordinary_contribution.py` 238-264 and 583-640:
  exact output mapping, bounded raw units, evidence/previews and result fields.
- `ordinary_library_package/completion_api.py` 93-159 and
  `library_completion.py` 178-218: all supplemental/consumer units and their order.
- `ordinary_lean/portable_candidate.py` 200-241: complete new groups, original
  order, exact import bindings and new-relative-to-parent condition.
- `ordinary_dedicated_host/owner.py` 624-667: outer wrapper and later close failure.
- `ordinary_reply_capacity/operator/prepare.py` 309-386 and 750-787:
  existing extraction/publication conveniences and their different input role.
- `ordinary_binding_reuse/baseline_bundle.py` 261-355 and
  `ordinary_custody_return/custody_return.py` 65-78: existing pure manifest
  machinery versus separately scoped custody access.
- Selected `custodian.py` append regenerates previews and indexes only after
  storing the supplied evidence. No projector-supplied success assertion is used
  as mathematical authority by that host.
