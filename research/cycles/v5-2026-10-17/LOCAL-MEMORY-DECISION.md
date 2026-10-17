# Local memory decision: one bounded build, proof remains separate

2026-10-17, `memo_independent_review`. Commissioned by
[LOCAL-RESUMPTION](LOCAL-RESUMPTION.md). Canonical workspace guard passed.
Source and retained-record analysis only: no compiler, test, proof, account,
environment or Git operation. This is the only file created by this assignment.

## Decision

The retained build measurements support **one prospectively selected serial
five-step compilation with a 2,048 MiB per-Job cap**, after the unused builder,
adopter, recipe and exact launch selection agree and receive review. Keep all
other limits, features, source/dependency identities and mathematical claims
unchanged. Root owns those edits and any execution; this note authorizes none.

Immediately before selection, require at least 1,024 MiB of observed physical
and system-commit headroom beyond the selected worker cap. Do not overlap it
with another large project Job. This is an operating-margin policy, not a
reservation of Windows resources or proof that unrelated applications cannot
grow. The controller and ordinary machine variability share that margin.

On a memory/CPU/wall/compiler refusal, preserve the output and re-decide from
the cause. Do not automatically retry, raise the cap, change features or replace
the selected inputs. A successful build still needs actual-result review and
does not fund a proof stage.

## Headroom arithmetic

Root's resumption observation was:

| Quantity | MiB |
|---|---:|
| Available physical: 3,539,072 KiB | 3,456.125 |
| System-commit headroom: 3,345,116 KiB | 3,266.71484375 |
| Commit remaining beyond the earlier 3,072 MiB build cap | 194.71484375 |
| Commit remaining beyond the proposed 2,048 MiB cap | 1,218.71484375 |
| Physical remaining beyond the proposed 2,048 MiB cap | 1,408.125 |

These readings change; recheck before launch. The earlier 3 GiB cap nearly
exhausts observed commit headroom before the controller and other activity.
The 2 GiB cap creates meaningful bounded headroom without buying resources or
changing the prover algorithm. It is a maximum allowed allocation, not a
prediction that compilation will consume that amount.

## Relevant completed build evidence

All values below are Windows Job **peak private commit**, not process working
sets. The old multi-command Job records report cumulative maxima: do not
subtract successive peak values to invent a per-command memory measurement.

| Retained operation | Observed peak bytes | MiB | Scope |
|---|---:|---:|---|
| `general-checker-host-05/build-01` | 1,475,215,360 | 1,406.875 | Complete retained SDK/Cargo host build; 1,332 total processes, clean closure |
| `small-aggregate-stage-host-build-01` | 1,233,174,528 | 1,176.046875 | Exact recent O3/fat-LTO stage-host compile/link; clean closure |
| `small-aggregate-snapshot-host-build-01` | 977,940,480 | 932.63671875 | Adjacent recent snapshot-host compile/link; context only, not a selected rebuild |
| `proof-validation-integration-build-01` | 695,197,696 | 662.9921875 | Four retained sequential compiles; clean closure |

The retained original Cargo artifact log explicitly records `fresh:false` for
both relevant SDK libraries: this was not merely a cached success. The circuit
crate has `execute/prove/std`; zkVM has
`client/commons-inprocess-only/disable-dev-mode/prove/std`. Both artifact rows
report release optimization 3, no debug assertions, no overflow checks and no
test build. These match the reviewed new SDK recipe's selected feature/profile
choices. The original Job peak includes their actual compilation and the
broader build around them.

In the integration build, the cumulative peak after module-relation was
589,680,640 bytes (562.36328125 MiB), unchanged after aggregate-relation. It is
an observed upper bound on each of those old command intervals, not an exact
isolated aggregate-relation peak. The new recipe rebuilds only those two
relations, not its old checker or old aggregate driver.

The proposed cap exceeds the largest relevant historical Job peak by
641.125 MiB. The new implementation uses five **disjoint serial** compiler
Jobs, so their memory maxima are not summed. Retained input manifests are
stream-hashed; compilation does not require loading the entire 2.32 GB runtime
manifest's contents into RAM at once.

### What the comparison does not prove

Steps 1-2 are new explicit direct-rustc recipes, not exact replay of unavailable
verbose Cargo command lines. The allocation patch, new metadata identities and
fresh downstream libraries can alter compiler behavior. The historical peaks
are therefore a strong practical reason to select one bounded build, **not a
formal upper bound or a guarantee that the new operation fits 2 GiB**. CPU,
wall and output limits also remain independent acceptance conditions.

## Why no proof is justified by this build decision

Reuse the completed allocation argument in
[SMALL-LAYOUT-FEASIBILITY](SMALL-LAYOUT-FEASIBILITY.md#appendix-po18-producer-memory-and-the-smallest-useful-correction):

- Uncorrected identified simultaneous po18 payload: 2,790.8466796875 MiB.
- Corrected identified payload: 2,331.8466796875 MiB.
- Structural requested-payload saving: 459 MiB; not a measured peak saving.
- The earlier different base-I po18 proof's approximately 3,371 MiB observed
  peak is not an upper bound for this aggregate.
- The retained po19 CPU path cannot fit its 4 GiB cap even after this correction.

At the resumption snapshot, the corrected **lower bound** leaves approximately
934.87 MiB of commit headroom. Exact circuit maxima, decoded capsule/parent
state, transcript/verifier overlap, allocator and thread state are additional;
their sum is not established below that margin. The existing 4 GiB proof cap
itself exceeds current system-commit headroom. A cap is not a reservation, but
the present evidence does not justify promising that a full worker can run
efficiently or safely within today's remaining capacity.

## Deliberate stop on non-decision-changing census

The finite D/A maxima remain computed in retained
`risc0/circuit/rv32im-sys/cxx/rv32im/emu/blocks.cpp` from all 43 template block
layouts and recursively traversed argument fields. They are not exposed as a
simple source literal. The selected retained base-proof text/JSON evidence
does not supply those tuning-log constants. Closing that census alone would
still leave the other live-state and allocator terms above. It cannot alone
establish an actual peak below available commit or remove the discrepancy
between the allowed 4 GiB envelope and today's observed headroom.

Consequently do not expand this assignment into a full circuit-layout census,
streaming redesign, smaller-geometry experiment or another proof-memory probe.
The decision-changing result is the historical compilation envelope. First
finish the new small adoption controls and the bounded build decision. A later
actual genuine full-po18 stage from the existing capsule is separate: no layout
replay, no duplicate preflight, no automatic 502-stage funding. The full v5
reciprocal-use and useful-growth goals remain open.

## Exact evidence identities read for this decision

Paths below are relative to the canonical project root; bytes were read and
hashed, not modified.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `experiments/general-checker-host-05/build-01/RESULT.json` | 5492 | `8f99425b382e027e1d14a3c6b6ecc82202492331c789557915314ddca7089de8` |
| `experiments/general-checker-host-05/build-01/commands/build-host/command.json` | 2619 | `e7854ccbd0b03fca1c8ab5523dcc9b256524c2358b5a72466daeb1ee2254fe41` |
| `experiments/general-checker-host-05/build-01/commands/build-host/stdout.txt` | 671667 | `5563fce251f5f5f35a446a0f629a73fc55f253f2a93a427cc8856eb82f0a2c85` |
| `experiments/v5-local-checks/proof-validation-integration-build-01/RESULT.json` | 27713 | `55ba9a702360dd10a6b9bea00f481d5066553a1b8debcb10ca43bbcab4de4069` |
| `experiments/v5-local-checks/small-aggregate-stage-host-build-01/RESULT.json` | 10359 | `2c201aa68a50ccc93c90f73ae8aba5d924cef858bbec900f858d738b0135e499` |
| `experiments/v5-local-checks/small-aggregate-snapshot-host-build-01/RESULT.json` | 10395 | `7ad07e35602092833d9f40e7f0775f0b4eceb451e52853875bd5baeaf63f78b1` |
