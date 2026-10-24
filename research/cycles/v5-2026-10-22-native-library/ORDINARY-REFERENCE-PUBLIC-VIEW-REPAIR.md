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
