# One bad index response must not destroy unrelated local proof work

Owner: `core_search`. Date: 2026-10-20.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Scope: source-only decision requested by root. No Python import, test, compiler,
native check, prover, socket operation, Git mutation or product edit was run.
The canonical guard passed. Existing used source/evidence remains unchanged.

## Decision

There is a concrete, central availability gap: one well-framed HTTP 200 response
containing malformed or falsely authenticated discovery metadata fails the entire
ordinary client operation, even when another configured provider is honest.
This revokes unrelated live warrants and staged data. Authentication prevents
false mathematics, but the failure policy unnecessarily amplifies a bad index
reply into loss of independently justified local work.

Select a narrow successor that **prevalidates search response metadata without
mutating the session, then calls the unchanged `SearchSession.accept` only after
success**. Explicitly rejected metadata settles the original ticket once at its
full reservation and returns a provider-attempt refusal. The caller may choose
another provider within the same existing grant and session. This is not an
automatic retry, allowance renewal, global absence result or mathematical
acceptance.

Root proposed this validation-only staging alternative during the source audit;
it is preferable to rewriting the session's prepare/commit logic now. Double
metadata validation is bounded by the one response, not accumulated session
history, and leaves the accepted trust/commit path unchanged. Do not clone or
replay the entire session.

## Evidence and deduplication

The relevant current chain is:

1. `client/workspace_staged.py` inherits `workspace_resilient.CommonsClient`.
2. `workspace_resilient.search_offer/search_page` retain `_async_action`.
3. `transport/search_resilience._send` sends a 200 body directly to
   `session.accept` outside the recoverable failure region.
4. `discovery/search_session.SearchSession.accept` raises on invalid metadata.
5. `client/workspace_atomic._async_action` invokes `_fail` on any exception.
6. The actual inherited mixed/evidence failure path closes owners, closes the
   grant budget and clears live warrant/context state; the staged successor also
   clears `_staged`.

The prior eight-control allocation explicitly tested invalid 200 metadata as a
fatal case. See `software/v5/transport/test_search_resilience.py` and the adopted
`research/cycles/v5-2026-10-17/SEARCH-RESILIENCE-REVIEW.md`. That evidence remains
correct for its selected scope, which deliberately allowed recovery only before
metadata acceptance. This successor changes that specific scope; it is not a
retest of the passing transport campaign or an audit of a newly discovered
violation of its old contract.

No existing selected implementation of transactional invalid-metadata recovery
was found in the recent search/staging sources and 2026-10-17 decision notes.
The existing independent outcome already establishes small transport/control
costs. Another large proof, compiler build or memory study cannot answer this
metadata-failure-policy question.

## Why simply catching `accept` is unsafe

`SearchSession.accept` owns both accounting and metadata mutation:

| Function/branch | State changed |
|---|---|
| `_take` | Removes the pending ticket; releases reservations; charges bytes and candidate scan allowance |
| `_store_summary` | Installs a summary and creates coverage |
| `_accept_offer` | Subsequently records known snapshot identity and an offer hint |
| candidates branch | Charges accepted candidates, commits dedup state and writes advisory cursor |
| `Coverage.accept` | After verification/callback, updates object observations and interval coverage |
| interval branch | Subsequently charges rows, commits dedup state and last verified cursor |
| failure handler | Conservatively charges reserved row allowances |

The main validators already check authentication before ordinary metadata
commits. However, a local allocation failure or another exception can occur
after a mutation. A catch around all of `accept` cannot infer that it is safe to
continue. Calling `abandon` after `accept` also cannot settle the same ticket:
`_take` has already removed it. Post-mutation failure can additionally interact
with existing conservative charges. Leave this original fatal path unchanged.

## Recommended minimal source scope

Use new files; do not edit already used predecessors:

- A transport successor, e.g. `transport/search_metadata.py`, importing the
  existing `_binding`, `_unchanged`, `_exchange` and `_abandon` helpers. Own a
  narrowly adapted `_send` and public offer/page functions. Preserve exact
  located-client/session/policy types and the existing HTTP/closure contract.
- A thin successor of `client/workspace_staged`, e.g.
  `client/workspace_search_metadata.py`, overriding only ordinary search methods
  and extending the original real owners' source-pin closure. Preserve storage,
  grants, source checks, staging, mathematical admission and contribution.
- A new changed-boundary test file and one short contract. Root selects actual
  integration source maps separately; unused test/integration paths are not
  runtime authorization.

The helper need support only `offer` and the two ordinary `page` modes used by
this public facade. A standalone `begin_summary` preflight is unnecessary unless
root deliberately selects that additional public route.

### Immutable preflight inputs

Before parsing, check the unchanged original owner and exact pending ticket and
reservation. Check that `raw` is bytes and respects the ticket's reply ceiling.
These local/transport invariants are outside the recoverable data-validation
catch. No metadata validation callback may mutate session fields except the
existing fatal deadline-state transition.

Preflight uses the original ticket request, query, summary and coverage, not
caller-provided replacements:

- **Offer:** validate the exact offer envelope, original namespace/features and
  assurance fields. For `NO_OFFER`/`REFUSED`, require the existing status/reason
  combinations and absent summary. For `OFFERED`, decode the compact summary
  with `summary_wire.decode_summary`, then call `discovery_query.verify_summary`.
  If this snapshot already exists, require equality to its verified summary
  without storing anything. Reuse the original offer-expiry/liveness checks.
- **Positive candidates:** parse canonical bounded JSON and call
  `candidate_query.verify_page` against the already verified summary and exact
  original request. It authenticates positive membership only. No coverage,
  candidate dedup or advisory-cursor write occurs during preflight.
- **Authenticated interval:** call `discovery_query.verify_page`, then perform
  the existing `Coverage.accept` cross-page object-consistency checks read-only
  against `coverage.observed`. That consistency check is additional to
  `verify_page`; omitting it leaves a remote metadata conflict to fail later.
  Do not install intervals or observations.

The preflight need return only success or a small typed rejection; discard its
temporary decoded/verified output before invoking unchanged `accept`. It must
not return a reusable "authenticated" capability or install a cache.

### Error boundary

Use a dedicated internal metadata-rejection type/result. Within the pure
parser/validator region, expected `ValueError`-family failures (including JSON
and Unicode decoding) may become that rejection. **Owner/session/offer guard
failures must escape:** wrap such callback errors in a dedicated non-ValueError
local sentinel before passing callbacks to compact-summary or candidate
validation, then re-raise the underlying failure outside metadata classification.
Check owner bindings/liveness again outside the catch.

Do not classify arbitrary errors by a broad string prefix. Do not catch the
unchanged `accept` commit, `_abandon`, `_unchanged`, persistence, source checks,
`MemoryError`, cancellation or unexpected programming faults as bad metadata.

An intentionally narrow first implementation may leave unexpected `TypeError`
or other programming errors fatal, even when malformed input can trigger one.
For example, a malicious unhashable termination value can reach a set membership
test in a pure verifier. That is an explicit residual refusal/liveness limit,
not a reason to swallow arbitrary exceptions around the whole operation.
Additional shape guards can be justified separately if needed; mathematical
acceptance must never be relaxed.

### Settlement and success

On typed rejection, while the original ticket is still pending:

1. Run the unchanged exact-ticket `_abandon`, charging **full reserved bytes,
   examined rows and candidates once**.
2. Recheck unchanged owner/session bindings and original deadline.
3. Return a distinct `REFUSED_PROVIDER_ATTEMPT` reason for invalid metadata,
   explicitly with `mathematical_acceptance=False`, `global_complete=False`,
   and no candidates, summaries or coverage.

Completed HTTP counters still record actual physical response bytes. The
session's reserved-cost ledger is deliberately more conservative on rejection;
this is not duplicate wire-traffic accounting. Earlier request/provider/page/
snapshot-attempt charges remain. No failure resets the session, request counter,
grant, contacts or deadlines.

On successful preflight, call the original `session.accept(ticket, raw)` outside
every recoverable catch. The original mathematical/discovery assurance semantics,
dedup behavior and acceptance result remain. Any late error remains fail-stop.

## Safety and cost argument

Let `M` be adopted search metadata, `A` be live mathematical authority, and `t`
the one outstanding serialized ticket. Preflight runs pure validators and
read-only consistency checks. If it rejects, `M_after = M_before` and
`A_after = A_before`. Exact abandonment removes `t` and applies its original
reservation to consumed costs, so rejection cannot fund additional attempts.
Observed clean socket closure and unchanged bindings are prerequisites for the
normal return. The original operation decorator then checks owner liveness and
census before exposing the result.

On success, the unchanged original acceptance procedure remains the sole
metadata commit path. Thus the new preflight cannot admit any response the old
path would reject. It can only reject earlier or duplicate verification.

If a valid provider remains among the configured contacts and the original
allowance/deadline suffices, rejecting a malformed earlier provider no longer
necessarily destroys the client's existing mathematical work. This is a
conditional liveness improvement, not recall, global completeness, guaranteed
honest-provider discovery or a bound against unlimited bad attempts.

Additional work is one bounded response validation. Summary geometry is already
bounded by at most eight queried features and 256 partitions/sibling levels;
interval pages have at most 32 examined rows; positive candidate pages have at
most eight authenticated hits. Wire and expanded summary bytes remain capped.
No additional scan of prior snapshots, candidates, proof ancestry or the global
corpus is required. The existing owner/controller CPU and wall caps still apply.
Do not claim lower CPU cost: successful replies are validated twice initially.
The payoff is preserving useful existing work when an index sends bad data.

## Small decisive controls, not another broad campaign

Run only a new bounded changed-boundary suite after root's source selection:

1. Invalid canonical/JSON offer, then honest offer in the same session/grant;
   prior live-token and staged-data mappings remain intact.
2. Tampered summary authentication, then honest alternative; no failed snapshot,
   hint or coverage installation.
3. Tampered positive membership proof, then honest candidate page; no dedup,
   cursor or candidate-state update from the failed step.
4. Invalid interval/filter/cross-page metadata, then honest interval; coverage
   and observed-object state unchanged by rejection.
5. Exact full reservation charged once for each rejected mode; an exhausted
   budget refuses the next attempt before dialing; no second abandon/accept.
6. Callback deadline/expiry failure, owner/ticket mutation, cancellation,
   allocation failure, dirty socket closure and late original-accept failure
   remain fatal. Deliberately distinguish data rejection from local uncertainty.
7. At least one new actual bounded loopback invalid-200 -> honest-response
   sequence exercises the selected facade/transport integration. Synthetic
   index fixtures and inert owners remain explicitly non-mathematical evidence.

Source validation of the actual issuer/source-map integration is necessary;
inert facade tests cannot establish it. No native verification or proof campaign
is needed to decide this changed discovery boundary.

## Selected implementation, awaiting root's bounded execution

Root selected this narrow implementation in the adjacent `SELECTION.md`.
The resulting fresh files are:

- `software/v5/transport/search_validation.py` (this worker).
- `software/v5/transport/test_search_validation.py` (this worker).
- `software/v5/client/workspace_validated.py` (root).

The helper keeps the exact original session/client types and reuses the existing
binding, bounded transport/clean-closure and abandonment helpers. Its pure
preflight checks the current offer/candidate/interval only. Local pending,
reservation, original-query and coverage-summary bindings are checked outside
the metadata error catch. Guard callback ValueErrors are wrapped with a distinct
non-ValueError sentinel and re-raised; they do not become metadata refusals.
Successful original acceptance stays outside every recoverable catch.

The eight new controls cover malformed JSON and UTF-8, tampered summary and
candidate/interval proofs followed by honest alternatives, cross-page consistency
without metadata writes, exact full failed reservations, original request
exhaustion, callback expiry while compact-summary decoding, fatal local
coverage-summary corruption, fatal late commit, fatal cleanup/cancellation/
allocation errors, and one two-connection loopback invalid-200 -> honest offer.
Only fixture construction/liveness/census/report are inert; public new decorated
methods, original session/transport/cleanup are actual code. No predecessor test
class is selected. A synthetic staged-data map and live-warrant-shaped mapping
are explicitly not mathematical evidence.

**No execution occurred in this worker.** Root owns review, the one small bounded
run, adoption, actual source-map integration and Git. This addresses one central
failure-amplification issue, not final-v5 release completion or the separate
unresolved genuine reciprocal-growth workload.
