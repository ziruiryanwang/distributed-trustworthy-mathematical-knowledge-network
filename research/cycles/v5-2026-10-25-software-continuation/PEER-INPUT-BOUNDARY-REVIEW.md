# Peer-input boundary: two concrete transport findings

2026-10-25. Independent source-only challenge by `ordinary_routing_gap`, with
decoder-only review by `ordinary_routing_gap/decode_limits`. Root owns selection,
implementation and execution. No product/helper import, test, build, network,
database, archive extraction or Git action occurred. No existing source/evidence
was edited. The witness traces below are deductions from source, **not executions**.

## Decision

Two actionable public-service defects were found: the connection cap is applied
after TLS negotiation, and shutdown waits for clients before cancelling them.
Neither is a mathematical-acceptance bypass. The reviewed inert-data/checker
boundary otherwise supports the earlier trust-boundary argument; no concrete
remote-selected executable/path or byte/depth/node-limit bypass was found.

The highest-payoff next change is a small fresh transport successor: bound raw
accepted connections before TLS and close/cancel owned connections before
awaiting shutdown. Do not reopen proof-certificate work or modify the checker.

## Exact source and assumptions

All package references below mean:

`experiments/v5-local-checks/sparse-access-assembly01/assembled/package`.

| Reviewed binding | SHA-256 |
|---|---|
| `PROFILE.json` | `97f93cc66f77ebcecd7a3a341baaaf4725236a8dec5fb9cee3c3e67d478f2834` |
| `peer_api.py` | `48ec02f0ecf76f44d7ab64e6e029bdfb4f7ccb3aba8513711dd6b07952c917e9` |
| `support/transport/http_provider.py` | `f81cdcaebbf05ad97342b81ac64444b33695b576045c8da41ba6f0a0903dd691` |
| `support/transport/ordinary_acquisition.py` | `d4599471b1285650876d53763c4a618a4dd5d7a953197954249052771a9df64f` |

The installed Python is `D:\Python314`. Its actual asyncio sources were read,
not imported, to avoid assuming obsolete `Server.wait_closed` behavior:

| Supplemental runtime source | SHA-256 |
|---|---|
| `Lib/asyncio/base_events.py` | `da597bc24e06382d9ef836d84d0e383ad1f6fd61d3b1fb1bfd2bd50d359f97b0` |
| `Lib/asyncio/sslproto.py` | `4b824f705e7c6c0a431d8b1154e9c3ca88128b6b37d07a795ad4f013b65d6f18` |
| `Lib/asyncio/streams.py` | `a45afc8e3e4480879d8e63f7fb567bd77825b453792bc1ca0419c7669d29f366` |
| `Lib/asyncio/proactor_events.py` | `edfe546a07074ed405ca7e7e27e7810082a17d419e00576db2445a672749020c` |

These hashes identify the source used for this argument, not a new hermetic
runtime attestation. Protected approved implementation/runtime and local state
remain premises. A hostile provider or connecting client is in scope; a hostile
same-account owner replacing that implementation is not.

## Finding 1 — application cap does not cap raw connections/TLS work

**Priority: P1 before public hostile-network exposure; availability/resource
accounting, not mathematical soundness.**

`http_provider.py:180–187` passes TLS directly to `asyncio.start_server`, with
backlog 16 and a five-second handshake timeout. The only connection/request
admission check is in `_serve`, lines 284–288: `len(self.tasks)` and
`self.requests`. Those counters change only when the application handler runs.

The selected runtime makes the reachability precise:

- `streams.py:78–84` installs a `StreamReaderProtocol` factory.
- `proactor_events.py:843–861` accepts a raw socket, constructs the SSL
  transport, and starts the next accept without consulting `Provider` counters.
  The raw transport attaches to the runtime Server at lines 65–66.
- `sslproto.py:604–606` invokes the application protocol's `connection_made`
  **after** successful TLS negotiation. Only then do `streams.py:238–256`
  invoke/schedule `_serve`.

**Source witness.** Configure a remotely reachable TLS service with
`max_connections = 1`. Establish at least two raw TCP connections and withhold
TLS completion on both. Until the five-second handshake timeout, both raw
transports and TLS states exist while `Provider.tasks` and `Provider.requests`
can still be zero. Continuing arrivals can replace expiring handshakes. No
trusted client certificate or valid mathematical/request body is required.
Backlog 16 bounds the pending accept queue, not the population already accepted
into TLS. The application `max_requests` likewise does not charge failed
pre-application handshakes.

Plaintext loopback does not have the five-second hidden handshake phase: its
application callback is scheduled after raw acceptance. Its cap still starts
after socket/reader/task allocation and is therefore an active-handler cap, not
a strict bound on every accepted socket or transient callback. No claim of
unlimited plaintext retention is made.

The public outer Job bounds aggregate process private commitment and eventually
stops excessive CPU/wall usage. It does not enforce this connection count, a
kernel socket/handle quota, or fair service to legitimate clients. Thus this is
not an escape from all resource limits; the avoidable outcome is service
starvation or exhaustion of the enclosing allocation before the advertised
application cap takes effect. No rate or memory exhaustion threshold was tested.

**Smallest defensible implementation remedy.** Own a raw listening socket and a
bounded accept loop. Reserve an active slot before starting its next accept;
track every accepted socket and handshake task before calling the public
`loop.connect_accepted_socket(..., ssl=...)` conversion. Keep the slot until
actual transport/socket closure, including failed handshake and cancellation.
Use the existing finite request ceiling additionally as a paid accepted-connection
attempt ceiling, while retaining distinct honest application-request counters.
Stop accepting at exhaustion, without retries or budget renewal. Keep the
existing TLS validation, handshake/shutdown timeout and HTTP byte bounds.

A semaphore **inside `_serve`**, a shorter handshake timeout, or backlog tuning
alone does not fix the pre-TLS admission gap. A separately configured trusted
front-end enforcing raw connection limits is an operational alternative, but
does not make this provider's own cap an end-to-end transport bound. No new
front-end subsystem is recommended for this local repair.

## Finding 2 — shutdown waits before cancelling the clients it awaits

**Priority: P1 for reliable finite service shutdown.**

`http_provider.py:191–196` calls `server.close(); await server.wait_closed()`
before taking `self.tasks`, cancelling them and gathering their completion.
In the actual Python 3.14 source, `base_events.py:335–352` closes the listener,
not existing clients. Lines 389–409 explicitly wait for **both** listener closure
and every attached connection to drop. This contradicts the ordering needed by
the code: client cancellation is located after the wait that needs it.

The peer lease requires only a 10–60 second cleanup reserve
(`peer_api.py:829–835`; directory service has the same range at 410–416), while
one application operation may last 60 seconds. `peer_api.py:888–907` wraps the
incorrectly ordered `stop` in that cleanup deadline. Its fallback cancels
application tasks only after timeout, when the original cleanup reserve is
already exhausted; it does not directly abort runtime-owned pending TLS clients.

**Source witness.** Use an allowed `operation_ms = 60000` and
`cleanup_seconds = 10`. Just before the service lease expires, connect and
withhold the HTTP header terminator. On a remote TLS service, first complete
TLS; the same trace is possible directly on allowed loopback HTTP. `_serve`
waits in `_headers` until its operation deadline, about 60 seconds away.
`stop` closes listening and waits for that still-open client before it reaches
task cancellation. The ten-second cleanup deadline expires first. This is a
reachable `cleanup_errors`/uncertain service exit, even with one client and
valid finite configuration; it is not a false mathematical acceptance. Existing
clean tests with no connected clients at shutdown do not cover this trace.

Incomplete TLS connections are a related ownership issue, but their normal
five-second handshake timeout alone is shorter than the minimum ten-second
reserve; this finding does **not** claim that one stalled handshake necessarily
exceeds that reserve. They still need explicit shutdown ownership rather than
being absent from the application's task census.

**Minimal remedy.** Stop accepting first. Cancel owned application/handshake
tasks and abort/close all accepted transports/sockets before awaiting them and
the listener's final closure, within the original cleanup deadline. In the
unchanged `asyncio.Server` implementation, public `abort_clients()` and
`close_clients()` are available (`base_events.py:354–360`); do not inspect private
`_clients` or rely on a post-handshake task set to cover pending handshakes. A
manual accept-loop successor should keep its own complete ownership set instead.
Do not clear the provider's server/connection references or report `quiescent`
until closure has actually been observed. Apply the same ordering to the
exception fallback and preserve all cleanup uncertainty.

## Boundary that did not produce a finding

The original trust-boundary checkpoint was reused, not requalified by testing.
The following source paths were independently challenged:

- HTTP reply lengths are checked before `_body`, with fixed route caps; selected
  endpoints are owner-approved, and wire data has no executable/path field.
  `OrdinaryBudget` charges every begun attempt, including its full cap on failure
  (`ordinary_acquisition.py:283–343,359–392`).
- `portable_evidence.read_evidence` requires exact fields, selected grammar and
  exact ordered direct-import census. `ordinary_evidence.py:75–138` checks byte,
  JSON-depth and integer-token limits **before** the general JSON parser;
  backward DAG indices, scope/depth and aggregate counts are independently
  checked. A peer cannot supply a replacement `Limits` object.
- `peer_api.py:624–690` enforces finite units/bytes/missing/preflight limits;
  selected-unit-only returns missing-premise status without ancestor fetch.
  `inspect` and `preview` remain explicitly not accepted/native-usable.
- `ordinary_admission.py:565–585` recomputes the plan. Its fixed command paths at
  587–616 and 676–710 come from selected local support and locally created call
  directories, not names supplied in evidence. Only a clean actual worker and
  exact report/artifact bindings reach `_commit_checked` at 626–647.
- Decoder review found no new bypass: `OriginalExpr.lean:321–447` reconstructs
  bounded shared DAGs, closes scope and re-encodes; `OriginalDecl.lean:357–378`
  preflights aggregate counts/overwrites/roundtrip; `CheckedExtension.lean:109–150`
  grounds references, uses `addDeclCore(..., doCheck := true)`, and checks exact
  generated inventories. This is not a mechanized kernel-correctness proof.

The decoder-only reviewer identified large-natural bytewise conversion as a
potentially quadratic cost (`OriginalExpr.lean:168–175,419–425`). Existing native
and outer CPU/commit caps remain necessary. Since this does not evade the
declared byte/node/CPU boundary, it is **not promoted to a third actionable
defect** or a reason to start a separate optimization campaign.

Decoder source hashes:

| Source | SHA-256 |
|---|---|
| `installation/py/ordinary_evidence.py` | `fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6` |
| `installation/lean-src/OriginalExpr.lean` | `8278826700b17f8a926bebcf36e0408540ddfa3e84637ce4c8ff8f37c9dce72b` |
| `installation/lean-src/OriginalDecl.lean` | `bfb5fc910808d9dc178977cfa6edeacf0b5cbfe7bd99bc6277ee11a456d516c1` |
| `installation/lean-src/CheckedExtension.lean` | `4c3f3d600eda6319dd6d4578797e16ae6dc0ab81cf97ca4d7bce014081463ea1` |

## Consequence and finite next discriminator

Root may select a fresh transport-only successor, preserving the exact frozen
sparse package. Source review should establish admission/ownership before TLS,
unchanged accepted HTTP routes, and cancel/close-before-wait shutdown. The useful
changed-boundary checks are (1) stalled loopback TLS handshakes under a one-slot
cap, (2) shutdown of a live incomplete-header request whose operation deadline
exceeds the cleanup budget, and (3) one ordinary positive read through unchanged
dispatch. Assert actual closure and paid attempts, not just reported counters.
No test, new assembly or runtime is authorized by this recommendation itself.

These findings advance safe ordinary service operation. They neither reopen
native soundness evidence nor establish new concepts, useful growth, worldwide
availability or completion of the full v5 objective.
