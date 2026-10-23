# Known-provider-failure continuation: source checkpoint

2026-10-23, `ordinary_api_flow`. Canonical workspace guard PASS. Source-only:
no product/test import, compile, test, network, native operation, state opening,
package assembly, Git mutation or campaign execution was performed by this agent.
Root subsequently reported file-only assembly01 completed under exact plan
`ae60677f`; the selected `peer_api.py` below is now used/frozen. Controls are
still unused. Assembly adoption and actual control execution remain root-owned.

## Selected files and scope

Fresh source under `software/v5/ordinary_resilient_package/`:

- `peer_api.py`: SHA256
  `656e7c3ccfff7613bf04fdec9d1a3656a49a803ad2f5662916db9e86bbe4b95d`.
- `failure_controls.py`: SHA256
  `9f7b4e3d059f4e0821ecc6cf769fe6fd52c73e52790a5acf8a3abc1ad16ad154`.

The predecessor remains unchanged at `software/v5/ordinary_peer_package/peer_api.py`,
SHA256 `a05a7e9a4e40329bbf994cbd1926672bb8c0b02fd6754d8ef62db519718e709a`.
Read-only exact text comparison confirms the prefix before `find` is identical
after removing only the new `json`/`ssl` imports and new classifier; the entire
suffix starting at `receive` is byte-text-identical, including final newline.
No receive, publish, serve, discovery session, client, transport or verifier
implementation changes were made.

The earlier provisional review hash
`538501a27510348e2789ca069b73a88e4830a4f241a44ede7bd145ec376ef592`
included one accidental extra final LF (31,038 bytes). Before assembly selection,
that one byte was removed to restore the exact predecessor suffix. A read-only
in-memory SHA256 calculation confirms appending exactly `0a` to current 31,037
bytes reproduces the earlier hash. No executable code changed between those
hashes. No separate provisional file was retained; no evidence was overwritten.
Root and independent reviewer were informed that the actual selected hash, not
the earlier provisional clearance, must be audited. No package rerun is requested.

This implements the adopted decision
`ORDINARY-DISCOVERY-FAILURE-DECISION.md` SHA256
`08be1678d09689d4416782aa5cda20afecb22c9f338c334ca34c4484085c4032`.
Root owns package integration, actual launch selection, adoption and Git.

## Implemented contract

The private `_provider_error` predicate uses the exact ten exception types and
26 exact plain-ValueError codes in the adopted decision. There is no broad
OSError/SSL/ValueError or prefix recovery. Generic EXACT_FIELDS/HASH_ENCODING,
unknown failures, session/query/ticket faults and transport-contract violations
remain fatal. Exception subclasses do not inherit recovery automatically.

The only recovery catches surround the actual `await client.offer` and
`await client.candidates` expressions. Before accepting a recognized failure,
the code checks the original allowance, shared ledger active state, local CA
pins, session `_live` state/query/deadline and an empty pending-ticket set.
These checks are outside the recoverable await; any of their errors stops.
Cancellation is not caught by the new Exception handlers and reaches the
unchanged outer BaseException/PeerFailure behavior: stop, retain partial report.

A failed offer advances to the next configured provider. A failed candidate
request exits both its page loop and remaining partition loop, then advances.
No retry, referral, new endpoint/session/client, counter refund, grant renewal,
fresh deadline or parallel fan-out is added. Earlier offers and matches are
retained. SearchClient's original conservative settlement remains responsible
for all failed attempts; the wrapper never settles a ticket a second time.

`provider_errors` contains `{provider, phase, error}` using the existing sanitized
error encoding; at most one entry per distinct selected provider, hence at most
64. It is deliberately not an all-malformed-reply resilience guarantee.
Finished contacts with recovered errors report
`SELECTED_CONTACTS_FINISHED_WITH_PROVIDER_ERRORS_NO_COMPLETENESS_CLAIM`;
normal finish keeps the old termination string. Status is INCOMPLETE_SEARCH.
Global budget/deadline/failure and cleanup behavior otherwise remains unchanged.
All global completeness, verified scan coverage and mathematical acceptance
flags remain false. A request timeout can exhaust the whole remaining deadline;
no slow-peer fairness claim is made.

## Focused native-free control, authored but NOT RUN

CLI arguments are `--package --profile-sha256 --python-runtime --lean-runtime
--output`. The caller supplies an existing fresh output directory. The harness
pins and loads the selected future package once through its real entry/loader.
Its inner allowance is 50 wall / 30 controller CPU seconds; root must separately
select a finite external Job envelope before running it.

The single table uses the real SearchClient, SearchSession, summary decoder,
authenticated summary verifier and positive candidate verifier. Two tiny
in-memory authenticated fixtures are created once: P0 has two records in
partition 7 and one in partition 8; P2 has one different record in partition 7.
These are inert V1 metadata, not ordinary evidence or new mathematical fixtures.
The normal-path seam replaces only exchange; a constructor spy calls the real
initializer to observe identity. Explicit global-fault rows additionally inject
one named local/session fault. No proof verifier is mocked.

The main row is P0 offer, P0 verified page, P0 malformed second page, P1 refused
offer, P2 offer, P2 verified page. It requires exact earlier/later records and
offers, ordered sanitized failures, no P0 partition-8 request, one original
client/session, unchanged deadlines, one unchanged prepaid shared ledger and
retained private verified/dedup state. It distinguishes HTTP completed replies
from provider success: malformed received JSON is a completed HTTP request.

Expected accounting is six requests, three candidate pages/full scan allowances,
four charged candidate slots (one prior hit, two reserved failed-page slots, one
later hit), three provider/snapshot-attempt slots, two authenticated snapshots,
zero reservations and zero pending tickets. Received malformed bytes are charged
at actual length; P1 abandonment charges its full 16,384-byte offer cap. Exact
request-body and reply-byte totals are computed from the inert exchanges.
The shared OrdinaryBudget retains the entire original search prepayment, even
when all its outer byte/request balance is prepaid; only SearchSession decides
whether the next search reservation fits.

Other rows reuse those fixtures and retain the earlier verified match:

- Request cap four: stop before any P2 exchange, INCOMPLETE_SEARCH with
  `SESSION_BUDGET:requests`, no renewed cap.
- Cancellation and unexpected ValueError: stop globally, no recovered error entry.
- Original session deadline, shared-ledger deadline, caller allowance, CA-pin
  failure, changed session query and foreign pending ticket: a recognized timeout
  cannot bypass the respective global check.
- Oversized raw reply reaching the real session: fatal transport-byte-contract
  violation rather than provider-local continuation.

The deliberately foreign pending-ticket row requires that corruption remain
visible (one foreign pending item), not be silently erased to resume search.
Every real request's own reservation is settled; the harness does not repair the
injected session. All other rows require no pending tickets/reservations.
A separate cheap predicate table checks all 36 allowed instances and 18 rejected
instances, including subclasses, cancellation and generic validator errors.

Guards prohibit SQLite opens, subprocesses, owner/custody opens, provider start,
real exchange and asyncio connection/listener APIs. Event-loop internal wakeup
machinery is not a peer connection; no blanket socket constructor mock is used.
The report is `FAILURE-CONTROLS.json`, with exact per-row calls/charges and explicit
zero native/owner/peer-operation claims. Passing it would qualify only this
fake-exchange metadata boundary, not real networking, mathematics, scalability,
whole-product readiness or universal malformed-reply recovery.

## Handoff gate

Source inspection/self-comparison only is complete. Root reports assembled
profile `cda4df6bddca464655096f681e555364cf711fe5ff52a54375da4f72be1b3dfd`
at `experiments/v5-local-checks/ordinary-resilient-package-assembly-01/package`.
That report is not an independent outcome audit by this agent. The used peer
source is frozen; controls remain unused/editable pending independent source
review and a separate finite root selection. No test outcome is asserted.
