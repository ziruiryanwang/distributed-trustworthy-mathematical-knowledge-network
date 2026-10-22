# Exact-packet controls01: independent actual outcome

2026-10-22, storage_outcome_audit. **The run FAILED: six groups passed, groups04
and05 errored.** Supervisor cleanup is clean. These failures are preserved;
neither the source-review pass nor the diagnosis turns them into executed passes.
No test was rerun and no used source/evidence was edited by this audit.

## Exact saved operation

Directory: `experiments/v5-local-checks/exact-packet-controls-01` under the
canonical project root. The selected test was34036B/SHA
`bd9a48119a3ae428e343a2d6061256026fc530cf0b281bf33e49e554214f2883`.

| Saved artifact | Bytes | SHA-256 |
|---|---:|---|
| `selection.json` |27024|`855e62da5bae3fde9837089bf2cc5876a6f9b5faefa2272de684c9948765f671`|
| `RESULT.json` |2001|`fe2d3e2bee12e9c8777d65d7140f866ec117820070272fc76b77377667abf29c`|
| `exact-packet-controls-result.json` |25886|`0019bb3a8c835d1a6d3aa078805ade67f1cb5eff4e5532a5c44943964337f9bb`|
| `command/stderr.txt` |8405|`4a9ef702bcfed18f4d079af44653610fd20e84ca5a24f3376485d37ee3bec127`|

Stdout is empty. Full stderr contains the eight test outcomes and both complete
tracebacks. Result and stderr agree:8 attempted,0 assertion failures,2 errors,
0 skipped, no reported forbidden calls and no unexpected event-loop errors.

I independently hashed all137 saved source-snapshot files (1895822B) against the
exact selection and all129 assembled logical modules (1694560B) against their
expected selection/base-map identities and recorded sizes. No discrepancy was
found. Exactly the six reviewed successor modules differ from the base129 map;
the other123 are unchanged. The selection contains29 runtime/map pins. The
frozen runner's final check completed without a `FINAL_BINDING_FAILED` result;
this audit did not repeat a large runtime-payload sweep.

The command exited1, direct child reaped, Job closed, final active processes0,
no cleanup errors or termination request. The saved Job reports1.53125 CPU
seconds; wrapper CPU is0.484375, so known total is **2.015625 CPU seconds**.
Outer wall is6.6148127 seconds. The nested supervision CPU field is not added
again. The report records total_processes2 across its lifetime; the configured
concurrent-process cap is1, not a claim of exactly one lifetime process.

## Six retained passes

- **01:** the ninth structurally valid packet is absent from max8 offers;
  actual exact-packet HTTP transfer succeeds, old offered acquisition refuses,
  no offer is forged, duplicate custody does not refund its new request.
- **02:** actual provider-dispatch mutation of the caller's entry does not
  change the request/readback/returned exact identity.
- **03:** malformed/bool/oversize/profile preflight, missing digest, wrong size,
  wrong module, injected same-length dishonest response and V1/V2 profile
  crossing refuse as asserted, with custody unchanged where required.
- **06–08:** extracted direct/staged/semantic-reader method controls pass,
  including later-body snapshot, stale-cache and changed-final-journal refusal,
  structural staged token and demanded-module/variant checks.

The latter three still use explicitly documented owner/admission/acquisition
doubles and removed decorators. These are changed-method control passes, not
live owner or cryptographic admission. All receipt payloads in this run are
intentionally inert. No actual mathematical proof, native check or Node role
was executed. The passing six groups need not be repeated to address04/05.

## Group04: incompatible fixture endpoint classes

Observed exception: `LOCATED_CUSTODY_EGRESS_BINDING`, while constructing the
expiring acquisition, before the requested expiry/commit controls run.

The exact saved call path is:

1. `Controls.fixture` obtains `f.endpoint` from the evidence provider's inherited
   `http_provider_receipts.Provider.start`. That method returns its own
   `http_provider_receipts.Endpoint` frozen dataclass.
2. `Controls.acquisition(expiring=True)` wraps that object in `_ExpiringContact`.
3. Acquisition construction calls `configured`, then endpoint `validate`.
4. `_ExpiringContact.validate` reconstructs the canonical approved endpoint via
   `OwnerEgressPolicy.endpoint`, which imports and returns the distinct
   `http_provider.Endpoint` dataclass, then requires equality with the wrapped
   endpoint. Dataclass equality requires the same class, not only equal fields.

Thus the fixture violates the existing canonical endpoint binding. The trace
directly identifies this guard, and the saved source identifies both distinct
classes. This is not a packet_exact expiry failure and does not justify weakening
egress comparison. The earlier request-budget exhaustion assertion completed;
the rest of group04 is not an executed pass. Its only observed dispatch is the
initial offer request.

A fixture successor should obtain its wrapped endpoint from the existing
`policy.endpoint` using the bound host/port/TLS values. It should not patch
dataclass equality, remove the policy guard or renew a consumed budget.

## Group05: provider allowance cannot cover its group-route reservation

Observed exception: `asyncio.IncompleteReadError` reading HTTP headers for the
initial `/v5/modules/group` request; no provider dispatch was recorded. The
failure occurs before the controller reaches the new packet_exact branch.

The saved fixture sets provider `max_reply_bytes=8*MiB`. The actual inherited
group route has a fixed16MiB reservation in `delta.transport.ROUTES`, inherited
from `http_provider_receipts.MODULE_MAX`. Unlike packet/offer requests, a group
request carries no provider-specific lowered allowance. `_serve` therefore
requires, before dispatch:

```text
reply_bytes + reserved_reply_bytes + 16 MiB <= 8 MiB
```

This is impossible even for the first tiny group response. `_serve` catches its
exception and closes without a response header; consequently client EOF and
empty dispatch observations are exactly consistent with this deterministic
source defect in the fixture configuration.

The provider does not persist the internal exception, so
`DELTA_PROVIDER_REPLY_QUOTA` is a **source-derived cause**, not a logged server
error. No claim of directly observed internal exception is made. No successful
placement, full-quote conservation, local-repeat or idempotence assertion from
group05 was reached. The existing source paths preserve failures/reservations,
but this audit did not connect to the saved database to promote that code
argument into a new inspected-row result.

A fixture successor needs a provider allowance sufficient for that unchanged
16MiB reservation plus earlier retained actual response bytes.32MiB is a small
sufficient test cap here; client limits, actual tiny payloads and time envelopes
need not be enlarged. This does not require altering product route bounds.

## Disposition

Both fixture defects escaped prospective source review. The correct record is
failed controls01 with retained scoped successes, not full qualification. No
defect in the six product successors is demonstrated by these two errors.

Root may select a fresh, independently reviewed **04/05-only** control successor
using canonical policy-created contacts and an adequate finite provider cap.
The six passed groups, used original test, product sources and all evidence stay
frozen. No runtime, installation build or old operation renewal is authorized
by this note. Full v5 and installed genuine mathematical integration remain
separate unfinished obligations.
