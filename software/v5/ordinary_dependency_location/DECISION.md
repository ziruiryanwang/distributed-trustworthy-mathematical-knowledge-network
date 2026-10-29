# Exact dependency location: reader interface and operator cost

2026-10-28. Source-only decision under [SELECTION.md](SELECTION.md). No code,
database, runtime, network or product change is selected by this note. Earlier
used sources and evidence remain frozen.

## Decision

The gap is real for open custody: a reader can discover a result yet fail to
obtain its proof-only dependencies because their holders are outside its chosen
supplier set. Existing exact retrieval already solves the closed-supplier case.
Location adds an availability opportunity; it changes neither mathematical
acceptance nor the possibility that a selected finite workflow must stop.

Recommend a complete **ordinary exact-export location** composition as the next
implementation target: one-hop advisory HTTP for the reader, then the existing
exact locator/evidence checks, with the retained maintained DHT available behind
an operator gateway. Readers need no Node runtime, inbound service or global
provider list. This is a recommendation for root's separate selection, not an
implementation authorization or an existing compatibility claim.

Do not select a whole-map-only product as the huge-network answer. A bounded
map is a useful small-federation backend or controlled fixture, but neither its
coverage nor its cumulative update cost establishes the intended scale property.
Likewise, wrapping the unchanged DHT in HTTP is insufficient: ordinary identity,
incremental advertisement cost, endpoint expiry and the complete receive path
are consequential implementation seams. If those seams cannot fit a justified
finite implementation, retain configured fallback and defer the addition; a
parser or another synthetic map benchmark would not close this workflow.

## The key the reader actually knows

`ordinary_registration_refresh/peer_api.py:1012-1034` iterates missing pairs
`(name_raw, ExportID)` under the loaded `SemanticID`. It first requests a locator
for that export and expected name, learns `UnitID`, then requests evidence with
the expected export/name. Therefore the first location key is
**`(SemanticID, ExportID)`**, with the known name checked at the ordinary locator
boundary. It is not an index feature or, initially, a UnitID.

`ordinary_lean/ordinary_semantics.py:198-201` hashes semantic identity, UnitID and
original name into ExportID. Its digest does not let a reader recover UnitID,
bundle identity, repository or module. Changing this identity/frontier to avoid
location would change the mathematical interchange contract and is outside the
narrow proposal.

`ordinary_multi_source/ordinary_acquisition.py:172-216` already creates locators
for every output of every retained evidence unit, transactionally with custody.
Its `get_locator` at271-294 uses the indexed export key and checks that evidence
is retained. A custodian answering for itself should reuse this exact lookup;
it needs no second all-export inventory, formal preview or global provider map.
The new sparse host already retains supplied support-only units. Asking known
custodians this question is precisely the existing configured-source solution.

## Alternatives and what each buys

| Composition | Useful scope | Cost or missing boundary |
|---|---|---|
| Existing configured fallback | A deliberately closed set of suppliers, including support-only custody | Already implemented:1-8 selected labels, exact locator/evidence, one shared ledger/deadline. Cannot learn a ninth, previously unknown holder. |
| Custodian answers for itself | One known custodian with many exports | Existing indexed `get_locator`; per-append export insertion already follows new evidence. Adding an advisory self-endpoint reply buys little over that route. |
| Bounded exact-key map over remote custodians | Small curated federation and finite handoffs | New route/client needed. Bounded startup/replacement scans are O(K) metadata; rebuilding after each append can be quadratic across cumulative growth. No whole-proof re-export is needed, but metadata cost remains. |
| Incremental exact registry at a selected operator | Many registrations, where operators can accept central or sharded registration | Viable alternative to DHT. Requires maintained registration/update/expiry, quotas, recovery and lookup implementation; the present immutable contact/authoring maps do not provide it. It must not be described as an already available cheap map. |
| Retained DHT behind an HTTP gateway | Independently advertised custody across participating operators | Reuses actual routing, intents, expiry and descriptor machinery. Requires a distinct ordinary-export role and complete gateway/reader integration; current publish counting is O(K) per call. |
| Bundles, modules and authoring handoffs | Already known packages or an approved normal Lean dependency | Can amortize transfer/endpoint metadata. Present artifacts do not resolve an arbitrary missing ExportID to a package or holder; see below. |

`peer_api.py:831-915` already makes fallback sequential and bounded, sharing one
deadline and reserving cleanup time. It catches only typed acquisition
unavailability, not arbitrary validation/cleanup exceptions. Keep this fast path
for callers who already know their suppliers. Do not make readers crawl formal
indexes for proof-only dependencies: `ContactMap` is about index predicates,
and a `type-symbol` feature means occurrence/relevance, not exact custody.

The [earlier routing choice](../../../research/cycles/v5-2026-10-25-software-continuation/RESUMED-ROUTING-CHOICE.md)
already rejected mandatory DHT readers. That decision need not be reopened.
Its 5,896-payload runtime census and192MiB code-enforced memory ceiling are
operator deployment burdens, not a measured memory claim. Reusing a retained
stack is a reason to compare it, not evidence that its maintenance is cheaper
than an incremental registry for a particular operator population.

## Bundle-level advertisement does not presently remove the first-hop key

The current baseline manifest contains `SemanticID` and batches of
`{unit_id,raw_sha256,raw_bytes}` (`ordinary_binding_reuse/baseline_bundle.py:96-126,
221-254`). The contribution companion keeps all supplied units but its separate
target list covers selected targets, not every support-only export
(`ordinary_contribution_bundle/project.py:279-325`). One can derive exact member
exports from the newly supplied unit bytes without re-exporting earlier proofs;
an unheld bundle cannot be selected from an arbitrary ExportID by these fields.

`ordinary_authoring_offers/authoring_offers.py:19-34,139-176` already maps the
exact semantic/export pair to repository, commit, project, module and export-name
hints. It still pays one entry per mapped export and makes no custody-availability
claim. Following Git hints adds source acquisition and explicit execution/trust
work; it is not an inert dependency fallback. Locally generated `MODULE.json`
records checked module targets/artifacts, not a discoverable network membership
service (`ordinary_module_package/README.md`, export/read-result sections).

Thus advertising a bundle endpoint once can amortize endpoint renewal only
after some discoverable ExportID-to-bundle membership is supplied. An existing
handoff containing that mapping is useful for its named members; it cannot
locate arbitrary imports beyond its supplied coverage. A new membership index
would move the per-export registration/storage cost, not erase it. No present
artifact found permits bundle-only routing to replace exact-export location
unchanged.

That is a reuse-as-is obstruction, not an argument against modifying the handoff.
A discovered target already supplies UnitID. Optional acquisition-hint metadata
could associate a known contribution bundle with its member locators and direct
import bundles. This could pay membership encoding/indexing once per immutable
bundle while renewing one bundle/provider advertisement for many exports. It
would need exact semantic/member binding, bounded hint traversal and ordinary
byte validation; an advisory membership claim never establishes acceptance.
Overlapping bundles can duplicate membership, corrections create new metadata,
and missing/stale hint graphs still leave arbitrary ExportIDs unresolved. Such
grouping is plausibly cheaper than per-export renewal for coherent contribution
packages, and deserves comparison before committing to universal per-export DHT
publication. It is a separate proposed modification, not an available manifest
field or a new schema selected here. Retain the exact-key fallback boundary for
imports outside supplied grouped hints. Prefer normal pinned package imports
when they already supply the required mathematics; do not generate a new closure
module merely to manufacture a hint.

## Minimum complete reader composition

1. The owner chooses a finite directory/gateway set, exact egress policy, maximum
   missing-export demands `m`, at most `d` directory requests per demand, an
   aggregate cap `p` on distinct supplier endpoints tried per demand, reply caps,
   and one original operation deadline with finalization reserve. Known suppliers
   and learned suppliers share that `p` attempt set; no recursive referrals.
2. Before the first preview/evidence acquisition ticket, prepay the entire
   permitted location slice in the existing `OrdinaryBudget`, including failed
   or unused reserved lookup capacity. Enforce its finite counters separately.
   `charge_external` requires `sequence == 0` (`ordinary_acquisition.py:311-375`);
   missing imports arise later. Do not reset the ledger or lazily call prepayment
   at the first dependency. An alternative integrated ticket design would need
   an explicit contract; no relaxation of this guard is implied.
3. For a missing semantic/export key, an advisory reply binds that exact request
   and returns only bounded candidate endpoints. It declares incomplete coverage,
   truncation/failure and no mathematical acceptance. Authenticating a directory
   or Noise peer identifies the source of a claim, not custody or correctness.
4. Validate each endpoint with the retained strict learned-contact policy: public
   canonical numeric IPv4, owner-approved ports, HTTPS, strict TLS name and only
   owner/system CA authority. Loopback requires the separate explicit test policy.
   A reply cannot select private addresses, CA paths, redirects or DNS expansion.
   Freeze the endpoint/policy binding. Lifetime begins at the reader's monotonic
   request start and is clipped by its original deadline; response arrival and
   remote timestamps cannot renew it. A gateway must not extend an upstream hint
   horizon; expired/unknown-authority descriptors require fresh bounded lookup.
5. Preserve the private endpoint, owner policy and absolute expiry through both
   locator and evidence acquisition. Revalidate them before each dial. Retrieve
   the exact locator/name, derive UnitID, retrieve exact evidence, check its
   semantic/export/name binding and then perform the ordinary local checking.
   A valid locator is not an output census or a mathematical warrant. If the
   unit is already present, reuse the existing exact-name membership check.
6. Charge every attempt, including unavailable or malformed replies, retain the
   existing conservative failure-byte charge, and stop on exhausted authority,
   invalid data or uncertain cleanup. Only explicitly settled unavailability may
   advance to the next bounded candidate. Report partial location/acquisition
   and unmet demands without describing them as global absence.

There is a real transport seam. Current ordinary acquisition calls
`http_provider.exchange` with relative timeout; TLS setup precedes its network
timeout. Shortening the ledger deadline alone does not prevent a dial after a
learned hint expires during setup. `ordinary_connect_ownership/fair_exchange.py:84-143`
already checks an absolute deadline after TLS/address setup and owns the raw
socket through cleanup, but its route allowlist excludes locator/evidence and
the proposed lookup. A narrow typed transport/client extension must preserve
that boundary and the ordinary validator/accounting path. Returning bare learned
endpoint dictionaries into configured receive would discard the expiry authority.

For `m` distinct missing exports, conservative reader work is at most `dm`
location calls plus `2mp` locator/evidence attempts, plus the explicitly reserved
target/search work. Shared units can reduce this bound. Enforce the original
request/reply-byte caps even when this algebraic maximum is larger; also report
request/header upper bounds and outer wall/CPU/memory containment. Global holder
count `N` does not appear as reader fanout because coverage is delegated and
incomplete, not because discovering all holders has become free.

## Operator publication and conditional scale

Use advertisements derived from **all outputs of newly supplied units**, not just
preview targets. Reuse the existing locator derivation. Publish only after local
custody commits; if append reporting is uncertain, verify each proposed export
against the custodian's existing exact lookup before advertising. Partial commits
are legal. Lost/failed publication means potentially undiscoverable custody;
stale publication means a possibly unavailable candidate. Neither may weaken
exact retrieval. An operator answering for its own custody needs no remote
registration protocol at all; remote registration is a separate capability.

The retained DHT's body domain is currently
`{foundation,policy,module_schema,body_schema}` and its reference includes
`{module_id,export_id,universes,body_hash}`
(`body_location/portable/location/protocol.py:177-240`). Those are different
identities. Reuse its algorithm and lifecycle, but explicitly extend the closed
domain/role, intent, IPC command and descriptor validation for ordinary exports.
Do not substitute an ordinary hash into a certified-body field. Gateway/provider
operators may run its current listening, publicly announced `clientMode:false`
service; readers remain outbound HTTP clients.

Retained intents, provider TTL/reprovide and withdrawal already express useful
lifecycle semantics. `_publishRoute` reports
`HINT_DISPATCHED_UNACKNOWLEDGED`, with `remote_placement_confirmed:false`;
withdrawal stops local renewal and does not instantly erase remote hints.
No advertisement establishes continued availability. Registration must be
operator-authorized, quota-bound and scoped to the finite service lease;
untrusted hints must not become an unbounded write/renewal obligation.

The current implementation is **not O(delta) publication**:
`maintained_roles.mjs:226-234` scans every `/application/published/` key before
every publish, including repeat keys. Adding `n` keys can visit Theta(n^2) local
keys. The local advertisement cap is4,096; the reprovide queue is32 with
concurrency2. A scale implementation must either explicitly accept that finite
scope or replace the repeated count scan with durable quota/count maintenance
and bounded recovery before claiming incremental cost. One-time corpus bootstrap,
new output parsing, per-export intent writes, replication and subsequent TTL
renewal all remain charged. No complete earlier proof corpus need be re-exported
or globally reindexed on each append. Sharding beyond local caps is operational
work and does not follow automatically from a gateway.

Current `portable_runtime/location/transport.mjs` does meter outbound attempts,
inbound upgrades and raw TCP receive-forwarding/send-admission bytes across all
service work. Do not reuse the stale claim that DHT bytes are wholly unmetered.
Those counters exclude kernel packets, pre-upgrade allocation and refused
chunks; query-event limits are separate. Outer containment and gateway/operator
aggregate CPU, memory, wall, request and maintenance limits are still required.

Under well-connected participating membership, usable routing tables, admitted
registrations, refreshed replicas and an available honest holder, DHT routing can
avoid enumerating all `N` providers. Logarithmic routing intuition is conditional,
not a worst-case adversarial availability guarantee. Total network metadata and
renewal depend on the number of advertised holder/export pairs and replication;
they may dominate when many exports are rarely requested. Bounded event/provider
caps, Sybil/eclipse behavior, queue pressure, offline providers and omitted
registration can all prevent discovery. Empty or truncated results never prove
absence. A gateway can censor or omit; checks contain correctness damage, while
budgets contain only the selected resource exposure.

## Payoff and stopping rule

The expected gain is repeated independent readers reaching support custody they
could not name in advance, without configuring or polling every provider. This
supports sparse reciprocal mathematical use; it is not evidence of novelty or a
net growth advantage. The gain is strongest when many readers reuse maintained
custody and registration churn is modest. Closed supplier groups should keep
the current cheaper fallback. Low-use exports with expensive renewal can make
selective advertisement or an incremental operator registry preferable to DHT.

The architecture warrants a complete source implementation only as the linked
producer/registration, finite operator service and bounded located-receive path.
The recommendation favors retained DHT reuse for arbitrary open distributed
keys; a grouped-handoff modification can be the better first step when actual
contributions already provide coherent bundle membership. Neither funds a new
DHT, a global static map, or a new registry in parallel. Root's selection must
choose the needed coverage, price membership and renewal plus the count-scan
repair/capped scope, and choose one backend. If operator lifecycle cost outweighs
the named unknown-holder workflow, defer the addition.

The decisive later qualification is one discovered result with a missing
support-only export available solely from an independently registered custodian
outside the original source set, followed through exact locator, evidence and
ordinary use under the original budget. Its negative boundary must cover omitted,
expired or unavailable hints and clean bounded failure. Use retained mathematics;
no new proof campaign or repeated broad architecture experiment is needed.
Include registration/renewal, gateway startup and failure costs with reader costs.
Do not mark completion from successful parsing, localhost map lookup, a DHT
provider event or a clean HTTP transfer alone.
