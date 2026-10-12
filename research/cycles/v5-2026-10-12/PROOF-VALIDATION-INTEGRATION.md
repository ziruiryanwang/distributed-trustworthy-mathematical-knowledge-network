# Minimum integration of validation-only proof correspondence

2026-10-12. Root requested this source/theory plan while it owns the separately
selected serde-only controls. **This document selects no new implementation,
compiler, native call, guest execution or proof.** The original checker,
aggregate, failed controls and all previously used bytes remain frozen.

## Decision and central reason

If the twelve focused syntax controls and independent actual review pass,
integrate the changed correspondence once through the real checking stack:

    fresh nanoda_lib
        -> unchanged module-relation source, recompiled
        -> unchanged exact-warrant claims-v2 source, recompiled
        -> unchanged native aggregate driver, relinked

The mathematical kernel, module relation and aggregate relation are not edited.
The only behavior change remains avoiding the construction of unused canonical
expression/level Values for a new theorem's proof. The proof is still fully
checked by the native kernel. Parse-once census is already in the claims-v2
source and need not receive a second isolated build or campaign.

This requires four compiler calls, not one and not a new dependency build.
An existing module rlib contains a dependency on the old checker crate; merely
placing a different `libnanoda_lib.rlib` beside that already compiled module
does not change its dependency safely. Recompile the dependent Rust crates
against explicit fresh artifacts, without changing their source semantics.

## Source closure: exactly32 production Rust files

All paths below are relative to the canonical root. A later bounded build
controller is one additional source file, not another mathematical component.
Snapshot this exact closure under its canonical-relative layout. Recheck every
unchanged file against the corresponding used source selection/snapshot, not
only against a new hash of whatever happens to be on disk.

### Fresh checker root and the already reviewed successor:2files

```text
software/v5/modules/native/proof_validation/lib.rs                 [NOT YET WRITTEN]
software/v5/modules/native/proof_validation/module_correspondence.rs
```

The new `lib.rs` is a thin alternate crate root. Preserve the old crate-level
attributes, public module names/order and `pub(crate) const STACK_SIZE: usize =
16_777_216`. Each unchanged module uses an explicit relative `#[path =
"../checker/src/NAME.rs"]`; `module_correspondence` selects the adjacent reviewed
successor. Do not wrap the old library as a nested module: its `crate::...`
references and public types must retain their original crate-root meaning.

If the old test declaration is retained for source correspondence, keep it
behind `#[cfg(test)]` with its explicit old source path. The selected full
library build is **not** `--test`; original test modules and the adjacent
correspondence test child are inactive and outside this production source
closure. The twelve focused tests already have their separate standalone root.

### Unchanged checker modules:14files

```text
software/v5/modules/native/checker/src/debug_printer.rs
software/v5/modules/native/checker/src/demand.rs
software/v5/modules/native/checker/src/env.rs
software/v5/modules/native/checker/src/expr.rs
software/v5/modules/native/checker/src/inductive.rs
software/v5/modules/native/checker/src/level.rs
software/v5/modules/native/checker/src/module.rs
software/v5/modules/native/checker/src/name.rs
software/v5/modules/native/checker/src/parser.rs
software/v5/modules/native/checker/src/pretty_printer.rs
software/v5/modules/native/checker/src/quot.rs
software/v5/modules/native/checker/src/tc.rs
software/v5/modules/native/checker/src/unique_hasher.rs
software/v5/modules/native/checker/src/util.rs
```

These are the complete production module declarations in the original root.
`union_find.rs` is present in the old tree but not declared/reachable from that
root; `main.rs`, CLI/preflight binaries, README, old tests and their dependencies
are not part of this rlib build. The `env!`/`include_str!` Cargo-package metadata
uses found in the old tree belong to `main.rs`, not this library closure.

### Unchanged module relation:9files

```text
software/v5/modules/receipt/src/lib.rs
software/v5/modules/receipt/src/canonical.rs
software/v5/modules/receipt/src/input.rs
software/v5/modules/receipt/src/foundation_static.rs
software/v5/modules/receipt/src/foundation_data.rs
software/v5/modules/receipt/src/commitments.rs
software/v5/modules/receipt/src/journal.rs
software/v5/modules/receipt/src/policy.rs
software/v5/modules/receipt/src/relation.rs
```

`foundation_data.rs` is a real compile input through `include!`, not optional
fixture data. Receipt guest/main, receiver host and native preflight binaries
are not part of this build. The relation continues importing the same public
`nanoda_lib::{module, module_correspondence, parser, util}` APIs and types.

### Unchanged claims-v2 relation and driver:7files

```text
software/v5/aggregate_claims/lib.rs
software/v5/aggregate_claims/header.rs
software/v5/aggregate_claims/membership.rs
software/v5/aggregate_claims/relation.rs
software/v5/aggregate_claims/wire.rs
software/v5/aggregate_parse_once/census.rs
software/v5/aggregate/native.rs
```

Preserve relative layout so the claims root's existing
`../aggregate_parse_once/census.rs` path resolves inside the fresh snapshot.
Its tests, graph controls, old reference census and parse-once differential
controls are all `cfg(test)`-only and need not be compiled or rerun. In
particular, do not repair the now-used old parse-once test in place or repeat
its15passing companion groups; root owns its separate single-group repair.

## Preserve Rust API identity without mixing crate instances

Keep crate names `nanoda_lib`, `dmkn_module_relation` and
`dmkn_aggregate_relation`. The driver uses two of these directly and the checker
transitively. Exact-Warrant V2 still means the existing full184-byte journal
graph,192-byte header, wire domains, bounds and private conclusion constructor.

The new checker must retain `Demand`, `ConditionalPremise`, `PremiseAuthority`,
the parser entry points, correspondence API and config layout. A changed crate
artifact may have a new Rust metadata identity even when the public API is
source-identical. Therefore:

1. Bind module compilation explicitly to the fresh checker rlib.
2. Bind claims compilation explicitly to the fresh module rlib.
3. Bind the driver explicitly to both fresh module and fresh claims rlibs.
4. Replace the old native-library/aggregate dependency-search paths with the
   one fresh artifact directory. Retain only the existing external dependency
   paths needed by the adopted recipe. Do not accidentally resolve an old
   project rlib from a predecessor output directory.

The same issue affects exception payload types and private native data types,
not just linker symbols. Mixing old/new checker instances would be the wrong
way to preserve type identity. A single rebuilt dependency chain avoids it.

## Exact retained recipes and the minimum compiler changes

| Input record | SHA-256 |
|---|---|
| `experiments/v5-local-checks/native-library-02/selection.json` | `7941f68e3615e7bb1119aa0083ce0cc73525e4b8e978f72ab4e596ba446b2cae` |
| `experiments/v5-local-checks/native-library-02/command/command.json` | `c07ca843fb34615dd4519c6197b6531b3185c42bf335ba0870ec6c3af46608aa` |
| `experiments/v5-local-checks/aggregate-native-build-01/compile-commands.json` | `1f80c02b5049dbb5bdb22fea28ff52d8def582871b27366dd1cd98a73be5e232` |
| `experiments/v5-local-checks/aggregate-claims-build-02/compile-commands.json` | `712a998a8a62c3fbff1289b69d02bb075a663fd6b6eec8e25e229fa04a6d7f3c` |

Use the successful native-library02 command for the checker: exact retained
compiler, target, edition2021, rlib/name, `overflow-checks=yes`, `panic=unwind`,
`opt-level=2` and all eight retained external rlibs. Change only source root
and fresh output. Do not add a different optimization profile merely because
the Cargo manifest uses opt-level3. Do not rebuild serde, bigint, semver or any
other dependency. Preserve linker/bitcode compatibility with the retained
recipe rather than guessing from a Cargo profile.

Use the original module-relation command with only fresh snapshot/output and
checker binding/search-path replacements. Use the claims-build02 relation and
driver commands with the analogous fresh path/binding replacements. Retain
the driver's required `-C lto=fat`: the earlier failed final link established
that retained dependencies include LLVM-bitcode archive members. No new test
binary, original checker CLI, delta driver, host verifier or guest is necessary
to answer this integration question.

One new bounded controller can reuse the same pinned supervisor/environment
and make these four calls in order. Root must separately select its exact
source hashes, finite CPU/wall/memory/output envelope and output directory.
Record each intermediate artifact so a later-stage failure does not force
rebuilding an already successful frozen checker. No implicit retry follows a
failure. Existing runtimes/libraries and all old outcomes stay untouched.

## Cargo and later guest integration: an important distinct boundary

The current `modules/receipt/Cargo.toml` still points `nanoda_lib` to
`../native/checker`. The current claims manifest points its module dependency
to `../modules/receipt`. Consequently, running Cargo on those unchanged
manifests would silently select the **old** correspondence implementation;
successful explicit native linking does not fix those manifests.

Do not edit either used manifest in place. If root later selects a Cargo/guest
successor, the minimum explicit solution is a fresh manifest overlay with:

- A checker package of the same dependency crate name whose `[lib] path`
  selects the fresh thin root, with `autobins=false` and the same dependency
  requirements. It need not invent a new public checking API.
- A fresh module-relation manifest whose `[lib] path` reuses the unchanged
  relation source and whose checker path selects that fresh checker package.
- A fresh claims manifest whose `[lib] path` reuses claims-v2 and whose module
  path selects the fresh module package; the guest entry can still reuse the
  unchanged aggregate `main.rs`.

The overlay source graph/lock/resolution and target-specific dependency build
require their own exact review. Native Windows rlibs cannot be transplanted
into the RV32 guest. A newly built guest image needs a newly adopted image ID;
old proof receipts do not certify the new binary. Exact semantic ModuleIDs,
foundation/policy bindings and embedded legacy module journals need not change
solely because this representation work is removed, but the aggregate image
and admission profile must bind the actual new guest. This plan stops before
that decision and before any proof investment.

## Decisive retained actual differential:2new calls, no reauthoring

First allow root's already selected claims-controls02 to produce/adopt its
V2-framed actual positive and invalid-proof baseline. At the writing of this
plan it is not assumed to have passed. Use those exact retained inputs and
stdout/exit evidence once available; do not reconstruct a convenient new
workload or rerun the old checker just to create another baseline.

The original actual mathematics remains the662480-byte corrected public
two-delta packet, SHA-256
`54c7dac7f83a9a06c2b23b17a77be20364c1b90e4cd3b1db58b69c62fda2dcf1`.
It has one genuine base frontier and two ordinary-source-derived deltas;
the second new theorem substantively uses the first twice. The expected
conditional aggregate has three exact members and three parent edges, ending
at module `52c564f87f31082468557df6eed0a04bc7adf9d28d9614fe6cf173f5633088bf`,
rank2. The native aggregate test does not itself verify that frontier receipt.

After root adopts the rebuilt chain, run only:

| New call | Required comparison with the retained V2 baseline |
|---|---|
| Exact retained `actual-two-delta.bin` | Exit0; identical complete structured stdout, including input hash/bytes, V2 header/root, every exact journal/opening, pending assumption, edge count, census and `mathematical_admission=false`. Raw stdout equality is also expected because the driver/dependencies are unchanged; investigate any difference. |
| Exact retained `invalid-proof.bin` | Exit2; identical complete refusal stdout with `CHECKER_PANIC_OR_UNRESOLVED_DEMAND` and `mathematical_admission=false`; preserve stderr and confirm a kernel type-equality failure, not a setup/syntax/lookup failure. |

The retained invalid proof changes the first child's theorem value from its
actual proof index1200 to its type index770. This is especially informative:
syntax validation alone does not reject all ill-typed proofs, so the native
kernel must still run and refuse it. The original retained diagnostic is
`tc.rs:945`, `assertion failed: self.def_eq(u, v)`. New source snapshot prefixes
can legitimately change stderr paths, so do not require exact stderr bytes.

No passing schema, rank, membership, Python binding or unchanged-graph group
needs repetition. The focused validator controls already distinguish failure
order/work bounds; the actual pair distinguishes successful integration and
continued mathematical rejection. If the V2 baseline fails for another reason,
stop to diagnose it rather than charging an optimization comparison against
an unqualified baseline.

## What this can establish and what it cannot

The refinement argument in `PROOF-VALIDATION-PLAN.md`, independently reviewed
source identity and focused controls justify preservation of correspondence
checks and their ordered visit counters, excluding allocation/resource faults.
The fresh actual pair then checks that the intended successor is linked into
the real conditional mathematical stack. Together they support one integrated
optimization; neither alone proves a new checker-to-Lean theorem.

Record native costs opportunistically, but do not claim speedup from two
short calls or extrapolate them to RV32/prover cost. The unchanged visit census
is deliberately expected: this optimization removes Value materialization,
not visits, input rows, native proof work or ancestry authority. A separately
selected informative guest screen should later combine it with parse-once
checking in one candidate. Guest/proof affordability, full-cost useful growth
and deployable v5 remain open until their respective obligations are met.

## Selected source implementation checkpoint

Root adopted this plan after independent principle review, the twelve syntax
groups' actual PASS, and the retained claims-controls02 actual PASS. Fresh
source implementation now consists of:

| Path under `software/v5/modules/native/proof_validation/` | SHA-256 |
|---|---|
| `lib.rs` | `c1961d6722b8d9677b68e6bb8bf318c4b2a4383adf09f82aa3c305e90099341a` |
| `integration/build.py` | `78bcf7fa950d5a350f9bdc1ef0464f79309f994f2a3e30d0974f233be1372d58` |
| `integration/BUILD-PROPOSAL.json` | `da8129fadd3913cf9d36fd196b259b157662065443773a78fcfea9b20346ed6e` |
| `integration/compare.py` | `d0b0bc18788cd8df2334dec97b488b2a33e61a21999e64bf40ac5fec6d03aff7` |

The source closure remains32Rust files, plus the build controller. The thin
root path-reuses the14unchanged checker modules; the builder checks their pins
against native-library02, all9module sources against the retained module map,
all7claims/driver sources against claims-build02, and the validator against
the successfully tested syntax snapshot. External dependencies are reused.
Only the newly compiled dependent project artifacts replace the old chain.

The four compiles share240workerCPU/240phasewall seconds,3072MiB and6processes;
the controller has60CPU/600totalwall seconds,1GiBoutput/8192entries,1MiBcommand
logs and the adopted owned-telemetry cleanup. The inert BUILD-PROPOSAL retains
`authorizes_compile_only=false`; root created a distinct reviewed selection
`948c505e...` and reports build01/session12588 live. This note does not declare
its outcome or authorize a retry. Used root/build source now remains frozen.

The separate comparison controller is still source-only. It accepts a fresh
config with schema `DMKN_V5_PROOF_VALIDATION_COMPARISON_V1`, name
`proof-validation-native-compare-NN`, `authorizes_two_native_calls=true`, its
own `{bytes,sha256}` source pin and the completed build's exact
`{path,bytes,sha256}` RESULT pin. The supplied COMPARE-PROPOSAL is deliberately
inert (`false`) and leaves the as-yet-unadopted build-result bytes/hash null.
Root must fill those from the terminal adopted build and select separately.

Only two new native calls are permitted, reading the retained V2 input files
directly. Their pinned SHA-256 values are:

- Actual two-delta input: `7e21d092206b08a9a71231045b8152df4179ee6575cdc5e3afc704ef03c0be58`.
- Invalid-proof input: `bfea350f79ed86d25a5e16fbc55dc705620f80ac8b429779b2aa26f8c312f2f1`.
- Actual positive stdout: `01d7c9cc45a16f520980e80672f90c0a97a69e31e344f748910df5abb24ffd0b`.
- Actual negative stdout: `42d71010ea316cdbce83b22f2ce5ef77ced0dda6a980802091de6bb15134205d`.

The shared native Job has60CPU/60phasewall seconds,1536MiB/2processes; the
controller has60CPU/300totalwall seconds,16MiBoutput/128entries,1MiBcommand logs.
It requires exact stdout bytes, exits0/2, the retained kernel `tc.rs:945`
type-equality refusal and no mathematical-admission flag. It rechecks source,
all four new build outputs, build finalization marker, baseline and pinned
runtime before/after, with cleanup and finalization failure overriding PASS.
No baseline test is rerun, no proof is generated, and no source is reauthored.

Root subsequently reported build01 terminal/reaped with raw four-compile PASS,
independent outcome review pending. At root's request the inert comparison
proposal now binds its actual27713-byte RESULT SHA-256
`55ba9a702360dd10a6b9bea00f481d5066553a1b8debcb10ca43bbcab4de4069`,
instead of the earlier null placeholders. Its selected output records are
checker `c0c0b10b...`, module `10efaf57...`, claims `829d68c1...` and native
driver `7ca635aa5bb18ce1a2a360d0f5e30f5d5ebf0b2fdce818aa8ae1029c92446635`
(1804800bytes). Reading these pins is not an independent outcome audit.
Comparison authorization remainsfalse until root's reviewed fresh selection.

This author's actions were source edits and read-only inspection only; root
owns all build/native/guest/proof launches and Git. Cargo overlays, guest and
proof investment remain unimplemented and separately held at this checkpoint.
