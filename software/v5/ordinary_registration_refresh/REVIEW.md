# Contact refresh: independent changed-boundary source review

2026-10-28. growth_design_audit. **PASS for the selected API and Provider source
boundary, subject to the separately selected controls and integration.** No
product imports, tests, runtime, owner/database access, network, Lean or Git
operation occurred. Root owns assembly, execution and adoption. Wrapper review
is separately owned; this review does not repeat it or the old protocol suite.

| Selected input | SHA-256 |
| --- | --- |
| peer_api.py | 12c29d1edb3f3bc0483d9fe01abb3a4c69dbc4cdc5225ead32c28842bb4699dc |
| http_provider.py | 3ce581f4057b6694c6d99a697847984fe7431a695989018f3e179217712859a2 |
| REFRESH-CONTRACT.md | 08bd691593d9924a47caaa8bdba625048ed570b9037d24b2969828d69e9fc33b |
| CUTOFF-CONTRACT.md | e18cd1358ca92b40fc54efc868b4817bb49495c6d699fd9396e35f9d4f649cce |

The comparison is against the deployed ordinary_multi_source peer API and
ordinary_reply_capacity Provider selected by ordinary_name_directory's map.
No deferred pattern source is needed. Review used exact source diffs and the
reused budget/contact/exchange definitions at the changed call boundaries.

## The selected composition has an explicit authority boundary

Local configuration fixes feed origins, TLS pins, exact routes, per-feed endpoint
scopes, egress policy and finite allocations. Feed replies cannot replace that
configuration. `_refresh_plan` validates the whole selected plan before requests:
1..8 feeds, 1..32 unique feed/compiled-route slots, complete request/byte capacity,
all required scopes, service configuration and server TLS input loading. Its
per-route sum of contact quotas is at most 16.

Consequently, for any compiled route r,

    |union of accepted endpoints for r|
      <= sum of returned counts for its slots
      <= sum of preapproved slot quotas for r <= 16.

Deduplication only reduces this size. This avoids arrival-dependent silent
eviction. The finite 32-slot plan also fits the older 2,048-route map limit;
the existing ContactMap parser independently enforces the final representation
and byte bounds. Correct source admission does not imply operator independence,
endpoint ownership, current reachability or useful mathematical coverage.

The registrar dials only the preselected feed endpoints. The names/IPs/ports in
accepted hints are compared with local egress and feed scope, then copied into
the immutable advisory map; they are never dialed by this operation. Approved
TLS names allow selected public-IP changes without accepting peer-selected CA
paths. A future reader still makes its own certificate/egress decision.

## Outcomes preserve distinctions that affect continued operation

Only fresh nonce-bound replies from this invocation are eligible. The function
has no persistent map argument, saved-map read or previous-slot fallback. A slot
therefore cannot retain a former endpoint after an explicit fresh empty answer.
Its absence also cannot erase another slot's successful endpoint.

The implementation distinguishes valid empty untruncated responses, empty
truncated responses, nonempty advisory responses, malformed reply bindings,
HTTP refusals, settled unavailable sources, absent legal attempt time and
insufficient remaining horizon. Rows outside policy are filtered with rejected
counts. Even when every row is rejected, the slot remains a rejected nonempty
response rather than becoming a successful empty withdrawal.

Accepted slots are rechecked at map assembly. `included` is separate from the
earlier `adopted` count, so a subsequently expired slot can retain diagnostic
counts without contributing an endpoint. `refresh_complete` requires every
selected slot to have survived assembly without truncation or rejection. It is
not global completeness. Empty union returns without a Provider/listener; a
nonempty partial union remains explicitly incomplete in READY and the terminal
report. Fatal pin, outer-budget or unconfirmed-cleanup failures remain fatal,
rather than being mislabeled as ordinary source unavailability.

## Budget lifetime is consistent across refresh and service

The complete refresh request/byte allowance is externally prepaid once. Each
slot is attempted at most once; per-slot reported reservations and actual HTTP
bytes are distinct from that aggregate prepayment. No retry or refund enlarges
the grant. Request creation occurs after the entire plan is validated.

For a caller-owned `OrdinaryBudget`, `_network` requires its exact type and no
pending ticket, narrows its deadline and reuses it. `charge_external` additionally
checks the preallocation phase, unique label and remaining aggregate capacity.
An already spent or duplicate allocation therefore refuses before exchange.
The caller-owned budget stays open; the operation does not claim authority to
close or renew it. Its deadline may have narrowed even if a later prepayment
check fails, consistent with the existing nonrenewing boundary.

An operation-owned budget is closed on all normal and exceptional exits. Its
deadline is the refresh slice, which reserves cleanup and the requested minimum
service time from the original allowance. Serving may legitimately continue
beyond the refresh slice because no refresh I/O occurs then. `OrdinaryBudget.close`
checks pending requests, not current time, so expiry after completed refresh does
not itself break closure. A supplied shared budget can be expired on return and
cannot be reused merely because its `closed` flag is false. The original outer
allowance and Provider's separate finite service quotas still govern serving
and cleanup. No budget grant is silently extended.

## Issuance and readiness use the clipped deadline

Each slot horizon comes from local monotonic request start and the original
allowance; a peer timestamp or service restart cannot refresh it. The earliest
included nonempty-slot horizon is passed to internal `directory_serve`, which
clips it again to the chosen service lease. Provider receives this clipped end,
not a longer raw advertisement horizon.

Review found and the author corrected a narrow READY ordering problem: the final
prepublication check now compares the required remaining interval with the
**clipped lease end**, rather than checking only the raw contact horizon. The
function constructs a local ready value, checks that condition, and only then
assigns `report.ready` and invokes the callback. A slow Provider start refuses
with `REFRESH_START_TOO_LATE`, leaves READY absent and follows bounded cleanup.
The selected source hash above includes this correction. No failed execution
was rewritten; these were unused source drafts.

For contacts with a cutoff, direct `dispatch` checks it before, throughout and
after reply construction, composing any caller budget check. HTTP dispatch also
combines the ordinary operation deadline with it. Header/body writers check
immediately before every enqueue and after every awaited drain. A header drain
crossing the limit cannot enqueue a new body afterward. Charges are made before
sending and remain conservative after interruption; finally releases the pending
reservation. Default None and noncontact paths preserve their prior handling.

This is a checked application boundary, not hard real-time scheduling between
check and write. It cannot revoke bytes already queued or shorten the existing
reader's separate contact horizon. A post-final-drain error can occur after a
complete response was queued. The contract states those limits rather than
claiming instantaneous global expiry.

## Minimal prospective controls

`control_tests.py`, SHA-256
`189489066a798bb46ef40817a1586e48ff974af46c9741a431f88d5b0421c2d0`,
contains twelve prospective groups, not twelve passing results. Static AST
parsing succeeded without importing or executing it. Root must select a
coherent package and bounded run before any execution.

The controls use the real selected API, contact parser and budget implementation,
with scripted exchange replies and an async service-capture double. Provider
HTTP tests use an in-memory StreamReader/writer and injected monotonic clock.
They cover:

1. Per-route quota, duplicate slot, total reservation and scope errors before I/O.
2. Shared-ledger prior charges, ownership, unchanged/narrowed deadline and
   aggregate/duplicate-allocation refusal.
3. Fresh endpoint replacement, successful empty withdrawal and no cached fallback.
4. Empty/truncated/malformed/HTTP/unavailable outcomes, retained charges and no listener.
5. Partial union, deduplication and one source's inability to withdraw another's row.
6. All-out-of-scope responses remaining rejected rather than valid empty.
7. Earlier-slot aging during later legal requests, and no legal attempt slice.
8. Finite cutoff validation, caller-check composition, direct expiry, post-reply
   expiry and noncontact compatibility.
9. Expiry before HTTP header enqueue and across header drain, with retained charges.
10. Writer chunk-boundary recheck after a drain.
11. None preserving the earlier contact response/write path.
12. A late Provider start under a shorter clipped lease suppressing READY and cleaning up.

The multi-chunk writer case is a lower-level helper control; legal contact reply
bodies are at most 32 KiB and do not themselves require a 64-KiB second chunk.
It is not represented as a larger supported contact response. Scripted exchange
time advances are checked against their actual selected attempt deadlines.
No artificial network timeout is presented as independent transport evidence.

The source selects no sockets, database, owner, subprocess or native calls during
the actual test coroutines. Event-loop setup may create its internal wakeup
socket before application socket guards are installed. The local package loader
verifies the selected software/runtime attachments; this is not mathematical
admission. A successful future control run will establish these injected seams,
not live loopback composition, public TLS operation or independent hosting.

One later bounded public loopback composition, if root selects it, should test
the actual refresh/listen/client boundary using existing metadata. It need not
rerun any theorem, directory parser, cryptography or broad old transport campaign.
