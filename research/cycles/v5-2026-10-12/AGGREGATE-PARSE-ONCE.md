# Aggregate parse-once successor

2026-10-12. Root-selected **source-only** implementation following
[AFFORDABILITY-NEXT](AFFORDABILITY-NEXT.md). No compiler, test, guest, proof,
network or Git execution by this author. This is not an aggregate receipt or
a measured performance result. Frozen aggregate sources remain unchanged.

## Exact scope and source map

Fresh source directory: `software/v5/aggregate_parse_once/`.

| File | SHA-256 |
|---|---|
| `lib.rs` | `6dfb8c28220d074a41492274bcb90fc337b78b354b3b5fdf56ad5d103d43a315` |
| `census.rs` | `88e9796bbb5493187f541d40e7c777afa8bfd4059929a9a2a1f118cfae815b04` |
| `relation.rs` | `5f3733fec79c7ed68d5476b8e804dc7c303aea097b7fa6b92eb98e03d1be2103` |
| `parse_once_controls.rs` | `635b9c234e66c6931838dd131510c7c9d4a548acd965f9b0912f1100f1512c6e` |

Only two production functions change:

1. `Census::charge(bytes)` returns `R<Value>` instead of `R<()>`. Its entire
   strict parse, traversal, field selection, checked addition and error sequence
   is unchanged. Its final `Ok(())` becomes `Ok(value)`.
2. The relation binds that return value and moves it into the unchanged public
   `module_relation::check(value)`, instead of reparsing identical bytes with
   `module_relation::check_bytes(bytes)`.

The updated source comments explain the ownership/canonical-size boundary.
The sole other relation-file difference is its test-only path to unchanged
`../aggregate/graph_controls.rs`. A read-only exact string comparison, after
normalizing CRLF/LF in memory, confirms that these are the only census/relation
changes. Original bytes were not normalized or rewritten.

The fresh lib path-reuses the following frozen files. Every build must pin and
snapshot these actual inputs while preserving the sibling directory layout;
pinning only the fresh four-file directory is insufficient.

| Unchanged file under `software/v5/aggregate/` | SHA-256 |
|---|---|
| `header.rs` | `642167ddde6a6f134efff58a2ab270916ebe050f7d0f29acf69f8aaa3465a8e8` |
| `membership.rs` | `25e6a2fa86f4c095dd9bd76ce83de60c55405bc9d52eeec1c668e51c07e04b6d` |
| `wire.rs` | `2368990cb04186b0e01f3b2075cf7e0505ffaa26f4f2aef6680a342b39f7957d` |
| `tests.rs` (test only) | `6a784eb7781284e8560928a5b47089721dadc38ef725f31ba7c3d89d14e089ae` |
| `graph_controls.rs` (test only) | `7a055e63d1a4420ac8187f592342f4574e3604f5eff0a14510cc9526e924bec4` |
| `census.rs` (test-only reference) | `f6ab62fe777482acb913972a34689eeaec16ed99fedae584cc6b62f6e4ba18df` |

The current unchanged module-relation/checker dependency remains the exact
compiled source relation, not a callback or alternative native trust mode.
No validation-only theorem-proof optimization, arena format, parser narrowing,
new public trust token, new journal profile or Cargo/backend migration is here.

## Equivalence argument

Fix the immutable bytes b of one delta frame and the pinned parser features.
Let P(b) be `parse_validated(b)`, S(V) be `canonical_size(V)`, C(c,V) be the
census operation on prior state c, and R(V) be the private unchanged
`module_relation::check_bound(V)`. All comparison claims exclude allocator/
process exhaustion, unsafe-runtime faults and timing; those stay subject to
the separately selected execution envelope.

Before:

    V = P(b); c' = C(c,V); drop(V); U = P(b); result = R(U).

After:

    V = P(b); c' = C(c,V); S(V); result = R(V).

P already executes S. Thus successful P(b)=V establishes S(V) succeeds. The
census borrows but does not mutate V. P is deterministic on the fixed bytes,
so a second successful parse yields U=V. The new call therefore supplies the
same Value to the same relation body. Both versions retain **two** complete
canonical-size traversals; this successor removes neither of them.

Failure cases are preserved:

- If the first parse refuses, both refuse with unchanged prior census state.
- If the census refuses, both execute the identical traversal/assertion order
  and leave identical failed-prefix counters. No relation is invoked.
- If both succeed, the omitted second raw parse cannot newly reject these
  unchanged bytes except through excluded resource/runtime effects. The retained
  public Value entry's size check cannot reject the unchanged validated V.
- A later relation refusal or native checker panic is produced by the same
  relation on the same semantic input. No exceptional path constructs a
  `ConditionalConclusion` or upgrades a native result into receipt authority.

The raw duplicate-key, integer-only, byte, default serde nesting and exact EOF
checks still occur once before a Value can reach the census. There is no public
entry accepting a caller's prevalidated assertion. An immutable local byte frame
cannot gain new duplicate keys between those same-process operations.

Induct on ordered delta frames. The base graph/census is identical. The argument
above preserves each delta journal and ordered exact returned parent journals,
and the unchanged `Graph::delta` preserves graph state/edges. Consequently final
target closure, unused-material refusals, sorted member journals, membership
commitment, maximum rank, seal height, receipt assumptions, census and consumed
wire bytes all agree. Header/profile/image/policy/whole-wire checks and private
construction are unchanged. This covers accepted-input sets and all exported
conditional data, not only a selected sample.

Cryptographic soundness assumptions do not change. A future compiled guest still
has a **new actual image**: old receipts are not silently certificates for it.
The eventual receiver must bind the adopted new image A, even though internal
184-byte I journals, ModuleIDs and semantic conclusions remain identical.

## What work is removed

One strict raw JSON parse, one full Value-tree construction and one tree
destruction disappear per delta. All canonical-size passes and aggregate
counters remain. Peak memory need not halve: the old extra tree was dropped
before its second parse. No claim of node-before-allocation, reduced native
proof work, fewer guest segments or lower total proving cost follows yet.

## Focused controls, not an unchanged campaign

`parse_once_controls.rs` contains five unexecuted test groups:

1. Named/positional records and noncanonical spelling/key order/Unicode escapes
   return exactly the same strict-parsed Value and census.
2. Duplicate keys, invalid integers/UTF-8/Unicode escapes, truncation, trailing
   input and the raw byte cap preserve strict refusal and initial counters.
3. Wrong record shapes and deep raw structures preserve exact partial counters
   and error results; no claim that serde depth equals the aggregate depth cap.
4. Global row/body/opening/edge/node caps, usize overflow and success followed
   by a cumulative refusal preserve the entire state at the failing boundary.
5. Both safe public relation-entry paths produce the same early relation refusal
   and census on named and positional shape-only records.

They use the frozen census source as reference, not a hand-rewritten imitation.
Its edge maximum refers to the unchanged `MAX_EDGES=128`. The new test-only
observation helper compares exact journal/parent bytes if supplied a successful
relation result, and catches diagnostic panics without granting authority.
Current unit fixtures deliberately do not fabricate accepted mathematics.

Original nine graph/Merkle/header controls are compiled through path references
for source compatibility but need not execute again. Run only the test filter
`parse_once_controls::` in a later root-selected operation. Actual mathematical
equivalence is compared to preserved controls02 output as below, with no rerun
of the old positive or its unchanged structural suite.

## Minimum retained-rlib build proposal

No runtime is authorized by this proposal. Use one fresh exact source snapshot
and selected finite Windows Job controller. Retain the successful build01
`libdmkn_module_relation.rlib`, SHA-256
`3d37e6dc700a7e789f8c0aa5f732ae6a7a4d8f46fd3ec9293f9d19bd35b31c0e`,
and all of its pinned checker/dependency/runtime provenance. Do not rebuild
that relation, the native checker, cryptographic dependencies or Cargo graph.

Only three compiler commands are needed:

1. Fresh aggregate rlib from `aggregate_parse_once/lib.rs`, retaining the same
   dependency inputs/flags and crate alias used by the original native driver.
2. Fresh `--test` executable from that lib and its pinned test-only paths.
3. Fresh native driver from the unchanged `aggregate/native.rs` (SHA-256
   `b153bdd3ae6be389b1e81d4731bfc7c1fcff22ce64eacb2668f54e835e2195ad`),
   linking the fresh aggregate rlib rather than the old one.

Retain explicit `-C lto=fat` for both final executable links; its absence caused
the preserved original build01 failure. Keep `embed-bitcode`, selected native
target/linker/libs, overflow checks and unwind behavior. Root should derive the
commands from the reviewed retained recipe and independently inspect every
changed source/output/rlib argument, not regenerate the environment or use a
glob selecting an arbitrary dependency version. All outputs are fresh paths.

Suggested maximum envelope remains no larger than the earlier compile phase:
240 aggregate worker CPU / 240 phase wall seconds, 3072 MiB, six processes,
plus at most 60 controller CPU and 600 overall wall seconds. This is a proposed
upper bound, not a new allocation or promise of success. Root may choose less.
Preserve exact Job closure/log/finalization checks and owned telemetry cleanup.

## Minimum changed-boundary native comparison

Root reports original controls02 PASS; its independent actual audit is separate.
The two retained actual inputs and expected output bytes already exist:

| Path relative to `experiments/v5-local-checks/aggregate-native-controls-02/evidence/` | SHA-256 |
|---|---|
| `actual-two-delta.bin` | `cec1e5fc3e211bd367a9171c2a398e2a1218e627f96d28848d60c9366746c808` |
| `cross-language-vectors.json` | `877f8d8b92d9b54c28ac7ab18949c22e302880d8a0dcec9781620a0a71347364` |
| `actual-two-delta/stdout.txt` | `877f8d8b92d9b54c28ac7ab18949c22e302880d8a0dcec9781620a0a71347364` |
| `invalid-proof.bin` | `112bf21c3d0ad44bbf6af9263ba5371810a9f284c2861f7db866e739f75417bc` |
| `invalid-proof/stdout.txt` | `42d71010ea316cdbce83b22f2ce5ef77ced0dda6a980802091de6bb15134205d` |

After source/build review, one fresh filtered test call and two fresh native
driver calls suffice. Positive output must match the complete retained JSON
value (or exact stdout bytes), including exact header, assumptions, all member
journals/openings, census, edges and input/wire binding. The negative must
return the same refusal with exit2, no mathematical admission and clean closure.
This is a new changed-entry comparison, not a repeat of the old implementation.

The graph missing-premise/wrong-rank and old nine structural controls do not
need reexecution: their implementation paths are unchanged and their retained
evidence is reused. A filtered test run must assert exactly the five intended
new cases passed; filtering everything away cannot count as success. Keep
outputs bounded and bind exact config/source/helper/runtime/binary/input files.

For those three workers a prospective envelope could keep the former individual
30 CPU / 60 wall-second limits (at most 90 worker CPU total), with at most 60
controller CPU and a separately chosen finite overall wall limit. No actual
receipt verification, authoring, guest execution, proof generation or network
request is needed. Passing this comparison supports representation equivalence
at the tested boundary, not an aggregate receipt, performance claim or v5 release.

## Independent source review

Assurance independently clears all four exact fresh hashes above: minimal
production diff, unchanged raw parser/counters, failed-prefix control checks,
relative source paths and original-test call compatibility. It agrees that only
the five new filtered groups and fresh output comparison are needed. This is
source clearance, not a compiler/control outcome or runtime selection.

## Implemented build and focused-control adapters

Root subsequently selected source-only adapters; both are implemented, unrun
and awaiting independent source/config review:

| Fresh file | SHA-256 |
|---|---|
| `aggregate_parse_once/build_native.py` | `7299aacdfbba7f24e79d24a64e597ba8d438349d9a327528e51c67321c950164` |
| `aggregate_parse_once/native_controls.py` | `4a95fee974a069a1f5d4f3f9fe19eddf521260e4a979086bf14e1e8ed3811274` |

Build config fields are exactly `schema`, `name`,
`authorizes_compile_only:true`, `sources`. Schema is
`DMKN_V5_AGGREGATE_PARSE_ONCE_BUILD_V1`; name matches
`aggregate-parse-once-build-[0-9]{2}`. Sources maps canonical-relative filenames
to `{bytes,sha256}`. Its exact twelve-file set is:

- Fresh `aggregate_parse_once/`: `lib.rs`, `census.rs`, `relation.rs`,
  `parse_once_controls.rs`, `build_native.py`.
- Frozen `aggregate/`: `header.rs`, `membership.rs`, `wire.rs`, `tests.rs`,
  `graph_controls.rs`, `census.rs`, `native.rs`.

The builder enforces frozen shared pins against retained build01's source map.
It derives exactly the aggregate rlib, tests and driver commands from retained
build01's pinned recipe, changing selected source/output arguments, the driver's
aggregate rlib binding, and adding fat LTO to the two final links. It validates
the retained module rlib's successful command, preserves the old FAIL and reuses
all exact runtime/helper/dependency pins. It snapshots the complete selected
source layout and rechecks both old and new snapshots. Existing compile phase
and finalization/owned-telemetry containment are reused unchanged.

Controls config fields are exactly `schema`, `native`, `tests`, `runtime_pins`,
`output_directory`. Schema is `DMKN_V5_AGGREGATE_PARSE_ONCE_CONTROLS_V1`;
native/tests/runtime file pins use `{path,bytes,sha256}`. Required runtime pins
are its actual controller, Python executable/DLL and the two selected binaries.
Only standard-library modules and three exact manifest-pinned frozen supervisor
modules are loaded; there is no eager import of any v5 package. The fixed input/
reference paths and hashes above are encoded and rechecked by the controller.

One new unit invocation must report exactly the five named new cases and nine
filtered old cases. Two new driver calls must byte-match the frozen positive
and negative stdout, with expected exits0/2 and clean Jobs. It does not invoke
any old executable, rebuild/recreate mathematical fixtures, verify receipts,
author Lean, run a guest or produce proofs. Generated input copies are verified
after each call and again at finalization. At most three workers each30CPU/
60wall are selected, at most90workerCPU+60controllerCPU/600totalwall, with the
former memory/process/log/output bounds and overriding finalization-failure
marker. Root owns actual config/source selection and launch.

Root's invocation review removed the controls' direct-source `__file__`
equality so the immutable `Run-V5-Check.py` snapshot can execute it. Canonical
cwd, isolation and mandatory actual-controller-path runtime pin remain; SOURCE
continues to be protected from output overlap. The updated controls hash above
replaces the earlier unrun draft hash, not any used source. The compile adapter
continues its retained direct-source invocation model.
