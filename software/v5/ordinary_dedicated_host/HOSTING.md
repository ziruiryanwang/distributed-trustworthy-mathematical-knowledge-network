# Host mathematical evidence without running a mathematical owner

Source-stage walkthrough, 2026-10-28. Use only the subsequently approved dedicated
host package and its exact PROFILE hash. This document does not claim an executed
deployment or authorize publication. Windows and the package's selected Python
and Lean runtime attachments remain required; no Lean worker or grounding runs.

A host stores inert mathematical units and an index of selected targets. Each
recipient decides what to acquire and independently checks it. Hosting is neither
mathematical acceptance nor a claim that every dependency is available.

## Prepare a fresh dedicated root

Start with an existing inert baseline bundle: a manifest and its `units/` files.
Select target rows from an exact producer/return record and retain their structured
Lean names, export IDs and unit IDs. Do not point this operation at an existing
owner's custody or copy a live SQLite database.

Create a UTF-8 configuration without a BOM. This complete example intentionally
contains invalid placeholder hashes; replace them with explicit selected values.
The structured name below is `Example.r`, also an illustrative choice.

```json
{
  "schema": "DMKN_DEDICATED_HOST_PREPARE_V1",
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
  "bundle_limits": {
    "max_units": 128,
    "max_bytes": 16777216,
    "max_batch_units": 128,
    "max_batch_bytes": 16777216
  },
  "custody_limits": {
    "objects": 256,
    "exports": 2048,
    "logical_bytes": 16777216,
    "db_pages": 4096
  },
  "index_limits": {
    "max_objects": 256,
    "max_postings": 32768,
    "max_features": 8192,
    "max_snapshots": 257,
    "max_logical_bytes": 16777216,
    "max_db_pages": 4096
  },
  "share_all_bundle": true
}
```

There must be one through 64 targets with unique export IDs, each present in the
selected bundle. Optional `bundle_limits` lowers existing finite defaults; omit
it to use those defaults. Other limits remain explicit. These example limits are
ceilings, not a promise that every selected bundle fits. Approval covers **all
bundle bytes and all generated export locators**, including unindexed declarations.

Choose a fresh host root and fresh operation-output/diagnostics directories, all
outside the bundle and package/runtime trees. Use the public launcher:

```powershell
# Set these to the package/runtimes and hashes explicitly approved for this run.
$hostPython = 'C:\approved-python\python.exe'
$hostPythonRoot = 'C:\approved-python'
$hostLeanRoot = 'C:\approved-lean'
$hostPackage = 'C:\approved-commons-package'
$hostProfile = 'REPLACE_WITH_APPROVED_PROFILE_SHA256'
$hostPrepareConfig = 'C:\commons-work\prepare-host.json'
$hostPrepareHash = (Get-FileHash -LiteralPath $hostPrepareConfig -Algorithm SHA256).Hash.ToLower()

& $hostPython -I -S -B "$hostPackage\run.py" `
  --profile-sha256 $hostProfile --python-runtime $hostPythonRoot --lean-runtime $hostLeanRoot `
  --wall-seconds 90 --cpu-seconds 30 --memory-mib 768 --active-processes 3 `
  --stdout-bytes 1048576 --stderr-bytes 1048576 `
  --diagnostics 'C:\commons-work\prepare-host-launch01' `
  host prepare --host-root 'C:\commons-work\dedicated-host01' `
  --config $hostPrepareConfig --config-sha256 $hostPrepareHash `
  --output 'C:\commons-work\prepare-host-output01'
```

Inspect the launcher outcome and complete host result. Success leaves a permanent
`DMKN-DEDICATED-HOST.json` marker, `host.lock`, fixed `custody/` and `index/`
children, and a final `HOST.json`. The latter records a prepared generation; it
does not mean a network listener exists. Keep all files together. Never remove
the marker or lock to bypass a refusal. Preserve partial roots after failure;
there is no resume, overwrite, refresh or automatic retry operation.

## Serve one finite session

After successful preparation and clean closure, select the exact `HOST.json`
SHA-256. Use a new config, output and diagnostics path. This complete loopback
example requests an ephemeral port; the actual port arrives in the live READY
record. It exposes no internet-facing endpoint.

```json
{
  "schema": "DMKN_DEDICATED_HOST_SERVE_V1",
  "host": "127.0.0.1",
  "port": 0,
  "tls": null,
  "lease_seconds": 60,
  "cleanup_seconds": 15,
  "limits": {
    "max_connections": 4,
    "max_requests": 32,
    "max_reply_bytes": 8388608,
    "operation_ms": 2000
  },
  "share_all_custody": true,
  "exclusive": true
}
```

Non-loopback serving additionally requires the existing TLS object with exactly
`cert_file`, `cert_sha256`, `key_file`, `key_sha256`, each an explicitly selected
absolute path/hash pair. No external deployment is selected by this guide.

```powershell
$hostServeConfig = 'C:\commons-work\serve-host.json'
$hostServeHash = (Get-FileHash -LiteralPath $hostServeConfig -Algorithm SHA256).Hash.ToLower()
$hostSealHash = (Get-FileHash -LiteralPath 'C:\commons-work\dedicated-host01\HOST.json' -Algorithm SHA256).Hash.ToLower()

& $hostPython -I -S -B "$hostPackage\run.py" `
  --profile-sha256 $hostProfile --python-runtime $hostPythonRoot --lean-runtime $hostLeanRoot `
  --wall-seconds 120 --cpu-seconds 30 --memory-mib 768 --active-processes 3 `
  --stdout-bytes 1048576 --stderr-bytes 1048576 `
  --diagnostics 'C:\commons-work\serve-host-launch01' `
  host serve --host-root 'C:\commons-work\dedicated-host01' --host-sha256 $hostSealHash `
  --config $hostServeConfig --config-sha256 $hostServeHash `
  --output 'C:\commons-work\serve-host-output01'
```

Run clients separately during this finite session. Use only the actual
`serve-host-output01/READY.json` for that invocation's endpoint; old readiness
files do not establish a current listener. Existing peer `find`, `preview` and
`inspect` use that endpoint without opening any client mathematical owner.
Actual mathematical use requires the ordinary recipient-checking route later.
After the lease, require provider/index/custody/lock cleanup and the final
launcher outcome. No service renewal happens automatically.

Dedicated operations share a real exclusive lock. Current supported ordinary
commands refuse state/output paths beneath the permanent marker, so contributor
work can continue in separate existing owner directories. This does not isolate
the host from old executables, arbitrary SDK calls or other same-user code that
ignores the convention. Preserve the existing protected-local-storage premise.
The hosted generation has no content-refresh API; SQLite's own reopening or
recovery may still write files. A same-PC copy is not independent failure tolerance.
