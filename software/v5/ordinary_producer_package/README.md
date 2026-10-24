# Approved local project to an inert proof bundle

These are source-only successors for the next consolidated package, not an
installed or runtime-qualified release. They add `produce-baseline`; the existing
native exporter, worker, bundle binder and receiver checker are reused unchanged.

The workflow is deliberately small: select useful declarations in an already
compiled, explicitly approved local Lean project; export their supported proof
data; share the resulting exact bundle by ordinary files/repositories; let a
receiver inspect and independently admit it. If an appropriate bundle already
exists, share it without another export. No commons owner, catalog, custody,
parent context, registration or certificate is required at the producer.

## Prospective installed invocation

Use the selected package's `owner.py` with Python `-I -S -B`. The filename does
not mean this operation opens an owner. Required options are:

| Options | Meaning |
|---|---|
| `--profile-sha256`, `--python-runtime`, `--lean-runtime` | Explicit adopted package and supported runtimes |
| `--project-production`, `--project-production-sha256` | Exact approved compiled-project selection JSON and its SHA-256 |
| `--approve-local-project` | Explicit local execution approval, not a mathematical trust assertion |
| `--output-names` | Nonempty JSON list of structured Lean target names |
| `--output` | Fresh output directory, separate from project/support directories |
| `--wall-seconds`, `--cpu-seconds`, `--memory-mib` | One original finite allocation, including startup and support loading |
| `--spool-mib` | Explicit complete spool allowance, 144 through 256 MiB |

The operation name is `produce-baseline`. State/context/reference/other-operation
options are rejected, even status flags explicitly set to their normal defaults.
Other operations still require their prior state arguments and reject production
options. Existing parser defaults for their status pagination remain unchanged.

The project-selection format is the existing
`DMKN_ORDINARY_TRUSTED_PROJECT_EXTRACTION_V1`, containing exactly `schema`,
`project_search_paths` and `modules`. It names ordinary absolute approved Windows
directories and structured module names; it does not pin the contents of every
transitive compiled artifact. Target names use the same structured Lean-name
encoding as existing public commands. No source build, Lake hook, dependency
download, peer binary or automatic retry is launched by this command.

## What the result means

Success is `PRODUCED_INERT_BASELINE_NOT_ACCEPTED`, with manifest/target identities,
bundle census and resource observations. `mathematical_acceptance` is false.
Share the exact `manifest.json` and its `units/` files without editing them.
The receiver can use the existing `intake-baseline` command with its own selected
parent and independently checked state. Producer reports and manifest membership
never replace receiver checking. A valid produced bundle need not fit one current
peer receive: production allows 8,192 units while that path selects at most 1,024
missing units. Fit is receiver-relative, not a producer success claim.

The 144 MiB minimum reserves the existing 64 MiB native writer, 64 MiB encoded
evidence, 2 MiB manifest, 12 MiB metadata and two 1 MiB logs. It is an authorization
ceiling, not predicted disk use or a hard filesystem quota. Native child processes
use the existing Job supervisor. Python controller limits remain cooperative;
hard containment requires supervising the entrypoint as well. Native CPU is
charged once, including failures; unknown accounting retains its full reservation.
All partial output is preserved and no existing accepted state is opened or changed.

## Costs and compatibility

Owner-free does not mean cheap for every library. The retained exporter imports
the private compiled environment, censuses it, and serializes the full selected
dependency closure outside the fixed 581-name seed. It does not stop at a remote
receiver's warm cache. Demand batching and reusing existing bundles may help;
overlap, repeated environment loading, unsupported declarations or large closures
may make ordinary approved package use the better route. No uptake, useful-growth
rate or universal speedup has been measured by adding this command.

The current adapter targets the selected Windows/Python 3.14/Lean 4.34.0 profile
and its existing declaration/axiom policy. Local artifact approval is essential;
resource limits and `loadExts := false` are not a hostile-artifact sandbox.

The next consolidated profile changes owner/profile source and therefore the
reference-support identity. Old installations and registered references remain
preserved, not silently relabeled or migrated. This producer route does not use
those references. It does not repair or qualify the separate currently incomplete
original-reference contribution/delta path and its diagnosed import-mode defect.
No new discovery protocol, candidate-ingest command or remote export service is
part of this source change.
