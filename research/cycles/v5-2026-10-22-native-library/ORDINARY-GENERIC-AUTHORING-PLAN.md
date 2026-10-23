# Smallest generic owner-source contribution API

2026-10-23. Source-only audit by `portable_integration_audit`, after the reviewed
body-discovery adapter handoff. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
No source implementation, build, experiment, state operation or Git mutation
was performed for this plan. Root owns any later source/runtime selection.

## Decision

Generalize the functioning **existing** owner-source pipeline into a library
entry point accepting caller-authored source, a bounded acquired-target set and
caller-chosen new output names. Do not build another pipeline or make users copy
the Stable fixture. The underlying request, exporter, candidate binder and
checker already support most of this generality; only thin wrappers and the
current orchestration impose the fixture restrictions.

Owner source remains explicitly owner-approved executable Lean code. Resource
supervision is not a hostile-source sandbox. Peer contributions continue to
cross the inert evidence boundary, never this source-execution API automatically.

## Source findings

| Existing seam | Already reusable | Current fixture restriction |
|---|---|---|
| `portable_owner_request.prepare` | Bounded target list, exact protected context lookups, local evidence closure, signature-only accepted theorem construction. | Current caller passes one target and `max_targets=1`. |
| `OwnerConstruction.constructPrepared` and portable constructor wrapper | Constructs selected meanings in an ordinary scratch owner environment, preserving actual name/definition checks. | No need for a new constructor or proof mechanism. |
| `SuccessorExport.selectedDeferred` | Accepts `Array Name`; checks distinct local new targets and computes one dependency-ordered selected closure. | No need for N separate exports or later Python graph merging. |
| `PortableConstructExportCommand` | Current-context labels and exact V2 candidate serialization already exist. | `run` accepts one Name and insists on `.thmInfo`, even though selectedDeferred is broader. |
| `portable_candidate.bind_candidate` | Exact expected target list, claimed-ID preservation, protected lookup of explicitly unclaimed names, new-output collision refusal, dependency order and bounded full units. | Current caller supplies `[stable_threefold]` and `max_targets=1`. |
| `ordinary_admission` | Existing preflight, actual-event checking, evidence retention before promotion and checked local root. | Must remain the sole mathematical acceptance path. |
| `ordinary_successor_authoring.author_successor` | Operates on an already opened owner/custody, preserves parent deadline/CPU accounting, retains failure and accepted state. | Hardcoded `SUCCESSOR`, one acquired target, specific-use assertion, five template sentinels, one preview/result. |

The old producer driver separately initializes a fresh owner and repeats much
of this orchestration. The generic contribution function should not initialize,
copy or migrate a catalog. Owner setup is a separate existing operation.

## Proposed public function

```text
contribute_source(
    owner, parent_root,
    acquired_targets,             # exact [{name, export_id, unit_id}, ...]
    source_body,                  # bounded UTF-8 owner-approved declaration text
    output_names,                 # bounded distinct encoded Lean names
    *, output_directory, authoring_profile,
    parent_deadline, make_budget, account_worker_cpu, check_parent
) -> contribution_result
```

Retain the existing trusted allocation callbacks initially; do not invent a new
funding/ledger framework merely to shorten the signature. An installed caller
can wrap these in its ordinary session API. One original finite allocation
covers preparation, source elaboration, candidate parsing, checking and output
retention; fresh stages never renew that parent allowance.

`source_body` contains the user's ordinary definitions/theorems, namespaces,
local notation and proofs. The controller generates the fixed `module`/Init/
selected-wrapper imports and construction prelude, inserts the exact body bytes,
then generates the export postlude. Users do not supply or replace sentinel
strings. Any collision or malformed use of controller state still fails the
final exact candidate binding/checker. This simple scratch-module interface is
not yet attachment to an arbitrary preexisting Lake project or arbitrary plugins.

Keep that initial scope explicit. Full existing-project integration needs its
own source/import ownership contract; do not promise it by calling a scratch
source-body function “general.” Ordinary definitions and theorem names within
the supported interface should nevertheless be caller-chosen, not fixture names.

## Minimal new native seam, not a second exporter

The Python request and binder already support multiple names. To expose that
capability, add a thin successor of the used export command which reads a
bounded **local output-target name list** and calls existing `selectedDeferred`
once on the array. Reuse the current context check, fresh output path,
`candidateBundleBytes` and limits. No new candidate/evidence wire schema.

Read encoded names from a controller-generated local JSON file using existing
name readers, instead of interpolating arbitrary Unicode names into Lean source
syntax. The candidate binder receives the very same expected list. Pin/read back
this file alongside the prepared request/source. This is a local control file,
not a peer truth claim or a new published protocol.

For each requested target, require current-module/new/not-boundary and supported
safe constant kind. Do not require every contribution to be a theorem: a plain
transparent definition is a legitimate output. Delegate complete generated-group
closure to the existing exporter; do not split a group to satisfy a list. Exact
output kind support must match the selected current ordinary checker, not be
inferred from successful elaboration. Unsupported axioms/unsafe/partial records
refuse under existing rules. The wrapper does not grant a warrant.

A strictly smaller interim API could accept one arbitrary new theorem name
using the existing compiled command unchanged. That removes the fixture name
but still prevents bare definitions and batching. Because the existing exporter
and binder already support arrays, the small wrapper generalization has a clear
product payoff; N independent exports and Python unit deduplication are worse
engineering for this need and are not recommended.

## Reuse the current control flow with only these changes

1. Validate the acquired/output sets, source bytes, supported authoring profile
   and allocation before native work. New output names must be distinct and
   absent from the selected protected context. Canonicalize a detached acquired
   list; reject name/ID conflicts, not merely duplicate text.
2. Freeze the selected context view for callbacks. Every acquired `(name,ID)`
   must be locally warranted, and its exact locator must reproduce the provided
   UnitID/ExportID. Reuse local custody and existing request construction; no
   network fetch or acceptance is silently performed by contribution.
3. Prepare the bounded acquired set. If it is empty, use one exact pinned basis
   anchor solely to satisfy the existing nonempty request syntax, with zero
   external evidence fetch. This is initialization of the authoring boundary,
   not a required research goal or a claim of remote reuse. Avoid changing the
   request schema merely for this representation detail.
4. In the fixed Init-plus-wrapper scratch module, nonbasis acquired names are
   absent initially. The current `owner_absent=True` hint is appropriate there
   and remains rechecked by Lean. Do not reuse it for an arbitrary preloaded
   project without the actual presence contract. Definitions retain construction
   semantics; accepted theorem signatures omit proof-only authoring ancestry.
5. Generate the source prelude/body/postlude and bounded output-name list; pin
   every controller input. Run one selected owner-authoring worker under the
   existing supervisor. Read back exact inputs and require the existing clean
   event before processing its inert candidate.
6. Bind once with the complete `output_names` list and prepared/protected IDs.
   Return unresolved local-interpretation names explicitly; do not guess IDs,
   change a claimed dependency or acquire new trust automatically.
7. Reuse ordinary preflight/admission for the whole selected unit closure. No
   compiler receipt, constructed theorem signature or index record is authority.
8. Return each requested output's exact name, UnitID and ExportID, and derive
   previews for all requested outputs from their admitted evidence. Existing
   custody already retains the complete evidence before promotion. Duplicate
   output previews share unit evidence; do not recheck a unit for each export.

Remove the fixture's `SUCCESSOR_ACQUIRED_METHOD_NOT_USED` condition from the
generic acceptance path. A caller may prepare extra options and use only some;
a valid new result need not depend on every requested method. Report actual
dependencies if useful. A particular growth experiment may independently demand
substantive reuse, but that is not mathematical admission or a global protocol
condition. Similarly, do not assert newly checked units are useful growth merely
because the requested outputs exist.

## Durability, installation and failure semantics

The return has separate facts: source execution completed; candidate bound;
units mathematically checked; exact publication bytes retained. Index insertion,
peer receipt, replica retention and useful growth remain separate operations.
If failure occurs after mathematical admission, preserve and report the accepted
root/evidence and unfinished publication status. Do not call it “nothing happened,”
roll back warranted mathematics or rerun authoring automatically.

Do not require public callers to invent helper paths and trust them by location.
The current tested orchestration relies on root's selected external authoring
helpers. A deployable API needs one optional owner-authoring capability in the
existing installation/support manifest: pinned Python controller/request/binder,
the selected compiler wrapper artifacts and actual worker/runtime attachments.
Reuse the existing installation identity and source-map discipline, without
rehashing an entire world library for each contribution. This is a packaging
consequence of the public API, not a new network identity system.

## Smallest next evidence and stop rule

First independently review the small Python parameterization and target-array
native wrapper. Use non-native controls for target collisions, empty acquired
set, exact acquired-set IDs, marker-free source assembly, budget propagation,
multiple output bookkeeping and accepted-but-publication-failed reporting.

If later selected, one bounded actual operation should use caller-chosen new
names and more than one acquired target; include a bare definition output so
that the generalized target path is genuinely exercised. Use existing retained
library evidence and one changed-boundary operation, not another foundation,
discovery, custody or full reciprocal campaign. Root owns its exact fresh state
and finite allocation; this plan authorizes neither.

Stop once an independent caller can supply its own source/acquired set/output
names through the same checked path. Do not add a project manager, plugin loader,
arbitrary source sandbox or certificate mechanism before that real workflow
demonstrates a need. This generic API is a consequential operability increment,
not final-v5 completion by itself.
