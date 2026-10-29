# Common receiver seam for exact dependency location

2026-10-28, growth_design_audit. Source-only response to [SELECTION.md](SELECTION.md)
and [OPERATOR-MODEL.md](OPERATOR-MODEL.md). No implementation, import, database
open, runtime, network, benchmark or Git change. This note resolves the common
reader boundary; it does not select or audit the DHT or grouped-membership backend.

**The existing mathematical admission API can remain unchanged.** The required
work is in bounded asynchronous acquisition: preserving a learned endpoint's
identity, owner permission and expiry through locator and evidence requests,
under the original aggregate grant. A returned endpoint dictionary is not enough.
The existing owned discovery transport is the smallest reusable transport base.

**Immediate priority:** repair the current fixed-provider acquisition transport
before selecting a new location backend. That repair needs no learned-candidate
API or location protocol. The dynamic design later in this note is a separate
possible successor, not a prerequisite for correcting the current workflow.

## What the reader already does

The selected `ordinary_registration_refresh/peer_api.py` has a useful separation:

1. Validate owner/context and acquire the selected preview/evidence.
2. Call synchronous `owner.preflight(parent, raw_units, limits, budget)`.
3. For each missing `(name_raw, ExportID)`, asynchronously acquire an exact
   locator and, if necessary, its evidence unit; repeat the finite preflight loop.
4. Call `owner.admit(parent, plan, operation)` only after a READY plan.

These boundaries occur at lines 957-987, 993-1034 and 1035-1046. The
`selected-unit-only` branch at 1002-1010 deliberately stops with grounded
premises needed and performs no dependency lookup. Preserve that policy.

The missing key is **(SemanticID, ExportID)** plus the caller's expected exact
name. `OrdinaryAcquisition.locator` checks the semantic/export/name binding and
reveals UnitID; `evidence` then checks the exact unit and its output-name census
(`ordinary_multi_source/ordinary_acquisition.py:481-530`). If the unit is already
held, `receive:1030-1033` still verifies that it exports the expected name. Neither
unit location nor locator syntax establishes mathematical validity.

Configured fallback is already bounded to 1-8 supplier labels. `_ReceiveSources`
tries them sequentially, catches only `AcquisitionUnavailable`, preserves a
finalization reserve, and treats the client's ledger as authoritative
(`peer_api.py:831-911`). It does not accept learned endpoints. `configured()`
copies a finite 1-64 endpoint table (`transport/clients.py:16-22`), and the current
acquisition client checks label membership before every request.

`OrdinaryAdmission.preflight` plans from local context and inert bytes.
`admit` replans from those bytes and requires READY; it does not trust the caller's
missing list or READY assertion (`ordinary_parse_reuse/ordinary_admission.py:
530-537,577-604`). No network callback should be added to either method, the
native checker, catalog commit or evidence store. Located bytes must enter the
same existing validation and admission path.

## The transport gap is concrete

Current `OrdinaryAcquisition._fetch` calls `http_provider.exchange` with a
relative timeout (`ordinary_acquisition.py:392-446`). In the current
`ordinary_registration_refresh/http_provider.py:134-203`, TLS context setup
precedes creation of that timeout. Shortening only the ledger deadline does not
prevent a later dial after setup has consumed the endpoint's remaining lifetime.
Furthermore, its final writer-close path suppresses exceptions from
`writer.wait_closed()`. A typed unavailability exception from this path alone
does not establish observed cleanup before another supplier is tried.

`ordinary_connect_ownership/fair_exchange.py:84-189` already has the relevant
ownership and time discipline: it narrows a relative attempt to an absolute
deadline, checks the remaining time after TLS/address setup, owns the raw socket
before connect, and requires observed closure before returning a settled refusal.
After stream handoff, uncertainty is terminal. However, its closed route allowlist
currently covers discovery/contact routes, not ordinary locator/evidence reads.

Consequently, a selected receiver successor should use this owned transport for
**all of its preview, locator and evidence attempts**, including its configured
fast path. Upgrading only learned endpoints would leave the earlier configured
fallback's cleanup uncertainty in the same operation. This is a proposed narrow
successor; previously used transport sources and evidence remain frozen.

## Immediate fixed-provider successor

The smallest useful intervention changes two auxiliary source roles only:

1. A successor of `ordinary_acquisition.py` calls the existing owned exchange
   from `_fetch`. Compute the absolute attempt horizon from the original ledger
   deadline and the optional attempt cap, without renewing it after request/TLS
   setup; pass it explicitly to `X.exchange(..., absolute_deadline=...)`.
   No endpoint-learning hook, new config field or extra lookup is required.
2. A successor of `fair_exchange.py` adds the existing four typed ordinary read
   routes to its closed allowlist: preview, locator, evidence and authoring offers.
   Their existing `H.ROUTES` and ordinary request validators already supply finite
   reply/request shapes. Add no generic arbitrary-route escape hatch.

The fourth route matters: `OrdinaryAcquisition.authoring_offers:463-479` shares
`_fetch` but is currently excluded from the owned exchange allowlist. Keep that
existing explicit advisory API operational through the same owned transport;
do not leave a hidden old-transport branch or accidentally break its caller.
It keeps `unavailable_errors=False`, so a settled refusal remains a terminal
failure there, without retry or source execution. Its request parser and
`AO.read_reply` validator are unchanged.

Keep `_fetch`'s ticket creation, conservative `finally` settlement, exact byte
validation, before-commit liveness check and optional inert custody unchanged.
Preserve its public result shape and accounting scope. Translate only the narrow
settled failures in the failure table below when `unavailable_errors=True`.
In particular, `X.SettledRefusal("HTTP_PROTOCOL")` is **terminal**, not an
`AcquisitionUnavailable`, empty result or reason to try another supplier. TLS
errors, unknown failures, cancellation and uncertain close stay terminal too.

No `peer_api.py`, `owner.py`, `profile.py`, mathematical admission code or native
helper needs to change for this immediate cut. The existing scheduler already
passes per-attempt caps; the original ledger deadline supplies the missing
absolute cap to transport. Existing entrypoint/outer wall limits remain required
for synchronous work and cleanup. An outer timeout is not a substitute for the
new predial deadline check or an observation of socket closure.

This addresses a real existing-use failure boundary independently of whether
unknown-custodian routing is worth building. Changed-boundary tests can use an
ordinary typed request with a fake transport/setup clock to settle late-setup,
response-validation and charging behavior, and the existing owned-socket controls
for ownership. A finite actual fixed-provider path may then confirm integration;
another mathematical proof campaign or routing experiment is unnecessary.

### Profile, implementation and anchor compatibility

The full investigator loader already includes both ordinary acquisition and
fair exchange in `SUPPORT` (`ordinary_advisory_query/profile.py:38-45`). Its
`PROFILE.json` pins every auxiliary payload. A two-role successor therefore
requires fresh source-map entries, payload hashes and PROFILE bytes, while the
loader source can remain byte-identical. Existing frozen distributions must not
be patched in place. The standalone inert host has a different frozen SOURCES
closure and does not currently include fair exchange; do not silently replace
its pinned acquisition helper with this successor.

Core mathematical implementation identity is bound by the separate installed
manifest/support groups (`ordinary_parse_reuse/ordinary_admission.py:224-244`).
These two transport helpers are auxiliary; keeping installation files/manifest
exact preserves core I and SemanticID. The earlier owned-connect assembly already
demonstrated this separation, but a new assembly must still verify its own exact
unchanged installation rather than borrow an old result label.

The local module anchor support identity is narrower than the package profile:
`ordinary_exact_module/module_export.py:29-65` includes owner.py, profile.py,
the module/controller/collector/store/native worker and specified mathematical
helpers. It does **not** include PROFILE.json, ordinary acquisition, fair exchange
or peer_api.py. `anchor_store.open_for_owner:761-800` hashes that selected support.
Thus the immediate two-helper cut can preserve existing anchor-support bytes and
identity, provided all listed owner/loader/math/helper pins stay exact. Verify
that descriptor equality at assembly; do not infer it merely from unchanged
core I. Altering shared owner.py/profile.py would change the anchor-support
identity and should be avoided for this repair. No native rebuild or anchor
migration is logically required by the two-helper change.

## Later dynamic-location source cut

The following additional work is needed only if root selects a learned-location
workflow. It is not part of the immediate fixed-provider repair above.

| Boundary | Smallest required change or exact reuse |
|---|---|
| Receive orchestration | Successor of the current receive/source scheduler accepts an optional finite location plan and privately bound candidates at missing-export boundaries. Keep existing closure/preflight/admit logic. |
| Ordinary typed client | Successor of `_fetch` accepts a private, non-network request-authority object, obtains the exact endpoint and absolute horizon, then uses owned transport. Existing locator/evidence validators, custody retention and `begin`/`finally settle` remain authoritative. |
| Owned transport | Extend the closed read-only route allowlist to ordinary preview/locator/evidence and the one selected advisory metadata route, with its explicit request/reply bounds. Preserve original socket ownership and cancellation/closure behavior. |
| Learned endpoint policy | Reuse `OwnerEgressPolicy` and immutable `Endpoint`; add a small operation-local bound-candidate representation, not a global registry. |
| Location I/O | A backend-specific bounded client runs only in orchestration, using its prepaid slice and the same owned transport. Its output is advisory candidates, never a plan or acceptance result. Backend protocol choice belongs to the other decision notes. |
| Packaging | Update only the selected successor roles, their profile/import closure and public configuration/docs. No new Lean binary, native relation, mathematical schema or owner-store migration follows from this seam. |

The conceptual private interface is `authorize(provider, route, request) ->
(exact_endpoint, absolute_horizon)`. It has **no network effects**: it checks
the original operation/ledger, owner policy, exact request-key binding and an
already issued immutable candidate. Configuration selects data, not arbitrary
Python callbacks or peer-supplied code. The authority object and candidate table
are constructed by the trusted orchestration module. A new bare label or an
unvalidated dictionary cannot silently enter the configured endpoint table.

This interface allows the existing `locator` and `evidence` call shapes to stay
intact. A bounded active candidate table can be replaced between missing demands,
only with no pending ticket; earlier per-demand attempt accounting is retained.
Do not grow one endpoint table in proportion to all encountered providers or
instantiate new ledgers to avoid table limits. Exact endpoint identity includes
address, port, TLS flag/name and owner trust binding; labels alone are not a
deduplication key.

## Permission and expiry carried to both dials

A private learned candidate needs the exact semantic/export key, canonical
expected name, immutable endpoint, owner-policy binding, lookup issuance identity,
reader-monotonic issuance start and absolute expiry. Its permitted ordinary
routes are locator for that ExportID and evidence for a UnitID established by a
successfully validated locator for the same demand. It is not a general capability
to query unrelated objects at an arbitrary address.

Reuse `contact_directory.endpoint_spec` for syntax and `OwnerEgressPolicy.endpoint`
for actual authorization (`ordinary_contact_federation/contact_directory.py:
63-122`). Public learned endpoints require canonical numeric public IPv4,
owner-approved ports and TLS; strict TLS names and the owner's system CA policy
remain. Loopback needs the separately explicit test policy. A remote response
cannot introduce a CA path, private destination, redirect or DNS resolution.
The current immutable-policy check pattern at `peer_api.py:184-206` is reusable,
but its single earliest-contact cutoff need not become the entire receive
operation's permanent deadline.

For request start `t0`, owner maximum hint age `a`, original network deadline `T`,
operation deadline `U`, finalization/cleanup reserve `R`, and a conservatively
translated upstream horizon `E`, require a candidate horizon

`e <= min(t0 + a, T, U - R, E)`.

`E` is supplied under the chosen backend's lifetime contract; a peer's arbitrary
wall-clock timestamp is not a reader-monotonic deadline. This boundary cannot
independently prove that a backend truthfully preserved upstream freshness. It
can enforce the owner's local maximum age and exact reply/request binding, and
must report the advisory status. The backend note must specify its conservative
lifetime translation before implementation. A fresh reply, callback entry or
duplicate hint must not renew an existing candidate: retain the earlier horizon
when merging duplicates within the operation.

The companion operator investigator reports a concrete upstream gap: current
maintained descriptors carry no lifetime field, and provider lookup does not
return the internal provider record's remaining TTL. Do not assume an existing
duration field supplies `E`. The proposed gateway contract must derive a bounded
remaining duration from the original advertisement/contact horizon, bind it to
the current descriptor/lookup reply, anchor each intermediate use to that
request's monotonic start, and clip it by local policy/deadline. The reader then
anchors the reported duration to its **original HTTP request start**, not receipt
time. Starting earlier conservatively charges transit/setup time. Replaying a
cached duration as a new full TTL would violate this contract; a nonce alone
does not prove an upstream peer preserved the horizon. This is an explicit
backend integration obligation, not an implemented freshness guarantee.

At each locator/evidence attempt, keep the initial attempt start and use
`min(e, original_operation_deadline, original_ledger_deadline, attempt_start + cap)`.
Check authority before transport; pass that absolute value to owned `exchange`,
whose post-TLS/address-setup check prevents a subsequent dial after the horizon.
The immutable endpoint/policy binding removes a mutable substitution window
under the existing trusted in-process/OS premise. Recheck authority after I/O
and before validation/retention. A locator fetched while permission was live
does not authorize an evidence dial after it expires.

Expired candidates can be filtered before an attempt is issued. Once `_fetch`
has begun a ticket, any expiry or other failure must pass through its existing
conservative settlement; it cannot refund the attempt or renew the deadline.
The smallest strict path treats begun-attempt expiry as terminal. Any later
choice to make it retryable requires an explicit no-dial/settled outcome, not
a broad exception catch. No change to mathematical truth follows from expiry:
it governs this operation's acquisition permission and resource exposure.

## One original aggregate resource grant

Keep `OrdinaryBudget` unchanged. It already supports prepaid external slices,
and `charge_external` requires sequence zero and no pending request
(`ordinary_acquisition.py:312-374`). Missing dependencies appear after ordinary
tickets have begun, so lazily calling `charge_external` at the first missing
export is invalid.

Before the first preview/evidence ticket, reserve the **whole selected location
slice**, including any bounded metadata traversal chosen by the backend. The
location client then enforces its finite subordinate request/reply counters as
the demands arise. The original ledger records that whole reservation, even
if unused; subordinate actual counters are explanatory and must not be added
again as fresh ledger charges. Search prepayments and all ordinary fetches share
that ledger. There is no refund, later top-up or fresh network deadline.

For standalone receive, perform this preparation before its first fetch. For
search-then-receive composition, the caller must create/reserve the common grant
before *any* fetch and preserve it across both phases. An already used ledger
without a reserved location slice can only perform its existing configured path
or refuse the requested extension. It cannot silently acquire a new slice.

Let `m` bound distinct missing export/name demands, `d` bound location metadata
requests per demand, and `p <= 8` bound distinct ordinary supplier candidates
per demand. Known and learned candidates share `p`: trying eight known suppliers
cannot then authorize eight learned suppliers. If lookup is deferred until known
failures, reserve at least one candidate slot for it, or explicitly accept that
the configured set can consume the whole opportunity. The simpler alternative
is merging the bounded candidate set before its first attempt.

For fixed per-response caps `L`, `C`, `V` for location, locator and evidence,
the conservative added bounds are

`requests <= m*d + 2*m*p`,

`reply authority <= m*d*L + m*p*(C + V)`.

Selected preview/evidence and discovery work are additional predeclared terms.
Existing request/byte caps may be smaller and stop the operation first. Reused
units can reduce evidence calls, but must retain exact output-name checks.
Request bodies and headers remain separately bounded by actual attempts times
`REQUEST_MAX` and `2*HEADER_MAX`; a reply budget is not a whole-wire byte budget.
Each attempted request also needs the existing close reserve within the same
outer deadline. CPU/memory and synchronous parsing require the existing process
containment; async timeout alone is insufficient.

This removes provider-population size from the reader's explicit fanout bound by
limiting selected attempts and accepting incomplete location. It does not prove
coverage, availability or logarithmic global discovery; those belong to the
chosen backend and its stated operating assumptions.

## Failure translation must be narrow

`fair_exchange.SettledRefusal` and current `AcquisitionUnavailable` have different
closed reason sets. Passing through strings would fail or inadvertently broaden
fallback. Preserve this explicit interpretation:

| Outcome | Proposed receiver behavior after charging |
|---|---|
| Owned transport confirms connection refusal/reset, broken pipe or its own attempt timeout | Translate the matching existing ordinary unavailability reason; another already authorized candidate may be tried. |
| Owned transport reports `PEER_EOF` | Map to ordinary `INCOMPLETE_READ` only because owned closure has completed. |
| Complete framed HTTP 404/503 | Preserve existing `HTTP_404`/`HTTP_503` unavailability handling. |
| `HTTP_PROTOCOL`, HTTP 400, invalid/mismatched locator/evidence, TLS/policy failure | Terminal typed failure; do not convert malformed or untrusted data into an empty successful answer. |
| Unobserved stream handoff/close, unknown local exception, cancellation, exhausted original grant | Terminal; no next provider dial. Preserve partial bytes/report and no new acceptance. |

The client still calls `budget.begin(maximum)` once per ordinary attempt and
`settle(ticket, actual_validated_length)` only for a successful validated result;
failure charges its full cap in `finally`. Retryable outcomes must not escape
before settlement and the original-grant liveness check. Location metadata
malformation may either be terminal or an explicitly bounded settled advisory
refusal, as selected by that client contract; it is never a valid empty/complete
location response.

## Why phase separation is sufficient, and what it cannot avoid

An async locator resolver may be invoked at the existing missing-frontier point,
before ordinary byte acquisition. A no-network authorization callback is then
invoked only when using its resulting private candidates. This is sufficient to
keep all networking outside mathematical admission. The final plan is still
recomputed by the unchanged owner and checked with the unchanged selected native
implementation. Subject to those existing trust premises, changing which
endpoint supplies exact bytes cannot increase the set of accepted statements.

A no-network callback alone cannot discover an unknown holder: some explicit
orchestration phase must perform and charge the chosen backend lookup. Nor can
an unchanged public `receive` be repeatedly restarted to discover one dependency
at a time without renewed-grant and repeated-target-fetch problems. Preserve one
operation/ledger and its finite missing-unit loop. The narrow orchestration
successor is cheaper and clearer than making admission resumable or adding a
persistent continuation protocol for this purpose.

No new experiment is needed to settle these source-level boundaries. If root
selects implementation, decisive changed-boundary checks are: expiry during
local TLS/address setup before each kind of dial; uncertain close forbidding
fallback; exact-key/name/UnitID substitution refusal; prepaid location work after
ordinary tickets without renewed authority; and one missing support export
resolved through a learned allowed endpoint. Reuse existing mathematical
admission evidence unless the implementation actually changes that boundary.

## Exact source bindings for this note

Paths are below `software/v5/`:

| Source | SHA-256 |
|---|---|
| `ordinary_registration_refresh/peer_api.py` | `12c29d1edb3f3bc0483d9fe01abb3a4c69dbc4cdc5225ead32c28842bb4699dc` |
| `ordinary_multi_source/ordinary_acquisition.py` | `076130f7a34b505df33ee550501d1c4276bb46e408ff226df765225933a0658e` |
| `ordinary_connect_ownership/fair_exchange.py` | `05cf2b5baef0130dbe3b43e594d6c800baf6b625c77125dd3356f59f78509575` |
| `ordinary_contact_federation/contact_directory.py` | `a77486e716eb774337f2aedc04771c34395b24a910848600a2eae702f8ae3eb4` |
| `ordinary_registration_refresh/http_provider.py` | `3ce581f4057b6694c6d99a697847984fe7431a695989018f3e179217712859a2` |
| `transport/clients.py` | `640d1344824829865060712370444b5051720ce7b0a741e8efc0da8a066c6464` |

This common reader cut is feasible in principle and reusable by either candidate
location design. It is not evidence that either backend's coverage or operating
cost justifies implementation. Root's whole-protocol choice remains necessary.
