# Finite service-session source review

2026-09-21. Narrow read-only review of `manage.serve` and
`py/service_worker.py`, including their actual exposure-record and supervisor
interfaces. **No blocking source/interface mismatch found for this declared
operator-local, finite-session cut.** No service, imports, compilation, or test
execution was performed by the reviewer. This is not a service outcome result.

## Authority and view correspondence

The operator supplies one local client/view/session/port and explicit bounded
session allowances. The wrapper creates a new scratch session directory,
records `grant.json`, and launches the pinned worker under the actual process
supervisor. Reusing a session directory refuses; there is no restart/retry loop.
The worker holds the scratch services lock while serving, so this supported
entry path allows one service per node scratch domain. That lock is not evidence
of child quiescence; the supervisor supplies the latter observation.

The worker reads the exact current-config, selected-client `view` handle through
`ReadOnlyControl`: mode=ro, query-only, existing initialized state, no pending
execution, and a bounded read transaction closed before serving. It does not
construct the writable control-store interface or invoke node dispatch.

The actual exposure author and source both match the worker's expected record:
`{kind,directory,foundation,catalog,complete,selected,mathematicalAcceptance}`,
with kind `peer_view`, mathematicalAcceptance false, and a new
`state/work/<request>/peer-view` directory. Exposure requires owner publication
markers for the selected local candidate sequences before building the view;
node commits the immutable view record in its terminal transaction. This review
checks that handoff, not the complete peer-acquisition/publication implementation.

Service authenticates the stored catalog and completion pins and their
foundation/catalog-digest relation. It checks the selected count against the
catalog, then the wire service reloads the completed view and checks every
selected bundle length/hash. It does not translate sender metadata into
mathematical acceptance. The peer-wire/service modules are authenticated before
their imports; the worker/import closure is independently pinned by supervision.

## Bounded execution and files

| Allowance | Supported bound |
| --- | --- |
| Requested session wall time | 1..360 seconds |
| Supervisor success wall | requested seconds + 30, at most 390 seconds |
| Job CPU / private commit | 120 seconds / 256 MiB |
| Job process ceiling | 8 |
| Accepted connections | at most 128 per session |
| Charged attempted HTTP responses | at most 256 MiB per session |
| stdout / stderr / event | 65,536 bytes each |
| Worker request | 16,384 bytes |

The four Python flags, worker CLI, 11-file pin set, and limits fit the real
supervisor. CPU/memory limits are process-tree controls; wall/output polling and
cleanup retain the supervisor's documented limitations. The inner service also
has finite header/line/idle/transfer limits and binds only `127.0.0.1`.
Attempted response bytes are charged before sending; received header bytes are
separately bounded by request count/header ceilings, not included in that send
allowance. This is not a global bandwidth or aggregate lifetime quota.

The service path writes only session/grant/evidence/readiness/lock files under
operator-selected scratch. It serves selected immutable view bytes and does not
import the mathematical checker, launch Lean, initialize a database, or update
node state. The imported inspection module contributes its read-only store
class, not its mathematical inspection operation. The literal zero-native and
false-acceptance fields reflect this reviewed source scope, not process-image
attestation or a new kernel check.

Supervisor failure returns an explicitly unknown service outcome. Worker
refusal is surfaced as a nonzero owner-command result; it must not be treated
as proof that a crashed or partially completed session sent no bytes. Ordinary
service completion forwards the exact finite-timing observation JSON rather
than running it through the integer-only public-request decoder.

## Non-goals and prerequisites

The supported command is an explicit owner grant, not an untrusted remote
execution API. A new owner-issued session grants a new finite allowance;
there is no claimed automatic capacity policy or indefinitely running daemon.
Trusted installation, runtime, owner filesystem, and stable immutable view
bytes remain assumptions. Path checks/locks are not hostile-same-account
confinement. Loopback authentication, port impersonation resistance, multi-host
TLS, and release/runtime attestation are not established by this service cut.

A positive service qualification must still demonstrate a genuinely committed
view, observed readiness, actual HTTP acquisition, session termination, and
supervisor quiescence. Earlier transport tests exercised the lower wire service,
not this new database-backed owner wrapper. Owner-01 tested early refusal
contracts only; its pass does not qualify `manage.serve`.

## Reviewed source pins

| Source | SHA-256 |
| --- | --- |
| `manage.py` | `057038F1B1FB95D4D740B326A3ADC07226D27FCEB086CD3C3EA0006AC71E76AB` |
| `py/service_worker.py` | `C94098CD5EE08ED8A4977843B138B3C0CFB905EE8A6F9D67CA9E39991ED21E86` |
| `py/peer_node.py` (exposure interface only) | `99B7F3AF3C4C4E0B66827157E743A75EAC320A54D04E90C1E4A9912991A90B18` |
| `py/peer_service.py` | `58D355B183790E54C0BC5C96738E3AC0C2358AA1C65D0C1704D45E9EF8F28407` |
| `py/peer_wire.py` | `B4AAD584E9F6F6D83872501D277C1F1CDE79E5A89618EFBF1260497BEB8D4946` |
| `py/inspect_context.py` | `FD0248A77583A60C357C179E854D2109A4F6A546F67557E81737B586F842E549` |
| `py/node.py` | `986279A99EDE271CB1D2039F1433B02C2DCB7EB6D1940863AAA95E3E8C8A73CB` |
| `py/storage.py` | `2BEF745773269C0D80B8855FB40F2C38F36692B531D154C2597287BDDD492387` |

The reviewer authored the underlying domains/runner; this note independently
reviews root's wrapper/worker and their handoff, not the reviewer's own core.
