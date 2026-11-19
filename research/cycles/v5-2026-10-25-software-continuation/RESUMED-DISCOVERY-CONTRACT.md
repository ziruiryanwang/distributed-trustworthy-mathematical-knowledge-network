# Lightweight discovery: untrusted hints under one owner grant

2026-10-25. `search_locality_argument`. Independent security/resource and
whole-cost challenge; source-only. Canonical guard and AGENTS read. The parallel
`ordinary_routing_gap` assignment owns implementation inventory and composition
choice. This checkpoint does not start code, tests, networking, Git operations,
runtime adoption or the separate mathematical-growth study. Full v5 is unfinished.

## Recommended minimal contract

Prefer an **optional, bounded, one-hop HTTP contact federation** for ordinary
laptop readers, provided the provider side is a real replaceable service and
the following egress/accounting conditions are implemented. Keep direct contacts
working. Let operators optionally use the retained DHT behind this interface;
do not make every reader maintain its routing state or install its Node closure.

The federation returns index-service suggestions, not theorem answers, source
execution authority, provider truth, membership completeness or cryptographic
evidence that the suggested server currently exists. Ordinary search/preview/
mathematical acceptance remain separate existing gates.

An initially small directory can publish an explicitly maintained catalog of
specialist contacts. It need not recursively query directories. The protocol
must permit independently operated alternatives, direct-provider use and retained
contacts; no particular directory, signer, registry root or DNS domain is
indispensable. This is a decentralized framework with conditional discovery,
not a proof of universal reachability. A fresh reader must still obtain at least
one bootstrap contact out of band.

## Actual boundaries that must be preserved

Selected ordinary package:
`experiments/v5-local-checks/fair-investigator-assembly01/assembled/package`,
PROFILE `ea7a958db31ac070aa59be1c1e3c50d4b195cfd982c63658bd80de15ef3c6d01`.

| Source inspected | Consequence for this design |
|---|---|
| `peer_api.py:_contacts` | Existing private/local endpoints and owner CA paths are deliberate owner choices. This is NOT a validator for automatically learned contacts. |
| `support/transport/http_provider.py:Endpoint.validate` | Rejects unspecified/multicast, requires TLS off-loopback, but permits private/link-local addresses. No DNS is needed because host is parsed as a literal IP. |
| `peer_api.py:find` and `_network` | One ordinary ledger; search requests/bytes prepaid with `charge_external`; original deadlines narrow only; unchanged explicit calls are separate grants. |
| `support/transport/ordinary_acquisition.py:OrdinaryBudget` | External charges require no pending fetch and `sequence == 0`; one cannot perform `begin/settle` directory fetches first and then call existing `find` unchanged. |
| `support/discovery/search_session.py` | One query/session, byte caps before decoding, conservatively retained failure/scan charges, bounded provider/snapshot/page/candidate sets, incomplete outcomes. |
| `support/discovery/fair_search.py` | Exact session/endpoints and serial fair rounds; `check_owner` has no provider parameter. It presently does not carry contact-specific expiry. |
| `support/transport/fair_exchange.py` | No redirect/DNS/retry, bounded framed replies, settled refusal required before continuing. Uncertain cleanup and external cancellation remain fatal. |
| `peer.py:run` | Package/runtime/config pins and allocation are checked before product operation; remote hints must not become local paths, profile selections or CLI grants. |

Also inspected the retained pure `portable_runtime/location/protocol.py`
`OwnerEgressPolicy`, `workflow.py` lifetime/accounting design, and
`transport/search_validation.py` pure preflight discipline. These are reusable
contracts, not proof that their older clients are installed in the ordinary
package. In particular, don't claim the ordinary fair path already uses the
older `_preflight` implementation: it has its own narrower recovery boundary.

## 1. Two different authorities: bootstrap versus suggestion

The owner approves seed directory endpoints, a fixed query, an egress profile,
the operation's resource envelope and whether automatic referral dialing is
allowed. A directory may only suggest values allowed by that already chosen
profile. A seed's permission to connect to one local address is **not transitive**
permission for its suggestions to access local services.

The smallest reusable public profile is the existing location policy's shape:

- Canonical numeric IPv4 only; use `IPv4Address`, not permissive URL parsing.
  Require global, nonreserved, nonmulticast, nonloopback, non-link-local,
  nonunspecified classification. Explicitly retain owner-denied ranges where
  the local environment requires them. Public IP classification is not a proof
  of physical routing: an operator with special routes must constrain those too.
- A bounded owner-selected set of destination ports; TLS mandatory.
- `ca_file = None` for suggestions, therefore the locally adopted system roots.
  Never accept peer-selected CA paths, certificates-as-trust-roots, client
  credentials, proxy configuration, TLS disable flags or certificate bypasses.
- An optional strict canonical DNS **certificate identity** may be suggested,
  as in the retained policy. It is verified by TLS hostname checking with owner
  trust roots; it is not used for DNS resolution. Dial only the vetted literal
  address. This is a claimed identity, not proof of mathematical honesty.
- No redirects, URL schemes, user-info, arbitrary paths, DNS referrals, IPv6
  zone IDs or IPv4-mapped IPv6 in this initial profile. IPv6/DNS support can be a
  later explicit transport extension; do not accidentally grant it via `Endpoint`.
- Local test mode is a separate explicit owner profile with an exact finite
  set of loopback address/port pairs. A reply cannot enable it or broaden it.

The strict TLS name can be learned because the owner explicitly chooses the
automatic WebPKI referral profile. That is different from silently weakening
today's `_contacts` promise that all such identities are directly owner supplied.
Directory TLS authenticates the chosen directory connection; provider TLS proves
control of its claimed certificate identity. Neither proves the other entity's
endorsement, service relevance or mathematical truth. A private PKI can remain
an owner-configured direct-contact path instead of remote trust-store discovery.

Validate policy on receipt and immediately before the actual dial. Preserve an
immutable exact endpoint tuple `(host,port,tls,server_name)` and owner policy
binding for the operation. Hash that tuple for local contact identity; don't use
an arbitrary peer label. The current `Endpoint.label` omits TLS server name,
so enforcing the total distinct-contact bound must not rely solely on the
SearchSession provider-label set. Check configured distinct endpoint count too.

## 2. Minimal wire and omission semantics

Each seed request binds schema/version, exact ordinary discovery namespace,
canonical query features or an explicit feature-subset route predicate, a fresh
client nonce, maximum reply bytes and maximum suggestions. A response must echo
that binding, contain a bounded list of inert endpoint tuples, and state its
advisory/incomplete status. No local paths, executable extractors, CA options,
new budgets or new seed directories are legal fields.

The first implementation needs only **one referral hop**: owner seeds -> index
suggestions -> ordinary `offer`/candidate requests. Suggested indexes cannot
extend the directory frontier. The index does not receive authority to issue
further contact transitions. A later multi-hop protocol needs a separate
demonstrated payoff; hop TTL alone would not bound a branching search tree.

Cap replies before allocating/parsing, enforce exact fields/canonical JSON,
bounded depth/strings/list count and unique endpoint tuples. Bind every retained
suggestion to its supplying seed, query, request and local expiry for diagnostics.
Selection/deduplication may be local deterministic policy; ranking is not truth.
Do not reward one seed's duplicate suggestions with extra contact slots or dial
retries. Also do not let an early malformed suggestion erase a later valid one
through a first-claim-wins identity policy.

Ordinary output should distinguish at least: no suggestions, unsupported
namespace, resource-limited/truncated suggestions, expired suggestion, locally
rejected endpoint, settled unavailable contact, malformed metadata, and fatal
local/cleanup failure. None is `NO_THEOREM_EXISTS`. A gateway that omits useful
providers cannot falsify mathematical acceptance; it can prevent useful work.
Multiple replaceable seeds mitigate single-operator omission but do not prove
independence or global coverage. The formal result remains incomplete even if
all selected seeds answered and every returned positive record verified.

## 3. Expiry is local permission to try, not objective recency

Let D be the original monotonic operation deadline; let t_j be directory request
j's monotonic start. The owner sets finite maximum hint age a. An adopted
contact expiry may be

`e_j = min(D, t_j + a, t_j + bounded_remote_max_age)`

if a remote maximum age is supported, otherwise omit the last term. The remote
value can only narrow permission; it cannot renew D or prove freshness. Check
`now < e_j` before adopting the response and before every connection attempt.
A delayed response must not earn a new full lifetime from arrival time.

Keep the original expiry in private controller state. Duplicate hints within
this operation do not reset it; for a simple conservative implementation retain
the minimum adopted expiry. A new owner-authorized operation can make a new
request, but must not be called an automatic continuation of the old grant.
Server wall timestamps and persisted raw monotonic numbers are not portable
expiry evidence. Across sessions, reacquire or require a separately specified
owner-authorized cache-age policy.

The current FairSearch needs a selected predial integration: its generic
`check_owner()` callback does not identify the target. The preferred narrow
successor gives the dial boundary the exact provider/endpoint and checks its
expiry/policy before I/O, abandoning any already-reserved ticket conservatively
on refusal. A simpler safe composition is to cap the entire search to the
earliest retained contact expiry, but that allows one short-lived hint to stop
all later contacts. Label that availability tradeoff; it is not equivalent to
per-contact continuation. Do not use a mutable closure that guesses the current
provider or bypass exact-class/session bindings.

The semantic promise is “no new dial begins after expiry,” not “no packet can be
in flight then.” Narrow each async attempt to residual operation/hint time and
reserve cleanup. Ordinary OS scheduling, synchronous TLS setup and cancellation
are not hard real-time; the outer process envelope remains necessary.

## 4. One grant and a bounded state machine

Use one owner-created outer ledger G with deadline D, total request cap R and
reply-byte cap B. Choose directory and search slices before I/O:

`R_D + R_S + R_A <= R`, `B_D + B_S + B_A <= B`,

where acquisition slices are zero when the operation only discovers candidates.
The controller's state machine is `DIRECTORY -> SEARCH -> CLOSED`, optionally
followed by already authorized acquisition under the same original ledger.
It never transitions back to directory on unhelpful search.

Two safe implementation shapes are possible; select one, not both implicitly:

1. Prepay directory and search using distinct outer `charge_external` labels,
   enforce both subbudgets in their controllers, and create exactly one
   SearchSession/FairSearch after directory completion. Do not then call existing
   `peer_api.find`, which would charge its search allocation a second time.
2. Prevalidate the sum and freeze both slices, prepay directory with a private
   controller, then call unchanged `find` once with the **same** original outer
   ledger so it prepays search. No outer `begin/settle` fetch may intervene;
   `charge_external` deliberately refuses after sequence becomes nonzero.

The first gives clearer all-before-I/O reservation. The second reuses more code
but still needs an explicit predial-expiry composition and immutable allocation
premises. A newly created ledger/session per suggestion is unacceptable.

Directory failures charge their whole reserved reply cap. Counts and bytes of
bad, duplicate, rejected, expired or unhelpful results remain charged; provider
claims cannot refund them. Search retains the current full candidate scan
reservation charge and independent byte/parse/proof checks. No metadata failure
may convert a local deadline, changed binding, external cancellation or unknown
transport cleanup into permission for another attempt.

A finite seed cap g, at most h hints per seed, and adopted-contact cap c <= 64
give at most min(g*h,c) distinct search endpoints. Also cap *processed* hints
(including duplicates) by g*h and wire bytes, not only the number adopted.
Request, page, candidate, snapshot and report caps remain independent. First
query selected seeds fairly under finite per-attempt time; then ordinary
FairSearch divides its unchanged search slice. This need not be highly concurrent
to be useful, and no new background maintenance is needed on the reader.

If U bounds request body bytes and H bounds one header block, then total
application bytes are bounded by

`B + R*(U + 2H)`

for requests obeying the same bounded framing. TLS/TCP/IP, DNS if ever introduced,
OS buffers and gateway backend routing are separate costs, not hidden inside
reply-byte accounting. Hard wall/CPU/memory/process containment is external;
cooperative callback checks are not a sandbox or a preemptive CPU guarantee.

## 5. Gateways can keep DHT maintenance off laptops

A gateway may be a directory backend that uses the retained location protocol,
static specialist registrations, or a bounded cache. These are replaceable
operator strategies behind the same advisory interface. The laptop need not
trust or know which one it uses for mathematical validity.

The gateway must enforce its **own** finite per-request DHT/descriptor work,
connections, queues, concurrent requests and reply bytes. Its inbound caller's
declared limits are not a trustworthy allocation or payment mechanism. Rate
limits, admission control and reserved maintenance capacity are operator service
obligations. An empty or incomplete DHT result stays incomplete when translated;
gateway wrapping must not upgrade an unmeasured DHT byte/event budget into
“bounded whole-network wire cost.” Current retained `WorkflowBudget.report`
explicitly reports DHT wire bytes as unmeasured.

The gateway is not a general URL fetch proxy. It accepts only the fixed discovery
request, calculates allowed route keys locally, and applies its own egress policy
to every backend dial. It cannot turn a client address into an arbitrary backend
destination. A provider descriptor may prove a peer-channel binding internally;
the gateway response still carries only gateway-supplied advice unless that
proof is explicitly exposed and verified. Such exposure is not needed for the
first useful discovery interface.

Publish/renew a service advertisement only through an authorized operator
configuration and finite lease. No unbounded browser-driven registration or
public write endpoint is necessary for the first federation. Multiple gateways
may independently use the same underlying DHT; this shares a failure domain and
does not establish independent coverage.

## Whole-cost decision, not an invented speedup

Let K be the number of actual reader queries in an accounting interval. Let
I be the extra local DHT runtime install/startup/adoption cost, M its local
maintenance cost, q_L local per-query routing cost, q_H HTTP directory cost,
q_G gateway backend cost and M_G gateway maintenance allocated to those queries.
Sharing gateway work is beneficial under a specified resource measure only if

`I + M + K*q_L > K*(q_H + q_G) + M_G`.

The left is not free merely because a dependency already exists; the right is
not free merely because somebody else operates it. Cache reuse and many readers
can amortize M_G; privacy, delay, service concentration and gateway churn are
additional tradeoffs. No numeric weights or empirical win are asserted here.
For infrequent ordinary laptop use, avoiding the mandatory known Node/runtime
closure is a credible favorable regime; already-running routing operators may
prefer direct DHT use. Therefore routing implementation should remain optional,
not outlawed and not imposed on every reader.

Neither route addresses the earlier `SEARCH-LOCALITY-DECISION.md` hot-list bound
or arbitrary semantic relevance. Actual discovery additionally needs overlap
between requested routes and registered specialist predicates, reachable honest
service capacity, and sufficient residual search resources. The resulting
software can be useful under explicit conditions without a global completeness
or guaranteed mathematical-growth claim.

## Exact falsifiers for root's eventual implementation selection

No tests are selected here. A changed-boundary suite should reject the design if
any of these occurs; existing mathematics/native campaigns need not be repeated.

1. **SSRF:** a seed suggests loopback, RFC1918, link-local/metadata service,
   unspecified, multicast, shared/non-global, reserved, IPv6-mapped or malformed
   literal addresses and the public profile reaches the dial function. Assert
   zero dials, not merely a later TLS failure. Explicit test mode permits only
   its exact approved loopback pairs and cannot be selected by a response.
2. **Trust injection:** a response supplies CA/local-file fields, plaintext,
   disallowed port, arbitrary URL/path, invalid TLS name or redirect; no local
   file access, trust mutation or follow-up dial occurs.
3. **Time laundering:** response arrives after request-start expiry, or expires
   between adoption and a later provider turn; no dial starts. A duplicate does
   not refresh expiry. Long TLS setup cannot reset the original attempt timer.
4. **Budget renewal:** g replies containing h suggestions, failed seeds,
   duplicate tuples, malicious counts and many namespaces cannot exceed original
   requests/reply bytes/contact cap. Exactly one search session is created; its
   deadline does not exceed the original grant. Directory work followed by search
   does not fail from accidentally using the forbidden post-fetch prepay phase.
5. **Binding substitution:** wrong namespace/query/nonce, changed endpoint after
   validation, or same IP/port with different TLS identities cannot silently
   acquire another endpoint's binding/expiry or bypass distinct-contact caps.
6. **Cleanup confusion:** a settled timeout may advance within remaining budget;
   unconfirmed socket closure, local guard failure and cancellation may not.
   Reclassifying every TLS/connect exception as “no provider” fails this gate.
7. **Omission laundering:** a truthful empty/truncated directory response,
   malformed candidate or total provider failure never becomes a mathematical
   negative, global-complete result or accepted theorem.
8. **Actual unknown endpoint:** a small integration given only seeds/query/grant
   obtains a supported ordinary provider through the real directory response,
   then the real offer/candidate boundary; no fixture injects the provider into
   the search contact map. This shows composition, not planet-scale behavior.

The task closes at this source contract. Root may select a fresh implementation
only after reconciling the parallel inventory and deciding whether a simple
independent directory service or optional retained-location gateway has the
better immediate deployment payoff.
