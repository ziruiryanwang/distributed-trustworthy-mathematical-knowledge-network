# Explicit multi-source receiving, with unchanged mathematical authority

2026-10-26. Root selects SOURCE IMPLEMENTATION ONLY after reading
NEXT-CORE-PAYOFF-AFTER-MIRROR (46810b46) and MULTI-SOURCE-CHALLENGE (8032ee35).
The mirror is closed/adopted in commit 2973295. No runtime, native build,
package assembly, external service or mathematical campaign is selected here.

## Payoff and boundary

Current receive uses its discovery provider for every preview, unit and missing
dependency. Another approved holder cannot supply just one missing item in that
operation. Expose the existing acquisition primitive's per-object source choice
through an optional bounded policy. A manual complete-mirror switch or ordinary
Git/Lake import remains simpler when it suffices. Lower APIs already have this
power; this change supplies supported composition, not a new trust mechanism.

For successful exact byte identities, supplier substitution leaves preflight and
local checker inputs unchanged under the existing hash/checker/protected-state
premises. It does not make cold proofs cheaper, create warrants, derive missing
previews, ensure general availability or establish mathematical-growth speedup.
At least one selected source must supply each requested preview/locator/evidence
kind within the same grant. A malformed or malicious response may still stop
this conservative first policy even if another holder could have succeeded.

## Selected source footprint and ownership

Fresh copies of exactly three current pure payloads, leaving originals frozen:

- `ordinary_bounded_transport/http_provider.py` -> `http_provider.py`.
- `ordinary_authoring_offers/ordinary_acquisition.py` -> `ordinary_acquisition.py`.
- `ordinary_sparse_access/peer_api.py` -> `peer_api.py`.

inert_rehost_relation owns the first two and ACQUISITION.md. Root owns peer_api,
integration, source selection, tests/plan coordination and Git.
inert_rehost_path owns only test_multi_source.py and TEST-PLAN.md after this
contract; current_acceptance_challenge owns independent REVIEW/outcome.
Canonical root is E:\Distributed Trustworthy Mathematical Knowledge Network;
explicit workdir and absolute edits are mandatory. No subagent Git or runtime.
No admission, kernel, catalog, custody, wire format, source discovery, partial
mirror preparation, contact registry or resource-ledger redesign.

## Fixed interface for parallel implementation

H.exchange adds keyword-only `classify_unavailable=False`, preserving default
behavior. H.TransportUnavailable has a bounded enumerated `reason`. Only opt-in
network-scope failures may produce it, after local endpoint/request/TLS setup:
the exchange timeout manager's own expiry, narrow refused/reset/aborted/broken-
pipe connection classes and IncompleteReadError. Explicitly exclude TLS errors.
Do not reclassify a bare TimeoutError whose own manager did not expire; never
catch broad OSError or CancelledError for recovery. Keep existing close cleanup.

O.preview, O.locator and O.evidence add keyword-only
`attempt_timeout_ms=None, unavailable_errors=False`, forwarding them to _fetch.
The default path keeps existing semantics. Opt-in _fetch calls H.exchange with
the capped remaining timeout and classification flag. O.AcquisitionUnavailable
exposes bounded `reason`, `provider`, `route`, only for typed exchange failure or
framed HTTP404/503 before validation/retention. Its exposure must occur after
normal failed-ticket settlement; settlement failure remains terminal. Counts and
full failed response-cap charges remain unchanged. No refunds or fresh ledger.
All protocol/status400, syntax, identity, CA/pin/config, cancellation, budget,
retention/SQLite and checking errors are terminal. No exception-string recovery.

Receive optionally accepts ALL THREE additional top-level fields together:
`acquisition_sources`, `attempt_timeout_ms`, `finalization_reserve_ms`.
The first is 1..8 distinct labels selected from existing contacts; the other two
are integers 1..60000 milliseconds (booleans refused). This explicit order
replaces acquisition order; never prepend selection.provider, try every contact,
follow referrals, or enlarge the list after failure. The original provider and
snapshot remain discovery-origin fields. Absent fields retain the old path.

Use the same client, original operation, shared ledger and parent. Compute ONE
network deadline D = min(operation.deadline, ledger.deadline) - reserve/1000.
For each fetch key and r sources still untried, choose timeout in milliseconds
no greater than min(attempt cap, floor(1000*(D-now-r*1 second)/r)). Refuse if no
positive slot remains. Recheck owner/CA/budgets before and after attempts; no
whole-fetch timeout may turn local retention failure into fallback. Catch only
O.AcquisitionUnavailable to advance. Each source is tried once per key.

Successful bytes still pass unchanged exact validation, PP.resolve, finite-unit
retention and existing bounded metadata preflights. Exactly one final owner.admit
occurs only after READY. selected-unit-only makes no ancestor requests. Reports
retain bounded per-provider counts/last availability reason (at most eight rows),
not an unbounded attempt history. No default report/config behavior is weakened.

The time division reserves network opportunities, conditional on bounded local
overhead; it does not guarantee finalization of arbitrary proofs. Requests are
at most m*p for m demanded keys and p selected sources, further capped by the
original request/byte/time ledger. No global provider/corpus scan is introduced.

## Decision-changing validation, not a repeated campaign

One focused native-free suite after independent source/selection review should
exercise real exact codecs and ledger plus explicit owner/transport doubles:
default compatibility, opt-in validation/order, unavailable A then B, disjoint
dependency holders, actual classified transport seams, time-slot arithmetic,
failed-cap charging/shared-ledger exhaustion, no-ancestor policy, and terminal
identity/TLS/local-retain/settlement/cancellation errors. Evidence-only custody
without the required preview still refuses. Doubled owner acceptance is not Lean
evidence. Use retained inert fixtures; do not recreate mathematics or run a
certificate/native campaign. A small actual loopback transport check is warranted
for real EOF/timeout classification; no external endpoint or package build.

Root later selects exact finite execution only after source compatibility and
test-plan review. Public overlay/guide integration follows only a demonstrated
usable boundary; no automatic repack or full-release label. Full v5 stays active.
