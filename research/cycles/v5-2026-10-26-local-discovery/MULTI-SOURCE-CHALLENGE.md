# Challenge: bounded source substitution, not renewed receiving authority

2026-10-26. Source/theory only; no code/runtime/state/network/Git mutation.
Read NEXT-CORE-PAYOFF-AFTER-MIRROR and selected source. The optional boundary is
justified subject to this challenge; root owns implementation/runtime selection.

## Actual obstruction and cheapest alternatives

Selected P is `experiments/v5-local-checks/exact-module-assembly01/assembled/package`.
Its `peer_api.py` matches ordinary_sparse_access's source (SHA-256 `48ec02f0...`);
its acquisition helper matches ordinary_authoring_offers (`d4599471...`). Receive
lines 608-685 use one provider for preview, target and dependency reads. Another
configured contact is not a fallback. Lower calls already select per-object
providers and share one nonrenewing OrdinaryBudget.

Prefer a manual source switch when one known complete mirror can satisfy the
request; copying a complete bundle for intake also works. Prefer a per-object map
for known stable placement. Lower APIs can already acquire/check mixed-source
unions: the gap is public receive composition, not mathematical/networking power.

Concrete case: A serves the exact preview/target but lacks prerequisite U; B serves
U but lacks the target preview. Each single-source receive fails; a source list
handles the unfamiliar frontier without a precomputed placement map. This split
case concerns lower stores, not current closed-bundle mirrors. Vanished A plus
complete B is simpler, but B must hold the exact preview too: evidence-only custody
does not guarantee the unchanged preview-first workflow can use B.

## Minimal semantics

An absent option preserves existing behavior. An explicit `acquisition_sources`
is an ordered list of at most eight distinct already configured contact labels;
it replaces acquisition order. Do not silently prepend the discovery provider,
try all contacts, follow referrals or enlarge the list after failure. Preserve
selection.provider/snapshot as the record's discovery origin, not source authority.
For each exact fetch key, try each listed source at most once. Retain the ordinary
per-source contact/TLS pins and explicit disclosure to the selected recipients.

Keep preview hash/size/record resolution, locator name/ExportID/UnitID binding,
evidence identity/membership and local retention unchanged. Different objects may
come from different holders; two replies to the same key cannot silently select
different mathematics. Preserve the current bounded metadata-preflight rounds
and exactly one final owner.admit, not a fresh checking attempt/grant per source.
selected-unit-only must still issue no ancestor requests and return missing premises.

Conditional safety: under the existing hash, checker/policy and protected-state
premises, successfully validated exact bytes yield the same final preflight and
admission inputs regardless of supplier. Availability choices supply no warrants.
Content/name conflicts and unsupported mathematics remain terminal. This is a
transport-independence argument, not improved checker soundness or global search.

## Retryability must be decided at the exchange stage

H.exchange performs TLS/CA-file setup before its network try. Classifying errors
around the whole await is therefore still too broad. Prefer an opt-in typed
unavailable outcome INSIDE its network scope, after TLS setup: that scope's own
timeout manager must have expired, or a specifically allowed refusal/reset/
aborted/broken-pipe/IncompleteReadError occurred. Preserve the default behavior.
Framed HTTP404/503 can be classified after exchange; premature EOF cannot establish
absence. Prevalidating CA files outside H.exchange does not remove its later reads.

Do not catch broad OSError or whole-fetch TimeoutError: TLS/local permission,
retention or budget failures may share those types. HTTP404/503 currently collapse
into generic ValueError; classify before that collapse, never by error strings.
TLS verification/pin/configuration, malformed headers/status400, content parsing,
identity, retain/SQLite, cancellation, budget/settlement and checking failures are
terminal. Emit the typed outcome only after the existing finally settles its
ticket. Failed attempts retain their full response-cap charge; no second ledger.

Counterexample: valid A bytes reach custody, then a local write fails/has uncertain
completion. Retrying B cannot repair that uncertainty. Conversely a forged preview
from A stops this conservative policy even if honest B could succeed. A malformed
responder can deny this operation; no Byzantine liveness claim is made.

## Finite time and locality

Use one original ledger/operation deadline, not one deadline per provider. Reserve
local finalization time and the existing HTTP close allowance of at most one
second per attempted exchange. A configured network-wait cap is passed into
H.exchange; do not cancel the entire fetch/retention phase to simulate that cap.
Partition remaining time among remaining sources conservatively, rechecking the
same original deadline before each attempt. Synchronous parsing/TLS/local I/O and
outer containment remain assumptions; a reserved slot is not a success guarantee.

For m required fetch keys and p selected sources, attempts are at most mp and
also bounded by the original request/response-byte grant. Failed caps, request/
header overhead, source service and local parse/retention remain charged. A failed
8-MiB reserved fetch can exhaust an 8-MiB grant before B is tried; refusal is then
correct, not a reason to reset the grant. Source coverage and spare budget must
hold for the benefit region. No step enumerates global peers or the whole corpus.

## Footprint and stopping rule

Minimum justified footprint is three pure payloads: opt-in network-scope typing
inside H.exchange; acquisition per-attempt cap/status handling; optional source
orchestration at receive's four sites, plus selection/docs/tests. Reuse all wire,
contacts, ledger, closure and checking semantics; no new transport/search mechanism.
Test only classification/accounting/order/no-ancestor and one unreached transport
boundary if selected. Do not repeat Lean acceptance or the completed mirror gate.
If the implementation requires renewed grants or architectural expansion, stop
and use the existing explicit source switch/map. No growth speedup is established.
