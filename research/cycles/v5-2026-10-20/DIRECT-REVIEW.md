# Ordinary direct contacts: independent source review

Reviewer: `core_release`. Scope: source only, no imports, tests, proof production,
builds or Git operations. Canonical workspace guard passed on resumption.

## Disposition

No blocking defect found in the selected owner-configured composition under the
existing trusted-local-owner threat model. This is clearance for the root's
separately selected focused controls, not evidence that those controls ran or
that direct network acquisition or final v5 is qualified.

Reviewed `software/v5/client/direct_contacts.py` SHA-256:
`97b4ead3e85b47bb3d06b1574802669794d0f80ba57db5fe38b1577c3a20496f`.

Reviewed accompanying `software/v5/client/DIRECT-CONTACTS.md` SHA-256:
`80372d88d60c2399553c46dca2a72bd348f0a3150e8096668e791aa471b824f5`.

Root adopted the documentation recommendation: the owner does not mutate
client/session/contact/budget internals after construction. Consistency guards
do not provide hostile in-process memory isolation. No additional state
framework, acquisition subtype or per-instance method patch is required.

## Consequential invariants

1. **Original operation.** The helper accepts the exact validated `CommonsClient`,
   uses its existing `_action`, `_enter`, `_active`, `_census` and fail-stop
   lifecycle, and consumes the same one-query slot as `find`. It does not issue a
   grant, construct a new client, replenish resources or create a new owner.

2. **Adopted source, not self-authorized hashing.** The helper's resolved source
   path must already occur in at least one actual issuer's selected `_pins`; all
   matching issuer pins must agree. The existing source-origin checks then
   include this helper. Computing the current file's hash is not substituted
   for prior source selection or mathematical authority.

3. **Finite search and acquisition.** The fresh exact `SearchSession` validates
   its ordinary limits, clamps its deadline to the original grant and uses the
   same clock as the exact `_LocatedSearchClient`. Its whole request/reply-byte
   suballocation is charged to the original acquisition budget before any dial.
   Setup failure does not refund it. Acquisition consumes the remainder of that
   same budget. Request/framing, storage and provider costs retain their existing
   separate accounting scopes; this is not a claim of one all-inclusive counter.

4. **Explicit contacts.** Exact `OwnerEgressPolicy` converts the owner's finite
   contact map to existing endpoints, rejects duplicate endpoints and limits
   providers. Expiries are bounded by the original grant. Existing validated
   search checks egress/expiry and settles unsuccessful attempts. Structural
   custody validates its guarded contact immediately before dialing. Remote
   replies cannot add endpoints, choose CAs or renew an expiry.

5. **No invented location.** `_LocatedSearchClient` is reused because existing
   validation requires that concrete guard. No location process, workflow or
   authenticated handoff is fabricated. The client retains `None` for channel
   and handoff, reports no location operation, and labels the origin explicitly
   as owner-configured. Its historical class name is not DHT evidence.

6. **Search-to-custody origin.** The exact `EvidenceAcquisition` shares the
   original stores, profile and budget and retains `verifier=None`. Both it and
   the client refer to the same actual search session. Inherited export requires
   the exact `(object_id, record_id)` in that session's returned candidates.
   `_Contact` rechecks selected owner bindings on the custody path. Constructor
   validation occurs before `binding.acquisition` is set and is intentionally
   allowed; post-construction checks require that exact acquisition.

7. **Mathematics unchanged.** A search hit and a structurally retrieved export
   are not live warrants. Packet offering, exact packet/summary bindings,
   custody readback and actual receipt/aggregate/native admission remain in the
   existing client. The helper neither installs a verifier in acquisition nor
   creates a handle, acceptance result or alternate mathematical mode.

8. **No new resource lifetime.** Binding itself performs no network I/O, starts
   no worker and opens no store. Original client/workspace close owns the
   existing resources and failure cleanup. A later acquisition can continue
   after the search phase's shorter deadline, but only within original grant
   and contact lifetime; that is not renewal of the completed search.

## Limits and next evidence

Python owner code is trusted and serialized. It can defeat private-state
guards by arbitrary in-process rewriting; the helper does not claim otherwise.
No new requirement to resist that threat should displace remote-input,
same-grant, candidate-origin and genuine-admission controls.

Focused tests should cover binding/prepayment/refusal/lifecycle boundaries and
one actual direct offer/page/structural resolution. The higher-value follow-up
is ordinary service-to-real-client mathematical use with retained evidence,
not repeated RAM work or another isolated transport campaign. Source review
does not establish worldwide coverage, public TLS deployment, continued
availability, net useful-growth advantage or aggregate certification.

## Exact focused-control selection reviewed

Source/closure clearance for one root-selected run:

- Selector `Select-DirectChecks.ps1`:
  `75d35547783bfb2e4b5f9c2ddf43b6e1bb823945fec87cc9da3a9646d86314fe`.
- `client/test_direct_contacts.py`:
  `5707cc9c334ca602fe41b56079e5725be30c5c21cc6b2c7591c77b0c9953906b`.
- `experiments/v5-local-checks/direct-contact-controls-01-selection.json`:
  `120597af89c992d48cd288f1ff9d0c033fbd23dd74c04b21fec49a652c1d11bd`.

Independently hashed all 84 source pins and 19 runtime pins with zero mismatch.
The selector reuses the exact serving03 selection, removes historical test
sources and legacy location aliases, and selects the seven ordinary
`portable_runtime/location` files. Protocol/workflow bytes equal the reviewed
implementations. Only the one new direct-control test remains.

All nine controls are source-reviewed. The fixture explicitly bypasses actual
issuer construction and liveness/census/reporting while retaining the exact
facade, decorators, grant, budget, search, index/custody and lifecycle paths.
The positive case is three actual loopback exchanges with returned-metadata
candidate selection, not proof checking. Out-of-scope endpoint rewriting cases
were removed before selection; one guarded disconnected-search consistency
case remains. No runtime has been performed by this reviewer.

Bounds: 30 CPU seconds, 90 wall seconds, 256 MiB, two active processes,
1 MiB stdout and stderr each. Native subprocess creation is prohibited inside
the test. This clearance does not predict or record a passing outcome.

## Actual saved-outcome audit

**PASS for all nine selected changed-boundary controls**, executed once by root
at `experiments/v5-local-checks/direct-contact-controls-01`; no rerun is needed.
Independently read the outer result, command and stderr, and inner result.
Rehashed all 84 original/snapshot source pairs, all 19 runtime pins and all 80
reported imported origins: zero mismatches. Saved selection has the exact
reviewed hash above.

The actual positive path made three real loopback requests and resolved one
previously unknown-ID structural candidate through returned index metadata.
The suite constructed 17 explicit inert clients. All genuine verification,
proof, native subprocess and public-network counters are zero. This is not
mathematical admission evidence; the source and controls preserve that limit.

Exit zero; nine tests, no failures/errors/skips. Known CPU:
`1.265625` inclusive Job + `0.421875` wrapper = **1.6875 seconds**.
Outer wall `5.078536600340158` seconds. Peak Job private commit `31,473,664`
bytes. Direct child reaped, final active processes zero, Job closed, no cleanup
errors and no termination request.

Evidence SHA-256:

- Outer result:
  `0ae3f47ef43f1da642d7d1f87d4235be72bd441579c59ec1eea3f04001765125`.
- Inner result:
  `3baf28e9df4dc2e5349d770f07e3a9dd29cabe0ed5afc24b9e6fce2226509a34`.
- Stderr:
  `0814c4ae819463c75b84c805144eb4871b35961025694535bc633f4de3a2969c`.

This closes the selected direct-contact facade boundary. Continue to the
ordinary real-reader integration rather than repeating these passing controls.
Final v5 and actual aggregate certification remain open.
