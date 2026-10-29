# Python-only inert mathematical hosting

This role stores disclosed mathematical bytes, derives selected search records,
and serves them for a finite session. Recipients independently check mathematics.
It creates no mathematical owner and requires no Lean installation, native helper,
seed inventory or proof checking. Initial support is Windows x64 with the selected
Python 3.14.6 distribution. Source-stage guide: use only a subsequently approved
distribution and its externally supplied SOURCES.json SHA-256.

## Install the selected role

Keep the distribution's `run.py`, `support.py`, `host_core.py`, `SOURCES.json`,
`support/` and `supervisor/` together. The profile pins 28 runtime source files;
the independent manifest pin binds that selection without a self-hash cycle.
The manifest's `source` fields are build provenance, never runtime import paths.
The selected Python executable and two DLLs are also pinned. Python's standard
library, SQLite/TLS support and Windows remain required trusted dependencies;
those three pins are not a complete Python distribution or hermetic attestation.

Use approved, protected software/runtime directories. State, configs, bundles,
operation output and diagnostics use canonical absolute local paths without
symlinks, reparse points or hardlinked files. Keep state/output/diagnostics separate
from each other and software/runtime/input trees. Fresh directories need an existing
ordinary parent. Inputs are operator-approved local data; no input selects code.

Use a fresh host root. Existing full-package hosts and mirror snapshots retain
their old source profiles; the new role does not migrate or relabel their seals.
Choose `init` plus later `append` for a growing collection, or `prepare` for one
fixed generation. Both preserve the existing evidence/preview/discovery wire format.

## Initialize a growing host

Save UTF-8 JSON without a BOM at an approved config path. This complete example
chooses finite cumulative storage limits; adjust them deliberately for the host.

```json
{
  "schema": "DMKN_INCREMENTAL_HOST_INIT_V1",
  "custody_limits": {
    "objects": 256, "exports": 2048,
    "logical_bytes": 16777216, "db_pages": 4096
  },
  "index_limits": {
    "max_objects": 256, "max_postings": 32768, "max_features": 8192,
    "max_snapshots": 257, "max_logical_bytes": 16777216, "max_db_pages": 4096
  },
  "partial_publication": true
}
```

Set these values from the approved distribution and your selected paths. Obtain
the profile pin from the approved release record; merely hashing unknown local
software does not approve it. The config hash binds your explicit local selection.

```powershell
$hostPackage = 'C:\approved-inert-host'
$hostPythonRoot = 'C:\approved-python'
$hostPython = "$hostPythonRoot\python.exe"
$hostProfile = 'REPLACE_WITH_APPROVED_SOURCES_SHA256'
$hostRoot = 'C:\commons-work\inert-host01'
$hostConfig = 'C:\commons-work\init-host.json'
$hostConfigHash = (Get-FileHash -LiteralPath $hostConfig -Algorithm SHA256).Hash.ToLower()

& $hostPython -I -S -B "$hostPackage\run.py" init `
  --profile-sha256 $hostProfile --python-runtime $hostPythonRoot `
  --host-root $hostRoot --config $hostConfig --config-sha256 $hostConfigHash `
  --output 'C:\commons-work\init-output01' --diagnostics 'C:\commons-work\init-launch01' `
  --wall-seconds 90 --cpu-seconds 30 --memory-mib 768 --active-processes 1 `
  --stdout-bytes 1048576 --stderr-bytes 1048576
```

Require a successful final launcher result and inspect both `output/RESULT.json`
and `diagnostics/SUPERVISION.json`. Success leaves a permanent marker, `host.lock`,
`custody/`, `index/` and `HOST.json`. Save the exact HOST.json hash after successful
closure. For an incremental host it identifies fixed configuration and software,
not the current contents. Later snapshots/counts are reported separately.

## Append an approved bundle

Select a current baseline bundle, including its manifest and exact `units/` files.
Existing contribution handoff output can supply this bundle and target rows.
No full earlier-corpus export is required. Imports may refer to material absent
from this bundle or host; hosting does not claim mathematical dependency closure.
Every supplied unit is retained, including support units that are not indexed.

The following hashes and structured target name are illustrative placeholders;
replace the complete target row with an actual selected producer/return record.

```json
{
  "schema": "DMKN_INCREMENTAL_HOST_APPEND_V1",
  "bundle_directory": "C:\\commons-work\\selected-bundle",
  "manifest": {
    "path": "C:\\commons-work\\selected-bundle\\manifest.json",
    "sha256": "REPLACE_WITH_EXACT_MANIFEST_SHA256"
  },
  "targets": [{
    "name": [[0, {"$bytes": [69,120,97,109,112,108,101]}], [0, {"$bytes": [114]}]],
    "export_id": "REPLACE_WITH_EXACT_EXPORT_ID",
    "unit_id": "REPLACE_WITH_EXACT_UNIT_ID"
  }],
  "share_all_bundle": true,
  "allow_partial_publication": true
}
```

Select 1 through 64 unique targets per call, each present in the supplied bundle.
This is a per-call limit; earlier indexed targets remain. Optional `bundle_limits`
may lower the current finite defaults, for example `max_units`, `max_bytes`,
`max_batch_units` and `max_batch_bytes`. Cumulative custody/index limits remain
those fixed at initialization. Approval covers all bundle bytes and generated
locators, not only indexed target declarations.

Wait for the prior operation and its children to close. Use fresh output and
diagnostics directories for every call and the same approved software profile.

```powershell
$hostSealHash = (Get-FileHash -LiteralPath "$hostRoot\HOST.json" -Algorithm SHA256).Hash.ToLower()
$hostConfig = 'C:\commons-work\append-host.json'
$hostConfigHash = (Get-FileHash -LiteralPath $hostConfig -Algorithm SHA256).Hash.ToLower()
& $hostPython -I -S -B "$hostPackage\run.py" append `
  --profile-sha256 $hostProfile --python-runtime $hostPythonRoot `
  --host-root $hostRoot --host-sha256 $hostSealHash `
  --config $hostConfig --config-sha256 $hostConfigHash `
  --output 'C:\commons-work\append-output01' --diagnostics 'C:\commons-work\append-launch01' `
  --wall-seconds 90 --cpu-seconds 30 --memory-mib 768 --active-processes 1 `
  --stdout-bytes 1048576 --stderr-bytes 1048576
```

Custody commits precede previews; previews precede index references. A failed
append may leave unindexed units/previews or a valid indexed prefix. Once all
processes close, the host can serve committed content without claiming that the
failed append completed. Existing identical data is reusable; conflicting bytes
or capacity exhaustion refuse. Any retry is a separately selected, funded call.

## Serve a finite session

Both incremental hosts and static prepared generations use this config shape:

```json
{
  "schema": "DMKN_DEDICATED_HOST_SERVE_V1",
  "host": "127.0.0.1", "port": 0, "tls": null,
  "lease_seconds": 60, "cleanup_seconds": 15,
  "limits": {
    "max_connections": 4, "max_requests": 32,
    "max_reply_bytes": 8388608, "operation_ms": 2000
  },
  "share_all_custody": true, "exclusive": true
}
```

Use the append command shape with operation `serve`, a pinned serve config,
the retained host root/descriptor pin and fresh output/diagnostics paths. Give
the whole operation enough wall time for startup, lease and cleanup; 120 seconds
fits this illustrative 60-second lease plus 15-second cleanup reserve. The actual
endpoint is written to that invocation's `output/READY.json`; port 0 requests an
ephemeral local port. Run clients separately during the session. An old READY
file never proves a listener is still running. Existing find/preview/inspect and
evidence acquisition clients retain the same protocol and checking obligations.

Outside loopback, `tls` is required and has exactly `cert_file`, `cert_sha256`,
`key_file`, `key_sha256`, using explicit selected absolute paths and hashes.
Only the approved custody/index is shared; authoring/contact maps are not served.
After the lease require clean provider, index, custody, lock and whole-Job closure.
The launcher sanitizes the child environment and adds only the selected Python
paths. No service renewal, detached worker or background daemon is created.

## Prepare a fixed generation instead

Use the append config's bundle/manifest/targets and optional bundle limits, but
change `schema` to `DMKN_DEDICATED_HOST_PREPARE_V1`, remove
`allow_partial_publication`, and add the explicit `custody_limits` and
`index_limits` objects shown for init. Keep `share_all_bundle: true`.
Call operation `prepare` using the init command shape, a fresh host root and the
pinned prepare config. Omit `--host-sha256` for both init and prepare; it is required
for append and serve. A successful prepare seals the fixed generation's content.
Serve it normally, but append is available only for an initialized incremental host.

## Limits and retained outcomes

Every invocation explicitly supplies wall 35–3600 seconds, worker CPU 4–600 seconds,
private-memory limit 1–8192 MiB, active processes 1–8, and each log cap 1–8388608
bytes. `--cpu-seconds` bounds cumulative CPU in the worker's Job. It is not a hard
aggregate cap over parent plus worker. The trusted parent separately checks
`min(60, cpu-seconds)` CPU seconds cooperatively and reports its measured CPU;
accounting totals must include that cost once. Worker Job limits use the existing
supervisor; polling can overshoot and such operations do not pass. The original
wall deadline includes parent setup and passes to the child unchanged. The
standalone wrapper has cooperative limits, not its own hard Job containment.
File/record/SQLite limits are logical bounds, not a disk quota.

Do not invoke hidden worker flags directly. Source/runtime/config bytes are
rechecked before successful completion. Failure preserves all partial state and
reports; it does not roll back committed additions. Never delete or recreate the
permanent host lock or marker to bypass a refusal. Failed initialization without
a final descriptor needs a fresh root. Host commands serialize through the lock;
same-user arbitrary code remains outside the protected-software/storage premise.
This role does not itself establish remote deployment, independent failure
tolerance, host-level hostile-code isolation or mathematical correctness.
