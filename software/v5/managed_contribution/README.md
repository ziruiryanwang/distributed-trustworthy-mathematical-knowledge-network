# Managed contributions through the ordinary public owner

This successor connects a separately running contributor to the existing managed
placement service. It adds one private credential handoff, not another network,
identity system, prover or mathematical acceptance rule. Source review and
subsequent installed tests have separate evidence; this directory alone is not
a completed v5 release.

Use a separately adopted successor release with **127 SDK sources**, including
`v5/client/private_credentials.py`, and this replacement managed owner. The
unchanged boot snapshots those sources plus its one owner entry (128 rows).
Old installed 126-source releases and their used sources stay unchanged.

## Ordinary operation

The public invocation, outer `DMKN_V5_INSTALLED_REQUEST_V1` request, manager
configuration, finite supervisor, lifecycle operations, TLS and close behavior
remain as described in the [predecessor owner guide](../managed_operator/README.md).
Apply these explicit differences to that guide:

- Every managed request now uses `DMKN_V5_MANAGED_OWNER_V2`.
- `serve` and `seal` require exactly one additional field, `intake_grant`, whose
  value is `null` or the specification below. Other operations do not add it.
- Managed results use `DMKN_V5_MANAGED_OWNER_RESULT_V2`; the internal worker
  schema/profile are also V2. A worker's parent-plan pin is generated internally;
  it is not a public parameter.
- A non-null grant enables the previously missing contributor handoff. Empty
  serving and retained read/route restoration remain available with `null`.

The new specification is exactly:

```text
intake_grant = {
  source: {host, port, tls, server_name},
  write_until_ms: integer UTC deadline,
  retention_until_ms: integer UTC horizon,
  limits: {
    placements, requests, reply_bytes, wire_overhead_bytes,
    structural_bytes, storage_bytes, index_calls, recovery_passes, new_cells
  },
  credential_path: fresh absolute private filename,
  confidentiality: "OWNER_PROVISIONED_PRIVATE_CREDENTIAL_DIRECTORY_V1"
}
```

This is schematic notation, not literal JSON. All resource values use the
existing placement ranges and admission rules. The source is the **pull
endpoint** from which the host may acquire submitted material; it is not a
contributor identity. Endpoints use explicit IPv4/port/TLS policy. Remote TLS
and explicit loopback plaintext retain the existing client's behavior.
Write/retention horizons must fit the actual existing generation and grant
limits and be live when issued; metadata does not extend those horizons.

Provision the credential's ordinary parent directory privately before launch.
The filename must not already exist. It must lie outside the entire original
public output workspace, original and nested operation/control/source trees,
release and manager trees. Overlap is rejected in both directions. The worker
authenticates the parent's exact pinned plan and reconstructs the exact child
plan before repeating this check, so relocation cannot hide the outer outputs.
Paths and file hashes are treated as nonsecret metadata.

**Privacy premise:** the operator provisions a private non-hostile directory and
uses trusted cooperating local processes. Ordinary-path checks do not verify
Windows ACL secrecy or isolate against code running under the same account.
This is not remote credential provisioning, a hostile-source sandbox or secure
erasure. Never include the private file in output collection or a source archive.

## What the handoff guarantees

After real service startup, the owner fixes its original service cutoff before
issuance or file I/O. It issues once through the existing ledger, exclusively
creates the private file, checks the write, flushes, fsyncs, closes, and performs
bounded exact canonical readback. Only then can it publish the nonsecret ready
facet. The private envelope is at most 8192 bytes.

The file contains exactly `schema`, `token`, and `metadata`. Its schema is
`DMKN_V5_PRIVATE_PLACEMENT_CREDENTIAL_V1`. The token is secret; do not print,
log, inspect through ordinary report handling, or copy it into a public plan.
Its grant ID is SHA-256 of the token's **ASCII hexadecimal spelling**, not the
decoded bytes. Public metadata contains the exact service bindings, endpoints,
pull source, finite horizons/limits, selected release/profile, original public
operation and its plan hash, exact joined worker session, issuing runtime, and
`service_until_ns`.

That last field is the integer floor of the original local monotonic cutoff.
Its scope is `SAME_HOST_CURRENT_MONOTONIC_CLOCK_PRIVATE_OWNER_V1`, not a portable
UTC timestamp, remote lease, post-reboot freshness proof or uptime guarantee.
Synchronous bounded file calls still rely on the enclosing process supervision;
the helper cannot interrupt a stalled filesystem syscall on its own.

The existing worker ready path remains:

```text
<public-run>/work/managed-worker/work/managed-ready.json
```

It contains existing service observations plus `service_until_ns` and
`intake_handoff`. For a grant, the latter contains:

```text
schema: DMKN_V5_PRIVATE_HANDOFF_READY_V1
status: READY
stage: READY
metadata: validated nonsecret metadata
credential: {path, bytes, sha256}
recipient_receipt_confirmed: false
mathematical_acceptance: false
```

The worker result preserves that facet (the parent includes its worker result).
With a null grant it is null. `READY` means the private file was checked and
nonsecret metadata was produced, not that a recipient received it, a placement
completed, a service remains live, or mathematics was accepted. Consume a
completed ready record; do not poll/read a partly written secret file.

Issuance charges the existing grant-count record before returning the token;
placement resource reservation occurs later on a new valid manifest. On an
ambiguous issue or failed write/readback/publication/boot, the operation fails,
retains charges and any private partial output, and attempts the original real
service close. There is no automatic reissue, refund, overwrite or deletion.
The failure observation exposes only a fixed code, stage and grant ID if known.

## Contributor API

Use the shipped helper with independently adopted expected public metadata,
contact, egress policy and finite client budget:

```python
from client.private_credentials import read_client

client, metadata = read_client(
    credential_pin, expected_metadata,
    egress=adopted_egress, contact=adopted_intake_endpoint,
    deadline=original_local_deadline,
    requests=request_cap, incoming_bytes=reply_cap,
    outgoing_bytes=request_byte_cap, operation_ms=operation_cap_ms,
)
try:
    # Use the unchanged PlacementClient submit/status API and its real caps.
    ...
finally:
    client.close()
```

`expected_metadata` is the complete explicitly adopted nonsecret metadata, not
values extracted from the unvalidated private envelope. The independently
adopted contact must equal its intake endpoint; neither the file nor its ready
pin chooses new egress rights or resource caps. The returned existing client
keeps its token in memory and its report omits it; callers must not dump private
attributes or wire bodies. `metadata` is explicitly whitelisted nonsecret data.

The reader validates exact file size/hash, canonical schema, all expected
metadata and token/grant binding, then clamps the independently chosen deadline
to the original service cutoff. Reading never starts a new service interval.
The unchanged client still performs actual transport and binding checks.
An old token can observe historical status or repeat an identical saved request
after restart; it cannot reserve a new request against a later issuing runtime.
Deleting a private file does not revoke copies, and this helper does not delete.

For in-process trusted integrations, the other public helpers are
`preflight(specification, protected)` (no effects) and
`publish(service, specification, *, release_sha256, profile_sha256, operation,
session, service_until_ns, protected)` (one issue/write). All helper failures
raise `CredentialError` with fixed codes and suppressed underlying exception
context; `observation()` is safe for the ordinary report. They do not return a
token-bearing credential dictionary.

## Scope of continued hosting

Populated **structural custody-only** hosting can keep `workspace/operations`
empty: existing placement acquisition does not create proof operations. Such
state can fit the unchanged fixed-layout reclaimer after genuine close and
retention expiry, within its exact entry/apparent-byte caps. Local proof work
belongs in a different workspace. Do not broaden reclamation or remove proof
evidence to force acceptance of a layout. The private credential file is outside
the manager and has a separate operator-owned lifetime.

This seam does not generate proofs, accept mathematical statements, guarantee
growth, establish independent hosting, or complete v5. Its consequential next
evidence is one separately authorized contributor using retained genuine bytes
through the ordinary managed service and surviving custody/route lifecycle.
