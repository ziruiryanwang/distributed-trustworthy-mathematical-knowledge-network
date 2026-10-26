# Bounded selected export companion

Source implementation, not yet executed or qualified. Root selection is
`research/cycles/v5-2026-10-26-local-discovery/SELECTIVE-EXPORT-SELECTION.md`.
The revised inert-only selection supersedes the earlier owner-backed option in
`SELECTIVE-EXPORT-INTEGRATION-CHOICE.md`. No frozen package, native implementation,
owner, anchor-support identity or existing source file is changed.

## Public call

Run approved `export.py` with supported Python 3.14.6 using `-I -S -B`. All
options are explicit:

```text
export.py --package ABS --profile-sha256 HEX --python-runtime ABS
          --entry-sha256 HEX --helper-sha256 HEX
          --request ABS --request-sha256 HEX --diagnostics FRESH_ABS
          --wall-seconds N --cpu-seconds N --memory-mib N
          --active-processes 1 --stdout-bytes N --stderr-bytes N
```

`entry-sha256` selects the approved entry source; `helper-sha256` selects its
fixed sibling `selected_export.py`. Neither permits a request-selected command,
source import path, shell or executable. Approval of these source files and the
package/Python/OS is a premise; self-hashing is not proof that code is safe.

Maximum limits are 600 wall seconds, 600 Job CPU seconds, 2048 MiB private
commitment, one active worker, and 1 MiB per output log. Minimum wall/CPU values
are 5 seconds/1 second. These are finite upper ceilings, not suggested defaults.
The companion does not introduce new memory-heavy work, grant renewal or retry.
CPU/private-commitment limits apply to the worker Job, not a combined
parent-plus-worker cap. Parent CPU is separately cooperatively checked and
reported; parent memory is outside the Job. The original wall deadline covers
setup, the worker and final output verification. Limits are not a hostile-code
sandbox or a hard disk quota.

The request is UTF-8 JSON at most 1 MiB with exactly these fields:

```json
{
  "schema": "DMKN_SELECTED_INERT_EXPORT_REQUEST_V1",
  "custody": "ABSOLUTE_EXISTING_CUSTODY_DIRECTORY",
  "targets": [{"name": ["structured-name-parts"], "export_id": "HEX", "unit_id": "HEX"}],
  "output": "ABSOLUTE_FRESH_OUTPUT_DIRECTORY",
  "custody_limits": {"objects": 1, "exports": 1, "logical_bytes": 1024, "db_pages": 256},
  "limits": {"units": 1024, "bytes": 67108864, "nodes": 2097152,
    "names": 65536, "edges": 262144, "locator_reads": 65536,
    "locator_bytes": 67108864, "output_bytes": 71303168}
}
```

The name/HEX/path placeholders are schematic, not valid test data. Use the
actual portable structured Lean name and identities. `custody_limits` must
exactly match the selected store's existing configuration, not these illustrative
minimum values. Export limits may be lowered; helper validation is authoritative
for their finite syntax bounds. No catalog, store ID or parent root is requested.

## Selected-code boundary

The parent first verifies the selected entry and the package's unchanged
`run.py` source (SHA-256
`47a2b63c73f1bd8346c5881c6d6a76abac86d33aa8e55bfc19bf3359ea924a39`).
That is the default contact-federation launcher source, not its older predecessor.
It reuses only pinned `bind_support`, path/byte helpers, `load_supervision` and
operational closure checks. The selected PROFILE commits INSTALLATION metadata
and named Python/supervisor files. No full package loader, owner state or Lean
installation is opened. A Lean runtime path is not required.

Inside the one fixed worker, exactly seven existing pure modules are loaded
from individually source-pinned package roles: `ordinary_evidence`,
`ordinary_semantics`, `portable_evidence`, `portable_candidate`,
`baseline_bundle`, `ordinary_preview`, and `portable_preview`. The exact fixed
foundation inventory is also pinned. Imports are explicitly ordered and cannot
be redirected through request data or the working directory. The approved
helper receives `E,S,PE,B,PP` as one API object. Existing source pins in export.py
are compatibility requirements; the caller still selects the actual PROFILE.

The parent does not invoke the old launcher's operation parser or silently add
an `owner` operation. It calls the unchanged Job supervisor for this one fixed
child action. The inherited environment is sanitized and its PATH contains only
the selected Python directories. No native checker/compiler/Lake or network is
launched. This is process/resource containment, not a hostile-local-code sandbox.

## Read/write and completion contract

Input custody is read by the helper with the selected read-only SQLite profile,
not via the read/write OrdinaryStore or mathematical catalog. All targets and
required complete dependencies remain inert and may be mathematically false.
Exact closure/basis checks establish transferable data consistency only.

The helper exports `manifest.json`, `units/<unit_id>.json` and `RESULT.json`
under one fresh output directory. The manifest is the existing baseline format.
The parent independently rechecks finite file lengths/hashes, exact output
census and the result/manifest bindings after the worker has cleanly exited.
Use existing `owner intake-baseline` for actual receiver-local admission.

Diagnostics contain `LAUNCH.json`, the supervisor's `child/` evidence,
`SUPERVISION.json`, fresh `WORKER.json`, and terminal `RUN.json`. Completion
requires worker exit zero, reaped direct child, closed Job, no termination,
zero active/terminated processes, no cleanup errors, exact input/report/output
bindings, and remaining original allowance. A helper RESULT or direct private
`--worker` invocation alone does not establish supervised completion. The
worker labels its own report `supervised_completion:false` even on success.

Failure preserves partial files and diagnostics. It does not authorize deletion,
automatic retry, database repair or journal recovery. Read snapshots can delay
DELETE-mode writer commits until closed; finite budgets bound this operation.
The output cannot overlap custody, package, Python, companion source, selected
request or diagnostics. Protected stable files and the supported OS/SQLite
implementation remain explicit premises.

Exporting this closure does not assert previous acceptance, avoid cold proof
checking, transfer a catalog warrant or make the commons final-v5 complete.
