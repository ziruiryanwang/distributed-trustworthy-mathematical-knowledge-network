# Typed guest: actual four-crate build audit

2026-10-21, adaptive_audit. **PASS for the selected compilation boundary.**
Root reported session90895 terminal exit0 before this audit. No compiler, guest,
assembler, test or proof was rerun. This result permits root to consider the
separate reviewed assembly step; it does not adopt an image or certificate.

## Exact evidence

Run: `experiments/v5-local-checks/typed-guest-build-01`.

| Record | SHA-256 |
|---|---|
| Selection, saved and external identical bytes | `bab4fd3e335683be859a1f38843b415eff13a2dcb9c215c931ae1d6f463911e3` |
| `RESULT.json` | `b1b4f7a82aabddc5dd3349a4f82ba79e846517a6db94c3a3d911702c7d6576a4` |
| `INPUT-MAP.json` | `f2942f0462044b79d7cc37edf387772d6e442cc0cebd3c3dde342182c6dfa12c` |
| `SOURCE-MAP.json` | `a05c6e910664260b05c4c875ea0df6545a4dd969b608f22a3b9585e590885356` |
| `RECIPES.json` | `fa11546f7fe58c752f58830429760c3958566ca36b6da7051fe2142306fa0ac5` |
| `ARTIFACT.json` | `f1d732f34287a63096f816fcc62f0724a470f6dc3dc725ae6b816787e08800ff` |

The attempt record exactly binds the result hash and
`PASS_TYPED_GUEST_FOUR_CRATE_COMPILES_ONLY`; no finalization override exists.
The reviewed builder and recipe pins remain exact. The source review remains
`TYPED-GUEST-REVIEW.md`, SHA `c9331517`.

## Independent checks

Read terminal records, command logs and finalization code. A read-only stdlib
diagnostic independently rehashed all331 recorded input files,37 project
snapshots,236 retained copies and both adapters. Snapshot and retained-directory
membership are exact, not just a matching subset. The236 copies total311693039
bytes; the original selection retains107 target rlib/rmeta pairs and22 macro
DLLs. All26 retained compiler-runtime input pins were included in the331.

The37 selected source files match the selection; the declared production map
has36 and excludes only support `bounded_parse/census.rs`. This preserves the
declared-static-closure scope: it is not a claim that compiler dep-info observed
all36 files. No historical native control was rerun.

Each of the four actual argv sequences equals its saved reviewed recipe in
checker/module/aggregate/guest order. They use the fresh source snapshot and
metadata names, the selected target/profile and fresh project rlibs; the module,
aggregate and guest extern paths do not substitute old project libraries.
All commands exited0 normally; before/after cumulative Job accounting chains
exactly, with zero active or terminated children and no cleanup errors.
The checker emitted two dead-code warnings and the module three; aggregate and
guest logs are empty. No error was masked as a warning.

All seven output hashes and both artifact pins match. The ELF is1809932 bytes,
SHA `eb66a3aa26ee64084dc244448ef7971606ea4943f2739521a57b777cda255f61`.
An independent ELF-header decode confirms32-bit little-endian RISC-V executable,
entry2100484 and the four reported load segments. The1927768-byte link map is
`04de7f3a0807dbe39a5959498ed25a992e9fd90de23a02765c397e9f19ddffda`.
`ARTIFACT.json` equals the result's artifact object. No assembled-image identity
is inferred from the ELF hash.

## Accounting and closure

| Quantity | Observed |
|---|---:|
| Checker inclusive worker CPU |15.171875s|
| Module inclusive worker CPU |4.984375s|
| Aggregate inclusive worker CPU |0.859375s|
| Guest inclusive worker CPU |20.90625s|
| Closed worker Job total |41.921875s|
| Controller CPU through inner measurement |8.21875s|
| Known disjoint CPU total |50.140625s|
| Worker phase wall |32.434705399908125s|
| Inner controller wall |49.885398699902s|
| Worker Job peak private commit |399953920B|

The Job reports closed, zero active/terminated children and no cleanup errors.
All recorded quantities fit their original limits. The nine cumulative processes
are not nine concurrent processes; the active-process ceiling remains six.

The pre-result census records334 entries/330573059B. Independent final read-only
census finds306 files+29 directories=335 entries/330605976B: exactly one additional
32917-byte `RESULT.json`. It remains below512MiB/4096entries. No override marker
was added by the post-report census.

**Timing boundary:** final report writing and process-exit tail are excluded from
the inner CPU/wall figures. Root confirms there was no separately metered outer
inclusive CPU or elapsed duration. Terminal exit0 is known; a fully measured
end-to-end build cost or hard bound on that unmetered tail is not established.
Do not call49.885398699902s the complete outer elapsed time. This accounting gap
does not justify repeating the successful compilation.

## Adoption boundary

Four new project compiles occurred, with zero Cargo/dependency compiles, guest
executions, image assemblies, proof calls or network calls in this operation.
This audit supports the exact compiled artifact, retained-input linkage and
clean terminal completion. It does not establish typed-guest target cost,
cryptographic renewal, scalable reuse, performance improvement or v5 completion.
Assembly and the exact FIRST/I execution require separate root selections and
actual audits; the prospective128-segment screen and unfunded proof boundary are
unchanged. All used sources/evidence remain frozen; no Git mutation by this agent.
