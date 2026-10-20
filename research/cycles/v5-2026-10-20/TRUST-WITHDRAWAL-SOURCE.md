# Trust withdrawal: initial source/liveness decision
Source inspection only; installed interface distribution `c249d086`; prior bytes
freeze. Root selects agreed API/fresh overlays before implementation; see design.

## Existing propagation points
- `admission.verifier.ReceiptVerifier._active`: called by live-handle describe,
  group opening, receipt admission before work, after worker and before minting.
  Add final `describe` check. Denial internally revokes; public close rejects busy.
- `AggregateReceiptVerifier._active` calls that base and revokes aggregate/member
  handles and cache on error. Its constructor forwards base arguments but its
  final profile ID is independently replaced: both must include the binding.
  Initialize override-visible guard/fields before base constructor liveness calls.
- `mixed_claims.receiver._active` rechecks actual I/A origins. Any failed mixed
  receive revokes. `MixedImportSession._active/_live` checks those same owners.
- Client cache hits resolve `_warrant`, not saved verdicts. Client `_active`
  calls issuer liveness; action failure clears warrants/caches and fails closed.
- `MixedSourceOperation` and preparation `source_live` recheck the import session
  after the frontend worker and before final return. No preparation edit is
  needed for this ordinary author route; standalone producer policy is separate.
- `RuntimeProfile.from_context/open_operation` currently have no withdrawal
  authority. A fresh instance/operation is therefore the restart bypass to close.

## Small coherent plan agreed with design author
Four fresh overlays suffice in principle: new `admission/trust.py`, plus
`admission/verifier.py`, `aggregate_claims/aggregate_admission.py`, and
`client/runtime.py`. Mandatory exact-class TrustDomain/TrustBinding; no optional
None, default-allow guard, per-operation empty domain or callback replacement.
Factory computes one whole-adoption support ID and shares its original binding
with I/A owners. Existing mixed/import/client checks propagate it. Preserve
every original byte pin, exact-class/source-origin and postworker check.

Support ID must cover stable role/relative-name content pins, I/A images,
foundation/policy, native/author/producer/runtime/source closure. **Do not hash
raw RuntimeProfile.describe()**: generated preparation-profile paths/bytes and
relocation change despite unchanged support. Domain/support ID enter owner
profile identity; mutable withdrawal status does not become a cached verdict.
Ordinary startup must `TrustDomain.open(existing_dir, expected_domain_id,
expected_support_id)` and fail closed if missing/corrupt/mismatched. Explicit
`create(fresh_dir, domain_id, support_manifest)` is separate owner adoption,
never automatic startup behavior. One immutable adoption record plus a
create-only, flushed WITHDRAWN tombstone avoids a general policy database.
Any marker, including partial content, denies; observing invalidity latches
denial. No clear/reinstate API. Cleanup/reporting must remain callable.
Owner-serialized applied withdrawal is the primary guarantee. Cross-process
concurrent actions need an explicit final-check linearization rule, not an
unsupported instantaneous cancellation claim. Existing worker costs stay
charged; after observed withdrawal no live/cache/postworker/new-operation
authority may pass. Filesystem rollback or deliberate creation of a new domain
by the trusted owner is outside this local policy's guarantees, not silent
automatic recovery. Persistence must ship with the gate, not be left implicit.
