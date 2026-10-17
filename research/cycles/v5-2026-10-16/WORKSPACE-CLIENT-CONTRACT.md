# Fixture-free workspace/client: source contract and actual gaps

2026-10-16. Source contract and implementation checkpoint. Root's
[PRODUCT-INTEGRATION-SELECTION](PRODUCT-INTEGRATION-SELECTION.md) authorizes the
fresh `frontier_network`, portable location and finite workspace client sources.
The client's actual interface is now [API.md](../../../software/v5/client/API.md).
Earlier proposed names below are design history, not competing public APIs.
No tests, runtime, Git mutation or product qualification is selected by this note. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Current implementation checkpoint

`software/v5/client/workspace.py` now composes the actual owners and selected
portable location package. `Workspace.open/reserve/operation` owns persistent
untrusted stores and a finite operation ledger; grants are recorded before
concrete owners are constructed and are not resumed from saved data. Only
successful operation construction transfers those exact owners. All child
outputs belong under the original grant directory; the enclosing actual Job
is still mandatory, including setup. `reserve(..., outer_deadline=...)` preserves
the launcher's original wall bound. Persistent `allocation_root/commons` is a
disjoint sibling of fresh launch runs and source snapshots; location adoption
uses that commons directory and create-only state/evidence below the grant.

The public lifecycle is `find -> search_offer/search_page -> resolve ->
packet_offers -> acquire -> import_context/extend_context -> author -> publish`.
Local receipt/packet admission and `semantic_material` are public alternatives.
Descriptions, candidates, available semantics and prepared packets do not mint
authority; real same-client live handles and exact selected journals do.
The one search/acquisition remains alive until client closure. No automatic
selection, new grant, fallback, service process or repair framework is hidden
inside the facade. `publish` is explicit quota-bounded local storage/indexing,
not mathematical admission or remote placement.

The independent source review led to these focused corrections: immutable
issuance revalidation; final-close detachment even if report persistence fails;
public bounded `history/read_record` including saved status and originating
operation; typed partial-publication recovery; separate finite-float operational
decoding; repeated core evidence/context input charges; expiry/call-exhaustion
fail-stop; truthful admission-submission counters; and bounded semantic-data
expansion. `semantic_material` reports `material_rows_bytes_upper_bound`, which
counts the encoded semantic rows conservatively, not full response framing.
The raw counter is not mathematical usefulness or a complete machine resource
total. Reconciliation retains the prior attempt and creates a new linked one.

This author has run no test, owner, proof, native worker or network operation.
Root owns the focused changed-boundary controls and any separate real-I
mathematical integration selection. The source milestone is not an end-to-end
pass and does not waive the open affordable aggregate/frontier or final-v5 gates.

This refines [GROWTH-CRITICAL-PATH](GROWTH-CRITICAL-PATH.md) into an implementation
decision. It does not restart the failed aggregate screen, invent A authority,
replace the growth comparisons, or import the fixture controller
`mixed_network.reciprocal_actual.Campaign` into the product.

## Decision: one integrated I-only mixed path, not four trivial wrappers

The existing mathematical components support a coherent v5 **local mixed import
and authoring** path with a genuine I receipt and no A owner. The current mixed
**network custody profile**, however, requires an adopted aggregate image. These
are different interfaces; an I-only local session must not be assigned a fake A
image to make the network constructor accept it.

There is a second independent obstacle to a fixture-free network workspace:
`location/controller.py` hardcodes the canonical research root, a specific v4
installation and manifest, a 5,896-file runtime census, location source placement
under `experiments/v5-local-checks`, and controller evidence under the same tree.
`ServiceLocationProcess` inherits these restrictions. Merely forwarding its
constructor from `Workspace.open(any_root, ...)` is not portable deployment.

Root's subsequent direction selects the more useful **integrated destination**:
an explicit I-only mixed wire-profile successor, the narrow portable-location
successor, and one finite persistent client composing those real components.
The profile changes accepted proof forms, not mathematics or packet bytes.
The local-only recommendation in the initial draft is withdrawn: do not build a
second local material vault merely to work around the current network profile.
The precise new-profile seam is below. This source contract is not permission
to modify used files; root still selects fresh sources and any actual operation.

An A-capable profile requires a real adopted A image/verifier installation, not
necessarily an A receipt on every operation. A legitimate I-only packet could
be handled by such a genuinely configured dual-owner client. That is different
from inventing A authority, but creating an unused A owner is unnecessary for
the present explicit I-only deployment. The genuine A lane remains separate;
its absence is not concealed and its scalable frontier gate is not waived.

### Alternatives root can actually select

| Alternative | What is genuinely available | Cost and boundary | Recommendation |
|---|---|---|---|
| A. Source-design the mixed network facade now; runtime held | Existing mixed network APIs compose under their real A-capable wire profile; a genuine A-backed reciprocal operation remains separately gated | Avoids a legacy branch, but leaves the actual current user lifecycle inaccessible and does not remove research-path coupling | Keep the exact network contract below; do not implement a fake-ready facade |
| B. Local workspace plus finite mixed session using genuine I | `ReceiptVerifier` -> `MixedImportSession.use_legacy_handle` -> `MixedSourceOperation` / `MixedOwnerPreparation`; I-only `MixedDeltaVerifier` accepts the resulting I-frontier mixed packet | Works locally but leaves the real network seam missing and would otherwise need a separate material vault | Do not isolate this as the next product endpoint |
| E. Explicit I-only mixed profile plus portable location and finite workspace | Existing mixed parser rejects tag-1 A under `aggregate_image=None`; existing mixed verifier checks genuine I/native deltas | Two narrow profile/custody/transport successors plus the separately mapped three-file location successor; common facade owns the lifecycle | Preferred integrated source destination after root selection |
| C. Existing legacy delta network lane | Exact `delta.receiver.DeltaVerifier`, `delta.custody.PacketStore`, `delta.transport.DeltaAcquisition`, and `delta.authoring` compose with genuine I | Different exact classes and wire profile; the newer `delta_claims` receiver is not accepted by legacy transport; it does not transparently provide mixed exact-warrant semantics | Do not copy or convert this lane merely to claim the new facade is network-ready |
| D. I receipt network workflow | `LocatedReceiptWorkflow` exists and uses a real `DeadlineReceiptVerifier` wrapper | Its exact wrapper is not the `ReceiptVerifier` accepted by mixed imports; access to original authority needs an explicit supported seam, not JSON reconstruction; location still has research-path coupling | Do not silently substitute it for the mixed pipeline |

In B or E, the retained receipt is checked normally. No changed source or full proof
production is required merely to obtain a fresh live I handle. Any subsequent
actual use still needs root's separately selected finite operation.

## Public lifecycle: persistent data, ephemeral authority

Names below are proposed, not shipped APIs. Keep the first implementation in
one module. There is no global research planner, natural-language-intention
field, mandatory task list, usefulness authority, or automatic sealing policy.

```text
Workspace.open(root, owner_profile, create=False)
  status()
  operation(grant) -> CommonsClient
  close()

CommonsClient
  find(formal_query, coverage_request)       # local committed-index mode
  find_remote(formal_query, fixed_route_plan, coverage_request)
  acquire(candidate, selected_offer, call_limits)
  retain(material, selected_semantics)      # untrusted exact bytes only
  admit_local(retained_reference, call_limits) -> live result
  import_context(warrants, openings, demanded_bodies, resolutions)
  author(context, local_lean_source, roots, call_limits)
  publish(contribution, selected_semantics, retention_policy)
  report()
  close()

Separate explicitly funded service owner:
  Workspace.serve(finite_service_grant)
```

An I receipt, an aggregate receipt/member opening, and a mixed packet are distinct
material kinds. Their explicit exact expected statement/summary and profiles are
input, not inferred mathematical authority from a filename. Local `admit_local`
dispatches only kinds for which this client owns the exact adopted verifier.
For the first I-only scope, A input refuses before construction of an A owner.

The full lifecycle has four different facts:

1. **Retained:** exact structurally valid bytes are stored and read back.
2. **Discoverable:** a selected export has an authenticated index record.
3. **Verified now:** an exact live local issuer has admitted a statement.
4. **Useful to this author:** the local agent has selected it and successfully
   applied it in an independently checked extension.

No earlier fact implies a later one. Publication is structural custody/indexing,
not admission. Authoring returns untrusted material; a local author who wishes
to use the new result must submit it through ordinary receipt/native admission.
The publish result never asserts remote placement or indefinite availability.

### Ownership and state rules

`Workspace` owns opened stores and bounded immutable material references.
`CommonsClient` owns its concrete verifier owners, import sessions, source
operations, preparation owner, operation grant and, later, network handoff.
No externally supplied callback can mint a handle or substitute a verifier.

The first implementation serializes calls and permits one active client per
workspace. A future service owner must have a separately allocated grant; it is
not an implicit extension of a user operation. Concurrent operations and mutable
installation updates are not needed to establish this seam.

Client states are `OPEN`, `FAILED`, `CLOSED` or `EXPIRED`. A missing formal query
match, missing body, declared unsupported profile, or unaffordable request is an
explicit bounded refusal/demand, not a false theorem. A failed **entered** mixed
receive or failed issuer liveness check can revoke all that issuer's handles.
The facade then fails the dependent client and retains all consumed costs; it
does not create a fresh owner and retry within the same call.

Close source operations and import sessions before their issuers. Cancel and
await any pending network action before closing acquisition. The existing
`MixedAcquisition.close()` closes both its shared `AcquisitionBudget` and its
mixed verifier. Therefore retain one acquisition for the whole finite client,
not one per `acquire()` call; do not close it after a successful fetch while
promising its handles remain usable. Close the independent I/A frontier owners
last. Close stores only after dependent operations and services have stopped.

`close()` is idempotent at the facade; a cleanup failure is reported as such,
not converted into a successful lifecycle. Cleanup time is a declared teardown
allowance, never extra time for mathematical work.

## Exact existing API mapping

These are source-level interfaces, not hypothetical replaceable duck types.

### Persistent mathematics and index data

```python
ModuleStore(root, codec, foundation, policy, limits, *, create=False)
  put_group(module, opening, *, before_commit=None)
  get_group(module, name, group_index=None)       # (opening, descriptor)
  put_body(module, name, response, *, before_commit=None)
  get_body(module, name, universes, body_hash)
  status(); close()

ModuleExportAdapter(codec, foundation, policy)
  encode_opening(module_id, relative_name, opening)
  describe(raw, expected_id=None)
  extract(raw, expected_id=None)
  resolve(record, raw)

discovery.discovery_store.Store(root, adapter, limits, create=False)
  admit(raw, expected_id=None)
  snapshot(snapshot_id=None)
  summary(snapshot_id, feature_ids, max_bytes=1048576)
  page(request)
  status(); close()
```

`ModuleStore` authenticates structural commitments, not the mathematics.
`ExportID` identifies a declaration export; it is not `ModuleID` or the exact
warrant J. `Store.admit` means *index admission*, never proof acceptance.
Configuration and persistent quotas must match on reopening. Old index snapshot
trees are immutable; quota exhaustion is a refusal, not implemented garbage
collection. Each `Store` operation resets its own local work guard, so the facade
must additionally limit the number and aggregate cost of its own store calls.

For a local query, reuse `compile_query(namespace, specs)` (one to eight formal
feature specifications), `SearchSession`, and existing store summary/page or
candidate query functions. Bind one query and explicit snapshot, serialize the
response canonically, and pass it through the existing session accept path.
Do not implement an unrelated local ranker or claim whole-corpus completeness.
Candidate-only results have no scan-coverage claim. Verified full pages report
coverage only within the selected committed metadata snapshot.

### Real mixed authority and ordinary Lean authoring

```python
MixedDeltaVerifier(
    *, legacy_verifier=None, aggregate_verifier=None,
    native_executable, runtime_pins, output_directory, envelope=None,
    operations=8, submitted_bytes=128*MIB, reserved_cpu_seconds=3600,
    controller_cpu_seconds=600, wall_seconds=3600,
    output_bytes=512*MIB, output_entries=4096)
  receive(packet, expected_summary, *, native_cpu_seconds=30,
          receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024)
  describe(handle); members(handle); export_packet(handle)
  describe_member(handle, exact_journal)
  open_member_group(handle, exact_journal, opening)
  open_group(handle, opening); report(); close()

MixedImportSession(
    *, legacy_verifier=None, aggregate_verifier=None, delta_verifier=None,
    max_sources=64, max_members=1024, max_receipts=128, max_calls=4096,
    submitted_bytes=256*MIB, data_bytes=16*MIB, wall_seconds=3600)
  use_legacy_handle(handle, receipt_bytes, *, resolutions=None)
  use_aggregate_member(handle, receipt_bytes, *, resolutions=None)
  use_delta_handle(handle, *, resolutions=None)
  variants(module); select_warrant(exact)
  open_group(module, opening); supply_body(module, universes, expression)
  selection(); require_selection(binding); census(); close()

prepare_mixed_context(session, foundation_bytes, foundation_sha256, *, limits=None)
MixedSourceOperation(session, foundation_bytes, foundation_sha256, source, roots,
                     *, limits=None, envelope=None)
  prepare(); finish(export_bytes); close()
MixedOwnerPreparation(profile, allowance, output_directory)
  author(operation, name, *, cpu_seconds, wall_seconds, memory_mib=2048)
  report(); close()
```

At least one exact live frontier owner is required by `MixedDeltaVerifier`.
I-only mixed packet parsing accepts tag-0 I claims; tag-1 A claims require an
adopted aggregate image. All imports retain original owner lifetimes. Direct
module selection is an exact J choice; conflicting complete derivations require
explicit `resolutions`, not unioning edges or silently replacing a proof.

The facade's `context` is an opaque same-client object retaining the actual live
`MixedImportSession`, its exact selection binding and representation revision.
It is not the serialized output of `prepare_mixed_context`. `author` constructs
the actual `MixedSourceOperation` from that retained session and revalidates
origin, binding and liveness. A saved context dict never becomes import authority.
Closing or changing the underlying representation invalidates that wrapper.

The context is prepared from already selected/opened declarations and demanded
bodies. Missing material returns `NEED_AUTHORING_CONTEXT_DATA`; it does not
launch unbudgeted recursive fetching. `MixedSourceOperation` binds the entire
selection, including representation revision. Changing a chosen representation
invalidates an outstanding source operation even if the visible module set is
unchanged. Its `finish` is single-consumption. The preparation owner executes
ordinary Lean source under its existing finite trusted-owner supervision and
returns `UNTRUSTED_MIXED_DELTA_PACKET_PREPARED`, not a mathematical handle.
`MixedOwnerPreparation.snapshot` deliberately refuses; it is not an A producer.

The prepared context omits imported theorem proof bodies, but includes fixed
foundation material and needed transparent semantics. The returned onward packet
retains selected unsealed native ancestry. The client must not report zero
ancestry merely because the frontend did not import those theorem proofs.

### Existing network composition, with no implicit protocol conversion

```python
mixed_network.custody.public_profile(aggregate_image)
mixed_network.custody.PacketStore(root, profile, limits, *, envelope=None, create=False)
  inspect(module, raw); put(module, raw, *, before_commit=None)
  get(digest, size); offer(request); status(); close()

MixedLocatedHandoff(channel, adapter, features, policy, budget,
                    location_limits, search_limits)
  begin_search()
MixedAcquisition.from_search(handoff, profile, module_custody, packet_custody,
                             *, verifier=None)
  export(provider, record); body(provider, resolved, digest, maximum)  # async
  offers(provider, module, *, max_offers=4, max_bytes=4096)          # async
  packet(provider, module, entry)                                  # async
  custody_ready(resolved, entry, demanded_bodies=())
  admit(resolved, entry, *, demanded_bodies=(), native_cpu_seconds=30,
        receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024)
  report(); close()
```

`MixedLocatedHandoff` is currently an alias of exact `DeltaLocatedHandoff`.
It requires one fresh actual `ServiceLocationProcess`, role `reader`, before
the child starts, the same absolute deadline as `AcquisitionBudget`, and the
same namespace/egress policy. It prepays the full location/search grant. Its
`begin_search()` and acquisition issuance are each one-shot. Issuance remains
consumed if constructing the acquisition fails.

The returned search client offers `offer`, `summary`, `page`, and `candidates`.
An offer discovers an initially unknown snapshot ID. Exact approved contacts
and local expiry survive into acquisition. `export` requires a candidate actually
returned by that same search, and `packet` requires an actual prior offer from
the selected provider. An acquired packet is not yet authority. `admit` reserves
verification work, calls the actual verifier, authenticates the chosen opening,
reads custody back and revalidates the live handle before returning it.

Bind **one formal query per finite remote client**. Several bounded candidate
pages and acquisitions can share its search/ledger. Changing queries requires
an explicit new operation, with previous costs preserved. Do not build another
handoff or call `charge_external` after acquisition starts: its prepayment is
immutable and `charge_external` is permitted only before the request sequence.
Multiple query scopes would require explicit up-front parent suballocation;
that generalization is unnecessary for the first implementation.

### Exact two-file I-only mixed profile successor

This is a restriction of supported authority forms over unchanged mixed packet
bytes and unchanged I/native mathematics. Do not change ModuleID, exact J, the
native relation, packet `SCHEMA`, receipt encoding, or the existing A profile.

Use a distinct profile schema, proof-form label, profile hash domain, offer
schema, custody configuration schema and fresh database name. Bind fixed
`RELATION_IMAGE`, `FOUNDATION`, `POLICY`, mixed packet schema and journal version;
set `aggregate_image=None` and supported claim tags to `[0]`. Omit A-header
configuration rather than copying irrelevant dummy fields. Validate exact fields
against the sole canonical I-only profile, not a remote-selected subset.

`parse_packet(..., aggregate_image=None)` already rejects every tag-1 claim as
`UNSUPPORTED_PROOF_FORM` before receipt/native admission. It also binds all exact
I journals and native deltas to fixed I/F/P and preserves complete unsealed
closure. An opaque receipt blob is still not checked by custody. Admission still
requires the exact `MixedDeltaVerifier`, with actual `ReceiptVerifier` origin,
`_aggregate_image is None`, and exactly matching I/F/P. No fallback dispatch to
A or the legacy delta checker is permitted.

Root selected `frontier_network/custody.py` and `frontier_network/transport.py`,
plus the package marker, while keeping facade implementation unselected:

| New surface | Exact changed code | Unchanged methods reusable after audit |
|---|---|---|
| I-only profile/offer helpers | New exact schemas/hash domain; exact fixed profile; offer binding and canonical byte/size/order validation | Existing packet digest/request/blob validators |
| Exact I-only `PacketStore` | Constructor adopts new profile/config/database, identical transaction/quota mechanics; `offer` emits new schema/proof-form; `inspect` revalidates exact profile and passes literal `aggregate_image=None` to the unchanged parser | Legacy `put/get/status/close` use receiver fields and `self.inspect` |
| Exact I-only composite provider | Constructor accepts only new exact store and matching F/P; initialize unchanged HTTP provider | Existing dispatch/framing/start/stop/status operate on `self.packets` and opaque requests |
| Exact I-only acquisition | Constructor binds new exact store/profile and genuine I-only mixed verifier; `offers` uses new offer validator; `report` overrides lexical old proof-form label | Mixed `admit/export/packet`; legacy `from_search/_active/_get/body/custody_ready/close`, subject to the selected same-identity location integration |

The old mixed store constructor and offer validator cannot simply be inherited:
their module globals capture the old A-capable profile/schema. Likewise mixed
`report` captures its module's `PROOF_FORM`; overriding only the constructor
would mislabel outcomes. Do not monkeypatch globals or widen old exact-type gates.
Preserve distinct exact class identities in the selected new transport.

Same mixed packet bytes may be structurally valid in both profiles, but stores,
offers, routes and live verifier profiles remain explicitly distinct. Do not
rename an old database or reuse saved authority during a future profile change.
Share only independently authenticated semantic data where its existing F/P
namespace permits it. Existing mixed I/A support and its future real-A gate stay
unchanged, not converted or marked passed by this restriction.

The portability reviewer maps three proposed fresh location source changes:
`controller.py`, `controller_services.py`, and `node_entry_services.mjs`.
Keep the other location callers in the same selected package identity so exact
`ServiceLocationProcess` and `DeltaLocatedHandoff` checks remain real; importing
a parallel subclass will fail them. Do not change the mathematical classes for
this integration. The exact adoption and launch map belongs to
`LOCATION-PORTABILITY-SEAM.md`, not a new generalized framework in this client.

## Live reuse: save verification without inventing cached trust

An admitted handle is an object issued in a private dictionary of its live
verifier. It is neither a serialized certificate nor a signed success report.

The client cache binds **issuer object identity, exact verifier profile, evidence
kind, complete exact J, and evidence digest/length**. For a mixed packet, bind
its packet digest and actual exact-member inventory; for A bind the exact
aggregate statement and member opening as well. `ModuleID` alone cannot choose
between warrant ranks or proof representations. All equality comparisons use
canonical exact data, not user-provided aliases.

A hit must still call the issuer's `describe` or `describe_member` path, check
exact expected bindings, and authenticate the requested opening. Return the
original handle, not a new wrapper pretending to be a verifier-issued handle.
If local retained bytes are used, read/hash them under the operation envelope;
if they are corrupt or mismatched, refuse without silently using an unrelated
copy. Caching avoids another full `receive` only. Live checks can still hash
installation bytes, read files and consume appreciable controller CPU.

Holding a target handle does not authorize every declaration a caller supplies.
An imported member must be in its actual inventory, with that exact J and
authenticated group. Supply only bodies committed by the selected descriptors.
Cache hits do not change the import representation or extend any deadline.

## Persistence and publication: small explicit state, not saved authority

The first workspace retains:

- Exact adopted local configuration and explicit supported material kinds.
- Existing module/body custody and formal-index SQLite stores, reopened with
  their identical configurations and quotas.
- Profile-specific I-only packet custody using the selected successor's existing
  SQLite blob/offer mechanics, plus bounded exact receipt references needed by
  local import; all are untrusted evidence, not handles.
- Immutable operation grants, outcomes and the last successful publication
  phase, with limits on record count and total bytes.

An I-only mixed packet cannot be assigned an invented A profile just to use
`mixed_network.PacketStore` today. The selected explicit I-only successor above
reuses its blob transaction mechanism with a distinct exact profile/config.
This eliminates the need for the initial draft's separate local material vault.
Keep readback, no-overwrite content conflicts, quotas, path/link checks and cold
reverification. Do not invent a trusted persistent verification cache.

Persist no handle, verifier object, active allowance, monotonic deadline or
`verified=true` authority bit. A saved successful report is audit data only.
After reopening, the client must obtain a fresh actual handle from retained
receipt/packet bytes using the current explicit adopted profile and a new
operation grant. Reopening neither restarts a pending operation nor refunds it.
An incomplete previous record is `INTERRUPTED_WITH_UNCERTAIN_TAIL`, not success.

Publication across material custody, `ModuleStore`, and the index is not atomic.
Use an explicit staged record:

```text
prepared intent -> exact evidence read back -> selected semantics read back
                -> selected export records indexed -> optional hints attempted
```

Write the index last. For each phase use the existing structural checks and
idempotent exact-data comparisons. On failure, retain completed phases and return
`PARTIAL_PUBLICATION`; do not delete data to simulate rollback. A bounded
explicit reconciliation operation may resume missing phases by checking actual
store contents, not trusting the phase label. It does not reuse the old work
allowance or claim mathematical acceptance. Corrupt or conflicting content
refuses. A stale or absent hint cannot invalidate a theorem; an indexed export
without all future bodies is not a promise of complete future availability.

The first retention policy is bounded append-only local custody within explicit
quotas. If a finite remote retention horizon is not actually enforced, do not
advertise a lease or automatic deletion/repair capability. Quota refusal is
preferable to pretending an unimplemented retention scheduler exists.

## Conserved grants and honest cost reports

At operation creation, adopt a finite immutable grant with unique ID, absolute
monotonic deadline, operation counts, input/output/storage ceilings, controller
CPU and worker CPU ceilings. Before constructing live owners, allocate their
sublimits within that grant. Clamp every owner and call to the original deadline;
do not pass `remaining` to a constructor after unaccounted setup and accidentally
extend the lifetime. Profile/runtime adoption and constructor hashing are work.

There must be one **enclosing enforceable operation boundary** for controller
and child work. Existing Python counters and component time checks are not hard
isolation. The source contract cannot claim a hard aggregate CPU or memory limit
just because nested components each accept a limit. If the first library relies
on a trusted caller's existing process/Job containment, report that requirement
explicitly; ordinary launch support is a separate selected implementation seam.

For the later acquisition path, `AcquisitionBudget` currently caps one submitted
verification reservation at 600 CPU seconds. `MixedAcquisition.admit` computes
`claim_count * receipt_cpu_seconds + delta_count * native_cpu_seconds`; the owner
has its own lifetime reservation. Both constrain the **same work**. These
reservations cannot be summed as actual consumed CPU or refunded on cache hit.
`MixedDeltaVerifier.receive` still reserves all claim CPU even when its internal
receipt cache hits, and it checks the packet's native deltas again. The facade's
same-live-handle reuse is the way to avoid that new receive.

HTTP failures preserve conservative reserved charges; a referral, timeout,
partial page or empty result grants no retries. A location event cap is not a
DHT byte meter. Index methods have per-call limits, so the client also charges
aggregate calls and its enclosing measured work; it never treats their fresh
internal guard as fresh user authorization.

Report at least:

| Field family | Meaning |
|---|---|
| Identity | Operation/grant ID, exact local profile and input evidence IDs, local/wire lane, start/cache state |
| Actions | Helper calls, new full receives, same-live-handle hits, actual observed worker calls, authoring calls, local/index writes, search requests |
| Authorization | Original ceilings, committed suballocations, reservations, exhausted/refused limit, prior operation linkage |
| Observations | Enclosing measured CPU/wall and measurement interval, nested worker observations as breakdown, byte counts and storage deltas |
| Unknowns | Failed-stage worker cost if unavailable, measurement/cleanup tails, unmeasured transport/provider costs, incomplete publication |
| Result | Exact bounded success/refusal/failure/partial state; authority exists only in a live handle, not in the report |

Do not add nested inclusive owner CPU to enclosing Job CPU. Do not call
`observed_success_worker_cpu` total cost: it omits failed work and controller
costs. Unknown is not zero. A reused handle may have zero new receipt/native
worker calls but substantial reads/hash CPU. Preserve full historical cost;
separate from-genesis comparison and forward decisions as already specified in
GROWTH-CRITICAL-PATH. A faster fixture-free API alone is not a proved net-growth
win against optimized ordinary sharing.

## Continued service and installation remain real missing seams

The existing `CompositeProvider(index=..., custody=..., packets=..., **limits)`
has async `start(host="127.0.0.1", port=0, *, tls_context=None)`, async `stop()`,
and `status()`. It enforces connection/request/reply and per-request time bounds.
It does **not** by itself give a total service lifetime. Public binding requires
TLS under its existing bind policy. A workspace service must supply a finite
absolute lifetime and an enclosing owner boundary, then stop and reap its child
before closing stores. Reopen requires an explicit new funded service grant;
do not reset used requests invisibly inside the same grant.

Maintained-location startup reports listening/dial attempted, not routing-ready.
Publishing yields advisory, possibly incomplete/unacknowledged placement, not a
global discoverability fact. A restarted service must read retained structural
state and explicitly republish bounded hints under the new service grant.
None of these actions restores mathematical authority from disk.

Before calling the future facade network-portable, select the mapped successor
for the actual location installation/evidence-root coupling. It must adopt exact
runtime/source maps and allowed output roots without weakening pin checks or
monkeypatching `ROOT`/`BASE`. Adopt the explicit I-only profile above or explicitly
require genuine A-capable deployment. These are consequential
source changes, not documentation details to hide in configuration.

## Small source selection and changed-boundary controls

The three I-only profile files are now source-selected and implemented:

```text
software/v5/frontier_network/__init__.py
software/v5/frontier_network/custody.py
software/v5/frontier_network/transport.py
```

Their source uses `public_profile()` with no remote-configurable parameters,
`PacketStore`, `CompositeProvider`, `FrontierAcquisition`, and the exact alias
`FrontierLocatedHandoff = delta.transport.DeltaLocatedHandoff`. The profile is
`DMKN_V5_I_FRONTIER_DELTA_WIRE_PROFILE_V1`, proof form
`bounded-i-frontier-mixed-delta-v1`, hash domain
`i-frontier-mixed-delta-wire-profile-v1`; SQLite filename is
`i-frontier-packets.sqlite`. No existing state or source was modified.

The later facade source remains a recommendation, not a selected implementation:

```text
software/v5/client/__init__.py
software/v5/client/workspace.py
software/v5/client/test_workspace.py
software/v5/client/API.md
```

The eventual workspace module owns immutable configuration, staged publication,
one query grant and the concrete finite mixed owner lifecycle. The two selected
`frontier_network` modules restrict the supported proof form and reuse existing
mechanisms. Pair them with the separate fresh three-file portability source
selection. No new verifier, sealer, ranker, agent SDK, packet conversion or general
plugin framework. Use real component classes, not fixture constants. A-selected
material refuses explicitly in this lane; unsupported location/runtime profiles
refuse rather than falling back to a research path. Document exact support.

Before implementation root must choose the exact installation/profile input and
whether enclosing supervision is supplied by the trusted caller or by a small
ordinary launcher. Do not assume the research campaign is that launcher.
Avoid creating opaque owner factories for tests that become production bypasses.

### Author's inherited-method source audit

The fresh source was checked against the actual methods before implementation;
this is not a runtime pass. Independent semantic review is separately assigned.

- `delta.custody.PacketStore.put` dispatches `self.inspect` before opening its
  transaction, then uses exact hashes, `self.get`, `self.status`, instance limits
  and profile ID. Its rollback, duplicate accounting and before-commit callback
  remain unchanged. `get` uses profile-neutral blob bounds/hash checks;
  `status` and `close` use only the shared table/field layout. The old constructor,
  parser and offer methods are not inherited into active use.
- `delta.transport.CompositeProvider.dispatch` invokes `self.packets.offer/get`;
  `_serve` uses unchanged route byte caps/framing and instance grants. Base HTTP
  `start/stop/status` remain profile-neutral. The fresh constructor calls only
  `D.H.Provider.__init__`, bypassing the old exact legacy-store constructor gate.
- `DeltaAcquisition.from_search` validates exact existing handoff, spends its
  one-shot issuance, preserves approved endpoint expiry/policy and calls `cls`.
  Thus it constructs the new exact profile-bound acquisition without replacing
  the handoff. `_active`, `_get`, `body`, `custody_ready`, and `close` are field-
  and opaque-byte mechanisms; `custody_ready` invokes the fresh store's parser.
  Close still revokes the mixed issuer and closes the shared budget.
- Mixed `export` and `packet` inherit the existing authenticated descriptor,
  candidate/offer, exact-byte, persistence and readback gates. Their assurance
  text says mixed packet, which is still true for this I-only restriction.
- Mixed `admit` requires the unchanged exact `MixedDeltaVerifier`, calls
  `custody_ready` before reservation/receive, retains the claims-plus-deltas
  reservation, opens the selected group and performs final issuer `describe`.
  Tag-1 therefore refuses before mathematical processing. No admission method
  or checker was copied. Both constructors and all offer validators/report
  labels that capture old profile globals are replaced in the new modules.

New native-free tests should cover only changed boundaries:

1. Workspace create/open exact configuration; structural bytes survive reopen;
   prior success JSON supplies no handle; incomplete attempts are not resumed.
2. Exact same-live-handle reuse avoids a second full receive, but invokes issuer
   liveness/opening checks; a foreign issuer, changed profile/evidence or changed
   exact J refuses. Use existing genuine-owner test facilities without weakening
   production exact-type gates.
3. Close/expiry/issuer failure invalidates dependents; no new owner/grant is
   created by retry, query change, cache miss, partial publication or reopening.
4. Same ModuleID/different J does not collide in authority cache; exact conflict
   resolution and representation changes invalidate outstanding source work.
5. Failure accounting preserves reservations/unknowns and avoids nested CPU
   double counting; all local index/publication calls consume finite parent work.
6. Bounded staged-publication interruption at each newly introduced cross-store
   boundary returns partial state; explicit fresh reconciliation checks actual
   content and neither duplicates quotas nor trusts a success marker.
7. Missing semantics return exact demands; author output remains untrusted;
   unsupported A kind is not converted into the working I-only lane.
8. Profile/store/offer cross-binding refuses old A/legacy labels, tag-1 claims
   refuse before verification, and reports expose the exact new proof form.
   Reuse inherited transaction/network tests; add only changed-profile controls.
9. One actual fresh selected location package identity flows through prospective
   handoff/search/acquisition; changed query, expired endpoint or consumed handoff
   never grants a fresh budget. Portable-path controls belong to the narrow
   location successor review, not a duplicate facade campaign.

After source review, one consequential actual test can exercise a fresh ordinary
contribution through this public facade using the retained genuine I receipt,
query/acquire it through the real selected network path, then close/reopen bytes
and obtain fresh receiving authority. Select a genuinely
changed user boundary; do not repeat the old exact-fixture reciprocal campaign
or rebuild/reprove I. Cost capture belongs to that same operation, not another
growth benchmark. No test or runtime is selected by this source note.

## Completion criteria for this increment, not the final v5 goal

The integrated increment is done only when an ordinary caller can perform the stated
supported lifecycle without experiment fixtures, hidden authority, unbounded
renewal or private state edits; its changed-boundary review and selected actual
operation agree with the implementation. It must expose retained data, exact
live warrants, costs, demands and partial outcomes in usable forms.

The final goal still requires a genuine economical scalable frontier route,
fixture-free distributed discovery/acquisition/publication, portable enforced
runtime ownership, sustainable availability and the previously stated release
assurance obligations. This note neither waives them nor labels this smaller
increment a completed v5.
