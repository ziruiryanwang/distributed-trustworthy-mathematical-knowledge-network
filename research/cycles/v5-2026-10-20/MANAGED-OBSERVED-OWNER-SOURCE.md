# Observed managed owner: bounded failed-close diagnostics

2026-10-21, core_release. Source-only implementation under
MANAGED-CONTRIBUTION02-SELECTION. No import, test, syntax execution, build,
service, credential access, state migration, deletion or Git mutation.

New source: `software/v5/managed_observed/client/managed_owner.py`,31626bytes,
SHA-256 `1c022737e4d51a25d873e6fd255cd87ee8427f21d7455f78b29d4b2e4d133503`.
Frozen predecessor `software/v5/managed_contribution/client/managed_owner.py`
remains26492bytes/SHA-256
`75c0e8a93c26594d459e716cf55dc6c982b1df079eeaed7834a1347fe4a40d09`.

Read-only reconstruction confirmed byte-for-byte equality outside exactly
three selected changes: the diagnostic helpers/constants, initialization of
the retained local service reference, and one post-cleanup observation call.
Original EOF/remaining source bytes are preserved.

## Narrow behavior

The worker initializes `service=None`, then retains the exact object returned
by its existing `services.service(generation)` after successful start. After
the existing `services.close()` attempt and exception collection, it appends
`report["service_close_observation"] = _service_close_observation(service)`.
Thus the cached actual final service report is projected even when the strict
composer returns a `GENERATIONS_CLOSE_UNPROVEN` exception instead of that report.
No extra close, retry, await, callback, process or admission operation is added.

The new pure `_project_service_close(raw)` retains only:

- Recognized final/live report kind, known CLOSED/FAILED status and the two
  selected service failure codes; unexpected strings are fixed redactions.
- The seven cleanup booleans and at most32 cleanup rows, restricted to the
  exact source component vocabulary and `CLEANUP_UNCERTAIN`. Truncation and
  missing/invalid list status are explicit.
- Location closed/channel-failed/forced-termination flags, bounded byte/frame
  counters and an integer exit code. No stderr content, source maps or paths.
- Intake flags, active/closing counts and the eleven fixed usage counters.
  No token, credential, limits/bindings, route, arbitrary nested field or string.

Exact builtin bool/int types are required; counters outside0..2^53-1 and exit
codes outside-2^31..2^32-1 become null. The projected serialization is capped at
8192bytes. Its schema is `DMKN_V5_MANAGED_SERVICE_CLOSE_OBSERVATION_V1`, with
`closure_authority=false` and `mathematical_acceptance=false` in every outcome.

`_service_close_observation` catches report/projection failures without calling
`_error`, str or repr, returning a fixed OBSERVATION_UNAVAILABLE result. A missing
owned reference gives NO_OWNED_SERVICE. An incomplete live snapshot remains
PARTIAL_SNAPSHOT, never a claimed final close. Existing exception precedence,
all cleanup attempts, manager.close, original budgets and strict CLOSED/sealed
success checks remain unchanged. The predecessor's general `_error` behavior is
unchanged; this is a privacy claim only about the newly added observation.

## Review/test boundary

Ready for independent changed-boundary review. Suggested minimum controls:
known failed-close projection; sentinel secrets in ignored/unknown fields;
wrong scalar types/oversized numbers and more than32 error rows; throwing report
and no service; source/wiring confirmation that original primary/close failure
and CLOSED checks remain. Do not rerun proof, network, storage or old controls
for these pure helpers. Root owns any test/build/public02 selection.

This is one replacement of `v5/client/managed_owner.py` in a future127-entry
SDK map. Existing owner/worker/result V2 schemas and every other selected logical
module remain unchanged; the diagnostic field is additive operational evidence,
not an accepted closure input or mathematical certificate.
