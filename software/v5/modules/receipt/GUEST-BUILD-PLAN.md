# Root-selected finite new module guest build

Source only until root selects an exact immutable JSON request and independent
review clears it. `build_guest.py` prepares fresh source/lock/cache data, checks
the offline unit graph, then compiles one new guest. It does not assemble an
image, execute a guest, prove, publish, fetch dependencies or rebuild the native
cryptographic backend. All earlier sources, targets, allocations and failures
remain unchanged.

## Selected source successor04: existential profile2

Guest04 changes the shared receipt relation to DMKN_CERTIFIED_MODULES_V2 and
DMKNM002/profile2/184bytes. It removes the whole-witness digest, retaining all
mathematical and exact-parent checks. Additive canonical_size/parse_validated
replace whole-witness serialization/hash with exact bounded size validation;
the old public parse/canonical/hash contracts and semantic policy remain.

No checker source, dependency/feature/backend, graph rule, builder or budget
changes from guest03. The fresh source selection rebinds all40files; only the
four receipt sources(canonical,relation,journal,native diagnostic) and this plan
differ. Actual focused profile2 differential/review must pass before root launch.
No old receipt/guest journal becomes valid by projection; test-only native
projections do not authorize parent receipt migration. Guest03's failed execution
and all earlier source/result bytes remain untouched. Subsequent image assembly
and bounded snapshot are separate fresh decisions, not implied by this build.

## Selection and invocation

Use the retained isolated Python required by `common03.helpers()` (it checks
the executable/DLL hashes), `-B -I -S`, canonical project workdir, then:

```text
software/v5/modules/receipt/build_guest.py ABSOLUTE_SELECTION SELECTION_SHA256
```

Selection schema `DMKN_V5_GUEST_BUILD_V1` has exactly:

- `name`: fresh `guest-build-NN`, output under `experiments/v5-local-checks/`.
- `sources`: exact canonical-root-relative file map `{bytes,sha256}`. Include
  the ten files in `WRAPPER` (including private `src/input.rs`), the three files in `OWN`, and revised checker
  Cargo/license/src Rust files. Do not include checker Cargo.lock, caches or
  a prior target. Include every referenced checker source file.
- `preparation_sha256`: eight exact adopted guest03 preparation records named
  in the adapter's `ADOPTED` set.
- `authorizes_guest_build_and_owned_telemetry_cleanup`: true, selected by root.
- `limits`: exactly1800 workerCPU seconds,1800 allocation-wall seconds,
  4096MiB Job memory,eight active processes,16GiB combined working bytes, using
  the names checked in source. These are ceilings, not promised requirements.

Root records and audits the request before launching. The source caps are
256files,2MiB per file and16MiB total. The source tree is copied to
`project/modules/receipt` and `project/modules/native/checker`; wrapper/helper
and checker maps plus exact new Cargo.lock are retained. The build-source
scripts/plan are separately snapshotted. The root user's package path and
retired workspace placeholder are never used as build roots.

## Exact lock and graph change

The adopted preparation already contains the compatible RUINT1.16.0 selection,
offline seed, std source and pinned toolchain. `guest_graph.repin_lock` changes
only the source-less root package name/version from commons-checker-guest0.0.2
to dmkn-module-relation0.1.0. It parses old/new TOML and requires every other
record/field to remain equal. No Cargo dependency update runs.

After a locked/offline unit-graph query, `guest_graph.verify_delta` normalizes
only selected wrapper/checker/cache paths. It expects the root package/binary
rename plus ONE `dmkn_module_relation` library unit and the root's corresponding
library dependency edge. Every old external unit, package identity, feature,
profile, platform and dependency edge remains exactly equal after normalization.
Every serde_json1.0.151 unit additionally must have exactly `default,std` features,
making the moved-Value identity assumption an enforced precompile graph check;
arbitrary_precision/raw_value/preserve_order are not permitted by this selection.
The checker source is new and independently pinned; its package/dependency
metadata remains unchanged. Unit ordering may vary but identities/edges may not.

Unexpected graph deltas refuse BEFORE compilation. They are retained evidence
to diagnose, not a trigger to update dependencies or widen the allowlist. The
host-only `module_host.rs` is excluded; Cargo auto-bin discovery is disabled.
The selected guest binary and shared library are the only new root targets.

## Build and evidence

The adapter reuses the held finite Windows Job supervision, environment and
owned/hash-pinned VCTIP cleanup pattern. It preserves the stronger pre/post
source/SDK/std/cache/runtime rebind. Explicitly allowed telemetry cleanup must
be disclosed; it is not silently recategorized as unassisted clean exit.
For the combined guest03 preparation, only the immediately redundant initial
retained-map computation is removed: the first full rebind still computes it
and compares the pinned adopted map before any allocation, copy or command.
All later rebind calls, offline checks, cache copies and fresh target behavior
stay intact. No unreviewed old-target/incremental-cache reuse is introduced.

This combined successor includes the independently source-reviewed and actual
differential-qualified move-based correspondence constructor and frontend A/B/C
repairs. Their current exact source bytes, including the private input module,
must appear in the new selection; oldguest02 and every used predecessor source,
artifact and result remain unchanged. Build03 does not adopt its new image or
claim a runtime saving merely from these source-level changes.

The actual command uses the retained Cargo/Rust tools, explicit new guest bin,
release RISC-V target, exact build-std flags, `--locked --offline` and a fresh
target. It requires one correct compiler artifact from the fresh main source,
one successful build-finished event, a bounded well-formed RISC-V ELF, and both
SDK startup symbols in the new link map. All command logs/maps/costs/closure
and failures survive under the fresh allocation. No old guest artifact can
substitute for a missing new compiler output.

Pass status is ONLY `PASS_NEW_MODULE_GUEST_CROSS_BUILD_ONLY`. Subsequent actual
image assembly, adopted image identity, host compiler, execution cost screen,
proof allocation and strict receiver qualification each need distinct root
selection. No proof campaign is authorized by this plan or its build pass.
