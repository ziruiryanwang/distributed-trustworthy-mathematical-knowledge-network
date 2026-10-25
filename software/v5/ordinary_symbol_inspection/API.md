# Inspect a newly encountered concept

This successor adds one operation to the existing peer API and CLI. It passed
23 focused controls and a real packaged loopback read; see REVIEW.md. The original
installation was not modified. `inspect` returns one exact inert declaration group, **not accepted
mathematics and not a Lean import**. It does not fetch the group's dependencies.

## Why it exists

A discovered theorem can refer to unfamiliar definitions such as `OrderData`
or `IsClosure`. Its preview gives their encoded names and exact export IDs in
`type_bindings`. Select one such pair to inspect the definition/group and its
constructor laws before deciding whether to acquire and check a whole theory.
The public operation uses existing locator and evidence endpoints; there is no
new wire protocol, proof format, search mechanism or trusted authority.

## Interface

Call `await peer_api.inspect(loaded, config, allowance, network_budget=budget)`.
Omit `network_budget` for a standalone two-request ledger. The existing CLI gains
`peer.py inspect` with its usual profile/runtime/config/output and resource
arguments. Do **not** provide catalog, custody, store-id or custody-limits.
Contacts use the unchanged peer contact schema and owner-selected TLS policy.

Exact configuration (the capitalized placeholders are selected JSON values):

```json
{
  "contacts": {"provider-label": CONTACT},
  "selection": {
    "provider": "provider-label",
    "name": ENCODED_LEAN_NAME,
    "export_id": "EXACT_EXPORT_ID"
  },
  "limits": {
    "requests": 2,
    "reply_bytes": 69632,
    "locator_bytes": 4096,
    "unit_bytes": 65536
  }
}
```

`requests` is exactly two. `locator_bytes` is 1..1 MiB; `unit_bytes` is 1..8 MiB;
`reply_bytes` is 1..9 MiB and must cover their sum. The example caps are choices,
not defaults or a promise that every group fits. Shared-ledger calls require
remaining capacity for both reservations before any request. They only narrow
the original deadline and do not close or replenish the caller's ledger.

## Output and assurance

Successful status is `INSPECTION_BOUND_NOT_ACCEPTED`. `locator` gives the exact
name/unit mapping; `evidence` is the existing parsed portable-evidence document
with its declaration group and import bindings. The result includes `unit_id`,
`semantic_id`, evidence/locator SHA-256 and byte counts, and the unchanged
acquisition/network accounting. No raw Python byte object enters the JSON report.

`mathematical_acceptance`, `dependencies_checked` and `native_usable` are all
false. Binding means the requested ExportID, encoded name, UnitID and output
census agree with the received bytes. It does not establish that the declarations
are well-typed in an accepted environment, that imports exist, or that any law is
true. Further semantic exploration is a separate explicit choice. Independent
admission and supported native realization remain separate operations.

Only two reads occur: locator, then evidence. No fallback, retry, dependency
traversal, source/native execution, recipient state opening or automatic caching
occurs. Failures preserve the completed locator and cost accounting when present;
begun failed fetches charge their full reply reservation. Config refusals happen
before network I/O. Transport closes its connections. The API uses cooperative
limits; the existing outer process envelope is still needed for hard containment.

## Source boundary

Only `peer.py` and `peer_api.py` differ from the native-src01 installed baseline.
The CLI changes are operation selection, state-free classification and dispatch.
All existing operations and acceptance paths are retained unchanged. The API adds
one bounded wrapper using `OrdinaryAcquisition.locator/evidence` and the existing
portable-evidence parser. Focused independent review and controls are recorded
separately in `REVIEW.md`. The actual selected OrderData read returned11,703
evidence bytes in two HTTP requests without ancestry acquisition. This is not
mathematical acceptance, broad-network validation or a final source release.
