# Next core decision: bounded multi-source ordinary acquisition

2026-10-26. Source-only recommendation by `next_core_payoff`. Canonical guard
passed; source-only recommendation for root, not implementation/test authorization.

## One recommended selection

**Add explicit opt-in, bounded per-object sourcing across a small ordered set of
already approved contacts to ordinary receive.** Preserve the existing one-source
default, immutable evidence identities, one original budget and final local
checking. Do not add a new DHT, index feature, certificate or workflow engine.

The exact current obstruction is source-visible: `ordinary_sparse_access/
peer_api.py:608` chooses `provider = selection["provider"]`. Preview, selected
unit, every missing ExportID locator and every dependency unit all use that same
provider (:636-685), even when contacts contains other allowed holders. A vanished
original provider cannot be replaced inside the operation; fragments held by
different contacts cannot be composed by this receive path.

This matters after inert mirroring: making a second holder usable should not
require rediscovery of the theorem or manual restart of a whole receiving grant.
It also removes the receiver-side requirement that one selected endpoint supply
every cold dependency. The mirror's current *closed-bundle preparation* remains
unchanged; this proposal does not claim that it already prepares arbitrary
partial stores. Complete mirrors advertising this exact target supply the immediate
failover use case; split custody is conditional on the required byte kinds below.

**Availability condition.** Let K contain the exact advertised preview, selected
unit and any subsequently requested exact locators/dependency units. Every k in K
must be supplied by some opted-in contact within the original grant. Unit custody
alone is insufficient: mirror preparation derives previews only for its selected
indexed targets (`ordinary_inert_mirror02/mirror.py:320-336`), while receive fetches
the preview before evidence. A holder can possess the target's exact unit and
still lack its advertised preview. This policy must then refuse if no source
supplies that preview. Evidence-first/local preview derivation could remove this
obstruction but changes ordering/contract; it is not needed for selected-target
complete mirrors and is expressly outside this minimal recommendation.

## Existing work is not the missing capability

The investigator handoff, exact-module, anchor/query and six-hit Repair probes
already expose formal question/reuse routes. `ordinary_method_return/ADOPTION.md`
records real 21-group/155125-byte checked reuse and a new checked observation law.
None executes multi-holder acquisition; do not repeat them. Mirror parser/service
review belongs to its current reviewers, not this note.

Huge-network query coverage remains unsolved, but another route/filter or concept
proof does not make an already discovered result available after a provider fails.
Completed packaging/workflow repairs do not change these fixed-provider calls.

## Reuse and trust argument

`ordinary_authoring_offers/ordinary_acquisition.py:365-488` already accepts a
provider per exact fetch, all sharing one `OrdinaryBudget`. Preview recomputes
the committed record; locator binds semantic ID, name and ExportID to UnitID;
evidence checks exact bytes/semantic ID/export membership before retention.
`receive` deduplicates units, preflights the union against the original local
parent, and calls unchanged `owner.admit` only after READY.

Consequently source choice need not affect the mathematical acceptance relation:
for exact successfully validated bytes, replacing their transporting endpoint
leaves every input to the final preflight/checker unchanged. Source selection
adds availability opportunities, not authority. Parent/context conflicts, content
collisions, unsupported mathematics and checker failures remain terminal.

## Smallest policy, including the difficult failure boundary

- Opt-in config names a distinct ordered subset, e.g. at most eight labels from
  existing contacts, plus an attempt cap and post-acquisition time reserve. This
  list replaces acquisition order: no automatic original-provider prepend, all-
  contacts attempt or unsolicited referral. Preserve the original search provider
  as provenance; select acquisition sources separately.
- For each exact preview/locator/evidence key, try each selected source at most
  once in order. Do not restart search, change the parent or issue a fresh ledger.
  Explicit owner source maps are a simpler alternative for known fixed placement,
  but force users to know an unfamiliar proof closure beforehand and do not
  handle an unavailable mapped source. One bounded ordered list is preferable.
- Introduce a narrow typed unavailable outcome **only around network exchange**:
  an attempt's bounded timeout, connection refusal/reset, or truncated response
  (`asyncio.IncompleteReadError`), plus received HTTP404/503. Current Provider
  closes on missing custody rather than emitting404; EOF is not proof of absence.
  Do not inspect generic exception strings or catch BaseException to continue.
- Request/config/TLS-trust setup errors, malformed protocol/status400, invalid
  content identity/syntax, changed source/CA pins, cancellation, exhausted budget,
  local retention/SQLite errors, settlement errors and all checking failures are
  terminal in this first policy. It need not recover from every malicious reply.
  A failed TLS policy never authorizes downgrade or a different trust store.
- `_fetch` currently has one broad cleanup handler. A successor must distinguish
  the exchange stage from validation and local `retain`, and settle its request
  ticket before exposing the typed retryable outcome. Catching TimeoutError or
  OSError around a whole client method is incorrect: local retention can raise
  them too. Handle HTTP404/503 as typed statuses, not message-string matches;
  reject TLS/trust errors even if subclasses overlap retryable transport types.
  Local writes must never masquerade as bad peers. Failed attempts keep the full
  reserved reply cap: no failed-byte refund or grant replenishment by a new holder.

**Time principle.** Let D be the fixed network deadline, no later than the
original ledger/operation deadline minus an explicit local-finalization reserve.
With r sources remaining and c the existing HTTP close allowance (one second),
choose attempt wait t <= min(configured cap, (D-now-r*c)/r); refuse if no positive
allowance remains. Later attempts recompute only from this same D. Thus a stalled
network wait cannot consume the reserved later-source slots. This is conditional
on bounded/cooperative local overhead: synchronous TLS/parsing/storage and outer
Job limits may still terminate the operation. It guarantees neither a successful
second provider nor enough time to check arbitrary proofs. No extra concurrent
requests or memory-heavy service is necessary.

## Comparator, payoff region and decisive evidence

Ordinary Git/Lake imports from a known approved complete library are usually
simpler; do not force this policy on them. Current manual selection of a known
complete mirror, or copying one complete retained bundle for intake, also works
and remains preferable when cheap. Multi-source acquisition is useful when a
selected source is unavailable or no one reachable contact supplies the needed
union, but approved alternatives do, within the original caps. It saves manual
whole-operation restarts/forced central aggregation, not kernel proof work.

For m selected fetch keys and p opted-in sources, attempts are bounded by m*p
and by the existing request/byte/time grant; no term enumerates global peers N.
Worst-case failed-cap charges can be large. Compare those, TLS/setup, metadata,
provider load and implementation maintenance against the avoided restart or
whole-closure replication/aggregation. No numeric speedup or general growth
advantage follows, and relevant source coverage remains an assumption.

First review the typed-failure/time/accounting contract in source; no experiment
is needed to rediscover the fixed-provider obstruction. If selected, use one
small native-free changed-boundary suite with exact retained inert bytes: first
source unavailable then second succeeds; two sources supply different exact
units; first stalls without consuming the second slot; invalid identity and local
retain failures do not fall back; failed tickets stay charged; selected-unit-only
still makes zero ancestor calls; available evidence without the required preview
still refuses. Reuse unchanged admission evidence; owner doubles are not Lean
acceptance. One bounded real HTTP seam is warranted only if those transport/error
classifications cannot otherwise be resolved.

Stop after the selected multi-source boundary is exact and reviewed; do not add
automatic provider discovery, partial-mirror preparation, retries across renewed
grants or another concept episode. If it requires those expansions to serve the
selected complete-mirror use case, prefer the existing explicit mirror switch.
Full v5 remains active, local/unpublished; no new package or public trial is selected.
