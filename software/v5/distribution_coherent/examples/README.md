# Ordinary checked contribution

`contribute.py` is an explicitly trusted local-owner example for the installed
`run` command. It uses existing SDK APIs, not a new network protocol or client.
The local agent chooses the mathematics. The system neither interprets human
intention nor supplies a research agenda.

The sequence is:

```text
one remote query OR exact local packet
  → actual admission → committed semantic import
  → caller's Lean source → untrusted exported packet
  → actual output admission → local custody and formal indexing
```

This is a check-before-index **owner policy**. The underlying network may store
untrusted packets; recipients still independently check what they use.
Publication is not automatic replication, global visibility or permanent
retention. The example produces no new succinct certificate. Native deltas may
retain a bounded unsealed ancestry; this is not a solution to economical
indefinite recursive certification.

## First adoption is separate from contribution

This successor requires the consolidated SDK with `admission.trust`. Before
the first mathematical operation, explicitly adopt its checking support through
the installed `run` entry: derive `RuntimeProfile.support_manifest`, compute
`support_id`, then call `TrustDomain.create` in a fresh persistent policy directory.
The generated installed README and [RUNTIME.md](../RUNTIME.md) give the owner code.
Keep its resulting three-field `trust-domain.json` in caller-controlled files.

Every contribution only calls `TrustDomain.open`, then constructs its runtime
with that exact domain. Missing, changed or withdrawn policy refuses; it never
auto-adopts, clears a withdrawal marker or retries under a new identity. Keep
the policy directory separate from installation, operation trees and the
mathematical workspace. A changed SDK/support identity needs a new deliberate
adoption, not reuse of an old support hash. Serving retained data remains a
separate nonadmitting operation.

The example's author/check/publish sequence is otherwise unchanged. It does not
automatically choose selective pair profiles or drive lazy semantic continuation.
To opt in, supply the new immutable paired-workspace configuration described in
the installed README; discovery providers/consumers must use that same profile.
Use `workspace.adapter.compile_query(specs)` when constructing route keys.

## Inputs and names

The example parameters have exactly these fields:

| Field | Meaning |
|---|---|
| `schema` | `DMKN_V5_CONTRIBUTE_EXAMPLE_WITHDRAWAL_V1` |
| `runtime_adoption`, `foundation` | The two installed-role singleton markers below |
| `trust_domain` | Existing owner adoption: exact `{directory, domain_id, support_id}` |
| `workspace_path`, `workspace_config`, `create_workspace` | Persistent validated/evidence workspace and explicit create/reopen choice |
| `operation_limits` | One finite existing workspace grant |
| `input` | One of the two forms below |
| `source` | Absolute UTF-8 Lean source pin `{path, bytes, sha256}`, at most 65,536 bytes |
| `roots` | One to 64 distinct formal names to capture |
| `export_names` | One to 64 distinct local declaration names to index |
| `author_limits` | `{cpu_seconds, wall_seconds, memory_mib}` |
| `admission_limits` | `{native_cpu_seconds, receipt_cpu_seconds, wall_seconds, memory_mib}` |

Local input:

```json
{
  "mode": "local-packet",
  "module": "<exact expected ModuleID>",
  "packet": {"path": "<absolute file>", "bytes": 123, "sha256": "<exact SHA-256>"}
}
```

The expected module, packet hash and structural store checks are **not** trust
in the theorem. Real admission is still required. The local path imports the
available semantics of all members of this one packet, not an entire library.
If those semantics are insufficient, it reports the demands without retrying.

Remote input:

```json
{"mode": "remote", "query": "<the existing remote-reader query object>"}
```

Here `query` is an object, not the explanatory string above. Its exact fields
are `contacts`, `egress_policy`, `specs`, `search_limits`,
`contact_lifetime_ms`, `selection`, `offer`, `page`, `packets`, and `admission`,
as documented in [REMOTE-READER.md](../REMOTE-READER.md). It performs one explicit
provider/page/result selection and does not retry. Remote acquisition uses
`query.admission`; new-output checking uses the top-level `admission_limits`.
Local input and output both use the top-level admission limits.

Lean names are arrays of tagged string or natural-number components:
`[["s", "MyNamespace"], ["s", "newTheorem"]]`, not
`"MyNamespace.newTheorem"`. A natural-number component has the form `["n", 3]`.
Use the installed SDK's `modules.codec.relocated_name(module, relative_name)`
for imported declarations. The corresponding source namespace is determined
by those exact formal components, not an arbitrary service label.
The supplied source must refer to the actually imported mathematics. This
fixed-source example does not invent names or synthesize a proof after search.
A local agent may instead call the same SDK directly and construct its source
while its client remains live.

## Complete local request construction

The following is a **caller-side example**, not an automatically executed
installer or additional supervisor. Start with an independently adopted release
digest and trusted interpreter/script; run its full `verify` first. Then save
this snippet as caller tooling, replace the explicit owner choices, and run it
with the installed Python using `-I -S -B`. Its SDK import uses only that already
adopted installation. Hashing locally chosen inputs binds a request to bytes;
it does not authenticate the bootstrap or prove those inputs mathematically.

Keep the installation, caller files, fresh operation directories and mutable
mathematical workspace separate. Their parents must already exist. Copy this
reviewed `contribute.py` into the caller directory; do not modify an existing
immutable release to add it. The request uses the ordinary owner source map.

```python
import hashlib
import json
from pathlib import Path
import sys

INSTALL = Path(r"C:\MathCommons\release")      # adopted installation
CALLER = Path(r"C:\MathCommons\caller")        # contribute.py, proof.lean, input.packet
OPERATIONS = Path(r"C:\MathCommons\operations")
STATE = Path(r"C:\MathCommons\math-workspace") # fresh for create_workspace=True
REQUEST = CALLER / "contribution-request.json" # fresh
TRUST_CONFIGURATION = CALLER / "trust-domain.json" # retained explicit adoption
EXPECTED_MODULE = "<replace with exact input ModuleID>"
ROOTS = [[["s", "MyNamespace"], ["s", "newTheorem"]]]  # match proof.lean
EXPORTS = ROOTS
MiB = 1024**2

# Import configuration vocabulary from the explicitly adopted release, not
# a downloaded plugin or unselected source tree.
sys.path[:0] = [str(INSTALL/"sdk/v5"), str(INSTALL/"sdk/portable")]
from evidence_network.custody import public_profile

release = json.loads((INSTALL/"V5-RELEASE.json").read_bytes())
trust_domain = json.loads(TRUST_CONFIGURATION.read_bytes())

def pin(path):
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest()}

workspace = {
    "schema": "DMKN_V5_CLIENT_EVIDENCE_WORKSPACE_V1",
    "wire_profile": public_profile(release["aggregate_image"]),
    "module_limits": {"modules": 32, "groups": 128, "declarations": 512,
        "bodies": 256, "logical_bytes": 32*MiB, "db_pages": 16384},
    "packet_limits": {"packets": 4, "offers": 8, "offers_per_module": 2,
        "packet_bytes": 16*MiB, "logical_bytes": 64*MiB, "db_pages": 32768},
    "index_limits": {"max_objects": 128, "max_postings": 8192,
        "max_features": 1024, "max_snapshots": 256,
        "max_logical_bytes": 32*MiB, "max_db_pages": 16384},
    "packet_envelope": {"packet_bytes": 16*MiB, "receipt_bytes": 8*MiB,
        "witness_bytes": 16*MiB, "claims": 1, "frontiers": 1, "deltas": 2,
        "edges": 3, "openings": 4096, "bodies": 8192, "rows": 250000,
        "nodes": 500000, "depth": 128, "rank": 2**64-1},
    "terminal_receipt_bytes": 8*MiB,
    "max_operations": 4, "max_report_bytes": MiB, "ledger_pages": 1024
}
operation = {
    "wall_seconds": 180, "controller_cpu_seconds": 90,
    "calls": 64, "input_bytes": 16*MiB, "worker_cpu_seconds": 80,
    "output_bytes": 128*MiB, "output_entries": 1024,
    "acquisition": {"requests": 1, "reply_bytes": MiB, "verify_attempts": 2,
        "verification_input_bytes": 4*MiB, "worker_cpu_seconds": 50},
    "imports": {"max_sources": 2, "max_members": 4, "max_receipts": 1,
        "max_calls": 4096, "submitted_bytes": 16*MiB, "data_bytes": 4*MiB}
}
owner = pin(CALLER/"contribute.py")
request = {
    "schema": "DMKN_V5_INSTALLED_REQUEST_V1",
    "name": "contribution-01", "workspace_root": str(OPERATIONS),
    "owner": {"root": str(CALLER), "entry": "contribute.py",
        "sources": {"contribute.py": {k: owner[k] for k in ("bytes", "sha256")}}},
    "runtime_mode": "aggregate",
    "limits": {"cpu_seconds": 150, "wall_seconds": 240,
        "memory_mib": 1024, "active_processes": 4,
        "stdout_bytes": MiB, "stderr_bytes": MiB},
    "output_limits": {"bytes": 256*MiB, "entries": 4096},
    "parameters": {
        "schema": "DMKN_V5_CONTRIBUTE_EXAMPLE_WITHDRAWAL_V1",
        "runtime_adoption": {"$installed": "runtime_adoption"},
        "foundation": {"$installed": "foundation"},
        "trust_domain": trust_domain,
        "workspace_path": str(STATE), "workspace_config": workspace,
        "create_workspace": True, "operation_limits": operation,
        "input": {"mode": "local-packet", "module": EXPECTED_MODULE,
                  "packet": pin(CALLER/"input.packet")},
        "source": pin(CALLER/"proof.lean"), "roots": ROOTS, "export_names": EXPORTS,
        "author_limits": {"cpu_seconds": 30, "wall_seconds": 60, "memory_mib": 768},
        "admission_limits": {"native_cpu_seconds": 10, "receipt_cpu_seconds": 10,
                            "wall_seconds": 60, "memory_mib": 512}
    }
}
raw = json.dumps(request, sort_keys=True, separators=(",", ":")).encode("utf-8")
with REQUEST.open("xb") as stream:
    stream.write(raw)
print(str(REQUEST), hashlib.sha256(raw).hexdigest())
```

These are small example quotas, not guaranteed resources for arbitrary
mathematics. The envelope must fit both the input and produced packet, including
their actual dependency graph. The example deliberately does not enlarge limits
or retry after refusal. For remote input, reserve additional requests and bytes:
the entire `search_limits` request/byte allowance is prepaid against acquisition,
then discovery resolution and packet acquisition spend further allowance.
An isolated local input needs no network request, but the existing grant schema
still requires positive request/reply caps.

The 80 worker-CPU grant above assigns 50 to admission/acquisition and the
remaining 30 to source preparation; it does not grant 80 to each worker.
The output admission shares that same acquisition allocation with input
admission. These explicit suballocations and original deadline are not renewed.
The outer Job remains the hard CPU/memory/process bound. There is no
hostile-code sandbox claim: owner code and this caller-selected Lean source
are trusted local inputs.

Launch from any working directory with absolute paths:

```text
INSTALL/base/receiver/runtime/python/python.exe -I -S -B INSTALL/distribution.py launch RELEASE_SHA run REQUEST.json REQUEST_SHA
```

## Outcomes, persistence and further use

Read `OPERATIONS/contribution-01/work/contribution-result.json`.
The path is inside the run's actual `location_workspace`; the installed
launcher uses `work` for it. Exit zero/top-level `COMPLETED` means that the
bounded operation and cleanup completed, **not** that a contribution exists.

- `COMPLETED` and `outcome=CONTRIBUTED`: the output was freshly admitted and
  locally published. `checked_output` describes the exact checked journal;
  `publication` identifies the local publication and index snapshot. This
  does not assert novelty, mathematical importance or a net resource benefit.
- `COMPLETED` and `outcome=NOT_CONTRIBUTED`: the selected remote result was
  absent/refused, or input/preparation needs semantic data. There was no
  automatic retry, fallback or proof-budget renewal.
- `FAILED`: execution or cleanup failed. A partial publication may already
  exist; preserve the report and workspace. A missing result may indicate an
  earlier configuration/refusal or enclosing-Job termination. Inspect the
  launch/boot records as well; never infer success from partial output.

All saved JSON is operational evidence, not a warrant that may be reloaded as
mathematical authority. `mathematical_acceptance=false` on the report denotes
that distinction; actual checking is performed by the live owners.
Input packets can remain in untrusted custody even if checking fails, but this
example does not index its new output before successful admission.

After clean closure, the existing finite `serve` command can expose the retained
workspace. Use `mode="validated"` and the identical workspace configuration.
Another owner may reopen with `create_workspace=false`, within the originally
selected quotas and operation count; select a fresh run/request name. There is
no in-place quota migration here. Do not delete evidence or automatically replay
a failed operation. Serving does not reconstitute old warrants: recipients must
again obtain actual acceptance under their own policy.

This source example and its documentation do not themselves establish executed
relocated authoring, positive full-cost growth, independent deployment, or the
completion of v5. Those claims require their own applicable evidence.
