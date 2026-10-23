# Use checked commons mathematics in a normal Lean project

This is the public-module integration source for the v5 candidate. The installed
command and ordinary Lean consumer have passed their selected local workflow;
final v5 remains unfinished. It extends
the existing ordinary owner with one operation: `export-module`. Existing
`init`, `status`, `contribute`, `extract-std` and `complete` behavior is retained.
See the [retained library workflow](../ordinary_library_support/README.md) for
extraction and completion; this export step is separate from admitting a result.

The [saved independent audit](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-PROJECT-EXPORT-SEAM.md)
records the exact public package/profile, normal theorem application and definition
reduction, preservation of earlier artifacts, and 14.83 seconds elapsed / 14.02
known inclusive CPU seconds. This is interoperability evidence, not a comparative
growth advantage. The selected development package is
`experiments/v5-local-checks/ordinary-module-package-assembly-01/package`, profile
`f01398e394a7bfda05f641469077cb74927aafd1cb1a3d42383d4b1d271e9435`.

If an approved ordinary Lean package already provides the mathematics you need,
prefer its normal pinned import. The bridge is for a result that you have checked
through the commons and want to reuse in an ordinary local proof project.

## Export an already checked result

Use the selected installed package and its exact profile hash. The command below
is wrapped for readability; supply it as one command in your shell.

```text
<python> -I -S -B <package>/owner.py export-module
  --profile-sha256 <selected-package-hash>
  --python-runtime <absolute-python-root> --lean-runtime <absolute-lean-root>
  --catalog <existing-catalog> --custody <existing-custody>
  --store-id <existing-store-id> --custody-limits <existing-limits.json>
  --wall-seconds <original-wall-budget> --cpu-seconds <original-cpu-budget>
  --memory-mib <child-memory-bound>
  --parent-root <explicit-local-context-root>
  --module-targets <absolute-targets.json> --output <fresh-absolute-directory>
```

`targets.json` is a nonempty array of exact `{name, export_id, unit_id}` records,
using the same structured-name encoding as `--acquired-targets`. Copy the records
returned by a successful public contribution or acquisition; do not replace
names with strings or infer IDs. The selected context must actually warrant the
records. Their syntactic validity or presence in custody alone is insufficient.
No database editing, test harness or new owner initialization is needed.

`--module-targets` is export-only. For this operation, do not supply source,
`--acquired-targets`, output names, project-authoring, completion, extraction,
status or initialization options. The output directory must be new and outside
the package, runtime, owner catalog and custody. The command never guesses a
latest parent or fetches missing dependencies from the network.

The exporter gathers exact full proof evidence for the selected dependency
closure, checks it over the approved fixed Init basis, and writes a genuine Lean
module. It does not substitute theorem assumptions or accept downloaded compiled
modules. Native source, worker and helper code come only from the pinned package.

## Read the result

Exit code 0 and outer `ok: true` mean the export and owner closure succeeded.
The result status is `CHECKED_PROOF_COMPLETE_LOCAL_MODULE`; useful fields are:

- `module_name`: the exact `DMKNBridge_<hex-key>` to import.
- `module_directory` and `manifest_path`: absolute local output locations.
- `artifact_parts`: byte lengths and SHA-256 hashes of all five module parts.
- `supported_runtime`: the selected Lean executable/pin, runtime directory,
  installation-manifest hash and implementation identity.
- `targets`, `source_context_root` and `new_catalog_acceptance: false`:
  the exact locally warranted mathematics selected, without new admission.

`MODULE.json` is written only after the native report and all artifact checks
pass. It records local generation, not a cryptographic certificate or a warrant
for another owner. The wrapper adds convenience locations/runtime identity to
its public result without changing that manifest's format.

## Import it in an ordinary project

Use the exact supported Lean runtime, not just the same printed version. The
exporter does not inspect your downstream project and cannot certify its runtime
or compatibility. The current profile uses the pinned Windows Lean 4.34.0 runtime.

For a direct Lean invocation, set a process-local module search path in this order:

```text
LEAN_PATH=<supported-runtime>/lib/lean;<module_directory>
```

Do not include the commons authoring helpers, receiver snapshot directories or
untrusted peer paths. Add other owner-trusted project paths only when needed.
An alternative is to copy all five manifest-verified same-stem parts together
into a dedicated local module directory; keep the manifest and avoid overwriting
another module. Do not copy these files into or modify the global toolchain.

An ordinary new-system source file can start with:

```lean
module
public import Init
public import DMKNBridge_<returned-hex-key>
public section

-- Write ordinary definitions and proofs using the exported declaration names.
```

Replace the placeholder with the literal returned module name. Invoke the
reported executable, for example with these arguments:

```text
-DElab.async=false -R <project-root> -o <fresh-Consumer.olean> <Consumer.lean>
```

This needs no owner state or commons helper imports in the consumer. It is
ordinary theorem application and kernel reduction, not reconstructed source
notation, attributes, typeclass registration or executable code. `#eval`,
`native_decide`, arbitrary Mathlib compatibility and IDE/Lake integration are not
promised by this profile. No project files or global environment are edited.

## Cost, limits and refusals

The first export pays for owner-context validation, full selected proof closure,
Init loading, rechecking and writing. Subsequent ordinary module import need not
rebuild the export. There is no automatic cache or guarantee of constant-cost
checking; huge closures can refuse. Current caps include 32 targets/units, 4 MiB
aggregate evidence/request bounds, 131,072 expression nodes and 4,096 names.
All stages share the original caller allowance; failed attempts count too.

Existing Init-name collisions outside the fixed basis refuse, even if they look
equivalent. Missing custody evidence, wrong identities, private-only semantics,
changed pins, oversized inputs or exhausted budgets also refuse. A refusal is
not necessarily a mathematical counterexample. No automatic retry or allowance
renewal occurs. Keep diagnostics and partial output; use a fresh directory for
any separately chosen subsequent attempt.

If export completes before a later reporting/owner-close failure, outer `ok` is
false but the successful module detail may remain in `module_export` or `result`.
Do not infer rollback or delete accepted state. Ordinary owner opening can perform
its existing interrupted-operation maintenance; export adds no mathematical root.

The owner-controlled installation and OS remain trust premises. Named runtime
pins are not a hermetic attestation of every transitive Init artifact. Windows
Jobs contain the selected process tree for resource accounting; they are not a
hostile-source filesystem sandbox. Exported binaries are local derived artifacts;
other peers must use their own acceptance policy, not trust these binaries as proof.
