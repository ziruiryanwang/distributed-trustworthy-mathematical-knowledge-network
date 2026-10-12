# Aggregate-DAG certificate implementation

2026-10-12. **Full v5 remains ACTIVE.** Root confirmed the later explicit user
resumption supersedes the completed guide/pause. This task is fresh aggregate
source implementation only: no build, runtime, proof, host adoption or release.
Canonical root is `E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Central decision and scope

[DELTA-SEALING-POLICY](DELTA-SEALING-POLICY.md) identifies why single-module
periodic sealing cannot skip intermediate certificates. The new guest checks a
bounded DAG of new extensions and verifies only its genuine certified boundary.
One aggregate application receipt is intended to replace intermediate receipts;
all new mathematical checking/proving remains charged. The old relation,
checker, image, 184-byte journals, frozen evidence and receivers stay unchanged.

Root assigns this author `software/v5/aggregate/` and this checkpoint. Assurance
independently reviews the new trust boundary. Genuine host/receiver integration
and any finite build/execution require later root selection. Membership alone,
native success, mocks and conditional conclusions never constitute a receipt.

## Exact first source profile

The crate uses the existing `dmkn_module_relation` as a path dependency and calls
its unchanged `relation::check_bytes` directly. No caller-supplied checker or
verification callback can manufacture a relation conclusion. The new wrapper
must discharge every returned exact `(image,journal)` assumption with
`env::verify` before committing a header. The real final receiver must verify
the actual adopted aggregate image A and require the header's A to equal it.

Header `DMKNA001`, version 1, is exactly 192 bytes:

    magic[8], version:u32LE, A[32], I[32], foundation[32], policy[32],
    members_root[32], count:u32LE, maximum_rank:u64LE, seal_height:u64LE.

I is fixed to
`9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e`;
image words use the existing little-endian encoding. Foundation and policy are
computed by the unchanged adopted relation. A must be nonzero and distinct from
I. Mathematical rank and recursive seal height remain different quantities.

The wire stream starts with `DMKNAI01`, version 1, A and four u32LE counts
(assumptions, frontier selections, deltas, targets). Each assumption is tag 0
plus an exact legacy journal, or tag 1 plus an exact prior aggregate header.
Each frontier is assumption index:u32LE, exact J[184], member index:u32LE,
sibling count:u32LE, and that many 32-byte siblings. Legacy frontiers require
index zero, empty path and byte equality to the assumption journal. Aggregate
frontiers require an exact membership proof. Targets are 32-byte ModuleIDs.
Then each delta is a u32LE length followed by unchanged complete witness bytes.
EOF is exact. Receipt bodies are SDK witnesses, not fields in this stream.

Bounds: 16 MiB entire framed stream, 8 unique crypto claims, 32 selected frontier
members, 16 deltas, 48 total members, 128 edges, 250,000 rows, 8,192 bodies,
4,096 imported-group openings, 500,000 JSON Values and depth 128, with stricter
existing parser limits retained. Checked arithmetic applies globally. A frame
length must fit the remaining wire budget before allocation. Only one witness
is parsed/checked at a time; the preliminary census tree is dropped before the
unchanged relation parses it. This is not a proved resident-memory/cycle bound.

Members are sorted by ModuleID with duplicates refused. Domain-separated SHA-256
leaves bind count, index and exact J; ordered node hashes bind count and level.
Odd widths duplicate the last node, and openings explicitly require its sibling
to equal that node. A separately domain-separated root binds count and top hash.
Path length, index, member profile and rank bound are checked.

The private graph accepts only selected frontier journals or real returned
relation conclusions. Every exact returned parent must already exist. Targets
are nonempty, unique and newly checked. Backward reachability must exhaust all
supplied members, which also implies every descriptor and selection is used.
The new height is checked `1 + max(prior aggregate heights)`, default max zero.

## Status

The Rust library, guest wrapper, source controls and API are implemented and
submitted for independent source review. No build/test/runtime/proof has run;
no aggregate image, receipt or mathematical aggregate authority exists yet.
Root separately owns `aggregate/bindings.py`; this author does not edit it.

The census is deliberately an additional inexpensive structural precheck: it
uses the retained bounded raw-input parser, then checks cumulative Values/depth,
rows/bodies/openings/parent edges. JSON Values are allocated before that census;
only the frame byte vector has a before-allocation wire-budget check. This is
not a claim of bounded resident memory without the later process envelope.
Actual returned edge count must equal the preliminary census.

Stable source review set (SHA-256):

| File under `software/v5/aggregate/` | SHA-256 |
|---|---|
| `Cargo.toml` | `58d5d9d2ccfde1c060948c9c2ef5978175c809ac187defb8e8c1573a409b9363` |
| `lib.rs` | `ae71c52390fd47fa3b0cb130b289ff19629bbd8cb976f59c0042e1aabb95c340` |
| `header.rs` | `642167ddde6a6f134efff58a2ab270916ebe050f7d0f29acf69f8aaa3465a8e8` |
| `membership.rs` | `25e6a2fa86f4c095dd9bd76ce83de60c55405bc9d52eeec1c668e51c07e04b6d` |
| `wire.rs` | `2368990cb04186b0e01f3b2075cf7e0505ffaa26f4f2aef6680a342b39f7957d` |
| `census.rs` | `f6ab62fe777482acb913972a34689eeaec16ed99fedae584cc6b62f6e4ba18df` |
| `relation.rs` | `0f4e240727511764ef4b86a8185c55eb310b89396dece2e8f12fca055bc3460b` |
| `main.rs` | `d7b9b93843b683215e0556e585bc5ea241c672fe4c2a89cc07afa41afb81acad` |
| `tests.rs` | `6a784eb7781284e8560928a5b47089721dadc38ef725f31ba7c3d89d14e089ae` |
| `graph_controls.rs` | `7a055e63d1a4420ac8187f592342f4574e3604f5eff0a14510cc9526e924bec4` |
| `API.md` | `90b14c1d415a4f01c80ee4237551d2554b2610c71f4c4f233a19e507d824431e` |

The source controls use fabricated *structural* journals only for isolated
commitment/graph bookkeeping; no test-only callback is present in production.
The actual corrected two-delta fixture is retained at
`experiments/v5-local-checks/delta-reprepare-01/evidence/delta-packet.json`.
Root can later select that fixture for genuine unchanged-checker native controls
without repeating ordinary Lean authoring. Any new guest/proof still requires a
separate finite selection and feasibility decision.

## Independent review and cross-language source correspondence

Assurance reports a narrow source-review pass for the eleven-file set above:
actual unchanged-checker call, exact pending SDK assumptions, bounded topology,
rank/closure/height, membership hashing and input limits. This is not compilation
or execution evidence. The two draft test syntax defects were corrected before
the stable hash set; no failed build was hidden or rerun.

This author read root's `aggregate/bindings.py`, SHA-256
`d749273ef5841afe881407bcb3c2655385dd635bdae12b37e09ca2381a46bcd5`,
and its actual `admission.bindings.journal` / `modules.codec` dependencies.
Its source encoding agrees with Rust on the complete 192-byte layout, fixed I,
foundation/policy, positive height/count, strict ModuleID order, exact LE fields,
all three SHA domain strings, count/index/level framing, duplicate-last padding,
exact path depth and rank bound. Lowercase hex digest order equals raw-byte
lexicographic order. Both explicitly provide only inert bindings, not authority.
Cross-language runtime vectors are still unexecuted.

## Proposed smallest next native discriminator (not selected runtime)

Use fresh output roots and the existing bounded Windows Job supervisor. Snapshot
and pin the exact new source and its unchanged relation dependencies; retain all
results even on failure. No Cargo dependency resolution/download or full checker
rebuild is needed. The current retained native checker is:

`experiments/v5-local-checks/native-library-02/libnanoda_lib.rlib`, SHA-256
`ba6d0db2e614c2bb032ca5d92d97d31a7ebfe87f85fa6cce6fe5549483b7c651`.

1. Compile unchanged `modules/receipt/src/lib.rs` once as
   `dmkn_module_relation.rlib`, using library02 and exactly retained native
   serde/serde_json/RISC0 dependencies from delta-native-build02. This compiles
   only the thin existing relation/codec, not `nanoda_lib` or the cryptosystem.
2. Compile `aggregate/lib.rs --test` against that retained/newly pinned rlib and
   run the nine source-control groups once. The test-only synthetic journals and
   graph statements remain structural evidence, not mathematical admission.
3. If required for the actual fixture, compile a small fresh native driver that
   exposes only `check INPUT`, invokes this exact aggregate relation, and emits
   its conditional header, pending claims, sorted member journals and openings.
   It must explicitly report `mathematical_admission=false`, bind exact input
   bytes, catch checker panics as refusal, and never verify imaginary receipts.
   No new public receipt authority or production host is warranted by this step.
4. Construct one framed input from the already accepted corrected two-delta
   packet, retaining its exact witnesses, exact base journal and second target.
   Use an explicitly synthetic distinct A only for native structural checking.
   Confirm all three exact member journals and three actual dependency edges,
   rank 2, height 1 and one pending I claim; compare Python and Rust header/root/
   every membership opening. The source relation verifies the mathematics of
   both new witnesses conditionally, but this call alone discharges no receipt.
5. Narrow negatives: one tampered actual proof, reversed/missing exact delta
   premise, changed member/path/header, unused frontier or target, and trailing
   input. Reuse unit-source negatives for purely structural cases instead of
   adding needless actual checker executions. Every path remains finite and
   globally accounted; no Lean reauthoring or base receipt proving repeats.

The preceding first proposal was refined after root's explicit next source
assignment: the implemented compile-only controller has **four** thin compiler
commands (unchanged relation rlib, aggregate rlib, tests, driver). The fourth
artifact is needed so the driver links the exact reusable aggregate rlib rather
than an independently copied relation. They share one 240 CPU / 240 wall-second,
3072 MiB, six-process worker phase, with at most 60 additional controller CPU
seconds and 600 overall wall seconds. This fits root's 300 CPU / 600 wall bound.
No compiler command rebuilds the checker or invokes Cargo. Specific retained
MSVC Job-owned telemetry cleanup is reused; no general process cleanup exists.

The separate source-only control controller selects one nine-group unit binary
and four actual native calls: positive two-delta, missing first premise, wrong
rank and changed theorem proof. Each worker reserves at most 30 CPU / 60 wall
seconds, with 150 worker CPU total and at most 60 controller CPU. The retained
packet is reused; no real receipt is reverified by these conditional tests.
Actual Python/Rust header/root/member openings and global census must agree.
The input encoder is root-owned `aggregate/input.py`, not a duplicate codec.
Original wall/CPU and output bounds are rechecked after final report writes;
a finalization failure writes an overriding marker and returns nonzero. Neither
source controller has been selected or executed by this author.

Source-only native additions, independently reviewed:

| File | SHA-256 |
|---|---|
| `aggregate/native.rs` | `b153bdd3ae6be389b1e81d4731bfc7c1fcff22ce64eacb2668f54e835e2195ad` |
| `aggregate/build_native.py` | `4b77bad55119746df2e66cf7b8336b62ee1db8bfa4dca7152b6c1512b4ad892a` |
| `aggregate/native_controls.py` | `a92e2bfb21e81c0a5dcae6713fc5d7a929723828111bbab797b356f41a6914c5` |

The compile controller's exact source set is its ten `AGGREGATE` names plus
nine `RELATION` names; its root-selected config schema is
`DMKN_V5_AGGREGATE_BUILD_V1`, with `name`, `authorizes_compile_only:true`, and
`sources` mapping each canonical-relative path to `{bytes,sha256}`. It retains
the old reviewed recipe/runtimes and checks all source/runtime pins before/after.

The control config schema is `DMKN_V5_AGGREGATE_NATIVE_CONTROLS_V1`, with exact
`packet`, `native`, `tests` file pins; `runtime_pins` list; and a fresh canonical
`output_directory`. Required runtime pins include the executed controller,
actual Python executable/DLL, both actual binaries, and the loaded aggregate
bindings/input, admission bindings, delta packet, module codec and production
producer sources. Additional imported package files can be pinned too. The
fixed frozen supervisor manifest independently binds its three loaded modules.
All controls use a clearly synthetic A (`07000000` repeated eight times), not
an invented genuine aggregate image or receipt.

Assurance source-cleared the build/controller pair and provisionally found no
blocking issue in the complete control source. Runtime clearance remains a
separate exact binary/config/pin review after a successful build. The author
has performed zero compiler, test, guest, receipt, proof or network executions.

Only a later separately reviewed aggregate guest execution-only screen can
estimate real proving feasibility. The previous one-child guest exceeded 2^25
cycles, so a quick native pass cannot authorize an aggregate proof or predict
its cost. The intended application benefit is avoided *intermediate receipt*
production; actual full-batch proving and surviving frontier/service costs must
still beat the selected optimized-library comparator in a nonempty workload
region. No inequality or workload result has been manufactured by this proposal.
