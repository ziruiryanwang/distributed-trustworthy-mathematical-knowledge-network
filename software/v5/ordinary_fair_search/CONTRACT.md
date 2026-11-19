# Fair finite search: source successor selection

Root selects a Python-only correction to the current ordinary default's
first-provider starvation. Existing index commitments, query semantics, positive
membership checks and mathematical acceptance are unchanged. Used predecessor
sources/packages stay frozen. No runtime or package adoption is yet selected.

## Scope and ownership

`current_security_obstruction` owns only `fair_exchange.py` and `fair_search.py`
here. Root owns the peer facade/profile/source-map integration, selection and
tests/review assignment. Reuse the selected ordinary HTTP codec and existing
search session, not the different located-client binding. No native rebuild,
network experiment, Git, shared-ledger edits or new discovery protocol.

## Invariants and API

One existing `SearchSession` and one already prepaid outer `OrdinaryBudget` retain
their original query, deadlines, caps, counters, deduplication and source checks.
No grant renewal/refund, replacement session, retries or simultaneous requests.
The scheduler visits providers with one offer each, then at most one candidate
request per active provider per round, preserving each partition/cursor.
Finished/refused providers leave the queue; nonprogressing advisory cursors stop
only that partition, not a global absence claim.

`fair_exchange.exchange(...)` uses the existing bounded HTTP framing and explicit
endpoint/CA policy; it returns ordinary bounded response/accounting or an explicit
settled provider refusal. Only recognized failures with clean observed closure
are recoverable. Unreturned-connect timeout/reset, uncertain cleanup, external
cancellation and unknown local failures remain fatal. An attempt that reserved
a ticket settles that exact ticket once even on failure; malformed proofs cannot
be returned as matches. Do not copy the old suppressed-close-error behavior.

`FairSearch(session, endpoints)` provides `run(providers, offer, page, *,
attempt_timeout_ms, check_owner, recover_metadata_failure)`, partial `result()`
and `report()`. Root supplies the existing owner/CA checks and precise recoverable
metadata-failure predicate. No catch-all recovery for local validation failures.
All reported matches remain independently verified positive records, not accepted
mathematics. Partial successes and charges survive later failure.

Prospective facade policy: 5000 ms maximum asynchronous attempt, narrowed further
by the original residual session time divided among the active queued providers,
with one second per-attempt stream-closure reserve. No legal positive slice means
explicit incomplete-budget termination before another dial. Exact integer/floor
rounding must not enlarge the grant. Session or owner expiry remains authoritative.
Synchronous CA/context loading, JSON/proof work and OS scheduling are not preempted
by this timer; the existing whole-operation Job remains necessary. No hard
all-work fairness guarantee or global completeness is claimed.

This changes the local search strategy, not the wire. Under adequate grants and
bounded local/cleanup work an early slow provider no longer owns all later I/O
opportunities. Small request/byte/scan/candidate grants may still prevent reaching
every peer. Offering all peers first can cost more before the first hit; expose
that tradeoff rather than claiming universal latency improvement.

## Later verification

Source review first. Native-free tests should cover round order, stalled offer
and page continuation, exact conservative accounting, original-budget exhaustion,
cursor progress, failed closure/cancellation/local errors and no false coverage.
Actual network validation, if necessary, is one bounded loopback test after a
separate selection. No theorem build, large corpus or benchmark is needed.
