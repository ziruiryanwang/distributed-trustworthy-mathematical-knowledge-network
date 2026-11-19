# Resumed routing choice: outbound-only ordinary readers

2026-10-25. Source decision by `ordinary_routing_gap`; only this checkpoint is
editable. The canonical guard passed and AGENTS.md was reread. User resumption
supersedes the earlier pause; root owns the implementation selection. No tests,
imports, network, native build, state, Git or shared-ledger mutations occurred.

## Recommendation

**Implement an optional, one-hop HTTP specialist-contact directory for the
ordinary client before integrating DHT into every reader.** Reuse ordinary fair
search after that lookup. Keep direct contacts supported; keep the existing DHT
as a later optional operator-side location mechanism, not a mandatory download
or child process for an outbound-only investigator.

This recommendation is narrower than a new search architecture: it repairs
unknown-provider endpoint acquisition. The remote directory's recommendation
remains an untrusted hint. Ordinary candidate validation, mathematical checking,
source-execution approval and coverage limits remain unchanged.

The source change should deliver a complete small behavior: a replaceable
directory can serve a bounded owner-approved registration map; a reader given
that directory and a formal query learns specialist HTTP contacts and searches
them under its original finite grant. A parser alone, inert contact JSON alone,
or another simulated directory does not complete this behavior.

## Comparison from actual sources

| Dimension | Reuse existing DHT in reader | One-hop HTTP directory |
|---|---|---|
| Already implemented location | Maintained Kademlia + Noise descriptor protocol, expiry/budget workflow | No current referral endpoint; new bounded map/route required |
| Transport already shipped in ordinary package | No | Yes: HTTP provider, settled fair exchange, TLS, exact Endpoint |
| Reader processes | Python plus owned Node child | Existing Python operation only |
| Runtime adoption | Fixed retained release manifest; 5,896 Node/overlay payloads; 192 MiB upper bound | Existing ordinary package/runtime, plus small source additions |
| Outbound-only behavior | Current reader requires listening/public announce and uses `clientMode:false`; needs a role-specific repair | Existing client requests are outbound only |
| What reader knows | Bootstrap DHT addresses/PeerIDs, semantic namespace and query route convention | One or more owner-selected directory HTTPS endpoints, semantic namespace and query route convention |
| Who can hide useful providers | Disconnected routing, missing advertisements, stale hints, eclipsing and bounded searches | Selected directories can omit providers; bounded maps can have incomplete registration |
| Work needed now | Ordinary namespace and grant bridge, light-reader role, runtime packaging, public serving integration | One advisory HTTP map/route, bounded reader composition, standalone serving entry, package closure |
| Stronger guarantee obtained | Decentralized rendezvous under DHT assumptions, not semantic completeness | Replaceable bounded contact selection, not global provider coverage |

The 192 MiB number is a code-enforced upper bound, **not measured startup RAM**.
The 5,896-file census is exact to the retained runtime profile. I did not time
either route or measure a latency advantage. The implementation/dependency
surface, not an invented benchmark, drives this provisional payoff choice.

The DHT option is not rejected in principle. It already solves a harder routing
problem than a configured directory. It becomes attractive if reachable
independent operators adopt it, or if registration/update churn makes approved
directory maps ineffective. Such operators could later expose the same bounded
contact interface to lightweight readers without making their hints authoritative.
No DHT-to-HTTP gateway is implemented or selected by this note.

## Inspected reusable files and actual seams

All paths below are under the canonical root.

### Reuse directly in a fresh coherent package

- `software/v5/ordinary_formal_query/discovery/ordinary_export_adapter.py`:
  `namespace_for` and `compile_query` already produce the ordinary domain and
  at most eight formal feature hashes. These do not require theorem IDs,
  certificate-policy IDs or provider names.
- `software/v5/ordinary_authoring_offers/http_provider.py`: bounded single
  request/connection HTTP profile, TLS, finite request/reply/connection quotas,
  dispatch and owned stop. `Provider` already has optional pure advisory-map
  roles, but there is **no contact-directory route today**.
- `software/v5/ordinary_fair_search/fair_exchange.py`: explicit numeric endpoint,
  bounded response, no redirects, settled recoverable failures, fatal uncertain
  closure. Its closed route allowlist currently permits only offer/candidates;
  a successor must explicitly add the new advisory route, not bypass it.
- `software/v5/ordinary_fair_search/fair_search.py`: fair offer/page rounds using
  one existing `SearchSession`, bounded metadata and conservative charges.
- `software/v5/discovery/search_session.py`: existing positive candidate and
  snapshot validation; leave it unchanged for this contact-only feature.
- `software/v5/ordinary_authoring_offers/ordinary_acquisition.py:301`:
  `OrdinaryBudget`, one parent deadline and conservative external prepayment.
  No new budget class is needed for mathematical acquisition.
- `software/v5/ordinary_bounded_operations/run.py`: existing hard outer operation
  launcher and retained supervisor. No new process supervisor is needed.

### Reuse the small pattern, not the wrong semantics

- `software/v5/ordinary_authoring_offers/authoring_offers.py`: bounded canonical
  input, immutable byte map, exact direct-key lookup, request/reply binding,
  deterministic bounded prefix, explicit truncation. Implement contact-specific
  schemas separately; an authoring repository offer is not a dial capability.
- `software/v5/portable_runtime/location/protocol.py`: the owner egress rules
  are suitable starting code: public numeric IPv4, owner-listed ports, HTTPS,
  strict optional TLS name, no remote CA file, explicit exact loopback test
  endpoints. Do not import the controller/Node closure merely to reuse these
  pure rules. Retain their source attribution and independently review the
  selected successor's actual endpoint validator.
- `software/v5/portable_runtime/location/workflow.py`: preserve the principle
  of owner-monotonic contact expiry plus immutable endpoint/policy binding. Its
  private ticket state and exact `_LocatedSearchClient` class need not be copied
  into a simpler HTTP lookup.

### Do not import as the shortcut

`software/v5/located_queries/client/located_queries.py` and its later
`pair_planning` successor require an exact certified `CommonsClient`, certificate
owner source pins, module/packet stores and `EvidenceAcquisition`. Those are not
needed for advisory ordinary contacts. The later `body_location` protocol also
has a foundation/policy body namespace that must not be substituted for ordinary
semantics. Existing body routing is real retained functionality, just not this
task's reuse unit.

The actual DHT reader constraints are explicit in
`portable_runtime/location/maintained_roles.mjs`: `validateConfig` requires one
listen address and, in public mode, an announce address; the Kademlia constructor
sets `clientMode:false` for both roles. Its portable controller hard-pins the
old release manifest/runtime census. Since the DHT path is not selected now,
investigating vendor client-mode internals cannot change this immediate choice
and was deliberately not expanded into another subtask.

## Minimal new behavior and wire semantics

Choose a fresh ordinary advisory route, for example
`/v5/ordinary/index-contacts`; the root fixes the final name and source identity.
It returns **index contacts only**, never another directory to chase.

The directory operator selects an immutable, bounded map keyed by ordinary
namespace and an exact nonempty feature predicate. It associates that key with
a bounded list of numeric HTTP endpoints. The map is pinned before serving and
never accepts remote writes, local paths or executable fields. The provider
does not have to host mathematical custody merely to serve this metadata.

A request carries the actual local ordinary namespace, a finite list of selected
feature-subset route predicates, a fresh nonce and response/contact caps. Every
predicate must be a subset of the compiled query. Singleton features are a
simple default convention (at most eight); callers may choose more selective
conjunctions within a fixed cap. No arbitrary provider inventory is requested.

A response binds exactly that request and contains the endpoint rows, an
explicit truncation flag, and false mathematical-acceptance/global-completeness
flags. Directory lookup is direct dictionary lookup by these selected keys,
not a scan of all theorem records or global peers. Deduplicate exact canonical
endpoint tuples across maps before the global contact cap; labels do not prove
independent operators. Distinct endpoints sharing a TLS name are still not
independent mathematical authorities.

There must be a declared common registration/query convention: if the reader
selects route set A and useful provider registrations cover keys B, contact
discovery needs `A ∩ B` nonempty in a queried directory. A correct transport
cannot fix absence of that overlap. A popular theorem-kind registration can be
a bounded starting point, but it is a hot key, not a relevance theorem.

Finite locally approved maps are a useful initial deployment compromise, not a
claim that manual updates scale without cost. Multiple communities can run
replaceable directories; no fixed compulsory server, universal registrar or
global task list is introduced. A client still needs some bootstrap knowledge.

## Expiry, egress and prepayment without hidden weakening

### Contact lifetime

For a directory request starting at owner monotonic time t, assign learned
contacts the fixed deadline

`e = min(original operation deadline, t + owner-selected maximum contact age)`.

Do not start this lease when a slow response arrives. A directory's timestamp,
reported freshness or max-age cannot enlarge it. This limits the client's use
of the suggestion; it is **not proof of provider liveness or map freshness**.
Nonce/request binding does not certify the directory's truth.

The cheapest composition can narrow the entire subsequent search deadline to
the earliest admitted contact expiry. This is conservative (one short-lived
contact may end all remaining search earlier), but avoids an unnecessary new
per-provider renewal mechanism. Alternatively add one explicit required predial
guard to the fresh fair-search composition; do not quietly hand raw referrals
to direct-contact `find` and discard their expiry.

### Egress and authority

Known directory endpoints are explicit owner choices. Learned endpoints must
pass the stricter remote-hint egress validator: public numeric IPv4, permitted
port, HTTPS and owner/system CA trust only. Plaintext/private/loopback access
requires the explicit exact test policy and cannot be enabled by a reply.
No DNS destination selection, redirects, proxy options, client credentials,
local CA filename or arbitrary URI comes from a directory.

Freeze the accepted endpoint/policy set, recheck it before each request, and
retain the search's exact-endpoint binding. TLS identifies the configured
endpoint name; it does not make the index result mathematically true. Use the
existing ordinary verification boundary after any candidate is selected.

### One original aggregate grant

The exact existing budget has a subtle constraint: `charge_external` requires
`sequence == 0`. Therefore fetching a directory with `OrdinaryAcquisition.begin`
and then calling current `find` is wrong: `find` tries to prepay after an issued
fetch. Do not relax that invariant to make the composition pass.

Select referral and search slices before I/O, with totals `R = Rd + Rs` and
`B = Bd + Bs` under the original grant. Prepay both at the beginning, maintain a
small explicit referral attempt/byte ledger within its slice, and create the
one `SearchSession` within the preallocated search slice. Factor the existing
fair-search body into an internal already-funded path so direct `find` and
federated find can share it without double charging. No public flag should let
serialized input falsely assert that prepayment already occurred.

An equally sound alternative is prepaying referral externally, reserving the
fixed search remainder before any I/O, never issuing `OrdinaryBudget.begin`
during referral, then letting current `find` prepay that exact remainder. The
first factoring is clearer if the new public composition is implemented.

Every failed begun referral consumes its ticket and full reply reservation.
Settled transport errors may move to the next already selected directory;
uncertain closure remains fatal. Directory and search phases share one original
absolute deadline and outer Job. Failed searches, empty results and unused
capacity do not create another grant. Report request/header overhead separately
from reply capacity, as existing code does.

## Concrete source successor scope

This is one feature, not one edited line. In a new selected overlay it requires:

1. A pure contact-map/validator module, explicitly distinct from authoring offers.
2. Small additions to the current HTTP provider's closed routes, optional role,
   dispatch and request-specific reply reservation; directory-only operation
   must be supported without opening an ordinary catalog/custody database.
3. The explicit new read-only route in settled fair exchange.
4. An ordinary peer-api composition for federated find and finite directory
   serving, reusing existing allowance/TLS/provider shutdown helpers.
5. Public CLI/launcher allowlist and state-free classification for those two
   operations; all indirect writable paths remain explicit and bounded.
6. Exact profile/source-map closure and a worked configuration handoff.

The frozen fair scheduler, mathematics/native support, custody, schema of
ordinary objects and the existing direct-contact behavior need no redesign.
No native rebuild should be required by these Python-only changes. Package
assembly and focused controls are separate root selections, not authorized here.

## Falsifiers and smallest useful verification

Source review should reject this selection if any of these is necessary:

- The directory cannot run without mathematical owner state or old certificate
  client dependencies.
- The reader needs a Node process, public listen address or the historical giant
  workspace to use the new route.
- A response can initiate recursive referrals, choose local trust material,
  escape egress policy or reset an original deadline/budget.
- Directory work must scan a corpus proportional to global mathematics rather
  than the selected bounded registration map and query-key set.
- Exact query/registration overlap is implausible for the stated first operator
  population, or the required manual curation/update cost dominates its usefulness.

If source review clears, one finite real public scenario is decisive for the
engineering seam: reader knows directories D1/D2 but not specialist P; D1 gives
an explicit empty/stale/refused outcome, D2 returns P; the reader applies egress
and the original lease, finds one ordinary candidate through P and closes all
resources with no grant renewal. Use synthetic inert candidate metadata; no
Lean theorem or new proof campaign is needed. Targeted controls cover request
binding, bounded maps, duplicate contacts, malicious endpoints, expiry during
handoff, response truncation, conserved charges and uncertain closure.

This would establish a usable unknown-provider lookup, not large-network recall,
useful mathematics, growth advantage or global final-v5 readiness. If a realistic
small community cannot maintain useful replaceable registrations, revisit the
optional DHT/operator-gateway route rather than polishing the directory further.
