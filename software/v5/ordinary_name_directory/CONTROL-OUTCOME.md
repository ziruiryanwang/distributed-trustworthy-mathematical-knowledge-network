# Historical name-directory controls: saved outcome audit

2026-10-28, next_value. **PASS for the selected fourteen synthetic control
groups and recorded clean closure.** Root executed `name-directory-controls01`;
this audit inspected only retained selection, source snapshots, reports, logs
and synthetic output artifacts. No control was rerun, no product was imported,
and no owner/database, native worker, network or Git operation was performed.
The canonical workspace guard passed.

The auditor authored the controls; root independently reviewed their source and
selected execution. This is an independent check of the executor's retained
outcome, not a claim of independently authored tests. Root found the test-only
generic-feature-validator mismatch before execution. The selected corrected
bytes retain exact ordinary portable-symbol spec comparisons. No failed runtime
was removed or relabeled.

## Selected and observed evidence

All evidence below is beneath
`experiments/v5-local-checks/name-directory-controls01`.

| Retained file | SHA-256 |
|---|---|
| `selection.json` | `77175abf4214416a28a559cd39fef716573f96a765e2bd9a355a6fac6b1affd0` |
| `RESULT.json` | `7c85c8d4f959609b1ee15392fb552611c8971b0130d8bed0a83df77077858f48` |
| `controls/RESULT.json` | `a61447a598c0691d1f55f45113935b09b1362f08ff453a92bd6d9c9c809e07d5` |
| `command/command.json` | `97f8e32d9ca68a32df67edae9be72f28d4c63b6df0d7ae9bd5e853f4e371bc99` |
| `command/stdout.txt` | `42843a3e955c9e47472d9a5f75939838e71958412049a8400b796b778d10508f` |

The outer report's selection hash matches the actual selection bytes. The
command matches the selected argv after substituting the recorded snapshot and
output roots, and agrees with the outer report. It uses the selected Python with
`-I -S -B`, the six explicit source/path pins and the fresh synthetic output.
Stdout is exactly the 2,554-byte controls result followed by CRLF; stderr is empty.

All eight selected source snapshots match their selection hashes and the current
frozen source files. The controls' six captured-source pins also match the actual
snapshot files. No unselected source change is needed to obtain this pass.

| Selected source | SHA-256 |
|---|---|
| `directory_index.py` | `bd0a1fcced90c694943dc902a61cae7220c3bdf7ad0ed6c0bd464b9fbe992447` |
| `query.py` | `322f6d4202c0aca09e7ccb6d33b1bd7c2651776474bbfefeccfc8ab88e8781dd` |
| `advisory_context.py` | `42a4b204e8a2a579d49b70981b539feb7a2417bb9bc40b2b47d5883d0b4e6193` |
| `controls.py` | `831b897d5b12fd396c65e3c79a29bc3b0c816698cdd0eaefc5668bd61ab7aefb` |
| `ordinary_lean/ordinary_evidence.py` | `fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6` |
| `discovery/formal_features.py` | `f1f53ee40ce32126085f7f776c47d9d0ab2c5b7c679d40f018f6bff70f6430e5` |
| `discovery/authenticated_index.py` | `77a12cda9dd4a303153b59d00998de8aa6bf08bb572af10136e21dfa9c96cc95` |
| `tools/Run-V5-Check.py` | `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651` |

The selection records three runtime pins. This saved-outcome audit does not
rehash or certify a current runtime installation; explicit runtime selection is
not a hermetic toolchain proof.

## Actual control coverage

`controls/RESULT.json` reports `PASS_HISTORICAL_DIRECTORY_CONTROLS`, fourteen
groups, and `mathematical_acceptance:false`. Its ordered case list exactly
matches the fourteen successful-group append sites in the frozen controls.

1. Real-codec exact hits and five-record non-power-of-two layout.
2. Authenticated first/last/interior absence and no specs for a mixed request.
3. Corrupted midpoint steering cannot prove a false absence.
4. Changed row/sibling and short fixed-width read refusal.
5. Descriptor pin, count, context and file-size binding.
6. Identical entries cannot reuse a tree across historical metadata contexts.
7. Exact Unicode, numeric and dotted-component names; one-through-eight bounds.
8. Singleton zero-height paths and generic supported empty vector.
9. Deliberate digest collision, including equal SymbolIDs, refuses before write.
10. Final-gate failure prevents descriptor publication; existing output refuses.
11. Eight requests over 257 records satisfy counted fixed-read/byte bounds.
12. Existing query mode compatibility and invalid directory arguments before opening.
13. Actual shared advisory full-map/projection branches with inert lifecycle doubles.
14. Actual export orchestration with inert installation/owner doubles and real builder.

Saved artifacts agree with these assertions. The eight direct codec fixtures
have descriptor counts 0, 1, 5, 8 or 257 as intended, with exact entries/tree
lengths. The collision directory remains empty. The stopped-before-manifest
fixture retains its two payload files without a descriptor. Bad returned-root
and bad-closure caller fixtures have no export directory.

The good caller has a two-record complete export, descriptor SHA-256
`be8ed449895ea82d53c769560412f88e6127eeaee1da1566235987a1047d810f`, matching
its retained receipt. The final-profile-failure caller retains 128-byte entries
and a 96-byte tree but no descriptor. Its report has exact error
`CONTROL_FINAL_PROFILE_CHANGED`, phase `DIRECTORY_BUILD`, publication `UNKNOWN`,
owner closure `CLOSED`, and `ok:false`. This is the intended failure control;
it is not counted as a successful export.

Per-case transient lookup results/read counters are asserted by the frozen
controls but not individually saved. The PASS establishes those assertions ran;
the evidence does not supply an independent timing series or full-scale benchmark.
The caller doubles establish ordering and boundary handling, not real catalog
grounding, lock behavior, metadata lineage or mathematical acceptance.

## Closure and costs

The enclosing report records `COMMAND_EXITED_ZERO_AND_CLOSED`, child exit code
zero, direct child reaped, final active processes zero, Job closed, no termination
request and no cleanup errors. The two cumulative processes recorded by the Job
are distinct from its one-active-process ceiling. These are saved closure facts;
this audit did not launch a process probe or reopen any state.

Recorded Job CPU is **0.265625 seconds** (0.203125 user + 0.0625 kernel).
Outer wrapper CPU is **0.125 seconds**, yielding **0.390625 seconds known CPU**.
The nested 0.015625 supervision CPU and controls' 0.09375 self CPU are included
in those scopes and must not be added again. Outer elapsed time is 1.0552909
seconds; command-through-cleanup elapsed time is 1.0383673 seconds. Peak Job
private commitment is 25,079,808 bytes. Logs are 2,556 stdout bytes and zero stderr.

The selected ceilings were 60 wall seconds, 30 CPU seconds, 256 MiB, one active
process and 1 MiB per stream. The report retains the sampled wall/total-CPU/log
and physical-disk-limit qualifications. No hard disk-quota claim follows.

This pass qualifies the finite core and changed-caller controls only. Relocated
wrapper/package qualification, a real historical owner export, practical speedup,
current-state absence and final-v5 readiness do not follow. All used sources and
this run's evidence remain frozen; no rerun or further runtime is selected here.
