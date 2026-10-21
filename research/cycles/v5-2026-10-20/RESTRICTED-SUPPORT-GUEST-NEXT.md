# Support-summary guest: minimal next build plan

2026-10-21, core_release. **SOURCE_PLAN_ONLY_NOT_SELECTED_OR_IMPLEMENTED**.
Prerequisite: independently reviewed native controls establish unchanged exact
J/pending-parent conclusions and meaningful work reduction. Root owns that gate.
No guest adapter, selector, compile, native run, image assembly, host or proof
operation is created or launched by this note.

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Paths below are relative to `experiments/v5-local-checks/` unless stated otherwise.

## Minimal work

Compile only the new RC core, unchanged aggregate source linked to that core,
and unchanged guest entry linked to that aggregate. Do not rebuild the original
module relation, Nanoda, SDK dependencies or snapshot host.

- Three compiler invocations: rc-core, aggregate, guest.
- Twelve production source files (three fresh, nine frozen).
- Five fresh outputs: RC rlib/rmeta, aggregate rlib/rmeta, guest ELF.
- Reuse the236-file dependency view from `typed-guest-build-01/retained`.
- Reuse guest03's exact original-module and Nanoda artifacts below.

The exact successor run/schema/adapter paths remain root's later selection,
not authority inferred from this plan.

## Exact successful guest03 adoption boundary

All records here belong to `restricted-guest-build-03/`:

| Record | SHA-256 |
|---|---|
| RESULT.json | 44f808cdd24c2707d114675bf77a4126a805865eaae825666db0c9403e354273 |
| selection.json | d110cb21351b2f07461986d971533a895011ab0da695e07c6b62175e7de85bf3 |
| RECIPES.json | f2c120697cde3569a5c4faf021b92096af95baa1e1ea683d11592763b24c8e74 |
| SOURCE-MAP.json | 7d1586b530cd1382bd5c40b75a71d804319b5f9da31ec1798dd7c34e41fcff1e |
| INPUT-MAP.json | ec9838b580641d17b25f2965fc39a11e97946d1b3f4ad959d4531f4a8480980d |

Require successful `DMKN_V5_RC_GUEST_FOUR_CRATE_BUILD_RESULT_V1` /
`PASS_RC_GUEST_FOUR_CRATE_COMPILES_ONLY`, matching sibling attempt
`c904c5fa4dce1258f1e527ea736b54823736df7073d573df3c5a644b8aec898b`,
clean four-command closure and absence of FINALIZATION-FAILED.json. This is the
actually successful guest03 module compile, not the historically failed module
operation that blocked earlier guest attempts. Preserve all earlier outcomes.

### Original-module artifacts

| Path under guest03 | Bytes | SHA-256 |
|---|---:|---|
| outputs/libdmkn_module_relation.rlib | 2349740 | d70c585aead8afe869ce96eadde46ef7d8f31efe1bdbb717955adcff8efa4f76 |
| outputs/libdmkn_module_relation.rmeta | 830551 | 6b879d8fff8c09c858e0ff4f51a442a3cae33aa3551c062cf55479025ef77828 |
| retained/projects/libnanoda_lib-7f1af4fb875deccc.rlib | 6360054 | 8ec342c7f606b9ccf34cdd5fbf4bf86cd75f6239fd2cd025c7d837d442cf5fde |
| retained/projects/libnanoda_lib-7f1af4fb875deccc.rmeta | 2446327 | d5266e9ea875433bff5b2c4f084ee48f64be6d5bb6104316a44096a85cc7d62e |

Recommend copying only the module pair,3180291bytes, into the successor's fresh
two-file retained-module directory. Hash before/after and require its exact map.
Reuse guest03's retained/projects directory in place for Nanoda (exactly those
two files), and the existing236-file dependency view in place. This avoids
another broad copy while keeping all old RC/aggregate outputs off search paths.
Directly pointing `--extern` at the old module pair could save this tiny copy,
but the isolated view gives simpler explicit dependency resolution.

The236-file recorded dependency map contains no dmkn_* or Nanoda entries.
Retain its exact pins and before/after binding in any future build. This planning
step reads the adopted map; it does not rerun its full dependency hashing audit.

## Exact twelve-source closure

The three fresh files are `software/v5/restricted_support/{lib.rs,syntax.rs,typing.rs}`.
Their final native-reviewed bytes must be used, not a second implementation.
The nine frozen files are:

| Canonical-root-relative path | SHA-256 |
|---|---|
| software/v5/restricted_composition/relation.rs | 540af158f61654f50aa50335dec7811b43448f3520050edf953db7e75060670b |
| software/v5/restricted_composition/foundation02.rs | e8d0e32b3c480eb05b6813b6afd8eae8413930e26a436955783b2bf3e2452dce |
| software/v5/restricted_composition/aggregate_lib.rs | bd5acb09eac6d093366554ad4901ee6118b81cf8db63b76f62e5bd02029d40ee |
| software/v5/restricted_composition/aggregate_relation.rs | 7439f70ebcf2919e9261634618ce537814b695a869b2934c8ffe61d96d13e8fa |
| software/v5/restricted_composition/census.rs | 7d18b7658827e15fc10df1d65c5376c146470a005dde590b4590236a73b14ba9 |
| software/v5/restricted_composition/wire.rs | 942fd9f99a0845552df566771c86b4a4a610688ba008aef9e47a18c0a8088395 |
| software/v5/aggregate_claims/header.rs | e4a3426b66506559a8ddb8eb9d06195af3d14676199e6f5a9251b7ff3ff550e1 |
| software/v5/aggregate_claims/membership.rs | f3671d5305407f11109c5b30ea1f173216c475b2ddc0ba485a4097a266df22ba |
| software/v5/aggregate/main.rs | d7b9b93843b683215e0556e585bc5ea241c672fe4c2a89cc07afa41afb81acad |

## Why the new aggregate uses the new core

Reconstruct the last three actual adopted guest03 recipes, preserving compiler,
target `riscv32im-risc0-zkvm-elf`, SDK/sysroot, optimization3, overflow checks,
panic-abort and all nonproject dependencies. Replace exact selected source,
emit/output paths, dependency paths, link-map path and project metadata only.
The three direct extern counts remain10/11/11.

1. New core: source restricted_support/lib.rs, explicit retained module rlib.
2. New aggregate: same aggregate_lib.rs and source closure, explicit retained
   module rlib **and explicit fresh new-core rlib**.
3. New guest: same main.rs, explicit retained module rlib and fresh aggregate rlib.

Use fresh metadata identities for all three project crates. The module retains
its actual guest03 metadata; the Nanoda pair retains its adopted metadata.
Allow project dependency search only in the fresh outputs, fresh two-file module
view and exact old Nanoda view. No `-L` directory may expose guest03 outputs,
native build outputs, old RC libraries or old aggregate libraries. No baseline
alias belongs in guest recipes; that alias is native-controls-only.

Source evidence: aggregate_relation.rs imports
`dmkn_rc_relation::relation as rc_relation` and calls its `check_with_census`
for every delta. `module_relation` supplies conclusion types and shared helpers,
not an alternate checking call. The module's adopted compiler recipe has only
Nanoda among its project externs, and its nine-source closure contains no RC or
aggregate reference. Thus it cannot carry an old RC implementation as a
transitive dependency. The old RC and aggregate artifacts are not selected.

The guest entry calls the new aggregate, verifies every pending exact claim
with the SDK, and commits the exact derived header. No semantic/wire change is
needed. Final actual recipe/output/link-map inspection remains necessary; this
source plan alone is not proof that a future linker consumed the intended files.

## Execution and stop condition

Reuse the adopted restricted snapshot host only for the same retained first
fixture, following RESTRICTED-SUPPORT-BUILD.md: old native preflight, unchanged
full-J/pending differential, actual new image execution and genuine base-I parent.
The matching fresh image/assembly/endpoint configuration must be explicitly
selected and independently adopted. There is no automatic guest or proof budget.
The75%-of-general padded-row threshold,64-po18-segment limit and full preparation/
execution CPU nonregression remain unchanged. A native work reduction alone does
not establish them or authorize portable certificate investment.
