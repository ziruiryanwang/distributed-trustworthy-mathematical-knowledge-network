# Independent allocation-adoption controls review

2026-10-17, `memo_independent_review`. Canonical guard passed. Source and exact
plan inspection only at this checkpoint; no test, compiler or proof was run by
the reviewer. The assigned source author is `memo_tests_review`; root owns
execution and adoption. No product/test source was edited in this review.

## Source and cap-only delta: PASS within the stated scope

Reviewed `software/v5/prover_memory/test_adoption.py`, 18,581 bytes, SHA-256
`6540b348117da8b7d58f166b8987acd21f2dcb4a2323cc8fe0de52bb1ee8d26a`.
Reviewed `adoption.py`, 15,611 bytes, SHA-256
`b41fd140a13782be3258452ecee7c7389bf2b8621f24fdb4d21f64962b334176`.
Replacing only its memory-limit literal 2048 with 3072 **in memory** reproduces
the exact prior reviewed hash
`56b633aa0a528cb383f47cf5b1e73bd9a8b18387382c23d4c8114348b2cc6459`.
Thus this adopter change is exactly the prospective cap change, not a hidden
acceptance-rule rewrite. The tests derive the selected cap from `A.LIMITS`.

The seven methods meaningfully exercise the new seam:

- Positive adoption runs actual `adopt_build`, inherited record reads and both
  refined stage hooks. Exact source-map/command/environment derivation, output
  pinning, serial-Job accounting and support-source closure remain active.
- Refusals cover altered limits/counts/command shape and old-library command
  substitution; omitted/traversal/empty-code sources; changed empty evidence;
  environment/runtime-map disagreement; live Job, excessive phase wall time,
  incorrect CPU sum and summed rather than maximum serial peak; missing,
  duplicate, wrong-digest or wrong-origin support source.
- Separate controls check inherited snapshot delegation and cleanup of both
  refined wrappers after an injected constructor refusal. They do not claim to
  requalify the already tested full lifecycle constructor or snapshot path.

### Synthetic evidence is not confused with the real descriptor

The positive first checks the real copied `SOURCE.json` hash against the
unchanged production anchor
`c93a45a6a558718c931c39b121e9bcffa7d464ecaa1d5b0e80185efd6cace710`, and its
five step names/order. A scoped mock then substitutes **only** that anchor for
the synthetic descriptor. It does not replace the validation function. The
anchor is restored on scope exit, including refusal.

The miniature fixture does not contain all real SDK sources or actual compiler
outputs. Its 1,071-entry runtime inventory points to nonexistent inert paths;
this tests manifest equality without rehashing a compiler installation. Counts,
times, fake output bytes and authority/accounting labels are openly synthetic.
Consequently a passing suite qualifies software control behavior only, not a
real five-step build, toolchain execution, measured memory, proof or mathematics.

### File and process scope

Fixtures and mutations derive from one fresh absolute `--output` beneath the
canonical `experiments` tree. The traversal negative changes a JSON map key;
it does not construct an escaping file, and the real adopter rejects that key
before a file lookup. The only appended bytes are in the new synthetic empty
evidence fixture. No original source, predecessor artifact or SDK input is
written. Files use exclusive creation and remain as evidence.

The actual ordinary source closure is imported from the selected snapshot.
The suite uses an inert support object with real path/size/hash checks, not a
real supervisor. `subprocess.Popen` is denied while the suite runs; the selected
imported modules are existing definition-only code, not test/build entrypoints.
No compiler, host, guest, proof or network call is present in the test path.
The outer test's Python process is, of course, a selected supervised process;
the reported zero native-process calls refers to processes spawned by the suite.

## Exact plan review: PASS for one seven-control run

Reviewed selector `research/cycles/v5-2026-10-17/Select-AllocationControls01.ps1`,
3,451 bytes, SHA-256
`bc5c8358545666c09b42b17d0f2f30ce448a50e98837544b801b3b11faee871d`.
It creates only the new finite selection and refuses an existing selection or
run directory. It verifies the retained runtime map before preserving it.

Reviewed actual selection
`experiments/v5-local-checks/prover-allocation-adoption-controls-01-selection.json`,
SHA-256 `cfff2cdbb4817fb6935a78aabbdbdbe6b07913b1b1c2286351f0c5a418f76ef9`.
Independently rebound all **30 source pins and 18 runtime pins**. Source closure
is the 24 inherited lifecycle modules plus three refined modules, this test,
the real descriptor and the outer runner. The compiler builder is not selected
or imported. The run directory was absent at review.

The pinned runner is
`tools/Run-V5-Check.py` / `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651`.
Its reviewed expansion invokes the pinned installed Python with `-I -S -B`,
the copied test source and fresh `<run>/controls` output, from canonical cwd.
It snapshots selected sources, binds the selection/runtime, uses the retained
Windows supervisor and rebinds runtime/snapshot bytes after completion.

Selected limits are 30 inclusive worker CPU seconds, 90 wall seconds, 512 MiB,
two active processes and 1 MiB each stdout/stderr. This is one small changed-
boundary control run, not a compiler/proof or an old lifecycle campaign.
Root may select that exact operation; no other launch is cleared here.

## Actual outcome

Not yet reviewed at this source/plan checkpoint. A passing actual result must
show seven tests, zero failures/errors/skips, exact original/snapshot/runtime
bindings, copied-source import origins and clean process closure. Actual costs
must come from saved supervisor records, not these synthetic fixture counters.
Any failed run remains preserved; no duplicate run is authorized by this note.

### Saved actual outcome: PASS, same scoped control boundary

Root executed the selected operation once. Independent review read only the
saved `experiments/v5-local-checks/prover-allocation-adoption-controls-01`
outcome; no rerun. The inner report and unittest log agree on **seven tests,
zero failures/errors/skips**. The real descriptor pin remains the selected
100,153-byte `c93a45a6...ece710` file. Synthetic compiler outputs, costs and
descriptor substitution remain explicitly labelled and do not become actual
build provenance. No executable was created in the synthetic controls tree.

Independently rebound all 30 original plus 30 copied source identities,
18 selected runtime files and all 28 reported import origins/pins. Imports
resolve under the selected source snapshot: the 27 production modules plus
the test's `__main__`. The copied selection is byte-identical to the reviewed
`cfff2cdb...f76ef9` selection. The saved stdout repeats the inner JSON with only
Windows text-output translation of its final LF into CRLF; it is not claimed
byte-identical to the saved binary-written JSON. Both original files remain
unchanged.

The outer status is `COMMAND_EXITED_ZERO_AND_CLOSED`, exit 0, direct child
reaped, Job closed, zero active/limit-terminated processes and no cleanup
errors. Two total processes remain within the selected limit. Observed logs
are 9,144 stdout / 1,087 stderr bytes, within limits. There is no finalization
override. The test source's native-process denial and the saved report's zero
native calls retain the stated no-compiler/native/guest/proof/network scope.

Actual inclusive worker CPU is 3.359375 seconds; separate wrapper CPU is
0.5 seconds: **3.859375 seconds known combined CPU**. The nested supervision
CPU field is part of the wrapper and is not added again. Outer wall time is
8.146288899937645 seconds, and observed Job peak private commit is 30,871,552
bytes. These are actual control-run costs, unlike the fixture's invented five
compiler records. Final report/exit tails are not thereby completely metered.

| Actual record | SHA-256 |
|---|---|
| Outer `RESULT.json` | `3cc253e3ff896693d8cd11f41560e1b476e06ace03785016f70a5101601ac664` |
| Inner `controls/RESULT.json` | `76ba4bc27772883e69aea7e90e1413c7c4df05134e57d7a6ceeb295f3beea0aa` |
| `command/stdout.txt` | `0f179b6cdf76c067aec5ce9b86a55a4f9b6319d70f0a5dd1068cfb416b592823` |
| `command/stderr.txt` | `e1bd517349d2ef934705679b1689d83c362ccd8bfc1a7780f053cbb5f791d243` |

This actual audit passes the new adoption-control boundary only. It does not
qualify the unexecuted compiler, corrected proof-memory envelope, A receipt,
full reciprocal operation or final v5. Selected sources and evidence now stay
frozen; no duplicate controls are needed for an unchanged boundary.
