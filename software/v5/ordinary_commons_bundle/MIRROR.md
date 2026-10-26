# Storage-only mathematical mirror

An operator can retain one explicitly approved finite mathematical bundle and
serve its exact bytes plus selected formal search records. This companion needs
approved **Windows x86-64 and Python 3.14.6**, not Lean, native package building,
a mathematical owner/catalog or a certificate. It checks data structure and
identity, **not mathematical truth**. Every consumer independently checks what
it uses. Copying a known complete bundle is simpler when no search service is
needed. The mirror neither invents mathematics nor automatically replicates it.

The [current root README](../../../README.md) controls source approval, licensing
and current selection. Work remains local and unpublished; the license is
undecided. No remote exposure or continuous service is selected by the examples.
Each prepare/serve invocation is an explicit finite operation, not a daemon or
an automatically renewed lease.

## Source layout and execution boundary

Use this folder's repaired `run.py`, `mirror.py` and `SOURCES.json` inside the
same verified commons extraction. Set `--source-root` to that extraction's root.
Do not fetch an older sidecar or execute the failed predecessor helper.

| File | Exact SHA-256 |
|---|---|
| `run.py` | `cef9b50b8a98231e7f9e60afb0f9021b7d5f495266b2320957076ab4e1c55bd0` |
| `mirror.py` | `86d0716d51f55040233bf2572c74bfdd7307a203a241ef2815c74f7958458920` |
| `SOURCES.json` | `1bc43d4c9896476443d0d6aab95015db7af32bc46a04cfb1624a5c40e638feb9` |

The loader checks 27 selected pure source/data dependencies, totaling 1,212,995
bytes, including the fixed inventory. These remain at their original paths.
It also checks the retained root `INVESTIGATOR-SOURCE-MANIFEST.json` digest
`65edf28f928d4100346a4603fe508252ddc6393950c34a373fbb33da4c6491f5`.
That historical manifest associates the unchanged selected dependencies; it
does not describe the larger root's census. Verify the full source using the
current `COMMONS-SOURCE-MANIFEST.json` and utility from the root README.

Independently approve executable sources and runtime. Pins provided alongside
untrusted code do not authenticate them. The launcher uses `-I -S -B`, checks its
selected python.exe/python314.dll/python3.dll and loads only selected source
modules. The normal Python stdlib, SQLite and TLS dependencies must be present;
not every runtime/OS dependency is attested. Windows Jobs constrain resources,
not filesystem/network permissions. Protect source, inputs and prepared state
against unauthorized local modification. Never execute received peer source.

## Prepare the disclosed data

Select an existing `DMKN_ORDINARY_BASELINE_BUNDLE_V1` directory, its independently
approved `manifest.json` SHA-256 and actual `{name, unit_id, export_id}` target
rows. The manifest describes the entire disclosed bundle. Targets restrict
indexing only: whole units, dependencies and supplied sibling declarations
remain addressable. Approve that entire disclosure.

Create a fresh request in this form. Hash/name placeholders are not executable
identities; copy exact target rows from the real data handoff. The illustrated
structured name spells `A` only to show the encoding.

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

Limits may only decrease. Optional `custody_limits` and `index_limits` must include
their complete key sets from `mirror.py` with no value above its default. Default
page limits conservatively reserve 484 MiB for two databases, possible journals
and metadata; they do not immediately allocate that amount. Lower output limits
need correspondingly lower page caps. Parsing, copying and indexing have costs.

Invoke the fixed parent with independently selected actual paths and input hash:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_inert_mirror02\run.py' prepare `
  --source-root 'C:\commons-source' `
  --source-manifest-sha256 '1bc43d4c9896476443d0d6aab95015db7af32bc46a04cfb1624a5c40e638feb9' `
  --python-runtime 'C:\tools\Python314' `
  --entry-sha256 'cef9b50b8a98231e7f9e60afb0f9021b7d5f495266b2320957076ab4e1c55bd0' `
  --helper-sha256 '86d0716d51f55040233bf2572c74bfdd7307a203a241ef2815c74f7958458920' `
  --request 'C:\commons-requests\prepare-01.json' --request-sha256 'EXACT_REQUEST_SHA256' `
  --diagnostics 'C:\commons-diagnostics\prepare-01' `
  --wall-seconds 120 --cpu-seconds 60 --memory-mib 768 --active-processes 1 `
  --stdout-bytes 1048576 --stderr-bytes 1048576
```

Here `--source-manifest-sha256` means adjacent **SOURCES.json**, not either
root distribution manifest. The hashes select already approved software, not
approval by themselves. Use absolute ordinary nonredirected Windows paths.
Output/diagnostic leaves must be absent with existing parents, disjoint from one
another and source, runtime, helper, request and input-bundle locations. Example
budgets are allowances, not promises that every permitted bundle fits.

The worker verifies exact bytes, aggregate syntax limits, targets and syntactic
import closure against the fixed basis, then prepares fresh inert stores and
`DESCRIPTOR.json`. It does not check Lean typing or complete generated inductive
groups. False but structurally valid mathematics may be hosted. Missing imports,
conflicts, cycles or malformed data refuse; refusal is not a falsity proof.
No prior state is overwritten and no failed allocation is automatically renewed.

## Readiness is a parent commit, not a worker report

The descriptor initially says `PREPARED_DATA_NOT_SUPERVISED_READY`; it cannot
authorize service. After zero worker exit, reaped child, closed Job, zero active/
terminated processes and no cleanup errors, the parent validates the descriptor
and reports. It writes checked `READY-PENDING.json`, then commits readiness by
nonoverwriting rename to `READY.json`. No further report write/readback follows
that rename. Pending files and successful-looking worker output are insufficient.

Normal completion requires exit zero and `INERT_MIRROR_PREPARE_COMPLETE` with the
exact READY digest. `RUN.json` deliberately remains an `ok:false` precommit
eligibility record, not a second terminal success signal. READY binds descriptor,
request, source and supervision outcomes. It is a protected local workflow seal,
not mathematical authority or a cryptographic availability certificate.
Never construct READY manually or call private `--worker` to bypass the parent.

If stdout is lost or interruption occurs around the rename, readiness may already
be committed. Preserve everything and inspect the exact READY/bound reports;
do not assume rollback or repeat preparation automatically. Earlier failures
leave partial/pending outputs nonready. Select actual READY and descriptor hashes
before serving; their filenames alone convey no authority.

## Serve one finite lease

Create a new request using the actual prepared directory and exact hashes:

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

Use the same parent command with action `serve`, the new request/hash and fresh
diagnostics. Select a wall allowance covering source bootstrap, lease and cleanup;
90 seconds for the illustrated 30-second lease is an allowance, not a latency
guarantee. CPU/memory/log caps remain explicit. While live, `SERVICE-READY.json`
reports the actual endpoint. Port zero is ephemeral and does not advertise a
contact; choose an approved stable port when explicit persistent contacts need it.

Remote binding requires existing TLS fields `cert_file`, `cert_sha256`, `key_file`,
`key_sha256`. Separately approve exposure and protect the key. The local example
does not select remote deployment. Connection/request/reply exhaustion can end
useful service before the lease; request/header/TLS costs differ from reply-byte
quotas. A lease promises neither fairness, global search coverage nor durability.

Serve validates exact READY/descriptor/support and prepared snapshot, holds its
exclusive lock, opens existing stores read-only for queries, and closes Provider/
stores at the end. Require exit zero, `INERT_MIRROR_SERVE_COMPLETE`, result
`LEASE_FINISHED`, `quiescent:true`, empty cleanup errors and clean outer
supervision. A live-ready notice is not terminal completion. Preserve uncertain
state/locks after failure; do not delete locks or edit databases to force restart.
Every later lease requires a new explicit operation and fresh diagnostics.

## Embedded use

`load_support(source_root, check_budget)` validates the same fixed selection and
returns the exact shared codecs, `.api`, `.inventory_raw` and source metadata.
It is intended once per fresh controlled process and rejects module collisions.
Embedded calls need caller-owned containment and do not produce the public
parent's READY seal. Successful storage/search does not change the receiving
investigator's independent mathematical checking obligations.
