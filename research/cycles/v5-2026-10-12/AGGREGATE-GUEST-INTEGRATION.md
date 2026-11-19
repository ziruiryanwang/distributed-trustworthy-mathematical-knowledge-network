# Integrating the economical aggregate guest

Root source-only decision, 2026-10-12. No Cargo command, guest build, image,
execution, proving or profile adoption is selected here. Native integration is
being implemented separately under PROOF-VALIDATION-INTEGRATION.md.

## Central obstacle and minimum consequence

The next scalability boundary is a genuine aggregate certificate and a public
selected-member import, not another test of the old network. Native deltas are
already useful but retain all unsealed proof witnesses and finite ancestry caps.
They cannot alone support indefinitely deep reuse by fresh agents.

The original aggregate Cargo manifest still selects the original checker. A
native link against optimized libraries does not change that Cargo dependency.
The fresh three-manifest overlay at software/v5/aggregate_guest explicitly
selects the validation-only checker root, unchanged module relation, exact-J
aggregate-v2 library and unchanged guest entry. Existing source manifests and
all previous images/receipts remain untouched. All dependencies retain their
existing version requirements and features; no registry update is intended.

The overlay is NOT a portable release: it deliberately retains the existing
absolute SDK source path. Reproducible vendoring/rights are still separate open
release work. The checker package's Apache license is its upstream license,
not a license decision for the whole commons.

## Resolve once, validate the changed graph, then compile

Reuse the adopted guest-build-05 lock and external package resolution as the
baseline. A future exact lock transformation adds only the aggregate package
record (depending on dmkn-module-relation, serde_json, risc0-zkvm); unchanged
registry/source/checksum/package records remain equal. Package source locations
for the checker and module change to the fresh overlays. Development targets
and dependencies are not selected by the production guest command.

The fresh offline Cargo unit graph must be compared structurally, not by a
coincidental package count. Required changes are the relocated checker/module
library roots, removal of the old module binary as root, and the new aggregate
library/binary and their explicit dependency edges. All reachable external
package versions, features, targets, profiles and dependency edges must match
the retained production graph after normalizing source/cache paths. Exact
serde_json default/std features remain part of Value identity. The workspace
uses resolver2 explicitly, the existing edition2021 production default.

An implementation owner must inspect actual graph metadata before pinning a
mechanical transform; these paragraphs do not authorize accepting an arbitrary
graph difference. In particular, Cargo build-std and host build-script units
are dependencies too. Do not reuse Windows rlibs for RV32 or manually infer
compiler flags from the TOML profiles. Reuse unchanged dependencies only with
compiler/target/feature/profile identity established; a fresh isolated full
build is the fallback if safe cache reuse costs more engineering than it saves.

Retained guest-build-05 completed in 434.6597575 wall seconds. This is a cost
reference, not a predicted new build duration or permission to repeat it. An
additional speculative compiler/caching experiment is not justified merely to
avoid a single bounded build. New native success remains a prerequisite to the
optimized guest selection, not proof that Cargo selected the intended sources.

## One execution, not a disposable benchmark followed by a replay

Once native integration and fresh host/guest builds pass, one finite aggregate
snapshot can answer the unresolved cost question. The reviewed aggregate host
retains that same completed execution for later proving and offers bounded
same-run diagnostics. Do not first screen successfully without retaining it.

Use the retained ordinary-source two-delta mathematics and genuine base receipt,
changing only the actual aggregate image field/framing needed by the new image.
Its proof-validity endpoint has already been established natively. Successful
guest execution must reproduce the expected exact journals, header, assumptions
and membership commitments under that image, not invent a more convenient
synthetic workload. Actual image adoption, input and resource selection are
future separately reviewed decisions. No limit is raised automatically.

The two optimizations remove redundant work by source refinement; they do not
prove a particular whole-program speedup. If a finite run fails, preserve its
completed segments and diagnostics and use those to choose the next change.
No blind budget increase, full proof launch or same-input rerun follows failure.

## Growth and continuation decision

Let C_native(W) include all currently unsealed witness acquisition/checking;
let C_member include genuine aggregate verification, the selected exact-J
membership path, interface openings and demanded semantics. For a fixed
profile, fixed cache state and service horizon, sealing can improve resource
cost only when the saved per-recipient costs exceed additional certification,
publication, retention, repair and failed-work costs in aggregate. Use the
three explicit comparators in GROWTH-WORKLOAD.md; do not give an ordinary
shared-library baseline unnecessary ancestry duplication.

There is a second independent benefit: a module with a certified frontier can
be reused by a fresh agent whose resource cap is too small for its unsealed
history. That is a resource-bounded capability claim, even if total network
CPU rises. It must not be relabeled a full-cost saving. Report feasibility and
economic benefit separately. Neither implies mathematical novelty or future
demand, and exact-J variants never count as new knowledge.

The next expensive investment is justified only by a bounded execution and an
explicit supported use/cost region, or by a clearly labeled functional release
requirement. A demonstration certificate needed to test the latter may be
worth producing without pretending that the small demonstration amortizes it.

## Concrete source handoff: exact-warrant optimized guest

Implementation owner: `v5_base_actual_audit`, 2026-10-12. This section appends
the completed source handoff without changing the root decision above. Root
owns exact runtime selection, launch and adoption; independent assurance owns
review. No Cargo graph/build, guest execution, image assembly, proof or Git
operation was performed by this implementation owner.

The source-only artifacts under `software/v5/aggregate_guest/` are:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `graph.py` | 7,934 | `2bbab886704aaa72ba4c6415b4187a1f5b0e699b6f3d61c512f16ea0d425af31` |
| `build.py` | 16,041 | `4e986f7d2b6d6560b81e98a5d490d9488795ef64111300d12cf264e036c60038` |
| `BUILD-PROPOSAL.json` | See exact file | `e10b3a5d5f32718583e41986d7b46dd6bb514867f31f5c3fc9cfbe0bf3978729` |

The proposal is deliberately inert:
`authorizes_guest_build_and_owned_telemetry_cleanup` is `false`. It binds the
38 source files and the adopted native differential result
`proof-validation-native-compare-01/RESULT.json` (6,071 bytes,
`f60945682fd510c837a26c6bc1703fe8065e8e1a2a301d675e9f869d44384d33`).
The controller requires an independently reviewed root selection with explicit
authorization; the proposal alone cannot launch it. Re-reading this pin was
not another native comparison or another actual-result audit.

### Graph and lock transformation

Read-only inspection of retained `guest-build-05/UNIT-GRAPH.json` found 296
units, root index 79, module library index 78 and checker index 140. These
three project units share the RV32 release build profile: optimization 3,
overflow checking enabled, panic abort and no project features. The old guest
binary has direct module, checker, RISC Zero, serde and serde_json dependencies,
plus build-std dependencies marked `noprelude`.

`repin_lock` preserves the parsed contents of every retained lock record and
adds exactly the local `dmkn-aggregate-claim-relation` 0.2.0 package, depending
on the module, RISC Zero and serde_json. It does not alter an external package
version, source, checksum or dependency record. Only the fresh lock copy is
written by a selected run; the retained lock remains unchanged.

The expected unit-graph transformation:

1. Relocates the unchanged module library to its fresh manifest overlay.
2. Relocates the checker to the optimized thin library root already used in
   the adopted native integration.
3. Replaces the old module binary root with the unchanged aggregate guest
   entry and its explicit module/RISC Zero/serde_json dependencies.
4. Adds the exact-warrant aggregate-v2 library and the root-to-library edge.
5. Preserves every external and build-std unit, profile, feature and edge.

The expected count is 297 units, but the count is not the acceptance rule.
`verify_delta` compares the complete graph after replacing dependency indices
with full unit identities. Only the retained/fresh Cargo-cache locations are
normalized; fresh project paths are explicit parts of the expected graph.
Every serde_json 1.0.151 unit must retain exactly `default` and `std` features.
This matters because feature-dependent JSON value representation belongs to
the pinned native/guest correspondence boundary.

The actual new Cargo graph has not been observed by this implementation owner.
In particular, no statement here asserts that Cargo will produce the predicted
library target metadata or accept the minimally changed lock. An unexpected
graph or lock requirement must stop before compilation and be diagnosed from
retained output; the controller must not relax graph equality automatically.

### Fresh build closure and finite envelope

The source closure contains the prior 32 Rust files from the adopted optimized
native source map, the unchanged aggregate guest entry, the three root-authored
overlay manifests, and the two new Python adapters: 38 files total. The prior
native driver is retained in the source census but is not a Cargo target. The
fresh project snapshot is `RUN/project/software/v5/`; production Cargo selects
only the intended checker/module/aggregate libraries and aggregate guest binary.

The controller reuses the pinned `general-checker-guest-03/common03.py` recipe,
retained offline registry seed and build-std inputs. It creates a fresh target
directory: no Windows rlib is reused for RV32 and no old target-cache identity
is assumed. Its two worker commands are an offline locked Cargo unit graph,
then the same production build with JSON artifact reporting. The retained
target, build-std list, compiler-builtins feature and release flags are kept.
The build can pass only after exactly one selected RV32 executable and the
expected SDK startup symbols are identified.

The proposed envelope is 1,800 aggregate worker CPU seconds, 1,800 total wall
seconds, 4,096 MiB and eight active processes, with a 16 GiB combined working
envelope. Controller CPU is separately bounded at 180 seconds. The retained
preparation census and inherited shared reserves (3 GiB working bytes, 192 MiB
archives and 30,000 entries) remain charged. This is not authorization to
overlap other memory-heavy jobs; root schedules against actual free resources.

Pins are rechecked before, between and after worker commands. Finalization
failure produces an overriding failure marker; a saved earlier PASS is not
enough if that marker exists. The build excludes image assembly, guest
execution, receipt verification, proving, host backend compilation and network
fetch commands. Even a passing ELF build would establish none of those later
outcomes. The optimized native comparison supplies an implementation
prerequisite, not an RV32 speedup measurement or a new checker-to-Lean theorem.

### Remaining handoff boundary

Root reported exact selection `011ac45c` held for independent review when this
source checkpoint was appended. The source owner must not edit those proposed
bytes while selection/review is pending. Any requested correction first needs
confirmation that the affected source has not been launched or used. Root's
host-link preparation is a separate assignment and is not duplicated here.

After review and any selected build, actual graph, ELF and closure adoption are
still required. Image adoption, one retained execution, economical certification
and real public selected-member import remain later central decisions. Full v5
release, useful-growth and deployment obligations are not closed by this handoff.

## Subsequent source-only image assembly seam

Root subsequently reported independent clearance of exact guest selection
`011ac45c` and launch as session `60734`, after the separately adopted host link
exited. The graph/build/manifests/proposal above are now used and must not be
edited. The implementation owner's next assignment is only a fresh assembly
adapter, not another compiler run or a claim that the live guest build passed.

`software/v5/aggregate_guest/assemble.py` is now source-complete: 7,814 bytes,
SHA-256 `4b9f0b54b44fcd34d239341b9e6e2081510bf9fa2a74b23202a7fa8476f34b0f`.
It adapts the retained module assembly seam; the old file and all previously
assembled images remain unchanged. Independent source review was requested.

The adapter takes only a future actual aggregate guest result, its exact
SHA-256, and a fresh output directory. It requires:

- The aggregate build's exact result schema and
  `PASS_OPTIMIZED_EXACT_WARRANT_AGGREGATE_GUEST_BUILD_ONLY`, with zero active
  processes and zero recorded guest/proof/image/network/host-build operations.
- Exactly the two successful, cleanly closed graph/build commands selected by
  the new controller.
- A matching terminal `aggregate-guest-build-NN-attempt.json`, with no
  `FINALIZATION-FAILED.json` that overrides the saved result.
- That build's exact `release/dmkn-aggregate-claim-guest` ELF, not an old module
  or collection ELF and not an arbitrary artifact beside a failed build.

Only the existing pinned `driver-build-04` assembler and the exact 58,736-byte
v1compat kernel are reused. The sole child command is `assemble USER KERNEL
FRESH_IMAGE`; no new backend/compiler is built. All inputs and terminal state
are rebound before and after. The output is `aggregate_image.bin`; its file
hash and the assembler's actual cryptographic image ID are recorded separately.
A successful output would be `PASS_NEW_AGGREGATE_IMAGE_ASSEMBLY_ONLY`, expressly
not mathematical admission, guest execution or receipt production.

Invocation remains subject to root's future exact selection inside the existing
bounded local-check Job. As with the retained assembly plan, a suitable proposed
outer ceiling is 120 CPU/120 wall seconds, 1,024 MiB and two active processes;
the single assembler child has a 60-second timeout. Root must pin the actual
successful build RESULT, terminal marker, ELF, adapter, retained assembler
result/executable, kernel and supervision/runtime before launching. No proposed
ceiling here renews another run or substitutes for that selection. No actual
guest result, image bytes or image ID was invented during this source work.

Independent assurance subsequently cleared assembly source `4b9f0b54` for one
root-selected bounded outer Job. Its inner captured-output size check is not
independent hostile-output or resource supervision; the outer Job and exact
input/output pins remain necessary. Source clearance is not an actual assembly
outcome. The implementation owner sent the exact handoff to root and made no
runtime launch.

## Actual graph refusal: exact four lexical paths, no compile

Root reported session `60734` terminal with exit 1. The preserved failed result
is `aggregate-guest-build-01/RESULT.json`, SHA-256
`231c94114e625a59371fdb1208aa7ae2838c9c35c9b8877b80bead4e7ad7e0ac`.
Its sole successful worker was the offline graph command: 5.359375 CPU seconds,
19.5355971 wall seconds, zero exit, no cleanup error and zero active processes.
The controller then raised `UNSELECTED_FULL_AGGREGATE_GUEST_GRAPH_DELTA` before
any compile. Total recorded cost was 146.420616 wall and 45.5625 controller CPU
seconds, in addition to that worker CPU. The failed outcome remains FAIL.

The saved graph is `commands/offline-aggregate-graph/stdout.txt`: 342,397 bytes,
SHA-256 `2cc441345c1cf3cc16e9dd21cca1bf2130319dbfa1124ad3ddb1d6507f2f4609`.
Read-only JSON comparison found 297 units and root 79. There are exactly four
different `target.src_path` fields, all in the intended local source units.
Let `P` be the failed run's `project/software/v5` directory. The paths are:

| Unit | Expected suffix under P | Actual Cargo suffix under P |
|---|---|---|
| Module library | `modules/receipt/src/lib.rs` | `aggregate_guest/module/../../modules/receipt/src/lib.rs` |
| Checker library | `modules/native/proof_validation/lib.rs` | `aggregate_guest/checker/../../modules/native/proof_validation/lib.rs` |
| Aggregate binary | `aggregate/main.rs` | `aggregate_guest/../aggregate/main.rs` |
| Aggregate library | `aggregate_claims/lib.rs` | `aggregate_guest/../aggregate_claims/lib.rs` |

Cargo retains the lexical relative segments from the manifest. The expected
transform had instead emitted their resolved spelling. No mathematical source
or compiler feature mismatch was found. Comparing full canonical graph
identities and dependency edges after correcting exactly those four expected
fields gives equality, including roots, all target metadata, profiles, features
and external/build-std edges. This diagnosis used saved JSON data only: no Cargo,
candidate application, compiler or test campaign was executed. It does not
retroactively change the failed controller outcome or establish an ELF.

Root adopted the minimum fresh source successor: a compile-only controller
that binds this graph and the unchanged failed-run project/lock, applies only
the four literal expected-field corrections, and retains whole-graph equality.
It must not rerun the successful graph command or generically normalize paths.
A fresh target and private byte-identical registry seed preserve the failed
cache/evidence; toolchain, SDK, resolution, features and compile flags remain
bound. The remaining original limits are conservatively 1,794 worker CPU,
134 controller CPU and 1,653 wall seconds, with the same memory/process/disk
ceilings. No blind renewal of the original 1,800-second envelope is selected.

The compile successor must report its own one-command result and explicit
predecessor graph binding. The assembly adapter must later recognize that
distinct lineage, not pretend one new command is two new successful commands.

### Fresh compile-only implementation handoff

`software/v5/aggregate_guest/compile_only.py` is source-complete, 17,854 bytes,
SHA-256 `d8e4bd4c9df8ac3fc8e8b1a4f5eb62333ce97817e954fcd08f1e3e687fc35c0b`.
The accompanying `COMPILE-PROPOSAL.json` is inert (authorization `false`). Root
and independent assurance received these exact bytes; no compile was launched
by the source owner. Used graph/build/manifests and failed evidence stay frozen.

The fresh controller imports the pinned used graph/build helpers without
calling their main functions. Its `corrected_graph` calls the original expected
transform for the retained old graph and failed-run source root, changes only
the four exact expected fields listed above, checks each lexical path resolves
to its exact source, then uses the original full canonical-graph comparison.
The serde_json `default`/`std` feature gate is retained. There is no new Cargo
graph command, no generic source-path normalization and no external-edge waiver.

It hard-pins the failed RESULT, SOURCE-MAP, environment profile, exact selection,
saved raw graph and external terminal attempt record. The failed result must
have the exact known gate refusal after one zero-exit, clean graph command.
The reused immutable source map must contain all 38 exact selected source
files plus only the transformed Cargo.lock. Actual project bytes, standard
library/lock, retained SDK/runtime/tools and registry seed are rebound. The
successful native integration/comparison remains bound through the predecessor.

One unchanged offline locked production Cargo compile uses that retained
manifest, a fresh target and a private byte-identical cache seed. Only output
locations change. The proposal conservatively retains 1,794 worker CPU,
134 controller CPU and 1,653 wall seconds; the controller checks these plus
the charged predecessor costs stay within the original 1,800/180/1,800 limits.
Its storage census includes both retained preparation and the failed prefix,
the new allocation and the same inherited shared reserves. Memory, process
and disk ceilings are unchanged.

The explicit new result schema is `DMKN_V5_AGGREGATE_GUEST_COMPILE_RESULT_V1`,
with success `PASS_OPTIMIZED_EXACT_WARRANT_AGGREGATE_GUEST_COMPILE_ONLY`. It
records the failed predecessor RESULT and successful saved graph pins, prior
charges, zero new graph calls and the actual single compile command. ELF,
startup-symbol and finalization-failure gates remain. It is neither a claimed
two-command pass nor an assembly, guest execution or proof result. The existing
unused assembly adapter is deliberately unchanged pending source review of
this new result lineage and root's later exact selection.

### Compile selection and explicit assembly-lineage successor

Independent source review cleared `compile_only.py` `d8e4bd4c`. Root then
reported launch of exact selection `19fef22e` as session `72234`, using the
required `D:\Python314` interpreter. The compile controller, inert proposal
(`3590807f5759c81f651588dd88b84f4216abfc8d973264d61920f2ba02963a4b`)
and selected configuration are now used/frozen. No second copy or compilation
is selected by this note, and no successful compile is presumed while live.

With root's explicit authority to revise the still-unused assembly adapter,
`assemble.py` was changed from source-only lineage `4b9f0b54` to 9,983 bytes,
SHA-256 `a2f804a9e739aacd01d3ec4b864fc209b2f8ea430ece1aeca9b4356b332ce8f2`.
Independent changed-boundary review was requested before any root selection.
This adapter deliberately accepts only the new successful compile-only schema:
one cleanly closed compile and zero new graph calls, with its exact terminal
attempt binding and no overriding finalization-failure marker.

The preserved graph prefix remains explicitly failed as a whole. Its RESULT,
saved successful graph and terminal attempt are pinned independently; the new
successful compile must name exactly those predecessor result/graph pins.
The prefix must have the known graph-comparison failure after its sole cleanly
closed, zero-exit graph command. Those records are rebound before and after
assembly. Thus the adapter recognizes one successful graph command followed
by a failed controller, plus a distinct successful compile; it never promotes
the predecessor FAIL to PASS or invents two commands in the new run. Existing
assembler/kernel/image-ID checks and the outer bounded-Job requirement remain.

Root caught an invocation mismatch before this unused adapter was selected:
the existing `__file__ == canonical SOURCE` guard would reject the intended
immutable `Run-V5-Check.py` source snapshot. Root explicitly authorized a narrow
correction. Current `assemble.py` is 10,305 bytes, SHA-256
`9f4de50bd35d13809eaa7a5340edcd15b7784e6be102cff3e7f7bb577bebe888`.
It accepts only the exact six-component path under `experiments/v5-local-checks`:
`<operation>/sources/software/v5/aggregate_guest/assemble.py`, with a bounded
lowercase alphanumeric/hyphen operation name. Canonical working directory and
isolated Python flags remain mandatory; original-source invocation is refused.
The outer selection still supplies the exact source hash and all artifact pins.
The previously cleared compile-lineage checks are unchanged; independent review
was requested specifically for this additional snapshot-invocation seam.

## Compile prefix completed; overall controller-resource failure preserved

Root reported session `72234` terminal and reaped. Read-only inspection found:

- The sole Cargo compile exited zero, without cleanup errors; its final Job had
  zero active/terminated processes. Recorded worker CPU was 222.640625 seconds
  and command wall time 197.9885544 seconds.
- The saved RESULT is
  `81cce68d9b20f22b12d12d5d698084eb8eb101493de71c6e35cd6acb7b44f47a`.
  It records an ELF and map after the selected artifact/startup checks, and no
  final input-rebinding error. It also records 149.640625 controller CPU seconds,
  exceeding the selected remaining 134-second controller allowance.
- The overriding `FINALIZATION-FAILED.json`, SHA-256
  `d0d6d8980c492d43a8927825aa153271543fa18d960305db5bde1e51c323dd54`,
  correctly establishes **FAIL_FINALIZATION**, with
  `overrides_result_and_attempt: true` and `REMAINING_TOTAL_ENVELOPE`.
  The saved raw PASS and attempt marker cannot override that failure.
- The retained user ELF is 1,682,292 bytes,
  `8aa35bf0a3ab57ef1caea04cceaae9659fd6c994009a1abad154df8dcd6d5868`.
  The retained map is 2,614,124 bytes,
  `2292e7fa3340775db8626529e1e0fd7f743504991afc3c494006b78dc1c9f3b7`.
  Neither is adopted for assembly by this note.

The resource failure does not itself show a compiler or mathematical source
defect. Equally, an apparently intact ELF does not erase the failed operation.
The existing assembly adapter must still reject this unadopted failed lineage.
No compile retry, image assembly or guest execution was performed by this
source owner. Independent assurance owns the actual sequence/closure audit.

### Minimum fresh artifact revalidation, not a renewed compilation

Root requested a principle design before deciding any new small allocation.
The minimum candidate is a read-only artifact-validation operation with its
own fresh output and explicit budget, not a larger allowance for the failed
controller and not another compile. Its input scope is:

1. Exact failed compile RESULT, overriding failure marker, saved attempt,
   selected configuration and used controller source.
2. The actual compiler output/log pins, `ARTIFACT.json`
   (`dc3a4f79e1006bf45d8355829486ee0b2bb019bd4fd12cf45fb0aec37cfc5904`),
   SOURCE-MAP (`75c710e3ee13f63cb6ef44da8656caa53c300bf649317d2b5669d8b9cde06ce0`),
   and GRAPH-COMPARISON
   (`a7f5ea2fe059e6a57a6aaad48e616986267afe2b7c8a8c60de3194e2b010d458`).
3. The already bound successful predecessor graph, corrected four-field
   comparison and all 38 retained source files plus their exact Cargo.lock.
4. The exact current user ELF and linker-map bytes named by that completed
   compile prefix, checked against all three agreeing evidence references.
5. The independently adopted source/compiler/SDK provenance records. Because
   this operation executes no compiler or SDK, it should reuse that audited
   provenance by exact record pins rather than recursively rehashing whole
   target, Cargo-home or SDK trees and generating another expensive census.

This preserves all source/artifact bindings while checking the decision-changing
boundary: whether these exact retained bytes are still the outputs of the
already audited successful compiler prefix. A new source/ELF mismatch or any
unresolved prior provenance failure refuses adoption; it is not repaired by
changing stored hashes. Distinct policy approval of the artifact is required.

If root selects and independently adopts it, the new status should be
`PASS_REVALIDATED_AGGREGATE_GUEST_ARTIFACT_ONLY`, explicitly retaining
`old_failure_preserved: true`, `prior_budget_met: false`, and zero new compile,
graph, assembly, guest or proof calls. It must never claim the predecessor
run met its budget or change its existing RESULT/override/attempt. Its own
small deadline/output checks should bracket the bounded work, including final
report handling, without another recursive filesystem census.

The two existing attempts already record 228 worker CPU seconds in total and
195.203125 controller CPU seconds. The latter exceeds the original 180-second
controller allocation; neither prior charge disappears after a new adoption.
The records exclude final reporting/exit tails, so these numbers must keep
that qualification rather than claiming an all-inclusive total. New validation
and any later assembly receive separate charges under explicit fresh authority.

An assembly successor would consume the explicit new artifact-adoption record
and the preserved failed lineage. Simply removing its failure-marker guard,
renaming the old result, or passing raw `81cce68d` as a successful build is not
the proposed path. No revalidation helper or fresh budget is authorized by this
principle note alone; root decides after the independent failure audit.

### Root-selected source implementation of bounded artifact adoption

Root adopted the narrow implementation scope and fresh outer envelope of
30 CPU/60 wall seconds, 512 MiB and two processes, with no compiler, target
census or SDK recrawl. `validate_artifact.py` is 13,843 bytes, SHA-256
`715733a37e150d307a99008970ea26fca84f5234beba17e4147577d58ed0f7c4`.
`ARTIFACT-VALIDATION-PROPOSAL.json` records that small envelope with execution
authorization `false`; root alone creates a runnable selection.

Independent source review cleared these validator bytes. The helper reads and
rebinds 56 exact named files: 12 evidence records, the 39-file project/lock,
the used controller, two compiler logs, ELF and map. It checks actual command
arguments, zero-exit/closed worker, Cargo's one `build-finished: true` and exact
binary artifact, agreed source/ELF/map lineage, ELF load headers and existing
startup symbols. Previously audited compiler/SDK provenance is reused, not
recrawled or rebuilt. Internal 24 CPU/45 wall margins and an overriding failure
marker protect its small report-finalization boundary inside the outer Job.
Its new artifact-only PASS explicitly retains the original resource failure
and all recorded predecessor charges. No validator execution was performed by
the implementation owner.

The still-unused assembly adapter was correspondingly revised to 12,602 bytes,
SHA-256 `61587d9a15a093c25b89f3e7d76439011c39831cbca8d19d986cd45db5426750`.
Its input is now `--artifact-validation ABSOLUTE_RESULT` plus
`--artifact-validation-sha256 EXACT_HASH` and `--output FRESH_DIRECTORY`.
Raw failed build evidence alone is not accepted. It requires the distinct
successful artifact-validation record, no validation finalization failure,
exact compile-result/artifact equality and the original exact overriding
compile failure marker **still present**. All are rebound before and after
the unchanged sole assembler/kernel call. The old failure is explicit in its
COMMAND/result, not suppressed, renamed or accepted as a budget pass. Separate
changed-boundary review was requested before root assembly selection.
