# Ordinary advertised service: implementation checkpoint

2026-10-20, core_search. Root selected fresh source only. No runtime, network,
test, packaging, Git operation, proof or RAM investigation was performed here.
Independent source review and changed-boundary controls are separately owned.

## Delivered source/API

`software/v5/client/serve_advertised.py` supplies `async serve(context)` and
`main(context)` for the unchanged trusted-owner boot/outer Job. It preserves
used HTTP-only and location sources. No DHT, search, theorem-admission or
workspace-consistency mechanism is reimplemented.

Exact top-level parameter fields are the HTTP predecessor's fields plus
`location`; schema is `DMKN_V5_ADVERTISED_WORKSPACE_SERVICE_V1`:

```text
schema, mode, workspace_path, workspace_config, bind, tls, service_limits,
location = {
  installation_root, egress, listen, announce, bootstrap,
  limits, routes, health_interval_ms
}
routes = [{features: [sorted unique feature hashes], stripe: 0..255}, ...]
```

`location.limits` is the retained maintained-role contract:
`service_ms`, `operation_ms`, `query_events`, `provider_limit`,
`advertised_keys`, `provider_ttl_ms`, `reprovide_interval_ms`, `maintenance_ms`,
`commands`, `descriptor_requests`, `descriptor_reply_bytes`, `metadata`,
`transport`. Metadata accepts only the retained finite quota names (omitted
names retain finite adopted defaults). Transport's four counters remain exact.
The existing owner egress policy validates destinations; the small added
listen check reproduces only its missing Python counterpart. No new egress mode.

The location installation is explicitly owner-selected, canonical, disjoint
from mutable workspace/run paths, and pinned to the unchanged adopted base
manifest. The retained full `v4-library-commons-02/commons-v4` works as this
role; current projected `distribution03/base` lacks Node and must not be used.
No silent search for an executable, package installation or runtime fallback.
The unchanged controller verifies every selected runtime file before/after
use. All fourteen MJS pins come from the boot-selected context source map;
the complete boot selection still needs its existing twenty-one portable files.

## Coupled lifecycle

The service opens one existing workspace under its exclusive lock, starts its
existing mode-selected HTTP provider, derives the exact actual endpoint and
namespace, then creates the maintained index-provider role. Location state and
private-channel evidence are fresh under the run workspace, never under the
retained mathematical store or installation. No writer can publish concurrently.

Routes are explicit, unique and bounded to 32. Every route must return exact
`HINT_DISPATCHED_UNACKNOWLEDGED`, matching route key, a positive observed
ADD_PROVIDER-write count, no returned error and false mathematical/global/
placement authority. An incomplete route ends the composed service, preserving
partial outcomes and stopping its possibly already-enabled renewal intent.
There is no republish loop or silent HTTP-only success fallback.

Before READY, require a fresh RUNNING location status and live HTTP listener.
During service, observe Node exit immediately through `process.wait()` and
request finite interval health statuses. This detects a stopped locator whose
Node IPC process remains alive. Each status validates namespace and role and
rechecks `server.is_serving()`. There is one final reserved status observation
before normal stop, to catch internal failure in the last observation interval.
This is sampled operational readiness, not continuous external availability.

For requested HTTP lifetime t and health interval h, reserve
`ceil(t/h) + 2` status commands. Publish + all statuses + stop must fit both the
owner command ceiling and a conservative 60-command cap (retained IPC allows
62). Every publish and status command has parent deadline
`min(phase_deadline, now + location.operation_ms/1000)`.

Let q be one location operation allowance, H the HTTP operation/drain reserve,
L=6 seconds the unchanged location-close allowance and F=5 seconds the local
report/source-check margin. The active cutoff is the minimum of requested
lifetime, owner location ceiling minus 2q, and original outer deadline minus
`H + 2q + L + F`. The two q windows fund final status then stop; no grant or
deadline is renewed. The configured child timer has the existing one-second
minimum and starts after child startup; the earlier absolute parent cutoff and
original Job remain authoritative, even for a very short service.

Cleanup attempts location stop, location close/reap/post-pin checks, HTTP drain
and workspace close, in that order. Earlier failure does not skip later cleanup.
Forced termination, channel failure, uncertain close, original-deadline expiry
and primary failures remain FAILED. Cancellation attempts the same cleanup and
is then re-raised. Inherited non-async hash/OS work is not mathematically bounded
by an asyncio timer; the original Job remains the hard fallback. The reported
health delay `h+q` is conditional on timely event-loop scheduling, explicitly
separate from that hard outer ceiling.

## Output and limitations

Fresh `service-ready.json` uses schema
`DMKN_V5_ADVERTISED_WORKSPACE_SERVICE_READY_V1`. Terminal
`service-result.json` uses `DMKN_V5_ADVERTISED_WORKSPACE_SERVICE_RESULT_V1`.
Reports preserve route outcomes, current sampled status, actual endpoint,
namespace/wire profile, exact original/effective cutoffs, location/controller
and HTTP counters, source/runtime verification evidence and component cleanup.

The first composed profile requires explicit nonzero IPv4 HTTP port. The
location policy remains either exact loopback-test endpoints or public IPv4
with system-CA HTTPS. The current provider returns `server_name=None`, so
public TLS must validate against the numeric IP (an appropriate IP SAN);
no DNS name, NAT inference, relay, wildcard bind or private-address downgrade
is invented. Readers still need independently obtained authorized bootstrap
contacts. Source composition alone is not an installed public command until
the optional runtime role is selected in a later distribution.

An ADD_PROVIDER dispatch has no remote acknowledgement. Stop/withdraw affects
local renewal, not remote records; their retention depends on receiving nodes'
policy. No global discovery, storage or removal claim is made. Every report
sets `global_complete:false` and `mathematical_acceptance:false`; genuine
mathematical checking remains exclusively in the existing receiving pipeline.

## Evidence next

Use only the new focused inert controls for this lifecycle plus, if root
selects it, one tiny actual two-role descriptor-to-HTTP composition. Do not
repeat previous DHT/authoring/native/READY campaigns. No test result is claimed
by this source checkpoint. Full aggregate certification, growth advantage and
public deployment readiness remain open.
