# Independent owned-connect source review

2026-10-28, growth_design_audit. **PASS for the selected source boundary; no
execution or product qualification is claimed.**

Reviewed `fair_exchange.py` SHA-256
`05cf2b5baef0130dbe3b43e594d6c800baf6b625c77125dd3356f59f78509575`
and `CONNECT-CONTRACT.md` SHA-256
`b0b62c301b8d8953557cc32fa6b64d0bfa882abf37a053114e46074b4eb8c93a`
against the selected predecessor and the independent
`ordinary_registration_refresh/CONNECT-OWNERSHIP-CHALLENGE.md`.

The implementation meets the material ownership obligations:

- Existing validation, compact request, HTTP codec, TLS context/name and
  response classifications remain. The original absolute deadline is narrowed,
  never renewed. Setup remains cooperative rather than preemptively timed.
- One numeric nonblocking TCP socket is allocated. Raw connect success is
  followed by a fresh remaining-time check. The transfer flag is set before
  `open_connection(sock=sock, ...)`; no host/port second connect is requested.
- Known raw refusal/reset/native-timeout proposes a settled result, but the
  result cannot leave the function until `finally` has successfully closed the
  owned socket and observed `fileno() == -1`. Close raising is fatal even if a
  descriptor was invalidated. Invalid descriptor observation alone is insufficient.
- A successful raw connect that consumed the original horizon also closes before
  returning timeout. Constructor/setup and unknown connect errors do not become
  peer unavailability. Allocated sockets are still cleaned on those paths.
- The timeout context handles its own cancellation. External cancellation is
  separately propagated; if raw close fails too, the original CancelledError
  is raised with that closure failure as cause. No cancellation is downgraded
  merely because a timer expired.
- Every ordinary no-writer post-transfer error, including refusal/reset/native
  timeout, becomes terminal `FAIR_STREAM_CLOSURE_UNOBSERVED`. Own timeout after
  transfer is also terminal. External cancellation remains cancellation. The
  helper does not reclaim the possibly transport-owned raw socket.
- The existing writer close/wait_closed settlement boundary is retained after
  successful stream handoff. This review does not broaden that boundary.
- Numeric and named IPv6 zones become an explicit scope-id field before socket
  allocation. Local interface lookup failures/uint32 overflow remain local
  failures; no zone is silently dropped and no DNS path is introduced.

The conditional assurance is the one stated in the contract: trusted
CPython/Windows raw-close semantics plus exclusive ownership witnesses no live
socket retained by this helper. It does not prove instantaneous kernel/IOCP
drainage, a hard CPU bound, all failure-path TLS recovery, or global operation.
No source blocker was found within this narrow change.

## Focused controls prepared, not executed

`control_tests.py` independently exercises the selected package's actual exchange
and timeout context, using scripted raw sockets, raw connect, stream handoff and
response. It replaces only the exchange module's socket binding; the global
socket.socket class remains intact. The real Windows loop is created before
application connect/bind/listen, database and process methods are denied.
Unhandled loop errors are counted and fail the run.

Eleven groups cover:

1. Exactly one owned socket/connect/stream handoff for numeric IPv4 and IPv6.
2. Refusal/reset/native-timeout closure before settled return.
3. Actual own-timer cancellation, original absolute deadline, and modeled horizon
   exhaustion immediately after TCP success.
4. External cancellation, an additional cancellation while own timeout unwinds,
   and external cancellation with failed raw close.
5. Close exception and noninvalidated descriptor refusal to settle.
6. Unknown connect errors, allocation failure and postallocation setup failure.
7. All selected no-writer stream errors and own timeout after handoff.
8. External cancellation after handoff without reclaiming stream ownership.
9. Unchanged TLS context, server name, header limit and remaining handshake cap.
10. Returned-writer recovery and failed writer cleanup.
11. Numeric/named IPv6 scope preservation and failed local scope before allocation.

These controls do not establish actual Winsock cleanup, HTTP parser behavior,
contact refresh, mathematical acceptance or useful growth. Root must select any
bounded execution; no control, import, socket experiment or product operation was
run during this review. All original public01 evidence remains unchanged.
