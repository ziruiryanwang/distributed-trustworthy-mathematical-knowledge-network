# Retained-recipient continuation: source contract

This is one fresh continuation from actual02's preserved reader1 custody. It does
not relabel the failed actual02 operation or repeat its successful first-reader
discovery, mathematical admission or prior source authoring. Root owns exact
configuration and launch selection. No runtime pass is implied by this document.

## Why a continuation is necessary

Actual02's replica publication completed two local provider-record writes and
reported two query errors involving departed peers. The Node correctly called
that `INCOMPLETE/QUERY_ERRORS`; the harness incorrectly required zero query
errors before even trying discovery. A decentralized service must tolerate this
partial advisory publication. Its usefulness is decided by the later real route,
authenticated descriptor, formal search and independent mathematical admission.

The successor retains the Node result unchanged. Local provider-write count is
diagnostic, not a prerequisite for trying discovery: neither a positive count nor
zero proves remote usability or absence. The following exact source outcomes may
proceed to the already budgeted real discovery:

| Status / termination | Required corresponding fields |
|---|---|
| `HINT_DISPATCHED_UNACKNOWLEDGED / ITERATOR_EXHAUSTED` | Positive writes, zero query errors, null error, as specified by the retained Node source |
| `INCOMPLETE / QUERY_ERRORS` | Positive query errors, null error; zero or positive writes |
| `INCOMPLETE / NO_PROVIDER_RECORD_WRITE` | Zero query errors and writes, null error |
| `INCOMPLETE / ABORTED_OR_FAILED` | Exactly `TimeoutError: The operation was aborted due to timeout` or `Error: LOCATION_QUERY_EVENT_CAP`; writes may be zero |

The last row admits only the retained source's local per-operation timeout or
event allowance outcome. Its text-only exception interface cannot safely classify
arbitrary failures; all other caught errors, fatal IPC/channel outcomes, malformed
replies or dead/expired owners still refuse. The exact route key, advisory fields,
census shape and original live owner/channel/deadline bind every allowed outcome.
No extra grant, publication retry or deadline extension is introduced. None of
these outcomes proves remote storage; actual discovery must still succeed.

## Exact configuration change

Run the root-selected snapshot's `delta/network_continue.py` under the existing
bounded owner. Schema: `DMKN_V5_DELTA_RETAINED_CONTINUATION_V1`.

The exact top-level keys match [V2](network_actual02_api.md), except `packet` is
replaced by `retained_custody`, with exactly three `{path, bytes, sha256}` pins:

| Key | Fixed path beneath `experiments/v5-local-checks/delta-network-actual-02/evidence` |
|---|---|
| `recipient_result` | `reader1-result.json` |
| `packet_db` | `reader1-packets/delta-packets.sqlite` |
| `module_db` | `reader1-modules/modules.sqlite` |

Both SQLite files must be closed, without WAL/SHM/journal sidecars. They are
opened only with `mode=ro&immutable=1`, `query_only=ON` and a finite SQL-progress
allowance. Every source pin is checked before reading and after the operation.
All packet bytes come from the retained recipient database, not the old original
packet file. Every retained group/body is compared exactly with the acquired
packet's structurally committed semantics. The retained export is reconstructed
from its received group and must reproduce the reader1 formal record.

The report supplies lineage/selection bindings only. Its `admitted` flag, prior
journal and closed handles are never used to accept mathematics. A new receiving
domain must still perform its own real receipt verification and both native checks.

`location`, its fourteen-file Node map, both exact aliases, ports and limits are
unchanged. The original 480-second workflow sits within the unchanged 600-second
outer wall ceiling. The formerly used `reader1` port remains only a permitted
loopback address in the fixed seven-port schema; no reader1 node is created.
The snapshot includes both fresh sources and the frozen `network_actual02.py`
whose unchanged receiving/cleanup implementation is reused.

## Decisive sequence and accounting

1. Rebuild separate transient-origin and replica custody/index instances solely
   from pinned prior-recipient bytes. Do not reopen any prior origin store.
2. Start a neutral router and the transient origin. Start one fresh reader with
   only the neutral bootstrap and its local theorem/equality/fold query features.
3. Obtain an actual first route while the origin is alive and replica has not
   advertised. No mathematical acquisition has happened at this reader.
4. Close the transient origin's Node, HTTP and stores; then start the replica.
5. The same reader tries its genuinely stale public result, incurs the bounded
   typed descriptor miss, and spends its preallocated second route on the same
   channel/deadline. No replica identity or HTTP endpoint is preloaded.
6. Real formal discovery/acquisition supplies the candidate. The reader verifies
   one receipt and two native deltas, then reconstructs its ordinary import context
   from its own durable readback. Only afterward do expected-byte assertions run.
7. Close and recheck every owner. Preserve original failures and separately account
   for this operation. A finalization failure overrides a preliminary pass label.

There are four Node lifetimes and at most three concurrent Nodes; one fresh
mathematical recipient, at most one cryptographic and two native checks; zero
authoring, guest execution or proof-production calls. No successful old admission
is repeated as a substitute for the unreached suffix.

The resulting evidence, if positive, is explicitly **the actual02 reader1 prefix
plus a fresh retained-custody continuation**, not one uninterrupted successful run.
It is not independent-host evidence, global search completeness or final v5 release.
