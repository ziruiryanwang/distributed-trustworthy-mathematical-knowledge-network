# Exact local discovery input preparation

2026-10-28. Source/data preparation only, following DISCOVERY-PLAN.md rather than
replacing it. No product import, index/database/owner access, service, network,
Lean operation, test or Git mutation occurred. Root owns any future exact launch.
Canonical root is `E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Prepared inputs and source checks

`serve-config.json` is a complete nine-field public serve configuration. It reopens
the actual finite-map index with the same six publication limits and create=false.
It requests one 300-second loopback lease, 15-second cleanup reserve, two concurrent
connections, 16 requests and 4 MiB total reply allowance. Whole selected custody is
explicitly shared; no new publication or authoring-offer map is selected.

This supersedes only DISCOVERY-PLAN's unused 120-second service proposal, following
root's explicit source-stage choice; no previous service was run or renewed.

`find-config-template.json` has exactly the six public find fields. Its three
contact fields host/port/tls are deliberately null: **do not run the template**.
Materialize those fields from this run's actual READY.json into a fresh file.
Everything else stays byte-for-value equivalent, including the known HashMap-only
query, providers, quotas, offer settings and atomic-v1 default. No new theorem
name, result ID, unit ID or expected answer may enter the query.

Source inspection covered the actual selected package's peer.py configuration,
state-free/stateful branching and readiness/result writes; peer_api.py contacts,
find, preview and serve; SearchSession's reservation bounds; candidate_query's
eight page limits; and http_provider.Endpoint validation. Values fit those exact
schemas and bounds. The index limits were compared with publication-request.json.
This was a source/schema check, not execution of product validators.

## Exact existing entrypoint and state

Use `experiments/v5-local-checks/kernel-admission-package01/distribution/package`
under the canonical root, PROFILE
`60b6e0d6c7d4e7d7761ed5f7ebb2d449afc55547f46f6924f0b93234a5a30f3b`.
The executable is `D:\Python314\python.exe -I -S -B PACKAGE\peer.py`.
Common flags are `--profile-sha256`, `--python-runtime D:\Python314`,
`--lean-runtime ROOT\software\runtime\lean-4.34.0-windows`, `--config`,
`--config-sha256`, `--output`, `--wall-seconds`, `--cpu-seconds`, `--memory-mib`.
All paths in an actual invocation must be absolute canonical paths.

Serve additionally supplies:

- `--catalog ROOT\experiments\v5-local-checks\std-kernel-catalog01`
- `--custody ROOT\experiments\v5-local-checks\std-kernel-custody01`
- `--store-id fb625cc1b7d03d081e45bbcf73f7d59765f04a64a402484f23d00ac3e60ce4e7`
- `--custody-limits` pointing to the exact selected snapshot of
  `software/v5/ordinary_std_intake/custody_limits.json`.

Find and preview must omit every state flag. No new recipient owner or library
grounding is involved. Serve holds the existing original owner's lock until
cleanup completes. Do not run its contribution, publication or another service
concurrently. The separate fresh frontier-control owner does not share this lock.

## Root-managed sequence using the existing supervisor

Prepare immutable package/runtime pins, source/config templates and all selection
schemas before starting the lease. Use fresh run names, such as
`finite-map-discovery-serve01`, `finite-map-discovery-find01` and
`finite-map-discovery-preview01` through `06`. These names are proposals, not
created runs or reservations. Each operation uses tools/Run-V5-Check.py directly.
It already starts the peer command without another workflow program. Include the
actual config as a selected source under software/v5, and use
`--config {snapshot}/software/v5/ordinary_finite_map_refinement/FILE.json` so the
runner's command is bound to a source snapshot. Output is a fresh child such as
`{output}/peer`, not the runner's existing command directory. Pin package files,
runtime inputs and original immutable event evidence; do not pin mutable SQLite
or lock bytes as if serving guaranteed no recovery/administrative writes.

| Call | Public wall / CPU / MiB | Outer wall / Job CPU / MiB / processes |
|---|---|---|
| serve | 330 / 30 / 768 | 360 / 45 / 1024 / 4 |
| find | 45 / 15 / 512 | 60 / 20 / 768 / 3 |
| each preview (at most six) | 35 / 8 / 384 | 45 / 12 / 512 / 3 |

One MiB per outer stdout/stderr stream is sufficient for these bounded reports.
The public peer has no native worker in these operations; the outer processes
cover the actual Python launcher/peer child and margin, not invented Lean calls.
The service API requires lease+cleanup to fit strictly inside its **remaining**
public allowance after startup. A startup consuming 15 seconds can therefore
refuse; it does not receive a renewed 330 seconds. Preserve that outcome.

After starting serve, retain its live process handle and wait only for its own
`{output}/peer/READY.json` or terminal result. A file is not evidence that the
process is still live. Check READY.status=READY, host=127.0.0.1, integer
1<=port<=65535, tls=false, lease_seconds=300, exact selected index/custody paths,
and mathematical_acceptance=false. Copy host/port/tls into the template's sole
contact. Select/hash the resulting fresh JSON before the find invocation.
The current READY schema has no absolute expiry timestamp; retain startup/readiness
observation times locally without treating them as a provider availability proof.

Require find's actual report ok=true, operation=find, matching PROFILE/config,
result status INCOMPLETE_SEARCH, the expected namespace and final published
snapshot when no publication intervenes. Preserve all provider errors, termination,
search/network charges and explicit coverage flags. For preview, copy only the
three returned match fields provider/snapshot_id/record; do not reconstruct the
record from the prewritten acquired-targets file. Each fresh preview config is
exactly contacts (actual find contact), selection (returned fields), and
limits={requests:1,reply_bytes:65536}. Preview all returned matches if at most six;
an unexpected larger/different set needs a fresh decision, not truncation relabeled
as the intended outcome. Root can prepare these six independent selections in one
bounded data step and run at most two concurrently, matching the provider cap.

Find reserves at most nine requests and the six previews at most six more, within
the original 16-request service ceiling. Worst-case public wall allowances do
**not** guarantee all six previews fit the 300-second lease: root planning and
source-selection time also passes. The new lease does accommodate a 45-second
find plus six 35-second public preview grants (255 seconds) with some margin.
Prepare first, run
promptly and preserve any expired/refused/partial result. Do not extend the lease,
retry failed requests or change the fixed cap. If only the intended two types are
needed and already identified from returned previews, omit unused later calls;
the operation must still report which actual candidates were inspected.

After the same service handle becomes terminal, require public LEASE_FINISHED,
quiescent=true, empty provider/owner/custody cleanup errors and outer clean reaping.
Only then may same-owner refinement begin. Closing the service does not establish
future or independent-provider availability.

## Adopting the bridge to theory use

Preview must return PREVIEW_BOUND_NOT_ACCEPTED, exact selection/preview binding,
the actual formal header and type_bindings, and no mathematical
acceptance claim. Read the types: select the universal nonemptiness equivalence
and zero-summary execution witness. Derive acquired triples as name from
preview.export_name, unit_id from preview.unit_id and export_id from the matched
record.object_id. Check against the prospective local acquired-targets.json only
after that selection. Agreement closes the interface bridge; it does not establish
independent receiving, novelty, a blinded discovery study or causal growth speedup.

No missing executable edge was found. Root can supply fresh JSON from saved
public outputs and use existing CLI/supervision, without changing an old kit's
compatibility map or writing another protocol or orchestration program.
