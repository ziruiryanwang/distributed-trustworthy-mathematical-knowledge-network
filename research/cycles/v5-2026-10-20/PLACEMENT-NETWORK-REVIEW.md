# Placement network seam: independent design review

2026-10-21, adaptive_audit. Reviewed full proposal
`SELECTIVE-PLACEMENT-NETWORK-SEAM.md`, SHA-256
`e1514d572d646619bb164fcf00e0bd28ef238d6eb51aeaa18254d4f598ff1ac0`,
and root's `PLACEMENT-NETWORK-SELECTION.md`. **The three-module composition is
viable in principle. One concrete wire-disclosure issue must be resolved in
the new source before execution; no change to used core files is needed.**
This is not a source-code or runtime pass. No import, test, network launch,
product edit or Git mutation was performed for this review.

## Concrete issue: local diagnostics are not a safe wire projection

The unchanged controller saves incomplete outcomes containing
`reason = str(error)[:1000]`; `PlacementLedger.public()` copies `outcome`
unchanged. Returning that row directly on status or duplicate submit would
expose raw local exceptions, contradicting the new closed-error/no-raw-
diagnostics wire contract. The fact that current controls use harmless
injected strings is not a general guarantee.

Likewise existing locator publish results contain `error` and
`census.last_query_error`, built from arbitrary transport exception text in
`maintained_roles.mjs`. Preserving the exact bounded local route observation
does not authorize transmitting those strings to a bearer-token client.

Required resolution in new modules only:

- Keep original local ledger and bounded exact route-journal evidence intact.
- Project incomplete core outcomes to closed public codes plus validated
  request/phase/recovery/resource facts; omit raw reason/exception strings.
- Project route observations to validated statuses, binding IDs and bounded
  numeric counters; replace/omit raw diagnostic text. Successful status still
  requires the existing positive-dispatch checks, not merely a renamed code.
- Apply projection consistently to fresh responses, status, exact replay and
  restart observations; catching only the fresh handler exception is not enough.
- Add one focused no-secret/raw-diagnostic disclosure control, including saved
  status and route observation. No core campaign needs repeating.

Root and both authors received this issue promptly before source completion.
It is a precise implementation requirement, not grounds for another broad
architecture cycle or a new authentication scheme.

## Composition checks

The proposed separate intake listener is justified: the selected read route
table and synchronous dispatcher remain unchanged. Existing `_headers`, `_body`,
`_header` and `_write` helpers can be reused; `_body` itself accepts a supplied
length, while the old exchange's route/16KiB request limit must not be reused
as though it covered the new17KiB envelope. Validate each new route's bound
before reading its body; full response accounting includes the ledger wrapper.

One shared exact Workspace and event loop avoid competing lock owners and
SQLite-thread misuse. A synchronously claimed intake slot prevents overlapping
new placement actions. Existing-request detection must use explicit primary-key
absence; saved `observation_only` is not a fresh/duplicate discriminator.
Duplicate/status paths cannot reserve, fetch, reconcile, dispatch or write the
route journal. A cleanup exception after core receipt commit remains an error,
not an opportunity to resume publication behind a successful-looking response.

The service-wide route envelope is necessary because used core reservations
do not fund locator work. Commit a durable charged attempt before publication;
cancelled/lost/uncertain attempts remain consumed. Exact `_hint` checks match
selected source: key/status/no-error/positive ADD_PROVIDER write, with no remote
acknowledgement or mathematical claim. A later cell reuse cites only a bounded
historical observation; it is not another dispatch or renewed retention.

Existing locator `command()` has one lock, finite frame/byte counts, deadline
checks and poison/kill on failed in-channel exchange. The proposed H+2L+1<=60
bound fits its64-frame boundary, but must be checked against actual selected
configuration (large core max_cells does not automatically fit). Node transport,
maintenance and storage bounds remain separately funded. Only bounded health,
one active intake publication and finite cleanup may contend for that channel;
do not introduce per-request background queueing or automatic retries.

## Exposure and evidence boundaries

Explicit endpoint+epoch/generation/namespace/profile provisioning is the token's
authority boundary, not a DHT hint. Public client TLS keeps system CA/hostname
validation and no downloaded trust override. Plaintext loopback cannot yield
an authenticated-public-peer claim. TLS/authorization never supplies mathematical
acceptance; selected receiver verification remains separate.

Application connection/task quotas alone do not bound pre-handler TLS handshakes:
`asyncio.start_server(ssl=...)` performs these before its application callback.
State that scope honestly, keep finite handshake/cleanup timeouts and the
external process/OS exposure boundary. A hard public anti-DoS handshake cap must
not be claimed from the intake action cap or backlog setting. This does not
require adding a proxy or new infrastructure to the selected local integration.

The proposed one real submit -> identical replay -> publisher withdrawal ->
goal-only discovery/acquisition is the appropriate next composition discriminator.
Reuse retained mathematics and do not rerun passed local-placement controls.
Its evidence must distinguish structural retrieval from actual receiver
admission, and loopback from independent hosting/public TLS. Full-cost growth,
rollover and final release remain separate; no new campaign is selected here.
