# Ordinary serving with maintained discovery

2026-10-20, core_search. Source/theory decision only: no code, process, network,
copy, packaging, test or Git operation. Root selects implementation and runtime.

## Recommendation

Add one fresh ordinary **serve-and-advertise** entry composing the current
read-only workspace HTTP provider with the **already implemented portable
maintained-location provider**. This closes a real deployment gap: an owner can
serve retained contributions and advertise formal query routes without manually
passing the HTTP endpoint to every reader. Readers still need independently
obtained, owner-approved overlay bootstrap contacts; this does not solve initial
peer discovery or make a disconnected network globally searchable.

Do not implement another DHT, search engine, publication workflow or mathematical
checker. Do not repeat the passed actual located discovery/authoring campaign.
The existing HTTP-only entry remains a useful smaller dependency profile.

## Existing seams and actual missing composition

| Concern | Reuse | Missing change |
|---|---|---|
| Retained data | `client/serve_workspace.py`, exclusive `Workspace.open(..., create=False)` | Fresh composed owner; preserve all modes and lock rules |
| HTTP index/body/packet access | Existing mode-selected `CompositeProvider` | Start first; bind its actual returned endpoint into location config |
| Portable maintained location | `portable_runtime/location/controller_services.py:ServiceLocationProcess` | Construct it from context source pins and owned temporary paths |
| Runtime adoption | `controller.py:AdoptedLocationRuntime` | Optional existing Node/overlay installation role |
| Provider advertisement | Existing `publish(features,stripe)`, maintained intents/reprovide | Explicit finite owner-selected route list |
| Consumer discovery | Existing located workflow/`CommonsClient.find` | No new consumer search mechanism |
| Containment | Existing `client.boot`/outer Job and original deadline | Account for sequential location and HTTP teardown |

The existing `actual_owner03.py` demonstrates the exact composition: start HTTP,
create role `index-provider` with its endpoint, publish a compiled formal route,
then an unrelated reader locates the provider and searches its index. That is
fixture orchestration, not an ordinary retained-workspace service. A focused
search found no already-shipped ordinary composed service to adopt instead.

The portable `node_entry_services.mjs` already contains the available-dial
successor and source-map V2. Use this selected portable file, not historical
hard-coded `location/node_entry_services_available.mjs`. The required-service
composition adds the retained ping capability; no network protocol change is
needed. Exact base manifest remains
`a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed`.

## Small, closed public contract

Create fresh `client/serve_advertised.py`; preserve the used HTTP-only source.
Its parameters can retain the existing workspace/bind/TLS/service-limit fields
and add one exact `location` object under a distinct schema. That object contains
only an explicitly owner-selected retained installation root, egress policy,
one listen address, bounded announce/bootstrap lists, existing finite location
limits, bounded health-observation interval and explicit routes `{features, stripe}`.
Do not accept caller replacements for namespace, role, descriptor endpoints,
individual runtime/executable paths, source pins, state paths or channel paths.
The retained root must match the fixed adopted base manifest and exact runtime
census; its path is not a new trust authority.

Derive namespace from the opened workspace index; role is `index-provider`;
endpoints contain exactly the actual successfully bound HTTP endpoint. Compile
or validate features under that namespace using the existing feature/route
functions. A route is a discovery hint, not a claim that every matching theorem
is present. Refuse duplicate routes and cap their number, for example at 32,
within both advertised-key and private-channel command/frame budgets. Leave
room for the stop command. No implicit corpus scan, all-export advertisement,
query expansion, new stripe selection or automatic retry.

Keep HTTP's explicit IP/non-loopback TLS rules and location's existing outbound
policy. The location profile is IPv4-only; refuse IPv6 in this composed entry
rather than silently changing the HTTP address or weakening its policy.
A port-zero listener must yield an actual allowed endpoint before Node
starts; the current exact loopback allowlist cannot authorize an unknown random
port in advance. The first profile should require an explicitly allowed HTTP
port when location is enabled, rather than silently broadening egress. Public
IPv4 endpoints use the existing system-CA HTTPS policy: listener setup alone
does not establish remote certificate acceptance or public reachability. NAT,
TLS name selection and relays remain explicit separate deployment work.

Reuse the frozen HTTP parameter/path/TLS helpers where practical. Its `serve()`
does not expose the opened workspace/provider, so wrapping it cannot safely
attach this role. Prefer one explicit small lifecycle successor over monkey
patching `_types`, replacing global classes, or introducing callback-based
service middleware. Preserve the current HTTP-only source and tests unchanged.

## Lifetime and cleanup composition

Let D be the unchanged outer deadline, H the current HTTP operation/drain
allowance, Q one location command allowance, and L = 6 seconds the retained
controller close allowance. Choose the active-service cutoff S before D by at
least H + 2Q + L plus a bounded reporting/source-check margin. The two Q windows
are a final live-status observation and then stop. This is a scheduling
allowance, not proof that OS or synchronous hashing always finishes on time;
the original outer Job remains the hard ceiling and overruns remain failures.

1. Validate all closed fields, path disjointness, pins and available cleanup
   margin. Open the existing workspace with its unchanged exclusive lock.
2. Start HTTP before constructing any advertised endpoint. Construct a portable
   runtime under `context.installation`, using the exact context-selected MJS
   hashes. Put fresh location state/evidence under `context.location_workspace`,
   not the persistent mathematical workspace or immutable installation.
3. Create one Node provider with service time clipped to the remaining original
   active interval. Every start/publish operation is bounded by S and the
   existing operation limit. Do not renew D, create another grant, or restart a
   failed child. Startup/source verification consumes the same interval.
4. Publish each selected route once. Record each actual returned disposition.
   Write composed READY only after HTTP is live and the selected dispatch
   condition succeeds. A neutral listening node or `CONNECTED` bootstrap is
   insufficient evidence of route advertisement. While serving, wait on the
   active cutoff **and** the owned Node exit/failure state; do not blindly sleep
   through early location failure and return PASS. A stopped/failed child
   terminates this composed service and triggers the same complete cleanup.
5. On expiry, cancellation or any startup/publication failure, stop location
   renewals first. Attempt bounded `stop`, then `close` even if stop failed.
   Then stop/drain HTTP, then close the workspace. Attempt every cleanup after
   a preceding error; failure and forced termination never become clean PASS.
6. Require the existing closed/returncode-zero/no-channel-failure/no-forced-kill
   location report, HTTP clean closure and workspace clean closure. Retain
   original deadlines, per-route outcomes and both components' counters.

Node's own timer must not predictably expire before the owner can send its stop
command: budget its fixed initial service time through S + 2Q and initiate final
status at S, then stop, with both before the outer cleanup cutoff. Bound startup and
publication by S even though the same child has its reserved stop interval.
Do not give Node an extra renewable service lease. The controller's synchronous pre/post
pin verification is already part of owner cost, not a free side operation.

No concurrent publication is added: the service owns the workspace lock. A local
agent can finish publication, close its writer, then serve; later publication
uses a distinct bounded operation after service closure. Removing the lock or
allowing writers is a different consistency problem, not this seam.

## Optional installation role, not a new runtime

The current `distribution_complete` base projection contains Python runtime and
selected supervisor helpers, **not** Node/overlay. Its documentation correctly
says location needs an adopted runtime. The selected controller requires the
exact 5,896 manifest-backed `overlay/` and `runtime/node/` files, at most 192 MiB,
and the exact fourteen MJS sources (nine base names plus five role names).

A retained full base already supplies this role: the original
`v4-library-commons-02/commons-v4` needs no copy/install for a selected source
control. The current `distribution03/base` is projected and **does not** include
Node; an older role ledger must not override that later installation state.
The exact role payload is 130,118,221 bytes according to the retained role
ledger. The complete boot source map also includes seven Python files: fourteen
MJS hashes alone do not constitute the full twenty-one-file portable location
source closure.
A later small distribution successor can offer two explicit projections:
current HTTP-only, and that projection union the existing Node/overlay role.
Keep the unchanged full base manifest as the catalogue; validate each named
projection exactly. No package-manager install, rebuilt Node, writable install,
untracked external executable or mandatory Node for direct-contact consumers.
The current complete distribution is frozen; do not edit it in place. A local
source/control selection may use the retained full base as its selected
installation immediately, but must
not be described as the projected installed public command until its optional
role and launcher are actually selected and checked.

## Authority and expiry

The composed implication is only:

`owner-authorized route dispatch -> candidate provider contact -> independently
checked search/acquisition -> existing mathematical acceptance`.

No implication skips the last checks. Peer identity authenticates the descriptor
channel, not theorem truth, completeness, availability or operator independence.
Neither service startup nor route dispatch constructs a warrant/READY semantic
context. Reports must keep `mathematical_acceptance: false` and
`global_complete: false`.

The actual publish status is `HINT_DISPATCHED_UNACKNOWLEDGED`: the selected DHT
ADD_PROVIDER operation has no remote acknowledgement. It does not prove storage
on a remote peer, global visibility, or successful search by any reader.
An incomplete route must remain visibly incomplete; do not call it advertised
merely because local intent exists. For a strict composed READY, require every
selected route to reach that dispatch status; otherwise terminate with the
partial outcomes preserved. `publish` enables local intent before dispatch, so
an INCOMPLETE result can leave renewal work until termination; do not repeatedly
issue publish or pretend that no side effect occurred. HTTP-only is separately available by owner choice,
not silent success fallback after advertising fails.

Stopping/withdrawing stops local renewal; it does not erase remote records.
Remote retention is governed by receiving nodes and their DHT policy, not a
globally enforced sender TTL. Report configured local TTL and stale-hint risk,
not a network-wide expiry promise. Descriptors use an authenticated fresh
request/nonce and client-side request-age limits; an old provider record cannot
grant fresh descriptor or mathematical authority. The existing bounded reader
failure handling remains required when a stale endpoint is encountered.

## Smallest decisive evidence

First use cheap inert lifecycle controls for wrong fields/endpoint/namespace,
post-HTTP Node startup failure, partial dispatch failure, cancellation and
cleanup failure. These test changed ownership/order, not cryptographic truth.

One finite actual local composition control is sufficient for this seam:

- Open an already retained tiny workspace through the new entry, start the
  existing adopted provider role, and dispatch one exact formal route.
- A reader supplied only the bootstrap/contact policy and formal route, **not
  the HTTP endpoint**, locates it, authenticates its descriptor and retrieves
  one existing authenticated offer/page through the existing search code.
- Confirm the endpoint equals the live service endpoint; all original limits
  are unchanged. Stop cleanly and reopen the same workspace to establish lock
  release. No Lean execution, proof production, theorem authoring or READY
  rerun is needed: data-only serving does not change mathematical acceptance.

Reuse prior maintained-location, authentication, provider and mathematical
campaigns. Do not repeat a broad grid, claim worldwide coverage from loopback,
or wait through TTLs merely to rediscover the documented stale-hint boundary.
The implementation should stop expanding if it requires a new DHT, generic
daemon manager, live concurrent publication or broad packaging campaign.

This advances ordinary decentralized availability/discovery, not aggregate
certification or a full-cost growth proof. Those central obligations stay open.
