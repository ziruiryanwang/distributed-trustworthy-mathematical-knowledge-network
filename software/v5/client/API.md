# Finite mathematical-commons workspace client

This client connects persistent mathematical data to one finite, supervised
agent operation: discover a candidate, acquire it, obtain a live mathematical
warrant, import selected semantics, author a contribution and publish its data.
The agent chooses its research. The client does not assign tasks or decide
whether mathematics is useful.

This is the current **I-only frontier lane**, not the complete v5 release.
It accepts the fixed I receipt relation and ordinary native-checked extensions
over that frontier. It does not mint aggregate certificates or provide an
economical way to advance every long native extension chain. Tag-1 aggregate
claims are refused, not silently downgraded. The full scalable-frontier and
public-release obligations remain open.

## 1. Three different things

| Object | Meaning | Survives reopening? |
|---|---|---|
| Stored packet, module opening or index record | Untrusted bytes with structural/content bindings | Yes, subject to quotas and storage health |
| `LiveWarrant` | Reference to an actual handle of this live client and its exact verifier | No |
| Saved report or publication outcome | Historical operational evidence, not mathematical authority | Yes |

Neither an index hit, successful storage, successful Lean source preparation nor
a JSON report permits mathematical use. Actual `admit_receipt`, `admit_local`
or `acquire` must return a live warrant. Closing or failing the operation revokes
its authority. Cached reuse is only within that same live operation and rechecks
the original issuer, exact evidence, profile and journal.

## 2. Supported environment and ownership

The caller is trusted local owner code on Windows. Run it through the selected
`launch.py` / `boot.py` enclosing Windows Job launcher, or an equivalently
adopted real enclosing Job. Process flags are `-I -S -B`, without `-O`.
See [launcher plan and invocation](../../../research/cycles/v5-2026-10-16/CLIENT-LAUNCH.md)
for the exact launcher interface.
Pinned supervision, runtime and source checks remain mandatory in the concrete
owners. Resource supervision is **not a hostile-code security sandbox**.
Do not run arbitrary downloaded Python or Lean source as trusted owner code.

Load one canonical `location` package from `portable_runtime/location` before
loading `client.workspace` and its transport dependencies. The selected launcher
handles this import order; a second alias or patched class is not compatible
with the exact-type gates. Immutable installation and source snapshots must be
disjoint from writable workspace paths.

Use a persistent workspace such as `allocation_root/commons`, a sibling of the
launcher's fresh run directory. `run/work` is scratch, not the persistent
commons. Set `AdoptedLocationRuntime(..., workspace_root=workspace.root)`;
put that operation's create-only location state and evidence under
`grant.directory`. Do not use the allocation parent as the location workspace:
it also contains immutable snapshots/installation boundaries.

The workspace takes an exclusive local file lock. One workspace has at most one
outstanding grant/client; calls on the client are serialized. Parallel independent
operations require separate owner workspaces and explicit outer allocations.

### Construction sequence

```python
from client.workspace import Workspace
from admission.verifier import ReceiptVerifier
from mixed_claims.receiver import MixedDeltaVerifier
from mixed_claims.authoring import MixedOwnerPreparation
from mixed_claims.packet import Envelope

workspace = Workspace.open(commons_path, config, create=is_new_workspace)
grant = workspace.reserve(limits, outer_deadline=boot_context.deadline)

# These mappings are the trusted owner's exact, pinned installation profiles.
# Construct all owners AFTER reserve; do not reuse a previous operation's owner.
receipt = ReceiptVerifier(
    **receipt_parameters, wall_seconds=grant.remaining_seconds())
delta = MixedDeltaVerifier(
    legacy_verifier=receipt, aggregate_verifier=None,
    **delta_parameters,
    envelope=Envelope(**config["packet_envelope"]),
    output_directory=grant.directory / "delta",
    wall_seconds=grant.remaining_seconds())
preparation = MixedOwnerPreparation(
    preparation_profile,
    {**preparation_allowance, "wall_seconds": grant.remaining_seconds()},
    grant.directory / "preparation")  # optional; use None for reader-only work

client = workspace.operation(
    grant, receipt_owner=receipt, delta_owner=delta,
    preparation_owner=preparation,
    foundation_bytes=foundation_bytes,
    foundation_sha256=foundation_sha256)
```

`receipt_parameters` supplies the unchanged verifier's supervisor manifest and
hash, executable/runtime pins, fixed image/foundation/policy and finite
operations/submitted-bytes/reserved-CPU caps. `delta_parameters` supplies the
native executable and exact current source/runtime pins plus finite caps.
`preparation_profile` and its allowance are the unchanged authoring owner's
exact pinned profile; they are not supplied by a peer. Avoid duplicate keywords
for the fields shown explicitly above. The client checks these actual owners;
there is no string-based factory, mock-owner mode or saved-success loader.

The receipt and delta CPU allowances are nested within `limits["acquisition"]`
and must not be added as independent consumption. Preparation worker CPU is a
disjoint suballocation; preparation plus acquisition cannot exceed the overall
worker allowance. Controller caps must fit the original controller allowance.
All owner deadlines must be no later than `grant.deadline`. Owner construction
and loading consume the original outer Job and grant time, not a new clock.

**Ownership transfers only when `workspace.operation` succeeds.** If any owner
construction or operation construction fails, the caller still owns and must
close all successfully created owners. After transfer, close the client first,
then the workspace, in `finally` blocks. Await cancellation of an in-flight async
call before closing. Do not infer clean descendant termination from the library
alone: inspect the enclosing launcher's terminal result.

## 3. Configuration and finite grants

`Workspace.open(root, config, create=False)` requires an absolute ordinary local
directory. `create=True` requires a fresh path; reopening requires the exact
same configuration. No migration or quota reset is implicit.

Configuration has exactly these keys:

```python
{
    "schema": "DMKN_V5_CLIENT_WORKSPACE_V1",
    "wire_profile": frontier_network.custody.public_profile(),
    "module_limits": module_store_limits,
    "packet_limits": frontier_packet_store_limits,
    "index_limits": discovery_store_limits,
    "packet_envelope": dataclasses.asdict(mixed_claims.packet.Envelope()),
    "max_operations": 4096,
    "max_report_bytes": 1048576,
    "ledger_pages": 65536,
}
```

Store-limit dictionaries are the exact existing `LIMITS` schemas in
`custody/module_store.py`, `frontier_network/custody.py` and
`discovery/discovery_store.py`. A numerical maximum is not a recommended
allocation: choose limits fitting the owner's intended workload.

`reserve(limits, *, outer_deadline=None)` persists a new grant before owners are
constructed. There is no automatic retry, renewal or refund. An outer deadline
can shorten the grant and never extends it. A grant exposes `identifier`,
`started`, `deadline`, `directory`, a copied `limits`, and `remaining_seconds()`.
Mutating its original issuance fields invalidates it.

The grant's exact fields and accepted ranges are:

| Field | Range |
|---|---|
| `wall_seconds`, `controller_cpu_seconds` | 1–3600 each |
| `calls` | 1–4096 |
| `input_bytes` | 1–512 MiB |
| `worker_cpu_seconds` | 1–86400 |
| `output_bytes` | 128 MiB–2 GiB |
| `output_entries` | 32–8192 |
| `acquisition` | Exact `transport.receipt_client.LIMITS` dictionary |
| `imports` | Dictionary below |

`imports` contains `max_sources` (1–128), `max_members` (1–1024),
`max_receipts` (1–128), `max_calls` (1–65536), `submitted_bytes` (1–256 MiB)
and `data_bytes` (1–16 MiB). `max_calls` also bounds client store calls;
`data_bytes` bounds the aggregate encoded data rows expanded by
`semantic_material`. Lower component constraints still apply.

Client `input_bytes` accounts for submitted/reloaded foundation, evidence,
source, formal query/record, selected roots/export names and context data,
including repeated submissions.
It is not physical network byte accounting; control metadata is excluded.
Acquisition/search have their own prepaid requests and response-byte caps.
The operation-directory census and per-store quotas are not a hard disk sandbox.
The fresh run census does not count persistent workspace storage.

## 4. Discovery and acquisition

The remote lifecycle is deliberately explicit. `find` runs one selected finite
route plan and returns contacts, not a theorem selected by the software:

```python
found = await client.find(
    channel, formal_specs, owner_egress_policy, location_limits, search_limits,
    routes=[{
        "features": selected_query_features, "stripe": 0,
        "event_cap": 128, "peer_cap": 8, "descriptors": 4,
    }])
```

`channel` is the exact portable `ServiceLocationProcess`, with the original
grant deadline and create-only state/evidence below its directory. The caller
constructs it from the selected adoption, role pins and configuration. Query
specification syntax is the existing `discovery.module_export_adapter.compile_query`
syntax; route features must be a subset of those compiled query features.
`policy` is the actual `location.protocol.OwnerEgressPolicy`, not advisory peer
configuration. `location_limits` and `search_limits` use the unchanged
`location.workflow.LIMITS` and `discovery.search_session.LIMITS` schemas.
Route reservations collectively fit their one original location allowance.

Then the local agent chooses contacts, partitions and candidates:

```python
offer = await client.search_offer(provider)
page = await client.search_page(
    provider, snapshot_id, partition, start, page_limits)
candidate = await client.resolve(provider, selected_record)
candidate_data = client.describe_candidate(candidate)
offers = await client.packet_offers(candidate)
warrant = await client.acquire(candidate, selected_offer_entry)
description = client.describe(warrant)
```

The provider, snapshot, partition, start and selected record come from the actual
returned search data; offer entries come from the actual packet-offer response.
This excerpt intentionally leaves those local choices to the agent. It does
not prescribe a mandatory task list or pretend that the first hit is best.

Defaults and optional bounds:

- `find`: `descriptor_bytes=4096`, `descriptor_age_ms=60000`.
- `search_offer`: `max_bytes=1048576`, `max_expanded_bytes=1048576`,
  `max_age_ms=60000`.
- `search_page`: `candidates_only=True`; false uses the unchanged authenticated
  page interface. Authentication is relative to the specified finite index,
  not global mathematical coverage.
- `packet_offers`: `max_offers=4`, `max_bytes=4096`.
- `acquire`: `bodies=()`, `native_cpu_seconds=30`, `receipt_cpu_seconds=30`,
  `wall_seconds=600`, `memory_mib=1024`. A body request is
  `{"digest": digest, "max_bytes": bound}`.

There is one handoff/search/acquisition per client. It remains live until close;
the client does not close it after each result, because that would revoke the
shared verifier. Each candidate is an opaque same-query reference. No candidate
or warrant can be reconstructed from its description. Empty or exhausted search
means only that the selected search did not supply a result; `global_complete`
remains false. There is no automatic fallback, retry or new allowance.

Local alternatives:

```python
warrant = client.admit_receipt(receipt_bytes, expected_summary)
warrant = client.admit_local(module_id, packet_sha256, packet_bytes_length)
```

`admit_receipt` defaults to 30 CPU / 60 wall seconds / 1024 MiB;
`admit_local` uses `acquire`'s admission defaults. The latter reads exact retained
packet bytes and performs fresh admission. It does not trust prior publication.

## 5. Selected imports and ordinary Lean contribution

```python
material = client.semantic_material(warrant)
ready = client.import_context(
    warrants=[{"warrant": warrant, "resolutions": None}],
    selected=selected_exact_warrants,
    openings=selected_openings,
    bodies=selected_bodies)
```

`selected_exact_warrants` is a list of exact 184-byte `journal` values from the
actual warrant's `describe` output, one chosen journal per directly selected
module. `selected_openings` and `selected_bodies` are the corresponding rows
from `material`, filtered to those module IDs. Openings have `module` and
`opening`; bodies have `module`, `universes` and `expression`.
If the same exact journal has conflicting supplied representations,
`resolutions` maps that journal's bytes to `"existing"` or `"incoming"`.
Different journals for the same semantic module remain distinct warrants;
direct selection must choose explicitly. The client does not infer choices
from names or silently replace an already selected exact journal.

`semantic_material` extracts available openings and transparent body data from
the actual admitted packet. It checks an aggregate data-row bound before
expanding repeated bodies across module addresses. This is available data, not
new authority or a guarantee that every future computation's body is present.
For a bare I receipt it returns `NEED_CALLER_OR_PROVIDER_SEMANTICS`: the receipt
does not contain those semantics. Obtain the exact committed data separately.

`ready` contains an opaque `context`, `status`, `demands` and cost report. Supply
missing exact openings/bodies with:

```python
ready = client.extend_context(
    ready["context"], warrants=[], selected=[],
    openings=additional_openings, bodies=additional_bodies)
```

Each successful extension supersedes the previous context wrapper. The session
and all source warrants keep their original lifetimes. A serialized context is
never authoring authority. Only one import session is created in an operation.

With a ready context and a selected preparation owner:

```python
prepared = client.author(
    ready["context"], lean_source, exported_roots,
    cpu_seconds=cpu_cap, wall_seconds=wall_cap, memory_mib=2048)
packet = prepared["child"]["packet"]
published = client.publish(
    packet, export_names,
    retention_policy={"mode": "quota-bounded-local-custody"})
```

Check the returned status before accessing `child`; unresolved context can
return demands. `roots` uses the unchanged ordinary-source authoring format.
The prepared result contains **untrusted** packet bytes. Publication stores
structurally bound data; it does not verify a theorem. To use this new packet
mathematically, call `admit_local` with the publication intent's module, hash
and length, or have a fresh recipient acquire and admit it.

## 6. Publication, recovery and closing

Publication stages are `INTENT`, `PACKET_READ_BACK`,
`SELECTED_SEMANTICS_READ_BACK` and `LOCALLY_PUBLISHED`. The client stores/readbacks
the packet, available module openings and bodies, then selected target exports
in the local formal index. Missing committed bodies remain explicitly missing.
The only supported retention policy is quota-bounded local custody.

There is no transaction spanning the three component databases. On partial
failure `PartialPublicationError` supplies `publication_id` and `outcome`;
already committed data remains. The operation is fail-stop, not rolled back.
After closing it, an explicitly authorized fresh operation can call
`reconcile(publication_id)`. Reconciliation needs the retained packet, checks
actual data and creates a new linked publication attempt; it does not edit the
original history or regenerate a lost packet. No private SQLite edit is needed.

```python
workspace.status()
workspace.history("operations", after=cursor, limit=16)
workspace.history("publications", after=cursor, limit=16)
workspace.read_record("operations", operation_id)  # status, grant, report
workspace.read_record("publications", publication_id)  # operation, intent, outcome
report = client.report()
await client.close()
workspace.close()
```

History is bounded lexical-ID paging, not chronological order or a snapshot of
concurrently inserted records. `read_record(..., max_bytes=1048576)` bounds saved
field data and returns only untrusted history. Reopening changes unfinished
operation status to `INTERRUPTED_WITH_UNCERTAIN_TAIL`; it never restores a grant,
warrant, context, used allowance or successful owner call. Saved status and
originating operation IDs make interrupted publications inspectable.

`admission_submissions` counts entered admission paths, not successful workers
or actual verifier attempts. Consult concrete owner reports for those outcomes.
Nested worker counters are not additive CPU totals. Reports disclose unknown
provider cost, DHT wire bytes, final report/exit tail and any uncertain worker
cost. The enclosing Job supplies actual process-tree accounting and closure.

A failed call revokes authority; expiry, changed issuance or exhausted calls
also fail-stop an open client. A concurrent-call refusal does not interrupt the
already running call. Cleanup or final-report uncertainty poisons further grants
in the current workspace object. A second `close` returns the retained state;
it does not convert incomplete cleanup into success.

After `CLEANUP_INCOMPLETE` or `CLOSED_REPORT_UNCERTAIN`, the trusted owner strategy
must exit its enclosing operation and require the parent's terminal descendant
closure before starting a new launch. Do not close/reopen the workspace within
the same live owner process to bypass this rule: the poison flag is process-local,
not a durable mechanism proving old descendants have stopped.

Local publication does **not** start a provider, advertise a DHT record, replicate
data or guarantee retention after the holder disappears. Existing selected
provider/location components can expose this data under separately owned finite
service lifetimes. This client adds no hidden service/repair framework. Public
service lifecycle and end-to-end integration must be completed and qualified
before claiming a deployable global v5.
