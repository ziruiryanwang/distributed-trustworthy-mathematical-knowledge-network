# Pre-handshake admission and prompt provider shutdown

2026-10-25 root selection. Full v5 remains active and unfinished. This is a
fresh source successor; all sparse/network-kit/bundle sources and used evidence
remain unchanged. Canonical root only; no shared research or paper edits.

## Concrete obstruction

The current `ordinary_sparse_access/http_provider.py` bounds HTTP handlers only
after `asyncio.start_server(..., ssl=...)` completes TLS. Pending TLS handshakes
therefore consume accepted-socket state before `max_connections` applies.
`backlog=16` bounds a different queue. Also, `stop` awaits server closure before
cancelling tracked handlers; Python 3.14 waits for client closure there. A slow
client can delay shutdown until its operation timeout, beyond a shorter cleanup
reserve. These are service availability/lifecycle defects, not proof soundness.

## Selected remedy and invariant

Select source-only repair of that transport in this directory. Reserve and
track a bounded raw connection before TLS/HTTP processing; charge failed
handshakes and other accepted attempts against a finite lifetime allowance.
Stop accepting first, cancel/close owned connections, then await their closure.
The existing outer process/resource supervisor remains necessary. No promise
of immunity to network saturation, OS resource exhaustion, or hostile local
processes follows.

For configured connection bound K, the implementation must maintain at most K
owned processing slots including handshakes, application work and cleanup.
There must be no unbounded accepted-task queue outside those slots. A bounded
OS listen queue is separate. Reuse `max_requests` conservatively as a total
accepted-attempt ceiling as well as the existing HTTP request ceiling; do not
introduce silent retries or new optional settings. Expose the distinction in
status. Preserve HTTP grammar/routes, TLS authentication, byte caps, one-request
semantics and mathematical acceptance. Preserve original service and cleanup
deadlines; do not fund extra time after cancellation.

Root selects synchronous nonblocking `socket.accept()` in one asynchronous
accept owner. Only a would-block result waits 10 ms before another check. This
avoids the selected Windows runtime's hidden AcceptEx socket/cancellation
ownership problem; acceptance, charging and registration have no intervening
await. There is at most one idle accept owner plus K occupied connection slots,
not an accepted-client task queue. Tradeoff: roughly at most 100 idle would-block
wakeups per second and up to one polling interval of additional arrival detection
delay before scheduler delay; this is not a hard latency guarantee. Unexpected
accept failures stop admission. Do not add a complex hidden accept-task framework
merely to avoid this small explicit supported-profile cost.

## Ownership and decisive evidence

- `search_locality_argument`: new `http_provider.py` and `IMPLEMENTATION.md`;
  exact-copy predecessor before patching, record changed functions/invariants.
- `ordinary_routing_gap`: source challenge and finite test harness/plan, disjoint
  from provider implementation. Review raw-socket ownership transfer and all
  cancellation/error paths against the supported Python 3.14 runtime.
- Root: selection, adoption, eventual exact finite runtime, packaging and Git.
- `execution_consent_review`: file-only `assemble.py`, exact-compatible
  `prepare_selected.py`/`compatibility.json`, README and execution-trust addendum.
  No native/loader-role change or edit to the frozen earlier source ZIP.

No execution is selected yet. Before running, root will review the source and
bounded test plan. Necessary evidence is a real loopback TLS stall under a small
cap, a prompt HTTP/TLS shutdown with unfinished clients, and an unchanged positive
route; selected failure/cancellation controls may use explicitly labelled doubles.
Do not rerun mathematical, sparse-search, custody, native build or certificate
campaigns. Tests must preserve failures, close all processes/sockets, and stay
within one small original resource envelope. Stop if the proposed change needs
an unbounded new framework; reconsider the simpler service restriction instead.
