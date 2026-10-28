# Dedicated inert host: lifecycle and public boundary

2026-10-28. Source-only implementation specification. No code or operation is
selected by this file alone. Root owns implementation selection. The existing
[data path](DATA-PATH.md) supplies codecs/storage/index/provider primitives.

## Fixed layout and public inputs

One freshly created absolute ordinary directory `H` owns exactly these roles:

```text
H/DMKN-DEDICATED-HOST.json   permanent exclusion marker
H/host.lock                one-byte OS lock file
H/custody/ordinary.sqlite   existing inert custody database
H/index/discovery.sqlite   existing discovery database
H/HOST.json                final sealed-generation descriptor
```

Existing stores may create their documented bounded SQLite sidecars. No arbitrary
role path, owner catalog, source, native snapshot or executable payload is added.
Operation reports, listener READY records and launcher diagnostics stay outside H.

Public entry: `host.py prepare|serve`, with existing PROFILE/runtime/finite
allocation arguments plus `--host-root`, `--config`, `--config-sha256`, `--output`.
Serve additionally requires `--host-sha256`, the exact selected HOST.json hash;
prepare forbids it. No catalog/store-id/custody CLI selection is accepted.
The root's bounded launcher must expose the host entry without granting extra
paths or bypasses to ordinary owner/peer/query operations.

Prepare configuration has exactly:

```text
{
  schema: "DMKN_DEDICATED_HOST_PREPARE_V1",
  bundle_directory: absolute path,
  manifest: {path: absolute path, sha256: lowercase 64-hex},
  targets: [{name, export_id, unit_id}, ...],
  custody_limits: {objects, exports, logical_bytes, db_pages},
  index_limits: {every existing discovery Store limit: selected integer},
  share_all_bundle: true
}
```

An optional `bundle_limits` object may supply any subset of existing
`baseline_bundle.Limits` fields, lowering their finite defaults; unknown fields
refuse. All existing limit validators and ceilings apply unchanged. Targets are
one through 64 existing `{name, export_id, unit_id}` rows with distinct export
IDs. They are embedded in the pinned configuration, not a separate artifact.
Every target unit must occur in the bundle; target identities must match actual
selected bytes. First version omits pair
access configuration and authoring offers; existing atomic indexing is sufficient.
The entire selected bundle and all generated export locators become addressable,
not only indexed targets. `share_all_bundle:true` approves that exact disclosure.

Serve configuration has exactly the existing provider fields:

```text
{
  schema: "DMKN_DEDICATED_HOST_SERVE_V1",
  host, port, tls, lease_seconds, cleanup_seconds,
  limits: {existing provider limit fields},
  share_all_custody: true,
  exclusive: true
}
```

The controller removes its schema and derives the existing `index` selection
from HOST.json with `path=H/index`, `create=false`, and sealed limits. Custody
selection similarly comes only from HOST.json and `H/custody`. Existing TLS,
address, lease, cleanup and provider validators apply unchanged; non-loopback
requires pinned TLS inputs. Config files, bundle/manifest/target inputs, TLS
files, output, package and runtime roots are all disjoint from H.

The selected helper signatures are:

```text
prepare(loaded, host_root, config, allowance, *, profile_sha256, finalize)
serve(loaded, host_root, config, allowance, *, profile_sha256,
      expected_host_sha256, finalize, ready=None)
```

The root-owned wrapper captures the exact pinned config bytes and bootstraps
approved support. Its `finalize()` rechecks captured config and selected profile.
The helper invokes it before sealing or starting service and after service
cleanup. The helper owns host creation/locking, store opening/closure and sealing;
the wrapper owns only its external output/report and whole-process supervision.
Both helper entrypoints are synchronous. `serve` runs the existing asynchronous
provider through its own `asyncio.run` while holding the host lock. Runner shutdown
must cancel/drain remaining provider tasks before custody or the lock closes;
putting the runner outside this helper would release them too early on SDK failure.
An unresponsive shutdown remains subject to the original outer process allowance.

## Prepare and seal

Before creation, validate all finite inputs/config and ordinary paths. H must
be fresh with an existing parent, not beneath another host marker or a recognized
existing state root (`ADOPTION.json`, `ordinary.sqlite` or `discovery.sqlite`
at an ancestor). This conservative ancestor check reads names/metadata only;
it does not open another store. Disjointness from explicit inputs/support/output
remains required. No global directory scan or state registry is introduced.

Create H, then write the permanent marker **before either store exists**. Its
exact canonical JSON is `{"schema":"DMKN_DEDICATED_HOST_V1"}`. Unknown,
malformed, nonregular or redirected markers refuse; ordinary non-host guards
refuse merely on marker-path existence without interpreting it.

Create `host.lock` containing one zero byte and acquire an exclusive nonblocking
Windows byte-range lock at offset zero using the existing `msvcrt.LK_NBLCK`
pattern. Validate ordinary path/single-link/size, retain the open handle, and
do not delete/recreate a lock file to break contention. Contention refuses;
the operation does not wait, retry, reset or increase its original allowance.

Under this lock, create **fresh** custody/index children and execute DATA-PATH's
bounded validation, custody insertion and target indexing. Partial stores are
never treated as ready. After final input/profile checks and successful index
and custody close, write a fresh pending descriptor and rename it to `HOST.json`.
The closed generation descriptor has exactly:

```text
{
  schema: "DMKN_DEDICATED_HOST_SEAL_V1",
  profile_sha256, semantic_id, namespace,
  manifest_sha256, targets,
  custody_limits, index_limits,
  custody_counts: {objects, exports, logical_bytes},
  index_snapshot_id, index_objects,
  assurance: "INERT_HOST_NOT_MATHEMATICAL_ACCEPTANCE",
  mathematical_acceptance: false
}
```

The marker bytes and child paths are fixed by this schema. Seal actual
`custody.status()["counts"]`, index status `latest` and `objects`, not inferred
unit counts. Units/evidence-byte totals remain preparation-report accounting.
The outer wrapper report pins exact config bytes; this helper descriptor does
not pretend a re-encoded config hash is the original input file hash.
No absolute preparation-input path is needed to serve. `profile_sha256` binds
this first version to its explicitly selected exact package; upgrades require
a separately designed transition, never relabeling the descriptor. Source/config
hashes select bytes and do not authenticate or certify mathematics.

Release the lock after descriptor finalization; report operation success only
after closure. The descriptor commits prepared data, not a claim that all later
report writes succeeded. If a failure occurs after it is installed, retain it
and report its publication state; do not erase it, report success or automatically
serve it. A later operation requires a fresh explicit selection of its exact pin.

## Serve and closure

Validate ordinary H/layout and its marker, then acquire the same host lock before
opening either SQLite store. Under lock, re-read and verify the selected HOST.json
pin, exact schema, PROFILE/semantic/namespace, fixed paths/limits, exact marker and
inert status. Missing HOST.json refuses even when partial databases exist.
Never follow descriptor-supplied arbitrary paths or accept an existing owner
custody directory as H by adding a marker.

Open existing custody and invoke existing owner-free `peer_api.serve`. Its index
opening must use the sealed existing index configuration. Compare the custody
status triple with `custody_counts`; briefly open the index with the existing
`_index(..., owner=None, create=False)` path, compare `latest`/`objects` with
`index_snapshot_id`/`index_objects`, and close it before invoking SDK serve.
The same root lock remains held through both openings. No full database hash is promised or
required: existing protected local storage and per-response identity checks
remain the premise, not a new authenticated database design.

Only the provider's actual listening callback can write this invocation's
`output/READY.json`. HOST.json means prepared content, not a live listener. Hold
the lock through the full finite lease, stop/drain the provider and close its
index, close custody, then release/close the lock. Attempt each cleanup on failure
under the original allowance. Report partial closure honestly. No automatic
renewal or resumption follows.

Successful reports remain `mathematical_acceptance:false`, with status
`PREPARED_INERT_HOST` or the existing finite-service result, exact host/config
pins, closure states and costs. Never emit an owner acceptance/root. Recipients
retain their unchanged dependency/identity/checking policy. Incomplete bundles
may be served honestly; complete dependency availability is not inferred.

The hosted generation has immutable **logical content**: no `put`, `admit`,
refresh, migration or pruning is exposed after preparation. Existing SQLite
reopens use read-write handles and configuration PRAGMAs and may recover journals.
Do not call this filesystem-read-only operation. A failed preparation retains
its partial root and cannot be restarted there; choose a newly selected root.

## Exclusion across the supported public commands

A host lock alone does not exclude old owner commands pointed at `H/custody`.
The minimal new supported package must therefore include these auxiliary guards:

| Entry boundary | Required refusal before mutation/open |
|---|---|
| Fresh `owner.py` `separated(paths, code)` | Reject any supplied path equal to or beneath a marker-bearing ancestor. Current owner state/output, peer state/index/output and query output/catalog paths already pass here. |
| `owner.py` producer path | Explicitly apply the same refusal to producer output before `produce_bundle`; that branch does not currently call `separated`. |
| Fresh `run.py` separation | Reject diagnostics and ordinary writable paths below the marker before `diagnostics.mkdir` or any launcher report. Child validation occurs too late to protect diagnostics. |
| Dedicated host entry | Use its own checked disjointness and host lock, permitting only its exact selected H; all external outputs/diagnostics still reject host descendants. |

Checking a path means bounded ancestor inspection, including the selected
directory itself and existing parents of a fresh output. Presence of
`DMKN-DEDICATED-HOST.json` is sufficient to deny non-host access, regardless of
its content. Permission/path errors refuse. Existing ordinary path rules reject
links/reparse points and filesystem alias tricks; current protected-path premises
still apply. The guard never deletes a marker or recursively scans directories.

The launcher may exempt the exact `--host-root` from this refusal only for its
validated host entry. It still includes H in all overlap checks and guards
diagnostics/output. No generic `allow_host` flag reaches ordinary commands.
The host controller never bypasses the ordinary guard for other paths.

These changes need no installed-core, implementation-ID, schema-of-stores or
mathematical-owner migration. Changing the current auxiliary owner and launcher
changes their selected package pins. A separate `peer.py` copy is unnecessary
because its existing checks use `base.separated`. Implementation review must
verify those actual call sites and all fresh output branches remain covered.

## What the exclusion argument does and does not establish

Assume the marker is retained under protected local storage, current supported
entries obey the guards, and all dedicated operations obey the lock. Then at
most one dedicated operation opens the stores; ordinary supported commands
cannot open/mutate their paths. Marker-before-store creation plus constructors'
fresh-directory checks prevents a racing failed preparation from producing a
successful mixed generation. The caller must not remove or replace marker/lock
files while any operation is live. Crashes release OS lock handles; they do not
turn a partial root into a sealed one.

Previously frozen executables, arbitrary SDK calls, approved source code with
filesystem effects, and hostile code running as the same OS user can ignore the
marker or mutate stores. The new package does not sandbox these actors or revoke
old executable copies. Running them against H is outside this supported-command
serialization guarantee. Protected-OS/cooperative local execution remains an
explicit premise. Stronger isolation would need separate principals/OS policy,
not a dishonest marker claim. No such system-policy change is selected here.

The contract is implementable with auxiliary sources and existing storage APIs.
No broad migration is required. Review this lifecycle and the unchanged acceptance
boundary before selecting small changed-boundary controls; no experiment, daemon
framework, new replication policy or further theory episode is commissioned here.
