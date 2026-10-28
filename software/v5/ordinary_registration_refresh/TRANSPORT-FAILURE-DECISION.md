# Closed-feed failure: own the TCP socket before transferring it to asyncio

2026-10-28. operable_scale_decision. Source/saved-output diagnosis only; canonical
guard passed. No execution, retry, network, owner/native operation, used-source
edit or Git. This selects an implementation direction for root, not a launch.

## Decision

**A narrow pre-transfer TCP ownership fix is justified and implementable.**
Create and retain the numeric TCP socket explicitly, await `loop.sock_connect`
inside the existing absolute attempt deadline, and confirm closure of that owned
socket before treating a known connect failure as settled. Only after successful
connection transfer it to the existing `asyncio.open_connection(sock=..., ssl=...)`
stream/TLS path. Keep no-writer failure after that transfer conservative and
terminal. Do not broaden the current `open_connection` exception catch.

This addresses a real unavailable-feed resilience limit: one unreachable feed
can currently abort the whole refresh/search despite unused budget and reachable
alternatives. It requires no mathematical changes, new wire protocol, TLS stack
or background retry. The current terminal behavior is deliberate conservatism,
not evidence of a leaked socket or broken registrar cutoff. Its observable
ownership boundary is nevertheless too coarse for ordinary unavailable TCP
endpoints, including the actual stopped-directory episode.

## What public01 actually establishes

The saved suite failed with `UnsettledTransportError` /
`FAIR_CONNECT_CLOSURE_UNOBSERVED` after its first valid contact read and natural
registrar closure. No second cycle ran. The first public refresh result remains
successful within its scope: one allowed endpoint, one scope rejection,
`INCOMPLETE_REFRESH_SERVICE_FINISHED`, both service/outer `quiescent:true`, no
cleanup errors, provider active/handshake/cleanup-pending counts zero, and no
reserved reply bytes. The suite also records both children reaped and no observer
cleanup errors or learned-endpoint dials.

The suite calls `X.exchange` on the closed registrar port with a 2-second attempt
and requires `CONNECTION_REFUSED`. It records the reader row only **after** the
await. On the thrown failure it preserves neither the underlying exception
type/errno/winerror nor that attempt's start/duration. Therefore the saved output
cannot distinguish a connect reset from a connect timeout; both reach the same
wrapper error. Do not invent a particular Winsock error or claim a proven leak.
The failed overall result remains failed; the successful prefix is not rewritten.

## Selected source explains the distinction

`ordinary_sparse_access/fair_exchange.py:64-151` is unchanged in the assembled
package (SHA-256 `89de88de6ddbc8a2d0aafb96aac150a8f5e7b550303fc9504f970e477ce16b71`).
It accepts ConnectionRefusedError while opening a stream. Reset/timeout before a
writer exists is fatal; acquired-stream failures settle only after close plus
successful bounded `wait_closed`. The 2026-10-17 SEARCH-RESILIENCE-REVIEW and
2026-10-20 ACQUISITION-RESILIENCE-REVIEW explicitly document that restriction.
The 2026-10-25 SEARCH-BOUNDARY preserves it. This is not a newly introduced
registration-refresh regression.

Read-only inspection of the selected `D:\Python314` distribution shows:

| Source | Ownership/cleanup fact |
| --- | --- |
| asyncio/streams.py:26-51 | `open_connection` awaits the complete `create_connection` and only then constructs/returns a StreamWriter. No writer does not identify which internal phase failed. |
| asyncio/base_events.py:1012-1056 | `_connect_sock` owns a newly created raw socket, awaits `sock_connect`, and closes the socket on every exceptional exit. Close OSError is suppressed, so callers do not observe its close result. |
| asyncio/base_events.py:1196-1236 | After TCP connection, transport/protocol construction and optional TLS run. On waiter failure it calls `transport.close()` and raises; it does not await that transport's closure. |
| asyncio/proactor_events.py:725-728; windows_events.py:577-607 | Windows `sock_connect` awaits IOCP ConnectEx through an overlapped future. No stream transport is needed at this phase. |
| windows_events.py:49-94,718-747,765-825 | Future cancellation requests cancellation of the overlapped operation. Completion bookkeeping may remain in the proactor cache until IOCP notification; cancellation failure is reported to the loop. |
| proactor_events.py:103-112,134-173 | Transport close can schedule `connection_lost` and cancel I/O before the socket is finally closed in that callback. Merely calling transport.close is not the same observation as completed stream closure. |

Thus blanket conversion of all no-writer timeouts/resets to settled refusals
would conflate raw TCP failure with asynchronous transport/TLS teardown. Reading
`_connect_sock` alone is insufficient justification for that change.

## Smallest corrected ownership boundary

Use a fresh successor of fair_exchange, preserving its public return type,
absolute-deadline narrowing, settled HTTP codec and conservative external charges.

1. Validate the existing endpoint and build local TLS context before allocating
   the socket, as today. Construct exactly one nonblocking numeric TCP socket
   of the appropriate address family; no DNS, duplicate handle, makefile, shared
   stream, spawned task or new allowance is introduced.
2. While the helper still exclusively owns that socket, await the public
   `loop.sock_connect(sock, numeric_address)` under the original timeout.
   Keep a clear ownership/phase flag rather than inferring phase from writer=None.
3. On a known refusal/reset/native timeout, or the helper's own attempt timeout
   during this phase, synchronously close the owned socket. Require close to
   return normally and `fileno() == -1` before returning an existing
   SettledRefusal reason: `CONNECTION_REFUSED`, `CONNECTION_RESET`, or
   `ATTEMPT_TIMEOUT`. Keep the existing FairSearch refusal vocabulary; no new
   status/schema or caller recovery-policy change is needed. Close error or
   failed closure observation is terminal.
   External cancellation and unknown/local errors still propagate after attempted
   cleanup; no broad OSError recovery or exception-string matching.
4. After TCP success, recheck remaining original time. Transfer that connected
   socket to the existing stream constructor using its `sock` parameter, with
   the same selected TLS context/name and remaining handshake deadline. Do not
   supply host/port again or let it create another connect attempt.
5. After transfer, keep no-writer reset/timeout/TLS failures fatal unless a
   separate future design obtains an actual close witness. Once the writer is
   returned, retain the current close plus bounded wait_closed rule. A raw
   Python reference to a transferred socket is not permission to bypass stream
   ownership or to pretend its asynchronous transport is closed.

Ownership transfer and every exception path need source review before execution.
In particular, a failure while entering stream setup cannot accidentally fall
back into the pre-transfer settled branch. All failed attempts remain charged;
the caller may try a later selected feed only within the same original envelope.
Neither the repair nor a failed request grants another attempt automatically.

## What confirmed socket closure means on Windows

For the new raw socket there are no SocketIO/makefile references. The selected
`socket.py:503-511` close path therefore calls native socket close rather than
deferring it behind file wrappers. A normal close return plus invalidated file
descriptor, under the trusted CPython/Windows socket contract, establishes that
the helper no longer owns a live socket on which to connect/send/read. Closing
also handles the race in which ConnectEx completed while its waiter timed out.

Cancellation is not itself the closure witness. `_OverlappedFuture.cancel`
requests cancellation, but may finish its Python future before Windows posts
completion. The helper must still close the exclusively owned socket and check
that result. IOCP may retain the closed socket/OVERLAPPED bookkeeping until its
completion notification; this is managed by the same trusted event loop. The
proposal does not promise that every kernel completion or queued packet has
already disappeared. Even the current writer.wait_closed path is not an assertion
that the process-wide IOCP cache is empty.

No extra background socket owner or task survives the helper's settled return.
Bounded attempted slots and the existing outer Job still bound the operation;
event-loop/OS cancellation/closure defects remain execution-premise failures,
not something a new catch can prove away. If the required guarantee were full
IOCP-cache drainage before every next dial, the current transport would need a
different contract too; do not silently claim it here or manipulate private
proactor caches. This repair observes the same meaningful local resource boundary
more directly before transport creation.

The inspected runtime files are evidence for the selected local implementation.
Existing named runtime pins are not a hash commitment to every stdlib file; the
complete approved-runtime/protected-storage premise remains explicit.

## Test expectation and smallest consequential evidence

The closed-port probe's exact `CONNECTION_REFUSED` expectation is too strong:
being closed does not promise which Windows error is reported within two seconds.
A future successor probe should accept only one of the explicitly supported
**settled pre-transfer** failure outcomes, require no successful contact reply,
and preserve cause/phase plus duration when an unexpected failure escapes.
It must not accept UnsettledTransportError as a settled successful continuation.
Provider quiescence already supplies independent evidence for the completed
first registrar cycle; a second probe must not relabel its old failed suite.

Source review should cover raw-socket success/transfer, timeout/reset/refusal with
confirmed close, close failure, external cancellation, and failure after transfer.
The smallest actual later check is one Windows closed/unreachable selected feed
followed by one available selected feed in the same finite budget, with observed
socket cleanup and preserved charges. Use a fresh selected source/package and
new output. No theorem, owner, native build or replay of already passing refresh
behavior is required to decide this changed transport seam.

Keeping the old transport and weakening only the harness would leave the real
unavailable-feed problem unresolved. Broadly rewriting TLS/stream ownership is
unnecessary for the demonstrated pre-connect gap. Root can select the narrow
successor after this principle decision; no code or runtime is selected here.

## Evidence identities

- Suite `registration-refresh-public01/suite/RESULT.json`:
  `91c11d1217b242cdc670fedc254054ced092837eac3abceaf7fd5110af86df94`.
- Cycle-1 `directory-refresh-serve-public/RESULT.json`:
  `8ba105ccdb83630d4e418446080b7f46b6aa9ade7896d89433b64ff721360258`.
- Inspected asyncio/streams.py:
  `a45afc8e3e4480879d8e63f7fb567bd77825b453792bc1ca0419c7669d29f366`.
- Inspected asyncio/base_events.py:
  `da597bc24e06382d9ef836d84d0e383ad1f6fd61d3b1fb1bfd2bd50d359f97b0`.
- Inspected asyncio/proactor_events.py:
  `edfe546a07074ed405ca7e7e27e7810082a17d419e00576db2445a672749020c`.
- Inspected asyncio/windows_events.py:
  `45b694f5dedd06d91ab749ac85291b771a45c00bd195285c66f0bd92ab5ce2b5`.
