# Allocation refinement: exact offline rebuild and adoption recipe

Status: **source preparation only; no build or proof selected**. Root's
`research/cycles/v5-2026-10-17/PROVER-ALLOCATION-SELECTION.md` owns scope. The
unchanged SDK, all used executables, capsule and receipts remain frozen.

## 1. What changes, and why it is safe

`preflight.patch` applies only to the exact source pinned in `SOURCE.json`.
It renames the byte-valued maximum to `MAX_WIT_BYTES_PER_ROW`, checks divisibility
by `size_of::<u32>()`, converts to words, then uses checked multiplication for
the requested word count. The existing `anyhow` and `ensure` imports already
exist at line 25; no import or dependency change is required. The retained Rust
source already uses `usize::is_multiple_of` in `Trace::add_block`.

The original 5,582 bytes must hash to `bf427f0e...228bde`; exact patched output
is 6,003 bytes, `88fbf84e...b67396`. Full digests are in `SOURCE.json`. Both use
UTF-8 without BOM, LF endings and final LF. Apply without fuzzy matching or
offsets into a **new source snapshot**, never into the retained SDK. Verify the
complete before and after hashes, not just a successful patch-tool exit code.

Every new trace row reserves at most 153 words. Row indexing precedes the new
auxiliary write, and a successful trace uses at most N rows, including Globals.
Both old and new vectors zero the entire accessible 153N-word prefix. Writes,
offsets, metadata and final truncation remain identical. The synchronous FFI
uses pointer plus **length**, not capacity, and the Vec remains live through
the copy into C++'s 153N-word buffer. The new overflow/divisibility checks refuse
instead of wrapping. They do not admit new traces.

This establishes the refinement without running duplicate old/new preflights.
The structural saving is 481,296,384 bytes = 459 MiB per po18 segment. It is not
an OS-peak measurement or an upper bound. The future genuine-segment acceptance
by the unchanged verifier is the implementation discriminator; do not repeat
old passing suites or execute a second preflight merely to restate this proof.

## 2. The five-step graph is explicit, not a Cargo prediction

`SOURCE.json.compiler_recipe.ordered_steps` contains complete argv templates
and per-step environment overlays. There is one literal parameter, `${RUN}`.
Before any launch, root chooses one fresh absolute canonical output directory,
expands every occurrence, and pins the resulting concrete selection. Reject
unexpanded tokens, existing outputs, paths outside that root, or changed inputs.
The JSON is data, not an instruction to launch a compiler now.

| Order | New artifact | New direct dependency |
|---|---|---|
| 1 | `risc0_circuit_rv32im` rlib | None; one source allocation correction |
| 2 | `risc0_zkvm` rlib | Step 1 |
| 3 | `dmkn_module_relation` rlib | Step 2 |
| 4 | `dmkn_aggregate_relation` rlib | Step 3 |
| 5 | `small_aggregate_stage_host.exe` | Steps 2, 3 and 4 |

This is four rlib compiles and one host compile/link. The original retained
Cargo run did not save verbose per-crate rustc argv; do not claim to replay
unavailable command lines. Steps 1-2 are a **new explicit direct-rustc recipe**
derived from the retained target manifests, fingerprints, artifact log and
source includes. They use edition 2024, target x86_64-pc-windows-msvc, O3,
embedded bitcode, unwind, release-style overflow/debug assertions off, the
retained warning flags and exact retained enabled features. There is no Cargo
dependency resolution, build-script invocation, native C++ rebuild or download.
The recipe makes these compiler choices visible rather than guessing Cargo's
cache behavior. Compiler identity and generated inputs stay pinned.

Steps 3-4 copy the exact retained integration argv (O2, overflow checks on,
unwind and bitcode) with only fresh source/output locations, new dependency
paths, fresh metadata and the new dependency search directory. Step 5 similarly
derives from the actual small stage-host argv, preserving O3, fat LTO, overflow
checks, unwind, native search paths and linker. No comparison requires final
proof bytes or executable hashes to stay identical.

Each rlib gets explicit fresh `-C metadata=dmkn_auxwords_a53940b67580e215_<crate>`
and a fresh output filename. All changed `--extern` paths propagate forward
through the graph. Never combine a new zkVM with the old module-relation rlib;
its embedded Rust dependency identity points at the old zkVM. Retained old
libraries may remain as read-only search inputs for unrelated dependencies, but
are never substitutes for a required new artifact. The new library directory
is first, and every changed direct dependency is explicitly named. Any metadata
mismatch or ambiguous resolution stops the build; no fallback to old libraries.

## 3. Complete finite inputs, snapshots and generated code

`SOURCE.json` pins 113 files in the two SDK `src` trees, 19 retained recipe/
manifest/generated-input records, and all 72 direct SDK extern references
(30 circuit, 42 zkVM). The maps were resolved from the retained artifact log
and checked for uniqueness. `rand` explicitly selects 0.9.2, not the also
retained 0.8.5. Proc-macro inputs are host `.dll` artifacts, not target `.rlib`s.
The old circuit entry in zkVM's *provenance* map is replaced by step 1 in its
actual argv; it is not the newly linked input.

Snapshot paths and identity rules:

- Copy the two complete pinned SDK `src` inventories under
  `${RUN}/source/sdk/risc0/{circuit/rv32im,zkvm}/src`. Copy the pinned package
  manifests to their matching crate roots, and the workspace manifest/lock and
  config as evidence. Only the designated preflight source receives the patch.
  Validate exact paths, length and hash for every file; preserve all bytes.
- Copy the frozen integration source-map files from the retained integration
  build's `source` directory under `${RUN}/source/integration`, with the map's
  relative paths unchanged. Copy the frozen small stage-host source-map files
  under `${RUN}/source/stage`. The maps are themselves pinned in `SOURCE.json`.
  Use these snapshots, not current mutable `software/` files. The ordinary
  nanoda checker rlib remains unchanged; it is not compiled again.
- Copy the pinned `preflight_opt_gen.rs` to `${RUN}/generated/rv32im` and set
  **only step 1's** OUT_DIR to that directory. The original rv32im build script
  generates this file; its retained output has no cfg/link directives. The
  pinned zkVM build output merely declares `gpu_accel` for cfg checking and
  does not enable it on this CPU build. No guest/build script is rerun.
- Retain the complete 1,071-entry `runtime_pins` map from the pinned actual
  small-stage `selection.json`: compiler/runtime, host proc macros, target and
  host dependency rlibs/rmeta, native archives and selected system inputs.
  This map is a reused finite input manifest, not a recursive search of the
  machine. Rebind every listed hash before/after, and separately bind every
  direct extern in `SOURCE.json`. Bind every literal compiler input in the
  argv to the union of these maps and newly produced outputs. Refuse omissions
  or conflicting hashes. Source inventories and generated files are additional
  inputs, not implicitly covered by the runtime map.
- Use the retained pinned Windows compiler environment profile and the same
  environment-construction semantics, explicit canonical cwd and exact rustc
  executable. Clear inherited OUT_DIR/Cargo-package variables before each
  per-step overlay; set CARGO_PKG_VERSION=5.0.0 for SDK crates. Do not invoke a
  wrapper, Cargo, compiler discovery, an ambient rustc, or build scripts. The
  future finite selection must pin the actual constructed environment and
  runner/helper closure; this source recipe does not invent that selection.

No dependency is downloaded. At preparation, enumerate only the already pinned
manifests, not wildcard libraries. The compiler's finite dependency search
directories are inherited from the successful commands; all eligible library
inputs require the pinned union above. This preserves the existing trusted
build/toolchain assumption; it is not a hostile-code sandbox.

## 4. Honest new adoption seam: required before build investment

The used `aggregate_small.producer.AggregateProducer._adopt_host_build` accepts exactly
one command, the old `SMALL_AGGREGATE_*_HOST_BUILD` schemas, zero backend and
relation rebuilds, and a three-file source map. The existing build adapter has
the same unchanged-library premise. **Neither can truthfully adopt this build.**
Do not edit their old result records, set rebuild counts to zero, or smuggle new
libraries under old pins. The old snapshot-host/layout adoption remains valid
and does not need a second execution.

The source-only `adoption.py` and `producer.py` now implement a fresh narrow
stage-host adoption seam. `RefinedAggregateProducer` retains the existing
completed-layout snapshot grammar; `RefinedLifecycleProducer` retains the new
generic selected-target lifecycle. Their common mixin changes only stage-build
adoption, binds the imported adapter closure in the support runtime map, and
does not change snapshot-host acceptance or proof verification. The distinct
build grammar is:

- Selection schema `DMKN_V5_PROVER_ALLOCATION_BUILD_V1`; result schema
  `DMKN_V5_PROVER_ALLOCATION_BUILD_RESULT_V1`; successful scope
  `PASS_PROVER_ALLOCATION_FIVE_STEP_COMPILE_ONLY`. These names now match the
  source builder and adopter; no actual build result yet exists.
- Pin this source descriptor and patch, original/derived source maps, concrete
  argv and environment, retained input manifests, declared finite limits,
  five ordered command records, output pins and complete output census.
  Input/source maps are frozen before compilation; generated output pins are
  appended only after the producing command has cleanly completed.
- Report two backend Rust crate rebuilds, two relation Rust crate rebuilds,
  one stage-host link, zero checker/C++/guest rebuilds and zero host/guest/proof/
  network calls. Check actual command order, exit status, cleanup and no live
  descendants; apply ordinary fail-closed accounting and no automatic retry.
- Verify the complete five-step dependency graph using exact produced path/length/hash, and
  require step 5's exact executable. Rebind all sources, runtime files, command
  records and outputs; do not treat a status string as evidence of build scope.
- Bind the new stage binary and result chain into the immutable producer
  profile. Preserve its old independently adopted snapshot host, actual
  capsule/session binding, A/I/F/P and exact target. Existing profile IDs are
  never reused for a different stage binary. No old proof-attempt record is
  migrated or restarted automatically.

The new adapter reuses the stable generic lifecycle/work accounting and
unchanged native stage protocol. The acceptance change is only how an
owner-controlled build is authenticated. Native proof verification remains
mandatory, and the source-refinement argument is not a certificate. Root owns
the adapter, finite limits, launch, result adoption and Git.

### Source builder and exact records

`build.py` has no launch on import. Its main entry requires isolated/no-site/
no-bytecode pinned Python, the exact canonical cwd and source path, and an
explicit SHA-256-pinned selection. The four selected preparation sources are
this recipe, `build.py`, `SOURCE.json` and `preflight.patch`. Preparation copies
their exact bytes plus all finite source/evidence inputs into a fresh directory;
the patch is applied only in memory and checked against the complete derived
source hash before that new file is written.

Five separate serial Windows Jobs each contain one compiler command. Each has
240 CPU seconds, 300 wall seconds, 3,072 MiB private commit and six active
processes. Total worker allowance is 1,200 CPU seconds; the controller has
120 ordinary / 180 finalization CPU seconds and 1,800 total wall seconds.
Fresh output is limited to 1 GiB / 8,192 entries, with 1 MiB combined stdout/
stderr per command. These are bounded proposed operation limits, not evidence
that compilation will fit or that proving has sufficient memory. Only exact
owned MSVC telemetry descendants may use the retained post-build cleanup rule.

The complete 1,071-entry runtime map is rebound before and after the build, not
before every compile. All original source/helper pins and fresh source/output
snapshots are rebound between phases. The compiler environment is constructed
without inherited variables; exact per-step environments and inputs are saved.
The producer adopter does not repeat that whole compiler-runtime scan.

`source-map.json` has `adapters` and `files` maps. The latter includes exact
copied/derived source pins, not compiler outputs. Retained records use
`source/evidence/{index:02d}-<basename>`. `compile-commands.json` is the ordered
list of `{name, argv}` objects. `INPUT-MAP.json` separates `source_inputs`,
`runtime_pins`, `helper_pins` and the explicit trusted-toolchain boundary.
`environment-profile.json` includes the exact base and all step environments.
Their digests bind into `RESULT.json`, whose output pins and five raw final
Job records are separate. `job.phase_jobs` is a list of `{name, stats}`; totals
sum disjoint serial Jobs, and peak commit takes their maximum. Completed rebuild
counts increase only after a clean command and pinned output. The external
attempt record binds the result digest. A finalization-failure sentinel overrides
both even if a preceding result reported success.

The source implementation and its independent review do not authorize compiler
execution. A fresh root selection, successful actual outcome and outcome review
remain necessary before adopting a host or selecting a genuine proof stage.

## 5. Stop conditions and next useful evidence

Source review and static pin/argv checks precede runtime. Stop on a changed
source, nonunique/unknown dependency, malformed patch, absent generated input,
metadata mismatch, expanded-path escape or compiler failure. Preserve every
attempt and charge; do not broaden features or rebuild native SDK components to
make a failed recipe pass without a new decision.

After a separately selected clean build and adoption, an actual segment proof
under a justified memory envelope can establish integration with the unchanged
verifier. Hardware headroom remains an independent prerequisite. The existing
source proof makes duplicate preflight comparison unnecessary. A single segment
is not full A completion, public reciprocal operation, useful-growth benefit or
deployable v5. The allocation correction addresses one concrete central cost
on the path to those goals without weakening them.
