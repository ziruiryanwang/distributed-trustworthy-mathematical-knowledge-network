# Bounded base-index projection: source contract

2026-10-20, core_growth. Root-adopted design inputs:
`PROFILE-INTEROPERABILITY-SEAM.md` (`6d931c96`) and independent review (`5e13cc3d`).
This contract selects no implementation, runtime or build. All paths are under
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Capability and non-goals

An owner projects an explicit finite list of held exports into the common base
index. A later ordinary HTTP or advertised service selects that retained base
index while serving the **original** module/packet custody. A default-profile
consumer can discover the exact same export without knowing its specialist
profile. Keep namespace validation and mathematical admission unchanged.

Prepare and serve are separate operations. There is no corpus scan, automatic
catch-up, dual serving, profile catalogue, global registry, new network protocol,
remote extraction code, proof copying or mathematical issuer construction.

## New helper and ownership

New logical module: `client.base_projection`, with public `prepare(context)`
returning a report, `main(context)` returning an exit code, and
`open_view(workspace, selector)` returning one closable `ProjectionView` whose
`index` is the real existing `discovery_store.Store` (not an adapter proxy).

The target is exactly `workspace.root / "base-projection-index"`. No caller path,
alternate namespace or alternate adapter is accepted. Resolve it using existing
ordinary/non-reparse path checks. Use `ModuleExportAdapter(C, foundation, policy)`
with no optional discovery profile, deriving foundation/policy from the actual
original module store and checking agreement with the workspace adapter.

Keep the source workspace open once under its existing exclusive lock. Refuse
closed/poisoned workspaces, missing lock/database, a live client, any reserved
grants, or an existing projection borrow. Acquire an explicit per-workspace borrow
token before opening the target; only its matching handle can release it. No
workspace adapter/index is replaced. Calls are serialized by the trusted owner;
this is not protection against arbitrary hostile code in the same process.

The target store is always closed explicitly **before** closing the workspace.
Constructor failure releases an unused borrow after its own cleanup. A close
failure remains a failure, with best-effort target/database cleanup before original
workspace cleanup; do not report a released/clean target solely because the
workspace's predecessor closer returned. Preserve all failed files; no automatic
delete, repair, index migration or retry.

## Materialization request and finite work

`prepare(context)` accepts exactly:

```text
schema: DMKN_V5_BASE_PROJECTION_PREPARE_V1
mode, workspace_path, workspace_config: existing owner-selected workspace fields
create: bool                       # explicit fresh target versus exact reopen
index_limits: existing Store.LIMITS # immutable target quota config
exports: [{module_id, relative_name, group_index}, ...]
limits: {export_bytes, wall_seconds}
```

Support the existing closed workspace modes; no supplied class/module/callback.
The existing installed `run` mechanism can invoke a tiny trusted owner entry
`from client.base_projection import main`. Its current launch contract still
requires `runtime_mode` atomic/aggregate and materializes runtime configuration,
but this helper creates no mathematical owner or native/proof process. Do not add
a new built-in command merely to avoid that inert existing configuration step.

Validate all closed request fields and the complete explicit locator list before
opening/creating target state. Require 1..64 distinct export IDs; valid exact names,
module digests and group indices 0..4095; selection canonical bytes <=64 KiB.
Reject malformed/oversized selection before target writes. Apply the existing
workspace/install/run/source disjointness rules. Report files are fresh fixed
names under `context.location_workspace`, never inside immutable installation.

Use the existing target Store limits, not larger implicit defaults. Require
`export_bytes` in [16 MiB,64 MiB] and finite `wall_seconds` in (0,300]. The active
deadline is the earlier of this duration and `context.deadline - 5 seconds`.
Check before/after each synchronous step; existing Store primitive ceilings and
the original enclosing Job remain the actual hard resource bounds. No timeout
check claims to preempt synchronous SQLite/hash work.

For each locator, in supplied order:

1. Reserve one codec maximum (16 MiB) from the remaining export-byte allowance
   before the custody read. Count the attempted item before it can fail.
2. Call the original `workspace.modules.get_group(module,name,group_index)`;
   encode its opening with the default adapter. Settle the reservation to the
   actual encoded export length on success; retain it on an unmeasured read/
   encoding failure. This is a conservative submitted-export/read allowance,
   not measured physical disk traffic or peak RAM. Process one export at a time.
3. Call target `Store.admit(raw, expected_id=codec.export_id(module,name))`.
   This re-extracts features and commits ordinary base index records. Never copy
   specialist feature claims or relabel a specialist record.
4. Record the returned `new`, record ID and snapshot ID as one acknowledged item.
   Stop on the first failure; do not skip it or retry inside the batch.

Capture constructor and each admission's available `Store.work` counters before
the next admission resets them, including counters from the failing call when
available. Sum them separately from observed inclusive controller CPU/wall time.
Any unavailable constructor/failure counters are marked unknown; the parent Job's
measured/charged consumption is retained. No count is a total proof-cost metric.

## Prefix, uncertainty and reconciliation

The <=64 KiB final report includes selection hash/ordered export IDs, source
namespace, target namespace/path/config, initial target snapshot/cut when known,
attempted count, acknowledged prefix, last acknowledged snapshot, byte charges,
known counters/unknowns, terminal error and both cleanup outcomes.

- Invalid preflight: no projection writes or target opening.
- Failure before entering the current `admit`: report the prior acknowledged
  prefix; the current item is not newly admitted by this attempt.
- Exception/interrupt after entering `admit`: conservatively mark the current
  item `COMMIT_OUTCOME_UNKNOWN`, even if a particular error normally rolls back.
  Do not equate the last acknowledged snapshot with the actual latest target.
- Full success: read and verify actual latest snapshot, require it matches the
  last returned snapshot, and report its exact `snapshot_id` and `local_cut`.
  PASS additionally requires target/workspace closure and final report success.

No new durable per-item ledger is needed. If hard termination or report failure
prevents a terminal report, the batch outcome is UNKNOWN, not zero work or rollback;
the original pinned launch request identifies its finite input. Retained target
transactions may already exist. A separately authorized later invocation can
reproject the same explicit list with `create=False`; ordinary idempotent admission
then confirms the exact records under a fresh finite allowance. Preserve the old
failure and charges. An unusable partially created target is refused, not silently
deleted or reconstructed. Broader damaged-store repair is not selected here.

## Closed service V2 selection; preserve V1

Add these explicit outer parameter schemas, leaving the V1 schema/constants,
closed field sets, default behavior and old report shapes unchanged:

- HTTP: `DMKN_V5_WORKSPACE_SERVICE_V2` = exact V1 fields plus `index_view`.
- Advertised: `DMKN_V5_ADVERTISED_WORKSPACE_SERVICE_V2` = exact advertised V1
  fields plus `index_view`.

The new `index_view` has exactly:

```text
schema: DMKN_V5_BASE_PROJECTION_VIEW_V1
index_limits: existing exact target Store.LIMITS
expected_snapshot_id: exact retained latest snapshot hash
```

V2 requires this selector; V1 refuses it. The fixed target path is derived from
the opened workspace, not the selector. `open_view` only reopens existing state
and requires the requested hash equals target `status().latest` and the verified
latest snapshot. Its `local_cut` is taken from that snapshot, not a caller claim.
Refuse a stale expected cut before starting listeners or location. Never select
an old retained snapshot while the existing offer handler serves a newer latest.

The provider gets `view.index`, `workspace.modules`, and `workspace.packets`;
all custody objects are the originals. Exactly one view is served per invocation.
The HTTP and location namespace both derive from `view.index.namespace`. V2
READY/result reports use corresponding V2 report schemas and include selected
view/cut, source workspace namespace, target-close outcome, and explicit coverage:
`OWNER_SELECTED_RETAINED_EXPORTS_NOT_ALL_SOURCE_PUBLICATIONS`. No assumption says
the target is synchronized with subsequent source publications or that every
requested export survived a previous incomplete batch. Serving a deliberately
chosen partial cut is allowed; it is never reported as complete source coverage.

During service the view has no materialization calls. Check latest still equals
the selected snapshot on normal final reporting. Stop/drain location and HTTP
before closing the projection, then close the workspace. All existing TLS, egress,
route/lifetime/health and cleanup reservations remain. Caller route feature hashes
must be compiled with the default adapter: an opaque hash cannot prove its own
namespace provenance. Derive route keys from the actual selected namespace;
do not claim to verify unprovided feature specs. Source-only specialist routes
are not automatically copied or advertised as base routes.

## Dispatcher and proxy changes that must not be omitted

`distribution_coherent.distribution.builtin_parameters` currently checks and then
overwrites `schema` with `ENTRY_SCHEMAS[command]`. The fresh successor must keep
the original V1 defaults, but accept **only the matching explicit V2** for `serve`
or `serve-advertised` and preserve that selected schema. Unknown/cross-command
schemas fail; do not silently downgrade V2. Keep existing wrapper bytes/command
names and `runtime_mode=None` for serving. The advertised installation root stays
launcher-injected/reserved exactly as before.

`serve_advertised._parameters` currently builds an HTTP proxy and overwrites its
schema with `H.SCHEMA`. In the V2 branch pass the exact HTTP V2 schema and retain
the validated `index_view`; in V1 retain the old proxy behavior and fields. This
requires changes in both service files and the distribution dispatcher, not just
a helper that no installed public command can reach.

## Exact proposed source scope

Under fresh `software/v5/base_projection/` only:

| File | Logical destination / predecessor |
|---|---|
| `client/base_projection.py` | New `v5/client/base_projection.py`; prepare/borrow/close helper |
| `client/serve_workspace.py` | Replace logical service; preserve predecessor `89723f2e8a03abcaa709560f6d991ffc5d2bb349ef6cb662aadad7589a73936c` |
| `client/serve_advertised.py` | Replace logical advertised service; preserve predecessor `80d6c0746eca23398cfe735af5d8de1076eb3725439414cce68de743c518a7ed` |
| `distribution.py` | Fresh distribution successor from `6d6f541112f5f25493a67da6a67065535d8a5e8347456004c89435cbfdc14ee6`; V2 allowlist, required helper source and concise docs |

Add the new helper to the built distribution's required source set. Do not edit
workspace/admission/checker/index algorithms or prior used sources. Root chooses
the exact map successor and runtime only after source review.

Focused subsequent controls: real held-opening/base extraction with unchanged
export ID and source index; wrong namespace/config/stale latest refusal; duplicate
idempotence; quota refusal/uncertain commit prefix; serialized borrow and both
cleanup paths; V1 parameter/report preservation; V2 installed parameter/proxy
selection and provider/location namespace binding. Use inert service components
where appropriate; no new theorem/proof or broad repeated network campaign.
