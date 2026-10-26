# Independent outcome and continuation audit: anchor query

2026-10-26. Reviewer: `update_trust_lifecycle`. This is a fresh checkpoint;
the used REVIEW/source/PLAN/EXECUTION and controls01 evidence remain unchanged.
Root owns launch, exact selections, adoption and Git. This review does not run
the product, tests, Lean, owner/custody APIs or a network service.

## controls01: failed before import, preserved

**FAILURE CONFIRMED; NO CONTROL OR PRODUCT PASS.** Read the exact selection,
command report, stdout/stderr, runner result and failing saved source. Selection
SHA-256 is `f82c1c0a5e78441bd60b4155aa94caf3872f73a7b6359f48d19ba3d9e4a1b09d`.
All seven original source pins, seven snapshots and three runtime pins still
match. Original and saved test source SHA-256 remains
`2817e4ffd3f6b925e34bc111e775f0bc95acdab41c787a4e5998f71fbad6d4ee`.

Python rejected test_query.py at line 680 because the outer `expected_paths`
list lacked its closing `]`. This is a parser failure before module execution,
not a product rejection or a failing mathematical/query assertion. Stdout is
empty, stderr is exactly 346 bytes, and the controls output directory was never
created. Consequently no test group ran and no companion was imported by this
harness. The prospective public01 operation was not run and is now unselected.

The outer report is COMMAND_FAILED, exit 1, child reaped, Job closed, zero final
active processes, no cleanup errors and no termination request. The root Job
measured 0.125 CPU seconds; separate runner CPU was 0.09375 seconds, for 0.21875
seconds of reported CPU without adding nested observations. Job wall through
cleanup was 0.27466179989278316 seconds; complete runner wall was
0.37054979987442493 seconds. Peak Job private commit was 17,604,608 bytes. The
original finite allocation is spent, not renewed by a source correction.

The earlier manual source review missed this syntax error. Its frozen source
verdict is preserved as the actual historical review, not rewritten to imply
that syntax validation happened. Future prelaunch source review should include
cheap stdlib `ast.parse` or `compile(source_bytes, filename, "exec")` checks.
These parse/compile to an inert AST/code object without executing it; they must
not import the subject, write bytecode, call main or touch state. Prohibiting
product execution does not prohibit this inexpensive source check.

## Narrow successor review

**PASS NARROW SOURCE DELTA; EXACT EXECUTION SELECTION PENDING.** Read the complete
CONTINUATION.md (`d2ffe6a7d17589bda438f03078dd9eedd865756d66816113ded2404be6d96691`)
and independently compared old/new bytes. test_query02.py is 47,051 bytes with
SHA-256 `2f9e6cd553c8ae84dcd6f95722e2d338a526ba2b06c4a1d7224f2baf0d7d58f0`.
It differs only by one ASCII `]` at zero-based offset 42,714, line 680. Removing
that one inserted byte reproduces the entire frozen original exactly. No case,
expected outcome, authority boundary, runtime budget or fixture is changed.

Independently ran stdlib AST parse and inert code-object compilation on both the
new harness and unchanged query.py; both passed without import/execution of
either source. The product is still
`52c48ed1da4d0f4955d88eb54b00df7475ec5f7bf4ae85497907b247adb261a1`.
An initial reviewer check command had a PowerShell command-argument quoting error,
then an LF/CRLF-specific comparison found no needle; neither executed the subject.
The successful byte-offset comparison above is independent of line-ending
assumptions. No product or controls were run by the reviewer.

Any successor gets fresh exact selection/output/finite limits; no previous
failure is erased and this source review alone does not authorize execution.

## Exact successor selections

**GO controls02; public02 source/selection GO conditional on a clean controls02
outcome and root's separate adoption/launch.** Reviewed the full changed selections
and verified every current selected source/runtime byte against its hash:

| Operation | Selection SHA-256 | Sources | External pins |
|---|---|---:|---:|
| anchor-query-controls02 | `facecbf452a78249993d2f155e851b464e6360d6b15492ca507de4188726456e` | 9 | 3 |
| anchor-query-public02 | `8bccce2ec35c77f902827975c155ecf0d2cbb0b52bf3e20be27d8c5e464f96fc` | 9 | 204 |

Each retains all seven prior source pins and adds only the exact test_query02.py
and CONTINUATION.md. The only argv change is snapshotted test_query02.py; the
subject remains the explicitly pinned original canonical query.py. Run names
and thus fresh output roots change to 02. Both output roots are absent at review.
All runtime pins and limits equal their respective 01 selections exactly.
Controls retain 90 wall / 35 inclusive CPU / 512 MiB / two active processes;
public retains 120 wall / 60 inclusive CPU / 1280 MiB / six active processes.
Each log cap remains 1 MiB. No product/native work is selected by controls mode.

The public map preserves all 184 adopted received-query01 external pins, the
four additional prior query fixtures and all 16 private registered-sidecar files.
Its actual read-only sidecar file census equals those 16 selected paths; every
hash matches, including the five module artifacts. Long absolute paths were
handled for hashing without changing recorded identities. The existing cold
public report and original custody limits are already in the preserved map.
No owner/custody API was opened. public01's output directory is absent; this audit
does not silently treat the abandoned conditional selection as an operation.

## controls02: actual seven-group outcome

**PASS NATIVE-FREE CHANGED-BOUNDARY CONTROLS.** Read the saved TEST-RESULT,
stdout/stderr, enclosing command/result and selected source snapshots. Nine
original source files, nine snapshots and all three runtime pins match; the
saved selection is exactly the reviewed facecbf45 selection. Saved test JSON
equals stdout except for the terminal line ending. All seven planned groups
are present in their original order, `ok=true`, `native_processes=0` and
`mathematical_acceptance=false`.

The actual groups report 17 config/wrapper refusals; full-chain/nontarget/basis
binding success and ten binding refusals; fifteen context/sidecar/revalidation
refusals; all four owner/custody close combinations; four setup-before-mkdir
refusals; five worker lifecycle cases; and six parent terminal cases. Worker
success closes both handles before publishing any hints. Changed anchor/context,
delegated artifact rejection and failed owner closure publish no hint files;
their saved output census contains only the candidate WORKER and synthetic
native artifacts. Both handle closes are attempted. Parent success occurs only
in the ready case; unclean supervision, unclosed handles, changed owner, changed
candidate and pending-write failure remain failures. These use the reviewed
explicit authority/native/supervisor doubles, not actual state or Lean validation.

Enclosing status is COMMAND_EXITED_ZERO_AND_CLOSED, exit 0, child reaped, Job
closed, zero final active processes, no cleanup errors or termination request.
Stdout is 7,478 bytes; stderr is empty. Job wall through cleanup is
1.2601966001093388 seconds and full runner wall is 1.3763454998843372 seconds.
Inclusive Job CPU is 0.5 seconds plus 0.078125 separate runner CPU: **0.578125
seconds total reported CPU**. Peak Job private commit is 34,836,480 bytes. Nested
harness observations are not added. The failed controls01 remains separately
preserved and charged.

Saved evidence pins:

- RESULT.json: `cebdb81999a60ed4bf7102f6d6079bbf86dbe1bcc206002a1ebbea264031edb6`.
- controls/TEST-RESULT.json: `52f6a1402c36a0fdf21701bd501647ea5b03d23a8f4848416173eaa0630b7a6a`.

This satisfies the controls prerequisite for root to select public02 once under
the exact reviewed 8bccce2e selection. No public outcome, real anchor/native
acceptance, law proof, search result, growth benefit or final-v5 claim follows
from these native-free controls alone.

## public02: actual registered-anchor question

**PASS THE SELECTED PUBLIC COMPANION WORKFLOW.** Root executed exactly one
public invocation under selection `8bccce2ec35c77f902827975c155ecf0d2cbb0b52bf3e20be27d8c5e464f96fc`.
The reviewed query.py and test_query02.py are unchanged. All nine original source
pins, nine saved source snapshots, 204 external pins and six reported output
length/hash pairs match after execution. No prior failed operation was relabeled
or reused as an output root. No reviewer product/native/state API was executed.

The saved invocation binds the approved question and exact selected original
companion to config SHA-256
`9941b6885e0868054ba237e5023f1136c83f55fc79a8c7d3fe185aeb04c96f04`.
Question SHA-256 is
`d10b628c1624d9808f3ab29ede688fec9325cf4f68d9a1cc5ae48c17605f5607`.
The actual source imports Init, the selected registered bridge module and the
selected OwnerQueryCommand, and contains only the same declaration-free formal
question as received-query01. It creates no theorem proof. No `-o` artifact is
selected; the saved native output census is exactly Query.lean and type.json.

### Actual private anchor binding

Using stdlib JSON/hash analysis only, independently reconstructed the complete
returned one-record plan from the current pinned private record. Its ten units
contain 21 outputs, including dependencies and non-target exports; the chosen
AllClosure target is not substituted for the complete import vocabulary. The
derived canonical plan SHA-256 is exactly
`6523e1f3b2e9d59d229c1c4fa09c767df28a4cae4a780e1a1abf784dff91bfce`.
The raw record digest, STORE binding, support ID, module name, direct Init import,
added-name list and all five artifact paths/pins agree with returned ANCHOR.json.
The five actual private artifacts total **19,888 bytes**. The three received
reference binding rows agree with the corresponding private record outputs;
the two fixed-basis rows and all identities also equal the independently audited
received-query01 output exactly.

The selected import directory is the actual existing registered operation's
private modules directory, not its earlier public cold copy. Returned LEAN_PATH
is exactly the selected helper directory, Lean library and that private directory,
using the reviewed extended Windows spelling. The recorded ordinary paths,
artifact contents and import selection remain bound. There is one module in
this actual fixture; the native-free controls, not this public run, cover new
multi-member projection logic.

### Exact mathematical question and hints

Independently compared the complete current bytes with the adopted, independently
decoded/reconstructed received-query01 artifacts. All four are **byte-identical**:

| Output | Bytes | SHA-256 |
|---|---:|---|
| native/type.json | 1173 | `333415560e87565ec9a774baaa317ff9e96d0773530da341391b174a9c91c915` |
| BINDINGS.json | 915 | `e93217483f53b1d78bef162e41f56be4c704dfae755930ee2e823ca8245e21dc` |
| QUERY.json | 2299 | `083a2e8f588345dcd1a1b371f3f2edfa684e2f6094564e7bea9a0b56363ebbd3` |
| SPECS.json | 104 | `689c10b92a751b3f217838c02d6a800a1ff86e1343426dd76985380aa632479d` |

Thus even the prospectively permitted forall-display-name difference did not
occur. Reuse the prior full AST/key audit instead of repeating a passing codec
experiment: one universe parameter, two level nodes, 30 expression nodes,
five exact reference bindings and the full AllClosure-cons-to-tail statement.
The namespace remains `d966de54aa32c6cd059ab9553a0968a320594a63561cadf742cca6265858079c`
and feature `941dc31cba88a2758910984aad0f044cb074b6614b8b78494a46524c150356ca`.
The actual new wrapper is 600 bytes with SHA-256
`487760826d2387d1919bf9d96679691286c490f3083154b9dac366155e25f27f`;
ANCHOR.json is 6,630 bytes with SHA-256
`3d1649c68e10ead3f1983a32431788d8f3d524e9e27925677e1537788723ed6e`.

### Owner closure, publication and cost

Actual WORKER reports native exit 0 and both owner handles closed, retaining
the candidate-only status. Its interpretation and output pins match the final
parent result. The parent reports ANCHOR_QUERY_READY only after its reviewed
closure/revalidation/publication path and clean worker-tree supervision. Public
stdout equals final RESULT, worker stdout equals WORKER, and root stdout equals
TEST-RESULT, apart from terminal line endings. Worker hash and input/output
binding checks all agree. No close error, pending result or leftover native
artifact is present. Ordinary opening may settle old reservations; this is not
a claim that the owner database is immutable or independently opened by review.

Root and companion supervisors both report exit 0, reaped direct children,
closed Jobs, zero final active/terminated processes, no cleanup errors and no
termination requests. Actual log lengths equal their reports; all stderr is
empty. CPU, wall and peak Job private commit stay within original finite caps.
The root's eight cumulative processes are a lifetime count, not a violation of
its six simultaneous-active-process cap.

| Scope | Wall seconds through cleanup | Inclusive Job CPU seconds |
|---|---:|---:|
| Root command | 3.722291300073266 | 2.640625 |
| Companion worker including Lean, nested above | 2.760123400017619 | 2.203125 |

Full runner wall is **4.109534699935466 seconds**. Root Job CPU plus the separate
runner CPU is **2.640625 + 0.765625 = 3.40625 seconds**. Peak root Job private
commit is 906,432,512 bytes. Nested worker/harness/wrapper diagnostics are not
added again. These are one local operation's costs, not an optimized-comparator
speedup result or an asymptotic large-network bound.

Saved evidence pins:

- Root RESULT.json: `d2f30def8aa36c0b6c2b59d82d09f8368d2016e78f5897cec712417069d17a9f`.
- public/TEST-RESULT.json: `5a630a8f6899e9b26690888c0e8351b28929f07e37ab7f041d9c70df024c1be1`.
- public/query/RESULT.json: `0667c97a65bb8fd8a619c4e3af5fda19ac8834a4d6814a2a7a302a48b6d327b6`.
- public/query/WORKER.json: `ae3137257375add578575cbb22ae550a8d5f7a7dd0092aef686fc69b46fb5eb3`.

## Final scoped disposition

The new companion closes the selected operator gap: a recipient can prepare
identity-bound search hints for a formal question using its already registered
received vocabulary, without custom supervision/import glue. Its used source,
controls02, public02 and preserved controls01 failure remain frozen. No rerun,
build, export, admission, provider, protocol extension or campaign is implied.

This proves neither the queried law nor successful/complete discovery, semantic
equivalence, useful novelty, growth acceleration, native nonempty-anchor-plan
restoration, hostile-source isolation, worldwide deployability or completed v5.
It remains local and unpublished. Root's next highest-payoff workflow decision
is separate from adopting this completed scoped audit.
