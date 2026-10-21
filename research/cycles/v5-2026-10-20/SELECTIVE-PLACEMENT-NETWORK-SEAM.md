# Complete the same placement feature: authenticated intake and cell dispatch

2026-10-21, core_growth. Source-only proposal for root selection. No product
edits, imports, tests, builds, native execution, networking or Git mutations.
Canonical root is `E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Decision

Add **three small modules**, leaving the just-reviewed placement controller,
ledger, codec, read-side provider, discovery protocol and Node locator unchanged.
Use **one generation, one shared Workspace, one read endpoint, one separate
placement endpoint and one V1 index-provider locator**. The two listeners share
one event loop and owner lock; they are not two independently opened workspaces.

The new observable capability is: a publisher submits a finite authenticated
placement, the custodian pulls/indexes it and dynamically dispatches its derived
cell, then an unrelated goal-only reader acquires it after the publisher stops.
This closes the gap between owner-local placement and remotely usable placement.
It does not introduce two-slot retirement, GC, a new DHT, new proof production,
or a mathematical authority at the custodian.

Keep the dedicated intake listener separate. The current read handler is
synchronous and has a closed route/16-KiB framing table. Extending it in place
would require a successor for all read framing merely to await `submit` and
carry a token envelope. A second bounded listener composes with the real
`CompositeProvider` without changing any read route or its quotas. Only the
read endpoint appears in the existing V1 locator descriptor; a publisher's
placement contact and grant are owner-provisioned, not discovered as write
authority from a DHT hint.

## Exact current seams inspected

Paths below are physical paths relative to the canonical root. The authoritative
114-source map is `experiments/v5-local-checks/distribution-terminal-i-01-input.json`,
SHA-256 `d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0`.

| Physical source | Existing callable boundary and consequence |
|---|---|
| `software/v5/selective_placement/placement/controller.py` | `start_service`, `issue_token`, async `submit`, `status`, `reconcile`, `seal`, `close`. Current cleanup-fixed hash `ef1c9b59072127379e955bafeea001a22d6e3d10c9c46dca1304f85ab09e2b49`. Reuse exact controller; an acquisition-close failure is not success. |
| `software/v5/selective_placement/placement/ledger.py` | Hashed-token authentication, deterministic request ID, exact duplicate observation, separately committed receipt; `public()` does not expose the token or manifest. There is no advertisement state or route-command funding here. |
| `software/v5/terminal_i/evidence_network/transport.py` | `CompositeProvider(index=..., custody=..., packets=..., **limits)`; inherited async `start`/`stop`, synchronous `dispatch`, `status`. This is the actual selected read-side implementation, not the old receipt-only provider. |
| `software/v5/transport/http_provider_receipts.py` | Reusable `_headers`, `_body`, `_header`, `_write`, `Endpoint`, `server_tls`; JSON header allowlist does not include Authorization. Its request limit remains 16 KiB. |
| `software/v5/base_projection/client/serve_workspace.py` | `_parameters` validates owner bind/TLS pins and cleanup margin; `_close_workspace` preserves cleanup errors. `serve(context)` opens a workspace itself, so do not call it beside a placement owner opening the same path. |
| `software/v5/body_location/client/serve_advertised.py` | Existing owner/service validation and `_hint`, `_live_status`, `_close_http` are reusable patterns. Its `serve` owns static routes and cannot simply accept dynamic cells; `_monitor` must not become an unbounded source of commands. No projected read-only index view for writable placement. |
| `software/v5/body_location/portable/location/controller_services.py` | `ServiceLocationProcess(adoption, role_pins, configuration, evidence, deadline=...)`; async `start`, inherited `command`, `close`, `report`. V1 index-provider supports the required single endpoint. |
| `software/v5/portable_runtime/location/controller.py` | `command(name, payload, until=...)` serializes over one private pipe and absolute deadline; frame/byte bounds remain. A failed command poisons the channel. Do not create a second channel or refresh deadlines to retry. |
| `software/v5/body_location/portable/location/maintained_roles.mjs` | `publish(features, stripe)` already commits intent and attempts actual ADD_PROVIDER dispatch. Positive status requires observed `add_provider_write > 0`; `INCOMPLETE` can still leave local intent. `withdraw`, `status`, `stop` already exist. |
| `software/v5/body_location/portable/location/node_entry_services.mjs` | Closed IPC `publish`, `withdraw`, `status`, `stop` commands already exposed. No Node source successor is needed. |
| `software/v5/pair_planning/client/located_queries.py` | Selected read-side goal/subset-route planning and aggregate query budgets. Reuse for the fresh reader, not a private list of the custodian's exports. |

Corrected placement contract is `SELECTIVE-PLACEMENT-CONTRACT.md`, SHA-256
`fbbb47b449d551a9a1a675b9814b310197fc4ef499aa43be192a2ebbeccb0823`.
The new proposal specializes its first one-generation network slice; it does
not claim that bounded retirement from that contract is already implemented.

## The three-module boundary

Proposed new physical subtree: `software/v5/placement_network/`.

1. `placement/network.py`: closed submit/status envelope codecs, bounded client
   exchange, and a small async placement listener. It borrows only existing
   HTTP framing/TLS helpers and calls the supplied exact controller/service.
   It does not open databases, choose arbitrary endpoints, issue grants over
   HTTP, perform mathematical verification, or serve general RPC.
2. `placement/advertisement.py`: one bounded SQLite route-attempt journal plus
   guarded coordination of successful placements with the existing private
   locator. Separate route state is necessary: the core receipt is already a
   committed immutable historical result before publication can happen.
   Do not rewrite that receipt to make network dispatch look atomic with it.
3. `client/serve_placement.py`: a trusted-owner async service API/entry that
   opens the Workspace once, opens the existing placement ledger/controller,
   starts the unchanged read provider and new intake listener, starts the
   V1 locator, reserves health/route/cleanup work, and closes all components.
   It owns ordinary paths and finite service configuration, not a new trust
   domain, daemon framework or remote source-execution API.

Root must select exact successor paths/maps before code work. No change to the
pending core-control inputs is needed. A normal selected owner entry can call
the service API and issue tokens locally; secret-bearing values stay in memory
and must never enter boot parameter JSON, reports, command arguments or logs.
The API returns a newly issued token only to the trusted owner caller, as the
existing controller already does. Delivery to the selected publisher is an
explicit owner credential-provisioning act. The integration can pass it through
a private in-memory callback; this is not a public grant-vending route or a
claim that a persisted service profile magically provisions credentials.

## Closed wire shape and honest byte bounds

Use two POST paths, `/v5/placement/submit` and `/v5/placement/status`, with
one request per connection, Content-Length, application/json and close.

- Submit fields: `schema`, `token`, `manifest`. The manifest is a nested JSON
  **object**, not an escaped JSON string or base64. Canonicalize that inner
  object and pass those exact bytes to `controller.submit`; require the
  independently computed request ID to match the response.
- Status fields: `schema`, `token`, `request_id`. It observes only the token's
  retained request. It cannot start a pull, route command, recovery or renewal.
- The inner canonical manifest remains at most **16,384 bytes**. The new
  submit envelope ceiling is **17,408 bytes** (16 KiB plus 1 KiB overhead),
  checked before body allocation/parse. Status ceiling is **1,024 bytes**.
  Validate the full canonical envelope and exact fields. The token is fixed
  64-character lower-case hexadecimal, so the closed wrapper fits comfortably
  in its explicit allowance; still test the maximum boundary, not a guess.
- Core `OUTCOME_MAX=65,536` is not the complete HTTP-response bound. Use an
  **81,920-byte** full-response ceiling for the bounded public ledger wrapper,
  a route facet capped at 4,096 bytes and envelope fields. Validate the actual
  whole encoding. Reserve that ceiling before beginning effects; do not claim
  that a maximal core outcome alone fits a 64-KiB reply.
- Keep existing 8-KiB header bounds. Set finite connections, total requests,
  incoming payload/header allowances, outgoing allowances and service/call
  deadlines. Charge malformed/busy/error traffic too. Retain conservative
  unknown-tail accounting where precise byte observations are unavailable.

Tokens are checked only on the new route, never inserted in the existing
read-route header allowlist. Error responses use closed error codes; do not
echo envelopes, token substrings, raw validation exceptions or arbitrary
transport diagnostics that could reveal secrets. No request-body logging.

## TLS and ownership are separate from mathematical trust

Use locally selected certificate/private-key pins on the server and ordinary
`ssl.create_default_context` with hostname verification/TLS >= 1.2 on the
client. The numeric endpoint requires a matching IP SAN unless a separately
owner-adopted DNS server name is explicitly selected. The publisher binds its
token to its configured placement endpoint and expected service epoch,
generation, namespace and wire profile; it never sends the token to a descriptor
supplied by an untrusted reader response.

The existing `OwnerEgressPolicy` public mode uses system CA trust only; it does
not accept a remote CA file or a downloaded trust override. Preserve that
behavior in this slice. An explicit allowed loopback test can use HTTP, but
report it as loopback cooperative evidence, **not authenticated public TLS**.
No endpoint/TLS identity means remote token submission remains disabled. Noise
peer identity on the locator channel is not HTTPS server authentication.

This isolates two authorities: the bearer token authorizes finite storage
work; the existing receiving verifier decides mathematical acceptance. Neither
the TLS certificate, token, custody ACK nor cell hint is a mathematical warrant.

## Serialization, duplicates and original authority

Allow only **one active intake action**, checked/set synchronously before its
first await. Other requests get a bounded BUSY/refusal rather than waiting in
an unbounded lock queue. Keep a small finite connection cap for parsing/BUSY
responses. The existing read listener has its own budget and can run while
intake is awaiting network I/O. SQLite operations remain synchronous on the
same owner/event loop; no worker thread gets the existing connections.

Within that slot, authenticate and compute the request ID before asking whether
the exact request already exists. A bounded primary-key lookup distinguishes
absence from an arbitrary database error. `controller.submit` still performs
all authoritative validation/reservation and exact-manifest checks. Capture
whether it was an existing request before the call: its returned `public()`
shape alone always says observation-only and does not encode newly-created.
For an existing request, return the recorded placement plus route observation,
**without any dispatch or route-state write**, even after reply loss or restart.

For a genuinely new request, await the unchanged controller. Only a clean
successful return with a committed receipt may enter the network publication
step. An exception, including `PlacementCleanupError` after receipt commit,
does not silently become a successful placement HTTP response. Durable state
remains inspectable; no rollback claim. On a closed/poisoned owner, stop intake.

Use the original service deadline and per-request deadline at every boundary;
HTTP timeout cancellation is a real interrupted operation, not license to
restart. Root's external supervisor still supplies the hard CPU/process bound.
Async timeouts do not preempt synchronous Store operations or guarantee health
scheduling while they run. Cleanup has separately reserved time, not revived
intake authority after expiry.

## Route journal and dispatch: bounded, not silently reliable

At startup, prepay a finite service-wide advertisement envelope, before intake
opens: at most L cells, original locator commands/transport budgets and route
journal storage. Set `L = generation.max_cells` and bind the original service
grant/config bindings. This is an additional explicit owner allocation, not
unfunded route work smuggled into the core placement's acquisition vector.

The journal lives at one exact ordinary managed path under the Workspace,
separate from its unchanged placement ledger. It binds generation, service
epoch, runtime ID, namespace and actual read endpoint. Bound total runs by the
existing generation's `max_runs`, cells/run by L, report bytes and SQLite pages;
do not create indefinitely many journal files or ever-growing free history.
Every mutation checks exact live owner identity and its original deadline.

For the first eligible indexed result of a cell in this run:

1. Confirm actual read provider and locator are live, and derive/compare the
   stripe-zero route from the successful receipt's independently checked
   fingerprint. Never dispatch a publisher's unverified proposed feature.
2. Persist a charged `DISPATCH_ATTEMPTED` row with the original request and
   finite allowance **before** `node.command("publish", {features:[f],stripe:0})`.
   An uncertain attempted call consumes its opportunity. There is no automatic
   retry, even when cancellation occurs before a reply is observed.
3. Preserve the returned exact bounded observation. Only existing `_hint`
   conditions (`HINT_DISPATCHED_UNACKNOWLEDGED`, matching key, no error, actual
   `add_provider_write > 0`) authorize that status. `INCOMPLETE` may have
   installed renewable local intent; retain that distinction.
4. Store the result under the same owner guard, then return a joined response
   with the original placement receipt and the separate route facet. If the
   journal commit fails after dispatch, report uncertainty, not no-dispatch.

A later distinct contribution in the same cell may cite an earlier dispatch
observation from the same still-live run; it does not receive a fabricated new
acknowledgement. Store bounded references/timestamps, not a new result per
request. A failed cell opportunity is not retried by unrelated submissions.
Explicit owner-selected re-advertisement after a service restart requires a
fresh finite runtime and readback of the referenced retained commitments;
old tokens remain status-only. The first integration need not exercise restart
re-advertisement, but its remote API must not introduce an implicit path.

Response facets must distinguish:

- Core receipt: `INDEXED_UNADVERTISED`, a historical custody/index fact.
- No attempted route, durable attempted/unknown route, returned incomplete
  intent, or observed `HINT_DISPATCHED_UNACKNOWLEDGED` with run/time binding.
- Client knowledge: `PEER_ACKNOWLEDGED` only after authenticated transport
  and expected binding checks; independently verified readback is separate.

There is deliberately no bare `ADVERTISED=true` or global-success boolean.
Even a positive dispatch is not a remote DHT ACK or discovery completeness.

## Dynamic command accounting and teardown

Select V1 index-only role, one actual read endpoint, no static routes required.
Let H bound initial/periodic/final health checks and L bound dynamic cells.
Reserve conservatively

    H + 2*L + 1 <= min(configured_command_limit, 60).

The terms cover one publish and at most one withdrawal per cell, all health
commands and stop. The 60-command ceiling stays below the retained 64-frame
pipe boundary including readiness/teardown margins. Existing Node transport,
metadata, descriptor and maintenance limits remain independent requirements;
the command inequality does not fund background traffic by itself.

One serialized existing `node.command` channel handles publication, health,
withdrawal and stop. Never run a second locator to escape its budget. Health
may be delayed behind a bounded publish; account for that in reported detection
scope instead of promising continuous readiness. At service end, close intake
and settle/cancel its bounded active handler first; stop/close locator and read
listener under reserved margins, then close route journal, placement controller
and Workspace. Preserve every cleanup error. No reclamation or deletion occurs.
Retained bytes can outlive a finite service; their recorded retention promise
is not a promise of uninterrupted service through that horizon.

## One decision-changing integration, not another proof campaign

After changed-boundary source controls, use retained evidence for a single
three-role scenario under a fresh fixed allocation:

1. A serves one already checked export/evidence. B starts with an empty matching
   fingerprint Workspace and no route for that cell. B's owner locally issues
   one bounded token. The harness keeps the token in memory, never artifacts.
2. A sends one new submit over the new public wire path. B genuinely pulls
   through its existing EvidenceAcquisition, commits/readbacks, indexes and
   calls the real V1 locator publish. Preserve the exact separate outcomes.
3. A repeats that **same** request once to model a lost reply; prove by saved
   counters/journal that this is observation only, with no new acquisition,
   funding row or route command. Then stop A's data service.
4. Fresh C knows only a formal goal, matching profile and overlay bootstrap,
   not A/B's object ID or a private manifest. C derives the cell, obtains B's
   actual descriptor, verifies the returned authenticated search interval,
   and acquires the exact export and evidence from B. If a suitable prior
   mathematical fixture can be admitted cheaply, use the existing receiver
   once; do not produce a new certificate. At minimum distinguish structural
   retrieval from mathematical admission in the final evidence.
5. Close all roles and audit the exact inputs, outputs, budgets and cleanup.

This scenario decides whether the new intake/route composition actually makes
a remote contribution discoverable after publisher withdrawal. Existing local
controller faults need not be rerun. New focused controls should target only
envelope maximum/overflow, no token leakage, unauthorized/expired submit,
single-intake BUSY, dispatch interruption and lost-response observation.
Public-TLS verification must not be claimed from a plaintext loopback run;
TLS framing can be separately checked against an explicitly adopted local test
certificate without changing public trust policy or calling it global deployment.

No full-cost profit, independent hosts, sustained finite-disk rollover or final
v5 qualification follows automatically. Those remain separate obligations; this
proposal is one concrete high-payoff implementation boundary, not a new broad
research agenda or a substitute release label.
