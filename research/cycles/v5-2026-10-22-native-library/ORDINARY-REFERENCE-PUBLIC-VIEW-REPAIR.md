# Ordinary-library public-view repair

## Why this is central

An agent should reuse an already checked ordinary Lean library without rebuilding
that library into a synthetic namespace or producing an expensive certificate for
every contribution. The preserved workflow02 exported and copied its library
successfully, but rejected Lean's legitimate public abstraction of checked
definitions. The exported-view census explains the failure. We reuse those saved
stages and change the interpretation boundary, not the mathematical trust policy.

The user has no external project to nominate. The retained `flip` fixture is a
controlled compatibility discriminator, not a claim of arbitrary project support.

## Selected relation

The private environment must still match the entire exact fixed basis and every
selected independently warranted declaration. Every present public record is
validated against its exact original. A safe singleton definition, theorem or
opaque declaration may be exposed with its exact name, universe order and type
but without its body. Its interpretation is the checked original, not a new
assumed axiom. Inductive, constructor, recursor and quotient rules remain full.

From names present in both actual public frontend and kernel maps, delete names
whose semantic dependencies are unavailable until stable. The resulting greatest
closed subset is the only usable basis. Quotient primitives carry their implicit
whole-family and `Eq` dependencies. Selected public units must have complete
whole-unit closure over this subset. Private proof helpers need not become public.

This follows the conditional interpretation argument in
[the independent contract](ORDINARY-REFERENCE-DELTA-CONTRACT.md). It does not
prove the implementation of Lean's kernel or grant a hidden helper computational
transparency. Exact original identities prevent merging conflicting definitions
merely because their signatures coincide.

## Versioned implementation

- `OrdinaryReferenceBase05.lean`: the changed native matcher; predecessor04 frozen.
- `reference_report02.py`: V2 exact request/report binder; predecessor parser frozen.
- `build_reference05.py` and selector: only three changed matcher build commands,
  retaining the twelve exact support artifacts from successful build04.
- `reference_continuation.py` and selector: reuse workflow02; one genuine positive
  matcher call, one changed transparent-body rejection, bounded in-memory report
  mutations. No recompile of fixture, exporter rerun or snapshot copy.

V2 adds all581 public basis rows with frontend/kernel projections, the ordered
usable subset and basis graph counters. The old fixed inventory stores universe
*counts*, whereas ordinary declarations store ordered names. The binder validates
reported basis parameter names and their counts; actual ordered-name and type
correspondence is a live matcher obligation. The parser does not replay the graph
or turn a saved report into authority. Registration must remain tied to a current
protected owner context and the exact clean native event.

Source review precedes execution. The native fixture's request deliberately uses
test-only labels: a correspondence pass will not establish mathematical admission,
protected registration or final v5. The next consequential capability is live
protected registration followed by a genuinely checked new delta that imports
the original library. Stop expanding diagnostics once this interface decision
has been resolved.

## Concrete protected realization API proposal

2026-10-24, `cold_intake_strategy`; source-design only, awaiting root adoption.
Read the actual `anchor_store`, request/report02, snapshot reopening and existing
live-integration/delta contracts. This section fixes spelling and lifetime seams;
it does not repeat the semantic audit or authorize software, native work or Git.

### One fresh typed successor, not inheritance or a second authority service

Select a fresh `ordinary_reference/reference_store.py` with one owner-local
`ordinary-realizations-v1` sidecar and two record kinds, `original-reference`
and `generated-delta`. Preserve `module-anchors-v1` unchanged. Do not subclass
`anchor_store.Store`: it directly uses generated-only module-global schemas and
limits, requires five new parts/nonempty added names, assumes Init/one bridge,
and its shallow8192-entry census cannot represent a4096-module snapshot.
Reuse its small file/pin primitives and protected lifecycle by composition or
explicit narrow successor code; do not introduce a generic registry framework.
The actual catalog owner and its existing lock remain the only authority.

Fresh schema names:

- Store: `DMKN_LOCAL_ORDINARY_REALIZATION_STORE_V1`.
- Selected support: `DMKN_LOCAL_ORDINARY_REALIZATION_SUPPORT_V1`.
- Reservation/closure: `DMKN_LOCAL_ORDINARY_REALIZATION_RESERVATION_V1` and
  `DMKN_LOCAL_ORDINARY_REALIZATION_CLOSED_V1`.
- Both strictly tagged record variants:
  `DMKN_LOCAL_ORDINARY_REALIZATION_V1`; ID is
  `sha256(b"DMKN-LOCAL-ORDINARY-REALIZATION-V1\0" + canonical_record)`.
- Private warrant table: `DMKN_LOCAL_REFERENCE_WARRANTS_V1`.

Store marker keeps the predecessor's actual store/adoption/activation,
semantic/foundation/implementation and local-limit bindings. Selected support
pins the exact implementation and helpers; an ID/hash supplied by a caller is
not support authentication. Initially require one unchanged selected support
across reference/deltas; support migration is not silently inferred.

### Reference reservation and record-last registration

`reserve_reference(selection, check, deadline=...)` creates exactly one private
live grant under `operations/<operation_id>/`. Selection binds the current
`source_context_root`, exact approved project selection, bundle-manifest pin,
targets and complete finite resource envelope. Reserve before preparation:
the snapshot ID and match-request pin cannot exist until the fresh final
`operations/<id>/snapshot/` location is known. Prepare directly there; never
move a path-bearing snapshot or copy it again at commit.

After preparation, `bind_reference_inputs(grant, request, snapshot, check)`
checks these inputs against the same selection/current owner and writes one
fresh `MATCH-INPUTS.json` before native launch. It pins snapshot manifest,
replay map, inventory, exact authenticated request and selected matcher/support.
It does not renew the grant/deadline or authorize a second native operation.
No saved reservation, request, report or Python value reconstructs a live grant.

`_commit_reference(grant, validated_live_match, check)` is a private controller
seam only after the actual clean supervised match, V2 binding, final snapshot/
support checks and complete current-warrant revalidation. Required retained
files are `snapshot/{prepared-manifest,replay-request,source-report}.json`,
the snapshot parts, and `events/{request,inventory,reference-report,warrants,
SUPERVISION}.json`. Request/report hashes alone never establish this event.

The reference record's exact fields are `schema`, `kind`, `store_binding`,
`support_id`, `operation_id`, `source_context_root`, `snapshot_id`, `targets`,
`snapshot_manifest`, `reference_report`, `warrants`, `event_files`. The three
named file pins and every event pin are `{path,bytes,sha256}`, with paths exact
operation-relative names, not caller-controlled traversal. `snapshot_id` equals
the prepared-manifest hash. Targets carry `{name,export_id,unit_id}`. No fake
module, `added_names`, catalog acceptance, or generated artifacts are required.
Keep the2-MiB record bound; reference targets retain the request's1024/1-MiB
bound, separately from generated targets32/64KiB.

`warrants.json` contains `{schema,semantic_id,foundation_id,bindings}`, where
bindings are unique sorted `{name,symbol_id}` rows: all581 fixed basis identities
plus every complete private output binding from the authenticated request.
The request's checked closed import relation ensures all private imports occur
there. This table contains no proof bodies and has its own32-MiB ceiling.
The request is retained as one-time evidence, not read/reencoded on every load.

Preserve the predecessor discipline: account for failed partial output; clean
failure closes but does not commit; unknown child cleanup blocks further use.
After final validation, write clean `CLOSED.json`, fresh record staging, then
non-overwriting same-volume publication into `records/<id>.json` last. Ambiguous
commit returns exact-ID lookup only, never automatic rerun/reconstruction; a
postcommit reporting failure leaves the committed record intact. Local-store
immutability/no hostile administrator or rollback remain explicit premises.

Reference bounds are independent: snapshot512-MiB parts +64-MiB snapshot
metadata, match request96MiB, V2 report32MiB, warrants32MiB; a768-MiB reference
operation ceiling leaves32MiB for inventory, control files, logs and record.
Enforce the remaining256-MiB metadata cap before writes, not after a partial
copy. Generated operations retain their128-MiB ceiling and generated-chain
limits. Store-wide reservation includes all retained/orphan bytes; a configured
store ceiling may explicitly refuse another reference. The census must allow
the exact4096-module/five-part snapshot depth/count, not widen arbitrary trees.

### Exact load and immutable view

`load_reference(reference_id, current_context, check) -> ReferenceView` requires
the real still-open owner, protected marker/support and exact record identity.
It checks every warrant-table binding against the just-validated current
context; current root may differ from historical `source_context_root`.
It reopens the exact snapshot with `snapshot_reopen.read_snapshot` and verifies
the pinned V2 metadata. It need not reread old proof-bearing request/evidence.
Return immutable bytes/tuples, never nested caller-mutable dictionaries:

```text
ReferenceView(
  reference_id, store_binding, support_id, registration_context_root,
  snapshot: SnapshotView,
  report_path, report_raw, report_sha256,
  warrant_bindings: tuple[(name_key, symbol_id)],
  public_frontier: tuple[(unit_id, tuple[(name_key, export_id)])],
  basis_bindings: tuple[(name_key, kind, ordered_level_keys, projection,
                         kernel_projection)],
  usable_basis_keys: tuple[name_key],
  private_module_keys, public_module_keys,
  record_raw, event_pins)
```

SnapshotView already carries exact roots, replay bytes, module keys, artifact
pins/paths and byte total; do not create a second conflicting artifact map.
Report metadata comes from the protected record's originally bound live report,
not a fresh peer report. Its complete public-unit rows define the frontier.
Reopening validates retained syntax/bindings; it does not re-prove correspondence
or claim that the original shape parser alone authenticates a saved report.

### Native files and concrete plan

Native phases read `request.json` (new work only,4MiB), `inventory.json`, and
`reference-plan.json` (envelope at most1MiB). The latter has exactly:

```text
schema = DMKN_ORDINARY_REFERENCE_MODULE_PLAN_V1
reference_id, snapshot_id, support_id, semantic_id, foundation_id,
implementation_id, registration_context_root, parent_delta_id,
original_roots, reference_report, replay_request, generated_plan
```

`original_roots` is the exact ordered snapshot root vector, each with fixed
`import_all=0,is_exported=1,is_meta=0`. The three last file roles are exact
`{path,bytes,sha256}` pins: retained `events/reference-report.json` (V2,32MiB),
retained `snapshot/replay-request.json` (16MiB), and the operation's
`generated-plan.json` (4MiB). No old private request/body enters this plan.
The reference report supplies both original module orders, all581 basis rows,
usable subset and complete public-unit kind/universe/projection metadata.
Its `context_root` equals **registration_context_root**, not the new request's
current context. Controller revalidates current warrants separately.

Generated-plan schema `DMKN_ORDINARY_REFERENCE_GENERATED_PLAN_V1` has exactly
`schema,reference_id,support_id,delta_id,modules,bindings`. Empty base means
`delta_id=parent_delta_id=""`, empty arrays. Nonempty modules carry
`delta_id,module_name,direct_imports,added_names,artifact_parts`; bindings carry
the predecessor's unit/output metadata with `realization="added"` only.
The first module's direct imports are exactly the original root names; later
modules import exactly the preceding generated name, with the same fixed flags.
The final delta ID equals `parent_delta_id`; no Init assumption or unrelated
reference/chain merge is allowed. Preserve32 modules,1024 units,16384 names,
256-MiB generated artifacts independently of the512-MiB original snapshot.

The `generated-delta` record variant has exactly `schema,kind,store_binding,
support_id,operation_id,source_context_root,reference_id,parent_delta_id,
module_name,direct_imports,targets,materialization_key,artifact_parts,units,
added_names,event_files`. Its key binds support, reference ID, parent delta ID
and targets; the existing `DMKNBridge_<key>` spelling remains usable. Five
artifacts and nonempty added names are required only for this variant. Its
`load_delta` returns the same exact ReferenceView plus a bounded linear generated
view; loading a foreign-reference parent or a legacy anchor record refuses.

The new request/pending/final reports bind `reference_id`, `parent_delta_id`
and exact `reference_plan_sha256`. New request units remain bounded32/4MiB;
the decoder grants only usable basis, public whole-unit frontier and generated
ancestors. Unknown imported names and any private kernel/frontend name collision
refuse; all deltas are new, `units_matched=0`. Worker pins all three plan files
and disjoint original/generated artifact maps across build/private/public
rereads. This is the existing delta contract with concrete file spelling, not
a new mathematical acceptance path.

Root retains controller/selection ownership. Native author confirmed these
metadata needs, especially original-root first imports and historical report
context versus current context; no native implementation starts from this note.

## Selected original-reference source implementation

Root adopted the interface in principle and then explicitly selected only
`ordinary_reference/reference_store.py` and `protected_metadata.py` for this
author. Root separately owns the controller, native author owns delta native/
worker, and the independent reviewer owns source clearance. No experiment,
import, native command, owner operation, package or Git mutation was run here.

Current source hashes before independent review:

- `reference_store.py`:
  `4c491692a0babe752671b2b307a9597fcc6d129e79f43eaee665366ae0aaa136`.
- `protected_metadata.py`:
  `6fac21a5366576618bee617205f5a0497a91b3d1cf176ebe97323711d88b4d7a`.

The implemented reference path is `open_for_owner` → `reserve_reference` →
`bind_reference_inputs` → private `_commit_reference` → `load_reference`.
Reservation selection has exact `source_context_root`, `{name,export_id}`
targets, and `project_selection`, `bundle_manifest`, `artifact_report` pins.
Binding returns immutable `NativeMatchInputs` with operation/snapshot identity
and final request/inventory/replay/report/supervision paths; request, inventory
and warrant metadata are written once before native work. Root's actual live
commit object contains exactly `bound_report,snapshot,supervision,report_raw`.
It must match final files, the initial grant, current complete private warrants
and the clean actual controller event. Errors expose exact-ID recovery through
`ReferenceCommitUnknown` / `ReferenceCommittedError` and `.report`.

Protected reopening uses its own body-free syntax/current-warrant loader. It
does not fabricate the live binder's private request or infer singleton/graph
semantics anew from metadata. The live commit still binds the real request and
V2 report; the trusted protected record then authenticates their retained IDs.
Current context need not equal historical registration context, but all fixed
basis/private output warrants must still hold. Snapshot integrity and original
metadata remain checked; original proof-bearing request is not read on load.

Root selected4GiB store/128 operations, with kind-specific finite file trees and
768MiB reference/128MiB delta operation caps. The reference path includes final
snapshot/input/report bytes and staged record in that same envelope; supervisor
logs are at `operation/supervision/{stdout,stderr}.txt`, with optional bounded
`FAILURE.json`. No duplicate large commit copy or path-moving snapshot occurs.

Generated-delta schemas/record-field constants and the separately pinned native
plan constructor are present, but generated reserve/commit/load are **not yet
implemented**. Do not present those declarations as an operational delta store.
They remain the next source integration task after the working reference path
has a source review. Both new files pass AST-only parsing; runtime behavior is
unqualified. Existing protected stores and frozen inputs remain unchanged.

### Generated-delta implementation added under the next root selection

Root then explicitly commissioned generated reserve/bind/private commit/load in
the same assigned store. Current `reference_store.py` SHA-256 is
`ff10bedc7fc88ecaee4dedc19a286c4cb37b69d15dc3f1907bc172d4737a67ba`;
`protected_metadata.py` remains `6fac21a5...`. Source-only, AST parse PASS;
independent changed-boundary review is pending, with no execution claim.

Exact controller seam:

1. `load_delta(id,current_context,check)` returns immutable `DeltaView`: its
   reference, latest delta ID/name/key, generated directories/frontier/plan,
   record bytes, generated artifact total and store/support bindings. Its
   `import_directories` contains only generated directories for an explicit-map
   consumer; original hash directories are not advertised as `LEAN_PATH` roots.
2. `reserve_delta(reference,parent_or_None,{source_context_root,targets},check,
   deadline=...)` requires sorted32-target metadata and the current same-base
   protected chain. It fixes reference/parent IDs and materialization key in the
   reservation before any final-path plan exists.
3. `prepare_delta_plan(grant,check)` writes the separate generated/reference
   plans once and returns `NativeDeltaPlan` (module name text, exact plan paths/
   bytes/hash, five-part output stem, report and supervision paths).
4. Closure uses that actual plan digest. `bind_delta_inputs(grant,request_raw,
   inventory_raw,check)` checks the exact current-warrant/all-new partition,
   writes final request/inventory once and returns `NativeDeltaInputs`.
5. `_commit_delta(grant,{report_raw,report,supervision},check)` consumes the
   controller's actual clean three-phase event. Exact new inventories/counts,
   no matched units, unchanged inputs/base/parent, five hashed output parts and
   all eight retained event files precede record-last publication. No saved
   pending/final report can register a module independently.

New metadata preserves original reference512MiB versus generated256MiB chain
artifact bounds,32 modules/1024 units/16384 names,4MiB chain-record/plan bounds,
and32-unit/4MiB new requests. Since all individual report/log/plan maxima cannot
jointly fit32MiB metadata, input binding explicitly reserves the known exact
input sizes plus23MiB future report/pending/trace/supervision/log/failure/staged
record headroom and a close marker. It refuses before native work if that does
not fit, rather than discovering excess after a failed partial write.

Both module-level and store-bound materialization-key helpers are exposed.
All-covered exact target reuse remains a controller fast path before reservation.
Commit errors retain the original classes but now report `kind` and the proper
`reference_id` or `delta_id` for exact lookup. Delta publication never changes
the acceptance catalog. Native/controller authors received these exact APIs;
the independent reviewer is reviewing only the new boundary, not repeating the
already cleared original interpretation argument or running another campaign.

## Public package integration seam (source-only proposal)

The selected reusable ancestor must be
`experiments/v5-local-checks/ordinary-preview-assembly-01/package`, not the older
anchor04 package. Its approved-project `library_extraction.py` exposes
`selected_project`, which the new snapshot/registration path requires. The
preview ancestor also preserves the current peer/discovery functionality.
Exact ancestor pins read for this proposal:

- PROFILE: `ab04e72440bcd09381a81d4b721d1103fa2e62bc260fa6c0434e6c568419016f`.
- ASSEMBLY: `6e09d2b255d8321bd522291276e03f10729cbc4f57536a57b29b63ab67a528bc`.
- owner: `2d4de791436d86810ef192e6a776cdbc0b45076f8c0bc75458e35e005cb6cbbe`.
- profile: `8f690bd50b5ded03da309ad7c42850954aac80d889650442cbba3110028ee48d`.

Minimal file delta: replace only `owner.py` and `profile.py`; add the following
15 payloads. This preserves132 old payloads and makes149 total payloads before
PROFILE/assembly metadata, with121 files in the existing profile schema. These
counts describe the proposal, not an assembled or adopted product.

| Logical package path | Selected source or retained artifact |
|---|---|
| `reference/baseline_bundle.py` | `ordinary_baseline/baseline_bundle.py` |
| `reference/baseline_snapshot.py` | `ordinary_baseline/baseline_snapshot.py` |
| `reference/snapshot_reopen.py` | `ordinary_baseline/snapshot_reopen.py` |
| `reference/reference_request.py` | `ordinary_baseline/reference_request.py` |
| `reference/reference_report.py` | `ordinary_baseline/reference_report02.py` (V2 alias) |
| `reference/protected_metadata.py` | `ordinary_reference/protected_metadata.py` |
| `reference/reference_store.py` | `ordinary_reference/reference_store.py` |
| `reference/reference_closure.py` | `ordinary_reference/reference_closure.py` |
| `reference/reference_registration.py` | `ordinary_reference/reference_registration.py` |
| `reference/reference_module.py` | `ordinary_reference/reference_module.py` |
| `reference/reference_match_worker.py` | `ordinary_reference/reference_match_worker.py` |
| `reference/reference_module_worker.py` | `ordinary_reference/reference_module_worker.py` |
| `reference/ReferenceModule.lean` | selected native source, no executable/codegen required |
| `reference/OrdinaryReferenceBase05.exe` | successful retained matcher05, SHA `918aebc5f3f20f305d7c684ff6c1200c164c1503712eaa2e3657fce697bd4aab` |
| `authoring/helpers/BaselineArtifactCore04.olean` | successful retained core04, SHA `574ae10f246dac8d720df80e6c82fadfd84b5d713f955e36bd4d566d9f7d7088` |

All source rows are under `software/v5/`; binaries are the exact successful
build04/build05 artifacts already independently audited. The native source's
current compile-only qualification is separately root-owned. No new delta
executable is needed: the selected worker runs the pinned source under Lean.

Loader: retain the same installation manifest, CORE/AUTHOR/SUPPORT paths and
schema. Pin every payload before importing anything, add an exact `reference/`
census and anti-preload names for the ten imported reference modules, then load
them in the table's first-ten-row dependency order after existing AUTHOR modules.
Require every loaded `__file__` to equal its selected logical path; expose
registration/module through the existing returned namespace. Workers are pinned
scripts, not imported by the loader. Preserve the14 old helper modules and add
only the required core04 `.olean`; do not treat arbitrary helper-directory files
as selected support. Root has already corrected the descriptor to select the
seven actual mathematical helper modules and reject duplicate filenames, so
its64-row bound is no longer exceeded by all70 unrelated authoring parts.

Owner facade: add `register-reference` and `export-reference-delta` inside the
existing owner/custody opening and lock lifetime, not a second authority API.
Registration takes an explicit current parent root, exact selected targets,
approved-project selection, inert artifact locator report, bundle manifest and
bundle directory; each selected input file has its own exact digest. It never
takes a saved correspondence report. Delta takes the current parent root,
reference ID, optional parent-delta ID and exact targets. Protected store code
owns their retained output paths: neither operation accepts an arbitrary output
directory. Both use the original allocation and controller budgets, with1MiB
native log caps and unchanged current-warrant checks. A later authoring adapter
must consume an explicit import artifact map; hash-based original snapshot
directories must never be advertised as valid ordinary `LEAN_PATH` roots.

This review ran no imports, tests, owner operations, package assembly or native
commands. Root retains selection and public-facade ownership; current successful
and failed predecessor evidence remains unchanged.

### Helper compatibility check changes the package proposal

Root requested exact helper comparison before selecting execution. All five
baseline build04 shared `.olean` files differ from the newer preview package's
authoring helpers: `OriginalExpr`, `OriginalDecl`, `CheckedExtension`,
`BootstrapSupport`, `OrdinaryExport`. All five `OwnerRebind` parts are identical
to the newer helper set used in ReferenceModule build01. Thus the15-addition
proposal above does **not** reproduce that build's exact selected helper bytes.
No compatibility is inferred merely from shared module names or source roles.

The cheapest exact-reuse correction is a dedicated `reference/helpers/` containing
the six build04 `.olean` files (the five listed modules and
`BaselineArtifactCore04`) and the five exact modern `OwnerRebind` parts. Ordinary
authoring retains its unchanged helper path. The reference controller must use
only the dedicated directory, not add both conflicting search roots. That yields
25 added payloads, not15:159 total and131 profile files, with132 unchanged and
the same two changed entry/loader files. It requires explicit root adoption and
controller/support-descriptor wiring before the fresh package can be used.

The source-only profile/assembler/selector assignment is now root-authorized
under fresh `software/v5/ordinary_reference_package`; no copying, assembly,
import, native command or owner operation has been performed by this agent.

### Adopted package draft: distinct exact helper profile and actual intake

Root adopts the dedicated11-file helper directory and adds the existing strict
`baseline_intake.py` as a justified public workflow dependency. Its alias loads
immediately after `baseline_bundle`. The current draft therefore has160 payloads
(132 unchanged, two changed,26 added), with132 profile files. These supersede
the preceding proposal counts; none is an executed assembly result.

The new loader leaves the descriptor's existing author helper paths unchanged.
It returns both `loaded.profile` for ordinary authoring and
`loaded.reference_profile`, the exact same `G.AuthoringProfile` class, same full
file pins and author-worker identity, but only `reference/helpers` as its helper
path. Both profiles are verified. It also returns `baseline_intake`,
`reference_registration` and `reference_module` for the root-owned owner facade.
Reference source aliases are pre-pinned/anti-preload checked and loaded only
after the unchanged authoring/support modules. Exact V2 report alias is checked.

New source-only files and current pre-review pins:

- `ordinary_reference_package/profile.py`:
  `a4e0b22c3f789135c8e450b4b61275d51494b490132f077624078e0d8fe70bf4`.
- `ordinary_reference_package/assemble.py`:
  `73adcf89e97dac0b460a49733692872812eef9617475fa4215acb680c53bcbeb`.
- `ordinary_reference_package/select_assembly.py`:
  `5e63e5936c31f0143a80f363f5b1770f4a4dcce7972c3fcf2768352d6e0b5e12`.

Assembly inventories the exact preview package and successful retained core04/
matcher05 evidence, keeps all160 payload identities, checks retained shared
support equality, copies into a fresh package and commits PROFILE last. The
selector requires the reviewed assembler digest and a complete16-source
payload-map digest, then pins20 source snapshots and at most256 runtime files.
No new package code is imported by selection/assembly; neither opens an owner
or native installation. Those are later independently selected public calls.
Its proposed finite outer envelope is90wall/50CPU/512MiB/two processes; this is
source specification, not launch authority or a consumed allowance.

AST-only parsing passed for all three files. One diagnostic-print spelling in
the first shell parse command raised a NameError after parsing; the corrected
AST-only command then completed normally. No test, source import, selector,
copy, assembly, compiler, Lean import or owner operation ran here. An independent
review has the source pins. The normal-source authoring seam remains under its
separate author and may require coherent additions before any package is frozen;
no broad package or runtime claim follows from the current drafts.

### Normal-source authoring package extension (still source-only)

Root next selects normal-source contribution over protected references. The
unused package drafts now include `reference_authoring.py`,
`reference_author_worker.py`, `ReferenceEnvironment.lean`, `ReferenceSource.lean`
and a required compiled `reference/helpers/ReferenceEnvironment.olean`.
`loaded.reference_authoring` shares the previously loaded core and registry.
The existing ordinary-authoring profile and peer/discovery files remain unchanged.
The profile's separate reference helper directory now has12 exact files.

Updated total:165 payloads (132 unchanged, two changed,31 added),137 profile
files,20 fresh source payloads and24 source snapshots in a prospective selection.
Only a future actual successful environment-helper artifact can satisfy this
package: no placeholder helper, name equivalence or source text is substituted.

The native author specifies
`ordinary-reference-source-build-01/build/objects/{ReferenceEnvironment,ReferenceSource}.olean`
and `DMKN_ORDINARY_REFERENCE_SOURCE_BUILD_V1`, status
`COMPILED_CANDIDATES_NOT_INSTALLED_OR_EXECUTED`. The assembler requires three
explicit root-reviewed successful BUILD/RESULT/selection digests, clean actual
two-command closure, exact two-output metadata, source-pin equality for both
shipped native sources and byte equality for all11 prior retained helper parts.
It packages only `ReferenceEnvironment.olean`; `ReferenceSource.olean` is a
separate syntax-qualification output, not required by the source-running worker.
No successful source-build pins existed at this package-edit stage and none is
invented. The source-only selector cannot infer authority from a proposed build.

Current post-extension source pins:

- profile: `43a061ac8275a7ab0669d1242efd4525fc6622902f2354bd5db4c11a16fefbd3`.
- assembler: `9245bdd2f257858b519f8384f52245048ea505a7ebb7033e8f3d2fd1e8cc28d6`.
- selector: `92554210128bb243080ff9cf074c1c598e0b03d83fe67dd11fcba07e321d58a3`.

All three passed AST-only parsing. Independent changed-boundary review received
these pins; no package code import, selector, assembly, compiler, native source
execution, owner call or mathematical acceptance occurred in this workstream.
Root owns the new `contribute-reference` CLI and controller; the native author
owns source worker/exporter/helper files. Those files were not edited here.

### Source02 provenance successor and eight-call public workflow draft

The first source build failed its second compiler command, after successfully
producing `ReferenceEnvironment.olean`. It remains failed. Root adopted the
independently audited one-command `ordinary-reference-source-continuation-01`:
BUILD `f35a2fd9abb6e45c735b0cf60d50c0b0115d90e25e2b3eb0e21d8762fb49c835`,
RESULT `90f9f8d28edd56aef6ff5a43da5718b557beff95cd71205f8d194df534126265`,
selection `8c81e10c81c6c8fe9e392294eb1425f35ae2291fa24e157f3d98939fd15f03ba`.
The unused assembler was changed before execution to package repaired Source02
under logical `reference/ReferenceSource.lean`, require the one actual output,
and retain exact failed01 RESULT/selection/BUILD-FAILURE/INPUTS provenance.
It explicitly requires the Environment command's exit0 and Source command's
exit1, clean failed-job closure, original Environment source identity and
retained output `a082feb7bfcf3b28199c4438baafc11e3e00b4ad37af07e3507473e1e452c698`.
Only the Environment output is shipped; Source02 output is compilation evidence.

Independent prelaunch review found that the initial assembler's owner JSON
parser rejected finite fractional durations in pinned operational receipts.
The narrow repair retains strict integer-only parsing for PROFILE/INSTALLATION,
and parses exact hash-bound diagnostics with duplicate-key/nonfinite rejection.
Final independently cleared assembler:
`c4628e67b8bf5109fedb839cf0815c874d1febc224106dc3dae496756754ef7f`.
Profile and selector remain `43a061ac...` and `92554210...`. Root subsequently
reports completed file-only assembly01; actual adoption/map review is root's
separate responsibility. These used source files are now frozen.

Source-only public workflow and selector are newly authored:

- `ordinary_reference_package/public_workflow.py`:
  `6809cc8c33ff2d5921adfdaabbddcfdc77b0fcad530bee604a85ffd769edd832`.
- `ordinary_reference_package/select_public_workflow.py`:
  `a345b30accf7efd1740b6697ca5036d726fecc1cbee1ec6c595235df7370a1f5`.

Both pass AST-only parsing and are awaiting independent source review. No
selector, public call, compilation, fixture rebuild or owner operation was
executed by this agent. The workflow uses only the frozen diagnostic/supervision
helper `relocated_smoke.py` (`aaba6e2e...`) and actual public owner subprocesses.
It does not create synthetic accepted state or invoke product Python APIs.

The selected calls, in order, are actual fresh initialization, six-unit baseline
intake, original-library registration, contribution A, new-only delta A,
contribution B through that delta, one semantic refusal, and public status.
A uses original scoped `lowF` and the registered `[simp] flip_low`; its second
result establishes general flip involution. B actually uses that returned
involution to prove injectivity, then original `flip_low` and `lowF` for a
concrete high-fiber theorem. Evidence identities come from actual returned
portable proofs. New proofs must have actual native admission records, exact
dependency imports and constant occurrences, with no original-unit redeclaration.
The delta contains only A's new units and creates no catalog acceptance itself.

The additional refusal is specifically `reference_false : False := by sorry`.
It must first compile successfully with all five bound artifact parts; a parser
or unavailable-import error is not a pass. The exporter must report the exact
`sorryAx` outside-approved-frontier refusal before candidate/admission creation.
Expected exception cleanup may request Job termination: it is recorded rather
than mislabeled a voluntary exit. Final accounting, reaping, joined threads,
closed Job, no cleanup errors and zero active processes remain necessary.
The final public status must show exactly basis/intake/A/B roots and the latest
accepted context. This checks the new compiler-output-versus-authority seam,
not a repeat of the earlier negative suite.

One parent envelope owns all eight calls:540wall/420CPU/1536MiB; the proposed
outer envelope is600wall/480CPU/1792MiB/eight processes. Per-call reservations
come only from remaining parent resources; uncertain CPU charges the full
reservation and stops. Replies and partial possible acceptance are saved before
assertions, with no automatic retry. Exactly one protected snapshot copy occurs
inside actual registration, not an extra harness copy. The named Lean runtime
is still a disclosed immutability premise; the product hashes the full snapshot
at actual registration. This controlled fixture cannot justify general library
support, useful growth, a speedup or globally deployable final v5.

Latest user steering: finish this selected workflow, then direct creative
analysis toward reasonable useful-growth justification before expanding the
architecture. No additional wrapper, diagnostic campaign or certificate work
is commissioned by this checkpoint.

Prelaunch targeted review fixes: root requires complete child closure before
replacing a call's conservative CPU reservation with an observed finite value
(zero active processes, at least one attached process, direct child reaped).
Otherwise the full reservation remains charged and accounting stays incomplete.
Native source inspection also found that `CheckedExtension.requireName` runs
before the dynamic boundary callback: the genuine `sorryAx` diagnostic is
`ORDINARY_EXTENSION SORRY_REFERENCE`, not the later outside-frontier diagnostic
predicted above. The workflow now requires that actual earlier semantic guard,
still after successful source compilation and before admission. Revised workflow
SHA256 `32b331c8e853c38e328eaf6cd8a96c349b57b8b4d8ad8b72e81a2f48d078d300`;
selector remains `a345b30a...`. AST-only parse passes; independent review has
the exact successor, and no operation was executed here.
