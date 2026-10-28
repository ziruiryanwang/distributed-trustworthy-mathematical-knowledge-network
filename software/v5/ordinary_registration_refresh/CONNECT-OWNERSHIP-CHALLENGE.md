# Independent challenge: explicit TCP socket ownership

2026-10-28, growth_design_audit. Source/theory only; no execution or rerun.

**The minimal split is defensible under the existing trusted CPython/Windows
runtime premise.** It supplies an observable local socket-close boundary for
failed TCP attempts without claiming that arbitrary failed TLS setup is settled.
I independently inspected the selected stdlib and current fair_exchange source.
This is agreement on the principle, not approval of an unseen implementation.

## Ownership argument

Let `R` mean a newly allocated, exclusively owned, nonblocking TCP socket with
no duplicated descriptor or file wrapper; `T` mean the socket has been offered
to stream construction; `W` mean a StreamWriter has actually been returned.
The permissible transition is `R -> connected R -> T -> W`. Set the transfer
phase **before** awaiting stream construction; never infer raw ownership just
from `writer is None`.

For a known error in `R`, normal synchronous `socket.close()` return followed
by `fileno() == -1` is a sufficient local ownership witness: the helper has no
live socket on which to continue the attempt. The descriptor check alone is
insufficient if close raised. Unknown/local errors and external cancellation
still propagate after attempted cleanup. Constructor/setup errors must not leak
a socket allocated before the error.

The selected `proactor_events.py:725` delegates `sock_connect` directly to the
proactor. `windows_events.py:577` uses ConnectEx and returns its overlapped
future; no stream transport exists in this phase. Cancelling the await cancels
that future, whose cancel method requests overlapped cancellation. Its cache may
retain the closed socket object and OVERLAPPED until a completion notification.
For cancelled/done futures, the later poll skips the normal connect callback.
No independent application task or duplicate socket is created by this path.

Thus cancellation itself is **not** the close witness. The subsequent owned
socket close is essential, including the completion-versus-timeout race. This
does not prove immediate IOCP-cache drainage, absence of in-flight packets, or
an OS-level hard close latency. Those stronger claims are unnecessary here and
are not established by the existing writer.wait_closed path either.

In `T`, stream creation can already have installed a transport before failing.
`base_events.py:1210` closes such a transport on waiter failure without awaiting
its completed closure. No-writer failure in `T` therefore remains terminal,
including ConnectionRefusedError; do not keep the old special-case recovery at
this new phase. A remaining raw Python reference is not a second owner permitted
to pretend transport cleanup finished. In `W`, retain close plus bounded
wait_closed and its existing fatal-uncertain-closure rule.

## Time and cancellation requirements

Use the existing original absolute deadline for TCP, stream/TLS setup and
response, with no renewed attempt allowance. Recompute remaining TLS handshake
time after TCP success. If no original time remains before transfer, close the
still-owned socket and return only the established timeout disposition.

CPython's timeout context records the task cancellation count on entry and
converts its own cancellation only when no additional cancellation request has
intervened (`timeouts.py:95-125`). Do not catch CancelledError and classify it
using `timer.expired()` alone: an external cancellation may coexist with expiry.
Let the context distinguish its own timeout; keep external cancellation terminal.
If cleanup also fails, retain the failure/cause rather than returning a refusal.
Native TCP TimeoutError is distinct from timeout-context expiry but may use the
same existing refusal label after raw closure. Unknown OSError is not a known
unavailable-peer classification.

## One compatibility detail to resolve in source

Choose AF_INET or AF_INET6 from the already validated numeric endpoint. IPv6
uses a numeric address tuple with flow/scope fields; never silently discard an
accepted zone identifier. `Endpoint.validate` uses ipaddress, which permits
scoped IPv6, whereas base_events' previous numeric fast path explicitly declines
`%` and may use address resolution. A bypass must preserve supported numeric
scope handling or explicitly reject an unsupported scope as a local validation
failure before allocation. This is a source obligation, not a reason to add DNS
or broaden the TLS rewrite. Passing both host/port and sock to stream creation
is invalid; use only sock plus the unchanged explicit TLS name/context options.

## Consequential controls

Inspect the final implementation, then exercise only its new ownership states:
successful transfer without another connect; refusal/reset/native and own-timer
timeout closed before return; failed close/invalid descriptor observation;
unknown errors and external cancellation; every no-writer post-transfer error;
and unchanged writer close/wait behavior. Test doubles must preserve the global
socket.socket class so Windows loop creation remains valid. A selected real
closed/unavailable feed followed by a usable feed addresses the platform boundary;
no mathematical replay or broad transport campaign follows from this change.

## Inspected runtime identities

| File under `D:/Python314/Lib` | SHA-256 |
|---|---|
| `asyncio/windows_events.py` | `45b694f5dedd06d91ab749ac85291b771a45c00bd195285c66f0bd92ab5ce2b5` |
| `asyncio/proactor_events.py` | `edfe546a07074ed405ca7e7e27e7810082a17d419e00576db2445a672749020c` |
| `asyncio/base_events.py` | `da597bc24e06382d9ef836d84d0e383ad1f6fd61d3b1fb1bfd2bd50d359f97b0` |
| `asyncio/streams.py` | `a45afc8e3e4480879d8e63f7fb567bd77825b453792bc1ca0419c7669d29f366` |
| `asyncio/timeouts.py` | `afdf711a5f5e8040f47cbf0f2b4090bf99593f3ca85f13b1dc57ef49170e248c` |
| `socket.py` | `cbe54d58421e90d7dcae9a18045db90d987bccc56f87ed0fc22ea718784157c2` |

These read-time identities document the argument; the existing executable pins
are not a new commitment to every stdlib byte or a proof of the native OS.
