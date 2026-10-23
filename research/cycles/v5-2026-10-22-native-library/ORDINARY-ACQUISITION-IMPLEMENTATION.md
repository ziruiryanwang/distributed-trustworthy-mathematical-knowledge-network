# Ordinary portable acquisition and cold inert custody

2026-10-23. Author: `portable_integration_audit`. Root approved the narrow
contract before transport edits. Canonical workspace guard passed. **Source-only:
no execution, network request, test, store creation, native work, migration or
mathematical acceptance occurred.** Root owns independent review, finite runtime
selection and integration. Any later network test is loopback-only unless
separately authorized; this does not authorize public deployment.

## User workflow and smallest change

An agent has an ordinary formal-index candidate but not its advertised bytes or
complete evidence. It needs to fetch those exact portable objects under finite
cost, retain them after the original provider disappears, and then pass them to
the independent local checking workflow. A certified ModuleSpec/receipt client
does not implement this ordinary format. A second index or network stack is not
needed.

The new `software/v5/transport/ordinary_acquisition.py` implements the two typed
byte fetches, an exact export-locator lookup, one shared acquisition budget and
minimal inert custody. The existing
`http_provider.py` gains only three ordinary routes, an optional `ordinary` role,
their per-request caps and raw-response dispatch. Its Endpoint, TLS, framing,
connection lifecycle, old handlers, old domains and existing client APIs are
unchanged. Ordinary helpers are imported lazily for the new role, not on old
discovery/module dispatch.

Both existing custody implementations were inspected first. `ModuleStore` is
coupled to module/group/body descriptors; `ReceiptStore` is coupled to receipt
profiles and offers. Neither can safely hold these objects unchanged. The small
new store reuses their ordinary-path and SQLite DELETE/FULL/quota/transaction
patterns, not their mathematical schemas. It is one content-addressed object
table, its exact export projection, and configuration/counters, not another
local-warrant or acceptance layer.

The product-path audit found why that projection is essential: portable imports
name ExportIDs, while complete evidence is addressed by UnitID. A cryptographic
hash cannot be inverted to bridge them. Root explicitly expanded this unexecuted
source assignment to close the gap rather than freezing an unusable acquisition
API. The projection derives from complete parsed output censuses, not name search,
peer aliases, index assertions or mathematical acceptance.

## Exact wire contract

| Route | Exact request | Successful response |
|---|---|---|
| `/v5/ordinary/preview` | `schema=DMKN_ORDINARY_PREVIEW_REQUEST_V1`, `object_sha256`, `object_bytes` | Original canonical V2 preview bytes, exactly the requested length/hash. Maximum 1 MiB. |
| `/v5/ordinary/evidence` | `schema=DMKN_ORDINARY_EVIDENCE_REQUEST_V1`, `semantic_id`, `unit_id`, `max_bytes` | Original canonical V2 evidence bytes with exact S/UnitID. Maximum 8 MiB and no more than the requested cap. |
| `/v5/ordinary/locator` | `schema=DMKN_ORDINARY_LOCATOR_REQUEST_V1`, `semantic_id`, `export_id`, `max_bytes` | Existing canonical `DMKN_ORDINARY_LEAN_EXPORT_LOCATOR_V2` containing S, UnitID and original export name. Maximum 1 MiB; exact ExportID binding, not proof that a unit exports that name. |

Every request rejects additional fields. No remote URI, native path, source,
compiler option or executable extension is accepted. JSON bytes are returned
unchanged through the existing application/json transport, not converted into
receipts or module openings. The provider serves only locally retained objects.
Missing objects/roles close the failed operation under the existing provider
behavior; unavailability never means mathematical nonexistence.

## Owner APIs

```text
OrdinaryStore(root, semantic_id,
              {objects, exports, logical_bytes, db_pages}, create=False)
store.put_preview(raw, before_commit=None)
store.put_evidence(raw, before_commit=None)
store.get_preview(sha256, exact_bytes, check_budget=None) -> raw
store.get_evidence(S, UnitID, max_bytes, check_budget=None) -> raw
store.get_locator(S, ExportID, max_bytes, check_budget=None) -> raw
store.status() / close()

Provider(index=optional_existing_index,
         custody=optional_existing_module_store,
         ordinary=optional_OrdinaryStore, ...existing_limits)

OrdinaryBudget(deadline=<original absolute monotonic parent deadline>,
               requests=<aggregate cap>, reply_bytes=<aggregate cap>)
budget.charge_external(label, requests, reply_bytes)  # prepay search/location
budget.report() / close()

OrdinaryAcquisition(adapter, explicitly_configured_endpoints, budget,
                    local_custody=None)
await client.preview(provider_label, actual_candidate_record)
await client.locator(provider_label, S, ExportID, max_bytes=1MiB,
                     expected_name=None)
await client.evidence(provider_label, S, UnitID, max_bytes,
                      expected_export_id=None, expected_export_name=None)
client.report()
```

The caller supplies the coherent `OrdinaryExportAdapter` and selected ordinary
helper assembly. `preview` detaches the candidate record before awaiting I/O,
requires its exact body hash/size and recomputes the complete adapter record,
including features and locator. `evidence` reparses the complete bounded V2 unit
and recomputes S/UnitID. Its optional paired expected ExportID/original-name
arguments also require that the actual complete unit output census contains
that name. `locator` recomputes the requested ExportID from returned S/UnitID/name
and, if supplied, matches the consumer's exact expected name. A locator alone
does not establish the actual unit's output census. Results return raw bytes
plus explicit nonacceptance.

These are separate explicit operations. No hidden follow-up request, dependency traversal,
provider retry, discovery request or proof check occurs. Before using the pair,
the integration controller still calls existing `portable_preview.resolve` to
bind the actual preview header/type bindings to the exact evidence. Independent
catalog admission must then establish warranted imports and check genuinely new
mathematics. Neither index membership nor either successful fetch does so.

For a missing imported `(originalName, ExportID)`, the consumer explicitly asks
`locator(..., expected_name=originalName)`, then explicitly fetches the returned
UnitID with both expected-export arguments. The latter rejects a unit that does
not actually export the requested name even if a peer constructs a self-consistent
locator hash for that nonexistent output. Basis symbols remain local foundation
obligations, not invented ordinary-unit locators.

Root's admission author has the durable storage contract: call `put_evidence`
with the parent deadline callback **before** accepted catalog promotion. The
catalog's UnitID and native snapshot alone cannot republish the complete evidence.
Inert bytes and exact locators may remain when later mathematical checking fails;
they carry no accepted flag and do not authorize promotion.

## Budget and timing boundaries

Both byte fetch types, exact locator lookups and all configured providers share
the same `OrdinaryBudget`.
Its deadline is supplied by the owner; neither client nor store silently creates
a new deadline. An owner may prepay a bounded search/location phase before any
fetch, but must enforce the corresponding subbudget itself. There is no refund
of prepaid external work. Recreating an owner budget would be new work, not a
continuation authorized by this API.

Calls are serialized. `begin` reserves the selected reply cap and consumes one
request before dispatch. Successful exact validation and optional retention
settle the actual response length. Any exception/cancellation after begin charges
the full cap, including malformed results, transport failure, expired budget and
local retention failure. All attempts settle in `finally`; changing providers
does not replenish requests, bytes or time. Pre-dispatch malformed input or an
unconfigured provider causes no request and no false network measurement.

Reply quotas intentionally measure reply bodies, not all transport costs.
Reports separately retain completed-response request/reply/header measurements
and conservative per-attempt request/header upper bounds. Incomplete transport
measurements are not reported as complete actual costs. TLS record/handshake,
DNS (not used; contacts are IP addresses), kernel buffers, CPU and physical disk
overhead are not inferred from payload counts. Storage has separate object,
export-row, logical-byte and SQLite-page quotas.

The reused exchange has a request timeout followed by **up to one additional
second of best-effort socket cleanup**. This requires an explicit outer cleanup
allowance; the absolute deadline is not a claim of process termination or fully
confirmed network closure at that instant. SQLite calls and bounded Python
parsing are synchronous; before/after checks do not preempt them. External hard
process/resource containment remains necessary, as with the existing transport.

## Cold storage, identity and failure behavior

One store is configured for one S and exact quotas. Byte keys are `(preview, SHA256)`
and `(evidence, UnitID)`; each row also binds the raw SHA-256. Preview variants
with different metadata therefore remain different byte objects even when they
claim one export. Evidence includes all exact direct imports in its portable
identity. No provider address or implementation/path enters either content ID.

Puts use actual bounded preview/evidence parsers and refuse mismatched S.
Every evidence output generates a recomputed ExportID and the existing portable
locator. All such rows, evidence bytes and counters commit in one transaction;
export-row count, projected bytes and physical pages have explicit quotas.
The existing locator profile bounds original-name representation: if any output
cannot be represented, the entire put refuses, never silently omits that output.
There is no partial accepted prefix or new mathematical consequence. Same-name
exports from different units and every member of a multi-output unit retain
distinct exact ExportID mappings; original names are not global lookup keys.

Duplicate puts compare exact raw bytes and the complete existing locator
projection without a new quota charge. Reads query BLOB length before materializing
it, then verify raw SHA-256 and exact preview/evidence content identity. Under
the protected-owner database premise, syntax/S were validated at put and need
not be reparsed on every service read. This removes repeated full unit/DAG census
from the provider hot path by argument, not a performance experiment. Remote
receiving clients still parse their selected evidence independently. Locator
reads validate their bounded canonical shape, S/ExportID/name binding and retained
evidence presence; they do not parse that full evidence body. Cold reopen uses
the same exact configuration without loading a Lean context. There are no all-corpus scans,
native modules, proof replay, deletion/GC or implicit retention entitlement.

Ordinary nonaliased paths, finite database/journal size and no WAL/SHM sidecars
are enforced. Serialized owner calls and protection against external mutation
remain premises. SQLite recovery preserves custody rather than mathematical
authority: all fetched objects remain inert. If a deadline expires after a
successful local storage commit, the acquisition may report failure with those
inert bytes retained; it does not invent an accepted mathematical result or
refund the attempt. The owner can inspect/reopen exact custody without repeating
network work automatically.

## Source review and next finite discriminator

No test was run, including Python syntax compilation. The catalog controls from
the preceding task are separate: root reports their five groups passed in
`6f61fd9a` and they must not be repeated here.

Review should focus on the changed route reservation/dispatch, exact ordinary
identity binding, shared failure accounting, no deadline renewal, cold retained
byte re-serving and the absence of any acceptance side effect. The later focused
loopback test should combine real typed fetches, wrong locator S/ExportID/name,
actual output omission, same-name exports from distinct units, all outputs of a
multi-output unit, invalid/absent responses, exhaustion across providers and
reopened custody. The old transport/module,
translation and catalog suites need no broad repetition.

This advances acquisition/custody, not independent-host availability, full public
deployment, efficient cold Lean context loading or a useful-growth advantage.

## Source pins

Paths are relative to canonical
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

| File | SHA-256 |
|---|---|
| New `software/v5/transport/ordinary_acquisition.py` | `e69bd0f33829e4709fdc1a7c3afe4150704dfeabfe30243195b379945081e826` |
| Narrowly changed `software/v5/transport/http_provider.py` | `431aae7f10f1a2c0c0323c4aea720f4139e57bb4bf7b61bf98e9e5b69d6cdd59` |
| Unchanged `software/v5/transport/clients.py` | `640d1344824829865060712370444b5051720ce7b0a741e8eefc0da8a066c6464` |
| Unchanged `software/v5/discovery/ordinary_export_adapter.py` | `fb732a01996a821ff52f95dcb8fbd6a7a89f9aecbbb6492e24198dcf79132600` |
| Unchanged `software/v5/ordinary_lean/portable_preview.py` | `b78dd54340b7b55e4359769d6784f7f225ba304457ce880ce2760717e865550d` |

Root must select the full coherent helper assembly, interpreter and any later
supervisor. Historical experiment snapshots and all accepted local state were
left unchanged.
