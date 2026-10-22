# Typed renewal: exact preparation-to-production seam

2026-10-22, source-only decision for root. No imports, selectors, generated
requests, snapshot, build, proof, runtime sweep or code changes were performed.
This note does not presume that U's pending production or the later ordinary
U-to-V operation has succeeded. It supplements, not repeats,
`POST-PREFLIGHT-PRIORITY.md`.

## Decision

**No new producer, relation, image, scheduler or adoption profile is needed for
the proposed A*(U)-parent V packet.** The exact existing typed lifecycle already
has the required public calls. The missing integration is one small supervised
local caller for generic snapshot and subsequent request construction. The
current typed CLI exposes only `preflight` and `run`, not these two phases.

If root selects implementation, add only a new trusted-local
`software/v5/typed_renewal/production_owner.py` caller with separately selected
`snapshot` and `request` actions, plus root's finite selectors. Do not edit the
used typed producer/operator, widen the current130 consumer, or rebuild hosts.
This is a proposed source selection, not authority to implement or run it.

## Existing calls, in exact order

The calls below are API notation, not executable future-result fabrication:

```python
owner = TypedLifecycleProducer(exact_existing_profile)
prepared = owner.prepare(actual_V_packet_bytes, actual_V_journal, envelope=envelope)
snapshot_report = owner.snapshot(
    prepared, configuration=actual_configuration_pin, selection=actual_outer_selection_pin)
owner.close()

# A later, separately selected invocation, after the first outer operation closes:
owner = TypedLifecycleProducer(exact_existing_profile)
request = owner.production_request(
    five_actual_snapshot_evidence_pins,
    allowance_id=new_V_allowance, budget=explicit_V_budget,
    checkpoints=[], prior_attempts=[], output_directory=fresh_V_stage_output,
    stage_limit=selected_finite_prefix, carried_external_costs=explicit_actual_costs)
owner.close()
```

`production_request` already runs full preflight. Calling `preflight` once more
would duplicate work unless a distinct later boundary requires fresh validation.
The returned request can then enter the unchanged existing typed operator's
`run --profile ... --request ... --owner-report ...` under its separately funded
finite production wrapper. No phase dispatches the next one automatically.

The actual source-derived V packet/journal must come from the ordinary client's
successful saved outputs and independent outcome audit. Never substitute the
old conditional V fixture just because its statement hash matches.

## Why the A-parent route is already supported

`aggregate_claims.prepare_mixed.prepare_mixed_seal` treats certified frontiers as
terminal premises. It selects the exact target delta's backward closure, preserves
ordered parent claims, encodes tag1 aggregate parents and derives the member
commitment and next seal height. For the specified packet the caller checks:

- One tag1 parent with the actual U receipt and exact H_U; no tag0 I parent.
- One U frontier and only V's new delta; selected indices all `(0,)`.
- Two exact members U/V, one edge, maximum member rank2 and seal height2.
- No U witness, old I receipt, theorem-proof body or whole fixture is supplied.

`TypedLifecycleProducer` inherits ordinary `prepare` and `snapshot`. Its
`_evidence_kind` dispatches **by exact key set**, not a permissive fallback:
ten roles select the retained general36 exception; five roles select ordinary
generic adoption. A failure never changes branches. New V uses only the generic
five-role path and cannot inherit the old comparison's exit1 exception.

The retained snapshot host's native relation derives the exact pending typed
claims. `receipt::verify_pending` accepts a legacy claim only at I, and an
aggregate claim only at the explicitly adopted A*. It checks a genuine resolved
Succinct/Poseidon2 receipt with development mode forbidden and exact journal
bytes before adding the receipt as an execution assumption. New guest execution
checks V's new delta and the U membership/interface premise; it does not execute
U's ancestor witness. The stage host again verifies typed parents and capsule
binding, resolves its ordered assumptions, and finish independently verifies the
final aggregate receipt. This is a source argument for the supported route, not
evidence that the future A-parent operation has completed.

## Stable source and profile identities

Reuse the exact existing profile document
`experiments/v5-local-checks/typed-production-controls-01-profile.json`, SHA-256
`1242b0a8430e68032bbedbddcb3c6539fbdc95a2a5cf567936545c5f891246cc`.
Its existing composite profile ID is
`166ad63e75a43a427f2b4fcd8642849ba0ab804ac54b08cea39cd422863e779e`.
It names A* `9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865`,
the corrected stage host and the separately adopted image-parametric snapshot
host. Its constructor adopts both actual build chains. No old-image build
provenance is rewritten as a typed-image build.

The profile's29 producer-source pins point to the **stable retained source root**
`experiments/v5-local-checks/typed-production-controls-01/sources/software/v5`.
Its support runtime has47 pins: these29 sources, two existing operator sources
and16 runtime files. The new outer caller may be a fresh snapshotted source, but
must import the29 producer modules from that stable root. Loading copied producer
modules from the new operation's source snapshot would fail origin checks and,
if accommodated by changing the profile, unnecessarily change profile identity.

The caller belongs in the outer selection's sources, not in the profile's exact
29-source list. The existing profile includes the needed aggregate preparation
modules `input.py` and `prepare_mixed.py`; current130 consumer intentionally does
not. Do not import the consumer owner/helper into this specialized environment:
`typed_renewal/source.py` also imports `modules.model` and `modules.source_rows`,
which are outside the producer29 closure. Use the existing `owner.prepare` and
small direct checks on its returned `PreparedSeal`, rather than expanding or
silently mixing two separately selected module installations. No algorithm copy
is needed for these workload-specific postconditions.

## Snapshot input and actual-outer binding

The pinned configuration has the existing exact schema
`DMKN_AGGREGATE_LIFECYCLE_SNAPSHOT_REQUEST_V1`, with:

```text
profile_id, profile_document, packet, target_journal,
envelope, cycles, po2, diagnostic_mode, limits, output_directory
```

`target_journal` is actual V J encoded as368 lowercase hex characters. `envelope`
contains every field of the selected producer's `Envelope`; po2 is18, mode is
`stats`, cycles is explicitly bounded by2^26. The snapshot rederives the complete
prepared object from pinned inputs and requires exact equality.

Use the existing `tools/Run-V5-Check.py` wrapper for the snapshot caller:
`aggregate_small._local_outer` requires its actual
`DMKN_V5_LOCAL_CHECK_RESULT_V1` closure, not the long-running typed-production
wrapper's different result schema. Its corresponding selection is
`DMKN_V5_LOCAL_CHECK_V1`; configuration, complete profile document, original V
packet and **all adopted producer installation pins** must be present in its
runtime map, at most256 entries. The selected caller source must be under
`software/v5`, because this wrapper rejects research-directory source entries.
The wrapper may snapshot the caller while retaining the stable producer modules
as runtime pins. No private profile mutation or temporary old-schema object is
needed.

Snapshot creates `wire.bin`, `header.bin`, `parent-0.bin`, `staging.json` and
`COMMAND.json`, binding exact staged bytes internally. They are genuinely new
outputs, not fictitious pre-existing outer runtime pins. The only staged parent
receipt is the actual U aggregate receipt. A separate later caller collects:

```text
result = snapshot-output/RESULT.json
outer = completed-snapshot-wrapper/RESULT.json
selection = exact snapshot selection
configuration = exact snapshot configuration
command = snapshot-output/COMMAND.json
```

Generic adoption checks clean actual outer/host closure, exact arguments and
limits, saved invocation/stdout, source/profile/configuration, staged bytes,
complete capsule, costs, finalization sentinels and output census. It rejects
missing or unfinished evidence rather than generating success metadata.

## Resource and lineage consequences

The existing snapshot ceiling is180 worker CPU /60 controller CPU /240 wall
seconds,3,072MiB and two active processes. Output maximum is208MiB/288 entries.
The pre-execution reservation includes **both**96MiB capsule/segment ceilings,
8MiB diagnostics, staged receipt/wire/header, logs and final reports. Choose a
configuration that covers that fixed reserve; an arbitrarily small output cap
will refuse before execution. The20MiB fixed-session envelope includes original
packet and adoption records;14MiB is reserved for remaining diagnostic/evidence
data. A large valid packet can therefore be operationally refused. No cap increase
or RAM campaign follows from this note.

The future segment count s and capsule bytes are unknown until the one actual
V layout. Do not borrow general36's session ID,36 segments or109 calls. With the
specified one aggregate parent, the existing graph has3s+1 host calls. Its exact
caps, missing graph and full-path fit come from the existing request/preflight,
not an extrapolated successful-completion promise. Fund only after that evidence.

The unchanged profile can serve both U and V, but **V is a new session and a new
explicit allowance**. U's successful checkpoints/allowance cannot continue into
V: session identity includes image, wire, exact header, complete capsule, ordered
parent receipt contents and actual snapshot-evidence contents. V prefixes must
retain their own successful checkpoints, complete failed/passed attempt lineage,
unchanged budget and carried-cost record. Charge actual V preparation/layout and
enclosing-owner costs explicitly; keep U certification as prior shared-capital
cost in the full-cost comparison, not invisible free ancestry or duplicated
per-consumer charges. The software's allowance check does not itself prove that
the caller's chosen carried-cost record is economically complete.

## Minimal caller obligations and stop condition

The caller only needs pinned-input loading, stable-source selection, the public
calls above, workload postconditions, exception-safe owner closure, and bounded
new output/report persistence. Its `snapshot` action must not make a production
request before its own actual outer is complete; its later `request` action must
not invoke `run`. Production uses the already-existing typed CLI unchanged.

Root can select this small adapter while the U proof runs. The next native work
remains conditional on actual U certification and ordinary V admission. A genuine
A-parent snapshot plus independent audit resolves the remaining layout/semantics
integration boundary; only then is a V proof allocation decision justified. No
new experimental sweep, duplicate U layout or new producer framework is indicated.

Read sources: `typed_production/{producer,operator,test_adoption}.py`,
`aggregate_lifecycle/{producer,snapshot}.py` and API, `aggregate_claims/prepare_mixed.py`,
`aggregate_small/{producer,aggregate_host,stage_host}` and `aggregate/receipt.rs`,
the existing profile records and `tools/Run-V5-Check.py`.
