# Service lifecycle: use finite serialized epochs first

2026-10-26. Source-only decision. No product imports, state inspection, tests,
network calls or product edits. This does not repeat the same-owner lock audit.

## Decision

The simplest operable route is **an owner-controlled finite schedule using the
existing public launcher**, with service leases separated by explicit publication
windows. Local agents can investigate in separate ordinary Lean projects and
perform state-free discovery while the disclosure-approved serving owner is busy.
Only intake/publication into that owner waits for its window. This needs no
simultaneous catalog mutation, new checker, replica consensus or persistent daemon.

Existing commands are sufficient to express this route; a safe, reusable
unattended sequencer is not currently shipped. Recommend a smaller first step:
**a finite service-only companion for N leases of one exact approved service
configuration/state**, with a preauthorized total horizon. Publication remains
operator-directed between plans. This removes per-lease human intervention without
inventing a mutation queue or selecting new mathematics. It must not be described
as continuous availability, automatic admission of arbitrary future work, or full
v5. Do not weaken the owner lock merely to avoid the orchestration step.

## Exact current selection

Default authority is `software/v5/ordinary_release_bundle/ADOPTION.md`.
Package `P/` below is
`experiments/v5-local-checks/transport-release-handoff01/suite/assembled/package/`.
Its observed PROFILE SHA-256 is
`b047d4492da79e363fcd154144a6d9088a93100fde7aac3c385f3a296a41dad7`;
installation manifest is
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
The newer archive-installation output does not silently replace this selection.

The inspected source copies match these actual default PROFILE roles:

| Source under `software/v5/` | SHA-256 |
|---|---|
| `ordinary_contact_federation/run.py` | `47a2b63c73f1bd8346c5881c6d6a76abac86d33aa8e55bfc19bf3359ea924a39` |
| `ordinary_sparse_access/peer.py` | `968d13e4c926b1520cba00502f3e98a87ffda7bdfefa0ec3fcf362c2d3efb655` |
| `ordinary_sparse_access/peer_api.py` | `48ec02f0ecf76f44d7ab64e6e029bdfb4f7ccb3aba8513711dd6b07952c917e9` |
| `ordinary_sparse_access/discovery_store.py` | `26ccca0fda86a255c38f7c3cc39b6b1fd88deba2ae10c6f79bc562b872c9502c` |
| `ordinary_bounded_transport/http_provider.py` | `9288996fa1d4e737f500043cddfc1c7935d9b7830ac6638596b6f7f278f2add7` |
| `ordinary_authoring_offers/ordinary_acquisition.py` | `d4599471b1285650876d53763c4a618a4dd5d7a953197954249052771a9df64f` |

The earlier `ordinary_bounded_operations/run.py` is not the actual selected
launcher; its contract remains useful documentation, not a substitute byte pin.

## What existing operations actually permit

1. Prepare separate, explicitly shareable owner/custody/index state. The whole
   custody must be disclosure-approved, including retained but unaccepted evidence
   and all dependency/sibling declarations; publishing a target is not an ACL.
   `EXPOSURE-BOUNDARY.md` and selected-export/intake already establish this route.
2. Use `P/run.py ... peer -- serve ...` with fresh diagnostics/output paths and
   a hash-bound service config. It requires existing index, `exclusive=true`,
   `share_all_custody=true`, explicit provider quotas, lease and cleanup reserve.
3. Wait for terminal clean closure, not merely `READY.json`. Then run selected
   `owner -- intake-baseline` if needed and `peer -- publish` serially. Use the
   actual returned local root/target identities, not a mutable global HEAD.
4. After successful publication and clean closure, start the next finite lease
   with fresh diagnostics/output. New index snapshots appear at the next lease;
   previous snapshot identifiers remain meaningful subject to retained storage.
5. Stop at the preauthorized horizon or any ambiguous outcome. No infinite
   `while true`, lock deletion, overwriting output or automatic mutation retry.

`P/run.py:160-202,280-355` has an explicit operation allowlist, one invocation,
hash-bound config/index path, finite Job envelope and no retry. It does not parse
mathematical results or run an arbitrary publisher program. `P/peer.py:174-226`
keeps find/preview/inspect/authoring-offers state-free but serializes serve,
publish and receive. `P/peer_api.py:738-800` verifies accepted target bindings
before indexing; multiple targets commit separately, so a failed publication is
not an atomic rollback. `:804-918` owns finite serving and cleanup.

Service lease accepts 1..3600 seconds, but launcher wall is at most 3600 seconds
and must cover bootstrap, lease and 10..60 seconds of cleanup. Thus a 3600-second
lease cannot fit that launcher; use a smaller lease and actual startup margin.
Remote binding requires TLS. Select a stable approved nonzero port for repeated
leases; port zero can change each time and needs updated contacts.

## Read snapshots are not a concurrency permission

The mathematical catalog owns checked contexts; custody holds inert bytes and
locators; the index holds derived searchable metadata. Only admission grants a
mathematical warrant. Serving happens to open/lock the catalog through this CLI,
but the HTTP provider does not check a theorem for every read.

Index trees/descriptors are immutable by content identity. That does not make
the current custody/index handles concurrent read replicas. DiscoveryStore uses
SQLite DELETE journaling (`discovery_store.py:57-122`), publication transactions
and new snapshot commits (`:221-274`). Current API explicitly requires exclusive
store use. Authoring offers are a selected in-memory snapshot (`peer_api.py:847-860`),
not a live file watcher. Do not bypass the CLI lock, copy live databases or assume
that merely selecting an old snapshot enables safe independent writers.

## Downtime, fairness and whole-cost accounting

Let epoch j have actual service time L_j, startup/closure gap G_j, and selected
mutation window M_j. In the ideal nonexhausted, failure-free case the service-time
fraction is sum(L_j)/sum(L_j+G_j+M_j). This is an accounting identity, not an
availability lower bound: quota exhaustion, provider failure and external
reachability can remove service earlier. No numeric improvement is asserted.

The provider closes admission after its lifetime accepted-attempt quota; malformed
or failed TLS connections consume attempts (`http_provider.py:269-304`). Byte
quota exhaustion can make further requests fail even while a lease is live.
Therefore a completed lease is not evidence of uninterrupted useful service.
Current inbound scheduling has capacity bounds, not per-user fairness or
adversarial availability. Periodic restarting restores an allowance only if that
next allowance was separately authorized; it is not a defense against saturation.

For N preauthorized epochs, reserve the sums of CPU caps, accepted-attempt caps,
response-payload caps, log caps and mutation costs across the whole plan. Add
launcher/sequencer CPU separately; do not add nested Job CPU twice. Response-body
limits are not total network-wire limits: headers, requests, TLS and refused
connections also cost resources. Keep an explicit total wall horizon, disk/log
budget and finite state quotas. Sampling/cleanup overshoot remains the launcher's
existing qualification. A finite sequence bounds planned cost, not infinite
sustainability; existing append-only index quotas eventually refuse without GC.

A reserved mutation window gives the scheduled publisher a turn if all other
writers obey that schedule and preceding operations close. It gives no fairness
against unrelated competing local processes, nor a progress promise for an
unbounded queue. Publication delay is at least the residual lease plus cleanup
and prior queued work. Choose lease length by the tolerated freshness delay,
not by making repeated bootstrap overhead artificially disappear.

## Recommended next action and stopping rule

If unattended service is selected, implement only a **finite, fail-closed
service-only runner around the unchanged public launcher**, outside frozen package
bytes. Inputs are one exact approved config/state/profile, N, aggregate
reservations and an original total horizon. Every operation is `peer serve`.
Run the existing `run.py` and its descendants under existing Job supervision too,
so its normally external wrapper is included in a per-epoch envelope; account for
the outermost runner separately. No new process-supervision implementation is
needed. Account for nested process counts/memory before choosing limits.

The complete plan has a fresh output directory, no resume and no overwrite.
Per-epoch fresh outputs/diagnostics, actual `LEASE_FINISHED`, `quiescent=true`,
empty cleanup errors and clean inner/outer supervision must all be checked.
Stop on nonzero/unknown outcome, `termination_requested`, state/profile/config
mismatch, exhausted original horizon or missing report. Never infer success
from readiness or exit zero alone. Do not include publication, intake, a general
shell, future-result watcher, arbitrary executable or automatic retry. A clean
new epoch consumes its prepaid allowance; it is not a retry of failed service.

This concretely lets an operator authorize, for example, an evening's bounded
serving once rather than manually restarting each sub-hour lease. Other agents
can continue private investigation/state-free discovery; publication into the
served owner waits until the service plan ends. A future contribution does not
silently change this plan's disclosure scope. It does not solve concurrent
same-owner publication, an unbounded arrival queue or indefinite service.

Windows Task Scheduler can start this runner with ordinary OS overlap settings,
but Scheduler alone does not interpret package reports, preserve uncertain
mutation outcomes, verify quiescence or reserve cross-lease payload/CPU quotas.
A documented PowerShell loop is an alternative only if it implements those same
checks; that is already the small service companion under another name. Prefer
one auditable project-owned helper over requiring each operator to reinvent the
checks. Do not install a scheduled task automatically as part of implementation.

A targeted source search of `software/v5` found existing finite service APIs and
test/harness checks of `LEASE_FINISHED`, but no current public repeated-service
plan runner. Historical managed-service lifecycle modules belong to different
product paths, not this selected package. No existing reliable public script was
identified that makes the proposed helper redundant.

Decision-changing evidence is one tiny two-lease native-free public service plan
plus failure/uncertain-cleanup and aggregate-exhaustion controls proving no next
epoch starts. Distinguish synthetic inert service fixtures from mathematical
admission; reuse prior transport/native evidence. No theorem campaign, transport
rewrite or native rebuild is needed. Stop when that narrow orchestration boundary
is established; do not expand into a general scheduler. Root must select exact
implementation/test scope before any execution.

Alternative: keep manual finite epochs and spend nothing on a runner. For a
future requirement of genuinely overlapping read service and updates, separately
select immutable disclosure snapshots or a dedicated inert rehost interface.
That would remove unnecessary catalog authority from serving but needs explicit
snapshot construction, transfer, update/retention and resource semantics. The
current lower-level API can rehost inert data only with caller-owned serialization;
it is not already a shipped concurrent service. Select that larger change only
if measured/required downtime or replication checking cost makes finite epochs
inadequate. Independent custodians can cover gaps, but that is a conditional
availability argument, not evidence of a deployed worldwide network.
