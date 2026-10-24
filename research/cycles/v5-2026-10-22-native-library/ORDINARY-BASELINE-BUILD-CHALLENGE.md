# Changed-native baseline build: independent source review

2026-10-24. `reference_soundness_audit`; canonical guard PASS. This is a separate
engineering review, not a repetition of the correspondence soundness audit.
Only source/retained metadata reads and read-only hashes were performed. No new
Python adapter was imported/executed; no selector, compiler, native candidate,
owner, package, test or Git operation ran. Root alone selects any later runtime.

## Disposition

**PASS for the selected narrow build adapter/selector source boundary.** No
blocking scope, input-identity, dependency, launch-budget or output-map defect
was found in the exact sources below. This clears their source design for
root's separately pinned selection; it is not evidence of compilation, a
successful build or an adopted mathematical support profile.

| Reviewed source | SHA-256 |
|---|---|
| `software/v5/ordinary_baseline/build_native.py` | `a2d2b12aa7ee9d3890ca307d3a71d6d22ad0a7274f1fe3da14e93bbbc984a868` |
| `software/v5/ordinary_baseline/select_native_build.py` | `bf11621bc9228cf602d5e707f4481264d731ec03065d1e2614c5dd204da226f9` |
| Frozen helper `software/v5/ordinary_package/build.py` | `49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5` |
| Frozen runner `tools/Run-V5-Check.py` | `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651` |

The companion author checkpoint is `ORDINARY-BASELINE-NATIVE-BUILD.md`; this
review independently inspected the implementation, selected helper/runner,
native imports/entry points and retained object provenance rather than relying
on that checkpoint's claims.

## Input identity and preserved build provenance

The ten reused `.olean`/`.o` files are exactly the five named shared modules in
the retained successful extractor build:

`experiments/v5-local-checks/ordinary-current-source-build-01/distribution/_build/extractor-objects`.

Read-only verification confirms all ten current lengths/hashes equal their
entries in `EXTRACTOR-OUTPUTS.json`, whose actual hash equals the adapter's
`f55d4c5b56fc299564b76d68c66d63d3090f439b44479b597b016113c4b53768`.
The retained outer result records exit zero, clean closure and the selection
identity `97a4c0d19aea620d067f9cf2a227706fd460654bf06b978cc201a2b7b2e8790b`;
the actual template file matches that hash. No prior build was rerun.

The retained extractor source map distinguishes its legacy `OrdinaryExport`
view from the public-module source. The former has hash `3e046d40...`, obtained
by the existing checked header-only legacy transform (remove `module` and
`public section`, convert the three `public import` lines to ordinary imports).
The source body is not replaced by the older receiver-specific export helper.
The other four shared modules are OriginalExpr, OriginalDecl, CheckedExtension
and BootstrapSupport with their preserved exact source identities. The new
adapter uses those preserved compiled pairs, not fresh objects opportunistically
found elsewhere in the workspace.

The 23 selected runtime/toolchain entries come only from the hash-pinned prior
template and the two fixed runtime roots. Explicit required entries include the
chosen Python, Lean, `leanc`, clang and linker. There are eight source snapshots,
ten shared objects, 23 runtime entries and two preserved metadata files: 43
distinct pinned inputs. All new native hashes are supplied explicitly to the
selector and checked before it emits a selection. The final selection binds the
selector, runner and helper too; it cannot silently replace the reviewed matcher
with a source hash remembered earlier in the investigation.

## Dependency closure and commands

The current four native source hashes match the author's invocation:

- Exporter `403f1f4369cd73ea905265f3df42d52f70c68cb5d4f24c03b696dd65f2fc629e`.
- Shared artifact core `6f160a089fd6e60c34654f7f90417155a94d921a78d7884dec949e4379fd5f28`.
- Collector wrapper `78abf44c6b2b17e065a03550e5b1af0dbc7020a8d7100bc7312832c73e3ddff7`.
- Reference matcher `5120d6bb7939e32b2c2cd45981dde015d9e041fd9d7a05e11cc453ce5fd3b30a`.

Exporter and artifact core import OrdinaryExport. The collector and matcher
import the artifact core. The matcher no longer imports OwnerRebind. Their
project-local dependency closure is therefore the five preserved shared modules
plus the selected new core; standard Lean imports remain within the stated
owner-selected runtime premise. The core has no competing executable `main`.

Compilation order makes the core available before the two consumers. There are
exactly four Lean/code-generation calls, four C-object calls and three links.
Each link uses the same five preserved `.o` inputs plus only its selected new
objects: exporter alone, core plus collector, or core plus matcher. No old
exporter executable or unselected `.o` is linked. New sources use the legacy
non-`module` output form; the expected four `.olean/.c/.o` triples plus three
executables are consistent with that selected source shape. An unexpected
companion refuses instead of silently enlarging the output set.

The resulting executable names match the actual source entry points:

| Executable | Actual future CLI, not invoked here |
|---|---|
| `BaselineExporter.exe` | `sysroot inventory request output` |
| `BaselineArtifacts.exe` | `sysroot request report` |
| `OrdinaryReferenceBase.exe` | `inventory replay-map request report` |

The last command has no `sysroot` argument: it imports its complete explicit
artifact map. The adapter does not call these CLIs and does not claim their
request/report schemas were exercised. It preserves the current matcher whose
report includes both `projection` and `kernel_projection`; future controllers
must consume that schema, not an older single-view report.

## Execution, budget and output boundaries

The selector writes a fresh selection and does not launch it. `Run-V5-Check`
authenticates that selection, snapshots source bytes and supervises the pinned
isolated Python command in one original Job. The proposed limit is
240 wall seconds / 180 inclusive CPU seconds / 1536 MiB / six active processes;
stdout and stderr are inherited by the runner with 1-MiB limits each.

The adapter's cooperative 210-second wall deadline and 150-second *own-process*
CPU check are not substitutes for inclusive Job accounting. Each subprocess
timeout is the remainder of the same original deadline; commands do not receive
new grants. `CREATE_NO_WINDOW` does not request Job breakaway. Compiler/linker
children inherit the encompassing Job and its final cleanup. A failed direct
child or timeout is not misreported as clean process-tree closure.

Command arguments use fixed executable paths and lists, not a shell or peer
command. `LEAN*` variables, including the selected runtime's documented
`LEAN_CC` compiler override and `LEAN_SYSROOT`, are removed before commands.
The explicit `LEAN_PATH` contains only copied shared/generated objects; `PATH`
is the selected runtime's `bin`. This is an owner-controlled named toolchain,
not a hermetic build or hostile-environment sandbox: standard runtime libraries,
compiler configuration and operating-system behavior retain that premise.

Output is a fresh fixed path disjoint from selected sources/shared inputs and
runtimes. Exact streaming copies are rehashed against originals. Directory
censuses after successful commands require the precise accumulated file set,
32-MiB generated-file bounds and 256-MiB generated aggregate bound. Input pins,
eight snapshots, staged native sources, copied shared objects, all 15 generated
outputs and metadata are rechecked before the final receipt.

The 384-MiB spool bound is cooperative/sampled, not a hard disk quota. It is
preflighted against exact input sizes plus the entire generated ceiling and
metadata allowance. An interrupted/misbehaving compiler can leave partial
output; the adapter preserves it, performs no retry/deletion and makes no
rollback claim. This matches the selected finite local build trust model.

## Necessary saved-outcome gate

A later `BUILD.json` alone cannot establish success: failure while writing or
checking the final receipt can leave that file present. Root must require the
actual enclosing `COMMAND_EXITED_ZERO_AND_CLOSED` result, complete command/output
censuses and exact input/output pins, with failures preserved. The receipt
already labels candidates **not installed or adopted**. Nothing in this source
review authorizes candidate execution, package assembly, mathematical admission
or reference registration, or completes the v5 goal.

## Build01 saved failure: independently verified

Root subsequently selected and ran build01 once. Its actual outcome is
**COMMAND_FAILED**, not a built/accepted candidate. Read-only inspection of the
saved outer result, stdout/stderr, `INPUTS.json`, failure receipt and output
directory establishes:

- Exporter code generation and C-object compilation each exited zero. The next
  command, `BaselineArtifactCore-codegen`, exited one. Lean reports reserved
  token `meta` used as a local binder at core lines 243 and 363. No collector,
  matcher or link command ran.
- The actual output directory contains only the exporter's `.c`, `.o` and
  `.olean`. There is no `BUILD.json` or `NATIVE-OUTPUTS.json`. Those three files
  are reusable candidate build inputs, not an installed or executed exporter.
- The outer result records clean process-tree closure: child exit one, zero
  active final Job processes, direct child reaped, Job closed and no cleanup
  errors. Wall time was 49.175299 seconds; known Job CPU was 6.421875 seconds and
  wrapper CPU 1.140625 seconds, totaling 7.5625 known CPU seconds without
  double-counting the wrapper's supervision subset. Peak Job private commit was
  614,010,880 bytes. This is a compile syntax failure, not evidence of exhausted
  memory or an impractical certificate workload.
- Independent read-only rehashing found all 43 selected runtime/input pins and
  all eight source snapshots unchanged. The used original sources, selected
  run, failure and charged costs remain frozen. No failed operation was retried
  by this audit.

| Saved artifact | SHA-256 |
|---|---|
| `selection.json` | `ff808bd2c58b353b7162f34bb66bcc22be19148efbe16a57f48765b96a8773c9` |
| `RESULT.json` | `b69fa1ccbb09adfd0cb931f482562b6c39cd516917756afe29b59b89ef892d0a` |
| `build/INPUTS.json` | `e4eb90fb27a33c88950ef6e697931712e4e02beb98770e2d6c6838c25b703195` |
| `build/BUILD-FAILURE.json` | `47fbff256f997ea38d316ef26ad305e52305ba26210b67a14a5429793ebd92b0` |
| `build/objects/BaselineExporter.c`, 396,098 bytes | `afb83c5f9a220d8abf20b3ebc50bdf77f76bed0fe93715569bab8494ef89c2e1` |
| `build/objects/BaselineExporter.o`, 323,361 bytes | `c28ccaacdc58ae345f335c6cfff5f028769d3b5211d9a15b23efa9071a4accf4` |
| `build/objects/BaselineExporter.olean`, 1,382,224 bytes | `e04caea5277a46a76f1d99d635692f7ccc6c9b7c9c463d3d4223383bb7010a34` |

Paths in this table are relative to
`experiments/v5-local-checks/ordinary-baseline-native-build-01`.

Root's new source-only02 selection may reuse those successful exporter outputs
and repair only the known reserved binders/import routing in fresh native
successors. Its new adapter/source delta and exact provenance are reviewed
separately below when stable. This does not convert failed01 into a successful
build or authorize another run before root's new finite selection.

### Fresh native02 source delta

Independently read all three complete no-index diffs and verified their hashes:

| Fresh source | SHA-256 |
|---|---|
| `BaselineArtifactCore02.lean` | `ff34631ed54114c3919c7f3aa50ced634c1e2bf66496a1ca2f8be12da74d9e0f` |
| `BaselineArtifacts02.lean` | `b77d489c2b8aee6551d422fc4f54b46d5ca7e00defb4adcc557e93a8681d287a` |
| `OrdinaryReferenceBase02.lean` | `252bf83fe5353daab8169a21310eeef1e4b6eed2617e8209d99a260a98192635` |

Disposition: **PASS for this narrow source correction**. The only body changes
rename three local `meta` binders and their uses to `metadata`: two in the core,
one in the matcher. The collector/matcher imports now name Core02. Namespaces,
protocol schemas, limits, semantic matching, projection counters and all other
logic are unchanged. The exact predecessor files remain unchanged.

The report-source compatibility review against matcher5120d6bb consequently
transfers to matcher02's identical request/report protocol; this is a direct
source-delta fact, not a second independent executed test. Compile success of
the corrected modules remains unestablished until a separately selected actual
build. Reuse of the exporter's successful01 object/code-generation products is
appropriate only with explicit pins and the preserved failed-run provenance.

### Fresh build02 adapter and selector clearance

**PASS for the narrow source-engineering boundary**, after one small provenance
correction. Independently read the complete01-to02 adapter/selector diffs and
checked their final identities; no adapter was imported or executed here.

| Fresh source | SHA-256 |
|---|---|
| `build_native02.py` | `dd54994b523fe9e8ef0d2f524cfdac228c33f7fae42a907844fb13ce6185e054` |
| `select_native_build02.py` | `281325b7d4b3b1b111ad605b925eb7ad6b34b680dd15c3f62b0ee0c7ae4fadc6` |

The new adapter authenticates the saved01 result, failure, logs, inputs and
selection; requires the exact clean-failed outcome and completed phase sequence
`exporter-codegen/0`, `exporter-object/0`, `core-codegen/1`; binds the original,
saved and staged exporter source; and requires unchanged named runtime/shared
inputs from the earlier build. It copies only the three exactly pinned exporter
outputs, without repeating either successful exporter compilation stage. The
three native02 modules compile in dependency order, followed by three links:
nine new commands, twelve new outputs and three reused outputs, fifteen total.
Only the new02 output root is written; failed01 remains preserved and charged.

The first reviewed02 draft repinned all output files after compilation without
equating the copied exporter subset to its original expected pins. That could
permit inconsistent `all_candidate_outputs` and `reused_exporter_outputs`
claims if a later command changed a copied artifact. The final adapter now
requires every copied exporter pin in the observed output map to equal its
authenticated predecessor pin before writing `NATIVE-OUTPUTS.json`; the
existing final rehash preserves that equality through the receipt checks. This
closes the finding without expanding the build scope.

The unchanged 256-MiB generated-directory ceiling already includes these three
copied files, so the spool reservation does not omit their bytes and must not
double-count them as an additional ceiling. The unchanged finite outer Job
envelope, cooperative limits, exact source snapshots and final input/output
checks retain the qualifications above. Runtime pins are still named pins,
not a hermetic build guarantee. The selector only emits a fresh selection.

This clearance authorizes no run by the reviewer. Root must separately select
the exact final hashes, require a clean actual02 Job result and inspect saved
outputs before treating any candidate as built. It does not establish native
fixture behavior, reference registration, ordinary delta use or v5 completion.

### Build02 saved failure and surgical native03 source correction

Read-only saved-result/log inspection confirms build02 also failed cleanly:
only `BaselineArtifactCore02-codegen` ran, exiting one at source251:53 with
`unexpected identifier; expected '}'`. Its multiline record fields lacked
explicit separators and were not aligned for layout-based separation. No new
core/collector/matcher output or executable exists; the output directory has
only the three copied exporter files. `BUILD.json` and `NATIVE-OUTPUTS.json`
are absent. This failure does not invalidate the previously successful exporter
compilation or refund either attempt's cost.

Saved selection hash is
`4b9eb52f3af4169dc6abb810932939b4c3311056ec9aa2e2bcf79967b79f686b`,
outer result hash
`9fe080047f4173805d4adaf97357ad990196d257545a51277058258eb9fae935`,
and failure receipt hash
`cda5dda914c8cca7ef3964c59ae6fb4aa07cec3530ffe121133d0b0de02954af`.
Actual closure has child exit one, zero active/terminated Job processes, child
reaped, Job closed and no cleanup errors. Wall time was 3.9635374 seconds;
known CPU was 2.453125 Job plus 1.03125 wrapper, or 3.484375 seconds total.
Peak private Job commit was 600,018,944 bytes. This addendum reviews the saved
failure and new source delta, not another full predecessor input audit.

Root created three fresh03 sources and retained all used02 bytes. Complete
02-to03 diffs and actual file hashes establish **PASS for the narrow native
source correction**:

| Fresh source | SHA-256 |
|---|---|
| `BaselineArtifactCore03.lean` | `d61da3c19355c33c93ad3fbd1134f474af9b1d7838db0ee22a49b30459463fc9` |
| `BaselineArtifacts03.lean` | `decd274b5db94c6b04bd54a6297a4b3811c885b5bcd2028a6428edbdddc1db56` |
| `OrdinaryReferenceBase03.lean` | `4405197c58fd1861f4fed8b9e9a07c5cb93745fe8a24d2ced2b8190f43dea840` |

The delta is four explicit field-separator commas in the core, five in the
matcher, and the two Core03 imports. Field values, namespaces, bounds, semantic
matching and request/report schemas are unchanged. This source-level correction
does not establish successful compilation; root's separately selected build03
must supply that evidence. No compiler, candidate or owner ran in this review.

### Build03 adapter/selector changed-lines clearance

**PASS for the narrow03 source-engineering delta.** Complete02-to03 diffs and
read-only hashes establish:

| Fresh source | SHA-256 |
|---|---|
| `build_native03.py` | `3afcbbce19779907e6ecd14bd1cbc79f9c5d9ccf34c05cea6f4915758d03defe` |
| `select_native_build03.py` | `638df1b12c23ed93e7f95079e950b0033ff860b19556b8da8b09f5f5879ae075` |

Changes only route the three new native modules, two collector/matcher
executables, adapter/selector snapshots and fresh output root to03, plus the
diagnostic prefix. The retained exporter is still copied directly from its
authenticated successful01 stages, not from02's copies. Its exact provenance
checks and final copied-exporter equality are unchanged. Nine commands, fifteen
total candidate files, source/runtime pins and all finite limits are unchanged.
The failed02 evidence above remains separately preserved;03 neither depends on
a02-generated mathematical artifact nor relabels02 as successful. This is not a
repeat whole01/02 review, and no selector, build or fixture was executed here.
Root alone selects any fresh03 operation and evaluates its actual clean outcome.

**Build04 narrow delta, 2026-10-24: PASS (source only).** Saved03 result/logs confirm another clean core syntax failure at251:54 (3.9713027wall seconds, 3.359375known Job+wrapper CPU seconds); preserve it. Native04 changes only three record first-field line breaks/alignment and two Core04 imports, with no value/namespace/semantic delta: core `ed43a59caa09011df458a6085f57653e174884f3bdd7a523dbd3b79df22e3353`, wrapper `2007380be2fdd8cede56f868425c851a7c2fe9256926ff09855edfa27431af77`, matcher `c7c0636b7252a3f62d277bb7497a14f7686b7ec61fdd722d6bb05dbba0ca5b19`. Adapter `6e63490a08da8edfd5a3e87c8cbf27c5200593576cd9a0b892d8e7e25a2853cf` and selector `f189f9869d382e845a1368c29f35e81b5b3c18b3cecfff32ba3c49c933d1b75e` change03 names/routing/diagnostics to04 only; exporter01 reuse/final equality, commands and bounds remain unchanged. Complete changed diffs and these five hashes checked; no prior-input re-audit or runtime performed.

### Build04 actual saved-outcome audit

**PASS: the three exact candidates were built, not installed or adopted.**
Saved-only inspection and independent file hashing verify all54 selected
input/runtime pins against selection/INPUTS, all8 original/source snapshots,
3 staged native sources,10 shared copies, and the exact15-file output census.
All15 actual output pins agree with BUILD and NATIVE-OUTPUTS. Twelve are new;
the other3 are unchanged exporter01 `.c/.o/.olean` files, checked directly
against01 as well as both receipt maps. No reused file is counted as new.

The9 zero-exit commands have the selected order and agree between stdout and
receipt. Each link uses exactly the five shared objects plus exporter alone,
core04/collector04, or core04/matcher04 respectively. The final stdout summary
matches9 commands/12 new/3 reused/15 total. Stderr is empty; no failure receipt
exists. The actual spool before BUILD is25,122,899 bytes, matching its receipt.

The actual outer result is `COMMAND_EXITED_ZERO_AND_CLOSED`, child0, zero
active/terminated processes, direct child reaped, Job closed, no cleanup errors
or termination request. Wall time is9.8305905 seconds; known CPU is7.171875 Job
plus1.046875 wrapper, totaling8.21875 seconds. Peak Job private commit is
631,877,632 bytes. Prior01/02/03 failures and costs remain separate and preserved.

Paths below are relative to
`experiments/v5-local-checks/ordinary-baseline-native-build-04`.

| Evidence | SHA-256 |
|---|---|
| `selection.json` | `0de88c987ff006d5f7a070996c3d01f7aa34cd7d6f880e180c3e51e47d213ac4` |
| `RESULT.json` | `f997200b7abb83d13a0682261858b576d9938031c0368292bc5b5ec2b17632ec` |
| `build/BUILD.json` | `5811c38b872b094c284579241d9c90d463432ac35dc96d0ae6008b5b7df76213` |
| `build/INPUTS.json` | `0faf678bdb29ff1f2808fa118f1a52afd7466f577e139e85cddb2aa09b11bb58` |
| `build/NATIVE-OUTPUTS.json` (exact full15-output map) | `a9d4187008149aeaa1ea9aeff8832ccd84d173c2b3ecfdd03ed0d28037204f0f` |

| Candidate under `build/objects/` | Bytes | SHA-256 |
|---|---:|---|
| `BaselineExporter.exe` | 809,472 | `2adcffad1ad4967f093e1acc6c31295c2519e7f9cbf35d04bee37d8580cc3c4f` |
| `BaselineArtifacts04.exe` | 347,136 | `d07197ea63c0b4bd92f3743ae1fe09c1251e1b73d01900c9b210c6920490795e` |
| `OrdinaryReferenceBase04.exe` | 955,392 | `7dad842f297df109f5557088552e8b6a65eaf47fb2201efbba4528e24dfad196` |

These are build identities, not evidence of actual export/collection/matching,
reference registration, mathematical admission, package adoption or completed
v5. This reviewer ran no compiler, candidate, owner or test; future execution
requires root's separate exact selection. Named runtime pins retain the stated
nonhermetic toolchain premise.
