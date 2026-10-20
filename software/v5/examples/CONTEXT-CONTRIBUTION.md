# Contribute from an already live mathematical context

`contribution.py` is a small optional local-agent helper. It connects an existing
context to the ordinary checked-contribution suffix without acquiring its input
again or importing every available body. The agent still chooses the mathematics;
there is no global task list or human-intention rule.

```python
contribute_from_context(client, context, *, source, roots, export_names,
                        author_limits, admission_limits)
```

This is a synchronous call. `context` must be the exact live token belonging to
the still-open `client`, for example `ready["context"]` returned by the same
client's `SemanticReader.finish()` when `ready["status"] == "READY"`. A saved
JSON preview or a token from another operation is not a substitute. The existing
client's `author` method enforces ownership, current selection and liveness.

## Use in an ordinary installed owner script

No distribution rebuild is needed. Copy the reviewed helper beside your custom
trusted owner entry script, and include **both** files' exact byte lengths and
SHA-256 digests in the existing installed request's `owner.sources` map. Keep
the adopted installation unchanged. Inside the custom owner's entry function,
the existing loader exposes the snapshotted helper under `run_context.sources_owner`:

```python
import sys

# In the installed owner entry, after receiving its run_context:
original_path = list(sys.path)
try:
    sys.path.insert(0, str(run_context.sources_owner))
    from contribution import contribute_from_context
finally:
    sys.path[:] = original_path  # Required by the installed loader's final check.

# client is already open; ready is from its demand-directed reader.finish(...).
# The caller has selected these values; no additional acquisition occurs here.
if ready["status"] == "READY":
    result = contribute_from_context(
        client, ready["context"], source=selected_lean_source,
        roots=selected_root_names, export_names=selected_export_names,
        author_limits={"cpu_seconds": 30, "wall_seconds": 60, "memory_mib": 768},
        admission_limits={"native_cpu_seconds": 10, "receipt_cpu_seconds": 10,
                          "wall_seconds": 60, "memory_mib": 512})
```

This is a continuation snippet, not a standalone launcher. The caller keeps the
existing runtime/workspace/grant setup and cleanup. The request snapshots and
binds this helper; the owner is trusted local code, not sandboxed by adding its
directory to `sys.path`. See `examples/README.md` for the ordinary `run`
request and lifecycle, and the installed semantic-reader documentation for
demand-directed selection. Unlike `contribute.py`, this helper has no input
selection or bulk-import stage and no `main` that opens another operation.

`source` is Lean source text, not a path. `roots` and `export_names` are one to
64 distinct formal names, each an array such as
`[["s", "MyNamespace"], ["s", "newTheorem"]]`. Imported names must refer to
the actual selected context. Limits have exactly the fields shown and remain
subject to the original grant, owner suballocations, deadlines and enclosing
Job. Example values do not guarantee success for arbitrary mathematics.

## Exact sequence and outcomes

The helper borrows the client's original workspace and grant. It calls authoring
once with the supplied context, validates the returned untrusted packet and
source/root binding, stores the new packet in quota-bounded custody, and calls
actual `admit_local` on that new packet's module, digest and byte length. Only
after the live checked result binds to that packet and summary does it call
`publish`. A completed publication must bind the same module, packet digest,
length and export selection.

- `status="CONTRIBUTED"`: actual new-output admission and local publication
  completed. `checked_output` records its journal; `publication` is the existing
  durable publication report. This says nothing about global visibility,
  novelty, benefit, permanent retention or newly produced succinct receipts.
- `status="NEED_AUTHORING_CONTEXT_DATA"`: authoring requested the returned
  `demands`; no new packet was stored, admitted or published by this helper.
  It does not fetch data or retry. The caller decides what to do next under
  its remaining original allowance.
- Exception: it propagates unchanged; no automatic fallback or fresh grant.
  Existing client failures can revoke the operation. Untrusted custody or
  partial publication may already persist, so preserve the workspace and
  original exception/publication record. Never treat an exception as a
  completed contribution or automatically replay it.

The helper never closes the client or workspace. The caller must serialize
access and run its existing cleanup on every outcome. Reports are inert
operational evidence: `mathematical_acceptance=false` means the report itself
is not reusable authority, not that the new packet bypasses actual checking.
This is trusted owner composition, not a hostile-source sandbox. The helper
alone is neither an executed Lean integration result nor final v5 acceptance.
