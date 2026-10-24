# Independent mixed-theorem native discriminator review

Date: 2026-10-23. Reviewer: `native_matching_audit`.

## Decision

**Source and exact selection cleared: no blocking defect found.** This clears
the proposed single bounded discriminator for root's launch decision. It does
not assert that the new Lean source compiles, that the discriminator passes, or
that the full ordinary-module product or v5 is qualified. No native process,
test, build, owner operation, project import or Git mutation was performed in
this review.

The decisive question is whether an acquired closure containing one exact
already-installed theorem and one new theorem can produce an ordinary importable
module, without silently replacing the installed theorem or accepting an
all-matched empty contribution. This directly addresses the previously observed
ordinary-library collision, rather than adding another certificate campaign.

## Exact reviewed bytes

All source and saved-input hashes below were independently checked. Paths are
relative to the sole canonical project root unless otherwise noted.

| Item | SHA-256 |
|---|---|
| `software/v5/ordinary_module_matching/native_check.py` | `c0cb4bd4ca1350351da0ae3145818b2b350e67cd565a394896c63942f163049f` |
| `software/v5/ordinary_module_matching/module_worker.py` | `3872864a27e9fbb12e56eaa2ebabd9299d97a336c5e58840648a86b5c371df18` |
| `software/v5/ordinary_module_matching/OrdinaryModule.lean` | `62269b34626ead7cd33fd2a492da66a34a1f1ca3cae7bc3e1f3d984d904ea525` |
| `tools/Run-V5-Check.py` | `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651` |
| `experiments/v5-local-checks/ordinary-module-native-03/collision-refusal/request.json` | `0070f06dc523bf03194c7a5a4b015d9e908e5ccb26ae6a68078cf429ec188032` |
| `experiments/v5-local-checks/ordinary-module-native-03/collision-refusal/inventory.json` | `c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0` |
| `experiments/v5-local-checks/ordinary-module-matching-native-01.selection.json` | `40fc345e43262a6b85e2a1ca5fd7bf7f4d886f1703913de37bab7456b8a25106` |

The full new harness, relevant worker invocation/report phases, native changes
against `ordinary_module_bridge/OrdinaryModule03.lean`, encoding functions in
`OriginalExpr.lean` and `OriginalDecl.lean`, saved raw request, and predecessor
selection/implementation reviews were read. This review does not repeat or
supersede the separate mathematical theorem-interface argument.

## Four-command discriminator

The harness makes exactly four sequential supervised native commands:

1. Pass the **unchanged raw saved request** to the new V2 worker. It must match
   singleton `Nat.add_zero` at index 0, check new
   `CommonsLibraryExample.add_zero` at index 1, and produce the exact full V2
   report. Assertions require one matched and one checked theorem, both checking
   passes, both fresh rereads and the five module artifacts.
2. Compile a normal Lean consumer importing only Init and the generated module.
   Its addition-zero proof uses the **new theorem**, so a report alone is not
   the positive result.
3. Change only the installed theorem proof's outer lambda binder name in both
   its descriptor and inventory. Require the exact native refusal
   `ORDINARY_MODULE VISIBLE_INVENTORY_MISMATCH name=Nat.add_zero`.
4. Project to the installed theorem alone. Require the exact native refusal
   `ORDINARY_MODULE NO_NEW_MODULE_DECLARATIONS`.

Both negatives require a build-only failure trace and no module artifacts,
pending report or final report. They use distinct fresh directories and cannot
rewrite the positive output. Their retained identity labels are test inputs,
not newly issued mathematical warrants.

The saved first descriptor proof equals its inventory proof. Its 24-node proof
ends at root 23 with lambda node
`[4, [[0, {"$bytes":[110]}]], 0, 0, 22]`. The codec retains binder names.
Changing both copies preserves their agreement, so classification proceeds to
the intended installed-inventory equality gate. This is deliberately an
**exact-evidence identity refusal**, not a claim that alpha-renaming invalidates
the theorem. The all-matched refusal precedes the module writer.

## Selection and resource boundary

The exact selection contains four source snapshots and 158 runtime pins. A
read-only key/value comparison against
`ordinary-current-relocated-smoke-01.selection.json` confirms **all 156
predecessor runtime pins are retained unchanged**, with none missing or changed.
The only two additions are the saved request and inventory above, both rehashed.
This reuses the earlier package audit; it is not a fresh independent rehash of
all 156 runtime files.

The selected package is
`experiments/v5-local-checks/ordinary-current-relocated-smoke-01-payload`, with
profile SHA-256
`192dfee12ac186fbdac0634212b28c1c6324222da2b035f8f295ec764303a68d`.
Its required `OrdinaryExport`, `OwnerRebind`, `OriginalExpr`, `OriginalDecl` and
`CheckedExtension` companions are present under `authoring/helpers`.
The selection invokes isolated Python with `-I -S -B`, uses the snapshot harness,
and sends outputs only to `{output}/native`. The named output root
`experiments/v5-local-checks/ordinary-module-matching-native-01` did not exist at
review time.

The one inner allowance is 180 wall seconds, 120 CPU seconds and 1536 MiB. The
outer allowance is 210 wall seconds, 150 CPU seconds, 2048 MiB and eight processes.
Each native child receives at most 100 wall seconds, 42 CPU seconds and four
processes, further reduced by remaining allowance and the 25-wall/62-CPU reserve.
Complete child Job CPU is charged once; unknown CPU charges the full grant and
stops the sequence. Expected exit-1 failures still receive terminal wall/CPU,
log-cap and clean-process checks. The reserve or envelope may cause a legitimate
resource refusal; no assumption that all four calls must fit is needed for
source clearance.

Only exact-pinned supervision helpers are imported by the harness. It does not
invoke the public owner/controller, extract mathematics, initialize an owner,
recollect a closure or start a compilation campaign. The proposed native
`lean --run` elaboration and normal consumer compilation are precisely the
unexecuted runtime boundary. Final pins cover selected sources, package/runtime,
saved inputs, requests, reports and generated artifacts.

## Remaining gate

Root may select the one exact run above, preserving its outcome whether it
passes or fails. The resulting saved evidence requires an outcome review before
adopting native compatibility. No automatic retry, new package, public API
integration, certificate, network operation or broader qualification follows
from this source clearance. Used predecessor sources and evidence remain frozen.

## Saved native01 failure and narrow native02 successor

The first selected run is now **FAILED**, not a mathematical refusal or a
resource exhaustion. The independent source review above missed a Lean parser
layout defect. The preserved stdout reports
`OrdinaryModule.lean:252:75: error: unexpected identifier; expected '}'`.
Parsing stopped before the native program's `main` checked any mathematics.

Read-only saved-evidence inspection confirms:

- Exactly one supervised call, labelled `mixed`; the worker phase trace is only
  `build STARTED`, then `build EXITED 1`. Neither fresh reread, ordinary consumer
  nor either negative control ran.
- No generated module artifacts, native pending/final report or accepted catalog
  entry exists. The actual request and inventory match the originally selected
  `0070f06d...` and `c81800ab...` bytes.
- All four original and snapshotted source hashes still equal the exact native01
  selection. The old sources and failed output remain unchanged.
- Inner and outer supervision both report reaped direct children, closed Jobs,
  zero remaining active processes and no cleanup errors. Outer Job CPU is
  2.484375 seconds, including the nested mixed Job's 1.984375 seconds; these must
  not be added. Outer command wall time through cleanup is 4.4066252 seconds;
  overall launcher wall time is 4.9955851 seconds. Launcher CPU is separately
  reported as 1.15625 seconds. No allowance limit was reached.
- The harness's `MATCHING_CHECK_UNCLEAN_PROCESS_TREE` text is a generic combined
  success/exit/cleanup assertion label. Here the positive call returned exit 1;
  the underlying supervision records show **clean closure**, not a process leak.

Saved evidence under
`experiments/v5-local-checks/ordinary-module-matching-native-01`:

| File | SHA-256 |
|---|---|
| `RESULT.json` | `917f53d7808269fc77f722edaba7b168486634efbb9458023c81ef51caa840f3` |
| `native/NATIVE-MATCHING-RESULT.json` | `2124f7234185a823621b62865e2d170c787774830ac9b3ffab5cf33392179c41` |
| `native/mixed/SUPERVISION.json` | `23f1e15899c36b1dbd37281078f7c9e855ed4610860eeeaba9684c41ad1c17b6` |
| `native/mixed/supervision/stdout.txt` | `88a0e37283a96f11440dab81c8088c79d2231818370c87cf35173794393ab047` |
| `native/mixed/native-report.json.phases.jsonl` | `5790cbefba24f0f4940121eee52507fb68ba3c7cdc52f1c44741c1fbe0754504` |

Root selected a fresh two-file successor, not modification or continuation of
the failed allocation. The complete read-only diff was inspected:

- `OrdinaryModule02.lean` changes only the two `plan` record-update blocks.
  It places each field on its own consistently indented line after `with` and
  removes the commas. All field expressions, branch conditions and checks are
  unchanged.
- `native_check02.py` changes only the native source filename/byte count/hash,
  its own required filename and the worker's native source argument. The worker,
  fixtures, assertions, four-command sequence and accounting remain unchanged.

Independently checked successor identities:

| Item | SHA-256 |
|---|---|
| `software/v5/ordinary_module_matching/OrdinaryModule02.lean` (27,358 bytes) | `45e83c3a2a53cc32968fb0ba187ca39b4b2614884284ee78aa78cf7ff28d2019` |
| `software/v5/ordinary_module_matching/native_check02.py` | `8d0238e312bca697b7d74d01785581bfc5954f45942cb134a369a108ca4f80a1` |
| `experiments/v5-local-checks/ordinary-module-matching-native-02.selection.json` | `5deafa2cbd9107ca585c54e5de5d4f02b9486bda5e0a7327457b70f0239d41c7` |

Exact selection comparison confirms all 158 runtime pins are identical, with
zero additions, removals or changed values. The same package, profile, inner and
outer limits are retained; the snapshot source map correctly names the two new
files and the unchanged worker/launcher. Only the harness filename changes in
the command arguments. The fresh native02 output root did not exist at review.

**Narrow successor source/selection clearance: no blocking defect found.**
Root may select the exact fresh native02 run. Compilation and all mathematical
outcomes remain unproved until that run; no retry was performed by the reviewer.
This syntax repair does not expand the previous discriminator's qualification
scope or justify any package/public-facade adoption.

## Independent saved native02 outcome audit

**PASS within the selected direct-native compatibility scope.** Root executed
the exact native02 selection once. This reviewer inspected only saved files and
recomputed hashes/structural comparisons; no Lean, project import, test or build
was rerun. Native01's failure and costs remain preserved separately.

### Actual mathematics and native outputs

The positive worker received the unchanged 5,546-byte saved mixed request and
823,690-byte foundation inventory, with the original selected hashes. The final
and pending reports each have exactly the 20 expected fields. An independent
comparison reconstructed their expected identities, inventories, name lists,
partition, counts and artifact paths/sizes from the actual request and files;
every field matches. The final report embedded in the harness result also
matches the separate native report.

In particular:

- `matched_unit_indices = [0]`, with exact installed `Nat.add_zero` inventory;
  `units_matched = 1`.
- The only added inventory is `CommonsLibraryExample.add_zero`;
  `units_checked = 1`, `checking_passes = 2`, `basis_rows = 581`.
- All three worker phases actually exited zero: `build`, `reread-private` and
  `reread-exported`. This is not merely a build-only report.
- The module directory contains exactly the five named parts, totaling 4,784
  bytes. Their saved hashes and byte lengths match actual files.
- The actual 239-byte ordinary consumer imports only Init and the generated
  `DMKNBridge_56630adecadb54b40462a1bd1d9b2fcbde375c9b3c93069f288fc1db61da467c`
  module. Its theorem `MatchingConsumer.useNew` has body
  `CommonsLibraryExample.add_zero n`; it is not a direct use of the installed
  theorem in place of the new one. The selected consumer-child code supplies
  only the pinned runtime and new module directory as its Lean search path.
  Actual compilation exited zero with empty stdout/stderr and five nonempty
  generated parts, all independently hash/size checked.

This establishes the narrow installed-theorem coexistence and ordinary-consumer
boundary for this fixture. It is a deliberately simple compatibility example,
not substantive mathematical discovery or a demonstrated useful-growth benefit.

### Actual refusal controls

Independent structural comparison of the proof-mismatch request with the
positive request finds exactly two differences: the outer lambda binder-name
byte array in the installed theorem's descriptor and its inventory copy. Both
now decode to `native_control_n`; the two proof copies still agree exactly.
Everything else, including the second theorem, is unchanged. The native build
exits 1 with precisely
`ORDINARY_MODULE VISIBLE_INVENTORY_MISMATCH name=Nat.add_zero`.
This confirms the intended exact-private-evidence identity check, not rejection
of the theorem's mathematical statement or alpha-renaming as unsound.

The all-matched request is exactly the selected projection to the first unit,
first unit ID and target `Nat.add_zero`, with other fields unchanged. Its native
build exits 1 with precisely `ORDINARY_MODULE NO_NEW_MODULE_DECLARATIONS`.

Both controls have only the build STARTED/EXITED-1 phase pair, empty stdout,
zero module-directory files, and no native final/pending report or module
manifest. They did not produce or admit mathematical output.

### Integrity, containment and complete costs

Independent rehashing covered 179 distinct files: all 158 selection runtime
pins, the four original/snapshot source pairs, all 142 saved INPUTS pins,
positive request/inventory and all ten module/consumer artifact pins. No hash
or stated-size mismatch was found. The unchanged package contains exactly the
127 pinned files, with no missing or extra files. The used source snapshots
match the exact reviewed successor selection.

All four per-call saved supervision events agree with their copies in the
outcome. Recorded command arguments, working directories and limits agree with
each corresponding command record. Actual log sizes agree with recorded sizes.
Every child and the outer Job report reaped direct children, closed Jobs,
zero active/terminated processes, no cleanup errors and no forced termination.
All final wall/CPU/log values and recorded peak private bytes are within their
selected limits. Cumulative `total_processes` counts are not simultaneous-process
counts.

| Call | Exit | Wall through cleanup (s) | Inclusive child Job CPU (s) |
|---|---:|---:|---:|
| Mixed build and both fresh rereads | 0 | 12.2668293 | 11.625 |
| Ordinary consumer | 0 | 0.6752387 | 0.53125 |
| Exact-proof mismatch | 1, expected | 5.9971925 | 5.859375 |
| All-matched refusal | 1, expected | 6.3103615 | 6.28125 |

The child CPU sum is 24.296875 seconds. The enclosing Job already includes those
children and reports 25.46875 CPU seconds; adding the separately reported
launcher's 1.3125 seconds gives **26.78125 known inclusive CPU seconds**.
Do not add the nested child CPU or wrapper-supervision subtotals again. Overall
launcher wall time is **27.8749604 seconds** (outer command through-cleanup wall:
27.1923982 seconds). Peak outer Job private commitment is 1,426,231,296 bytes.
These are this selected local run's costs, not a workload-average performance
estimate or an end-to-end public workflow measurement.

Principal saved evidence under
`experiments/v5-local-checks/ordinary-module-matching-native-02`:

| File | SHA-256 |
|---|---|
| `RESULT.json` | `b738240881ff7a512af8413f4c3ac61b823b078821c25ca1984f267eb75eeeef` |
| `native/NATIVE-MATCHING-RESULT.json` | `2a82a3a7a6b5e31f649e66865d9131744d305f457818ffa946d15eb2d475b5ec` |
| `native/mixed/native-report.json` | `8c26c78f2b95728b220b337d261fb0cfac3acee74a2fc55da046d96d8f84c59d` |
| `native/mixed/native-report.json.pending` | `ba9bde0998856b07077e2c1b96a10446b9e5f74ab7c3711ca20b8606901fd3c9` |
| `native/normal-consumer/Consumer.lean` | `4d963014702ddcae3015b4ad4cc3143fd16c39ad4d7add3303dac8b48a7ae21f` |
| `native/proof-mismatch/request.json` | `d9c91ece870a31d237020d13a4219aff9582c014a58ede1975f841033808b5b3` |
| `native/all-matched/request.json` | `d1a932b3fd712fc341aafe7dd4ad51be0d5c5880dfd224885931524e94d2d755` |

### Adoption boundary

Root can adopt actual direct-native matching, both rereads, the normal consumer
and the two exact refusals. The run deliberately bypasses the public owner and
module-export facade and does not produce a new package or catalog acceptance.
It does not establish general conflicting-proof interchangeability, broader
Lean/library compatibility, ancestry-independent verification cost, hostile
source isolation, network scalability, useful growth or final-v5 readiness.
No further run or allocation is selected by this review.
