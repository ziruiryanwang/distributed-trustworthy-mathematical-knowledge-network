# Root source review of remaining-capacity replies

2026-10-28. PASS for the source argument, not an executed test or package adoption.
Candidate http_provider.py SHA-256:
`929fbf453bb23d353f89384db3dbb8cd4e11e6fd5383a09a36d93fc92631b93b`.

The actual diff from the selected ordinary_multi_source provider contains only
the eight inserted lines after ordinary request validation. The route check is
exactly evidence or locator. The remaining allowance is positive before use;
the effective maximum cannot exceed the original protocol-valid maximum. The
later aggregate check, reservation, synchronous dispatch, complete-response size
check, charge-before-write and finally release are unchanged. Preview's exact
object size and all discovery routes retain their previous behavior.

The unchanged OrdinaryStore checks the indexed object length before loading its
BLOB. Its serve function revalidates the effective request. A missing object or
an object too large for the smaller cap still refuses rather than truncating or
asserting absence elsewhere. No caller-controlled path or executable is added.

The CONTRACT's invariant C+U<=B is the correct one: U contains only uncharged
reservations. Admission uses the larger conservative Q=U+D; charging a response
of length b<=r replaces r in U with b in C. Cancellation after charging preserves
that charge; release cannot increase C+U. There is no intervening await in the
new read/validate/reserve transition. The argument depends on the existing
single-event-loop ownership of counters and does not prove concurrent fairness,
header-byte bounds or a new total-process bound.

Root's control source uses the real HTTP parser, dispatch, codecs and scratch
SQLite custody. Controlled writers exercise deterministic in-flight reservation
and cancellation behavior. Its first source review found omitted required HTTP
headers; both were corrected before any execution. The controls deliberately
avoid sockets and native workers: the changed code is inside _serve, and socket
admission/TLS behavior did not change. Source review of controls and a finite
execution selection remain separate.
