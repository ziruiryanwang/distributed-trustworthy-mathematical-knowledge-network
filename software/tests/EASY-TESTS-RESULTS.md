# Easy single-machine tests: 2026-09-22

**21 checks passed:** the existing 18 transport controls and three new
real-socket scenarios. No second computer, VM, Lean build or external service
was used. [Run guide](EASY-TESTS.md); [independent review](EASY-NETWORK-REVIEW.md).

| Fresh allocation | Result | Supervised wall | Worker Job CPU |
| --- | --- | ---: | ---: |
| [transport-02](../qualification/transport-02/result.json) | 18 passed, no failures/errors/skips | 0.7018594 s | 0.296875 s |
| [local-network-smoke-02](../qualification/local-network-smoke-02/result.json) | 3 passed, no failures/errors/skips | 2.9070863 s | 0.515625 s |

These are worker intervals, not total engineering time or complete machine/agent
costs. Parent preparation/reporting and review work are not included. Descendant
service CPU is already inside the Job total and must not be added again.

## New scenarios

1. **Supplier turnover:** A runs in its own Python process. A consumer fetches
   its catalog and exact package; A exits naturally after two connections.
   The subsequent offline probe returns no catalog. B then runs in a separate
   process, serving a view built from the received package, and supplies exactly
   the same bundle bytes. B also exits naturally at its connection quota.
2. **Interrupted transfer:** a real socket sends one byte less than its advertised
   bundle length. The receiver refuses `BUNDLE_FRAMING_REFUSED`, closes the
   connection, and creates no acceptance record. The responder thread ends;
   partial fixture data is retained.
3. **Bad request followed by good:** the service rejects an invalid Host header,
   then serves a valid catalog request. The report has two connections, one
   response, `HTTP_PROFILE_REFUSED`, and normal quota shutdown.

All three supplier processes exited zero without forced cleanup. The enclosing
Job ended with zero active processes, zero terminated processes, a reaped direct
child and a closed Job. The suite loaded no checker/codec/SQL module and ran no
native stage. Synthetic CBOR fixtures are deliberately **not verified mathematics**;
these results complement, not replace, the earlier actual Lean/reuse evidence.

## Preserved unsuccessful attempts

The first prelaunch guard rejected a reviewer hash from before the hidden-window
flag addition. No allocation or child was created; independently reversing that
one source delta reproduced the stale digest exactly.

[Smoke01](../qualification/local-network-smoke-01/result.json) then ran once and
failed one of three assertions: a connection to stopped A timed out instead of
returning the test's expected immediate `PEER_UNAVAILABLE`. Both are documented
transport errors; process completion and no returned catalog are the relevant
offline conditions. The other two scenarios passed. Failed-run Job CPU was
0.359375 s and supervised wall 2.6469408 s; these costs are not discarded.

The only test correction allows those two refusal codes and records the probe;
natural supplier exit remains mandatory. Smoke02 is a fresh allocation with
its own exact source snapshots, not a rerun or relabeling of Smoke01. No product
source was changed, and the delivered v1 archive remains byte-identical.

## Evidence and limits

Smoke02 result SHA-256:
`0d7233e2a766de63f8fc16fa77cbcac258e18c1c4fc9141320597edaf8f91dbc`.
Its supervisor receipt SHA-256:
`80c20cec474cd3078797d443cad5671369af33271e56de45defe5b01399e81fc`.
Full commands, snapshots, streams, per-supplier lifecycle/report records and
truncation observations remain beside the linked results. Independent source
and outcome review is recorded separately in the review note linked above.

This establishes a practical easy-testing path on one machine. It does not
establish independent-host deployment, arbitrary network-fault tolerance,
mathematical acceptance, search quality, long-term availability or scalability.
No such qualification is required merely to continue development.
