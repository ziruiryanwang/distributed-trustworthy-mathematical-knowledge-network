# Mandatory local whole-adoption withdrawal

**Select a persisted owner-controlled guard, not an optional in-memory hook.**
This changes whether a local installation still trusts an adopted checking
stack; it neither changes theorem truth nor creates global revocation authority.
One domain contains one immutable whole-runtime adoption, not a dependency graph.

## API and identity

- `TrustDomain.create(fresh_directory, domain_id, support_manifest)` is an
  explicit owner adoption action only; create metadata and record with no overwrite.
- `TrustDomain.open(existing_directory, expected_domain_id, expected_support_id)`
  is mandatory on ordinary startup. Missing, malformed, changed, unknown or
  redirected state refuses; no implicit creation, fallback or per-operation reset.
- `bind()` returns an opaque exact-class binding to this original domain/adoption.
  `check(binding)` validates identity, immutable metadata and current denial state.
- `withdraw(reason)` creates a bounded `WITHDRAWN` marker without replacement,
  flushes before acknowledgment and never offers clear/reinstate. Any existing
  marker, including incomplete/unreadable content, denies; reason text is diagnostic.

The support ID hashes canonical stable role/relative-name → length/SHA-256 rows
and exact I/A image, foundation, policy and receipt-scheme identifiers. Include
all selected SDK/controller/native/authoring/runtime and parameter roles, not
just the currently used receipt image. Exclude operation budgets, per-run paths
and generated preparation-profile file digests; normalize their stable role
contents instead, so relocation cannot reset withdrawal. RuntimeProfile derives
and matches this support map from its actual selected pins; a caller assertion
of "complete support" is insufficient. Preserve the existing trusted-owner/OS
assumption; these pins do not establish hermetic OS/DLL or checker correctness.

## Live invariant and update ordering

For this adoption, every authority-producing or authority-using action must
pass its original guard at entry and its final authority publication/return
boundary. Once denial is observed, that guard and affected owners stay denied
even if the marker later disappears; clear their handles/caches without refunding
charges. Bytes already returned remain inert data, not reusable live authority.

The current owner-serialized model linearizes acceptance at its final guard
check and withdrawal at marker creation. A queued request is not an applied
update. An in-flight worker may finish, but a marker present at its post-worker
gate refuses its result. No immediate worker cancellation is promised. Concurrent
updates/atomic check-and-mint across threads need explicit synchronization before
such a stronger contract is claimed; a late update cannot recall returned bytes.
Remote queries, contributions, peers and historical reports cannot adopt,
replace or withdraw the guard. Only the trusted local operator chooses policy.

## Minimum coherent successor

1. New bounded `admission/trust.py`: exact class/origin, immutable support record,
   explicit create/open, create-only denial, sticky refusal; no global registry.
2. Fresh actual `runtime_efficient/admission/verifier.py` successor: mandatory
   binding parameter, original-object/domain checks and guard identity in profile;
   `_active` denies and internally clears handles even while a worker is busy;
   add a final check before direct `describe` returns its copied live facts.
   Do not call public `close()` there: it rejects `_busy` and can mask withdrawal.
3. Fresh aggregate admission successor forwards the same binding before base
   initialization and includes it in its replacement profile ID. Both I and
   A-only construction are covered; no `None`, default-allow or legacy fallback.
4. Fresh RuntimeProfile successor requires the opened domain, validates the
   complete support map, checks again at every new operation and passes the
   same binding to all configured issuers. Reusing/newly constructing a profile
   from the same persisted domain cannot revive a denied adoption.
5. Update explicit source maps/origin pins and all supported constructor callers.
   Exact-class gates remain. Existing mixed owners, import sessions, cache hits
   and post-authoring checks propagate issuer refusal; audit those paths, do not
   fork them gratuitously. Standalone preparation emits no acceptance authority.

## Restart and release boundary

The marker survives ordinary restart; reopening must never provision an empty
domain. Retained receipts are rechecked under current policy, not saved success
flags. Trusted filesystem rollback by the owner/OS is outside this local model;
hashes/generations alone cannot provide hardware antirollback. Missing metadata
fails closed. Withdrawal does not delete mathematical custody or alter others'
policies. Test crash/write failure, restart, cached/live/post-worker/new-operation
denial and malformed/default-bypass cases before adoption. Broader secure update
distribution, hostile-input isolation and cryptographic/checker assurance remain
release obligations; this concrete persisted gate closes only local withdrawal.
