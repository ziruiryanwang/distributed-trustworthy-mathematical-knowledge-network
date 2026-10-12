# Guest build02 recovery: three project compiles over retained dependencies

Status: SOURCE READY FOR INDEPENDENT REVIEW. No compiler, Cargo, guest,
assembly or proof was run by this author. Root owns exact selection and launch.
The unrelated unused stage-host builder remains HOLD.

## Actual failure and preserved cost

`bounded-parse-guest-build-02` completed offline resolution and exact comparison
of the 297-unit graph. Its compile command was interrupted by the ordinary
controller-CPU envelope, not by a Rust compiler diagnostic. The controller then
exceeded its total envelope during finalization. `FINALIZATION-FAILED.json`
overrides `RESULT.json` and the attempt record; no ELF/map/ARTIFACT was produced.

The result records 190.21875 worker CPU seconds, 88.640625 controller CPU seconds,
179.7263687 wall seconds, 381 processes, clean Job closure, 1,203,777,536 peak
Job bytes, and 11,755 output entries / 871,399,184 output bytes. The final
controller tail was not measured exactly: actual controller CPU is greater
than 90 seconds. Thus this operation costs **more than 280.21875 total CPU
seconds**, and the two bounded-parse attempts together cost **more than
300.34375 CPU seconds**. No recovery erases or reclassifies that work.

Frozen failure/result pins:

| Record | SHA-256 |
|---|---|
| build02 RESULT | `792ed5825ae3110dc3ddc1a85b49636b63469f5e4cb1d662e70d8ddf27d6b4b6` |
| build02 finalization override | `36c6f5c6b7084dbb08d461c008ea8b39e71e80bf95cc90860e455936b637cf55` |
| build02 selection | `a537fdbc9bf27b9a0832bb14a72aa07aad4d96abe9cc6bb433473a58935c16e2` |
| build02 source map | `1ca936d624d91d7d395ac89f7535e1564473ee62e05a6f357e754b6d2c93281b` |
| build02 unit graph | `142224e56a81b3d73960a0aa5c5f80360658ccf0f1bff06883152cbfe92511fe` |
| build02 graph comparison | `36b0bd9bc55a15adca6f8e878bda3b2529d015fe841075aa3f2d30e771780bc5` |

The monitor checks CPU/logs approximately every 0.1 seconds, but a fresh-tree
census only every 10 seconds after the preceding census, plus command boundaries.
The census repeatedly resolves paths for each entry. Large output-tree scans are
a source-visible avoidable cost; no timing profile permits exact causal CPU
apportionment. The recovery avoids rebuilding/copying the large dependency tree
instead of rewriting the monitor or raising its budget.

Separate latent defect: the failed `-vv --message-format=json` build output
contains ordinary build-script lines. Unconditional `json.loads` would fail
after an eventual successful compile. This is not the observed build02 cause.
The new path does not parse new Cargo output at all.

## Reuse argument and its trust boundary

Rust crates are separate compilation units. Recompilation of the changed module
crate, the aggregate crate that uses it, and the final binary can reuse unchanged
dependency artifacts when compiler/target/features/dependency identities and
native-link requirements match. This is a compatibility argument, not a claim
of reproducible identical ELF bytes or a newly executed full Cargo graph.

The old `aggregate-guest-compile-01` Cargo child completed successfully
(222.640625 worker CPU seconds, exit zero, clean closure). Its operation also
failed finalization. The new selection explicitly adopts the currently hashed
retained dependency bytes; it does **not** invent historical hashes, claim that
old finalization passed, or grant mathematical authority to those artifacts.
Independent compiler/checker trust remains part of the larger assurance model.

The pinned old nonverbose stdout is all JSON (256 artifact messages, 41
build-script messages, final success true). The 41 script messages have no
additional native `linked_libs` or `linked_paths`. Native payloads bundled in
retained rlibs remain those exact bytes. Their availability is not a claim that
all arbitrary Cargo builds can be reduced to this recipe.

The fresh view contains exactly:

| Adopted files | Count | Bytes |
|---|---:|---:|
| 108 target library versions, each paired rlib/rmeta | 216 | 281,325,788 |
| Conservative retained host proc-macro DLL view | 22 | 39,173,632 |
| Total | 238 | 320,499,420 |

Libraries are keyed by `(package_id, target_name)`, not only by crate name:
several names have multiple selected versions. The old module and aggregate
rlib/rmeta pairs are excluded. Every retained file is copied to a new regular
file, not hardlinked. The copied view's exact map is checked before use and on
finalization. Subsequent fresh crates receive explicit new rlib extern paths and
distinct metadata salts; the search directories never contain the old project
libraries. Existing caches and project snapshots are read-only.

The sole package-ID relocation exception is `nanoda_lib@0.4.19`, from the old
aggregate guest checker wrapper to the build02 bounded-parse checker wrapper.
The already-passing exact graph comparison allows that relocation, and all 16
checker Rust source pins must equal the old compile source map. Other direct
dependency package IDs and feature sets match exactly.

## Three reconstructed recipes

The fresh files are:

| Source | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/bounded_parse_guest/recipes.py` | 9,412 | `61d020dfc0597cd74c887d162bf88187e446ab1f4a9f67faa2ae2dbd3e7e7927` |
| `software/v5/bounded_parse_guest/build_projects.py` | 18,648 | `a2ccf89c795cfafd6f9cc8ec14afb6447a95ab317ae483a323b94b62ce80fb49` |

`recipes.py` is pure data-to-argv construction, with no filesystem or subprocess
operations. `build_projects.py` is the fresh bounded controller. Both await
independent review; no Python project import/test was performed by this lane.

Only these Rust compilation commands are prospective:

1. `bounded_parse/module_lib.rs` to new module rlib/rmeta.
2. `bounded_parse/aggregate_lib.rs` to new aggregate rlib/rmeta, referring to 1.
3. Unchanged `aggregate/main.rs` to the new guest ELF, referring to 1 and 2.

Roots and their transitive source includes are read directly from the complete
immutable 39-file build02 snapshot. Exactly 16 non-checker Rust files are
compiler-read sources. The controller rechecks the whole snapshot map and its
38 selected source pins plus lock; there is no fresh source-copy tree.

The recipes retain edition 2021, target `riscv32im-risc0-zkvm-elf`, opt-level 3,
abort panic, overflow checks on, debug assertions off, stripped debug info, and
the selected lower-atomic/text-address/fatal-warning/getrandom configuration.
Libraries use linker-plugin LTO and the binary uses fat LTO with embedded
bitcode. Seven build-std externs use `noprelude`; direct extern counts are
11/10/11. Explicit `--emit` destinations bind link/metadata/dep-info outputs.
These are **reconstructed equivalent-profile argv**, not captured Cargo argv.

The saved project profile has `codegen_units: null`, `debuginfo: 0`,
`split_debuginfo: null`, `rpath: false`, `incremental: false`, and resolved strip
`Named: debuginfo`. The recipe likewise supplies no explicit codegen-unit count,
debug info, split-debug option, rpath or incremental directory: the same pinned
compiler's defaults apply to both unspecified settings. Explicit strip matches
the saved resolved setting. For `lto: true`, the new libraries preserve LLVM
bitcode for the final binary's full cross-crate fat-LTO step; the retained
dependency rlibs already support the old successful full-LTO binary link.
This reproduces the intended release optimization semantics, not every
uncaptured Cargo flag, compilation schedule, metadata hash or byte sequence.

Compiler/runtime binding comprises 26 exact rustc, rust-lld, bin DLL and host
sysroot library files (395,093,004 bytes), plus the pinned existing bounded
helper/Python closure. No Cargo executable is invoked, no graph command repeats,
and no SDK/std/checker/dependency source is compiled. OS facilities remain part
of the retained host trust boundary; this is not a hermetic-build theorem.

## Macro/environment review

The 16 project Rust sources contain no `env!`/`option_env!`; the sole include
requires `foundation_data.rs`, already in the source set. Nonbuiltin macro
paths were inspected rather than presumed context-independent:

- `risc0_zkvm::guest::entry!(main)` expands the entry function declarations;
  SDK assembly includes outside that expansion were consumed in the retained
  SDK compilation. The inspected guest/mod.rs hash is
  `c149e205515d214b48e54313c163ff17c15e0bda275122df4c63205573ed3656`.
- `serde_json::json!` expands through its defining crate with no Cargo-environment
  read in its macro definition.
- Two `Deserialize` derives use the retained serde_derive 1.0.229 DLL. Its
  `env!("CARGO_PKG_VERSION_PATCH")` was evaluated when that proc-macro DLL was
  compiled; the emitted version token is already fixed. Its emitted serde
  private references agree with the retained guest serde 1.0.229, not the
  different host serde version. No dynamic environment read was found in the
  inspected derive source. Serde's own OUT_DIR includes likewise belong to its
  previous compilation, not these new consumer roots.

The controller still records its complete private invocation environment.
This narrow review does not generalize to arbitrary proc macros.

## Finite prospective envelope and output contract

The one fresh name is `bounded-parse-direct-build-01`. A root-selected six-field
`DMKN_V5_BOUNDED_PARSE_DIRECT_PROJECT_BUILD_V1` selection pins both adapters,
all 238 retained artifacts and exact limits, with an explicit retained-adoption
authorization flag. All three compiles share one Job and phase clock:

- 240 inclusive worker CPU seconds, 300 shared worker wall seconds;
- 4,096 MiB memory and six active processes;
- 40 ordinary / 60 total controller CPU seconds, 420 total wall seconds;
- 512 MiB **total** fresh output and 4,096 entries;
- 8 MiB combined stdout/stderr per command.

The copied view consumes 320,499,420 of 536,870,912 fresh bytes, leaving
216,371,492 bytes for all outputs, temporary files, logs and evidence. This is
not an extra 512 MiB allowance after copying. Whether the compiler stays within
that remaining space/time is an implementation uncertainty, not a reason to
silently enlarge the budget. The substantially smaller tree removes the
known large-census shape while preserving checks and fail-closed finalization.

Prospective PASS is only `PASS_BOUNDED_PARSE_THREE_PROJECT_COMPILES_ONLY` under
`DMKN_V5_BOUNDED_PARSE_DIRECT_PROJECT_BUILD_RESULT_V1`. It requires three
completed commands, exact ELF/map checks including `_start` and `__start`,
unchanged inputs, complete copied view, clean closure and no finalization
override. `ARTIFACT.json` pins the ELF/map. The result retains build02's failed
lineage and unknown accounting tail. It certifies no guest execution or proof.

New provenance records are deliberate contracts, not cosmetic compatibility:

- `SOURCE-MAP.json`: `source_snapshot`, complete `project`, the 16
  `compiler_read_sources`, and the two `adapters`.
- `INPUT-MAP.json`: exact original inputs and copied artifact map.
- `RECIPES.json`: `DMKN_V5_DIRECT_PROJECT_RECIPES_V1`, explicitly
  `RECONSTRUCTED_EQUIVALENT_PROFILE_NOT_CAPTURED_CARGO_ARGV`.
- `GRAPH-COMPARISON.json`: `DMKN_V5_RETAINED_GRAPH_PROJECTION_V1`, saved graph
  hash and comparison, three new units, and zero new graph commands.

The separately owned assembly adapter must consume this provenance explicitly;
it may not pretend this run has the previous copied-project/Cargo schema. Root
must select any assembly only after independent actual build adoption. Execution
screen, receipt production, reciprocal mathematical use and public v5 readiness
remain separate open gates.

## Concrete remaining checks

Independent review should challenge graph/artifact crate identities, matched
metadata/extern binding, native/archive linker closure, source/macro inputs,
new-file isolation and finite finalization. Successful compile/ELF is still
unobserved. Assembly, current-image acceptance and meaningful reciprocal benefit
are not implied by source review. No held stage-host work was expanded here.

## Independent source addendum: direct-build assembly boundary

At root's request the build author separately read the complete unused
`software/v5/bounded_parse_guest/assemble.py` (17,931 bytes,
`220f54cf19fb9bebfd61674df332113a9e0f98bbd003bcecb5a268738048ca01`),
`research/cycles/v5-2026-10-12/Select-BoundedParseAssembly01.ps1` (7,615 bytes,
`b82ec0187eae50ca08e6b24cac10ea7e721626bd773fd3efef48d947943a8e72`),
the retained outer runner and snapshot consumer. No adapter/selector edit or
execution was performed. **No concrete contract or closure mismatch found.**

The adapter accepts only the fresh direct-build PASS/three successful closed
commands, matching attempt, no new finalization override, explicit retained
failed02 lineage, and the new source/input/recipe/graph contracts. It compares
actual argv to recorded recipes and binds the exact ELF path and map. The root
selector includes both new sources, 18 Python runtime pins, the driver/result/
kernel triple, current build records/artifacts, all six retained failed02
records, all 39 retained sources and both used direct adapters. This remains
below the outer runner's 256-runtime-input ceiling. The selector's weaker
preparation checks do not bypass the stricter inner pre-invocation checks.

The size limits fit all currently known inputs: the largest retained JSON record
is the 544,592-byte graph; the largest retained project file is 85,478 bytes,
both below the adapter's 2 MiB record/source limit. The 66,679,296-byte pinned
driver has its own 128 MiB maximum; the 58,736-byte kernel is below 64 MiB.
Prospective ELF/map/image bounds are respectively 64/32/64 MiB. Their actual
sizes and new records still require the actual-build audit; a larger result
would be a refusal, not silently accepted. The three-artifact driver closure
is exactly the earlier assembly selection's driver result, executable and
kernel, with no inferred extra compiler or dependency-tree reads.

The snapshot consumer expects the unchanged generic assembly status/image
fields that this adapter emits. Assembly remains inside the selected outer
Job; its inner PASS cannot override failed outer completion or runtime binding.
It neither executes the guest nor produces a receipt. Skipping another hash of
all 238 libraries at assembly is intentional: actual-build adoption establishes
the build, while assembly rebinds the exact successful ELF and its small source/
provenance closure. This addendum is source review, not actual-build adoption,
assembly permission or whole-v5 assurance.
