# Typed-row controls and selector: focused source review

2026-10-20, reviewer `core_growth`. Scope: final control wrapper, compile
selection script and the eight Rust controls, including exact fixture binding
and source closure. `core_search` separately reviews compiler recipe details;
this does not repeat that build audit or the general architecture review.
Only source/data reads and this checkpoint were performed. No selector,
compiler, tests, native checker, proof or RAM probe ran.

## Disposition and reviewed bytes

**No blocking source defect found in the scoped adapters/controls.** A future
control launch still needs the separately selected successful binary and exact
outer runtime map. These source findings do not authorize execution or establish
passing tests.

| File | SHA-256 |
|---|---|
| `software/v5/typed_rows/run_controls.py` | `60e9f67454b5e305f5379c4856177498f9aa2309df037fe6e78f12dc7bcb56b0` |
| `software/v5/typed_rows/controls.rs` | `4de1694aa8a90b83ffae9afa8f57fd7016e9a87509a6b4b6f9163d23301d2e02` |
| `software/v5/typed_rows/controls_root.rs` | `5c0232d74e052e55d159803d57c1246fab5c10c3141abddc24d649e8d297bb68` |
| `research/cycles/v5-2026-10-20/Select-TypedRowsBuild.ps1` | `06305d440041c42ab7b147286437f525bebc88eb1ee9f54ee21554c69695c9f2` |

The earlier wrapper hash `1d5c2f2b` is superseded before execution by the final
Windows-environment/stack configuration above, which was reread completely.

## Wrapper boundary

The wrapper requires canonical cwd, Windows and isolated/no-site/no-bytecode
Python with optimization disabled. It runs only from the outer local-check
`sources` snapshot. Binary and fresh output resolve under the canonical
`experiments/v5-local-checks` tree; the binary's exact caller-selected SHA-256
is checked before and after execution. No shell command is constructed.

Exactly one direct test process runs with `--test-threads=1` and a 60-second
inner wall timeout. It inherits the existing outer Job; there is no new Job,
budget renewal, retry or proof operation. The child environment is now an
explicit Windows allowlist plus System32 PATH, the three fixture paths,
`RUST_BACKTRACE=0` and `RUST_MIN_STACK=16777216`. The last matches the retained
checker-thread stack and changes only this child, not machine configuration.

On successful subprocess return, wrapper acceptance requires exit zero, exactly
the selected number of distinct `test ... ok` lines, and a matching harness
summary with **zero failed, ignored, measured and filtered tests**. The actual
control source has eight `#[test]` functions; the future selection must pass
`--expected-tests 8`. No test treats missing fixtures as an optional skip.

The wrapper checks fixture hashes again after normal completion and bounds each
saved log to 1 MiB before reading it. That is a final log-size check, not a live
disk limiter. On timeout/exception it fails without creating a successful result;
the original outer Job and report own final process containment and failure
accounting. Therefore the final control selection must also pin the binary and
all three fixtures in its outer runtime map for post-failure binding checks.
Do not describe the wrapper as a security sandbox or a complete disk quota.

The outer runner creates `{output}` before launching the snapshot. Because this
wrapper requires a fresh output directory, its argument must be a new child
such as **`{output}/evidence`**, not `{output}` itself. This is a launch-map
precondition, not a reason to weaken the wrapper's freshness check.

## Retained data: actual paths, hashes and schemas

I rehashed all three on-disk fixtures with read-only file operations. Their
actual lengths satisfy both the wrapper's 1 MiB limit and each Rust control's
more specific limit.

| Fixture under `experiments/v5-local-checks/` | Bytes | Exact SHA-256 |
|---|---:|---|
| `delta-reprepare-01/evidence/delta-packet.json` | 662,480 | `54c7dac7f83a9a06c2b23b17a77be20364c1b90e4cd3b1db58b69c62fda2dcf1` |
| `aggregate-claims-controls-02/evidence/actual-two-delta.bin` | 215,540 | `7e21d092206b08a9a71231045b8152df4179ee6575cdc5e3afc704ef03c0be58` |
| `aggregate-claims-controls-02/evidence/actual-two-delta/stdout.txt` | 4,444 | `01d7c9cc45a16f520980e80672f90c0a97a69e31e344f748910df5abb24ffd0b` |

The packet's retained `deltas` array is the two module inputs, not an aggregate
wire. The binary is the exact aggregate input. The expected text is the retained
`DMKN_NATIVE_AGGREGATE_CONCLUSION_V1` object, including header, assumptions,
member journals, census, edges and wire bytes. These paths/schema roles align
with the controls; no old runtime packet is confused with a receipt or proof.

The Rust helper independently checks each required file's existence, file type,
size and hash before reading its semantics. The first positive compares the
two actual retained frames using both `legacy_relation::check_bytes` and new
`module_relation::check_bytes`, requires exact journal encodings and ordered
parent-premise sequences, and requires 930/583 typed suffix rows with total
1,355/1,009 rows. Its accumulated census is pinned to
`[rows=2364,bodies=22,openings=23,edges=3,nodes=29858,depth=28]`.

The aggregate positive consumes the exact retained binary, not reconstructed
JSON. It compares exact header bytes, ordered assumptions, ordered member
journals, all six census fields, edge count and wire length to the saved old
output. It does not rebuild/rerun the old graph just to recreate that oracle.
The old oracle is explicitly non-admission; no new certificate follows.

## What the eight controls actually establish if they pass

- All fourteen variants compare direct native mapping against the actual old
  decoder, plus virtual old counts. Additional cases cover both binder variants
  and all four styles, target `usize::MAX`, Unicode, `nondep=true` and universe
  order. Generic dummy foundation here is intentionally syntax-only.
- Generic declaration metadata and invalid non-row typed fields survive the
  decoder unextracted. The 257-universe case checks no new decoder-wide arity
  refusal; it is not evidence that such an expression is semantically valid.
- Duplicate/escaped-equivalent keys, negative/float/exponent numbers, invalid
  Unicode/UTF-8, EOF and width boundaries are tested against old strict parsing
  or literal fallback as appropriate.
- Nested generic data compares old/new default parser recursion behavior.
- The actual old census code is compiled beside the new census. Tests compare
  success, exact first refusal and all partial counters at equality, overflow,
  malformed shape and sequential-parent failure boundaries.
- Unsupported raw forms select `Prepared::Legacy`; supported invalid
  schema/foundation forms remain typed then produce the same semantic error.
  The source dispatch structure, reviewed separately, establishes no semantic
  retry; identical errors alone would not prove that property.
- The final two controls perform the retained module and aggregate comparisons
  described above. Neither bypasses the mathematical checker with a mocked
  success flag.

These are finite changed-boundary tests, not exhaustive equivalence or performance
proofs. In particular the arity/nondep tests establish decoder behavior, not
every possible reached/unused kernel case. Source-level consumer simulation and
the retained actual positives supply the complementary justification.

## Compile-selection source closure

The selector's 39 unique relative source entries match the builder's declared
`FRESH | REUSED` set: 14 fresh files, five receipt inputs, three aggregate files,
three bounded-parse files, one legacy memo correspondence and thirteen unchanged
checker modules. The new test root links production crates and includes only
new census, old census and controls; it does not activate the checker's or old
aggregate's broad `cfg(test)` suites. The observed eight-test count is therefore
consistent with this wiring.

All non-test `#[path]`/`include!` dependencies in these roots are covered,
including retained foundation data. The old `tests.rs`, correspondence controls
and graph controls are behind disabled `cfg(test)` in their separately compiled
library crates; they are not missing runtime test inputs. `run_controls.py` is
not a compiler input and belongs in the later outer test source map instead.

The selector checks canonical cwd and the reviewed builder hash, refuses an
existing selection/run/attempt, gathers exact lengths/hashes and creates only
one fresh selection file with exclusive creation. It starts no compiler. It
does not by itself prove every freshly gathered hash is the already reviewed
one: root must compare the final generated map to the final reviewed sources
before selecting its hash for execution. Compiler recipes, reused runtime
objects and their finite budget remain `core_search`/root's separate scope.
