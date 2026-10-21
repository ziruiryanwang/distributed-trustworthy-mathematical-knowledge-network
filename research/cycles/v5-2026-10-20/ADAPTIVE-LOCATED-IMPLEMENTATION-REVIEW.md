# Adaptive located-query implementation: independent source review

2026-10-20. Reviewer: core_growth. Canonical project root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

**GO for root's one selected finite structural control operation.** This is a
source judgment, not an executed result, mathematical acceptance, authenticated
network qualification or completion of v5. No runtime was launched by this review.

Reviewed helper: `software/v5/located_queries/client/located_queries.py`, SHA-256
`419df8428528203858eff69da43c7e3ed7e5634d06007dc5e30ca2f33df82c4e`.
Scope is `ADAPTIVE-LOCATED-SELECTION.md`; use the selected 110-source dependency
map plus the four adopted iterative-query successors, not historical logical-path
predecessors. Existing verifier, workflow, transport and direct-query sources
remain unchanged. The corresponding five control groups remain root-selected.

## Central invariants checked against the actual source

- Reservation takes one fresh exact reader/channel and one exact client. It
  binds the original grant, acquisition budget, namespace, egress policy,
  adoption, source pins, output paths and configuration. It does not fabricate
  a handoff or create an issuer. The new helper origin is registered with the
  actual owners; existing location/runtime adoption remains an explicit premise.
- There is one prospective external charge: requests are route attempts plus
  descriptors plus search requests; reply capacity is L.reply_bytes, which
  already contains S.bytes. Each generation validates all dimensions, debits
  both full vectors and records its row before retirement, construction or I/O.
  No empty, unavailable, failed or partly constructed generation refunds it.
- The same original child starts at most once. Each generation constructs the
  real ServiceLocatedWorkflow and uses actual observed_route/available_descriptor
  ticket parsing and settlement. Route termination/census diagnostics are kept;
  route event counts are not asserted to measure DHT wire traffic.
- Replacement requires quiescent workflow, search, structural and shared-budget
  tickets. Old search/workflow states are terminal, structural acquisition is
  retired without closing shared authority, and candidate/staging maps clear.
  Captured contact bindings reject replacement generations. The inherited
  semantic-reader guard also binds its original search/acquisition.
- Contact expiry comes from each descriptor's original absolute workflow expiry,
  narrowed by the already fixed deadline. It is not recomputed at handoff.
  Actual begin_search produces the SearchSession; no second session resets its
  caps. Contact policy and exact current generation are rechecked before use.
- No-contact is decided from unexpired retained contacts after settled work and
  live budget checks. Its workflow is permanently RETIRED_NO_CONTACTS even after
  the next generation starts. It is not global absence. Malformed/authentication
  failures, deadline races and cancellation stay failures.
- Mathematical warrants, checked evidence caches and custody are neither
  reissued nor reset by rotation. Ordinary admission/import rules remain intact;
  multiple warranted selections still precede one sealed READY context.

## Corrected issue: service lifetime is not mathematical lifetime

The first read found that generic check_origin required an open/unfailed channel,
which would invalidate local mathematical use after an ordinary service ending.
The reviewed hash removes that transport-liveness test from origin validation
and places it in validate_next. Generic checks still enforce original identities,
configuration and acquisition/grant authority. Expired searches/contacts reject
their own new work, but do not independently revoke previously issued warrants.
An actual failed client action still uses the existing fail-stop path.

Envelope ACTIVE is lifecycle state, not a promise that transport is running or
time remains. report exposes the same channel's closed/failed status and clamps
remaining time at zero. It cannot renew the envelope or original grant. Its
compact snapshot reads workflow scalars instead of calling the mutating workflow
report. The inherited search report may mark its own SearchSession expired;
binding does not confuse that local search state with mathematical authority.

## Failure ordering and review boundary

The async catch covers validation, charging, old-generation retirement and
partial new construction, not just route calls. A newly allocated row and any
partially attached workflow/search receive terminal markers before diagnostic
capture. Diagnostic failure is recorded without skipping awaited original-channel
cleanup; inherited failure handling closes the original budget/issuers. FAILED
is preserved through later close. The decorator's final active/census checks
remain outside the helper catch, so caller `finally: await client.close()` is
still mandatory; no claim of universal async cleanup by synchronous _fail is made.

No remaining source blocker was found within this changed boundary. The separate
control fixture's no-contact expectation was reconciled to RETIRED_NO_CONTACTS.
The five-group run uses real structural search and location parsers but inert
channel transport and issuers: it must not be reported as accepted mathematics,
real channel authentication, measured useful growth or a deployment test.
