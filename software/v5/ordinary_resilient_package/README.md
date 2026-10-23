# Discovery that can continue after a failed provider

This small successor preserves the ordinary project/peer package and changes
only `peer_api.py`. No certificate, native-checker or wire-format change is needed.
The later [library-completion package](../ordinary_library_package/README.md)
includes this change; these are successive source checkpoints, not separate
networks or competing project roots.

Use the existing `peer.py find` interface. On a recognized provider-local failure,
search retains earlier matches, reports the failure, and continues to the next
already selected provider if the original allowance remains live. Failed attempts
stay charged. There is no retry, provider referral, new session or renewed budget.

The report adds `provider_errors` with provider, operation phase and sanitized
error information. Search remains incomplete positive discovery: no result is a
mathematical warrant, and an empty answer does not prove mathematical absence.

Recovery deliberately uses an exact exception/code allowlist. Unknown errors,
local pin failures, cancellation, exhausted budgets, deadline expiration and
session corruption still stop the call. This does not recover from every possible
malformed reply. One slow provider can consume the remaining wall-clock budget;
fair scheduling and acquisition failover are not supplied by this change.

## Evidence

The source and file-only assembly passed independent review. The assembled
profile is `cda4df6bddca464655096f681e555364cf711fe5ff52a54375da4f72be1b3dfd`.
All 115 other payloads remain unchanged. A preselection one-newline source/hash
discrepancy was retained and independently resolved, not treated as hash equality.

One focused native-free check passed all 11 scenarios and 54 classifier examples.
It used the real client, session and authenticated metadata verification with
fake transport replies. Earlier and later matches survived two failed providers;
global faults stopped correctly, with exact charges retained. It took 1.63 wall
seconds and 1.375 known CPU seconds. No sockets, native checking or owner state
were exercised. No broad networking, growth or final-release claim follows.

See the [combined independent review and outcomes](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-COMPLETION-AND-FAILURE-REVIEW.md).
The existing peer/package trust, platform and license limitations remain.
