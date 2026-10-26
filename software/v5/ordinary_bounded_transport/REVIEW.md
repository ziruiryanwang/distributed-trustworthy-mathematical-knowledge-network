# Independent source review: bounded transport successor

2026-10-25. Disposition: **SOURCE PASS for the selected finite controls and
file-only integration, not an execution result or release adoption.** The
reviewer authored the direct transport tests; the provider author independently
reviewed those tests. Root owns execution, source snapshots, actual-outcome
adoption and Git. No product import, database open, socket connection, build,
certificate generation or test execution was performed during this review.

## Exact reviewed boundary

| File in this directory | Bytes | SHA-256 |
|---|---:|---|
| http_provider.py | 29560 | `9288996fa1d4e737f500043cddfc1c7935d9b7830ac6638596b6f7f278f2add7` |
| IMPLEMENTATION.md | 7486 | `be437c3c4e2f7d02d5679d55e59c8944b3cb785306d7fa832759a94d1fb891d5` |
| test_provider.py | 23555 | `c80d8b43778360857a885303c63a96110c80a8c9beb5fcd885d3bf94654722de` |
| assemble.py | 11449 | `1633315be5c12aeb6733246e1c90ec7792f098b4f15d7991cd1e4bdcc0b7d835` |
| prepare_selected.py | 5929 | `5a4b1e3692cd982d462208af9632f394eccabc279da6a238c8158786230a5d73` |
| compatibility.json | 10728 | `cbf3a831a794e6ed9b7d8a1a686c6d454368b8a730d6ab386af96410f3be153d` |
| test_public.py | 11092 | `156b56539dbbf3640534b2faff5a2535eb9c839f1d0813fc8ccbc2b878386d09` |

The earlier input-boundary review is retained at
`research/cycles/v5-2026-10-25-software-continuation/PEER-INPUT-BOUNDARY-REVIEW.md`.
It found the pre-handshake admission gap and shutdown ordering defect. This
review addresses their fresh successor, not a renewed audit of every old route.

## Admission and ownership argument

Assume the selected Python 3.14 single event loop and owner-controlled runtime.
Let K be the configured `max_connections`, R be `max_requests`, and S be the set
of `_Connection` records. Initially S is empty. Only the accept owner inserts
records. It checks `len(S) < K` before synchronous nonblocking acceptance and has
no suspension point between successful acceptance, charging and worker/record
registration. Therefore one successful transition adds at most one record while
preserving `len(S) <= K`. Reaping removes a record only after both raw socket
closure (`fileno == -1`) and worker completion. TLS negotiation and cleanup
occupy those same records. There is no post-accept queue outside S.

The loop checks `accepted_attempts < R` before accepting and increments exactly
once per accepted socket. Neither failed handshake nor setup failure refunds
that increment. Thus accepted attempts are bounded by R, separately from HTTP
handler starts. The OS listen backlog is separate from application ownership;
K is not a bound on all remote SYNs, kernel bytes or network traffic.

Using synchronous nonblocking `socket.accept()` avoids Windows AcceptEx's hidden
pending accepted socket. The 10 ms would-block poll and capacity event are small,
explicit tradeoffs. Unexpected accept failures stop admission. There is no
retry loop that silently renews accepted attempts.

## Transfer, cancellation and shutdown

The actual `D:\Python314\Lib\asyncio` source was checked as text. The premises
and source hashes are recorded in IMPLEMENTATION.md: connection-waiter failure
closes its transport; failed TLS need not call the application protocol; the
Proactor transport closes the retained raw socket. `_OwnedProtocol` additionally
captures a successful post-handshake transport before the waiter resumes.

The source covers cancellation before the worker's first step through its done
callback. During transfer, unknown closure does not free the record. Known
transports are aborted on stop; unresolved sockets retain occupancy and halt
admission. A runtime failure before discoverable transport construction is not
claimed recoverable: it fails quiescence and leaves the outer supervisor as the
final containment boundary.

`stop` closes the listener, aborts known transports and cancels tracked tasks
before its first await. It uses one saved absolute one-second cleanup deadline,
never extended by repeated calls. Earlier per-connection cleanup deadlines
remain earlier. Tasks and raw sockets must both settle before `server` becomes
None. This removes the earlier wait-for-server-before-cancellation dependency.
The outer service and process deadlines still apply, including synchronous
event-loop stalls which cooperative cancellation alone cannot preempt.

No blocking source defect was found in this selected ownership/lifecycle change.
This is a reasoned supported-runtime argument, not a proof of Python, OpenSSL or
OS correctness and not a promise of service availability under attack.

## Protocol and mathematical boundary

Dispatch and client exchange remain unchanged. HTTP grammar, header/body/reply
ceilings, one-request connections, TLS verification and ordinary acquisition
rules are preserved. `_serve` no longer owns task/connection admission; the
outer worker does. This repair does not admit new mathematics, trust peer
reports, run remote source or weaken local checking. Finite accepted-attempt
exhaustion can deny useful service; bounding it is not per-actor fairness.

## Direct controls and corrections before use

The six groups in TEST-PLAN.md use real loopback sockets and TLS, one freshly
created inert preview store, and a transparent wrapper delegating to real
`connect_accepted_socket`. No fake status, raw closure or mathematical warrant
is substituted. Both stop counters and actual socket closure are required.
The positive TLS client validates a fresh output-local certificate with SAN,
key usage, SKI and server-auth EKU. There is no certificate-store modification
or reuse/publication of an operator identity.

The test source loads only thirteen exact unchanged support modules and the
separately pinned candidate. It verifies sparse PROFILE
`97f93cc66f77ebcecd7a3a341baaaf4725236a8dec5fb9cee3c3e67d478f2834`
and its bound installation manifest
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
Empty namespace paths prevent silent extra product imports; no native loader or
Lean stage is selected. The approved PowerShell 7 executable is pinned at
`362a356ce7f0940ec74f73a8fc2c990a2cc24a38a11c90bbd8eca947110ad139`.

Provider-author review found one setup-cleanup gap: preview population and TLS
context setup originally occurred before the store cleanup scope. Before any
execution they were moved inside the existing try/finally. Store-close failures
are recorded, and an earlier test/setup exception is preserved rather than
replaced by a cleanup exception. An unsuccessful explicit stop is not retried
as a fresh success. Malformed-client write/close resets are expected outcomes,
not failures of mathematical acceptance.

Root may select one original 60 wall-second / 30 CPU-second / 768 MiB /
4-process outer envelope. The direct harness has 50 wall / 25 cooperative CPU
seconds; its one PowerShell child has a 12-second maximum inside that same
outer envelope. This source review neither creates nor renews such an allowance.

## File-only assembler and wrapper

The full fresh assembler and final wrapper were read. The assembler requires
the exact sparse base profile/receipt and complete 152-file census, preserves
installation/native bytes, and permits only the provider replacement and two
documentation additions. It rechecks complete old/new maps and commits the new
PROFILE last. The output is fresh; failures are preserved. The pinned reused
fair-assembler helper remains unchanged.

The final compatibility map has exactly the same 45 noncompiled roles and 72
native role names as the prior map. Its sole changed pin is the provider above.
The wrapper binds that exact map and the unchanged offline helper, checks actual
noncompiled files, refuses unknown interfaces and does not import product code.
It is explicitly configuration compatibility, not native validation or package
authentication. The unchanged public launcher still owns actual runtime checks.
README and EXECUTION-TRUST accurately separate inert exchange, trusted project
execution, protected local state and Job resource limits; Job limits are not
a hostile-source access-control sandbox.

## Public-harness review

The root-owned public harness uses the actual offline preparer, requires the
old wrapper to refuse the new interface without output, then starts the actual
assembled public directory service with one real incomplete-header client.
It checks the actual lease result, zero outstanding provider state, public
supervision evidence, reaped child and clean Job closure. No native mathematical
event or existing owner database is selected.

Two source issues were corrected before launch: the launcher wall cap is now
35 seconds, satisfying its unchanged minimum, rather than invalid 25 seconds;
real client reset is accepted alongside EOF while quiescence evidence remains
mandatory. The original 55-second harness deadline was not extended. The final
hash above includes these corrections. No additional blocking source issue was
found in that changed integration control.

## Required later evidence and limits

Only actual saved outcomes can establish whether these finite controls pass.
Root must still select exact source/runtime inputs, execute once, preserve
failures and obtain independent outcome review before adoption. This review
does not establish mathematical growth, scalable recall, independent-host
operation, global availability, exploit absence or completion of deployable v5.
