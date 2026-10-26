# Optional ordinary specialist-contact federation: source selection

Root selects source implementation of the missing query-to-provider operation,
not another DHT, certificate campaign, mathematical experiment or release label.
The actual reader knows formal query features and a few chosen directories, not
the useful provider endpoint, snapshot, result ID or definition name.

## Decision and argument

Use one-hop, owner-selected HTTP directories with exact specialist route keys.
Readers need no inbound listener or Node/DHT installation. Operators may later
back a directory with existing routing, but this implementation does not claim
that integration. Multiple replaceable directories and direct contacts remain
possible; no universally designated service or authoritative global catalogue.

The retained DHT costs a separate runtime closure and service/client-mode changes.
Those costs are not justified merely to discover advisory HTTP endpoints. Reuse
the shipped HTTP codec/provider, settled fair exchange, ordinary feature compiler,
fair search, aggregate budget and the pure public-egress rules already designed
for location. There is no existing directory HTTP route; it must actually be
implemented and tested, not described as already available.

For d selected directories and r selected route predicates, at most d*r bounded
lookups occur (hard cap 32), yielding at most 64 distinct contacts. Directory maps
use exact-key lookup, not global scans or all feature-subset enumeration. Total
client network allowance is a fixed directory slice plus the unchanged search
slice, both inside one original OrdinaryBudget. Work is independent of the
network's total corpus size only for this finite contact lookup; relevant route
coverage and within-provider posting selectivity remain separate premises.

Reachability requires a selected directory to hold a matching live specialist
registration and enough remaining budget. Honest omission/staleness, no overlap,
failure and truncation return explicit incompleteness, never proof of absence.
Directory suggestions establish neither endpoint possession nor mathematical
acceptance. HTTPS authenticates the contacted server under the owner's trust
store; only the unchanged ordinary acceptance path warrants mathematics.

## Wire and source responsibilities

New helper `contact_directory.py` lives logically under support/transport.
Route `/v5/ordinary/contacts`, map/request/reply schemas with version V1.
Canonical request fields: schema, namespace, features, nonce, max_contacts,
max_bytes. Exact sorted 1..8 feature keys select an entry. A bounded immutable
ContactMap contains schema, namespace, entries; each entry has features and
endpoints. Maximum 2048 entries, 16 endpoints per entry, 2 MiB map; replies at
most 32768 bytes and 64 contacts. Endpoint fields are exactly host, port, tls,
server_name; no paths, redirects, nested referrals, extra grants or CA settings.
Reply binds schema/namespace/features/nonce, carries contacts and truncated,
status/assurance as advisory, global_complete=false, mathematical_acceptance=false.
Map absence is not global absence. Use exact field validation and canonical JSON.

Egress mirrors retained OwnerEgressPolicy semantics: canonical literal public
IPv4, owner-selected ports, TLS and system CA only, strict TLS name; no DNS dial
or IPv6 fallback. Explicit loopback-test mode lists exact 127.0.0.1 ports, cannot
be enabled by peers and never authorizes a nested referral. Bootstrap directory
contacts remain explicitly owner-selected, including their own pinned CA files.

Local hint expiry is anchored to the monotonic START of each lookup and capped
by the original operation deadline and owner max_age_ms (at most 60000). It is a
local use horizon, NOT a claim of real provider freshness. The composition may
narrow all subsequent search to the earliest admitted contact horizon; document
the availability tradeoff. No peer timestamp or response delay renews it.

## Public operations

- `peer directory-find`: owner contacts + selected directories (<=8), full specs,
  a finite list of route specs (<=8, each a subset of the compiled full query),
  directory limits/egress and existing search limits/offer/page. Prepay directory
  allowance without calling OrdinaryBudget.begin; preserve sequence==0 for the
  existing find preallocation. Check combined search+directory capacity before
  I/O; enforce directory counters independently; call existing find exactly once
  with the SAME ledger and a narrowed common deadline. No per-referral search or
  renewed wall/grant. Preserve settled transport failure charges and make
  uncertain cleanup terminal. Expose learned contacts as advisory report data,
  not a persistent authorization for future receiving operations.
- `peer directory-serve`: state-free, finite read-only service. Config supplies
  entries using ordinary formal specs (compiled locally), endpoint hints, host,
  port, optional locally pinned TLS certificate/key, lease/cleanup and provider
  limits. No index, custody or catalogue required; no remote registration/write.
  The existing package/runtime selection remains required; it does not launch
  Lean or certify anything. Readiness, bounded serving and clean closure follow
  existing serve conventions. No automatic renewal or background daemon.

Direct find/serve and mathematical acceptance remain unchanged. Selected old
package is `experiments/v5-local-checks/fair-investigator-assembly01/assembled/package`,
PROFILE ea7a958db31ac070aa59be1c1e3c50d4b195cfd982c63658bd80de15ef3c6d01.
All predecessor bytes stay frozen. New source overlays only; no native rebuild.

## Ownership and verification

- ordinary_routing_gap: new contact_directory.py and successor http_provider.py
  with only the optional role/route; helper interface notes in IMPLEMENTATION.md.
- search_locality_argument: successor peer_api.py with the two compositions;
  use the helper contract, coordinate exact field names with its author.
- concept_software_bridge: independent test design and source audit after its
  paper checkpoint; no edits to either author's code.
- Root: small successor peer.py/run.py/profile.py dispatch/load integration,
  prospective finite test selection and later file-only package integration.

Implement through absolute-path apply_patch under this fresh directory only.
Do not modify frozen predecessor files, paper work, shared ledgers or Git index.
Source work is selected now. Execution requires root reading source and review.
Decisive checks: real unknown-endpoint lookup then ordinary candidate search;
no private/mapped-address/TLS/CA escalation; namespace/nonce/route binding;
expired hints never dial; aggregate grants never reset; slow/bad directories
cannot consume unlimited work; no-contact and truncation remain incomplete;
directory-only public service closes without math state. Keep tests small,
native-free, loopback-only and explicitly separate from growth evidence.

### Source-review correction: absolute predial horizon

A relative timeout recomputed inside the transport can drift beyond the original
contact deadline if local entry or TLS setup is delayed. Root selects a tiny
fresh fair_search.py successor passing its immutable session deadline into the
new optional absolute_deadline keyword of fair_exchange.exchange. Directory
calls pass their request-start horizon too. Transport narrows (never renews)
that absolute deadline and checks remaining time after TLS setup, before starting
open_connection. The API caps SearchSession.deadline to the parent ledger BEFORE
constructing FairSearch. A focused delayed-setup zero-dial control must cover it.
These are cooperative predial checks, not hard real-time packet scheduling.
