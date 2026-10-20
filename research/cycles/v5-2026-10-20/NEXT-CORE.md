# Next core step: serve a retained workspace without a workload recipe

2026-10-20, `core_growth`. Canonical guard passed. Source-only recommendation;
no implementation, runtime, Git mutation or renewed proof campaign.

## Single recommendation

Add one ordinary trusted-owner service entry, tentatively
`software/v5/client/serve_workspace.py`, that opens an **existing persistent
Workspace**, exposes its current index/semantic/evidence stores through the
existing bounded `CompositeProvider`, and closes cleanly at the owner's finite
deadline. Optionally compose the **existing** maintained location service for
explicit bounded route advertisements. No new protocol, scheduler or daemon
framework is needed.

This is a public-product capability, not another fixed mathematics campaign.
Inputs are local workspace/configuration, explicit wire mode, endpoint/TLS
configuration, finite service limits and optional selected location routes.
There are no BASE/FIRST/SECOND identifiers, source proof, receipt-production
request, ports fixed in code, historical-result loader or fixture phase.

Why now: `client.publish` ends at `LOCALLY_PUBLISHED`. `client/API.md` explicitly
says it does not start a provider, advertise a DHT record or replicate data.
An agent can contribute locally but currently needs to copy the networking
recipe from `actual_owner03.Strategy.consumer` or `terminal_strategy.Strategy`
to make that contribution available to another agent. `RuntimeProfile` closes
the analogous checking-owner construction problem, not this serving gap.

## Reuse, not duplicate

| Already present | Use unchanged |
|---|---|
| Persistent workspace and exact data profiles | Selected Workspace class, `open(..., create=False)`, its existing index/modules/packets, and `close()` |
| Typed read-only HTTP service | `frontier_network.transport.CompositeProvider` for atomic I-frontier packets; `mixed_network.transport.CompositeProvider` for mixed; `evidence_network.transport.CompositeProvider` for evidence/staged/validated |
| HTTP/TLS framing, request/concurrency/byte ceilings and shutdown | Existing `start`, `stop`, counters and binding policy; do not implement a second server |
| Optional discoverability | `AdoptedLocationRuntime`, `ServiceLocationProcess`, existing role/source pins and bounded `publish` commands |
| Honest query/acceptance boundaries | Existing authenticated index replies, recipient search budgets and genuine admission; serving does not create a warrant |
| Live mathematical reuse | Existing `RuntimeProfile` and ordinary client; not constructed by a data-only service |

Prior genuine I/native reciprocal evidence establishes that retained packets can
support actual semantic reuse and checked extension. The new real-owner
`runtime_check` targets factory integration and a retained receipt/import; it
does not serve persisted data. Prior actual network recipes establish component
composition but are tied to one workload. The new source-validation tests cover
bad index replies, not ordinary service startup/reopen/cleanup. None duplicates
this proposed release-owned service entry.

## Essential scope versus optional route maintenance

The essential deliverable is data persistence -> independently callable finite
read-only service -> clean stop -> reopen and serve the same retained data.
This needs no verifier, mathematical owner grant, Lean frontend or cryptographic
proof generation. Workspace bytes remain untrusted data; recipients still
perform normal admission.

Location is an explicitly configured composition option, not a prerequisite for
opening stored data. If configured, start the existing `index-provider` role
only after the HTTP service is listening; publish only the finite supplied
formal feature/stripe selections. Reuse its already implemented TTL/reprovide
mechanism within the original service lifetime. Do not enumerate all exports
to advertise, invent an automatic global topic planner, add route state
migrations, or create an unbounded refresh loop.

Publication data and service allocation have different lifetimes. Reopening
retained data uses a **fresh explicitly selected** service output/state
directory, deadline and allowance; it never restores an old live channel,
grant or successful JSON report. A stopped service's advertisements may remain
stale until their existing expiry. That is an availability hint, not acceptance.

## Implementation-ready contract

Use the existing launcher/boot trusted-owner entry convention, e.g.
`main(context)` with a finite parameter schema:

- absolute existing workspace path and exact existing workspace configuration;
- explicit supported mode; its store/provider types must match exactly;
- HTTP bind host/port and explicit optional TLS certificate/key selection;
- existing provider `max_connections`, `max_requests`, `max_reply_bytes`,
  `operation_ms` limits, plus a service deadline bounded by `context.deadline`;
- optional existing location configuration, exact portable source/role pins,
  bootstrap addresses, owner egress policy and bounded feature/stripe routes.

Keep the workspace disjoint from immutable installation/snapshots and the fresh
run directory. Never silently create an empty workspace when opening the chosen
existing one fails. Open exactly once and hold its existing exclusive lock;
this first entry does not permit a second writer process to use that workspace.
Concurrent publishing by a separately locked process is a later explicit
ownership/concurrency problem, not solved by removing the lock.

If HTTP startup succeeds but location startup/publication fails, preserve the
error and stop every successfully started component. On all exits stop
advertising/location, stop and drain HTTP tasks, then close the workspace.
Attempt every cleanup even when an earlier close fails. Report exact terminal
status, endpoint, namespace/profile, original allocation, service counters and
cleanup uncertainty. Do not call a dispatched DHT hint acknowledged replication.
The actual enclosing Job remains the hard resource/lifetime boundary.

No new store schema, proof cache, cost registry, receipt format or mathematical
acceptance rule is in scope. No remote-write endpoint is added.

## Smallest acceptance criterion

Source review plus focused finite controls should establish:

1. Caller-selected existing workspace/mode/config and limits are used; unknown
   mode, profile mismatch, absent workspace and bad limits fail without silently
   creating data or starting a service.
2. A fresh service owner exposes a retained **genuine mathematical packet's
   existing structural data**. Through its returned ordinary endpoint, a new
   bounded formal query obtains the expected candidate, exact group/opening and
   packet bytes without receiving its target content ID as the query input.
3. Stop and reopen under a distinct fresh service allocation. The same committed
   stored result remains obtainable; there is no original live client/issuer
   authority or private state repair. Source bytes and mathematical packet stay
   unchanged.
4. An injected failure after HTTP bind still closes HTTP and all started
   location processes; request/byte/deadline caps remain enforced.

Use the retained fusion packet/publication data named in RELEASE-DECISION and
ATOMIC-REUSE-OUTCOME as inputs, never regenerate them. A fresh test copy or
structural import of selected retained data preserves the frozen original.
One local two-lifetime service test can exercise the new boundary; it need not
rerun the full discovery/authoring/reciprocal campaign. If location is included,
use one already supported explicit route, not another routing benchmark.
Mathematical acceptance and independent-host deployment remain separate:
querying genuine bytes does not make this service test a new proof check.

## Simpler alternative and stop rule

The simpler alternative is directly documenting `CompositeProvider(...)`,
`start`, existing `ServiceLocationProcess` and `stop` for each caller. Those
APIs already suffice for an expert, and no new algorithm is needed. The small
entry is justified only if it removes fixture dependence, supplies one
correctly ordered lifetime/cleanup path, and is directly callable by a user.
If it expands into a generic service framework or repeated demonstration,
stop and retain the direct-API example instead.

This step makes another agent's contribution reachable and reusable using
existing primitives. It does not prove positive full-cost growth, permanent
retention, universal search completeness, independent public hosting or final
v5 completion. Those original requirements remain open, not downgraded.
