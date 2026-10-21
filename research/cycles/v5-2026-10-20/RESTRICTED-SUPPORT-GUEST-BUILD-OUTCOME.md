# Support guest: actual three-crate build audit

2026-10-21, core_release. **PASS: exactly three selected compiles completed
with the adopted support core and isolated retained artifacts.** This is
build-only evidence, not guest execution, certificate production, economic
success or v5 release. No rerun, rebuild or old compiler/library-tree audit
was performed.

Run: `experiments/v5-local-checks/restricted-support-guest-build-01`.

## Independently checked bindings

| Record | SHA-256 |
|---|---|
| Original and saved selection | `7db15fceba38fda2b336ef3ff530a237214db11b99e3315e3d3b47d678b6a9db` |
| RESULT | `d90dcb854b01f407c067c6eec6cc29c6f98cc54291896c2afe79cadbb3534e10` |
| Sibling attempt | `9a724bc4e2584fa72ab9be8492dfe26c8ace0f1ebd78df9c58cd5a05c147f091` |
| RECIPES | `8fb548310f8b0773601cb0f89517964e48ec522cd989f8e13966c4eaabe27f06` |
| SOURCE-MAP | `cb0d70e9bc818d81aee427e1233b988b0b8ca5c74b418d6cff5266f9e9683ebf` |
| INPUT-MAP | `686728b379bc4997bd0ce00c53653eaedc0a2cb0fdf37a6ba23bd553129a4264` |
| ARTIFACT | `f32af5d89e30133d131573991156591ba6130796cba6ca2f2ca5e1087ad41a04` |

The result has the selected three-crate schema and
`PASS_RC_SUPPORT_GUEST_THREE_CRATE_COMPILES_ONLY`; the exact attempt agrees
and no overriding finalization-failure marker exists. All twelve selected
production files match their canonical and retained snapshot bytes; the snapshot
contains exactly twelve files. Both reviewed adapter pins and source-map/input-map
bindings match. All five fresh output pins match. The native build/control
adoption records match the selected exact records and the result/input bindings.
The copied retained module view contains precisely its two pinned artifacts.

The recorded 236-entry dependency map agrees with the already adopted guest03
map. Existing dependencies and compiler files were not rehashed in this audit:
their successful retained-artifact adoption and the reviewed builder's rebinding
are reused. Production closure remains the builder's declared static closure,
not a new claim of independently observed compiler file-access completeness.

## Actual new-core linking and outputs

All three actual command records equal their recorded recipes, in exact
`rc-core, aggregate, guest` order, with the selected source paths and fresh
metadata identities. Extern counts are 10/11/11. Each command has exactly the
five allowed search paths: fresh outputs, typed libraries, typed macros, the
old exact Nanoda view and the fresh isolated module view. No old RC/aggregate
output path or native baseline alias is present. Explicit project externs bind
the fresh RC rlib into aggregate and fresh aggregate into guest.

The pinned link map contains the support-specific
`dmkn_rc_relation::syntax::Arena::support` symbol, along with `_start` and
`__start`. This corroborates the selected linking records; symbols alone are
not treated as a proof of compiler correctness.

| Fresh artifact | Bytes | SHA-256 |
|---|---:|---|
| Guest ELF | 627224 | `0e6a4c356817dc640a157b592d5ead8868b6ef5d3cb8c388d08d3f4580c5909a` |
| RC rlib | 943284 | `679eb0dbd80a5961e255d3883632e3989023314f4d48241946a047606d298d4c` |
| RC rmeta | 144745 | `9428beeb2171b13b4a5d09217a70d11b9acd20f4ab996cec9d070ab00fc35378` |
| Aggregate rlib | 577718 | `d183f529270ecd01e0a556117206c235dc9ec4b48ba187a4f00e5f1e1ce4c26f` |
| Aggregate rmeta | 187231 | `62148f0fb10fad094e29f78c23a59b05a061bde1fbe50d75ed85e6f962b28d58` |

The 619776-byte link-map digest is
`a8f7593cef15b5f80b7e0e4aa3aa8a10b764d115512d0784966a1b5ac2bc202e`.
ARTIFACT and RESULT agree exactly. No combined guest image or image ID has
yet been produced by this build.

## Closure and costs

Each command exits 0 with empty cleanup errors, no active or terminated
processes afterward, and empty stdout/stderr (six checked logs). Shared-Job
CPU deltas are 1.8125, 0.984375 and 7.6875 seconds, summing exactly to final
worker CPU **10.484375 s**. Disjoint controller CPU is **4.296875 s**;
known total is **14.78125 s**. Total wall is **14.376229400280863 s**.
Final active/terminated counts are 0/0, cumulative process count 7; this is not
seven concurrent processes. Peak Job private commit is 255582208 bytes.
Reported sampled output is 6542561 bytes / 59 entries before terminal records.
The documented final-report/exit tail exclusion remains, not silently zeroed.

Actual counters show three compiler calls and zero module/checker/dependency
compiles, Cargo/graph/network calls, image assembly, guest execution and proof.
The selected original economic screen is still untested for this guest.
