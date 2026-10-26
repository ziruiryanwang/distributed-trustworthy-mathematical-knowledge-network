# Inert mathematical mirror: source-only operator companion

**Source implementation; not yet executed/adopted.** This companion lets a
storage operator prepare one explicitly disclosed finite mathematical-data bundle
and serve its exact bytes plus selected formal search records. The operator needs
approved Windows x86-64 and Python 3.14.6, **not Lean, a native package build,
a mathematical owner/catalog or a certificate**. Every mathematical consumer
still independently checks what it uses. This is availability/discovery plumbing,
not a claim of useful-growth acceleration or completed v5.

Use ordinary bundle copying for backup or known-bundle transfer. This companion
is useful when unchanged clients need unknown-ID formal search and selective
evidence retrieval. It does not automatically fetch, replicate, publish elsewhere,
maintain, update, repair or run forever. Everything remains local/unpublished;
the project's license is undecided.

## Approved software and source layout

Keep this folder's `run.py`, `mirror.py` and `SOURCES.json` together **outside**
the unchanged investigator source extraction. Use the current 169-file investigator
distribution selected by `ordinary_investigator_bundle/ADOPTION.md`, whose manifest
SHA-256 is `65edf28f928d4100346a4603fe508252ddc6393950c34a373fbb33da4c6491f5`.
The companion's fixed SOURCES SHA-256 is
`1bc43d4c9896476443d0d6aab95015db7af32bc46a04cfb1624a5c40e638feb9`.

The loader verifies 27 selected source/data files, totaling 1,212,995 bytes,
including the fixed inventory. It loads only pinned pure codecs, existing
discovery/custody/HTTP helpers and the existing Windows Job supervisor. It neither
runs the investigator native build route nor uses PROFILE/INSTALLATION metadata.
Package import paths are closed; unlisted modules are not fetched or imported.

Independently approve the companion sources, fixed manifest and runtime before
running them. File hashes supplied beside untrusted code do not establish trust.
The launcher pins the selected python.exe/python314.dll/python3.dll and requires
`-I -S -B`; this is not attestation of every runtime/OS dependency. The approved
Python distribution must include its normal stdlib, SQLite and TLS dependencies.
Jobs limit resources, not filesystem/network privileges. Software, inputs and
prepared state must remain protected against unauthorized local modification.
Never execute a received Lean project, native module or Python source.

## Prepare exact inert stores

Obtain an existing `DMKN_ORDINARY_BASELINE_BUNDLE_V1` directory, its independently
selected `manifest.json` digest, and the actual exact `{name, unit_id, export_id}`
targets from the data handoff. The manifest defines the full disclosed data set;
targets limit indexing only. Whole units, imported dependencies and supplied
sibling declarations will remain addressable. Approve that entire disclosure.

Create an operator request with this shape; the target/hash placeholders are not
valid ready-to-run identities. The illustrative structured name encodes `A`;
copy the actual complete target rows from the handoff, rather than transcribing names:

```json
{
  "schema": "DMKN_INERT_MIRROR_PREPARE_REQUEST_V1",
  "bundle_directory": "C:/commons-data/approved-bundle",
  "manifest_sha256": "REPLACE_WITH_EXACT_MANIFEST_SHA256",
  "targets": [{"name": [[0, {"$bytes": [65]}]], "unit_id": "ACTUAL_64_HEX", "export_id": "ACTUAL_64_HEX"}],
  "output_directory": "C:/commons-data/mirror-01",
  "share_all_bundle": true,
  "limits": {
    "units": 1024, "bytes": 67108864, "nodes": 2097152,
    "names": 65536, "edges": 262144, "targets": 64,
    "preview_bytes": 16777216, "metadata_bytes": 16777216,
    "output_bytes": 536870912, "index_hash_steps": 32000000
  }
}
```

Limits may only decrease. Optional `custody_limits` and `index_limits` must provide
the complete respective key sets in `mirror.py`; their individual values may only
decrease from its defaults. Default page caps reserve 484 MiB conservatively for
two databases, possible journals and bounded metadata; they do not immediately
allocate that amount. A lower output cap requires correspondingly lower page caps.
Preparation CPU, structural parsing, copies and indexing are real charged costs.

Using independently approved paths/pins, invoke the fixed entrypoint:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\inert-mirror\run.py' prepare `
  --source-root 'C:\commons-investigator-source' `
  --source-manifest-sha256 '1bc43d4c9896476443d0d6aab95015db7af32bc46a04cfb1624a5c40e638feb9' `
  --python-runtime 'C:\tools\Python314' `
  --entry-sha256 'APPROVED_RUN_PY_SHA256' --helper-sha256 'APPROVED_MIRROR_PY_SHA256' `
  --request 'C:\commons-requests\prepare-01.json' --request-sha256 'EXACT_REQUEST_SHA256' `
  --diagnostics 'C:\commons-diagnostics\prepare-01' `
  --wall-seconds 120 --cpu-seconds 60 --memory-mib 768 --active-processes 1 `
  --stdout-bytes 1048576 --stderr-bytes 1048576
```

All paths are absolute ordinary nonredirected Windows paths. Output and diagnostic
leaves must not exist; their parents must exist. They must be disjoint from each
other, approved source/runtime/helper/request locations and the input bundle.
The example budgets are choices, not a promise every allowed bundle fits them.
No retry or budget renewal occurs after refusal.

The worker verifies exact bytes, aggregate syntax bounds, target identities and
syntactic import closure against the fixed basis, then prepares fresh inert stores
and a `DESCRIPTOR.json`. This does **not** verify Lean typing or complete generated
inductive groups. False but structurally valid mathematics may be mirrored.
Missing/conflicting imports, cycles or malformed data refuse this profile; that
refusal is not a mathematical falsity judgment. Existing state is never overwritten.

## Understand completion before serving

The worker descriptor is explicitly `PREPARED_DATA_NOT_SUPERVISED_READY`.
It cannot authorize service. After zero exit, reaped child, closed Job, zero active/
terminated processes and no cleanup errors, the parent verifies exact reports and
descriptor binding. It writes all diagnostic reports and a checked temporary
`READY-PENDING.json`, then uses a nonoverwriting rename to `READY.json` as the
readiness commit point. There are no further report writes/readback checks after
that rename. Pending files and a preseal RUN report are not completion authority.

Normal completion returns exit zero and `INERT_MIRROR_PREPARE_COMPLETE`, with the
exact READY digest. `RUN.json` deliberately remains an `ok:false` precommit
eligibility record; it is not a second terminal success signal. The parent READY
seal binds descriptor, request, software and supervised outcome hashes. It is a
protected local workflow marker, **not a cryptographic custody certificate or
mathematical warrant**. Do not construct it manually or use private `--worker`.

If final stdout is lost or the parent is interrupted around rename, the outcome
may already be committed. Preserve everything and inspect the exact READY seal
and its bound reports; do not assume rollback or automatically repeat preparation.
Failure before promotion leaves partial data/pending reports nonready. Serving
requires the operator's exact selected READY and descriptor hashes, not existence
of an arbitrary file named READY or a worker's successful-looking message.

## Serve one finite lease

Use a fresh operator request:

```json
{
  "schema": "DMKN_INERT_MIRROR_SERVE_REQUEST_V1",
  "prepared_directory": "C:/commons-data/mirror-01",
  "descriptor_sha256": "ACTUAL_DESCRIPTOR_SHA256",
  "ready_sha256": "ACTUAL_PARENT_READY_SHA256",
  "config": {
    "host": "127.0.0.1", "port": 0, "tls": null,
    "lease_seconds": 30, "cleanup_seconds": 10,
    "share_all_custody": true, "exclusive": true,
    "limits": {"max_connections": 2, "max_requests": 64,
               "max_reply_bytes": 16777216, "operation_ms": 1000}
  }
}
```

Use the same command shape with action `serve`, the new request/hash and fresh
diagnostic leaf. Allow time for source bootstrap, the lease and cleanup inside
the one original allocation; e.g. 90 wall seconds for the 30-second example is
an allowance, not a latency guarantee. CPU/memory/log caps stay explicit.
`SERVICE-READY.json` reports the actual endpoint while the worker is live;
port zero is ephemeral and does not advertise the endpoint to other participants.
Select a nonzero approved port when stable explicit contacts are required.

Remote binding requires the existing TLS configuration with `cert_file`,
`cert_sha256`, `key_file`, `key_sha256`; independently approve exposure and protect
the key. No remote exposure is selected by this local source implementation.
Attempt/reply exhaustion can end useful service before lease expiry; a lease is
not a fairness or availability guarantee. Request/header/TLS costs remain distinct
from reply-payload quotas. Holders may disappear and global search is incomplete.

Serve verifies the exact local READY/descriptor, unchanged support selection and
prepared snapshot/store status, holds the prepared state's exclusive lock, opens
the existing stores read-only for queries, and closes Provider/stores at the end.
Require exit zero, `INERT_MIRROR_SERVE_COMPLETE`, result `LEASE_FINISHED`,
`quiescent:true`, empty cleanup errors and clean outer supervision. A live READY
notice alone is not completion. Preserve uncertainty/locks after failures; do not
delete locks or edit databases to force a restart. Each later finite lease is a
separately authorized operation with fresh diagnostics, not automatic renewal.

## Embedding boundary

`load_support(source_root, check_budget)` validates the same fixed source map
and returns exact shared codec/module objects, `.api`, `.inventory_raw` and source
metadata. It is intended once per fresh controlled process and rejects module
collisions. Direct helper calls need caller-owned containment and do not create
the public parent's READY seal. Neither this source API nor successful hosting
changes the receiving investigator's existing mathematical acceptance rules.
