# Independent aggregate stage-host build review

Disposition: **PASS_SOURCE_AND_EXACT_SELECTION_REVIEW** for one trusted,
compile-only stage-host link. No execution, certificate production, admission,
performance claim or full-v5 acceptance follows from this review.

Reviewer: `memo_independent_review`. Canonical root throughout:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Consequential decision

The retained complete frontier capsule removes the missing-execution-layout
obstacle to using the reviewed aggregate producer. That producer needs a stage
host, but does not require another SDK, checker or relation build. The existing
one-link builder is an appropriate minimal next implementation step. I found no
source/data blocker to root selecting it once under its exact finite envelope.

This review reused the Rust/source analysis in
`research/cycles/v5-2026-10-12/AGGREGATE-PRODUCTION-SEAM.md`; it did not repeat a
checker/backend build or rerun an already passing test. It read the builder,
relevant retained helper definitions, retained records and root's fresh selector
as source/data. No project Python imports, compilation, test, host or proof call
were made by this reviewer.

## Exact reviewed selection

`experiments/v5-local-checks/aggregate-stage-host-build-01-selection.json`
is 292,269 bytes, SHA-256
`fde4496bea48c5682116c5f2bf7e37bf7834fb422a4abef04b43867dee709326`.
It has exactly the six fields required by the builder: `schema`, `name`,
`authorizes_compile_only`, `sources`, `runtime_pins`, `limits`. The schema is
`DMKN_V5_AGGREGATE_STAGE_HOST_BUILD_V1`, the name is
`aggregate-stage-host-build-01`, and compile-only authority is true.

| Source | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/aggregate_production/build.py` | 17,828 | `a1d2c22427ffa9f8293813ac76359f9cdde6a3f73870c75a209dad2310bc781a` |
| `software/v5/aggregate_production/stage_host.rs` | 22,515 | `5865e6afb30bd81adb79d6fe04e09ac8bb7238b40956284fa3bcd2d4da4fe102` |
| `software/v5/aggregate/receipt.rs` | 3,631 | `41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254` |

Total selected source is 43,974 bytes. `receipt.rs` is the stage host's additional
path-module source. The reviewed Rust bytes are unchanged.

Root's `Select-AggregateStageBuild02.ps1` constructs this selection without
execution. It retains old digest values rather than blessing arbitrary current
runtime bytes. It verifies held records and source identities, checks freshness,
and uses exclusive `CreateNew` with flush. The first selector is preserved: its
PowerShell argv-array wrapper failed before creating output. Selector02 removes
that wrapper; it does not change the proposed build. Neither selector should be
rerun against the already-created selection.

## Independent retained-runtime reconstruction

I independently reconstructed the Python filter in PowerShell from the pinned
old 3,142-entry runtime map and retained compiler argv. It keeps only:

1. Every old `C:` map key.
2. Immediate `.rlib`, `.rmeta`, `.dll`, `.lib`, `.a` files in the exact fourteen
   retained `-L` directories.
3. The exact retained `rustc.exe` and immediate Rust-bin DLLs.
4. The same link/runtime suffixes immediately within the retained target
   `lib/rustlib/x86_64-pc-windows-msvc/lib` directory.

The resulting map has **1,071 entries**, including **98 C-drive entries** and
**25 Rust-toolchain entries**. Every selected path exists. Its metadata size is
**2,320,491,997 bytes**. Comparison of every selected path/digest against the
fresh selection found **zero differences**. All seven direct externs are in the
map, as are the compiler and exact MSVC linker.

I independently hashed all seven direct externs and the transitive checker;
each matched both the old map and the new selection:

| Retained library | Bytes | SHA-256 |
|---|---:|---|
| `libanyhow-696464f4b2560bb1.rlib` | 633,352 | `d60ad9251b31138bb6506c42adf062e5c37d6e9728d626a47c047a7173a10b30` |
| `libbincode-c374a8dbb9e79ad3.rlib` | 674,634 | `c9dc6a56e36315e813f1f02aeb8a67edd1c5fdc287347fb7810f94c9e310ddfa` |
| `librisc0_zkvm-e4b4822463e0ff62.rlib` | 12,713,862 | `5c5bff2476163fe1fcb6453f9b7d5aa84e1887b349a939ae5fffddd90ee5c434` |
| `libserde-c8458b918a5c64a0.rlib` | 944,484 | `c2bdec00d6bc0942b77e31495ca7d3aec7df7370e42cf65335b232ff35e32044` |
| `libserde_json-9fcbc8f7ff06ebf5.rlib` | 2,078,164 | `6bfb6c46c8fb3bfdc98ad1d5712a790aa3fec7f834f5fe3e8be567fc023100ea` |
| `libdmkn_module_relation.rlib` | 4,217,412 | `10efaf57720635b0c347487194283117599ecb3be326b4c51b3c9dbcc144a4bf` |
| `libdmkn_aggregate_relation.rlib` | 916,696 | `829d68c1a2c51138785394e19bcb35692902144d7be19f1dbfc9c9742f1952b4` |
| `libnanoda_lib.rlib` | 11,339,020 | `c0c0b10ba18adf5c20496d751cc9cbbc911677fafe64461d963dadc53a37c4a2` |

The first five are in the retained general-checker host05 release-deps directory;
the last three are in `experiments/v5-local-checks/proof-validation-integration-build-01`.
I deliberately did not duplicate the full 2.32 GB runtime hash pass. The builder
checks every selected runtime hash before preparation and again during finalization.
The metadata/map comparison alone is not a claim that every current runtime byte
has already passed that execution-time check.

## Retained recipe and helpers

All five retained record hashes match the builder's constants:

| Record below `experiments/v5-local-checks` | SHA-256 |
|---|---|
| `aggregate-host-build-01/RESULT.json` | `4cdb12b5e3aeaebcfef5e0370bd445f24ff6779b196ca69cbab60f9d57002a75` |
| `aggregate-host-build-01/compile-command.json` | `acc215837499107a01bfe60544dceeb40ff19ad4d67f93252867bbf30f3de96b` |
| `aggregate-host-build-01/environment-profile.json` | `34525808d26848e9582ad5ada38ff66fae2205f79ae0421a33f72fbd67af4e18` |
| `aggregate-host-build-01-selection.json` | `b8c64994f64c66eaa8a90612d5fa0f3ebcad4ce053e86f4f8fe485408cadbb8b` |
| `aggregate-host-build-01-attempt.json` | `cdc489e3d1dcd73bcb4ab782fd10138ccaaf452725976c2f38ac644348590ee2` |

The old result is `PASS_AGGREGATE_HOST_ONE_LINK_ONLY`, has one compiler command,
and records zero active and zero terminated processes. The attempt binds that
exact result; no old finalization-failure override was present.

The pinned support/build/prepare/artifact/provision/census/phase helpers and
`run_stage.py`/`domains.py` were read and their current hashes checked against the
retained chain. The Python executable and DLL also match their retained pins.
The retained environment's `cl.exe`, `link.exe`, and `rc.exe` bytes/hashes match
all three saved observations. VCTIP and the full Rust runtime are additionally
bound by the builder, not claimed separately rehashed here.

The one compiler argv substitutes **exactly three entries**: crate name,
stage-host snapshot source path and fresh executable path. It preserves
edition 2021, binary target, `x86_64-pc-windows-msvc`, optimization 3, fat LTO,
bitcode, overflow checks, unwind panic mode, seven externs, fourteen library
directories and the exact MSVC linker. There is no Cargo, SDK, checker or relation
rebuild, no network command, and no host/guest/proof invocation. Cargo-related
environment variables do not themselves invoke Cargo.

## Finite execution envelope and expected feasibility

| Bound | Value |
|---|---:|
| Inclusive worker CPU | 240 s |
| Worker wall | 300 s |
| Job memory | 3,072 MiB |
| Active processes | 6 |
| Ordinary controller CPU | 40 s |
| Controller CPU including finalization reserve | 60 s |
| One total wall clock | 420 s |
| Fresh output | 512 MiB / 8,192 entries |
| Command log | 1 MiB |

The wrapper uses one shared Job, checks inclusive user-plus-kernel CPU live and
at finalization, attaches its suspended child before resumption, and enforces
finite output and log bounds. The monotonic/controller clocks begin before
preflight and do not reset at finalization. Only the fresh run is censused.
The large runtime map is hashed twice, not needlessly a third time immediately
before the compiler. Explicit environment construction avoids inherited
credentials and isolates temporary/profile/cache paths.

The phase helper kills/reaps on failure, restricts telemetry cleanup to exact
owned descendants, refuses unknown descendants, and requires quiescence without
termination/cleanup error for success. Final records are exclusive; a late output
envelope failure emits an overriding `FINALIZATION-FAILED.json`. Constructor or
preflight failures before run creation still need root's outer terminal/accounting
record; absence of `RESULT.json` must never be treated as successful nonexecution.

Historical reference, not a predicted result: the retained aggregate snapshot
host used 65.375 worker + 6.640625 controller CPU seconds, 72.2037113 wall seconds,
987,435,008 peak Job bytes and a 6,626,304-byte executable. The more comparable
module stage-host03 reference used 105.625 worker + 19.1875 controller CPU seconds,
213.1983675 wall seconds, 1,103,548,416 peak Job bytes and a 66,652,160-byte executable.
These make the proposed finite envelope plausible. They do not prove the new
fat-LTO link will finish. A failure must be retained, not automatically retried.

This is a trusted Windows toolchain build, **not** a hermetic build or security
sandbox. Hashes establish input identity, not compiler correctness or the
mathematical soundness of the resulting stage host.

## Root-only next operation and adoption

If root selects execution, use the exact retained **`D:\Python314\python.exe`**
with `-I -S -B`, the actual canonical
`software/v5/aggregate_production/build.py`, the absolute reviewed selection path
and its SHA-256 above, with canonical workdir. The builder checks both
`sys.executable` and its actual `__file__`; an unchanged generic snapshot launcher
or a different bundled Python is not interchangeable.

The only fresh run is
`experiments/v5-local-checks/aggregate-stage-host-build-01`, with the adjacent
`aggregate-stage-host-build-01-attempt.json`. Both were absent when reviewed.
Do not recreate the selection, reuse this run name after an attempt, run the
produced host, fund a proof stage, or install anything merely from this clearance.

After one terminal operation, independent adoption must inspect: exact command
substitution, source/snapshot/input identities, executable identity, final and
attempt binding, absence of overriding finalization failure, Job quiescence,
inclusive costs, output census and outer terminal state. A passing compiler
outcome establishes only that this retained one-link recipe built the reviewed
stage host. Producer controls, actual staged proof production, economical reuse,
full-cost growth and deployable-v5 acceptance remain separate obligations.
