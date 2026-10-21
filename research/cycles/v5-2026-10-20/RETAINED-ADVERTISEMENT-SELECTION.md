# Retained route restoration: one small implementation slice

2026-10-21, root. Read/adopt contracta05798de. Implement only owner-only
`advertise_retained(request_id, until=...)` on an originally funded later run
of a SEALED_SERVING generation. Original receipts, custody, index, publisher
permissions and immutable max_runs stay unchanged. No automatic restoration,
public write route, manager, deletion or old campaign restart.

core_release owns fresh successors under `software/v5/retained_advertisement/`:
`placement/advertisement.py` from b5523f82 and `client/serve_placement.py` from
used319ddf07. Follow the exact contract: bounded committed-record/index/local
metadata predicates; fresh owner guard; original horizon; one charged durable
attempt per cell/current run; no retry on uncertainty; current-run facet only.
Track at most one owner restoration task and drain it with HTTP intake under
one original shared cutoff. Ordinary submit/status guards remain unchanged.
Record concise API/diff reasoning in RETAINED-ADVERTISEMENT-SOURCE.md.

core_growth owns one fresh focused control harness and selection preparer,
RETAINED-ADVERTISEMENT-CONTROLS.md checkpoint. Reuse fixture patterns, not old
passing test methods: sealed two-run restoration, unchanged receipt/custody/
index, bad/incomplete/missing representative, expired horizon, uncertain
same-run no-redispatch, immutable run/config caps and cancellation/closure.
Real local stores; simulated locator/transport; no actual native/proof/network.
Use one compact bounded selection; root alone selects runtime after review.

adaptive_audit completes actual integration02 audit first, then independently
reviews these changed sources/controls at RETAINED-ADVERTISEMENT-REVIEW.md.
Root integrates, launches later, adopts and commits explicit reviewed paths.
Canonical root is `E:\Distributed Trustworthy Mathematical Knowledge Network`;
explicit workdirs/absolute edits, no subagent Git. Used sources stay frozen.

This slice fixes loss of discoverability across a funded restart, not continuous
disk reclamation or full-cost growth. Defer the larger lifecycle manager and
physical-profile implementation until this economical primitive is reviewed;
then redirect a lane to the unresolved certificate/useful-growth bottleneck.
