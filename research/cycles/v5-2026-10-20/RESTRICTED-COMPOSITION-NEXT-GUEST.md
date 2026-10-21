# RC0 next critical path: three guest compiles, one matched cost decision

2026-10-21, source-only preparation requested by root. No build, guest execution,
proof, resource survey or deployment is selected by this note. Native controls
and their independent outcome adoption are prerequisites. Root adopts the
retained-dependency reuse direction in principle, not an unobserved result.

## Minimal implementation

Compile only three new guest crates, in order:

| Crate | Exact source root |
|---|---|
| dmkn_rc_relation | restricted_composition/lib.rs |
| dmkn_aggregate_relation | restricted_composition/aggregate_lib.rs |
| dmkn-aggregate-claim-guest | unchanged aggregate/main.rs |

All paths in this table are under `software/v5/`. Guest source closure is the
five core files, four aggregate/census/wire files, unchanged
`aggregate_claims/{header,membership}.rs`, and unchanged `aggregate/main.rs`:
12 files. Native controls, fixtures and their original-W emitter are not in this
closure. The existing main still checks every exact pending receipt with
`env::verify`, then commits the exact header. No new entry algorithm is needed.
Give each newly compiled crate a fresh metadata identity. Preserve the selected
RISC0 target, std feature closure, overflow checks, abort behavior and LTO flags.

Do not recompile a general checker or module relation. The original guest-target
module library already has the same canonical/commitment/journal/policy source
hashes as the retained native library used by the RC controls. RC calls only
those helpers and uses the conclusion type; there is no call to native checking
or complete foundation traversal. Presence as a transitive compiled dependency
does not constitute execution. Review the reachable source calls and final link
map; do not claim byte size alone proves unreachability.

## Exact retained guest artifacts

Base directory:
`experiments/v5-local-checks/aggregate-guest-compile-01/target/riscv32im-risc0-zkvm-elf/release/deps/`

| File | Bytes | SHA-256 |
|---|---:|---|
| libdmkn_module_relation-c98240db3a2d8c8d.rlib | 2349140 | fd75a524f44440099b7472700f2c31015fd48fba1a3f70a9e0ca32a183918fd4 |
| libdmkn_module_relation-c98240db3a2d8c8d.rmeta | 830820 | 2c46b5e0a3f18610f0ab1235f34426492249a47b2c08c3529b029bfa15a5c740 |
| libnanoda_lib-7f1af4fb875deccc.rlib | 6360054 | 8ec342c7f606b9ccf34cdd5fbf4bf86cd75f6239fd2cd025c7d837d442cf5fde |
| libnanoda_lib-7f1af4fb875deccc.rmeta | 2446327 | d5266e9ea875433bff5b2c4f084ee48f64be6d5bb6104316a44096a85cc7d62e |

Their original successful build result is
`81cce68d9b20f22b12d12d5d698084eb8eb101493de71c6e35cd6acb7b44f47a`;
source-map digest is
`75c710e3ee13f63cb6ef44da8656caa53c300bf649317d2b5669d8b9cde06ce0`.
The exact artifact paths come from its retained successful compiler-artifact
stream, already used by the prior reconstructed guest recipes. These are guest
target libraries, not the incompatible Windows-native rlibs.

Reuse the already filtered `typed-guest-build-01/retained/{libraries,macros}`
view for the other 236 files: 107 target rlib/rmeta pairs and 22 macro DLLs.
Its selected input map is
`f2942f0462044b79d7cc37edf387772d6e442cc0cebd3c3dde342182c6dfa12c`;
selection is `bab4fd3e335683be859a1f38843b415eff13a2dcb9c215c931ae1d6f463911e3`.
Bind each used artifact to that recorded map before and after compilation.
Only the four original project artifacts above need a new small isolated view;
there is no reason to recopy the complete 236-file dependency view.

There are therefore 240 retained artifacts in the combined view. Do not place
the entire old target/deps tree on the search path: it contains an old aggregate
crate. Explicit extern paths plus the two filtered views and fresh output
directory keep crate selection unambiguous. The same compiler/runtime identities
and source/feature checks from `typed_guest/recipes.py` remain applicable, but
the RC core is a new explicitly specified unit, not a fictitious existing Cargo
graph node. No new Cargo graph or dependency build is required.

## Host and preparation changes that must not be missed

The existing `aggregate_small/aggregate_host.rs` invokes the selected native
aggregate relation as mandatory preflight. Its old executable will reject RC
wire even if supplied the new guest image. Relink this unchanged source once
against the qualified RC native aggregate/core and original module dependencies.
Retain its receipt verification, po18, bounded segment storage, session binding,
fixed SDK, assumption resolution and no-dev-mode behavior. Reuse the retained
snapshot-host recipe; do not rebuild the SDK/backend.

Unchanged host source pins:

- aggregate_small/aggregate_host.rs: 20,755 bytes,
  `6644d9a03f25a59089fd735b0e2f2229ec8940dedbe2502568dfd8c6a36d9c25`.
- aggregate/receipt.rs: 3,631 bytes,
  `41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254`.
- aggregate/main.rs: 816 bytes,
  `d7b9b93843b683215e0556e585bc5ea241c672fe4c2a89cc07afa41afb81acad`.

A small untrusted wire wrapper can reuse `aggregate_claims/input.py::encode`:
that encoder treats witness bytes as opaque. Validate RC schema/frame bounds,
call the existing graph-envelope encoder, verify its exact prefix, and replace
only the 12-byte wire magic/version with DMKNRC01/version1. Do not mutate global
encoder constants or change receipt identities. The RC relation independently
checks the result. No new graph, Merkle implementation or trusted predictor is
needed. The old FIRST-specific `frontier_snapshot.py::derive` cannot be reused
unchanged: it pins a different target and witness.

Assemble once with the retained assembler and kernel using a new three-compile
result adapter. A fresh actual image A_RC is mandatory. Existing A capsules,
profiles and receipts cannot be relabeled. Assembly consumes its adopted build
closure; it need not redo compiler dependency discovery. No proving-stage host
relink is needed until a later explicit decision to produce a certificate.

## One genuinely matched execute-only comparison

Use only the first new RC target: the four-universe/16-binder context transport
theorem, its three explicit binary_congr applications, and the retained genuine
base-I receipt. Bind the fixture and exact J to the independently adopted native
RC/original-W differential result. The predicted J is not a receipt.

General arm: the strongest retained qualified general image, typed guest
`9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865`, and this
target's exact emitted original W, with one base-I boundary assumption. RC arm:
the identical local spec, universes, actual proof expression and exact ordered
parent opening/journal set encoded as RC0, with the same base-I receipt. Both
arms contain only BASE and the new target; neither contains historical FIRST.

The member journals, member Merkle root, ranks, seal height, target, foundation
and policy must be identical. The final aggregate headers may differ only in
bytes12..43, the actual aggregate image. Wire magic and witness representations
necessarily differ. Both hosts must derive the expected header independently,
verify the real base receipt, execute exactly once at po18 and retain complete
untrusted capsules/diagnostics. No fake first-RC receipt is needed. The second
conditional native fixture tests composition shape, not portable authority.

Record instruction count, actual/padded rows, segment histogram, capsule bytes,
each arm's disjoint controller plus inclusive worker CPU, and preparation cost.
Prefer ordinary stats over PC sampling. Do not rerun old FIRST or compare its
148/167 segments with this different theorem. Neither a source-node count nor
native time predicts a RISC0 speedup.

## Prospective investment thresholds, not source predictions

The source establishes removal of full-F row interpretation, general native
construction/checking and correspondence from the RC guest path. It does not
establish what fraction of cycles those operations consume. Fixed cryptographic
segment/recursion workspace is unchanged. A small matched execution resolves
the remaining payoff constant; another memory survey does not.

Recommended root-selected screen, fixed before either arm executes:

- Both exact mathematical endpoints and complete clean captures pass.
- RC padded rows are at most75% of the general arm's padded rows.
- RC uses at most64 po18 segments. This is a proposed operational investment
  ceiling, not a theorem, historical FIRST threshold, or affordability claim.
- RC's measured preparation plus execution CPU does not exceed the general
  arm's corresponding total. Treat host timing as secondary single-run evidence;
  deterministic segment/row differences are the main decision statistic.

Why include an absolute ceiling? The retained staged graph uses `3s+m` calls.
With one assumption,64 segments imply at most193 stage calls;128 would imply385.
The relative criterion alone could select a still-unattractive huge workload.
These numbers are transparent policy choices root may revise **before** the
experiment, not conclusions derived from the small source input. Failing the
screen leaves a correct optional restricted lane, not permission to move the
goalposts or launch a costly proof.

Before proof funding, price the actual stage mix using retained matched-po18
stage evidence or justified per-stage bounds. For the same single assumption,
reducing segments from S_G to S_RC removes `3*(S_G-S_RC)` staged calls, but CPU
price, one-time development/build cost, certificate reception and custody costs
must remain explicit. Do not count a capsule as a certificate or claim full-cost
growth from padded-row savings. A proof-funding decision is separate.

Build and execute envelopes can reuse the already qualified finite envelopes:
guest build240 worker CPU/300 wall seconds and4GiB cap; snapshot arm180 CPU/
240 wall/3GiB and one120-second child timeout,2^26 cycles,po18,N256 structural
maximum. These are upper limits, not a new hardware requirement or reason to
survey RAM. The old four-crate typed build actually used41.921875 worker CPU
seconds,8.21875 controller CPU and49.8854 wall seconds. Do not extrapolate those
into a guarantee. Reuse defaults once; refuse failure without automatic retries.

## Proposed disjoint ownership

- Growth, after root selection: fresh `restricted_guest/{recipes,build}.py`,
  adapting retained strict recipes to three compiles and the isolated240-file
  dependency view. No new checker source or guest entry.
- Release: minimal RC wire preparation and fresh snapshot-host link adapter,
  preserving native preflight and unchanged host/receipt source.
- Root: exact selections/callers, small assembly adapter, one matched-pair
  preparation/launch, adoption and trust-profile decisions. The two arms can
  remain separate fresh outputs even under one paired selector.
- Adaptive: source closure/assumption review, then actual same-target and full
  accounting audit. Do not repeat unchanged network/custody/SDK suites.

These names are proposals, not assignments or runtime authorization. Root may
consolidate small adapters instead of expanding a hierarchy. The imax correction
is separately justified in IMAX-ADDENDUM; the stable core is otherwise unchanged.
