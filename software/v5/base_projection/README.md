# Base-index projection

This optional helper lets a node with a specialist discovery profile expose a
selected part of its held mathematics to ordinary base-profile search. It does
not weaken namespace checking or add a mathematical trust mode.

For example, a node may maintain a conclusion-fingerprint index for specialized
queries. Another node cannot derive arbitrary specialist features from the base
profile. The owner can therefore re-index selected held exports using the base
adapter, then serve that base index together with its original module and packet
custody. The export identifiers are unchanged. No theorem proof is copied or
rechecked merely to create this index.

Use this only when cross-profile discovery is needed. A base-profile workspace
can already serve its original index; it need not maintain a duplicate index.

## Two separate operations

1. **Prepare a bounded projection.** The owner supplies exact held export locators
   and finite quotas. The helper reads each selected opening and calls the existing
   base adapter and real index admission code. It stops at the first failure.
2. **Serve a retained cut.** The owner supplies the exact latest snapshot hash from
   a successful preparation or explicit later inspection/reconciliation. A V2
   service reopens that cut and serves its selected index with the original
   workspace's custody. Serving never prepares or catches up a projection.

The sole target path is `workspace.root / "base-projection-index"`. It is metadata
under the existing exclusively locked workspace, not a second workspace or an
independent copy of packet custody. The original adapter and index are unchanged.
The target has independent immutable quotas; do not edit or automatically rebuild
it when reopening fails.

## Preparation API

The trusted owner entry can contain:

```python
from client.base_projection import main
```

Invoke it using the installed `run` contract, with these exact parameters:

```text
schema: DMKN_V5_BASE_PROJECTION_PREPARE_V1
mode: atomic | mixed | evidence | staged | validated
workspace_path: existing absolute workspace path
workspace_config: that workspace's exact original configuration
create: true for a new projection; false for exact reopening
index_limits: all six existing Store limits
exports:
  - module_id: exact 64-character lowercase digest
    relative_name: codec-native exact name, for example [["s", "result"]]
    group_index: exact containing group, 0..4095
limits:
  export_bytes: integer from 16777216 through 67108864
  wall_seconds: finite number greater than 0 and at most 300
```

The existing `run` launcher still requires its `atomic` or `aggregate`
`runtime_mode` metadata and materializes its runtime configuration. Preparation
does not construct an issuer or launch a native/proof process. No new built-in
command, arbitrary adapter, caller-selected target path or input callback is
accepted. The run's existing hard process containment remains necessary.

There must be 1–64 distinct export IDs, in the requested order, with the canonical
locator list at most 64 KiB. The exact Store quota keys are `max_objects`,
`max_postings`, `max_features`, `max_snapshots`, `max_logical_bytes` and
`max_db_pages`; their existing ranges and exact-config reopening rules apply.
The source workspace must be disjoint from installation, run and source roots.

Each attempted export reserves 16 MiB before custody reading. Successful encoding
settles that reservation to actual submitted export length. Unmeasured failed
reading/encoding retains the whole reservation. Consequently an allowance may
refuse another item even if its eventual encoded length would have been small.
This deliberately conservative allowance is not measured disk traffic or RAM.
One export is processed at a time; there is no corpus scan.

The active deadline is the earlier of the requested duration and the original
outer deadline minus five seconds. Checks surround synchronous work but cannot
preempt a running SQLite/hash operation; existing Store primitive bounds and the
original enclosing Job provide the hard ceiling.

## Outcomes and recovery

`prepare(context)` returns and saves `base-projection-result.json` in the run's
location workspace. `main(context)` returns zero only for `status: PASS`.
Preflight errors raise before opening the source or target. A terminal report
has at most 64 KiB and records:

- The selection hash and ordered export IDs, source namespace and target config.
- `initial`, `attempted`, `acknowledged`, and `last_acknowledged_snapshot`.
- `outcome`, `current_export_id`, conservative `submitted_export_bytes`, and errors.
- Constructor/admit `store_work` samples and known totals, with unknown samples
  explicit; observed inclusive process CPU/wall are separate and not additive.
- `cleanup.projection_closed`, `cleanup.workspace_closed`, and cleanup errors.

`ALL_ACKNOWLEDGED` records a fully acknowledged list and authenticated actual
latest `snapshot_id`/`local_cut`. PASS additionally requires clean closure and a
successful final report. `STOPPED_BEFORE_CURRENT_ADMIT` means the current item
was not newly admitted by this attempt; earlier acknowledged items may persist.
`COMMIT_OUTCOME_UNKNOWN` conservatively covers any failure after entering the
current admission. The last acknowledged snapshot is then not a claim about the
actual latest state. `ALL_ACKNOWLEDGED_CUT_UNCONFIRMED` means every item returned
an acknowledgment but final latest-cut verification did not complete; it does
not provide a final `snapshot_id` or `local_cut` and cannot be PASS.

A missing valid terminal report—because of hard termination or failed report
writing—means an unknown batch outcome, not rollback or zero work. Preserve the
original pinned input and all charges. A separate, explicitly chosen invocation
with `create: false` and the same list can use ordinary idempotent admissions to
reconcile retained records under a fresh allowance. There is no internal retry,
durable per-item ledger, deletion, repair or allowance reset. A damaged partial
target is refused for later explicit investigation.

## Selecting the projection in services

Use the explicit V2 outer schema:

- HTTP: `DMKN_V5_WORKSPACE_SERVICE_V2`.
- Advertised service: `DMKN_V5_ADVERTISED_WORKSPACE_SERVICE_V2`.

All prior fields remain, plus the following exact `index_view`:

```text
schema: DMKN_V5_BASE_PROJECTION_VIEW_V1
index_limits: the projection's exact six immutable quotas
expected_snapshot_id: the projection's exact retained latest snapshot hash
```

V1 retains its old behavior and refuses the extra field. The dispatcher preserves
only the matching explicit V2 schema, and the advertised entry forwards HTTP V2
without downgrading it. Existing wrapper commands are unchanged.

`open_view(workspace, selector)` returns a `ProjectionView`. It verifies the actual
latest snapshot before listeners start. `.index` is the original concrete Store
class; `.descriptor()` returns copied view/cut data; `.assert_current()` refuses
a changed cut; `.close()` is idempotent on success and returns `{"closed": true}`.
Close errors remain errors even if fallback cleanup closes the database.

Only one projection borrow may exist. The source must have no active client or
reserved grants and must not be poisoned or closed. A trusted owner serializes
calls and must not reserve clients, mutate the index, or close the workspace
during a borrow. This is not isolation from malicious same-process owner code.
Stop and drain transports before closing the projection, then the workspace.

HTTP and location namespaces derive from the selected base index. Compile route
features with the base adapter: an opaque feature hash cannot demonstrate its
own profile provenance. Specialist routes are not copied automatically.

## Exact assurance boundary

Successful projection establishes structural/hash-bound index records re-extracted
from the selected held openings under the base adapter. It does not establish
mathematical truth, custody certification, global search completeness, benefit
or continued availability. Those retain their original separate verification and
service obligations. All reports explicitly set `mathematical_acceptance: false`.

Coverage is always
`OWNER_SELECTED_RETAINED_EXPORTS_NOT_ALL_SOURCE_PUBLICATIONS`. A selected partial
cut is allowed. Later source publications do not automatically enter this index.
Work scales with the bounded selected exports and their existing index primitives,
not an enumeration of the full source corpus; no claim makes individual large
openings or feature extraction constant-time.

This fresh source is implementation work awaiting the separately selected focused
controls and integration. It is not a completed v5 release or a new proof result.
