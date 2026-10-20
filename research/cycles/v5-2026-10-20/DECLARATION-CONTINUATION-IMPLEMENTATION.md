# Exact-declaration continuation implementation

Source-only checkpoint, 2026-10-20. No tests, native checker, prover, network,
installation or Git operation was run by the implementation author.

## Concrete change

An agent may now attempt one exact-name declaration request and retain its
existing work when that supplier is positively known to be unavailable. It
can explicitly choose another already-authorized supplier in a later call.
There is no retry loop, new contact, renewed deadline or replacement budget.

The existing fail-stop `resolve_declaration` and `SemanticReader.resolve`
methods are unchanged. These are new optional methods:

- `try_declaration(acquisition, provider, module, relative_name, max_bytes,
  *, attempt_timeout_ms=5000)` in the transport helper.
- `client.try_resolve_declaration(origin_candidate, module, relative_name,
  *, max_bytes, supplier=None, attempt_timeout_ms=5000)`.
- `reader.try_resolve(demand, *, max_bytes, supplier=None,
  attempt_timeout_ms=5000)`.

Transport success is `DECLARATION_VALIDATED` with the existing adapter's
`resolved` data and `mathematical_acceptance=False`. The facade then commits
and reads back the group before returning `DECLARATION_CUSTODIED` with a live
same-client candidate. The reader returns its existing `RESOLVED` or
`NO_PROGRESS` result. Neither candidate nor structural custody accepts a
mathematical assertion.

An unsuccessful settled attempt returns the same record through all layers:

```text
schema: DMKN_SEMANTIC_DECLARATION_ATTEMPT_V1
status: UNAVAILABLE_AT_SELECTED_SUPPLIER
supplier: exact selected existing supplier
reason: one of the existing body-transport availability reasons
request: {module_id, relative_name, group_index: null}
settlement: FULL_REPLY_RESERVATION_CHARGED
global_complete: false
mathematical_acceptance: false
```

## Preserved boundaries

The transport reuses the existing body attempt's exact owner/contact binding,
unchanged-state checks, response parser and unavailable-result type. Its small
fixed `/v5/modules/group` exchange is separate because the used body exchange
has a fixed body route; no global route mutation or artificial body descriptor
is used. Request and reply accounting mirror that already selected transport.

Only refused connections, cleanly closed interrupted reads, read timeouts with
observed closure, and HTTP 404/503 can return the unavailable result. Malformed
HTTP or HTTP 200 data, wrong names/modules, invalid commitments, changed or
expired contacts, exhausted allowances, cancellation and uncertain cleanup
remain exceptions. Final contact/source/liveness checks are still required.

For success, the reply must be canonical; the unchanged export adapter performs
`encode_opening(requested_module, requested_name, opening)`, `describe`, then
`resolve`. The returned locator is also checked against the exact request.
These checks precede custody. Custody, readback, input charging and candidate
issuance have no recoverable exception handler.

For a settled miss, the original grant and helper step charges advance, but no
candidate, group, body, selected member, retained semantic byte, pending demand
or semantic revision changes. The helper remains collecting; the client remains
in its original operation. Successful source/liveness checks after settlement
are necessary, not a guarantee inferred from an HTTP status alone.

## Exact logical source map

These fresh files are source candidates, not an installed release:

| Logical module | Selected candidate source |
|---|---|
| `transport.declaration_resilience` | `software/v5/transport/declaration_resilience.py` |
| `client.workspace_evidence` | `software/v5/client/supplier_complete/workspace_evidence.py` |
| `client.semantic_reader` | `software/v5/client/supplier_complete/semantic_reader.py` |

The two logical client overlays are full successors of the corresponding
`supplier_resilient` sources. All other selected logical modules remain as
before. The declaration source guard adopts only existing issuer source pins;
it extends the unchanged body-attempt pin set with the declaration helper.
Caller code must select the fresh logical map explicitly. The current installed
distribution and all used predecessor sources remain unchanged. No new installer
or repeated distribution build is selected by this checkpoint.

Initial review bytes: transport 8,485 bytes / `d8ee2dafc3237726501a1180ebb6b1be641ea9e5d8092c8ee841e1095da3e06c`;
workspace 39,159 bytes / `2a674d313a6e114394708a02336faefc082142ea29e00d763662147696b59e6e`;
reader 29,233 bytes / `7d8c93ddd7b1aabdcad6e47c864c0a8601e6e84cfbf35f1b4d02cfcc26de65fa`.

Independent controls and source review are separate. They target this changed
declaration failure boundary, not repeated body tests or mathematical admission.
This change does not solve affordable certification or establish global search
completeness, useful-growth advantage, hostile-source isolation or full v5.
