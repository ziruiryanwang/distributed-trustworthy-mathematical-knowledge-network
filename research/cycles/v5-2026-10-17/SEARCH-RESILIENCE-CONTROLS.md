# Focused within-grant search-resilience controls

2026-10-17; author memo_tests_review. Selection: `LOCAL-RESUMPTION.md`, core
contract: `LOCAL-NEXT-CENTRAL.md`. Canonical root and guard observed.

## Status and assurance boundary

Authored only fresh `software/v5/transport/test_search_resilience.py` and this
checkpoint. No test suite, compiler, Lean, proof, native subprocess, external
network call, cloud operation or Git mutation was executed by the author.
Root owns source/plan review and any one bounded invocation.

Final selected test source is 23,776 bytes, SHA-256
`21a540bd9a80fa83214ac25d184195141f8a52f146a424622cad31bf30619f52`.
This identity was checked read-only after authoring; it is not a runtime pass.

The suite uses actual `SearchSession`, `_LocatedSearchClient`,
`OwnerEgressPolicy`, helper HTTP parsing/closure/settlement, authenticated
summary/candidate verification, and the new facade's async methods with its
inherited entry/decorator/fail-stop cleanup. One existing in-memory SQLite
candidate fixture is imported for construction only; no predecessor test runs.

The facade constructor, `_active`, `_census`, report and grant/issuers are
explicitly inert. A `LiveWarrant`-shaped map entry is fabricated and carries no
mathematical authority. Its preservation tests object lifetime only. Genuine
issuer construction, source-pin-extension construction and full owned-workspace
qualification remain **source-review-only**, not demonstrated by this suite.
Neither a loopback response nor authenticated synthetic metadata is mathematics.

## Eight tests, no broad campaign

| Test | Exact distinction |
|---|---|
| Dead/expired then honest | Refused connection or expired unchanged contact consumes one original ticket; honest offer remains reachable in the same session/grant with the old deadline and live map. Expired contact never dials. |
| Receive refusals | Acquired-stream reset/broken pipe, EOF, malformed HTTP,400/404/503, and actual bounded read timeout return refusal only after one successful close wait. No implicit retry. |
| Candidate and interval pages | Failed page fully charges original bytes, rows and hits exactly once without coverage/candidate promotion; later honest page uses remaining original allowance. |
| Exhaustion | A one-request original allowance cannot be renewed to reach the next peer; the second call fails before redial and inherited fatal cleanup revokes the synthetic map. |
| Fatal failures | Close uncertainty, cancellation before/after stream acquisition, reset/timeout before any writer, unexpected local OS error, MemoryError and invalid200 metadata remain fatal. Transport failures charge the full reservation; metadata rejection charges actual received bytes. |
| Pre-dial invariants | Changed endpoint/policy, original deadline expiry and invalid attempt timeout never dial and remain fatal. |
| In-flight invariants | Deadline expiry, allowance mutation or private-ticket corruption cannot be converted to a recoverable refusal. |
| Actual tiny loopback | Exactly three HTTP connections:503 offer, honest offer, authenticated candidate. Same original session/grant/token map; finite server/task closure; no TLS, DHT or independently hosted qualification. |

Most cases patch only `asyncio.open_connection` with real `StreamReader` and an
inert writer. They do not patch the helper's classification or session logic.
Timeout fixtures wait for the helper's own actual bounded timeout; they do not
forge a return value. The real-loopback case uses two ephemeral127.0.0.1 servers
under exact owner-approved ports. Actual socket evidence is reported separately
from inert cases. No external endpoint is contacted.

The helper intentionally treats reset/timeout **before** writer acquisition as
fatal because it cannot prove closure of an unreturned transport. Tests preserve
this distinction rather than weakening it to match the broader brainstorm.

## Root-selected invocation and outcome

```text
<selected-python> -I -S -B <snapshot>/software/v5/transport/test_search_resilience.py --output <fresh-absolute-output>
```

Use canonical project cwd. Output must be fresh below canonical `experiments`,
with an existing parent. No other product/runtime/workspace data is opened by
the fixture. Only the eight named tests are loaded. A Popen-denial guard covers
the suite; actual loopback I/O is deliberately permitted. The suite writes one
RESULT with test counts, all loaded local source pins, explicit synthetic
authority labels and distinct actual-socket evidence. Root's outer finite
supervisor must account for all import/fixture/test/report work and closure.

Expected successful outcome: eight tests, zero failures/errors/skips, one
actual-loopback evidence row with three connections and clean handlers/servers.
This is not an already-observed outcome. A failed attempt must remain retained;
no automatic rerun or edits to used bytes are authorized by this document.

## Complete conservative source closure

The following76 paths are relative to `software/v5`. They were enumerated by
read-only recursive source import inspection, including package initializers
and function-local imports, not by running Python. This is a conservative
snapshot set: actual loaded modules are additionally returned in RESULT.
Use the direct `location` Python source tree, not the old launcher's portable
overlay or Node scripts. Location controller definitions are imported but no
controller is constructed, no runtime pins are scanned and no Node process
starts. No launch/boot/control-owner module or old client test is needed.

```text
admission/__init__.py
admission/bindings.py
admission/verifier.py
aggregate_claims/__init__.py
aggregate_claims/admission_binding.py
aggregate_claims/aggregate_admission.py
aggregate_claims/bindings.py
authoring/__init__.py
authoring/context.py
authoring/imports.py
authoring/source.py
client/__init__.py
client/workspace_atomic.py
client/workspace_evidence.py
client/workspace_mixed.py
client/workspace_resilient.py
custody/module_store.py
custody/receipt_store.py
delta/__init__.py
delta/custody.py
delta/packet.py
delta/receiver.py
delta/reprepare.py
delta/transport.py
delta_claims/__init__.py
delta_claims/claims.py
delta_claims/receiver.py
discovery/authenticated_index.py
discovery/candidate_query.py
discovery/discovery_query.py
discovery/discovery_store.py
discovery/formal_features.py
discovery/module_export_adapter.py
discovery/search_session.py
discovery/summary_wire.py
discovery/test_candidate_query.py
evidence_network/__init__.py
evidence_network/custody.py
evidence_network/packet.py
evidence_network/transport.py
frontier_network/__init__.py
frontier_network/custody.py
frontier_network/transport.py
location/__init__.py
location/available_descriptor.py
location/controller.py
location/controller_services.py
location/observed_route.py
location/protocol.py
location/workflow.py
mixed_claims/__init__.py
mixed_claims/authoring_atomic.py
mixed_claims/imports_atomic.py
mixed_claims/packet.py
mixed_claims/receiver.py
mixed_network/__init__.py
mixed_network/custody.py
mixed_network/transport.py
modules/__init__.py
modules/codec.py
modules/model.py
modules/native_rows.py
modules/receipt/__init__.py
modules/receipt/witness.py
modules/source_rows.py
preparation/__init__.py
preparation/owner.py
production/__init__.py
production/producer.py
transport/clients.py
transport/http_provider.py
transport/http_provider_receipts.py
transport/located_receipts.py
transport/receipt_client.py
transport/search_resilience.py
transport/test_search_resilience.py
```

`discovery/test_candidate_query.py` is the sole predecessor test-module import;
only `Fixture`, `Clock`, namespace/features/partition and query limits are used.
Its `unittest.main` is protected by its normal main guard. The selected test
suite is constructed only from `SearchResilienceControls` in the new entrypoint.

The selected Python/stdlib/SQLite runtime and outer runner/supervisor are
separate root-owned runtime pins. No provider state, source corpus, existing
workspace, production receipts or native executables are fixture inputs.
