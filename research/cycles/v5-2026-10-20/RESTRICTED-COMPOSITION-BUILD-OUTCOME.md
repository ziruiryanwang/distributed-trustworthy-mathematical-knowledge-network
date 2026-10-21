# RC native build01: independent actual failure audit

2026-10-21, core_release. Read-only audit of the one completed root-selected
compile. No compiler, control, guest, proof or network operation was launched
by this audit; all used build01 sources and evidence remain unchanged.

## Disposition

**FAIL_BUILD, with soundly preserved failure evidence and clean owned-process
closure.** The first `rc-core` compiler exited1 at a missing closing parenthesis
in `foundation.rs`'s `trans_type`. No library or executable was produced, and
neither subsequent compile nor any control ran. This is not a semantic-refinement
failure or pass: the source did not reach Rust typechecking. The earlier source
review missed this syntax defect; its source PASS was not compile evidence.

Six nested `pi(...)` constructors begin at lines29-31. After the terminal
`eq(5, 4, 2)` call the expression closes only five of those six constructors.
The compiler consequently reports the outer `pi` at29:24 as unclosed when it
reaches the function's closing brace. The narrow repair is one additional `)`;
it must be in fresh selected successor files, not a rewrite of used01 bytes.

## Independently checked bindings

| Record | SHA-256 |
|---|---|
| external build selection | `cd3fb30006a60edff0e6c4dbfbb99b488a97c56493c50532244085fe07a7ffd1` |
| RESULT.json | `519d354af8f18b33e0c902293fc7d2a438c6a1ce80d955b8d09df0715863f4de` |
| finalized attempt | `05c5bb08a7db0fb03c104af462ba04fcda081e7502f70c53424ef5f37c37cb8d` |
| source-map.json | `2aa2860215ef36f69da73d8dbce65ad9280cc9b115b99be75d11de21afa00741` |
| compile-commands.json | `20cc380c1edd09fe4f596c2fb828e824742e87eedfb2e6045a9f3796a44ef053` |
| owned Job closure | `841310f962aedb3a018e79c6657a43f58fc22c5c7a6c8420eae1fa984fdaa009` |
| compiler stderr,572bytes | `7a26318f3bd4dd49acd717db9c3bcdef1a36ce9792a86276399c451a0fdd5b52` |

The run is `experiments/v5-local-checks/restricted-composition-build-01`.
Direct read/hash checks establish:

- All15 selected source files match both their canonical originals and the
  exact saved snapshot, by size and SHA. The snapshot has exactly15 files.
  Saved selection and source-map entries agree with the external selection.
- All174 retained compiler/runtime pins still match. The five separately pinned
  retained command/map/result/original-checker/original-module-library records
  also match. No checker, dependency or module relation was rebuilt.
- The actual command in RESULT, command.json and the first entry of the saved
  compile plan is identical. Independently deriving it from the retained
  aggregate recipe reproduces the exact argv: only RC core crate/root/output,
  distinct metadata and new-run dependency path are changed as selected.
- The intended compile plan has three commands; the actual command list has
  **one**. The rc-core command is rlib compilation with retained explicit
  module/serde externs, not a test or program invocation. The other two commands
  are planned-but-unexecuted, not failed or successful outputs.
- Both actual log hashes/sizes agree. stdout is empty. RESULT binds the exact
  selection; the finalized attempt binds RESULT and its FAIL status. There is
  no FINALIZATION-FAILED override. All three intended artifacts are absent.

The controls-root private includes of syntax/foundation/typing were already
within this15-file map and used existing dependencies; that change required no
adapter expansion. It did not cause this parse failure.

## Cost and closure

The recorded total elapsed time is3.6389387999661267seconds. Controller CPU is
1.734375seconds; inclusive worker Job CPU is0.046875seconds. These are disjoint
coordinates, so known measured CPU totals1.78125seconds. The documented final
report/exit tail remains excluded. No inference/proof-performance conclusion
can be drawn from a parse-only failure.

The sole command and final Job record both have zero active processes, zero
terminated-by-limit processes and empty cleanup errors. The Job record is
`closed:true`; no selected telemetry process remained. Peak Job private commit
is14,942,208bytes. The sampled output census is144,155bytes/36entries and is not
a hard disk quota. The two total processes counted by the wrapper/Job are not
two project compile commands. No application outside the owned Job was stopped.

## Consequential next action

Review the fresh foundation02/lib02/controls_root02 and build02/selector02
changes only. The correction should add the missing delimiter, redirect the
two crate roots to the corrected signature, and give the successor its own
selection/run/artifact metadata. Preserve all original15source bytes, logs,
charges and failed output directory. Root may then select one fresh compile;
this audit does not itself launch or fund it. Control execution, guest economics,
cryptographic production and deployment remain separate unfinished boundaries.

## Narrow successor source review

**PASS for the corrected02 source/adapter boundary, not actual compilation.**
Read-only pairwise diffs against the retained01 files establish these exact
changes; no generic semantic or release re-audit was repeated.

| Source | Reviewed SHA-256 |
|---|---|
| foundation02.rs | `e8d0e32b3c480eb05b6813b6afd8eae8413930e26a436955783b2bf3e2452dce` |
| lib02.rs | `8399f2c78e6cac10ae3a262cc4c9c8d33b94c8f770fb6a0108dcfeb49b266059` |
| controls_root02.rs | `962d57d9e709c74fd6e9cec9d60f8741b31993f9c630d487dd9cc3dd5e0c1519` |
| build02.py | `0a7c986b1e012c8d5a0259373c77f9c902737f6122f743ddcd5c250eb86b510b` |
| Select-RestrictedCompositionBuild02.ps1 | `2b690cf3afb3e157012a87a5a066cc078d981335d754bb76bced1e24a63cc8b6` |

The new foundation is byte-identical except for the single additional `)`.
Both crate roots reach it as module `foundation`. In reviewed lib02 the path
attribute correctly precedes `pub(crate) mod foundation`; the earlier unused
misplaced-attribute draft is not this reviewed digest. No public API changes.

Build02 and its selector replace only the four source filenames (foundation,
library root, controls root, builder), the run/selection name and crate metadata
suffix01-to02. Fifteen files are still selected. Compile count, explicit retained
dependencies, source snapshots, resource bounds, output refusal, finalization
and cleanup stay unchanged. Source includes still close inside those files.
The original used15-file set remains intact. This permits a fresh selected02
compile, not rerunning or editing01.

The still-unused controls adapter/selector were also read for the requested
narrow change, with **PASS**:

- run_controls.py:
  `48e86f99dd1a2ca754de37ff75dca659edf11b4b736c91c9096ee3ed4590779b`.
- Select-RestrictedCompositionControls01.ps1:
  `3a8f0870e29c63f5043fc634df032e42c79cc6b9fd17b4f36462a320e1f52cda`.

Both consistently bind build02's binary/result/attempt/selection. The adapter
now requires the exact ordered40 names in the independently reviewed controls
source, not merely40 unique success labels. Its exact refusal indices3-21,
24-29 and35 give the26 actual refusal cases; the five private typing/signature
checks and four counter checks cannot be substituted for refusals. The complete
ordered lists match the source's direct checks, mutation loop and prepared
refusals. Existing exit/schema/status/errors/per-case/authority checks remain.
The9source/26runtime-pin selection, fixture binding, outer Job and one bounded
native invocation are unchanged. No controls invocation has occurred here.
