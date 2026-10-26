# Pre-TLS transport admission: source checkpoint

Status: **SOURCE ONLY, independent challenge in progress**. No imports, tests,
network, database, build, package, mathematical operation or Git work was run by
the provider author. Root owns finite runtime selection and product adoption.

## Existing obstruction and exact successor

The sparse predecessor starts TLS inside `asyncio.start_server` before its
application callback applies `max_connections`. Its `stop` also waits for
`Server.wait_closed` before cancelling application handlers; supported Python
3.14 waits for client connections there. Thus handshakes escape the application
cap, and a stalled client can defer cleanup until its longer operation timeout.

The predecessor `ordinary_sparse_access/http_provider.py` was checked at 20,766
bytes, SHA-256
`f81cdcaebbf05ad97342b81ac64444b33695b576045c8da41ba6f0a0903dd691`, then copied
exactly to this fresh sibling before applying source patches. Frozen predecessor,
network kit, bundle and evidence bytes are not edited.

## Ownership invariant

Let K be `max_connections` and R be `max_requests`. On the supported single
event-loop execution, the selected implementation maintains:

1. At most K `_Connection` records exist. A record is reserved synchronously
   after a successful nonblocking `listener.accept`, before any TLS conversion,
   and remains occupied through handshake, HTTP work and cleanup.
2. One accept-owner task exists separately from those K connection workers.
   There is no accepted-socket/task queue outside the records. When K records
   are occupied, the owner waits for capacity without accepting another socket.
   The bounded OS listen backlog of 16 is a different queue.
3. Every accepted socket is charged once before TLS: `accepted_attempts <= R`.
   Failed handshakes and failed task setup do not refund this charge. At R the
   listener closes; existing admitted clients retain their existing bounds.
4. A connection record is reusable only after its retained raw socket reports
   `fileno() == -1` AND its worker task is done. Task exit alone is insufficient.
   A worker cancelled before its first coroutine step has its raw socket closed
   by an already-registered completion callback.
5. Closure uncertainty retains the record and task in supervision and halts
   admission. It is not reported as a free slot or quiescent service.

The accept owner uses synchronous nonblocking `accept`, yielding 10 ms only on
would-block. This avoids the Windows `sock_accept` / AcceptEx hidden socket and
completion-versus-cancellation ownership boundary. Busy acceptance has no polling
sleep; nominal added idle detection delay is at most 10 ms **excluding scheduler
delay**. This is not a latency, fairness or availability guarantee. An unexpected
accept error stops admission; it does not trigger an error-retry loop.

## TLS and shutdown

Raw accepted sockets are handed directly to `loop.connect_accepted_socket` with
the selected TLS context. No plaintext stream is read or upgraded, so an early
ClientHello cannot be consumed by an application reader. `_OwnedProtocol` records
the application transport in its post-handshake `connection_made` callback. This
covers cancellation after handshake completion but before the waiter resumes.
Failed handshakes can omit application protocol callbacks entirely; cleanup
therefore observes the retained raw socket rather than a writer-close future.

`stop` closes the listener, aborts known transports and cancels every tracked
worker plus the accept owner **before its first await**. One absolute one-second
cleanup deadline is saved and never extended by repeated stop/cancellation.
Any earlier connection cleanup deadline remains earlier. Ordinary graceful
connection cleanup also retains the predecessor's one-second limit. An outer
service/cleanup deadline and process supervisor remain authoritative.

The original TLS handshake maximum remains 5 seconds, and the HTTP operation
deadline remains `operation_ms` starting after connection establishment. Existing
HTTP grammar, routes, request/body/response bounds, reservations, one-request
semantics, endpoint/TLS authentication and mathematical acceptance are unchanged.
No new request budget, cryptographic trust rule or automatic retry is added.

Python cancellation of the connection waiter closes its transport; during the
handshake this aborts underlying I/O. After successful TLS establishment a known
transport can be aborted directly. If the runtime unexpectedly fails before
returning any transport and fails to close its handed-off raw socket, the record
is retained, admission stops and quiescence fails. This code does not manipulate
private asyncio fields or pretend to recover from arbitrary runtime failure.

## Changed implementation surface and status

Changed functions: Provider initialization/start/stop, `_serve` ownership shell,
and status. Added `_Connection`, `_OwnedProtocol`, a bounded accept owner, worker
setup/cleanup and completion/reaping helpers. Dispatch, HTTP codecs, client
exchange and mathematical roles remain unchanged. `server` is now the raw
listener, retaining `.close()` for the existing outer fallback. `tasks` includes
the accept owner as well as workers and retains unresolved cleanup ownership.

The original `requests` remains the count of HTTP handlers begun, not parsed
successful requests and not TLS attempts. New `accepted_attempts` counts socket
acceptance; `handshakes`, `handshake_failures`, `accept_failures`, `cleanup_pending`,
`cleanup_failures`, `accepting` and `admission_exhausted` expose distinct lifecycle
facts. `active` counts occupied connection records, including cleanup, not the
separate accept-owner task. The old `refused` is not a measurement of OS backlog
refusals or unaccepted traffic.

## Runtime reasoning sources

The actual supported files under `D:\Python314\Lib\asyncio` were inspected as
text, not imported or executed:

| File | Relevant behavior | SHA-256 |
|---|---|---|
| base_events.py | 1210-1234: connection waiter exception closes transport; 1671-1694: accepted-socket transfer | `da597bc24e06382d9ef836d84d0e383ad1f6fd61d3b1fb1bfd2bd50d359f97b0` |
| sslproto.py | 393-430: failed handshake need not notify app; 612-636: close during handshake aborts; 671-674: raw transport force-close | `4b824f705e7c6c0a431d8b1154e9c3ca88128b6b37d07a795ad4f013b65d6f18` |
| proactor_events.py | 135-172: abort cancels I/O; connection-lost closes the same raw socket | `edfe546a07074ed405ca7e7e27e7810082a17d419e00576db2445a672749020c` |
| windows_events.py | 549-574: AcceptEx creates a hidden accepted socket and cancellation helper | `45b694f5dedd06d91ab749ac85291b771a45c00bd195285c66f0bd92ab5ce2b5` |
| streams.py | 180-280: reader protocol and post-handshake connection callbacks | `a45afc8e3e4480879d8e63f7fb567bd77825b453792bc1ca0419c7669d29f366` |

These are supported-runtime premises, not a formal proof of Python, TLS or OS
correctness. Handshake bytes/CPU and OS/network queues remain real extra costs.
The cap does not prevent network saturation, unfair clients, OS exhaustion,
hostile local processes or synchronous event-loop stalls. This repair supports
bounded service ownership; it is not worldwide deployability or growth evidence.

Independent source review and the separately authored finite stalled-TLS,
unfinished-HTTP shutdown and unchanged-positive-route controls remain required.
No execution result or final-v5 completion is claimed here.
