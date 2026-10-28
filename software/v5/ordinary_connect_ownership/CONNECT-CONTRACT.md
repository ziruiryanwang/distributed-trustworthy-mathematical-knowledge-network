# Owned TCP connection contract

2026-10-28 source-only implementation of SELECTION.md. Candidate
`fair_exchange.py` SHA256
`05cf2b5baef0130dbe3b43e594d6c800baf6b625c77125dd3356f59f78509575`.
Predecessor `ordinary_sparse_access/fair_exchange.py` remains unchanged at
`89de88de6ddbc8a2d0aafb96aac150a8f5e7b550303fc9504f970e477ce16b71`.

The useful boundary is continuing to the next already selected contact feed
after a known unavailable-peer failure whose raw socket this attempt can close.
This implements the adopted TRANSPORT-FAILURE-DECISION; it does not infer which
failure caused registration-refresh-public01 or relabel that failed workflow.

## Ownership and outcomes

1. Perform existing endpoint/request/TLS setup and numeric-address construction
   within the original attempt horizon. Allocate exactly one TCP socket, set it
   nonblocking and await the public event loop's `sock_connect` under the existing
   absolute timeout context. No task, DNS request, retry or second socket is added.
2. Before stream handoff, only `ConnectionRefusedError`, `ConnectionResetError`
   or native/own-attempt timeout proposes `CONNECTION_REFUSED`,
   `CONNECTION_RESET` or `ATTEMPT_TIMEOUT`. Finally, close the still-owned socket
   and require both normal `close()` return and `fileno() == -1` before returning
   any such outcome. A close error or nonnegative descriptor is terminal
   `FAIR_RAW_SOCKET_CLOSURE_UNCERTAIN` with its cause retained.
3. Unknown local/connect failures stay terminal after attempted raw cleanup.
   External cancellation propagates as `CancelledError`; if raw cleanup also
   fails, that failure is chained to the cancellation. Only the timeout context
   translates its own cancellation into an attempt timeout. Concurrent external
   cancellation is not a settled refusal.
4. After TCP success, recompute the original remaining time. If exhausted,
   close the raw socket and return an attempt timeout. Otherwise set the transfer
   flag before calling/awaiting `asyncio.open_connection(sock=sock, ...)`.
   Preserve TLS context, exact server name, header limit and shutdown timeout;
   use only the newly remaining time as the TLS handshake timeout.
5. After that handoff, every no-writer exception stays terminal, including a
   refusal/reset/native timeout. Ordinary exceptions become
   `FAIR_STREAM_CLOSURE_UNOBSERVED` with their cause; cancellation propagates.
   The helper never closes the raw socket once it may belong to a transport.
6. Once a writer exists, the prior HTTP parser, peer-error classification,
   `writer.close()` and bounded `wait_closed()` path are unchanged. Existing
   writer-close failures remain `FAIR_SOCKET_CLOSURE_UNCERTAIN`.

Wire and return schemas, six refusal reasons, byte charges and grants are
unchanged. New diagnostic strings distinguish raw cleanup from uncertain
stream setup; no phase attribute or schema is added. The old failed workflow's
missing cause/errno/winerror/duration cannot be reconstructed from this change.

## Numeric IPv4 and IPv6

Parse the already validated host with `ipaddress.ip_address`. IPv4 uses
`AF_INET` and `(host, port)`; IPv6 uses `AF_INET6` and
`(unscoped_numeric_host, port, 0, scope_id)`. An absent scope is zero; an ASCII
decimal scope is its integer index; a named scope uses public
`socket.if_nametoindex`, a local interface lookup available on Windows. Require
the index to fit uint32. Invalid/missing interfaces fail before socket allocation.
This retains numeric and named scoped IPv6 without passing a '%' literal to
Windows ConnectEx or asking a hostname resolver to interpret it. Endpoint
acceptance, HTTP Host text and TLS server name remain unchanged. Interface names
and indices remain host-local, as they were before.

## Runtime premise and evidence limits

The newly created raw socket has no `SocketIO`/makefile reference. Under the
approved CPython/OS runtime, a normal raw close plus invalid descriptor witnesses
that the helper retains no live socket handle. Cancelling a Python future alone
does not provide that witness. Windows may still retain closed-socket OVERLAPPED
bookkeeping until its completion is received; neither this witness nor the old
writer `wait_closed()` proves a process-wide empty IOCP cache, absent queued
packets or instantaneous kernel work completion. No private proactor state is
read or changed. Local setup and close are not preemptively bounded CPU work.

The source argument inspected selected `D:/Python314/Lib` files: streams.py
26-51 (writer after create_connection), base_events.py 100-149 and 1012-1236
(numeric resolution, failed-connect and stream/TLS cleanup), proactor_events.py
103-173 and 725-728 (scheduled transport close and public sock_connect),
windows_events.py 49-94, 577-607 and 718-825 (ConnectEx/cancellation bookkeeping),
socket.py 503-511 (native close without SocketIO references), and timeouts.py
95-140 (own versus external cancellation). selector_events.py 625-653 preserves
the constructed numeric tuple through its no-DNS numeric fast path.

Source hashes retained for the core ownership argument:

- streams.py: `a45afc8e3e4480879d8e63f7fb567bd77825b453792bc1ca0419c7669d29f366`
- base_events.py: `da597bc24e06382d9ef836d84d0e383ad1f6fd61d3b1fb1bfd2bd50d359f97b0`
- proactor_events.py: `edfe546a07074ed405ca7e7e27e7810082a17d419e00576db2445a672749020c`
- windows_events.py: `45b694f5dedd06d91ab749ac85291b771a45c00bd195285c66f0bd92ab5ce2b5`
- socket.py: `cbe54d58421e90d7dcae9a18045db90d987bccc56f87ed0fc22ea718784157c2`
- selector_events.py: `f4a52017fadd42996267db676bfa716dec9fd3085e9205c19f20c7384ad25ddc`
- ipaddress.py: `3fc3d0f8276914c9c6538568fbdea52645f7fd74bb9aaf62fe5759f34850eb68`

These source observations retain the approved-runtime/protected-storage premise;
named runtime pins do not attest the complete standard library or native OS.
Per-attempt added work/storage is constant and independent of corpus size.
No imports, controls, sockets, owner access, native build or Git operations were
executed for this implementation. Root selects packaging and finite validation;
the independent reviewer owns the new ownership-boundary controls.
