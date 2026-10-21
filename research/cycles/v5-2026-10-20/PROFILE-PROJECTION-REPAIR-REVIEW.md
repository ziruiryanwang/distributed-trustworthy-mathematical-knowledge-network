# Independent source review: controls02 harness repair

2026-10-20, adaptive_audit. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

**GO for root's separate finite controls02 selection.** No runtime is performed
or authorized by this review itself. Product sources and noisy controls01 stay
frozen; the controls01 evidence HOLD and 3.421875 known CPU seconds remain.

Reviewed exact fresh sources:

- `software/v5/base_projection/controls02.py`:
  `814863a6fa778ae431f36178ba080071f8c434024bbd17a78a0144512b768b1b`.
- `research/cycles/v5-2026-10-20/Select-BaseProjection02.ps1`:
  `af2f8eb7015f0a2010ea0a2718840fe41d8b5f48cf9b687144355e25da517f0c`.

I compared the complete controls01/02 diff. It changes only the faulty socket
guard, asynchronous exception observation and the report's own source identity
(plus a trailing blank line). The actual eight test groups and product assertions
are unchanged.

The repair patches `socket.socket.__init__` instead of replacing `socket.socket`.
The exact Python class remains usable by the Windows Proactor `isinstance` check,
and already-created event-loop sockets are not reinitialized. Subsequent socket
construction is refused. Existing asyncio network/process guards remain. Root
explicitly selected this constructor-method approach; an earlier alternative
network-method list is superseded, not a simultaneous requirement.

Each selected test installs an event-loop exception handler, counts all observed
contexts and retains at most 16 bounded descriptions. The handler also delegates
to the previous/default handler, preserving raw stderr. Teardown drains resources,
yields once to queued callbacks, records the count and fails if it is nonzero.
Cleanup restores the original handler after removing guards. This does not claim
an exhaustive system monitor or observation after handler restoration; the next
saved-outcome audit must still inspect actual stderr, not only unittest's label.

The selector pins the exact noisy01 request `faf0214a`, rechecks all 153 prior
source entries and all 19 retained runtime pins, and adds only the reviewed fresh
controls02 source: 154 snapshots. It uses a fresh operation/output name and the
same isolated flags, 45 CPU-second/75 wall-second/384 MiB/two-process envelope
and one-MiB log caps. It stages only and cannot silently replace prior evidence.

No mathematical, discovery, namespace, custody, service or distribution algorithm
changes. A clean new result could close the harness-evidence gap; it would not
turn either local structural run into live network, growth or final-v5 evidence.
